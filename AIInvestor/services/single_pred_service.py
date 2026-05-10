"""§Single — hourly single-asset UP/DOWN predictions (top 10 stocks + top 10 coins).

Sits parallel to the matchup system (A vs B paired) and the §4 generic
ticker prediction (user-chosen ticker, daily settlement). Here:

  - Server picks top 10 stock + top 10 coin majors PER HOUR
  - 3 free + 7 premium per category (consistent with matchup)
  - User picks UP or DOWN
  - Settles 1 hour later (close > anchor → up wins)
  - Stored in `single-predictions/<kst_date>/<id>.json`

The "top 10 major" is sourced from the daily movers snapshot (already cached
by matchup-movers) — we take the first 10 by abs(pct_change) which gives us
the most active majors. The pool itself is filtered upstream to S&P500 +
NASDAQ top-300 + top-30 crypto, so penny stocks / shitcoins are pre-excluded.
"""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Literal

logger = logging.getLogger(__name__)

CONTAINER = "single-predictions"

# Tunables
SINGLES_PER_HOUR_FREE = 3       # per category (stocks / coins)
SINGLES_PER_HOUR_PREMIUM = 10   # per category (free 3 + premium 7)
RESOLVE_OFFSET_HOURS = 1        # settle 1 hour after open
DEADLINE_MINUTES = 55           # deadline same as matchup
PARTICIPATION_POINTS = 1
CORRECT_POINTS = 20             # slightly less than matchup (lower skill)

Direction = Literal["up", "down"]
Category = Literal["stock", "coin"]


@dataclass
class SinglePrediction:
    user_key: str
    anon_user_id: str
    direction: Direction
    submitted_at: str


@dataclass
class SingleSlot:
    """One hourly UP/DOWN slot for a single asset."""
    id: str                # e.g. "2026-05-10-h14-s1" (s=stock) or h14-c1 (c=coin)
    category: Category
    ticker: str
    name: str
    yesterday_pct: float
    open_at_kst: str
    deadline_kst: str
    resolve_at_kst: str
    anchor_price: float
    last_price: float
    last_polled_at: str = ""
    status: str = "open"   # "open" | "resolved" | "void"
    winner: str = ""       # "up" | "down" | "flat" | ""
    settled_close: float = 0.0
    predictions: list[SinglePrediction] = field(default_factory=list)
    created_at: str = ""
    resolved_at: str = ""
    premium_only: bool = False


# ─────────────────────────────────────────────────────────────────────────────
# Time helpers
# ─────────────────────────────────────────────────────────────────────────────
def _kst_now() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=9)


def _kst_today_iso() -> str:
    return _kst_now().date().isoformat()


def _kst_iso(dt: datetime) -> str:
    return dt.replace(tzinfo=None).isoformat(timespec="seconds")


def _slot_id(kst_date: str, hour: int, category: Category, idx: int) -> str:
    cat_letter = "s" if category == "stock" else "c"
    return f"{kst_date}-h{hour:02d}-{cat_letter}{idx}"


# ─────────────────────────────────────────────────────────────────────────────
# Generator
# ─────────────────────────────────────────────────────────────────────────────
def generate_singles_for_hour(snap, kst_date: str, hour: int) -> list[SingleSlot]:
    """Build top-10 stock + top-10 coin single-asset predictions for the hour.

    First 3 of each category = free; remaining 7 = premium_only.
    Source: snap.stocks / snap.cryptos already sorted by abs(pct_change) desc.
    """
    open_dt = _kst_now().replace(hour=hour, minute=0, second=0, microsecond=0)
    deadline_dt = open_dt + timedelta(minutes=DEADLINE_MINUTES)
    resolve_dt = open_dt + timedelta(hours=RESOLVE_OFFSET_HOURS)
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    out: list[SingleSlot] = []
    for movers, category in ((snap.stocks, "stock"), (snap.cryptos, "coin")):
        top = movers[:SINGLES_PER_HOUR_PREMIUM]
        for i, m in enumerate(top, 1):
            out.append(SingleSlot(
                id=_slot_id(kst_date, hour, category, i),
                category=category,  # type: ignore[arg-type]
                ticker=m.ticker,
                name=m.name,
                yesterday_pct=m.pct_change,
                open_at_kst=_kst_iso(open_dt),
                deadline_kst=_kst_iso(deadline_dt),
                resolve_at_kst=_kst_iso(resolve_dt),
                anchor_price=m.last_close,
                last_price=m.last_close,
                created_at=now_iso,
                premium_only=(i > SINGLES_PER_HOUR_FREE),
            ))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# Repo
