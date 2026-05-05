"""Factory that returns either the SQLite or the Blob UserProfileRepo.

The handlers use the same `get_or_create / update / get / delete` surface
in both cases, so the only thing that changes between 1차 (local) and
2차 (Azure) is which backend is constructed at startup.

NOTE: handler code currently calls these methods synchronously (SQLite
implementation is sync). When STORAGE_BACKEND=blob, the methods become
async — the handler will need `await` calls. We keep the sync path as
the default and provide a thin async wrapper around the SQLite repo so
the call sites can become uniformly `await ...` once the switch is
flipped (2차-B follow-up).
"""

from __future__ import annotations

import logging
from typing import Protocol

from config import Config
from .user_profile import UserProfile, UserProfileRepo

logger = logging.getLogger(__name__)


class AsyncUserProfileRepo(Protocol):
    async def get_or_create(
        self, user_key: str, default_language: str, default_persona: str
    ) -> UserProfile: ...
    async def update(self, user_key: str, **fields) -> UserProfile: ...
    async def get(self, user_key: str) -> UserProfile: ...
    async def delete(self, user_key: str) -> bool: ...


def build_repo(config: Config):
    """Return the configured repo (sync `UserProfileRepo` or async `BlobUserProfileRepo`)."""
    backend = config.storage_backend
    if backend == "blob":
        if not config.storage_account_name:
            raise RuntimeError(
                "STORAGE_BACKEND=blob requires STORAGE_ACCOUNT_NAME to be set."
            )
        from .user_profile_blob import BlobUserProfileRepo
        account_url = f"https://{config.storage_account_name}.blob.core.windows.net"
        logger.info("Using BlobUserProfileRepo (account=%s)", config.storage_account_name)
        return BlobUserProfileRepo(account_url=account_url, salt=config.user_id_salt)

    # default: sqlite
    logger.info("Using SQLite UserProfileRepo at %s", config.sqlite_path)
    return UserProfileRepo(db_path=config.sqlite_path, salt=config.user_id_salt)
