# Build self-contained docs/tools/merc-salary-calculator.html from merc-salary-data.json.
# Run after _export_merc_salary_json.py (or this script will try to export first).
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSON = HERE / "merc-salary-data.json"
OUT = HERE / "merc-salary-calculator.html"
EXPORT = HERE / "_export_merc_salary_json.py"

HTML_HEAD = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>JAZZ · калькулятор зарплат наёмников</title>
<style>
:root{--bg:#16171a;--panel:#22252b;--line:#3a3f4a;--text:#e8eaed;--muted:#9aa0a6;--accent:#c4a35a;--good:#6abf69;--bad:#e07070;--warn:#d4a017;--mono:ui-monospace,Consolas,monospace;--sans:"Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;font-family:var(--sans);background:var(--bg);color:var(--text)}
header{padding:14px 18px;border-bottom:1px solid var(--line);background:var(--panel)}
header h1{margin:0 0 4px;font-size:1.15rem;color:var(--accent)}
header p{margin:0;color:var(--muted);font-size:.82rem;max-width:960px;line-height:1.45}
.layout{display:grid;grid-template-columns:minmax(280px,380px) 1fr;gap:0;min-height:calc(100vh - 88px)}
@media(max-width:900px){.layout{grid-template-columns:1fr}}
.side{border-right:1px solid var(--line);background:#1c1e23;padding:12px 14px;display:flex;flex-direction:column;gap:10px;max-height:calc(100vh - 88px);overflow:auto}
.main{padding:14px 18px 40px;overflow:auto}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:end}
.bar label,.field label{display:block;font-size:.7rem;color:var(--muted);margin-bottom:3px}
.bar select,.bar input,.field select,.field input{background:var(--panel);border:1px solid var(--line);color:var(--text);border-radius:4px;padding:6px 8px;width:100%}
.field{margin-bottom:2px}
.list{flex:1;overflow:auto;border:1px solid var(--line);border-radius:6px;background:var(--bg);min-height:220px}
.item{display:flex;justify-content:space-between;gap:8px;padding:7px 9px;border-bottom:1px solid var(--line);cursor:pointer;font-size:.82rem}
.item:hover,.item.on{background:var(--panel)}
.item .n{font-weight:600}
.item .m{font-family:var(--mono);font-size:.72rem;color:var(--accent);white-space:nowrap}
.item .s{font-size:.68rem;color:var(--muted)}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 14px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;min-width:120px}
.stat b{display:block;font-family:var(--mono);font-size:1.2rem;color:var(--accent)}
.stat span{font-size:.7rem;color:var(--muted)}
.stat.big b{font-size:1.45rem;color:var(--text)}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-bottom:12px}
.card h2{margin:0 0 8px;font-size:.95rem;color:var(--accent)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
@media(max-width:700px){.grid2{grid-template-columns:1fr}}
.meta{font-size:.78rem;color:var(--muted);line-height:1.5}
.meta code{font-family:var(--mono);color:var(--accent);font-size:.74rem}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:.68rem;margin:0 4px 4px 0;color:var(--muted)}
.pill.aim{color:#8ab4f8;border-color:#3a5080}
.pill.ame{color:#6abf69;border-color:#2a5a2a}
.pill.merc{color:#d4a017;border-color:#6a5a20}
.pill.warn{color:var(--warn);border-color:#6a5a20}
table{width:100%;border-collapse:collapse;font-size:.8rem}
th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}
th{color:var(--muted);font-weight:500}
td.mono,.mono{font-family:var(--mono);color:var(--accent)}
td.num,.num{font-family:var(--mono);text-align:right}
button{background:var(--panel);border:1px solid var(--line);color:var(--text);border-radius:4px;padding:6px 10px;cursor:pointer;font-size:.8rem}
button.primary{border-color:var(--accent);color:var(--accent)}
button:hover{border-color:var(--accent)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:8px}
.callout{font-size:.78rem;color:var(--muted);background:#1a1c21;border-left:3px solid var(--accent);padding:8px 10px;margin:10px 0;line-height:1.45}
.empty{color:var(--muted);font-size:.85rem;padding:20px 8px}
.chk{display:flex;align-items:center;gap:6px;font-size:.8rem;color:var(--muted);padding-top:16px}
input[type=range]{width:100%}
.range-val{font-family:var(--mono);color:var(--accent);font-size:.85rem}
.hidden{display:none !important}
</style>
</head>
<body>
<header>
  <h1>JAZZ · калькулятор зарплат наёмников</h1>
  <p>Формула vanilla <code>GetMercPrice</code> / <code>GetDailyMercSalary</code> (ModTools <code>Mercenary.lua</code>).
  Контракт AIM/AME: до <b>30</b> дней (JAZZ). Скидка за срок растянута до 30: normal 3–30 →25%, long only 7–30 →35% (<code>System_HireContractDuration</code>).
  M.E.R.C.: в игре prepaid рефандится, дальше дневной кредит — здесь показываем эквивалент контракта и суточный burn.</p>
</header>
<div class="layout">
  <aside class="side">
    <div class="bar">
      <div class="field" style="flex:1;min-width:120px">
        <label>Рынок</label>
        <select id="aff">
          <option value="all">Все</option>
          <option value="AIM">AIM</option>
          <option value="AME">AME</option>
          <option value="MERC">MERC</option>
          <option value="jazz">Только Jazz</option>
          <option value="vanilla">Только vanilla</option>
        </select>
      </div>
      <div class="field" style="flex:1;min-width:140px">
        <label>Поиск</label>
        <input id="q" type="search" placeholder="ник / id / роль"/>
      </div>
    </div>
    <button id="customDraft" type="button" class="primary" style="width:100%">Свой черновик (ручная цена)</button>
    <div class="list" id="list"></div>
  </aside>
  <main class="main">
    <div id="empty" class="empty">Выберите наёмника слева.</div>
    <div id="panel" class="hidden">
      <div class="stats" id="stats"></div>
      <div class="grid2">
        <div class="card">
          <h2>Параметры контракта</h2>
          <div class="grid2" style="margin-bottom:8px">
            <div class="field">
              <label>Дневная ставка (StartingSalary) — своя</label>
              <input id="customSalary" type="number" min="0" max="20000" step="1" value=""/>
            </div>
            <div class="field">
              <label>Рост за уровень ‰ (SalaryIncrease)</label>
              <input id="customInc" type="number" min="0" max="10000" step="10" value=""/>
            </div>
          </div>
          <div class="grid2" style="margin-bottom:8px">
            <div class="field">
              <label>Мед. депозит</label>
              <select id="customMed">
                <option value="none">none</option>
                <option value="small">small (×1)</option>
                <option value="large">large (×2)</option>
                <option value="extreme">extreme (×3)</option>
              </select>
            </div>
            <div class="field">
              <label>Скидка за срок</label>
              <select id="customDisc">
                <option value="normal">normal (до 25%@30д)</option>
                <option value="long only">long only (до 35%@30д)</option>
                <option value="none">none</option>
              </select>
            </div>
          </div>
          <div class="row" style="margin-bottom:8px">
            <button id="resetPreset" type="button">Сброс к пресету</button>
            <span class="meta" id="overrideHint"></span>
          </div>
          <div class="field">
            <label>Срок (дней) — <span class="range-val" id="daysVal">7</span></label>
            <input id="days" type="range" min="1" max="30" value="7"/>
          </div>
          <div class="field" style="margin-top:8px">
            <label>Уровень — <span class="range-val" id="lvlVal">1</span> <span class="meta">(старт <span id="lvlStart">1</span>)</span></label>
            <input id="lvl" type="range" min="1" max="21" value="1"/>
          </div>
          <div class="row">
            <label class="chk"><input type="checkbox" id="medical" checked/> Мед. депозит в цене</label>
            <label class="chk"><input type="checkbox" id="haggle"/> +1 торг (Haggling)</label>
          </div>
          <div class="row">
            <button class="primary" id="addSquad" type="button">В отряд</button>
            <button id="preset7" type="button">7д</button>
            <button id="preset14" type="button">14д</button>
            <button id="preset30" type="button">30д</button>
          </div>
        </div>
        <div class="card">
          <h2>Карточка</h2>
          <div id="cardMeta" class="meta"></div>
          <div class="callout" id="note"></div>
        </div>
      </div>
      <div class="card">
        <h2>Разбивка цены</h2>
        <table>
          <tbody id="breakdown"></tbody>
        </table>
      </div>
      <div class="card">
        <h2>Отряд / сумма</h2>
        <div class="row" style="margin-bottom:8px">
          <button id="clearSquad" type="button">Очистить</button>
          <span class="meta" id="squadSummary"></span>
        </div>
        <table>
          <thead><tr><th>Наёмник</th><th>Aff</th><th class="num">Ур.</th><th class="num">Дней</th><th class="num">Контракт</th><th></th></tr></thead>
          <tbody id="squadBody"></tbody>
          <tfoot><tr><th colspan="4">Итого</th><th class="num" id="squadTotal">$0</th><th></th></tr></tfoot>
        </table>
      </div>
      <div class="card">
        <h2>Кривая дневной ставки по уровню</h2>
        <table>
          <thead><tr><th class="num">Ур.</th><th class="num">$/день</th><th class="num">нед.×7 (без скидки)</th><th class="num">14д контракт</th></tr></thead>
          <tbody id="curve"></tbody>
        </table>
      </div>
    </div>
  </main>
</div>
<script>
const DATA = """

HTML_TAIL = r""";

function MulDivRound(a, b, c) {
  return Math.floor((a * b + Math.floor(c / 2)) / c);
}
function money(n) {
  const s = Math.round(n).toLocaleString("en-US");
  return "$" + s;
}
function dailySalary(m, level) {
  const startLvl = m.lvl || 1;
  let cur = m.salary || 0;
  const inc = m.inc || 250;
  const lvl = Math.max(level, startLvl);
  for (let L = startLvl; L < lvl; L++) {
    cur += MulDivRound(cur, inc, 1000);
  }
  return cur;
}
function durationDiscountPercent(m, days) {
  const d = m.disc || "normal";
  if (d === "none") return 0;
  let minDay = 0, minDiscount = 0, maxDay = 0, maxDiscount = 0;
  if (d === "normal") {
    minDay = 3; minDiscount = 0; maxDay = 30; maxDiscount = 25;
  } else if (d === "long only") {
    minDay = 7; minDiscount = 0; maxDay = 30; maxDiscount = 35;
  } else return 0;
  if (days >= minDay && days <= maxDay) {
    return minDiscount + MulDivRound(days - minDay, maxDiscount - minDiscount, maxDay - minDay);
  }
  return 0;
}
function medicalDeposit(m) {
  const kind = m.med || "small";
  if (kind === "none") return 0;
  const salary = m.salary || 0;
  if (kind === "small") return salary;
  if (kind === "large") return MulDivRound(salary, 200, 1000) * 10;
  if (kind === "extreme") return MulDivRound(salary, 300, 1000) * 10;
  return 0;
}
function haggleAmount(m, offered) {
  const h = m.hag || "normal";
  let percent = 0, min = 0;
  if (h === "low") { percent = 10; min = 100; }
  else if (h === "normal") { percent = 25; min = 200; }
  else if (h === "high") { percent = 50; min = 500; }
  else return 0;
  return Math.max(MulDivRound(offered, percent * 10, 1000), min);
}
function mercPrice(m, days, includeMedical, level) {
  days = days || 7;
  level = level || m.lvl || 1;
  const daily = dailySalary(m, level);
  const pct = 100 - durationDiscountPercent(m, days);
  let price = MulDivRound(daily * days, pct, 1000) * 10;
  if (days > 1) {
    const pct1 = 100 - durationDiscountPercent(m, days - 1);
    const oneLess = MulDivRound(daily * (days - 1), pct1, 1000) * 10;
    const minRaise = oneLess + 100;
    if (price < minRaise) price = minRaise;
  }
  const medical = includeMedical ? medicalDeposit(m) : 0;
  price += medical;
  return { price, medical, daily, discount: durationDiscountPercent(m, days) };
}

const DRAFT = {
  id: "__draft__",
  nick: "Свой черновик",
  aff: "AIM",
  role: "custom",
  tier: "",
  lvl: 1,
  salary: 100,
  inc: 250,
  med: "small",
  disc: "normal",
  hag: "normal",
  src: "custom",
};

let selectedId = null;
let squad = [];
let syncingOverrides = false;

const el = (id) => document.getElementById(id);

function filtered() {
  const aff = el("aff").value;
  const q = el("q").value.trim().toLowerCase();
  return DATA.filter((m) => {
    if (aff === "AIM" || aff === "AME" || aff === "MERC") {
      if (m.aff !== aff) return false;
    } else if (aff === "jazz") {
      if (m.src !== "jazz") return false;
    } else if (aff === "vanilla") {
      if (m.src !== "vanilla") return false;
    }
    if (!q) return true;
    const hay = `${m.nick} ${m.id} ${m.role} ${m.tier} ${m.aff}`.toLowerCase();
    return hay.includes(q);
  });
}

function renderList() {
  const list = el("list");
  const rows = filtered();
  list.innerHTML = rows.map((m) => {
    const on = m.id === selectedId ? " on" : "";
    return `<div class="item${on}" data-id="${m.id}">
      <div><div class="n">${escapeHtml(m.nick)}</div>
      <div class="s">${escapeHtml(m.id)} · ${escapeHtml(m.role || "—")} · L${m.lvl}</div></div>
      <div class="m">${money(m.salary)}/д</div>
    </div>`;
  }).join("") || `<div class="empty">Нет совпадений</div>`;
  list.querySelectorAll(".item").forEach((node) => {
    node.addEventListener("click", () => selectMerc(node.dataset.id));
  });
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[c]);
}

function baseMerc() {
  if (selectedId === DRAFT.id) return { ...DRAFT };
  return DATA.find((m) => m.id === selectedId) || null;
}

function fillOverridesFromBase(m) {
  syncingOverrides = true;
  el("customSalary").value = String(m.salary);
  el("customInc").value = String(m.inc);
  el("customMed").value = m.med || "small";
  el("customDisc").value = m.disc || "normal";
  syncingOverrides = false;
  updateOverrideHint(m);
}

function updateOverrideHint(base) {
  if (!base) { el("overrideHint").textContent = ""; return; }
  const sal = Number(el("customSalary").value);
  const inc = Number(el("customInc").value);
  const med = el("customMed").value;
  const disc = el("customDisc").value;
  const changed = sal !== base.salary || inc !== base.inc || med !== base.med || disc !== base.disc;
  if (base.id === DRAFT.id) {
    el("overrideHint").textContent = "черновик · все поля ручные";
  } else if (changed) {
    el("overrideHint").textContent = `override · пресет был ${money(base.salary)}/д, inc ${base.inc}`;
  } else {
    el("overrideHint").textContent = "как в данных";
  }
}

function effectiveMerc() {
  const base = baseMerc();
  if (!base) return null;
  const sal = Number(el("customSalary").value);
  const inc = Number(el("customInc").value);
  return {
    ...base,
    salary: Number.isFinite(sal) && sal >= 0 ? sal : base.salary,
    inc: Number.isFinite(inc) && inc >= 0 ? inc : base.inc,
    med: el("customMed").value || base.med,
    disc: el("customDisc").value || base.disc,
  };
}

function selectMerc(id) {
  selectedId = id;
  const m = baseMerc();
  el("empty").style.display = m ? "none" : "block";
  el("panel").classList.toggle("hidden", !m);
  if (!m) { renderList(); return; }
  el("lvl").min = m.lvl;
  el("lvl").value = m.lvl;
  el("lvlStart").textContent = String(m.lvl);
  fillOverridesFromBase(m);
  renderList();
  renderCalc();
}

function selectDraft() {
  selectedId = DRAFT.id;
  el("empty").style.display = "none";
  el("panel").classList.remove("hidden");
  el("lvl").min = 1;
  el("lvl").value = 1;
  el("lvlStart").textContent = "1";
  fillOverridesFromBase(DRAFT);
  renderList();
  renderCalc();
}

function renderCalc() {
  const base = baseMerc();
  const m = effectiveMerc();
  if (!m || !base) return;
  const days = Number(el("days").value);
  const lvl = Number(el("lvl").value);
  const withMed = el("medical").checked;
  const withHaggle = el("haggle").checked;
  el("daysVal").textContent = String(days);
  el("lvlVal").textContent = String(lvl);
  updateOverrideHint(base);

  let { price, medical, daily, discount } = mercPrice(m, days, withMed, lvl);
  let haggle = 0;
  if (withHaggle) {
    haggle = haggleAmount(m, price);
    price += haggle;
  }
  const perDayEff = days > 0 ? Math.round(price / days) : price;
  const weekRaw = daily * 7;

  el("stats").innerHTML = `
    <div class="stat big"><b>${money(price)}</b><span>контракт ${days}д</span></div>
    <div class="stat"><b>${money(daily)}</b><span>дневная ставка</span></div>
    <div class="stat"><b>${money(perDayEff)}</b><span>эффективно $/день</span></div>
    <div class="stat"><b>${discount}%</b><span>скидка за срок</span></div>
    <div class="stat"><b>${money(medical)}</b><span>мед. депозит</span></div>
  `;

  const overriden = m.salary !== base.salary || m.inc !== base.inc;
  el("cardMeta").innerHTML = `
    <div><b>${escapeHtml(base.nick)}</b> <span class="pill ${base.aff.toLowerCase()}">${escapeHtml(base.aff)}</span>
    <span class="pill">${escapeHtml(base.src)}</span>
    ${base.tier ? `<span class="pill">${escapeHtml(base.tier)}</span>` : ""}
    ${overriden ? `<span class="pill warn">custom $</span>` : ""}</div>
    <div>Id: <code>${escapeHtml(base.id)}</code> · роль <code>${escapeHtml(base.role || "—")}</code></div>
    <div>Сейчас: StartingSalary <code>${m.salary}</code> · SalaryIncrease <code>${m.inc}</code> (‰) ·
      Medical <code>${escapeHtml(m.med)}</code> · Discount <code>${escapeHtml(m.disc)}</code></div>
    <div>Пресет данных: <code>${base.salary}</code> / inc <code>${base.inc}</code> / med <code>${escapeHtml(base.med)}</code></div>
  `;

  let note = "";
  if (base.id === DRAFT.id) {
    note = "Черновик: задайте дневную ставку и параметры выше — формула та же, что у AIM/AME hire.";
  } else if (overriden) {
    note = `Ручная ставка ${money(m.salary)}/д вместо пресета ${money(base.salary)}/д. Мед. депозит считается от введённой StartingSalary.`;
  } else if (m.aff === "MERC") {
    note = "M.E.R.C.: в JAZZ prepaid контракта возвращается на кредитный счёт; дальше начисляется дневная ставка. Сумма контракта ниже — ориентир «если бы платили AIM-стилем» и оценка burn.";
  } else if (discount > 0) {
    note = `Скидка за длительность ${discount}% (DurationDiscount=${m.disc}; пик на 30д). Медицинский депозит возвращается, если наёмник не ранен тяжело к концу контракта.`;
  } else {
    note = "Без скидки за срок на этой длительности. Медицинский депозит — из StartingSalary (не из leveled daily).";
  }
  el("note").textContent = note;

  const wageOnly = price - medical - haggle;
  el("breakdown").innerHTML = `
    <tr><td>Дневная ставка (ур. ${lvl})</td><td class="num">${money(daily)}</td></tr>
    <tr><td>× ${days} дн. до скидки</td><td class="num">${money(daily * days)}</td></tr>
    <tr><td>Скидка за срок (${discount}%)</td><td class="num">−${money(daily * days - wageOnly)}</td></tr>
    <tr><td>Зарплата за контракт</td><td class="num">${money(wageOnly)}</td></tr>
    <tr><td>Мед. депозит (${escapeHtml(m.med)})</td><td class="num">${money(medical)}</td></tr>
    <tr><td>Торг</td><td class="num">${money(haggle)}</td></tr>
    <tr><th>Итого к оплате</th><th class="num">${money(price)}</th></tr>
    <tr><td>Нед. без скидки (daily×7)</td><td class="num">${money(weekRaw)}</td></tr>
  `;

  const curve = el("curve");
  const rows = [];
  for (let L = m.lvl; L <= Math.min(21, m.lvl + 10); L++) {
    const d = dailySalary(m, L);
    const p14 = mercPrice(m, 14, true, L).price;
    rows.push(`<tr><td class="num">${L}</td><td class="num">${money(d)}</td><td class="num">${money(d * 7)}</td><td class="num">${money(p14)}</td></tr>`);
  }
  curve.innerHTML = rows.join("");
}

function renderSquad() {
  const body = el("squadBody");
  body.innerHTML = squad.map((row, idx) => {
    return `<tr>
      <td>${escapeHtml(row.nick)}<div class="meta">${escapeHtml(row.id)}</div></td>
      <td><span class="pill ${row.aff.toLowerCase()}">${escapeHtml(row.aff)}</span></td>
      <td class="num">${row.lvl}</td>
      <td class="num">${row.days}</td>
      <td class="num">${money(row.price)}</td>
      <td><button data-rm="${idx}" type="button">×</button></td>
    </tr>`;
  }).join("") || `<tr><td colspan="6" class="empty">Отряд пуст — добавьте наёмников.</td></tr>`;
  body.querySelectorAll("button[data-rm]").forEach((b) => {
    b.addEventListener("click", () => {
      squad.splice(Number(b.dataset.rm), 1);
      renderSquad();
    });
  });
  const total = squad.reduce((s, r) => s + r.price, 0);
  const burn = squad.reduce((s, r) => s + r.daily, 0);
  el("squadTotal").textContent = money(total);
  el("squadSummary").textContent = squad.length
    ? `${squad.length} чел. · суточный burn ≈ ${money(burn)}`
    : "";
}

el("aff").addEventListener("change", renderList);
el("q").addEventListener("input", renderList);
["days", "lvl", "medical", "haggle", "customSalary", "customInc", "customMed", "customDisc"].forEach((id) => {
  el(id).addEventListener("input", () => { if (!syncingOverrides) renderCalc(); });
  el(id).addEventListener("change", () => { if (!syncingOverrides) renderCalc(); });
});
el("preset7").addEventListener("click", () => { el("days").value = 7; renderCalc(); });
el("preset14").addEventListener("click", () => { el("days").value = 14; renderCalc(); });
el("preset30").addEventListener("click", () => { el("days").value = 30; renderCalc(); });
el("resetPreset").addEventListener("click", () => {
  const m = baseMerc();
  if (m) fillOverridesFromBase(m);
  renderCalc();
});
el("customDraft").addEventListener("click", selectDraft);
el("addSquad").addEventListener("click", () => {
  const m = effectiveMerc();
  const base = baseMerc();
  if (!m || !base) return;
  const days = Number(el("days").value);
  const lvl = Number(el("lvl").value);
  const withMed = el("medical").checked;
  const withHaggle = el("haggle").checked;
  let { price, daily } = mercPrice(m, days, withMed, lvl);
  if (withHaggle) price += haggleAmount(m, price);
  const nick = m.salary !== base.salary
    ? `${base.nick} @${m.salary}`
    : base.nick;
  squad.push({ id: base.id, nick, aff: base.aff, days, lvl, price, daily });
  renderSquad();
});
el("clearSquad").addEventListener("click", () => { squad = []; renderSquad(); });

renderList();
renderSquad();
</script>
</body>
</html>
"""


def main() -> None:
    if not JSON.is_file():
        subprocess.check_call([sys.executable, str(EXPORT)])
    data = json.loads(JSON.read_text(encoding="utf-8"))
    # Compact JSON for embed
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    OUT.write_text(HTML_HEAD + payload + HTML_TAIL, encoding="utf-8")
    print("wrote", OUT, "mercs", len(data), "bytes", OUT.stat().st_size)


if __name__ == "__main__":
    main()
