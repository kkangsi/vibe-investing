# LAON VaultGuard

> LLM-based Automated Observer for Non-public Keys

LAON VaultGuard is a cross-platform security auditing platform that detects hardcoded cloud credentials, API keys, tokens, and secrets before they reach public Git repositories.

## Features

- Multi-LLM secret detection (OpenAI, DeepSeek, MiniMax, Mimo)
- GitHub, GitLab, and local repository monitoring
- REST API and web dashboard
- Slack, Telegram, and Email alerts
- SQLite-based audit trail
- Cross-platform (Windows, Linux, macOS)

## Architecture

See: docs/Architecture.md

## API

See: docs/API.md

## Database

See: docs/Database.md

## Technology Stack

- Node.js
- Express.js
- SQLite
- simple-git
- node-cron

## Roadmap

- [ ] GitHub App integration
- [ ] VSCode extension
- [ ] SIEM integration
- [ ] Kubernetes deployment

## License

MIT
