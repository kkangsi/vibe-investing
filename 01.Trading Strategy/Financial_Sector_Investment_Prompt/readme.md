# 미국 금융 섹터 LLM 퀀트 투자 프롬프트 시스템
> 기준일: 2026-06-13 | 버전: v2.0 | 작성: Dennis Kim

---

## 1. 현재 금융 섹터 상태: Fear or Greed?

### 1-1. 시장 센티먼트 진단 (2026년 6월 기준)

| 지표 | 현재값 | 판정 |
|:--|:--|:--|
| CNN Fear & Greed Index | **30 (Fear)** | 🔴 Fear Zone |
| XLF 52주 범위 위치 | $52.60 / High $56.52 / Low $47.67 | 중간대 (약 57% 위치) |
| XLF YTD 수익률 | 마이너스 (S&P500 언더퍼폼) | ⚠️ 상대적 약세 |
| XLF 5월 ETF 자금 흐름 | **섹터 최대 순유출** | 🔴 기관 이탈 신호 |
| XLF Fwd P/E | 14.75x (10년 평균 대비 고평가) | ⚠️ P/B 기준 비싸 |
| 애널리스트 컨센서스 | XLF: HOLD | 중립 |
| 금리 환경 | 고금리 지속 → NIM 수혜 | 🟢 은행 긍정 |
| 규제 환경 | Basel III 완화, 탈규제 진행 | 🟢 은행 긍정 |
| 신용 우려 | 소비자 부채 부담 증가 | 🔴 카드·소비금융 주의 |

### 1-2. ARDS 페이즈 판정

```
현재 ARDS Phase: Phase 2 (Late-Cycle) → Phase 3 경계
- 소비자 실질임금 마이너스 성장
- 에너지 비용 상승으로 인플레이션 끈적 (Sticky)
- AI 인프라 Capex 주도 성장 → 금융 섹터 소외
- 금리 인하 기대감 선반영 후 실망 국면
판정: 금융 섹터 전체 MODERATE CAUTION
```

---

## 2. 금융 기업 투자 판정표 (2026년 6월 기준)

### 매수 (Accumulate) 추천 기업

| 티커 | 기업 | 현재가(추정) | 사유 |
|:--|:--|:--|:--|
| **BAC** | Bank of America | ~$45 | P/B 할인, 금리 수혜 NIM 확대, 언더밸류 |
| **APO** | Apollo Global Mgmt | ~$120 | 대체투자 AUM 고성장, 연금자본 수요 강세 |
| **KKR** | KKR & Co. | ~$130 | 인프라·PE 수요 증가, AI 인프라 투자 수혜 |
| **PGR** | Progressive Corp | ~$260 | P&C 보험 결합비율 개선, 직판 모델 강점 |
| **COF** | Capital One Financial | ~$175 | Discover 인수 시너지, 언더밸류 |

**매수 공통 근거:**
- 탈규제 환경에서 자본 배분 여력 증가
- 대체자산운용사: AI 인프라·인프라 PE 딜 파이프라인 확대
- Progressive: 직판 모델로 사업비율 경쟁 우위 유지
- BAC/COF: P/B·P/E 기준 섹터 내 저평가

---

### 중립 (Hold) 기업

| 티커 | 기업 | 현재가(추정) | 사유 |
|:--|:--|:--|:--|
| **JPM** | JPMorgan Chase | ~$309 | 퀄리티 최우수, 단 P/B 고평가·ROE 과잉달성 우려 |
| **V** | Visa | ~$350 | 네트워크 해자 강고, 규제 리스크 제한 |
| **MA** | Mastercard | ~$570 | V와 동일 구조, 크로스보더 회복 긍정 |
| **GS** | Goldman Sachs | ~$590 | M&A 사이클 회복 기대, 성과보수 변동성 주의 |
| **BLK** | BlackRock | ~$1,050 | iShares ETF 패시브 지배, 성장률 안정 |

**중립 공통 근거:**
- JPM: ROE 25% 목표 5년 연속 초과달성 → 추가 상승 제한적
- V/MA: 반독점 규제 리스크 상시 존재, 현 밸류에이션에 선반영
- GS/BLK: 과열은 아니나 매크로 불확실성 내 촉매 부재

---

### 매도/회피 (Sell/Avoid) 기업

| 티커 | 기업 | 현재가(추정) | 사유 |
|:--|:--|:--|:--|
| **UNH** | UnitedHealth Group | ~$407 | 다중 규제 조사, 결합비율 악화, MA 사기 소송 |
| **WFC** | Wells Fargo | ~$75 | 자산상한(Asset Cap) 규제 지속, 성장 제약 |
| **BRK.B** | Berkshire Hathaway | ~$530 | 시총 $1T+ 과중, 현금 누적 속 수익률 희석 우려 |

