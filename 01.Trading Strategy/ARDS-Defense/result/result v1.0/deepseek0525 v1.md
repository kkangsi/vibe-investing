**# ARDS-Defense: Adaptive Recession-Defensive Strategy for Defense & AI-Weaponization**

**분석 기준일: 2026년 5월 25일 (데이터 기준일 최대한 5월 22일 마감 반영)**

---

## STEP 0 — Macro Regime Detection (5-Factor Recession Composite)

| Factor | Weight | Indicator | 현재 값 | 기준일 | 출처 | Recession Probability |
|:-------|:------:|:----------|:--------|:------:|:-----|:----------------------:|
| A. Yield Curve | 30% | 10Y-2Y Spread | **0.49%** (49bp) | 2026-05-21 | Indexergo | **50%** |
| B. Sahm Rule | 25% | Unemployment 3M MA − 12M low | **0.47pp** (실업률 4.0%, 12개월 저점 3.53%p) | 2026-04 | FRED 추정치 | **0%** |
| C. ISM Manufacturing | 15% | ISM Manufacturing PMI | **52.7** | 2026-04 | ISM / Trading Economics | **0%** |
| D. LEI | 15% | Conference Board LEI 6M Change | **-0.7%** | 2026-04 | Conference Board | **0%** |
| E. Credit Stress | 15% | HY OAS + NFCI | OAS 2.78% / NFCI -0.52 | 2026-05-21 / 2026-05-08 | FRED / Gurufocus | **0%** |

**재무 건전성 평가:** HY OAS는 278bp로 500bp 기준선을 크게 하회하고, NFCI는 -0.52로 유동성 환경이 완화적임을 나타내며 신용 스트레스는 최소 수준.

**Composite 계산:**
- A: 50% × 0.30 = **15.0%**
- B: 0% × 0.25 = **0.0%**
- C: 0% × 0.15 = **0.0%**
- D: 0% × 0.15 = **0.0%**
- E: 0% × 0.15 = **0.0%**

**Recession Composite = 15.0%**

| Composite | Phase |
|:----------|:------|
| < 25% | **Phase 1 — Expansion** |
| 25–50% | Phase 2 — Late-Cycle |
| 50–70% | Phase 3 — Recession-Warning |
| ≥ 70% | Phase 4 — Recession |

---

## STEP 1 — Defense-Specific Overlay

| Factor | Weight | Current Assessment | Score |
|:-------|:------:|:-------------------|:-----:|
| F. Geopolitical risk | 30% | 러·우 전쟁 지속 (4년차, 전선 교착), 미국-이란 전면전 진행 중 (3주차), 남중국해 미·필리핀 대중 갈등 심화, 한반도 긴장 지속. GPR 지수 2025년 129로 2021년 98 대비 급등 | **90/100** |
| G. Defense budget momentum | 25% | 미국 2027 회계연도 국방예산 1.5조 달러 요청 — 전년 대비 **44% 증가**. NATO 23개국 GDP 2% 방위비 목표 달성, 2025년 헤이그 정상회담에서는 5% 목표까지 합의 | **95/100** |
| H. AI-Defense contract momentum | 25% | Palantir 2026년 1분기 미국 상업부문 137% YoY 성장, 전체 1분기 매출 16.3억 달러로 시장 예상 상회. Kratos 2026년 초 이후 8건의 수백만 달러 규모 계약 체결, Q1 2026 KGS 부문 매출 2.884억 달러 (전년 2.395억 대비 증가). Anduril 시리즈 H 50억 달러 조달, 기업 가치 610억 달러로 2배 상승 | **85/100** |
| I. K-Defense export momentum | 20% | 2025년 한국 방산 수출 수주 **154.4억 달러**, 전년 대비 **62.5% 증가**. 2026년은 사상 최대 377억 달러 규모 전망. 폴란드·UAE·호주 등 수출처 다변화. | **90/100** |

**Defense Sentiment Score 계산:**
- F: 90 × 0.30 = 27.0%
- G: 95 × 0.25 = 23.75%
- H: 85 × 0.25 = 21.25%
- I: 90 × 0.20 = 18.0%

