#!/usr/bin/env python3
"""
미국 금융 섹터 LLM 퀀트 백테스팅 시스템
US Financial Sector LLM Quant Backtesting System

Author: Dennis Kim (HoKwang Kim) / Betalabs Inc.
GitHub: github.com/gameworkerkim
ORCID: 0009-0002-0962-2175
기준일: 2026-06-13 | 버전: v2.0

설치 요구사항:
    pip install yfinance pandas numpy matplotlib scipy

사용법:
    python financial_sector_backtest.py
"""

import warnings
warnings.filterwarnings("ignore")

import json
import datetime
import numpy as np
import pandas as pd

# ─────────────────────────────────────────────
# 1. 데이터 수집 (yfinance 사용)
# ─────────────────────────────────────────────
def fetch_price_data(tickers: list, start: str = "2020-01-01", end: str = None) -> pd.DataFrame:
    """
    yfinance로 주가 데이터 수집.
    yfinance 미설치 시 시뮬레이션 데이터 생성.
    """
    if end is None:
        end = datetime.date.today().isoformat()

    try:
        import yfinance as yf
        raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False)
        if isinstance(raw.columns, pd.MultiIndex):
            prices = raw["Close"]
        else:
            prices = raw[["Close"]].rename(columns={"Close": tickers[0]})
        prices = prices.dropna(how="all")
        print(f"[DATA] yfinance로 {len(prices)}일치 실제 데이터 수집 완료.")
        return prices

    except ImportError:
        print("[DATA] yfinance 미설치. 시뮬레이션 데이터 생성 중...")
        return _simulate_prices(tickers, start, end)
    except Exception as e:
        print(f"[DATA] 데이터 수집 오류({e}). 시뮬레이션 데이터 사용.")
        return _simulate_prices(tickers, start, end)


def _simulate_prices(tickers: list, start: str, end: str) -> pd.DataFrame:
    """
    실제 데이터 수집 실패 시 시뮬레이션 데이터 생성.
    각 티커별 대략적 실제 가격 수준 반영.
    """
    dates = pd.bdate_range(start=start, end=end)
    np.random.seed(42)

    # 2020년 초 기준 가격 (실제 근사치)
    base_prices = {
        "XLF": 30.0, "JPM": 135.0, "BAC": 35.0, "WFC": 52.0,
        "V": 210.0, "MA": 310.0, "AXP": 130.0,
        "BRK-B": 220.0, "UNH": 290.0, "PGR": 115.0,
        "BLK": 580.0, "KKR": 32.0, "APO": 40.0,
        "GS": 250.0, "KBE": 47.0, "KRE": 58.0,
    }

    # 연간 기대수익률 및 변동성 (섹터 특성 반영)
    params = {
        "XLF": (0.12, 0.22), "JPM": (0.14, 0.23), "BAC": (0.10, 0.26),
        "WFC": (0.05, 0.27), "V": (0.18, 0.18), "MA": (0.19, 0.19),
        "AXP": (0.13, 0.25), "BRK-B": (0.13, 0.16), "UNH": (0.08, 0.28),
        "PGR": (0.20, 0.21), "BLK": (0.15, 0.22), "KKR": (0.22, 0.28),
        "APO": (0.21, 0.27), "GS": (0.13, 0.26), "KBE": (0.09, 0.28),
        "KRE": (0.07, 0.31),
    }

    data = {}
    n = len(dates)
    dt = 1 / 252

    for t in tickers:
        base = base_prices.get(t, 100.0)
        mu, sigma = params.get(t, (0.10, 0.25))
        drift = (mu - 0.5 * sigma**2) * dt
        shock = sigma * np.sqrt(dt)
        log_returns = drift + shock * np.random.randn(n)
        prices = base * np.exp(np.cumsum(log_returns))
        data[t] = prices

    df = pd.DataFrame(data, index=dates)
    print(f"[DATA] 시뮬레이션 데이터 생성: {len(df)}일치, {len(tickers)}개 종목")
    return df


