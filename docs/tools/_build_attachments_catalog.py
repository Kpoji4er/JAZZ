# -*- coding: utf-8 -*-
"""Build docs/tools/attachments-catalog.html from weapon component CSVs."""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, "docs", "technical", "weapons", "data")
OUT = os.path.join(HERE, "attachments-catalog.html")

if HERE not in sys.path:
    sys.path.insert(0, HERE)
from _attach_classify import classify_component  # noqa: E402


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


def flags_for(comp: dict, params: list[dict], used_n: int) -> list[str]:
    flags = []
    effects = [e for e in (comp.get("effects") or "").split(";") if e]
    keys = {p["key"] for p in params}
    slot = (comp.get("slot") or "").strip()
    cid = comp.get("component_id") or ""
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
    # leftover_optic / entity_visual / nonjazz_scope — not "any non-JAZZ Scope"
    flags.extend(classify_component(cid, slot, effects))
    if used_n == 0:
        flags.append("unused")
    return flags


def main():
    effects_rows = {r["effect_id"]: r for r in load_csv("weapon-component-effects.csv")}
    weapons_meta = {}
    active_weapon_ids = set()
    for w in load_csv("weapons.csv"):
        status = (w.get("catalog_status") or "").strip()
        weapons_meta[w["id"]] = {
            "id": w["id"],
            "name": w.get("display_name") or w["id"],
            "family": w.get("family_id") or "",
            "tier": w.get("tier_label") or "",
            "status": status,
        }
        # Cut/outdated stubs (AR15, M4Commando, MP5) stay in CSV but not in live catalog
        if status == "active":
            active_weapon_ids.add(w["id"])

    # component_id -> list of mounts (only playable: modifiable OR default)
    mounts = defaultdict(list)
    by_weapon = defaultdict(list)
    for opt in load_csv("weapon-component-options.csv"):
        cid = (opt.get("component_id") or "").strip()
        if not cid:
            continue
        wid = opt["weapon_id"]
        if wid not in active_weapon_ids:
            continue
        is_default = (opt.get("is_default") or "").lower() == "true"
        modifiable = (opt.get("modifiable") or "").lower() == "true"
        # Dead wiring: Modifiable=false without default — not "on weapon" in-game
        if not modifiable and not is_default:
            continue
        entry = {
            "weapon_id": wid,
            "slot": opt.get("slot_type") or "",
            "default": is_default,
            "modifiable": modifiable,
        }
        mounts[cid].append(entry)
        meta = weapons_meta.get(wid, {"id": wid, "name": wid, "family": "", "tier": ""})
        by_weapon[wid].append(
            {
                "component_id": cid,
                "component_name": opt.get("component_name") or cid,
                "slot": opt.get("slot_type") or "",
                "default": entry["default"],
                "modifiable": entry["modifiable"],
            }
        )

    # dedupe mounts per weapon+slot for same component
    for cid, lst in list(mounts.items()):
        seen = set()
        uniq = []
        for m in lst:
            key = (m["weapon_id"], m["slot"])
            if key in seen:
                continue
            seen.add(key)
            uniq.append(m)
        uniq.sort(key=lambda x: (x["weapon_id"], x["slot"]))
        mounts[cid] = uniq

    comps = []
    skipped_unused = 0
    for row in load_csv("weapon-components.csv"):
        # Mounts are cosmetic rails — skip from catalog noise
        if (row.get("slot") or "").strip().lower() == "mount":
            continue
        used_list = []
        for m in mounts.get(row["component_id"], []):
            meta = weapons_meta.get(m["weapon_id"], {"id": m["weapon_id"], "name": m["weapon_id"], "family": "", "tier": ""})
            used_list.append(
                {
                    "id": m["weapon_id"],
                    "name": meta["name"],
                    "family": meta.get("family", ""),
                    "tier": meta.get("tier", ""),
                    "slot": m["slot"],
                    "default": m["default"],
                }
            )
        # Catalog = only components actually wired on at least one weapon
        if not used_list:
            skipped_unused += 1
            continue
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
        flags = flags_for(row, params, len(used_list))
        comps.append(
            {
                "id": row["component_id"],
                "name": row.get("display_name") or row["component_id"],
                "slot": row.get("slot") or "?",
                "cost": row.get("cost") or "",
                "diff": row.get("modification_difficulty") or "",
                "used": len(used_list),
                "source": row.get("source") or "",
                "group": row.get("group") or "",
                "effects": effect_details,
                "params": params,
                "raw_effects": row.get("effects") or "",
                "raw_params": row.get("parameters") or "",
                "flags": flags,
                "weapons": used_list,
            }
        )

    weapons_index = []
    for wid, parts in sorted(by_weapon.items()):
        meta = weapons_meta.get(wid, {"id": wid, "name": wid, "family": "", "tier": "", "status": ""})
        # dedupe parts by component+slot
        seen = set()
        clean = []
        for p in parts:
            if (p.get("slot") or "").strip().lower() == "mount":
                continue
            key = (p["component_id"], p["slot"])
            if key in seen:
                continue
            seen.add(key)
            clean.append(p)
        clean.sort(key=lambda x: (x["slot"], x["component_id"]))
        weapons_index.append(
            {
                "id": wid,
                "name": meta["name"],
                "family": meta.get("family", ""),
                "tier": meta.get("tier", ""),
                "status": meta.get("status", ""),
                "parts": clean,
            }
        )

    # Weapon tab: only parts present in the used-component catalog
    used_ids = {c["id"] for c in comps}
    for w in weapons_index:
        w["parts"] = [p for p in w["parts"] if p["component_id"] in used_ids]

    slots = sorted({c["slot"] for c in comps})
    summary = {
        "total": len(comps),
        "by_slot": {s: sum(1 for c in comps if c["slot"] == s) for s in slots},
        "empty": sum(1 for c in comps if "empty" in c["flags"]),
        "orphan_params": sum(1 for c in comps if "orphan_params" in c["flags"]),
        "legacy_flat_cth": sum(1 for c in comps if "legacy_flat_cth" in c["flags"]),
        "leftover_optic": sum(1 for c in comps if "leftover_optic" in c["flags"]),
        "entity_visual": sum(1 for c in comps if "entity_visual" in c["flags"]),
        "nonjazz_scope": sum(1 for c in comps if "nonjazz_scope" in c["flags"]),
        "unused_skipped": skipped_unused,
        "wrong_sign": sum(1 for c in comps if "wrong_sign" in c["flags"]),
        "weapons_with_slots": len(weapons_index),
        "active_weapons": len(active_weapon_ids),
    }

    data_js = json.dumps(
        {
            "components": comps,
            "slots": slots,
            "summary": summary,
            "weapons": weapons_index,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )

    html = HTML_TEMPLATE.replace("/*__DATA__*/", data_js)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(
        f"Wrote {OUT} components={summary['total']} weapons={summary['weapons_with_slots']} "
        f"empty={summary['empty']} leftover_optic={summary['leftover_optic']} "
        f"entity_visual={summary['entity_visual']} unused_skipped={summary['unused_skipped']}"
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
.tabs{display:flex;gap:8px;padding:10px 18px 0;background:#1c1e23;border-bottom:1px solid var(--line)}
.tabs button{background:transparent;border:1px solid var(--line);color:var(--muted);border-radius:4px 4px 0 0;padding:6px 12px;cursor:pointer}
.tabs button.on{color:var(--accent);border-bottom-color:#1c1e23;background:var(--bg)}
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
.guns{font-size:.72rem;color:#b8bdc4;line-height:1.45;margin-top:6px}
.guns b{color:var(--accent);font-weight:600}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 7px;font-size:.68rem;margin:0 4px 4px 0;color:var(--muted)}
.pill.warn{color:var(--warn);border-color:#6a5a20}
.pill.bad{color:var(--bad);border-color:#6a3030}
.pill.ok{color:var(--good);border-color:#2a5a2a}
.pill.def{color:var(--accent);border-color:#6a5a20}
.eff{font-size:.78rem;margin:6px 0 0;padding-left:0;list-style:none}
.eff li{margin:4px 0;padding:6px 8px;background:#1a1c21;border-radius:4px;border-left:3px solid var(--line)}
.eff .ename{font-weight:600}
.eff .edesc{color:var(--muted);font-size:.72rem;margin-top:2px}
.params{font-family:var(--mono);font-size:.72rem;margin-top:8px;color:var(--muted)}
.params div{margin:2px 0}
.params .hint{color:#7a8088;font-family:var(--sans);font-size:.68rem;margin-left:6px}
.wtable{width:100%;border-collapse:collapse;font-size:.78rem;margin-top:8px}
.wtable th,.wtable td{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left}
.wtable th{color:var(--muted);font-weight:500}
.wtable .mono{font-family:var(--mono);color:var(--accent)}
#detail{position:fixed;inset:auto 0 0 0;max-height:50vh;overflow:auto;background:#1a1c21;border-top:1px solid var(--line);padding:14px 18px;display:none;z-index:5}
#detail.open{display:block}
#detail h2{margin:0 0 8px;font-size:1rem;color:var(--accent)}
.close{float:right;background:transparent;border:1px solid var(--line);color:var(--text);border-radius:4px;padding:2px 8px;cursor:pointer}
.hidden{display:none !important}
</style>
</head>
<body>
<header>
  <h1>JAZZ · каталог аттачментов</h1>
  <p>Только <b>active</b> оружие и компоненты, реально стоящие на нём.
  Вырезанные stubs / Mount / unused отброшены.
  <b>leftover_optic</b> = ванильная линейка оптики (ReflexSight/LROptics/…) — должна быть JAZZ_*.
  <b>entity_visual</b> = irons / default mesh (Visuals.Entity), не «неправильный прицел».
  Остальные слоты (Mag/Barrel/…) — shared ID, без требования JAZZ_ префикса.</p>
</header>
<div class="tabs">
  <button type="button" class="on" id="tabComp">По аттачу</button>
  <button type="button" id="tabWep">По оружию</button>
</div>
<div class="bar" id="barComp">
  <div><label>Слот</label><select id="slot"><option value="">Все</option></select></div>
  <div><label>Оружие (фильтр)</label><select id="weaponFilter"><option value="">Любое</option></select></div>
  <div><label>Флаг</label><select id="flag">
    <option value="">Любой</option>
    <option value="empty">empty</option>
    <option value="orphan_params">orphan_params</option>
    <option value="legacy_flat_cth">legacy_flat_cth</option>
    <option value="leftover_optic">leftover_optic</option>
    <option value="entity_visual">entity_visual</option>
    <option value="nonjazz_scope">nonjazz_scope</option>
    <option value="wrong_sign">wrong_sign</option>
  </select></div>
  <div><label>Источник</label><select id="src"><option value="">Все</option><option value="jazz">jazz</option><option value="vanilla_233360">vanilla</option></select></div>
  <div><label>Поиск</label><input id="q" placeholder="MagLarge, Suppressor, AK47…"/></div>
  <div class="chk"><input type="checkbox" id="hasFx" checked/><label for="hasFx" style="margin:0">Показывать пустые</label></div>
</div>
<div class="bar hidden" id="barWep">
  <div><label>Семейство</label><select id="fam"><option value="">Все</option></select></div>
  <div><label>Оружие</label><select id="weapon"></select></div>
  <div><label>Поиск оружия</label><input id="wq" placeholder="USP45, Thompson…"/></div>
</div>
<main>
  <div class="stats" id="stats"></div>
  <div class="grid" id="grid"></div>
  <div id="wepView" class="hidden"></div>
</main>
<div id="detail"><button class="close" id="closeBtn">✕</button><div id="detailBody"></div></div>
<script>
const DATA = /*__DATA__*/;
const $ = id => document.getElementById(id);
const byId = Object.fromEntries(DATA.components.map(c => [c.id, c]));

DATA.slots.forEach(s => { const o=document.createElement('option'); o.value=s; o.textContent=s+' ('+DATA.summary.by_slot[s]+')'; $('slot').appendChild(o); });

// weapon filter options
const wepsSorted = DATA.weapons.slice().sort((a,b)=> (a.tier||'').localeCompare(b.tier||'') || a.id.localeCompare(b.id));
wepsSorted.forEach(w => {
  const o=document.createElement('option');
  o.value=w.id; o.textContent=(w.tier?w.tier+' · ':'')+w.name+' ('+w.id+')';
  $('weaponFilter').appendChild(o);
  const o2=o.cloneNode(true); $('weapon').appendChild(o2);
});
const fams=[...new Set(DATA.weapons.map(w=>w.family).filter(Boolean))].sort();
fams.forEach(f=>{ const o=document.createElement('option'); o.value=f; o.textContent=f; $('fam').appendChild(o); });

function renderStats(n) {
  const s = DATA.summary;
  $('stats').innerHTML = [
    ['Показано', n],
    ['Компонентов', s.total],
    ['Оружий со слотами', s.weapons_with_slots],
    ['Active в CSV', s.active_weapons],
    ['Empty', s.empty],
    ['Legacy flat CTH', s.legacy_flat_cth],
    ['Leftover optic', s.leftover_optic],
    ['Entity / irons', s.entity_visual],
    ['Unused skipped', s.unused_skipped],
  ].map(x => '<div class="stat"><b>'+x[1]+'</b><span>'+x[0]+'</span></div>').join('');
}

function flagPills(flags) {
  return flags.map(f => {
    const cls = f==='empty'||f==='orphan_params'||f==='wrong_sign'||f==='leftover_optic' ? 'bad'
      : (f==='legacy_flat_cth'||f==='nonjazz_scope') ? 'warn'
      : f==='entity_visual' ? 'ok' : 'ok';
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

function weaponsPreview(c, limit) {
  if (!c.weapons.length) return '<div class="guns">нет на оружии</div>';
  const show = c.weapons.slice(0, limit);
  const more = c.weapons.length - show.length;
  return '<div class="guns"><b>Оружие ('+c.weapons.length+'):</b> '+
    show.map(w => w.id+(w.default?'*':'')).join(', ')+
    (more>0 ? ' … +'+more : '')+
    ' <span style="color:#7a8088">(* = default)</span></div>';
}

function weaponsTable(c) {
  if (!c.weapons.length) return '<div class="meta">Не стоит ни на одном стволе в options CSV</div>';
  return '<table class="wtable"><tr><th>ID</th><th>Имя</th><th>Tier</th><th>Family</th><th>Слот</th><th></th></tr>'+
    c.weapons.map(w => '<tr><td class="mono">'+w.id+'</td><td>'+w.name+'</td><td>'+(w.tier||'—')+
      '</td><td>'+(w.family||'—')+'</td><td>'+w.slot+'</td><td>'+(w.default?'<span class="pill def">default</span>':'')+
      '</td></tr>').join('')+'</table>';
}

function filteredComps() {
  const slot=$('slot').value, flag=$('flag').value, src=$('src').value, q=$('q').value.trim().toLowerCase();
  const wep=$('weaponFilter').value;
  const showEmpty=$('hasFx').checked;
  return DATA.components.filter(c => {
    if (slot && c.slot!==slot) return false;
    if (flag && !c.flags.includes(flag)) return false;
    if (src && c.source!==src) return false;
    if (!showEmpty && c.flags.includes('empty')) return false;
    if (wep && !c.weapons.some(w => w.id===wep)) return false;
    if (q) {
      const hit = c.id.toLowerCase().includes(q) || c.name.toLowerCase().includes(q) ||
        c.raw_effects.toLowerCase().includes(q) ||
        c.weapons.some(w => w.id.toLowerCase().includes(q) || (w.name||'').toLowerCase().includes(q));
      if (!hit) return false;
    }
    return true;
  }).sort((a,b)=> a.slot.localeCompare(b.slot)||a.id.localeCompare(b.id));
}

function openDetail(c) {
  $('detail').classList.add('open');
  $('detailBody').innerHTML = '<h2>'+c.name+' <span class="id">'+c.id+'</span></h2>'+
    '<div class="meta">slot <b>'+c.slot+'</b> · cost '+c.cost+' · diff '+c.diff+' · used_by '+c.used+
    ' · '+c.source+' · group '+c.group+'</div>'+flagPills(c.flags)+effectList(c)+paramBlock(c)+
    '<h2 style="margin-top:14px;font-size:.9rem">Стоит на оружии</h2>'+weaponsTable(c)+
    '<div class="params" style="margin-top:10px">raw effects: '+(c.raw_effects||'—')+'<br/>raw params: '+(c.raw_params||'—')+'</div>';
}

function renderComps() {
  const rows = filteredComps();
  renderStats(rows.length);
  $('grid').classList.remove('hidden');
  $('wepView').classList.add('hidden');
  const g=$('grid'); g.innerHTML='';
  rows.forEach(c => {
    const card=document.createElement('div'); card.className='card';
    card.innerHTML = '<div class="id">'+c.id+'</div><h3>'+c.name+'</h3>'+
      '<div class="meta"><span class="pill">'+c.slot+'</span> used '+c.used+' · '+c.source+'</div>'+
      flagPills(c.flags)+
      '<div class="meta">'+(c.effects.map(e=>e.id).join(', ')||'—')+'</div>'+
      weaponsPreview(c, 8);
    card.onclick=()=>openDetail(c);
    g.appendChild(card);
  });
}

function fillWeaponSelect() {
  const fam=$('fam').value; const q=$('wq').value.trim().toLowerCase();
  const sel=$('weapon'); const cur=sel.value;
  sel.innerHTML='';
  wepsSorted.filter(w => {
    if (fam && w.family!==fam) return false;
    if (q && !(w.id.toLowerCase().includes(q) || w.name.toLowerCase().includes(q))) return false;
    return true;
  }).forEach(w => {
    const o=document.createElement('option');
    o.value=w.id; o.textContent=(w.tier?w.tier+' · ':'')+w.name+' ('+w.id+')';
    sel.appendChild(o);
  });
  if ([...sel.options].some(o=>o.value===cur)) sel.value=cur;
}

function renderWeapon() {
  fillWeaponSelect();
  const wid=$('weapon').value;
  const w = DATA.weapons.find(x => x.id===wid);
  $('grid').classList.add('hidden');
  $('wepView').classList.remove('hidden');
  if (!w) { $('wepView').innerHTML='<div class="meta">нет оружия</div>'; return; }
  renderStats(w.parts.length);
  const bySlot = {};
  w.parts.forEach(p => { (bySlot[p.slot]=bySlot[p.slot]||[]).push(p); });
  let html = '<div class="card" style="cursor:default"><div class="id">'+w.id+'</div><h3>'+w.name+
    '</h3><div class="meta"><span class="pill">'+(w.family||'?')+'</span> tier '+(w.tier||'—')+' · parts '+w.parts.length+'</div></div>';
  Object.keys(bySlot).sort().forEach(slot => {
    html += '<h2 style="margin:16px 0 8px;font-size:.85rem;color:var(--muted)">'+slot+'</h2><div class="grid">';
    bySlot[slot].forEach(p => {
      const c = byId[p.component_id];
      const fx = c ? (c.effects.map(e=>e.id).join(', ')||'—') : '—';
      html += '<div class="card" data-cid="'+p.component_id+'"><div class="id">'+p.component_id+'</div><h3>'+p.component_name+'</h3>'+
        '<div class="meta">'+(p.default?'<span class="pill def">default</span>':'')+
        (p.modifiable?'':'<span class="pill warn">locked</span>')+'</div>'+
        '<div class="meta">'+fx+'</div></div>';
    });
    html += '</div>';
  });
  $('wepView').innerHTML = html;
  $('wepView').querySelectorAll('.card[data-cid]').forEach(el => {
    el.onclick = () => { const c=byId[el.dataset.cid]; if (c) openDetail(c); };
  });
}

function setTab(mode) {
  const comp = mode==='comp';
  $('tabComp').classList.toggle('on', comp);
  $('tabWep').classList.toggle('on', !comp);
  $('barComp').classList.toggle('hidden', !comp);
  $('barWep').classList.toggle('hidden', comp);
  if (comp) renderComps(); else renderWeapon();
}

$('tabComp').onclick=()=>setTab('comp');
$('tabWep').onclick=()=>setTab('wep');
['slot','flag','src','hasFx','weaponFilter'].forEach(id=>$(id).addEventListener('change',renderComps));
$('q').addEventListener('input',renderComps);
['fam','weapon'].forEach(id=>$(id).addEventListener('change',renderWeapon));
$('wq').addEventListener('input',renderWeapon);
$('closeBtn').onclick=()=>$('detail').classList.remove('open');
setTab('comp');
</script>
</body>
</html>
'''

if __name__ == "__main__":
    main()
