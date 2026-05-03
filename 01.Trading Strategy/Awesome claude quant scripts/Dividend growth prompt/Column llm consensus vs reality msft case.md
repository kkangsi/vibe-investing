# LLM이 모두 추천한 종목, 그래서 사도 되나? — 마이크로소프트 사례에서 본 AI 시대 투자의 함정

## 11개 LLM 결과 모두가 "MSFT 추천"이었지만, 실제 시장은 무엇을 말하는가

**김호광 (Dennis Kim)** | Cyworld Z 전 CEO, Betalabs Inc. CEO
**작성일**: 2026년 5월 3일
**카테고리**: AI · 투자 · 기술 칼럼

---

## 들어가며 — 11개의 LLM 결과가 모두 같은 답을 했다

알파고 이후 바둑이 재미없어졌다. 이름을 가리고 기보를 보면 누가 누구랑 대국을한지 알 수 없는 시대에 살게 되었다. 
개성이 사라진 바둑의 미래는 어찌될 것인지 알 수 없지만 실력은 높아졌고 평준화되었다. 
인공지능 바둑 프로그램이 대중화 된 이후, 바둑 해석은 바둑 기사가 인공지능이 착점하는 것과 얼마나 유사하게 두느냐는 설명으로 바뀌게 되었다. 기보에 대한 설명 역시 인공지능 착점 대비 몇%인가가 중요해졌다.

이와 유사하게 인공지능을 이용한 퀀트, 헤지 펀드의 사장은 대중화 될 것이다.

인공지능(AI) 헤지펀드는 AI 에이전트가 데이터 분석, 롱/숏 포지션 선정, 투자 규모 결정 및 거래 실행까지 전 과정 또는 핵심 과정을 수행하는 펀드이다.
데이터 기반의 신속한 의사결정으로 수익을 극대화하려는 시도로, 대표적으로 Abundance나 엑스포넨셜자산운용 등이 AI 기술을 활용하여 주식, 채권, 원자재 등 다양한 자산에 투자하고 있다.
주요 특징 및 동향AI 에이전트 활용이다. 수천 개의 AI 봇이 인터넷 데이터를 분석해 투자 아이디어를 발굴하고 거래를 실행하고 있다. 오픈소스 프로젝트: 개발자 Virat Singh이 만든 ai-hedge-fund 같은 교육용/실험적 프로젝트가 존재하고 있다.

시장 전망은 폭발적이다
코투(Coatue)와 같은 대형 헤지펀드는 AI 시장을 '슈퍼 사이클'로 보며 투자를 확대하고 있으며, AI 기반 솔루션인 링크 알파(Linq Alpha) 같은 기술도 등장했다.

리스크 관리 입장에서 인공지능은 인간의 감정적 결정을 배제하고 있다.
레이 달리오 등은 AI 시장의 거품 가능성을 경고하며, 기술주 투자에 대한 주의를 당부하기도 하고 있다.핵심 주체 및 플랫폼 Abundance이다. 인스타카트 창업자가 설립, AI가 전적으로 운영하는 주식 펀드.엑스포넨셜자산운용이다.
Togo는 글로벌 데이터를 분석하여 투자 기회를 찾아주는 AI 어시스턴트 플랫폼이다. 한편, 80조 원을 운용하는 코투(Coatue)와 같은 대형 펀드들은 AI 기술이 금융 산업 전반의 패러다임을 바꿀 것으로 예상하고 있다.

시장의 기대가 있다면 시장 초반에는 놀라운 수익율을 알려줄 것이지만, 점차 대중화됨에 따라 수익율은 수렴될 것이다. 모두가 인공지능을 사용하고 있다면 상장사 역시 인공지능의 조언에 따라 각종 조언, IR, 마케팅을 하게 될 것이기 때문에 기업의 경영자에 따른 컬러, 스타일, 창의적인 마케팅 역시 무채색이될 가능성이 높아지고 트레이딩 전략, 퀀트, 헤지펀드 아이디어는 누구나 아는 공공재처럼 되어 투자의 기회와 수익율을 갉아 먹을 것이다.

