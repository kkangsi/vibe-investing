"""§Signal — AI 메모리 공급망 상관관계 분석 + 매매 신호.

대상: NVDA(리더), 000660.KS(SK하이닉스), 005930.KS(삼성전자), MU(마이크론), SNDK(샌디스크)
공급망 시계:
  - LEADER (선행): NVDA — AI GPU 수요의 원천
  - COINCIDENT (동행): Hynix / Micron — HBM/DRAM 사이클 직접 노출
  - LAGGING/REVERTING (후행/회귀): Samsung / Sandisk

처리:
  1) 90일 가격 batch 다운로드 (yfinance)
  2) 60일 rolling 상관 + 일간 수익률 행렬
  3) Samsung/Hynix, Sandisk/Micron 로그-스프레드 z-score
  4) 휴리스틱 신호 (llm_trading_prompt.md §시그널 로직):
       - NVDA +2% & corr>0.4 → Hynix/Micron BUY
       - Samsung/Hynix |z|>1.5 → 페어 매매
       - MU 20일 +15% & SNDK 20일 <5% → SNDK 추격 BUY
       - 60일 corr<0.25 → "broken" 으로 모든 신호 신뢰도 -50%
  5) blob signal-cache/<KST_date>-<hour>.json 캐시 (30분 cron)

면책: 교육/연구용. 실투자 자문 아님 — 응답에 disclaimer 동봉.
"""

from __future__ import annotations

import asyncio
import json
import logging
import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Literal

logger = logging.getLogger(__name__)

CONTAINER = "signal-cache"

# Ticker definitions — order matters for the 5x5 correlation matrix render
TICKERS: list[tuple[str, str, str]] = [
    # (label, yf_ticker, role)
    ("NVDA",     "NVDA",       "LEADER"),
    ("Hynix",    "000660.KS",  "COINCIDENT"),
    ("Micron",   "MU",         "COINCIDENT"),
    ("Samsung",  "005930.KS",  "LAGGING"),
    ("Sandisk",  "SNDK",       "LAGGING"),
]

ROLL_WIN = 60        # 일간 rolling correlation 윈도우
LOOKBACK_DAYS = 120  # yfinance fetch 범위 (60d + 버퍼)

# ──────────────────────────────────────────────────────────────────────────────
# Data classes
# ──────────────────────────────────────────────────────────────────────────────
Action = Literal["BUY", "SELL", "HOLD"]
Health = Literal["stable", "weakening", "broken"]


@dataclass
class TickerSignal:
    label: str
    role: str
    action: Action
    confidence: int          # 0–100
    rationale: str
    last_price: float
    ret_1d_pct: float
    ret_5d_pct: float
    ret_20d_pct: float


@dataclass
class PairTrade:
    long: str
    short: str
    z_score: float
    confidence: int
    rationale: str


@dataclass
class MemorySignalSnapshot:
    as_of: str               # ISO UTC
    kst_date: str            # YYYY-MM-DD KST
    correlation_health: Health
    matrix: list[list[float]]   # 5×5 correlation, NaN→0
    z_samsung_hynix: float
    z_sandisk_micron: float
    signals: list[TickerSignal] = field(default_factory=list)
    pairs: list[PairTrade] = field(default_factory=list)
    data_gaps: list[str] = field(default_factory=list)
    error: str = ""