# ─────────────────────────────────────────────
# 2. 기술적 지표 계산
# ─────────────────────────────────────────────
def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def compute_ma_deviation(prices: pd.Series, window: int = 200) -> pd.Series:
    ma = prices.rolling(window).mean()
    return (prices / ma - 1) * 100


def compute_fear_greed(prices_df: pd.DataFrame, sector_ticker: str = "XLF") -> pd.DataFrame:
    """
    금융 섹터 Fear/Greed 프록시 스코어 계산 (0=Extreme Fear, 100=Extreme Greed)
    7개 지표 균등 가중
    """
    p = prices_df[sector_ticker].dropna()
    results = pd.DataFrame(index=p.index)

    # 1. 모멘텀 (RSI 기반)
    rsi = compute_rsi(p)
    results["rsi_score"] = rsi.clip(0, 100)

    # 2. 이동평균 이격도
    dev200 = compute_ma_deviation(p, 200)
    results["ma_score"] = (dev200 + 30).clip(0, 100) * (100 / 60)
    results["ma_score"] = results["ma_score"].clip(0, 100)

    # 3. 52주 포지션
    high52 = p.rolling(252).max()
    low52 = p.rolling(252).min()
    results["position_score"] = ((p - low52) / (high52 - low52) * 100).clip(0, 100)

    # 4. 단기 모멘텀 (20일)
    mom20 = p.pct_change(20) * 100
    results["momentum_score"] = (mom20 + 20).clip(0, 100) * (100 / 40)
    results["momentum_score"] = results["momentum_score"].clip(0, 100)

    # 5. 변동성 역지표 (낮을수록 Greed)
    vol20 = p.pct_change().rolling(20).std() * np.sqrt(252) * 100
    results["vol_inv_score"] = (100 - vol20.clip(0, 100)).clip(0, 100)

    # 6. 상대강도 (vs 5일 전)
    short_mom = p.pct_change(5) * 100
    results["short_mom_score"] = (short_mom + 5).clip(0, 100) * (100 / 10)
    results["short_mom_score"] = results["short_mom_score"].clip(0, 100)

    # 7. 장기 모멘텀 (60일)
    mom60 = p.pct_change(60) * 100
    results["long_mom_score"] = (mom60 + 25).clip(0, 100) * (100 / 50)
    results["long_mom_score"] = results["long_mom_score"].clip(0, 100)

    score_cols = [c for c in results.columns if c.endswith("_score")]
    results["fear_greed"] = results[score_cols].mean(axis=1)

    def label(x):
        if x < 20: return "Extreme Fear"
        elif x < 40: return "Fear"
        elif x < 60: return "Neutral"
        elif x < 80: return "Greed"
        else: return "Extreme Greed"

    results["fg_label"] = results["fear_greed"].apply(label)
    return results


# ─────────────────────────────────────────────
# 3. FQS/OHS 프록시 계산 (가격 기반)
# ─────────────────────────────────────────────
def compute_fqs_proxy(prices: pd.Series, market: pd.Series) -> pd.Series:
    """
    FQS 프록시: 상대 모멘텀 + 변동성 역수 기반
    실제 펀더멘털 데이터 없이 가격으로 추정
    """
    # 12개월 상대 모멘텀
    ret_12m = prices.pct_change(252)
    mkt_ret_12m = market.pct_change(252)
    rel_mom = ret_12m - mkt_ret_12m

    # 변동성 (낮을수록 안정적 = 높은 FQS)
    vol = prices.pct_change().rolling(63).std() * np.sqrt(252)

    # FQS 프록시: 상대 모멘텀 정규화 + 안정성
    mom_score = rel_mom.rank(pct=True) * 40 + 30  # 30~70 범위
    stab_score = (1 - vol.rank(pct=True)) * 30 + 50  # 50~80 범위

    fqs = (mom_score + stab_score) / 2
    return fqs.clip(20, 90)


