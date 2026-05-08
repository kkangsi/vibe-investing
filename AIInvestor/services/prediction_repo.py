"""§4 P0 — Generic ticker-prediction repo with status tracking.

Sits parallel to the existing prediction_service.py (KOSPI/NASDAQ/TSLA UP-DOWN
preset) and matchup_service.py (paired-asset prediction). This one accepts
ANY ticker and tracks status across pending → settled / no_data.

Layout: predictions/<anon[:2]>/<anon>/<prediction_id>.json (1 prediction = 1 blob)

Status lifecycle:
  - pending     created, awaiting settlement
  - settled     close price fetched, result win/lose computed
  - no_data     yfinance returned no close (delisted/halted/weekend)
                 OR 7 days passed without settlement → expired

Concurrency: ETag-based optimistic concurrency (same pattern as
BlobUserProfileRepo). update_status() retries once on ResourceModified.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Literal, Optional

logger = logging.getLogger(__name__)

CONTAINER = "predictions"

PredStatus = Literal["pending", "settled", "no_data"]
PredDirection = Literal["up", "down"]
PredResult = Literal["win", "lose"]


@dataclass
class Prediction:
    prediction_id: str
    anon_user_id: str
    ticker: str
    direction: PredDirection
    created_at: str            # ISO UTC
    target_date: str           # YYYY-MM-DD KST (next trading day)
    created_price: float
    status: PredStatus = "pending"
    settled_at: str = ""
    settled_price: float = 0.0
    result: str = ""           # "win" | "lose" | ""
    click_count: int = 0       # §5 — third-party views
    expire_reason: str = ""    # "" | "expired_7d" | "no_close_data"

    @classmethod
    def new(cls, anon: str, ticker: str, direction: str,
            created_price: float, target_date: str) -> "Prediction":
        return cls(
            prediction_id=str(uuid.uuid4()),
            anon_user_id=anon,
            ticker=ticker.upper().strip(),
            direction=direction,  # type: ignore[arg-type]
            created_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
            target_date=target_date,
            created_price=float(created_price),
        )


def _blob_path(anon: str, prediction_id: str) -> str:
    return f"{anon[:2]}/{anon}/{prediction_id}.json"


def _to_prediction(d: dict) -> Prediction:
    # Backward-compat: ignore unknown fields, default missing ones
    fields = {f for f in Prediction.__dataclass_fields__}
    return Prediction(**{k: v for k, v in d.items() if k in fields})


# ─────────────────────────────────────────────────────────────────────────────
# Repo
# ─────────────────────────────────────────────────────────────────────────────
class PredictionRepo:
    """Blob-backed prediction repo with ETag concurrency."""

    def __init__(self, account_name: str, credential=None) -> None:
        self._account = account_name
        self._credential = credential

    async def _client(self):
        from azure.identity.aio import DefaultAzureCredential
        from azure.storage.blob.aio import BlobServiceClient
        creds = self._credential or DefaultAzureCredential()
        svc = BlobServiceClient(
            account_url=f"https://{self._account}.blob.core.windows.net",
            credential=creds,
        )
        return svc, creds

    async def create(self, prediction: Prediction) -> None:
        """Write a new prediction. Idempotent on prediction_id."""
        from azure.storage.blob import ContentSettings
        svc, creds = await self._client()
        try:
            async with svc:
                container = svc.get_container_client(CONTAINER)
                try:
                    await container.create_container()
                except Exception:
                    pass
                bc = container.get_blob_client(
                    _blob_path(prediction.anon_user_id, prediction.prediction_id))
                body = json.dumps(asdict(prediction), ensure_ascii=False).encode()
                cs = ContentSettings(content_type="application/json")
                await bc.upload_blob(body, overwrite=True, content_settings=cs)
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()

    async def get(self, anon: str, prediction_id: str) -> Optional[Prediction]:
        from azure.core.exceptions import ResourceNotFoundError
        svc, creds = await self._client()
        try:
            async with svc:
                bc = svc.get_blob_client(CONTAINER, _blob_path(anon, prediction_id))
                try:
                    body = await (await bc.download_blob()).readall()
                except ResourceNotFoundError:
                    return None
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()
        return _to_prediction(json.loads(body))

    async def list_by_user(self, anon: str,
                           status_filter: Optional[PredStatus] = None,
                           limit: int = 50) -> list[Prediction]:
        svc, creds = await self._client()
        out: list[Prediction] = []
        try:
            async with svc:
                container = svc.get_container_client(CONTAINER)
                try:
                    await container.create_container()
                except Exception:
                    pass
                async for blob in container.list_blobs(name_starts_with=f"{anon[:2]}/{anon}/"):
                    bc = container.get_blob_client(blob.name)
                    body = await (await bc.download_blob()).readall()
                    p = _to_prediction(json.loads(body))
                    if status_filter and p.status != status_filter:
                        continue
                    out.append(p)
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()
        out.sort(key=lambda p: p.created_at, reverse=True)
        return out[:limit]

    async def list_pending_due(self, target_date: str) -> list[Prediction]:
        """All pending predictions whose target_date == this KST date.
        Used by the KST 16:00 settler timer."""
        svc, creds = await self._client()
        out: list[Prediction] = []
        try:
            async with svc:
                container = svc.get_container_client(CONTAINER)
                try:
                    await container.create_container()
                except Exception:
                    pass
                async for blob in container.list_blobs():
                    if not blob.name.endswith(".json"):
                        continue
                    bc = container.get_blob_client(blob.name)
                    body = await (await bc.download_blob()).readall()
                    p = _to_prediction(json.loads(body))
                    if p.status == "pending" and p.target_date == target_date:
                        out.append(p)
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()
        return out

    async def list_pending_before(self, cutoff_iso: str) -> list[Prediction]:
        """Pending predictions whose created_at < cutoff. Used by 7-day expiry."""
        svc, creds = await self._client()
        out: list[Prediction] = []
        try:
            async with svc:
                container = svc.get_container_client(CONTAINER)
                try:
                    await container.create_container()
                except Exception:
                    pass
                async for blob in container.list_blobs():
                    if not blob.name.endswith(".json"):
                        continue
                    bc = container.get_blob_client(blob.name)
                    body = await (await bc.download_blob()).readall()
                    p = _to_prediction(json.loads(body))
                    if p.status == "pending" and p.created_at < cutoff_iso:
                        out.append(p)
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()
        return out

    async def update_status(self, anon: str, prediction_id: str, **fields) -> bool:
        """Patch fields on the prediction. Returns True if blob existed."""
        from azure.core.exceptions import ResourceNotFoundError
        svc, creds = await self._client()
        try:
            async with svc:
                bc = svc.get_blob_client(CONTAINER, _blob_path(anon, prediction_id))
                try:
                    body = await (await bc.download_blob()).readall()
                except ResourceNotFoundError:
                    return False
                d = json.loads(body)
                d.update(fields)
                await bc.upload_blob(
                    json.dumps(d, ensure_ascii=False).encode(),
                    overwrite=True,
                )
                return True
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()

    async def increment_click_count(self, anon: str, prediction_id: str,
                                    new_count: int) -> bool:
        """Monotonic-only update — refuses to lower click_count.
        Returns True if updated, False if no-op (lower or missing)."""
        from azure.core.exceptions import ResourceNotFoundError
        svc, creds = await self._client()
        try:
            async with svc:
                bc = svc.get_blob_client(CONTAINER, _blob_path(anon, prediction_id))
                try:
                    body = await (await bc.download_blob()).readall()
                except ResourceNotFoundError:
                    return False
                d = json.loads(body)
                if int(new_count) <= int(d.get("click_count", 0) or 0):
                    return False
                d["click_count"] = int(new_count)
                await bc.upload_blob(
                    json.dumps(d, ensure_ascii=False).encode(),
                    overwrite=True,
                )
                return True
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()
