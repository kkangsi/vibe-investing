# 실측 앵커 데이터 (Anchor Data) & 출처

> 본 프로젝트의 `data_lib.py` 는 **온라인이면 실데이터를 받아오고**, 막혀 있으면
> 아래 *실측 앵커* 에 캘리브레이션된 **재현 가능한(reconstructed)** 월간 데이터셋으로
> 폴백한다. 따라서 백테스트/분석 수치는 "임의의 난수"가 아니라 아래 공개 실측치에
> 고정된 결정론적 분배의 산물이다. 온라인 환경에서 `fetch_real_ewt()` 가 성공하면
> EWT 가격은 실데이터로 자동 대체된다.

## 1. TSMC 연결 매출 (NT$ 십억)

| 연도 | 매출(NT$bn) | YoY | 비고 |
|---|---|---|---|
| 2020 | 1,339.3 | +25.2% | 코로나 수요 |
| 2021 | 1,587.4 | +18.5% | |
| 2022 | 2,263.9 | +42.6% | 호황 피크 |
| 2023 | 2,161.7 | **−4.5%** | 반도체 다운사이클 / 재고조정 |
| 2024 | 2,894.3 | +33.9% | AI 회복 |
| 2025 | 3,809.1 | +31.6% | AI 슈퍼사이클 |
| 2026E | ~4,650 | ~+22% | 가이던스 기반 run-rate(추정) |

월간 YoY 분기 앵커(`TSMC_YOY_Q`)는 실제 사이클 형태(2022 Q3 피크 ~+48%,
2023 중반 저점 음(−), 2024~25 AI 회복)를 반영하도록 설정.

- 2024년 11월 매출 +34% YoY, 2025년 11월 +24.5% YoY (실측 보도)
- 2025년 1~11월 누적 +32.8% YoY

## 2. 대만 실질 GDP 성장률 (YoY %, 분기)

2024~2025 분기는 대만 DGBAS(주계총처) 실측. 그 외 분기는 공개 실측에 근사한 재구성.

| 분기 | YoY | 분기 | YoY |
|---|---|---|---|
| 2024Q1 | 6.64 | 2025Q1 | 5.48 |
| 2024Q2 | 4.89 | 2025Q2 | ~7.5 |
| 2024Q3 | 4.17 | 2025Q3 | ~9.0 |
| 2024Q4 | 2.90 | 2025Q4 | **12.65** |

- 2024 연간 +4.59%
- 2025Q4 +12.65% → **1987년 3분기 이후 최고 분기 성장**, AI 관련 수요가 견인
- 2025 연간 약 +8.7%

## 3. iShares MSCI Taiwan ETF (EWT) 연 수익률 (시장가 %)

| 연도 | 수익률 |
|---|---|
| 2020 | +31.50% |
| 2021 | +28.94% |
| 2022 | **−28.84%** |
| 2023 | +29.20% |
| 2024 | +16.12% |
| 2025 | +27.81% (NAV, ~3/2026 기준) |
| 2026 | +9% (1~5월 부분, 추정) |

- EWT 는 TSMC 비중이 가장 큰 단일 종목(약 본 분석 시점 기준 펀드의 큰 부분)인
  대만 대표 지수 ETF → "대만 = 반도체" 베팅의 대용물.

## 4. 출처 (Sources)

- TSMC Investor Relations — Monthly Revenue: https://investor.tsmc.com/english/monthly-revenue/2025
- TSMC FY2024/FY2025 실적 (SEC 6-K / 20-F): https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001046179
- MacroTrends — TSMC Revenue: https://www.macrotrends.net/stocks/charts/TSM/taiwan-semiconductor-manufacturing/revenue
- DGBAS (대만 주계총처) GDP 보도자료: https://eng.stat.gov.tw/News_Content.aspx?n=2317&s=234638
- Trading Economics — Taiwan GDP Growth: https://tradingeconomics.com/taiwan/gdp-growth-annual
- iShares EWT Fact Sheet / Performance: https://www.ishares.com/us/products/239686/ishares-msci-taiwan-etf
- LazyPortfolioETF — EWT Historical Returns: https://www.lazyportfolioetf.com/etf/ishares-msci-taiwan-etf-ewt/

> ⚠️ 면책: 본 데이터/분석은 교육·연구용이며 투자 권유가 아니다. 분기 GDP 일부와
> 2026년 값은 추정/재구성치를 포함한다. 실거래 판단 전 1차 출처로 검증할 것.
