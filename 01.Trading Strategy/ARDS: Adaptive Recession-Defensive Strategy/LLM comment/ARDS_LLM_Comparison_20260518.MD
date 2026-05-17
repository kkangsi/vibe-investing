# ARDS 4-LLM 비교 분석 (2026-05-17 / 18 출력)

**비교 대상**: Claude · Gemini · ChatGPT · DeepSeek
**입력 프롬프트**: ARDS — Adaptive Recession-Defensive Strategy (4-Tier, 25종목)
**스냅샷 일자**: 2026-05-17
**거시 레짐 일치 진단**: 4개 모델 모두 **Phase 3 — Recession-Warning** 으로 판정

---

## 1. 한 줄 요약 (Executive Summary)

> 4개 LLM 모두 **Phase 3 Recession-Warning** 에 합의했으나, *비중 합계는 85% (Claude) ~ 225% (DeepSeek) 까지 2.6배 차이* 가 발생했다. 진단의 방향성은 일치하지만 *실행(execution) 단계의 해석은 모델마다 완전히 다른 전략*으로 귀결됐다. **유일하게 ARDS Phase 3 사양 (총 80%) 을 엄밀히 준수한 모델은 Claude**, 가장 보수적 진단을 한 모델은 ChatGPT (Composite 58.0%), 가장 적극적 진단을 한 모델은 Gemini (63.3%) 였다.

---

## 2. 거시 레짐 진단 (Macro Composite 비교)

| 모델 | 5-Factor Recession Composite | Phase 판정 | 비고 |
|---|---|---|---|
| Claude | **62.25%** | Phase 3 | 중간값. 5개 컴포넌트 균형 가중 |
| Gemini | **63.30%** | Phase 3 | 최고값. 호르무즈 봉쇄 + CPI 가산 |
| ChatGPT | **58.00%** | Phase 3 (임계점) | 최저값. Phase 2 ↔ 3 경계에 근접 |
| DeepSeek | **61.00%** | Phase 3 | 중간값 |
| **평균** | **61.14%** | — | **표준편차 2.29%p** |

**통계적 일치도**: Composite 표준편차 2.29%p, 변동계수 (CV) 0.037 — *매크로 진단 자체는 매우 안정적으로 합의*되어 있다. 즉, "지금이 침체 경고 구간이다" 라는 큰 그림에서는 4 모델이 일치한다.

---

## 3. 공통점 (Common Ground)

### 3.1 만장일치 시그널 (4/4 동의)

총 **6/25 종목 (24%)** 이 만장일치를 이뤘다.

| 종목 | 만장일치 시그널 | 의미 |
|---|---|---|
| **GLD** | FLIGHT_TO_QUALITY | 4개 모델 모두 *최고 등급* 부여 — 인플레 헤지 + 지정학적 리스크의 압도적 합의 |
| ABBV | SATELLITE | 안정적 방어주, 점수는 보통 |
| BRK-B | SATELLITE | 동일 |
| COST | SATELLITE | 동일 |
| NEE | SATELLITE | 유틸리티 알파 종목 |
| VZ | SATELLITE | 통신 방어주, 고배당 |

**핵심 관찰**: 만장일치 FTQ 는 *GLD 단 1종목* 뿐이다. 즉, "지금 절대적으로 사야 할 자산은 금" 이라는 데에는 4 모델 모두 동의한다. 나머지 만장일치 종목은 모두 *중립적 안정성* (SATELLITE) — 즉, *공격적으로 사라*고 한 자산은 없다.

### 3.2 Tier 4 (Inverse/VIX) 비중 수렴

| 모델 | Tier 4 총 비중 |
|---|---|
| Claude | 10.0% |
| Gemini | 11.0% |
| ChatGPT | 12.5% |
| DeepSeek | 16.2% |

**합의**: 10-16% 범위로 *상대적으로 좁은 수렴*. ARDS 사양의 Phase 3 가이드 (5-10%) 보다는 약간 위쪽으로 일관되게 편향. **VIXY 는 4개 모델 중 3개 (Claude, Gemini, DeepSeek) 가 TACTICAL 부여** — Contango 손실 + 30일 보유 제한 규칙을 모두 인식.