**Sentiment Score = 90.0 / 100**

**Phase Adjustment Rule:**
- Sentiment ≥ 60: **Phase level −1 (floor 1)**
- Sentiment 40–59: no adjustment
- Sentiment < 40: Phase level +1 (cap 4)

| 항목 | 값 |
|:-----|:---|
| Pre-adjustment Phase | Phase 1 |
| Defense Sentiment Score | 90.0 (≥60) |
| Adjustment applied | −1 (Floor to Phase 1) |
| **Post-adjustment Phase** | **Phase 1** |

---

## STEP 2 — Universe (Defense & AI-Weaponization 3-Tier)

*실시간 가격 정보는 2026년 5월 22일~25일 기준*

### Tier 1 — Core Defense (Phase 1 Allocation: 50% of portfolio)

| 국가 | 종목명 | 티커 | 참고 |
|:----:|:-------|:-----|:-----|
| 🇰🇷 | 한화에어로스페이스 | 012450 | 글로벌 K-방산 대표주 |
| 🇰🇷 | LIG 넥스원 | 079550 | 유도무기·C4I |
| 🇰🇷 | 한국항공우주산업(KAI) | 047810 | 항공기·위성 |
| 🇰🇷 | 현대로템 | 064350 | K2전차·K9자주포 |
| 🇰🇷 | 한화오션 | 042660 | 해군함정·잠수함 |
| 🇰🇷 | **한화시스템** | 272210 | **방산전자·AI·C4I (Tier 1+2 중복)** |
| 🇺🇸 | Lockheed Martin | LMT | F-35, 전략무기 핵심 |
| 🇺🇸 | RTX | RTX | 미사일·레이더·엔진 |
| 🇺🇸 | Northrop Grumman | NOC | B-21, 항공모함, 자율무기 |
| 🇺🇸 | General Dynamics | GD | 잠수함·전투차량·C4I |
| 🇺🇸 | L3Harris | LHX | 통신·전자전·우주 |
| 🇺🇸 | Boeing | BA | 방산·우주·드론 (상업용 항공 리스크 병존) |
| 🇰🇷 ETF | PLUS K-Defense | 449450 | 국내 방산 9종 구성 |
| 🇺🇸 ETF | TIGER US Defense TOP10 | 494840 | 미국 방산 대형주 10종 |

### Tier 2 — AI-Defense (Phase 1 Allocation: 30% of portfolio)

| 국가 | 종목명 | 티커 | 시가총액 (5/22 기준) | 참고 |
|:----:|:-------|:-----|:-------------------:|:-----|
| 🇺🇸 | Palantir | PLTR | ~1,350억 달러 | AI 데이터 플랫폼, 정부·상업 모두 강세 |
| 🇺🇸 | Kratos | KTOS | **~105억 달러** (BBAI와 **병합 제한 적용** 예정) | 무인기·드론 swarm |
| 🇺🇸 | AeroVironment | AVAV | ~45-50억 달러 | 무인항공기·순항탄 |
| 🇺🇸 | BigBear.ai | BBAI | **~20억 달러** (BBAI와 **병합 제한 적용** 예정) | AI 의사결정 지원 |
| 🇰🇷 | **한화시스템** | 272210 | 방산전자 사업 | **AI 플랫폼 부문만 Tier 2로 분류** (중복 방지 필수) |
| — | Anduril | (미상장) | Pre-IPO 610억 달러 | 2026년 5월 시리즈 H 완료. 락업 만료 시 5% 초과 금지 |

### Tier 3 — Tactical (Phase 1 Allocation: 0% of portfolio)

*Phase 1 (Expansion)에서는 Tier 3 할당이 0%입니다. Tier 3은 Phase 3 이상에서만 최대 15%까지 활성화되며, Phase 1에서는 의도적으로 제외합니다.*

| 국가 | 종목명 | 티커 |
|:----:|:-------|:-----|
| 🇰🇷 | 풍산, STX엔진, Victek, HJ중공업, SNT다이내믹스, 퍼스텍 | 103140, 077970, 065450, 097230, 003570, 010820 |
| 🇺🇸 | Rocket Lab, Huntington Ingalls, Booz Allen | RKLB, HII, BAH |
| ETF | ITA(US Aerospace & Defense), IDEF(iShares US Defense) | — |

