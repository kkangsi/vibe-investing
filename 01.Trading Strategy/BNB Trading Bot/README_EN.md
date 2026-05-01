# BNB-ETH Quantitative Analysis & Trading Signal

> **A 4-year statistical study of Binance Coin (BNB) vs Ethereum (ETH), MM/HODLer hypothesis verification, and an ETH-trend-based BNB trading strategy**

[![Korean](https://img.shields.io/badge/Language-한국어-blue)](README.md)
[![English](https://img.shields.io/badge/Language-English-red)](README_EN.md)
[![Chinese](https://img.shields.io/badge/Language-中文-green)](README_CN.md)
[![Data](https://img.shields.io/badge/Data-CoinMetrics-orange)](https://coinmetrics.io/)
[![Period](https://img.shields.io/badge/Period-2022.05~2026.04-yellow)](#)

---

## 📌 Overview

This project **statistically tests** the following hypotheses:

1. Does ETH lead BNB in price movements?
2. When BNB follows ETH trend reversals, are the response speeds asymmetric between rallies and drops?
3. Have BNB-holder reward programs (e.g. Binance HODLer Airdrops) altered BNB's price structure?
4. Do projects airdropped on BNB Chain move independently of BNB itself?
5. Does the resulting structure benefit **only BNB holders**?

To answer these questions, we run a quantitative analysis on 4 years (1,460 trading days) of daily price data and ship a results-driven trading signal program.

---

## 🎯 Key Findings (TL;DR)

| Metric | Value | Interpretation |
|---|---|---|
| BNB-ETH Pearson correlation | **0.7283** | Very strong contemporaneous co-movement |
| Optimal lead-lag | lag = 0 | No daily lead-lag relationship |
| Granger causality (ETH→BNB, lag 1) | p = 0.2546 | Not significant on daily data |
| ETH golden cross → BNB follow | median **6 days** | Rallies are followed quickly |
| ETH death cross → BNB follow | median **11 days** | Drops are followed 1.8× slower |
| % of ETH-down days where BNB drops less | **68.7%** | Strong evidence of downside protection |
| BNB's ETH beta — pre-HODLer era | 0.643 | — |
| BNB's ETH beta — post-HODLer era | **0.534** | **-16.9% drop (decoupling)** |

**Most important finding**: After Binance HODLer Airdrops launched in earnest, **the correlation stayed flat but beta dropped significantly**. BNB still moves in the same direction as ETH, but no longer with the same magnitude — a quantitative footprint of the user's hypothesis: "MM/foundation USDT-buying defense" of BNB price.

---

## ✅ Hypothesis Verification

| # | Hypothesis | Result | Statistical Evidence |
|---|---|---|---|
| 1 | ETH leads BNB | △ Partial | Not visible daily; visible only at trend timescale |
| 2 | BNB follows trend transitions (slowly) | ○ Confirmed | 11-day vs 6-day asymmetry |
| 3 | BNB drops less than ETH on down days | ◎ **Strong** | 68.7% of ETH-down days show BNB declining less |
| 4 | Decoupling progressed post-HODLer | ◎ **Confirmed** | BNB's ETH beta 0.643 → 0.534 (-16.9%) |
| 5 | BNB & BNB-Chain airdrop tokens are independent | ○ Qualitative | NIGHT, BREV, ALLO, etc. dropped immediately post-airdrop |
| 6 | Only BNB holders benefit structurally | ○ Confirmed | Beta drop + airdrop token decline observed simultaneously |

**Legend**: ◎ Strongly confirmed · ○ Confirmed · △ Partial · × Not confirmed

---

## 📊 Window-Based Cumulative Returns (as of 2026-04-30)

| Window | BNB | ETH | BTC |
|---|---|---|---|
| 24h | -0.38% | +0.11% | +0.67% |
| 72h | -1.78% | -1.80% | -1.24% |
| 7d | -3.69% | -3.17% | -2.47% |
| 30d | -0.25% | +7.38% | +11.85% |
| 90d | -28.22% | -16.41% | -9.19% |
| 180d | -43.81% | -41.72% | -30.64% |
| 365d | +2.51% | +25.70% | -19.03% |
| **3y** | **+87.08%** | **+23.19%** | **+171.38%** |

> Despite recent underperformance, BNB outperforms ETH over a 3-year horizon — interpretable as the effect of its own yield cycle (airdrops/staking).

---

## 🔬 Trading Strategy & Backtest

### Strategy Definition

```
ENTRY (LONG BNB):  ETH 20-day MA > 50-day MA  (golden cross)
EXIT (CASH):        ETH 20-day MA < 50-day MA  (death cross)
Execution:          Enter/exit at next-day close (T+1)
Transaction cost:   0.10% per trade (0.20% round-trip)
```

### Backtest Results (2022-05 ~ 2026-04, 1,461 days)

| Strategy | Total Return | CAGR | Sharpe | Max DD | Volatility |
|---|---|---|---|---|---|
| ETH MA Cross → BNB | **+123.21%** | 23.07% | 0.738 | -38.44% | 37.77% |
| BNB Buy & Hold | +211.85% | 34.18% | 0.818 | -55.49% | 53.24% |
| ETH Buy & Hold | +127.30% | 23.65% | 0.649 | -63.88% | 67.88% |

- BNB Buy & Hold wins on absolute return
- The strategy wins on **volatility, MDD, and Sharpe (vs ETH B&H)**
- 47.9% time in market (~half in cash), 14 round-trip trades over 4 years

### Current Signal (2026-04-30)

```
🟢 LONG BNB
ETH trend     : UPTREND (MA20=$2,318 > MA50=$2,203)
BNB price     : $614.98
Entry date    : 2026-03-20 @ $642.11
Current P&L   : -4.23%
Days held     : 42 days
```

---

## 🚀 Usage

### Install dependencies

```bash
pip install pandas numpy yfinance ccxt scipy statsmodels
```

### Run signal program

```bash
# Print current signal
python bnb_signal.py

# Run backtest + save CSVs
python bnb_signal.py --backtest

# Save signal history CSV only
python bnb_signal.py --csv-only

# Customize MA parameters
python bnb_signal.py --ma-short 10 --ma-long 30 --backtest

# Adjust data window
python bnb_signal.py --days 730 --backtest
```

### Automatic Data Source Fallback

The program tries data sources in this order:

1. **yfinance** (Yahoo Finance, BNB-USD/ETH-USD)
2. **ccxt + Binance** (BNBUSDT/ETHUSDT spot)
3. **CoinGecko REST API** (limited to 365 days on free tier)

---

## 📂 File Manifest

| File | Description |
|---|---|
| `BNB_ETH_분석보고서.docx` | Comprehensive analysis report (Korean DOCX) |
| `bnb_signal.py` | Standalone trading signal program |
| `00_summary.json` | Key statistics summary |
| `01_prices.csv` | BNB/ETH/BTC daily prices (4 years) |
| `02_returns.csv` | Daily log returns |
| `03_window_returns.csv` | Cumulative returns by window |
| `04_yearly_correlation.csv` | Year-over-year BNB-ETH correlation |
| `05_rolling_corr_30d.csv` | 30-day rolling correlation series |
| `06_lead_lag.csv` | ±7-day cross-correlation |
| `07_granger_eth_to_bnb.csv` | Granger causality test results |
| `08_trend_transition_delays.csv` | BNB follow-up days per ETH trend transition |
| `09_backtest_metrics.csv` | Backtest performance metrics |
| `10_individual_trades.csv` | Individual trade log (15 trades) |
| `11_backtest_daily.csv` | Daily backtest (positions, equity curves) |
| `12_current_signal.json` | Current live signal state |

---

## 🧠 Methodology

### Data Processing
- Daily log returns from close prices
- Aligned across 4 years (1,460 trading days)
- Missing values dropped

### Statistical Tests
- **Pearson / Spearman** correlation, with 30-day / 90-day rolling
- **±7-day cross-correlation** for lead-lag analysis
- **Granger causality** (5 lags, F-test)
- **Trend transitions** based on MA(20/50) golden/death cross
- **Asymmetric beta** via OLS regressions split by ETH return sign
- **z-test** for beta-difference significance

### Backtesting
- Look-ahead bias prevention (T+1 entry)
- Transaction cost: 0.10% per trade
- Cumulative equity curves, MDD, Sharpe Ratio computed

---

## ⚠️ Limitations & Disclaimers

- **Sample size**: 4 years / 1,460 days / 14 round-trip trades — small sample
- **MA parameters**: Standard (20, 50); not optimized to avoid overfitting
- **Decoupling underway**: ETH signal validity may decay as decoupling progresses
- **Regulatory risk**: Binance/BNB are directly exposed to global regulatory shifts
- **This is not investment advice** — it's a quantitative academic analysis

---

## 📚 References

- [CoinMetrics Reference Rate Methodology](https://coinmetrics.io/reference-rates/)
- [Binance HODLer Airdrops Program](https://www.binance.com/en/airdrop)
- [Binance Megadrop](https://www.binance.com/en/megadrop)
- BNB Chain Ecosystem Report (Binance Research, 2025)

---

## 📜 License & Citation

Free for academic and research use. Please cite as:

```
Kim, D. (2026). BNB-ETH Quantitative Analysis and Trading Signal.
Betalabs Inc. https://github.com/gameworkerkim
```

---

**Author**: Dennis Kim (김호광), CEO, Betalabs Inc.  
**Contact**: gameworker@gmail.com  
**GitHub**: [github.com/gameworkerkim](https://github.com/gameworkerkim)
