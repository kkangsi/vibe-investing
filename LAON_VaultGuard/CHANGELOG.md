# CHANGELOG

## v0.5.0 (2026-06-07) — Production Release

### 🚀 New Features

**Storage Engine**
- Dual-engine architecture: **SQLite** (WAL, ACID) + JSON (legacy, single-device only)
- `npm run migrate` — one-click JSON → SQLite migration
- Runtime engine switch via `STORAGE_ENGINE=sqlite|json`

**Differential Privacy**
- 14 secret masking rules before LLM transmission
- `DP_ENABLED=true` by default — zero code exfiltration guarantee

**SARIF v2.1.0 Export**
- `npm run export-sarif` — GitHub Code Scanning / GitLab SAST compatible
- Severity → level mapping, confidence → rank scoring

**Prometheus Metrics**
- `/metrics` endpoint — counters, gauges, histograms
- No external dependency (prom-client not needed)

**Docker**
- Multi-stage Alpine image with better-sqlite3 native compilation
- `docker-compose up -d` + `--profile ollama` for GPU LLM

**VS Code Extension**
- Real-time secret highlighting (13 patterns)
- Problems panel integration (masked fingerprints only)
- Deep LLM scan via `Cmd+Shift+P`

**Setup Wizard**
- Multi-select LLM providers (DeepSeek, Claude, ChatGPT, Ollama)
- Ollama auto-detection + install guide + 5-model comparison table
- 4-language i18n: 한국어 / English / 中文 / 日本語

**Pre-commit Hook**
- `npx laon-vaultguard hook install` — blocks commits with secrets
- Fast regex scan (<1s, no LLM), bypass via `--no-verify`

**Feedback Loop**
- `PUT /api/findings/:id/feedback` — accurate / false_positive
- Feedback stats endpoint for few-shot prompt improvement

**Dashboard Auth**
- `DASHBOARD_TOKEN` Bearer token protection on mutating APIs

**PDF Export**
- `GET /api/report/pdf` — print-optimized, severity color coded

**Security Fixed**
- LLM retry: `maxRetries: 3` (exponential backoff on 429/5xx)
- JSON file lock: atomic write + exclusive lock (TOCTOU protection)

**npm Package**
- Published: `npx create-laon-vaultguard` — interactive setup
- Published: `npx laon-vaultguard scan .` — CLI scanhttps://www.npmjs.com/package/laon-vaultguard

### 📊 Backtest
- `npm run backtest` → **54/54 tests passed**
- Full checklist: [docs/BACKTEST_CHECKLIST.md](docs/BACKTEST_CHECKLIST.md)

### 📚 Documentation
- 4-language READMEs (KO/EN/ZH/JA) with npm badges
- CLI manual updated: hook, SARIF, alerts, report endpoints
- Semgrep integration guide: LAON as scan orchestrator
- SaaS transition strategy: market analysis + 30-day GTM plan

### 🔧 Bug Fixes (from v0.4 code review)
- `llm-harness.ts`: timeoutId hoisted, schema validation + cleartext guard
- `cli.ts`: version display fixed to v0.5.0
- `scan-runner.ts`: md5 → sha256 (FIPS-compatible)
- `candidate-filter.ts`: git grep error handling fixed
- `git-monitor.ts`: dead filePattern removed, token-in-URL replaced with .netrc
- ARDS-Defense: duplicate lowercase `readme.md` removed

---

## v0.4.0 (2026-06-07) — Bug Patch + Design Review

### 🔧 Bug Fixes (7 code-level)
- `llm-harness.ts`: timeout → WAL concurrency fix
- `cli.ts`: version v0.2.0 → v0.4.0
- `scan-runner.ts`: md5 → sha256
- `candidate-filter.ts`: simple-git error handling
- `git-monitor.ts`: dead code removal + token security
- `llm-harness.ts`: schema validation + cleartext guard

### 📚 Documentation
- DEVELOPMENT.md §8~§9 design improvements + priority actions
- README v0.4 completed, v0.5 planned

---

## v0.3.0 — Performance & Accuracy

- Incremental scan caching (file hash)
- 2-Tier LLM: lightweight → heavyweight
- Batch processing (50 candidates/chunk)
- Shannon entropy pre-filter
- Context risk classification
- Log rotation (LOG_RETENTION_DAYS)

## v0.2.0 — Cross-platform + Email Reports

- macOS / Linux / Windows (WSL) support
- Nodemailer email alerts (realtime/daily/weekly)
- GitHub OAuth + remote repo support
- Alert configuration UI

## v0.1.0 — Initial Release

- Multi-LLM secret scanning harness
- Git grep candidate filter
- Web dashboard with SSE
- Telegram/Slack alert integration
