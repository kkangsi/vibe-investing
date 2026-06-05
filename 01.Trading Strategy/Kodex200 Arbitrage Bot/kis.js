// kis.js
// ======
// 한국투자증권(KIS) Open API 현재가 폴링 클라이언트.
//   - 토큰: POST /oauth2/tokenP (appkey/appsecret, 약 24h)
//   - 현재가: GET /uapi/domestic-stock/v1/quotations/inquire-price
//             tr_id FHKST01010100, output.stck_prpr(현재가)
//
// 30초~5분 추세가 목표이므로 1초 폴링이면 충분 → WebSocket(실시간체결) 없이 REST로
// 구현해 무의존성을 유지한다. (WS H0STCNT0 업그레이드는 README의 선택지로 안내.)
//
// KIS_APP_KEY / KIS_APP_SECRET 가 없으면 isMock()=true → feeds.js가 합성 틱으로 대체.

const baseUrl = () => process.env.KIS_BASE_URL || 'https://openapi.koreainvestment.com:9443';
const appKey = () => process.env.KIS_APP_KEY;
const appSecret = () => process.env.KIS_APP_SECRET;

export function isMock() {
  return !appKey() || !appSecret();
}

let tokenCache = { token: null, expiresAt: 0 };

async function getAccessToken() {
  const now = Date.now();
  if (tokenCache.token && now < tokenCache.expiresAt - 60_000) return tokenCache.token;
  const res = await fetch(`${baseUrl()}/oauth2/tokenP`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'client_credentials',
      appkey: appKey(),
      appsecret: appSecret(),
    }),
  });
  if (!res.ok) throw new Error(`KIS 토큰 발급 실패: ${res.status} ${await res.text()}`);
  const json = await res.json();
  const ttl = (json.expires_in || 86400) * 1000;
  tokenCache = { token: json.access_token, expiresAt: now + ttl };
  return tokenCache.token;
}

// 단일 종목 현재가. KIS는 종목별 단건 조회라 codes를 순회한다(초당 호출수 유의).
async function fetchOne(code, token) {
  const url = new URL(`${baseUrl()}/uapi/domestic-stock/v1/quotations/inquire-price`);
  url.searchParams.set('fid_cond_mrkt_div_code', 'J');
  url.searchParams.set('fid_input_iscd', code);
  const res = await fetch(url, {
    headers: {
      authorization: `Bearer ${token}`,
      appkey: appKey(),
      appsecret: appSecret(),
      tr_id: 'FHKST01010100',
      custtype: 'P',
    },
  });
  if (!res.ok) throw new Error(`KIS 현재가 실패(${code}): ${res.status}`);
  const json = await res.json();
  const o = json.output || {};
  const price = parseFloat(o.stck_prpr);
  return Number.isFinite(price) ? price : null;
}

// ETF 실시간 NAV(iNAV) 조회. 괴리율 = (시장가 − NAV)/NAV 계산에 사용.
//   GET /uapi/etfetn/v1/quotations/inquire-price, tr_id FHPST02400000, output.nav
// (tr_id·필드명은 KIS 문서 기준 best-effort — 실연동 시 응답으로 검증할 것.)
export async function fetchEtfNav(code) {
  const token = await getAccessToken();
  const url = new URL(`${baseUrl()}/uapi/etfetn/v1/quotations/inquire-price`);
  url.searchParams.set('fid_cond_mrkt_div_code', 'J');
  url.searchParams.set('fid_input_iscd', code);
  const res = await fetch(url, {
    headers: {
      authorization: `Bearer ${token}`,
      appkey: appKey(),
      appsecret: appSecret(),
      tr_id: 'FHPST02400000',
      custtype: 'P',
    },
  });
  if (!res.ok) throw new Error(`KIS NAV 실패(${code}): ${res.status}`);
  const o = (await res.json()).output || {};
  const nav = parseFloat(o.nav ?? o.etf_nav ?? o.nav_prpr);
  return Number.isFinite(nav) ? nav : null;
}

// 반환: [{ code, price, ts }]
export async function fetchPrices(codes) {
  const token = await getAccessToken();
  const ts = Date.now();
  const out = [];
  for (const code of codes) {
    try {
      const price = await fetchOne(code, token);
      if (price != null) out.push({ code, price, ts });
    } catch {
      /* 단건 실패는 건너뛴다(다음 폴링에서 회복) */
    }
  }
  return out;
}
