# Awesome Vibe Investing — 큐레이션 인덱스

AI 기반 투자 도구를 카테고리별로 평가한 큐레이션 리스트 모음입니다.

각 리스트는 단순 나열이 아니라 다음 기준으로 평가합니다.

- 강점, 약점, 적합한 사용자 유형
- 활성도 / 성숙도 / 학습곡선 / 한국 시장 적합성 / 라이선스
- 공통 함정과 주의점
- 사용자 유형별 시작 경로

> 영문 readers: 본 인덱스는 한국어로 작성되었으며, 일부 큐레이션은 한국어 본문입니다. 번역기를 사용해 주세요.
> English readers: this index is in Korean. Use a translator. Some curation lists are also Korean-only.

---

## 메인 레포로 돌아가기

→ [README.md](README.md) (한국어)
→ [README_EN.md](README_EN.md) (English)

---

## 1. Awesome Vibe Invest — Stocks & Equities

→ [전체 문서](Awesome%20vibe%20invest.MD)

NASDAQ / S&P500 분석을 위한 AI 도구 30+ 큐레이션.

다루는 12개 카테고리:

| 카테고리 | 내용 |
|---|---|
| 멀티 에이전트 프레임워크 | TradingAgents, FinRobot, AgenticTrading 등 |
| 강화학습 트레이딩 | RL 기반 알고리즘 트레이딩 도구 |
| 금융 LLM | 금융 특화 LLM 모델 |
| 백테스트 엔진 | 검증 도구 |
| MCP 인프라 | Model Context Protocol 활용 |
| 한국 시장 자원 | pyKRX, 한국투자증권 OpenAPI 등 |
| 공통 함정 | 백테스트, LLM hallucination, 운영, 거버넌스, 비용 등 12가지 |
| 사용자 유형별 시작 경로 | 5개 시나리오 |

언어: 한국어

---

## 2. Awesome Vibe Invest — Crypto & DeFi Edition

→ [전체 문서](Awesome%20vibe%20invest%20crypto.MD)

비트코인을 비롯한 암호화폐 LLM 트레이딩 큐레이션. 벤치마크 결과와 지속적 업데이트가 있는 프로젝트 중심 평가.

핵심 데이터 — Alpha Arena Season 1 결과:

| 순위 | 모델 | 성과 |
|---|---|---|
| 1위 | DeepSeek V3.1 | +46% (실제 자본 $10,000 → $14,764) |
| 2위 | Qwen3 Max | - |
| 3위 | Claude Sonnet 4.5 / Grok 4 | - |
| 하위 | Gemini 2.5 Pro | - |
| 하위 | GPT-5 | -75% |

핵심 결론: 모델 IQ가 곧 트레이딩 IQ는 아니다.

다루는 9개 카테고리:

1. 벤치마크 & 평가 인프라 (Nof1 Alpha Arena 등)
2. 학술 검증 LLM 트레이딩 (CryptoTrade EMNLP 2024 등)
3. 프로덕션 멀티 에이전트 봇
4. Solana 네이티브 AI 에이전트 (ElizaOS, Solana Agent Kit, GOAT, Rig)
5. 멀티체인 / EVM 에이전트 툴킷
6. MEV / DEX 전용 봇
7. 예측 시장 (Polymarket, Kalshi) AI 에이전트
8. 데이터 인프라 & 온체인 분석
9. 공통 함정 (Crypto 특화) — 24/7 시장, slippage, MEV, CEX 리스크

언어: 한국어

---

## 3. Awesome AI Quant Prompt — GitHub Repos Evaluation

→ [전체 문서](Awesome%20AI%20Quant%20Prompt%20github%20repos%20evaluation%20kr.MD)

AI 퀀트 프롬프트 엔지니어링을 다루는 GitHub 레포에 대한 한국어 평가.

언어: 한국어

---

## 4. Awesome Vibe Trading Bot

→ [전체 문서](Awesome%20Vibe%20Trading%20Bot.MD)

자연어 기반 트레이딩 봇 큐레이션.

언어: 한국어

---

## 추천 시작 경로

| 관심 영역 | 추천 리스트 |
|---|---|
| 미국 주식 (NASDAQ / S&P500) | 1번 |
| 가상화폐 / DeFi | 2번 |
| AI 퀀트 프롬프트 엔지니어링 | 3번 |
| 트레이딩 봇 일반 | 4번 |

각 리스트의 "추천 시작 경로" 또는 "공통 함정" 섹션을 가장 먼저 읽으세요. 레포 스타 수가 곧 품질이 아니며, 학술 논문 기반이라고 실전에서 작동하는 것도 아닙니다.

---

## 평가 원칙

이 큐레이션 시리즈가 다른 awesome 리스트와 다른 점:

- **단순 링크 나열이 아닌 평가** — 각 항목에 강점, 약점, 적합 사용자 명시
- **5축 정량 평가** — 활성도, 성숙도, 학습곡선, 한국 시장 적합성, 라이선스
- **공통 함정 명시** — 각 리스트에 카테고리 특유의 함정을 별도 섹션으로 정리
- **사용자 유형별 진입로** — 초보 / 개인 트레이더 / 헤지펀드 / 학술 연구자 등

---

## 기여하기

- 누락된 좋은 레포 제보 — 이슈 또는 PR 환영
- 평가에 대한 반박 — 토론은 큐레이션 품질을 높입니다
- 본인 백테스트 결과 공유 — 큐레이션 항목들의 walk-forward 결과
