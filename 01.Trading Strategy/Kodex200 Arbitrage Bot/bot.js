// bot.js
// ======
// 차익거래 알람 봇 메인 루프.
//   1초마다: 시세 폴링 → 멀티TF 바 갱신 → 시그널 평가 → 알람.
//   --record 옵션이면 모든 틱을 ticks.csv로 적재(Python lead-lag 검증 입력).
//
// 실행:
//   node bot.js                 # 키 있으면 실데이터, 없으면 MOCK
//   node bot.js --record        # 틱을 ticks.csv에 기록
//   node bot.js --once          # 1회 평가 후 종료(스모크 테스트)
//
// 환경변수:
//   KIS_APP_KEY/KIS_APP_SECRET        → KIS 실시간 시세
//   TOSS_CLIENT_ID/TOSS_CLIENT_SECRET → 토스 시세(보조)
//   ARB_POLL_MS(기본 1000), ARB_MOCK_LAG_MS(기본 4000)

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// .env 로더 — 이 폴더의 .env를 읽는다(동적 import 전에 실행).
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

const { ALL_CODES, nameOf } = await import('./instruments.js');
const { Board } = await import('./bars.js');
const { evaluate, evaluateDisparity, DEFAULT_CONFIG } = await import('./signal.js');
const { createFeed } = await import('./feeds.js');
const { emit, logPath } = await import('./notify.js');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const args = new Set(process.argv.slice(2));
const RECORD = args.has('--record');
const ONCE = args.has('--once');
const POLL_MS = Number(process.env.ARB_POLL_MS || 1000);
const TICKS_PATH = process.env.ARB_TICKS_PATH || path.join(__dirname, 'ticks.csv');

const board = new Board(ALL_CODES);
const feed = await createFeed(ALL_CODES);

let tickStream = null;
if (RECORD) {
  tickStream = fs.createWriteStream(TICKS_PATH, { flags: 'w' });
  tickStream.write('ts,code,price\n');
}

console.log('==================================================================');
console.log(' ⚠️  고위험 트레이딩(HIGH-RISK)  ⚠️');
console.log(' 단기 차익거래 알람 도구입니다. 차익거래 창은 매우 짧고, 호가 스프레드·');
console.log(' 수수료·슬리피지·체결 실패·급격한 역행으로 원금 손실 위험이 큽니다.');
console.log(' 본 봇은 알람·리서치 전용이며 투자 권유가 아닙니다. 자동주문 미포함.');
console.log(' 초단타·고빈도 매매는 증권사 FDS(이상거래 탐지)로 계좌·API가 제한될');
console.log(' 수 있습니다. 폴링≥1초·약관 rate limit을 준수하세요.');
console.log('==================================================================');
console.log(`[arb-bot] mode=${feed.mode}  poll=${POLL_MS}ms  종목=${ALL_CODES.length}개`);
console.log(`[arb-bot] 알람 로그: ${logPath()}${RECORD ? `  틱기록: ${TICKS_PATH}` : ''}`);
console.log(`[arb-bot] 확인 타임프레임: ${DEFAULT_CONFIG.confirmTimeframes.join(', ')}  (초단기 노이즈 차단)\n`);

let polls = 0;
async function step() {
  const ticks = await feed.poll();
  board.ingest(ticks);
  if (tickStream) for (const t of ticks) tickStream.write(`${t.ts},${t.code},${t.price}\n`);

  const { signals } = evaluate(board, DEFAULT_CONFIG);
  for (const s of signals) emit(s, { mode: feed.mode });
  // 괴리율(iNAV) 신호 — NAV가 들어오는 모드(MOCK/KIS)에서만 발화.
  const { signals: dispSignals } = evaluateDisparity(board, DEFAULT_CONFIG);
  for (const s of dispSignals) emit(s, { mode: feed.mode });

  polls++;
  // 워밍업 안내(바가 차기 전).
  if (polls === 1) console.log('[arb-bot] 워밍업 중… 타임프레임 바가 채워지면 시그널 평가 시작\n');
}

if (ONCE) {
  await step();
  process.exit(0);
}

console.log('[arb-bot] 시작. Ctrl+C로 종료.\n');
const timer = setInterval(() => {
  step().catch((e) => console.error('[arb-bot] step 오류:', e.message));
}, POLL_MS);

process.on('SIGINT', () => {
  clearInterval(timer);
  if (tickStream) tickStream.end();
  console.log('\n[arb-bot] 종료.');
  process.exit(0);
});