**매도/회피 근거:**
- UNH: 매사추세츠 州 MassHealth 과청구 $1억 소송, 결합비율 상승, EPS 가이던스 하향
- WFC: Fed 자산상한 해소 지연 → 대출 성장 구조적 제약
- BRK.B: 현금성 자산 $300B+ 누적 → 자본효율성(ROE) 희석, 상승 촉매 없음

---

## 3. LLM 퀀트 분석 마스터 프롬프트

아래 프롬프트를 Claude, GPT-4o, Gemini 등 LLM에 복사하여 사용하세요.

```
# ROLE
당신은 규율 기반 미국 금융주 퀀트 애널리스트입니다.
임무는 매수 권유가 아니라 두 모듈로 독립 채점하는 것입니다.
Module 1: 펀더멘털 품질(FQS) / Module 2: 과열도(OHS)
마지막에만 사분면으로 결합합니다.

# CORE PRINCIPLES
1. 품질 vs 타이밍 분리 — 좋은 기업도 비쌀 수 있다
2. 이익의 질 우선 — NIM·결합비율·AUM 순유입 중시
3. 규제 자본 적정성 — CET1, RBC, LCR 필수 확인
4. GAAP vs 핵심이익 분리 — 일회성 제거 후 판단
5. 레버리지 ETF — 30일 이내 청산 원칙
6. 근거 기반 — 수치 지어내기 금지, 추정 시 [추정] 표기
7. 투자자문 아님 — 출력은 진단, 권유 아님

# INPUT (아래 항목을 채워서 입력)
[기업명/티커/기준일/현재가]: {예: JPMorgan Chase / JPM / 2026-06-13 / $309}
[섹터 서브그룹]: {Banking / Cards & Payments / Insurance / Asset Management / Diversified / Brokerage}
[비즈니스 모델]: {간단 설명}

-- 펀더멘털 데이터 --
최근 4분기 매출 YoY: {}
핵심 수익지표:
  ▸ 은행: NIM={} / 비이자수익비중={} / 대출성장률={}
  ▸ 카드: GPV성장={} / 크로스보더={}
  ▸ 보험: 결합비율={} / 경과보험료성장={}
  ▸ 자산운용: AUM={} / 순유입={}
ROE={} / ROA={} / 영업이익률={}
CET1={} (은행) / RBC={} (보험) / 부채비율={}
연체율(NPL)={} / 무보험예금비중={}
FCF마진={} / 배당성향={} / 자사주비율={}
대출손실충당금(LLR)={} / 스트레스테스트={}

-- 타이밍 데이터 --
Fwd P/E={} / P/B={} / P/TBVPS={}
5년 백분위(Fwd P/E)={}%
RSI(14)={} / 200일 이평 이격={}% / 최근 실적 갭={}%
30일 목표가 상향 건수={} / 공매도 비중={}%
ARDS Phase={1 Expansion / 2 Late-Cycle / 3 Recession-Warning / 4 Recession}

# MODULE 1 — FUNDAMENTAL QUALITY SCORE (FQS)
각 축 0~100 채점 → 가중합 = FQS

| 축 | 가중 | 핵심 질문 | 레드플래그 |
|:--|:---:|:--|:--|
| A 성장의 질 | 15% | 유기적 성장 가속? NIM/AUM순유입 추이? | M&A 성장, 연체율 상승 |
| B 수익성·자본효율성 | 20% | ROE·ROA 업계 우위? 조정이익 지속성? | ROE 하락, NIM 축소 |
| C 안정성·예측가능성 | 20% | 예금안정·보험유지율·AUM장기계약? | 예금유출, AUM 순유출 |
| D 자본적정성 | 15% | CET1/RBC 규제치 상회? 배당여력? | CET1 근접, 배당 삭감 이력 |
| E 자본배분 | 10% | 배당·자사주 지속성? | 과도 배당, 무분별 M&A |
| F 해자·경쟁력 | 15% | 전환비용·규제장벽·브랜드? | 핀테크 잠식, 금리리스크 |
| G 회계 투명성 | 5% | 충당금 적정성, 자산건전성? | 충당금 급변동, 빈번한 일회성 |

FQS 등급: 80+ = A / 65~79 = B / 50~64 = C / <50 = D

# MODULE 2 — OVERHEATING SCORE (OHS)
각 성분 0~100 채점 → 가중합 = OHS (높을수록 과열)

| 성분 | 가중 | 채점 기준 |
|:--|:---:|:--|
| A 밸류에이션 | 20% | Fwd P/E·P/B 5년 백분위 고점권↑ |
| B 기술적 | 30% | RSI 70+·200일 이평 +20%+·어닝서프라이즈 클수록↑ |
| C 포지셔닝 | 20% | 목표가 상향 군집·공매도 극저↑ |
| D 내구성(역가중) | 15% | FQS 강할수록 OHS↓ (완충) |
| E 매크로(ARDS) | 15% | Late-Cycle/Recession-Warning일수록↑ |

OHS 페이즈: <36 = Accumulate / 36~55 = Hold / 56~75 = Trim-Wait / 76+ = Overheated

# 사분면 결합 (임계값 FQS 65, OHS 56)
┌─────────────────────────────────────────────────┐
│ FQS≥65 & OHS<56  → Accumulate (매수 기회)       │
│ FQS≥65 & OHS≥56  → Hold/Trim-Wait (보유/일부매도)│
│ FQS<65 & OHS<56  → Avoid/Value-Trap (회피)      │
│ FQS<65 & OHS≥56  → Overheated-Speculation (매도)│
└─────────────────────────────────────────────────┘

# OUTPUT — JSON 형식으로만 출력 (주석 없음)
{
  "ticker": "",
  "as_of": "YYYY-MM-DD",
  "fundamental": {
    "fqs": 0,
    "grade": "A|B|C|D",
    "subscores": {
      "growth": 0,
      "profitability_efficiency": 0,
      "stability_visibility": 0,
      "capital_adequacy": 0,
      "capital_allocation": 0,
      "moat_competition": 0,
      "accounting_transparency": 0
    }
  },
  "timing": {
    "ohs": 0,
    "phase": "Accumulate|Hold|Trim-Wait|Overheated",
    "subscores": {
      "valuation": 0,
      "technical": 0,
      "positioning": 0,
      "durability_inv": 0,
      "macro": 0
    }
  },
  "quadrant": "Accumulate|Hold/Trim-Wait|Avoid/Value-Trap|Overheated-Speculation",
  "gaap_bridge": "GAAP-비GAAP 격차 한줄 설명",
  "price_bands_12m": {
    "bull": [0, 0],
    "base": [0, 0],
    "bear": [0, 0]
  },
  "instruments": {
    "single_lev": "",
    "single_inv": "",
    "sector_long": "XLF / KBE / KRE / IAK / IPAY",
    "index_hedge": "FAS(3x레버리지) / FAZ(3x인버스)"
  },
  "confidence": 0.0,
  "bull_points": ["", "", ""],
  "bear_points": ["", "", ""],
  "estimated_fields": [],
  "data_gaps": []
}

# 면책: 권유 아님. 투자 책임은 본인.
```

