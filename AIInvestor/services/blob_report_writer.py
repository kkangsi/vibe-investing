"""Persist daily MarketReport blobs and purge the CDN edge.

Layout:
    container "reports"
      └── reports/<YYYY-MM-DD>/<persona>.<lang>.json

Each blob is the rendered report (the same string the bot would send to a
user). When users tap [예, 보기], the handler fetches the rendered text
from the CDN endpoint instead of regenerating via DeepSeek.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from typing import Iterable

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.cdn.aio import CdnManagementClient
from azure.storage.blob.aio import BlobServiceClient

from .market_report import MarketReport
from .persona_engine import Persona, list_personas

logger = logging.getLogger(__name__)

CONTAINER = "reports"
SUPPORTED_LANGS = ("ko", "en", "ja", "zh")


def report_blob_path(date_str: str, persona_key: str, language: str) -> str:
    return f"{date_str}/{persona_key}.{language}.json"


class BlobReportWriter:
    """Uploads pre-rendered reports and purges the CDN endpoint."""

    def __init__(
        self,
        storage_account_name: str,
        cdn_subscription_id: str | None = None,
        cdn_resource_group: str | None = None,
        cdn_profile_name: str | None = None,
        cdn_endpoint_name: str | None = None,
        credential=None,
    ) -> None:
        self._account_url = f"https://{storage_account_name}.blob.core.windows.net"
        self._credential = credential or DefaultAzureCredential()
        self._cdn = {
            "subscription_id": cdn_subscription_id,
            "resource_group": cdn_resource_group,
            "profile": cdn_profile_name,
            "endpoint": cdn_endpoint_name,
        }
        self._service: BlobServiceClient | None = None

    async def _client(self) -> BlobServiceClient:
        if self._service is None:
            self._service = BlobServiceClient(
                account_url=self._account_url, credential=self._credential
            )
        return self._service

    async def aclose(self) -> None:
        if self._service is not None:
            await self._service.close()
        if hasattr(self._credential, "close"):
            await self._credential.close()

    async def upload_report(
        self,
        report: MarketReport,
        persona: Persona,
        language: str,
        rendered_text: str,
    ) -> str:
        """Upload a single rendered report blob. Returns the blob path."""
        path = report_blob_path(report.date, persona.key, language)
        body = json.dumps(
            {
                "date": report.date,
                "persona_key": persona.key,
                "persona_name": persona.name(language),
                "language": language,
                "rendered_text": rendered_text,
                "data": asdict(report),
            },
            ensure_ascii=False,
        ).encode("utf-8")

        client = (await self._client()).get_blob_client(CONTAINER, path)
        await client.upload_blob(
            body,
            overwrite=True,
            content_type="application/json",
            content_settings_kwargs={"cache_control": "public, max-age=3600"},
        )
        logger.info("uploaded report blob %s (%d bytes)", path, len(body))
        return path

    async def upload_all(
        self,
        reports_by_lang: dict[tuple[str, str], tuple[MarketReport, str]],
    ) -> list[str]:
        """Upload every (persona, language) report.

        `reports_by_lang` is keyed by (persona_key, language) and yields
        (MarketReport, rendered_text). Returns the list of paths written.
        """
        paths: list[str] = []
        personas_by_key = {p.key: p for p in list_personas()}
        for (persona_key, language), (report, rendered) in reports_by_lang.items():
            persona = personas_by_key.get(persona_key)
            if persona is None:
                continue
            paths.append(await self.upload_report(report, persona, language, rendered))
        return paths

    async def purge_cdn_paths(self, paths: Iterable[str]) -> None:
        """POST a purge to the CDN endpoint. Best-effort — failures are logged but not raised."""
        if not all(self._cdn.values()):
            logger.warning("CDN parameters not fully configured; skipping purge")
            return
        try:
            async with CdnManagementClient(self._credential, self._cdn["subscription_id"]) as client:
                purge_paths = [f"/{CONTAINER}/{p}" for p in paths]
                poller = await client.endpoints.begin_purge_content(
                    resource_group_name=self._cdn["resource_group"],
                    profile_name=self._cdn["profile"],
                    endpoint_name=self._cdn["endpoint"],
                    content_file_paths={"contentPaths": purge_paths},
                )
                await poller.result()
                logger.info("CDN purge succeeded for %d paths", len(purge_paths))
        except Exception:
            logger.exception("CDN purge failed (non-fatal)")


async def fetch_cached_report(
    storage_account_name: str,
    date_str: str,
    persona_key: str,
    language: str,
    credential=None,
) -> str | None:
    """Read a pre-rendered report from Blob Storage. Returns the text or None if absent."""
    path = report_blob_path(date_str, persona_key, language)
    creds = credential or DefaultAzureCredential()
    async with BlobServiceClient(
        account_url=f"https://{storage_account_name}.blob.core.windows.net",
        credential=creds,
    ) as svc:
        client = svc.get_blob_client(CONTAINER, path)
        try:
            download = await client.download_blob()
            body = await download.readall()
            doc = json.loads(body)
            return doc.get("rendered_text")
        except Exception as exc:
            logger.debug("report blob miss path=%s err=%s", path, exc)
            return None
