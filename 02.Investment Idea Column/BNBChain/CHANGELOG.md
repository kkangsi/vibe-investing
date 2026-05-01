# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-05-01

### Added
- Initial GitHub release with full reproducibility package
- 7 publication-grade figures (PNG + PDF) generated from Python source
- DOCX with embedded figures and academic captions
- 4 CSV data files with verified sources
- 4 analysis scripts + 7 figure generation scripts (all English)
- MIT (code) + CC BY 4.0 (data/paper) dual licensing
- CITATION.cff for academic citation support
- Comprehensive README with reproducibility instructions
- Data dictionary and figures insertion guide

### Notable Methodology
- Bootstrap 95% CI with N=10,000 iterations
- Hyperliquid HYPE counterfactual case included (Direct N=2 → N=3)
- Cohen's d normalized from -10.665 (artifact, N=2) to -1.519 (N=3 with HYPE)
- Three-actor differential impact analysis ($1.69B holder gain, $4.80B foundation loss, $104B BNB Chain market cap growth)
- Decoupling pattern observation with explicit causality non-establishment

## Pre-release Versions (Internal Development)

### [v0.5] - 2026-04-28
- Korean-language draft completed (~9,600 words)
- N=18 token sample without HYPE
- Bootstrap CI calculated for N=18 sample
- Cohen's d Megadrop vs Direct (N=2) = -10.665 (flagged as artifact)
- External academic evaluation requested

### [v0.4] - 2026-04-25
- Theorem 6 (Foundation Break-Even Impossibility) proof completed
- Theorem 7 (Nash Equilibrium) proof completed
- Section 4.10 scenario analysis added (α 2-15%, θ 30-60%, d 10-90%)

### [v0.3] - 2026-04-22
- Section 7 BNB Chain decoupling pattern observed
- Messari Q1-Q3 2025 data integration

### [v0.2] - 2026-04-18
- Theorems 1-5 (Foundation Cost Function) developed
- Megadrop, HODLer, Launchpool category definitions

### [v0.1] - 2026-04-15
- Initial concept: distribution mechanism asymmetry hypothesis
- Companion to SSRN 6632838 ("The 72-Hour Shock")

## Roadmap (Subsequent Versions)

### [v1.1] (planned)
- Expanded sample to N≥50 tokens
- Daily OHLCV data integration via CoinGecko/Binance APIs
- Real Granger causality testing (Section 7 limitation 6 resolution)

### [v2.0] (planned)
- Sample size N≥100
- Propensity Score Matching (PSM) for selection bias
- Heckman 2-step estimation
- Multi-exchange comparison (Bybit, OKX, Coinbase listings)
- LaTeX paper compilation for journal submission

## Citation Note

For academic citation, please use the metadata in [CITATION.cff](CITATION.cff)
or the BibTeX template in the [README.md](README.md).

When citing v1.0 specifically, please use:
> Kim, H. (2026). Distribution Asymmetry of Centralized Exchange Airdrops and the
> BNB Chain Ecosystem (v1.0) [Preliminary working paper and dataset]. GitHub.
> https://github.com/gameworkerkim/distribution-asymmetry-cex-airdrops
