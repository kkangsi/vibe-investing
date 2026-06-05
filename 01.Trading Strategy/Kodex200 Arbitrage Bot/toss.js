// toss.js
// =======
// 토스증권 Open API 클라이언트.
//   - Base URL: https://openapi.tossinvest.com
//   - 인증: OAuth 2.0 Client Credentials (POST /oauth2/token), 토큰 캐싱
//   - 시세: GET /api/v1/prices?symbols=...
//   - 일봉: GET /api/v1/candles?symbol=...&interval=1d&count=200 (필요 시 before 페이지네이션)
//
// 자격증명(TOSS_CLIENT_ID / TOSS_CLIENT_SECRET)이 없으면 MOCK 모드로 동작.
// MOCK 모드는 종목코드 기반 결정론적 합성 일봉을 생성하므로, 키 없이도
// 대시보드/시그널 로직을 그대로 시연·검증할 수 있다.

// 환경변수는 .env 로더 이후에 읽혀야 하므로 호출 시점에 lazy 평가한다.
const baseUrl = () => process.env.TOSS_BASE_URL || 'https://openapi.tossinvest.com';
const clientId = () => process.env.TOSS_CLIENT_ID;
const clientSecret = () => process.env.TOSS_CLIENT_SECRET;

export function isMock() {
  return !clientId() || !clientSecret();
}

let tokenCache = { token: null, expiresAt: 0 };

