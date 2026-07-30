# -*- coding: utf-8 -*-
"""Build interactive CTH accuracy explorer HTML from cth-sim-matrix.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "cth-sim-matrix.json"), encoding="utf-8") as f:
    data = json.load(f)
data_js = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

html = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>JAZZ CTH Accuracy Matrix</title>
<style>
:root {
  --bg:#16171a; --panel:#22252b; --line:#3a3f4a; --text:#e8eaed; --muted:#9aa0a6;
  --accent:#c4a35a; --good:#6abf69; --mid:#d4a017; --bad:#e07070;
  --mono:ui-monospace,Consolas,monospace; --sans:"Segoe UI",system-ui,sans-serif;
}
*{box-sizing:border-box}
body{margin:0;font-family:var(--sans);background:var(--bg);color:var(--text)}
header{padding:14px 18px;border-bottom:1px solid var(--line);background:var(--panel)}
header h1{margin:0 0 4px;font-size:1.15rem;color:var(--accent)}
header p{margin:0;color:var(--muted);font-size:.82rem;max-width:980px}
.bar{display:flex;flex-wrap:wrap;gap:10px;padding:12px 18px;border-bottom:1px solid var(--line);background:#1c1e23;align-items:end}
.bar label{display:block;font-size:.7rem;color:var(--muted);margin-bottom:3px}
.bar select,.bar input{background:var(--panel);border:1px solid var(--line);color:var(--text);border-radius:4px;padding:6px 8px;min-width:120px}
.bar .chk{display:flex;align-items:center;gap:6px;font-size:.82rem;padding-bottom:6px}
main{padding:12px 18px}
table{width:100%;border-collapse:collapse;font-size:.78rem}
th,td{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;white-space:nowrap}
th{position:sticky;top:0;background:#1c1e23;color:var(--muted);font-weight:500;z-index:1}
td:first-child,th:first-child,td:nth-child(2),th:nth-child(2),td:nth-child(3),th:nth-child(3){text-align:left}
td.id{font-family:var(--mono);color:var(--accent)}
.cell{font-family:var(--mono);font-weight:600}
.note{color:var(--muted);font-size:.75rem;margin:8px 0 14px}
.fam{display:inline-block;padding:1px 6px;border:1px solid var(--line);border-radius:999px;font-size:.68rem;color:var(--muted)}
.stats{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:12px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px 12px;min-width:120px}
.stat b{display:block;font-size:1.2rem;font-family:var(--mono);color:var(--accent)}
.stat span{font-size:.72rem;color:var(--muted)}
canvas{width:100%;max-width:900px;height:220px;background:#121316;border:1px solid var(--line);border-radius:6px}
</style>
</head>
<body>
<header>
  <h1>JAZZ · матрица точности (iron sights)</h1>
  <p>Симуляция AccuracyRangeCTH: профили стрелка × дистанции. Без situational (укрытие/ночь).
  Recoil не влияет на первую пулю. Damage/калибр здесь не считаются — только CTH.</p>
</header>
<div class="bar">
  <div><label>Семейство</label><select id="family"><option value="">Все</option></select></div>
  <div><label>Профиль</label><select id="profile"></select></div>
  <div><label>Сортировка</label><select id="sort">
    <option value="d12">CTH @12</option>
    <option value="d20">CTH @20</option>
    <option value="d30">CTH @30</option>
    <option value="d8">CTH @8</option>
    <option value="tier">Tier</option>
    <option value="id">ID</option>
    <option value="AA">AimAccuracy</option>
    <option value="R">WeaponRange</option>
  </select></div>
  <div><label>Поиск</label><input id="q" placeholder="AK47, HiPower…"/></div>
  <div class="chk"><input type="checkbox" id="onlyOut"/><label for="onlyOut" style="margin:0">Только outlier-кандидаты</label></div>
</div>
<main>
  <div class="stats" id="stats"></div>
  <canvas id="chart" width="900" height="220"></canvas>
  <p class="note">Линии — выбранное семейство (или все) средний CTH по дистанции для текущего профиля. Точки — выбранное оружие (клик по строке).</p>
  <table>
    <thead id="thead"></thead>
    <tbody id="tbody"></tbody>
  </table>
</main>
<script>
const DATA = ''' + data_js + r''';
const DISTS = DATA.distances;
const $ = id => document.getElementById(id);
const fams = [...new Set(DATA.weapons.map(w => w.family))].sort();
fams.forEach(f => { const o=document.createElement('option'); o.value=f; o.textContent=f; $('family').appendChild(o); });
DATA.profiles.forEach(p => {
  const o=document.createElement('option');
  o.value=p.id;
  const aim = p.aim ? 'full aim' : 'snap';
  o.textContent = p.id + '  Dex'+p.dex+'/Mrk'+p.mrk+'/L'+p.lvl+' '+aim;
  $('profile').appendChild(o);
});
$('profile').value = 'A70f';

const OUTLIER_IDS = new Set((DATA.outliers_A70f||[]).map(o => o.id));
OUTLIER_IDS.add('HiPower');
OUTLIER_IDS.add('Type56');
OUTLIER_IDS.add('STG44');
OUTLIER_IDS.add('FG42');
OUTLIER_IDS.add('Thompson');
OUTLIER_IDS.add('Auto5_quest');
OUTLIER_IDS.add('Glock17');
OUTLIER_IDS.add('MG58');
OUTLIER_IDS.add('ArcticWarfare');

function colorFor(v) {
  if (v <= 0) return 'var(--muted)';
  if (v >= 75) return 'var(--good)';
  if (v >= 45) return 'var(--accent)';
  if (v >= 20) return 'var(--mid)';
  return 'var(--bad)';
}

let selected = null;

function filtered() {
  const fam = $('family').value;
  const q = $('q').value.trim().toLowerCase();
  const only = $('onlyOut').checked;
  return DATA.weapons.filter(w => {
    if (fam && w.family !== fam) return false;
    if (only && !OUTLIER_IDS.has(w.id)) return false;
    if (q && !(w.id.toLowerCase().includes(q) || w.name.toLowerCase().includes(q))) return false;
    return true;
  });
}

function sortRows(rows) {
  const key = $('sort').value;
  const prof = $('profile').value;
  const copy = rows.slice();
  copy.sort((a,b) => {
    if (key.startsWith('d')) {
      const d = key.slice(1);
      return (b.cth[prof][d]||0) - (a.cth[prof][d]||0);
    }
    if (key === 'tier') return (a.tier||'').localeCompare(b.tier||'') || a.id.localeCompare(b.id);
    if (key === 'id') return a.id.localeCompare(b.id);
    return (b[key]||0) - (a[key]||0) || a.id.localeCompare(b.id);
  });
  return copy;
}

function render() {
  const prof = $('profile').value;
  const rows = sortRows(filtered());
  $('thead').innerHTML = '<tr><th>ID</th><th>Name</th><th>Fam / Tier</th><th>AA</th><th>Max</th><th>R</th><th>BDR</th><th>G</th>' +
    DISTS.map(d => '<th>@'+d+'</th>').join('') + '</tr>';
  const tb = $('tbody');
  tb.innerHTML = '';
  rows.forEach(w => {
    const tr = document.createElement('tr');
    if (selected === w.id) tr.style.background = '#2a2f38';
    tr.innerHTML = '<td class="id">'+w.id+'</td><td>'+w.name+'</td><td><span class="fam">'+w.family+'</span> '+
      (w.tier||'—')+'</td><td>'+w.AA+'</td><td>'+w.MaxAim+'</td><td>'+w.R+'</td><td>'+w.BDR+'</td><td>'+w.G+'</td>' +
      DISTS.map(d => {
        const v = w.cth[prof][String(d)]||0;
        return '<td class="cell" style="color:'+colorFor(v)+'">'+v+'</td>';
      }).join('');
    tr.addEventListener('click', () => { selected = w.id; render(); draw(); });
    tb.appendChild(tr);
  });

  // stats for current filter @ profile
  const at = d => {
    const xs = rows.map(w => w.cth[prof][String(d)]||0).filter(v => v>0);
    if (!xs.length) return '—';
    return Math.round(xs.reduce((a,b)=>a+b,0)/xs.length);
  };
  $('stats').innerHTML = [
    ['Оружий', rows.length],
    ['Avg @8', at(8)+'%'],
    ['Avg @12', at(12)+'%'],
    ['Avg @20', at(20)+'%'],
    ['Avg @30', at(30)+'%'],
    ['Avg @40', at(40)+'%'],
  ].map(p => '<div class="stat"><b>'+p[1]+'</b><span>'+p[0]+'</span></div>').join('');
  draw();
}

function draw() {
  const canvas = $('chart');
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0,0,W,H);
  const pad = {l:36,r:12,t:12,b:28};
  const pw = W-pad.l-pad.r, ph = H-pad.t-pad.b;
  const prof = $('profile').value;
  const fam = $('family').value;
  const pool = fam ? DATA.weapons.filter(w=>w.family===fam) : DATA.weapons;

  ctx.strokeStyle = '#3a3f4a'; ctx.fillStyle='#9aa0a6'; ctx.font='11px sans-serif';
  for (let p=0;p<=100;p+=25) {
    const y = pad.t + ph*(1-p/100);
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(W-pad.r,y); ctx.stroke();
    ctx.fillText(String(p), 4, y+3);
  }
  DISTS.forEach((d,i) => {
    const x = pad.l + (i/(DISTS.length-1))*pw;
    ctx.fillText(String(d), x-6, H-8);
  });

  // family / all average
  ctx.beginPath();
  ctx.strokeStyle = '#5b8def';
  DISTS.forEach((d,i) => {
    const xs = pool.map(w => w.cth[prof][String(d)]||0);
    const avg = xs.reduce((a,b)=>a+b,0)/xs.length;
    const x = pad.l + (i/(DISTS.length-1))*pw;
    const y = pad.t + ph*(1-avg/100);
    if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  });
  ctx.stroke();

  if (selected) {
    const w = DATA.weapons.find(x => x.id === selected);
    if (w) {
      ctx.beginPath();
      ctx.strokeStyle = '#c4a35a';
      DISTS.forEach((d,i) => {
        const v = w.cth[prof][String(d)]||0;
        const x = pad.l + (i/(DISTS.length-1))*pw;
        const y = pad.t + ph*(1-v/100);
        if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
        ctx.fillStyle='#c4a35a';
        ctx.beginPath(); ctx.arc(x,y,3,0,Math.PI*2); ctx.fill();
        ctx.beginPath();
      });
      // re-stroke line properly
      ctx.beginPath();
      ctx.strokeStyle = '#c4a35a';
      DISTS.forEach((d,i) => {
        const v = w.cth[prof][String(d)]||0;
        const x = pad.l + (i/(DISTS.length-1))*pw;
        const y = pad.t + ph*(1-v/100);
        if (i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      });
      ctx.stroke();
      ctx.fillStyle='#c4a35a';
      ctx.fillText(w.id, pad.l+8, pad.t+14);
    }
  }
}

['family','profile','sort','onlyOut'].forEach(id => $(id).addEventListener('change', render));
$('q').addEventListener('input', render);
render();
</script>
</body>
</html>
'''

out = os.path.join(HERE, "cth-accuracy-matrix.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("Wrote", out, os.path.getsize(out))
os.remove(os.path.join(HERE, "_matrix_min.json"))