def compute_ohs_proxy(prices: pd.Series, window_fast: int = 20, window_slow: int = 200) -> pd.Series:
    """
    OHS 프록시: RSI + 이평 이격 기반 과열도
    """
    rsi = compute_rsi(prices)
    dev = compute_ma_deviation(prices, window_slow)

    # RSI 기여 (RSI 70+ = 고과열)
    rsi_contrib = rsi.clip(30, 90) / 90 * 50

    # 이격 기여 (이격 +20% = 고과열)
    dev_contrib = dev.clip(-20, 40) / 40 * 50

    ohs = (rsi_contrib + dev_contrib).clip(0, 100)
    return ohs


# ─────────────────────────────────────────────
# 4. 사분면 판정 및 시그널 생성
# ─────────────────────────────────────────────
FQS_THRESHOLD = 65
OHS_THRESHOLD = 56

def classify_quadrant(fqs: float, ohs: float) -> str:
    if fqs >= FQS_THRESHOLD and ohs < OHS_THRESHOLD:
        return "Accumulate"
    elif fqs >= FQS_THRESHOLD and ohs >= OHS_THRESHOLD:
        return "Hold/Trim-Wait"
    elif fqs < FQS_THRESHOLD and ohs < OHS_THRESHOLD:
        return "Avoid/Value-Trap"
    else:
        return "Overheated-Speculation"


def generate_signals(prices_df: pd.DataFrame, tickers: list, market_ticker: str = "XLF") -> pd.DataFrame:
    """
    각 종목별 일별 사분면 시그널 생성
    """
    market = prices_df[market_ticker]
    signals = {}

    for t in tickers:
        if t not in prices_df.columns:
            continue
        p = prices_df[t]
        fqs = compute_fqs_proxy(p, market)
        ohs = compute_ohs_proxy(p)
        quadrant = pd.Series(
            [classify_quadrant(f, o) for f, o in zip(fqs, ohs)],
            index=p.index
        )
        signals[t] = quadrant

    return pd.DataFrame(signals)


# ─────────────────────────────────────────────
# 5. 백테스팅 엔진
# ─────────────────────────────────────────────
def backtest_quadrant_strategy(
    prices_df: pd.DataFrame,
    signals_df: pd.DataFrame,
    ticker: str,
    initial_capital: float = 100_000,
    rebalance_freq: str = "W",  # 'D', 'W', 'M'
    transaction_cost: float = 0.001,
) -> dict:
    """
    사분면 기반 전략 백테스팅.
    Accumulate → 1.5x 레버리지 (최대 포지션)
    Hold/Trim  → 0.5x (축소)
    Avoid      → 0.0x (청산)
    Overheated → -0.3x (약간 숏 또는 현금)
    """
    if ticker not in prices_df.columns or ticker not in signals_df.columns:
        return {}

    prices = prices_df[ticker].dropna()
    sigs = signals_df[ticker].reindex(prices.index, method="ffill")

    weight_map = {
        "Accumulate": 1.0,
        "Hold/Trim-Wait": 0.5,
        "Avoid/Value-Trap": 0.0,
        "Overheated-Speculation": 0.0,
    }

    # 리밸런싱 날짜
    if rebalance_freq == "W":
        rebal_dates = prices.resample("W-FRI").last().index
    elif rebalance_freq == "M":
        rebal_dates = prices.resample("ME").last().index
    else:
        rebal_dates = prices.index

    portfolio = pd.Series(index=prices.index, dtype=float)
    cash = initial_capital
    position = 0.0  # 주식 수
    current_weight = 0.0

    prev_price = prices.iloc[0]
    portfolio.iloc[0] = initial_capital

    for i, (date, price) in enumerate(prices.items()):
        if i == 0:
            continue

        # 포트폴리오 가치
        port_value = cash + position * price

        # 리밸런싱 체크
        if date in rebal_dates or i == 1:
            sig = sigs.get(date, "Avoid/Value-Trap")
            target_weight = weight_map.get(sig, 0.0)

            if abs(target_weight - current_weight) > 0.05:  # 5% 이상 변화 시만 리밸
                target_value = port_value * target_weight
                target_shares = target_value / price

                trade_shares = target_shares - position
                trade_cost = abs(trade_shares * price) * transaction_cost

                cash = cash - trade_shares * price - trade_cost
                position = target_shares
                current_weight = target_weight

        portfolio[date] = cash + position * price

    portfolio = portfolio.fillna(method="ffill")

    # 바이앤홀드 비교
    bah = (prices / prices.iloc[0]) * initial_capital

    return {
        "ticker": ticker,
        "strategy": portfolio,
        "buy_and_hold": bah,
        "initial_capital": initial_capital,
    }


