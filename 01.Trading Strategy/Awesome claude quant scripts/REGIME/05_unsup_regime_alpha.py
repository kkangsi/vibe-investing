"""
05_unsup_regime_alpha.py
========================
두 가지 확장:
  (A) 비지도 레짐: 거시 변수에서 KMeans와 HMM이 '스스로' 국면을 찾게 한다.
      (앞서 사람이 정한 2축 경계 대신, 데이터 구조가 레짐을 결정)
  (B) 베타 중립 알파: 각 종목 수익률을 QQQ로 회귀해 시장 부분을 제거하고,
      남은 '잔차(종목 고유 알파)'에 레짐을 적용한다.
      핵심 질문: 시장 전체가 아니라 '이 종목만의' 초과수익이 레짐에 따라 달라지나?

정직성 원칙: 잔차 알파가 레짐에 무관하면(대부분 그럴 것), 그렇게 말한다.
"""
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from hmmlearn import hmm

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 40)
np.random.seed(42)

DATA = "/home/claude/market_data_2020_2026.csv"
MACRO = ["DXY", "UST10Y", "CPI_YoY", "ConsumerSentiment", "WTI"]
M7 = ["AAPL","MSFT","GOOGL","AMZN","META","NVDA","TSLA"]
INFRA = ["AVGO","AMD","TSM","ASML","MU","VRT","ETN","SMCI","DLR","GEV"]
STOCKS = M7 + INFRA
MKT = "QQQ"

df = pd.read_csv(DATA, parse_dates=["Date"], index_col="Date")

# ============================================================
# (A) 비지도 레짐 추출
# ============================================================
def macro_features():
    """레짐 분류용 거시 피처: 추세(60d)로 정규화."""
    f = pd.DataFrame(index=df.index)
    f["rate_trend"] = df["UST10Y"].diff(60)
    f["dollar_trend"] = df["DXY"].pct_change(60)
    f["wti_trend"] = df["WTI"].pct_change(60)
    f["cpi_level"] = df["CPI_YoY"]
    f["sent_trend"] = df["ConsumerSentiment"].diff(60)
    return f.dropna()

def kmeans_regimes(feat, k=4):
    X = StandardScaler().fit_transform(feat)
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    lab = pd.Series(km.labels_, index=feat.index, name="kmeans")
    # 클러스터 해석: 각 클러스터 중심의 거시 특성으로 라벨링
    centers = pd.DataFrame(
        StandardScaler().fit(feat).inverse_transform(km.cluster_centers_),
        columns=feat.columns)
    return lab, centers

def hmm_regimes(feat, k=4):
    X = StandardScaler().fit_transform(feat)
    model = hmm.GaussianHMM(n_components=k, covariance_type="full",
                            n_iter=200, random_state=42)
    model.fit(X)
    states = model.predict(X)
    lab = pd.Series(states, index=feat.index, name="hmm")
    # 상태 지속성(transition diagonal) — HMM의 장점: 레짐이 끈끈한가
    persist = np.diag(model.transmat_)
    return lab, persist

def describe_clusters(feat, lab, name):
    print(f"\n--- {name} 클러스터별 거시 평균 (해석용) ---")
    g = feat.groupby(lab).mean()
    g["n_days"] = lab.value_counts().sort_index()
    print(g.round(2).to_string())
    return g

# ============================================================
# (B) QQQ 베타 중립 잔차 알파
# ============================================================
def beta_neutral_residuals():
    """종목 일간수익률 ~ QQQ수익률 회귀 -> 잔차 = 시장 제거된 종목 고유 알파."""
    rets = np.log(df[[MKT] + STOCKS]).diff().dropna()
    mkt = sm.add_constant(rets[MKT])
    resid = pd.DataFrame(index=rets.index)
    betas = {}
    for s in STOCKS:
        m = sm.OLS(rets[s], mkt).fit()
        betas[s] = m.params[MKT]
        resid[s] = m.resid           # 시장으로 설명 안 되는 부분
    return resid, betas, rets

