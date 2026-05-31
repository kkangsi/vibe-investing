# ExxonMobil (XOM) Multi-Factor Quant

엑슨모빌(XOM)에 대한 **재현 가능한 팩터 기반 매수/보유/매도 판정** 프레임워크입니다. "석유의 시대가 저문다"는 서사에도 불구하고, 유가 비탄력성·정유 과점·문명의 석유 의존이라는 구조적 사실 위에서 XOM을 **페트로달러에 투자하는 가장 직관적이고 지루하며 실패가 적은 전략**으로 다룹니다. 설계 원칙: *"LLM은 엑셀이지 오라클이 아니다."*

A reproducible, factor-based **buy / hold / sell** framework for ExxonMobil (XOM), framing it as the most intuitive, boring, and low-failure way to invest in the petrodollar — grounded in oil-price inelasticity, the refining oligopoly, and civilization's dependence on oil. Design principle: *"An LLM is Excel, not an oracle."*

---

## 문서 (Documents)

| 문서 | 설명 | Description |
| --- | --- | --- |
| [`ExxonMobil_quant_thesis_KR.md`](./ExxonMobil_quant_thesis_KR.md) | 투자 컨셉·통계·프롬프트 해설 (한국어) | Investment concept, statistics & prompt guide (Korean) |
| [`ExxonMobil_quant_thesis_EN.md`](./ExxonMobil_quant_thesis_EN.md) | 투자 컨셉·통계·프롬프트 해설 (영어) | Investment concept, statistics & prompt guide (English) |
| [`ExxonMobil_quant_prompt.md`](./ExxonMobil_quant_prompt.md) | 3개 국어 멀티팩터 의사결정 프롬프트 (KR/EN/CN) | Trilingual multi-factor decision prompt |
| [`ExxonMobil_insight.md`](./ExxonMobil_insight.md) | 팩터별 정성 분석 (원본 인사이트) | Factor-by-factor qualitative analysis (original insight) |
| [`llms.txt`](./llms.txt) | LLM·검색 인덱스 요약 | LLM / search index summary |

> 권장 읽기 순서: **insight → thesis(KR/EN) → prompt**.
> Recommended reading order: **insight → thesis (KR/EN) → prompt**.

---

## 핵심 통계 (Key Statistics)

- **호르무즈 / Hormuz**: 전 세계 석유·가스의 약 20% 통과. 2026년 사태로 Brent 약 40~50% 급등. (Dallas Fed: 공급 20% 제거 시 WTI ~$98, 글로벌 GDP −2.9%p)
- **정유 과점 / Refining oligopoly**: 캘리포니아 상위 4사 약 90%(→약 98%), 미국 그 외 상위 4사 약 48%, 미국 CR4 약 46%. 글로벌 통합 메이저 처리량 25% 미만, NOC 약 53%.
- **곡물·석유 / Food–oil**: 하버-보슈 합성질소비료가 약 38억 명을 먹여 살림. 질소비료 비용의 약 90%가 천연가스.
- **수요 정점 / Peak demand**: IEA WEO 2025 현행정책 시 2050년 약 113 mb/d(+13%), OPEC 약 123 mb/d, IEA STEPS는 2030 정점.
- **XOM 주주환원 / Shareholder returns**: 43년 연속 배당 인상, 연 배당 약 $4.12(수익률 약 2.7%), 2026 자사주 약 $200억, 총 주주환원 연 약 $370억(주주환원수익률 약 6%, 멀티플 포함 총기대수익률 8.5~9.5%).

---

## 면책 (Disclaimer)

본 자료는 정보 제공 목적이며 투자 자문 또는 매매 권유가 아닙니다. 모든 투자 판단과 책임은 투자자 본인에게 있습니다.
This material is for informational purposes only and is not investment advice or a solicitation. All investment decisions and responsibility rest with the investor.

*Author: HoKwang Kim (Dennis Kim) · vibe-investing · 2026-05-31*
