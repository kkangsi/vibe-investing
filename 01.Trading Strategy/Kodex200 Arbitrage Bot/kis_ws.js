// kis_ws.js
// =========
// KIS 실시간 체결가(H0STCNT0) WebSocket 스트리밍 클라이언트.
// REST 1초 폴링보다 지연이 작아 lead-lag 탐지에 유리하다.
//
//   1) approval_key 발급: POST /oauth2/Approval (appkey/secretkey)
//   2) ws 연결 후 종목별 H0STCNT0 구독 메시지 전송(tr_type '1')
//   3) 데이터 프레임(파이프 구분): `<암호화>|H0STCNT0|<건수>|<body>`
//      body는 ^로 구분된 46필드/건. [0]=종목코드, [2]=현재가.
//   4) PINGPONG(JSON) 수신 시 동일 프레임으로 응답.
//
// Node 22+ 내장 WebSocket(globalThis.WebSocket)을 사용해 무의존성을 유지한다.
// 없으면 createKisWs()가 null을 반환 → feeds.js가 REST 폴링으로 폴백한다.

const httpBase = () => process.env.KIS_BASE_URL || 'https://openapi.koreainvestment.com:9443';
// 실전 21000 / 모의 31000. KIS_WS_URL로 override 가능.
const wsBase = () =>
  process.env.KIS_WS_URL ||
  (process.env.KIS_PAPER === '1'
    ? 'ws://ops.koreainvestment.com:31000'
    : 'ws://ops.koreainvestment.com:21000');

const FIELDS_PER_RECORD = 46; // H0STCNT0 응답 1건당 필드 수
const IDX_CODE = 0;
const IDX_PRICE = 2;

async function getApprovalKey() {
  const res = await fetch(`${httpBase()}/oauth2/Approval`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'client_credentials',
      appkey: process.env.KIS_APP_KEY,
      secretkey: process.env.KIS_APP_SECRET,
    }),
  });
  if (!res.ok) throw new Error(`KIS approval_key 실패: ${res.status} ${await res.text()}`);
  const json = await res.json();
  if (!json.approval_key) throw new Error('approval_key 없음(응답 형식 확인)');
  return json.approval_key;
}

function subscribeMsg(approvalKey, code) {
  return JSON.stringify({
    header: {
      approval_key: approvalKey,
      custtype: 'P',
      tr_type: '1', // 등록(해지는 '2')
      'content-type': 'utf-8',
    },
    body: { input: { tr_id: 'H0STCNT0', tr_key: code } },
  });
}

function parseDataFrame(text) {
  // `<enc>|H0STCNT0|<cnt>|<body>`
  const parts = text.split('|');
  if (parts.length < 4 || parts[1] !== 'H0STCNT0') return [];
  const cnt = parseInt(parts[2], 10) || 1;
  const body = parts.slice(3).join('|').split('^');
  const ts = Date.now();
  const out = [];
  for (let r = 0; r < cnt; r++) {
    const base = r * FIELDS_PER_RECORD;
    const code = body[base + IDX_CODE];
    const price = parseFloat(body[base + IDX_PRICE]);
    if (code && Number.isFinite(price)) out.push({ code, price, ts });
  }
  return out;
}

// 스트리밍 피드. 반환: { mode, poll(), close() }  — poll()은 마지막 호출 이후 누적 틱을 drain.
export async function createKisWs(codes) {
  if (typeof globalThis.WebSocket === 'undefined') return null; // Node<22 → 폴백
  const approvalKey = await getApprovalKey();

  let buffer = [];
  let ws = null;
  let closed = false;

  function connect() {
    ws = new globalThis.WebSocket(wsBase());
    ws.addEventListener('open', () => {
      for (const code of codes) ws.send(subscribeMsg(approvalKey, code));
      console.log(`[kis-ws] 연결·구독 완료 (${codes.length}종목)`);
    });
    ws.addEventListener('message', (ev) => {
      const text = typeof ev.data === 'string' ? ev.data : String(ev.data);
      if (text[0] === '{') {
        // 제어 메시지(구독 응답/PINGPONG).
        try {
          const j = JSON.parse(text);
          if (j?.header?.tr_id === 'PINGPONG') ws.send(text); // 그대로 되돌려 keepalive
        } catch { /* noop */ }
        return;
      }
      const ticks = parseDataFrame(text);
      if (ticks.length) buffer.push(...ticks);
    });
    ws.addEventListener('close', () => {
      if (closed) return;
      console.error('[kis-ws] 연결 종료 → 3초 후 재연결');
      setTimeout(connect, 3000);
    });
    ws.addEventListener('error', (e) => console.error('[kis-ws] 오류:', e?.message || e));
  }
  connect();

  return {
    mode: 'KIS-WS',
    async poll() {
      const out = buffer;
      buffer = [];
      return out;
    },
    close() {
      closed = true;
      try { ws?.close(); } catch { /* noop */ }
    },
  };
}
