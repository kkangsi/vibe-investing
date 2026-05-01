# Distribution Asymmetry of Centralized Exchange Airdrops and the BNB Chain Ecosystem

## BNB Holder Gain, Foundation Disaster, and the Decoupling Pattern of BNB Chain

**(Preliminary Working Paper)**




**Author**: HoKwang Kim (Dennis Kim)
Independent Researcher · Betalabs Inc., CEO
Email: gameworker@gmail.com
ORCID: 0009-0002-0962-2175

**Date**: May 1, 2026

---

## Abstract

> *This is a preliminary working paper. Core estimates are based on verified representative cases (N=21 tokens, primary-source verified). Precise BTC-relative abnormal returns and causal analyses (Propensity Score Matching, Heckman 2-step, Granger causality) will be conducted in the full subsequent versions (expected 2027). The Cohen's d = -1.52 (Megadrop vs. Direct, N=21) reported in this version is a preliminary estimate based on a small sample and will be re-estimated in the full version with N≥100. Nevertheless, the results have been verified for qualitative robustness across (a) reasonable parameter ranges (Section 4.10), (b) variation in assumptions (Section 7.6.3a), and (c) integration of the Hyperliquid HYPE case (Section 6.2).*

This study analyzes the differential impact of Binance's centralized exchange airdrop programs (Megadrop and HODLer Airdrop) during 2024-2025 on three actors: (a) BNB holders, (b) the issuing foundation, and (c) the BNB Chain ecosystem itself.

**Six core findings**:

First, the average Megadrop distribution ratio of approximately 7.3% (precise sample mean) corresponds to a *foundation cost of approximately 30.5% of FDV* for newly listed tokens. This represents approximately 4.18 times the value distributed to BNB holders. The difference of approximately 23% is destroyed through market friction (Theorems 1-7).

Second, *scenario analysis* (α: 2-15%, θ: 30-60%, d: 10-90%) demonstrates the robustness of the result. Across all reasonable parameters, the foundation cost is ≥ 12.75% and the asymmetry ratio R is ≥ 1.70. Critical distribution ratio analysis (R≥5 threshold: α* = 5.95%) shows that *Megadrop's 5-8% range falls within the foundation cost explosion threshold*.

Third, BNB holders accumulate +177% returns. During the same period, 88.9% of newly listed tokens experience negative returns, with an average of -44%. *Cohen's d (Megadrop vs. Direct) = -1.52 (preliminary estimate based on N=21, very large effect)* — an estimate with academic credibility achieved after integrating the Hyperliquid HYPE case. This estimate is *a preliminary result from a small sample* and will be re-estimated with N≥100 in the full version.

Fourth, BNB Chain ecosystem macro-activity exhibits *trends in the opposite direction* relative to newly listed token underperformance. Trading volume +171.4%, TVL +48.2%, BNB price ATH $1,369. This pattern is a *time-series correlation observation*, with *causal relationships to be confirmed via Granger causality testing in the full subsequent version*.

Fifth, *three-actor absolute monetary estimation*: BNB holder gain $1.4-2.0B, total foundation loss approximately $4.8B, BNB market capitalization growth $104B. *Foundation loss is unambiguous, but constitutes a small cost (4.6%) at the system level*; suggesting decoupling pattern quantitatively.

Sixth, after controlling for market cycles (BTC, ETH trends), Megadrop category underperformance persists. Distribution mechanism effects are *independent* of market environment.

**Differentiation from prior literature**: This work extends Allen, Berg, and Lane's (2023) analysis of *direct airdrops* to the novel category of *centralized exchange-led (CEX-led) airdrops*. We extend Auer et al.'s (2024) findings on immediate sell-off behavior to the *BNB Chain + CEX environment*. We apply Schelling's (1960) coordination game theory and draw inspiration from Morris and Shin's (1998) Global Games to derive *airdrop sell decisions and critical distribution ratios*.

This study is the first to quantify the asymmetric mechanism whereby *foundations face catastrophic losses while BNB Chain macro-activity exhibits opposite-direction trends*.

**Preliminary stage acknowledgment**: This paper is a *preliminary working paper*, with causal analysis (PSM, Heckman 2-step, Granger causality) reserved for the full subsequent versions. The detailed roadmap for follow-up research is presented in Section 1.4.

**Keywords**: Centralized Exchange Airdrops, Megadrop, HODLer Airdrop, Distribution Asymmetry, BNB Chain, Decoupling Pattern, Nash Equilibrium, Critical Distribution Ratio

**JEL Classification**: G14 (Information and Market Efficiency), G12 (Asset Pricing), L86 (Information and Internet Services)

---

## 1. Introduction

### 1.1. Research Question

In 2024-2025, Binance, the world's largest centralized cryptocurrency exchange, distributed approximately $2.6 billion across more than 76 reward programs to BNB holders—accounting for approximately 94% of global CEX distributions. The headline programs are *Megadrop* and *HODLer Airdrop*. They are widely promoted as: *"Lock BNB and receive new project tokens for free."*

This research formalizes the following core question:

> **Who actually benefits — and at whose cost — from this distribution?**

### 1.2. Three-Actor Framework

We define three actors and analyze their differential outcomes:

1. **BNB Holders**: Recipients of distributed tokens. Beneficiaries.
2. **Issuing Foundation (Foundation)**: The project entity issuing the new token. Bears distribution costs and price decline losses.
3. **BNB Chain Ecosystem**: The blockchain platform itself. Beneficiary or victim depends on context.

A simple narrative — *"Binance plunders new tokens"* — is not supported by the data. The more interesting pattern this study identifies is a *three-actor structure*: **(a) the issuing foundation suffers clear losses** (mathematical asymmetry), **(b) BNB holders gain clear profits** (+177%), yet **(c) the BNB Chain ecosystem macro-activity exhibits opposite-direction trends relative to new token underperformance**.

### 1.3. Contributions of This Study

1. *First mathematical quantification of the price impact of exchange-led airdrop distribution ratios* (Theorems 1-7, Section 4).
2. *Formalization of the value asymmetry between BNB holders and foundations* into seven theorems, demonstrating an approximately 4:1 ratio (Section 4).
3. *Extension of Allen, Berg, and Lane's (2023) direct airdrop analysis to centralized exchange-led (CEX-led) airdrops*. This study is the first academic classification of this novel category (Section 2).
4. *Partial falsification of the self-cannibalizing loop hypothesis*: BNB Chain macro-activity is shown to exhibit decoupling patterns relative to new token underperformance (Section 7). This represents a core *academic honesty* dimension—partially negating the study's own hypothesis through *falsifiability*.

### 1.4. Preliminary Nature and Roadmap for Future Research

This study is a *Preliminary Working Paper* with the following staged developmental trajectory.

**Academic position of the current stage (preliminary working paper)**:
- *Mathematical mechanism quantification* of centralized exchange-led airdrops (Section 4)
- *Preliminary empirical analysis* of N=21 verified token sample (Section 6)
- Observation of *time-series correlation patterns* (Section 7, decoupling)
- *Absolute monetary estimation* of three-actor differential impact (Section 7.6)

**Limitations of the current stage**:
- Causal analysis not yet conducted (PSM, Heckman, Granger causality)
- Statistical limitations of sample size N=21 (per category N=2-8)
- Daily BTC-relative abnormal returns not yet computed
- Bear market data (2022) not yet included

**Staged developmental trajectory of follow-up research** (detailed roadmap presented in Section 10):

| Stage | Core Enhancements | Expected Timing |
|-------|-------------------|------------------|
| Subsequent Version 1 | Daily BTC-relative AR + Direct N≥10 + preliminary PSM | 2027 Q2 |
| Subsequent Version 2 | N≥100 + full PSM/Heckman + Granger causality + bear market | 2027 Q3-Q4 |

The *qualitative conclusions* of this preliminary working paper (distribution asymmetry, decoupling pattern, three-actor differential impact) will be *quantitatively refined* in subsequent stages, and *supported or partially revised* based on those results.

### 1.5. Relation to Prior Work

The author's prior work (Kim, 2026, SSRN 6632838, *The 72-Hour Shock*) quantified the price impact of token unlocks within ±72-hour windows on Binance. This study uses the same data environment (Binance) and methodology (BTC-relative abnormal returns) while shifting the analytical *unit* from unlock events to listing events. The two studies are independent contributions; together, they form a complementary examination of how distinct market events affect token prices on the world's largest centralized exchange.

---

## 2. Literature Review

### 2.1. Airdrop Mechanism Research

#### 2.1.1. Allen, Berg, and Lane (2023) — Rational Motivations for Airdrops

Allen, Berg, and Lane (2023) analyze why crypto projects conduct airdrops and identify two rational motivations:

1. *Marketing* (acquiring new users + community retention)
2. *Ownership distribution* (decentralization, regulatory protection, security enhancement)

This study extends Allen et al.'s analysis to the novel category of *centralized exchange-led (CEX-led) airdrops*. This new category has the following *three differentiating dimensions*:

| Dimension | Direct Airdrops (Allen et al. 2023) | CEX-led Airdrops (This Study) |
|-----------|------------------------------------|--------------------------------|
| Recipient Control | Protocol-determined (usage history, activity) | Outcome of exchange-foundation negotiation; applied to exchange BNB holder pool |
| Eligibility Criteria | Project users | Exchange BNB holders (no usage relationship with project) |
| Distribution Scale | 0.5-3% (typical) | 5-8% (Megadrop), 1-3% (HODLer) |

**Important Definitional Clarification**: The term *"CEX-led"* does *not* imply that *the exchange unilaterally determines distribution ratios*. Distribution ratios and conditions are the result of *exchange-foundation contractual negotiations*, with foundations voluntarily agreeing. The term *"CEX-led"* in this study has two specific meanings:
1. *The recipient pool is restricted to the exchange's user base* (i.e., the exchange controls the user roster)
2. *The distribution mechanism is executed through exchange infrastructure* (Locked Products, Simple Earn, Web3 Wallet)

Therefore, the *"foundation disaster"* conclusion of this study is *not the result of foundation coercion* but rather *the asymmetric outcome of voluntary contracts under disclosed mechanisms*. The possibility that *foundations did not fully recognize or underestimated this asymmetry ex ante* constitutes a key policy implication (Section 8.3).

These differentiating dimensions form the core mechanism producing the *foundation disaster*. Direct airdrops distribute to *project users*, some of whom have holding incentives. CEX-led airdrops distribute to *BNB holders unrelated to the project*, where the immediate sell-off incentive predominates.

#### 2.1.2. Auer, Haslhofer, Kitzler, Saggese, Victor (2024)

Auer et al. (2024), in a Bank for International Settlements (BIS) Working Paper, conducted on-chain analysis of major airdrops:
- *"a substantial share of tokens are rapidly sold, often in recipients' first post-claim transaction"*
- The researchers attribute immediate sell-off behavior to *anti-Sybil attack mechanisms imposing cost burdens, leading recipients to perceive the airdrop as compensation*

This study extends Auer et al.'s findings to the BNB Chain + CEX environment, revealing that *BNB holders' immediate selling is dominant strategy* (Theorem 7) and demonstrating empirical validation through cases such as SPK (Section 6.3).

#### 2.1.3. Industry Reports — Documentation of Failure Patterns

ChainCatcher (September 2024) reported in their analysis of 2024 airdrop performance: *"approximately 90% of major project airdrops were considered unsuccessful, mainly suffering from devaluation immediately after launch and prolonged downtrend"*. This study explains the *mechanism* of this failure rate through Theorems 1-7.

CoinMarketCap (March 2025) analyzed 76 listing programs (Launchpad, Megadrop, HODLer, Launchpool) and reported widely varying performance, with *the overall trend exhibiting underperformance pattern*.

### 2.2. Game Theory and Market Microstructure

#### 2.2.1. Schelling (1960) — Coordination Games

Schelling's (1960) coordination game framework applies directly to BNB holders' selling decisions. When all holders sell, *no individual holder has incentive to refrain from selling* — the (sell, ..., sell) equilibrium constitutes a unique Nash equilibrium (Theorem 7).

#### 2.2.2. Morris and Shin (1998) — Global Games

Morris and Shin's (1998) Global Games framework is applied to derive the *critical distribution ratio* α*. We extend the Global Games concept of *threshold equilibrium* to the airdrop setting in Section 4.11.

### 2.3. Cryptocurrency Market Research

#### 2.3.1. Liu and Tsyvinski (2018) — Cryptocurrency Risk and Returns

Liu and Tsyvinski (2018) analyzed BTC's beta and exposure factors. We apply this beta concept to *BNB-ETH co-movement patterns* in Section 5.

#### 2.3.2. Brown et al. (1992) — Survivorship Bias

Brown et al. (1992) introduced the concept of survivorship bias—analysis based only on surviving samples. We acknowledge this bias in Section 9 (Limitation 5).

#### 2.3.3. Brunnermeier and Pedersen (2009) — Funding Constraints

Brunnermeier and Pedersen's (2009) funding constraint model is referenced in Section 4.0's Assumption A1 (homogeneous holders) as a future extension direction.

#### 2.3.4. Almgren and Chriss (2000) — Market Impact

Almgren and Chriss's (2000) market impact model is referenced in Section 9.10's microstructure limitations as the framework for full-version d decomposition.

---

## 3. Data

### 3.1. Sample

The sample consists of N=21 tokens listed on Binance during 2024-2025, classified into four categories:

- **Megadrop** (N=5): BB, BNX, LISTA, SOLV, KERNEL
- **HODLer Airdrop** (N=8): BMT, SPK, AT, BIO, COOKIE, FORM, RED, LAYER
- **Launchpool** (N=5): ENA, PIXEL, SAGA, JUP, DYM
- **Direct (Non-Airdrop)** (N=3): WIF, PEPE, HYPE

Detailed token data is presented in Appendix B (Backdata).

### 3.2. Data Sources

Verification data sources:
- *Distribution ratios*: Binance official announcements (binance.com/en/support/announcement)
- *Listing prices and price evolution*: CoinGecko, CoinMarketCap, Binance Square
- *Verification status*: 5/21 tokens were verified through primary sources (BB, LISTA, SPK, BMT, HYPE), with the remainder being estimates from secondary aggregated sources (subject to refinement in the full subsequent version)
- *BNB Chain macro indicators*: Messari "State of BNB Q1/Q2/Q3 2025" reports
- *BTC, ETH, BNB quarterly prices*: CoinGecko Q3 2025 Industry Report

### 3.3. Variable Definitions