# ============================================================
# 메인 분석
# ============================================================
def main():
    print("=" * 80)
    print("(A) 비지도 레짐 추출: KMeans vs HMM")
    print("=" * 80)
    feat = macro_features()
    km_lab, km_centers = kmeans_regimes(feat)
    hmm_lab, hmm_persist = hmm_regimes(feat)

    print(f"\nKMeans 레짐 분포:\n{km_lab.value_counts().sort_index().to_string()}")
    describe_clusters(feat, km_lab, "KMeans")
    print(f"\nHMM 레짐 분포:\n{hmm_lab.value_counts().sort_index().to_string()}")
    describe_clusters(feat, hmm_lab, "HMM")
    print(f"\nHMM 상태 지속확률(대각): {np.round(hmm_persist,3)}")
    print("  -> 1에 가까울수록 레짐이 끈끈함(현실적). HMM이 KMeans보다 부드러운 전환.")
    # 두 방법 일치도
    agree = (km_lab.values == hmm_lab.reindex(km_lab.index).values)
    # 라벨 번호는 임의이므로 '동시 전환 일치' 대신 조정랜드지수 사용
    from sklearn.metrics import adjusted_rand_score
    ari = adjusted_rand_score(km_lab.values, hmm_lab.reindex(km_lab.index).values)
    print(f"\nKMeans vs HMM 일치도 (Adjusted Rand Index): {ari:.3f}")
    print("  (1=완전일치, 0=무작위. 두 비지도 방법이 비슷한 구조를 찾는지 점검)")

    print("\n" + "=" * 80)
    print("(B) QQQ 베타 중립 잔차 알파에 레짐 적용")
    print("=" * 80)
    resid, betas, rets = beta_neutral_residuals()
    print("\n종목별 QQQ 베타 (시장 민감도):")
    bser = pd.Series(betas).sort_values(ascending=False)
    print(bser.round(2).to_string())

    # HMM 레짐을 잔차에 정렬
    reg = hmm_lab.reindex(resid.index).ffill()
    states = sorted(reg.dropna().unique())

    print("\n--- 레짐별 '잔차 알파' 연율 평균 % (시장 제거 후 종목 고유 초과수익) ---")
    rows = []
    for s in STOCKS:
        row = [s]
        for st in states:
            r = resid[s][reg == st].dropna()
            row.append(round(r.mean()*252*100, 1) if len(r) > 20 else np.nan)
        rows.append(row)
    adf = pd.DataFrame(rows, columns=["Stock"] + [f"R{int(s)}" for s in states])
    print(adf.to_string(index=False))

    # 핵심 검정: 잔차 알파가 레짐에 유의하게 의존하는가?
    print("\n--- 잔차 알파가 레짐에 유의하게 의존하는가? (Kruskal-Wallis) ---")
    sig = 0
    for s in STOCKS:
        groups = [resid[s][reg == st].dropna().values for st in states]
        groups = [g for g in groups if len(g) > 20]
        if len(groups) >= 2:
            h, p = stats.kruskal(*groups)
            tag = "유의" if p < 0.05 else "ns"
            if p < 0.05: sig += 1
            print(f"  {s:6s} p={p:.3f} {tag}")
    print(f"\n  => {sig}/{len(STOCKS)} 종목의 '시장 제거 후 고유 알파'가 레짐에 유의 의존.")

    # 비교: 베타 중립 전 (총수익) 대비 레짐 의존 변화
    print("\n--- 비교: 총수익 vs 잔차알파, 레짐 의존 유의 종목 수 ---")
    sig_raw = 0
    for s in STOCKS:
        groups = [rets[s][reg == st].dropna().values for st in states]
        groups = [g for g in groups if len(g) > 20]
        if len(groups) >= 2:
            _, p = stats.kruskal(*groups)
            if p < 0.05: sig_raw += 1
    print(f"  총수익 기준 유의: {sig_raw}/{len(STOCKS)}")
    print(f"  잔차알파 기준 유의: {sig}/{len(STOCKS)}")
    print("  해석: 잔차에서 유의 종목이 크게 줄면 -> 레짐 효과는 대부분 '시장 전체'")
    print("        효과였고, 종목 고유 알파는 레짐 무관 = 거시 레짐으로 종목선택 불가.")

    # 저장
    pd.DataFrame({"kmeans": km_lab, "hmm": hmm_lab}).to_csv("/home/claude/out_unsup_regime.csv")
    adf.to_csv("/home/claude/out_residual_alpha.csv", index=False)
    bser.to_csv("/home/claude/out_betas.csv")
    print("\n저장: out_unsup_regime.csv, out_residual_alpha.csv, out_betas.csv")
    return km_lab, hmm_lab, resid, reg, adf, bser

if __name__ == "__main__":
    main()
