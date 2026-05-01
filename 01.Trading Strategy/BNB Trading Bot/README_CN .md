# BNB-ETH 量化分析与交易信号

> **Binance Coin (BNB) 与 Ethereum (ETH) 四年期统计分析、做市商/HODLer 假设的实证检验，以及基于 ETH 趋势的 BNB 交易策略**

[![Korean](https://img.shields.io/badge/Language-한국어-blue)](README.md)
[![English](https://img.shields.io/badge/Language-English-red)](README_EN.md)
[![Chinese](https://img.shields.io/badge/Language-中文-green)](README_CN.md)
[![Data](https://img.shields.io/badge/Data-CoinMetrics-orange)](https://coinmetrics.io/)
[![Period](https://img.shields.io/badge/Period-2022.05~2026.04-yellow)](#)

---

## 📌 项目概述

本项目对以下核心假设进行**统计学验证**：

1. ETH 在价格走势上是否领先 BNB？
2. BNB 在跟随 ETH 趋势反转时，上涨与下跌的反应速度是否对称？
3. 类似 Binance HODLer Airdrops 的 BNB 持有人激励项目是否改变了 BNB 的价格结构？
4. 在 BNB Chain 上空投上线的项目是否独立于 BNB 价格运行？
5. 由此形成的结构是否**仅惠及 BNB 持有人**？

为回答上述问题，我们对四年期（1,460 个交易日）的日级价格数据进行量化分析，并提供基于研究结果的交易信号程序。

---

## 🎯 核心结论 (TL;DR)

| 指标 | 数值 | 解读 |
|---|---|---|
| BNB-ETH Pearson 相关系数 | **0.7283** | 同期联动极强 |
| 最优领先-滞后 (lead-lag) | lag = 0 | 日级数据无领先关系 |
| Granger 因果检验 (ETH→BNB, lag1) | p = 0.2546 | 日级因果关系不显著 |
| ETH 金叉 → BNB 跟随 | 中位数 **6 天** | 上涨跟随快 |
| ETH 死叉 → BNB 跟随 | 中位数 **11 天** | 下跌跟随慢 1.8 倍 |
| ETH 下跌日中 BNB 跌幅更小的占比 | **68.7%** | 下行保护的强证据 |
| HODLer 之前 BNB 对 ETH 的 Beta | 0.643 | — |
| HODLer 之后 BNB 对 ETH 的 Beta | **0.534** | **下降 16.9%（脱钩）** |

**最重要的发现**：在 Binance HODLer Airdrops 全面推行之后，**相关系数几乎不变，但 Beta 显著下降**。即 BNB 仍与 ETH 同方向移动，但波动幅度不再相同 —— 这是用户假设（"做市商/项目方使用 USDT 对 BNB 价格进行护盘"）的量化痕迹。

---

## ✅ 用户假设验证结果

| # | 假设 | 结果 | 统计证据 |
|---|---|---|---|
| 1 | ETH 领先 BNB | △ 部分符合 | 日级未观测到，仅在趋势级别可见 |
| 2 | BNB 跟随趋势反转（缓慢） | ○ 符合 | 下跌 11 天 vs 上涨 6 天 |
| 3 | 下跌时 BNB 跌幅小于 ETH | ◎ **强烈符合** | 68.7% 的 ETH 下跌日中 BNB 跌幅更小 |
| 4 | HODLer 之后脱钩进展 | ◎ **符合** | BNB 对 ETH 的 Beta 0.643 → 0.534 (-16.9%) |
| 5 | BNB 与 BNB Chain 上市币价格无关 | ○ 定性符合 | NIGHT、BREV、ALLO 等空投后立即遭抛压 |
| 6 | 仅 BNB 持有人结构性受益 | ○ 符合 | Beta 下降与空投币下跌同时观测 |

**图例**：◎ 强烈符合 · ○ 符合 · △ 部分符合 · × 不符合

---

## 📊 各窗口累计收益率（截至 2026-04-30）

| 时间窗 | BNB | ETH | BTC |
|---|---|---|---|
| 24 小时 | -0.38% | +0.11% | +0.67% |
| 72 小时 | -1.78% | -1.80% | -1.24% |
| 7 天 | -3.69% | -3.17% | -2.47% |
| 30 天 | -0.25% | +7.38% | +11.85% |
| 90 天 | -28.22% | -16.41% | -9.19% |
| 180 天 | -43.81% | -41.72% | -30.64% |
| 365 天 | +2.51% | +25.70% | -19.03% |
| **3 年** | **+87.08%** | **+23.19%** | **+171.38%** |

> 短期 BNB 表现疲软，但 3 年累计跑赢 ETH —— 可解读为其自身收益循环（空投/质押）效应。

---

## 🔬 交易策略与回测

### 策略定义

```
入场 (LONG BNB):  ETH 20 日均线 > 50 日均线  (金叉)
出场 (CASH):       ETH 20 日均线 < 50 日均线  (死叉)
执行规则:          信号产生后次日收盘成交 (T+1)
交易成本:          每笔 0.10% (双边 0.20%)
```

### 回测结果（2022-05 ~ 2026-04，共 1,461 日）

| 策略 | 总收益 | CAGR | Sharpe | 最大回撤 | 年化波动率 |
|---|---|---|---|---|---|
| ETH MA 信号 → BNB | **+123.21%** | 23.07% | 0.738 | -38.44% | 37.77% |
| BNB 持有不动 | +211.85% | 34.18% | 0.818 | -55.49% | 53.24% |
| ETH 持有不动 | +127.30% | 23.65% | 0.649 | -63.88% | 67.88% |

- 绝对收益：BNB 持有不动最高
- **波动率/MDD/Sharpe（对比 ETH 持有）**：策略胜出
- 持仓时间占比 47.9%（约一半时间持现），4 年共 14 对完整交易

### 当前信号（2026-04-30）

```
🟢 当前持有 BNB 多头
ETH 趋势     : UPTREND (MA20=$2,318 > MA50=$2,203)
BNB 价格     : $614.98
入场日期     : 2026-03-20 @ $642.11
当前盈亏     : -4.23%
持仓天数     : 42 天
```

---

## 🚀 使用方法

### 安装依赖

```bash
pip install pandas numpy yfinance ccxt scipy statsmodels
```

### 运行信号程序

```bash
# 输出当前信号
python bnb_signal.py

# 执行回测并保存 CSV
python bnb_signal.py --backtest

# 仅保存信号历史 CSV
python bnb_signal.py --csv-only

# 自定义均线参数
python bnb_signal.py --ma-short 10 --ma-long 30 --backtest

# 调整数据时间窗
python bnb_signal.py --days 730 --backtest
```

### 数据源自动 Fallback

程序按以下顺序尝试数据源：

1. **yfinance**（Yahoo Finance, BNB-USD/ETH-USD）
2. **ccxt + Binance**（BNBUSDT/ETHUSDT 现货）
3. **CoinGecko REST API**（免费版限定 365 天）

---

## 📂 产物文件清单

| 文件 | 内容 |
|---|---|
| `BNB_ETH_분석보고서.docx` | 综合分析报告（韩文 DOCX） |
| `bnb_signal.py` | 独立运行的交易信号程序 |
| `00_summary.json` | 核心统计摘要 |
| `01_prices.csv` | BNB/ETH/BTC 日价格（4 年） |
| `02_returns.csv` | 日级对数收益率 |
| `03_window_returns.csv` | 各窗口累计收益率 |
| `04_yearly_correlation.csv` | 年度 BNB-ETH 相关系数 |
| `05_rolling_corr_30d.csv` | 30 日滚动相关系数序列 |
| `06_lead_lag.csv` | ±7 日交叉相关 |
| `07_granger_eth_to_bnb.csv` | Granger 因果检验结果 |
| `08_trend_transition_delays.csv` | 趋势转换时 BNB 跟随天数 |
| `09_backtest_metrics.csv` | 回测绩效指标 |
| `10_individual_trades.csv` | 单笔交易记录（15 笔） |
| `11_backtest_daily.csv` | 日级回测（持仓、净值曲线） |
| `12_current_signal.json` | 当前信号状态 |

---

## 🧠 分析方法

### 数据处理
- 收盘价对数收益率
- 4 年期（1,460 个交易日）对齐
- 缺失值剔除

### 统计检验
- **Pearson / Spearman** 相关系数及 30/90 日滚动相关
- **±7 日交叉相关** 进行领先-滞后分析
- **Granger 因果检验**（5 个滞后阶，F 检验）
- **趋势转换** 基于 MA(20/50) 金叉/死叉
- **非对称 Beta** 通过 OLS，按 ETH 收益率符号拆分回归
- **z 检验** 检验 Beta 差异显著性

### 回测
- 防止前视偏差（T+1 入场）
- 交易成本：每笔 0.10%
- 计算累计净值曲线、最大回撤、Sharpe 比率

---

## ⚠️ 局限与免责

- **样本量**：4 年 / 1,460 日 / 14 笔完整交易 —— 样本较小
- **均线参数**：使用标准 (20, 50)，未做优化以避免过拟合
- **脱钩进行中**：随时间推移 ETH 信号有效性可能减弱
- **监管风险**：币安/BNB 直接暴露于全球监管变化
- **本资料不构成投资建议** —— 仅为学术性量化分析整理

---

## 📚 参考资料

- [CoinMetrics 参考利率方法论](https://coinmetrics.io/reference-rates/)
- [Binance HODLer Airdrops 项目](https://www.binance.com/en/airdrop)
- [Binance Megadrop](https://www.binance.com/en/megadrop)
- BNB Chain 生态分析报告（Binance Research, 2025）

---

## 📜 许可与引用

可自由用于学术和研究目的，引用格式：

```
Kim, D. (2026). BNB-ETH 量化分析与交易信号.
Betalabs Inc. https://github.com/gameworkerkim
```

---

**作者**：Dennis Kim（金昊光），CEO, Betalabs Inc.  
**联系**：gameworker@gmail.com  
**GitHub**：[github.com/gameworkerkim](https://github.com/gameworkerkim)
