// server.js
// =========
// 차익거래 알람 봇 웹 대시보드 백엔드 (Node 내장 http만 사용 — 의존성 0).
//
//   GET  /api/health   → 소스/모드/가용성/업타임
//   GET  /api/state    → composite·drivers·trackers 스냅샷 + 시그널 + 최근 알람
//   POST /api/source   → 데이터 소스 전환 ({ source: 'TOSS'|'KIS'|'MOCK'|'AUTO' })
//   GET  /             → public/index.html (대시보드 UI)
//
// 실행:  node server.js [port]
//   - KIS_APP_KEY/SECRET 있으면 한국투자 실시간, TOSS_CLIENT_ID/SECRET 있으면 토스,
//     없으면 MOCK. 대시보드 셀렉터로 런타임에 소스를 바꿀 수 있다.

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// .env 로더(이 폴더의 .env) — 동적 import 전에 실행.
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

const { ALL_CODES } = await import('./instruments.js');
const { Board } = await import('./bars.js');
const { evaluate, evaluateDisparity, snapshot, DEFAULT_CONFIG, DISPLAY_TIMEFRAMES } =
  await import('./signal.js');
const { createFeed, pickMode, sourceAvailability } = await import('./feeds.js');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || process.argv[2] || 3100;
const POLL_MS = Number(process.env.ARB_POLL_MS || 1000);
const COOLDOWN_MS = Number(process.env.ARB_COOLDOWN_MS || 90_000);
const startedAt = Date.now();

// --- 런타임 상태 ---
const state = {
  requested: (process.env.ARB_SOURCE || 'AUTO').toUpperCase(),
  resolved: 'MOCK',
  feed: null,
  board: new Board(ALL_CODES),
  latest: { composite: {}, drivers: [], trackers: [] },
  signals: { leadlag: [], disparity: [] },
  alerts: [], // 최근 발화 알람(최신순)
};
const cooldown = new Map(); // `${type}:${code}:${dir}` -> ts

// 소스 전환: 기존 피드 종료 → 보드 리셋(스케일 혼합 방지) → 새 피드 생성.
async function setSource(requested) {
  state.requested = String(requested || 'AUTO').toUpperCase();
  try { state.feed?.close?.(); } catch { /* noop */ }
  state.board = new Board(ALL_CODES);
  state.feed = await createFeed(ALL_CODES, state.requested);
  state.resolved = state.feed.mode || pickMode(state.requested);
  console.log(`[dashboard] 소스 전환: 요청=${state.requested} → 실제=${state.resolved}`);
}

function pushAlerts(signals, type) {
  const now = Date.now();
  for (const s of signals) {
    const key = `${type}:${s.code}:${s.direction}`;
    if (now - (cooldown.get(key) || 0) < COOLDOWN_MS) continue;
    cooldown.set(key, now);
    state.alerts.unshift({
      time: new Date(now).toISOString(),
      type,
      code: s.code,
      name: s.name,
      direction: s.direction,
      action: s.action,
      metric: type === 'DISPARITY' ? s.disparity : s.gap,
    });
  }
  if (state.alerts.length > 60) state.alerts.length = 60;
}

async function step() {
  const ticks = await state.feed.poll();
  state.board.ingest(ticks);
  const lead = evaluate(state.board, DEFAULT_CONFIG).signals;
  const disp = evaluateDisparity(state.board, DEFAULT_CONFIG).signals;
  state.signals = { leadlag: lead, disparity: disp };
  state.latest = snapshot(state.board, DEFAULT_CONFIG);
  pushAlerts(lead, 'LEADLAG');
  pushAlerts(disp, 'DISPARITY');
}

// --- HTTP ---
const MIME = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8' };

function sendJson(res, code, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(body);
}

function health() {
  return {
    requested: state.requested,
    resolved: state.resolved,
    mock: state.resolved === 'MOCK',
    availability: sourceAvailability(),
    pollMs: POLL_MS,
    timeframes: DISPLAY_TIMEFRAMES,
    confirmTimeframes: DEFAULT_CONFIG.confirmTimeframes,
    codes: ALL_CODES.length,
    uptimeMs: Date.now() - startedAt,
    node: process.version,
  };
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const p = url.pathname;

  if (p === '/api/health') return sendJson(res, 200, health());

  if (p === '/api/state') {
    return sendJson(res, 200, {
      ts: Date.now(),
      source: { requested: state.requested, resolved: state.resolved },
      ...state.latest,
      signals: state.signals,
      alerts: state.alerts,
    });
  }

  if (p === '/api/source' && req.method === 'POST') {
    let body = '';
    req.on('data', (c) => { body += c; if (body.length > 1e4) req.destroy(); });
    req.on('end', async () => {
      try {
        const { source } = JSON.parse(body || '{}');
        const allowed = ['TOSS', 'KIS', 'MOCK', 'AUTO'];
        if (!allowed.includes(String(source).toUpperCase())) {
          return sendJson(res, 400, { error: '허용되지 않은 소스', allowed });
        }
        await setSource(source);
        sendJson(res, 200, health());
      } catch (e) {
        sendJson(res, 500, { error: e.message });
      }
    });
    return;
  }

  // 정적 파일.
  let file = p === '/' ? '/index.html' : p;
  const full = path.join(__dirname, 'public', path.normalize(file).replace(/^(\.\.[/\\])+/, ''));
  fs.readFile(full, (err, data) => {
    if (err) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(full)] || 'application/octet-stream' });
    res.end(data);
  });
});

// --- 부팅 ---
await setSource(state.requested);
setInterval(() => { step().catch((e) => console.error('[dashboard] step 오류:', e.message)); }, POLL_MS);

server.listen(PORT, () => {
  console.log('==================================================================');
  console.log(' ⚠️  고위험 트레이딩(HIGH-RISK) — 알람·리서치 전용, 투자 권유 아님');
  console.log(' 초단타·고빈도 매매는 증권사 FDS로 계좌·API가 제한될 수 있습니다.');
  console.log('==================================================================');
  console.log(`[dashboard] http://localhost:${PORT}  소스=${state.resolved}  poll=${POLL_MS}ms`);
});
