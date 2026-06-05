// feeds.js
// ========
// 통합 시세 피드. 우선순위: KIS(실시간 선택) → 토스 → MOCK.
//   - poll()이 [{ code, price, ts }] 배열을 반환한다(1초 주기 호출 전제).
//   - 실키가 없으면 MOCK: '진짜 지수' 랜덤워크를 만들고, 빅2는 즉시 반영하되
//     ETF는 LAG_MS 만큼 지연 반영시켜 lead-lag를 의도적으로 주입한다.
//     → 봇이 실제로 시그널을 내고, Python 검증기가 그 지연을 되찾아낼 수 있다.

import * as kis from './kis.js';
import { createKisWs } from './kis_ws.js';
import { DRIVERS, TRACKERS } from './instruments.js';

// 토스 클라이언트(이 폴더에 자체 포함된 toss.js).
const toss = await import('./toss.js');

export function pickMode() {
  if (!kis.isMock()) return 'KIS';
  if (!toss.isMock()) return 'TOSS';
  return 'MOCK';
}

// ---- 실시간(토스) Map → 배열 정규화 ----
async function pollToss(codes) {
  const map = await toss.fetchPrices(codes);
  const ts = Date.now();
  const out = [];
  for (const [code, v] of map) if (v?.price != null) out.push({ code, price: v.price, ts });
  return out;
}

// ---- MOCK 합성기(lead-lag 주입) ----
function createMock(codes) {
  const lagMs = Number(process.env.ARB_MOCK_LAG_MS || 4000); // ETF 지연(기본 4초)
  const stepVol = Number(process.env.ARB_MOCK_VOL || 0.0006); // 폴링당 지수 변동성
  // 가끔 강한 추세를 넣어 차익거래 창을 만든다.
  let trend = 0;
  let trendLeft = 0;

  const driverBase = new Map(DRIVERS.map((d, i) => [d.code, 70000 + i * 50000]));
  const trackerBase = new Map(TRACKERS.map((t, i) => [t.code, 10000 + i * 3000]));
  // 지수 누적 로그수익률 히스토리(지연 조회용): [{ ts, cum }]
  const indexHist = [{ ts: Date.now(), cum: 0 }];
  let cum = 0;
  let tick = 0;

  // 결정론 PRNG(시드 고정 — Math.random 회피).
  let seed = 0x9e3779b9;
  const rand = () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  const gauss = () => Math.sqrt(-2 * Math.log(Math.max(1e-9, rand()))) * Math.cos(2 * Math.PI * rand());

  function indexCumAt(targetTs) {
    // targetTs 이하의 가장 최근 누적값(지연 반영).
    let v = indexHist[0].cum;
    for (const h of indexHist) {
      if (h.ts <= targetTs) v = h.cum;
      else break;
    }
    return v;
  }

  return {
    mode: 'MOCK',
    async poll() {
      tick++;
      const ts = Date.now();
      if (trendLeft <= 0 && rand() < 0.15) {
        trend = (rand() < 0.5 ? -1 : 1) * stepVol * (3 + rand() * 4);
        trendLeft = 8 + Math.floor(rand() * 12);
      }
      const drift = trendLeft-- > 0 ? trend : 0;
      const indexStep = drift + stepVol * gauss();
      cum += indexStep;
      indexHist.push({ ts, cum });
      // 오래된 히스토리 정리.
      while (indexHist.length > 600) indexHist.shift();

      const out = [];
      // 빅2: 지수를 즉시 반영 + 개별 노이즈.
      for (const d of DRIVERS) {
        const base = driverBase.get(d.code);
        const idio = 0.0003 * gauss();
        const px = base * Math.exp(cum + idio);
        out.push({ code: d.code, price: Math.round(px), ts });
      }
      // ETF: 지수를 lagMs 지연 반영 × leverage + 추적노이즈.
      const laggedCum = indexCumAt(ts - lagMs);
      for (const t of TRACKERS) {
        const base = trackerBase.get(t.code);
        // 빅2 가격이 exp(cum)이므로 지수 수익률 ≈ cum.
        // 시장가(price)는 지연 반영(laggedCum), NAV(iNAV)는 현재 공정가치(cum)를 즉시 반영.
        // → 급변동 구간에 price와 nav 사이 괴리(premium/discount)가 실제로 발생한다.
        const noise = 0.0002 * gauss();
        const px = base * Math.exp(t.leverage * laggedCum + noise);
        const nav = base * Math.exp(t.leverage * cum); // 노이즈 없는 공정가치
        out.push({
          code: t.code,
          price: Math.round(px * 100) / 100,
          nav: Math.round(nav * 100) / 100,
          ts,
        });
      }
      return out;
    },
  };
}

export async function createFeed(codes) {
  const mode = pickMode();
  if (mode === 'KIS') {
    // Node 22+ 이고 비활성화하지 않았으면 WebSocket 스트리밍 우선.
    if (typeof globalThis.WebSocket !== 'undefined' && process.env.ARB_KIS_WS !== '0') {
      try {
        const ws = await createKisWs(codes);
        if (ws) return withNav(ws, mode); // 시세는 WS, NAV는 REST 보강(괴리율용)
      } catch (e) {
        console.error('[feeds] KIS WS 실패 → REST 폴백:', e.message);
      }
    }
    return withNav({ mode, poll: () => kis.fetchPrices(codes) }, mode);
  }
  if (mode === 'TOSS') return { mode, poll: () => pollToss(codes) };
  return createMock(codes);
}

// 실모드(KIS) 피드에 ETF NAV를 보강한다. NAV는 가격보다 느리게 변하므로 저빈도로
// REST 조회해 캐시하고, poll()이 돌려준 추종 ETF 틱에 nav 필드를 붙인다.
function withNav(feed, mode) {
  const navCache = new Map(); // code -> { nav, at }
  const NAV_TTL = Number(process.env.ARB_NAV_TTL_MS || 5000);
  const trackerCodes = TRACKERS.map((t) => t.code);
  return {
    mode: feed.mode || mode,
    close: feed.close,
    async poll() {
      const ticks = await feed.poll();
      // NAV 갱신(만료된 것만).
      const now = Date.now();
      for (const code of trackerCodes) {
        const hit = navCache.get(code);
        if (hit && now - hit.at < NAV_TTL) continue;
        try {
          const nav = await kis.fetchEtfNav(code);
          if (nav != null) navCache.set(code, { nav, at: now });
        } catch { /* NAV 실패는 무시(괴리율 신호만 비활성) */ }
      }
      for (const t of ticks) {
        const hit = navCache.get(t.code);
        if (hit) t.nav = hit.nav;
      }
      return ticks;
    },
  };
}
