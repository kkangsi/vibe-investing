// amqs.js
// =======
// Adaptive Momentum Quant Strategy (AMQS) 시그널 엔진 — JS 포팅.
// 원본: 01.Trading Strategy/Adaptive Momentum Quant Strategy (AMQS)/live_momentum_screener.py
//
// 4-Factor Composite 모멘텀:
//   score = 0.50·Z(12-1) + 0.30·Z(6-1) + 0.15·Z(3-1) + 0.05·Z(1/Vol)
//   - Z() : universe 내 횡단면 z-score 정규화
//   - 12-1 : 12개월 전 → 1개월 전 수익률 (최근 1개월 제외 = 단기 평균회귀 차단)
//   - Vol  : 60일 실현 변동성(연환산)
//
// 국내 적용(원본 대비 변경점):
//   - 레짐 벤치마크: QQQ → KODEX 200(KOSPI200 프록시)
//   - VIX 미제공 → 지수 20일 실현 변동성을 변동성 게이지로 대체
//   엔진 로직(가중치/룩백/손절)은 원본과 동일.

const TRADING_DAYS = 252;

// 캔들 배열(과거→현재, 각 원소 { close })에서 종가 시계열만 추출.
function closes(candles) {
  return candles.map((c) => c.close).filter((v) => typeof v === 'number' && v > 0);
}

// n 거래일 전 종가 (인덱스 기준).
function priceNDaysAgo(series, n) {
  const idx = Math.max(0, series.length - 1 - n);
  return series[idx];
}

// 단순 수익률.
function ret(a, b) {
  if (!a || !b) return null;
  return a / b - 1;
}

// 연환산 실현 변동성 (마지막 window 거래일).
function realizedVol(series, window = 60) {
  const tail = series.slice(-window - 1);
  if (tail.length < 5) return null;
  const rets = [];
  for (let i = 1; i < tail.length; i++) rets.push(tail[i] / tail[i - 1] - 1);
  const mean = rets.reduce((s, r) => s + r, 0) / rets.length;
  const variance = rets.reduce((s, r) => s + (r - mean) ** 2, 0) / rets.length;
  return Math.sqrt(variance) * Math.sqrt(TRADING_DAYS);
}

// 한 종목의 원시(raw) 모멘텀 팩터 계산. z-score 정규화 전 단계.
export function rawFactors(candles) {
  const series = closes(candles);
  if (series.length < 30) return null;
  const last = series[series.length - 1];

  // 거래일 기준 근사: 1M≈21, 3M≈63, 6M≈126, 12M≈252.
  const p1 = priceNDaysAgo(series, 21);
  const p3 = priceNDaysAgo(series, 63);
  const p6 = priceNDaysAgo(series, 126);
  const p12 = priceNDaysAgo(series, Math.min(252, series.length - 1));

  const ret_12_1 = ret(p1, p12);
  const ret_6_1 = ret(p1, p6);
  const ret_3_1 = ret(p1, p3);
  const vol60 = realizedVol(series, 60);

  // 60일 추적 고점 — 손절(트레일링 스탑) 판단용.
  const trailWindow = series.slice(-60);
  const trailingHigh = Math.max(...trailWindow);

  return {
    price: last,
    ret_12_1,
    ret_6_1,
    ret_3_1,
    vol60,
    inv_vol: vol60 ? 1 / vol60 : null,
    trailingHigh,
    dataDays: series.length,
  };
}

// 횡단면 z-score: 값 배열 -> z 배열. 결측은 평균(=0)으로 보정.
function zscores(values) {
  const valid = values.filter((v) => v != null && Number.isFinite(v));
  if (valid.length < 3) return values.map(() => 0);
  const mean = valid.reduce((s, v) => s + v, 0) / valid.length;
  const sd = Math.sqrt(valid.reduce((s, v) => s + (v - mean) ** 2, 0) / valid.length) || 1;
  return values.map((v) => (v != null && Number.isFinite(v) ? (v - mean) / sd : 0));
}

// universe 전체에 대해 4-factor composite z-score + 0~100 모멘텀 점수 부여.
// items: [{ code, name, ..., factors }]  (factors = rawFactors 결과)
export function scoreUniverse(items) {
  const f = items.map((it) => it.factors || {});
  const z12 = zscores(f.map((x) => x.ret_12_1));
  const z6 = zscores(f.map((x) => x.ret_6_1));
  const z3 = zscores(f.map((x) => x.ret_3_1));
  const zv = zscores(f.map((x) => x.inv_vol));

  const composite = items.map((_, i) => 0.5 * z12[i] + 0.3 * z6[i] + 0.15 * z3[i] + 0.05 * zv[i]);

  const min = Math.min(...composite);
  const max = Math.max(...composite);
  const span = max - min || 1;

  return items.map((it, i) => ({
    ...it,
    composite_z: round(composite[i], 3),
    momentum_score: round(((composite[i] - min) / span) * 100, 1),
  }));
}

