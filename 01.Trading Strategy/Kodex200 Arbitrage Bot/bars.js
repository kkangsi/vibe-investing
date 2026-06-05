// bars.js
// =======
// 틱 스트림 → 멀티 타임프레임 OHLC 바 집계 + 추세 확인.
//
// 토스/KIS 모두 30초·60초 캔들을 직접 주지 않으므로(토스 캔들 API는 1분봉·일봉만
// 제공), 1초 폴링으로 받은 현재가 틱을 여기서 30s/60s/2m/3m/5m 바로 리샘플링한다.
//
// 핵심 요구사항: "밀리세컨드가 아니라 30초~5분 추세를, 그것도 너무 단기 말고
//                일정 시간 지속되는 추세를 검증" → trendOf()가 단일 바가 아니라
//                최근 N개 바의 '방향 일관성(consistency)'까지 함께 반환한다.

// 표준 타임프레임(ms). 라벨은 표시/설정 키로 사용.
export const TIMEFRAMES = [
  { key: '30s', ms: 30_000 },
  { key: '60s', ms: 60_000 },
  { key: '2m', ms: 120_000 },
  { key: '3m', ms: 180_000 },
  { key: '5m', ms: 300_000 },
];

// 한 (종목 × 타임프레임)에 대한 바 시계열.
class Series {
  constructor(tfMs, maxBars = 40) {
    this.tfMs = tfMs;
    this.maxBars = maxBars;
    this.bars = []; // { t0, open, high, low, close }  (완료 + 진행중, 과거→현재)
  }

  push(price, tsMs) {
    const bucket = Math.floor(tsMs / this.tfMs) * this.tfMs;
    const cur = this.bars[this.bars.length - 1];
    if (!cur || cur.t0 !== bucket) {
      this.bars.push({ t0: bucket, open: price, high: price, low: price, close: price });
      if (this.bars.length > this.maxBars) this.bars.shift();
    } else {
      cur.high = Math.max(cur.high, price);
      cur.low = Math.min(cur.low, price);
      cur.close = price;
    }
  }

  // 최근 lookback개 바의 종가 배열(과거→현재). 진행중 바 포함.
  closes(lookback) {
    return this.bars.slice(-lookback).map((b) => b.close);
  }
}

// 한 종목의 모든 타임프레임 묶음.
export class Instrument {
  constructor() {
    this.series = new Map(TIMEFRAMES.map((tf) => [tf.key, new Series(tf.ms)]));
    this.lastPrice = null;
    this.lastNav = null;
    this.navBuf = []; // 괴리율 추세 확인용 [{ ts, disp }] (disp = (price-nav)/nav)
    this.navBufMax = 60;
  }

  onTick(price, tsMs, nav = null) {
    if (!Number.isFinite(price)) return;
    this.lastPrice = price;
    for (const s of this.series.values()) s.push(price, tsMs);
    if (Number.isFinite(nav) && nav > 0) {
      this.lastNav = nav;
      this.navBuf.push({ ts: tsMs, disp: price / nav - 1 });
      if (this.navBuf.length > this.navBufMax) this.navBuf.shift();
    }
  }

  // 괴리율 추세. 최근 lookback개 샘플이 모두 band를 넘고 같은 부호로 '지속'될 때만 confirmed.
  //   disp>0: 시장가 > NAV (프리미엄, 고평가) / disp<0: 디스카운트(저평가)
  disparityOf({ band = 0.003, lookback = 5, minConsistency = 0.8 } = {}) {
    const buf = this.navBuf.slice(-lookback);
    if (buf.length < lookback) return { disp: this.lastDisp(), confirmed: false, bars: buf.length };
    const disp = buf[buf.length - 1].disp;
    const dir = Math.sign(disp);
    let agree = 0;
    for (const b of buf) if (Math.sign(b.disp) === dir && Math.abs(b.disp) >= band) agree++;
    const consistency = agree / buf.length;
    const confirmed = Math.abs(disp) >= band && consistency >= minConsistency && dir !== 0;
    return { disp, confirmed, consistency, bars: buf.length };
  }

  lastDisp() {
    return this.navBuf.length ? this.navBuf[this.navBuf.length - 1].disp : null;
  }

  // 타임프레임별 추세. 반환:
  //   ret         : lookback 구간 누적 수익률(첫 바 시가 → 마지막 바 종가)
  //   consistency : 바 단위 수익률이 ret 부호와 같은 비율(0~1). "지속성" 지표.
  //   bars        : 사용된 바 개수
  //   confirmed   : |ret| ≥ minRet 이고 consistency ≥ minConsistency 일 때 true
  trendOf(tfKey, { lookback = 4, minRet = 0.0015, minConsistency = 0.6 } = {}) {
    const s = this.series.get(tfKey);
    if (!s) return null;
    const closes = s.closes(lookback + 1); // 구간 수익률엔 경계가 lookback+1개 필요
    if (closes.length < 3) return { ret: 0, consistency: 0, bars: closes.length, confirmed: false };

    const ret = closes[closes.length - 1] / closes[0] - 1;
    const dir = Math.sign(ret);
    let agree = 0;
    let steps = 0;
    for (let i = 1; i < closes.length; i++) {
      const step = Math.sign(closes[i] - closes[i - 1]);
      if (step === 0) continue;
      steps++;
      if (step === dir) agree++;
    }
    const consistency = steps ? agree / steps : 0;
    const confirmed = Math.abs(ret) >= minRet && consistency >= minConsistency && dir !== 0;
    return { ret, consistency, bars: closes.length, confirmed };
  }
}

// 종목 묶음 전체를 들고 있는 보드.
export class Board {
  constructor(codes) {
    this.byCode = new Map(codes.map((c) => [c, new Instrument()]));
  }

  ingest(ticks) {
    for (const t of ticks) {
      const inst = this.byCode.get(t.code);
      if (inst) inst.onTick(t.price, t.ts, t.nav);
    }
  }

  get(code) {
    return this.byCode.get(code);
  }
}