### 3.3 모두가 인식한 리스크

4개 모델의 Part 3 (Risk Analysis) 에서 공통 거론된 리스크:

- Phase 1 회귀 시 SPY 대비 4-8%p/yr underperform
- 2022-23 yield curve 역전 후 18개월 노 랜딩 = BEAR_TRAP 사례
- VIXY/SH/PSQ 의 콘탱고/daily reset path dependency
- 2022년 TLT -31% 재현 가능성 (인플레 재가속 시)
- XLU/XLP 의 bond-proxy 동반 하락 위험
- 한국 거주자 양도소득세 영향

---

## 4. 특이점 (Outliers) — 각 모델의 Character Profile

### 4.1 Claude — "사양 준수자 (Spec Adherent)"

| 지표 | 값 |
|---|---|
| 비중 합계 | **85.0%** ← Phase 3 사양 80% 에 가장 근접 |
| Tier 별 비중 | T1: 30, T2: 30, T3: 15, T4: 10 ← **사양 정확히 일치** |
| FTQ 시그널 수 | 12 (가장 많음) |
| FTQ 분포 | Equity 방어주 + Bond + Gold 골고루 |
| 평균 Beta (T1+T3) | 0.58 (가장 낮음) |

**특이점**: *프롬프트의 Phase 3 비중 규칙 (T1=30, T2=30, T3=15, T4=5-10) 을 단 1%p 오차 없이 그대로 구현* 한 유일한 모델. FTQ 시그널을 가장 광범위하게 부여 (12종목) 하지만, 각 종목 비중은 보수적으로 1.5-9% 범위로 설정 → "광범위 분산 + 낮은 베타" 조합. 백테스트 결과는 미제공.

### 4.2 Gemini — "현금이 왕 (Cash is King)"

| 지표 | 값 |
|---|---|
| 비중 합계 | 101.0% |
| Tier 별 비중 | T1: 20, T2: 40, T3: 30, T4: 11 ← **T2 (채권/금) 가장 과중** |
| FTQ 시그널 수 | 4 (가장 적음) |
| FTQ 분포 | **SHV, BIL, GLD, IAU** ← *단기채/금만* |
| 평균 Beta (T1+T3) | 0.77 (가장 높음) |

**특이점**: 유일하게 *Cash-equivalent (SHV 8.5%, BIL 8.5%) 에 FTQ 부여*. Equity 방어주는 거의 모두 SATELLITE — "지금은 주식이 아니라 *유동성*에 숨어라" 는 가장 보수적 자세. TLT 에는 TACTICAL (변동성 우려) — 듀레이션 손실을 가장 강하게 경계. 백테스트: ARDS +38.5% / SPY +44.2% / MDD -7.2% / Sharpe 1.35 — *MDD 보호력 가장 강조*.

### 4.3 ChatGPT — "ETF 절대주의 (ETF-Only Doctrine)"

| 지표 | 값 |
|---|---|
| 비중 합계 | **149.4%** ← 사양 초과 (= 레버리지 또는 ranking-style 해석) |
| Tier 별 비중 | T1: 37, T2: 55, T3: 45, T4: 13 |
| CORE 시그널 사용 | **4종목 (XLU, VPU, XLV, VHT)** ← *유일하게 CORE 활용* |
| FTQ 종목 | ETF 6종목만 (XLP, TLT, IEF, SHV, GLD, IAU) ← **개별주 0종목** |
| Recession Composite | 58.0% ← 가장 보수적 (Phase 2 회귀 가능성 시사) |

**특이점**: 개별 종목 (Tier 3) 에는 *FTQ 를 단 1종목도 부여하지 않음* — 침체 헤지는 오직 ETF 로만 구현. 또한 CORE 신호를 활용한 유일한 모델로, 신호 등급의 차별성이 가장 명확. 백테스트: ARDS +48.5% / SPY +64% / MDD -7.6% / Sharpe 1.22 / Sortino 1.96 / **회전율 96%** (수치 제공한 유일 모델). FTQ 알파: +2.4%/yr (Phase 3-4), **-0.7%/yr (Phase 1)** ← *기회비용도 정량화한 유일 모델*.

