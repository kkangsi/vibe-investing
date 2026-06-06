/**
 * 심볼 사전 — 티커 ↔ 영문명 ↔ 한글명 ↔ 별칭. 검색 자동완성(#2)·워치리스트(#4)·ETF(#3) 공용.
 * 구성: 나스닥100 핵심 + 전략 유니버스(빅테크/AI반도체/AI인프라) + 한국 선호 US ETF.
 * g: 워치리스트/표시 그룹. 'nasdaq'=기타 나스닥100, 'etf'=ETF.
 */
export type SymGroup = "bigtech" | "ai_semi" | "ai_infra" | "etf" | "nasdaq";

export interface Sym {
  t: string; // 티커
  en: string; // 영문명
  ko: string; // 한글명
  g: SymGroup;
  alias?: string[]; // 약칭/별칭 (검색용)
}

export const SYMBOLS: Sym[] = [
  // --- 빅테크 (M7) ---
  { t: "AAPL", en: "Apple", ko: "애플", g: "bigtech", alias: ["애플", "사과"] },
  { t: "MSFT", en: "Microsoft", ko: "마이크로소프트", g: "bigtech", alias: ["MS", "엠에스", "마소"] },
  { t: "GOOGL", en: "Alphabet (Google) A", ko: "알파벳 (구글)", g: "bigtech", alias: ["구글", "Google", "알파벳"] },
  { t: "GOOG", en: "Alphabet (Google) C", ko: "알파벳 (구글) C", g: "bigtech", alias: ["구글", "Google"] },
  { t: "AMZN", en: "Amazon", ko: "아마존", g: "bigtech", alias: ["아마존"] },
  { t: "META", en: "Meta Platforms", ko: "메타 (페이스북)", g: "bigtech", alias: ["페이스북", "Facebook", "페북", "인스타"] },
  { t: "TSLA", en: "Tesla", ko: "테슬라", g: "bigtech", alias: ["테슬라", "테벌", "테슬"] },

  // --- AI 반도체 ---
  { t: "NVDA", en: "NVIDIA", ko: "엔비디아", g: "ai_semi", alias: ["엔비디아", "엔비", "NVidia"] },
  { t: "AVGO", en: "Broadcom", ko: "브로드컴", g: "ai_semi", alias: ["브로드컴"] },
  { t: "AMD", en: "Advanced Micro Devices", ko: "AMD (에이엠디)", g: "ai_semi", alias: ["에이엠디", "암드"] },
  { t: "TSM", en: "TSMC", ko: "TSMC (대만 반도체)", g: "ai_semi", alias: ["대만반도체", "티에스엠", "타이완"] },
  { t: "MU", en: "Micron", ko: "마이크론", g: "ai_semi", alias: ["마이크론", "메모리"] },
  { t: "ASML", en: "ASML Holding", ko: "ASML (에이에스엠엘)", g: "ai_semi", alias: ["에이에스엠엘", "노광", "EUV"] },
  { t: "INTC", en: "Intel", ko: "인텔", g: "ai_semi", alias: ["인텔"] },
  { t: "QCOM", en: "Qualcomm", ko: "퀄컴", g: "ai_semi", alias: ["퀄컴"] },
  { t: "MRVL", en: "Marvell", ko: "마벨", g: "ai_semi", alias: ["마벨", "마블"] },
  { t: "AMAT", en: "Applied Materials", ko: "어플라이드 머티어리얼즈", g: "ai_semi", alias: ["어플라이드", "AMAT"] },
  { t: "LRCX", en: "Lam Research", ko: "램리서치", g: "ai_semi", alias: ["램리서치"] },
  { t: "KLAC", en: "KLA Corp", ko: "KLA", g: "ai_semi", alias: ["케이엘에이"] },
  { t: "ADI", en: "Analog Devices", ko: "아날로그 디바이스", g: "ai_semi", alias: ["아날로그디바이스"] },
  { t: "NXPI", en: "NXP Semiconductors", ko: "NXP 반도체", g: "ai_semi", alias: ["엔엑스피"] },
  { t: "MCHP", en: "Microchip", ko: "마이크로칩", g: "ai_semi", alias: ["마이크로칩"] },

  // --- AI 인프라 (서버·네트워크·전력·소프트웨어) ---
  { t: "ANET", en: "Arista Networks", ko: "아리스타 네트웍스", g: "ai_infra", alias: ["아리스타"] },
  { t: "VRT", en: "Vertiv", ko: "버티브", g: "ai_infra", alias: ["버티브", "냉각", "전력"] },
  { t: "DELL", en: "Dell Technologies", ko: "델", g: "ai_infra", alias: ["델", "Dell"] },
  { t: "SMCI", en: "Super Micro", ko: "슈퍼마이크로", g: "ai_infra", alias: ["슈퍼마이크로", "슈마컴", "Supermicro"] },
  { t: "ORCL", en: "Oracle", ko: "오라클", g: "ai_infra", alias: ["오라클"] },
  { t: "CEG", en: "Constellation Energy", ko: "콘스텔레이션 에너지", g: "ai_infra", alias: ["콘스텔레이션", "원전"] },
  { t: "HPE", en: "Hewlett Packard Enterprise", ko: "HPE", g: "ai_infra", alias: ["에이치피이"] },
  { t: "CSCO", en: "Cisco", ko: "시스코", g: "ai_infra", alias: ["시스코"] },
  { t: "SNOW", en: "Snowflake", ko: "스노우플레이크", g: "ai_infra", alias: ["스노우플레이크", "눈송이"] },
  { t: "PLTR", en: "Palantir", ko: "팔란티어", g: "ai_infra", alias: ["팔란티어", "팔란"] },
  { t: "STX", en: "Seagate", ko: "씨게이트", g: "ai_infra", alias: ["씨게이트"] },
  { t: "WDC", en: "Western Digital", ko: "웨스턴디지털", g: "ai_infra", alias: ["웬디", "웨스턴디지털"] },

  // --- 기타 나스닥100 인기 종목 ---
  { t: "NFLX", en: "Netflix", ko: "넷플릭스", g: "nasdaq", alias: ["넷플릭스", "넷플"] },
  { t: "ADBE", en: "Adobe", ko: "어도비", g: "nasdaq", alias: ["어도비", "포토샵"] },
  { t: "COST", en: "Costco", ko: "코스트코", g: "nasdaq", alias: ["코스트코", "코카"] },
  { t: "PEP", en: "PepsiCo", ko: "펩시코", g: "nasdaq", alias: ["펩시"] },
  { t: "CMCSA", en: "Comcast", ko: "컴캐스트", g: "nasdaq", alias: ["컴캐스트"] },
  { t: "TMUS", en: "T-Mobile", ko: "티모바일", g: "nasdaq", alias: ["티모바일"] },
  { t: "INTU", en: "Intuit", ko: "인튜이트", g: "nasdaq", alias: ["인튜이트"] },
  { t: "ISRG", en: "Intuitive Surgical", ko: "인튜이티브 서지컬", g: "nasdaq", alias: ["인튜이티브", "수술로봇"] },
  { t: "AMGN", en: "Amgen", ko: "암젠", g: "nasdaq", alias: ["암젠"] },
  { t: "BKNG", en: "Booking Holdings", ko: "부킹홀딩스", g: "nasdaq", alias: ["부킹", "부킹닷컴"] },
  { t: "GILD", en: "Gilead", ko: "길리어드", g: "nasdaq", alias: ["길리어드"] },
  { t: "ADP", en: "ADP", ko: "ADP", g: "nasdaq", alias: ["에이디피"] },
  { t: "VRTX", en: "Vertex Pharma", ko: "버텍스 파마", g: "nasdaq", alias: ["버텍스"] },
  { t: "REGN", en: "Regeneron", ko: "리제네론", g: "nasdaq", alias: ["리제네론"] },
  { t: "PANW", en: "Palo Alto Networks", ko: "팔로알토 네트웍스", g: "nasdaq", alias: ["팔로알토", "보안"] },
  { t: "CRWD", en: "CrowdStrike", ko: "크라우드스트라이크", g: "nasdaq", alias: ["크라우드스트라이크", "보안"] },
  { t: "MELI", en: "MercadoLibre", ko: "메르카도리브레", g: "nasdaq", alias: ["메르카도", "남미아마존"] },
  { t: "SBUX", en: "Starbucks", ko: "스타벅스", g: "nasdaq", alias: ["스타벅스", "스벅"] },
  { t: "MDLZ", en: "Mondelez", ko: "몬델리즈", g: "nasdaq", alias: ["몬델리즈"] },
  { t: "ABNB", en: "Airbnb", ko: "에어비앤비", g: "nasdaq", alias: ["에어비앤비", "에비"] },
  { t: "PYPL", en: "PayPal", ko: "페이팔", g: "nasdaq", alias: ["페이팔"] },
  { t: "ADSK", en: "Autodesk", ko: "오토데스크", g: "nasdaq", alias: ["오토데스크"] },
  { t: "FTNT", en: "Fortinet", ko: "포티넷", g: "nasdaq", alias: ["포티넷", "보안"] },
  { t: "CDNS", en: "Cadence", ko: "케이던스", g: "nasdaq", alias: ["케이던스", "EDA"] },
  { t: "SNPS", en: "Synopsys", ko: "시놉시스", g: "nasdaq", alias: ["시놉시스", "EDA"] },
  { t: "MAR", en: "Marriott", ko: "메리어트", g: "nasdaq", alias: ["메리어트", "호텔"] },
  { t: "WDAY", en: "Workday", ko: "워크데이", g: "nasdaq", alias: ["워크데이"] },
  { t: "DDOG", en: "Datadog", ko: "데이터독", g: "nasdaq", alias: ["데이터독"] },
  { t: "TTD", en: "The Trade Desk", ko: "트레이드데스크", g: "nasdaq", alias: ["트레이드데스크"] },
  { t: "ROP", en: "Roper", ko: "로퍼", g: "nasdaq" },
  { t: "MNST", en: "Monster Beverage", ko: "몬스터 음료", g: "nasdaq", alias: ["몬스터"] },
  { t: "AEP", en: "American Electric Power", ko: "아메리칸 일렉트릭", g: "nasdaq" },
  { t: "PCAR", en: "Paccar", ko: "팩카", g: "nasdaq" },
  { t: "ODFL", en: "Old Dominion", ko: "올드 도미니언", g: "nasdaq" },
  { t: "CPRT", en: "Copart", ko: "코파트", g: "nasdaq" },
  { t: "ROST", en: "Ross Stores", ko: "로스 스토어스", g: "nasdaq" },
  { t: "DXCM", en: "Dexcom", ko: "덱스컴", g: "nasdaq" },
  { t: "IDXX", en: "IDEXX", ko: "아이덱스", g: "nasdaq" },
  { t: "EA", en: "Electronic Arts", ko: "EA (일렉트로닉 아츠)", g: "nasdaq", alias: ["EA", "게임"] },
  { t: "CSGP", en: "CoStar", ko: "코스타", g: "nasdaq" },
  { t: "KDP", en: "Keurig Dr Pepper", ko: "큐리그 닥터페퍼", g: "nasdaq" },
  { t: "KHC", en: "Kraft Heinz", ko: "크래프트 하인즈", g: "nasdaq" },
  { t: "EXC", en: "Exelon", ko: "엑셀론", g: "nasdaq" },
  { t: "CTAS", en: "Cintas", ko: "신타스", g: "nasdaq" },
  { t: "FAST", en: "Fastenal", ko: "패스널", g: "nasdaq" },
  { t: "VRSK", en: "Verisk", ko: "베리스크", g: "nasdaq" },
  { t: "BIIB", en: "Biogen", ko: "바이오젠", g: "nasdaq", alias: ["바이오젠"] },
  { t: "LULU", en: "Lululemon", ko: "룰루레몬", g: "nasdaq", alias: ["룰루레몬"] },
  { t: "ON", en: "ON Semiconductor", ko: "온 세미컨덕터", g: "ai_semi", alias: ["온세미"] },
  { t: "GFS", en: "GlobalFoundries", ko: "글로벌파운드리즈", g: "ai_semi", alias: ["글로벌파운드리"] },
  { t: "ZS", en: "Zscaler", ko: "지스케일러", g: "nasdaq", alias: ["지스케일러", "보안"] },
  { t: "TEAM", en: "Atlassian", ko: "아틀라시안", g: "nasdaq", alias: ["아틀라시안"] },
  { t: "MDB", en: "MongoDB", ko: "몽고DB", g: "nasdaq", alias: ["몽고디비"] },
  { t: "ARM", en: "Arm Holdings", ko: "암 홀딩스", g: "ai_semi", alias: ["암", "ARM"] },
  { t: "APP", en: "AppLovin", ko: "앱러빈", g: "nasdaq", alias: ["앱러빈"] },

  // --- 한국인 선호 US ETF (#3) ---
  { t: "QQQ", en: "Invesco QQQ (Nasdaq 100)", ko: "나스닥100 ETF", g: "etf", alias: ["나스닥", "큐큐큐"] },
  { t: "QQQM", en: "Invesco QQQ M", ko: "나스닥100 ETF (저보수)", g: "etf", alias: ["나스닥"] },
  { t: "TQQQ", en: "ProShares UltraPro QQQ 3x", ko: "나스닥100 3배 레버리지", g: "etf", alias: ["티큐", "3배", "레버리지"] },
  { t: "QLD", en: "ProShares Ultra QQQ 2x", ko: "나스닥100 2배", g: "etf", alias: ["2배"] },
  { t: "SQQQ", en: "ProShares UltraPro Short QQQ 3x", ko: "나스닥100 인버스 3배", g: "etf", alias: ["인버스", "곱버스"] },
  { t: "SPY", en: "SPDR S&P 500", ko: "S&P500 ETF", g: "etf", alias: ["에스피", "스파이"] },
  { t: "VOO", en: "Vanguard S&P 500", ko: "S&P500 ETF (뱅가드)", g: "etf", alias: ["부", "뱅가드"] },
  { t: "SCHD", en: "Schwab US Dividend", ko: "미국 배당 ETF (슈드)", g: "etf", alias: ["슈드", "배당"] },
  { t: "JEPI", en: "JPM Equity Premium Income", ko: "JEPI 월배당", g: "etf", alias: ["제피", "월배당"] },
  { t: "JEPQ", en: "JPM Nasdaq Equity Premium", ko: "JEPQ 나스닥 월배당", g: "etf", alias: ["제큐", "월배당"] },
  { t: "SOXL", en: "Direxion Semiconductor 3x", ko: "반도체 3배 레버리지", g: "etf", alias: ["속슬", "반도체3배", "레버리지"] },
  { t: "SOXX", en: "iShares Semiconductor", ko: "반도체 ETF", g: "etf", alias: ["반도체"] },
  { t: "SMH", en: "VanEck Semiconductor", ko: "반도체 ETF (반에크)", g: "etf", alias: ["반도체", "에스엠에이치"] },
  { t: "NVDL", en: "GraniteShares NVDA 2x", ko: "엔비디아 2배 레버리지", g: "etf", alias: ["엔비2배", "엔비디아레버리지"] },
  { t: "TSLL", en: "Direxion TSLA 2x", ko: "테슬라 2배 레버리지", g: "etf", alias: ["테슬라레버리지"] },
  { t: "SCHG", en: "Schwab US Large-Cap Growth", ko: "미국 성장주 ETF", g: "etf", alias: ["성장주"] },
  { t: "VTI", en: "Vanguard Total Market", ko: "미국 전체시장 ETF", g: "etf", alias: ["전체시장"] },
  { t: "BITO", en: "ProShares Bitcoin Strategy", ko: "비트코인 선물 ETF", g: "etf", alias: ["비트코인"] },
  { t: "GLD", en: "SPDR Gold", ko: "금 ETF", g: "etf", alias: ["금", "골드"] },
];

