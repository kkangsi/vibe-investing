// instruments.js
// ==============
// 차익거래 봇의 종목 유니버스. KRX 6자리 코드(토스/KIS 모두 동일).
//
// 가설: 삼성전자 + SK하이닉스가 KOSPI200의 ~55%를 차지하므로, 이 두 종목의
//       (추세 확인된) 움직임은 KOSPI200을 추종하는 현물/레버리지/인버스 ETF의
//       향후 움직임을 선행(lead)한다. ETF가 아직 반영하지 못한 구간 = 차익거래 창.
//
// 비중은 2026년 기준 KOSPI200 지수 내 추정 가중치. 정확치는 KRX/지수사업자 공시로
// 갱신할 것. composite(합성 지수 프록시) 계산에만 쓰이며 INDEX_WEIGHT 합은 1 미만이다
// (나머지 ~45%는 관측하지 않는 잔차 — 그래서 composite는 '정확한 지수'가 아니라
//  '선행 예측자'로만 사용한다).

// 빅2 — 합성 KOSPI200 프록시의 입력.
export const DRIVERS = [
  { code: '005930', name: '삼성전자',     indexWeight: 0.33 },
  { code: '000660', name: 'SK하이닉스',   indexWeight: 0.22 },
];

// 추종 상품 — 빅2 대비 lead-lag/괴리를 감시할 대상.
//   leverage: KOSPI200 일일수익률 배수(현물 1x, 레버리지 +2x, 인버스 -1x/-2x).
//   kind: 'spot' | 'leverage' | 'inverse'
export const TRACKERS = [
  { code: '069500', name: 'KODEX 200',            kind: 'spot',     leverage:  1 },
  { code: '102110', name: 'TIGER 200',            kind: 'spot',     leverage:  1 },
  { code: '122630', name: 'KODEX 레버리지',        kind: 'leverage', leverage:  2 },
  { code: '114800', name: 'KODEX 인버스',          kind: 'inverse',  leverage: -1 },
  { code: '252670', name: 'KODEX 200선물인버스2X', kind: 'inverse',  leverage: -2 },
];

// 폴링/표시에 필요한 전체 코드 목록.
export const ALL_CODES = [...DRIVERS, ...TRACKERS].map((x) => x.code);

// 코드 → 메타 빠른 조회.
export const META = new Map(
  [...DRIVERS.map((d) => ['driver', d]), ...TRACKERS.map((t) => ['tracker', t])].map(
    ([role, x]) => [x.code, { ...x, role }],
  ),
);

// 빅2의 지수 가중치 합 — composite 정규화에 사용.
export const DRIVER_WEIGHT_SUM = DRIVERS.reduce((s, d) => s + d.indexWeight, 0);

export function nameOf(code) {
  return META.get(code)?.name ?? code;
}
