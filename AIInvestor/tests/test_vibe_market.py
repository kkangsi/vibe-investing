"""§Vibe P2 — 10분 시세 스냅샷 (Yahoo Python 포팅 + Azure 어댑팅) 테스트."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from services.vibe import market_snapshot as ms


@pytest.fixture(autouse=True)
def _reset_memo():
    """각 테스트가 module-level 메모이즈를 오염 없이 시작하도록."""
    ms._memo["t"] = 0.0
    ms._memo["snapshot"] = None
    yield
    ms._memo["t"] = 0.0
    ms._memo["snapshot"] = None


# ──────────────────────────────────────────────────────────────────────────────
# Pure helpers
# ──────────────────────────────────────────────────────────────────────────────
class TestMarketWindow:
    def test_inside_window_returns_true(self) -> None:
        # UTC 18:00 = 한낮 미 장중
        d = datetime(2026, 6, 6, 18, 0, tzinfo=timezone.utc)
        assert ms.is_us_market_window_utc(d) is True

    def test_before_window(self) -> None:
        d = datetime(2026, 6, 6, 12, 59, tzinfo=timezone.utc)
        assert ms.is_us_market_window_utc(d) is False

    def test_after_window(self) -> None:
        d = datetime(2026, 6, 6, 21, 31, tzinfo=timezone.utc)
        assert ms.is_us_market_window_utc(d) is False

    def test_boundary_open(self) -> None:
        d = datetime(2026, 6, 6, 13, 0, tzinfo=timezone.utc)
        assert ms.is_us_market_window_utc(d) is True

    def test_boundary_close(self) -> None:
        d = datetime(2026, 6, 6, 21, 30, tzinfo=timezone.utc)
        assert ms.is_us_market_window_utc(d) is True


class TestPyRound:
    def test_basic(self) -> None:
        assert ms._py_round(1.235, 2) == 1.24

    def test_negative(self) -> None:
        assert ms._py_round(-1.235, 2) == -1.24

    def test_zero_digits(self) -> None:
        assert ms._py_round(42.7, 0) == 43.0


# ──────────────────────────────────────────────────────────────────────────────
# Yahoo parsers
# ──────────────────────────────────────────────────────────────────────────────
class TestQuoteParser:
    def test_valid_chart_meta(self) -> None:
        body = {"chart": {"result": [{"meta": {
            "regularMarketPrice": 100.0,
            "chartPreviousClose": 95.0,
        }}]}}
        q = ms.parse_quote_from_chart(body)
        assert q["price"] == 100.0
        assert q["prevClose"] == 95.0
        assert q["chgPct"] == pytest.approx(5.263, abs=0.01)

    def test_falls_back_to_previous_close(self) -> None:
        body = {"chart": {"result": [{"meta": {
            "regularMarketPrice": 50.0,
            "previousClose": 49.0,
        }}]}}
        q = ms.parse_quote_from_chart(body)
        assert q["prevClose"] == 49.0

    def test_missing_meta_raises(self) -> None:
        with pytest.raises(ValueError):
            ms.parse_quote_from_chart({"chart": {"result": [{}]}})

    def test_zero_prev_close_raises(self) -> None:
        body = {"chart": {"result": [{"meta": {
            "regularMarketPrice": 100.0,
            "chartPreviousClose": 0.0,
        }}]}}
        with pytest.raises(ValueError):
            ms.parse_quote_from_chart(body)


class TestScreenerParser:
    def test_extracts_rows(self) -> None:
        body = {"finance": {"result": [{"quotes": [
            {"symbol": "NVDA", "shortName": "NVIDIA",
             "regularMarketPrice": 150.0,
             "regularMarketChangePercent": 5.5,
             "regularMarketVolume": 100_000_000},
            {"symbol": "AAPL", "longName": "Apple Inc.",
             "regularMarketPrice": 200.0,
             "regularMarketChangePercent": 2.0},
        ]}]}}
        rows = ms.parse_screener(body)
        assert len(rows) == 2
        assert rows[0]["ticker"] == "NVDA"
        assert rows[0]["volume"] == 100_000_000.0
        assert rows[1]["name"] == "Apple Inc."
        assert rows[1]["volume"] == 0.0

    def test_skips_malformed_rows(self) -> None:
        body = {"finance": {"result": [{"quotes": [
            {"symbol": None, "regularMarketPrice": 1.0, "regularMarketChangePercent": 0.0},
            {"symbol": "X", "regularMarketPrice": "not-a-number",
             "regularMarketChangePercent": 0.0},
            {"symbol": "Y", "regularMarketPrice": 1.0,
             "regularMarketChangePercent": 0.5},
        ]}]}}
        rows = ms.parse_screener(body)
        assert [r["ticker"] for r in rows] == ["Y"]

    def test_empty_when_no_result(self) -> None:
        assert ms.parse_screener({"finance": {}}) == []


# ──────────────────────────────────────────────────────────────────────────────
# build_snapshot — 순수 조립
# ──────────────────────────────────────────────────────────────────────────────
class TestBuildSnapshot:
    def _quotes(self, **overrides) -> dict[str, dict[str, float]]:
        base = {}
        # 모든 지수가 +1% 상승 가정
        for s in ms.INDEX_NAMES:
            base[s] = {"price": 100.0, "prevClose": 99.0, "chgPct": 1.0}
        for s in ms.SECTOR_NAMES:
            base[s] = {"price": 50.0, "prevClose": 49.5, "chgPct": 1.0}
        base[ms.VIX_SYMBOL] = {"price": 18.0, "prevClose": 18.0, "chgPct": 0.0}
        base.update(overrides)
        return base

    def test_all_indices_present(self) -> None:
        snap = ms.build_snapshot(self._quotes(), [], [], "2026-06-06T18:00:00+00:00")
        assert len(snap["indices"]) == len(ms.INDEX_NAMES)
        assert {t["ticker"] for t in snap["indices"]} == set(ms.INDEX_NAMES)

    def test_missing_quote_excluded(self) -> None:
        q = self._quotes()
        del q["SPY"]
        snap = ms.build_snapshot(q, [], [], "2026-06-06T18:00:00+00:00")
        tickers = {t["ticker"] for t in snap["indices"]}
        assert "SPY" not in tickers
        assert len(snap["indices"]) == len(ms.INDEX_NAMES) - 1

    def test_vix_extracted(self) -> None:
        snap = ms.build_snapshot(self._quotes(), [], [], "ts")
        assert snap["vix"] == 18.0

    def test_vix_null_when_missing(self) -> None:
        q = self._quotes()
        del q[ms.VIX_SYMBOL]
        snap = ms.build_snapshot(q, [], [], "ts")
        assert snap["vix"] is None

    def test_risk_label_risk_on_when_all_up(self) -> None:
        snap = ms.build_snapshot(self._quotes(), [], [], "ts")
        # 모든 지수 +1% + 모든 섹터 + + VIX 정상
        assert snap["risk_label"] == "RISK_ON"
        assert snap["risk_score"] > 60

    def test_risk_label_risk_off_when_all_down_and_vix_high(self) -> None:
        q = self._quotes()
        for k in list(q):
            if k == ms.VIX_SYMBOL:
                q[k] = {"price": 35.0, "prevClose": 30.0, "chgPct": 16.0}
            else:
                q[k] = {"price": 95.0, "prevClose": 100.0, "chgPct": -5.0}
        snap = ms.build_snapshot(q, [], [], "ts")
        assert snap["risk_label"] == "RISK_OFF"
        assert snap["risk_score"] < 40

    def test_movers_capped_at_10(self) -> None:
        gainers = [{"ticker": f"G{i}", "name": f"G{i}",
                    "price": 10.0, "chgPct": 5.0, "volume": 1000} for i in range(15)]
        snap = ms.build_snapshot(self._quotes(), gainers, [], "ts")
        assert len(snap["movers"]["gainers"]) == 10

    def test_breadth_counts(self) -> None:
        q = self._quotes()
        # 6 sectors up, 5 sectors down
        sector_list = list(ms.SECTOR_NAMES)
        for i, s in enumerate(sector_list):
            q[s] = {"price": 50.0, "prevClose": 50.0,
                    "chgPct": 1.0 if i < 6 else -1.0}
        snap = ms.build_snapshot(q, [], [], "ts")
        assert snap["breadth"]["sectors_up"] == 6
        assert snap["breadth"]["sectors_down"] == 5


# ──────────────────────────────────────────────────────────────────────────────
# refresh_market_snapshot — off-hours skip + mocked-fetch happy path
# ──────────────────────────────────────────────────────────────────────────────
class TestRefreshMarketSnapshot:
    def test_skips_off_hours(self) -> None:
        # UTC 06:00 = 미 장외
        fake_now = datetime(2026, 6, 7, 6, 0, tzinfo=timezone.utc)
        with patch("services.vibe.market_snapshot.datetime") as mock_dt:
            mock_dt.now.return_value = fake_now
            mock_dt.side_effect = lambda *a, **k: datetime(*a, **k)
            result = asyncio.run(ms.refresh_market_snapshot("acct"))
        assert result["skipped"] is True
        assert result["reason"] == "off-hours"

    def test_force_overrides_window(self) -> None:
        fake_now = datetime(2026, 6, 7, 6, 0, tzinfo=timezone.utc)

        async def fake_quotes(session, syms):
            return {s: {"price": 100.0, "prevClose": 99.0, "chgPct": 1.0}
                    for s in syms}

        async def fake_screener(session, scr_id, count=10):
            return [{"ticker": "X", "name": "X", "price": 1.0,
                     "chgPct": 5.0, "volume": 100}]

        async def fake_save(account, path, payload, credential=None):
            pass

        with patch("services.vibe.market_snapshot.datetime") as mock_dt, \
             patch.object(ms, "fetch_all_quotes", side_effect=fake_quotes), \
             patch.object(ms, "_fetch_screener", side_effect=fake_screener), \
             patch("services.vibe.blob_state.save_json", side_effect=fake_save):
            mock_dt.now.return_value = fake_now
            mock_dt.side_effect = lambda *a, **k: datetime(*a, **k)
            result = asyncio.run(ms.refresh_market_snapshot("acct", force=True))
        assert result["skipped"] is False
        assert result["quotes_ok"] > 0

    def test_happy_path_saves_blob_and_returns_summary(self) -> None:
        fake_now = datetime(2026, 6, 6, 18, 0, tzinfo=timezone.utc)

        async def fake_quotes(session, syms):
            return {s: {"price": 100.0 + i, "prevClose": 100.0, "chgPct": float(i)}
                    for i, s in enumerate(syms)}

        async def fake_screener(session, scr_id, count=10):
            return [{"ticker": f"{scr_id}{i}", "name": f"n{i}",
                     "price": 10.0, "chgPct": 7.5 if "gain" in scr_id else -7.5,
                     "volume": 500_000} for i in range(5)]

        saved: list[tuple] = []

        async def fake_save(account, path, payload, credential=None):
            saved.append((path, payload))

        with patch("services.vibe.market_snapshot.datetime") as mock_dt, \
             patch.object(ms, "fetch_all_quotes", side_effect=fake_quotes), \
             patch.object(ms, "_fetch_screener", side_effect=fake_screener), \
             patch("services.vibe.blob_state.save_json", side_effect=fake_save):
            mock_dt.now.return_value = fake_now
            mock_dt.side_effect = lambda *a, **k: datetime(*a, **k)
            result = asyncio.run(ms.refresh_market_snapshot("acct"))

        assert result["skipped"] is False
        assert result["gainers"] == 5
        assert result["losers"] == 5
        # Blob 저장됐는지
        assert len(saved) == 1
        assert saved[0][0] == "market/latest.json"
        assert saved[0][1]["ts"].startswith("2026-06-06T18")
        # Module 캐시 갱신 확인
        assert ms._memo["snapshot"] is not None


class TestGetCachedMarket:
    def test_returns_memo_when_fresh(self) -> None:
        import time as _t
        ms._memo["snapshot"] = {"x": 1}
        ms._memo["t"] = _t.monotonic()  # 방금 갱신
        result = asyncio.run(ms.get_cached_market("acct"))
        assert result == {"x": 1}

    def test_falls_back_to_blob_when_stale(self) -> None:
        async def fake_load(account, path, *, default=None, credential=None):
            return {"from_blob": True}

        # memo 만료 처리: t 를 멀리 보냄
        ms._memo["t"] = 0.0
        ms._memo["snapshot"] = None
        with patch("services.vibe.blob_state.load_json", side_effect=fake_load):
            result = asyncio.run(ms.get_cached_market("acct"))
        assert result == {"from_blob": True}
        # memo 갱신됐어야 함
        assert ms._memo["snapshot"] == {"from_blob": True}

    def test_returns_none_when_no_data(self) -> None:
        async def fake_load(account, path, *, default=None, credential=None):
            return default

        with patch("services.vibe.blob_state.load_json", side_effect=fake_load):
            result = asyncio.run(ms.get_cached_market("acct"))
        assert result is None
