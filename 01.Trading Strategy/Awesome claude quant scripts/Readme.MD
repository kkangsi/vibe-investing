# Awesome Claude Quant Scripts

Claude를 활용해 만든 트레이딩 전략 스크립트 모음입니다.

→ [상위 폴더 README](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/README.md)
→ [메인 레포 README](https://github.com/gameworkerkim/vibe-investing/blob/main/README.md)

---

## 중요한 주의 고지 (Important Notice)

> **LLM은 엑셀이지, 정답을 알려주는 오라클(신탁)이 될 수 없습니다.**

본 폴더의 모든 LLM 기반 프롬프트와 스크립트를 사용하기 전에 다음 사항을 반드시 인지하십시오.

### 본 연구로 입증된 LLM의 4가지 구조적 한계

1. **언어별 출력 결과의 비대칭** — 동일한 프롬프트라도 한국어, 영어, 중국어로 입력했을 때 결과가 크게 달라집니다. 본 연구에서 4개 frontier LLM × 3개 언어 = 11개 결과물의 평균 Jaccard 유사도가 **0.297**에 불과했습니다. 9개의 모든 언어 쌍이 J<0.5로, 동일 LLM 내에서도 언어 간 일관성이 낮습니다.

2. **LLM별 학습 편차** — Claude, ChatGPT, Gemini, DeepSeek 등 frontier LLM은 학습 코퍼스, RLHF 정책, 토크나이저 차이로 정량 메트릭(Sharpe, P/E, 수익률 등) 보고에서 체계적 편차를 보입니다. 특히 한국어 LLM에서 *Sharpe inflation* (비현실적 수익률 보고) 같은 *Cultural Optimism Bias*가 관찰되었습니다.

3. **데이터 cutoff와 hallucination** — 본 연구에서 Gemini와 ChatGPT가 EN/CN/KR에서 **AVGO 분할 전 가격($1,695, $1,410, $1,420, $1,350)을 4번 모두 보고**한 사례가 발견되었습니다. 이는 *동일 학습 코퍼스에 인코딩된 hallucination signature*입니다. LLM 합의가 강해도 *학습 cutoff까지의 narrative*에 갇혀 있습니다.

4. **Cross-LLM Consensus의 시점 편향** — 11개 LLM 모두가 추천한 *universal pick* MSFT조차, 2026년 4월 29일 어닝 발표 후 다음 위험을 *어떤 LLM도 인지하지 못했다*는 사실이 밝혀졌습니다.
   - Calendar 2026 capex $190B (단일 기업 사상 최대)
   - Commercial RPO의 45%가 OpenAI 단일 고객 의존
   - OpenAI의 2030년까지 $665B burn rate
   - 같은 날 어닝 우위를 보인 GOOG는 0/11로 추천 누락

### 사용자에게 요구되는 것

- LLM 출력은 **검증의 대상**이지 결과 그 자체가 아닙니다.
- 프롬프트의 universe 정의 자체에 의문을 제기할 수 있는 **시장 도메인 지식**이 필요합니다.
- LLM이 모르는 정보 (학습 cutoff 이후 어닝, 정책 변화, 시스템 위험)를 **실시간 시장 데이터로 보완**해야 합니다.
- 정량 메트릭(Sharpe, MD)은 **단일 값이 아니라 RANGE로** 해석해야 합니다.

### 본 연구 결과를 기반으로 한 권장 검증 워크플로

1. **Cross-LLM consensus 확인** — Frontier LLM 4개+에서 common stock 추출
2. **다국어 cross-validation** — 한국어 + 영문 + 중국어로 동일 프롬프트
3. **실시간 어닝 검증** — 가장 최근 분기 어닝을 SEC EDGAR에서 직접 확인
4. **시스템 위험 검토** — Concentration risk, circular financing 노출도
5. **Universe 외부 재검토** — 프롬프트 criteria로 누락된 강한 종목 검토

### 본 연구 자료 (Reference)

본 주의 고지의 근거가 된 실증 연구:

-  **칼럼**: [LLM이 모두 추천한 종목, 그래서 사도 되나? — 마이크로소프트 사례에서 본 AI 시대 투자의 함정](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt/Column%20llm%20consensus%20vs%20reality%20msft%20case.md) (markdown)
-  **PDF 버전**: [Column_LLM_Consensus_vs_Reality_MSFT_Case_v2.pdf](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt/Column_LLM_Consensus_vs_Reality_MSFT_Case_v2.pdf)
-  **학술 논문 예정** — 4개 LLM × 3개 언어 = 11개 결과물의 정량 메트릭 분석

본 폴더의 모든 스크립트는 위 연구의 결과를 사전 인지한 사용자를 전제로 작성되었습니다.

---

## 개요

이 폴더는 4종의 트레이딩 전략과 1개의 Sample 템플릿, 그리고 전체 전략 맵 (`trading map.png`)을 담고 있습니다.

전체 개요는 [Awesome claude quant scripts.MD](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Awesome%20claude%20quant%20scripts.MD)를 참조하세요.

---

## 수록 전략

| # | 전략 | 폴더 | 분류 |
| --- | --- | --- | --- |
| 1 | [AI supply chain bayesian analysis](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/AI%20supply%20chain%20bayesian%20analysis) | AI 공급망 베이지안 분석 | 연구 / 정량 분석 |
| 2 | [DAT quant strategy](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/DAT%20quant%20strategy) | DAT 기업 정량 전략 | 트레이딩 전략 |
| 3 | [Declining Stock Quant Script Using LLM](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Declining%20Stock%20Quant%20Script%20Using%20LLM) | LLM 기반 하락주 스크립트 | 트레이딩 전략 |
| 4 | [Long-Term Dividend Investing](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Long-Term%20Dividend%20Investing) | 장기 배당 투자 | 트레이딩 전략 |
| 5 | [Dividend growth prompt](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt) | 배당 성장 프롬프트 + Cross-Lingual LLM 검증 연구 | 연구 / 트레이딩 전략 |
| - | [Sample](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Sample) | 새 전략 시작 시 사용할 템플릿 | Template |

---

## 전략별 설명

### 1. AI supply chain bayesian analysis

AI 산업의 공급망 위험을 베이지안 추론으로 분석한 연구 자료. 반도체, GPU, 클라우드, 데이터 등 AI 공급망 핵심 노드의 의존성과 단일 실패점(SPOF) 위험을 정량화합니다.

활용:

* 엔비디아·TSMC·ASML 같은 단일 노드 의존도가 높은 기업의 risk-adjusted 평가
* AI 섹터 포트폴리오의 공급망 집중도 측정
* 지정학적 충격 시 가장 먼저 영향받을 종목 식별

### 2. DAT quant strategy

DAT (Digital Asset Treasury) 기업, 즉 비트코인·이더리움·솔라나를 재무제표에 핵심 자산으로 보유하는 기업의 정량 트레이딩 전략입니다.

연관:

* [DAT mNAV 아비트리지 칼럼](https://github.com/gameworkerkim/vibe-investing/blob/main/mNAV(Market-to-Net-Asset-Value)%20arbitrage)에서 이론 배경 확인
* MSTR, BMNR, SBET 등 15개 기업 대상

### 3. Declining Stock Quant Script Using LLM

급락 중인 종목 가운데 반등 가능성이 있는 종목을 LLM이 선별하는 스크립트. 단순 모멘텀 역발상이 아니라 펀더멘털과 기술적 지표를 함께 검토합니다.

연관:

* [Earnings Momentum Agent](https://github.com/gameworkerkim/vibe-investing/blob/main/Harness%20quantv2)와 보완적 — Earnings Momentum이 "저점 + 실적 반등"을 잡는 반면, 본 스크립트는 "급락 + 회복 가능성"을 분석

### 4. Long-Term Dividend Investing

장기 배당 투자를 위한 종목 선별 스크립트. 단순 배당수익률이 아니라 배당 성장성, 지속 가능성, 페이아웃 비율, 재무 건전성을 종합 평가합니다.

활용:

* 은퇴 자금 운용
* 인컴 포트폴리오 구성
* 배당 귀족주 (Dividend Aristocrats) 후보 발굴

### 5. Dividend growth prompt — Cross-Lingual LLM 검증 연구

배당 성장 종목 발굴 프롬프트와, 그 프롬프트를 4개 frontier LLM × 3개 언어로 검증한 학술적 실증 연구. 본 README 상단의 "주의 고지"를 뒷받침하는 연구이자, *LLM 프롬프트 퀀트의 한계*와 *검증 워크플로*를 정립한 자료입니다.

수록:

* 11개 결과물 (Claude, ChatGPT, Gemini, DeepSeek × 한·영·중) 원본 데이터
* Cross-Lingual LLM Accuracy Paper v5 (학술 논문, 43페이지)
* MSFT 사례 분석 칼럼 (markdown + PDF v2)
* AI 헤지펀드 / 페르소나 AI 오픈소스 레퍼런스 (12개 프로젝트)

핵심 발견:

* MSFT 11/11 universal pick의 시점 편향
* 같은 날 GOOG 어닝 서프라이즈를 LLM 0/11이 누락
* OpenAI 의존도와 circular financing의 시스템 위험 누락

활용:

* 본 폴더의 다른 LLM 기반 스크립트 사용 전 *반드시 선행 학습*
* 본인의 LLM 프롬프트 퀀트 결과를 검증하는 5단계 체크리스트 적용
* 페르소나 AI (Buffett, Munger, Wood, Burry 등)의 한계와 가능성 이해

### Sample

새 전략을 만들 때 사용할 템플릿 폴더입니다. 표준 구조 (README, 스크립트, 데이터, 백테스트, 한계)를 따릅니다.

→ [Sample Readme.MD](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Sample%20Readme.MD) 참조

---

## 전체 맵

`trading map.png` — 본 폴더의 4종 전략 + Sample이 어떤 시장 상황에 적합한지 시각화한 맵.

---

## 사용 권장 순서

>  **반드시 0단계부터 시작하십시오.** 본 README 상단의 주의 고지를 인지하지 않은 상태로 LLM 스크립트를 사용하면 *"엑셀에 잘못된 함수를 넣고 결과를 그대로 신뢰하는 것"*과 같습니다.

0. **선행 학습** — [Dividend growth prompt 폴더의 칼럼](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt/Column%20llm%20consensus%20vs%20reality%20msft%20case.md) 또는 [PDF v2](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt/Column_LLM_Consensus_vs_Reality_MSFT_Case_v2.pdf)를 읽고 LLM 프롬프트 퀀트의 4가지 구조적 한계와 5단계 검증 워크플로를 인지
1. [Awesome claude quant scripts.MD](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Awesome%20claude%20quant%20scripts.MD)에서 전체 개요 읽기
2. 본인 관심 영역에 맞는 전략 폴더로 이동
3. 해당 전략의 README와 한계 섹션 읽기
4. 백테스트 데이터 재현
5. **Cross-LLM + 다국어 + 실시간 어닝으로 검증**
6. 페이퍼 트레이딩 검증 후 실거래 고려

---

## Disclaimer

모든 스크립트는 연구·교육 목적입니다. 본 폴더의 LLM 기반 프롬프트 퀀트는 *"LLM에게 맡기는 투자"*가 아니라 *"AI를 도구로 쓰는 투자자가 되는 훈련"*을 위한 것입니다. 사용자는 본 README 상단의 주의 고지를 인지하고, 모든 LLM 출력을 독립적인 시장 데이터와 본인 판단으로 검증할 책임이 있습니다.

자세한 내용은 [메인 README의 Disclaimer](https://github.com/gameworkerkim/vibe-investing/blob/main/README.md#disclaimer) 참조.
