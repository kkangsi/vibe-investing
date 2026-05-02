# vibe-investing

A repository of AI-powered market analysis essays, quant trading strategies, and curated AI investment tool lists.

Markets covered: US NASDAQ / S&P500, cryptocurrency, European luxury sector, crypto-equity correlation.

- Author: Dennis Kim (HoKwang Kim)
- License: MIT
- Update frequency: 1-2 times per week
- Korean README: [README.md](README.md)

> **Language note:** Most articles are written in Korean. Items tagged `[KR]` have not been translated yet. Use a translator (Google Translate, DeepL, ChatGPT, Claude) to read them. Code, datasets, and table headers are language-neutral.

---

## Investment Philosophy

1. **I have worked in the blockchain market since 2017, serving as a bridge between Korea and China.** Hypotheses that worked in one market often moved in the opposite direction in the other. Reading that gap is the starting point.

2. **AI is a tool — like Excel.** LLMs are not omnipotent. The human insight that reads the model matters more.

3. **Model intelligence is not trading intelligence.** In Alpha Arena Season 1, GPT-5 returned -75% while DeepSeek V3.1 returned +46%. The smarter model is not the one that makes money.

4. **A backtest is just a hypothesis.** Survival in live trading is verification. Every backtest result in this repo is published with its limitations.

5. **Data is open.** 14+ CSVs make every analysis reproducible. Closed alpha is not alpha.

---

## Quick Start