**Vibe Investing Quant Script 백테스트의 기록**

지난 한 달간 나는 4개의 frontier LLM (Claude, DeepSeek, Gemini, ChatGPT)에 **동일한 미국 배당 성장 종목 발굴 프롬프트**를 한국어, 영어, 중국어로 입력해 11개의 결과물을 얻었다.

**11개 모든 결과물에서 추천된 *유일한 종목*은 Microsoft (MSFT)** 였다. 11/11 = 100% universal pick.

이 발견은 처음에 매우 강한 신호로 보였다. *"4개의 다른 회사가 만든 4개의 다른 LLM이, 3개의 다른 언어로 받았는데 *모두* 같은 결론에 도달했다면, 그 종목은 진짜 강한 것 아닌가?"*

그런데 — **2026년 4월 29일 발표된 Microsoft FY26 Q3 어닝**, **같은 날 발표된 Alphabet (Google) Q1 2026 어닝**, **OpenAI의 사용자 위기 신호**를 종합해보면, 이야기는 훨씬 복잡하다.

이 칼럼은 그 데이터를 정리하면서, *LLM의 consensus를 어떻게 비판적으로 받아들여야 하는지*를 정리한다. 핵심 메시지는 모델 넘어 모델을 읽은 인간의 인사이트에 있다.

> **LLM은 퀀트와 데이터 분석의 엑셀이다. 사용자가 잘 써야 하고, 영어 기반 다양한 LLM 교차 검증을 해야 하며, 모델을 해석하고 실시간 시장 변화로 검증할 능력이 필요하다.**

---

## 1. Microsoft FY26 Q3 — 화려한 표면

2026년 4월 29일 발표된 Microsoft FY26 Q3 어닝 (분기 종료 2026년 3월 31일):

| 지표 | 값 | YoY 변화 |
|---|---|---|
| Revenue | $82.9B | +18% (constant currency 15%) |
| Operating income | $38.4B | +20% |
| Diluted EPS | $4.27 | +23% GAAP |
| Microsoft Cloud | $54.5B | +29% |
| Azure | (number not disclosed) | +40% (consensus 38% 상회) |
| AI business run rate | $37B annual | +123% YoY |
| Commercial RPO (예약 매출) | **$627B** | +99% YoY |
| Capex (Q3 한 분기) | $30.876B (+84% YoY) | - |
| 주주 환원 | $10.2B (배당 + 자사주) | - |

표면적으로 Microsoft는 *AI 시대의 압도적 승자*다. Azure는 컨센서스를 넘어 +40% 성장. AI 비즈니스는 $37B 연간 run rate, +123% YoY 폭증. RPO (미래 예약 매출) 잔액은 $627B로 *전년 대비 거의 2배*.

**"이런 회사를 LLM이 universal pick으로 추천하지 않을 이유가 없다."**

LLM들이 모두 MSFT를 추천한 것은 *틀린 답이 아니다*.
윈도우라는 OS, 오피스라는 업무용 프로그램의 구독 모델, Azure라는 클라우드, OpenAI라는 포트폴리오는 보기에는 훌륭하다.

---

## 2. 그러나 — 4가지 구조적 위험을 LLM은 인지하지 못했다

본 11개 결과물 중 *어떤 LLM도* 다음 위험을 명시적으로 언급하지 않았다:

### 위험 1: Calendar 2026 capex $190B의 정확한 규모

Microsoft의 FY26 capex 가이던스: $110-120B (전년 약 $80B에서 큰 폭 증가). Calendar 2026 capex는 약 $190B (component price 영향 $25B 포함). 단일 기업 사상 최대.

**무엇이 위험인가?**:
- 영업이익률 압박 (Q3 gross margin 68%로 YoY 하락)
- Free cash flow yield 2.27%, capex가 영업이익을 압박할 수 있음

LLM들은 "AI capex 부담"이라고 *추상적으로*만 언급. *$190B*라는 구체적 숫자나, *FCF yield 2.27%*라는 정량적 위험은 어떤 LLM도 표현하지 못함.