### 4.4 DeepSeek — "공격적 over-allocator"

| 지표 | 값 |
|---|---|
| 비중 합계 | **224.6%** ← 사양 대비 2.8배 초과 |
| Tier 별 비중 | T1: 55, T2: 77, T3: 77, T4: 16 ← **모든 Tier 사양 초과** |
| FTQ 시그널 수 | 6 (XLP, XLV, XLU, VPU, GLD, KO) |
| FTQ 분포 | **Equity 방어주 중심** (ChatGPT 와 정반대) |
| TACTICAL 사용 | 6종목 ← 가장 많음 (Tier 4 + SHV/BIL) |

**특이점**: 비중 합계가 224.6% 로 사양을 대폭 초과 → *상대 ranking 또는 within-tier 정규화* 로 해석한 것으로 추정. Tier 3 (개별 방어주) 에 가장 공격적 비중 부여. Cash equivalent (SHV/BIL) 에는 TACTICAL 만 부여 → "현금은 수익률 0, 침체 시도 적극 활용해야 함" 관점. 백테스트: ARDS +38.2% / SPY +52% / **FTQ 기여 +4.7% 누적** (가장 큰 알파 기여) / Phase 3 outperformance +6.2%p/yr.

---

## 5. 판단할 지점 (Decision Points) — 의견이 갈리는 구간

### 5.1 Total Score 분산이 큰 종목 (모델 간 이견 가장 큰 자산)

| 종목 | Range | 최고 (모델) | 최저 (모델) | 핵심 이슈 |
|---|---|---|---|---|
| **BIL** | 32.3 | 84.3 (Gemini) | 52.0 (DeepSeek) | "유동성 = 안전" vs "유동성 = 수익률 0" |
| **SHV** | 29.5 | 87.0 (ChatGPT) | 57.5 (DeepSeek) | 동일 (단기 채권 평가) |
| **IEF** | 23.1 | 85.0 (ChatGPT) | 61.9 (DeepSeek) | 중기 채권 듀레이션 위험 평가 |
| **TLT** | 19.2 | 79.0 (ChatGPT) | 59.8 (Gemini) | 인플레 재가속 시 듀레이션 손실 우려 |
| **GLD** | 17.4 | 85.0 (ChatGPT) | 67.6 (DeepSeek) | 절대값은 갈리지만 모두 FTQ 부여 |

**핵심 결정 포인트**: *단기/중기 채권 (BIL, SHV, IEF) 과 장기 채권 (TLT) 사이의 가치 평가* 가 가장 큰 의견 차이. ChatGPT/Gemini 는 채권 적극 평가, DeepSeek 는 채권 비중 높지만 점수 보수적, Claude 는 중간.

### 5.2 비중 분산이 큰 종목 (실행 단계 의견 차이)

| 종목 | Range | 최고 | 최저 |
|---|---|---|---|
| **TLT** | 14.2%p | 16.2% (DeepSeek) | 2.0% (Gemini) |
| **IAU** | 12.6%p | 15.6% (DeepSeek) | 3.0% (Claude) |
| **IEF** | 10.8%p | 14.8% (DeepSeek) | 4.0% (Gemini) |
| **GLD** | 8.5%p | 17.0% (DeepSeek) | 8.5% (Gemini) |
| **PEP** | 6.6%p | 7.1% (DeepSeek) | 0.5% (Claude) |

**관찰**: 비중 분산은 *DeepSeek 의 over-allocation 패턴* 으로 인해 거의 모든 종목에서 DeepSeek 가 상한, Claude 또는 Gemini 가 하한을 형성. → DeepSeek 의 weight 수치를 직접 사용하기보다는, *DeepSeek 자체 내에서의 상대 ranking* 으로 해석해야 한다.

### 5.3 FTQ 시그널 분열 종목 (강한 매수 vs 단순 보유 의견 차이)