# ─────────────────────────────────────────────
# 6. 성과 지표 계산
# ─────────────────────────────────────────────
def calc_performance(returns: pd.Series, risk_free: float = 0.045) -> dict:
    """연율화 성과 지표 계산"""
    if returns.empty or returns.std() == 0:
        return {}

    daily_rf = risk_free / 252
    excess = returns - daily_rf
    trading_days = 252

    cagr = (1 + returns).prod() ** (trading_days / len(returns)) - 1
    vol = returns.std() * np.sqrt(trading_days)
    sharpe = excess.mean() / returns.std() * np.sqrt(trading_days)

    cumulative = (1 + returns).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    mdd = drawdown.min()

    win_rate = (returns > 0).mean()
    calmar = cagr / abs(mdd) if mdd != 0 else np.nan

    return {
        "CAGR": round(cagr * 100, 2),
        "Annual_Volatility": round(vol * 100, 2),
        "Sharpe_Ratio": round(sharpe, 3),
        "Max_Drawdown": round(mdd * 100, 2),
        "Win_Rate": round(win_rate * 100, 2),
        "Calmar_Ratio": round(calmar, 3),
        "Total_Return": round((cumulative.iloc[-1] - 1) * 100, 2),
    }


# ─────────────────────────────────────────────
# 7. 현재 상태 스냅샷 출력
# ─────────────────────────────────────────────
def print_current_snapshot(prices_df: pd.DataFrame, signals_df: pd.DataFrame,
                            fg_df: pd.DataFrame, tickers: list):
    """현재(최신 날짜) 종목별 상태 스냅샷 출력"""
    latest = prices_df.index[-1]

    print("\n" + "=" * 70)
    print(f"  📊 미국 금융 섹터 현황 스냅샷  |  {latest.date()}")
    print("=" * 70)

    # Fear/Greed
    if not fg_df.empty and "fear_greed" in fg_df.columns:
        fg_val = fg_df["fear_greed"].iloc[-1]
        fg_label = fg_df["fg_label"].iloc[-1]
        bar = "█" * int(fg_val / 5) + "░" * (20 - int(fg_val / 5))
        print(f"\n  🎯 섹터 Fear/Greed Score: {fg_val:.1f} / 100  [{fg_label}]")
        print(f"     [{bar}]")
        print(f"     0=Extreme Fear ←────────────→ 100=Extreme Greed")

    # ARDS Phase 추정
    fg_latest = fg_df["fear_greed"].iloc[-1] if not fg_df.empty else 50
    if fg_latest < 30:
        ards = "Phase 3-4 (Recession-Warning / Recession)"
    elif fg_latest < 50:
        ards = "Phase 2-3 (Late-Cycle / Recession-Warning)"
    elif fg_latest < 70:
        ards = "Phase 2 (Late-Cycle)"
    else:
        ards = "Phase 1 (Expansion)"
    print(f"  📈 ARDS Phase 추정: {ards}")

    print("\n" + "-" * 70)
    print(f"  {'티커':<8} {'현재가':>9} {'FQS':>6} {'OHS':>6} {'사분면':<28} {'판정'}")
    print("-" * 70)

    market = prices_df["XLF"] if "XLF" in prices_df.columns else prices_df.iloc[:, 0]

    verdict_map = {
        "Accumulate": "✅ 매수",
        "Hold/Trim-Wait": "⚠️ 중립",
        "Avoid/Value-Trap": "🚨 회피",
        "Overheated-Speculation": "🔴 매도",
    }

    for t in tickers:
        if t not in prices_df.columns:
            continue
        p = prices_df[t]
        price = p.iloc[-1]
        fqs_s = compute_fqs_proxy(p, market)
        ohs_s = compute_ohs_proxy(p)
        fqs_val = fqs_s.iloc[-1] if not fqs_s.empty else 50
        ohs_val = ohs_s.iloc[-1] if not ohs_s.empty else 50
        quad = classify_quadrant(fqs_val, ohs_val)
        verdict = verdict_map.get(quad, "❓ 불명")
        print(f"  {t:<8} ${price:>8.2f}  {fqs_val:>5.1f}  {ohs_val:>5.1f}  {quad:<28} {verdict}")

    print("=" * 70)
    print("  ⚠️  FQS/OHS는 가격 기반 프록시. 실제 펀더멘털 데이터로 검증 필요.")
    print("  ⚠️  본 출력은 투자 권유가 아닙니다. 투자 책임은 본인에게 있습니다.")
    print("=" * 70)