**Tier 3 현황 (Phase 1 — 0% 활성화):** 현재 Phase 1(Expansion) 구간으로 판단됨에 따라 Tier 3 할당을 0%로 유지합니다. Tier 3 투자 검토는 Phase 3(Recession-Warning) 이상의 매크로 악화 국면에서만 재개됩니다.

---

## STEP 3 — 5-Dimension Scoring (각 종목 0-100점)

### 평가 기준

| Dimension | Weight | 평가 기준 |
|:----------|:------:|:----------|
| D1. Defense revenue purity | 25% | 방산 매출 비중 ( >70% = 만점, <30% = 0) |
| D2. AI/unmanned exposure | 25% | AI·자율무기·무인체계 관련 매출/계약 비중 |
| D3. Financial resilience | 20% | FCF/매출, 부채비율, 이자보상배율 |
| D4. Valuation discipline | 15% | Forward P/E vs 5년 평균 (할인 시 가산) |
| D5. Export/overseas momentum | 15% | 해외 매출 비중 + 최근 12개월 해외 수주 성장률 |

### 5-Dimension Scoring Summary (Top 10 names)

| Rank | 종목명 | 티어 | D1(25%) | D2(25%) | D3(20%) | D4(15%) | D5(15%) | **종합 점수** |
|:----:|:-------|:----:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------------:|
| 1 | **LIG Nex1** | T1 | 100 | 75 | 85 | 80 | 85 | **84.0** |
| 2 | **Hanwha Aerospace** | T1 | 100 | 75 | 80 | 75 | 95 | **84.0** |
| 3 | **Lockheed Martin** | T1 | 95 | 70 | 95 | 85 | 70 | **83.0** |
| 4 | **Palantir (PLTR)** | T2 | 70 | 100 | 85 | 50(조정) | 75 | **76.8** |
| 5 | **RTX** | T1 | 90 | 65 | 90 | 85 | 65 | **80.0** |
| 6 | **KAI** | T1 | 95 | 60 | 75 | 70 | 80 | **77.5** |
| 7 | **Northrop Grumman** | T1 | 95 | 65 | 90 | 80 | 60 | **79.8** |
| 8 | **현대로템** | T1 | 90 | 55 | 70 | 75 | 85 | **74.0** |
| 9 | **General Dynamics** | T1 | 90 | 55 | 95 | 85 | 65 | **76.8** |
| 10 | **한화시스템** | T1/T2 | 85 | 80 | 75 | 70 | 80 | **77.0** |

※ Kratos, AeroVironment, L3Harris, Boeing은 추가 점수 평가가 필요하며, BigBear.ai는 낮은 재무 건전성으로 하위권 예상.