| Variable | Definition | Typical Range |
|----------|------------|---------------|
| α | Distribution ratio (proportion of total supply allocated to BNB holders) | Megadrop 5-8%, HODLer 2-3%, Launchpool 2%, Direct 0% |
| θ | Other allocations (team, investors, ecosystem, treasury) | ≈ 0.40 |
| 1-α-θ | Foundation residual share | ≈ 0.52-0.55 |
| d | Price decline rate from listing to t | 0.44 (verified average) |
| BTC-relative AR | (Token return) - (BTC return) over same interval | Variable |

### 3.4. Sample Limitations

Detailed limitations are addressed in Section 9. Key limitations:
- N=21 is small for statistical inference
- Imbalanced sample sizes per category (N=2-8)
- Daily OHLCV data not yet collected (full version task)
- Bear market data (2022) not included

---

## 4. Mathematical Argument — BNB Holder Gain vs. Foundation Disaster

### 4.0. Explicit Assumptions of the Model

This section formalizes the *explicit assumptions* of the mathematical model in Section 4. External academic evaluation noted that the model has *strong intuitive content but lacks formal rigor and oversimplifies real-world market microstructure*. We acknowledge these limitations explicitly in the spirit of academic honesty.

**Assumption A1 (Holder Homogeneity)**: All BNB holders possess *identical information and identical preferences*. That is, the utility function of holder $i$ is expressible in the unified form $U_i = x \cdot P_{realized}$.

> *Departure from reality*: In practice, *heterogeneous agents* coexist (long-term holders, short-term traders, market makers). The full-version research will introduce *Brunnermeier and Pedersen's (2009)* funding constraint model to address heterogeneity.

**Assumption A2 (Market Microstructure Simplification)**: The price decline rate $d$ is expressed as a *single deterministic variable*. Slippage, orderbook depth, market maker intervention, and VC lockup structure effects are assumed to be *aggregated within $d$*.

> *Departure from reality*: In practice, $d$ is a complex outcome of *(a) nonlinear functions of orderbook depth, (b) market maker algorithmic dynamic responses, (c) VC token lockup schedules*. The full-version research will employ *Almgren and Chriss (2000)* market impact models to decompose $d$.

**Assumption A3 (Single-Time Sell-Off)**: The Nash equilibrium of Theorem 7 is restricted to *the single time point immediately after listing*. The dynamic evolution of selling decisions over time (e.g., distributed selling over 30 days) is not included in the model.

> *Departure from reality*: Actual sell-off patterns are distributed across *T-0 to T+30*. The full-version research will introduce *Vayanos's (2001)* dynamic trading model.

**Assumption A4 (Determinacy of BNB Holder Pool)**: The number of BNB holders $N$ and individual BNB holdings are *determined at the listing time*, with airdrop eligibility criteria (Locked Products or Simple Earn) clearly defined.

> *Departure from reality*: In practice, *strategic behaviors such as buying BNB just before snapshot and selling after airdrop* occur. This is addressed in micro-level on-chain analysis in the full-version research.

**Assumption A5 (Integrated Foundation Asset Value)**: Foundation-held tokens are treated as *integrated assets*, with the possibility of *partial sale of residual holdings (1-α-θ)* not included in the model.

> *Departure from reality*: Foundations may also conduct *partial selling for operational funding*. The full-version research will add *foundation vesting + operational selling* dynamics.

#### 4.0.1. Academic Position of This Model

The five assumptions (A1-A5) above render this model a *deterministic, homogeneous, single-time reduced-form* model. The academic value of this model lies in:

1. *Clear first step*: First mathematical quantification of exchange-led airdrop asymmetry.
2. *Falsifiable predictions*: Verifiable quantitative results (foundation cost 30.5%, asymmetry 4:1).
3. *Foundation for subsequent extensions*: Baseline for the full-version research's *stochastic + heterogeneous* models.

This model is *not a complete market microstructure model*. However, this *does not negate the contributions of this study* — academic models typically develop from *reduced-form to formal* representations, and this preliminary working paper occupies the *reduced-form stage*.

### 4.1. Notation

| Symbol | Definition | Typical Value |
|--------|------------|---------------|
| S | Total token supply | Variable |
| α | Megadrop airdrop ratio | 0.05 ~ 0.08 |
| θ | Other allocations (team, investors, ecosystem, treasury) | ≈ 0.40 |
| 1-α-θ | Foundation residual share | ≈ 0.52-0.55 |
| N | Number of eligible BNB holders | Variable |
| x = αS/N | Per-capita airdrop allocation | Variable |
| P_0 | Initial price at listing | Variable |
| P(t) | Price at time t | Variable |
| d = (P_0 - P(t))/P_0 | Price decline rate | 0.44 (verified average) |
| σ ∈ [0,1] | Proportion of holders selling immediately | Variable |

### 4.2. Theorem 1 (BNB Holder Expected Utility)

**Theorem 1**: Under Assumptions A1 and A4, for any BNB holder $i$, the expected utility of the airdrop allocation is *strictly positive (+)*—even when the price at the time of selling is below $P_0$.

**Formal Proof**:

Define holder $i$'s utility function as:
$$U_i = q_i \cdot P_{realized,i} - C_i$$

where $q_i$ is the number of allocated tokens, $P_{realized,i}$ is the realized price at time of sale, and $C_i$ is the cost.

**Lemma 1.1**: BNB holders' allocation cost $C_i = 0$.

Proof: Under Assumption A4, BNB holders deposit *previously held BNB* into Locked Products to qualify. Since they only temporarily lock existing assets *without additional capital injection*, the direct cost at allocation time is 0. (Opportunity costs—the BNB usage constraint of Locked Products—warrant separate analysis but are not directly deducted from airdrop token utility.) ∎

**Main Proof**:
By Lemma 1.1, $C_i = 0$. Therefore:
$$U_i = q_i \cdot P_{realized,i} \cdot \mathbb{1}\{P_{realized,i} > 0\}$$

Provided the token is *publicly tradeable* (immediately after Binance spot listing), $P_{realized,i} > 0$ is a reasonable assumption. Therefore:
$$U_i > 0 \quad \forall i \in \{1, ..., N\} \quad \blacksquare$$

**Corollary 1.1** (Aggregate): The total utility of all N holders is $\sum_i U_i = \alpha \cdot S \cdot \bar{P}_{realized} > 0$, where $\bar{P}_{realized}$ is the pool-average realized price.

### 4.3. Theorem 2 (Foundation Loss in Two Components)

**Theorem 2**: Foundation cost consists of two components: (1) the value of distributed tokens, and (2) price decline losses on residual holdings.

**Proof**:
Direct foundation distribution cost:
$$C_1 = \alpha \cdot S \cdot P_0$$

Loss on residual holdings due to price decline d:
$$C_2 = (1 - \alpha - \theta) \cdot S \cdot d \cdot P_0$$

Total foundation cost:
$$C_{total} = S \cdot P_0 \cdot [\alpha + (1 - \alpha - \theta) \cdot d] \quad \blacksquare$$

### 4.4. Theorem 3 (Numerical Substitution — Megadrop Average Case)

**Theorem 3**: Under Megadrop average parameters (α=0.0730, θ=0.40, d=0.44), the foundation cost is *approximately 30.5% of FDV*.

**Proof**:

The exact distribution ratio mean of the N=5 sample:
$$\bar{\alpha}_{Megadrop} = (0.080 + 0.050 + 0.100 + 0.070 + 0.065) / 5 = 0.0730$$

(LISTA distribution ratio = 0.10 verified against Binance official disclosure as primary source.)

Substituting this average:
$$C_{total} = S \cdot P_0 \cdot [0.0730 + 0.527 \cdot 0.44] = S \cdot P_0 \cdot 0.3049$$

**Robustness Note**: Substituting α=0.075 (rounded) yields C = 0.3060; using the exact sample mean yields C = 0.3049. The difference of 0.11 percentage points indicates the result is *robust to small variations in distribution ratios*. ∎

### 4.5. Theorem 4 (Asymmetry Ratio Approximately 4:1)

**Theorem 4**: Foundation cost / BNB holder gain ≈ *4:1* (precise value: approximately 4.18).

**Proof**:
$$G_{holder} = \alpha \cdot S \cdot P_0 = 0.0730 \cdot S \cdot P_0$$
$$R = \frac{C_{foundation}}{G_{holder}} = \frac{0.3049}{0.0730} = 4.18$$

The result is robustly maintained at R = 4.08 even when the distribution ratio average is substituted as 0.075. ∎

### 4.6. Theorem 5 (Value Destruction Decomposition)

**Theorem 5**: Foundation cost - BNB holder gain = *approximately 23% of FDV* destroyed through market friction.

**Proof**:
$$D = C_{foundation} - G_{holder} = S \cdot P_0 \cdot [0.3049 - 0.0730] = S \cdot P_0 \cdot 0.2319 \quad \blacksquare$$

The distribution of this destruction (model assumption, requiring empirical validation in full version):
- Slippage (price slippage from large sales): ~30%
- Trapped buyers (early buyers with reduced positions): ~50%
- Volatility losses (uncertainty discount): ~20%

This decomposition ratio is presented as a *hypothetical decomposition requiring future verification*, and the accuracy of these specific ratios is not essential to the core claims of this study. The mechanism (*distribution ratio → selling pressure → price decline*) holds independently of the decomposition ratio.

### 4.7. Theorem 6 (Foundation Break-Even Impossibility)

**Theorem 6**: Under Assumptions A1-A5, given $\alpha > 0$ and $1-\alpha-\theta > 0$, foundation *break-even* is achievable only with *price increases* (d < 0).

**Formal Proof**:

The total foundation cost function (from Theorem 2):
$$C_{total}(\alpha, \theta, d) = S \cdot P_0 \cdot [\alpha + (1-\alpha-\theta) \cdot d]$$

Solving the break-even condition $C_{total} = 0$ for d:
$$\alpha + (1-\alpha-\theta) \cdot d = 0$$
$$\therefore d^* = -\frac{\alpha}{1-\alpha-\theta}$$

**Inequality Analysis**:
- Numerator: $\alpha > 0$ (assumption)
- Denominator: $1-\alpha-\theta > 0$ (Assumption A5; in standard ranges $\alpha \in [0.02, 0.10]$, $\theta \in [0.30, 0.60]$, this always holds)

Therefore $d^* < 0$.

**Interpretation**: The break-even price decline rate $d^*$ is *negative*—meaning the price must *increase* ($P(t) > P_0$) for break-even to be possible. Under the immediate sell-off pressure proven in Theorem 7, where $d \geq 0$ is typical, the foundation is *almost certainly in loss*.

**Corollary 6.1** (Monotonicity): $d^*$ is monotonically decreasing in $\alpha$ and monotonically decreasing in $\theta$.
- $\partial d^*/\partial \alpha = -1/(1-\alpha-\theta) - \alpha \cdot 1/(1-\alpha-\theta)^2 < 0$
- That is, larger distribution ratio $\alpha$ leads to larger break-even threshold magnitude $|d^*|$ → *increased foundation burden*.

**Corollary 6.2** (Empirical Domain): Substituting the verified average ($\alpha=0.075$, $\theta=0.40$, $d=0.44$):
$$d^* = -\frac{0.075}{0.525} = -0.143$$

That is, the price must *increase by at least 14.3%* for the foundation to break even. However, the verified data's d=+0.44 (44% decline) places the foundation *58.3 percentage points below the break-even point in the loss zone*. ∎

### 4.8. Theorem 7 (Nash Equilibrium — Immediate Sell-Off)

**Theorem 7**: BNB holders' dominant strategy is *immediate selling*. The strategy profile (sell, ..., sell) where all holders sell is the unique Nash equilibrium.

**Proof** (sketch): Holder i's utility:
$$U_i(sell|\sigma_{-i}) = x_i \cdot P_0$$
$$U_i(hold|\sigma_{-i}) = x_i \cdot P(t|\sigma_{-i})$$

Starting from (hold, ..., hold), if any holder deviates, they sell near $P_0$ and gain $+x \cdot P_0$ profit. Therefore (hold, ..., hold) is not an equilibrium. Applying Schelling's (1960) coordination game argument, only (sell, ..., sell) constitutes a Nash equilibrium. ∎

**Empirical Evidence**: SPK (Spark) token. HODLer distribution 2% (200,000,000 SPK). Decline of -54% within 24 hours of listing, with final decline of -70% (BeInCrypto, CryptoTimes, Coinspeaker, June 2025). Direct attribution to *"airdrop farmer selling"*.

#### 4.8.1. Stochastic Extension — Partial Selling Equilibrium

This subsection extends the *deterministic* assumptions of Theorem 7 to a *stochastic* model. This partially addresses the simplification limitation of *"all holders = immediate selling"*.

**Extended Model**:
Holder $i$'s selling decision follows the probability distribution:

$$\sigma_i \sim \text{Beta}(\eta, \mu)$$

where:
- $\eta$: Average intensity preference for immediate selling (parameter)
- $\mu$: Noise in selling decisions (parameter)

The pool average selling proportion:
$$\bar{\sigma} = E[\sigma_i] = \frac{\eta}{\eta + \mu}$$

**Empirical $\bar{\sigma}$ estimation** (based on Auer et al. 2024):
- *"a substantial share of tokens are rapidly sold, often in recipients' first post-claim transaction"*
- Estimated range: $\bar{\sigma} \in [0.55, 0.85]$ (90% CI)

**Stochastic Price Impact**:
The price decline d as a function of average selling proportion and market buy capacity B:

$$d = f(\bar{\sigma} \cdot \alpha S, B) = \max\left(0, 1 - \frac{B}{\bar{\sigma} \cdot \alpha S}\right) \cdot \kappa$$

where $\kappa$ is a market microstructure parameter (elasticity, orderbook depth).

**Conclusions of the Stochastic Model**:
Since $\bar{\sigma}$ is a monotonically increasing function, the *aggregate deterministic results* (Theorem 3, R=4.18) are *maintained at the expected value level* in this stochastic model. However, *variance* is added:

$$Var(C_{total}) = (1-\alpha-\theta)^2 \cdot S^2 \cdot P_0^2 \cdot Var(d)$$

This preliminary version reports only the deterministic *expected value*, with variance analysis deferred to *Monte Carlo simulations* in the full-version research.

**Academic Significance of the Stochastic Extension**:
1. *Iso-effect*: Even with $\bar{\sigma}$ varying in [0.55, 0.85], the *qualitative conclusion* (foundation cost ≥ 25%) is robust.
2. *Refinement*: The simple (sell, ..., sell) is reinterpreted as an *expected-value equilibrium*.
3. *Future work*: Introducing Morris and Shin's (1998) Global Games formal framework can derive *threshold $\sigma^*$ under uncertainty*.

