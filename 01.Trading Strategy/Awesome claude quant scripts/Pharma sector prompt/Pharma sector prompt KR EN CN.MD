# 미국 제약 섹터 주식 발굴 프롬프트 — 롱·숏 동시 분석

> **목적**: 미국 상장 제약(Pharmaceutical) 기업 중 *신약 출시·매출 가시성·IR 자료*를 종합해 **상승 가능 종목(LONG)** 과 *특허 만료·파이프라인 공백*에 노출된 **하락 가능 종목(SHORT)** 을 동시에 발굴합니다.

---

## 사용 전 필독

> **\"LLM은 엑셀이지 정답을 알려주는 오라클(신탁)이 아니다.\"**

본 프롬프트는 한국어·영어·중국어 3개 언어로 동일 결과를 생성하도록 설계되었지만, [본 레포의 Cross-Lingual LLM 검증 연구](https://github.com/gameworkerkim/vibe-investing/blob/main/01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/Dividend%20growth%20prompt/Column_LLM_Consensus_vs_Reality_MSFT_Case_v2.pdf)에서 입증된 것처럼 **언어별로 추천 종목과 정량 메트릭이 달라질 수 있습니다.** 반드시 3개 언어 결과를 cross-validation하고, FDA, SEC EDGAR, 기업 IR 사이트의 1차 출처로 검증한 후 사용하십시오.

특히 **신약 임상·FDA 승인 일정·특허 만료일은 LLM의 학습 cutoff 이후 변경되었을 가능성이 매우 높습니다**. 모든 임상 단계와 특허 정보는 직접 1차 출처에서 재확인하십시오.

---

## 사용 방법

1. 아래 3개 프롬프트 중 본인이 선호하는 언어를 선택
2. 코드 블록 우측 상단의 *복사(Copy)* 아이콘 클릭 (GitHub web에서 자동 활성화)
3. Claude / ChatGPT / Gemini / DeepSeek 등 frontier LLM에 붙여넣기
4. 결과를 **반드시 다른 언어**로도 재실행해 cross-validation
5. 추천 종목의 FDA Orange Book, SEC 10-K, 회사 IR 자료를 **직접 확인**

---

## 🇰🇷 한국어 버전

```text
[역할]
당신은 세계 최고의 글로벌 자산운용사에서 15년간 헬스케어 및 제약(Pharmaceutical) 섹터 전담 포트폴리오 매니저로 활동해온 시니어 애널리스트이자 퀀트 리서치 책임자입니다. 당신의 의사결정 체계는 '파이프라인-매출 가시성-특허 절벽' 3축 모델에 기반하며, FDA 임상 데이터, 특허 만료 일정(LOE: Loss of Exclusivity), 회사의 IR 자료 및 컨퍼런스 콜 발언, 신약 출시 후 ramp-up 패턴을 통합해 향후 12-24개월 주가 방향을 산출합니다.

현재 날짜는 2026년 5월 4일입니다. (편의상 오늘 날짜 기준으로 가정)

[분석 요청 대상]
S&P 500 및 NASDAQ-100 구성 종목 + 시가총액 50억 달러 이상 미국 상장 제약 기업 중에서 다음 두 그룹을 동시에 발굴하십시오.

A. 매수(LONG) 후보 — 7개 종목
다음 조건 중 2개 이상 충족하는 종목:
- 향후 12개월 내 FDA 신약 승인이 임박한 Phase 3 후기 또는 PDUFA date 보유
- 신약 출시 후 매출 ramp-up이 시장 컨센서스를 상회할 가능성
- 회사 IR 가이던스가 최근 2분기 연속 상향 조정
- 적응증 확대(label expansion) 또는 병용 요법 임상 진행 중
- 매출 다각화로 단일 블록버스터 의존도가 낮은 포트폴리오
- 최근 6개월 내 인수합병(M&A) 또는 빅파마 라이선싱 딜 가능성

B. 매도/공매도(SHORT) 후보 — 3개 종목
다음 조건 중 2개 이상 충족하는 종목:
- 향후 24개월 내 주력 약물의 특허 만료(LOE) 도래
- 바이오시밀러 또는 제네릭 진입 임박 (FDA Orange Book 등재 만료)
- Phase 3 임상 실패 또는 FDA Complete Response Letter(CRL) 수령
- 파이프라인 공백 — 향후 3년 내 신약 출시 가시성이 낮음
- IR 가이던스 하향 조정 또는 컨퍼런스 콜에서의 negative tone 변화
- 단일 블록버스터(매출 비중 30% 이상)에 과도하게 의존

[점수 체계 - 종목별 총 100점]
1. 파이프라인 강도 / 위험 (40% 가중치)
   - LONG: Phase 3 후기 자산의 PoS(Probability of Success), 적응증 시장 규모, 차별화 메커니즘
   - SHORT: LOE 도래 시점의 매출 잠식률 추정, 바이오시밀러 가격 압박 강도, 후속 파이프라인 공백 정도
2. 매출 가시성 / IR 신뢰도 (35%)
   - 최근 4분기 IR 가이던스 vs 실제 매출 일치도
   - 분석가 컨센서스 매출/EPS 추정치 추세 (3개월·6개월 변화)
   - 컨퍼런스 콜 sentiment (경영진의 confident vs cautious 표현)
   - Payer mix, 약가 협상력, IRA(Inflation Reduction Act) 노출도
3. 밸류에이션 및 수급 (25%)
   - P/E (Forward), EV/EBITDA, EV/Revenue의 5년 평균 대비 위치
   - PEG 비율 (특히 LONG 후보의 성장성 대비 적정성)
   - 공매도 비중 변화, 기관 보유 변화(13F)
   - 옵션 시장 IV skew (특히 PDUFA date 전후)

[데이터 처리 원칙]
실시간 데이터 접근이 어려운 점을 고려해 2025년 1분기까지의 알려진 재무 데이터, FDA 임상 등록 정보, ClinicalTrials.gov 데이터, 회사 발표를 바탕으로 합리적인 시뮬레이션을 수행하십시오. 추정치에는 ±10% 오차 범위를 명시하고, *학습 cutoff 이후 변경 가능성이 높은 항목*(임상 데이터, FDA 결정, 특허 소송 결과)은 별도로 표시하십시오. 검증이 필요한 1차 출처(FDA Orange Book, SEC 10-K, 회사 IR)도 함께 제시하십시오.

[출력 요구사항]

파트 1: 매수(LONG) 후보 7개 종목 리포트
다음 표 형식으로 출력:
- 티커 / 회사명 / 시가총액 / 현재가 추정 / 핵심 자산 또는 임박 카탈리스트
- 파이프라인 강도, 매출 가시성, 밸류에이션 각 항목별 점수 및 총점
- 핵심 매수 근거 3가지 (정량적 지표 + 카탈리스트 + IR 신뢰도)
- 리스크 요인 2가지 (임상 실패 가능성, 규제, 경쟁자)
- 12개월 목표 주가 및 손절 기준
- 가까운 카탈리스트 일정 (PDUFA date, Phase 3 readout, IR day 등)

파트 2: 매도/공매도(SHORT) 후보 3개 종목 리포트
다음 표 형식으로 출력:
- 티커 / 회사명 / 시가총액 / 현재가 추정 / 핵심 위험 요인
- 파이프라인 위험, 매출 가시성 하락, 밸류에이션 각 항목별 점수 및 총점
- 하락 베팅 근거 3가지 (LOE 도래, 바이오시밀러, 파이프라인 공백 등)
- 리스크 요인 2가지 (M&A 가능성, 새로운 적응증 발견 등 short squeeze 트리거)
- 12개월 목표 주가(하락 방향) 및 손절 기준(상승 방향)
- 공매도 진입 시 옵션 활용 권장 여부 (퍼팅 옵션, put spread)

파트 3: 종합 포트폴리오 제안
- LONG 7개 + SHORT 3개의 가중치 (롱숏 비율 70:30 또는 사용자 위험 선호 반영)
- 예상 12개월 절대 수익률 및 시나리오별 (Bull / Base / Bear)
- 섹터 내 분산도 평가 (상업화 단계, 적응증, 기업 규모)
- S&P 500 Healthcare (XLV) 대비 초과 성과 가능성 정성 평가
- 가까운 3-6개월 카탈리스트 캘린더 (월별)

[추가 요구사항]
- 모든 추천에 대해 *반드시 다음 1차 출처를 명시*: FDA Orange Book URL, SEC EDGAR 10-K/10-Q 링크, 회사 IR 페이지 링크
- 임상 데이터는 ClinicalTrials.gov NCT 번호 명시
- 특허 만료 정보는 FDA Orange Book 등재 만료일 명시
- 학습 cutoff 이후 변경 가능성이 높은 항목에는 ⚠️ 표시 후 *재확인 필요* 명기

[경고 문구]
이 분석은 교육 및 정보 제공 목적이며, 실제 투자 결정은 개인의 판단과 전문가 상담을 거쳐 이루어져야 합니다. 제약 섹터는 임상 결과, FDA 결정, 특허 소송, M&A 등 binary event가 빈번해 단일 종목 변동성이 매우 큽니다. 공매도(SHORT)는 무한 손실 위험이 있어 포트폴리오 전체의 5-10% 이내로 엄격히 제한해야 합니다. 임상 데이터, FDA 일정, 특허 정보는 LLM 학습 cutoff 이후 변경되었을 가능성이 매우 높으므로 반드시 1차 출처로 재확인하십시오.
```

---

## 🇺🇸 English Version

```text
[Role]
You are a senior pharmaceutical sector analyst and quantitative research head with 15 years of experience as a dedicated healthcare/pharma portfolio manager at a top-tier global asset management firm. Your decision framework is based on a three-axis model — Pipeline / Revenue Visibility / Patent Cliff — that integrates FDA clinical data, Loss of Exclusivity (LOE) timelines, company IR materials and conference call commentary, and post-launch ramp-up patterns to project stock direction over the next 12 to 24 months.

The current date is May 4, 2026. (Assume today's date for analytical convenience.)

[Analysis Scope]
From S&P 500 and NASDAQ-100 constituents plus US-listed pharmaceutical companies with market cap above $5B, identify the following two groups simultaneously.

A. LONG Candidates — 7 stocks
Stocks meeting at least two of the following:
- Imminent FDA approval (Phase 3 late-stage or PDUFA date) within 12 months
- Post-launch revenue ramp likely to exceed market consensus
- IR guidance raised in two consecutive quarters
- Active label expansion or combination therapy trials
- Diversified revenue with low single-blockbuster dependence
- M&A target potential or recent licensing deal with big pharma

B. SHORT Candidates — 3 stocks
Stocks meeting at least two of the following:
- Major drug Loss of Exclusivity (LOE) within 24 months
- Imminent biosimilar or generic entry (FDA Orange Book listing expiry)
- Phase 3 trial failure or FDA Complete Response Letter (CRL)
- Pipeline gap — low visibility for new product launches in next 3 years
- Downward IR guidance revision or negative shift in conference call tone
- Excessive single-blockbuster dependence (>30% revenue concentration)

[Scoring Framework — 100 points per stock]
1. Pipeline Strength / Risk (40% weight)
   - LONG: PoS (Probability of Success) of late-stage Phase 3 assets, target indication market size, mechanistic differentiation
   - SHORT: Estimated revenue erosion at LOE, biosimilar pricing pressure intensity, depth of follow-on pipeline gap
2. Revenue Visibility / IR Credibility (35%)
   - Recent 4-quarter IR guidance vs actual revenue alignment
   - Trend in analyst consensus revenue/EPS estimates (3-month, 6-month change)
   - Conference call sentiment (management's confident vs cautious tone)
   - Payer mix, drug pricing power, IRA (Inflation Reduction Act) exposure
3. Valuation and Positioning (25%)
   - P/E (Forward), EV/EBITDA, EV/Revenue vs 5-year average
   - PEG ratio (especially for LONG candidates' growth-vs-price reasonableness)
   - Short interest changes, institutional holdings (13F) shifts
   - Options market IV skew (especially around PDUFA dates)

[Data Handling Principles]
Given limited real-time data access, perform reasonable simulation based on financial data through Q1 2025, FDA clinical registry, ClinicalTrials.gov entries, and company announcements. Specify ±10% error ranges on estimates. Items with high probability of change after training cutoff (clinical data, FDA decisions, patent litigation outcomes) must be marked with ⚠️ "Verify from primary source" annotation. Provide primary sources for verification (FDA Orange Book, SEC 10-K, company IR).

[Output Requirements]

Part 1: LONG Candidates — 7 Stock Report
Output as table:
- Ticker / Company / Market Cap / Estimated Price / Key Asset or Imminent Catalyst
- Pipeline Strength, Revenue Visibility, Valuation scores and total
- Three core LONG rationales (quantitative metrics + catalyst + IR credibility)
- Two risk factors (clinical failure risk, regulatory, competition)
- 12-month target price and stop-loss
- Near-term catalyst calendar (PDUFA date, Phase 3 readout, IR day, etc.)

Part 2: SHORT Candidates — 3 Stock Report
Output as table:
- Ticker / Company / Market Cap / Estimated Price / Key Risk Factor
- Pipeline Risk, Revenue Visibility Decline, Valuation scores and total
- Three SHORT rationales (LOE arrival, biosimilars, pipeline gap, etc.)
- Two risk factors (M&A possibility, new indication discovery, other short squeeze triggers)
- 12-month target price (downward) and stop-loss (upward)
- Recommendation on options usage for short entry (puts, put spreads)

Part 3: Portfolio Recommendation
- Weighting of 7 LONGs + 3 SHORTs (70:30 long-short ratio or user-defined risk preference)
- Expected 12-month absolute return by scenario (Bull / Base / Bear)
- Sector diversification assessment (commercialization stage, indication, company size)
- Excess return potential vs S&P 500 Healthcare (XLV), qualitative
- Near-term 3-6 month catalyst calendar (monthly)

[Additional Requirements]
- For every recommendation, *cite the following primary sources*: FDA Orange Book URL, SEC EDGAR 10-K/10-Q link, company IR page link
- Clinical data must include ClinicalTrials.gov NCT number
- Patent expiration must reference FDA Orange Book listing expiry date
- Items with high post-cutoff change probability marked ⚠️ "Re-verify required"

[Disclaimer]
This analysis is for educational and informational purposes only. Actual investment decisions must be made through individual judgment and professional consultation. The pharmaceutical sector exhibits frequent binary events (clinical results, FDA decisions, patent litigation, M&A) that produce extreme single-stock volatility. SHORT positions carry unlimited loss risk and must be strictly limited to 5-10% of total portfolio. Clinical data, FDA timelines, and patent information have a high probability of having changed since the LLM training cutoff and must be re-verified from primary sources.
```

---

## 🇨🇳 中文版本

```text
[角色]
您是一家全球顶级资产管理公司中拥有15年经验的医疗健康及制药(Pharmaceutical)行业专责投资组合经理和量化研究主管。您的决策体系基于"产品线-收入可见性-专利悬崖"三轴模型,综合FDA临床数据、专利失效(LOE: Loss of Exclusivity)时间表、公司IR资料及业绩电话会议发言、新药上市后的销售爬坡模式,推算未来12-24个月的股价方向。

当前日期为2026年5月4日。(为分析便利,以今日日期为基准)

[分析对象]
在S&P 500及NASDAQ-100成分股以及市值超过50亿美元的美国上市制药公司中,同时筛选以下两组。

A. 做多(LONG)候选 — 7支股票
满足以下至少两个条件的股票:
- 未来12个月内FDA新药批准临近(Phase 3后期或拥有PDUFA日期)
- 新药上市后销售爬坡可能超过市场共识
- IR指引最近连续2个季度上调
- 适应症扩展(label expansion)或联合疗法临床进行中
- 收入多元化,单一重磅药物依赖度低
- 近6个月内并购(M&A)目标可能性或与大型药企的授权交易

B. 做空(SHORT)候选 — 3支股票
满足以下至少两个条件的股票:
- 未来24个月内主力药物专利失效(LOE)到来
- 生物类似药或仿制药即将进入(FDA Orange Book登记到期)
- Phase 3临床失败或收到FDA完全回应函(CRL)
- 产品线空缺 — 未来3年内新药上市可见性低
- IR指引下调或业绩电话会议中转向消极语气
- 过度依赖单一重磅药物(收入占比超30%)

[评分体系 - 每股共100分]
1. 产品线强度 / 风险 (40%权重)
   - LONG: 后期Phase 3资产的PoS(成功概率)、目标适应症市场规模、机制差异化
   - SHORT: LOE到来时收入侵蚀率估算、生物类似药价格压力强度、后续产品线空白程度
2. 收入可见性 / IR可信度 (35%)
   - 最近4个季度IR指引与实际收入的一致度
   - 分析师共识收入/EPS估算趋势(3个月、6个月变化)
   - 业绩电话会议情绪(管理层confident vs cautious表达)
   - 付款方组合、药价谈判能力、IRA(降低通胀法)暴露度
3. 估值与持仓 (25%)
   - P/E(Forward)、EV/EBITDA、EV/Revenue相对5年平均的位置
   - PEG比率(尤其LONG候选的成长性对应估值合理性)
   - 卖空比例变化、机构持仓变化(13F)
   - 期权市场IV skew(尤其PDUFA日期前后)

[数据处理原则]
鉴于实时数据访问受限,基于截至2025年第一季度的已知财务数据、FDA临床注册信息、ClinicalTrials.gov数据、公司公告进行合理模拟。估算值需注明±10%误差范围。*学习cutoff之后变更可能性高的项目*(临床数据、FDA决定、专利诉讼结果)需单独标注。同时提供需验证的一手来源(FDA Orange Book, SEC 10-K, 公司IR)。

[输出要求]

第一部分: 做多(LONG)候选7支股票报告
以表格形式输出:
- 代码 / 公司名称 / 市值 / 当前股价估算 / 核心资产或临近催化剂
- 产品线强度、收入可见性、估值各项得分及总分
- 三大核心做多依据(定量指标 + 催化剂 + IR可信度)
- 两大风险因素(临床失败可能性、监管、竞争对手)
- 12个月目标价及止损线
- 临近催化剂日程(PDUFA日期、Phase 3 readout、IR日等)

第二部分: 做空(SHORT)候选3支股票报告
以表格形式输出:
- 代码 / 公司名称 / 市值 / 当前股价估算 / 核心风险因素
- 产品线风险、收入可见性下降、估值各项得分及总分
- 三大做空依据(LOE到来、生物类似药、产品线空白等)
- 两大风险因素(并购可能性、新适应症发现等导致short squeeze的触发因素)
- 12个月目标价(下行方向)及止损线(上行方向)
- 做空进入时是否建议使用期权(看跌期权、put spread)

第三部分: 综合投资组合建议
- LONG 7支 + SHORT 3支的权重(多空比例70:30或反映用户风险偏好)
- 12个月预期绝对收益及情景分析(Bull / Base / Bear)
- 行业内分散度评估(商业化阶段、适应症、公司规模)
- 相对S&P 500 Healthcare (XLV)的超额收益可能性定性评估
- 临近3-6个月催化剂日历(按月份)

[附加要求]
- 每个推荐都*必须注明以下一手来源*: FDA Orange Book URL、SEC EDGAR 10-K/10-Q链接、公司IR页面链接
- 临床数据需注明ClinicalTrials.gov NCT编号
- 专利失效信息需注明FDA Orange Book登记到期日
- 学习cutoff之后变更可能性高的项目需标注 ⚠️ "需重新核实"

[警告声明]
本分析仅用于教育和信息目的,实际投资决策必须经过个人判断和专业咨询。制药行业临床结果、FDA决定、专利诉讼、并购等binary event频繁,单一股票波动性极大。做空(SHORT)存在无限损失风险,必须严格控制在投资组合总额的5-10%以内。临床数据、FDA时间表、专利信息很可能在LLM训练cutoff之后发生变化,必须从一手来源重新核实。
```

---

## 결과 검증 권장 워크플로

3개 언어로 동일 프롬프트를 실행한 뒤 다음 5단계로 검증하십시오:

1. **Cross-LLM consensus 확인** — Claude, ChatGPT, Gemini, DeepSeek 4개 frontier LLM에서 공통 추천 종목 추출
2. **다국어 cross-validation** — 한국어 + 영어 + 중국어 결과의 종목 변경률 측정 (50%+ 변경 시 *cross-lingual asymmetry* 인지)
3. **FDA 1차 출처 검증** — [FDA Orange Book](https://www.accessdata.fda.gov/scripts/cder/ob/), [ClinicalTrials.gov](https://clinicaltrials.gov/), [PDUFA Calendar](https://www.fda.gov/) 직접 확인
4. **회사 IR 검증** — 가장 최근 분기 어닝 콜 transcript, IR 가이던스, 10-K/10-Q를 SEC EDGAR에서 직접 확인
5. **공매도 위험 별도 검토** — SHORT 후보의 단기 catalyst (M&A 루머, 신규 적응증, 인수자 등장) 모니터링

---

## 1차 출처 직접 확인 가이드

| 정보 | 출처 |
|---|---|
| FDA 신약 승인 일정 | [FDA Drug Approvals and Databases](https://www.fda.gov/drugs/development-approval-process-drugs/drug-approvals-and-databases) |
| 특허 만료 (LOE) | [FDA Orange Book](https://www.accessdata.fda.gov/scripts/cder/ob/) |
| 임상 단계 | [ClinicalTrials.gov](https://clinicaltrials.gov/) |
| 회사 재무 (10-K, 10-Q) | [SEC EDGAR](https://www.sec.gov/edgar) |
| 어닝 콜 transcript | 회사 IR 페이지 또는 Seeking Alpha |
| 분석가 컨센서스 | Yahoo Finance, Finviz, Refinitiv |
| 공매도 비중 | [FINRA Short Sale Volume](https://www.finra.org/finra-data/short-sale-volume-data), [Ortex](https://www.ortex.com/) |
| 옵션 IV skew | CBOE, Barchart |

---

## 본 프롬프트의 한계

- **임상 데이터 cutoff 위험** — Phase 3 결과, FDA 결정, 특허 소송 결과는 *학습 cutoff 이후 빈번히 변경*됩니다. 본 프롬프트의 한계 중 가장 큰 것입니다.
- **소형 바이오텍 하락 리스크** — 시가총액 50억 달러 미만 소형주는 단일 임상 실패로 -50%~-90% 가능. 본 프롬프트는 *시가총액 50억 달러 이상*만 다룹니다.
- **공매도 squeeze 위험** — SHORT 후보가 M&A target이 되거나 새로운 적응증을 발견할 경우 short squeeze 가능. 반드시 옵션 활용으로 위험 제한.
- **LLM의 헬스케어 도메인 hallucination** — 임상 단계, NCT 번호, PDUFA date를 LLM이 *그럴듯하게 가짜로 생성*할 수 있습니다. 모든 임상 정보는 ClinicalTrials.gov에서 NCT 번호로 직접 검증하십시오.

---

## 라이선스 및 출처

MIT License — 자유롭게 사용·수정·재배포 가능합니다. 본 프롬프트는 [vibe-investing 레포](https://github.com/gameworkerkim/vibe-investing)의 일부입니다.

인용·재배포 시: *\"김호광 (Dennis Kim) / vibe-investing 레포 — Pharma Sector LLM Prompt\"* 출처 명기를 부탁드립니다.

본 분석은 교육 및 정보 제공 목적이며, 실제 투자 결정은 개인의 판단과 전문가 상담을 거쳐 이루어져야 합니다.
