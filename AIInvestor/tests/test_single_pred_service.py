"""Tests for §Single hourly UP/DOWN predictions (pure-function units)."""

from __future__ import annotations

import pytest

from services.movers_source import Mover, MoversSnapshot
from services.single_pred_service import (
    CORRECT_POINTS,
    PARTICIPATION_POINTS,
    SINGLES_PER_HOUR_FREE,
    SINGLES_PER_HOUR_PREMIUM,
    SinglePrediction,
    SingleSlot,
    _slot_id,
    generate_singles_for_hour,
)


def _mk_snap() -> MoversSnapshot:
    """12 stocks + 12 coins — enough for 10 each per hour."""
    stocks = [
        Mover(t, t, "stock", price, pct) for (t, price, pct) in [
            ("NVDA", 800, 0.12), ("TSLA", 250, -0.08), ("AAPL", 200, 0.07),
            ("AMD", 150, -0.05), ("META", 500, 0.04), ("MSFT", 410, 0.03),
            ("GOOG", 195, 0.06), ("AMZN", 180, -0.04), ("AVGO", 1500, 0.05),
            ("ORCL", 175, 0.02), ("CRM", 290, -0.03), ("ADBE", 480, 0.01),
        ]
    ]
    cryptos = [
        Mover(t, t.replace("-USD", ""), "crypto", price, pct)
        for (t, price, pct) in [
            ("BTC-USD", 70000, 0.10), ("ETH-USD", 3500, -0.06),
            ("SOL-USD", 200, 0.15), ("DOGE-USD", 0.15, 0.20),
            ("AVAX-USD", 35, -0.04), ("MATIC-USD", 0.85, 0.05),
            ("LINK-USD", 18, 0.07), ("DOT-USD", 7.5, -0.02),
            ("ADA-USD", 0.55, 0.08), ("XRP-USD", 0.65, 0.04),
            ("BNB-USD", 600, 0.03), ("TRX-USD", 0.12, 0.06),
        ]
    ]
    return MoversSnapshot(kst_date="2026-05-10", fetched_at="x",
                          stocks=stocks, cryptos=cryptos)


class TestSlotId:
    def test_stock_format(self) -> None:
        assert _slot_id("2026-05-10", 14, "stock", 1) == "2026-05-10-h14-s1"

    def test_coin_format(self) -> None:
        assert _slot_id("2026-05-10", 14, "coin", 1) == "2026-05-10-h14-c1"

    def test_zero_padded_hour(self) -> None:
        assert _slot_id("2026-05-10", 4, "stock", 7) == "2026-05-10-h04-s7"


class TestGenerator:
    def test_generates_20_slots_total(self) -> None:
        """10 stocks + 10 coins per hour."""
        snap = _mk_snap()
        slots = generate_singles_for_hour(snap, "2026-05-10", 14)
        assert len(slots) == 20

    def test_10_each_category(self) -> None:
        snap = _mk_snap()
        slots = generate_singles_for_hour(snap, "2026-05-10", 14)
        stocks = [s for s in slots if s.category == "stock"]
        coins = [s for s in slots if s.category == "coin"]
        assert len(stocks) == 10
        assert len(coins) == 10

    @staticmethod
    def _idx_from_id(slot_id: str) -> int:
        # "2026-05-10-h14-s10" → 10 ; need numeric (not alphabetic) sort
        suffix = slot_id.split("-")[-1]
        return int(suffix[1:])  # strip 's' or 'c' prefix

    def test_first_3_each_are_free(self) -> None:
        snap = _mk_snap()
        slots = generate_singles_for_hour(snap, "2026-05-10", 14)
        stocks = sorted([s for s in slots if s.category == "stock"],
                        key=lambda s: self._idx_from_id(s.id))
        coins = sorted([s for s in slots if s.category == "coin"],
                       key=lambda s: self._idx_from_id(s.id))
        for i, s in enumerate(stocks[:3]):
            assert not s.premium_only, f"stock #{i+1} should be free, got {s.id}"
        for i, s in enumerate(coins[:3]):
            assert not s.premium_only, f"coin #{i+1} should be free, got {s.id}"

    def test_remaining_7_each_are_premium(self) -> None:
        snap = _mk_snap()
        slots = generate_singles_for_hour(snap, "2026-05-10", 14)
        stocks = sorted([s for s in slots if s.category == "stock"],
                        key=lambda s: self._idx_from_id(s.id))
        coins = sorted([s for s in slots if s.category == "coin"],
                       key=lambda s: self._idx_from_id(s.id))
        for i, s in enumerate(stocks[3:]):
            assert s.premium_only, f"stock #{i+4} should be premium, got {s.id}"
        for i, s in enumerate(coins[3:]):
            assert s.premium_only, f"coin #{i+4} should be premium, got {s.id}"

    def test_anchor_set_to_movers_close(self) -> None:
        snap = _mk_snap()
        slots = generate_singles_for_hour(snap, "2026-05-10", 14)
        # First stock slot's anchor should match NVDA's 800
        first_stock = next(s for s in slots if s.id == "2026-05-10-h14-s1")
        assert first_stock.ticker == "NVDA"
        assert first_stock.anchor_price == 800.0
        assert first_stock.last_price == 800.0  # initial = anchor

    def test_resolve_at_one_hour_after_open(self) -> None:
        """Resolve happens 1 hour after open per spec."""
        snap = _mk_snap()
        slots = generate_singles_for_hour(snap, "2026-05-10", 14)
        from datetime import datetime
        for s in slots:
            opens = datetime.fromisoformat(s.open_at_kst)
            resolves = datetime.fromisoformat(s.resolve_at_kst)
            assert (resolves - opens).total_seconds() == 3600


class TestRewardConstants:
    def test_free_per_hour_is_3(self) -> None:
        assert SINGLES_PER_HOUR_FREE == 3

    def test_premium_per_hour_is_10(self) -> None:
        assert SINGLES_PER_HOUR_PREMIUM == 10

    def test_correct_reward(self) -> None:
        # Single is easier than matchup → 20 P (vs matchup's 30 P)
        assert CORRECT_POINTS == 20

    def test_participation_reward(self) -> None:
        assert PARTICIPATION_POINTS == 1


class TestPredictionDataclass:
    def test_includes_user_key_and_anon(self) -> None:
        p = SinglePrediction(user_key="uk", anon_user_id="anon",
                             direction="up", submitted_at="ts")
        assert p.user_key == "uk"
        assert p.anon_user_id == "anon"
        assert p.direction == "up"
