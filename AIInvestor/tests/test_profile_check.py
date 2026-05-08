"""§2 P0 — tests for the /api/profile/check pre-warm cache path.

We exercise the in-process anon cache directly (no Blob roundtrips) since
the BlobUserProfileRepo wraps Azure SDK with async I/O that needs network.
The cache layer is the hot path that determines p95 latency, so it gets
the bulk of unit coverage.
"""

from __future__ import annotations

import time

import pytest

from services.user_profile_blob import (
    _ANON_CHECK_CACHE,
    _ANON_CHECK_TTL,
    _anon_cache_get,
    _anon_cache_put,
    anon_cache_evict,
)


@pytest.fixture(autouse=True)
def _clear_cache():
    _ANON_CHECK_CACHE.clear()
    yield
    _ANON_CHECK_CACHE.clear()


class TestAnonCache:
    def test_miss_returns_none(self) -> None:
        assert _anon_cache_get("abcdef0123456789") is None

    def test_put_then_hit(self) -> None:
        _anon_cache_put("abcdef0123456789", {
            "exists": True, "has_birth_info": True, "last_seen": "2026-05-08T00:00:00",
        })
        hit = _anon_cache_get("abcdef0123456789")
        assert hit is not None
        assert hit["exists"] is True
        assert hit["has_birth_info"] is True

    def test_evict_removes_entry(self) -> None:
        _anon_cache_put("abcdef0123456789", {"exists": True, "has_birth_info": False, "last_seen": None})
        anon_cache_evict("abcdef0123456789")
        assert _anon_cache_get("abcdef0123456789") is None

    def test_ttl_expiry(self, monkeypatch) -> None:
        """After TTL the entry should be evicted on next read."""
        anon = "abcdef0123456789"
        _anon_cache_put(anon, {"exists": True, "has_birth_info": False, "last_seen": None})
        # Manually set entry expiry to the past
        _, payload = _ANON_CHECK_CACHE[anon]
        _ANON_CHECK_CACHE[anon] = (time.monotonic() - 1, payload)
        assert _anon_cache_get(anon) is None
        # And the expired entry should now be removed from the dict
        assert anon not in _ANON_CHECK_CACHE

    def test_evict_nonexistent_is_noop(self) -> None:
        # Should not raise even if anon was never cached
        anon_cache_evict("nonexistent_anon_key")

    def test_payload_shape(self) -> None:
        """Stored payload must have exactly the 3 fields the API contract promises."""
        _anon_cache_put("abcdef0123456789", {
            "exists": True, "has_birth_info": True, "last_seen": "2026-05-08T00:00:00",
        })
        payload = _anon_cache_get("abcdef0123456789")
        assert set(payload.keys()) == {"exists", "has_birth_info", "last_seen"}

    def test_ttl_is_5_minutes(self) -> None:
        """Spec target: 5min in-process TTL — guard against accidental tweak."""
        assert _ANON_CHECK_TTL == 300
