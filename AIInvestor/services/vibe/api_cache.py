"""§Vibe — API 메모리 캐시.

기존 AIInvestor 정책과 동일 패턴:
  - module-level dict 에 (timestamp, payload) 저장
  - TTL 내 hit 면 Blob round-trip 생략
  - cron 이 Blob 쓰기 → endpoint 가 읽기 — 단방향 흐름

instance scaling 시 instance 별 별도 캐시 (stampede 무해, worst case Blob 1회/5분).
"""

from __future__ import annotations

import time
from typing import Any, Awaitable, Callable


class _Memo:
    __slots__ = ("ttl_s", "_t", "_payload")

    def __init__(self, ttl_s: float) -> None:
        self.ttl_s = float(ttl_s)
        self._t = 0.0
        self._payload: Any = None

    def is_fresh(self) -> bool:
        return self._payload is not None and (time.monotonic() - self._t) < self.ttl_s

    def get(self) -> Any:
        return self._payload

    def set(self, payload: Any) -> None:
        self._t = time.monotonic()
        self._payload = payload

    def invalidate(self) -> None:
        self._t = 0.0
        self._payload = None


# Endpoint-별 memo 인스턴스. 키 = blob path.
_MEMOS: dict[str, _Memo] = {}


def memo_for(path: str, ttl_s: float = 60.0) -> _Memo:
    """경로별 싱글톤 _Memo. 첫 호출에 ttl 결정 (이후 재사용)."""
    m = _MEMOS.get(path)
    if m is None:
        m = _Memo(ttl_s)
        _MEMOS[path] = m
    return m


async def cached_blob_read(
    account_name: str,
    path: str,
    ttl_s: float = 60.0,
    *,
    default: Any = None,
) -> Any:
    """Blob JSON 을 memo 통해 캐싱. fresh → memo, else → Blob fetch + memo set."""
    from . import blob_state

    memo = memo_for(path, ttl_s)
    if memo.is_fresh():
        return memo.get()
    payload = await blob_state.load_json(account_name, path, default=default)
    if payload is not None:
        memo.set(payload)
    return payload
