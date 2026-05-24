#!/usr/bin/env python3
"""
midterm_backtest.py
===================
미국 중간선거 "하락 매수" 전략 백테스트.

목적
----
원본 인포그래픽("중간선거 해 최저점에서 매수하면 1년 뒤 +36%")의 주장을
실제 S&P 500 연간 수익률 데이터로 검증한다. 두 가지 기준으로 측정한다:

  1) IMAGE 방식 : 중간선거 해의 (가상의) 저점에서 매수 → 사후적·이론적 상한
  2) REALISTIC  : 중간선거 해 연말 종가에서 매수 → 그 다음 해 연간 수익률
                  (= 누구나 실제로 실행 가능한 현실적 기준)

핵심 메시지: "1년 뒤 반등"은 사실이지만, 현실적 기준(연말 매수)의 기대치는
인포그래픽의 +36%보다 훨씬 낮으며, 1939년 같은 명백한 실패와
1966/1970/1974 같은 "단기 반등 ≠ 추세 전환" 사례가 존재한다.

데이터 출처: S&P 500 연간 가격수익률(배당 제외 근사), Robert Shiller / Slickcharts /
Macrotrends 공개 데이터 기반. 과거 성과는 미래를 보장하지 않는다.

사용법
------
    python midterm_backtest.py            # 콘솔 표 + 통계 출력
    python midterm_backtest.py --plot     # 차트 PNG도 저장
"""

import argparse
import statistics as st

# ---------------------------------------------------------------------------
# S&P 500 연간 가격 수익률 (%), 연말-연말 기준. 배당 제외 근사치.
# 출처 교차검증: Shiller, Slickcharts, Macrotrends, Seeking Alpha 공개 데이터.
# ---------------------------------------------------------------------------
SP500_ANNUAL = {
    1938: 29.28, 1939: -1.10, 1940: -10.67, 1941: -12.77, 1942: 19.17,
    1943: 25.06, 1944: 19.03, 1945: 35.82, 1946: -8.43, 1947: 5.20,
    1948: 5.70, 1949: 18.30, 1950: 30.81, 1951: 23.68, 1952: 18.15,
    1953: -1.21, 1954: 52.56, 1955: 32.60, 1956: 7.44, 1957: -10.46,
    1958: 43.72, 1959: 12.06, 1960: 0.34, 1961: 26.64, 1962: -8.81,
    1963: 22.61, 1964: 16.42, 1965: 12.40, 1966: -9.97, 1967: 23.80,
    1968: 10.81, 1969: -8.24, 1970: 3.56, 1971: 14.22, 1972: 18.76,
    1973: -14.31, 1974: -25.90, 1975: 37.00, 1976: 23.83, 1977: -6.98,
    1978: 6.51, 1979: 18.52, 1980: 31.74, 1981: -4.70, 1982: 20.42,
    1983: 22.34, 1984: 6.15, 1985: 31.24, 1986: 18.49, 1987: 5.81,
    1988: 16.54, 1989: 31.48, 1990: -3.06, 1991: 30.23, 1992: 7.49,
    1993: 9.97, 1994: 1.33, 1995: 37.20, 1996: 22.68, 1997: 33.10,
    1998: 28.34, 1999: 20.89, 2000: -9.03, 2001: -11.85, 2002: -21.97,
    2003: 28.36, 2004: 10.74, 2005: 4.83, 2006: 15.61, 2007: 5.48,
    2008: -36.55, 2009: 25.94, 2010: 14.82, 2011: 2.10, 2012: 15.89,
    2013: 32.15, 2014: 13.52, 2015: 1.36, 2016: 9.54, 2017: 19.42,
    2018: -6.24, 2019: 28.88, 2020: 16.26, 2021: 26.89, 2022: -19.44,
    2023: 24.23, 2024: 23.31,
}

# 중간선거 연도 (대통령 임기 2년차, 짝수해 중 대선 없는 해)
MIDTERM_YEARS = [
    1938, 1942, 1946, 1950, 1954, 1958, 1962, 1966, 1970, 1974,
    1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014,
    2018, 2022,
]

# 원본 인포그래픽이 주장한 "그 해 최대 손실률"과 "1년 뒤 수익률"(저점 매수 가정).
# 검증/대조용으로만 사용. (이미지 OCR 값)
IMAGE_CLAIM = {
    1950: (-12.0, 41.7), 1954: (-4.4, 51.1), 1958: (-4.4, 41.0),
    1962: (-26.4, 37.5), 1966: (-20.2, 37.3), 1970: (-25.0, 48.9),
    1974: (-35.9, 44.4), 1978: (-12.8, 18.1), 1982: (-13.5, 66.1),
    1986: (-9.4, 44.3), 1990: (-19.2, 33.5), 1994: (-8.5, 18.5),
    1998: (-19.2, 39.8), 2002: (-33.0, 36.1), 2006: (-7.5, 26.2),
    2010: (-15.6, 33.6), 2014: (-7.3, 10.9), 2018: (-19.4, 39.9),
    2022: (-24.5, 23.6),
}


def realistic_backtest():
    """중간선거 해 연말 매수 → 다음 해 연간 수익률. 현실적으로 실행 가능한 기준."""
    rows = []
    for y in MIDTERM_YEARS:
        nxt = y + 1
        if nxt in SP500_ANNUAL:
            rows.append((y, SP500_ANNUAL[nxt]))
    return rows