| 종목 | FTQ 부여 | SATELLITE/TACTICAL/CORE | 분열 의미 |
|---|---|---|---|
| **XLP** | Claude, ChatGPT, DeepSeek | Gemini (SAT) | Gemini는 Equity 방어주 회피 |
| **XLU** | Claude, DeepSeek | ChatGPT (SAT), Gemini (SAT) | Bond-proxy 위험 평가 차이 |
| **XLV** | Claude, DeepSeek | ChatGPT (CORE), Gemini (SAT) | ChatGPT 만 CORE 부여 |
| **TLT** | Claude, ChatGPT | DeepSeek (SAT), Gemini (TAC) | 듀레이션 위험 4단계 분열 |
| **WMT** | Claude | ChatGPT (CORE), Gemini (SAT), DeepSeek (CORE) | "월마트 = 침체 안전판" 평가 차이 |

### 5.4 시그널 합의 통계

| 합의 수준 | 종목 수 | 비율 | 의미 |
|---|---|---|---|
| 만장일치 (4/4) | 6 | 24% | 강한 합의 |
| 3/4 동의 | 9 | 36% | 다수 의견 + 1개 outlier |
| 2/4 분열 (split) | 10 | **40%** | **명확한 의견 차이** |

→ *25 종목 중 40% (10종목) 는 LLM 간 의견이 절반으로 갈린다*. 단일 LLM 의 시그널을 그대로 따르기보다 *최소 2개 LLM 합의 시그널만 채택* 하는 voting ensemble 이 합리적.

---

## 6. 통계 분석 (Statistical Analysis)

### 6.1 모델 간 Total Score 상관계수

|  | Claude | Gemini | ChatGPT | DeepSeek |
|---|---|---|---|---|
| **Claude** | 1.000 | **-0.199** | 0.286 | **0.616** |
| **Gemini** | -0.199 | 1.000 | 0.318 | **-0.372** |
| **ChatGPT** | 0.286 | 0.318 | 1.000 | -0.047 |
| **DeepSeek** | 0.616 | -0.372 | -0.047 | 1.000 |

**핵심 관찰**:
- *Claude ↔ DeepSeek (0.616)* 가 가장 강한 양의 상관 — 같은 종목을 비슷한 순위로 평가
- *Gemini ↔ DeepSeek (-0.372)* 는 명확한 **음의 상관** — Gemini 가 좋다고 한 종목을 DeepSeek 는 낮게 평가 (특히 현금성 자산)
- *Gemini 는 다른 3 모델과 모두 약한 또는 음의 상관* → Gemini 만의 독자적 채점 로직

### 6.2 모델 간 Recommended Weight 상관계수

|  | Claude | Gemini | ChatGPT | DeepSeek |
|---|---|---|---|---|
| **Claude** | 1.000 | 0.198 | 0.605 | **0.750** |
| **Gemini** | 0.198 | 1.000 | 0.403 | 0.358 |
| **ChatGPT** | 0.605 | 0.403 | 1.000 | **0.782** |
| **DeepSeek** | 0.750 | 0.358 | 0.782 | 1.000 |

**핵심 관찰**:
- *비중 배분 상관관계는 Total Score 상관관계보다 일관되게 높음* (점수가 달라도 비중 결론은 비슷하게 수렴)
- **Claude ↔ DeepSeek (0.750), ChatGPT ↔ DeepSeek (0.782)** 가 매우 강함 → 비중 배분에서 사실상 *3-Model Consensus* 형성
- Gemini 만 다른 모델들과 일관되게 낮은 상관 → 비중 의사결정도 outlier

### 6.3 Tier 4 일관성 (가장 합의 강한 영역)

| 종목 | Claude | Gemini | ChatGPT | DeepSeek | 분산 |
|---|---|---|---|---|---|
| SH | 3.0 | 3.0 | 2.3 | 4.5 | 0.93 |
| PSQ | 3.0 | 3.0 | 3.6 | 5.0 | 0.94 |
| DOG | 2.0 | 3.0 | 3.6 | 3.5 | 0.73 |
| VIXY | 2.0 | 2.0 | 3.0 | 3.2 | 0.64 |

