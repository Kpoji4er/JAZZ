# -*- coding: utf-8 -*-
"""Build docs/tools/attachments-catalog.html from weapon component CSVs."""
from __future__ import annotations

import csv
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "docs", "technical", "weapons", "data")
OUT = os.path.join(HERE, "attachments-catalog.html")


def load_csv(name):
    path = os.path.join(DATA, name)
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


PARAM_HINTS = {
    "Recoil": "отдача (меньше = лучше удержание в очереди)",
    "ScopeMagnification": "кратность оптики (целая часть)",
    "ScopeSubMagnification": "кратность, десятые (1+sub/10)",
    "ScopeAimLevel": "мин. кликов aim, чтобы оптика включилась",
    "ScopeHandlingReduce": "штраф Handling от оптики (legacy)",
    "AimAccuracyIncrease": "+AimAccuracy за клик",
    "ShotAP": "+ShootAP за выстрел (дороже)",
    "IncreaseMaxAimActions": "+MaxAimActions",
    "MaxAimActionsDecrease": "−MaxAimActions",
    "MagazineSize": "+ёмкость магазина (аддитивно)",
    "MagazineSizeMultiplier": "ёмкость ×(value/100)",
    "ReliabilityIncrease": "+Reliability",
    "ReliabilityDecrease": "−Reliability",
    "RangeIncrease": "+WeaponRange",
    "RangeDecrease": "−WeaponRange",
    "NoiseMultiplier": "множитель шума (ниже = тише)",
    "stealth_kill_bonus": "бонус stealth kill",
    "LaserCTH": "плоский CTH от лазера (pp), если d≤LaserDistance",
    "LaserDistance": "макс. дистанция лазера (тайлы)",
    "bonus_cth": "legacy плоский +CTH (pp) — конфликт с accuracy-model",
    "BonusCTH": "legacy плоский +CTH",
    "ScopeCTH": "legacy плоский +CTH оптики",
    "bonus_cth_bipod": "плоский +CTH prone с bipod",
    "BarrelRecoilRecude": "−Recoil от ствола (опечатка Recude)",
    "BuckshotAngleIncrease": "угол дроби",
    "DamageIncrease": "+Damage",
    "min_aim": "мин. aim / free aim quirks",
}


def parse_params(raw: str) -> list[dict]:
    if not raw:
        return []
    out = []
    for chunk in raw.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" in chunk:
            k, v = chunk.split("=", 1)
        else:
            k, v = chunk, ""
        out.append({"key": k, "value": v, "hint": PARAM_HINTS.get(k, "")})
    return out


def flags_for(comp: dict, params: list[dict]) -> list[str]:
    flags = []
    effects = [e for e in (comp.get("effects") or "").split(";") if e]
    keys = {p["key"] for p in params}
    if not effects and not params:
        flags.append("empty")
    if not effects and params:
        flags.append("orphan_params")
    flat = {"bonus_cth", "BonusCTH", "ScopeCTH", "bonus_cth_bipod", "LaserCTH"}
    if keys & flat or any(
        e in ("MinorAccuracyBonus", "AccuracyBonusWhenAimed", "ScopeCTHBonus", "NightsIronsBonus")
        for e in effects
    ):
        flags.append("legacy_flat_cth")
    if "BarrelRecoilRecude" in keys:
        try:
            if float(next(p["value"] for p in params if p["key"] == "BarrelRecoilRecude")) < 0:
                flags.append("wrong_sign")
        except StopIteration:
            pass
    if int(comp.get("used_by_count") or 0) == 0:
        flags.append("unused")
    return flags


def main():
    effects_rows = {r["effect_id"]: r for r in load_csv("weapon-component-effects.csv")}
    comps = []
    for row in load_csv("weapon-components.csv"):
        params = parse_params(row.get("parameters") or "")
        effect_ids = [e for e in (row.get("effects") or "").split(";") if e]
        effect_details = []
        for eid in effect_ids:
            er = effects_rows.get(eid, {})
            effect_details.append(
                {
                    "id": eid,
                    "name": er.get("display_name") or eid,
                    "desc": er.get("description") or "",
                    "default_params": er.get("parameters") or "",
                }
            )
        flags = flags_for(row, params)
        comps.append(
            {
                "id": row["component_id"],
                "name": row.get("display_name") or row["component_id"],
                "slot": row.get("slot") or "?",
                "cost": row.get("cost") or "",
                "diff": row.get("modification_difficulty") or "",
                "used": int(row.get("used_by_count") or 0),
                "source": row.get("source") or "",
                "group": row.get("group") or "",
                "effects": effect_details,
                "params": params,
                "raw_effects": row.get("effects") or "",
                "raw_params": row.get("parameters") or "",
                "flags": flags,
            }
        )

    slots = sorted({c["slot"] for c in comps})
    summary = {
        "total": len(comps),
        "by_slot": {s: sum(1 for c in comps if c["slot"] == s) for s in slots},
        "empty": sum(1 for c in comps if "empty" in c["flags"]),
        "orphan_params": sum(1 for c in comps if "orphan_params" in c["flags"]),
        "legacy_flat_cth": sum(1 for c in comps if "legacy_flat_cth" in c["flags"]),
        "unused": sum(1 for c in comps if "unused" in c["flags"]),
        "wrong_sign": sum(1 for c in comps if "wrong_sign" in c["flags"]),
    }

    data_js = json.dumps(
        {"components": comps, "slots": slots, "summary": summary, "effects_catalog": list(effects_rows.values())},
        ensure_ascii=False,
        separators=(",", ":"),
    )

    html = HTML_TEMPLATE.replace("/*__DATA__*/", data_js)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(
        f"Wrote {OUT} components={summary['total']} empty={summary['empty']} "
        f"orphan={summary['orphan_params']} flatCTH={summary['legacy_flat_cth']} unused={summary['unused']}"
    )


