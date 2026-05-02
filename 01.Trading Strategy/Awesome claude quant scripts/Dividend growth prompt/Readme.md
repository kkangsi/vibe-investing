# Dividend Growth Prompt — 한국어/영어 프롬프트 + 3사 LLM 비교 분석

> **S&P 500 + NASDAQ-100 배당 성장 종목 발굴 LLM 프롬프트 + Claude / Gemini / DeepSeek 결과 실증 비교**

한 줄 요약 - 인공지능도 실수할 수 있다는 것을 보여주는 예
---

## 디렉터리 구조

```
Dividend growth prompt/
├── Readme.md                              # 본 문서 (3사 LLM 비교 분석)
├── Dividend Growth Prompt kr.MD           # 한국어판 프롬프트
├── Dividend_Growth_Prompt_EN.md           # 영문판 프롬프트 (토큰 31% 절감)
└── result/
    ├── Claude_Dividend_Growth_Portfolio_Report_2026Q2.md     # 24KB, 453 lines
    ├── DeepSeek Prompt Result260502.MD                       # 10.3KB, 136 lines
    └── Gemini_Dividend_Growth_Portfolio_2026.md              # 5.91KB, 81 lines
```

---

## 프롬프트 사용법

### 빠른 시작

| 사용 시나리오 | 권장 파일 | 토큰 절감 |
| --- | --- | --- |
| 한국어 출력 원함 | [Dividend Growth Prompt kr.MD](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt/Dividend%20Growth%20Prompt%20kr.MD) | - |
| **토큰 절감 (권장)** | [Dividend_Growth_Prompt_EN.md](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt/Dividend_Growth_Prompt_EN.md) | **−31%** |
| 영문 프롬프트 + 한국어 출력 | 영문판 + 끝에 *"Respond in Korean"* 추가 | −23% |

---

## 평가 환경

| 항목 | 내용 |
| --- | --- |
| 프롬프트 | 동일 영문/한국어 프롬프트 |
| 실행일 | 2026년 5월 2일 |
| Temperature | 기본값 (각 LLM default) |
| 평가 방식 | 단일 실행 (N=1) — *통계적 유의성 없음, 정성적 관찰만* |
| 비교 대상 | Claude (24KB, 453 lines), DeepSeek (10.3KB, 136 lines), Gemini (5.91KB, 81 lines) |

> **출력 분량 차이**: Claude 출력이 *Gemini의 4배* 분량. 이는 *위험 고지·내러티브 깊이·종목별 상세 분석* 측면에서 Claude의 우위를 시사하며, 동시에 *토큰 비용 4배* 의 트레이드오프를 의미.

---

## Part 1 — Top 10 종목 비교

### 1.1 3사 추천 종목 통합 매트릭스