### 위험 2: Commercial RPO의 45%가 OpenAI 의존

가장 충격적 사실은 1월 29일 Q2 어닝 시 공개되었다.

Microsoft의 Commercial RPO 잔액의 약 45%가 OpenAI에서 유래한다는 사실이 공개되자, 시장은 즉각적으로 반응했다 — Microsoft 주가 *9.99% 하락*. 시가총액 *약 $440B 증발*.

이는 무엇을 의미하나?
- Microsoft의 미래 수익이 *단일 고객 (OpenAI)에 과도하게 집중*
- 만약 OpenAI가 자금 위기에 처한다면 → Microsoft RPO 계약 이행 위험
- 전형적인 *concentration risk*

**LLM은 이 사실을 어떤 결과물에서도 언급하지 않았다.** 학습 데이터 cutoff 이전 narrative만 재생산.

### 위험 3: OpenAI Revenue Share 종료의 양면 효과

어닝 발표 이틀 전인 2026년 4월 27일, Microsoft와 OpenAI는 파트너십을 재구조화했다. Microsoft의 OpenAI revenue share payment 종료.

표면적으로는 Microsoft 수익성에 +. 그러나:
- OpenAI가 *Microsoft 외 다른 클라우드 (Oracle, AWS) 도 사용 가능*
- Microsoft의 *AI 차별성 우위 약화*

LLM이 학습한 시점에는 OpenAI가 Microsoft Azure에 *exclusive*로 묶여 있었다. *현재의 non-exclusive 구조*는 LLM이 학습하지 못한 새로운 정보.

### 위험 4: Q2 어닝 후 9.99% 하락 사례

Microsoft Q2 FY2026 어닝은 컨센서스를 7.57% 상회했지만, 시장은 9.99% 하락으로 응답. 이는 시장이 *"좋은 어닝 + 무거운 capex burn"의 균형*에 회의적임을 보여준다.

이 사례는 *LLM의 학습 데이터에 거의 없는 정보*. 시장 반응의 *복합적 동학*은 학습 코퍼스의 평균적 narrative로 포착되지 않는다.

---

## 3. Google의 어닝 서프라이즈 — LLM이 *전혀 추천하지 않은* 종목

같은 날 (2026-04-29), Alphabet은 Q1 2026 어닝을 발표했다.

| 지표 | Microsoft FY26 Q3 | Alphabet Q1 2026 | 우위 |
|---|---|---|---|
| Revenue 성장 | +18% YoY | **+22% YoY (11분기 연속 두자릿수)** | Google |
| Cloud 성장 | Azure +40% | **Google Cloud +63%** | Google (압도적) |
| EPS 컨센서스 대비 | 미세 상회 | **$5.11 vs $2.62 예상의 거의 2배** | Google (압도적) |
| 어닝 후 주가 반응 | flat | **+10% 상승** | Google |
| Cloud backlog | $627B (45% OpenAI 의존) | $462B (분산) | Google (질적 우위) |

특히 충격적인 것은 *Search 비즈니스의 부활*이다. Google Search 매출은 +19% YoY 성장하며, AI 경험이 검색 사용 증가를 유도하고 쿼리는 사상 최고치. *AI Mode와 AI Overviews가 Search를 대체하지 않고 강화*하고 있다.

지난 2년간 시장의 가장 큰 *bear case*는 *"AI 챗봇이 Google Search ad revenue를 잠식할 것"* 이었다. Q1 2026 어닝은 이 thesis를 정면 반박.

추가로 인상적인 데이터:
- Cloud 운영이익이 1년 만에 3배로 성장 ($6.6B), 운영마진 17.8% → 32.9%
- Gemini 모델 기반 GenAI products의 revenue가 +800% YoY
- Gemini Enterprise paid MAU +40% QoQ
- Total paid subscriptions 350M 도달 (Gemini App 기여)

**그런데 본 11개 LLM 결과물 중 Google/Alphabet (GOOG/GOOGL)을 추천한 결과물은 0개였다.**