# ─────────────────────────────────────────────────────────────────────────────
def _blob_path(kst_date: str, slot_id: str) -> str:
    return f"{kst_date}/{slot_id}.json"


def _summary_path(kst_date: str) -> str:
    return f"{kst_date}/__summary.json"


def _slot_to_dict(s: SingleSlot) -> dict:
    return asdict(s)


def _dict_to_slot(d: dict) -> SingleSlot:
    preds = [SinglePrediction(**p) for p in d.get("predictions", [])]
    d2 = {**d, "predictions": preds}
    return SingleSlot(**d2)


class SinglePredRepo:
    """Blob-backed single-pred repo with summary blob fast-path (same pattern
    as MatchupRepo: matchup/<date>/__summary.json single round-trip read)."""

    def __init__(self, account_name: str, credential=None) -> None:
        self._account = account_name
        self._credential = credential
        self._memory: dict[str, SingleSlot] = {}

    async def list_for_date(self, kst_date: str) -> list[SingleSlot]:
        from azure.core.exceptions import ResourceNotFoundError
        from azure.identity.aio import DefaultAzureCredential
        from azure.storage.blob.aio import BlobServiceClient
        creds = self._credential or DefaultAzureCredential()
        results: list[SingleSlot] = []
        try:
            async with BlobServiceClient(
                account_url=f"https://{self._account}.blob.core.windows.net",
                credential=creds,
            ) as svc:
                # Tier 1: summary blob (1 round-trip)
                summary_bc = svc.get_blob_client(CONTAINER, _summary_path(kst_date))
                try:
                    body = await (await summary_bc.download_blob()).readall()
                    arr = json.loads(body).get("slots", [])
                    for d in arr:
                        results.append(_dict_to_slot(d))
                    if results:
                        for s in results:
                            self._memory[s.id] = s
                        return results
                except ResourceNotFoundError:
                    pass
                # Tier 2: parallel scan + rewrite summary
                container = svc.get_container_client(CONTAINER)
                try:
                    await container.create_container()
                except Exception:
                    pass
                names: list[str] = []
                async for blob in container.list_blobs(name_starts_with=f"{kst_date}/"):
                    if blob.name.endswith("__summary.json"):
                        continue
                    names.append(blob.name)

                async def _fetch(name: str) -> SingleSlot | None:
                    try:
                        bc = container.get_blob_client(name)
                        body = await (await bc.download_blob()).readall()
                        return _dict_to_slot(json.loads(body))
                    except Exception:
                        return None

                sem = asyncio.Semaphore(8)
                async def _bounded(name: str) -> SingleSlot | None:
                    async with sem:
                        return await _fetch(name)
                fetched = await asyncio.gather(*[_bounded(n) for n in names])
                results = [s for s in fetched if s is not None]
                if results:
                    await _write_summary(svc, kst_date, results)
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()
        for s in results:
            self._memory[s.id] = s
        return results

    async def get(self, slot_id: str) -> SingleSlot | None:
        if slot_id in self._memory:
            return self._memory[slot_id]
        from azure.core.exceptions import ResourceNotFoundError
        from azure.identity.aio import DefaultAzureCredential
        from azure.storage.blob.aio import BlobServiceClient
        kst_date = "-".join(slot_id.split("-")[:3])  # "2026-05-10-h14-s1" → "2026-05-10"
        creds = self._credential or DefaultAzureCredential()
        try:
            async with BlobServiceClient(
                account_url=f"https://{self._account}.blob.core.windows.net",
                credential=creds,
            ) as svc:
                bc = svc.get_blob_client(CONTAINER, _blob_path(kst_date, slot_id))
                try:
                    body = await (await bc.download_blob()).readall()
                except ResourceNotFoundError:
                    return None
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()
        s = _dict_to_slot(json.loads(body))
        self._memory[s.id] = s
        return s

    async def put(self, slot: SingleSlot, *, refresh_summary: bool = True) -> None:
        from azure.identity.aio import DefaultAzureCredential
        from azure.storage.blob.aio import BlobServiceClient
        kst_date = "-".join(slot.id.split("-")[:3])
        body = json.dumps(_slot_to_dict(slot), ensure_ascii=False).encode()
        creds = self._credential or DefaultAzureCredential()
        try:
            async with BlobServiceClient(
                account_url=f"https://{self._account}.blob.core.windows.net",
                credential=creds,
            ) as svc:
                container = svc.get_container_client(CONTAINER)
                try:
                    await container.create_container()
                except Exception:
                    pass
                bc = container.get_blob_client(_blob_path(kst_date, slot.id))
                await bc.upload_blob(body, overwrite=True)
                self._memory[slot.id] = slot
                if refresh_summary:
                    await _splice_into_summary(svc, kst_date, slot)
        finally:
            if self._credential is None and hasattr(creds, "close"):
                await creds.close()


