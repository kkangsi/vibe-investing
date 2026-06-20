"""
backtest.py
===========
가설: TSMC 월간 매출은 대만 경제/증시의 *선행지표* 다 (leadlag.py 가 검증).
따라서 TSMC 매출 모멘텀으로 대만 ETF(EWT) 노출을 타이밍하면
단순 매수후보유(Buy&Hold) 대비 위험조정수익을 개선할 수 있는가?

전략 (TSMC-Momentum Timing)
---------------------------
- 신호: TSMC 매출 YoY(%) 의 3개월 변화(가속도, tsmc_mom3).
        * mom3 > 0  -> 반도체 사이클 가속 -> EWT 100% 롱
        * mom3 <= 0 -> 사이클 둔화 -> EWT 50%(중립) 로 축소
- 룩어헤드 방지: 신호는 *전월* 값으로 당월 포지션 결정 (.shift(1)).
- TSMC 월매출은 익월 10일 공시 -> 실거래 가능한 정보. (시차 현실적)
- 비교군: EWT Buy&Hold (항상 100%).

지표: CAGR, 연변동성, Sharpe(rf=0), MDD, 누적수익.
주의: data_source 가 'reconstructed' 면 결과는 *방법론 예시* 이며,
      온라인에서 fetch_real 로 실데이터 교체 후 재실행 권장.
"""
from __future__ import annotations
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
from data_lib import get_data

RESULTS = Path(__file__).resolve().parents[1] / "results"
RESULTS.mkdir(exist_ok=True)


def perf_stats(monthly_ret: pd.Series) -> dict:
    r = monthly_ret.dropna()
    n = len(r)
    cum = (1 + r).prod()
    cagr = cum ** (12 / n) - 1
    vol = r.std() * np.sqrt(12)
    sharpe = (r.mean() * 12) / vol if vol > 0 else np.nan
    eq = (1 + r).cumprod()
    mdd = (eq / eq.cummax() - 1).min()
    return {
        "total_return_%": round((cum - 1) * 100, 2),
        "CAGR_%": round(cagr * 100, 2),
        "vol_ann_%": round(vol * 100, 2),
        "sharpe": round(sharpe, 2),
        "MDD_%": round(mdd * 100, 2),
        "months": int(n),
    }


def main():
    df, source = get_data()
    ret = df["EWT"].pct_change()

    # 신호 (전월 정보로 당월 포지션) — 룩어헤드 방지
    signal = df["tsmc_mom3"].shift(1)
    weight = np.where(signal > 0, 1.0, 0.5)
    weight = pd.Series(weight, index=df.index)

    strat_ret = weight * ret
    bh_ret = ret

    stats = {
        "data_source": source,
        "strategy_TSMC_momentum": perf_stats(strat_ret),
        "benchmark_buy_and_hold": perf_stats(bh_ret),
    }
    # 거래 통계
    pos_changes = int((weight.diff().abs() > 0).sum())
    pct_in_full = float((weight == 1.0).mean())
    stats["turnover_events"] = pos_changes
    stats["pct_time_full_long_%"] = round(pct_in_full * 100, 1)

    with open(RESULTS / "backtest_metrics.json", "w") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # 자산곡선
    eq_s = (1 + strat_ret.fillna(0)).cumprod()
    eq_b = (1 + bh_ret.fillna(0)).cumprod()
    out = pd.DataFrame({"weight": weight, "strat_ret": strat_ret,
                        "bh_ret": bh_ret, "equity_strategy": eq_s,
                        "equity_buyhold": eq_b})
    out.to_csv(RESULTS / "backtest_timeseries.csv")

    fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                           gridspec_kw={"height_ratios": [3, 1]})
    ax[0].plot(eq_b.index, eq_b, label="Buy & Hold EWT", color="#7f8c8d")
    ax[0].plot(eq_s.index, eq_s, label="TSMC-Momentum Timing", color="#0a7d6b", lw=2)
    ax[0].set_title(f"Equity curve (1 = start)   [data source: {source}]")
    ax[0].legend()
    ax[0].grid(alpha=.3)
    ax[1].fill_between(weight.index, weight, step="mid", color="#2980b9", alpha=.4)
    ax[1].set_ylabel("EWT weight")
    ax[1].set_ylim(0, 1.1)
    ax[1].grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(RESULTS / "backtest_equity.png", dpi=130)

    print("source:", source)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