왜? 본 프롬프트의 *narrow dividend criteria* (5년 연속 배당 증가, CAGR ≥ 8% 등) 때문에 Alphabet이 자동 제외되었기 때문이다 (Alphabet은 2024년부터 배당 시작).

이는 다음을 시사한다. 프롬프트의 규칙에 사로잡혀, 하네스에 잡혀 정말 좋은 구글을 추천하지 않았던 것이다.
- 프롬프트 criteria가 *우주를 좁게 정의*하면 *우수한 종목이 누락*된다
- "11/11 universal pick"의 의미는 *그 좁은 우주 안에서만* 유효
- 엄격한 하네스 프롬프트 LLM consensus만 따르는 투자자는 **Google 같은 어닝 서프라이즈 종목을 놓친다**

---

## 4. OpenAI의 위기 신호 — Microsoft RPO 45%의 그림자

Microsoft RPO의 45%가 OpenAI 의존인 만큼, OpenAI의 건전성은 Microsoft의 미래에 직결된다. 그런데 OpenAI는 *심각한 자금 위기*를 보이고 있다.

### 4.1 재무 위기

| 지표 | 값 |
|---|---|
| 2025년 cash burn (1H만) | $13.5B |
| 2026년 expected loss | $14B (revenue $13B vs 지출 $22B) |
| 2026 burn rate | revenue의 57% (Anthropic 33%의 약 1.7배) |
| Total burn through 2030 | $665B (revised up $112B) |
| 2025 adjusted gross margin | 33% (2024 40%에서 하락) |
| 2025 inference cost | 4배 증가 (단년) |
| 자금 모색 중 | $100B+ (Nvidia, Microsoft, Amazon, SoftBank) |
| 추정 부채 | ~$100B |
| Profitability 예상 | 2030+ |

OpenAI는 *재무적으로 자력으로 살아남기 어려운 상태*다. "OpenAI는 build-out phase를 거쳐 high revenue phase로 갈 수 있는 deep pocket이 없다"는 평가가 나온다.

### 4.2 ChatGPT 사용자 위기

| 지표 | 변화 | 시점 |
|---|---|---|
| 4월 2026 uninstall rate | +132% YoY | - |
| 3월 2026 uninstall spike | +413% YoY (Pentagon partnership 발표 후) | - |
| MAU growth | 168% (1월) → 78% (4월) | 4개월 |
| Time spent | -10% (11월 vs 7월) | - |
| Web traffic share | 86.7% (Jan 2025) → 64.5% (Jan 2026), -22pp | 12개월 |
| 1B weekly users 목표 (Feb 2026) | MISSED | - |

ChatGPT의 추세는 명확히 *둔화*. Sam Altman이 "code red" memo를 발행한 것은 우연이 아니다.

### 4.3 Gemini의 추격

반면 Google Gemini는 가속 중:

| 지표 | 변화 |
|---|---|
| Gemini 글로벌 MAU 점유율 | +3pp (May-Nov 2025) |
| ChatGPT 점유율 변화 | -3pp (Aug-Nov 2025) |
| Gemini 다운로드 성장 | +190% YoY |
| ChatGPT 다운로드 성장 | +85% YoY (코호트 평균 110% 미달) |
| Gemini web traffic share (12개월) | 5.7% → 21.5% |
| Apple Intelligence + Gemini 통합 | 2026 Jan, $5B 추정 |

**검색엔진 회사 Google이 OpenAI를 빠르게 따라잡고 있다.** Google의 강점:
- *기존 광고 매출 모델 ($60B/quarter)*로 AI 손실 흡수 가능
- Search 모노폴리 (자기 데이터)
- Apple/Android 채널의 천연 distribution
- 이미 350M paid subscribers

OpenAI의 약점:
- 광고 비즈니스가 없음 (단, 2026년부터 ChatGPT에 광고 도입 발표 — *desperation 신호*)
- 단일 product에 의존 (ChatGPT)
- Apple-Gemini 파트너십으로 mobile 채널 잠식

---