| Goal | Recommended Path |
|---|---|
| Market insights only | [Columns](#columns) — start with LTCM or After Market Close |
| Browse trading strategies | [Trading Strategies](#trading-strategies) |
| Browse AI investment tools | [Curation](AWESOME.md) |
| Run code immediately | [Tools](#tools) — Nasdaq-BTC Coupling Bot |
| Get datasets only | [Datasets](#datasets) |
| Read research papers | [Research / Papers](#research--papers) |

---

## Recent Updates

| Date | Item | Type |
|---|---|---|
| 2026-05 | Awesome claude quant scripts (4 strategies) | Trading Strategy `[KR]` |
| 2026-05-01 | Awesome AI Quant Prompt evaluation | Curation `[KR]` |
| 2026-05-01 | Awesome Vibe Trading Bot | Curation `[KR]` |
| 2026-04-17 | Nasdaq-BTC Coupling Bot v1 | Tool |
| 2026-04 | BTC-Nasdaq coupling analysis | Column `[KR]` |
| 2026-04 | Luxury investment strategy | Column `[KR]` |
| 2026-04 | DAT mNAV arbitrage | Column `[KR]` |
| 2026-04 | After Market Close disclosure timing | Column `[KR]` |

---

## Columns

Seven essays analyzing macro market trends and industry shifts. Full index in [02.Investment Idea Column/README.md](02.Investment%20Idea%20Column/README.md).

| # | Title | Topic | Data | Lang |
|---|---|---|---|---|
| 1 | [Risk Management Lessons from LTCM](Vibe%20Investing%20Risk%20Management.MD) | 1998 LTCM collapse + AI investing risks | - | KR |
| 2 | [Microsoft's Fintool Acquisition](Microsoft%20fintool%20acquisition%20column.MD) | $37B financial data terminal market analysis | - | KR |
| 3 | [Invisible Hand or Coordinated Fraud?](Crypto%20perp%20manipulation%20column.MD) | Mathematical analysis of crypto perp pump-dump | - | KR |
| 4 | [Does the Market Open When Closed?](AfterMarketClose/After_Market_Close_Column.md) | 91.2% of impactful disclosures hit AMC | 34 cases | KR |
| 5 | [DAT mNAV Arbitrage Strategy](mNAV(Market-to-Net-Asset-Value)%20arbitrage/Dat%20mnav%20arbitrage%20strategy.MD) | MSTR/BMNR digital asset treasury analysis | 3 CSVs | KR |
| 6 | [When to Buy Luxury](01.Trading%20Strategy/Luxury%20investment%20strategy/Luxury%20investment%20strategy.md) | LVMH/Hermès/Kering 3-tier portfolio | 4 CSVs | KR |
| 7 | [BTC-Nasdaq Coupling](01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/Nasdaq%20crypto%20coupling%20strategy.MD) | 6-year correlation + 6 regime classification | 4 CSVs | KR |

`[KR]` = Article body is in Korean. Use a translator to read.

Recommended reading order: 1 → 4 → 6 → 7 (risk management → market structure → sector analysis → quantitative analysis)

---

## Trading Strategies

Full index in [01.Trading Strategy/README.md](01.Trading%20Strategy/README.md).

| Category | Description |
|---|---|
| [Awesome claude quant scripts](01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/) | 4 trading strategies built with Claude (AI supply chain Bayesian / DAT / Declining stocks / Long-term dividend) |
| [Luxury investment strategy](01.Trading%20Strategy/Luxury%20investment%20strategy/) | LVMH/Hermès/Kering luxury sector 3-tier portfolio |
| [Investment Strategy Based on Bitcoin and Nasdaq Coupling](01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/) | BTC-QQQ correlation-based 6 regime trading |

---

## Tools

Three AI trading tools developed in-house.

| # | Name | Description | Validation |
|---|---|---|---|
| 1 | [Harness Quant v2](Harness%20quant%20v2%20readme%20.MD) | LLM-based NASDAQ/S&P500 analysis. 6 scenarios + backtest + MCP + multi-agent debate | - |
| 2 | [Earnings Momentum Agent](Harness%20quantv2/Earnings%20momentum%20agent%20readme%20.MD) | Earnings surprise Top 30 recommendation pipeline | 24-month backtest hit rate 83.3% (backtest only) |
| 3 | [Nasdaq-BTC Coupling Bot](01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/) | Real-time BTC-QQQ 30-day rolling correlation tracking + regime classification + signal generation | Python 547 lines |

Tool documentation is currently in Korean. Code, comments, and class/function names are in English. Read each tool's "Known Limitations" section before any live trading.

---

## Research / Papers

Quantitative analysis based on data and statistics. All analyses are reproducible from public CSVs.

| Topic | Location | Data Scale |
|---|---|---|
| AI supply chain Bayesian analysis | [Awesome claude quant scripts/AI supply chain bayesian analysis/](01.Trading%20Strategy/Awesome%20claude%20quant%20scripts/) | Bayesian inference model |
| AMC disclosure timing empirical study | [AfterMarketClose/](AfterMarketClose/) | 34 8-K disclosures + next-day returns |
| DAT mNAV cycle analysis | [mNAV(...) arbitrage/](mNAV(Market-to-Net-Asset-Value)%20arbitrage/) | 12 cycles + 15 companies |
| Luxury sector backtest | [Luxury investment strategy/](01.Trading%20Strategy/Luxury%20investment%20strategy/) | 225 backtests + 3 strategies compared |
| BTC-Nasdaq coupling analysis | [Investment Strategy ... Coupling/](01.Trading%20Strategy/Investment%20Strategy%20Based%20on%20Bitcoin%20and%20Nasdaq%20Coupling/) | 26 quarters + 31 events + 6 regimes |
| Earnings momentum backtest | [Harness quantv2/](Harness%20quantv2/) | 24 months, 768 decisions |

---

## Datasets

CSV datasets published for research and validation. Analyzable immediately with Python pandas. Column headers are in English.

| Category | File | Description |
|---|---|---|
| Disclosure timing | `disclosure_timing_cases.csv` | 34 AMC disclosures + next-day returns |
| DAT companies | `dat_companies_2026.csv` | 15 DAT company status |
| DAT companies | `dat_vs_benchmark_performance.csv` | Half-year return comparison |
| DAT companies | `mnav_cycles_arbitrage_signals.csv` | mNAV cycles + trade signals |
| Luxury sector | `luxury_companies_etfs_2026.csv` | 13 luxury companies/ETFs |
| Luxury sector | `luxury_performance_2020_2026.csv` | Half-year returns |
| Luxury sector | `luxury_backtest_3strategies.csv` | 225 backtest log entries |
| Luxury sector | `luxury_portfolio_by_risk.csv` | Risk-tier portfolios |
| Coupling | `btc_qqq_correlation_2020_2026.csv` | 26 quarters of correlation |
| Coupling | `btc_nasdaq_event_log.csv` | 31 event impacts |
| Coupling | `intraday_coupling_samples.csv` | 4 intraday sessions |
| Coupling | `correlation_regimes_signals.csv` | 6 regime classification |
| Earnings momentum | `backtest_log_24months.csv` | 768 decision logs |

Each CSV is located in its corresponding column or strategy folder.

---

## Curation

Awesome series — AI investment tools evaluated by category — has been moved to a separate file.

→ [AWESOME.md](AWESOME.md)

Categories covered:
- Stocks & Equities (30+ NASDAQ/S&P500 AI tools)
- Crypto & DeFi (LLM trading bots + benchmarks)
- AI Quant Prompt `[KR]`
- Vibe Trading Bot `[KR]`

---

## Directory Structure

```
vibe-investing/
├── README.md                              Korean main
├── README_EN.md                           This file
├── AWESOME.md                             Curation index
│
├── 01.Trading Strategy/                   Trading strategies
│   ├── README.md
│   ├── Awesome claude quant scripts/      Claude-based 4 strategies + Sample
│   ├── Luxury investment strategy/        Luxury sector + 4 CSVs
│   └── Investment Strategy Based on Bitcoin and Nasdaq Coupling/
│
├── 02.Investment Idea Column/             Column index
│   └── README.md
│
├── AfterMarketClose/                      AMC column + CSV
├── mNAV(...)/                             DAT mNAV column + 3 CSVs
├── Harness quantv2/                       Earnings Momentum Agent
│
├── Vibe Investing Risk Management.MD      LTCM column
├── Microsoft fintool acquisition column.MD Fintool column
├── Crypto perp manipulation column.MD     Crypto perp column
├── Harness quant v2 readme .MD            Harness Quant v2 tool
│
├── Awesome vibe invest.MD                 Curation 1
├── Awesome vibe invest crypto.MD          Curation 2
├── Awesome AI Quant Prompt ...kr.MD       Curation 3
└── Awesome Vibe Trading Bot.MD            Curation 4
```

---

## About

**Dennis Kim (HoKwang Kim)**

Cyworld CEO, CEO of BetaLabs Inc., Web3 Investor

Working in the blockchain market since 2017, with a long-running role as a bridge between the Korean and Chinese blockchain ecosystems. The work of cross-validating patterns observed in one market against the other is woven into the analytical stance of this repository.

- Email: gameworker@gmail.com
- GitHub: [@gameworkerkim](https://github.com/gameworkerkim)

---

## Disclaimer

All content is for research and educational purposes only.

- No tool guarantees returns
- Backtest results are based on idealized scenarios; live trading returns will differ (slippage, commissions, taxes, latency)
- Self-managed assets are fine; managing third-party funds requires a license
- Market structure analysis columns are statistical/academic commentary and do not name specific actors
- Short-selling, inverse ETFs, and leveraged products can be catastrophic for individuals
- The user is solely responsible for investment outcomes and legal risks

For detailed risk disclosures, see the "Known Limitations" section of each column/tool.

---

## License

MIT License. Free to use, modify, and distribute.

When citing columns, please attribute "Dennis Kim / vibe-investing".

---

## Contributing

- Issues and PRs are welcome
- Counterpoints to evaluations, missing repo suggestions, and backtest results all welcome
- English translation contributions especially welcome
