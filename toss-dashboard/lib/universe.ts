export interface UniverseStock {
  symbol: string;
  name: string;
  nameKr?: string;
  market: "KR" | "US";
  sector: string;
  tag?: string;
}

// 한국인들이 사랑하는 주식 & ETF
export const POPULAR_KR_STOCKS: UniverseStock[] = [
  { symbol: "005930", name: "삼성전자", market: "KR", sector: "반도체", tag: "💎 국민주" },
  { symbol: "000660", name: "SK하이닉스", market: "KR", sector: "반도체", tag: "🔥 핫이슈" },
  { symbol: "035420", name: "NAVER", market: "KR", sector: "인터넷", tag: "🌐 빅테크" },
  { symbol: "035720", name: "카카오", market: "KR", sector: "인터넷", tag: "💬 플랫폼" },
  { symbol: "207940", name: "삼성바이오로직스", market: "KR", sector: "바이오" },
  { symbol: "068270", name: "셀트리온", market: "KR", sector: "바이오" },
  { symbol: "005380", name: "현대차", market: "KR", sector: "자동차" },
  { symbol: "000270", name: "기아", market: "KR", sector: "자동차" },
  { symbol: "051910", name: "LG화학", market: "KR", sector: "2차전지" },
  { symbol: "373220", name: "LG에너지솔루션", market: "KR", sector: "2차전지", tag: "⚡ 배터리" },
  { symbol: "006400", name: "삼성SDI", market: "KR", sector: "2차전지" },
  { symbol: "012330", name: "현대모비스", market: "KR", sector: "자동차부품" },
];

export const POPULAR_KR_ETFS: UniverseStock[] = [
  { symbol: "069500", name: "KODEX 200", market: "KR", sector: "ETF", tag: "📊 코스피" },
  { symbol: "102110", name: "TIGER 200", market: "KR", sector: "ETF" },
  { symbol: "122630", name: "KODEX 레버리지", market: "KR", sector: "ETF", tag: "⚡ 2X" },
  { symbol: "114800", name: "KODEX 인버스", market: "KR", sector: "ETF" },
  { symbol: "229200", name: "KODEX 코스닥150", market: "KR", sector: "ETF" },
  { symbol: "305720", name: "KODEX 2차전지산업", market: "KR", sector: "ETF", tag: "🔋 배터리" },
  { symbol: "091160", name: "KODEX 반도체", market: "KR", sector: "ETF", tag: "💻 반도체" },
  { symbol: "139660", name: "TIGER 미국S&P500", market: "KR", sector: "ETF", tag: "🇺🇸 S&P500" },
  { symbol: "133690", name: "TIGER 미국나스닥100", market: "KR", sector: "ETF", tag: "🇺🇸 나스닥" },
  { symbol: "448290", name: "TIGER 미국AI빅테크10", market: "KR", sector: "ETF", tag: "🤖 AI" },
];

// 한국 주식 섹터별
export const KR_SECTORS: { name: string; stocks: UniverseStock[] }[] = [
  {
    name: "반도체 / AI",
    stocks: [
      { symbol: "005930", name: "삼성전자", market: "KR", sector: "반도체" },
      { symbol: "000660", name: "SK하이닉스", market: "KR", sector: "반도체" },
      { symbol: "042700", name: "한미반도체", market: "KR", sector: "반도체" },
      { symbol: "336370", name: "솔브레인홀딩스", market: "KR", sector: "반도체" },
      { symbol: "036830", name: "솔브레인", market: "KR", sector: "반도체" },
    ],
  },
  {
    name: "2차전지 / 소재",
    stocks: [
      { symbol: "373220", name: "LG에너지솔루션", market: "KR", sector: "2차전지" },
      { symbol: "006400", name: "삼성SDI", market: "KR", sector: "2차전지" },
      { symbol: "051910", name: "LG화학", market: "KR", sector: "2차전지" },
      { symbol: "096770", name: "SK이노베이션", market: "KR", sector: "2차전지" },
      { symbol: "247540", name: "에코프로비엠", market: "KR", sector: "2차전지" },
    ],
  },
  {
    name: "자동차 / 부품",
    stocks: [
      { symbol: "005380", name: "현대차", market: "KR", sector: "자동차" },
      { symbol: "000270", name: "기아", market: "KR", sector: "자동차" },
      { symbol: "012330", name: "현대모비스", market: "KR", sector: "자동차" },
      { symbol: "011210", name: "현대위아", market: "KR", sector: "자동차" },
      { symbol: "018880", name: "한온시스템", market: "KR", sector: "자동차" },
    ],
  },
  {
    name: "인터넷 / 플랫폼",
    stocks: [
      { symbol: "035420", name: "NAVER", market: "KR", sector: "인터넷" },
      { symbol: "035720", name: "카카오", market: "KR", sector: "인터넷" },
      { symbol: "259960", name: "크래프톤", market: "KR", sector: "게임" },
      { symbol: "036570", name: "엔씨소프트", market: "KR", sector: "게임" },
      { symbol: "263750", name: "펄어비스", market: "KR", sector: "게임" },
    ],
  },
  {
    name: "바이오 / 제약",
    stocks: [
      { symbol: "207940", name: "삼성바이오로직스", market: "KR", sector: "바이오" },
      { symbol: "068270", name: "셀트리온", market: "KR", sector: "바이오" },
      { symbol: "326030", name: "SK바이오팜", market: "KR", sector: "바이오" },
      { symbol: "128940", name: "한미약품", market: "KR", sector: "제약" },
      { symbol: "000100", name: "유한양행", market: "KR", sector: "제약" },
    ],
  },
  {
    name: "방산 / 조선",
    stocks: [
      { symbol: "012450", name: "한화에어로스페이스", market: "KR", sector: "방산" },
      { symbol: "047810", name: "한국항공우주", market: "KR", sector: "방산" },
      { symbol: "009540", name: "HD한국조선해양", market: "KR", sector: "조선" },
      { symbol: "010140", name: "삼성중공업", market: "KR", sector: "조선" },
      { symbol: "042660", name: "한화오션", market: "KR", sector: "조선" },
    ],
  },
  {
    name: "금융",
    stocks: [
      { symbol: "105560", name: "KB금융", market: "KR", sector: "금융" },
      { symbol: "055550", name: "신한지주", market: "KR", sector: "금융" },
      { symbol: "086790", name: "하나금융지주", market: "KR", sector: "금융" },
      { symbol: "316140", name: "우리금융지주", market: "KR", sector: "금융" },
      { symbol: "032830", name: "삼성생명", market: "KR", sector: "금융" },
    ],
  },
];