# ──────────────────────────────────────────────────────────────────────────────
# Math helpers (pure functions, no external deps)
# ──────────────────────────────────────────────────────────────────────────────
def _pct_returns(prices: list[float]) -> list[float]:
    """Daily simple returns. Skips invalid (zero/None)."""
    out = []
    for i in range(1, len(prices)):
        if prices[i - 1] and prices[i - 1] > 0:
            out.append((prices[i] - prices[i - 1]) / prices[i - 1])
    return out


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def _std(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = _mean(xs)
    var = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return math.sqrt(var)


def _corr(a: list[float], b: list[float]) -> float:
    """Pearson correlation, returns 0 if undefined."""
    n = min(len(a), len(b))
    if n < 2:
        return 0.0
    x, y = a[-n:], b[-n:]
    mx, my = _mean(x), _mean(y)
    num = sum((x[i] - mx) * (y[i] - my) for i in range(n))
    dx = sum((x[i] - mx) ** 2 for i in range(n))
    dy = sum((y[i] - my) ** 2 for i in range(n))
    if dx <= 0 or dy <= 0:
        return 0.0
    return num / math.sqrt(dx * dy)


def _ret_over(prices: list[float], k: int) -> float:
    """k-day return as fraction. Returns 0.0 if insufficient data."""
    if len(prices) <= k:
        return 0.0
    base = prices[-1 - k]
    if base <= 0:
        return 0.0
    return (prices[-1] - base) / base


def _spread_z(pa: list[float], pb: list[float], win: int = 60) -> float:
    """log-spread z-score: log(A) - β·log(B), z=(spread - μ)/σ.

    Returns 0.0 if data insufficient or undefined.
    """
    n = min(len(pa), len(pb))
    if n < max(10, win // 2):
        return 0.0
    a = pa[-n:]
    b = pb[-n:]
    # Reject zero/negative prices
    if any(x <= 0 for x in a) or any(x <= 0 for x in b):
        return 0.0
    la = [math.log(x) for x in a]
    lb = [math.log(x) for x in b]
    ma, mb = _mean(la), _mean(lb)
    cov = sum((la[i] - ma) * (lb[i] - mb) for i in range(n))
    varb = sum((lb[i] - mb) ** 2 for i in range(n))
    if varb <= 0:
        return 0.0
    beta = cov / varb
    spread = [la[i] - beta * lb[i] for i in range(n)]
    sm = _mean(spread)
    ss = _std(spread)
    if ss <= 0:
        return 0.0
    return (spread[-1] - sm) / ss


# ──────────────────────────────────────────────────────────────────────────────
# yfinance batch fetch
# ──────────────────────────────────────────────────────────────────────────────
def _fetch_prices_sync() -> dict[str, list[float]]:
    """Download last LOOKBACK_DAYS days of close prices for all 5 tickers."""
    import yfinance as yf
    yf_tickers = [t[1] for t in TICKERS]
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=LOOKBACK_DAYS + 14)  # weekend buffer
    out: dict[str, list[float]] = {}
    try:
        df = yf.download(yf_tickers, start=start.isoformat(),
                         end=(end + timedelta(days=1)).isoformat(),
                         auto_adjust=True, progress=False, threads=True,
                         group_by="ticker")
    except Exception:
        logger.exception("yfinance batch fetch failed")
        return {}

    for label, ticker, _role in TICKERS:
        try:
            if len(yf_tickers) == 1:
                closes = df["Close"].dropna()
            else:
                closes = df[ticker]["Close"].dropna()
            out[label] = [float(v) for v in closes.tolist() if v > 0]
        except (KeyError, IndexError, ValueError):
            out[label] = []
    return out


async def fetch_prices() -> dict[str, list[float]]:
    return await asyncio.to_thread(_fetch_prices_sync)


# ──────────────────────────────────────────────────────────────────────────────
# Signal heuristics — matches llm_trading_prompt.md §시그널 로직
# ──────────────────────────────────────────────────────────────────────────────
def _propagate_lead(follower: str, nvda_ret_1d: float, correlation: float
                    ) -> tuple[Action, int, str]:
    """NVDA 선행 → 동행 종목 ouropagation."""
    if nvda_ret_1d > 0.02 and correlation > 0.4:
        conf = min(85, int(correlation * 100))
        return ("BUY", conf,
                f"NVDA +{nvda_ret_1d*100:.1f}% 선행, 상관 {correlation:.2f} "
                f"→ 익일 추종 가능성")
    if nvda_ret_1d < -0.02 and correlation > 0.4:
        conf = min(85, int(correlation * 100))
        return ("SELL", conf,
                f"NVDA {nvda_ret_1d*100:.1f}% 하락 선행 위험")
    return ("HOLD", 40, "선행 신호 미약 또는 상관 약화")


def compute_signals(prices: dict[str, list[float]]) -> MemorySignalSnapshot:
    """Build the snapshot from raw price series. Pure function (no IO)."""
    now_utc = datetime.now(timezone.utc)
    kst = now_utc + timedelta(hours=9)

    gaps: list[str] = []
    for label, _, _ in TICKERS:
        if len(prices.get(label, [])) < 21:
            gaps.append(label)

    # If too many gaps, return error snapshot
    if len(gaps) >= 3:
        return MemorySignalSnapshot(
            as_of=now_utc.isoformat(timespec="seconds"),
            kst_date=kst.date().isoformat(),
            correlation_health="broken",
            matrix=[[0.0] * 5 for _ in range(5)],
            z_samsung_hynix=0.0, z_sandisk_micron=0.0,
            data_gaps=gaps,
            error=f"insufficient_data: {len(gaps)} tickers under 21 bars",
        )

    rets: dict[str, list[float]] = {
        label: _pct_returns(prices.get(label, []))
        for label, _, _ in TICKERS
    }

    # 5×5 correlation matrix
    labels = [t[0] for t in TICKERS]
    matrix: list[list[float]] = []
    for a in labels:
        row = []
        for b in labels:
            row.append(round(_corr(rets[a], rets[b]), 3))
        matrix.append(row)

    # Health: NVDA↔Hynix 60-day correlation
    c_nh = _corr(rets["NVDA"][-ROLL_WIN:], rets["Hynix"][-ROLL_WIN:])
    health: Health = (
        "stable" if c_nh > 0.45
        else "weakening" if c_nh > 0.25
        else "broken"
    )

    # Spread z-scores
    z_sh = round(_spread_z(prices["Samsung"], prices["Hynix"]), 2)
    z_sm = round(_spread_z(prices["Sandisk"], prices["Micron"]), 2)

    # Returns
    nvda_d1 = _ret_over(prices["NVDA"], 1)
    nvda_d5 = _ret_over(prices["NVDA"], 5)
    nvda_d20 = _ret_over(prices["NVDA"], 20)
    mu_d20 = _ret_over(prices["Micron"], 20)
    sndk_d20 = _ret_over(prices["Sandisk"], 20)

    def _last(p: list[float]) -> float:
        return float(p[-1]) if p else 0.0

    # Per-ticker signals
    signals: list[TickerSignal] = []

    # NVDA itself — momentum gauge
    if nvda_d20 > 0.15:
        nv_act, nv_conf, nv_why = ("HOLD", 50,
            f"20일 +{nvda_d20*100:.1f}% — 과열 주의, 신규 진입 자제")
    elif nvda_d5 > 0:
        nv_act, nv_conf, nv_why = ("BUY", 55,
            f"5일 +{nvda_d5*100:.1f}% 상승 추세, 수요 원천")
    else:
        nv_act, nv_conf, nv_why = ("HOLD", 40, "선행 모멘텀 둔화")
    signals.append(TickerSignal(
        label="NVDA", role="LEADER", action=nv_act, confidence=nv_conf,
        rationale=nv_why, last_price=_last(prices["NVDA"]),
        ret_1d_pct=round(nvda_d1 * 100, 2),
        ret_5d_pct=round(nvda_d5 * 100, 2),
        ret_20d_pct=round(nvda_d20 * 100, 2),
    ))

    # Hynix — coincident, propagates from NVDA
    c_nh_full = _corr(rets["NVDA"], rets["Hynix"])
    h_act, h_conf, h_why = _propagate_lead("Hynix", nvda_d1, c_nh_full)
    signals.append(TickerSignal(
        label="Hynix", role="COINCIDENT", action=h_act, confidence=h_conf,
        rationale=h_why, last_price=_last(prices["Hynix"]),
        ret_1d_pct=round(_ret_over(prices["Hynix"], 1) * 100, 2),
        ret_5d_pct=round(_ret_over(prices["Hynix"], 5) * 100, 2),
        ret_20d_pct=round(_ret_over(prices["Hynix"], 20) * 100, 2),
    ))

    # Micron — coincident
    c_nm_full = _corr(rets["NVDA"], rets["Micron"])
    m_act, m_conf, m_why = _propagate_lead("Micron", nvda_d1, c_nm_full)
    signals.append(TickerSignal(
        label="Micron", role="COINCIDENT", action=m_act, confidence=m_conf,
        rationale=m_why, last_price=_last(prices["Micron"]),
        ret_1d_pct=round(_ret_over(prices["Micron"], 1) * 100, 2),
        ret_5d_pct=round(_ret_over(prices["Micron"], 5) * 100, 2),
        ret_20d_pct=round(_ret_over(prices["Micron"], 20) * 100, 2),
    ))

    # Samsung — lagging, spread reversion
    if z_sh > 1.5:
        s_act, s_conf, s_why = ("SELL", 65,
            f"삼성/하이닉스 z={z_sh:.2f} 과대 — 평균 회귀 매도")
    elif z_sh < -1.5:
        s_act, s_conf, s_why = ("BUY", 65,
            f"삼성/하이닉스 z={z_sh:.2f} 과소 — 평균 회귀 매수")
    else:
        s_act, s_conf, s_why = ("HOLD", 45, "스프레드 중립 범위")
    signals.append(TickerSignal(
        label="Samsung", role="LAGGING", action=s_act, confidence=s_conf,
        rationale=s_why, last_price=_last(prices["Samsung"]),
        ret_1d_pct=round(_ret_over(prices["Samsung"], 1) * 100, 2),
        ret_5d_pct=round(_ret_over(prices["Samsung"], 5) * 100, 2),
        ret_20d_pct=round(_ret_over(prices["Samsung"], 20) * 100, 2),
    ))

    # Sandisk — lagging, NAND chase
    if mu_d20 > 0.15 and sndk_d20 < 0.05:
        sn_act, sn_conf, sn_why = ("BUY", 60,
            f"MU 20일 +{mu_d20*100:.1f}% 대비 SNDK +{sndk_d20*100:.1f}% "
            f"후행 — NAND 따라잡기 추격 매수")
    elif z_sm > 1.5:
        sn_act, sn_conf, sn_why = ("SELL", 58,
            f"SNDK/MU z={z_sm:.2f} 과대 — 회귀 매도")
    else:
        sn_act, sn_conf, sn_why = ("HOLD", 45, "NAND 사이클 중립")
    signals.append(TickerSignal(
        label="Sandisk", role="LAGGING", action=sn_act, confidence=sn_conf,
        rationale=sn_why, last_price=_last(prices["Sandisk"]),
        ret_1d_pct=round(_ret_over(prices["Sandisk"], 1) * 100, 2),
        ret_5d_pct=round(_ret_over(prices["Sandisk"], 5) * 100, 2),
        ret_20d_pct=round(_ret_over(prices["Sandisk"], 20) * 100, 2),
    ))

    # Pair trades
    pairs: list[PairTrade] = []
    if abs(z_sh) > 1.5:
        pairs.append(PairTrade(
            long="Hynix" if z_sh > 0 else "Samsung",
            short="Samsung" if z_sh > 0 else "Hynix",
            z_score=z_sh,
            confidence=min(80, int(abs(z_sh) * 35)),
            rationale="삼성/하이닉스 로그-스프레드 평균 회귀",
        ))
    if abs(z_sm) > 1.5:
        pairs.append(PairTrade(
            long="Micron" if z_sm > 0 else "Sandisk",
            short="Sandisk" if z_sm > 0 else "Micron",
            z_score=z_sm,
            confidence=min(75, int(abs(z_sm) * 30)),
            rationale="SNDK/MU NAND 스프레드 평균 회귀",
        ))

    # Correlation broken → halve all confidences
    if health == "broken":
        for s in signals:
            s.confidence = max(20, s.confidence // 2)
            s.rationale = f"[상관 붕괴 경고] {s.rationale}"
        for p in pairs:
            p.confidence = max(15, p.confidence // 2)

    return MemorySignalSnapshot(
        as_of=now_utc.isoformat(timespec="seconds"),
        kst_date=kst.date().isoformat(),
        correlation_health=health,
        matrix=matrix,
        z_samsung_hynix=z_sh,
        z_sandisk_micron=z_sm,
        signals=signals,
        pairs=pairs,
        data_gaps=gaps,
    )


# ──────────────────────────────────────────────────────────────────────────────
# Blob cache
# ──────────────────────────────────────────────────────────────────────────────
def _cache_path() -> str:
    """signal-cache/<KST_date>-h<HH>.json — 30분 단위로 hour만 카운트."""
    kst = datetime.now(timezone.utc) + timedelta(hours=9)
    return f"{kst.date().isoformat()}-h{kst.hour:02d}.json"


def _latest_path() -> str:
    """signal-cache/latest.json — 항상 최신 스냅샷 (read fast-path)."""
    return "latest.json"


async def refresh_memory_signal(account_name: str, credential=None
                                ) -> MemorySignalSnapshot:
    """Fetch prices + compute signals + write to blob. Returns snapshot."""
    from azure.identity.aio import DefaultAzureCredential
    from azure.storage.blob.aio import BlobServiceClient

    prices = await fetch_prices()
    snap = compute_signals(prices)
    body = json.dumps(asdict(snap), ensure_ascii=False).encode("utf-8")
    creds = credential or DefaultAzureCredential()
    try:
        async with BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=creds,
        ) as svc:
            container = svc.get_container_client(CONTAINER)
            try:
                await container.create_container()
            except Exception:
                pass
            await container.get_blob_client(_cache_path()).upload_blob(
                body, overwrite=True)
            await container.get_blob_client(_latest_path()).upload_blob(
                body, overwrite=True)
    except Exception:
        logger.exception("refresh_memory_signal blob write failed")
    finally:
        if credential is None and hasattr(creds, "close"):
            await creds.close()
    return snap


async def get_cached_signal(account_name: str, credential=None
                            ) -> MemorySignalSnapshot | None:
    """Read latest.json. Returns None if not yet refreshed."""
    from azure.core.exceptions import ResourceNotFoundError
    from azure.identity.aio import DefaultAzureCredential
    from azure.storage.blob.aio import BlobServiceClient

    creds = credential or DefaultAzureCredential()
    try:
        async with BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=creds,
        ) as svc:
            bc = svc.get_blob_client(CONTAINER, _latest_path())
            try:
                body = await (await bc.download_blob()).readall()
            except ResourceNotFoundError:
                return None
    finally:
        if credential is None and hasattr(creds, "close"):
            await creds.close()
    data = json.loads(body)
    signals = [TickerSignal(**s) for s in data.get("signals", [])]
    pairs = [PairTrade(**p) for p in data.get("pairs", [])]
    return MemorySignalSnapshot(
        as_of=data["as_of"], kst_date=data["kst_date"],
        correlation_health=data["correlation_health"],
        matrix=data["matrix"],
        z_samsung_hynix=data["z_samsung_hynix"],
        z_sandisk_micron=data["z_sandisk_micron"],
        signals=signals, pairs=pairs,
        data_gaps=data.get("data_gaps", []),
        error=data.get("error", ""),
    )
