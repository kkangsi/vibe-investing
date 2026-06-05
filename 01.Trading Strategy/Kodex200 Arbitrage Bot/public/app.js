// app.js — 대시보드 프론트엔드. /api/state 폴링 → 렌더, /api/source 로 소스 전환.
const $ = (s) => document.querySelector(s);
const TFS = ['30s', '60s', '2m', '3m', '5m'];
const CONFIRM = ['60s', '2m'];

const pct = (x, d = 2) => (x == null ? '–' : `${x >= 0 ? '+' : ''}${(x * 100).toFixed(d)}%`);
const won = (x) => (x == null ? '–' : Math.round(x).toLocaleString('ko-KR'));
const cls = (x) => (x == null || Math.abs(x) < 1e-9 ? 'flat' : x > 0 ? 'up' : 'down');

let health = null;

async function loadHealth() {
  health = await fetch('/api/health').then((r) => r.json());
  renderSource();
}

function renderSource() {
  const seg = $('#sourceSeg');
  [...seg.children].forEach((b) => {
    const src = b.dataset.source;
    b.classList.toggle('active', src === health.requested);
    // 자격증명 없는 실소스는 비활성(선택은 가능하되 MOCK 폴백 안내).
    const avail = health.availability || {};
    b.disabled = false;
    b.title = (src === 'KIS' || src === 'TOSS') && !avail[src]
      ? `${src} 자격증명 없음 → 선택 시 MOCK으로 동작` : '';
  });
  const badge = $('#modeBadge');
  const mock = health.mock;
  const mismatch = health.requested !== 'AUTO' && health.requested !== health.resolved;
  badge.textContent = mock
    ? (mismatch ? `MOCK (${health.requested} 키없음)` : 'MOCK')
    : `LIVE · ${health.resolved}`;
  badge.className = 'mode-badge ' + (mock ? (mismatch ? 'warn' : 'mock') : 'live');
  $('#footMeta').textContent =
    `소스 ${health.resolved} · poll ${health.pollMs}ms · 확인TF ${health.confirmTimeframes.join('·')} · ${health.codes}종목 · Node ${health.node}`;
}

$('#sourceSeg').addEventListener('click', async (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;
  health = await fetch('/api/source', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ source: btn.dataset.source }),
  }).then((r) => r.json());
  renderSource();
});

function renderDrivers(drivers, composite) {
  $('#driverCards').innerHTML = drivers.map((d) => `
    <div class="dcard">
      <div><span class="nm">${d.name}</span><span class="wt">${(d.weight * 100).toFixed(0)}% 비중</span></div>
      <div class="px">${won(d.price)}</div>
      <div class="tfs">${TFS.map((tf) => {
        const t = d.trends[tf];
        const c = t ? cls(t.ret) : 'flat';
        const cf = t && t.confirmed ? ' cf' : '';
        return `<span class="tfchip${cf}"><span class="muted">${tf}</span> <span class="${c}">${t ? pct(t.ret) : '–'}</span></span>`;
      }).join('')}</div>
    </div>`).join('');

  $('#compositeRow').innerHTML =
    `<span class="lbl">합성 지수수익률</span>` +
    TFS.map((tf) => `<span class="tfchip"><span class="muted">${tf}</span> <span class="${cls(composite[tf])}">${pct(composite[tf])}</span></span>`).join('');
}

function gapColor(gap) {
  if (gap == null) return '';
  const a = Math.min(0.4, Math.abs(gap) * 30); // 0.3%↑ 진하게
  const rgb = gap > 0 ? '255,90,95' : '47,140,255';
  return `background:rgba(${rgb},${a.toFixed(3)})`;
}

function renderTrackers(trackers, signals) {
  const sigByCode = {};
  for (const s of signals.leadlag) sigByCode[s.code] = s.direction;
  $('#trackerBody').innerHTML = trackers.map((t) => {
    const dispCls = cls(t.disparity);
    const dispStrong = t.disparityConfirmed ? ' strong' : '';
    const sig = sigByCode[t.code];
    const sigBadge = sig ? `<span class="badge-sig ${sig}">LL ${sig === 'UP' ? '▲' : '▼'}</span>` : '';
    const cells = TFS.map((tf) => {
      const g = t.perTf[tf];
      const gap = g ? g.gap : null;
      const strong = CONFIRM.includes(tf) && gap != null && Math.abs(gap) >= 0.0015 ? ' strong' : '';
      return `<td class="cell-gap ${cls(gap)}${strong}" style="${gapColor(gap)}">${gap == null ? '–' : pct(gap)}</td>`;
    }).join('');
    return `<tr>
      <td class="left nm">${t.name}${sigBadge}<div class="kind">${t.code} · ${t.kind}</div></td>
      <td>${t.leverage > 0 ? '+' : ''}${t.leverage}x</td>
      <td>${won(t.price)}</td>
      <td>${t.nav == null ? '–' : won(t.nav)}</td>
      <td class="${dispCls}${dispStrong}">${pct(t.disparity)}</td>
      ${cells}
    </tr>`;
  }).join('');
}

function renderAlerts(alerts) {
  $('#alertCount').textContent = alerts.length ? `(${alerts.length})` : '';
  const list = $('#alertList');
  if (!alerts.length) { list.innerHTML = '<li class="empty">아직 발화한 알람이 없습니다 (워밍업/임계 미달)</li>'; return; }
  list.innerHTML = alerts.map((a) => {
    const arrow = a.direction === 'UP' ? '▲' : '▼';
    const ac = a.direction === 'UP' ? 'up' : 'down';
    const hhmm = a.time.slice(11, 19);
    const label = a.type === 'DISPARITY' ? '괴리율' : 'lead-lag';
    return `<li>
      <span class="t">${hhmm}</span>
      <span class="atag ${a.type}">${label}</span>
      <span class="${ac}">${arrow} ${a.name}</span>
      <span class="muted">${pct(a.metric)}</span>
      <span>${a.action}</span>
    </li>`;
  }).join('');
}

async function tick() {
  try {
    const s = await fetch('/api/state').then((r) => r.json());
    if (s.source && health && s.source.resolved !== health.resolved) await loadHealth();
    renderDrivers(s.drivers, s.composite);
    renderTrackers(s.trackers, s.signals);
    renderAlerts(s.alerts);
  } catch (e) { /* 일시 오류 무시 */ }
}

(async function main() {
  await loadHealth();
  await tick();
  setInterval(tick, 1500);
})();