// 시장 레짐 판단 (KODEX 200 프록시 기반).
// benchmarkCandles: 국면 벤치마크 일봉(과거→현재).
export function determineRegime(benchmarkCandles) {
  const series = closes(benchmarkCandles);
  if (series.length < 20) {
    return { regime: 'UNKNOWN', label: '판정 불가', reason: '데이터 부족', action: '데이터 확보 후 재평가' };
  }
  const now = series[series.length - 1];
  const ma200 = movingAverage(series, Math.min(200, series.length));
  const ret5d = series.length >= 6 ? (now / series[series.length - 6] - 1) * 100 : 0;
  const vol20 = (realizedVol(series, 20) || 0) * 100;

  let regime, label, action;
  if (ret5d < -8) {
    regime = 'DEFENSIVE';
    label = '방어';
    action = '방어 바스켓으로 회전 · 신규 모멘텀 매수 중단';
  } else if (now < ma200 || vol20 > 30) {
    regime = 'RISK_OFF';
    label = '위험 회피';
    action = '주식 비중 50%로 축소 · 현금 버퍼 확보';
  } else {
    regime = 'RISK_ON';
    label = '위험 선호';
    action = 'Top 모멘텀 종목 풀 투자';
  }

  return {
    regime,
    label,
    action,
    benchmark: round(now, 2),
    ma200: round(ma200, 2),
    pct_above_ma200: round((now / ma200 - 1) * 100, 2),
    ret_5d_pct: round(ret5d, 2),
    vol_20d_ann_pct: round(vol20, 2),
  };
}

// 개별 종목 시그널: 매수 / 보유 / 매도.
// scored: scoreUniverse 결과 1개 원소, regime: determineRegime 결과.
export function signalFor(scored, regime) {
  const f = scored.factors || {};
  const z = scored.composite_z ?? 0;
  const price = f.price;
  const stopPrice = price ? round(price * 0.88, 2) : null; // -12% 손절선
  const drawdownFromHigh = f.trailingHigh && price ? (price / f.trailingHigh - 1) * 100 : 0;
  const reasons = [];

  let signal = 'HOLD';

  // 1) 트레일링 스탑: 60일 고점 대비 -12% 이탈 → 매도
  if (drawdownFromHigh <= -12) {
    signal = 'SELL';
    reasons.push(`60일 고점 대비 ${round(drawdownFromHigh, 1)}% → 손절선 이탈`);
  } else if (z >= 0.5) {
    signal = 'BUY';
    reasons.push(`모멘텀 z=${z} (상위권)`);
  } else if (z <= -0.5) {
    signal = 'SELL';
    reasons.push(`모멘텀 z=${z} (하위권, 추세 약화)`);
  } else {
    signal = 'HOLD';
    reasons.push(`모멘텀 z=${z} (중립권)`);
  }

  // 2) 레짐 오버레이
  if (regime.regime === 'DEFENSIVE') {
    if (signal === 'BUY') reasons.push('레짐 방어 → 신규 매수 보류');
    signal = signal === 'SELL' ? 'SELL' : 'AVOID';
  } else if (regime.regime === 'RISK_OFF' && signal === 'BUY') {
    signal = 'HOLD';
    reasons.push('레짐 위험회피 → 매수 강도 하향(보유)');
  }

  return {
    signal,
    momentum_score: scored.momentum_score,
    composite_z: z,
    price,
    stop_price: stopPrice,
    drawdown_from_high_pct: round(drawdownFromHigh, 1),
    ret_12_1_pct: f.ret_12_1 != null ? round(f.ret_12_1 * 100, 1) : null,
    ret_6_1_pct: f.ret_6_1 != null ? round(f.ret_6_1 * 100, 1) : null,
    ret_3_1_pct: f.ret_3_1 != null ? round(f.ret_3_1 * 100, 1) : null,
    vol_60d_ann_pct: f.vol60 != null ? round(f.vol60 * 100, 1) : null,
    reason: reasons.join(' · '),
  };
}

function movingAverage(series, window) {
  const tail = series.slice(-window);
  return tail.reduce((s, v) => s + v, 0) / tail.length;
}

function round(v, d = 2) {
  if (v == null || !Number.isFinite(v)) return null;
  const m = 10 ** d;
  return Math.round(v * m) / m;
}
