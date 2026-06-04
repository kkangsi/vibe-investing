// universe.js
// ============
// 한국인이 선호하는 국내 주식(섹터별 10종목) + 인기 ETF 10종목.
// 종목코드는 KRX 6자리 표준코드(토스 Open API symbols 파라미터에 그대로 사용).
//
// 선정 기준: 2026년 기준 개인투자자 거래·보유 상위 + 증권사 톱픽으로 자주 언급되는
// 섹터 대표주 위주. 시장 상황에 맞게 종목을 자유롭게 교체해도 엔진은 동일하게 동작.

export const SECTORS = [
  {
    key: 'semiconductor',
    name: '반도체 / AI',
    stocks: [
      { code: '005930', name: '삼성전자' },
      { code: '000660', name: 'SK하이닉스' },
      { code: '042700', name: '한미반도체' },
      { code: '000990', name: 'DB하이텍' },
      { code: '058470', name: '리노공업' },
      { code: '039030', name: '이오테크닉스' },
      { code: '240810', name: '원익IPS' },
      { code: '036930', name: '주성엔지니어링' },
      { code: '403870', name: 'HPSP' },
      { code: '399720', name: '가온칩스' },
    ],
  },
  {
    key: 'battery',
    name: '2차전지 / 소재',
    stocks: [
      { code: '373220', name: 'LG에너지솔루션' },
      { code: '006400', name: '삼성SDI' },
      { code: '005490', name: 'POSCO홀딩스' },
      { code: '247540', name: '에코프로비엠' },
      { code: '086520', name: '에코프로' },
      { code: '003670', name: '포스코퓨처엠' },
      { code: '066970', name: '엘앤에프' },
      { code: '096770', name: 'SK이노베이션' },
      { code: '005070', name: '코스모신소재' },
      { code: '121600', name: '나노신소재' },
    ],
  },
  {
    key: 'auto',
    name: '자동차 / 부품',
    stocks: [
      { code: '005380', name: '현대차' },
      { code: '000270', name: '기아' },
      { code: '012330', name: '현대모비스' },
      { code: '204320', name: 'HL만도' },
      { code: '161390', name: '한국타이어앤테크놀로지' },
      { code: '011210', name: '현대위아' },
      { code: '005850', name: '에스엘' },
      { code: '307950', name: '현대오토에버' },
      { code: '018880', name: '한온시스템' },
      { code: '073240', name: '금호타이어' },
    ],
  },
  {
    key: 'internet_game',
    name: '인터넷 / 게임',
    stocks: [
      { code: '035420', name: 'NAVER' },
      { code: '035720', name: '카카오' },
      { code: '259960', name: '크래프톤' },
      { code: '036570', name: '엔씨소프트' },
      { code: '251270', name: '넷마블' },
      { code: '293490', name: '카카오게임즈' },
      { code: '263750', name: '펄어비스' },
      { code: '112040', name: '위메이드' },
      { code: '192080', name: '더블유게임즈' },
      { code: '194480', name: '데브시스터즈' },
    ],
  },
  {
    key: 'bio',
    name: '바이오 / 제약',
    stocks: [
      { code: '207940', name: '삼성바이오로직스' },
      { code: '068270', name: '셀트리온' },
      { code: '000100', name: '유한양행' },
      { code: '128940', name: '한미약품' },
      { code: '326030', name: 'SK바이오팜' },
      { code: '196170', name: '알테오젠' },
      { code: '141080', name: '리가켐바이오' },
      { code: '028300', name: 'HLB' },
      { code: '214150', name: '클래시스' },
      { code: '087010', name: '펩트론' },
    ],
  },
  {
    key: 'defense_ship',
    name: '방산 / 조선',
    stocks: [
      { code: '012450', name: '한화에어로스페이스' },
      { code: '064350', name: '현대로템' },
      { code: '079550', name: 'LIG넥스원' },
      { code: '047810', name: '한국항공우주' },
      { code: '329180', name: 'HD현대중공업' },
      { code: '042660', name: '한화오션' },
      { code: '010140', name: '삼성중공업' },
      { code: '009540', name: 'HD한국조선해양' },
      { code: '010620', name: 'HD현대미포' },
      { code: '272210', name: '한화시스템' },
    ],
  },
  {
    key: 'finance',
    name: '금융 / 지주',
    stocks: [
      { code: '105560', name: 'KB금융' },
      { code: '055550', name: '신한지주' },
      { code: '086790', name: '하나금융지주' },
      { code: '316140', name: '우리금융지주' },
      { code: '138040', name: '메리츠금융지주' },
      { code: '032830', name: '삼성생명' },
      { code: '000810', name: '삼성화재' },
      { code: '024110', name: '기업은행' },
      { code: '006800', name: '미래에셋증권' },
      { code: '071050', name: '한국금융지주' },
    ],
  },
  {
    key: 'entertainment',
    name: '엔터 / 콘텐츠',
    stocks: [
      { code: '352820', name: '하이브' },
      { code: '035900', name: 'JYP Ent.' },
      { code: '041510', name: '에스엠' },
      { code: '122870', name: '와이지엔터테인먼트' },
      { code: '035760', name: 'CJ ENM' },
      { code: '253450', name: '스튜디오드래곤' },
      { code: '376300', name: '디어유' },
      { code: '036420', name: '콘텐트리중앙' },
      { code: '214320', name: '이노션' },
      { code: '034120', name: 'SBS' },
    ],
  },
];