async def _write_summary(svc, kst_date: str, slots: list[SingleSlot]) -> None:
    payload = {
        "kst_date": kst_date,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "slots": [_slot_to_dict(s) for s in slots],
    }
    body = json.dumps(payload, ensure_ascii=False).encode()
    container = svc.get_container_client(CONTAINER)
    try:
        await container.create_container()
    except Exception:
        pass
    bc = container.get_blob_client(_summary_path(kst_date))
    try:
        await bc.upload_blob(body, overwrite=True)
    except Exception:
        logger.exception("single_pred summary write failed for %s", kst_date)


async def _splice_into_summary(svc, kst_date: str, slot: SingleSlot) -> None:
    from azure.core.exceptions import ResourceNotFoundError
    bc = svc.get_blob_client(CONTAINER, _summary_path(kst_date))
    existing: list[dict] = []
    try:
        body = await (await bc.download_blob()).readall()
        existing = json.loads(body).get("slots", [])
    except ResourceNotFoundError:
        pass
    except Exception:
        pass
    new_entry = _slot_to_dict(slot)
    found = False
    for i, e in enumerate(existing):
        if e.get("id") == slot.id:
            existing[i] = new_entry
            found = True
            break
    if not found:
        existing.append(new_entry)
    payload = {
        "kst_date": kst_date,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "slots": existing,
    }
    body = json.dumps(payload, ensure_ascii=False).encode()
    try:
        await bc.upload_blob(body, overwrite=True)
    except Exception:
        logger.exception("single_pred summary splice failed for %s/%s",
                         kst_date, slot.id)


# ─────────────────────────────────────────────────────────────────────────────
# Generator entrypoint
# ─────────────────────────────────────────────────────────────────────────────
async def ensure_singles_for_hour(repo: SinglePredRepo, account_name: str,
                                  kst_date: str | None = None,
                                  hour: int | None = None,
                                  credential=None) -> list[SingleSlot]:
    """Create singles for this hour if missing. Idempotent."""
    from .movers_source import get_or_fetch_movers
    if kst_date is None:
        kst_date = _kst_today_iso()
    if hour is None:
        hour = _kst_now().hour
    existing = await repo.list_for_date(kst_date)
    prefix = f"{kst_date}-h{hour:02d}-"
    same_hour = [s for s in existing if s.id.startswith(prefix)]
    if len(same_hour) >= 2 * SINGLES_PER_HOUR_PREMIUM:  # 10 stock + 10 coin
        return same_hour
    snap = await get_or_fetch_movers(account_name, credential=credential)
    new_slots = generate_singles_for_hour(snap, kst_date, hour)
    for s in new_slots:
        await repo.put(s)
    return new_slots