---

## 4. Fear/Greed 섹터 스코어보드 프롬프트

금융 섹터 전체 센티먼트를 한 번에 진단할 때 사용합니다.

```
# 금융 섹터 Fear/Greed 진단 프롬프트

아래 데이터를 기반으로 미국 금융 섹터의 현재 Fear/Greed 상태를 
0(Extreme Fear) ~ 100(Extreme Greed) 척도로 채점하고 판정하라.

## 입력 데이터
- XLF 현재가 및 52주 위치: {}
- XLF Fwd P/E 및 5년 백분위: {}
- 금융 섹터 ETF 자금 흐름(4주): {}
- 금융주 평균 RSI(14): {}
- 실적 시즌 어닝 서프라이즈율: {}
- 공매도 비중(XLF): {}
- Fed 금리 방향성: {}
- 신용 스프레드(HY-IG): {}
- VIX: {}
- ARDS Phase: {}

## 채점 기준 (7개 지표 균등 가중)
1. 밸류에이션 백분위 (낮을수록 Fear)
2. 기술적 모멘텀 RSI (낮을수록 Fear)
3. 자금 흐름 (순유출일수록 Fear)
4. 실적 서프라이즈 (하향일수록 Fear)
5. 공매도 비중 (높을수록 Fear)
6. 신용 환경 (스프레드 확대일수록 Fear)
7. 매크로 ARDS (Recession-Warning일수록 Fear)

## 출력 형식
{
  "fear_greed_score": 0~100,
  "label": "Extreme Fear|Fear|Neutral|Greed|Extreme Greed",
  "component_scores": {...},
  "key_signal": "가장 강한 Fear 또는 Greed 신호",
  "tactical_implication": "현재 지수 수준에서의 포지셔닝 가이드"
}
```

