// selftest.js
// ===========
// 가상 시계로 전체 파이프라인(바 집계 → 시그널)을 빠르게 검증한다.
// 실봇은 60s·2m 바가 차려면 수 분이 걸리므로, 여기서는 ts를 인위적으로 전진시켜
// ~20분 분량의 틱을 즉시 생성하고, lead-lag(ETF 지연)를 주입해 시그널이 실제로
// 발화하는지 단정한다.  실행: node selftest.js
//
// 동시에 ticks_sim.csv를 남겨 Python lead-lag 검증기의 입력으로도 쓸 수 있다.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { ALL_CODES, DRIVERS, TRACKERS } from './instruments.js';
import { Board } from './bars.js';
import { evaluate, evaluateDisparity, DEFAULT_CONFIG } from './signal.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 결정론 PRNG.
let seed = 12345;
const rand = () => {
  seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const gauss = () => Math.sqrt(-2 * Math.log(Math.max(1e-9, rand()))) * Math.cos(2 * Math.PI * rand());

const LAG_MS = 4000;       // 주입 lead-lag
const STEP_MS = 1000;      // 1초 틱
const N = 20 * 60;         // 20분
const T0 = 1_700_000_000_000;

const board = new Board(ALL_CODES);
const rows = [['ts', 'code', 'price']];
const driverBase = new Map(DRIVERS.map((d, i) => [d.code, 70000 + i * 50000]));
const trackerBase = new Map(TRACKERS.map((t, i) => [t.code, 10000 + i * 3000]));
const hist = []; // { ts, cum }
let cum = 0, trend = 0, trendLeft = 0;
let fired = 0;
let dispFired = 0;
const firedCodes = new Set();

function cumAt(ts) {
  let v = 0;
  for (const h of hist) { if (h.ts <= ts) v = h.cum; else break; }
  return v;
}

for (let i = 0; i < N; i++) {
  const ts = T0 + i * STEP_MS;
  if (trendLeft <= 0 && rand() < 0.12) {
    trend = (rand() < 0.5 ? -1 : 1) * 0.0008 * (4 + rand() * 5);
    trendLeft = 20 + Math.floor(rand() * 20);
  }
  const drift = trendLeft-- > 0 ? trend : 0;
  cum += drift + 0.0005 * gauss();
  hist.push({ ts, cum });

  const ticks = [];
  for (const d of DRIVERS) {
    const px = Math.round(driverBase.get(d.code) * Math.exp(cum + 0.0003 * gauss()));
    ticks.push({ code: d.code, price: px, ts });
  }
  const lagged = cumAt(ts - LAG_MS);
  for (const t of TRACKERS) {
    const base = trackerBase.get(t.code);
    const px = Math.round(base * Math.exp(t.leverage * lagged + 0.0002 * gauss()) * 100) / 100;
    const nav = Math.round(base * Math.exp(t.leverage * cum) * 100) / 100; // 현재 공정가치
    ticks.push({ code: t.code, price: px, nav, ts });
  }
  for (const tk of ticks) rows.push([ts, tk.code, tk.price]);
  board.ingest(ticks);

  // 바가 좀 찬 뒤부터 평가.
  if (i > 180 && i % 10 === 0) {
    const { signals } = evaluate(board, DEFAULT_CONFIG);
    for (const s of signals) { fired++; firedCodes.add(s.code); }
    const { signals: disp } = evaluateDisparity(board, DEFAULT_CONFIG);
    dispFired += disp.length;
  }
}

const csv = path.join(__dirname, 'ticks_sim.csv');
fs.writeFileSync(csv, rows.map((r) => r.join(',')).join('\n') + '\n');

console.log(`[selftest] 20분/${N}틱 시뮬레이션 완료. 주입 lead-lag=${LAG_MS}ms`);
console.log(`[selftest] lead-lag 시그널 발화=${fired}, 발화 종목=${[...firedCodes].join(', ') || '없음'}`);
console.log(`[selftest] 괴리율 시그널 발화=${dispFired}`);
console.log(`[selftest] 시뮬 틱 CSV: ${csv}`);

if (fired === 0 || dispFired === 0) {
  console.error(`[selftest] ❌ 실패: lead-lag=${fired}, 괴리율=${dispFired} — 임계값/파이프라인 점검 필요`);
  process.exit(1);
}
console.log('[selftest] ✅ 통과: lead-lag + 괴리율(iNAV) 시그널 모두 정상 발화함');
