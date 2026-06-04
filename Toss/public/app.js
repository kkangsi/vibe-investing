// app.js — 대시보드 프론트엔드 (vanilla JS)

const SIGNAL_KR = { BUY: '매수', HOLD: '보유', SELL: '매도', AVOID: '회피' };

const fmt = (n) => (n == null ? '–' : Number(n).toLocaleString('ko-KR'));
const pct = (n) => (n == null ? '–' : `${n > 0 ? '+' : ''}${n}%`);

async function getJSON(url) {
  const res = await fetch(url);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || `요청 실패 (${res.status})`);
  return data;
}

function signalPill(sig) {
  return `<span class="signal-pill ${sig}">${SIGNAL_KR[sig] || sig}</span>`;
}

function tile(item) {
  const score = item.momentum_score ?? 0;
  const metrics = `
    <span>12-1 <b>${pct(item.ret_12_1_pct)}</b></span>
    <span>6-1 <b>${pct(item.ret_6_1_pct)}</b></span>
    <span>변동성 <b>${item.vol_60d_ann_pct ?? '–'}%</b></span>`;
  return `
    <div class="tile ${item.signal}">
      <div class="tile-head">
        <div>
          <div class="tile-name">${item.name} <span class="tile-code">${item.code}</span></div>
          ${item.tag ? `<div class="tile-tag">${item.tag}</div>` : ''}
        </div>
        ${signalPill(item.signal)}
      </div>
      <div class="tile-price">${fmt(item.price)}<span style="font-size:12px;color:var(--muted)"> 원</span></div>
      <div class="score-bar"><div class="score-fill" style="width:${score}%"></div></div>
      <div class="tile-metrics">${metrics}</div>
      <div class="tile-reason">${item.reason || ''}</div>
    </div>`;
}

function renderRegime(regime, mock) {
  const el = document.getElementById('regime');
  el.innerHTML = `
    <div class="regime-grid">
      <span class="regime-badge ${regime.regime}">${regime.label || regime.regime}</span>
      <div class="regime-metric">KODEX 200<b>${fmt(regime.benchmark)}</b></div>
      <div class="regime-metric">200일선<b>${fmt(regime.ma200)}</b></div>
      <div class="regime-metric">200일선 대비<b>${pct(regime.pct_above_ma200)}</b></div>
      <div class="regime-metric">5일 수익률<b>${pct(regime.ret_5d_pct)}</b></div>
      <div class="regime-metric">20일 변동성<b>${regime.vol_20d_ann_pct ?? '–'}%</b></div>
      <div class="regime-action">📌 권고: <b>${regime.action}</b></div>
    </div>`;

  const banner = document.getElementById('modeBanner');
  if (mock) {
    banner.classList.remove('hidden');
    banner.innerHTML = '⚠️ <b>MOCK 모드</b> — 토스 Open API 자격증명(TOSS_CLIENT_ID/SECRET)이 없어 결정론적 시연 데이터로 동작 중입니다. 실데이터는 .env 설정 후 표시됩니다.';
  } else {
    banner.classList.add('hidden');
  }
}

function renderDashboard(data) {
  renderRegime(data.regime, data.mock);

  document.getElementById('etfGrid').innerHTML = data.etfs.map(tile).join('');

  const sectorsEl = document.getElementById('sectors');
  sectorsEl.innerHTML = data.sectors.map((s) => `
    <div class="sector-block">
      <div class="sector-title">${s.name} <span class="count">${s.items.length}종목</span></div>
      <div class="grid">${s.items.map(tile).join('')}</div>
    </div>`).join('');
}

function renderSearch(data) {
  const el = document.getElementById('searchResult');
  el.classList.remove('hidden');
  const r = data.result;
  el.innerHTML = `
    <h3>🔍 ${r.name} <span style="font-size:13px;color:var(--muted)">${r.code} · ${r.sector || ''}</span> ${signalPill(r.signal)}</h3>
    <div class="sr-row">
      <div class="sr-metric">현재가<b>${fmt(r.price)} 원</b></div>
      <div class="sr-metric">모멘텀 점수<b>${r.momentum_score ?? '–'} / 100</b></div>
      <div class="sr-metric">손절선<b>${fmt(r.stop_price)} 원</b></div>
      <div class="sr-metric">12-1 모멘텀<b>${pct(r.ret_12_1_pct)}</b></div>
      <div class="sr-metric">6-1 모멘텀<b>${pct(r.ret_6_1_pct)}</b></div>
      <div class="sr-metric">고점대비<b>${pct(r.drawdown_from_high_pct)}</b></div>
      <div class="sr-reason">근거: ${r.reason || ''} · 레짐: <b>${data.regime.label}</b></div>
    </div>`;
  el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function doSearch() {
  const q = document.getElementById('searchInput').value.trim();
  if (!q) return;
  const el = document.getElementById('searchResult');
  el.classList.remove('hidden');
  el.innerHTML = '<div>검색 중…</div>';
  try {
    const data = await getJSON(`/api/search?q=${encodeURIComponent(q)}`);
    renderSearch(data);
  } catch (e) {
    el.innerHTML = `<div class="error">⚠️ ${e.message}</div>`;
  }
}

document.getElementById('searchBtn').addEventListener('click', doSearch);
document.getElementById('searchInput').addEventListener('keydown', (e) => { if (e.key === 'Enter') doSearch(); });

(async function init() {
  try {
    const data = await getJSON('/api/dashboard');
    renderDashboard(data);
  } catch (e) {
    document.getElementById('regime').innerHTML = `<div class="error">⚠️ 대시보드 로드 실패: ${e.message}</div>`;
  }
  // 공유 가능한 검색 링크: /?q=삼성전자 로 접속하면 자동 검색
  const q = new URLSearchParams(location.search).get('q');
  if (q) {
    document.getElementById('searchInput').value = q;
    doSearch();
  }
})();