| 티커 | 회사명 | Claude | DeepSeek | Gemini | 추천 LLM 수 | 평균 점수 |
| --- | --- | --- | --- | --- | --- | --- |
| **MSFT** | Microsoft | 85 (#6) | 88 (#1) | 88 (#1) | **3사 일치** | **87.0** |
| **UNH** | UnitedHealth | 84 (#2) | 82 (#5) | 93 (#3) | **3사 일치** | **86.3** |
| V | Visa | 86 (#4) | - | 92 (#4) | 2사 (C+G) | 89.0 |
| ABBV | AbbVie | 78 (#3) | 82 (#6) | - | 2사 (C+D) | 80.0 |
| BLK | BlackRock | 82 (#5) | 78 (#10) | - | 2사 (C+D) | 80.0 |
| AVGO | Broadcom | - | 86 (#2) | 89 (#2) | 2사 (D+G) | 87.5 |
| COST | Costco | 87 (#1) | - | - | 1사 (Claude only) | 87.0 |
| LRCX | Lam Research | 80 (#7) | - | - | 1사 (Claude only) | 80.0 |
| OKE | ONEOK | 75 (#8) | - | - | 1사 (Claude only) | 75.0 |
| NOC | Northrop Grumman | 79 (#9) | - | - | 1사 (Claude only) | 79.0 |
| GWW | W.W. Grainger | 81 (#10) | - | - | 1사 (Claude only) | 81.0 |
| JNJ | Johnson & Johnson | - | 84 (#3) | - | 1사 (DeepSeek only) | 84.0 |
| PEP | PepsiCo | - | 82 (#4) | - | 1사 (DeepSeek only) | 82.0 |
| CAT | Caterpillar | - | 81 (#7) | - | 1사 (DeepSeek only) | 81.0 |
| TXN | Texas Instruments | - | 79 (#8) | - | 1사 (DeepSeek only) | 79.0 |
| LIN | Linde | - | 79 (#9) | - | 1사 (DeepSeek only) | 79.0 |
| JPM | JPMorgan Chase | - | - | 90 (#5) | 1사 (Gemini only) | 90.0 |
| LOW | Lowe's Companies | - | - | 93 (#6) | 1사 (Gemini only) | 93.0 |
| LMT | Lockheed Martin | - | - | 89 (#7) | 1사 (Gemini only) | 89.0 |
| COP | ConocoPhillips | - | - | 91 (#8) | 1사 (Gemini only) | 91.0 |
| TMO | Thermo Fisher | - | - | 89 (#9) | 1사 (Gemini only) | 89.0 |
| ADP | ADP | - | - | 86 (#10) | 1사 (Gemini only) | 86.0 |

### 1.2 일치도 요약

* **3사 합의 (Strong Consensus)**: **MSFT, UNH** 만 *2종* — 매우 좁은 합의
* **2사 합의**: V, ABBV, BLK, AVGO 4종
* **1사 단독 추천**: 16종 — *각 LLM 의 학습 데이터 + 해석 차이* 를 보여주는 가장 큰 분산 영역
* **총 추천 종목 수**: 22종 (3사 합산, 중복 제거)

> **주요 시사점**: 동일 프롬프트에도 *3사 모두 동의한 종목은 단 2종*. 이는 *단일 LLM 의존의 위험성* 을 명확히 보여줍니다.

### 1.3 섹터 분포 비교 (프롬프트 명시 6대 섹터)

프롬프트가 *균등 분산* 을 요구한 *6대 섹터* 별 분포:

| 섹터 (프롬프트 명시) | Claude | DeepSeek | Gemini | 비고 |
| --- | --- | --- | --- | --- |
| **필수소비재** | 1 (COST) | 1 (PEP) | 0 | Gemini *위반*: LOW 를 필수소비재로 분류했으나 실제 *임의소비재* |
| **헬스케어 (제약·의료기기)** | 2 (UNH, ABBV) | 3 (JNJ, UNH, ABBV) | 2 (UNH, TMO) | DeepSeek *과집중* (3종) |
| **금융 (자산관리·카드)** | 2 (V, BLK) | 1 (BLK) | 2 (V, JPM) | Gemini *위반*: JPM 은 *전통 은행*, 자산관리·카드 아님 |
| **테크 (레거시 SW·반도체 장비)** | 2 (MSFT, LRCX) | 3 (MSFT, AVGO, TXN) | 2 (MSFT, AVGO) | DeepSeek *과집중* (3종) |
| **에너지 (인프라·미드스트림)** | 1 (OKE) | 0 | 1 (COP) | DeepSeek *완전 누락* / Gemini *분류 의심*: COP 는 *상류 E&P*, 미드스트림 아님 |
| **산업재 (방산·상업서비스)** | 2 (NOC, GWW) | 1 (CAT) | 2 (LMT, ADP) | DeepSeek 만 1종 |
| **소재** ★프롬프트에 없음 | 0 | **1 (LIN)** | 0 | DeepSeek *위반*: 소재 섹터는 프롬프트에 없음 |
| **합계** | 10 | 10 | 10 | - |

### 1.4 섹터 준수도 평가

| LLM | 6대 섹터 준수 | 위반 사항 | 점수 |
| --- | --- | --- | --- |
| **Claude** | **6/6 충실** | 없음 — *모든 섹터 1-2종 균등 분산* | **A** |
| **DeepSeek** | 5/6 — *에너지 누락* | LIN(소재) 가 프롬프트에 없는 섹터 / 에너지 0종 | C |
| **Gemini** | 6/6 명목상 충족하나 *분류 오류* | LOW(임의소비재→필수소비재 오분류) / JPM(은행→자산관리·카드 오분류) / COP(E&P 상류→미드스트림 오분류) | C+ |

> **Claude 가 섹터 준수도에서 명확한 우위** — 프롬프트가 명시한 6대 세부 섹터를 *오분류 없이* 모두 충족.

### 1.5 점수 분포 비교

| 지표 | Claude | DeepSeek | Gemini |
| --- | --- | --- | --- |
| 평균 총점 | **81.7** | 82.1 | **90.0** |
| 최고 점수 | 87 (COST) | 88 (MSFT) | 93 (UNH, LOW) |
| 최저 점수 | 75 (OKE) | 78 (BLK) | 86 (ADP) |
| 점수 표준편차 (추정) | ~3.7 | ~3.0 | ~2.5 |
| 점수 범위 (스프레드) | 12점 | 10점 | 7점 |

> **Gemini 의 점수 인플레이션 문제**: Gemini 평균 90점은 *이상치*. 100점 만점 시스템에서 *모든 종목이 86점 이상* 이라는 것은 *변별력 상실* 또는 *과신* 의 신호. Claude(81.7) / DeepSeek(82.1) 와 비교 시 약 **8점 인플레이션**. 사용자는 Gemini 점수를 *상대 비교에만* 활용해야 하며, *절대 점수로 매수 결정* 하지 말 것.

### 1.6 종목 선정의 *공통 오류 정정*

#### Gemini 의 섹터 오분류 정정

| 종목 | Gemini 분류 | 실제 분류 | 정정 |
| --- | --- | --- | --- |
| **LOW (Lowe's)** | 필수소비재 | **임의소비재 (Consumer Discretionary)** | Lowe's 는 home improvement 유통업체로 *경기민감* 임의소비재. 필수소비재 아님 |
| **JPM (JPMorgan Chase)** | 금융 (카드) | **금융 (전통 은행, Diversified Bank)** | JPM 은 commercial/investment bank 가 핵심 사업. 카드 사업은 일부일 뿐. 프롬프트 요구 *"자산관리·카드"* 와 명백히 다름 |
| **COP (ConocoPhillips)** | 에너지 (인프라) | **에너지 (상류 E&P, Upstream)** | ConocoPhillips 는 *원유·가스 생산* 회사로 상류(upstream). 프롬프트 요구 *"인프라·미드스트림"* 과 다름. 미드스트림은 EPD, ET, OKE, KMI 등 |

#### DeepSeek 의 섹터 누락/위반 정정

| 종목 | DeepSeek 분류 | 문제 | 정정 |
| --- | --- | --- | --- |
| **LIN (Linde)** | 소재 | **프롬프트에 *"소재"* 섹터 없음** | LIN 은 산업용 가스 — *소재 섹터* 분류 자체가 정확하나, 프롬프트 6대 섹터에 *소재* 가 포함되지 않으므로 *선정 자체가 부적절* |
| (에너지 누락) | 0종 | 프롬프트는 *에너지 1-2종 분산* 요구 | 에너지 종목 0개는 *섹터 분산 위반* |

#### Claude 의 섹터 분류 정확성 (참고)

| 종목 | Claude 분류 | 평가 |
| --- | --- | --- |
| OKE (ONEOK) | 에너지 미드스트림 | **정확** — 프롬프트 명세 *그대로* 충족 |
| LRCX (Lam Research) | 테크 반도체 장비 | **정확** — 프롬프트 명세 *반도체 장비* 정확히 일치 |
| GWW (Grainger) | 산업재 상업서비스 | **정확** — Dividend King (53년 연속 인상) + 프롬프트 명세 *상업서비스* 일치 |
| COST (Costco) | 필수소비재 | **정확** — Costco 는 wholesale + 멤버십 모델로 필수소비재 분류 일반적 |
| NOC (Northrop) | 산업재 방산 | **정확** |

---

## Part 2 — 추천 ETF 비교 (오류 정정 포함)

### 2.1 3사 ETF 추천 매트릭스

| ETF | Claude | DeepSeek | Gemini | 추천 LLM 수 |
| --- | --- | --- | --- | --- |
| **SCHD** (Schwab US Dividend Equity) | ★ | ★ | ★ | **3사 일치** |
| **VYM** (Vanguard High Dividend Yield) | ★ | - | ★ | 2사 (C+G) |
| **DGRO** (iShares Core Dividend Growth) | - | ★ | ★ | 2사 (D+G) |
| **JEPI** (JPMorgan Equity Premium Income) | ★ | ★ | - | 2사 (C+D) |

> **3사 모두 추천 = SCHD 단 1종**. 모든 LLM 이 SCHD 를 *최고 배당 ETF* 로 인정.

### 2.2 ETF 핵심 지표 비교

#### SCHD (3사 모두 추천)

| 지표 | Claude | DeepSeek | Gemini | 검증 (참고) |
| --- | --- | --- | --- | --- |
| 운용보수 | 0.06% | 0.06% | 0.06% | 0.06% (3사 일치) |
| 순자산 (AUM) | $68B | $64B+ | $62B | 약 $60-70B 범위 (모두 합리적) |
| 30일 SEC Yield | **3.62%** | **3.41%** | **3.4%** | 약 3.4-3.6% (시점 차이 가능) |
| 분배 주기 | 분기 | 분기 | 분기 (No 월배당) | 분기 (3사 일치) |

> **Claude 의 SEC Yield 3.62% 가 다른 두 LLM 보다 약 0.2%p 높게 추정**. 시점 + 데이터 cutoff 차이로 보이며, 모두 *프롬프트 조건 (≥2.5%) 충족*.

#### JEPI (Claude + DeepSeek)

| 지표 | Claude | DeepSeek |
| --- | --- | --- |
| 운용보수 | 0.35% | 0.35% |
| 순자산 (AUM) | $42B | $36B+ |
| 30일 SEC Yield | **7.45%** | **7.12%** |
| 분배 주기 | **월배당** | **월배당** |

> **JEPI 는 *옵션 프리미엄 (Covered Call)* 기반 ETF**. Claude 가 명시한 대로 분배금의 *60-70% 가 옵션 프리미엄*, *30-40% 만 배당*. 따라서 *순수 배당 성장 ETF 가 아님*. **사용자 주의**: JEPI 를 SCHD 와 같은 카테고리로 보면 안 됨.

#### VYM (Claude + Gemini)

| 지표 | Claude | Gemini |
| --- | --- | --- |
| 운용보수 | 0.06% | 0.06% |
| 순자산 (AUM) | $58B | $55B |
| 30일 SEC Yield | 2.78% | 2.9% |
| 분배 주기 | 분기 | 분기 |

#### DGRO (DeepSeek + Gemini)

| 지표 | DeepSeek | Gemini |
| --- | --- | --- |
| 운용보수 | 0.08% | 0.08% |
| 순자산 (AUM) | $28B+ | $29B |
| 30일 SEC Yield | 2.35% | 2.4% |
| 분배 주기 | 분기 | 분기 |

> **DGRO 의 SEC Yield 2.35% / 2.4% 는 프롬프트 조건 *≥2.5%* 미충족 가능성**. DeepSeek/Gemini 모두 *프롬프트 조건 위반* 후보 추천. 실제 SEC Yield 가 시점에 따라 2.4-2.6% 사이를 오가므로 *경계선* 이지만, *Claude 는 이 ETF 를 추천하지 않음* 으로써 *조건 엄격 준수*.

### 2.3 ETF 추천의 *오류 정정*

| 오류 | LLM | 정정 |
| --- | --- | --- |
| **DGRO의 SEC Yield 조건 미달 가능성** | DeepSeek (2.35%), Gemini (2.4%) | 프롬프트 조건 *≥2.5%* 와 정확히 일치하지 않음 — 시점에 따라 2.5% 미달 가능. *경계선 후보* 로 표시 권장. *Claude 는 이를 회피하여 VYM (2.78%) 과 SCHD 만 분기배당 + JEPI 월배당으로 구성* |
| **JEPI 를 *배당 성장 ETF* 로 오해** | Claude, DeepSeek | JEPI 는 *옵션 프리미엄 income ETF*. 분배금의 *60-70% 가 옵션 매도 수익* 으로 *세제상 일반소득 (한국: 배당소득세 + 종합과세 합산)*. *순수 배당 성장 카테고리 아님* — Claude는 이 점을 *명확히 명시*, DeepSeek는 *명시 부족* |
| **SCHD Top 5 보유 종목 차이** | Claude vs DeepSeek 다른 종목 | Claude: VZ, CSCO, PFE, TXN, HD / DeepSeek: HD, CSCO, TFC, CVX, PNC — *시점 + 데이터 cutoff 차이*. 두 LLM 모두 *데이터 시점 명시 필요*. Gemini는 Top 5 미명시 |

---

## Part 3 — 동일가중 포트폴리오 비교

### 3.1 핵심 지표 비교

| 지표 | Claude | DeepSeek | Gemini |
| --- | --- | --- | --- |
| **세전 배당수익률** | **2.10%** | **2.08%** | **2.05%** |
| 5년 배당 CAGR | 11.4% | (미표기) | (미표기) |
| Forward P/E | 22.3x | (미표기) | (미표기) |
| 평균 배당성향 | 34.6% | (미표기) | (미표기) |
| 추정 변동성 | 17.8% | (미표기) | (미표기) |
| **추정 Sharpe Ratio (3Y)** | **0.82** | **1.45** ⚠️ | **1.25** ⚠️ |
| **추정 Maximum Drawdown** | -21.4% | -18.2% | -18.5% |
| 베타 (vs S&P 500) | 0.92 | (미표기) | (미표기) |
| **12개월 기대수익률** | **+13.3%** | **+13.5%** | (수치 미표기) |

> **세전 배당수익률은 3사 매우 근접 (2.05-2.10%)**. 이는 *프롬프트의 배당 성장 조건 (≥8% CAGR + 페이아웃 ≤60%)* 이 *낮은 현재 yield + 높은 미래 성장* 종목을 자동 필터링한 결과. *고배당 yield 가 아닌 배당 성장* 전략의 본질을 잘 보여줌.

### 3.2 Sharpe Ratio 의 학술적 의심

학술 문헌에서 *Sharpe Ratio* 해석:

| Sharpe Ratio | 해석 |
| --- | --- |
| 1.5+ | **이론적으로 매우 우수**. 헤지펀드 최상위. **단, value-only 또는 long-only 전략은 *too good to be true* 의심** |
| 1.0-1.5 | 우수. 멀티팩터 + 리스크 관리 잘 된 포트폴리오 |
| 0.7-1.0 | 양호. 일반적인 우수 헤지펀드 |
| 0.5-0.7 | 보통. 인덱스 펀드 수준 |
| < 0.5 | 부족 |

**3사 LLM 추정값 평가**:

* **Claude 0.82**: *학술적으로 합리적*. Long-only dividend growth 전략의 *현실적 범위* (보통 0.6-1.0)
* **Gemini 1.25**: *경계*. 다소 낙관적이지만 가능 범위
* **DeepSeek 1.45**: **Too good to be true 의심**. Long-only + 무위험금리 5% 가정 시 *Excess Return ≈ 8.5%/연* 이 변동성 대비 너무 우수. 이는 *과거 3년 (2022.04-2025.04)* 의 *cherry-picked period* 또는 *변동성 과소추정* 의 결과 가능

### 3.3 무위험금리 가정의 차이

| LLM | 가정 무위험금리 | 비고 |
| --- | --- | --- |
| Claude | **4.20% (10Y UST)** | *명시적* 으로 표기. 학술 표준 |
| DeepSeek | **5.00%** | 의외로 높음 — 2022-2023 일시 고점 반영 가능 |
| Gemini | (미표기) | *투명성 부족* |

> **DeepSeek 의 5% 무위험금리 + Sharpe 1.45 조합은 일관되지 않음**. 무위험금리가 5%면 Excess Return 이 더 작아져야 하므로 Sharpe 가 낮아져야 하는데, 오히려 *Sharpe 1.45* 라는 것은 *변동성을 과소추정* 했음을 시사.

### 3.4 12개월 기대수익률 비교

| LLM | 기대수익률 | 시나리오 분석 |
| --- | --- | --- |
| **Claude** | **+13.3%** | 4가지 시나리오 (강세 35% / 기본 45% / 약세 15% / 침체 5%) 가중평균. *방법론 명시* |
| **DeepSeek** | **+13.5% ± 5%** | 단순 추정치. *범위 명시는 좋음* |
| **Gemini** | (수치 미제공) | *"연간 3-5%p 알파 기대"* 만 정성적 표현 — *정량 미흡* |

---

## 3사 LLM 의 *관찰된* 특성 (실증 기반)

### Claude Opus 4.7

**관찰된 강점**:

* **출력 분량 압도적**: 24KB / 453 lines — *Gemini의 4배, DeepSeek의 2.3배*
* **위험 고지 충실**: 각 종목별 risk factor 2가지 + stop-loss + ±5% 오차범위 *모두 충실히 명시*
* **섹터 준수도 A등급**: 프롬프트 6대 섹터 *오분류 없이* 모두 충족
* **방법론 투명성**: Sharpe 0.82 (현실적), 무위험금리 4.20% 명시, 시나리오 분석 4가지 + 확률 가중평균
* **개인 컨텍스트 통합**: V (Visa) 분석에서 *"Dennis님이 작업 중인 STABLE1 같은 Web3 결제 인프라"* 언급, OKE 분석에서 *"Dennis님의 글로벌 자산 운용 관점"* — 이는 *과거 대화 기억* 활용 (메모리 기능 사용 시)
* **사용자별 맞춤 카테고리**: COST 의 멤버십 수익을 *"채권화"* 로 형식화

**관찰된 약점**:

* **토큰 비용 가장 높음**: 출력 분량 4배 = *비용 4배*
* **반도체 장비 (LRCX), Costco (COST) 같은 *비주류* 종목 강조** — 합의도 낮음
* **AI 빅테크 노출 부족**: AVGO 누락 — DeepSeek/Gemini 와 차별화

### DeepSeek V3.1 / V4

**관찰된 강점**:

* **점수 매트릭스 명확**: 표 형식 깔끔, 비교 용이
* **AI 빅테크 적극 발굴**: AVGO #2, MSFT #1 — Alpha Arena +46% 학습 효과 시사
* **Sharpe Ratio 명시 (1.45)**: *수치 자체는 의심* 이나 *제공한 점은 평가*

**관찰된 약점**:

* **섹터 위반**: LIN (Linde) 은 *소재 섹터* — 프롬프트 6대 섹터에 없음
* **에너지 섹터 완전 누락**: 프롬프트의 *에너지 1-2종 분산* 요구 무시
* **헬스케어 + 테크 과집중** (각 3종) — 균등 분산 약함
* **Sharpe Ratio 1.45 + 무위험금리 5% 의 비일관성** — 변동성 과소추정 의심
* **PEP 배당성향 65% 추천** — 프롬프트 조건 *≤60% 위반*
* **위험 고지 분량 부족**: Claude 대비 *상세도 약함*
* **출력 분량 불균등**: Top 1-3 은 상세, Top 7-10 은 간략 — *서두 가중*

### Gemini 3.x

**관찰된 강점**:

* **출력 가장 간결**: 5.91KB / 81 lines — *토큰 비용 최저*
* **Top 3 (UNH, LOW, V) 상세 분석**: *3사 중 가장 깊은 종목별 내러티브* (단, Top 3 만)

**관찰된 약점**:

* **점수 인플레이션 심각** (평균 90점, 표준편차 2.5) — *변별력 상실*
* **섹터 오분류 3건**:
  * LOW (Lowe's): *임의소비재* 를 *필수소비재* 로 오분류
  * JPM (JPMorgan): *전통 은행* 을 *카드 (자산관리·카드)* 로 오분류
  * COP (ConocoPhillips): *상류 E&P* 를 *인프라 (미드스트림)* 으로 오분류
* **방법론 투명성 부족**: 무위험금리 미명시, 시나리오 분석 없음
* **포트폴리오 12개월 기대수익률 정량 미제공**
* **Top 4-10 종목별 분석 누락** — Claude/DeepSeek 대비 부족

---

## 핵심 상이점 정리

### 1. *섹터 분산* 충실도

```
Claude    ★★★★★  6대 섹터 모두 정확히 분산 (Grade A)
Gemini    ★★      6/6 명목상 충족, 3건 오분류 (Grade C+)
DeepSeek  ★★      5/6 충족, 에너지 누락 + LIN 위반 (Grade C)
```

### 2. *점수 변별력* (표준편차)

```
Claude    ~3.7  점수 범위 75-87 (12점 스프레드) — 변별력 우수
DeepSeek  ~3.0  점수 범위 78-88 (10점 스프레드) — 변별력 양호
Gemini    ~2.5  점수 범위 86-93 (7점 스프레드) — 변별력 부족 + 인플레
```

### 3. *Sharpe Ratio 신뢰성*

```
Claude   0.82  ★★★ 학술 합리적 범위, 무위험금리 4.20% 명시
Gemini   1.25  ★★  경계 영역, 무위험금리 미명시
DeepSeek 1.45  ★   too good to be true, 무위험금리 5% 와 비일관
```

### 4. *위험 고지 분량*

```
Claude    24KB ★★★★★  종목별 risk factor 2가지 + stop-loss + 시나리오 4가지
DeepSeek  10KB ★★★    종목별 risk 1가지, 시나리오 분석 없음
Gemini    6KB  ★★     Top 3 만 상세, 나머지 누락
```

### 5. *프롬프트 조건 준수도*

| 조건 | Claude | DeepSeek | Gemini |
| --- | --- | --- | --- |
| 6대 섹터 분산 | ★★★ | ★ (LIN 위반, 에너지 누락) | ★★ (3건 오분류) |
| 배당성장 ≥8% CAGR | ★★★ | ★★★ | ★★★ |
| 배당성향 ≤60% | ★★★ | ★★ (PEP 65%, TXN 62%) | ★★ (LMT 45%, ADP 58%) |
| ETF 운용보수 ≤0.35% | ★★★ | ★★★ | ★★★ |
| ETF SEC Yield ≥2.5% | ★★★ | ★★ (DGRO 2.35% 미달) | ★★ (DGRO 2.4% 경계) |
| ±5% 오차범위 명시 | ★★★ | ★★★ | ★★★ |

> **DeepSeek 의 PEP 배당성향 65% 는 *프롬프트 조건 ≤60% 위반***.

---

## 사용자에게 주는 권고

### 1. *Consensus Picks* 부터 매수 검증

3사 LLM 모두 추천한 **MSFT, UNH** 는 *학습 데이터의 강한 시그널* 을 가진 *합의 종목*. 이 2종부터 *독립 데이터 소스* (SeekingAlpha, Morningstar, 10-K) 로 검증 시작.

**2사 합의** (V, ABBV, BLK, AVGO) 도 *중요 후보군*. 특히:
* **V (Visa)**: Claude + Gemini 모두 86-92점 부여 — *고합의 + 고점수*
* **AVGO (Broadcom)**: DeepSeek + Gemini 86-89점 — *AI 빅테크 노출* 측면에서 Claude 의 누락 보완

### 2. *단독 추천 종목* 신중 검토

각 LLM 의 *unique pick* 은 *학습 데이터 우위* 또는 *해석 차이* 의 결과:

| LLM | 단독 추천 | 의미 |
| --- | --- | --- |
| Claude | COST, LRCX, OKE, NOC, GWW | *Dividend Aristocrat* 강조 (GWW 53년 연속), *반도체 장비* 정확 분류 |
| DeepSeek | JNJ, PEP, CAT, TXN, LIN | *AI 인프라 + 산업재* 강조 (CAT 데이터센터 전력), 단 LIN 은 섹터 위반 |
| Gemini | JPM, LOW, LMT, COP, TMO, ADP | *방산 (LMT) + 의료기기 (TMO)* 강조, 단 JPM/LOW/COP 은 섹터 오분류 |

→ *단독 추천 종목* 은 *반드시 SEC EDGAR 10-K + Morningstar* 로 *교차 검증*.

### 3. Gemini 점수 인플레이션 주의

Gemini 의 *평균 90점 / 표준편차 2.5* 는 *모든 종목이 우수* 라는 *변별력 부족* 출력. **Gemini 점수를 *상대 비교* 에는 사용 가능, *절대 매수 결정* 에 사용하지 말 것**.

### 4. DeepSeek Sharpe Ratio 1.45 의심

DeepSeek 의 Sharpe 1.45 는 *학술적으로 too good to be true*. 실제 백테스트 시 *1.0 미만* 일 가능성 높음. **DeepSeek 의 정량 추정치를 그대로 신뢰하지 말 것**.

### 5. ETF 포트폴리오 권장 (오류 정정 후)

3사 합의 + 오류 정정 후 *최종 ETF 포트폴리오*:

| 역할 | ETF | 권장 비중 | 이유 |
| --- | --- | --- | --- |
| **코어** | **SCHD** | 50% | 3사 모두 추천 + 운용보수 0.06% + Yield 3.4-3.6% + 분기배당 |
| **분산 위성** | VYM 또는 DGRO | 30% | VYM (광범위 540종 분산) 또는 DGRO (배당성장 순수, 단 yield 2.5% 경계) |
| **인컴 위성** | JEPI (선택) | 20% (또는 0%) | **주의**: 옵션 프리미엄 ETF, *순수 배당 성장 아님*. 한국 거주자 *세제 비효율* 가능 |

> **JEPI 사용 시 주의**: 분배금의 60-70% 가 옵션 매도 수익으로 *일반소득 과세*. 한국 거주자는 *종합과세 합산* 시 세후 수익률이 SCHD 대비 낮을 수 있음. *세제 효율* 만 보면 *VYM 또는 DGRO 가 우월*.

### 6. *Cross-LLM Validation* 권장 워크플로

```
1단계: DeepSeek 로 1차 분석 (비용 효율) → 22종 후보군 도출
       ↓
2단계: Claude 로 위험 검증 (보수적) → 섹터 분산 + risk factor 심화
       ↓
3단계: Gemini 로 최신 데이터 cross-check (Google Finance 통합 시)
       ↓
4단계: 3사 합의 종목 (MSFT, UNH) → Core 포지션
       2사 합의 (V, ABBV, BLK, AVGO) → Satellite
       1사 단독 (16종) → Watchlist (독립 데이터 검증 후 판단)
```

---

## 한계와 주의사항

### 본 비교 분석의 한계

1. **단일 실행 (N=1)** — 동일 LLM 도 재실행 시 *다른 결과* 가능. *통계적 유의성 없음*
2. **시점 한정** — 2026년 5월 2일 실행. 학습 데이터 cutoff 차이 존재
3. **모델 버전** — 각 LLM 의 정확한 버전 명시 어려움 (서비스 업데이트로 변동)
4. **저자 단일 평가** — 객관적 벤치마크 아님

### LLM 사용의 일반 위험

* **Hallucination**: 모든 LLM 이 *존재하지 않는 종목/배당 데이터* 보고 가능
* **Look-ahead bias**: 학습 데이터에 *미래 정보 누설* 가능
* **Survivorship bias**: 학습 데이터 *생존 종목 편중*, 상폐된 dividend cutter 누락
* **데이터 cutoff**: *실시간 가격/배당 아님* — 반드시 *독립 데이터 소스 교차 검증*

### Disclaimer

* 본 비교 분석은 *교육·연구 목적* — 실제 투자 권유 아님
* 본 비교는 *단일 실행 (N=1)* 결과로 *통계적 유의성 없음*
* 모든 투자 결정은 *독립 데이터 소스 + 전문가 상담* 후 본인 책임
* **과거 배당 기록이 미래 배당을 보장하지 않습니다**
* *DeepSeek 같은 중국 LLM* 사용 시 *지정학적 위험* 별도 검토
* 한국 거주자: *외환거래법 + 양도소득세 22% + 종합과세* 별도 확인

---

## 향후 확장 계획

### v2.0 (계획)

* **N≥10 반복 실행** — 통계적 유의성 확보
* **추가 LLM** — GPT-5.4, Qwen3 Max, Claude Sonnet 4.6
* **Hyperparameter 비교** — temperature 0.0 / 0.3 / 0.7
* **12개월 후 검증** — 실제 수익률 vs 예측 backtest

### v3.0 (장기)

* **자동 LLM Battle Pipeline** — Python 스크립트 자동 호출 + 결과 합산
* **Consensus + Dissent 자동 분류**
* **Streamlit Dashboard**

---

## 작성 정보

**시리즈**: vibe-investing — Awesome Claude Quant Scripts
**연관 sub-strategy**:
* [AI Supply Chain Bayesian Analysis](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/AI%20supply%20chain%20bayesian%20analysis)
* [DAT Quant Strategy](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/DAT%20quant%20strategy)
* [Long-Term Dividend Investing](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Long-Term%20Dividend%20Investing) — *코드 구현 보완판*
* [Declining Stock Quant Script Using LLM](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Declining%20Stock%20Quant%20Script%20Using%20LLM) — *반대 전략 (하락 + 인버스)*

**저자**: 김호광 (Dennis Kim / HoKwang Kim)
- Independent Researcher, Betalabs Inc. CEO, Cyworld Z 전 CEO
- ORCID: [0009-0002-0962-2175](https://orcid.org/0009-0002-0962-2175)
- GitHub: [@gameworkerkim](https://github.com/gameworkerkim)
- Email: [gameworker@gmail.com](mailto:gameworker@gmail.com)

**작성일**: 2026년 5월 2일 v1.0 (실제 3사 LLM 결과 데이터 반영)
**라이선스**: MIT (자유 사용, 출처 표기 권장)

---

> *"One LLM may hallucinate. Three LLMs converge on truth — but only when they disagree do you find the alpha."*
> *"하나의 LLM 은 환각을 만들 수 있다. 세 LLM 이 합의할 때 진실에 가까워진다 — 그러나 그들이 의견이 갈릴 때, 비로소 알파를 발견한다."*
