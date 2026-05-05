"""Multilingual ticker alias resolution."""

from __future__ import annotations

import pytest

from services.ticker_lookup import TickerLookup


@pytest.fixture(scope="module")
def lookup():
    return TickerLookup()


@pytest.mark.parametrize("query,expected", [
    # Exact ticker (any case)
    ("AAPL", "AAPL"),
    ("aapl", "AAPL"),
    ("MSFT", "MSFT"),
    # English company names
    ("tesla", "TSLA"),
    ("TESLA", "TSLA"),
    ("apple", "AAPL"),
    ("nvidia", "NVDA"),
    # Korean
    ("애플", "AAPL"),
    ("테슬라", "TSLA"),
    ("엔비디아", "NVDA"),
    ("마이크로소프트", "MSFT"),
    # Japanese
    ("テスラ", "TSLA"),
    ("アップル", "AAPL"),
    ("エヌビディア", "NVDA"),
    # Chinese
    ("特斯拉", "TSLA"),
    ("苹果", "AAPL"),
    ("英伟达", "NVDA"),
    # Tickers with separator
    ("BRK-B", "BRK-B"),
    # Korean abbreviations / nicknames
    ("엔비",   "NVDA"),
    ("테슬",   "TSLA"),
    ("마소",   "MSFT"),
    ("넷플",   "NFLX"),
    ("아마",   "AMZN"),
    ("페북",   "META"),
    ("코베",   "COIN"),
    # Multi-word company names
    ("eli lilly",         "LLY"),
    ("home depot",        "HD"),
    ("johnson and johnson","JNJ"),
    ("berkshire hathaway", "BRK-B"),
    # Cross-language
    ("애브비",  "ABBV"),
    ("화이자",  "PFE"),
    ("머크",    "MRK"),
    ("리오토",  "LI"),         # Li Auto
    ("샤오펑",  "XPEV"),
    ("拼多多",  "PDD"),
    ("阿里",    "BABA"),
    ("京东",    "JD"),
    # Korean retail favorites
    ("팔란티어", "PLTR"),
    ("코인베이스", "COIN"),
    ("마이크로스트래티지", "MSTR"),
    ("브로드컴", "AVGO"),
    ("인텔",     "INTC"),
    ("퀄컴",     "QCOM"),
    # Major ETFs
    ("SPY",      "SPY"),
    ("스파이",   "SPY"),
    ("QQQ",      "QQQ"),
    ("큐큐큐",   "QQQ"),
    ("나스닥100 ETF", "QQQ"),
    ("VOO",      "VOO"),
    ("VTI",      "VTI"),
    ("TQQQ",     "TQQQ"),
    ("타큐",     "TQQQ"),
    ("SQQQ",     "SQQQ"),
    ("SCHD",     "SCHD"),
    ("슈드",     "SCHD"),
    ("JEPI",     "JEPI"),
    ("제피",     "JEPI"),
    ("JEPQ",     "JEPQ"),
    ("ARKK",     "ARKK"),
    # Bitcoin ETF
    ("IBIT",     "IBIT"),
    ("블랙록 비트코인", "IBIT"),
    # Sector ETF
    ("XLK",      "XLK"),
    ("기술 ETF", "XLK"),
    # International ETF
    ("EWY",      "EWY"),
    ("한국 ETF", "EWY"),
    ("FXI",      "FXI"),
    ("중국 ETF", "FXI"),
    # Commodity
    ("GLD",      "GLD"),
    ("금 ETF",   "GLD"),
])
def test_resolve_known(lookup, query, expected):
    assert lookup.resolve(query) == expected


def test_alias_count_above_threshold(lookup):
    """Coverage smoke test — at least 200 unique tickers and 600 aliases loaded."""
    aliases = lookup._aliases
    unique_tickers = set(aliases.values())
    assert len(aliases) >= 600, f"only {len(aliases)} aliases loaded"
    assert len(unique_tickers) >= 200, f"only {len(unique_tickers)} unique tickers"


def test_unknown_query_falls_back_to_uppercase(lookup):
    # Unknown company name passes through to uppercase so yfinance can decide
    assert lookup.resolve("xyzcorp") == "XYZCORP"


def test_empty_query(lookup):
    assert lookup.resolve("") == ""
    assert lookup.resolve("   ") == ""