# ─────────────────────────────────────────────
# 8. 백테스팅 결과 출력
# ─────────────────────────────────────────────
def print_backtest_results(results_list: list):
    print("\n" + "=" * 80)
    print("  📈 백테스팅 성과 요약 (사분면 전략 vs Buy & Hold)")
    print("=" * 80)
    print(f"  {'티커':<8} {'전략':<12} {'CAGR%':>8} {'샤프':>7} {'MDD%':>8} {'승률%':>8} {'총수익%':>10}")
    print("-" * 80)

    for res in results_list:
        if not res:
            continue
        t = res["ticker"]
        strat_ret = res["strategy"].pct_change().dropna()
        bah_ret = res["buy_and_hold"].pct_change().dropna()

        strat_perf = calc_performance(strat_ret)
        bah_perf = calc_performance(bah_ret)

        if strat_perf:
            print(f"  {t:<8} {'사분면전략':<12} "
                  f"{strat_perf.get('CAGR',0):>7.1f}% "
                  f"{strat_perf.get('Sharpe_Ratio',0):>7.3f} "
                  f"{strat_perf.get('Max_Drawdown',0):>7.1f}% "
                  f"{strat_perf.get('Win_Rate',0):>7.1f}% "
                  f"{strat_perf.get('Total_Return',0):>9.1f}%")
        if bah_perf:
            print(f"  {t:<8} {'Buy&Hold':<12} "
                  f"{bah_perf.get('CAGR',0):>7.1f}% "
                  f"{bah_perf.get('Sharpe_Ratio',0):>7.3f} "
                  f"{bah_perf.get('Max_Drawdown',0):>7.1f}% "
                  f"{bah_perf.get('Win_Rate',0):>7.1f}% "
                  f"{bah_perf.get('Total_Return',0):>9.1f}%")
        print("  " + "·" * 78)

    print("=" * 80)