// 한국인이 선호하는(개인 순매수·보유 상위 단골) ETF 10종목.
// 국내 상장 ETF이므로 토스 Open API의 국내 종목 코드로 동일하게 조회 가능.
export const ETFS = [
  { code: '069500', name: 'KODEX 200', tag: '국내 대형주' },
  { code: '360750', name: 'TIGER 미국S&P500', tag: '미국 대표지수' },
  { code: '133690', name: 'TIGER 미국나스닥100', tag: '미국 기술주' },
  { code: '381180', name: 'TIGER 미국필라델피아반도체나스닥', tag: '미국 반도체' },
  { code: '379800', name: 'KODEX 미국S&P500', tag: '미국 대표지수' },
  { code: '305720', name: 'KODEX 2차전지산업', tag: '국내 2차전지' },
  { code: '102110', name: 'TIGER 200', tag: '국내 대형주' },
  { code: '229200', name: 'KODEX 코스닥150', tag: '코스닥 성장주' },
  { code: '396500', name: 'TIGER 반도체TOP10', tag: '국내 반도체' },
  { code: '122630', name: 'KODEX 레버리지', tag: '국내 레버리지' },
];

// 국내 시장 레짐(국면) 판단용 벤치마크 — KODEX 200을 KOSPI 대형주 지수 프록시로 사용.
export const REGIME_BENCHMARK = { code: '069500', name: 'KODEX 200' };

// 코드 -> {name, sector} 빠른 조회용 맵.
export function buildSymbolIndex() {
  const idx = new Map();
  for (const s of SECTORS) {
    for (const stock of s.stocks) {
      idx.set(stock.code, { ...stock, sector: s.name, sectorKey: s.key, type: 'stock' });
    }
  }
  for (const etf of ETFS) {
    idx.set(etf.code, { ...etf, sector: 'ETF', sectorKey: 'etf', type: 'etf' });
  }
  return idx;
}

// 이름/코드로 종목 찾기(검색 기능 보조). 부분 일치 허용.
export function findByQuery(query) {
  const q = query.trim().toLowerCase();
  const idx = buildSymbolIndex();
  // 코드 정확 일치
  if (idx.has(q)) return { code: q, ...idx.get(q) };
  for (const [code, meta] of idx) {
    if (code === q) return { code, ...meta };
  }
  // 이름 부분 일치
  for (const [code, meta] of idx) {
    if (meta.name.toLowerCase().includes(q)) return { code, ...meta };
  }
  return null;
}
