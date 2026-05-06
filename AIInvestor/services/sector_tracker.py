"""Track which sectors a user keeps asking about, surface follow-up offers.

§17.1 of paper_plan.md. Trigger condition:
  same dominant sector ≥ 3 of last 5 queries  AND  last follow-up > 60 min ago

Output: (should_offer, dominant_sector, related_etfs, peer_tickers)
The handler then asks: "반도체 섹터에 관심이 많으시네요... 비교해드릴까요?"
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone, timedelta
from typing import Iterable

from .user_profile import UserProfile

# Recent ticker memory size
RECENT_MAX = 10
# Window of last queries we look at when deciding to offer follow-up
DOMINANCE_WINDOW = 5
DOMINANCE_THRESHOLD = 3
# Don't re-offer the same kind of follow-up within this many minutes
FOLLOWUP_COOLDOWN_MIN = 60

# Curated peer + ETF map per yfinance "sector" string. Kept small + Korean-retail focused.
SECTOR_RELATED: dict[str, dict[str, list[str]]] = {
    "Technology": {
        "etfs": ["XLK", "SMH", "SOXX", "QQQ", "TQQQ"],
        "peers": ["AAPL", "MSFT", "NVDA", "AVGO", "AMD", "INTC", "QCOM", "ASML", "ARM", "TSM"],
    },
    "Communication Services": {
        "etfs": ["XLC", "QQQ"],
        "peers": ["GOOGL", "META", "NFLX", "DIS", "CMCSA", "TMUS"],
    },
    "Consumer Cyclical": {
        "etfs": ["XLY", "AMZN", "QQQ"],
        "peers": ["AMZN", "TSLA", "HD", "MCD", "SBUX", "NKE", "BKNG", "LULU"],
    },
    "Consumer Defensive": {
        "etfs": ["XLP"],
        "peers": ["WMT", "COST", "PG", "KO", "PEP", "MDLZ", "PM"],
    },
    "Financial Services": {
        "etfs": ["XLF"],
        "peers": ["JPM", "BAC", "WFC", "GS", "MS", "V", "MA", "AXP", "PYPL"],
    },
    "Healthcare": {
        "etfs": ["XLV"],
        "peers": ["JNJ", "LLY", "UNH", "PFE", "MRK", "ABBV", "TMO", "DHR"],
    },
    "Energy": {
        "etfs": ["XLE", "USO"],
        "peers": ["XOM", "CVX", "COP", "OXY", "SLB", "PSX", "EOG"],
    },
    "Industrials": {
        "etfs": ["XLI"],
        "peers": ["CAT", "DE", "BA", "GE", "RTX", "LMT", "HON", "UPS", "FDX"],
    },
    "Utilities": {
        "etfs": ["XLU"],
        "peers": ["NEE", "DUK", "SO", "AEP", "EXC"],
    },
    "Real Estate": {
        "etfs": ["XLRE", "VNQ"],
        "peers": ["AMT", "PLD", "EQIX", "O", "SPG"],
    },
    "Basic Materials": {
        "etfs": ["XLB"],
        "peers": ["LIN", "FCX", "NEM"],
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def update_recent(profile: UserProfile, ticker: str, sector: str | None) -> dict:
    """Compute the new recent_tickers + sector_count fields. Returns kwargs to .update()."""
    rt = list(profile.recent_tickers)
    if ticker in rt:
        rt.remove(ticker)
    rt.insert(0, ticker)
    rt = rt[:RECENT_MAX]

    sc = dict(profile.sector_count)
    if sector:
        sc[sector] = sc.get(sector, 0) + 1

    return {"recent_tickers": rt, "sector_count": sc}


def maybe_offer_followup(
    profile: UserProfile,
    sector_resolver: callable,
) -> tuple[str, list[str], list[str]] | None:
    """Decide whether to offer a sector follow-up.

    Args:
        profile: current UserProfile (after update_recent applied)
        sector_resolver: callable(ticker) -> sector string. We use this to
            look up sectors for each item in recent_tickers (the snapshot
            cache will hit ~99% of the time since these were just queried).

    Returns:
        (sector_name, etf_list, peer_list) when an offer should be made, else None.
    """
    if not profile.recent_tickers:
        return None

    # Cooldown check
    if profile.last_followup_at:
        try:
            last = datetime.fromisoformat(profile.last_followup_at.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) - last < timedelta(minutes=FOLLOWUP_COOLDOWN_MIN):
                return None
        except Exception:
            pass

    # Look at last DOMINANCE_WINDOW tickers
    window = profile.recent_tickers[:DOMINANCE_WINDOW]
    sectors_in_window = []
    for tkr in window:
        sec = sector_resolver(tkr)
        if sec:
            sectors_in_window.append(sec)

    if len(sectors_in_window) < DOMINANCE_THRESHOLD:
        return None

    counts = Counter(sectors_in_window)
    dominant_sector, count = counts.most_common(1)[0]
    if count < DOMINANCE_THRESHOLD:
        return None

    related = SECTOR_RELATED.get(dominant_sector)
    if not related:
        return None

    # Filter peers — exclude tickers user already saw
    peers = [p for p in related.get("peers", []) if p not in profile.recent_tickers][:5]
    etfs = list(related.get("etfs", []))[:4]
    if not peers and not etfs:
        return None

    return (dominant_sector, etfs, peers)
