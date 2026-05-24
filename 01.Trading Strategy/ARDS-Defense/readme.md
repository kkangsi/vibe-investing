# ARDS-Defense
### Adaptive Recession-Defensive Strategy for Defense & AI-Weaponization

> "전쟁과 분쟁의 시대, 방산은 더 이상 경기방어주가 아니라 구조적 성장주다.
> 그 구조적 성장 속에서도 경기 사이클은 반드시 찾아온다. 이 전략은 그 역설을 거래한다."

냉전이 지나고 팍스 아메리카나의 시대가 저물면서 다시 새로운 혼돈의 시기가 오고 있습니다. 러시아 - 우크라이나 전쟁은 유럽의 재무장을 촉발 시켰으며, 일본 역시 1%로 묶여 있던 군비를 증강하고 있습니다. 이란과 이스라엘, 미국의 중동 전쟁은 미국이 1년간 생산할 무기 방어체계를 단시간 내에 소모시켰습니다.

방산(Defense)과 AI 무기화(AI-Weaponization) 섹터에 특화된 적응형 경기방어 투자 전략입니다.
거시 레짐을 판별해 Phase를 산출하고, 방산 특수 지표(Defense Sentiment)로 이를 조정한 뒤,
한국·미국 방산 종목을 3-Tier로 나눠 Phase별 자산 배분을 자동 산출합니다.

---

## Repository 구조

```
ARDS-Defense/
├── README.md                ← 본 문서 (전략 전문 + 다국어 프롬프트)
├── prompts/
│   ├── ARDS-Defense_KO.md    ← 한국어 실행 프롬프트 (v1.1)
│   ├── ARDS-Defense_EN.md    ← English execution prompt (v1.1)
│   └── ARDS-Defense_ZH.md    ← 中文执行提示词 (v1.1)
└── result/                  ← 각 LLM의 출력 결과 보관
    ├── claude/               ← Claude 실행 결과
    ├── gpt/                  ← GPT 실행 결과
    ├── gemini/               ← Gemini 실행 결과
    └── DeepSeek/                 ← DeepSeek 실행 결과
```

`result/` 서브 폴더에는 동일 프롬프트를 여러 LLM·여러 언어로 실행한 출력 결과를 보관합니다.
멀티-LLM 교차검증(cross-validation) 및 언어별 출력 비대칭(cross-lingual asymmetry) 분석에 활용합니다.

---

## STEP 1 — 투자 논리 (Investment Thesis)

### 1.1 왜 지금 방산 + AI인가
전쟁·분쟁의 구조화(Structuration of Warfare) 와 국방비 슈퍼사이클(Defense Supercycle) 이라는
두 개의 거대한 흐름이 중첩되고 있습니다. 글로벌 국방비 지출은 2026년 기준 2.6조 달러를 돌파했으며,
2030년까지 3.6조 달러로 확대될 전망입니다. 이 중 펜타곤의 AI 예산만 20억 달러 미만에서
134억 달러로 단일 연도에 급증했습니다.

단순한 국방비 증가가 아닌, **국방비 내 AI/소프트웨어 비중의 구조적 재편**이 핵심입니다.
2025년 VC-backed 방산 스타트업 투자는 미국·유럽 합산 약 77억 달러로 2024년의 2배 이상을
기록했으며, 팔란티어는 2026년 연간 매출 가이던스를 71.8억~72억 달러로 제시하며
2025년(33.2억 달러) 대비 2배 이상 성장을 예고했습니다.

> ⚠️ 위 수치는 작성 시점 기준 추정치입니다. 실행 프롬프트는 매크로/펀더멘털 지표를
> **웹검색으로 실시간 재확보**하도록 설계되어 있으니, 매 실행 시 최신 값으로 갱신됩니다.