async function getAccessToken() {
  const now = Date.now();
  if (tokenCache.token && now < tokenCache.expiresAt - 30_000) return tokenCache.token;

  const body = new URLSearchParams({
    grant_type: 'client_credentials',
    client_id: clientId(),
    client_secret: clientSecret(),
  });
  const res = await fetch(`${baseUrl()}/oauth2/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
  if (!res.ok) throw new Error(`Toss OAuth 실패: ${res.status} ${await res.text()}`);
  const json = await res.json();
  const ttl = (json.expires_in || 3600) * 1000;
  tokenCache = { token: json.access_token, expiresAt: now + ttl };
  return tokenCache.token;
}

async function authedGet(path, params) {
  const token = await getAccessToken();
  const url = new URL(`${baseUrl()}${path}`);
  for (const [k, v] of Object.entries(params || {})) url.searchParams.set(k, v);
  const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
  if (!res.ok) throw new Error(`Toss API ${path} 실패: ${res.status} ${await res.text()}`);
  return res.json();
}

// 여러 종목 현재가 조회. 반환: Map<code, { price, change, changeRate }>
export async function fetchPrices(codes) {
  if (isMock()) return mockPrices(codes);
  const out = new Map();
  // symbols 최대 200개 — 청크 분할
  for (let i = 0; i < codes.length; i += 200) {
    const chunk = codes.slice(i, i + 200);
    const json = await authedGet('/api/v1/prices', { symbols: chunk.join(',') });
    for (const row of json.prices || json.data || []) {
      const code = row.symbol || row.code;
      out.set(code, {
        price: num(row.price ?? row.close ?? row.last),
        change: num(row.change),
        changeRate: num(row.changeRate ?? row.rate),
      });
    }
  }
  return out;
}

// 일봉 조회. count는 최대 200이므로 days>200이면 before로 페이지네이션.
// 반환: [{ time, close }] (과거 → 현재 정렬)
export async function fetchCandles(code, days = 260) {
  if (isMock()) return mockCandles(code, days);
  const collected = [];
  let before = undefined;
  while (collected.length < days) {
    const params = { symbol: code, interval: '1d', count: 200 };
    if (before) params.before = before;
    const json = await authedGet('/api/v1/candles', params);
    const rows = json.candles || json.data || [];
    if (!rows.length) break;
    for (const r of rows) {
      collected.push({ time: r.time ?? r.timestamp ?? r.date, close: num(r.close ?? r.c) });
    }
    before = rows[rows.length - 1].time ?? rows[rows.length - 1].timestamp;
    if (rows.length < 200) break;
  }
  // 과거 → 현재 정렬 + 중복 제거
  const uniq = dedupeByTime(collected).sort((a, b) => String(a.time).localeCompare(String(b.time)));
  return uniq.slice(-days);
}

function dedupeByTime(rows) {
  const seen = new Set();
  const out = [];
  for (const r of rows) {
    const k = String(r.time);
    if (seen.has(k)) continue;
    seen.add(k);
    out.push(r);
  }
  return out;
}

function num(v) {
  const n = typeof v === 'string' ? parseFloat(v.replace(/,/g, '')) : v;
  return Number.isFinite(n) ? n : null;
}

// ---------------------------------------------------------------------------
// MOCK 모드: 결정론적 합성 데이터 (키 없이 시연/검증용)
// ---------------------------------------------------------------------------

// 코드 문자열 -> 32bit 시드
function hashSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

// mulberry32 PRNG
function rng(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// 종목별 결정론적 일봉 — drift/vol을 코드 해시로 분산시켜 매수/보유/매도가 골고루 나오게.
export function mockCandles(code, days = 260) {
  // 레짐 벤치마크(KODEX 200)는 시연을 위해 완만한 상승 추세(RISK_ON 근방)로 고정.
  if (code === '069500') return mockBenchmarkCandles(days);

  const seed = hashSeed(code);
  const rand = rng(seed);
  // drift: 연 -25% ~ +60%, vol: 연 18% ~ 75%
  const annDrift = -0.25 + rand() * 0.85;
  const annVol = 0.18 + rand() * 0.57;
  const dailyDrift = annDrift / 252;
  const dailyVol = annVol / Math.sqrt(252);

  // 시작가: 코드 끝자리로 가격대 분산 (1,000 ~ 400,000원)
  let price = 1000 + (seed % 400) * 1000;
  const out = [];
  // 종목마다 후반부에 추세 전환을 한 번씩 줘서 손절/추세약화 케이스도 생성
  const flipAt = 0.55 + (rand() * 0.35);
  for (let i = 0; i < days; i++) {
    const t = i / days;
    const localDrift = t > flipAt ? dailyDrift * (rand() < 0.5 ? -1.4 : 1.2) : dailyDrift;
    // box-muller
    const u1 = Math.max(1e-9, rand());
    const u2 = rand();
    const zn = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    const shock = localDrift + dailyVol * zn;
    price = Math.max(50, price * (1 + shock));
    const d = new Date(Date.UTC(2025, 5, 5));
    d.setUTCDate(d.getUTCDate() - (days - i));
    out.push({ time: d.toISOString().slice(0, 10), close: Math.round(price) });
  }
  return out;
}

// 레짐 벤치마크용 합성 일봉: 200일선 위 + 5일 수익률 양호 → RISK_ON 시연.
function mockBenchmarkCandles(days = 260) {
  const rand = rng(hashSeed('KODEX200-bench'));
  let price = 33000; // KODEX 200 현실적 레벨(약 3.3만원)
  const dailyDrift = 0.12 / 252; // 연 +12% 추세
  const dailyVol = 0.13 / Math.sqrt(252);
  const out = [];
  for (let i = 0; i < days; i++) {
    const u1 = Math.max(1e-9, rand());
    const u2 = rand();
    const zn = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    price = Math.max(50, price * (1 + dailyDrift + dailyVol * zn));
    const d = new Date(Date.UTC(2025, 5, 5));
    d.setUTCDate(d.getUTCDate() - (days - i));
    out.push({ time: d.toISOString().slice(0, 10), close: Math.round(price) });
  }
  return out;
}

export function mockPrices(codes) {
  const out = new Map();
  for (const code of codes) {
    const c = mockCandles(code, 6);
    const last = c[c.length - 1].close;
    const prev = c[c.length - 2].close;
    out.set(code, {
      price: last,
      change: last - prev,
      changeRate: round((last / prev - 1) * 100, 2),
    });
  }
  return out;
}

function round(v, d = 2) {
  const m = 10 ** d;
  return Math.round(v * m) / m;
}
