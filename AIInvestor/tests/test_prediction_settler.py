"""Tests for §4 generic prediction settler — pure-function units only.

Repo + cron live calls require Azure Blob; we cover those with the integration
test in §8. Here we exercise:
  - next_trading_day_kst() weekend-skip logic
  - Prediction.new() factory invariants
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from services.prediction_repo import Prediction
from services.prediction_settler import _next_trading_day, next_trading_day_kst


class TestNextTradingDay:
    def test_friday_skips_to_monday(self) -> None:
        # 2026-05-08 = Friday → next trading day is Monday 2026-05-11
        assert _next_trading_day("2026-05-08") == "2026-05-11"

    def test_saturday_skips_to_monday(self) -> None:
        assert _next_trading_day("2026-05-09") == "2026-05-11"

    def test_sunday_skips_to_monday(self) -> None:
        assert _next_trading_day("2026-05-10") == "2026-05-11"

    def test_monday_to_tuesday(self) -> None:
        assert _next_trading_day("2026-05-11") == "2026-05-12"

    def test_thursday_to_friday(self) -> None:
        assert _next_trading_day("2026-05-07") == "2026-05-08"

    def test_kst_helper_returns_iso(self) -> None:
        result = next_trading_day_kst(
            now=datetime(2026, 5, 7, 23, 0, 0, tzinfo=timezone.utc),
        )
        # 23:00 UTC + 9h = 08:00 KST May 8 (Friday) → next is May 11
        assert result == "2026-05-11"


class TestPredictionFactory:
    def test_new_assigns_uuid(self) -> None:
        p = Prediction.new("a" * 16, "AAPL", "up", 165.30, "2026-05-08")
        assert len(p.prediction_id) == 36  # UUID4 string

    def test_new_uppercases_ticker(self) -> None:
        p = Prediction.new("a" * 16, "aapl", "up", 165.30, "2026-05-08")
        assert p.ticker == "AAPL"

    def test_new_starts_pending(self) -> None:
        p = Prediction.new("a" * 16, "AAPL", "up", 165.30, "2026-05-08")
        assert p.status == "pending"
        assert p.click_count == 0
        assert p.result == ""

    def test_new_strips_whitespace(self) -> None:
        p = Prediction.new("a" * 16, "  TSLA  ", "down", 250.0, "2026-05-08")
        assert p.ticker == "TSLA"
