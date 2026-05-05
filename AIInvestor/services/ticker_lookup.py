"""Multilingual company-name → ticker lookup.

Loads aliases from data/ticker_aliases.csv at process start. The CSV is
case-insensitive and supports Korean / Japanese / Chinese / English. Unknown
queries fall through to upper-case (the existing yfinance path).
"""

from __future__ import annotations

import csv
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

_DEFAULT_PATH = Path(__file__).resolve().parent.parent / "data" / "ticker_aliases.csv"

_TICKER_RE = re.compile(r"^[A-Z]{1,5}(?:[.\-][A-Z]{1,3})?$")


class TickerLookup:
    def __init__(self, csv_path: Path | str | None = None) -> None:
        path = Path(csv_path) if csv_path else _DEFAULT_PATH
        self._aliases: dict[str, str] = {}
        if path.exists():
            self._load(path)
        else:
            logger.warning("ticker alias CSV not found at %s — lookup will fall back to upper-case only", path)

    def _load(self, path: Path) -> None:
        with path.open(newline="", encoding="utf-8") as f:
            # Skip blank lines and comment lines (starting with '#')
            cleaned = (line for line in f if line.strip() and not line.lstrip().startswith("#"))
            reader = csv.DictReader(cleaned)
            for row in reader:
                alias = (row.get("alias") or "").strip().lower()
                ticker = (row.get("ticker") or "").strip().upper()
                if alias and ticker:
                    self._aliases[alias] = ticker
        unique_tickers = len(set(self._aliases.values()))
        logger.info("loaded %d ticker aliases covering %d unique tickers", len(self._aliases), unique_tickers)

    def resolve(self, query: str) -> str:
        """Return a ticker symbol for the query, or the upper-cased query if no match."""
        cleaned = query.strip()
        if not cleaned:
            return ""

        # 1. Multilingual alias table — case-insensitive, covers '애플', 'tesla', etc.
        key = cleaned.lower()
        if key in self._aliases:
            return self._aliases[key]

        compact = re.sub(r"\s+", " ", key)
        if compact in self._aliases:
            return self._aliases[compact]

        # 2. Already-uppercase ticker (the user typed it in caps): trust it
        first_token = cleaned.split()[0]
        if first_token == first_token.upper() and _TICKER_RE.match(first_token):
            return first_token

        # 3. Fallback: yfinance gets the upper-cased first token; it will raise if unknown
        return first_token.upper()