### 1.2 경기방어 + 구조적 성장의 이중적 성격
| 성격 | 내용 |
|------|------|
| **Recession-Defensive** | 경기 침체기에도 국방 예산은 후행적으로 삭감되며, 지정학적 위기는 경기와 무관하게 발생 |
| **Structural Growth** | AI·자율무기·우주방어·사이버전으로의 패러다임 전환은 경기 사이클을 초월한 10년+ 투자 사이클 |
| **Asymmetric Alpha** | 전통 방산주 vs AI 방산주는 동일 섹터 내에서도 완전히 다른 리스크-리턴 프로파일 (방어적 배당주 vs 고성장 기술주) |

---

## STEP 2 — Universe (투자 유니버스)

### 2.1 한국 (KOSPI/KOSDAQ) 상장 방산 기업
| Tier | 종목명 | 티커 | 핵심 사업 | AI/무인화 연계 |
|------|--------|------|-----------|----------------|
| Core | 한화에어로스페이스 | 012450 | 항공엔진, 미사일, 자주포(K9), 우주발사체 | 한화 방산 3사 AI·무인화 통합 플랫폼(DAPA-GO) |
| Core | LIG넥스원 | 079550 | 유도미사일, 정밀타격, 감시정찰 | AI 기반 지휘통제체계 |
| Core | 한국항공우주(KAI) | 047810 | 전투기(KF-21), 훈련기, 위성 | 무인전투기(UCAV) 개발 |
| Core | 현대로템 | 064350 | 전차(K2), 장갑차, 철도 | 무인전차·자율주행 기술 |
| Core | 한화오션 | 042660 | 함정, 잠수함 | 무인수상정(USV) 기술 |
| Core | 한화시스템 | 272210 | C4I, 레이더, 위성통신 | AI·무인화 플랫폼 핵심 |
| Satellite | 풍산 | 103140 | 탄약, 포탄 | — |
| Satellite | STX엔진 | 077970 | 함정용 엔진, 발전기 | — |
| Satellite | LIG에이스피 | 453250 | 방산 부품(PCB, 전자장비) | — |
| Satellite | 빅텍 | 065450 | 군용 전원공급체계 | — |
| Satellite | SNT중공업 | 003570 | 함정 엔진, 방산 차량 부품 | — |
| Satellite | 퍼스텍 | 010820 | 유도무기 체계, 항공기 개조 | — |
| Satellite | HJ중공업 | 097230 | 함정 건조 | — |
| Satellite | 한일단조 | 024740 | 방산 차량 부품, 단조품 | — |
| Satellite | 스페코 | 013810 | 방산 기계부품(탄약 제조설비 등) | — |
| Satellite | 포메탈 | 119500 | 방산 단조/주조 부품 | — |
| Watchlist | 현대위아 | 011210 | 항공기 엔진 부품, 방산 차량 | — |
| Watchlist | 진양산업 | 003780 | 군수용 고무/플라스틱 부품 | — |

### 2.2 미국 (NYSE/NASDAQ) 상장 방산 기업
| Tier | 종목명 | 티커 | 핵심 사업 | AI/무인화 연계 |
|------|--------|------|-----------|----------------|
| Core | Lockheed Martin | LMT | 전투기(F-35), 미사일, 위성 | AI 전장관리, 자율비행 |
| Core | RTX Corp | RTX | 미사일(Patriot), 레이더, 항공엔진 | AI 센서퓨전, 요격체계 |
| Core | Northrop Grumman | NOC | 스텔스 폭격기(B-21), 우주, 미사일 | 자율무인기(X-47B 등) |
| Core | General Dynamics | GD | 전차, 잠수함, IT/C4I | 사이버 보안, AI 지휘통제 |
| Core | L3Harris | LHX | 전자전, 통신, 위성 | AI 신호정보(SIGINT) |
| Core | Boeing | BA | 전투기(F/A-18), 수송기, 위성 | 자율비행, MQ-25 무인급유기 |
| AI-Defense | Palantir | PLTR | AI 전장관리 플랫폼(AIP/Maven) | 국방 AI 순수 플레이 |
| AI-Defense | Kratos Defense | KTOS | 무인전투기(UTAP-22, XQ-58) | 자율무인기 특화 |
| AI-Defense | AeroVironment | AVAV | 소형 무인기(Switchblade) | 자율공격 드론 |
| AI-Defense | BigBear.ai | BBAI | AI 의사결정 분석 | 국방 AI 데이터 분석 |
| Satellite | Huntington Ingalls | HII | 항공모함, 잠수함 | — |
| Satellite | Textron | TXT | 헬기, 무인기 | — |
| Satellite | Rocket Lab | RKLB | 우주발사체, 위성 | — |
| Satellite | GE Aerospace | GE | 군용 항공엔진 | — |
| Satellite | Howmet Aerospace | HWM | 항공우주 부품(터빈 블레이드 등) | — |
| Satellite | CAE Inc | CAE | 군용 시뮬레이션 훈련체계 | AI 기반 시뮬레이션 |
| Satellite | Booz Allen Hamilton | BAH | 국방 컨설팅, 사이버 보안 | AI 컨설팅 |
| Pre-IPO | Anduril Industries | (비상장) | AI 자율무기, 무인전투기(Fury), 로봇잠수함 | 국방 AI 스타트업 대장 (밸류 ~$61B) |

