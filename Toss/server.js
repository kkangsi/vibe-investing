// server.js
// =========
// 토스증권 Open API + AMQS 모멘텀 퀀트 대시보드 백엔드.
//
//   GET /api/health     → 모드/메타 정보
//   GET /api/dashboard  → 레짐 + 섹터별 종목 + ETF 시그널(매수/보유/매도)
//   GET /api/search?q=  → 종목명/코드 검색 후 동일 방식 시그널
//
// 실행: TOSS_CLIENT_ID / TOSS_CLIENT_SECRET 환경변수 설정 시 실데이터,
//       없으면 결정론적 MOCK 데이터로 동작.

import express from 'express';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// --- 의존성 없는 초경량 .env 로더 (있으면 읽고, 없으면 MOCK 모드) ---
(function loadEnv() {
  try {
    const envPath = path.join(path.dirname(fileURLToPath(import.meta.url)), '.env');
    if (!fs.existsSync(envPath)) return;
    for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
      const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
      if (m && !process.env[m[1]]) process.env[m[1]] = m[2].replace(/^["']|["']$/g, '');
    }
  } catch { /* noop */ }
})();

// 동적 import — 위 loadEnv() 이후에 모듈을 평가해 .env가 반영되도록 한다.
const { SECTORS, ETFS, REGIME_BENCHMARK, findByQuery, buildSymbolIndex } = await import('./src/universe.js');
const { fetchCandles, isMock } = await import('./src/toss.js');
const { rawFactors, scoreUniverse, determineRegime, signalFor } = await import('./src/amqs.js');
const IS_MOCK = isMock();

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = process.env.PORT || process.argv[2] || 3000;

app.use(express.static(path.join(__dirname, 'public')));

// --- 간단한 메모리 캐시 (candles, dashboard) ---
const CANDLE_TTL = 10 * 60 * 1000; // 10분
const candleCache = new Map(); // code -> { at, candles }
let dashboardCache = { at: 0, data: null };
const DASH_TTL = 5 * 60 * 1000;

async function getCandles(code) {
  const hit = candleCache.get(code);
  if (hit && Date.now() - hit.at < CANDLE_TTL) return hit.candles;
  const candles = await fetchCandles(code, 260);
  candleCache.set(code, { at: Date.now(), candles });
  return candles;
}

// 동시성 제한 매핑 (Toss rate limit 보호)
async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let i = 0;
  async function worker() {
    while (i < items.length) {
      const idx = i++;
      try {
        out[idx] = await fn(items[idx], idx);
      } catch (e) {
        out[idx] = { error: String(e.message || e) };
      }
    }
  }
  await Promise.all(Array.from({ length: Math.min(limit, items.length) }, worker));
  return out;
}

// universe 전체의 factors를 채워서 반환.
async function loadUniverseFactors() {
  const items = [];
  for (const s of SECTORS) for (const st of s.stocks) items.push({ ...st, sector: s.name, sectorKey: s.key, type: 'stock' });
  for (const e of ETFS) items.push({ ...e, sector: 'ETF', sectorKey: 'etf', type: 'etf' });

  await mapLimit(items, 8, async (it) => {
    const candles = await getCandles(it.code);
    it.factors = rawFactors(candles);
    return it;
  });
  return items;
}

async function buildDashboard() {
  if (dashboardCache.data && Date.now() - dashboardCache.at < DASH_TTL) return dashboardCache.data;

  const [benchCandles, items] = await Promise.all([getCandles(REGIME_BENCHMARK.code), loadUniverseFactors()]);
  const regime = determineRegime(benchCandles);
  const scored = scoreUniverse(items);

  const withSignals = scored.map((it) => ({
    code: it.code,
    name: it.name,
    sector: it.sector,
    sectorKey: it.sectorKey,
    type: it.type,
    tag: it.tag,
    ...signalFor(it, regime),
  }));

  // 섹터/ETF로 재그룹화
  const byKey = new Map();
  for (const row of withSignals) {
    if (!byKey.has(row.sectorKey)) byKey.set(row.sectorKey, []);
    byKey.get(row.sectorKey).push(row);
  }
  for (const arr of byKey.values()) arr.sort((a, b) => (b.momentum_score ?? 0) - (a.momentum_score ?? 0));

  const sectors = SECTORS.map((s) => ({ key: s.key, name: s.name, items: byKey.get(s.key) || [] }));
  const etfs = (byKey.get('etf') || []);

  const data = {
    asOf: new Date().toISOString(),
    mock: IS_MOCK,
    regime,
    summary: summarize(withSignals),
    sectors,
    etfs,
  };
  dashboardCache = { at: Date.now(), data };
  return data;
}

function summarize(rows) {
  const c = { BUY: 0, HOLD: 0, SELL: 0, AVOID: 0 };
  for (const r of rows) c[r.signal] = (c[r.signal] || 0) + 1;
  return c;
}

app.get('/api/health', (req, res) => {
  res.json({ ok: true, mock: IS_MOCK, benchmark: REGIME_BENCHMARK, sectors: SECTORS.length, etfs: ETFS.length });
});

app.get('/api/dashboard', async (req, res) => {
  try {
    const data = await buildDashboard();
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: String(e.message || e) });
  }
});

app.get('/api/search', async (req, res) => {
  const q = (req.query.q || '').toString().trim();
  if (!q) return res.status(400).json({ error: '검색어(q)가 필요합니다. 종목명 또는 6자리 코드를 입력하세요.' });

  try {
    // 1) 큐레이션 universe에서 이름/코드 매칭, 없으면 숫자코드면 그대로 사용
    let meta = findByQuery(q);
    if (!meta && /^\d{6}$/.test(q)) meta = { code: q, name: q, sector: '검색', type: 'unknown' };
    if (!meta) return res.status(404).json({ error: `'${q}' 종목을 찾지 못했습니다. 6자리 코드로 시도해 보세요.` });

    // 2) 횡단면 z-score를 위해 universe factors + 검색 종목을 함께 점수화
    const [benchCandles, universe] = await Promise.all([getCandles(REGIME_BENCHMARK.code), loadUniverseFactors()]);
    const regime = determineRegime(benchCandles);

    const target = { ...meta };
    const idx = buildSymbolIndex();
    const inUniverse = idx.has(meta.code);
    if (!inUniverse) target.factors = rawFactors(await getCandles(meta.code));

    const pool = inUniverse ? universe : [...universe, target];
    const scored = scoreUniverse(pool);
    const me = scored.find((x) => x.code === meta.code) || target;

    res.json({
      mock: IS_MOCK,
      regime,
      result: {
        code: meta.code,
        name: meta.name,
        sector: meta.sector,
        type: meta.type,
        ...signalFor(me, regime),
      },
    });
  } catch (e) {
    res.status(500).json({ error: String(e.message || e) });
  }
});

app.listen(PORT, () => {
  console.log(`AMQS 대시보드: http://localhost:${PORT}  (mode: ${IS_MOCK ? 'MOCK' : 'TOSS LIVE'})`);
});
