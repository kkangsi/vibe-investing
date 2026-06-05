// signal.js
// =========
// 차익거래 시그널 엔진.
//
// 아이디어:
//   1) 빅2(삼성·하이닉스)의 타임프레임 수익률을 지수 가중으로 합성 → compositeRet.
//      이는 KOSPI200이 '방금 어디로 움직였는지'에 대한 선행 추정치다(빅2가 55%).
//   2) 각 추종 ETF의 '기대 수익률' = leverage × (compositeRet / DRIVER_WEIGHT_SUM).
//      (빅2 가중합을 그 비중으로 나눠 지수 전체 움직임으로 환산. 잔차 45%는 미관측
//       이므로 근사치임 — 그래서 임계값과 추세확인으로 노이즈를 걸러낸다.)
//   3) gap = 기대 수익률 − 실제 ETF 수익률.
//      |gap|이 임계값을 넘고, 빅2 추세가 confirmed이며, 지정한 '확인 타임프레임들'에서
//      동시에 성립하면 → ETF가 아직 못 따라온 lead-lag 차익거래 창으로 본다.
//
// 방향:
//   gap > 0  → ETF가 (레버리지 부호 고려) 기대보다 덜 올랐다 → ETF 상승 여력(롱 후보)
//   gap < 0  → ETF가 기대보다 덜 내렸다/과도하게 올랐다 → ETF 하락 여력(숏/회피 후보)

import { DRIVERS, TRACKERS, DRIVER_WEIGHT_SUM, nameOf } from './instruments.js';

export const DEFAULT_CONFIG = {
  // 추세 확인용 파라미터(bars.trendOf로 전달).
  trend: { lookback: 4, minRet: 0.0012, minConsistency: 0.6 },
  // 차익거래로 인정할 최소 gap(기대-실제 수익률 차).
  gapThreshold: 0.0015, // 0.15%
  // 이 타임프레임들 '모두'에서 동시에 성립해야 발화 → 초단기 노이즈 차단.
  confirmTimeframes: ['60s', '2m'],
  // 빅2 추세가 confirmed여야 하는 기준 타임프레임.
  driverTimeframe: '60s',
  // 괴리율(iNAV) 신호 파라미터.
  disparity: { band: 0.003, lookback: 5, minConsistency: 0.8 }, // band 0.3%
};

// 빅2 합성 수익률(특정 타임프레임). null이면 데이터 부족.
function compositeReturn(board, tfKey, trendCfg) {
  let acc = 0;
  let confirmedCount = 0;
  for (const d of DRIVERS) {
    const inst = board.get(d.code);
    const tr = inst?.trendOf(tfKey, trendCfg);
    if (!tr) return null;
    acc += d.indexWeight * tr.ret;
    if (tr.confirmed) confirmedCount++;
  }
  return { weightedRet: acc, indexRet: acc / DRIVER_WEIGHT_SUM, driversConfirmed: confirmedCount };
}

// 한 ETF에 대해 한 타임프레임의 gap을 계산.
function gapFor(board, tracker, tfKey, trendCfg) {
  const comp = compositeReturn(board, tfKey, trendCfg);
  const inst = board.get(tracker.code);
  const tr = inst?.trendOf(tfKey, trendCfg);
  if (!comp || !tr) return null;
  const expected = tracker.leverage * comp.indexRet;
  const gap = expected - tr.ret;
  return { expected, actual: tr.ret, gap, indexRet: comp.indexRet, etfTrend: tr };
}

// 전체 평가. 발화 조건을 만족한 시그널 배열을 반환.
export function evaluate(board, config = DEFAULT_CONFIG) {
  const { trend, gapThreshold, confirmTimeframes, driverTimeframe } = config;
  const out = [];

  // 빅2 추세가 기준 타임프레임에서 확실히 살아있어야 한다.
  const driverComp = compositeReturn(board, driverTimeframe, trend);
  const driversOk = driverComp && driverComp.driversConfirmed >= 1 &&
    Math.abs(driverComp.indexRet) >= trend.minRet;

  for (const tracker of TRACKERS) {
    const perTf = {};
    let allConfirm = true;
    let signedGapSum = 0;

    for (const tfKey of confirmTimeframes) {
      const g = gapFor(board, tracker, tfKey, trend);
      perTf[tfKey] = g;
      if (!g || Math.abs(g.gap) < gapThreshold || Math.sign(g.gap) !== Math.sign(perTf[confirmTimeframes[0]]?.gap ?? g.gap)) {
        allConfirm = false;
      }
      if (g) signedGapSum += g.gap;
    }

    if (!driversOk || !allConfirm) continue;

    const gap = signedGapSum / confirmTimeframes.length;
    const dir = Math.sign(gap);
    // ETF 종류에 따른 사람이 읽을 액션.
    const action = dir > 0
      ? (tracker.kind === 'inverse' ? 'ETF 하락분 미반영 → 인버스 상승여력(롱 후보)' : 'ETF 상승 미반영 → 롱 후보')
      : (tracker.kind === 'inverse' ? '인버스 과도상승 → 하락 되돌림(숏/회피)' : 'ETF 과도/괴리 → 숏·회피 후보');

    out.push({
      type: 'LEADLAG',
      code: tracker.code,
      name: nameOf(tracker.code),
      kind: tracker.kind,
      leverage: tracker.leverage,
      indexRet: driverComp.indexRet,
      driversConfirmed: driverComp.driversConfirmed,
      gap,
      direction: dir > 0 ? 'UP' : 'DOWN',
      action,
      perTf,
    });
  }

  // gap 절댓값 큰 순.
  out.sort((a, b) => Math.abs(b.gap) - Math.abs(a.gap));
  return { driverComp, signals: out };
}

// 괴리율(iNAV vs 시장가) 차익거래 신호.
//   disp = (시장가 − NAV)/NAV. 지속적 프리미엄/디스카운트를 되돌림 기회로 본다.
//   disp>0(프리미엄, 고평가) → 시장가 하락 되돌림 예상(숏/회피)
//   disp<0(디스카운트, 저평가) → 시장가 상승 되돌림 예상(롱 후보)
export function evaluateDisparity(board, config = DEFAULT_CONFIG) {
  const cfg = config.disparity || DEFAULT_CONFIG.disparity;
  const out = [];
  for (const tracker of TRACKERS) {
    const inst = board.get(tracker.code);
    const d = inst?.disparityOf(cfg);
    if (!d || !d.confirmed) continue;
    const dir = Math.sign(d.disp);
    out.push({
      type: 'DISPARITY',
      code: tracker.code,
      name: nameOf(tracker.code),
      kind: tracker.kind,
      leverage: tracker.leverage,
      disparity: d.disp,
      consistency: d.consistency,
      // 되돌림 방향: 프리미엄이면 하락(DOWN), 디스카운트면 상승(UP).
      direction: dir > 0 ? 'DOWN' : 'UP',
      action: dir > 0
        ? `시장가 NAV 대비 프리미엄(고평가) → 하락 되돌림(숏/회피)`
        : `시장가 NAV 대비 디스카운트(저평가) → 상승 되돌림(롱 후보)`,
    });
  }
  out.sort((a, b) => Math.abs(b.disparity) - Math.abs(a.disparity));
  return { signals: out };
}