### 2.3 ETF Universe (일괄 투자)
| ETF 명 | 티커 | 국가 | 특징 | 운용사 |
|--------|------|------|------|--------|
| PLUS K방산 | 449450 | 한국 | K-방산 핵심 10종목 (한화에어로·LIG넥스원·KAI·현대로템 등) | 한화자산운용 |
| PLUS 글로벌방산 | 496770 | 글로벌 | 美·유럽 방산 혼합 (LMT·RTX·NOC·Thales·BAE) | 한화자산운용 |
| TIGER 미국방산TOP10 | 494840 | 미국 | 미국 방산 대형주 10종목 (Defense Score 기준) | 미래에셋자산운용 |
| iShares US Aerospace & Defense | ITA | 미국 | 미국 항공우주·방산 전반 (약 30종목) | BlackRock |
| iShares Defense Industrials Active | IDEF | 글로벌 | 글로벌 방산 액티브 (미국 60% + 유럽·한국 등) | BlackRock |

---

## STEP 3 — 실행 프롬프트 (다국어)

아래 프롬프트(v1.1)를 그대로 복사해 **웹검색 가능한 LLM**에 붙여넣어 실행하세요.
빈칸 없이 즉시 실행 가능하며, 매크로 지표는 웹검색으로 실시간 확보하도록 설계되어 있습니다.

| 언어 | 파일 | 비고 |
|------|------|------|
| 🇰🇷 한국어 | [`prompts/ARDS-Defense_KO.md`](prompts/ARDS-Defense_KO.md) | 기본(primary) |
| 🇺🇸 English | [`prompts/ARDS-Defense_EN.md`](prompts/ARDS-Defense_EN.md) | 글로벌 배포용 |
| 🇨🇳 中文 | [`prompts/ARDS-Defense_ZH.md`](prompts/ARDS-Defense_ZH.md) | 중화권 배포용 |

### v1.1 핵심 로직 (3개 언어 공통)
- **STEP 0** — 5-Factor Recession Composite로 거시 Phase(1~4) 판별
- **STEP 1** — Defense Sentiment Score(0~100)로 Phase 레벨 ±1 조정
- **STEP 2** — 3-Tier Universe (Core Defense / AI-Defense / Tactical)
- **STEP 3 + 3.5** — 5-Dimension Scoring → Tier 내 비중 자동 배분(Score 가중 + 40% 캡)
- **STEP 4** — Phase별 자산 배분 Matrix
- **STEP 5~7** — AI-Defense 특별 규칙, 실행 규칙, 반대 시나리오

> v1.1 개정 요지: 웹검색 강제 및 출처 명시 의무화, Phase 조정 로직 숫자화,
> Scoring↔비중 연동(STEP 3.5 신설), Score 60점 미만 종목 편입 제외.
> 상세 내용은 각 프롬프트 파일 하단의 개정 내역 표 참조.

---

## STEP 4 — 운용 가이드라인

