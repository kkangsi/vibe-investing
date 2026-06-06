"""§Vibe P3 — 읽기 API 메모리 캐시 helper 테스트.

HTTP endpoint 자체는 Azure Functions framework 가 wrap 해서 단위테스트가 까다로움.
대신 cached_blob_read + Memo 의 동작과, 응답 페이로드 셰이프 (helper 출력) 를 검증.
"""

from __future__ import annotations

import asyncio
import time
from unittest.mock import patch

import pytest

from services.vibe import api_cache


@pytest.fixture(autouse=True)
def _reset_memos():
    api_cache._MEMOS.clear()
    yield
    api_cache._MEMOS.clear()


class TestMemo:
    def test_initial_not_fresh(self) -> None:
        m = api_cache._Memo(ttl_s=60.0)
        assert m.is_fresh() is False
        assert m.get() is None

    def test_set_then_fresh(self) -> None:
        m = api_cache._Memo(ttl_s=60.0)
        m.set({"x": 1})
        assert m.is_fresh() is True
        assert m.get() == {"x": 1}

    def test_invalidate(self) -> None:
        m = api_cache._Memo(ttl_s=60.0)
        m.set({"y": 2})
        m.invalidate()
        assert m.is_fresh() is False

    def test_stale_when_ttl_expired(self, monkeypatch) -> None:
        m = api_cache._Memo(ttl_s=0.01)
        m.set({"z": 3})
        # monotonic 을 미래로 점프
        original = time.monotonic()
        monkeypatch.setattr("services.vibe.api_cache.time.monotonic",
                            lambda: original + 1000.0)
        assert m.is_fresh() is False

    def test_memo_for_returns_same_instance(self) -> None:
        a = api_cache.memo_for("p1", ttl_s=60.0)
        b = api_cache.memo_for("p1", ttl_s=999.0)
        assert a is b
        # 첫 호출의 ttl 이 고정
        assert a.ttl_s == 60.0

    def test_memo_for_different_paths(self) -> None:
        a = api_cache.memo_for("p1", ttl_s=60.0)
        b = api_cache.memo_for("p2", ttl_s=60.0)
        assert a is not b


class TestCachedBlobRead:
    def test_first_call_hits_blob(self) -> None:
        calls: list[str] = []

        async def fake_load(account, path, *, default=None, credential=None):
            calls.append(path)
            return {"data": "fresh"}

        with patch("services.vibe.blob_state.load_json", side_effect=fake_load):
            result = asyncio.run(api_cache.cached_blob_read(
                "acct", "signals/latest.json", ttl_s=60.0,
            ))
        assert result == {"data": "fresh"}
        assert calls == ["signals/latest.json"]

    def test_second_call_within_ttl_uses_memo(self) -> None:
        calls: list[str] = []

        async def fake_load(account, path, *, default=None, credential=None):
            calls.append(path)
            return {"hit": True}

        with patch("services.vibe.blob_state.load_json", side_effect=fake_load):
            asyncio.run(api_cache.cached_blob_read(
                "acct", "x.json", ttl_s=60.0,
            ))
            asyncio.run(api_cache.cached_blob_read(
                "acct", "x.json", ttl_s=60.0,
            ))
        assert calls == ["x.json"]  # 두 번째는 memo 가 가로챔

    def test_none_payload_not_cached(self) -> None:
        """Blob 이 없으면 (None) memo 도 갱신 안 됨 → 다음 호출에 다시 시도."""
        call_count = [0]

        async def fake_load(account, path, *, default=None, credential=None):
            call_count[0] += 1
            return None

        with patch("services.vibe.blob_state.load_json", side_effect=fake_load):
            asyncio.run(api_cache.cached_blob_read("acct", "y.json", ttl_s=60.0))
            asyncio.run(api_cache.cached_blob_read("acct", "y.json", ttl_s=60.0))
        assert call_count[0] == 2

    def test_default_passed_through(self) -> None:
        async def fake_load(account, path, *, default=None, credential=None):
            return default

        with patch("services.vibe.blob_state.load_json", side_effect=fake_load):
            result = asyncio.run(api_cache.cached_blob_read(
                "acct", "missing.json", ttl_s=60.0, default={"fallback": True},
            ))
        assert result == {"fallback": True}

    def test_stale_memo_refreshes(self, monkeypatch) -> None:
        """TTL 경과 후 호출은 Blob 을 다시 친다."""
        call_count = [0]

        async def fake_load(account, path, *, default=None, credential=None):
            call_count[0] += 1
            return {"v": call_count[0]}

        with patch("services.vibe.blob_state.load_json", side_effect=fake_load):
            asyncio.run(api_cache.cached_blob_read("acct", "z.json", ttl_s=0.01))
            # 시간 점프
            original = time.monotonic()
            monkeypatch.setattr("services.vibe.api_cache.time.monotonic",
                                lambda: original + 9999.0)
            result = asyncio.run(api_cache.cached_blob_read("acct", "z.json", ttl_s=0.01))
        assert call_count[0] == 2
        assert result == {"v": 2}