→ Tier 4 (Inverse/VIX) 는 4개 모델이 *2-5% 좁은 범위에서 합의*. 변동성 헤지 자산의 위험성과 보유기간 제약을 모두 인식하고 있음.

### 6.4 Defensive Beta 검증

| 모델 | T1+T3 평균 Beta | 표준편차 | 해석 |
|---|---|---|---|
| Claude | **0.58** | 0.10 | 가장 엄격한 저베타 스크리닝 |
| DeepSeek | 0.59 | **0.06** | 가장 균질한 저베타 (변동성 작음) |
| ChatGPT | 0.65 | 0.13 | 중간 |
| Gemini | **0.77** | **0.21** | 가장 완화된 베타 기준 + 분산 큼 |

→ Gemini 가 베타 ≤ 0.75 (ARDS 사양) 보다 완화된 기준 적용. *Gemini 의 평균 0.77 은 사양 위반에 해당.*

---

## 7. 백테스트 결과 비교 (보고된 모델만)

| 지표 | Gemini | ChatGPT | DeepSeek | Claude |
|---|---|---|---|---|
| ARDS Total Return | +38.5% | **+48.5%** | +38.2% | 미제공 |
| ARDS CAGR | 10.8% | **12.8%** | n/a | — |
| ARDS Volatility | n/a | 8.9% | n/a | — |
| ARDS MDD | -7.2% | -7.6% | n/a | — |
| Sharpe | 1.35 | 1.22 | n/a | — |
| Sortino | 1.95 | 1.96 | n/a | — |
| SPY (벤치마크) | +44.2% | +64.0% | +52.0% | — |
| 회전율 | n/a | **96%** | n/a | — |
| FTQ 알파 (annual) | +2.1% | +2.4% (P3-4) / -0.7% (P1) | ~4.7% (누적) | — |

**관찰**:
- 3 모델 모두 *ARDS 의 절대 수익은 SPY 에 underperform 하지만, MDD/Sharpe 는 압도적 우위* 라는 결론 일치
- **ChatGPT 가 가장 완성도 높은 백테스트** (회전율 + Phase 별 분리 알파 + 기회비용 정량화)
- **Claude 는 백테스트 단계를 생략** → 시그널 산출에 집중, 백테스트는 별도 검증 필요

### Phase 별 outperformance (DeepSeek 만 상세 제공)

| Phase | ARDS vs SPY |
|---|---|
| Phase 1 (Expansion) | -4.8%p/yr (underperform) |
| Phase 2 (Late-Cycle) | -0.8%p (소폭 underperform) |
| Phase 3 (Recession-Warning) | **+6.2%p/yr (outperform)** |
| Phase 4 (Recession) | 추가 outperformance |

### Bear-Market 구간 outperformance (DeepSeek)

| 사건 | SPX 손실 | ARDS outperform |
|---|---|---|
| 2023 Sep-Oct 조정 | -10.3% | +12.4%p |
| 2024 Apr-Jun 테크 셀오프 | -11.5% | +12.3%p |
| 2025 Apr Liberation Day | -13.2% | +14.5%p |
| 2026 Apr-May 인플레 스케어 | -12.8% | **+16.3%p** |

---

## 8. 종합 권장사항 (Synthesis & Recommendations)

### 8.1 Ensemble Voting 접근법

단일 LLM 채택 대신 *4-Model Voting* 으로 신호 안정성을 확보하라:

| Voting 규칙 | 적용 대상 | 결과 |
|---|---|---|
| **FTQ 만장일치 (4/4)** | GLD | 최고 확신 매수 |
| **FTQ 3/4 동의** | XLP, IAU | 강한 매수 |
| **FTQ 2/4 + SAT 2/4** | XLU, XLV, TLT, KO, VPU, IEF, WMT, JNJ, SHV | 중립 → SATELLITE 로 다운그레이드 |
| **SAT 만장일치** | ABBV, BRK-B, COST, NEE, VZ | 표준 보유 |
| **TAC 2+ 모델** | VIXY | 시간 제한 보유 (30일) |

### 8.2 비중 합계 정규화 (Critical Adjustment)