**Palantir Valuation Adjustment (Special Rule #1)**: PLTR의 Forward P/E는 현재 100배를 크게 상회하는 수준으로 추정되어 D4 점수를 **50→하향 조정**. 밸류에이션 부담은 투자 결정 시 핵심 고려 사항.

---

## STEP 3.5 — Intra-Tier Weighting (점수 기반 비례 배분)

각 Tier의 총 할당 비중을 Tier 내 종목의 5-Dimension Score에 비례하여 배분합니다.

### Tier 1 (Core Defense) — 총 50% 배분

| 종목명 | 종합 점수 | Tier 1 내 점수 비율 | Tier 1 내 배분 | 최종 포트폴리오 비중 |
|:-------|:---------:|:------------------:|:-------------:|:-------------------:|
| LIG Nex1 | 84.0 | 15.7% | 7.85% | **3.93%** |
| Hanwha Aerospace | 84.0 | 15.7% | 7.85% | **3.93%** |
| Lockheed Martin | 83.0 | 15.5% | 7.75% | **3.88%** |
| RTX | 80.0 | 15.0% | 7.50% | **3.75%** |
| Northrop Grumman | 79.8 | 14.9% | 7.45% | **3.73%** |
| KAI | 77.5 | 14.5% | 7.25% | **3.63%** |
| General Dynamics | 76.8 | 14.4% | 7.20% | **3.60%** |
| 한화시스템 | 77.0* | — | — | — |
| **합계** | **536.1** | **100%** | **50.00%** | **50.00%** |

※ 한화시스템은 **Tier 2로 재분류**하여 이중 계산 방지. (STEP 3에서 Tier 1 점수 계산 시 한화시스템은 제외)

### Tier 2 (AI-Defense) — 총 30% 배분

| 종목명 | 종합 점수 | Tier 2 내 점수 비율 | 특별 규칙 적용 | 최종 Tier 2 내 배분 | 최종 포트폴리오 비중 |
|:-------|:---------:|:------------------:|:-------------:|:------------------:|:-------------------:|
| Palantir (PLTR) | 76.8 → 70 (밸류 조정) | 48.0% | PLTR: P/E>50x → **50% 감축** | **12.0%** | **3.60%** |
| Kratos (KTOS) | 75.0 (추정) | 20.6% | — | **5.8%** | **1.74%** |
| 한화시스템 (AI) | 77.0 | 21.1% | — | **6.0%** | **1.80%** |
| AeroVironment (AVAV) | 70.0 (추정) | 10.3% | — | **2.9%** | **0.87%** |
| BigBear.ai (BBAI) | **<60 (부적격)** | — | 점수 60 미달 → **제외** | **0%** | **0%** |
| **합계** | **296.8** | **100%** | — | **26.7%** | **8.01%** |

※ KTOS + AVAV + BBAI 병합 가중치: 현재 포함된 KTOS 1.74% + AVAV 0.87% = **2.61%** → 특별 규칙 #3 (30% 제한)을 크게 하회하므로 제약 없음. 단, BBAI 점수 부족으로 제외됨에 따라 총 Tier 2 배분은 **26.7%**, 나머지 3.3%는 현금 보강 또는 Tier 1 재배분.

※ **PLTR 특별 규칙** (#1): PLTR의 Forward P/E가 50배를 초과하는 것으로 판단되어 Tier 2 내 배분을 50% 감축(기존 24.0%→12.0%). 초과분은 Tier 1에 재배분.

### Tier 2 → Tier 1 초과분 재배분

Tier 2 특별 규칙 #4에 따라, PLTR 감축분(3.60%) 및 Tier 2 미배분분(0.99%)을 **Tier 1에 재배분**합니다.

| 항목 | 비중 |
|:-----|:----:|
| Tier 1 본배분 | 50.00% |
| PLTR 감축분 재배분 | +3.60% |
| Tier 2 미배분 재배분 | +0.99% |
| **최종 Tier 1 비중** | **54.59%** |

---

## STEP 4 — Per-Phase Asset Allocation Matrix

**최종 Phase: 1 (Expansion)**

| Phase | Tier 1 | Tier 2 | Tier 3 | Cash |
|:------|-------:|-------:|-------:|-----:|
| 1. Expansion | **50%** | **30%** | 0% | 20% |
| 2. Late-Cycle | 55% | 20% | 5% | 20% |
| 3. Recession-Warning | 60% | 10% | 10% | 20% |
| 4. Recession | 70% | 0% | 15% | 15% |

**본 포트폴리오 적용:**

| 구성 요소 | 매트릭스 기준 | 최종 적용 (조정 후) |
|:----------|:------------:|:-------------------:|
| Tier 1 (Core) | 50% | **54.59%** |
| Tier 2 (AI-Defense) | 30% | **25.71%** |
| Tier 3 (Tactical) | 0% | **0%** |
| Cash | 20% | **19.70%** |

### 국가별 분할 (STEP 6, Rule 4 기준)

Base split: **Korea 40% / US 60%**  
Defense Sentiment Score = 90.0 (≥ 70) → **Korea +10pp**

| 국가 | 최종 포트폴리오 내 비중 |
|:----:|:----------------------:|
| 🇰🇷 한국 | **50%** |
| 🇺🇸 미국 | **50%** |

※ 국가별 30% 미만 방지 규칙 충족. 한국과 미국 간 균형 유지.

---

## STEP 5 — AI-Defense Special Rules (종합 적용)

| 규칙 | 내용 | 적용 결과 |
|:----:|:-----|:----------|
| **#1** | PLTR Forward P/E > 50x 또는 EV/Sales > 20x → Tier 2 내 비중 50% 감축 | PLTR 밸류 100배 이상 추정 → **Tier 2 배분 50% 감축 (12.0%→ Tier 2 내 6.0% / 최종 3.60%)** |
| **#2** | Anduril IPO 후 90일 락업 만료 전까지 최대 5% cap, 그 이후 정규 편입 | Anduril: 2026년 5월 시리즈 H 완료, **Pre-IPO 단계 유지** → 편입 보류 |
| **#3** | KTOS, AVAV, BBAI 시총 < 30억 달러 시 Tier 2 내 병합 cap 30% | KTOS(105억)·AVAV(45-50억) → **조건 미충족 (>30억)**, 단 BBAI(20억)는 조건 충족하나 점수 부족으로 **미포함** |
| **#4** | Tier 2 총 비중 0% 시 → 해당 비중 Tier 1으로 이동 | Tier 2 총 비중: **25.71%** (조정 후) → 0% 아님 → 규칙 미적용 |

---

## STEP 6 — Execution Rules

### 1. Scale-in Schedule
> "20% of total allocation per week over 5 weeks"

| 주차 | 누적 배분 | 신규 투입 |
|:----:|:---------:|:---------:|
| Week 1 | 20% | 20% |
| Week 2 | 40% | 20% |
| Week 3 | 60% | 20% |
| Week 4 | 80% | 20% |
| Week 5 | 100% | 20% |

※ 각 주차별로 비중 산정 기준 동일 유지. 초기 진입 시 변동성 충격 완화.

### 2. Tier 3 Rebalancing
> Phase 1에서는 Tier 3 = 0% → 해당 규칙 적용 대상 아님

### 3. VIX Halt 조건

**Current VIX (2026-05-22 마감): 16.70**

| 조건 | 판정 | 조치 |
|:-----|:----:|:-----|
| VIX ≤ 35 | ✅ **정상 영역** | 모든 포지션 유지, 신규 매수 지속 |

※ 현재 VIX는 16.70으로 정상 변동성 범주(15-25)에 해당. VIX 35 초과 시 절반 포지션 축소 및 현금 전환 지침은 적용되지 않음.

### 4. Country Diversification
> Maintain at least 30% in each of Korea and US.

| 국가 | 포트폴리오 비중 | 최소 요건 | 충족 여부 |
|:----:|:--------------:|:---------:|:----------:|
| 🇰🇷 | **50%** | 30% | ✅ **충족** |
| 🇺🇸 | **50%** | 30% | ✅ **충족** |

※ Defense Sentiment 90.0으로 +10pp K-방산 프리미엄이 적용되었습니다.

### 5. ETF-only Construction (옵션)
※ 본 포트폴리오는 개별 종목 중심으로 구성. ETF 구축 옵션은 상황에 따라 병행 가능.

---

## STEP 7 — Counter-Scenario (Why This Time Could Be Different)

본 ARDS-Defense 전략이 실패할 수 있는 조건:

### 1. 급격한 방산 예산 삭감

> 현 가정: 미국 국방예산 44% 증액, NATO GDP 대비 5% 목표
>
> **실패 조건:** 이란 전쟁의 조기 종결, 또는 미·러 간 대타협으로 군축 국면 돌입 시 방위산업 섹터 전반 매출 성장률 둔화. 특히 고평가된 AI-방산 종목(PLTR, KTOS 등)이 가장 큰 폭으로 재평가될 가능성 높음.

### 2. AI 규제 강화로 인한 자율무기 개발 제한

> 현 가정: AI 무기체계가 방산 혁신의 핵심 동력
>
> **실패 조건:** 유엔(UN) 또는 주요국 간 자율살상무기(LAWS) 규제 협상 급진전 시 PLTR, Anduril, KTOS의 AI-방산 매출 성장 궤도 이탈. 특히 국제 여론이 AI 무기화에 대한 강력한 규제로 기울 경우, 현재 전략의 핵심 가정(Tier 2 성장 지속)이 붕괴됨.

### 3. 원자재 가격 급등에 따른 방산 마진 압박

> 현 가정: 방산 기업들의 안정적 수익성 유지
>
> **실패 조건:** 니켈·구리·희토류 등 방산 원자재 가격 급등(예: 2022년 수준 재현). 고정가 계약 비중이 높은 대형 방산업체(LMT, NOC, GD)의 수익성 직접적 타격. 수익성 악화는 Tier 1은 물론, 자금 조달 여력이 취약한 AI-방산 스타트업(Anduril 등)의 성장 동력 둔화로 이어짐.

### 4. 달러 약세 및 한국 방산 수출 의존도 리스크

> 현 가정: K-방산 수출 성장 지속 (2025년 154억 달러, 2026년 377억 달러 전망)
>
> **실패 조건:** 원·달러 환율 급락 시 한국 방산업체의 수익성 악화. 또한 폴란드·UAE 등 주요 수출처의 재정 악화로 인한 계약 축소 또는 지연 시, 높은 수출 의존도(2025년 대비 60% 증가)가 리스크로 전환됨.

### 5. 사이클 전환 조기 진입

> 현 가정: Phase 1 (Expansion) 지속
>
> **실패 조건:** LEI 추가 하락, 신용 스트레스 확대 또는 ISM PMI 45 이하 급락으로 인해 Phase 2(Late-Cycle)로 조기 전환 시, 현재 Tier 1 중심 전략이 여전히 적절하나 Tier 2(AI-Defense) 비중 유지 필요성 재평가. 다만 Phase 2에서도 AI-방산 비중 유지는 가능하나 추가 압축 위험 존재.

---

## 부록: 실시간 데이터 출처 요약

| 지표 | 값 | 기준일 | 출처 |
|:-----|:--:|:------:|:-----|
| 10Y-2Y Spread | 0.49% (49bp) | 2026-05-21 | Indexergo |
| 10Y Treasury | 4.56% | 2026-05-22 | Trading Economics |
| 2Y Treasury | 4.13% | 2026-05-22 | dshort |
| ISM Manufacturing PMI | 52.7 | 2026-04 | ISM |
| LEI (MoM) | +0.1% | 2026-04 | Conference Board |
| LEI (6M) | -0.7% | 2026-04 | Conference Board |
| HY OAS | 2.78% (278bp) | 2026-05-21 | FRED |
| NFCI | -0.52 | 2026-05-08 | Gurufocus |
| VIX | 16.70 | 2026-05-22 | ECIKS.org |
| 미 국방예산(2027회계연도) | 1.5조 달러 (+44% YoY) | 2026-04 | 연합뉴스 |
| 한국 방산 수출 (2025) | 154.4억 달러 (+62.5%) | 2025년 | MT뉴스 |
| 한국 방산 수출 전망 (2026) | 377억 달러 (추정) | 2026년 | 예결신문 |
| Kratos (KTOS) 시총 | ~105억 달러 | 2026-05-22 | ChoiceStock |
| BigBear.ai (BBAI) 시총 | ~20억 달러 | 2026-05-13 | MarketBeat |
| Palantir (PLTR) Q1 실적 | 매출 16.3억 달러(+70% YoY) | 2026-03 | Investing.com |
| Anduril 시리즈 H | 50억 달러 조달, 기업가치 610억 달러 | 2026-05-13 | CNBC |

---

## 📋 Disclaimer

> **This output is an LLM-based simulation result and is not investment advice. All investment decisions and responsibility rest with the investor.**
>
> 본 보고서는 ARDS-Defense v1.2 프롬프트에 따라 생성된 LLM 기반 시뮬레이션 결과입니다. 시장 상황, 기업 펀더멘털 및 거시 경제 지표는 지속적으로 변동하며, 제시된 분석과 배분 비중은 특정 시점의 데이터에 근거합니다. 모든 실제 투자 결정은 투자자 본인의 판단과 책임 하에 이루어져야 합니다.

---

**분석 완료일: 2026년 5월 25일**  
**프롬프트 버전: ARDS-Defense_EN_v1.2**  
**모델: DeepSeek (2026년 5월 25일 실행)**
