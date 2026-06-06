"""§Vibe — 10분 시세 스냅샷 (Yahoo Finance, 키 불필요).

원본: cron-worker/src/market.ts + providers/yahoo.ts 의 충실 Python 포팅.
지수 4 + VIX + 섹터 ETF 11 + 한국인 선호 ETF 10 → Yahoo chart meta 호출,
급등/급락 Top10 → Yahoo 사전정의 screener (day_gainers / day_losers).

흐름:
  1) 미 장 시간(UTC 13:00–21:30) 밖이면 skip (비용 가드)
  2) 동시 fetch (부분 실패 허용)
  3) build_snapshot — 순수 함수 (테스트 가능)
  4) Blob `vibe/market/latest.json` 에 overwrite

Function instance 내 module-level 캐시:
  _MEMO = (timestamp_utc, snapshot)
  API endpoint 가 fresh(5분 이내) 면 Blob 안 거치고 즉시 반환.
"""

from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)

# 원본(market.ts)의 universe 상수 그대로
INDEX_NAMES: dict[str, str] = {
    "SPY": "S&P 500", "QQQ": "나스닥100",
    "DIA": "다우", "IWM": "러셀2000",
}
SECTOR_NAMES: dict[str, str] = {
    "XLK": "기술", "XLF": "금융", "XLV": "헬스케어", "XLE": "에너지",
    "XLI": "산업재", "XLY": "경기소비재", "XLP": "필수소비재",
    "XLU": "유틸리티", "XLB": "소재", "XLRE": "리츠", "XLC": "커뮤니케이션",
}
ETF_DISPLAY: list[str] = [
    "QQQ", "TQQQ", "SOXL", "SCHD", "JEPI",
    "JEPQ", "SMH", "SOXX", "NVDL", "TSLL",
]
VIX_SYMBOL = "^VIX"

YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
YAHOO_SCREENER = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
UA = "Mozilla/5.0 (Vibe Investing dashboard / research)"
HTTP_TIMEOUT_S = 8.0
MAX_PARALLEL = 12

# Module-level memoization (가이드: 메모리 캐싱 정책 그대로)
_MEMO_TTL_S = 300.0  # 5분
_memo: dict[str, Any] = {"t": 0.0, "snapshot": None}


# ──────────────────────────────────────────────────────────────────────────────
# Pure helpers
# ──────────────────────────────────────────────────────────────────────────────
def _py_round(x: float, ndigits: int = 2) -> float:
    """원본 series.pyRound 와 동일 (Banker's rounding 회피, 0.5 → away)."""
    if x is None:
        return 0.0
    m = 10 ** ndigits
    return float(int(x * m + (0.5 if x >= 0 else -0.5))) / m