const norm = (s: string) => s.toLowerCase().replace(/\s+/g, "");

/** 티커/영문명/한글명/별칭으로 검색. 접두 우선 + 부분일치. 최대 limit개. */
export function searchSymbols(query: string, limit = 8): Sym[] {
  const q = norm(query);
  if (!q) return [];
  const scored: Array<{ s: Sym; score: number }> = [];
  for (const s of SYMBOLS) {
    const fields = [s.t, s.en, s.ko, ...(s.alias ?? [])].map(norm);
    let best = 99;
    for (const f of fields) {
      if (f === q) best = Math.min(best, 0);
      else if (f.startsWith(q)) best = Math.min(best, 1);
      else if (f.includes(q)) best = Math.min(best, 2);
    }
    if (best < 99) scored.push({ s, score: best });
  }
  scored.sort((a, b) => a.score - b.score || a.s.t.localeCompare(b.s.t));
  return scored.slice(0, limit).map((x) => x.s);
}

export const SYM_BY_TICKER: Record<string, Sym> = Object.fromEntries(SYMBOLS.map((s) => [s.t, s]));

/** 워치리스트(#4): 빅테크 + AI반도체 + AI인프라 (그룹 순서 유지). */
export const WATCHLIST: Sym[] = SYMBOLS.filter((s) => s.g === "bigtech" || s.g === "ai_semi" || s.g === "ai_infra");
export const WATCHLIST_TICKERS: string[] = [...new Set(WATCHLIST.map((s) => s.t))];

/** 인기 ETF(#3) 티커. */
export const ETF_TICKERS: string[] = SYMBOLS.filter((s) => s.g === "etf").map((s) => s.t);