---

## 5. 섹터별 특화 채점 루브릭

### Banking (은행)
| 축 | 핵심 지표 | 채점 포인트 |
|:--|:--|:--|
| A 성장 | NIM + 비이자수익 유기적 성장 | NIM 확대 중: +, 축소 중: - |
| B 수익성 | ROTCE, ROE, 효율성비율(Cost/Income) | ROTCE 15%+: A |
| C 안정성 | 무보험예금 비중, CET1, NPL 90일+ | 무보험예금 <25%: 우수 |
| D 자본 | CET1 규제치 대비 여유, 스트레스테스트 | 여유 >2%p: 우수 |
| E 배분 | 배당성향 30~50%, 자사주 | 과잉배당(>70%): 감점 |
| F 해자 | 소매 점포망, 브랜드, 지역 우위 | 디지털 전환 속도 체크 |
| G 회계 | ACL 적정성, NPL 분류 엄격성 | 충당금 갑작스런 변동: 감점 |

### Cards & Payments (카드·결제)
| 축 | 핵심 지표 | 채점 포인트 |
|:--|:--|:--|
| A 성장 | GPV 성장률, 크로스보더 거래 증가 | GPV YoY 10%+: A |
| B 수익성 | 순이익률, 건당 수익, 영업레버리지 | 영업이익률 50%+: A |
| C 안정성 | 반복적 네트워크 수익 비중 | 네트워크 수익 >70%: 우수 |
| F 해자 | 네트워크 효과, 전환비용, 규제 감시 | 반독점 규제: 상시 모니터 |

### Insurance (보험)
| 축 | 핵심 지표 | 채점 포인트 |
|:--|:--|:--|
| A 성장 | 경과보험료 성장, 신계약 증가율 | 경과보험료 YoY 8%+: A |
| B 수익성 | 결합비율(손해율+사업비율), ROE | 결합비율 <95%: 우수 |
| C 안정성 | 보유계약 유지율, 재보험 의존도 | 유지율 >85%: 우수 |
| D 자본 | RBC 비율 300%+, 부채적정성 | RBC <200%: 감점 |

### Asset Management (자산운용)
| 축 | 핵심 지표 | 채점 포인트 |
|:--|:--|:--|
| A 성장 | AUM 성장, 순유입률(유기적) | 순유입 >3% AUM: A |
| B 수익성 | 평균 Fee Rate, 영업이익률, ROE | 영업이익률 40%+: A |
| C 안정성 | 장기계약 AUM 비중, 고객 집중도 | 장기계약 >60%: 우수 |
| G 회계 | 성과보수 일회성 여부, GAAP 격차 | 성과보수 변동성 큼: 주의 |

---

## 6. 투자 도구 매핑 (금융 섹터 전용)

| 전략 | 도구 | 설명 |
|:--|:--|:--|
| 섹터 롱 | **XLF** | S&P500 금융 전종목, Expense 0.08% |
| 은행 집중 | **KBE** | S&P 은행 ETF |
| 지역은행 | **KRE** | 지역은행 집중 |
| 보험 | **IAK** | iShares U.S. Insurance ETF |
| 결제·핀테크 | **IPAY** | 모바일 결제 ETF |
| 레버리지(단기) | **FAS** | 금융 3배 레버리지 (30일 이내) |
| 인버스(단기) | **FAZ** | 금융 3배 인버스 (30일 이내) |

> ⚠️ 레버리지·인버스 ETF는 일일 리셋 decay 존재. 반드시 30일 이내 청산.

---

## 7. 백테스팅 Python 코드

아래 파일을 참조하세요: `financial_sector_backtest.py`

백테스팅 코드는 다음 기능을 포함합니다:
1. yfinance로 XLF, JPM, BAC, GS, V, UNH 등 주요 금융주 데이터 수집
2. FQS/OHS 프록시 지표 계산 (RSI, 이동평균, P/E 백분위 추정)
3. Fear/Greed 스코어보드 출력
4. 사분면별 전략 백테스팅 (Accumulate / Hold / Trim / Sell)
5. 성과 지표 출력 (CAGR, Sharpe, MDD, Win Rate)

---

## 면책 고지

```
본 문서는 투자 권유가 아닌 분석 프레임워크 제공을 목적으로 합니다.
모든 투자 결정의 책임은 투자자 본인에게 있으며,
실제 투자 시 전문 투자 자문사와 상담하시기 바랍니다.

작성: Dennis Kim (HoKwang Kim) / Betalabs Inc.
GitHub: github.com/gameworkerkim
ORCID: 0009-0002-0962-2175
```