## 5. Circular Financing — LLM이 인지하지 못한 시스템 위험

가장 우려스러운 패턴은 AI 산업 내부의 *순환 자금*이다:

```
Microsoft → OpenAI 투자 → OpenAI → Microsoft Azure 지출
Nvidia → OpenAI $100B → OpenAI → Nvidia GPU 구매
        (CFO Sarah Friar 명언: "will go back to Nvidia")
Nvidia → CoreWeave 투자 → CoreWeave → Nvidia chips
SoftBank → OpenAI $40B → Stargate → 다른 corporate partners
```

**의미**:
- AI 산업의 "혁신 자금"이 *동일 기업군 내에서 순환*
- 회계적 revenue처럼 보이지만 *내부 자금 이동*에 가까움
- Oracle 신용등급 junk 근접 (Stargate 투자로)
- Microsoft 1월 29일 -12% 하락, $440B 시총 증발 (Cloud backlog 45% OpenAI 의존 공개 후)

이 *시스템 위험*은 본 11개 LLM 결과물 중 *어떤 결과물도 언급하지 않은* 위험이다. Cross-LLM consensus가 *시스템 위험을 집단적으로 누락*한다.
마이크로소프트는 장기간 배당을 지속한 회사이지만 배당금은 0.88%이다. 5년간 약 60% 주가 상승으로 배당과 성장이 다른 배당주보다 약하다.
올해 크게 약세인 아메리칸 익스프레스의 경우 1.19%로 좀 더 후한 배당을 하고 있고 지난 5년간 100%의 주가 상승이 있었다. 

---

## 6. 한국 투자자를 위한 5단계 점검표

본 분석을 종합해 *LLM consensus를 비판적으로 검증*하는 5단계 체크리스트:

### Step 1. Cross-LLM consensus 확인 (v4 워크플로)
- Frontier LLM 4개+에서 common stock 추출
- 6/11 이상 universal pick만 강한 신호로 인정 (MSFT 11/11, V 10/11, UNH 9/11 등)

### Step 2. 다국어 cross-validation (v4 워크플로)
- 한국어 + 영문 + 중국어로 동일 프롬프트
- 종목 변경률이 50%+면 *cross-lingual asymmetry* 인지

### Step 3. **실시간 어닝 검증 (NEW)**
- 가장 최근 분기 어닝을 SEC EDGAR에서 *직접 확인*
- LLM의 narrative와 실제 가이던스 비교
- 점검 항목: Capex 규모, 단일 고객 의존도, OpenAI 의존도

### Step 4. **시스템 위험 검토 (NEW)**
- Circular financing 노출도
- 단일 고객 의존도 (예: MSFT의 OpenAI 45%)
- Cloud backlog의 질적 분석

### Step 5. **Universe 외부 재검토 (NEW)**
- 프롬프트 criteria로 누락된 강한 종목 (예: GOOG의 Q1 2026 어닝 서프라이즈)
- 동일 섹터의 alternative consideration
- *LLM이 추천한 universe 자체*에 의문 제기

---

## 7. Microsoft에 대한 최종 종합 의견

| 평가 항목 | 점수 | 의견 |
|---|---|---|
| LLM 합의 강도 | ⭐⭐⭐⭐⭐ | 11/11 universal — 논쟁 여지 없음 |
| 어닝 fundamentals | ⭐⭐⭐⭐⭐ | Revenue +18%, Azure +40% — 압도적 |
| AI business growth | ⭐⭐⭐⭐⭐ | $37B run rate, +123% YoY — 폭발적 |
| 배당 안정성 | ⭐⭐⭐⭐⭐ | 21년 연속 증가 + $10.2B 분기 환원 |
| 배당 수익률 | ⭐⭐ | 0.88% — 너무 낮음 |
| **OpenAI 의존 위험** | ⭐⭐ | **RPO 45% — 심각한 concentration** |
| **Capex 부담** | ⭐⭐ | **Calendar 2026 $190B — 사상 최대** |
| **Circular financing 노출** | ⭐⭐⭐ | OpenAI 자금 위기 시 RPO 영향 |
| Q2 어닝 후 시장 반응 | ⭐⭐⭐ | -9.99% — 시장 회의 신호 |