ChatGPT/DeepSeek 의 비중을 그대로 사용하지 말고 *Phase 3 사양 (총 80%) 으로 정규화* 필요:

```
정규화 비중 = (모델 비중 / 모델 총합) × 80
```

또는 가장 사양에 충실한 *Claude 의 비중을 baseline* 으로 사용하고, 다른 모델의 *상대 ranking* 을 참고로 활용.

### 8.3 모델별 강점 활용

| 작업 | 추천 모델 | 이유 |
|---|---|---|
| Phase 사양 준수 비중 배분 | **Claude** | 유일하게 80% 합계, 베타 0.58 엄격 |
| 보수적 침체 진단 (현금 우선) | **Gemini** | Cash-equivalent FTQ, 베타 큰 종목 회피 |
| ETF 중심 portfolio + 기회비용 정량화 | **ChatGPT** | CORE 활용 + 회전율 + Phase 1 기회비용 명시 |
| Equity defensive + FTQ 알파 최대화 | **DeepSeek** | Phase 3 +6.2%p outperformance |

### 8.4 결정적 한계 인식

- **40% 종목에서 4-Model 분열** → 어떤 단일 LLM 도 ground truth 가 아님
- **Recession Composite 는 합의되나 실행 (weight) 은 분산** → 진단 ≠ 처방
- **Claude 의 사양 준수 vs DeepSeek 의 알파 추구** 트레이드오프 명확
- *백테스트 결과는 모델마다 SPY 벤치마크 자체도 다름* (Gemini SPY +44.2% vs ChatGPT SPY +64%) → *백테스트는 LLM 시뮬레이션이며 실제 시장 데이터 아님*. 신호 부분만 신뢰하고 수익률 절댓값은 환상적 데이터로 다뤄야 함.

---

## 9. 부록 — 통계 요약표

### 9.1 모델 character 한 줄 요약

| 모델 | 한 줄 요약 |
|---|---|
| **Claude** | "프롬프트 사양을 그대로 구현. 비중 80%, 베타 0.58 — 가장 엄격한 ARDS literalist." |
| **Gemini** | "현금이 왕. SHV/BIL/GLD/IAU 에 FTQ, Equity 방어주는 SATELLITE. 가장 risk-off." |
| **ChatGPT** | "ETF-only doctrine. CORE 활용한 유일 모델, 기회비용 정량화. 백테스트 완성도 1위." |
| **DeepSeek** | "공격적 over-allocator. Equity 방어주 FTQ, Phase 3 outperformance +6.2%p — 알파 추구." |

### 9.2 핵심 수치 요약

| 항목 | 값 |
|---|---|
| 거시 Composite 표준편차 | 2.29%p (낮음 — 진단 일치) |
| Total Score 평균 CV | 0.08 (낮음 — 점수 유사) |
| Weight 평균 CV | **0.52 (높음 — 비중 매우 다름)** |
| 비중 합계 범위 | 85.0% (Claude) ~ 224.6% (DeepSeek) |
| 만장일치 시그널 | 6/25 (24%) |
| 분열 시그널 (2/4) | 10/25 (40%) |
| 만장일치 FTQ | **1/25 (GLD only)** |
| 강한 양의 상관 (Score) | Claude-DeepSeek r=0.616 |
| 강한 양의 상관 (Weight) | ChatGPT-DeepSeek r=0.782 |
| 음의 상관 | Gemini-DeepSeek r=-0.372 |

---

## 작성 정보

**분석 일자**: 2026-05-18
**비교 도구**: pandas 기반 정규화 + voting consensus 분석
**원본 CSV 파일**: `claude_0518.csv`, `gemini_0518.csv`, `chatgpt_0518.csv`, `deepseek_csv_20260517_84dd88.csv`
**저자**: 김호광 (Dennis Kim / HoKwang Kim) — Betalabs Inc., Independent Researcher
**GitHub**: [@gameworkerkim](https://github.com/gameworkerkim)
**라이선스**: MIT

---

> *"4개 모델이 같은 그림을 보고도 다른 그림을 그렸다. 진단 일치 ≠ 처방 일치. 합의는 voting 에서, 알파는 분열에서 나온다."*
