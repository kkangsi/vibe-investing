"""User profile abstraction.

A user profile carries persona choice, language preference, onboarding flags,
and free-form interest tags / watchlist tickers. Backed by SQLite for the
local 1차 phase; a Cosmos DB implementation will satisfy the same interface
in 2차 (see paper_plan.md §6.4).
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def make_anon_user_id(user_key: str, salt: str) -> str:
    digest = hashlib.sha256(f"{salt}:{user_key}".encode("utf-8")).hexdigest()
    return digest[:16]


@dataclass
class UserProfile:
    user_key: str
    anon_user_id: str
    persona_key: str
    language: str
    intro_seen: bool
    research_consent: bool
    onboarding_step: str
    interest_tags: list[str] = field(default_factory=list)
    watchlist_tickers: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    # §17.1 — sector follow-up tracking
    recent_tickers: list[str] = field(default_factory=list)        # LRU, max 10
    sector_count: dict[str, int] = field(default_factory=dict)     # {"Technology": 4, ...}
    last_followup_at: str = ""                                     # ISO; rate-limit follow-ups
    # §17.2 — daily deep analysis quota
    daily_deep_count: int = 0
    daily_deep_reset_at: str = ""                                  # ISO of next midnight KST


class UserProfileRepo:
    """SQLite-backed repository. Thread-safe for the synchronous handlers."""

    _SCHEMA = """
        CREATE TABLE IF NOT EXISTS users (
            user_key            TEXT PRIMARY KEY,
            anon_user_id        TEXT NOT NULL,
            persona_key         TEXT NOT NULL DEFAULT 'buffett',
            language            TEXT NOT NULL DEFAULT 'en',
            intro_seen          INTEGER NOT NULL DEFAULT 0,
            research_consent    INTEGER NOT NULL DEFAULT 0,
            onboarding_step     TEXT NOT NULL DEFAULT 'greeting',
            interest_tags       TEXT NOT NULL DEFAULT '[]',
            watchlist_tickers   TEXT NOT NULL DEFAULT '[]',
            recent_tickers      TEXT NOT NULL DEFAULT '[]',
            sector_count        TEXT NOT NULL DEFAULT '{}',
            last_followup_at    TEXT NOT NULL DEFAULT '',
            daily_deep_count    INTEGER NOT NULL DEFAULT 0,
            daily_deep_reset_at TEXT NOT NULL DEFAULT '',
            created_at          TEXT NOT NULL,
            updated_at          TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_users_anon ON users(anon_user_id);
    """

    # ALTER statements for upgrading older databases. SQLite ignores ALTER
    # if the column already exists (well, it errors — we catch).
    _MIGRATIONS = (
        "ALTER TABLE users ADD COLUMN recent_tickers TEXT NOT NULL DEFAULT '[]'",
        "ALTER TABLE users ADD COLUMN sector_count TEXT NOT NULL DEFAULT '{}'",
        "ALTER TABLE users ADD COLUMN last_followup_at TEXT NOT NULL DEFAULT ''",
        "ALTER TABLE users ADD COLUMN daily_deep_count INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE users ADD COLUMN daily_deep_reset_at TEXT NOT NULL DEFAULT ''",
    )

    def __init__(self, db_path: str | Path, salt: str) -> None:
        self._path = str(db_path)
        self._salt = salt
        self._lock = threading.Lock()
        Path(self._path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(self._SCHEMA)
            # Idempotent migrations (each ALTER may already be applied)
            for stmt in self._MIGRATIONS:
                try:
                    conn.execute(stmt)
                except sqlite3.OperationalError:
                    pass

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._path, isolation_level=None)
        conn.row_factory = sqlite3.Row
        return conn

    def get_or_create(self, user_key: str, default_language: str, default_persona: str) -> UserProfile:
        anon = make_anon_user_id(user_key, self._salt)
        now = _now_iso()
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE user_key = ?", (user_key,)).fetchone()
            if row is None:
                conn.execute(
                    """
                    INSERT INTO users
                      (user_key, anon_user_id, persona_key, language,
                       intro_seen, research_consent, onboarding_step,
                       interest_tags, watchlist_tickers, created_at, updated_at)
                    VALUES (?, ?, ?, ?, 0, 0, 'greeting', '[]', '[]', ?, ?)
                    """,
                    (user_key, anon, default_persona, default_language, now, now),
                )
                row = conn.execute("SELECT * FROM users WHERE user_key = ?", (user_key,)).fetchone()
        return _row_to_profile(row)

    def update(self, user_key: str, **fields) -> UserProfile:
        if not fields:
            return self.get(user_key)

        coerced: dict[str, object] = {}
        for k, v in fields.items():
            if k in {"interest_tags", "watchlist_tickers", "recent_tickers"} and isinstance(v, list):
                coerced[k] = json.dumps(v, ensure_ascii=False)
            elif k == "sector_count" and isinstance(v, dict):
                coerced[k] = json.dumps(v, ensure_ascii=False)
            elif k in {"intro_seen", "research_consent"}:
                coerced[k] = 1 if v else 0
            else:
                coerced[k] = v
        coerced["updated_at"] = _now_iso()

        sets = ", ".join(f"{k} = ?" for k in coerced)
        params = list(coerced.values()) + [user_key]
        with self._lock, self._connect() as conn:
            conn.execute(f"UPDATE users SET {sets} WHERE user_key = ?", params)
            row = conn.execute("SELECT * FROM users WHERE user_key = ?", (user_key,)).fetchone()
        if row is None:
            raise KeyError(f"user not found: {user_key}")
        return _row_to_profile(row)

    def get(self, user_key: str) -> UserProfile:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM users WHERE user_key = ?", (user_key,)).fetchone()
        if row is None:
            raise KeyError(f"user not found: {user_key}")
        return _row_to_profile(row)

    def delete(self, user_key: str) -> bool:
        """Hard-delete the user's row. Returns True if a row was removed."""
        with self._lock, self._connect() as conn:
            cur = conn.execute("DELETE FROM users WHERE user_key = ?", (user_key,))
        return cur.rowcount > 0


def _row_to_profile(row: sqlite3.Row) -> UserProfile:
    keys = row.keys()
    return UserProfile(
        user_key=row["user_key"],
        anon_user_id=row["anon_user_id"],
        persona_key=row["persona_key"],
        language=row["language"],
        intro_seen=bool(row["intro_seen"]),
        research_consent=bool(row["research_consent"]),
        onboarding_step=row["onboarding_step"],
        interest_tags=json.loads(row["interest_tags"] or "[]"),
        watchlist_tickers=json.loads(row["watchlist_tickers"] or "[]"),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        recent_tickers=json.loads(row["recent_tickers"] or "[]") if "recent_tickers" in keys else [],
        sector_count=json.loads(row["sector_count"] or "{}") if "sector_count" in keys else {},
        last_followup_at=row["last_followup_at"] if "last_followup_at" in keys else "",
        daily_deep_count=row["daily_deep_count"] if "daily_deep_count" in keys else 0,
        daily_deep_reset_at=row["daily_deep_reset_at"] if "daily_deep_reset_at" in keys else "",
    )
