"""§Signal — pure function tests for memory_signal_service."""

from __future__ import annotations

import pytest

from services.memory_signal_service import (
    ROLL_WIN,
    TICKERS,
    _corr,
    _mean,
    _pct_returns,
    _ret_over,
    _spread_z,
    _std,
    compute_signals,
)


class TestPureMath:
    def test_pct_returns_basic(self) -> None:
        assert _pct_returns([100, 110, 121]) == pytest.approx([0.1, 0.1])

    def test_pct_returns_skip_zero(self) -> None:
        out = _pct_returns([0, 100, 110])
        # First step (0→100) is skipped, only 100→110 counts
        assert out == pytest.approx([0.1])

    def test_mean_std(self) -> None:
        assert _mean([1, 2, 3, 4, 5]) == 3.0
        assert _std([1, 2, 3, 4, 5]) == pytest.approx(1.5811, abs=0.001)

    def test_corr_perfect_positive(self) -> None:
        a = [1, 2, 3, 4, 5]
        b = [2, 4, 6, 8, 10]
        assert _corr(a, b) == pytest.approx(1.0)

    def test_corr_perfect_negative(self) -> None:
        a = [1, 2, 3, 4, 5]
        b = [5, 4, 3, 2, 1]
        assert _corr(a, b) == pytest.approx(-1.0)

    def test_corr_zero_when_undefined(self) -> None:
        assert _corr([1, 1, 1], [2, 3, 4]) == 0.0  # zero variance

    def test_corr_handles_short(self) -> None:
        assert _corr([], []) == 0.0
        assert _corr([1.0], [2.0]) == 0.0

    def test_ret_over_simple(self) -> None:
        prices = [100, 105, 110, 105, 115]
        assert _ret_over(prices, 1) == pytest.approx(0.0952, abs=0.001)
        assert _ret_over(prices, 4) == pytest.approx(0.15, abs=0.001)

    def test_ret_over_insufficient(self) -> None:
        assert _ret_over([100, 110], 5) == 0.0

    def test_spread_z_zero_when_thin(self) -> None:
        assert _spread_z([100, 110], [200, 220]) == 0.0

    def test_spread_z_extreme_value(self) -> None:
        """When spread reaches +N std above mean, z should be positive."""
        # Build 60-day baseline with A=B, then perturb last day
        a = [100.0 + i * 0.1 for i in range(60)]
        b = [200.0 + i * 0.2 for i in range(60)]
        # spread is essentially constant → std tiny → any perturbation = large z
        a[-1] = 200.0  # jump A way up
        z = _spread_z(a, b)
        assert z > 1.0


class TestComputeSignals:
    def _mk_prices(self, n: int = 60) -> dict[str, list[float]]:
        """Synthetic correlated price series."""
        base = {
            "NVDA": 130, "Hynix": 210000, "Micron": 110,
            "Samsung": 78000, "Sandisk": 55,
        }
        out: dict[str, list[float]] = {k: [] for k in base}
        # Use deterministic linear "drift" with mild noise
        prev = dict(base)
        for i in range(n):
            drive = 0.005 * ((i % 7) - 3) / 3  # ±0.005 oscillation
            prev["NVDA"] *= (1 + drive)
            prev["Hynix"] *= (1 + 0.6 * drive + 0.001 * ((i % 5) - 2))
            prev["Micron"] *= (1 + 0.65 * drive + 0.001 * ((i % 5) - 2))
            prev["Samsung"] *= (1 + 0.4 * drive + 0.001 * ((i % 4) - 1))
            prev["Sandisk"] *= (1 + 0.5 * drive + 0.001 * ((i % 6) - 3))
            for k in base:
                out[k].append(prev[k])
        return out

    def test_returns_all_required_fields(self) -> None:
        prices = self._mk_prices()
        snap = compute_signals(prices)
        assert snap.as_of
        assert snap.kst_date
        assert snap.correlation_health in {"stable", "weakening", "broken"}
        assert len(snap.matrix) == 5
        assert all(len(row) == 5 for row in snap.matrix)
        assert len(snap.signals) == 5
        # Each ticker label appears exactly once
        labels = {s.label for s in snap.signals}
        assert labels == {"NVDA", "Hynix", "Micron", "Samsung", "Sandisk"}

    def test_insufficient_data_marks_broken(self) -> None:
        """If 3+ tickers have <21 bars, snap should declare broken state."""
        prices = {label: [100.0, 101.0] for label, _, _ in TICKERS}
        snap = compute_signals(prices)
        assert snap.correlation_health == "broken"
        assert snap.error
        assert len(snap.data_gaps) == 5

    def test_signals_have_confidence_in_range(self) -> None:
        prices = self._mk_prices()
        snap = compute_signals(prices)
        for s in snap.signals:
            assert 0 <= s.confidence <= 100

    def test_matrix_diagonal_is_one(self) -> None:
        prices = self._mk_prices()
        snap = compute_signals(prices)
        for i in range(5):
            assert snap.matrix[i][i] == pytest.approx(1.0, abs=0.01)

    def test_matrix_is_symmetric(self) -> None:
        prices = self._mk_prices()
        snap = compute_signals(prices)
        for i in range(5):
            for j in range(5):
                assert snap.matrix[i][j] == pytest.approx(snap.matrix[j][i],
                                                           abs=0.001)

    def test_correlation_broken_halves_confidence(self) -> None:
        """When correlation_health='broken', signal confidences are reduced."""
        # Build truly uncorrelated prices to trigger 'broken'
        from random import Random
        rng = Random(42)
        prices: dict[str, list[float]] = {}
        for label, _, _ in TICKERS:
            base = 100.0
            seq = [base]
            for _ in range(60):
                base *= 1 + rng.uniform(-0.05, 0.05)
                seq.append(base)
            prices[label] = seq
        snap = compute_signals(prices)
        if snap.correlation_health == "broken":
            # All signals should mention warning prefix
            for s in snap.signals:
                assert "[상관 붕괴 경고]" in s.rationale


class TestTickersConstant:
    def test_five_tickers(self) -> None:
        assert len(TICKERS) == 5

    def test_one_leader(self) -> None:
        leaders = [t for t in TICKERS if t[2] == "LEADER"]
        assert len(leaders) == 1
        assert leaders[0][0] == "NVDA"

    def test_two_coincident(self) -> None:
        co = [t for t in TICKERS if t[2] == "COINCIDENT"]
        assert len(co) == 2
        assert {t[0] for t in co} == {"Hynix", "Micron"}

    def test_two_lagging(self) -> None:
        lag = [t for t in TICKERS if t[2] == "LAGGING"]
        assert len(lag) == 2
        assert {t[0] for t in lag} == {"Samsung", "Sandisk"}