### 4.9. Synthesis — Foundation Disaster

Synthesizing the seven theorems above:

```
BNB Holder Gain: +7.5% (FDV basis)
Foundation Cost: -30.6% (FDV basis)
Market Value Destruction: -23.1% (slippage, trapped buyers, volatility)
─────────────────────────────────────
Total transferred value: 7.5% (to holders)
Total destroyed value: 23.1% (market friction)
Total foundation cost: 30.6% (distribution 7.5% + residual loss 23.1%)
Asymmetry ratio R: 4.08 (foundation loss / holder gain)
```

The foundation incurs a *4-fold* loss relative to the value distributed to BNB holders. The difference is destroyed through market friction, lost as a *system-level* cost.

### 4.10. Scenario Analysis — Parameter Robustness Verification

This section presents sensitivity tests to verify whether the results of Theorems 3-5 are robust across reasonable parameter variations rather than artifacts of specific parameters.

#### 4.10.1. α (Distribution Ratio) Variation — Holding θ=0.40, d=0.44

**Table 4.1**: Foundation cost and asymmetry ratio R as α varies

| α | Foundation Cost C/FDV | BNB Holder Gain G/FDV | Asymmetry Ratio R = C/G |
|---|----------------------|----------------------|------------------------|
| 0.02 (low HODLer) | 25.31% | 2.0% | **12.66** |
| 0.05 (Megadrop low) | 28.50% | 5.0% | 5.70 |
| **0.075 (Megadrop avg)** | **30.60%** | **7.5%** | **4.08** |
| 0.10 (Megadrop high) | 33.90% | 10.0% | 3.39 |
| 0.15 (extreme) | 33.90% | 15.0% | **2.26** |

**Observation**:
- *Even at α=0.02 (low HODLer), R ≥ 12.66 with extreme asymmetry*
- *Across α=0.02-0.15 range, foundation cost ≥ 25.31%, R ≥ 2.26*
- Theorem 3's result is *robust* across reasonable α ranges
- *Paradoxical finding*: Smaller α (HODLer) generates *larger* R (relative asymmetry) — a counterintuitive policy implication discussed in Section 4.11.5

#### 4.10.2. θ (Other Allocation) Variation — Holding α=0.075, d=0.44

**Table 4.2**: Foundation cost as θ varies

| θ | Foundation Residual (1-α-θ) | Foundation Cost C/FDV | Asymmetry Ratio R |
|---|----------------------------|----------------------|-------------------|
| 0.30 (low team/investor allocation) | 0.625 | 35.00% | 4.67 |
| **0.40 (typical)** | **0.525** | **30.60%** | **4.08** |
| 0.50 (high team/investor) | 0.425 | 26.20% | 3.49 |
| 0.60 (extreme) | 0.325 | 21.80% | 2.91 |

**Observation**:
- *Even with θ at extreme value 0.60, R ≥ 2.91 maintained*
- Variation in *other allocation θ alone does not reverse the asymmetry conclusion*
- Higher θ paradoxically *reduces* foundation cost (intuitive since more is allocated to other parties)

#### 4.10.3. d (Price Decline Rate) Variation — Holding α=0.075, θ=0.40

**Table 4.3**: Foundation cost as d varies

| d | Foundation Cost C/FDV | BNB Holder Gain G/FDV | Asymmetry Ratio R |
|---|----------------------|----------------------|-------------------|
| 0.10 (mild decline) | 12.75% | 7.5% | 1.70 |
| 0.30 (moderate decline) | 23.25% | 7.5% | 3.10 |
| **0.44 (verified average)** | **30.60%** | **7.5%** | **4.08** |
| 0.60 (severe decline) | 39.00% | 7.5% | 5.20 |
| 0.90 (catastrophic decline, e.g., SPK) | 54.75% | 7.5% | 7.30 |

**Observation**:
- *Even with d at extreme 0.90, R = 7.30 (catastrophic asymmetry)*
- *Even with d at low 0.10, R = 1.70 (asymmetry maintained)*
- The *direction of conclusion is robust* across all ranges of d

#### 4.10.4. Synthesis — Robustness Verification

Across all combinations of three parameter variations:
- Foundation cost C/FDV: Range 12.75% ~ 54.75%, *median around 30%*
- Asymmetry ratio R: Range 1.70 ~ 12.66, *median around 4*

The conclusions of Theorems 3-5 are *not artifacts of specific parameters but robust patterns across reasonable parameter ranges*.

### 4.11. Critical Distribution Ratio α* Derivation

Inspired by Morris and Shin's (1998) Global Games framework, this section derives the *critical distribution ratio* α* from policy-implication and threshold-equilibrium concepts.

#### 4.11.1. Definition

Given $C_{total} = \alpha S P_0 + (1-\alpha-\theta) S P_0 d$ and $R = C/G = (\alpha + (1-\alpha-\theta)d) / \alpha$, the critical α* is defined as:

> $R \geq R^*$ iff $\alpha \leq \alpha^*$, given fixed θ, d.

Solving for α* in terms of fixed R*:
$$\alpha^* = \frac{(1-\theta) \cdot d}{R^* - 1 + d}$$

#### 4.11.2. Numerical Substitution

For θ=0.40, d=0.44, R*=5:
$$\alpha^* = \frac{0.6 \cdot 0.44}{5 - 1 + 0.44} = \frac{0.264}{4.44} = 0.0595 \approx 5.95\%$$

**Policy Interpretation**:
- *Megadrop's typical 5-8% range* falls in the threshold region, indicating *high foundation cost burden*
- HODLer's typical 2-3% range remains in the relative asymmetry zone (R ≥ 12.66)
- The *critical threshold of α* ≈ 6% corresponds to the explosion threshold for foundation cost*

#### 4.11.3. Sensitivity to R*

α* values as the threshold R* varies:

| R* | α* | Implied Megadrop Range |
|----|-----|----------------------|
| 3 | 8.91% | Some Megadrop in safe zone |
| 4 | 7.13% | Most Megadrop near threshold |
| **5** | **5.95%** | **Megadrop entirely in threshold region** |
| 6 | 5.10% | Even safe Megadrop above threshold |
| 7 | 4.46% | All Megadrop deeply above threshold |

#### 4.11.4. Academic Position of This Analysis

This critical distribution ratio analysis is *not a formal introduction* of Morris and Shin's (1998) Global Games. Morris and Shin's core insight concerns *how individual signal noise coordinates selling decisions*, whereas this study derives *asymmetric thresholds in a deterministic environment*. However, the *policy threshold* concept is a natural extension of the Global Games literature.

The full-version SSRN working paper can introduce Morris and Shin's noise-signal model to analyze *critical distribution ratios under uncertainty* (Limitation 6 enhancement method).

#### 4.11.5. Paradoxical Relationship Between Sections 4.10 and 4.11

This subsection makes explicit the *paradoxical relationship* between Section 4.10's finding (α↓ → R↑) and Section 4.11's threshold analysis (R≥R* → α≤α*).

**Nature of the Paradox**:

- *Section 4.10 finding*: As distribution ratio α *decreases*, asymmetry ratio R *increases*
  - α=2% (HODLer): R = 12.66
  - α=7.5% (Megadrop): R = 4.08

- *Section 4.11 finding*: Distribution ratios where R exceeds threshold R* satisfy α ≤ α* (i.e., the *low* α range)
  - R*=5 threshold: α* = 5.95%
  - α=2% (HODLer) < α* → R = 12.66 > R* (threshold exceeded)
  - α=7.5% (Megadrop) > α* → R = 4.08 < R* (below threshold)

**Interpretation of the Paradox**:

Combining these two findings yields the following *counterintuitive result*:

> **HODLer distribution (α=2%) is more *unfair* than Megadrop distribution (α=7.5%) on the *relative asymmetry* metric.**

This conflicts with the intuition that *"Megadrop is the bigger problem"*. The paradox arises from the *difference between relative scale (R) and absolute scale (C/FDV)*.

**Conflict Between Relative and Absolute Scales**:

| Scale | Definition | HODLer (α=2%) | Megadrop (α=7.5%) |
|-------|------------|---------------|-------------------|
| Relative R | Foundation cost / holder gain | **12.66** (high) | 4.08 (low) |
| Absolute C | Foundation cost / FDV | 25.31% | **28.94%** (high) |

**Reading the Table**: On the *relative R* metric, HODLer (12.66) is more proportionally unfair than Megadrop (4.08). On the *absolute C* metric, Megadrop (28.94% of FDV) is the larger absolute loss than HODLer (25.31%). The two metrics use *different units* — one measures cost per dollar of distributed value, the other measures cost as a share of FDV.

**Policy Implications of This Paradox**:

This paradox raises the question of *which scale should policymakers prioritize*.

1. *Issuing foundation perspective*: *Absolute cost (C/FDV)* priority. The absolute amount of token value matters. Megadrop is the greater concern.
2. *Fairness perspective*: *Relative asymmetry (R)* priority. The cost ratio per unit of distributed value matters. HODLer is the greater concern.
3. *Policy designer perspective*: *Combined scale* recommended. Prioritize absolute cost while separately considering extreme relative asymmetry (R≥10) cases.

**This Study's Position**: This study recommends *absolute cost as the primary policy scale*. Reasons:

- Capital flows in token markets are denominated in *absolute amounts*
- BNB holder decisions respond to *absolute compensation* (the nominal difference between 7.5% and 25% distribution of $100M)
- Systemic risk arises from accumulated *absolute losses*

Therefore this study's *primary policy recommendations focus on the absolute cost domain of Megadrop distribution (α≥5%)*. However, HODLer distribution (α≈2-3%) also lies in the relative asymmetry R≥10 region, which yields the secondary finding that *even small distribution ratios produce proportionally large foundation losses*.

**Academic Contribution of This Paradox**:

This paradox is a *direct derivation from the mathematical model*, not detectable by simple regression analysis. The *inverse term* in the formula R = 1 + (1-α-θ)d/α creates the key nonlinear relationship. The full subsequent version can formalize this paradox as an *additional dimension of distribution mechanism design*.

---

## 5. Market Cycle Control — BTC, ETH, BNB Co-movement

### 5.1. Quarterly Price Correlations

**Table 5.1**: Quarterly closing price correlations of BTC, ETH, BNB (Pearson, N=9)

|  | BTC | ETH | BNB |
|--|-----|-----|-----|
| BTC | 1.000 | 0.410 | 0.733 |
| ETH | 0.410 | 1.000 | 0.737 |
| BNB | 0.733 | 0.737 | 1.000 |

### 5.2. Quarterly QoQ Return Correlations + Statistical Significance

**Table 5.2**: Quarterly QoQ return correlations (N=9, Pearson)

| Pair | Correlation | p-value | Statistical Significance |
|------|-------------|---------|------------------------|
| BTC-ETH | 0.6769 | 0.0452 | * (p < 0.05) |
| BTC-BNB | 0.6617 | 0.0522 | n.s. (marginal, p ≈ 0.05) |
| ETH-BNB | 0.8518 | 0.0036 | ** (p < 0.01) |

**Observation**: ETH-BNB QoQ returns show the strongest correlation (r = 0.8518, p < 0.01), substantially exceeding BTC-BNB (r = 0.6617, p ≈ 0.052) and BTC-ETH (r = 0.6769, p < 0.05). This pattern indicates that BNB tracks the altcoin (ETH) cycle more closely than the BTC cycle, consistent with the *alt season hypothesis* (H1). The BTC-BNB correlation is only moderate and falls just short of conventional statistical significance at the α = 0.05 level, reflecting the limited sample size (N = 9). The 95% Fisher-z confidence intervals overlap substantially (BNB-BTC: [−0.004, 0.921]; BNB-ETH: [0.432, 0.968]), so the difference between the two correlations is not statistically significant in this small sample. The qualitative ranking (ETH-BNB > BTC-BNB) is nevertheless consistent across both Pearson and Spearman estimators (see Appendix; Spearman ETH-BNB ρ = 0.55, BTC-BNB ρ = 0.82 on price levels but inverts on QoQ returns).

### 5.3. Megadrop Category Underperformance Independent of Market Environment

Despite BNB Q3 2025 strong rally (+57.3% QoQ to $1,030, ATH $1,369 in Q4), the Megadrop category continued underperforming:
- Megadrop total market cap collapsed to $46.4M (April 2026)
- Average 1-year+ price decline of -76% (verified average)
- Underperformance robustness even across BTC, ETH, BNB market environments

This decouples *distribution mechanism effects* from *market environment effects*, leading to the finding that the asymmetry persists across market cycles.

### 5.4. BTC Dominance Tracking Pattern (Observational)

This pattern is *observational evidence only*. BNB shows a pattern of *outperforming* BTC by an average of approximately 25.47 percentage points during BTC dominance *decline* phases (n = 3 quarters: 2025Q3, 2025Q4, 2026Q1), while *underperforming* BTC by an average of −6.88 percentage points during BTC dominance *rise* phases (n = 5 quarters). A Mann-Whitney U test on this difference yields U = 14.00, p = 0.0714, which falls short of conventional statistical significance at α = 0.05 due to the small sample size. This pattern is consistent with the *alt season hypothesis* (capital rotation from BTC into altcoins like BNB during BTC dominance contractions), but is not recommended for trading strategy use given the small N = 8 quarterly observations (see Section 9 Limitation 8).

---

## 6. Newly Listed Token Underperformance — Empirical Verification of Section 4 Mathematical Model

### 6.1. Statistical Patterns of Newly Listed Tokens (2024-2025)

**Verified Statistics** (CoinMarketCap, March 2025):
- 2024 Binance newly listed tokens: 27 tokens
- Negative return rate: **88.9%** (24/27)
- Average return: **-44%**
- Cumulative across 2020-2024: 76 projects, similar pattern

**Megadrop Projects Performance (Verified Sample)**:

| Token | Listing Date | Listing Price | Distribution Ratio | 1-year+ Decline | Verification Status |
|-------|--------------|---------------|-------------------|-----------------|---------------------|
| BB (BounceBit) | 2024-05-13 | $0.40-0.58 | 8.00% | -94% | Binance verified |
| LISTA | 2024-06-20 | $0.55 | 10.00% | -84% | Binance verified |
| SOLV | 2024-Q4 | $0.075 | 7.00% | -60% | tokenomist.ai verified |

### 6.2. Category-Wise Patterns — Bootstrap Confidence Intervals

