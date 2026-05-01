# vibe investing

> **인공지능을 이용한 바이브 투자(Vibe Investing) 관련 의견과 자료를 나누는 레포**

AI 투자(Vibe Investing) 큐레이션 어썸 시리즈 4편, 시장 분석 칼럼 9편, **SSRN 제출 학술 논문 1편 (리뷰 전)**, AI 트레이딩 도구 3종 (Harness Quant v2 + Earnings Momentum Agent + Nasdaq-BTC Coupling Bot) 을 다룹니다. 리서치하는 마켓은 미국 나스닥, S&P500, 가상화폐, 유럽 명품 섹터, 크립토-주식 상관관계, **BNB Chain 생태계, DeFi 대안 금융, AI 공급망, DAT 퀀트, 장기 배당주, DeepSeek V4** 입니다. 인공지능은 엑셀과 같은 도구입니다. LLM은 만능이 아니며, 모델을 읽는 인간의 통찰력이 가장 중요하다고 믿습니다. 지금 비트코인과 나스닥의 커플링의 시그널이 강력한 가운데 우리는 소음과 신호에서 신호를 인공지능이라는 도구를 통해 발견할 수 있습니다.

트레이딩은 도박이 아닙니다. 자신의 인사이트를 통해서 주식과 크립토 마켓에서 새로운 가치를 발견하는 관조의 과정이라고 믿습니다.

2026년 4월 25일 추가된 LLM을 이용한 Awesome Claude Quant Scripts에 **4개의 sub-strategy (AI Supply Chain Bayesian Analysis, DAT Quant Strategy, Long-Term Dividend Investing, Declining Stock Quant Script) 가 추가** 되었습니다.
**2026년 5월 1일 추가된 BNB Chain 분배 비대칭 학술 논문 (SSRN 6688740) 은 본 레포 최초의 학술 working paper 이며, 현재 SSRN 분류팀 검토 대기 중 (PRELIMINARY_UPLOAD) 입니다
.** 동반 논문 SSRN 6632838 (72-Hour Shock) 과 함께 *2-paper 시리즈* 를 이룹니다. 