# ─────────────────────────────────────────────
# 9. 차트 출력 (matplotlib 선택적)
# ─────────────────────────────────────────────
def plot_results(results_list: list, fg_df: pd.DataFrame, show: bool = True):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.ticker as mtick

        n = min(len(results_list), 4)
        if n == 0:
            return

        fig, axes = plt.subplots(n + 1, 1, figsize=(14, 4 * (n + 1)))
        if n + 1 == 1:
            axes = [axes]

        # Fear/Greed 패널
        ax0 = axes[0]
        if not fg_df.empty and "fear_greed" in fg_df.columns:
            fg = fg_df["fear_greed"].rolling(5).mean()
            ax0.fill_between(fg.index, fg, 50, where=(fg >= 50),
                             color="#2ecc71", alpha=0.4, label="Greed")
            ax0.fill_between(fg.index, fg, 50, where=(fg < 50),
                             color="#e74c3c", alpha=0.4, label="Fear")
            ax0.plot(fg.index, fg, color="#2c3e50", lw=1.5)
            ax0.axhline(50, color="gray", lw=0.8, ls="--")
            ax0.axhline(20, color="#e74c3c", lw=0.8, ls=":", label="Extreme Fear (20)")
            ax0.axhline(80, color="#2ecc71", lw=0.8, ls=":", label="Extreme Greed (80)")
            ax0.set_ylim(0, 100)
            ax0.set_ylabel("Fear/Greed Score")
            ax0.set_title("금융 섹터 Fear/Greed Index (XLF 기반 프록시)")
            ax0.legend(loc="upper right", fontsize=8)
            ax0.yaxis.set_major_formatter(mtick.FormatStrFormatter("%d"))
            ax0.grid(alpha=0.3)

        # 개별 종목 전략 vs BaH
        colors = ["#3498db", "#e67e22", "#9b59b6", "#1abc9c"]
        for i, res in enumerate(results_list[:n]):
            ax = axes[i + 1]
            strat = (res["strategy"] / res["initial_capital"] * 100 - 100)
            bah = (res["buy_and_hold"] / res["initial_capital"] * 100 - 100)
            ax.plot(strat.index, strat, color=colors[i % len(colors)],
                    lw=1.8, label=f"{res['ticker']} 사분면전략")
            ax.plot(bah.index, bah, color="gray", lw=1.2, ls="--", label="Buy & Hold")
            ax.axhline(0, color="black", lw=0.8)
            ax.set_ylabel("누적 수익률 (%)")
            ax.set_title(f"{res['ticker']} — 사분면 전략 vs Buy & Hold")
            ax.legend(loc="upper left", fontsize=9)
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%+.0f%%"))
            ax.grid(alpha=0.3)

        fig.suptitle("미국 금융 섹터 LLM 퀀트 백테스팅 | Dennis Kim / Betalabs Inc.",
                     fontsize=13, fontweight="bold", y=1.01)
        plt.tight_layout()

        output_path = "/mnt/user-data/outputs/financial_backtest_chart.png"
        try:
            plt.savefig(output_path, dpi=120, bbox_inches="tight")
            print(f"\n[CHART] 차트 저장: {output_path}")
        except Exception:
            plt.savefig("financial_backtest_chart.png", dpi=120, bbox_inches="tight")
            print("[CHART] 차트 저장: financial_backtest_chart.png")

        if show:
            try:
                plt.show()
            except Exception:
                pass

    except ImportError:
        print("[CHART] matplotlib 미설치. 차트 생략.")
    except Exception as e:
        print(f"[CHART] 차트 생성 오류: {e}")