HTML_TEMPLATE = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>JAZZ Attachments Catalog</title>
<style>
:root{--bg:#16171a;--panel:#22252b;--line:#3a3f4a;--text:#e8eaed;--muted:#9aa0a6;--accent:#c4a35a;--good:#6abf69;--bad:#e07070;--warn:#d4a017;--mono:ui-monospace,Consolas,monospace;--sans:"Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;font-family:var(--sans);background:var(--bg);color:var(--text)}
header{padding:14px 18px;border-bottom:1px solid var(--line);background:var(--panel)}
header h1{margin:0 0 4px;font-size:1.15rem;color:var(--accent)}
header p{margin:0;color:var(--muted);font-size:.82rem;max-width:1100px}
.bar{display:flex;flex-wrap:wrap;gap:10px;padding:12px 18px;border-bottom:1px solid var(--line);background:#1c1e23;align-items:end}
.bar label{display:block;font-size:.7rem;color:var(--muted);margin-bottom:3px}
.bar select,.bar input{background:var(--panel);border:1px solid var(--line);color:var(--text);border-radius:4px;padding:6px 8px;min-width:140px}
.bar .chk{display:flex;align-items:center;gap:6px;font-size:.82rem;padding-bottom:6px}
main{padding:12px 18px 40px}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px 12px;min-width:110px}
.stat b{display:block;font-family:var(--mono);font-size:1.15rem;color:var(--accent)}
.stat span{font-size:.7rem;color:var(--muted)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:10px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px;cursor:pointer}
.card:hover{border-color:var(--accent)}
.card h3{margin:0 0 6px;font-size:.95rem}
.card .id{font-family:var(--mono);font-size:.72rem;color:var(--accent)}
.meta{font-size:.75rem;color:var(--muted);margin:4px 0 8px}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 7px;font-size:.68rem;margin:0 4px 4px 0;color:var(--muted)}
.pill.warn{color:var(--warn);border-color:#6a5a20}
.pill.bad{color:var(--bad);border-color:#6a3030}
.pill.ok{color:var(--good);border-color:#2a5a2a}
.eff{font-size:.78rem;margin:6px 0 0;padding-left:0;list-style:none}
.eff li{margin:4px 0;padding:6px 8px;background:#1a1c21;border-radius:4px;border-left:3px solid var(--line)}
.eff .ename{font-weight:600}
.eff .edesc{color:var(--muted);font-size:.72rem;margin-top:2px}
.params{font-family:var(--mono);font-size:.72rem;margin-top:8px;color:var(--muted)}
.params div{margin:2px 0}
.params .hint{color:#7a8088;font-family:var(--sans);font-size:.68rem;margin-left:6px}
#detail{position:fixed;inset:auto 0 0 0;max-height:45vh;overflow:auto;background:#1a1c21;border-top:1px solid var(--line);padding:14px 18px;display:none;z-index:5}
#detail.open{display:block}
#detail h2{margin:0 0 8px;font-size:1rem;color:var(--accent)}
.close{float:right;background:transparent;border:1px solid var(--line);color:var(--text);border-radius:4px;padding:2px 8px;cursor:pointer}
</style>
</head>
<body>
<header>
  <h1>JAZZ · каталог аттачментов</h1>
  <p>Все WeaponComponent из CSV: эффекты, параметры, флаги (пусто / orphan params / legacy flat CTH / unused).
  Оптика в новой модели сдвигает reach, а не даёт плоский +CTH — помеченные legacy_flat_cth стоит чистить.</p>
</header>
<div class="bar">
  <div><label>Слот</label><select id="slot"><option value="">Все</option></select></div>
  <div><label>Флаг</label><select id="flag">
    <option value="">Любой</option>
    <option value="empty">empty</option>
    <option value="orphan_params">orphan_params</option>
    <option value="legacy_flat_cth">legacy_flat_cth</option>
    <option value="unused">unused</option>
    <option value="wrong_sign">wrong_sign</option>
  </select></div>
  <div><label>Источник</label><select id="src"><option value="">Все</option><option value="jazz">jazz</option><option value="vanilla_233360">vanilla</option></select></div>
  <div><label>Поиск</label><input id="q" placeholder="MagLarge, глушитель…"/></div>
  <div class="chk"><input type="checkbox" id="hasFx" checked/><label for="hasFx" style="margin:0">Показывать пустые</label></div>
</div>
<main>
  <div class="stats" id="stats"></div>
  <div class="grid" id="grid"></div>
</main>
<div id="detail"><button class="close" id="closeBtn">✕</button><div id="detailBody"></div></div>
<script>
const DATA = /*__DATA__*/;
const $ = id => document.getElementById(id);
DATA.slots.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s+' ('+DATA.summary.by_slot[s]+')'; $('slot').appendChild(o); });

function renderStats(n) {
  const s = DATA.summary;
  $('stats').innerHTML = [
    ['Показано', n],
    ['Всего', s.total],
    ['Empty', s.empty],
    ['Orphan params', s.orphan_params],
    ['Legacy flat CTH', s.legacy_flat_cth],
    ['Unused', s.unused],
    ['Wrong sign', s.wrong_sign],
  ].map(x => '<div class="stat"><b>'+x[1]+'</b><span>'+x[0]+'</span></div>').join('');
}

function flagPills(flags) {
  return flags.map(f => {
    const cls = f==='empty'||f==='orphan_params'||f==='wrong_sign' ? 'bad' : f==='legacy_flat_cth' ? 'warn' : 'ok';
    return '<span class="pill '+cls+'">'+f+'</span>';
  }).join('');
}

function effectList(c) {
  if (!c.effects.length) return '<div class="meta">Нет effects</div>';
  return '<ul class="eff">'+c.effects.map(e =>
    '<li><div class="ename">'+e.id+'</div><div class="edesc">'+(e.desc||e.name)+
    (e.default_params ? ' · defaults: '+e.default_params : '')+'</div></li>'
  ).join('')+'</ul>';
}

function paramBlock(c) {
  if (!c.params.length) return '';
  return '<div class="params">'+c.params.map(p =>
    '<div><b>'+p.key+'</b>='+p.value+(p.hint?'<span class="hint">'+p.hint+'</span>':'')+'</div>'
  ).join('')+'</div>';
}

function filtered() {
  const slot=$('slot').value, flag=$('flag').value, src=$('src').value, q=$('q').value.trim().toLowerCase();
  const showEmpty=$('hasFx').checked;
  return DATA.components.filter(c => {
    if (slot && c.slot!==slot) return false;
    if (flag && !c.flags.includes(flag)) return false;
    if (src && c.source!==src) return false;
    if (!showEmpty && c.flags.includes('empty')) return false;
    if (q && !(c.id.toLowerCase().includes(q) || c.name.toLowerCase().includes(q) || c.raw_effects.toLowerCase().includes(q))) return false;
    return true;
  }).sort((a,b)=> a.slot.localeCompare(b.slot)||a.id.localeCompare(b.id));
}

function openDetail(c) {
  $('detail').classList.add('open');
  $('detailBody').innerHTML = '<h2>'+c.name+' <span class="id">'+c.id+'</span></h2>'+
    '<div class="meta">slot <b>'+c.slot+'</b> · cost '+c.cost+' · diff '+c.diff+' · used_by '+c.used+
    ' · '+c.source+' · group '+c.group+'</div>'+flagPills(c.flags)+effectList(c)+paramBlock(c)+
    '<div class="params" style="margin-top:10px">raw effects: '+(c.raw_effects||'—')+'<br/>raw params: '+(c.raw_params||'—')+'</div>';
}

function render() {
  const rows = filtered();
  renderStats(rows.length);
  const g=$('grid'); g.innerHTML='';
  rows.forEach(c => {
    const card=document.createElement('div'); card.className='card';
    card.innerHTML = '<div class="id">'+c.id+'</div><h3>'+c.name+'</h3>'+
      '<div class="meta"><span class="pill">'+c.slot+'</span> used '+c.used+' · '+c.source+'</div>'+
      flagPills(c.flags)+
      '<div class="meta">'+(c.effects.map(e=>e.id).join(', ')||'—')+'</div>';
    card.onclick=()=>openDetail(c);
    g.appendChild(card);
  });
}
['slot','flag','src','hasFx'].forEach(id=>$(id).addEventListener('change',render));
$('q').addEventListener('input',render);
$('closeBtn').onclick=()=>$('detail').classList.remove('open');
render();
</script>
</body>
</html>
'''

if __name__ == "__main__":
    main()