### 4.1 한국/미국 비중 원칙
- **기본 배분: 한국 40% / 미국 60%** (미국 방산 시장의 규모와 AI 방산 집중도 반영)
- **Defense Sentiment ≥ 70** 시 K-방산 비중 **+10%p 확대** (한국 방산 수출 모멘텀이 독립적으로 강할 때)

### 4.2 ARDS 원본과의 차이점 (Defense Adaptation Note)
| 차원 | ARDS 원본 | ARDS-Defense |
|------|-----------|--------------|
| Universe | 4-Tier (ETF·채권·방어주·Inverse) | 3-Tier (Core Defense·AI-Defense·Tactical) |
| 경기방어 메커니즘 | XLP·XLV·TLT·GLD로 도피 | Tier 1 방산주로 집중 (방산 = 자체 방어) |
| 성장 요소 | 없음 | Tier 2 AI-Defense (구조적 성장) |
| Inverse | SH·PSQ·VIXY | Tier 3 후발 방산주 (상대적 약세 베팅) |
| 특수 시그널 | DIP_BUY·FLIGHT_TO_QUALITY | Defense Sentiment Score (지정학·국방비·AI 계약·K-수출) |
| 국가 분할 | 없음 | 한국·미국 이원화 |

### 4.3 Anduril IPO 대응
Anduril은 2026년 5월 Series H 라운드에서 50억 달러를 조달하며 기업가치를 610억 달러로
평가받았고, IPO가 임박했습니다.
- **상장 직후**: Tier 2에 5% 한도로 편입 (Lock-up 리스크)
- **상장 90일 후**: Lock-up 해제 확인 시 최대 15%까지 확대
- **상장 전**: PLTR·KTOS·AVAV로 AI-Defense 익스포저 확보

---

## STEP 5 — 리스크 관리

| 리스크 | 내용 |
|--------|------|
| **지정학 리스크 역설** | 전쟁 종결/긴장 완화 시 방산주는 최대 30% 급락 가능 (2025년 중동 휴전 당시 실제 사례) |
| **AI 방산 밸류에이션 리스크** | PLTR·Anduril·BBAI 등은 EPS보다 계약 파이프라인으로 거래 → 금리 상승기 멀티플 압축에 극도로 취약 |
| **K-방산 수출 집중 리스크** | 폴란드·UAE·사우디 등 특정 국가 의존도가 높아 지정학적 급변 시 매출 공백 가능 |
| **원자재·공급망 리스크** | 희토류·반도체·특수합금 등 방산 원자재의 중국 의존도가 높아 미중 갈등 심화 시 생산 차질 가능 |
| **Phase 4 규칙의 기회비용** | PLTR·Anduril 등이 침체기에도 계약을 수주하며 반등할 경우, AI-Defense 0% 규칙이 오히려 수익을 제한할 수 있음. 이 규칙은 2022년 Fed 긴축기 당시 고성장 기술주의 60~80% 하락 경험에 근거 |

---

## 참고자료
- ARDS 원본 전략: *ARDS: Adaptive Recession-Defensive Strategy*
- Chatham House: *"How a surge in defence and dual-use technology investment could reconfigure the global AI race"* (2026.04)
- JP Morgan Private Bank: *"The new security landscape: Investing in defense tech, energy & resilience"* (2026 Mid-Year Outlook)
- CNBC: *"Anduril doubles valuation to over $60 billion as defense tech funding boom continues"* (2026.05.13)

---

## ⚠️ 면책 조항 (Disclaimer)
본 자료는 **교육 및 연구 목적의 LLM 시뮬레이션 결과**이며, 특정 종목의 매수·매도를
권유하는 것이 아닙니다. 모든 투자 판단과 그에 따른 책임은 투자자 본인에게 있습니다.

방산 섹터는 지정학적 사건에 극도로 민감하게 반응하므로, 본 전략만으로 포트폴리오 전체를
구성하는 것은 권장하지 않습니다. **ARDS 원본(경기방어 ETF·채권·금)과의 병행 운용을 강력히 권고합니다.**

> *This material is an LLM-based simulation result for educational and research purposes only,
> and is not a solicitation to buy or sell any security. All investment decisions and
> responsibility rest with the investor.*