# ─────────────────────────────────────────────
# 10. JSON 리포트 저장
# ─────────────────────────────────────────────
def save_json_report(snapshot_data: dict, fg_score: float, fg_label: str):
    report = {
        "report_date": datetime.date.today().isoformat(),
        "author": "Dennis Kim (HoKwang Kim) / Betalabs Inc.",
        "github": "github.com/gameworkerkim",
        "sector_sentiment": {
            "fear_greed_score": round(fg_score, 1),
            "label": fg_label,
            "ards_phase": "Phase 2-3 (Late-Cycle / Recession-Warning 경계)",
        },
        "stock_signals": snapshot_data,
        "disclaimer": "본 리포트는 투자 권유가 아닙니다. 투자 책임은 본인에게 있습니다.",
    }

    output_path = "/mnt/user-data/outputs/financial_sector_report.json"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[REPORT] JSON 리포트 저장: {output_path}")
    except Exception:
        with open("financial_sector_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print("[REPORT] JSON 리포트 저장: financial_sector_report.json")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("\n🏦 미국 금융 섹터 LLM 퀀트 백테스팅 시스템 v2.0")
    print("   Author: Dennis Kim (HoKwang Kim) / Betalabs Inc.")
    print("   기준일:", datetime.date.today().isoformat())
    print("─" * 55)

    # 분석 대상 티커
    universe = [
        "XLF",   # 섹터 ETF (벤치마크)
        "JPM",   # JPMorgan Chase (중립)
        "BAC",   # Bank of America (매수)
        "WFC",   # Wells Fargo (매도/회피)
        "V",     # Visa (중립)
        "MA",    # Mastercard (중립)
        "UNH",   # UnitedHealth (매도)
        "PGR",   # Progressive (매수)
        "GS",    # Goldman Sachs (중립)
        "BLK",   # BlackRock (중립)
        "KKR",   # KKR (매수)
        "APO",   # Apollo (매수)
        "KBE",   # 은행 ETF
        "KRE",   # 지역은행 ETF
    ]

    backtest_tickers = ["XLF", "JPM", "BAC", "UNH"]  # 백테스팅 집중 종목

    # 데이터 수집 (2020-01-01 ~ 현재)
    print("\n[1/5] 가격 데이터 수집 중...")
    prices = fetch_price_data(universe, start="2020-01-01")

    # Fear/Greed 계산
    print("[2/5] Fear/Greed 스코어 계산 중...")
    fg_df = compute_fear_greed(prices, sector_ticker="XLF")

    # 시그널 생성
    print("[3/5] 사분면 시그널 생성 중...")
    signals = generate_signals(prices, universe)

    # 현재 스냅샷 출력
    print_current_snapshot(prices, signals, fg_df, universe)

    # 백테스팅 실행
    print("\n[4/5] 백테스팅 실행 중...")
    results = []
    snapshot_data = {}

    for t in backtest_tickers:
        if t not in prices.columns:
            continue
        res = backtest_quadrant_strategy(
            prices, signals, t,
            initial_capital=100_000,
            rebalance_freq="W",
            transaction_cost=0.001,
        )
        if res:
            results.append(res)

        # 스냅샷용 데이터
        if t in prices.columns:
            market = prices["XLF"]
            fqs_s = compute_fqs_proxy(prices[t], market)
            ohs_s = compute_ohs_proxy(prices[t])
            fqs_val = round(float(fqs_s.iloc[-1]), 1) if not fqs_s.empty else 50.0
            ohs_val = round(float(ohs_s.iloc[-1]), 1) if not ohs_s.empty else 50.0
            quad = classify_quadrant(fqs_val, ohs_val)
            snapshot_data[t] = {
                "price": round(float(prices[t].iloc[-1]), 2),
                "fqs_proxy": fqs_val,
                "ohs_proxy": ohs_val,
                "quadrant": quad,
            }

    # 결과 출력
    if results:
        print_backtest_results(results)

    # 차트 저장
    print("\n[5/5] 차트 생성 중...")
    plot_results(results, fg_df, show=False)

    # JSON 리포트
    fg_final = float(fg_df["fear_greed"].iloc[-1]) if not fg_df.empty else 50.0
    fg_label = fg_df["fg_label"].iloc[-1] if not fg_df.empty else "Neutral"
    save_json_report(snapshot_data, fg_final, fg_label)

    print("\n✅ 분석 완료.")
    print("   ⚠️  본 시스템은 교육·연구 목적이며 투자 권유가 아닙니다.")
    print("   ⚠️  실제 투자 결정 전 전문 투자자문사와 상담하세요.")


if __name__ == "__main__":
    main()
