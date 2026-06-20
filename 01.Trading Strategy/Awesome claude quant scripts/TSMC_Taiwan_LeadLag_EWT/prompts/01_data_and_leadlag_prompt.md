# Prompt 01 — 데이터 수집 & 선행지표(Lead-Lag) 검증

아래 프롬프트를 Claude(또는 동급 코딩 에이전트)에 그대로 붙여 넣으면
`data_lib.py` + `leadlag.py` 결과를 재현할 수 있다.

---

당신은 매크로/주식 퀀트 리서처다. 다음을 수행하라.

**1) 데이터 (2020-01 ~ 2026-05, 월간)**
- TSMC 월간 매출과 YoY 성장률. (가능하면 TSMC IR 월매출 실데이터, 불가 시
  연간 실측치 + 분기 YoY 앵커로 월간 재구성. 2022 Q3 피크 ~+48%, 2023 중반
  저점 음(−), 2024~25 AI 회복을 반드시 반영.)
- 대만 실질 GDP 분기 YoY (DGBAS 실측: 2024Q1 6.64 … 2025Q4 12.65). 월간 보간.
- iShares MSCI Taiwan ETF(EWT) 월간 가격. 온라인이면 yfinance→stooq 순 시도,
  실패 시 연 수익률 실측(2020 +31.5%, 2022 −28.8%, 2025 +27.8% 등)에 고정된
  재현 가능 시계열 생성.
- 실측 앵커와 출처를 `anchors.md` 로 문서화하라.

**2) 선행지표 검증 — "TSMC 성장률 vs 대만 GDP 성장률, 무엇이 선행하는가?"**
- TSMC YoY 를 −12~+12개월 시프트하며 대만 GDP YoY 와 교차상관(cross-correlation)
  을 계산. 상관이 최대가 되는 lag 를 찾아라. (lag>0 → TSMC 가 GDP 선행)
- 간이 그레인저 인과: GDP_t 를 (a) GDP 자기시차만 (b) +TSMC 시차 로 회귀하여
  TSMC 가 추가하는 증분 R² 를 보고하라.
- 결과를 `leadlag_summary.json`, 교차상관 막대그래프 `leadlag.png` 로 저장.

**3) 해석 — 통념을 검증/반증하라**
- "TSMC 가 대만 GDP 의 22%이므로 당연히 선행지표"라는 통념이 *데이터로* 성립하는가?
- 성립하지 않는다면 그 이유(기저효과, 주문 백로그, 분기 GDP vs 월간 매출의
  공시 시차)를 설명하라. 결과를 미화하지 말고 honest 하게 보고하라.

산출물: `data_lib.py`, `leadlag.py`, `results/leadlag_summary.json`,
`results/leadlag_crosscorr.csv`, `results/leadlag.png`, `data/anchors.md`.
