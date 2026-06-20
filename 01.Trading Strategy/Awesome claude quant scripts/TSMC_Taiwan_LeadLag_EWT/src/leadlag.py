"""
leadlag.py
==========
"TSMC 매출 성장률"과 "대만 GDP 성장률" 중 무엇이 선행지표인가?

방법
----
1) 교차상관(cross-correlation): TSMC YoY 를 k개월 시프트시켰을 때
   대만 GDP YoY 와의 상관계수가 최대가 되는 k 를 찾는다.
   k>0 (TSMC 를 미래로 미뤘을 때 상관 최대) => TSMC 가 GDP 를 *선행*.
2) 간이 그레인저 인과(OLS 기반): GDP_t 를 GDP 과거 + TSMC 과거로 회귀하여
   TSMC 과거항의 설명력(증분 R^2)을 본다.
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


def cross_correlation(x: pd.Series, y: pd.Series, max_lag: int = 12) -> pd.DataFrame:
    """x 를 lag 만큼 *선행*시켰을 때 y 와의 상관. lag>0 => x 가 y 를 선행."""
    rows = []
    for lag in range(-max_lag, max_lag + 1):
        xs = x.shift(lag)
        df = pd.concat([xs, y], axis=1).dropna()
        if len(df) > 10:
            r = df.corr().iloc[0, 1]
            rows.append({"lag_months": lag, "corr": r, "n": len(df)})
    return pd.DataFrame(rows)


def granger_like(gdp: pd.Series, tsmc: pd.Series, p: int = 3) -> dict:
    """GDP_t ~ GDP_{t-1..p} 대비 + TSMC_{t-1..p} 추가 시 증분 R^2."""
    d = pd.DataFrame({"gdp": gdp, "tsmc": tsmc}).dropna()
    Y = d["gdp"].values[p:]
    n = len(Y)
    # 제한모형: GDP 자기시차
    Xr = np.column_stack([np.ones(n)] + [d["gdp"].values[p - k:-k][:n] for k in range(1, p + 1)])
    # 확장모형: + TSMC 시차
    Xf = np.column_stack([Xr] + [d["tsmc"].values[p - k:-k][:n] for k in range(1, p + 1)])

    def r2(X, y):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        ss_res = (resid ** 2).sum()
        ss_tot = ((y - y.mean()) ** 2).sum()
        return 1 - ss_res / ss_tot

    r2r, r2f = r2(Xr, Y), r2(Xf, Y)
    return {"r2_restricted": r2r, "r2_full": r2f,
            "incremental_r2_from_tsmc": r2f - r2r, "lags": p, "n": n}


def main():
    df, source = get_data()
    df.to_csv(RESULTS / "panel_data.csv")
    tsmc = df["tsmc_rev_yoy"]
    gdp = df["tw_gdp_yoy"]

    cc = cross_correlation(tsmc, gdp, max_lag=12)
    best = cc.loc[cc["corr"].idxmax()]
    cc.to_csv(RESULTS / "leadlag_crosscorr.csv", index=False)

    gl = granger_like(gdp, tsmc, p=3)

    summary = {
        "data_source": source,
        "best_lag_months": int(best["lag_months"]),
        "best_corr": round(float(best["corr"]), 3),
        "interpretation": (
            "lag>0 이면 TSMC 매출성장률이 대만 GDP 성장률을 선행"
            if best["lag_months"] > 0 else
            "lag<=0 이면 TSMC 가 동행/후행"
        ),
        "granger_like": {k: round(v, 4) if isinstance(v, float) else v
                         for k, v in gl.items()},
    }
    with open(RESULTS / "leadlag_summary.json", "w") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # 차트
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
    ax[0].plot(df.index, tsmc, label="TSMC rev YoY %", color="#0a7d6b")
    ax[0].plot(df.index, gdp, label="Taiwan GDP YoY %", color="#c0392b")
    ax[0].axhline(0, color="grey", lw=.7)
    ax[0].set_title("TSMC revenue vs Taiwan GDP (YoY)")
    ax[0].legend(fontsize=8)
    ax[1].bar(cc["lag_months"], cc["corr"], color="#2c3e50")
    ax[1].axvline(best["lag_months"], color="#e67e22", ls="--",
                  label=f"best lag = {int(best['lag_months'])}m")
    ax[1].set_title("Cross-correlation\n(lag>0: TSMC leads GDP)")
    ax[1].set_xlabel("TSMC lead (months)")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(RESULTS / "leadlag.png", dpi=130)

    print("source:", source)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
