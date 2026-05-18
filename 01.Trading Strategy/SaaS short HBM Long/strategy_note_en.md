# Hedge Fund Trader and Quant Perspectives on AI Disruption

## Hedge Fund Trader Perspective

**Theme**: An event-driven, macro long/short strategy that captures both the "SaaS-pocalypse" and the HBM supercycle simultaneously.

### Short Targets — Subscription Services in the Crosshairs

Pure SaaS / subscription models: Adobe, Duolingo, Wix, Shutterstock, etc.

**Entry criteria**:

- Inclusion in BofA's list of 26 "AI high-risk" names
- DAU / paid-subscriber growth deceleration signals (e.g., Duolingo's pattern of DAU growth alongside declining paid-conversion rate)
- Pre-emptive short positioning around Big Tech free AI-agent launch announcements

**Options strategy**: Collect premium via covered calls or put-spread selling while capping risk. In high-volatility regimes, buy OTM puts to hedge tail risk.

### Long Targets — AI Hardware and Physical-Gateway Platforms

- **Core longs**: Samsung Electronics, SK Hynix (HBM supply bottleneck + ongoing P/E re-rating)
- **Supplementary longs**: Uber (physical data and driver network + transaction gateway platform), TSMC (foundry monopoly)

**Entry timing**: Accumulate on dips caused by US Treasury yield spikes from Japanese bond selling. Widen the position as the gap between Nomura's price target and spot widens.

### Pair Trade — Software Destruction, Hardware Concentration

- **Short leg**: SEG SaaS Index ETF (or a custom SaaS basket)
- **Long leg**: SOX (semiconductor index), Samsung / Hynix / Micron basket

**Macro overlay**: If the US 30-year yield stays above 5.1%, long-duration SaaS valuations face additional pressure — increase pair weight.

### Macro Hedge

Japan's selling of US Treasuries → upward pressure on rates → potential compression of Nasdaq / growth-stock valuations.

To hedge, mix in TLT shorts or rate-futures shorts to reduce overall portfolio beta.

---

## Quant Perspective

**Theme**: A market-neutral, statistical long/short portfolio that isolates an AI disruption factor.

### Factor Design

**AI Disruption Score**:

- Subscription revenue share (higher → short)
- AI patents per R&D dollar (lower → short)
- Physical assets / proprietary data ownership (none → short)
- Management NLP sentiment on earnings calls (frequency of "AI threat" mentions)

Short the top 20% by this score, long the bottom 20% (semiconductors and infrastructure) to build a factor-neutral portfolio.

### Statistical Arbitrage

Analyze the cointegration relationship between SaaS indices (e.g., WCLD) and semiconductor indices (SOX); enter long/short when the residual spread exceeds 2σ.

**High-frequency signal**: When names like Duolingo and Adobe show short-term momentum breakdowns, amplify downside signals via trend-following models.

### NLP Signals — Earnings Calls and News Analysis

Automatically scale up the short allocation when news mention frequency of keywords like "SaaS-pocalypse" or "Big Squeeze" spikes.

Quantify negative analyst language ("Disappoint", "Automation not Agentic" — e.g., RBC's Agentforce review) and trade the surprise reaction.

### Risk Management

- Maintain net beta at 0–0.1 via minimum-variance optimization under sector-neutral constraints.
- Monitor stock-loan availability: a spike in SaaS short interest signals squeeze risk → rotate to higher-liquidity tickers or convert exposure into puts.

### Execution Algorithm

- VWAP / TWAP order splitting to minimize slippage.
- During intraday volatility spikes: limit orders for shorts, volatility-collapse entries for longs.

---

## Prompts for LLM Strategy Extraction

### Korean Prompt

```text
당신은 글로벌 헤지펀드의 매크로 트레이더이자 퀀트 리서처입니다. 
다음 칼럼을 읽고, 구독형 서비스가 AI로 인해 몰락하는 상황에서 
취할 수 있는 구체적인 공매도 전략과 투자 전략을 두 관점에서 도출하세요.

- 헤지펀드 트레이더 관점: 종목 공매도·롱 아이디어, 페어 트레이드, 
  매크로 오버레이, 옵션 전략, 이벤트 진입 타이밍 등을 포함하세요.
- 퀀트 관점: 팩터 모델, 통계적 차익거래, NLP 시그널, 
  리스크 관리, 실행 알고리즘 등을 포함하세요.

칼럼:
[여기에 칼럼 전체 텍스트를 붙여넣으세요]

출력은 한국어로, 각 항목을 명확히 구분해주세요.
```

### English Prompt

```text
You are a macro trader and a quantitative researcher at a global hedge fund. 
Based on the following article, extract concrete short-selling and investment 
strategies for the AI-driven collapse of subscription-based services from two perspectives.

- Trader perspective: Include specific short/long ideas, pairs trades, 
  macro overlay, options strategies, and event-based entry timing.
- Quant perspective: Include factor models, statistical arbitrage, 
  NLP signals, risk management, and execution algorithms.

Article:
[Insert the full column text here]

Output in English, clearly separating the two perspectives.
```

Feeding a column into this prompt yields a structured hedge-fund trading playbook in the form summarized above.