**한 줄 요약**:

> *"Microsoft는 LLM 시대의 dividend growth 표준 답안이지만, *2026년의 Microsoft*는 2024-2025의 narrative와 다르다. AI 비즈니스의 폭발적 성장은 사실이지만, OpenAI 45% 의존도와 Calendar 2026 $190B capex는 LLM이 인지하지 못한 위험이다. 11/11 universal pick은 *학습 데이터 cutoff까지의 narrative*이지, *실시간 시장 risk*가 아니다."*

**한국 투자자 권고**:

1. **MSFT 신규 매수 시**: 분할 매수 + 5년+ 장기 + AI capex 리스크 인지. 현재 yield 0.88%는 *income generation 목적에 부적합*.
2. **이미 MSFT 보유 중이라면**: OpenAI 의존도를 *quarterly로 모니터링*. RPO 45% → 30%로 다각화 시 positive, 50%+로 증가 시 warning.
3. **Diversification 권고**: AI 노출을 MSFT에만 집중하지 말고 *Google (GOOG)* 도 검토. Google은 *광고 매출 + Cloud + Gemini*의 다각화로 *MSFT보다 낮은 concentration risk*.
4. **현금 수익이 필요한 투자자**: MSFT 0.88% yield는 부적합. *SCHD ETF (3.5%)* 또는 *전통적 dividend aristocrat (JNJ, PG, KO 등)* 으로 income 부분 보완.

---

## 8. LLM 시대 투자의 새로운 due diligence

본 11개 결과물 + 시장 검증을 통해 정리한 *AI 시대 투자 due diligence 원칙*:

### 원칙 1. LLM은 엑셀이다, 신탁이 아니다
- 도구로서 기능 (데이터 수집, 초기 분석, 자연어 explanation)
- 검증의 책임은 *사용자에게*

### 원칙 2. 영어 기반 다양한 LLM 교차 검증
- 한국어 LLM의 Sharpe inflation 함정 회피
- Cross-LLM (Claude vs Gemini vs ChatGPT)으로 합의 추출
- Cross-language로 hallucination signature 식별

### 원칙 3. 실시간 시장 변화로 LLM consensus 검증
- 학습 데이터 cutoff 후의 어닝, 정책 변화, 산업 동학
- LLM이 인지 못하는 *concentration risk*, *circular financing*
- 가장 최근 분기 SEC EDGAR 직접 인용

### 원칙 4. 모델 해석 + 검증 능력
- LLM이 지정한 universe 외부 재검토
- 프롬프트 criteria의 limitations 인지
- 정량 메트릭 (Sharpe, MD)을 *RANGE로 보고* (ChatGPT 방식 모범)

### 원칙 5. 검색엔진 회사 vs AI-only 회사 균형
- Google: 광고 모노폴리 + Search + Gemini 통합 (sustainable)
- Microsoft: Azure + OpenAI 의존 + capex burn (high reward, high risk)
- OpenAI: AI-only, $665B burn until 2030 (speculative)

---

## 9. 결론 — "LLM 시대의 정직한 투자자"가 되는 법

본 칼럼의 출발점은 단순한 발견이었다: *11개 LLM 결과 모두가 MSFT를 추천했다*.

그러나 *2026년 4월 29일의 시장*은 다음을 보여줬다:
- Microsoft는 강하지만 *capex burn과 OpenAI 의존*이라는 시점 의존적 위험을 가짐
- Google은 *어닝 서프라이즈로 MSFT를 능가하는 성장*을 보였지만 *LLM은 추천 universe에서 제외*
- OpenAI는 *$665B burn through 2030*으로 사실상 자력 생존 불가능
- Gemini는 ChatGPT를 빠르게 따라잡고 있음
- AI 산업의 *circular financing*은 시스템 위험으로 부상

LLM은 우리에게 *과거 narrative*를 압축해서 보여준다. 그것은 *유용*하지만 *충분하지 않다*.