def is_us_market_window_utc(now: datetime) -> bool:
    """UTC 13:00–21:30 (≈ 미 동부 09:00 프리 ~ 17:30). 외부에서 skip."""
    mins = now.hour * 60 + now.minute
    return 13 * 60 <= mins <= 21 * 60 + 30


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def build_snapshot(
    quotes: dict[str, dict[str, float]],
    gainers: list[dict[str, Any]],
    losers: list[dict[str, Any]],
    ts: str,
) -> dict[str, Any]:
    """순수 조립: quote 맵 + 스크리너 → 스냅샷. market.ts/buildMarketSnapshot 와 동치."""
    def tile(sym: str, name: str) -> dict[str, Any] | None:
        q = quotes.get(sym)
        if not q:
            return None
        return {"ticker": sym, "name": name,
                "price": _py_round(q["price"], 2),
                "chg_pct": _py_round(q["chgPct"], 2)}

    indices = [t for t in (tile(s, INDEX_NAMES[s]) for s in INDEX_NAMES) if t]
    sectors = [t for t in (tile(s, SECTOR_NAMES[s]) for s in SECTOR_NAMES) if t]
    etfs = [t for t in (tile(s, s) for s in ETF_DISPLAY) if t]
    vix_q = quotes.get(VIX_SYMBOL)
    vix = _py_round(vix_q["price"], 1) if vix_q else None

    sectors_up = sum(1 for s in sectors if s["chg_pct"] > 0)
    sectors_down = sum(1 for s in sectors if s["chg_pct"] < 0)

    # 리스크 게이지 (원본과 동일 heuristic)
    avg_idx_chg = (sum(t["chg_pct"] for t in indices) / len(indices)) if indices else 0.0
    up_ratio = (sectors_up / len(sectors)) if sectors else 0.5
    base_vix = vix if vix is not None else 18.0
    score = (50.0
             + _clamp(avg_idx_chg * 6, -25, 25)
             - _clamp((base_vix - 18.0) * 1.0, -15, 25)
             + (up_ratio - 0.5) * 20)
    score = _py_round(_clamp(score, 0, 100), 0)
    risk_label = "RISK_OFF" if score < 40 else "RISK_ON" if score > 60 else "NEUTRAL"

    def _movers(rows: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
        return [{
            "rank": i + 1,
            "ticker": r["ticker"],
            "name": r["name"],
            "price": _py_round(r["price"], 2),
            "chg_pct": _py_round(r["chgPct"], 2),
            "volume": int(round(r.get("volume") or 0)),
        } for i, r in enumerate(rows[:limit])]

    return {
        "ts": ts,
        "indices": indices,
        "vix": vix,
        "sectors": sectors,
        "etfs": etfs,
        "movers": {"gainers": _movers(gainers), "losers": _movers(losers)},
        "breadth": {"sectors_up": sectors_up, "sectors_down": sectors_down},
        "risk_score": score,
        "risk_label": risk_label,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Yahoo HTTP — minimal, 키리스
# ──────────────────────────────────────────────────────────────────────────────
def parse_quote_from_chart(json_body: dict[str, Any]) -> dict[str, float]:
    """chart meta → {price, prevClose, chgPct}. 부재 시 KeyError."""
    meta = (json_body.get("chart", {})
            .get("result", [{}])[0].get("meta", {}))
    price = meta.get("regularMarketPrice")
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    if not isinstance(price, (int, float)) or not isinstance(prev, (int, float)) or prev == 0:
        raise ValueError("yahoo: no meta price")
    return {"price": float(price), "prevClose": float(prev),
            "chgPct": (float(price) / float(prev) - 1) * 100.0}


def parse_screener(json_body: dict[str, Any]) -> list[dict[str, Any]]:
    """Yahoo predefined screener → 행 리스트."""
    quotes = (json_body.get("finance", {})
              .get("result", [{}])[0].get("quotes", []))
    rows: list[dict[str, Any]] = []
    for q in quotes:
        ticker = q.get("symbol")
        price = q.get("regularMarketPrice")
        chg = q.get("regularMarketChangePercent")
        if not ticker or not isinstance(price, (int, float)) or not isinstance(chg, (int, float)):
            continue
        rows.append({
            "ticker": ticker,
            "name": q.get("shortName") or q.get("longName") or ticker,
            "price": float(price),
            "chgPct": float(chg),
            "volume": float(q.get("regularMarketVolume") or 0),
        })
    return rows


async def _fetch_quote(session: aiohttp.ClientSession, sym: str) -> tuple[str, dict[str, float] | None]:
    url = YAHOO_CHART.format(sym=sym)
    try:
        async with session.get(url, params={"range": "1d", "interval": "1d"}) as r:
            if r.status != 200:
                return sym, None
            body = await r.json(content_type=None)
        return sym, parse_quote_from_chart(body)
    except Exception:
        return sym, None


async def _fetch_screener(session: aiohttp.ClientSession,
                          scr_id: str, count: int = 10) -> list[dict[str, Any]]:
    try:
        async with session.get(YAHOO_SCREENER,
                               params={"scrIds": scr_id, "count": str(count)}) as r:
            if r.status != 200:
                return []
            body = await r.json(content_type=None)
        return parse_screener(body)
    except Exception:
        return []


async def fetch_all_quotes(session: aiohttp.ClientSession,
                           symbols: list[str]) -> dict[str, dict[str, float]]:
    """동시 fetch with semaphore. 부분 실패 허용."""
    sem = asyncio.Semaphore(MAX_PARALLEL)

    async def _bounded(s: str):
        async with sem:
            return await _fetch_quote(session, s)

    results = await asyncio.gather(*(_bounded(s) for s in symbols))
    return {sym: q for sym, q in results if q is not None}


# ──────────────────────────────────────────────────────────────────────────────
# Orchestrator — called by cron + by API endpoints (memory cache)
# ──────────────────────────────────────────────────────────────────────────────
async def refresh_market_snapshot(account_name: str,
                                  force: bool = False) -> dict[str, Any]:
    """Yahoo → snapshot → Blob. 미 장외 시간은 skip dict 반환.

    `force=True` 면 시간대 무시 (수동 트리거용).
    """
    from . import blob_state

    now = datetime.now(timezone.utc)
    if not force and not is_us_market_window_utc(now):
        return {"skipped": True, "reason": "off-hours",
                "ts": now.isoformat(timespec="seconds")}

    syms = (list(INDEX_NAMES) + [VIX_SYMBOL]
            + list(SECTOR_NAMES) + ETF_DISPLAY)
    syms = list(dict.fromkeys(syms))  # dedup (QQQ in both INDEX + ETF_DISPLAY)

    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT_S)
    headers = {"User-Agent": UA, "Accept": "application/json"}
    async with aiohttp.ClientSession(timeout=timeout, headers=headers) as session:
        quotes, gainers, losers = await asyncio.gather(
            fetch_all_quotes(session, syms),
            _fetch_screener(session, "day_gainers", 10),
            _fetch_screener(session, "day_losers", 10),
        )

    ts = now.isoformat(timespec="seconds")
    snapshot = build_snapshot(quotes, gainers, losers, ts)

    # Blob 저장 + module-level 캐시 갱신
    await blob_state.save_json(account_name, "market/latest.json", snapshot)
    _memo["t"] = time.monotonic()
    _memo["snapshot"] = snapshot

    return {"skipped": False, "ts": ts,
            "risk": snapshot["risk_score"],
            "gainers": len(snapshot["movers"]["gainers"]),
            "losers": len(snapshot["movers"]["losers"]),
            "quotes_ok": len(quotes), "quotes_expected": len(syms)}


async def get_cached_market(account_name: str) -> dict[str, Any] | None:
    """API endpoint 용. Module-level (5분) → Blob → None 폴백 순서."""
    from . import blob_state

    if _memo["snapshot"] is not None and (time.monotonic() - _memo["t"]) < _MEMO_TTL_S:
        return _memo["snapshot"]

    snap = await blob_state.load_json(account_name, "market/latest.json", default=None)
    if snap is not None:
        _memo["t"] = time.monotonic()
        _memo["snapshot"] = snap
    return snap
