#!/usr/bin/env python3
"""
verify_leadlag.py
=================
가설 검증: "삼성전자+SK하이닉스(KOSPI200의 ~55%)의 추세 확인된 움직임이
KOSPI200 추종 ETF(현물/레버리지/인버스)를 선행(lead)하는가?"

방법:
  1) 봇이 남긴 틱 CSV(ts,code,price)를 고정 그리드로 리샘플(ffill).
  2) 빅2 로그수익률을 지수 가중 합성 → composite(지수 프록시) 수익률.
  3) 각 ETF 수익률과 composite를 lag별로 교차상관.
     - lag>0 에서 상관 피크 → composite가 ETF를 '선행' = 가설 지지 = 차익거래 창.
  4) 피크 상관 lag/계수를 표로 출력.

입력 우선순위: --csv 인자 > ticks_sim.csv(셀프테스트 산출) > ticks.csv(실봇 --record)

실행:
  python verify_leadlag.py
  python verify_leadlag.py --csv ticks.csv --grid 1 --maxlag 30 --ret-window 5
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

# 봇과 동일한 유니버스/가중치(instruments.js와 일치시킬 것).
DRIVERS = {"005930": ("삼성전자", 0.33), "000660": ("SK하이닉스", 0.22)}
TRACKERS = {
    "069500": ("KODEX 200", 1),
    "102110": ("TIGER 200", 1),
    "122630": ("KODEX 레버리지", 2),
    "114800": ("KODEX 인버스", -1),
    "252670": ("KODEX 200선물인버스2X", -2),
}
DRIVER_WSUM = sum(w for _, w in DRIVERS.values())


def default_csv(here):
    for name in ("ticks_sim.csv", "ticks.csv"):
        p = os.path.join(here, name)
        if os.path.exists(p):
            return p
    return None


def load_grid(csv_path, grid_s):
    df = pd.read_csv(csv_path)
    df["ts"] = pd.to_datetime(df["ts"].astype("int64"), unit="ms")
    wide = df.pivot_table(index="ts", columns="code", values="price", aggfunc="last")
    # 코드 컬럼은 문자열로(앞자리 0 보존).
    wide.columns = [str(c).zfill(6) for c in wide.columns]
    grid = wide.resample(f"{grid_s}s").last().ffill().dropna(how="all")
    return grid


def log_returns(series, window):
    return np.log(series).diff(window)


def crosscorr(a, b, lags):
    """corr(a_t, b_{t+lag}) — lag>0 이면 a가 b를 선행."""
    out = []
    for lag in lags:
        if lag >= 0:
            x, y = a.iloc[: len(a) - lag], b.iloc[lag:]
        else:
            x, y = a.iloc[-lag:], b.iloc[: len(b) + lag]
        x, y = x.reset_index(drop=True), y.reset_index(drop=True)
        m = x.notna() & y.notna()
        if m.sum() < 10:
            out.append(np.nan)
        else:
            out.append(np.corrcoef(x[m], y[m])[0, 1])
    return np.array(out)


def backtest(grid, comp, args):
    """비용 차감 event-study 백테스트.

    진입: 시점 t에서 빅2 composite가 entry 이상 추세 + ETF가 아직 못 따라온 gap.
    포지션: ETF가 가야 할 방향(sign(leverage*comp))으로 진입.
    청산: hold초 뒤. 손익 = 방향 × ETF 실현수익 − 왕복비용(수수료+스프레드+슬리피지).
    겹치는 거래 금지(같은 ETF는 hold초 쿨다운).
    """
    rw = args.ret_window
    hold = max(1, args.hold // args.grid)        # 보유: 그리드 스텝 수
    rt_cost_bps = 2 * args.commission_bps + args.spread_bps + args.slippage_bps  # 왕복 비용
    entry = args.entry / 100.0
    entry_gap = args.entry_gap / 100.0

    print("\n=== 비용 차감 백테스트 (event-study) ===")
    print(f"진입 임계 comp≥{args.entry:.2f}% & gap≥{args.entry_gap:.2f}% · 보유 {args.hold}s · "
          f"왕복비용 {rt_cost_bps:.1f}bps(수수료 {args.commission_bps}×2+스프레드 {args.spread_bps}+슬리피지 {args.slippage_bps})")
    print(f"{'ETF':<22}{'거래':>6}{'총bps':>9}{'비용bps':>9}{'순bps':>9}{'승률':>8}{'판정':>10}")
    print("-" * 74)

    summary = []
    for code, (name, lev) in TRACKERS.items():
        if code not in grid.columns:
            continue
        px = grid[code]
        etf_ret = log_returns(px, rw)
        n = len(grid)
        cool_until = -1
        trades = []
        idx = grid.index
        comp_aligned = comp.reindex(idx)
        for i in range(rw, n - hold):
            if i < cool_until:
                continue
            cr = comp_aligned.iloc[i]
            er = etf_ret.iloc[i]
            if not np.isfinite(cr) or not np.isfinite(er):
                continue
            expected = lev * cr
            gap = expected - er
            if abs(cr) < entry or abs(gap) < entry_gap or np.sign(gap) != np.sign(expected):
                continue
            direction = np.sign(expected)
            p0 = px.iloc[i]
            p1 = px.iloc[i + hold]
            if not (np.isfinite(p0) and np.isfinite(p1) and p0 > 0):
                continue
            gross_bps = direction * (p1 / p0 - 1) * 1e4
            net_bps = gross_bps - rt_cost_bps
            trades.append((gross_bps, net_bps))
            cool_until = i + hold

        if not trades:
            print(f"{name:<22}{0:>6}{'-':>9}{'-':>9}{'-':>9}{'-':>8}{'표본부족':>10}")
            continue
        g = np.array([t[0] for t in trades])
        nb = np.array([t[1] for t in trades])
        win = float((nb > 0).mean())
        verdict = "수익" if nb.mean() > 0 else "손실"
        print(f"{name:<22}{len(trades):>6}{g.mean():>9.1f}{rt_cost_bps:>9.1f}"
              f"{nb.mean():>9.1f}{win*100:>7.0f}%{verdict:>10}")
        summary.append((name, len(trades), nb.mean(), nb.sum(), win))

    print("-" * 74)
    if summary:
        net_pos = [s for s in summary if s[2] > 0]
        total_net = sum(s[3] for s in summary)
        print(f"\n순(net) 기준 수익 ETF: {len(net_pos)}/{len(summary)} · 전체 누적 순손익 {total_net:.0f}bps")
        if not net_pos:
            print("→ 비용 차감 후 우위 없음. lead-lag는 존재해도 비용에 잠식되는 전형적 결과.")
        else:
            print("→ 비용 차감 후에도 양(+)의 ETF 존재. 단, MOCK/합성이면 방법론 시연일 뿐 —")
            print("  반드시 실시장 ticks.csv + 실제 호가스프레드로 재검증할 것.")
    print("\n⚠️ 고위험 트레이딩: 단기 차익거래는 빠른 청산·체결 실패·역행 리스크가 크다.")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=None)
    ap.add_argument("--grid", type=int, default=1, help="리샘플 그리드(초)")
    ap.add_argument("--maxlag", type=int, default=30, help="±최대 lag(초)")
    ap.add_argument("--ret-window", type=int, default=5, help="수익률 산출 윈도우(그리드 스텝 수)")
    # 백테스트 파라미터(비용은 bps 단위).
    ap.add_argument("--hold", type=int, default=5, help="보유시간(초)")
    ap.add_argument("--entry", type=float, default=0.12, help="진입 composite 추세 임계(%)")
    ap.add_argument("--entry-gap", type=float, default=0.15, help="진입 gap 임계(%)")
    ap.add_argument("--commission-bps", type=float, default=1.5, help="편도 수수료(bps)")
    ap.add_argument("--spread-bps", type=float, default=5.0, help="호가 스프레드 비용(bps)")
    ap.add_argument("--slippage-bps", type=float, default=2.0, help="슬리피지(bps)")
    ap.add_argument("--no-backtest", action="store_true", help="백테스트 생략")
    args = ap.parse_args()

    csv_path = args.csv or default_csv(here)
    if not csv_path or not os.path.exists(csv_path):
        print("틱 CSV가 없습니다. 먼저 `node selftest.js` 또는 `node bot.js --record`로 생성하세요.")
        sys.exit(1)

    grid = load_grid(csv_path, args.grid)
    have = [c for c in list(DRIVERS) + list(TRACKERS) if c in grid.columns]
    missing = [c for c in list(DRIVERS) + list(TRACKERS) if c not in grid.columns]
    print(f"입력: {os.path.basename(csv_path)}  그리드={args.grid}s  관측치={len(grid)}행")
    if missing:
        print(f"누락 종목(데이터 없음): {missing}")

    # composite 지수 수익률.
    comp = None
    for code, (_, w) in DRIVERS.items():
        if code not in grid.columns:
            continue
        r = log_returns(grid[code], args.ret_window) * (w / DRIVER_WSUM)
        comp = r if comp is None else comp.add(r, fill_value=0)
    if comp is None:
        print("빅2 데이터가 없어 composite를 만들 수 없습니다.")
        sys.exit(1)

    lags = np.arange(-args.maxlag, args.maxlag + 1)
    lag_unit = args.grid  # 초

    print("\n=== lead-lag 교차상관 (composite=삼성+하이닉스 vs 각 ETF) ===")
    print(f"{'ETF':<22}{'배수':>5}{'피크상관':>9}{'피크lag':>9}{'해석':>22}")
    print("-" * 70)
    rows = []
    for code, (name, lev) in TRACKERS.items():
        if code not in grid.columns:
            continue
        etf_ret = log_returns(grid[code], args.ret_window)
        # 인버스/레버리지는 부호·배수 정규화 후 비교.
        norm = etf_ret / lev
        cc = crosscorr(comp.dropna(), norm.dropna(), lags)
        if np.all(np.isnan(cc)):
            continue
        k = int(np.nanargmax(cc))
        peak_lag = int(lags[k]) * lag_unit
        peak = cc[k]
        verdict = "지수 선행(가설지지)" if peak_lag > 0 else ("동시" if peak_lag == 0 else "ETF 선행(역행)")
        print(f"{name:<22}{lev:>5}{peak:>9.3f}{peak_lag:>7}s {verdict:>22}")
        rows.append((name, lev, peak, peak_lag))

    # 종합 판정.
    leads = [r for r in rows if r[3] > 0 and r[2] > 0.3]
    print("-" * 70)
    if leads:
        avg_lag = np.mean([r[3] for r in rows if r[3] > 0])
        print(f"\n판정: {len(leads)}/{len(rows)} ETF에서 composite가 양(+)의 lag로 선행 "
              f"(평균 선행 ≈ {avg_lag:.1f}s, 상관>0.3).")
        print("→ 빅2 추세가 ETF를 선행하는 lead-lag 구조가 데이터에서 확인됨(차익거래 가설 지지).")
    else:
        print("\n판정: 유의한 선행 lag가 관측되지 않음.")
        print("→ 현재 데이터에서는 차익거래 창이 닫혀 있음(실시장에선 LP 차익거래로 흔한 결과).")
    if not args.no_backtest:
        backtest(grid, comp.dropna(), args)

    print("\n주의: 합성/MOCK 데이터의 결과는 '방법론 검증'일 뿐이다. 실거래 판단은")
    print("      실봇 --record 로 모은 실시장 ticks.csv 에 대해 다시 돌려야 한다.")


if __name__ == "__main__":
    main()