**LLM 시대의 정직한 투자자가 되는 법**:
1. LLM을 엑셀처럼 사용 — *결과를 검증하라*
2. 영어 기반 다양한 LLM 교차 검증
3. 실시간 어닝, SEC 공시로 *시점 보정*
4. 시스템 위험 (concentration, circular financing) 직접 검토
5. Universe 외부 재검토 — *LLM이 누락한 우수 종목*을 찾아라

이것이 11/11 universal pick MSFT를 맹목적으로 따르지 않으면서, 동시에 무작정 거부하지도 않는 균형 잡힌 접근이다.

정량화된 퀀트 모델에서 데이터를 추출하는 것은 이제 LLM이 있어서 효율적으로 할 수 있지만, 같은 LLM이라도 한국어, 영어, 중국어에 대한 학습데이터와 가중치 차이로 결과가 차이가 날 수 밖에 없어 이에 대한 주의가 필요하다. 앞으로 투자에서 인간이 보는 인사이트가 더욱 중요해지며 투자의 변동성과 수익율이 더 줄어들 가능성이 높다. 모두 같은 인공지능을 통해 모델을 탐구하고 주식을 살펴볼 것이기 때문이다.



---

## 더 자세한 자료

- **학술 논문 (v5)**: [Cross_Lingual_LLM_Accuracy_Paper.pdf](result/ENG_Report/Cross_Lingual_LLM_Accuracy_Paper.pdf) (곧 업데이트 예정)
- **v5 마크다운 요약**: [Cross_Lingual_LLM_Accuracy_Paper.md](result/ENG_Report/Cross_Lingual_LLM_Accuracy_Paper.md) (곧 업데이트 예정)
- **11개 결과물**: [GitHub Repository](https://github.com/gameworkerkim/vibe-investing/tree/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt)
- **Microsoft FY26 Q3 Earnings**: [SEC EDGAR Form 8-K](https://www.sec.gov/Archives/edgar/data/0000789019/000119312526191457/msft-ex99_1.htm)
- **Alphabet Q1 2026 Earnings**: [SEC EDGAR Form 8-K](https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000043/googexhibit991q12026.htm)

---

## 면책 (Disclaimer)

본 칼럼은 *교육 및 정보 제공* 목적이다. 모든 종목 추천은 *LLM 출력의 cross-validation 분석*을 위한 자료이며, *투자 권유가 아니다*. 모든 투자 결정은 *독립 데이터 소스 + 전문가 상담* 후 본인 책임이다. 과거 배당 기록이 미래 배당을 보장하지 않는다.

본 칼럼의 어닝 데이터는 *2026년 4월 29일 발표 시점 기준*이다. Microsoft, Alphabet, OpenAI의 financial situation은 *수시로 변동*하며, 본 칼럼 작성 후 변화가 있을 수 있다. 본 칼럼은 *분석 시점의 snapshot*이며, *실시간 검증의 중요성*은 칼럼의 핵심 메시지이다.

---

**저자 소개**

김호광 (Dennis Kim / HoKwang Kim)은 Cyworld Z 전 CEO, Betalabs Inc. CEO이며 Web3, AI, 블록체인 분야 독립 연구자다. Microsoft Azure MVP를 거의 10년간 유지했으며, 2016년부터 인공지능의 사회적 영향을 연구하고 있다. GitHub에서 quantitative finance와 AI 관련 오픈소스 프로젝트를 운영한다.

- **Email**: gameworker@gmail.com
- **GitHub**: [@gameworkerkim](https://github.com/gameworkerkim)
- **ORCID**: [0009-0002-0962-2175](https://orcid.org/0009-0002-0962-2175)

---

**Citation**:

```
김호광 (2026). "LLM이 모두 추천한 종목, 그래서 사도 되나? — 마이크로소프트 사례에서 본
AI 시대 투자의 함정". vibe-investing GitHub Repository.
https://github.com/gameworkerkim/vibe-investing
```

**라이선스**: MIT
