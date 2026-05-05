"""Daily U.S. market report — S&P 500 / NASDAQ / NDX + NASDAQ-100 movers.

The report is built once per US trading day and cached in process memory
(TTL 24h). In 2차 작업 the same data structure will be persisted as a Blob
JSON for CDN edge serving.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable

import pandas as pd
import yfinance as yf

from .i18n import PERSONA_LANGUAGE_INSTRUCTION, t
from .persona_engine import PersonaEngine
from .stock_service import StockServiceError

logger = logging.getLogger(__name__)


NASDAQ_100_TICKERS: list[str] = [
    "AAPL", "ABNB", "ADBE", "ADI", "ADP", "ADSK", "AEP", "AMAT", "AMD", "AMGN",
    "AMZN", "ANSS", "APP", "ARM", "ASML", "AVGO", "AZN", "BIIB", "BKNG", "BKR",
    "CCEP", "CDNS", "CDW", "CEG", "CHTR", "CMCSA", "COST", "CPRT", "CRWD", "CSCO",
    "CSGP", "CSX", "CTAS", "CTSH", "DASH", "DDOG", "DXCM", "EA", "EXC", "FANG",
    "FAST", "FTNT", "GEHC", "GFS", "GILD", "GOOG", "GOOGL", "HON", "IDXX", "INTC",
    "INTU", "ISRG", "KDP", "KHC", "KLAC", "LIN", "LRCX", "LULU", "MAR", "MCHP",
    "MDB", "MDLZ", "MELI", "META", "MNST", "MRVL", "MSFT", "MSTR", "MU", "NFLX",
    "NVDA", "NXPI", "ODFL", "ON", "ORLY", "PANW", "PAYX", "PCAR", "PDD", "PEP",
    "PLTR", "PYPL", "QCOM", "REGN", "ROP", "ROST", "SBUX", "SHOP", "SNPS", "TEAM",
    "TMUS", "TSLA", "TTD", "TTWO", "TXN", "VRSK", "VRTX", "WBD", "WDAY", "XEL",
    "ZS",
]

INDEX_TICKERS = {
    "sp500":  "^GSPC",
    "nasdaq": "^IXIC",
    "ndx":    "^NDX",
}


@dataclass
class TickerMove:
    ticker: str
    prev_close: float
    last_close: float
    change_pct: float


@dataclass
class MarketReport:
    date: str  # YYYY-MM-DD (US trading day basis, derived from latest close)
    sp500_close: float | None
    sp500_change_pct: float | None
    nasdaq_close: float | None
    nasdaq_change_pct: float | None
    ndx_close: float | None
    ndx_change_pct: float | None
    top_gainers: list[TickerMove] = field(default_factory=list)
    top_losers: list[TickerMove] = field(default_factory=list)
    persona_commentary: str = ""

    def render(self, language: str, persona_name: str) -> str:
        s = t(language)
        title = {
            "ko": "📊 오늘의 시황",
            "en": "📊 Today's Market",
            "ja": "📊 本日の市況",
            "zh": "📊 今日市场",
        }.get(language, "📊 Today's Market")

        index_label = {
            "ko": ("S&P 500", "NASDAQ 종합", "NASDAQ-100"),
            "en": ("S&P 500", "NASDAQ Composite", "NASDAQ-100"),
            "ja": ("S&P 500", "NASDAQ総合", "NASDAQ-100"),
            "zh": ("S&P 500", "NASDAQ综合", "NASDAQ-100"),
        }.get(language, ("S&P 500", "NASDAQ Composite", "NASDAQ-100"))

        gainers_label = {"ko": "📈 상승 Top 5", "en": "📈 Top 5 Gainers",
                         "ja": "📈 上昇 Top 5",  "zh": "📈 涨幅 Top 5"}.get(language, "📈 Top 5 Gainers")
        losers_label  = {"ko": "📉 하락 Top 5", "en": "📉 Top 5 Losers",
                         "ja": "📉 下落 Top 5",  "zh": "📉 跌幅 Top 5"}.get(language, "📉 Top 5 Losers")
        commentary_label = {"ko": "💬 한 줄 코멘트", "en": "💬 Comment",
                            "ja": "💬 一言コメント", "zh": "💬 一句点评"}.get(language, "💬 Comment")

        lines = [f"{title} ({self.date})", ""]
        for label, close, chg in zip(
            index_label,
            (self.sp500_close, self.nasdaq_close, self.ndx_close),
            (self.sp500_change_pct, self.nasdaq_change_pct, self.ndx_change_pct),
        ):
            if close is None or chg is None:
                lines.append(f"• {label}: N/A")
            else:
                arrow = "▲" if chg >= 0 else "▼"
                lines.append(f"• {label}: {close:,.2f} {arrow} {chg:+.2f}%")
        lines.append("")
        lines.append(gainers_label)
        for m in self.top_gainers:
            lines.append(f"  {m.ticker}: {m.last_close:,.2f} ▲ {m.change_pct:+.2f}%")
        lines.append("")
        lines.append(losers_label)
        for m in self.top_losers:
            lines.append(f"  {m.ticker}: {m.last_close:,.2f} ▼ {m.change_pct:+.2f}%")
        if self.persona_commentary:
            lines.append("")
            lines.append(f"{commentary_label} — {persona_name}")
            lines.append(self.persona_commentary)
        lines.append("")
        lines.append(f"⚠ {s.disclaimer}")
        return "\n".join(lines)


class MarketReportService:
    """Builds the daily report. Caches one report per UTC date in process memory."""

    def __init__(self, persona_engine: PersonaEngine) -> None:
        self._engine = persona_engine
        self._cache: dict[str, MarketReport] = {}
        self._lock = asyncio.Lock()

    async def build(
        self,
        persona,
        language: str,
        interests: Iterable[str] | None = None,
    ) -> MarketReport:
        async with self._lock:
            cache_key = f"{datetime.now(timezone.utc).date().isoformat()}::{persona.key}::{language}"
            cached = self._cache.get(cache_key)
            if cached is not None:
                return cached

            base = await asyncio.to_thread(_fetch_market_data)
            commentary = await self._build_commentary(persona, language, base, list(interests or []))
            base.persona_commentary = commentary
            self._cache[cache_key] = base
            return base

    async def _build_commentary(self, persona, language: str, report: MarketReport, interests: list[str]) -> str:
        lang_instruction = PERSONA_LANGUAGE_INSTRUCTION.get(language, PERSONA_LANGUAGE_INSTRUCTION["en"])
        interest_block = ""
        if interests:
            interest_block = (
                "\nThe user previously expressed interest in: "
                + ", ".join(interests)
                + ". Reference these only if naturally relevant.\n"
            )

        gainers = ", ".join(f"{m.ticker} {m.change_pct:+.1f}%" for m in report.top_gainers) or "(none)"
        losers = ", ".join(f"{m.ticker} {m.change_pct:+.1f}%" for m in report.top_losers) or "(none)"

        user_prompt = (
            f"Today's U.S. market snapshot ({report.date}):\n"
            f"- S&P 500: {report.sp500_change_pct:+.2f}% (close {report.sp500_close})\n"
            f"- NASDAQ Composite: {report.nasdaq_change_pct:+.2f}% (close {report.nasdaq_close})\n"
            f"- NASDAQ-100: {report.ndx_change_pct:+.2f}% (close {report.ndx_close})\n"
            f"- Top NDX-100 gainers: {gainers}\n"
            f"- Top NDX-100 losers: {losers}\n"
            f"{interest_block}\n"
            "In ONE OR TWO sentences, give your persona's reading of today. "
            "Be concrete (mention an index move or one notable ticker). "
            "Do not give buy/sell instructions; do not invent numbers beyond what's listed."
        )

        try:
            response = await self._engine._client.chat.completions.create(
                model=self._engine._model,
                temperature=0.5,
                timeout=20.0,
                messages=[
                    {"role": "system", "content": f"{persona.system_prompt}\n\n{lang_instruction}"},
                    {"role": "user", "content": user_prompt},
                ],
            )
            return (response.choices[0].message.content or "").strip()
        except Exception:
            logger.exception("market commentary generation failed")
            return ""


# -----------------------------
# Synchronous yfinance fetch
# -----------------------------

def _fetch_market_data() -> MarketReport:
    indices = yf.download(
        tickers=list(INDEX_TICKERS.values()),
        period="5d",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False,
        threads=True,
    )

    sp_close, sp_chg = _index_close_and_change(indices, INDEX_TICKERS["sp500"])
    nq_close, nq_chg = _index_close_and_change(indices, INDEX_TICKERS["nasdaq"])
    nx_close, nx_chg = _index_close_and_change(indices, INDEX_TICKERS["ndx"])

    moves = _ndx100_moves(NASDAQ_100_TICKERS)
    moves.sort(key=lambda m: m.change_pct, reverse=True)
    gainers = moves[:5]
    losers = list(reversed(moves[-5:])) if len(moves) >= 5 else []

    today = datetime.now(timezone.utc).date().isoformat()
    return MarketReport(
        date=today,
        sp500_close=sp_close,
        sp500_change_pct=sp_chg,
        nasdaq_close=nq_close,
        nasdaq_change_pct=nq_chg,
        ndx_close=nx_close,
        ndx_change_pct=nx_chg,
        top_gainers=gainers,
        top_losers=losers,
    )


def _index_close_and_change(df: pd.DataFrame, ticker: str) -> tuple[float | None, float | None]:
    try:
        close = df[ticker]["Close"].dropna()
    except (KeyError, TypeError):
        return None, None
    if len(close) < 2:
        return None, None
    prev = float(close.iloc[-2])
    last = float(close.iloc[-1])
    if prev == 0:
        return last, None
    return last, (last - prev) / prev * 100.0


def _ndx100_moves(tickers: list[str]) -> list[TickerMove]:
    data = yf.download(
        tickers=tickers,
        period="5d",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    out: list[TickerMove] = []
    for tkr in tickers:
        try:
            close = data[tkr]["Close"].dropna()
        except (KeyError, TypeError):
            continue
        if len(close) < 2:
            continue
        prev = float(close.iloc[-2])
        last = float(close.iloc[-1])
        if prev == 0:
            continue
        out.append(TickerMove(
            ticker=tkr,
            prev_close=prev,
            last_close=last,
            change_pct=(last - prev) / prev * 100.0,
        ))
    return out
