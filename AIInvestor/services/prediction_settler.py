"""§4 P0 — Settle pending predictions + expire stale ones.

Two operations on the generic ticker prediction system:
  1. settle_predictions(target_date) — KST 16:00 cron
       fetches close price for every pending prediction targeting this date,
       computes win/lose, transitions to "settled" or "no_data".
  2. expire_stale_predictions(cutoff_days=7) — KST 02:30 cron
       any prediction still pending older than cutoff → "no_data" with
       expire_reason="expired_7d".

yfinance is wrapped in asyncio.to_thread (sync API) and bounded by Semaphore.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta, timezone

from .prediction_repo import Prediction, PredictionRepo

logger = logging.getLogger(__name__)

_SEM = asyncio.Semaphore(4)  # bound concurrent yfinance calls


def _kst_today_iso() -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=9)).date().isoformat()


def _next_trading_day(d_iso: str) -> str:
    """Naive next-trading-day: skip weekends. US holidays not modeled — settler
    will produce no_data on those days, which is the desired behavior."""
    d = datetime.strptime(d_iso, "%Y-%m-%d").date()
    d += timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d.isoformat()


def next_trading_day_kst(now: datetime | None = None) -> str:
    """Public helper used by /api/predictions/create.
    Returns YYYY-MM-DD KST of the next trading day after `now`."""
    now = now or datetime.now(timezone.utc)
    kst = now + timedelta(hours=9)
    return _next_trading_day(kst.date().isoformat())


def _fetch_close_sync(ticker: str, date_iso: str) -> float | None:
    """yfinance .history() for a single date. None on no-data."""
    import yfinance as yf
    try:
        d = datetime.strptime(date_iso, "%Y-%m-%d").date()
        df = yf.Ticker(ticker).history(
            start=date_iso,
            end=(d + timedelta(days=1)).isoformat(),
            auto_adjust=False,
        )
        if df is None or df.empty or "Close" not in df.columns:
            return None
        # Take the last close (handles multi-row edge case)
        v = float(df["Close"].iloc[-1])
        return v if v > 0 else None
    except Exception:
        logger.exception("yfinance fetch failed for %s on %s", ticker, date_iso)
        return None


async def fetch_close_price(ticker: str, date_iso: str) -> float | None:
    async with _SEM:
        return await asyncio.to_thread(_fetch_close_sync, ticker, date_iso)


async def settle_predictions(repo: PredictionRepo,
                             target_date: str | None = None) -> dict:
    """KST 16:00 cron — settle every pending prediction targeting today.

    Returns {settled_win, settled_lose, no_data, errors}.
    """
    target_date = target_date or _kst_today_iso()
    pending = await repo.list_pending_due(target_date)
    counts = {"settled_win": 0, "settled_lose": 0, "no_data": 0, "errors": 0}
    if not pending:
        return counts

    async def _one(p: Prediction) -> None:
        try:
            close = await fetch_close_price(p.ticker, target_date)
            now = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if close is None:
                await repo.update_status(
                    p.anon_user_id, p.prediction_id,
                    status="no_data", settled_at=now,
                    expire_reason="no_close_data",
                )
                counts["no_data"] += 1
                return
            won = (p.direction == "up" and close > p.created_price) or \
                  (p.direction == "down" and close < p.created_price)
            await repo.update_status(
                p.anon_user_id, p.prediction_id,
                status="settled", settled_at=now,
                settled_price=close,
                result="win" if won else "lose",
            )
            if won:
                counts["settled_win"] += 1
            else:
                counts["settled_lose"] += 1
        except Exception:
            logger.exception("settle failed for %s", p.prediction_id)
            counts["errors"] += 1

    # Bound batch fan-out
    await asyncio.gather(*[_one(p) for p in pending])
    return counts


async def expire_stale_predictions(repo: PredictionRepo,
                                   cutoff_days: int = 7) -> int:
    """KST 02:30 cron — flip 7-day-old pendings to no_data."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=cutoff_days)
              ).isoformat(timespec="seconds")
    stale = await repo.list_pending_before(cutoff)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for p in stale:
        await repo.update_status(
            p.anon_user_id, p.prediction_id,
            status="no_data", settled_at=now, expire_reason="expired_7d",
        )
    return len(stale)
