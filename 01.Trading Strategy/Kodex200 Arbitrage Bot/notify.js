// notify.js
// =========
// 알람 싱크: 콘솔 + 로그파일(alerts.log). 외부 의존성 0.
//   - 같은 (코드,방향) 시그널은 COOLDOWN_MS 동안 재발화하지 않음(스팸 차단).
//   - 로그는 JSON Lines로 적재 → Python 검증/리포트에서 그대로 파싱 가능.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LOG_PATH = process.env.ARB_LOG_PATH || path.join(__dirname, 'alerts.log');
const COOLDOWN_MS = Number(process.env.ARB_COOLDOWN_MS || 90_000);

const lastFired = new Map(); // `${code}:${dir}` -> ts

const pct = (x) => `${(x * 100 >= 0 ? '+' : '')}${(x * 100).toFixed(2)}%`;

export function emit(signal, ctx = {}) {
  const key = `${signal.type}:${signal.code}:${signal.direction}`;
  const now = Date.now();
  if (now - (lastFired.get(key) || 0) < COOLDOWN_MS) return false;
  lastFired.set(key, now);

  const time = new Date(now).toISOString();
  const arrow = signal.direction === 'UP' ? '▲' : '▼';
  const body =
    signal.type === 'DISPARITY'
      ? `[괴리율] 괴리 ${pct(signal.disparity)} · 지속 ${(signal.consistency * 100).toFixed(0)}%`
      : `[선행] 지수선행 ${pct(signal.indexRet)} · gap ${pct(signal.gap)} · 빅2확인 ${signal.driversConfirmed}/2`;
  const line = `[${time}] ${arrow} ${signal.name}(${signal.code}) ${body} → ${signal.action}`;

  // 콘솔
  console.log(line);

  // 로그파일(JSONL)
  const record = { time, mode: ctx.mode, ...signal, perTf: undefined }; // perTf는 장황 → 제외
  try {
    fs.appendFileSync(LOG_PATH, JSON.stringify(record) + '\n');
  } catch (e) {
    console.error('alerts.log 기록 실패:', e.message);
  }
  return true;
}

export function logPath() {
  return LOG_PATH;
}