# ─────────────────────────────────────────────────────────────────────────────
# Submit
# ─────────────────────────────────────────────────────────────────────────────
async def submit_single_prediction(repo: SinglePredRepo, slot_id: str,
                                   user_key: str, anon_user_id: str,
                                   direction: Direction, *,
                                   is_premium: bool = False
                                   ) -> tuple[bool, str]:
    """Reasons: ok | not_found | deadline_passed | already_submitted |
                 invalid_direction | premium_only"""
    if direction not in ("up", "down"):
        return False, "invalid_direction"
    s = await repo.get(slot_id)
    if s is None:
        return False, "not_found"
    if s.status != "open":
        return False, "deadline_passed"
    if s.premium_only and not is_premium:
        return False, "premium_only"
    try:
        deadline = datetime.fromisoformat(s.deadline_kst)
        if _kst_now().replace(tzinfo=None) >= deadline:
            return False, "deadline_passed"
    except ValueError:
        return False, "deadline_passed"
    if any(p.user_key == user_key for p in s.predictions):
        return False, "already_submitted"
    s.predictions.append(SinglePrediction(
        user_key=user_key, anon_user_id=anon_user_id,
        direction=direction,
        submitted_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    ))
    await repo.put(s)
    return True, "ok"


# ─────────────────────────────────────────────────────────────────────────────
# Resolve (5-min cron)
# ─────────────────────────────────────────────────────────────────────────────
async def _fetch_spot(ticker: str) -> float | None:
    def _sync() -> float | None:
        import yfinance as yf
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="1d", interval="5m", auto_adjust=False)
            if len(hist) > 0:
                return float(hist["Close"].iloc[-1])
        except Exception:
            return None
        return None
    return await asyncio.to_thread(_sync)


async def update_gauges(repo: SinglePredRepo,
                        kst_date: str | None = None) -> int:
    if kst_date is None:
        kst_date = _kst_today_iso()
    slots = await repo.list_for_date(kst_date)
    open_slots = [s for s in slots if s.status == "open"]
    if not open_slots:
        return 0
    tickers = {s.ticker for s in open_slots}
    sem = asyncio.Semaphore(4)
    prices: dict[str, float] = {}

    async def _one(t: str) -> None:
        async with sem:
            p = await _fetch_spot(t)
            if p is not None and p > 0:
                prices[t] = p

    await asyncio.gather(*[_one(t) for t in tickers])
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    updated = 0
    for s in open_slots:
        p = prices.get(s.ticker)
        if p is None:
            continue
        s.last_price = p
        s.last_polled_at = now_iso
        await repo.put(s)
        updated += 1
    return updated


async def resolve_due_singles(repo: SinglePredRepo, profile_repo, *,
                              usage_logger=None,
                              kst_date: str | None = None) -> dict:
    """5-min cron — resolve any slot whose resolve_at_kst <= now."""
    from .point_ledger import add_points
    if kst_date is None:
        kst_date = _kst_today_iso()
    slots = await repo.list_for_date(kst_date)
    now_naive_kst = _kst_now().replace(tzinfo=None)
    due = []
    for s in slots:
        if s.status != "open":
            continue
        try:
            if datetime.fromisoformat(s.resolve_at_kst) <= now_naive_kst:
                due.append(s)
        except ValueError:
            continue

    summary: dict[str, int] = {}
    for s in due:
        close = await _fetch_spot(s.ticker)
        if close is None or close <= 0:
            s.status = "void"
            await repo.put(s)
            summary[s.id] = 0
            continue
        s.last_price = close
        s.settled_close = close
        s.resolved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if abs(close - s.anchor_price) / max(s.anchor_price, 1e-9) < 0.0001:
            s.winner = "flat"
        elif close > s.anchor_price:
            s.winner = "up"
        else:
            s.winner = "down"
        s.status = "resolved"
        winners = 0
        if s.winner in ("up", "down"):
            for p in s.predictions:
                if p.direction == s.winner:
                    try:
                        await add_points(
                            profile_repo, p.user_key, CORRECT_POINTS,
                            reason="single_pred_correct", ref=s.id,
                            usage_logger=usage_logger,
                        )
                        winners += 1
                    except Exception:
                        logger.exception("single credit failed for %s", p.user_key)
        await repo.put(s)
        summary[s.id] = winners
    return summary
