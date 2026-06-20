# Prompt 02 — 반도체 슈퍼사이클 × 대만 ETF 투자 시나리오 백테스트

`backtest.py` 결과를 재현하는 프롬프트.

---

당신은 시스템 트레이딩 퀀트다. 가설을 검정하라.

**가설**: "TSMC 월간 매출은 대만 경제/증시의 선행지표다. 따라서 TSMC 매출
모멘텀으로 대만 ETF(EWT) 노출을 타이밍하면 단순 매수후보유 대비 위험조정수익을
개선할 수 있다."

**전략 — TSMC-Momentum Timing**
- 신호: TSMC 매출 YoY 의 3개월 변화(가속도, `tsmc_mom3`).
- mom3 > 0 → 사이클 가속 → EWT 비중 100%. mom3 ≤ 0 → 사이클 둔화 → 50% 축소.
- **룩어헤드 방지**: 신호는 전월 값으로 당월 포지션 결정(`shift(1)`).
  TSMC 월매출은 익월 10일 전후 공시되므로 실거래 가능한 정보 시차다.
- 벤치마크: EWT Buy & Hold (항상 100%).

**평가**
- CAGR, 연변동성, Sharpe(rf=0), MDD, 누적수익, 회전수, 풀롱 비중.
- 자산곡선 + 하단에 EWT 비중을 그린 `backtest_equity.png` 저장.
- `backtest_metrics.json` 저장.

**중요 — 결과를 정직하게 보고하라**
- 전략이 벤치마크를 *이기지 못하면* 이긴다고 쓰지 마라. 왜 이기지 못했는지
  (둔화 구간 비중축소가 회복 초입의 V자 반등을 놓침, 슈퍼사이클에서 항상-롱이
  유리) 설명하라.
- 시나리오 3종을 논하라: (a) 항상-롱(슈퍼사이클 베팅), (b) 모멘텀 타이밍,
  (c) 다운사이클 방어(모멘텀 붕괴 시에만 축소). 각각의 적합 투자자 성향을 적시.

산출물: `backtest.py`, `results/backtest_metrics.json`,
`results/backtest_timeseries.csv`, `results/backtest_equity.png`.