def describe(values):
    """수익률 리스트의 요약 통계."""
    n = len(values)
    pos = sum(1 for v in values if v > 0)
    return {
        "n": n,
        "mean": st.mean(values),
        "median": st.median(values),
        "min": min(values),
        "max": max(values),
        "stdev": st.pstdev(values),
        "win_rate": 100 * pos / n,
        "positive": pos,
        "negative": n - pos,
    }


def baseline_all_years():
    """비교 기준: 전체 연도(중간선거 다음 해 제외) 평균."""
    nxt_set = {y + 1 for y in MIDTERM_YEARS}
    others = [v for yr, v in SP500_ANNUAL.items() if yr not in nxt_set]
    return describe(others)


def print_report():
    print("=" * 72)
    print(" 미국 중간선거 '하락 매수' 전략 백테스트")
    print(" (S&P 500 연간 가격수익률, 배당 제외 근사 / 과거≠미래)")
    print("=" * 72)

    rows = realistic_backtest()
    vals = [r[1] for r in rows]
    s = describe(vals)

    print("\n[현실적 기준] 중간선거 해 연말 매수 → 다음 해 연간 수익률")
    print("-" * 72)
    print(f"{'선거해':>6} | {'다음해':>6} | {'다음해 수익률':>12} | 결과")
    print("-" * 72)
    for (y, ret) in rows:
        flag = "승" if ret > 0 else "패 ★"
        print(f"{y:>6} | {y+1:>6} | {ret:>11.2f}% | {flag}")
    print("-" * 72)
    print(f"표본 수            : {s['n']}회")
    print(f"승률(플러스)       : {s['win_rate']:.1f}%  ({s['positive']}승 {s['negative']}패)")
    print(f"평균 수익률        : {s['mean']:+.2f}%")
    print(f"중앙값             : {s['median']:+.2f}%")
    print(f"최저 / 최고        : {s['min']:+.2f}% / {s['max']:+.2f}%")
    print(f"표준편차(변동성)   : {s['stdev']:.2f}%p")

    base = baseline_all_years()
    print("\n[비교 기준] 그 외 모든 연도 평균")
    print("-" * 72)
    print(f"평균 {base['mean']:+.2f}%  |  중앙값 {base['median']:+.2f}%  |  승률 {base['win_rate']:.1f}%")
    edge = s["mean"] - base["mean"]
    print(f"→ 중간선거 다음 해 초과수익(평균): {edge:+.2f}%p")

    print("\n[인포그래픽 주장 대조] 이미지의 '1년 뒤 수익률'은 저점 매수 가정치")
    print("-" * 72)
    img_vals = [v[1] for v in IMAGE_CLAIM.values()]
    print(f"이미지 평균 주장   : +{st.mean(img_vals):.1f}%  (저점 매수 = 사후적 상한)")
    print(f"현실적 백테스트    : {s['mean']:+.2f}%  (연말 매수 = 실행 가능)")
    print(f"괴리               : 약 {st.mean(img_vals) - s['mean']:.1f}%p 과장")

    print("\n[전략이 깨진/주의 사례]")
    print("-" * 72)
    print(" 1939 : 다음해(1940) -10.67% — 대공황+2차대전, 명백한 실패")
    print(" 1973 : 1974 -25.90% — 중간선거 다음해가 아니라 '선거 전년→선거해' 약세")
    print(" 1966/1970/1974 : 12개월 반등은 있었으나 secular 약세장 지속")
    print("        (단기 반등 ≠ 추세 전환). 측정 구간의 함정에 유의.")
    print("=" * 72)
    print("\n결론: '1년 뒤 반등' 경향은 통계적으로 실재하나, 인포그래픽의 +36%는")
    print("저점 매수를 가정한 상한선이다. 현실적 기대치는 그보다 낮고, 분산이 크며,")
    print("구조적 위기에서는 깨진다. 따라서 무조건 매수가 아니라 '원인 진단 + 분할매수'.")
    return s, base


def make_plot(s, base):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = realistic_backtest()
    years = [f"{y+1}" for y, _ in rows]
    vals = [r for _, r in rows]
    colors = ["#2E7D32" if v > 0 else "#C00000" for v in vals]

    fig, ax = plt.subplots(figsize=(12, 6))
    xpos = range(len(years))
    ax.bar(xpos, vals, color=colors)
    ax.axhline(0, color="#333", lw=0.8)
    ax.axhline(s["mean"], color="#2E75B6", ls="--", lw=1.2,
               label=f"Post-midterm avg {s['mean']:+.1f}%")
    ax.axhline(base["mean"], color="#888", ls=":", lw=1.2,
               label=f"All other years avg {base['mean']:+.1f}%")
    ax.set_title("Midterm Strategy Backtest: S&P 500 return in the year AFTER each midterm",
                 fontsize=12)
    ax.set_ylabel("Annual return (%)")
    ax.set_xticks(list(xpos))
    ax.set_xticklabels(years, rotation=45, ha="right")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    out = "midterm_backtest.png"
    plt.savefig(out, dpi=130)
    print(f"\n차트 저장: {out}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--plot", action="store_true", help="결과 차트 PNG 저장")
    args = ap.parse_args()
    stats_real, stats_base = print_report()
    if args.plot:
        make_plot(stats_real, stats_base)