동시에 **Awesome Vibe Trading Bot (14종 트레이딩 봇 평가)**, **DeFi 대안 금융 칼럼**, **DeepSeek V4 칼럼** 도 새로 추가되었습니다.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with](https://img.shields.io/badge/Made%20with-Claude%20%2B%20Python-blue)](https://github.com/gameworkerkim/vibe-investing/blob/main)
[![Updates](https://img.shields.io/badge/Updates-Weekly-brightgreen)](https://github.com/gameworkerkim/vibe-investing/blob/main)
[![Awesome Lists](https://img.shields.io/badge/Awesome--Lists%20%C3%97%204-orange)](https://github.com/gameworkerkim/vibe-investing/blob/main)
[![Columns](https://img.shields.io/badge/Columns-9%20Published-purple)](https://github.com/gameworkerkim/vibe-investing/blob/main)
[![Academic](https://img.shields.io/badge/Academic-1%20SSRN%20Working%20Paper-red)](https://ssrn.com/abstract=6688740)
[![Tools](https://img.shields.io/badge/Tools-3%20Built-cyan)](https://github.com/gameworkerkim/vibe-investing/blob/main)
[![Datasets](https://img.shields.io/badge/Datasets-16%2B%20CSV-red)](https://github.com/gameworkerkim/vibe-investing/blob/main)

---

## Curation Map

아래 다이어그램은 **Awesome Claude Quant Scripts**가 정리한 8대 퀀트 전략 분류 체계입니다. 본 레포의 칼럼·도구·데이터셋은 이 분류 위에서 작동합니다 — 예컨대 *Earnings Momentum Agent*는 Growth × Quality × Momentum 멀티팩터, *Nasdaq-BTC Coupling Bot*은 Statistical Arbitrage / Time-Series Momentum, *DAT mNAV 칼럼*은 Value/Pair Trading의 변형, *Long-Term Dividend Investing*은 Quality + Value, *AI Supply Chain Bayesian Analysis*는 ML + Multi-Factor 변형입니다.

[![Trading Strategy Taxonomy — Awesome Claude Quant Scripts](https://github.com/gameworkerkim/vibe-investing/raw/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/trading%20map.png)](/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/trading%20map.png)

> 4대 핵심 팩터 (Value, Growth, Quality, Momentum) + 4대 고급 전략 (Multi-Factor, Trend Following, Statistical Arbitrage, Machine Learning) — 각 전략별 학계·업계 대가의 원전 논문, Python 코드 골격, Claude 프롬프트 템플릿 큐레이션은 [Awesome Claude Quant Scripts](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Awesome%20claude%20quant%20scripts.MD) 참조.

**4개의 sub-strategy 추가 (2026년 4-5월)**:
* [AI Supply Chain Bayesian Analysis](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/AI%20supply%20chain%20bayesian%20analysis) — Bayesian 추론으로 AI 공급망 종목 분석
* [DAT Quant Strategy](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/DAT%20quant%20strategy) — Digital Asset Treasury 기업 (MSTR, BMNR 등) 퀀트 전략 (8번 칼럼의 코드 구현)
* [Long-Term Dividend Investing](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Long-Term%20Dividend%20Investing) — 장기 배당주 발굴 + Quality 팩터 통합
* [Declining Stock Quant Script Using LLM](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Declining%20Stock%20Quant%20Script%20Using%20LLM/Declining%20Stock%20Quant%20Script%20Using%20LLM.MD) — 하락 종목 탐지 + 인버스(숏) ETF 매칭 LLM 프롬프트 (S&P 500 + NASDAQ-100)

---

## Quick Links

### 어썸 큐레이션 시리즈

| # | 제목 | 다루는 영역 |
| --- | --- | --- |
| 1 | [**Awesome Vibe Invest — Stocks & Equities**](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20vibe%20invest.MD) | 주식 (NASDAQ / S&P500) — 30+ AI 투자 GitHub 레포 평가 |
| 2 | [**Awesome Vibe Invest — Crypto & DeFi Edition**](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20vibe%20invest%20crypto.MD) | 비트코인 / 크립토 — 벤치마크 중심 LLM 트레이딩 큐레이션 |
| 3 | [**Awesome Claude Quant Scripts**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Awesome%20claude%20quant%20scripts.MD) | 퀀트 전략 8종 — 학계 원전 논문 30+편 + Claude 프롬프트 + Python 골격 + sub-strategy 3종 |
| 4 | [**Awesome Vibe Trading Bot**](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20Vibe%20Trading%20Bot.MD) | 14개 코인 트레이딩 봇 평가 — 전통 봇 8종 (Freqtrade, Hummingbot 등) + AI/LLM 봇 6종 (TradingAgents, FinRL 등) |

### 칼럼 시리즈

| # | 제목 | 주제 |
| --- | --- | --- |
| 1 | [**LTCM의 사례로 배우는 모델을 읽는 힘**](https://github.com/gameworkerkim/vibe-investing/blob/main/Vibe%20Investing%20Risk%20Management.MD) | 1998년 LTCM 사태 분석 + 2026년 AI 바이브 투자의 리스크 |
| 2 | [**Microsoft의 Fintool 인수 — Excel이 곧 Bloomberg가 되는 날**](https://github.com/gameworkerkim/vibe-investing/blob/main/Microsoft%20fintool%20acquisition%20column.MD) | Microsoft의 Fintool 인수 시너지 분석 |
| 3 | [**보이지 않는 손인가, 계획딘 사기인가**](https://github.com/gameworkerkim/vibe-investing/blob/main/Crypto%20perp%20manipulation%20column.MD) | 가상화폐 선물 시장의 비정상적 pump & dump 패턴 수학적 검토 |
| 4 | [**시장은 닫혔을 때 열리는가**](https://github.com/gameworkerkim/vibe-investing/blob/main/AfterMarketClose/After_Market_Close_Column.md) | 미국 상장기업 91.2%가 AMC에 악재를 공시하는 이유 — 34건 실증 데이터 |
| 5 | [**DAT 기업의 mNAV 아비트리지 전략**](https://github.com/gameworkerkim/vibe-investing/blob/main/mNAV(Market-to-Net-Asset-Value)%20arbitrage/Dat%20mnav%20arbitrage%20strategy.MD) | MSTR, BMNR 등 디지털 자산 보유 기업의 크립토 가치-시총 격차 분석 |
| 6 | [**명품은 언제 사야 하는가**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Luxury%20investment%20strategy/Luxury%20investment%20strategy.md) | LVMH, Hermès, Kering — 중국 경기 침체 시대의 명품 투자 3단계 전략 |
| 7 | [**가상화폐와 나스닥은 얼마나 동기화되고 있을까?**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/Nasdaq%20crypto%20coupling%20strategy.MD) | BTC-QQQ 6년 상관관계 + 6 regime 분류 + 인트라데이 lag 측정 |
| 8 | [**DeFi 대안 금융 — 전통 은행을 대체할 수 있을까?**](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/DeFi/Defi%20alternative%20finance%20column%20kr.MD) | DeFi가 전통 금융을 대체할 가능성 분석 — Aave, Compound, MakerDAO, Curve, Uniswap |
| 9 | [**DeepSeek V4 — 중국발 LLM의 트레이딩 활용 가능성**](https://github.com/gameworkerkim/vibe-investing/tree/main/02.Investment%20Idea%20Column/DeepSeek%20V4) | DeepSeek V4 모델 분석 + Alpha Arena Season 1에서 DeepSeek V3.1이 +46% 1위한 의미 |

### 학술 논문 (SSRN Working Paper)

| # | 제목 | 상태 |
| --- | --- | --- |
| 1 | [**Distribution Asymmetry of Centralized Exchange Airdrops and the BNB Chain Ecosystem**](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/README_KR.md) [[**논문 PDF**](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/paper/Distribution_Asymmetry_CEX_Airdrops_with_figures.pdf)] | 바이낸스 Megadrop / HODLer Airdrop 의 분배 비대칭 메커니즘 — 7개 정리 + 부트스트랩 95% CI + N=21 토큰 + Hyperliquid HYPE 반사실 + 디커플링 패턴 (SSRN 6688740, **PRELIMINARY_UPLOAD — 분류팀 검토 대기 중**) |
| 2 | [**The 72-Hour Shock: Token Unlock Price Impact**](https://ssrn.com/abstract=6632838) | 토큰 언락 72시간 가격 영향 분석 (SSRN 6632838, 동반 논문) |

### 직접 개발 중인 도구

| # | 제목 | 설명 |
| --- | --- | --- |
| 1 | [**Harness Quant v2**](https://github.com/gameworkerkim/vibe-investing/blob/main/Harness%20quant%20v2%20readme%20.MD) | LLM 기반 NASDAQ/S&P500 분석 패키지 (6개 시나리오 + 백테스트 + MCP + 멀티 에이전트 토론) |
| 2 | [**Earnings Momentum Agent**](https://github.com/gameworkerkim/vibe-investing/blob/main/Harness%20quantv2/Earnings%20momentum%20agent%20readme%20.MD) | 저점 반등 + 매출 성장 + 어닝 서프라이즈 + 시장 심리 종합 Top 30 추천 파이프라인 (24개월 백테스트 hit rate 83.3%) |
| 3 | [**Nasdaq-BTC Coupling Bot**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/) | BTC-QQQ 30일 rolling correlation 실시간 추적 + 6 regime 분류 + 트레이딩 신호 생성 (547 lines, 10 classes) |

---

## Vibe Investing이란?

**Vibe Coding**(바이브 코딩)이 자연어로 LLM에 지시해서 코드를 만드는 패러다임이라면,
**Vibe Investing**(바이브 인베스팅)은 자연어 지시 → LLM이 도구를 호출 → 시장 데이터·뉴스·소셜 신호 수집·분석 → 투자 의사결정 산출까지의 **agentic 파이프라인**을 지칭합니다.

전통적 알고리즘 트레이딩이 "if RSI < 30 then buy" 같은 경직된 룰 기반이라면, vibe investing은 다음과 같이 정의될 수 있습니다.

* **자연어로 전략 정의** ("섹터가 호전되고 시장에서 호평받는 종목을 찾아줘")
* **LLM이 능동적으로 도구 호출** (가격, 펀더멘털, 뉴스, 소셜, 내부자 거래, 온체인 데이터)
* **다층적 추론과 합의** (Bull/Bear/Risk/PM 멀티 에이전트 토론)
* **JSON으로 구조화된 결정** (사람이 검증 가능한 reasoning trail)

이 레포는 vibe investing의 **현재 도구·솔루션 지형을 정리**하고, **시장의 흐름을 분석한 칼럼**을 함께 공개하며, **직접 만들고 있는 레퍼런스 구현체**도 함께 공유합니다. **2026년 5월부터는 SSRN 학술 working paper 시리즈도 추가** 되어, 시장 패턴의 *수학적 형식화* 까지 영역을 확장합니다.

---

## 이 레포에는 무엇이 있나요?

### 1. Awesome Vibe Invest — Stocks & Equities

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20vibe%20invest.MD)

NASDAQ / S&P500을 분석하는 AI 도구 30+ 큐레이션. 12개 카테고리 (멀티 에이전트 프레임워크, 강화학습 트레이딩, 금융 LLM, 백테스트 엔진, MCP 인프라, 한국 시장 자원, 공통 함정 등).

### 2. Awesome Vibe Invest — Crypto & DeFi Edition

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20vibe%20invest%20crypto.MD)

비트코인을 비롯한 암호화폐 LLM 트레이딩 큐레이션. **벤치마크 결과**와 **지속적 업데이트**를 갖춘 프로젝트 중심으로 평가.

**가장 중요한 데이터 — Alpha Arena Season 1 결과**:

* **DeepSeek V3.1**: +46% (실제 자본 $10,000 → $14,764)
* Qwen3 Max
* Claude Sonnet 4.5
* Grok 4
* Gemini 2.5 Pro
* **GPT-5**: -75%

→ **모델 IQ가 곧 트레이딩 IQ는 아니다** 라는 사실을 입증한 최초의 실거래 벤치마크.

### 3. Awesome Claude Quant Scripts — 퀀트 전략 + Claude 프롬프트 큐레이션

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Awesome%20claude%20quant%20scripts.MD)

> *"Claude가 생성한 코드는 항상 사람이 검증해야 한다.*
> *직접 검증할 능력이 없다면, 다른 LLM을 통해서라도 교차 검증 및 환각을 필터링해야 한다."*

**8대 퀀트 전략을 학계 원전 → Python 코드 골격 → Claude 프롬프트 템플릿의 3-레이어로 묶은 종합 레퍼런스.** Vibe Investing이 *어떤 도구를 쓰느냐* 에 대한 큐레이션이라면, 이 어썸 리스트는 *어떤 전략을 어떤 이론적 기반 위에서 돌리느냐* 에 대한 큐레이션입니다.

**다루는 8대 전략**: Value, Growth, Quality, Momentum (4대 핵심 팩터) + Multi-Factor, Trend Following, Statistical Arbitrage, Machine Learning (4대 고급 전략)

**4개 Sub-Strategy (2026년 4-5월 추가)**:

#### 3-1. AI Supply Chain Bayesian Analysis

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/AI%20supply%20chain%20bayesian%20analysis)

AI 공급망 종목을 *Bayesian 추론* 으로 분석하는 sub-strategy. NVIDIA, TSMC, ASML, AMD, Broadcom 같은 핵심 AI 반도체 공급망 종목의 *prior probability* 를 시장 컨센서스로 설정하고, *likelihood* 를 펀더멘털·기술적 신호로 측정한 뒤, *posterior probability* 를 도출하여 매매 결정.

**핵심 차별점**:

* *베이즈 정리* P(buy|signals) = P(signals|buy) × P(buy) / P(signals) 로 매매 결정 형식화
* AI 공급망 의존성 그래프 (예: NVDA → TSMC → ASML 공정 의존)
* 단일 종목 결정이 아닌 *공급망 전체 베타 노출* 분석
* Multi-Factor 전략의 ML 변형

**적합 사용자**: AI 공급망의 *상호 의존성* 을 정량적으로 분석하고 싶은 투자자.

#### 3-2. DAT Quant Strategy

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/DAT%20quant%20strategy)

칼럼 5번 (*DAT 기업의 mNAV 아비트리지 전략*) 의 **Python 코드 구현**. Strategy (MSTR), BitMine (BMNR), SharpLink (SBET) 같은 디지털 자산 보유 기업의 *mNAV (Market-to-Net-Asset-Value) 비율* 을 실시간 추적하고 매매 신호 생성.

**핵심 기능**:

* mNAV 실시간 계산 (시가총액 / BTC·ETH·SOL 보유분 시가)
* 5가지 트레이딩 신호: Sub-NAV Long, Premium Peak Short, Pair Trade, Options, LLM 알림
* 15개 DAT 기업 자동 모니터링
* 칼럼 5번의 *Jim Chanos 페어 트레이드* 자동 재현 (MSTR short + BTC long)

**적합 사용자**: DAT 기업 아비트리지 전략을 *실제 코드* 로 운영하고 싶은 투자자.

#### 3-3. Long-Term Dividend Investing

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Long-Term%20Dividend%20Investing)

장기 배당주 발굴 sub-strategy. Quality + Value 팩터의 결합으로 *지속 가능한 배당* 을 제공하는 종목을 선별. *Dividend Aristocrats (25년 이상 배당 증가)*, *Dividend Kings (50년 이상)* 그룹을 출발점으로 ROE, FCF, 부채비율 필터링.

**핵심 기능**:

* Dividend Yield + Payout Ratio + Dividend Growth Rate (DGR) 3대 지표
* DCF (Dividend Discount Model) 적정주가 계산
* ROE ≥ 15%, FCF ≥ Dividend × 1.5, Debt/Equity ≤ 1.0 필터
* 장기 holding period (5+ years) 기반 백테스트

**적합 사용자**: 단기 트레이딩보다 *장기 cash flow 중심* 투자를 원하는 투자자. AI 트레이딩 도구의 *반대 극단* 을 균형 있게 제시.

#### 3-4. Declining Stock Quant Script Using LLM (하락 종목 발굴 + 인버스 ETF 매칭)

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Declining%20Stock%20Quant%20Script%20Using%20LLM/Declining%20Stock%20Quant%20Script%20Using%20LLM.MD)

> *"상승할 종목을 찾는 것만큼, 하락할 종목을 찾는 것도 중요하다.*
> *하락에 배팅하는 것은 *과감한 행위* 가 아니라 *시장 비대칭에 대한 대응* 이다."*

S&P 500 + NASDAQ-100 구성 종목 중 향후 1-4주 내 *유의미한 하락 가능성이 높은 종목* 을 찾는 LLM 프롬프트 sub-strategy. 단순 하락 탐지에 그치지 않고, *해당 종목에 매칭되는 인버스(숏) ETF* 까지 자동 추천하여 *실제 매매 가능한 형태* 로 결과 제시.

**3대 멀티팩터 분석 모델**:

| 팩터 | 가중치 | 핵심 지표 |
| --- | --- | --- |
| **기술적 분석** | **40%** | RSI 70+ (과매수), MACD 데드크로스, 50일/200일 이평 데드크로스, 볼린저 밴드 상단 터치 후 거래량 감소, 헤드앤숄더/라이징 웻지/더블 탑 패턴 |
| **펀더멘털 분석** | **30%** | 12개월 예상 PER 섹터 평균 대비 50%+ 프리미엄, 어닝 리비전 정점, 부채비율 급등, FCF 적자 전환, 경기소비재/산업재 매출 전망 악화 |
| **수급/심리 분석** | **30%** | 기관/내부자 대량 순매도, 숏 비율 증가 + 숏 스퀴즈 가능성 낮음, 애널리스트 목표가 하향, 풋옵션 미결제약정 급증 + 풋/콜 비율 상승, 부정 키워드 (소송/규제/경고) 빈도 급증, 공매도 잔고 비율 + 대차 수수료 상승 |

**출력 형식 (Top 5 하락 후보 종목)**:

각 종목별 다음 정보 자동 생성:
* 티커 + 회사명
* **하락 확률 (%)**
* **매칭된 인버스(숏) 주식/ETF** (존재 시) — 예: SQQQ (QQQ 3x 인버스), SPXS (S&P 500 3x 인버스)
* 핵심 하락 근거 3가지 (정량 + 정성)
* 기술적/펀더멘털/수급 요약
* **예상 하락 폭 (% 범위)** + **손절(Stop-loss) 기준가**

**핵심 차별점**:

* *Long bias 시장* (대부분의 quant 도구는 long-only) 의 *반대편* 을 LLM 으로 형식화
* **인버스 ETF 자동 매칭** — 한국 거주자가 *직접 공매도 어려운 환경* 에서 *대안적 하락 베팅* 도구 제시
* *S&P 500 + NASDAQ-100* 한정으로 *유동성 + 옵션 시장* 풍부
* 1-4주 *단기 holding* 으로 인버스 ETF 의 *변동성 부패 (volatility decay)* 영향 최소화

**중요한 위험 고지** (저자가 명시한 사항):

1. **인버스 ETF는 일일 리밸런싱 구조** — 1일 초과 보유 시 *변동성 부패* 발생 → 표시된 1-4주 보유는 *직접 공매도 대비 추적오차 누적* 가능
2. **교육·연구 목적의 가상 시뮬레이션** — 실제 투자 권유 아님
3. **과거 패턴이 미래 수익 보장 안 함**
4. **하락 베팅은 *손실 무한대* 가능** — 직접 공매도 시 주가 무한 상승 위험, 인버스 ETF 시 *지속적 decay*

**적합 사용자**: 시장 *long bias* 에 대응하여 *short 기회* 도 발굴하고 싶은 투자자. 본인 자산의 *5-10% 이내* 로 hedging 또는 단기 베팅용도.

**부속 자료**: 즉시 사용 가능한 LLM 프롬프트 (Claude/GPT-5/Gemini 호환) — *복사 후 LLM 에 붙여넣으면 즉시 Top 5 하락 후보 + 인버스 ETF 매칭 결과 출력*

### 4. Awesome Vibe Trading Bot — 14개 코인 트레이딩 봇 평가 (2026년 5월 신규)

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20Vibe%20Trading%20Bot.MD)

> *"전통 트레이딩 봇 8종 + AI/LLM 기반 봇 6종 — 동일한 평가 기준으로 비교"*

GitHub 의 코인 트레이딩 봇 **14개 프로젝트** 를 *전통 봇* 과 *AI/LLM 봇* 두 카테고리로 나누어 평가한 큐레이션. 단순 나열이 아닌 *동일 기준 비교 평가* + *한계 명시* + *한국 거주자 관점*.

**카테고리 A — 전통 트레이딩 봇 (8종)**:

| 봇 | 언어 | GitHub Stars | 핵심 |
| --- | --- | --- | --- |
| **Freqtrade** | Python | **39,900+** | FreqAI ML, GPU 가속 백테스팅, 카테고리 최대 |
| Hummingbot | Python/Cython | 8,000+ | 마켓 메이킹 특화, CEX/DEX |
| Superalgos | JavaScript | 5,000+ | 비주얼 전략 빌더, SA 토큰 인센티브 |
| Jesse | Python | 6,900+ | AI 트레이딩 에이전트, 간편 구문 |
| Gekko (아카이브) | Node.js | 10,000+ | **2020년 이후 유지보수 중단 — 사용 비권장** |
| PyCryptoBot | Python | 2,400+ | 교육용 적합, 간단한 구조 |
| Ninjabot | Go | 1,200+ | 고성능, 바이낸스 특화 |
| Scuriolus | Rust | 신규 | 메모리 안전성, 비동기 처리 |
| chrisleekr/binance-trading-bot | Node.js | 한국어 지원 | 트레일링 매매, MongoDB |

**카테고리 B — AI/LLM 기반 봇 (6종, 신규)**:

| 봇 | 언어 | GitHub Stars | 핵심 AI 방법론 |
| --- | --- | --- | --- |
| **TradingAgents** | Python | 매우 높음 | UCLA/MIT 학술 backed, arXiv 2412.20138, 7개 LLM 역할 분담 |
| OctoBot | Python | 5,500+ | ChatGPT/Ollama 통합, 전통 + AI hybrid |
| qrak/LLM_trader | Python | 신규 | Vision AI 차트 분석, ChromaDB 벡터, RAG |
| **FinRL** | Python | **14,900+** | AI4Finance Foundation, 12+ RL 알고리즘 (DQN, PPO 등) |
| Sibyl | Python | 신규 | LLM Oracle + LSTM + RAG hybrid |
| LLM-TradeBot | Python | 신규 | 8 LLM 제공자, 멀티에이전트 채팅룸, Web Dashboard |

**전통 봇 추천 순위**: Freqtrade → Hummingbot → Jesse → chrisleekr (한국어)

**AI/LLM 봇 추천 순위**: TradingAgents → OctoBot → FinRL → qrak/LLM_trader → LLM-TradeBot → Sibyl

**피해야 할 봇**: Gekko (2020년 유지보수 중단)

**AI/LLM 봇 5가지 추가 위험**:

1. **Hallucination 위험** — 존재하지 않는 패턴 보고 가능
2. **비용 폭증** — 24/7 운영 시 월 $1,000+ 가능
3. **모델 deprecation** — LLM 6-12개월마다 새 버전
4. **Backtest 어려움** — temperature/seed 비결정적
5. **Look-ahead bias** — LLM 학습 데이터에 미래 정보 포함

**한국 niche 5가지 (개발자에게 기회)**:

1. 한국어 LLM 트레이딩 봇 큐레이션
2. Upbit/Bithumb LLM 통합 트레이딩
3. KOSPI/KOSDAQ 멀티에이전트 LLM 트레이딩
4. 한국 거주자 외환거래법 준수 자동매매 도구
5. 한국 시장 특화 RAG 엔진 (DART 공시, 한국은행 ECOS 등)

### 5. 칼럼: LTCM의 사례로 배우는 모델을 읽는 힘

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Vibe%20Investing%20Risk%20Management.MD)

> *"모델은 언제나 진실을 가리킨다. 손가락은 언제나 탐욕을 가리킨다."*

1998년 노벨경제학상 수상자 2명이 운영한 헤지펀드 LTCM이 4개월 만에 청산된 사건을 분석하고, 이를 2026년 AI 바이브 투자 환경에 적용한 칼럼.

### 6. 칼럼: Microsoft의 Fintool 인수 — Excel이 곧 Bloomberg가 되는 날

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Microsoft%20fintool%20acquisition%20column.MD)

> *"앞으로 30년의 터미널은 터미널이 아닐 것이다. 대답하는 스프레드시트 셀일 것이다."*

직원 6명, 조달 $7.24M의 스타트업 Fintool을 마이크로소프트가 인수한 사건 분석.

### 7. 칼럼: 보이지 않는 손인가, 계획된 사기인가?

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Crypto%20perp%20manipulation%20column.MD)

> *"벤포드 법칙은 거짓말을 못 한다. 온체인 데이터는 영원히 남는다."*

가상화폐 무기한 선물 시장에서 반복되는 "급등 → 청산 폭포 → 원점 복귀" 패턴을 **수학적·통계적 논증** 과 **온체인 포렌식** 으로 분석한 칼럼.

### 8. 칼럼: 시장은 닫혔을 때 열리는가

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/AfterMarketClose/After_Market_Close_Column.md)

> *"모든 공시는 동일하게 중요하다. 다만 투자자의 주의력은 동일하지 않다."*

미국 상장기업의 시장 충격 공시가 압도적으로 **장 마감 후(After Market Close)에 집중** 되는 현상을 실제 데이터로 분석한 칼럼.

### 9. 칼럼: DAT 기업의 mNAV 아비트리지 전략

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/mNAV(Market-to-Net-Asset-Value)%20arbitrage/Dat%20mnav%20arbitrage%20strategy.MD)

> *"Strategy(MSTR)는 이상한 물건이다. 80억 달러의 빚을 내어 610억 달러의 비트코인을 샀다. 하지만 시장은 이를 1,520억 달러로 평가했다. 그렇다면 질문은 — 추가로 지불한 910억 달러는 무엇에 대한 값인가?"*
>
> — Jim Chanos, 2024년 12월

비트코인, 이더리움, 솔라나를 기업 재무제표에 핵심 자산으로 보유하는 **DAT (Digital Asset Treasury) 기업들의 mNAV(Market-to-Net-Asset-Value) 비율 아비트리지 전략** 검증.

### 10. 칼럼: 명품은 언제 사야 하는가

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Luxury%20investment%20strategy/Luxury%20investment%20strategy.md)

> *"A Birkin bag is forever. An LVMH share is not."*

중국 경기 침체와 부동산 위기로 촉발된 **2024-2025 명품 섹터 역사적 조정** 실증 분석.

### 11. 칼럼: 가상화폐와 나스닥은 얼마나 동기화되고 있을까?

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/Nasdaq%20crypto%20coupling%20strategy.MD)

> *"비트코인이 나스닥을 따라가는가, 나스닥이 비트코인을 따라가는가?"*

2020-2026년 BTC-QQQ 30일 rolling correlation을 26개 분기로 세분화하고, **31개 주요 거시·업계 이벤트의 상관관계 영향** 을 분석한 칼럼.

### 12. 칼럼: DeFi 대안 금융 — 전통 은행을 대체할 수 있을까? (2026년 5월 신규)

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/DeFi/Defi%20alternative%20finance%20column%20kr.MD)

> *"전통 은행은 *허가*를 요구한다. DeFi는 *코드*를 요구한다.*
> *그 차이가 1조 달러 시장의 운명을 결정한다."*

DeFi (Decentralized Finance) 가 전통 금융을 *대체* 할 수 있는지에 대한 실증 분석. Aave, Compound, MakerDAO, Curve, Uniswap 같은 *blue-chip DeFi 프로토콜* 의 TVL, 수익률, 위험 (스마트 컨트랙트 해킹, depeg, 규제) 을 다룹니다.

**다루는 내용**:

* DeFi vs. 전통 금융 — *세 가지 핵심 차이* (허가 vs. 무허가, 중개 vs. 자동화, 글로벌 vs. 관할권)
* Aave V3, Compound V3 — *대출/차입 프로토콜* 의 작동 원리
* MakerDAO/Sky — *알고리즘 스테이블코인 (DAI/USDS)* 의 부채 담보 모델
* Curve, Uniswap V4 — *분산 거래소 (DEX)* 의 Concentrated Liquidity
* DeFi 수익 농사 (Yield Farming) — Aave 5-8% APY vs 미국 국채 4.5%
* DeFi 위험 5가지 — 스마트 컨트랙트 해킹 (Curve 2023 +$70M), depeg (UST 2022 -100%), 청산 캐스케이드, 규제 (MiCA, SEC), key 관리
* 한국 거주자 관점 — 외환거래법, 양도소득세 22%, KYC 우회 위험
* 전통 금융 대체 가능성 — *틈새 시장 (Niche)* vs *주류 (Mainstream)* 시나리오

**핵심 통찰**: DeFi는 *전통 금융을 대체* 하기보다 *상호 보완* 하는 경로가 현실적. 그러나 *국경 없는 자본 이동* 과 *24/7 시장* 측면에서 *영구적인 niche* 는 확보.

### 13. 칼럼: DeepSeek V4 — 중국발 LLM의 트레이딩 활용 가능성 (2026년 5월 신규)

[**전체 칼럼 보기**](https://github.com/gameworkerkim/vibe-investing/tree/main/02.Investment%20Idea%20Column/DeepSeek%20V4)

> *"DeepSeek V3.1은 Alpha Arena Season 1에서 +46%로 1위였다.*
> *V4는 무엇을 약속하는가?"*

DeepSeek V4 모델 분석과 트레이딩 분야 활용 가능성 검토. **DeepSeek V3.1이 Alpha Arena Season 1에서 GPT-5 (-75%) 를 압도하고 +46% 1위를 차지한 사건** 의 의미를 V4 관점에서 재평가.

**다루는 내용**:

* DeepSeek V3.1의 Alpha Arena +46% 성과 — *모델 IQ ≠ 트레이딩 IQ* 의 실증
* DeepSeek V4 추정 사양 — MoE 아키텍처, 추론 비용, 컨텍스트 윈도우
* 미국 LLM (GPT-5, Claude Opus 4.7) vs 중국 LLM (DeepSeek V4, Qwen3 Max) 비교
* 트레이딩 시 LLM 선택 기준 — 비용, 추론 속도, hallucination rate, vendor 안정성
* DeepSeek V4 활용 시 한국 투자자의 *법적/지정학적 위험*
* Open-source LLM (DeepSeek, Qwen) 의 *self-hosting* 옵션과 비용 절감 효과

**핵심 통찰**: *최고 성능 LLM 이 최고 트레이더는 아니다*. DeepSeek V3.1의 +46% 는 *시장 적합성* 의 결과이며, V4도 동일한 패턴을 보일 것이라는 보장은 없다. *벤치마크와 실거래의 격차* 를 항상 인지할 것.

### 14. 학술 논문: BNB Chain 분배 비대칭 (SSRN 6688740, PRELIMINARY_UPLOAD)

[**백서 PDF 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/paper/Distribution_Asymmetry_CEX_Airdrops_with_figures.pdf), [**한국어 README**](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/README_KR.md), [**SSRN 6688740**](https://ssrn.com/abstract=6688740)

> **상태 알림**: 본 논문은 2026년 5월 1일 SSRN에 제출되어 **PRELIMINARY_UPLOAD 상태이며, SSRN 분류팀의 자동 검토 및 분류 검증 단계 대기 중** 입니다. 검토 완료 후 *Public Access* 상태로 전환되며, 이때 SSRN의 자동 DOI 가 부여됩니다. 본 단계의 논문은 *동료 검토(peer-review)를 거치지 않은 working paper* 이며, *preliminary stage acknowledgment* 가 abstract 에 명시되어 있습니다.

> *"누가 실제로 이익을 얻고, 누구의 비용으로 이루어지는가?"*

본 레포 **최초의 SSRN 제출 학술 논문**. 2024-2025년 바이낸스의 중앙화 거래소 (CEX) 에어드롭 프로그램 (Megadrop 및 HODLer Airdrop) 의 *분배 비대칭 메커니즘* 을 *7개 정리 + 부트스트랩 95% CI + 디커플링 패턴* 으로 형식화. 동반 논문 [SSRN 6632838 (72-Hour Shock)](https://ssrn.com/abstract=6632838) 과 함께 **2-paper 시리즈** 를 구성.

**핵심 발견 6가지**:

| 발견 | 정량 결과 |
| --- | --- |
| **재단 재앙** | 평균 분배 비율 α=7.3% → 재단 비용 약 30.5% FDV (홀더 이익의 4.18배) |
| **수학적 강건성** | 합리적 파라미터 범위 (α 2-15%, θ 30-60%, d 10-90%) 에서 R ≥ 1.70 |
| **임계 분배 비율** | α* = 5.95% (R*=5) — Megadrop 일반 5-8% 범위가 폭발 영역 |
| **부트스트랩 95% CI** | Megadrop −76.0% [−86.4%, −65.8%], Direct (HYPE 포함) +384.3% [+68.0%, +990.0%] |
| **Cohen's d** | Megadrop vs. Direct (N=21) = **−1.52** (very large effect) |
| **디커플링 패턴** | BNB Chain 거래량 +171.4%, TVL +47.2% / Megadrop 카테고리 시가총액 −75% |

**3 행위자 절대 금액 영향 (2024-2025)**:

* BNB 홀더 (이익): **+$14억-20억**
* 발행 재단 (손실): **−$48억** (홀더 이익의 2.84배)
* BNB Chain 시가총액 (성장): **+$1,040억**

**다국어 README 4종 제공** ([English](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/README.md), [한국어](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/README_KR.md), [中文](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/README_CN.md), [日本語](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/README_JP.md))

### 15. Harness Quant v2 — 시나리오 매트릭스 기반 AI 트레이딩 플랫폼

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Harness%20quant%20v2%20readme%20.MD)

NASDAQ/S&P500 종목을 대상으로 **하네스 엔지니어링** (LLM이 도구를 호출하며 추론하는 agentic loop) 방식으로 분석하는 패키지.

### 16. Earnings Momentum Agent — 어닝 서프라이즈 특화 Top 30 추천

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/Harness%20quantv2/Earnings%20momentum%20agent%20readme%20.MD)

> *"어닝 서프라이즈는 주가를 올리지만, 어닝 쇼크는 다음날 갭 다운을 만든다."*

매월 첫 거래일에 NASDAQ + S&P500 약 700 종목을 스캔해 종합한 **Top 30 추천**. **24개월 백테스트 hit rate 83.3%**.

### 17. Nasdaq-BTC Coupling Bot — 실시간 상관관계 추적 트레이딩 신호 생성기

[**전체 문서 보기**](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/)

위 11번 칼럼의 분석을 **실시간 트레이딩 신호 생성 시스템으로 구현** 한 Python 봇. **547 lines, 10 classes**.

---

## 왜 이 레포가 필요한가요?

AI 트레이딩 분야는 **월 단위로 새 레포가 쏟아져 나옵니다.**

* virattt/ai-hedge-fund가 55,800 stars를 넘었고
* ElizaOS는 17,600+ stars로 크립토 AI 에이전트의 표준이 됐고
* TradingAgents, FinRobot, AgenticTrading 같은 프레임워크가 매월 메이저 업데이트
* Claude Opus 4.7, GPT-5.4, Gemini 3.x 등 frontier LLM이 끊임없이 진화
* MCP 같은 새 표준이 등장하면서 인프라 지형도 매주 바뀜
* **Nof1 Alpha Arena는 GPT-5 -75%, DeepSeek +46%로 우리의 직관을 흔듭니다**

문제는 — **어떤 것이 실제로 쓸만한지, 어떤 것이 README만 화려한지** 판단하기 어렵다는 점입니다. 별 수가 곧 품질도 아니고, 학술 논문 기반이라고 실전에서 작동하는 것도 아니며, 백테스트 결과는 종종 cherry-picked입니다.

**그리고 도구 큐레이션과 별개로, 전략 자체에 대한 큐레이션도 필요합니다.** 모든 퀀트 도구는 결국 *어떤 팩터를 어떤 이론적 기반 위에서 돌리느냐* 의 변형입니다. **Awesome Claude Quant Scripts** 는 그 학술적 토대(Graham, Fama-French, Jegadeesh-Titman, Novy-Marx, AQR, López de Prado…)를 Claude가 즉시 활용 가능한 프롬프트 형태로 정리해, *도구 선택 → 전략 설계 → 코드 생성* 의 사이클을 압축합니다.

**또한 트레이딩 봇 자체에 대한 평가도 필요합니다.** **Awesome Vibe Trading Bot** 은 14개 트레이딩 봇 (전통 8 + AI/LLM 6) 을 *동일 기준* 으로 비교 평가하여 *어떤 봇이 어떤 사용자에게 적합한지* 명확히 합니다. Freqtrade가 모든 사람에게 정답은 아니며, TradingAgents의 학술 backed 가 실거래 수익을 보장하지도 않습니다.

**또한 AI만이 답은 아닙니다.** 전통적 시장 구조 분석 — 공시 타이밍, DAT 기업의 mNAV 아비트리지, 명품 섹터 양극화, DeFi 대안 금융 — 역시 AI로 증폭된 분석 능력을 통해 새롭게 이해할 수 있는 영역입니다.

**그리고 칼럼 형태의 직관 분석을 넘어 *학술적 형식화* 단계로 나아가야 합니다.** 2026년 5월부터 SSRN에 제출되기 시작한 본 레포의 학술 working paper 시리즈는 이 *직관 → 형식화* 단계를 잇는 가교 역할을 합니다.

이 레포는 그 혼란을 정리하기 위한 **개인 큐레이션의 공개판** 입니다. 동시에:

* 큐레이션 과정에서 배운 패턴을 **직접 구현체로** 만들어 함께 공개합니다 (Harness Quant v2, Earnings Momentum Agent, Nasdaq-BTC Coupling Bot, DAT Quant Strategy 등)
* 시장의 거시 흐름과 산업 변화를 **칼럼으로 분석** 합니다 (LTCM, Microsoft Fintool, DAT mNAV, 명품, BTC-Nasdaq 커플링, DeFi, DeepSeek V4 등)
* **칼럼의 직관을 학술 working paper로 형식화** 하여 SSRN 등 학계 채널로 발표합니다 (preliminary 단계 명시)
* **트레이딩 봇 자체도 평가** 하여 카테고리별 추천 명확화 (Awesome Vibe Trading Bot)
* **실증 데이터와 백테스트** 를 CSV로 함께 공개해 독자가 직접 검증 가능합니다
* 모든 콘텐츠를 **MIT 라이선스** (학술 논문은 별도 듀얼 라이선스) 로 자유롭게 활용 가능하게 공개합니다

---

## 어디서 시작하면 되나요?

### 처음 오신 분

본인 관심 영역에 맞춰 어썸 리스트를 골라 보세요:

* **주식 투자 도구**: [Awesome Vibe Invest — Stocks](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20vibe%20invest.MD) 의 *"추천 시작 경로"* 섹션
* **크립토 트레이딩 도구**: [Awesome Vibe Invest — Crypto](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20vibe%20invest%20crypto.MD)
* **퀀트 전략 자체**: [Awesome Claude Quant Scripts](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Awesome%20claude%20quant%20scripts.MD) — 8대 퀀트 전략 + 3개 sub-strategy
* **트레이딩 봇**: [Awesome Vibe Trading Bot](https://github.com/gameworkerkim/vibe-investing/blob/main/Awesome%20Vibe%20Trading%20Bot.MD) — 14개 봇 비교

### AI 시대의 시장 통찰을 얻고 싶은 분

칼럼을 읽으세요 (권장 순서):

* **리스크 관리에 대한 통찰**: [LTCM 사례 칼럼](https://github.com/gameworkerkim/vibe-investing/blob/main/Vibe%20Investing%20Risk%20Management.MD) — 가장 먼저
* **산업 변화에 대한 통찰**: [Microsoft Fintool 인수 칼럼](https://github.com/gameworkerkim/vibe-investing/blob/main/Microsoft%20fintool%20acquisition%20column.MD)
* **시장 구조의 어두운 면**: [가상화폐 선물 pump-dump 패턴 분석](https://github.com/gameworkerkim/vibe-investing/blob/main/Crypto%20perp%20manipulation%20column.MD)
* **공시 타이밍의 구조적 비대칭**: [시장은 닫혔을 때 열리는가](https://github.com/gameworkerkim/vibe-investing/blob/main/AfterMarketClose/After_Market_Close_Column.md)
* **크립토-주식 교차 영역 아비트리지**: [DAT mNAV 아비트리지 전략](https://github.com/gameworkerkim/vibe-investing/blob/main/mNAV(Market-to-Net-Asset-Value)%20arbitrage/Dat%20mnav%20arbitrage%20strategy.MD)
* **전통 섹터에서의 역발상 기회**: [명품 투자 전략](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Luxury%20investment%20strategy/Luxury%20investment%20strategy.md)
* **크립토-주식 커플링의 실증 데이터**: [나스닥-크립토 커플링 전략](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/Nasdaq%20crypto%20coupling%20strategy.MD)
* **DeFi 대안 금융의 가능성과 한계**: [DeFi 대안 금융 칼럼](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/DeFi/Defi%20alternative%20finance%20column%20kr.MD)
* **중국 LLM의 트레이딩 활용**: [DeepSeek V4 칼럼](https://github.com/gameworkerkim/vibe-investing/tree/main/02.Investment%20Idea%20Column/DeepSeek%20V4)

### 학술적 형식화에 관심 있는 분

* **CEX 에어드롭 분배 비대칭의 수학적 모형**: [BNB Chain 학술 working paper (SSRN 6688740, PRELIMINARY_UPLOAD)](https://github.com/gameworkerkim/vibe-investing/blob/main/02.Investment%20Idea%20Column/BNBChain/README_KR.md)
* **토큰 언락 가격 영향**: [The 72-Hour Shock (SSRN 6632838)](https://ssrn.com/abstract=6632838)

### 바로 코드를 보고 싶은 분

여섯 가지 선택지가 있습니다:

* **시나리오 매트릭스 방식**: [Harness Quant v2](https://github.com/gameworkerkim/vibe-investing/blob/main/Harness%20quant%20v2%20readme%20.MD)
* **어닝 모멘텀 특화**: [Earnings Momentum Agent](https://github.com/gameworkerkim/vibe-investing/blob/main/Harness%20quantv2/Earnings%20momentum%20agent%20readme%20.MD)
* **크립토-주식 실시간 신호**: [Nasdaq-BTC Coupling Bot](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling)
* **DAT 아비트리지 자동화**: [DAT Quant Strategy](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/DAT%20quant%20strategy)
* **장기 배당주 발굴**: [Long-Term Dividend Investing](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Long-Term%20Dividend%20Investing)
* **하락 종목 + 인버스 ETF 발굴**: [Declining Stock Quant Script Using LLM](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Declining%20Stock%20Quant%20Script%20Using%20LLM/Declining%20Stock%20Quant%20Script%20Using%20LLM.MD) — Claude/GPT-5에 프롬프트만 붙여넣으면 Top 5 하락 후보 + 인버스 ETF 자동 출력

### 데이터를 직접 분석하고 싶은 분

16개 이상의 CSV 데이터셋을 공개합니다. Python pandas로 즉시 분석 가능:

* **공시 타이밍**: `disclosure_timing_cases.csv` (34건)
* **DAT 기업**: 3개 CSV (15개 DAT 기업, 반기별 수익률, mNAV 사이클)
* **명품 섹터**: 4개 CSV (13개 기업/ETF, 백테스트 225건, 19개 자산 할당)
* **나스닥-크립토 커플링**: 4개 CSV (26 분기 + 31 이벤트 + 56 인트라데이 + 6 regime)
* **어닝 모멘텀**: `backtest_log_24months.csv` (768건 의사결정)
* **BNB Chain 분배 비대칭**: `listed_tokens.csv` (N=21), `btc_eth_bnb_quarterly.csv` (N=9 분기), `bnb_chain_metrics.csv` (Q1-Q3 2025), `correlation_matrix.csv`

---

## 로드맵

### 완료

* Awesome Vibe Invest v1 (주식, 30+ 레포)
* Awesome Vibe Invest — Crypto Edition (크립토 + 벤치마크 중심)
* Awesome Claude Quant Scripts — 8대 퀀트 전략 + 학계 원전 30+편
* **Awesome Claude Quant Scripts sub-strategy 4종 추가** (AI Supply Chain Bayesian, DAT Quant, Long-Term Dividend, Declining Stock + 인버스 ETF)
* **Awesome Vibe Trading Bot — 14개 봇 평가 (전통 8 + AI/LLM 6)**
* Harness Quant v2 (6 시나리오 + 백테스트 + MCP + 토론)
* LTCM 칼럼 (리스크 관리)
* Microsoft Fintool 인수 칼럼
* 가상화폐 선물 pump-dump 수학적 검토 칼럼
* Earnings Momentum Agent — 24개월 백테스트 hit rate 83.3%
* 시장은 닫혔을 때 열리는가 — 34건 AMC 공시 실증 분석
* DAT mNAV 아비트리지 — 15개 DAT 기업 + Chanos 페어 트레이드 복기
* 명품 투자 전략 — LVMH/Hermès/Kering + 3단계 포트폴리오
* 가상화폐와 나스닥은 얼마나 동기화되고 있을까? — 2020-2026 BTC-QQQ 상관관계 + 6 regime 분류
* Nasdaq-BTC Coupling Bot — 547줄 Python 트레이딩 신호 생성기
* **DeFi 대안 금융 칼럼** — Aave, Compound, MakerDAO, Curve, Uniswap 분석
* **DeepSeek V4 칼럼** — 중국 LLM의 트레이딩 활용 가능성 + Alpha Arena 회고
* **SSRN 6688740 working paper 제출 (PRELIMINARY_UPLOAD)** — Distribution Asymmetry of CEX Airdrops, 본 레포 최초의 학술 working paper, 다국어 README 4종 (EN/KR/CN/JP). 현재 SSRN 분류팀 검토 대기 중

### 진행 중 / 예정

* **SSRN 6688740 분류팀 승인 → Public Access 전환** (1-3 영업일 내 예정) — 자동 DOI 부여 후 README/CITATION.cff 업데이트
* **BNB Chain working paper v2.0** (2027 예정) — 표본 N≥100, Granger 인과성 검정, PSM + Heckman 2단계, 다중 거래소 비교 (Bybit, OKX, Coinbase), 동료 검토 학술지 LaTeX 제출
* **Awesome Claude Quant Scripts 영문판** — international reach 확대
* **Awesome Claude Quant Scripts v2** — KR equity, Crypto-native, FX 도메인별 sub-curation 추가
* **Awesome Vibe Trading Bot 영문판 + 한국 niche 5종 sub-curation**
* **영문 번역판** — Awesome 시리즈 + 칼럼 전체
* **한국 주식(KOSPI/KOSDAQ) 시나리오** — pyKRX + 한국투자증권 OpenAPI 연동
* **Anthropic의 finance agent 전략 칼럼**
* **한국 자산운용업의 1년 안 5가지 변화 칼럼**
* **온체인 자산 통합** — DeFi/스테이블코인/예측시장 신호
* **Awesome Vibe Invest — 한국 시장 Edition** (KOSPI/KOSDAQ 특화)
* **월간 인사이트 리포트** — 주요 시그널 백테스트 hit-rate 공개
* **VTCLR 패턴 탐지 오픈소스 도구** — 벤포드 법칙 + 지갑 클러스터링 기반 Python 패키지
* **Earnings Momentum Agent v2** — walk-forward validation + regime-aware 필터 + 2022년 금리상승기 백테스트
* **DAT mNAV Watcher** — Claude + MCP 기반 실시간 mNAV 모니터링 오픈소스
* **명품 섹터 regime detector** — 중국 소비심리 + 부동산 지표 → 명품 매수·매도 신호
* **Coupling Bot v2** — ETH/SOL 확장, Kelly Criterion 포지션 사이즈, Multi-timeframe (1분, 5분, 1시간), walk-forward 백테스트
* **Coupling Bot Docker/AWS 배포 가이드** — 24시간 무인 운영 환경 구성
* **DeFi 대출 프로토콜 자동 모니터** — Aave/Compound TVL + APY + 청산 위험 추적

---

## 콘텐츠 통계

```
어썸 큐레이션:    4편 (총 65+ 도구/봇/전략 평가 + 8대 퀀트 전략 + 30+편 학계 원전)
                  - Awesome Vibe Invest (주식 30+)
                  - Awesome Vibe Invest Crypto (크립토)
                  - Awesome Claude Quant Scripts (8대 전략 + 4 sub-strategy)
                  - Awesome Vibe Trading Bot (14개 봇)
칼럼:             9편 (총 90,000+ 단어)
                  - LTCM, Fintool, pump-dump, AMC, DAT, 명품, BTC-Nasdaq, DeFi, DeepSeek V4
학술 working paper: 1편 SSRN 제출 (6688740, PRELIMINARY_UPLOAD)
                    + 동반 논문 1편 (SSRN 6632838)
직접 개발 도구:   3편 메인 (Harness Quant v2 + Earnings Momentum Agent + Nasdaq-BTC Coupling Bot)
                  + 4편 sub-strategy (AI Supply Chain Bayesian, DAT Quant, Long-Term Dividend, Declining Stock)
                   → 총 27개 시나리오, 파이프라인, regime 단계, sub-strategy
백테스트 로그:    24개월 × 월간 리밸런싱 = 768 의사결정
                   + 26 분기 상관관계 추적 (커플링 봇)
                   + 부트스트랩 N=10,000회 반복 (BNB Chain working paper)
공개 데이터셋:    16+ CSV (총 1,500+ 데이터 포인트)
                  - 공시 타이밍 34건, DAT 기업 15개, 명품 13개+백테스트 225건
                  - 나스닥-크립토 커플링 26분기+31이벤트+56인트라데이+6regime
                  - Earnings Momentum 768건
                  - BNB Chain working paper N=21 토큰 + N=9 분기 + Q1-Q3 2025 거시 지표
오픈소스 Python:  Nasdaq-BTC Coupling Bot 547 lines (10 classes, 18 functions)
                  + BNB Chain working paper 분석 11개 스크립트
                  + 4개 sub-strategy 코드/프롬프트 (AI Supply Chain, DAT Quant, Long-Term Dividend, Declining Stock + 인버스 ETF)
프롬프트 템플릿:  Awesome Claude Quant Scripts 14개 (전략별 8개 + 범용 T1~T5 + Declining Stock LLM 프롬프트)
                  + sub-strategy 4개 추가 프롬프트
검증된 출처:      150+ 학술 페이퍼, 공식 문서, 산업 보고서
                  + 14개 트레이딩 봇 GitHub repo 검증
지원 언어:        한국어 (영문 요약 포함)
                  + BNB Chain working paper 다국어 README 4종 (EN/KR/CN/JP)
GitHub 통계:      Stars 86, Forks 17 (2026년 5월 1일 기준)
```

---

## 기여하기 (Contributing)

다음 모두 환영합니다:

* **별 누르기** — 가장 큰 응원
* **누락된 좋은 레포 제보** — 이슈 또는 PR
* **평가에 대한 반박** — 토론은 큐레이션 품질을 높입니다
* **영문 번역** — international contribution
* **한국 시장 자원 추천** — DART, ECOS, NICE 등 활용 사례
* **본인 백테스트 결과 공유** — Harness Quant 또는 Earnings Momentum Agent의 walk-forward 결과
* **칼럼 주제 제안** — 다음에 다뤘으면 하는 시장 이슈
* **CSV 데이터 확장** — 공시 타이밍, DAT, 명품, BNB Chain 데이터셋에 추가 케이스 기여
* **퀀트 전략 추가** — Awesome Claude Quant Scripts에 새 팩터/논문/Claude 프롬프트 제안
* **트레이딩 봇 평가 기여** — Awesome Vibe Trading Bot에 누락된 봇 또는 평가 반박
* **학술 working paper 협업** — BNB Chain working paper v2.0 (N≥100, Granger 인과성) 데이터 수집, 검증, LaTeX 변환에 기여

이슈 또는 PR로 부담 없이 알려주세요. **반대 의견도 환영합니다** — *"이 평가는 틀렸다"* 는 피드백이 가장 가치 있습니다.

---

## Disclaimer

이 레포의 모든 콘텐츠는 **연구·교육 목적** 입니다.

* **어떤 도구도 수익을 보장하지 않습니다** — Alpha Arena의 GPT-5 -75%가 실제 데이터이며, Earnings Momentum Agent의 83.3% hit rate는 백테스트 상의 이상적 시나리오입니다
* 모든 평가는 작성 시점의 공개 정보 기반 주관적 평가입니다
* 실전 자본 운용 전 반드시 자체 백테스트, 페이퍼 트레이딩, 법률 검토를 거치세요
* **Claude를 포함한 LLM이 생성한 코드에는 사실 오류, 구조적 편향, 보안 취약점이 포함될 수 있습니다.** Awesome Claude Quant Scripts의 모든 프롬프트와 코드 골격은 사용자가 직접 검증할 능력이 없다면 다른 LLM으로 교차 검증해 환각을 필터링해야 합니다
* 미국 SEC/CFTC, 한국 금감원, EU MiCA 모두 AI 기반 자동 트레이딩에 규제 적용 가능 — 본인 자산 운용은 OK, 타인 자금 운용은 라이선스 필요
* MEV bot의 sandwich attack 같은 일부 전략은 윤리적 회색지대 + 일부 관할권에서 시장 조작으로 해석 가능
* 시장 구조 분석 칼럼(예: 가상화폐 선물 pump-dump, AMC 공시 타이밍, DAT mNAV 아비트리지)은 **특정 주체를 지목하지 않는 통계적, 학술적 논평** 이며, 개별 사건의 법적 성격 규명은 관할 수사, 규제 기관의 몫입니다
* **BNB Chain 학술 working paper (SSRN 6688740) 는 *PRELIMINARY_UPLOAD 단계의 working paper* 입니다.** 본 글 작성 시점에 SSRN 분류팀의 자동 검토 단계 (1-3 영업일 소요) 이며, *동료 검토(peer-review)를 거치지 않았습니다*. 표본 N=21은 완전한 통계적 추론에 부족하며, 디커플링 패턴의 *인과성* 은 *관찰 증거* 일 뿐입니다. 후속 v2.0 (2027 예정) 에서 Granger 인과성 검정 + N≥100 으로 보강 예정. *완성된 학술적 결론* 으로 인용하지 않도록 주의
* 어닝 서프라이즈 기반 전략은 **시장 regime 의존적** 입니다
* **Awesome Vibe Trading Bot 의 14개 봇 평가는 작성 시점 (2026년 5월) 기준** 이며, GitHub stars/forks 는 시점에 따라 변동. 모든 봇의 backtest 결과는 *cherry-picked period* 가능성. 특히 **AI/LLM 봇은 5가지 추가 위험** (hallucination, 비용 폭증, 모델 deprecation, backtest 어려움, look-ahead bias) 을 사전에 인지할 것
* **DeFi 칼럼의 권고** 는 *블루칩 프로토콜* (Aave, Compound, MakerDAO, Curve, Uniswap) 에 한정되며, 신생 DeFi 프로토콜은 *스마트 컨트랙트 해킹 + depeg + 청산 캐스케이드* 위험이 훨씬 큼. **한국 거주자는 DeFi 사용 시 외환거래법 + 양도소득세 22% + KYC 우회 위험 사전 검토 필수**
* **DeepSeek V4 같은 중국 LLM 사용** 은 *지정학적 위험* (미중 기술 분쟁, US 제재, 데이터 주권) 별도 검토 필요. *self-hosting* 시에도 모델 weights 다운로드 채널의 안전성 확인
* **하락 베팅, 공매도, 곱버스 ETF, 레버리지 투자는 개인에게 치명적일 수 있습니다.** DAT mNAV 아비트리지 칼럼의 5가지 위험 고지, 명품 투자 전략의 3단계 위험 경고를 반드시 참조하세요. **특히 Declining Stock Quant Script Using LLM 의 인버스(숏) ETF 매칭 결과** 는 *일일 리밸런싱 구조* 로 인해 *1일 초과 보유 시 변동성 부패 (volatility decay)* 가 발생합니다. 1-4주 보유는 *직접 공매도 대비 추적오차 누적* 가능성이 있으며, 본인 자산의 *5-10% 이내* 로 hedging/단기 베팅 용도로만 사용 권장
* 투자 결과 + 법적 리스크에 대한 책임은 사용자에게 있습니다

---

## About

**김호광 (Dennis Kim)**
Cyworld CEO, Betalabs Inc. 창업자, 개발자, Web3 Investor, 독립 연구자
Web3, 블록체인, AI 트레이딩 영역에서 활동하고 있습니다.

* Email: [gameworker@gmail.com](mailto:gameworker@gmail.com)
* GitHub: [@gameworkerkim](https://github.com/gameworkerkim)
* ORCID: [0009-0002-0962-2175](https://orcid.org/0009-0002-0962-2175)
* SSRN Author Page: [Author ID 7497180](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=7497180)

이 레포는 AI를 활용한 창업가로서의 얻은 인사이트를 바탕으로 만들어졌습니다. 2026년 5월부터는 SSRN 학술 working paper 시리즈를 통해 시장 구조의 *수학적 형식화* 영역으로도 확장합니다 (현재 SSRN 6688740 분류팀 검토 대기 중).

---

## 라이선스

MIT License — 자유롭게 사용·수정·배포 가능합니다. 출처 표기만 부탁드립니다.

칼럼은 인용·재배포 시 *"김호광 (Dennis Kim) / vibe-investing 레포"* 출처 명기를 부탁드립니다.

**학술 working paper** (BNB Chain 분배 비대칭, SSRN 6688740) 은 별도의 듀얼 라이선스 적용:

* 소스 코드 (Python 분석 스크립트): MIT License
* 논문, 데이터, 다이어그램: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Attribution 필수
* 학술 인용 시 BibTeX 형식: BNBChain README 참조. 단 현재 PRELIMINARY_UPLOAD 단계이므로 *동료 검토 거치지 않은 working paper* 임을 인용 시 명시 권장

---

***"Models always point to truth. Fingers always point to greed."***  
*"모델은 언제나 진실을 가리킨다. 손가락은 언제나 탐욕을 가리킨다."*

***"Model intelligence is not trading intelligence."***  
*"모델의 지능이 곧 트레이딩 지능은 아니다."*  
— Alpha Arena Season 1 lesson

***"Benford's law cannot lie. On-chain data lasts forever."***  
*"벤포드 법칙은 거짓말을 못 한다. 온체인 데이터는 영원히 남는다."*

***"Earnings surprises lift the stock,  
earnings shocks create the next morning's gap down."***  
*"어닝 서프라이즈는 주가를 올리지만,  
어닝 쇼크는 다음날 갭 다운을 만든다."*

***"The market closes, but information opens.  
The question is — who reads it first?"***  
*"시장은 닫히고, 정보는 열린다. 문제는 — 누가 먼저 읽는가이다."*  
— After Market Close 칼럼

***"Trade the premium, not the faith."***  
*"믿음이 아니라 프리미엄을 거래하라."*  
— DAT mNAV 아비트리지 칼럼

***"A Birkin bag is forever. An LVMH share is not.  
Don't confuse the brand's immortality with your portfolio's fate."***  
*"버킨 백은 영원하다. LVMH 주식은 그렇지 않다.  
브랜드의 영속성과 당신 포트폴리오의 운명을 혼동하지 말라."*  
— 명품 투자 전략 칼럼

***"The question was never whether crypto and stocks move together.  
The question is — when, how fast, and in which direction?  
Those who know the regime, know the trade."***  
*"크립토와 주식이 함께 움직이는가는 질문이 아니다.  
언제, 얼마나 빠르게, 어느 방향으로인가가 질문이다.  
Regime을 아는 자가 거래를 안다."*  
— 나스닥-크립토 커플링 칼럼

***"Theory without code is philosophy. Code without theory is gambling.  
Claude collapses the gap — but never replaces verification."***  
*"이론 없는 코드는 도박이고, 코드 없는 이론은 철학이다.  
Claude는 그 간극을 압축하지만, 결코 검증을 대체하지 않는다."*  
— Awesome Claude Quant Scripts

***"Traditional banks ask for permission. DeFi asks for code.  
That difference decides the fate of a trillion-dollar market."***  
*"전통 은행은 허가를 요구한다. DeFi는 코드를 요구한다.  
그 차이가 1조 달러 시장의 운명을 결정한다."*  
— DeFi 대안 금융 칼럼

***"DeepSeek V3.1 returned +46%. GPT-5 returned -75%.  
Bench scores measure the model. Markets measure the trader."***  
*"DeepSeek V3.1은 +46%, GPT-5는 -75%였다.  
벤치마크는 모델을 측정한다. 시장은 트레이더를 측정한다."*  
— DeepSeek V4 칼럼

***"The best bot is not the most starred bot.  
It is the one that fits your style, your capital, and your risk tolerance."***  
*"별이 가장 많은 봇이 최고의 봇은 아니다.  
당신의 스타일, 자본, 위험 감수성에 맞는 봇이 최고이다."*  
— Awesome Vibe Trading Bot

***"Finding stocks that will fall is as important as finding stocks that will rise.  
Betting on the downside is not aggression — it is symmetry with the market."***  
*"상승할 종목을 찾는 것만큼, 하락할 종목을 찾는 것도 중요하다.  
하락에 배팅하는 것은 *과감한 행위* 가 아니라 *시장 비대칭에 대한 대응* 이다."*  
— Declining Stock Quant Script Using LLM

***"Who actually benefits — and at whose cost?  
Foundations face catastrophic losses while ecosystem macro-activity grows in opposite direction.  
The decoupling is mathematical, not coincidental."***  
*"누가 실제로 이익을 얻고, 누구의 비용으로 이루어지는가?  
재단은 치명적 손실을 입는 반면, 생태계 거시 활동은 반대 방향으로 성장한다.  
디커플링은 우연이 아니라 수학이다."*  
— Distribution Asymmetry of CEX Airdrops (SSRN 6688740, PRELIMINARY_UPLOAD)

**이 레포가 도움이 되셨다면 별 하나로 응원해주세요.**  
매주 1-2회 갱신을 약속드립니다.