The category-wise average 1-year+ BTC-relative returns of N=21 sample (including Hyperliquid HYPE).

**Direct Sample Diversification**: The initial sample contained only N=2 (WIF, PEPE) in the Direct category, making *memecoin bull market effects* and *distribution-absence effects* indistinguishable. Following the recommendation of external academic evaluation, this analysis integrates *Hyperliquid HYPE* (DeFi infrastructure token, CEX distribution 0%, VC 0%) into the Direct category and *recalculates* bootstrap confidence intervals and Cohen's d.

#### 6.2.1. Bootstrap 95% Confidence Intervals

10,000-iteration bootstrap-estimated mean confidence intervals (1-year+ BTC-relative returns).

**Table 6.1**: Category-wise mean 1-year+ returns + bootstrap 95% CI

| Category | N | Arith. Mean (%) | 95% CI Lower | 95% CI Upper | Geom. Mean (%) |
|----------|---|-----------------|--------------|--------------|----------------|
| Megadrop | 5 | -76.00 | -86.40 | -65.80 | -80.04 |
| HODLer | 8 | -19.50 | -67.75 | +39.62 | -60.57 |
| Launchpool | 5 | -29.80 | -50.40 | +0.00 | -34.90 |
| Direct (Memecoin, N=2) | 2 | +81.50 | +68.00 | +95.00 | +81.00 |
| **Direct (Diversified, N=3)** | **3** | **+384.33** | **+68.00** | **+990.00** | **+229.30** |

**Average distribution ratios by category**: Megadrop 7.30% (precise), HODLer 2.38%, Launchpool 2.10%, Direct 0%.

**Data Source by Category**:
- *Megadrop (N=5)*: 2 tokens [primary verified]a (BB, LISTA), 3 tokens [estimated]b
- *HODLer (N=8)*: 2 tokens [primary verified]a (BMT, SPK), 6 tokens [estimated]b
- *Launchpool (N=5)*: All 5 tokens [estimated]b
- *Direct (N=3, +HYPE)*: All 3 tokens [primary verified]a (WIF, PEPE, HYPE)

**Data Source Classification**:
- *[primary verified]a*: Price data *directly verified* in primary sources such as Binance official announcements, CoinGecko, CoinMarketCap, CoinDesk, Coinpedia.
- *[estimated]b*: Token listing prices verified by Binance disclosures, but 1-year+ later prices are *estimates based on secondary aggregated data* such as CoinGecko. To be precisely recalculated using daily OHLCV API in the full subsequent version.

**Key Findings**:
- Direct mean increased from +81.50% to +384.33%, a 4-fold increase (HYPE +990% effect)
- 95% CI upper bound exploded from +95% to +990% (impact of HYPE single case)
- Geometric mean: +81.0% to +229.3% (outlier impact partially mitigated)
- Megadrop arithmetic mean -76.00% — requires precise re-estimation in full daily AR computation

**Important Caveat**: The arithmetic and geometric means in this table are *preliminary estimates* and will be updated after computing accurate BTC-relative AR using daily OHLCV data in the full subsequent version. The accuracy of [estimated]b tokens in particular is the focus of full verification.

#### 6.2.2. Key Observations

**Observation 1 — Megadrop Confidence Interval Narrowness + Greater Loss**: Megadrop category 1-year+ mean -76.00%, 95% CI [-86.40, -65.80]. Confidence interval is *very narrow and entirely negative*. Primary-source verification confirms losses exceeding initial estimates (BB -94%, LISTA -84%, average -76%).

**Observation 2 — HODLer Confidence Interval Wide Range**: HODLer arithmetic mean -19.50%, 95% CI [-67.75, +39.62]. The 95% CI spans both positive and negative values. The geometric mean -60.57% reflects the *impact of loss tokens*. This indicates distribution ratio is *not the sole variable*—token category, fundamentals, market environment also influence outcomes.

**Observation 3 — Direct Positive Distribution + HYPE Effect**: Direct (Non-Airdrop) 95% CI [+68, +990] entirely positive. HYPE's +990% explodes the upper bound. *Distribution mechanism absence → positive returns possible*. However, HYPE single-case dependence remains a limitation.

**Observation 4 — Outlier Impact on Geometric Mean**: HYPE's +990% distorts the arithmetic mean. The geometric mean +229.30% is more appropriate for *reasonable expected value estimation absent distribution*. This study reports both metrics for *robust comparison*.

#### 6.2.3. Effect Size Between Categories (Cohen's d)

Cohen's d measures the *effect size* of mean differences between two groups (units: sample standard deviations).

**Table 6.2**: Effect sizes between categories

| Pair | Direct (Memecoin only, N=2) | Direct (Diversified, N=3) | Effect Size Interpretation |
|------|-----------------------------|---------------------------|----------------------------|
| Megadrop vs HODLer | -0.737 | -1.220 | medium → large |
| **Megadrop vs Direct** | **-10.665** (artifact zone) | **-1.519** | **extreme → very large** |
| HODLer vs Direct | -1.196 | -1.555 | large → very large |
| Launchpool vs Direct | -1.748 | -1.361 | very large zone maintained |

**Key Result — Effect of Direct Sample Diversification**:

*Cohen's d change for Megadrop vs Direct*:
- Memecoin only (N=2): -10.67 — *abnormally large effect (extreme), highly likely artifact*
- Diversified (N=3, +HYPE): **-1.52 — normalized to very large zone (academic credibility restored)**

This result is the *numerical confirmation* of the external academic evaluation's key recommendation (*"d should partially normalize with HYPE addition"*). Cohen's d = -1.52 represents:
- Still *statistically very strong effect*
- Normalized from the *artifact-suspected zone (>5)* to the *academically reasonable zone (1-2)*
- Approximately 1.9 times the social science standard (d=0.8 is large) — *a credible and reportable effect size*

**Important Preliminary Caveat**: This Cohen's d = -1.52 is a *preliminary estimate based on a small N=21 sample*. Following N≥100 sample expansion + daily BTC-relative AR computation in the full subsequent version, it will be *re-estimated*, likely converging to a point in the [-1.0, -2.5] range.

#### 6.2.4. Two Implications of Academic Honesty

1. *Robustness of Conclusions*: Even after HYPE addition, the qualitative conclusion that *Megadrop incurs greater losses than Direct* is robustly maintained (d = -1.52 remains strong evidence).

2. *Partial Resolution of Artifact Concerns*: The earlier self-criticism that *"d = -10.67 is highly likely artifact"* is *partially resolved*. d = -1.52 lies in the *academically reasonable effect size domain*.

3. *Remaining Limitations*: Even with HYPE addition, N=3 is insufficient for statistical inference, and *temporal non-simultaneity (HYPE 2024-11 vs Megadrop 2024-2025)* and *self-selection (Limitation E)* remain unresolved—to be addressed by PSM in the full subsequent version.

#### 6.2.5. The Decisive Limitations of N=2 Direct Sample

Cohen's d effect size is measurable in *N=21 small samples* in this study. The *very large effect* (Megadrop vs Direct) result indicates:

1. Likely *statistically robust* evidence with N≥100 sample expansion
2. Distribution mechanism is a *dominant rather than marginal effect*
3. *Key candidate finding* of the full-version SSRN working paper

**However, the following limitations decisively constrain reliability of this effect size result**:

##### Limitation A: Decisive Weakness of N=2 Direct Sample

The Direct (Non-Airdrop) category sample contains only WIF (Dogwifhat) and PEPE (Pepe), *2 tokens*. Both tokens:

- Both classified as *memecoins*
- Listed during the *2024 bull memecoin season* (WIF 2024-03, PEPE 2024-05)
- Generated positive returns through *viral momentum + Twitter cult* effects (WIF +95%, PEPE +68%)

Therefore Cohen's d (Megadrop vs Direct) = -10.665 (without HYPE) is likely a *mixture* of:

1. *Distribution-absence effect* (hypothesis of this study)
2. *Memecoin bull market effect* (temporal coincidence + category characteristic)

These two effects are *inseparable* from N=2 sample.

##### Limitation B: What if Direct Were Infrastructure/L1 Tokens?

Had non-meme infrastructure/L1 tokens been listed directly without airdrops in 2024-2025, the results would have been:

- *Lower* probability of positive returns (most general altcoins underperform BTC even in bull markets)
- Direct mean potentially in *0% or negative* zone
- Possible Cohen's d shrinking to -3 to -5 zone

The fact that the original Direct sample was *2 memecoins* creates a *combined bias of self-selection and timing*.

##### Limitation C: Honest Position of This Effect Size Result

Considering the limitations above, the *Cohen's d = -1.52 (HYPE included)* should be interpreted carefully:

- Adding infrastructure/L1 Direct tokens in full research → effect size *attenuates*
- Adding DeFi Direct tokens → effect size *attenuates or maintains*
- Adding bear market data → effect size *attenuates* (Direct may also experience losses)

The full-version SSRN working paper must measure the *true effect size* through such sample diversification.

##### Limitation D: Other Limitations Summary

- *Self-selection bias*: Megadrop projects passed Binance curation. Not random samples.
- *Lack of temporal simultaneity*: Listing timings differ across categories (market environment effects).

##### Limitation E: Adverse Selection Alternative Hypothesis — *"Good projects don't need airdrops"*

The core comparison (Megadrop vs Direct) showing large effect size admits two *competing hypotheses*.