// 미국 주식
export const US_STOCKS: UniverseStock[] = [
  // 매그니피센트 7
  { symbol: "AAPL", name: "Apple", nameKr: "애플", market: "US", sector: "빅테크", tag: "🍎" },
  { symbol: "MSFT", name: "Microsoft", nameKr: "마이크로소프트", market: "US", sector: "빅테크", tag: "🪟" },
  { symbol: "NVDA", name: "NVIDIA", nameKr: "엔비디아", market: "US", sector: "AI/반도체", tag: "🤖 AI" },
  { symbol: "AMZN", name: "Amazon", nameKr: "아마존", market: "US", sector: "빅테크" },
  { symbol: "META", name: "Meta", nameKr: "메타", market: "US", sector: "소셜미디어" },
  { symbol: "GOOGL", name: "Alphabet", nameKr: "구글", market: "US", sector: "빅테크" },
  { symbol: "TSLA", name: "Tesla", nameKr: "테슬라", market: "US", sector: "전기차", tag: "⚡ EV" },
  // 반도체
  { symbol: "AMD", name: "AMD", nameKr: "AMD", market: "US", sector: "반도체" },
  { symbol: "INTC", name: "Intel", nameKr: "인텔", market: "US", sector: "반도체" },
  { symbol: "QCOM", name: "Qualcomm", nameKr: "퀄컴", market: "US", sector: "반도체" },
  // 기타 인기
  { symbol: "PLTR", name: "Palantir", nameKr: "팔란티어", market: "US", sector: "AI/데이터", tag: "🔮 AI" },
  { symbol: "COIN", name: "Coinbase", nameKr: "코인베이스", market: "US", sector: "크립토" },
];

export const US_ETFS: UniverseStock[] = [
  { symbol: "SPY", name: "SPDR S&P 500 ETF", nameKr: "S&P500", market: "US", sector: "ETF", tag: "📊 S&P500" },
  { symbol: "QQQ", name: "Invesco QQQ", nameKr: "나스닥100", market: "US", sector: "ETF", tag: "💻 나스닥" },
  { symbol: "TQQQ", name: "ProShares UltraPro QQQ", nameKr: "나스닥3배", market: "US", sector: "ETF", tag: "⚡ 3X" },
  { symbol: "SQQQ", name: "ProShares UltraPro Short QQQ", nameKr: "나스닥인버스3배", market: "US", sector: "ETF" },
  { symbol: "SOXL", name: "Direxion Semiconductor 3X", nameKr: "반도체3배", market: "US", sector: "ETF", tag: "🔥 반도체" },
  { symbol: "ARKK", name: "ARK Innovation ETF", nameKr: "ARK 혁신", market: "US", sector: "ETF" },
  { symbol: "SCHD", name: "Schwab US Dividend Equity ETF", nameKr: "배당주", market: "US", sector: "ETF" },
  { symbol: "GLD", name: "SPDR Gold Shares", nameKr: "금 ETF", market: "US", sector: "ETF", tag: "🥇 금" },
];

export function getAllSymbols(): string[] {
  return [
    ...POPULAR_KR_STOCKS.map((s) => s.symbol),
    ...POPULAR_KR_ETFS.map((s) => s.symbol),
    ...KR_SECTORS.flatMap((sec) => sec.stocks.map((s) => s.symbol)),
    ...US_STOCKS.map((s) => s.symbol),
    ...US_ETFS.map((s) => s.symbol),
  ].filter((v, i, a) => a.indexOf(v) === i);
}

export function findStock(symbol: string): UniverseStock | undefined {
  const all = [
    ...POPULAR_KR_STOCKS,
    ...POPULAR_KR_ETFS,
    ...KR_SECTORS.flatMap((s) => s.stocks),
    ...US_STOCKS,
    ...US_ETFS,
  ];
  return all.find((s) => s.symbol === symbol);
}