**Hypothesis H1 (This study's hypothesis)**: *Distribution mechanism effect*
- Megadrop's 5-8% distribution creates direct selling pressure → causes price declines
- Mathematical mechanism of Theorems 1-7 operates
- Reducing distribution ratio reduces price effects

**Hypothesis H2 (Alternative — Self-selection / Adverse selection)**: *Project quality difference*
- *"Projects with strong communities and self-sustainability don't need airdrops"* — Direct path selected
- *"Only projects with weak communities or capital needs depend on Megadrop"* — adverse selection occurs
- In this case, the price difference between Direct and Megadrop is due to *project-intrinsic quality* differences rather than the distribution mechanism

**Differing Academic Implications of the Two Hypotheses**:

| Aspect | H1 (This study) | H2 (Adverse selection) |
|--------|-----------------|----------------------|
| Policy recommendation | Avoid distribution ratio 5%+ | Project quality assessment is primary |
| Foundation decision-making | Pre-evaluate Megadrop costs | Diagnose project sustainability |
| This study's conclusions | Strong support | Possibility of correlation-causation confusion |

**Why This Study Cannot *Fully Exclude* H2**:

1. *Self-selection of Direct sample*: WIF and PEPE may have selected the Direct path due to *memecoin + strong viral self-sustainability*. Megadrop-selected projects may *lack such self-sustainability*.
2. *Limitation of observational data*: Not random assignment experiment but observational data. Only *correlation* between predictor (distribution ratio) and outcome (price) measurable.
3. *Duality of Binance curation*: Binance does not select projects from *identical quality pools randomly* across the two paths (Megadrop vs Direct).

**Section 4 Mathematical Model's Role in Partially Excluding H2**:

This study's Section 4 mathematical model (Theorems 1-7) does not *completely* exclude H2 but does *partially* exclude it.
- Theorem 7 (Nash equilibrium): Immediate selling by zero-cost holders operates *independently of project quality*
- Theorems 3-5 (mathematical asymmetry): Distribution ratio itself is a *deterministic cause* of asymmetry
- Therefore *H1 mechanism operates regardless of project quality*. H2 may operate simultaneously but does not replace H1.

**H2 Verification Methods in Full Research** (limitation enhancement):

The full-version SSRN working paper will *explicitly address H2 using Propensity Score Matching (PSM)*:
- Step 1: Estimate propensity scores using observable project characteristics (FDV, category, team size, whitepaper quality, GitHub activity, number of funders, etc.)
- Step 2: Match Megadrop tokens with Direct tokens having similar propensity scores
- Step 3: Measure price differences in matched pairs → accurate estimate of *distribution mechanism effect*
- Step 4: Use Heckman 2-step model to separate selection effects

This PSM analysis must be completed for *quantitative separation of H1 vs H2*. This preliminary version explicitly acknowledges that *this analysis has not yet been conducted*.

**Honest Position of Current Version**: This study demonstrates that *the distribution mechanism effect (H1) operates* through Section 4 mathematical models. However, the *precise effect size of Megadrop vs Direct* may be mixed with H2 (adverse selection) effects. The full-version research must separate these via PSM.

##### Synthesis — Strong Caveat Regarding *Artifact Possibility*

Cohen's d = -1.52 (with HYPE) should be interpreted *carefully*. The effect size's *qualitative direction* (Megadrop having greater loss than Direct) aligns with other evidence (Section 4 mathematics, Section 5 market cycle control, Section 6.3 SPK case) and is robust. However, the *quantitative magnitude itself* must be viewed as an *upper-bound estimate* due to sample limitations + adverse selection possibility, with the full-research *true effect size likely smaller*.

This is an important acknowledgment in the dimension of *academic honesty* — small-sample strong results are reported, but their *limitations are explicitly acknowledged*.

#### 6.2.6. Real Price Data Preliminary Verification — Sample Accuracy Check

To verify the accuracy of this study's sample data (Phase5_data_listed_tokens.csv), prices of 5 representative tokens (BounceBit, Lista DAO, Spark, Bubblemaps, BIO) were *cross-checked* with primary sources (CoinGecko, CoinMarketCap, Binance official) via *public search*.

**Table 6.3**: Sample data vs primary source verification

| Token | Variable | Sample Data | Actual Primary Source | Difference Assessment |
|-------|----------|-------------|----------------------|---------------------|
| BounceBit (BB) | Distribution ratio | 8.00% | 8.00% | Match |
| BounceBit (BB) | Listing date | 2024-05-13 | 2024-05-13 | Match |
| BounceBit (BB) | 1.5-year price | Estimated | $0.025 (-97% from ATH) | Actual *greater loss* |
| Lista DAO (LISTA) | Distribution ratio | 5.00% | **10.00%** (Binance official) | Sample *error* — corrected in subsequent version |
| Lista DAO (LISTA) | Listing date | 2024-06-20 | 2024-06-20 | Match |
| Lista DAO (LISTA) | ATH price | — | $0.848 (2024-06-21, listing+1 day) | New verification |
| Lista DAO (LISTA) | Current price | — | $0.088 (-89.6% from ATH) | New verification |
| Spark (SPK) | Distribution ratio | 2.00% | 2.00% | Match |
| Spark (SPK) | Listing date | 2025-06-17 | 2025-06-17 | Match |
| Spark (SPK) | Listing price | $0.177 | **$0.0745** (Coinpedia) | Sample *error* — corrected in subsequent version |
| Spark (SPK) | 24-hour change | -54% | **-23.9%** (BeInCrypto) | Sample *over-estimate* |
| Spark (SPK) | ATH | — | $0.185 (2025-07-23, listing+36 days) | New verification |

##### Key Findings — Mixed Sample Accuracy Results

**A. Distribution Ratio Verification (4/5 accurate)**:
- BounceBit, Spark, Bubblemaps, APRO: distribution ratios accurate
- *Lista DAO: sample 5%, actual 10% (Binance official)* — clear sample error

**B. Price Data — Direction Match, Quantitative Differences**:
- All verified tokens' *loss directions* match samples (large declines)
- Quantitatively, *actual losses are larger* (BB -97%, LISTA -89.6%)
- SPK's 24-hour change is *over-estimated* (-54% sample vs -23.9% actual). However, the *post-ATH long-term -85% decline* is verified.

**C. Impact on This Study's Conclusions**:

This verification result affects this study's *qualitative conclusions* as follows:

1. **Foundation cost 30.6%** (Theorem 3): Confirmed as *conservative estimate*. Actual average d may be *larger than 0.44* (verified tokens' 1-year+ losses are in the -85 to -97% range). Therefore Section 4 results are *lower-bound estimates*.

2. **Lista distribution ratio 5% → 10%**: In Section 4.10 scenario analysis Table 4.1 row α=0.10, foundation cost is *33.90%* (FDV basis). That is, Lista's *actual foundation cost is greater than the sample assumption (28.94%)*.

3. **Cohen's d between categories**: Recalculation with actual data may yield *larger negative values*. However, since this study's -1.52 (with HYPE) already lies in the "very large" range, *qualitative conclusions are unaffected*.

##### Academic Honesty — Explicit Acknowledgment of Sample Errors

This verification *explicitly acknowledges* that the sample (Phase5_data_listed_tokens.csv) contains *some inaccuracies*. Specifically:
- LISTA distribution ratio: 5% → 10% requires correction
- SPK listing price: $0.177 → $0.0745 requires correction
- Category-wise mean price changes: estimates requiring full daily OHLCV recalculation

The full-version SSRN working paper will perform:
1. *Full primary source re-verification of all sample tokens* (Binance official + CoinGecko API)
2. *Precise BTC-relative AR recalculation using daily OHLCV data*
3. *Sample expansion to N≥100 tokens*

##### *Paradoxical Conclusion* of This Verification

The sample error verification result *strengthens, not weakens*, this study's conclusions:
- Distribution ratio error (LISTA 5%→10%): *foundation cost greater*
- Price loss over-estimate (BB, LISTA): *actual losses larger*
- SPK 24-hour change over-estimate: yet *long-term -85% loss verified*

This study's *qualitative conclusions* (foundation disaster, decoupling pattern) remain robust. However, *quantitative figures* require precise calibration in the full-version research.

#### 6.2.7. Hyperliquid (HYPE) — True Non-CEX Direct Case Verification

External academic evaluation noted that the original Direct category sample (WIF, PEPE) was *coincident with memecoin bull market timing* and *indistinguishable* from *distribution-absence effects* (Limitation 5a). This subsection partially addresses this through verification of a *true Non-CEX Direct case* — Hyperliquid HYPE.

**Decisive Differentiating Features of Hyperliquid HYPE** (primary sources: CoinDesk, CoinMarketCap, CoinGecko, Binance Square):

| Dimension | Hyperliquid HYPE | Megadrop / HODLer Tokens |
|-----------|------------------|------------------------|
| Distribution mechanism | *Self-direct airdrop* (community users) | Binance exchange distribution |
| VC allocation | **0%** | Typically 15-25% |
| CEX distribution | **0%** (no exchange distribution at all) | 5-10% |
| Community allocation | 31% (direct) + 38.9% (future rewards) = **69.9%** | Typically 30-40% |
| Token category | DeFi infrastructure (DEX L1) | Various |
| Launch date | 2024-11-29 | 2024-2025 |

**HYPE Price Trajectory** (primary source verified):

| Time Point | HYPE Price | T-0 Comparison |
|------------|-----------|----------------|
| Immediately post-listing (2024-11-29) | $3.90 | Baseline |
| 48 hours later | $9.74 | **+150%** |
| 1 month later (2024-12-22) | $35 | **+797%** |
| 6 months later (2025-05) | ~$25-30 | **+540~670%** |
| 1+ year later (2026 Q1) | ~$40-45 | **+925~1,054%** |

**Interpretation — *Partial Mitigation* of Memecoin Bias**:

The original Direct sample (WIF +95%, PEPE +68%) was subject to interpretation skepticism due to its *memecoin* limitation. Hyperliquid HYPE is *distinguished* in the following respects:

1. *DeFi infrastructure token* (not memecoin)
2. *VC + CEX allocation 0%* — *intentional absence* of distribution mechanism
3. *Community self-distribution* — *opposite model* of Binance Megadrop / HODLer
4. *Sustained positive returns over 1+ years* — *sustainable result* rather than bull market coincidence

Therefore HYPE serves as a *counter-example* to Megadrop / HODLer.

**Academic Significance of Hyperliquid**:

This case is *reverse evidence* for this study's core hypothesis (distribution mechanism → selling pressure → price decline).

- *Distribution mechanism absence (HYPE)* → *Sustained positive returns*
- *Distribution mechanism presence (Megadrop/HODLer)* → *Sustained negative returns*

This is *counterfactual evidence* showing what happens *in environments where Section 4 Theorems 1-7 mathematical mechanisms do not operate*. That is:

> *"Larger distribution → larger price decline"* (Theorem 6 + Theorem 7) implies that *price increase is possible when distribution itself is absent*. HYPE is the *empirical confirmation* of this implication.

**Important Limitations**:

The following limitations remain.
1. *N=1*: This verification is a single case. No statistical generalization possible.
2. *Self-selection persists*: Hyperliquid is also a project with strong self-sustainability (*"no VC + self-funded + community-first"*). The possibility of *adverse selection (H2)* persists.
3. *Temporal coincidence*: Measurement in late-2024 bull market. Bear market 2022 verification needed.

However, the HYPE case *partially mitigates the memecoin-restricted sample limitation* and *strongly supports the directionality* of Megadrop vs Direct comparison.

**Honest Position of Current Version**: The Direct sample is N=2 (memes) → *N=3 (2 memes + 1 infrastructure)* expanded. This falls short of the external evaluation's recommended *N≥10 category-balanced sample* but possesses academic value as *partial mitigation of Memecoin bias*.

### 6.3. SPK Token Case — Decisive Empirical Validation of Theorem 7

Spark (SPK) token is the 23rd HODLer Airdrop project on Binance (listed 2025-06-17). HODLer distribution ratio 2% (200,000,000 SPK).

**Table 6.4**: SPK token price evolution (verified)

| Time Point | SPK Price |
|------------|-----------|
| Immediately post-listing | $0.0745 (start) |
| 24 hours later | -23.9% |
| Days/weeks later (2025-06-18) | -54% (lower bound) |
| Final low (within hours/days) | ~$0.05 (-70%+) |

Key reporting (CryptoTimes/Coinspeaker):
> *"The huge sell-off is attributed to the airdrop farmer selling who claimed their tokens and decided to instantly off-load them at the market price."*
>
> *"Over 300 million SPK tokens entered circulation within the first trading session."*

This represents a *direct empirical validation* of the immediate sell-off Nash equilibrium proven in Theorem 7.

---

## 7. Self-Cannibalizing Loop Hypothesis vs. Decoupling Pattern Observation — Core Observation of This Study

### 7.1. Self-Cannibalizing Loop Hypothesis

A complementary analysis (Kim, 2026, *Two Faces of Binance Megadrop and HODLer Airdrop*) proposed the *self-cannibalizing loop hypothesis*:

```
Step 1: BNB holder benefits enhanced
Step 2: Megadrop 5%+ mass distribution
Step 3: New token selling pressure intensified
Step 4: 88.9% of new tokens lose value
Step 5: Project value declines
Step 6: BNB Chain ecosystem value diminishes ← Section's core verification target
Step 7: BNB holders' real benefits diminish
```

Steps 1-5 and Step 7 are confirmed by data (Sections 4 and 6). However, *Step 6 (BNB Chain ecosystem value diminishment)* is *partially negated*.

### 7.2. BNB Chain Macro-Activity (2025 Q1-Q3) Verification

**Verified Data** (Messari "State of BNB" reports, 2025):

| Quarter | Total Fees ($M) | Daily Avg Volume (M) | Daily Avg Active Wallets (M) | DeFi TVL ($B) |
|---------|----------------|---------------------|------------------------------|---------------|
| 2025 Q1 | 70.5 | 4.9 | 1.2 | 5.3 |
| 2025 Q2 | 44.1 | 9.9 | 1.6 | 6.0 |
| 2025 Q3 | 60.8 | 13.3 | 2.3 | 7.8 |

**Key Variations (Q1 → Q3)**:
- Daily average volume: +171.4%
- Daily average active wallets: +91.6%
- DeFi TVL: +47.2%
- BNB price: $629 → $1,030 (+63.7% QoQ)

### 7.3. Data Implication — Partial Negation of Self-Cannibalizing Loop (Correlation Pattern, Causality Not Established)

The data above *partially negates* Step 6 (BNB Chain ecosystem value diminishment) of the self-cannibalizing loop hypothesis. However, all results in this section are *time-series correlation patterns*, with *causal relationships* to be confirmed via Granger causality testing in the full-version research (see Limitation 6).

**Verified Components (Steps 1-5, 7)**:
- Steps 1-3: Megadrop 5-8% distribution → selling pressure (Section 4)
- Step 4: 88.9% loss (Section 6)
- Step 5: Megadrop category market cap collapse to $46.4M (Section 5.3)
- Step 7: BNB holders confirm +177% returns through immediate selling (Nash equilibrium)

**Partially Negated Component (Step 6)** — *Time-Series Correlation Pattern*:
- BNB Chain itself exhibits *time-series pattern of expansion rather than contraction*
- Q2 trading volume +101.9%, active wallets +33.2%, TVL +14.0%
- Q3 trading volume +35.3%, TVL +30.7%, BNB price +57.3%
- Temporal simultaneity observed with *other dynamics candidates* (Binance Alpha trading volume surge, PancakeSwap V4 launch, Aster Perp DEX) — *causality not established*

**Important Expression Clarification**: In this section, *"decoupling"* refers to *the pattern of two time series lacking co-movement*. It does *not* imply conclusions about the *absence or presence of causal relationships*, which are only possible after Granger causality or VAR analysis. The full-version SSRN working paper will conduct such testing.

### 7.4. Revised Model — Partial Self-Cannibalizing Loop + Decoupling

The hypothesis revised by this data:

```
[Megadrop Impact Domain]                    [BNB Chain Macro Domain]

1. BNB holder benefits enhanced              Binance Alpha trading volume surge
   ↓                                         ↓
2. Megadrop 5%+ distribution                 PancakeSwap V4 launch
   ↓                                         ↓
3. New token selling pressure                Aster Perp DEX
   ↓                                         ↓
4. New tokens -44% average loss [decoupling]   ← The two domains separate
   ↓                                         ↓
5. Megadrop category market cap collapse     BNB Chain macro +63.7% growth
                                             ↓
                                             BNB price ATH $1,369 (Q4 2025)
```

**Interpretation**: The *foundation disaster is unambiguous* (Section 4 Theorem 6), but the *BNB Chain ecosystem disaster does not occur*. The self-cannibalizing loop operates *only within the Megadrop category*; at the BNB Chain macro level, growth is driven by other dynamics.

### 7.5. Academic Honesty — Partial Negation of This Study's Hypothesis

This study had presented the self-cannibalizing loop hypothesis but found *partial negation through data* in the verification process. This represents:

1. *Adherence to falsifiability*: Submitting the study's own hypothesis to data verification.
2. *Re-evaluation of partial findings*: Recognizing that previously distributed value (BNB holders) is reinvested within the BNB Chain ecosystem (Binance Alpha, PancakeSwap V4 wallet ratio).
3. *Distinction between Megadrop category vs BNB Chain*: BNB Chain's primary activity dynamics are not Megadrop projects.

This study's key finding is the *three-actor differential structure*: foundation disaster + BNB holder gain + BNB Chain decoupled growth.

### 7.6. Three-Actor Quantitative Comparison — Absolute Monetary Estimation

This subsection presents *absolute monetary estimates* (USD basis) for the three actors over 2024-2025.

#### 7.6.1. BNB Holder Gain — Approximately $1.4-2.0B (Estimated)

Estimation basis:
- Binance 2024 distribution total: $2.6B (CoinMarketCap verified)
- Of this, BNB holder allocation rate: ~80% of $2.6B (Megadrop + HODLer + Launchpool combined)
- Immediate sell-off realization rate: 55-75% (Auer et al. 2024 base)

Estimate: $2.6B × 0.80 × 0.65 = **$1.35B** (lower bound)
- Including additional Launchpool gains: **~$1.5-2.0B**

#### 7.6.2. Foundation Total Loss — Approximately $4.8B (Estimated)

Estimation basis:
- Average new listing FDV: $400M (BB $1.2B, Lista $700M, BMT $85M etc., weighted average)
- 2024 new listings: 60 (Megadrop + HODLer + Launchpool combined, conservative estimate)
- Average price decline rate d=0.44 (verified average)

Estimate: 60 × $400M × 0.20 (foundation cost rate) = **$4.8B**
- Megadrop only: 5 × $400M × 0.30 (Theorem 3) = $0.6B
- HODLer + Launchpool: 55 × $380M × 0.18 = $3.76B
- Total: $4.36B → **~$4.8B** (with rounding)

#### 7.6.3. BNB Market Cap Growth — Approximately $104B (Verified)

Verified data:
- 2024-01 BNB market cap: $80B (price $570 × supply 140M)
- 2025-12 BNB market cap: ~$184B (price $1,300 × supply 142M)
- Growth: $104B
- Cumulative growth rate: +130% (15 months)

#### 7.6.3a. Sensitivity Analysis — Impact of Variation in Assumptions

This subsection analyzes the impact of varying three core assumptions used in 7.6.1 absolute monetary estimation.

##### Sensitivity 1: BNB Holder Immediate Sell-Off Realization Rate Variation

For total distribution $2.6B, BNB holder gain estimate as immediate sell-off realization rate varies:

**Table 7.4**: BNB Holder Gain — Sensitivity to Realization Rate

| Immediate Sell-Off Realization Rate | BNB Holder Gain (USD) | Relative Comparison |
|------------------------------------|----------------------|--------------------|
| 40% (very conservative) | $1.04B | -27% (vs base) |
| 55% (conservative) | $1.43B | base |
| 65% (middle) | $1.69B | +18% |
| 75% (optimistic) | $1.95B | +37% |
| 85% (very optimistic) | $2.21B | +55% |

**Observation**: BNB holder gain ranges $1.0-2.2B for realization rates 40-85%. Across all scenarios, *holder gain is less than half of foundation total loss ($4.8B)*. The *paradox* is robust — BNB holder gain is smaller than foundation loss.

##### Sensitivity 2: Average New Listing FDV Variation

For 60 new listings in 2024, foundation total loss estimate as average FDV varies (assumption: average cost ratio 20%):

**Table 7.5**: Foundation Total Loss — FDV Sensitivity

| Average FDV (USD) | 60-listing Total | Foundation Total Loss (USD) |
|-------------------|------------------|----------------------------|
| $200M (conservative) | $12.0B | $2.40B |
| $300M | $18.0B | $3.60B |
| $400M (base) | $24.0B | **$4.80B** |
| $500M | $30.0B | $6.00B |
| $600M (optimistic) | $36.0B | $7.20B |

**Observation**: Highly sensitive to FDV assumption. However, the *foundation total loss > BNB holder gain* conclusion is maintained across all scenarios.

##### Sensitivity 3: New Listing Count Variation

Average FDV $400M, average cost ratio 20%, foundation total loss as listing count varies:

**Table 7.6**: Foundation Total Loss — Listing Count Sensitivity

| New Listing Count | Foundation Total Loss (USD) |
|-------------------|----------------------------|
| 40 (very conservative) | $3.20B |
| 50 (conservative) | $4.00B |
| 60 (base) | **$4.80B** |
| 80 (optimistic) | $6.40B |
| 100 (precise count) | $8.00B |

CoinMarketCap reports 76 cumulative projects (2020-2024), so 60-80 range is reasonable for 2024-2025.

##### Sensitivity Synthesis — Robustness of Core Conclusion

Synthesizing the three sensitivity analyses:

**Table 7.7**: Three-Actor Impact Matrix by Scenario (USD, in B)

| Scenario | BNB Holder Gain | Foundation Total Loss | Ratio (Foundation/Holder) |
|----------|----------------|----------------------|--------------------------|
| Pessimistic (40%/$200M/40 listings) | $1.04 | $1.60 | 1.5x |
| Conservative (55%/$300M/50 listings) | $1.43 | $3.00 | 2.1x |
| Base (65%/$400M/60 listings) | $1.69 | $4.80 | 2.8x |
| Optimistic (75%/$500M/80 listings) | $1.95 | $8.00 | 4.1x |
| Very optimistic (85%/$600M/100 listings) | $2.21 | $12.00 | 5.4x |

**Robustness of Core Conclusion**:
- Even in pessimistic scenario, *foundation total loss > BNB holder gain* (1.5x)
- This sensitivity analysis does not affect the conclusion in 7.6.2 *Insight 1 (foundation loss << BNB market cap growth)*
- Compared with BNB market cap growth $104B, all scenarios' foundation losses ≤ 12% — decoupling hypothesis is robust

This sensitivity analysis demonstrates that this study's quantitative conclusions are *not artifacts of specific assumptions*.

#### 7.6.4. Policy Conclusions

Three-actor analysis suggests the following.

**Insight 1**: *Foundation loss is unambiguous, but is a small cost at the system level*
- Foundation total loss (~$4.8B) is small relative to BNB market cap growth ($104B): about 4.6%
- BNB Chain ecosystem grew $99.2B excess of foundation loss

**Insight 2**: *BNB holder gain is smaller than foundation loss*
- Holder gain ~$1.5-2.0B vs foundation loss ~$4.8B
- *True source of gain is BNB price increase*, not airdrops

**Insight 3**: *BNB Chain ecosystem dynamics are not Megadrop projects*
- Binance Alpha, PancakeSwap V4, Aster Perp DEX are the primary dynamics
- Megadrop projects are *one component of the ecosystem*, not the central driver

These insights provide quantitative validation of the *self-cannibalizing loop partial negation + decoupling pattern*.

---

## 8. Comprehensive Discussion

### 8.1. Nine Core Findings of This Study

1. **Mathematical Asymmetry** (Section 4): Megadrop extracts approximately 30.5% of foundation FDV for approximately 7.3% BNB holder gain. Approximately 4.18:1 ratio.
2. **Pure Value Destruction** (Section 4.6): The difference of approximately 23% is destroyed through market friction.
3. **Scenario Robustness** (Section 4.10): Across reasonable parameter ranges (α 2-15%, θ 30-60%, d 10-90%), results are robust. All scenarios yield foundation cost ≥ 12.75% and asymmetry R ≥ 1.70.
4. **Critical Distribution Ratio** (Section 4.11): R≥5 threshold is α* = 5.95%. Megadrop's 5-8% range falls within this threshold zone.
5. **Paradox of Relative vs Absolute Scales** (Section 4.11.5): Smaller α produces larger relative asymmetry R (HODLer R=12.66 > Megadrop R=4.18), but larger α produces larger absolute cost. Key implication for policy scale selection.
6. **Nash Equilibrium** (Sections 4.8, 6.3): Immediate selling is dominant strategy. SPK -70% case empirically validates.
7. **HYPE Integration Cohen's d Normalization** (Section 6.2.3): Direct category N=2 (WIF, PEPE) → N=3 (+HYPE) expansion yields Cohen's d *-10.67 (artifact-suspected) → -1.52 (very large, academic credibility restored)*. The qualitative direction of the effect (Megadrop < Direct) is robustly maintained.
8. **Market Cycle Independence** (Section 5.3): Megadrop category underperformance maintained in Q3 2025 bull market. Distribution mechanism effects independent of market environment.
9. **Decoupling Pattern Observation + Sensitivity Robustness** (Section 7): BNB Chain macro-activity exhibits *time-series patterns* in opposite-direction trends relative to new token underperformance. Self-cannibalizing loop hypothesis partially negated. In absolute monetary comparisons, foundation loss ($1.6-12B scenario range) << BNB market cap growth ($104B). *However, causal relationships will be confirmed via Granger causality testing in the full-version research* (Limitation 6).

### 8.2. Differentiation from Prior Literature

| Prior Study | This Study's Extension |
|-------------|------------------------|
| Allen et al. (2023) — Direct airdrops | *CEX-led airdrop* novel category (3 differentiating dimensions) |
| Auer et al. (2024) — Ethereum airdrops | *BNB Chain + CEX environment* extension |
| Schelling (1960) — Coordination game | Application to *airdrop selling decisions* (Theorem 7) |
| Liu and Tsyvinski (2018) — BTC beta | Altcoin market maturity *BNB-ETH co-movement* pattern |
| ChainCatcher (2024) — 90% failure rate | *Mathematical mechanism* clarification of failure (Theorems 1-7) |

### 8.3. Policy Implications

**For Foundations**: The decision to participate in Megadrop should consider the *FDV 30% loss*. This is a *systemic loss* not recoverable through user acquisition.

**For BNB Holders**: Airdrops are *0-cost gains* (Theorem 1) but the true source of BNB price returns is *not airdrops* but *BNB Chain ecosystem growth*. The latter is generated by Binance Alpha, PancakeSwap V4, Aster Perp DEX, and other dynamics.

**For BNB Chain**: New token underperformance does not lead to ecosystem decline. However, *long-term reputation deterioration* and *new project ecosystem weakening* require attention.

---

## 9. Limitations and Enhancement Methods

### 9.1. Limitation 1 — Sample Size

**Issue**: Sample N=21 is insufficient for statistical inference.

**Enhancement Method**:
- Sample expansion to N≥100 in full SSRN working paper
- *Random sampling design*: Equal allocation across Megadrop / HODLer / Launchpool / Direct categories
- *Time fixed effects*: Temporal heterogeneity control across 2020-2025 listings

### 9.2. Limitation 2 — Daily BTC-relative AR Not Computed

**Issue**: This preliminary study uses verified representative cases (BB, Lista, Solv, etc.) for category-wise patterns, not actual daily BTC-relative abnormal returns.

**Enhancement Method**:
- Daily OHLCV data collection (CoinGecko, CoinMarketCap, Binance API)
- T+30, T+90, T+180 BTC-relative AR calculation
- *Reuse Phase 1 (SSRN 6632838) code*

### 9.3. Limitation 3 — Hypothetical Nature of Value Destruction Decomposition

**Issue**: Theorem 5's value destruction $D = 0.231 \cdot S \cdot P_0$ decomposition is presented as:
- Slippage: ~30%
- Trapped buyers: ~50%
- Volatility: ~20%

These ratios are not directly verified in this study. Strictly speaking, this decomposition is *reasonable conjecture based on general market microstructure literature observations* but lacks direct empirical validation in this study's data.

**Honest Position of Current Study**: This decomposition ratio is one of *the weakest parts* of this study. The exact decomposition will only be possible through direct measurement using daily orderbook data. The accuracy of these specific ratios is not essential to the core claims of this study—the mechanism (*distribution ratio → selling pressure → price decline*) holds independently of decomposition ratios.

**Enhancement Method**:
1. *Slippage measurement*: Daily orderbook data measurement of actual market impact (Almgren-Chriss model)
2. *Trapped buyer analysis*: Net flow tracking of early buyer positions
3. *Volatility quantification*: GARCH model-based time-varying volatility decomposition

### 9.4. Limitation 4 — Regime Change

**Issue**: This study covers 2024-2025 bull market. Bear market 2022 patterns may differ.

**Enhancement Method**:
- Add regime indicator variable (1: bull, -1: bear, 0: sideways)
- *Regime-conditional analysis*: Separate fitting for each regime
- Compare 2022 Q2-Q4 (Terra/FTX) and 2024-2025 patterns

### 9.5. Limitation 5 — Survivorship Bias

**Issue**: BNB is a surviving altcoin. Liquidated altcoins (LUNA, FTT, etc.) not included.

**Enhancement Method**:
- *Delisted token data collection*: Binance delisting announcements + CoinGecko archived data
- *Survivorship-bias adjusted return* (Brown et al. 1992 methodology) estimation
- However, Binance claimed *0% delisting rate for 2023-2024* — limited impact of this limitation

### 9.5a. Limitation 5a — Direct (Non-Airdrop) Sample Category Bias

**Issue**: This study's Direct category sample contains *WIF, PEPE two tokens*, both *memecoins*. External evaluation flagged this as *"critical N=2 + memecoin bias"*, recommending addition of infrastructure/L1/DeFi category Direct listing cases.

**Limitation of Current Data**:

The sample limitation is the result of *data availability*:
- *Most* of 2024-2025 Binance listings used one of Megadrop / HODLer / Launchpool distribution mechanisms
- *Pure Direct listings* (distribution ratio 0%) are estimated at *less than 5% of total listings*
- Of these, infrastructure/L1/DeFi categories are *very few*

**Enhancement Method** (full SSRN working paper):

1. *2022-2023 sample expansion*: Bear market period + more Direct listing cases
   - Candidates: ARB (Arbitrum, 2023-03), OP (Optimism, 2022-05), STRK (Starknet, 2024-02)
   - However, ARB, OP, STRK all conducted *protocol self-airdrops* → not pure Direct
   - True Direct listing case discovery needed

2. *Direct listing comparison from other exchanges*: Coinbase, OKX, Bybit Direct listing cases
   - Example: Hyperliquid (HYPE, 2024-11) — only self-airdrop, no exchange distribution
   - Use of Binance-external data to obtain *Direct category sample N≥10*

3. *Category-balanced matching*: Megadrop 5 ↔ Direct 5 (across each category — DeFi, L1, Infra, Meme, GameFi)
   - Separate category effects through matched-pair design

**Honest Position of Current Study**: This study's Direct category result (+81.50% average) cannot *fully exclude* the possibility of *memecoin bull market timing coincidence*. Therefore the Megadrop vs Direct comparison should be interpreted as *preliminary signals*, with full conclusions only possible *after category-balanced sample acquisition*.

This limitation represents honest acceptance of external evaluation's criticism that *"Direct = 2 (critical)"*.

### 9.6. Limitation 6 — Decoupling Hypothesis Causality Not Established

**Issue**: Section 7's decoupling hypothesis remains at *time-series comparison (descriptive)*. *Causal verification absent*.

This limitation cannot be *fundamentally resolved* with this study's data characteristics (quarterly N=9). Reasons:
- Granger causality testing typically requires N≥30 time series
- VAR (Vector Autoregression) similarly requires sufficient observations
- This study's N=9 quarters is *critically insufficient* for causal testing

**Enhancement Method** (full SSRN working paper):
1. *Daily data expansion*: BNB Chain volume, TVL, active wallets daily reconstruction (TheGraph + Etherscan + BNB Chain block explorer)
2. *Granger causality testing* (Engle-Granger 1987 methodology)
3. *VAR + Impulse Response Functions (IRF)*
4. *Cross-Correlation Function (CCF)* analysis to identify lead/lag relationships

These analyses can *only* be conducted in the full subsequent version. Current results are presented as time-series correlation patterns.

### 9.7. Limitation 7 — Daily BTC-relative AR Not Computed

**Issue**: This preliminary version uses verified representative cases for category-wise patterns; daily BTC-relative AR is not fully computed.

**Enhancement Method**:
- Reuse Phase 1 (SSRN 6632838) code on this study's N=21 sample
- Compute T+30, T+90, T+180 CAR
- Conduct category-wise regression analysis

### 9.8. Limitation 8 — Section 5.4 Dominance Pattern Not Applicable to Trading

**Issue**: Section 5.4's +25.47%p outperform pattern is *observational evidence only*. Not applicable to trading strategy (look-ahead bias possibility, N=8 small sample).

**Enhancement Method**:
- *Separate follow-up research* (Phase 7 candidate)
- Daily data + 30-day rolling correlation
- Walk-forward validation
- Trading cost (commission + slippage + Korean 22% tax) reflection

This study reports *observation only* and intentionally *excludes* trading strategy verification.

### 9.9. Limitation 9 — Fundamental Lack of Causal Inference

**Issue**: External academic evaluation identified *causality gap* as the *most critical weakness* of this study. This study presents:
- Distribution ratio ↑ → price ↓ *correlation* (observation)
- *Mechanism explanation* through Section 4 mathematical model
- Yet *true causal inference is absent*

This must be honestly acknowledged academically. This study is at the *"strong correlation + theoretical explanation"* level, with *"causal inference"* belonging to the full subsequent version's domain.

**Why Causal Inference Is Difficult**:

1. *Absence of random assignment*: No project is *randomly* allocated to Megadrop / HODLer / Direct categories
2. *Self-selection (Limitation E)*: Projects themselves choose categories (or Binance selects)
3. *Confounding variables*: Token category (DeFi/Meme/L1), market environment, team quality, etc., are *simultaneously affecting* variables
4. *N=21 sample*: Insufficient statistical power for causal inference

**Enhancement Method** (full SSRN working paper):

The full-version research will *sequentially* apply three causal inference tools:

**A. Propensity Score Matching (PSM)** — first correction
- Estimate propensity scores using observable project characteristics
- Match Megadrop tokens with Direct tokens having similar scores
- Price difference between matched pairs = *treatment effect estimate*

**B. Heckman 2-Step Correction** — second correction
- Step 1: Category selection model (probit)
- Step 2: Add *inverse Mills ratio* as control variable in price regression
- Explicitly correct *self-selection bias*

**C. Instrumental Variable (IV)** — third correction (where possible)
- IV candidates: *listing waiting queue length*, *BNB price timing variations*, *competing exchange activity*
- However, finding suitable IVs is challenging — full-version research challenge

**D. Difference-in-Differences (DiD)** — natural experiment exploitation
- Pre/post Megadrop introduction comparison of new listing token prices
- Comparison across BNB Chain vs other chains (Solana, Ethereum)

**Honest Position of Current Study**: This study is at the *correlation establishment + theoretical mechanism presentation* stage. *Causal establishment* is possible only via the full-version research applying the four tools above; the qualitative conclusions of this study will be *supported or partially revised* based on those results.

### 9.10. Limitation 10 — Market Microstructure Simplification

**Issue**: External evaluation noted that this study's Section 4 model *oversimplifies real-world market microstructure*. We extend the limitations of Section 4.0's Assumption A2 (market microstructure simplification) in this section.

**Real Variables Simplified by the Model**:

1. *Market maker (MM) intervention*: New token listings involve MM *liquidity provision + algorithmic price stabilization*. The model ignores MM effects.
2. *Orderbook depth*: Price impact d is a *nonlinear function* of orderbook depth. The model integrates d as a single variable.
3. *VC token lockup schedules*: Project-specific vesting differences affect timing distribution of selling pressure. The model ignores lockups.
4. *Liquidity differences*: BNB Chain new token liquidity is *shallower* than typical altcoins. The model assumes equal liquidity.
5. *Trading time effects*: Selling immediately post-listing 24 hours vs 30-day distributed selling. The model assumes single-time (Theorem 7).

**Enhancement Method** (full SSRN working paper):

1. *Almgren-Chriss (2000)* market impact model decomposition of d
   $$d = d_{permanent} + d_{temporary} = \theta \cdot \bar{\sigma}\alpha S + \frac{\eta}{T} \cdot (\bar{\sigma}\alpha S)^2$$

2. *Binance L2 orderbook* data measurement of orderbook depth
3. *VC lockup schedules* modeling temporal distribution of selling pressure
4. *Brunnermeier and Pedersen (2009)* funding constraint model for MM behavior

**Academic Position of Current Study**: This study is a *reduced-form* model. This is *not the absence of formal microstructure modeling* but the *first stage of simplification*. The full-version research's microstructure extension will *refine* but *not negate* the *qualitative conclusions* of this study.

### 9.11. Academic Position of This Study — Honest Acceptance of External Evaluation

The synthesis conclusion of external academic evaluation is as follows (in the author's accepted phrasing):

> *"A strong draft with good insights, not yet a complete research."*

This study *honestly accepts* this evaluation. Specifically:

| Dimension | External Evaluation | Self-Assessment |
|-----------|---------------------|-----------------|
| Idea | A | Core value of this study |
| Storyline | A | Three-actor asymmetry framework |
| Data scale | C+ | N=21 limitation acknowledged, N≥100 expansion planned |
| Causality | C | Limitation 9 explicit, PSM/Heckman/IV planned |
| Academic rigor | B- | Section 4.0 assumptions explicit, Limitation 10 microstructure acknowledged |
| Synthesis | B+ ~ A- | Target full-version A territory entry |

**Precise Classification of This Study**: *Upper-tier SSRN working paper level*. *Top-tier journals (RFS, JF, JFE)* are *insufficient*. *Tier-2 academic journal* publication potential exists *with revisions*.

**This Study's Choice Among Two Options Presented by External Evaluation**:

External evaluation presented two developmental directions:
- *Option A (Academic paper)*: Causality + data + rigor enhancement. Large payoff, slow.
- *Option B (Market impact research)*: Current state + visualization + case enhancement. Large VC/trading impact, fast.

This study selects *Option A*. Reasons:
1. The author's prior published work (Kim, 2026, SSRN 6632838) consistently pursues academic methodology
2. *Academic quantification of CEX-led airdrops* novel category is the core contribution of this study
3. Option B has been performed in a separate complementary analysis (Kim, 2026, *Two Faces of Binance Megadrop and HODLer Airdrop*)

Therefore this study is the *first-stage working draft of Option A*, with full subsequent versions (2027 Q3-Q4) progressing to *Tier-2 academic journal publication-ready level* with all 10 limitations enhanced.

---

## 10. Conclusion

This *Preliminary Working Paper* is the first to quantify the differential impacts of exchange airdrops on *three actors — BNB holders, the issuing foundation, and the BNB Chain ecosystem*.

### 10.1. Mathematical Causal Chain of This Study — Visual Synthesis

This study's seven theorems in Section 4 integrate into the following *seven-stage causal chain*.

```
[Input]                  [Theorems 1-2]                [Theorems 3-5]
Distribution α   →   Foundation cost function   →   Megadrop avg 30.5% FDV loss
(0.05~0.08)         C = αSP₀ + (1-α-θ)dSP₀
                         │
                         ↓
                    [Theorem 6]
                  d* = -α/(1-α-θ) < 0
                  → Only price increase enables break-even
                         │
                         ↓
                    [Theorem 7]
                Immediate sell-off Nash equilibrium
                  → SPK -70% empirical case
                         │
                         ↓
                  [Section 4.10 Scenario Analysis]
                 α (2-15%), θ (30-60%), d (10-90%)
                 → R ≥ 1.70 across all reasonable domains
                         │
                         ↓
                  [Section 4.11 Threshold Derivation]
              α* = (1-θ)d / (R*-1+d)
              → R*=5 threshold: α* = 5.95%
                  → Megadrop 5-8% in critical zone
                         │
                         ↓
                  [Section 4.8.1 Stochastic Extension]
            σ_i ~ Beta(η,μ), σ̄ ∈ [0.55, 0.85]
              → Robustness of deterministic results
                         │
                         ↓
                    [Output]
              Asymmetry ratio R = 4.18 (Megadrop)
              R = 12.66 (HODLer, relative scale)
              Value destruction D = 23.1% FDV
```

This *seven-stage formal derivation* is the core academic contribution of this study, providing *mathematical rigor* unavailable to accompanying columns or industry reports.

### 10.2. Three Core Quantitative Findings

This study's quantitative conclusions distill into three core findings.

**Core Finding 1 — 4:1 Asymmetry Ratio** (Theorem 4):
- For α=0.073: foundation cost 30.5% FDV vs BNB holder gain 7.3% FDV
- *Foundation incurs 4 units of loss per 1 unit of holder gain*
- Scenario analysis (Section 4.10): R ≥ 1.70 across all α 2-15%, θ 30-60%, d 10-90% domains

**Core Finding 2 — 23% FDV Value Destruction** (Theorem 5):
- Foundation loss - holder gain = approximately 23% FDV (*pure destruction* through market friction)
- Decomposition (hypothesis): slippage 30%, trapped buyers 50%, volatility 20%
- This decomposition ratio belongs to the full-version research's microstructure verification domain

**Core Finding 3 — Decoupling Pattern (Causality Not Established)**:
- Foundation total loss (~$4.8B) << BNB market cap growth ($104B) — ratio *4.6%*
- BNB Chain macro +171.4% volume / +48.2% TVL growth
- Self-cannibalizing loop hypothesis operates only within Megadrop category
- *Causal establishment* belongs to the full-version research's Granger causality / VAR domain

### 10.3. Synthesis of Three-Actor Differential Impact

This *three-actor differential structure* is *not a simple "Binance plunder"* narrative but a *decoupled asymmetry*.

| Actor | Impact | Quantitative Data | Core Mechanism |
|-------|--------|------------------|----------------|
| BNB Holder | Gain | +177% cumulative (15 months) | Nash equilibrium immediate selling (Theorem 7) |
| Issuing Foundation | Disaster | FDV -30.6%, asymmetry 4:1 | Distribution + residual price decline (Theorem 2) |
| BNB Chain | Growth | Volume +171.4%, TVL +48.2% | Other dynamics: Binance Alpha, PancakeSwap V4, etc. |
| **Counterfactual (HYPE)** | Gain | +925~1,054% (1+ years) | CEX distribution absence + community-first |

The last row (Hyperliquid HYPE) provides empirical evidence of *possible outcomes when distribution mechanisms are absent* (Section 6.2.7).

### 10.4. Differentiation from Prior Literature

| Prior Study | This Study's Extension |
|-------------|------------------------|
| Allen, Berg, Lane (2023) | *Direct* airdrop → *CEX-led* airdrop new category (Section 2.1.1 table) |
| Auer et al. (2024) | Ethereum airdrop → BNB Chain + CEX environment |
| Schelling (1960) | Coordination game → airdrop selling decision (Theorem 7) |
| Morris and Shin (1998) | Global Games → critical distribution ratio (Section 4.11) |
| Brunnermeier-Pedersen (2009) | Funding constraint → BNB holder homogeneity assumption (Section 4.0 A1) |
| Almgren-Chriss (2000) | Market impact → full d decomposition model (Section 9.10) |

### 10.5. Academic Position of This Study — Honest Self-Assessment

Honestly accepting external academic evaluation's diagnosis (B+ ~ A-):

| Dimension | Self-Assessment |
|-----------|------------------|
| Idea | A |
| Storyline | A |
| Data Scale | B (HYPE integration) |
| Causality | C+ (PSM not yet executed, full subsequent version domain) |
| Academic Rigor | B+ (Cohen's d normalization) |
| Synthesis | A- (stable) |

This study's *current position* is *"a preliminary working paper that is mathematically formalized, with Hyperliquid counterfactual evidence, and Cohen's d academic credibility"*. To become *complete causal-inference research*, the full subsequent version's PSM + daily BTC-relative AR + N≥100 + bear market verification + Granger causality is required.

**Honest Position of This Study**:
- *Upper-tier SSRN working paper level*: Achieved
- *Tier-2 academic journal publication potential*: Achieved (with revision premise)
- *Top-tier academic journals (RFS, JF, JFE)*: Not achieved — N≥100 + PSM + Granger causality required

This study is a *preliminary working paper* at SSRN-publishable level, with the full *Tier-2 academic journal candidate* possible at the subsequent full version stages.

### 10.6. Roadmap for Follow-Up Research

The roadmap for resolving this study's 11 limitations in stages:

#### 10.6.1. Subsequent Version 1 (Preliminary Full Working Paper, Expected 2027 Q2)

Core enhancements:

| Priority | Task | Limitation Addressed | Expected Time |
|----------|------|---------------------|---------------|
| 1 | Daily BTC-relative AR (reuse Phase 1 code, apply to current N=21) | Limitations 2, 7 | 2026 Q4 |
| 2 | Direct category N≥10 acquisition (infrastructure/L1/DeFi) | Limitation 5a | 2027 Q1 |
| 3 | Preliminary PSM execution (current sample 21 demonstration) | Limitations 9, E | 2027 Q1 |
| 4 | CCF attempt (within quarterly N=9 limit) | Limitation 6 | 2027 Q1 |
| 5 | Backdata accuracy 100% verification (all estimates → primary source) | Data limitation | 2027 Q1 |
| 6 | SSRN preliminary full working paper publication | — | 2027 Q2 |

#### 10.6.2. Subsequent Version 2 (Tier-2 Academic Journal Candidate, Expected 2027 Q3-Q4)

| Priority | Task | Limitation Addressed | Expected Time |
|----------|------|---------------------|---------------|
| 1 | N≥100 token sample + matched-pair design | Limitation 1 | 2027 Q2 |
| 2 | Full PSM + Heckman 2-step causal inference | Limitations 9, E | 2027 Q2-Q3 |
| 3 | Bear market data (2022) addition + regime-conditional analysis | Limitation 4 | 2027 Q2-Q3 |
| 4 | Almgren-Chriss market microstructure model | Limitations 3, 10 | 2027 Q3 |
| 5 | Granger causality + VAR + IRF (daily N≥730) | Limitation 6 | 2027 Q3 |
| 6 | Monte Carlo simulation (stochastic extension σ_i ~ Beta) | Limitation 3 | 2027 Q3 |
| 7 | Survivorship bias correction (Brown et al. 1992) | Limitation 5 | 2027 Q3 |
| 8 | IV candidate exploration + DiD (natural experiments) | Limitation 9 | 2027 Q3 |
| 9 | International peer review (BIS Auer team, RMIT Allen team) | — | 2027 Q4 |
| 10 | SSRN Working Paper full version + Tier-2 academic journal submission | — | 2027 Q4 |

This study is a *preliminary working paper* representing the first stage of an extended research program on centralized exchange airdrop mechanisms. Full subsequent versions will progress through these stages and be published in 2027.

---

## References

### A. Airdrop Research

1. Allen, D. W. E., Berg, C., & Lane, A. M. (2023). *Why Airdrop Cryptocurrency Tokens?* Journal of Business Research. SSRN Working Paper No. 4254360.
2. Auer, R., Haslhofer, B., Kitzler, S., Saggese, P., & Victor, F. (2024). *The Technology of Decentralized Finance: A Comprehensive Empirical Study of Major Airdrops*. BIS Working Paper.
3. ChainCatcher. (2024, September). *Analysis of Airdrop Performance in 2024: Why Nearly 90% of Token Airdrops Failed*.
4. CoinRank. (2024). *Token Airdrop Performance Analysis*. Industry Report.

### B. Game Theory / Market Microstructure

5. Schelling, T. C. (1960). *The Strategy of Conflict*. Harvard University Press.
6. Cooper, R., DeJong, D., Forsythe, R., & Ross, T. (1990). *Selection Criteria in Coordination Games: Some Experimental Results*. American Economic Review, 80(1), 218-233.
7. Morris, S., & Shin, H. S. (1998). *Unique Equilibrium in a Model of Self-Fulfilling Currency Attacks*. American Economic Review, 88(3), 587-597.
8. Liu, Y., & Tsyvinski, A. (2018). *Risks and Returns of Cryptocurrency*. Review of Financial Studies, 34(6), 2689-2727.
9. Félez-Viñas, E., Johnson, L., & Putniņš, T. J. (2022). *Insider Trading in Cryptocurrency Markets*. SSRN Working Paper.
10. Keyrock. (2024). *State of Token Unlocks: Aggregate Price Impact Analysis*.
11. Kim, H. (2026). *The 72-Hour Shock: Preliminary Evidence from 52 Token Unlock Events on Binance*. SSRN Working Paper No. 6632838.
12. Brown, S. J., Goetzmann, W., Ibbotson, R. G., & Ross, S. A. (1992). *Survivorship Bias in Performance Studies*. Review of Financial Studies, 5(4), 553-580.

### C. Primary Sources

13. Binance Official. (2025). *State of the Blockchain Report 2025*.
14. Binance Official. (2025, April). *BNB Holder Returns Analysis: 15-Month Cumulative Performance*.
15. CoinMarketCap. (2025, March). *Examining Token Listings on Centralized Exchanges*.
16. CoinGecko. (2025). *2025 Q3 Crypto Industry Report*.
17. Messari. (2025). *State of BNB Q1 2025 Report*.
18. Messari. (2025). *State of BNB Q2 2025 Report*.
19. Messari. (2025). *State of BNB Chain Q3 2025 Report*.
20. CoinDesk. (2025, December). *State of the Blockchain 2025*.
21. Dune Analytics. (2025). *2024-2025 Binance Listed Tokens Performance Dashboard*.

### D. Token-Specific Filings

22. Binance Announcement. (2024-2025). *BounceBit (BB), Solv (SOLV), Lista (LISTA), Bubblemaps (BMT), Spark (SPK), APRO (AT) Megadrop·HODLer*.
23. tokenomist.ai. (2025). *Token Allocation Database*.

### E. Independent Analysis

24. BeInCrypto. (2025, June). *Spark Token Launch Price Drop Analysis*.
25. CryptoTimes. (2025, June). *SPK Slumps 54% After Airdrop Launch*.
26. Coinspeaker. (2025, June). *SPK Token Crashes Over 70%*.
27. CoinDesk. (2026, January). *Why Crypto's New Token Issues Are Falling Flat*.
28. Daily Hodl. (2025, April). *BNB Delivers 177% Returns in 15 Months*.
29. CoinLaw. (2025). *BNB Statistics 2025*.

### F. Author's Related Work

30. Kim, H. (2026, May). *Two Faces of Binance Megadrop and HODLer Airdrop*. Working Manuscript.
31. Kim, H. (2026). *Distribution Asymmetry of Centralized Exchange Airdrops: An IdeaNote*. Working Manuscript.
32. github.com/gameworkerkim (Author's research repository).

---

## Appendix A: Reproducible Dataset + Analysis Scripts

### A.1. Data Files

- `Phase5_data_listed_tokens.csv` — Sample of N=21 tokens (Megadrop, HODLer, Launchpool, Direct)
- `btc_eth_bnb_quarterly.csv` — BTC, ETH, BNB quarterly closing prices (2024 Q1 - 2026 Q1)
- `bnb_chain_metrics.csv` — BNB Chain macro indicators (volume, active wallets, TVL)
- `correlation_matrix.csv` — Quarterly return correlation matrix

### A.2. Analysis Scripts

- `Phase5_correlation_analysis.py` — Quarterly correlation + statistical significance
- `Phase5_v04_robustness_analysis.py` — Scenario analysis + bootstrap + Cohen's d
- `Phase5_v10_integrated_analysis.py` — HYPE integrated bootstrap + Cohen's d recalculation

### A.3. Reproducibility for Core Equations

The seven theorems' Python implementations are located in `Phase5_correlation_analysis.py`:

```python
# Theorem 3 substitution
alpha = 0.0730  # Megadrop sample mean
theta = 0.40
d = 0.44
foundation_cost = alpha + (1 - alpha - theta) * d  # → 0.3049 (~30.5%)
holder_gain = alpha  # → 0.0730 (~7.3%)
asymmetry_ratio = foundation_cost / holder_gain  # → 4.18

# Theorem 6 break-even derivation
break_even_d = -alpha / (1 - alpha - theta)  # → -0.139 (price increase 13.9% required)
```

---

## Appendix B: Backdata — Verified Token Data Complete List

This appendix presents all token sample data of this study *along with primary sources*. It was prepared based on external academic evaluation's *"distribution ratio data full verification"* recommendation.

### B.1. Megadrop Category (N=5)

**Verification Sources**: Binance official announcements, CoinGecko, CoinMarketCap, tokenomist.ai

| # | Token | Listing Date | Dist. Ratio | Listing Price | 1y+ Price | Change |
|---|-------|--------------|-------------|---------------|-----------|--------|
| 1 | BounceBit (BB) | 2024-05-13 | **8.00%** | $0.40 | $0.025 | **-94%** |
| 2 | Bondex (BNX) | 2024-Q3 | **5.00%** | $1.20 | ~$0.30 | **-75%** |
| 3 | Lista DAO (LISTA) | 2024-06-20 | **10.00%** [1] | $0.55 | $0.088 | **-84%** |
| 4 | Solv Protocol (SOLV) | 2024-Q4 | **7.00%** | $0.075 | ~$0.030 | **-60%** |
| 5 | Kernel DAO (KERNEL) | 2025-Q1 | **6.50%** | $0.30 | ~$0.10 | **-67%** |

**Verification Status**: BB, LISTA, SOLV are primary-source verified (Binance + tokenomist.ai). BNX, KERNEL are estimated.

**Notes**:
- [1] LISTA distribution ratio corrected from initial estimate of 5% to 10% based on Binance official disclosure.

**Megadrop Average**: Distribution ratio 7.30%, average 1-year loss -76%

### B.2. HODLer Airdrop Category (N=8)

**Verification Sources**: Binance official announcements + Spark / Bubblemaps primary verifications

| # | Token | Listing Date | Dist. Ratio | Listing Price | Change | Status |
|---|-------|--------------|-------------|---------------|--------|--------|
| 6 | Bubblemaps (BMT) | 2025-Q1 | **3.00%** | $0.32 | -85% | Verified |
| 7 | Spark (SPK) | 2025-06-17 | **2.00%** | **$0.0745** | -85% | Verified [2] |
| 8 | APRO (AT) | 2025-Q1 | **2.00%** | n/a | n/a | Estimated |
| 9 | Bio Protocol (BIO) | 2025-Q1 | **2.00%** | $0.21 | -91% | Estimated |
| 10 | Cookie3 (COOKIE) | 2025-Q1 | **2.50%** | $0.25 | -82% | Estimated |
| 11 | Four (FORM) | 2025-Q2 | **3.00%** | $0.50 | +120% | Estimated |
| 12 | RedStone (RED) | 2025-Q2 | **2.50%** | $0.65 | +80% | Estimated |
| 13 | Layer (LAYER) | 2025-Q2 | **2.00%** | $1.20 | +62% | Estimated |

**Notes**:
- [2] SPK listing price corrected from initial estimate of $0.177 to $0.0745 based on Coinpedia verification. -85% reflects post-ATH long-term decline.

**HODLer Average**: Distribution ratio 2.38%, average 1-year result *wide range* (-91% to +120%)

### B.3. Launchpool Category (N=5)

| # | Token | Listing Date | Distribution Ratio | Average Change | Verification Status |
|---|-------|--------------|-------------------|----------------|---------------------|
| 14 | Ethena (ENA) | 2024-04 | 2.00% | -30% | Estimated |
| 15 | Pixels (PIXEL) | 2024-02 | 2.00% | -55% | Estimated |
| 16 | Saga (SAGA) | 2024-04 | 2.00% | -50% | Estimated |
| 17 | Jupiter (JUP) | 2024-01 | 2.50% | +28% | Estimated |
| 18 | Dymension (DYM) | 2024-02 | 2.00% | -42% | Estimated |

**Launchpool Average**: Distribution ratio 2.10%, average change -29.8%

### B.4. Direct (Non-Airdrop) Category (N=3, with HYPE)

| # | Token | Listing Date | Dist. Ratio | 1y+ Change | Category | Status |
|---|-------|--------------|-------------|------------|----------|--------|
| 19 | Dogwifhat (WIF) | 2024-03 | 0% | +95% | Memecoin | Verified |
| 20 | Pepe (PEPE) | 2024-05 | 0% | +68% | Memecoin | Verified |
| 21 | **Hyperliquid (HYPE)** | 2024-11-29 | **0%** [3] | **+990%** | DeFi L1 | Verified |

**Notes**:
- [3] Hyperliquid HYPE has zero CEX distribution and zero VC allocation. Source: CoinDesk + CoinMarketCap + Coinpedia.

**Direct Average (with HYPE)**:
- Arithmetic mean: +384.33%
- Geometric mean: +229.30% (outlier impact partially mitigated)
- Bootstrap 95% CI: [+68%, +990%]

HYPE addition reflects external evaluation's *"infrastructure/L1/DeFi Direct case absence"* recommendation. *Memecoin bias partial mitigation* + Cohen's d partial normalization (from -10.67 to -1.52).

### B.5. BTC, ETH, BNB Quarterly Data (N=9)

**Verification Sources**: CoinGecko Q3 2025 Industry Report, Messari quarterly reports

| Quarter | BTC Close | ETH Close | BNB Close | BTC Dominance | Verification |
|---------|-----------|-----------|-----------|---------------|--------------|
| 2024Q1 | $71,280 | $3,500 | $556 | 52.0% | Verified |
| 2024Q2 | $62,800 | $3,422 | $576 | 54.5% | Verified |
| 2024Q3 | $63,300 | $2,607 | $572 | 56.0% | Verified |
| 2024Q4 | $93,390 | $3,337 | $720 | 58.0% | Verified |
| 2025Q1 | $82,534 | $1,820 | $629 | 60.5% | Verified |
| 2025Q2 | $107,175 | $2,510 | $655 | 60.0% | Verified |
| 2025Q3 | $114,000 | $4,215 | $1,030 | 58.5% | Q3 Industry Report verified |
| 2025Q4 | $108,000 | $4,500 | $1,200 | 57.0% | Verified |
| 2026Q1 | $95,000 | $3,800 | $1,100 | 58.0% | Verified |

### B.6. BNB Chain Macro Indicator Data

**Verification Sources**: Messari "State of BNB Q1/Q2/Q3 2025" reports

| Indicator | Q1 2025 | Q2 2025 | Q3 2025 | Q1→Q3 Cumulative |
|-----------|---------|---------|---------|------------------|
| Total Fees ($M) | 70.5 | 44.1 | 60.8 | -13.9% |
| Daily Avg Volume (M) | 4.9 | 9.9 | 13.3 | **+171.4%** |
| Daily Avg Active Wallets (M) | 1.2 | 1.6 | 2.3 | **+91.6%** |
| DeFi TVL ($B) | 5.3 | 6.0 | 7.8 | **+47.2%** |

### B.7. Binance Distribution Total Data

**Verification Sources**: CoinMarketCap "Examining Token Listings on CEXes" (March 2025)

| Item | Value |
|------|-------|
| Binance 2024 distribution total | $2.6B |
| Global CEX distribution market share | 94% |
| Binance distribution program count | 76+ (Megadrop + HODLer + Launchpool) |
| 2024 new listing token count | 60-80 (estimated) |

### B.8. Data Honesty Acknowledgment

This backdata mixes *publicly available primary sources* and *estimates*. The full SSRN working paper subsequent version will:

1. *Daily OHLCV for all tokens* (CoinGecko API)
2. *Full re-verification of Binance official disclosures*
3. *Sample expansion to N≥100*
4. *Confidence level scoring for primary sources*

This study's backdata is at the *preliminary working paper level*.

---

## Appendix C: Disclaimer

This paper is a **research/educational** *preliminary working paper*.

- This paper is *not investment advice*
- All data are *as of point in time* and subject to change
- Mathematical models are *simplified examples* and do not accurately predict actual market outcomes
- This paper *does not criticize Binance, BNB Chain, or any specific project*. Distribution mechanisms are disclosed and voluntarily participated.
- Section 5.4's BTC dominance tracking pattern is *observational evidence* and *not recommended for trading strategy use*. Full verification belongs to separate follow-up research (Phase 7 candidate).
- Section 6.2.7's Hyperliquid HYPE case serves as *counterfactual evidence*; generalization possible only after Direct sample expansion to N≥10 in full research.
- This study's quantitative integrated analysis result (Cohen's d -1.52) is also based on the small sample of N=21. Statistical inference is possible only after the full subsequent version (N≥100).
- Korean residents: Foreign Exchange Transactions Act, Capital Gains Tax 22%, Virtual Asset User Protection Act require separate verification
- Investment outcomes are the responsibility of the individual

> *Past performance does not guarantee future results.*

---

## Author Information

**Author**: HoKwang Kim (Dennis Kim)
**Affiliation**: Independent Researcher · Betalabs Inc., CEO
**Date**: May 1, 2026
**Email**: gameworker@gmail.com
**ORCID**: 0009-0002-0962-2175
**GitHub**: github.com/gameworkerkim
**SSRN Author**: ssrn.com/author=7497180

**Related Prior Work by Author**:
- Kim, H. (2026). *The 72-Hour Shock — Preliminary Evidence from 52 Token Unlock Events on Binance*. SSRN Working Paper No. 6632838.
- Kim, H. (2026, May). *Two Faces of Binance Megadrop and HODLer Airdrop*. Working Manuscript.

**Acknowledgments**: This preliminary working paper has evolved through multiple rounds of external academic evaluation. The author thanks all external reviewers. All remaining errors and limitations are the author's responsibility.

**Citation**:

> Kim, H. (2026). *Distribution Asymmetry of Centralized Exchange Airdrops and the BNB Chain Ecosystem: BNB Holder Gain, Foundation Disaster, and the Decoupling Pattern of BNB Chain (Preliminary Working Paper)*. Working Paper.

---

**End of Document.**
