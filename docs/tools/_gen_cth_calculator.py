# -*- coding: utf-8 -*-
"""Build standalone docs/tools/cth-calculator.html from cth-calculator-data.json.

Mirrors Code/AccuracyRangeCTH.lua + Unit:CalcChanceToHit firearm pipeline
(skill/aim, range/optic, multiplicative combat factors). Optics are the
primary compare surface.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSON = HERE / "cth-calculator-data.json"
OUT = HERE / "cth-calculator.html"
EXPORT = HERE / "_export_cth_calculator_data.py"

HTML = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>JAZZ · калькулятор точности (CTH)</title>
<style>
:root{--bg:#16171a;--panel:#22252b;--line:#3a3f4a;--text:#e8eaed;--muted:#9aa0a6;--accent:#c4a35a;--good:#6abf69;--bad:#e07070;--warn:#d4a017;--blue:#8ab4f8;--mono:ui-monospace,Consolas,monospace;--sans:"Segoe UI",system-ui,sans-serif}
*{box-sizing:border-box}body{margin:0;font-family:var(--sans);background:var(--bg);color:var(--text)}
header{padding:14px 18px;border-bottom:1px solid var(--line);background:var(--panel);display:flex;justify-content:space-between;align-items:flex-start;gap:16px}
header .copy{flex:1;min-width:0}
header h1{margin:0 0 4px;font-size:1.15rem;color:var(--accent)}
header p{margin:0;color:var(--muted);font-size:.82rem;max-width:1100px;line-height:1.45}
.lang{display:flex;gap:4px;flex-shrink:0;padding-top:2px}
.lang button{min-width:44px}
html[lang=en] tr.fit td:first-child::after{content:" · on gun"}
.layout{display:grid;grid-template-columns:minmax(240px,300px) 1fr;min-height:calc(100vh - 92px)}
@media(max-width:980px){.layout{grid-template-columns:1fr}}
.side{border-right:1px solid var(--line);background:#1c1e23;padding:12px 14px;display:flex;flex-direction:column;gap:8px;max-height:calc(100vh - 92px);overflow:auto}
.main{padding:14px 18px 48px;overflow:auto}
.field label,.bar label{display:block;font-size:.7rem;color:var(--muted);margin-bottom:3px}
.field select,.field input,.bar select,.bar input{background:var(--panel);border:1px solid var(--line);color:var(--text);border-radius:4px;padding:6px 8px;width:100%}
.field{margin-bottom:6px}
.list{flex:1;overflow:auto;border:1px solid var(--line);border-radius:6px;background:var(--bg);min-height:200px}
.item{display:flex;justify-content:space-between;gap:8px;padding:7px 9px;border-bottom:1px solid var(--line);cursor:pointer;font-size:.82rem}
.item:hover,.item.on{background:var(--panel)}
.item .n{font-weight:600}
.item .s{font-size:.68rem;color:var(--muted)}
.item .m{font-family:var(--mono);font-size:.72rem;color:var(--accent);white-space:nowrap}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-bottom:12px}
.card h2{margin:0 0 10px;font-size:.95rem;color:var(--accent)}
.card.optic{border-color:#5a4a28}
.stats{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;min-width:110px}
.stat b{display:block;font-family:var(--mono);font-size:1.25rem;color:var(--accent)}
.stat span{font-size:.7rem;color:var(--muted)}
.stat.big{min-width:150px}
.stat.big b{font-size:1.8rem;color:var(--text)}
.stat.good b{color:var(--good)} .stat.mid b{color:var(--warn)} .stat.bad b{color:var(--bad)}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:end}
.row .field{flex:1;min-width:120px}
.chk{display:flex;align-items:center;gap:6px;font-size:.8rem;color:var(--muted);padding:4px 0}
.range-val{font-family:var(--mono);color:var(--accent);font-size:.85rem}
table{width:100%;border-collapse:collapse;font-size:.78rem}
th,td{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;white-space:nowrap}
th{color:var(--muted);font-weight:500;position:sticky;top:0;background:#1c1e23;z-index:1}
td.l,th.l{text-align:left}
td.mono{font-family:var(--mono);color:var(--accent)}
.cell{font-family:var(--mono);font-weight:600}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:.68rem;margin-right:4px;color:var(--muted)}
.pill.reflex{color:#8ab4f8;border-color:#3a5080}
.pill.combat{color:#6abf69;border-color:#2a5a2a}
.pill.long{color:#d4a017;border-color:#6a5a20}
.pill.night{color:#c9a0e8;border-color:#4a3a60}
.pill.irons{color:var(--muted)}
.note{color:var(--muted);font-size:.75rem;line-height:1.45;margin:8px 0 0}
.callout{font-size:.78rem;color:var(--muted);background:#1a1c21;border-left:3px solid var(--accent);padding:8px 10px;margin:8px 0 0;line-height:1.45}
canvas{width:100%;height:240px;background:#121316;border:1px solid var(--line);border-radius:6px}
tr.sel{background:#2a2f38}
tr.fit td:first-child::after{content:" · на стволе";color:var(--muted);font-size:.65rem}
.meta{font-size:.78rem;color:var(--muted);line-height:1.5}
.hidden{display:none !important}
button{background:var(--panel);border:1px solid var(--line);color:var(--text);border-radius:4px;padding:6px 10px;cursor:pointer;font-size:.8rem}
button:hover,button.on{border-color:var(--accent);color:var(--accent)}
</style>
</head>
<body>
<header>
  <div class="copy">
    <h1 data-i18n="h1">JAZZ · калькулятор точности</h1>
    <p data-i18n-html="intro">Ядро <code>AccuracyRangeCTH</code> + боевые множители <code>CalcChanceToHit</code>.
    Прицел не даёт плоский +CTH: сдвигает зону <b>E</b>, включает AimAccuracy% после AimLevel,
    штрафует упор (near) сразу при установке. Коллем смягчает ближнюю зону оружия.
    Видимость цели тоже режется оптикой после unlock. Возможный выстрел 2–100%; 0 = за пределом дальности.</p>
  </div>
  <div class="lang" role="group" aria-label="Language">
    <button type="button" data-lang="ru" class="on">RU</button>
    <button type="button" data-lang="en">EN</button>
  </div>
</header>
<div class="layout">
<aside class="side">
  <div class="row">
    <div class="field" style="flex:1"><label data-i18n="family">Семейство</label><select id="fam"></select></div>
  </div>
  <div class="field"><label data-i18n="search">Поиск</label><input id="q" data-i18n-placeholder="searchPh" placeholder="AKM, СВД, Glock…"/></div>
  <div class="list" id="wlist"></div>
</aside>
<main class="main">
  <div class="stats" id="hero"></div>
  <div class="grid">
    <div class="card">
      <h2 data-i18n="cardShooter">Стрелок и прицеливание</h2>
      <div class="row">
        <div class="field"><label><span data-i18n="dex">Ловкость</span> <span class="range-val" id="dexV"></span></label><input type="range" id="dex" min="1" max="100" value="70"/></div>
        <div class="field"><label><span data-i18n="mrk">Меткость</span> <span class="range-val" id="mrkV"></span></label><input type="range" id="mrk" min="1" max="100" value="70"/></div>
      </div>
      <div class="row">
        <div class="field"><label><span data-i18n="lvl">Уровень</span> <span class="range-val" id="lvlV"></span></label><input type="range" id="lvl" min="1" max="10" value="5"/></div>
        <div class="field"><label><span data-i18n="str">Сила</span> <span class="range-val" id="strV"></span></label><input type="range" id="str" min="1" max="100" value="70"/></div>
      </div>
      <div class="row">
        <div class="field"><label><span data-i18n="aimClicks">Клики aim</span> <span class="range-val" id="aimV"></span></label><input type="range" id="aim" min="0" max="6" value="3"/></div>
        <div class="field"><label><span data-i18n="distance">Дистанция, кл.</span> <span class="range-val" id="distV"></span></label><input type="range" id="dist" min="0" max="80" value="20"/></div>
      </div>
      <div class="row">
        <button type="button" data-aim="snap">Snap</button>
        <button type="button" data-aim="plus1">+1</button>
        <button type="button" data-aim="full" data-i18n="fullAim">Полный aim</button>
      </div>
      <p class="note" id="aimNote"></p>
    </div>
    <div class="card optic">
      <h2 data-i18n="cardOptic">Прицел и обвес</h2>
      <div class="field"><label data-i18n="scope">Прицел</label><select id="scope"></select></div>
      <div class="field"><label data-i18n="barrel">Ствол</label><select id="barrel"></select></div>
      <div class="field"><label data-i18n="stock">Приклад</label><select id="stock"></select></div>
      <div class="field"><label data-i18n="grip">Рукоять / цевьё</label><select id="grip"></select></div>
      <div class="field"><label data-i18n="mag">Магазин</label><select id="mag"></select></div>
      <div class="field"><label data-i18n="side">Лазер / бок</label><select id="side"></select></div>
      <p class="meta" id="opticMeta"></p>
    </div>
    <div class="card">
      <h2 data-i18n="cardCombat">Бой</h2>
      <div class="field"><label data-i18n="cover">Укрытие / стойка цели</label>
        <select id="cover">
          <option value="open" data-i18n="coverOpen">Открыто, стоя</option>
          <option value="crouch" data-i18n="coverCrouch">Сидит, без укрытия (−12)</option>
          <option value="prone" data-i18n="coverProne">Лежит, без укрытия (−23)</option>
          <option value="exposed" data-i18n="coverExposed">Слабое / exposed (−12)</option>
          <option value="half" data-i18n="coverHalf">Частичное (~середина)</option>
          <option value="full" data-i18n="coverFull">Полное укрытие (−45)</option>
        </select>
      </div>
      <div class="chk"><input type="checkbox" id="dust"/><label for="dust" data-i18n="dust">Пылевая буря на укрытии (−40 к cover)</label></div>
      <div class="field"><label data-i18n="vis">Видимость</label>
        <select id="vis">
          <option value="off" data-i18n="visOff">Без штрафа видимости</option>
          <option value="day" selected data-i18n="visDay">День, чистая</option>
          <option value="heat" data-i18n="visHeat">Жара (×0.9 дист. видимости)</option>
          <option value="rain" data-i18n="visRain">Дождь (×1.1)</option>
          <option value="fog" data-i18n="visFog">Ливень / туман (×1.3)</option>
          <option value="storm" data-i18n="visStorm">Буря (×1.5)</option>
          <option value="night" data-i18n="visNight">Ночь / подземелье (×1.6)</option>
          <option value="nightLit" data-i18n="visNightLit">Ночь, цель подсвечена</option>
          <option value="nightNV" data-i18n="visNightNV">Ночь, ПНВ стрелка (×1.3 к штрафу irons)</option>
          <option value="spotter" data-i18n="visSpotter">Слепой огонь, видит команда (−10)</option>
          <option value="blind" data-i18n="visBlind">Слепой огонь (−60)</option>
          <option value="nolos" data-i18n="visNoLos">Нет LoS (−50)</option>
        </select>
      </div>
      <div class="field"><label data-i18n="sight">Зрение, кл. (Aware 46)</label><input type="number" id="sight" min="8" max="60" value="46"/></div>
      <div class="field"><label data-i18n="supp">Подавление стрелка</label>
        <select id="supp">
          <option value="0" data-i18n="none">Нет</option>
          <option value="-10" data-i18n="suppLight">Лёгкое (−10)</option>
          <option value="-20" data-i18n="suppMed">Среднее (−20)</option>
          <option value="-30" data-i18n="suppHeavy">Тяжёлое (−30)</option>
          <option value="-50" data-i18n="suppHeavy2">Тяжёлое 2 (−50)</option>
          <option value="-70" data-i18n="suppPinned">Прижат (−70)</option>
        </select>
      </div>
      <div class="row">
        <div class="field"><label data-i18n="pain">Боль, стаки</label><input type="number" id="pain" min="0" max="8" value="0"/></div>
        <div class="field"><label data-i18n="conc">Контузия</label>
          <select id="conc"><option value="0" data-i18n="none">Нет</option><option value="-15" data-i18n="yes15">Да (−15)</option></select>
        </div>
      </div>
      <div class="row">
        <div class="field"><label data-i18n="tarms">Травма рук</label>
          <select id="tarms"><option value="0" data-i18n="none">Нет</option><option value="-20" data-i18n="tierMed20">Средняя (−20)</option><option value="-50" data-i18n="tierHvy50">Тяжёлая (−50)</option></select>
        </div>
        <div class="field"><label data-i18n="thead">Травма головы</label>
          <select id="thead"><option value="0" data-i18n="none">Нет</option><option value="-15" data-i18n="tierMed15">Средняя (−15)</option><option value="-40" data-i18n="tierHvy40">Тяжёлая (−40)</option></select>
        </div>
      </div>
      <div class="row">
        <div class="field"><label data-i18n="drunk">Пьянство, стаки</label><input type="number" id="drunk" min="0" max="5" value="0"/></div>
        <div class="field"><label data-i18n="morale">Мораль (−3…+3)</label><input type="number" id="morale" min="-3" max="3" value="0"/></div>
      </div>
      <div class="row">
        <div class="field"><label data-i18n="tracers">Трассеры на цели</label><input type="number" id="tracers" min="0" max="8" value="0"/></div>
        <div class="field"><label data-i18n="extra">Прочее, пункты</label><input type="number" id="extra" value="0"/></div>
      </div>
      <div class="chk"><input type="checkbox" id="oa"/><label for="oa" data-i18n="oa">Opportunity / interrupt</label></div>
      <div class="chk"><input type="checkbox" id="supported"/><label for="supported" data-i18n="supported">Пулемёт с опорой / сошки / setup</label></div>
      <div class="field"><label data-i18n="stance">Стойка стрелка (отдача / опора)</label>
        <select id="stance">
          <option value="Standing" data-i18n="stanceStand">Standing</option>
          <option value="Crouch" data-i18n="stanceCrouch">Crouch</option>
          <option value="Prone" data-i18n="stanceProne">Prone</option>
        </select>
      </div>
      <div class="chk"><input type="checkbox" id="autoW"/><label for="autoW" data-i18n="autoW">Перк AutoWeapons (отдача ×0.85)</label></div>
    </div>
  </div>
  <div class="card">
    <h2 data-i18n="cardBreak">Разбивка выстрела</h2>
    <table><thead><tr><th class="l" data-i18n="colStage">Стадия</th><th data-i18n="colValue">Значение</th><th class="l" data-i18n="colMeaning">Смысл</th></tr></thead><tbody id="brk"></tbody></table>
    <p class="note" id="post"></p>
  </div>
  <div class="card optic">
    <h2 data-i18n="cardCompare">Сравнение прицелов</h2>
    <div class="row" style="margin-bottom:8px">
      <div class="field"><label data-i18n="cmpAim">Aim в таблице</label>
        <select id="cmpAim">
          <option value="current" data-i18n="cmpCurrent">Как слайдер</option>
          <option value="snap" data-i18n="cmpSnap">Snap / MinAim</option>
          <option value="plus1" data-i18n="cmpPlus1">+1 клик</option>
          <option value="full" data-i18n="cmpFull">Полный aim</option>
        </select>
      </div>
      <div class="chk" style="padding-bottom:8px"><input type="checkbox" id="onlyFit" checked/><label for="onlyFit" data-i18n="onlyFit">Только слот этого ствола + irons</label></div>
      <div class="chk" style="padding-bottom:8px"><input type="checkbox" id="withCombat" checked/><label for="withCombat" data-i18n="withCombat">С текущими боевыми модификаторами</label></div>
    </div>
    <p class="note" data-i18n="cmpNote">Δ — к открытому прицелу на той же дистанции и том же aim-режиме. Серые AA% ещё не unlock. Near действует сразу.</p>
    <div style="overflow:auto;max-height:420px">
      <table><thead id="cmpHead"></thead><tbody id="cmpBody"></tbody></table>
    </div>
  </div>
  <div class="card">
    <h2 data-i18n="cardChart">CTH по дистанции</h2>
    <canvas id="chart" width="980" height="240"></canvas>
    <p class="note" data-i18n="chartNote">Серый — irons. Акцент — выбранный прицел. Точка — текущая дистанция. Пунктир — конец эффективной зоны E.</p>
  </div>
</main>
</div>
<script>
const DATA = __DATA__;
const FAM_EN = {"pistol":"Pistols","autopistol":"Machine pistols","revolver":"Revolvers","submachine-gun":"SMGs","carbine":"Carbines","assault-rifle":"Assault rifles","battle-rifle":"Battle rifles","sniper-rifle":"Sniper rifles","shotgun":"Shotguns","machine-gun":"Machine guns","light-machine-gun":"LMGs"};
const I18N = {
ru:{
title:"JAZZ · калькулятор точности (CTH)",h1:"JAZZ · калькулятор точности",
intro:"Ядро <code>AccuracyRangeCTH</code> + боевые множители <code>CalcChanceToHit</code>. Прицел не даёт плоский +CTH: сдвигает зону <b>E</b>, включает AimAccuracy% после AimLevel, штрафует упор (near) сразу при установке. Коллем смягчает ближнюю зону оружия. Видимость цели тоже режется оптикой после unlock. Возможный выстрел 2–100%; 0 = за пределом дальности.",
family:"Семейство",search:"Поиск",searchPh:"AKM, СВД, Glock…",all:"Все",
cardShooter:"Стрелок и прицеливание",dex:"Ловкость",mrk:"Меткость",lvl:"Уровень",str:"Сила",aimClicks:"Клики aim",distance:"Дистанция, кл.",fullAim:"Полный aim",
cardOptic:"Прицел и обвес",scope:"Прицел",barrel:"Ствол",stock:"Приклад",grip:"Рукоять / цевьё",mag:"Магазин",side:"Лазер / бок",
emptyIrons:"Открытый прицел",emptyBase:"База оружия",emptyNone:"База / нет",none:"Нет",factory:"Заводской",
cardCombat:"Бой",cover:"Укрытие / стойка цели",
coverOpen:"Открыто, стоя",coverCrouch:"Сидит, без укрытия (−12)",coverProne:"Лежит, без укрытия (−23)",coverExposed:"Слабое / exposed (−12)",coverHalf:"Частичное (~середина)",coverFull:"Полное укрытие (−45)",
dust:"Пылевая буря на укрытии (−40 к cover)",vis:"Видимость",
visOff:"Без штрафа видимости",visDay:"День, чистая",visHeat:"Жара (×0.9 дист. видимости)",visRain:"Дождь (×1.1)",visFog:"Ливень / туман (×1.3)",visStorm:"Буря (×1.5)",
visNight:"Ночь / подземелье (×1.6)",visNightLit:"Ночь, цель подсвечена",visNightNV:"Ночь, ПНВ стрелка (×1.3 к штрафу irons)",visSpotter:"Слепой огонь, видит команда (−10)",visBlind:"Слепой огонь (−60)",visNoLos:"Нет LoS (−50)",
sight:"Зрение, кл. (Aware 46)",supp:"Подавление стрелка",
suppLight:"Лёгкое (−10)",suppMed:"Среднее (−20)",suppHeavy:"Тяжёлое (−30)",suppHeavy2:"Тяжёлое 2 (−50)",suppPinned:"Прижат (−70)",
pain:"Боль, стаки",conc:"Контузия",yes15:"Да (−15)",tarms:"Травма рук",thead:"Травма головы",
tierMed20:"Средняя (−20)",tierHvy50:"Тяжёлая (−50)",tierMed15:"Средняя (−15)",tierHvy40:"Тяжёлая (−40)",
drunk:"Пьянство, стаки",morale:"Мораль (−3…+3)",tracers:"Трассеры на цели",extra:"Прочее, пункты",
oa:"Opportunity / interrupt",supported:"Пулемёт с опорой / сошки / setup",stance:"Стойка стрелка (отдача / опора)",
stanceStand:"Стоя",stanceCrouch:"Сидя",stanceProne:"Лёжа",autoW:"Перк AutoWeapons (отдача ×0.85)",
cardBreak:"Разбивка выстрела",colStage:"Стадия",colValue:"Значение",colMeaning:"Смысл",
cardCompare:"Сравнение прицелов",cmpAim:"Aim в таблице",cmpCurrent:"Как слайдер",cmpSnap:"Snap / MinAim",cmpPlus1:"+1 клик",cmpFull:"Полный aim",
onlyFit:"Только слот этого ствола + irons",withCombat:"С текущими боевыми модификаторами",
cmpNote:"Δ — к открытому прицелу на той же дистанции и том же aim-режиме. Серые AA% ещё не unlock. Near действует сразу.",
cardChart:"CTH по дистанции",chartNote:"Серый — irons. Акцент — выбранный прицел. Точка — текущая дистанция. Пунктир — конец эффективной зоны E.",
heroCore:"Ядро",heroAfterRange:"После дистанции",heroOverflow:"Overflow → крит",heroE:"E / BDR / R",heroAim:"Aim",heroAA:"AA эфф.",heroMiss:"Miss→graze",heroCoverG:"Cover→graze",
aimNoteMin:"На этом прицеле MinAim: нулевой клик считается как 1. MaxAim после обвеса: {n}.",
aimNote:"Snap = 0 кликов (Ловкость). Полный aim раскрывает Меткость. MaxAim: {n}.",
rowSnap:"Ловкость / snap",rowPrec:"Меткость / precision",rowGain:"Aim gain",rowCore:"Ядро до cap",rowRange:"Дальность",
metaDex:"канал Dex",metaMark:"канал Mark",metaGain:"клики × AA × mastery {n}",metaOverflow:"избыток +{n} в крит",metaCap:"cap 100 на попадание",metaOor:"за WeaponRange",
queue:"Очередь (recoil eff {er}, retention {ret}%): {shots}",shotN:"п{n}",
cmpScope:"Прицел",cmpFam:"Семья",
fSpotter:"Видит споттер",fBlind:"Слепой огонь",fNoLos:"Нет LoS",fVisOptic:"Видимость (оптика {mag}×)",fVisLit:"Видимость (подсветка)",fVisNV:"Видимость (ПНВ)",fVisNight:"Видимость (ночь)",fVis:"Видимость цели",
fTgtCrouch:"Цель сидит",fTgtProne:"Цель лежит",fCover:"Укрытие",fCoverDust:"Укрытие (пыль)",fWeak:" слабое",fFull:" полное",fHalf:" частичное",
fLaser:"Лазер",fLaserFall:"Лазер (спад)",fSupp:"Подавление",fPain:"Боль ×{n}",fConc:"Контузия",fArms:"Травма рук",fHead:"Травма головы",fDrunk:"Пьянство ×{n}",fMorale:"Боевой дух",fTracers:"Трассеры",fExtra:"Прочее",
fNightIrons:"Контрастный прицел",fComp:"Компонент",fPistol:"Пистолет вблизи",fUnsup:"Без опоры",fCloseW:"Ближняя зона оружия",fCloseO:"Ближняя зона оптики",
aaOn:" (вкл)",aaWait:" (ждёт aim≥{n})",wpnClose:"оружие Close",
onGun:" · на стволе"
},
en:{
title:"JAZZ · accuracy calculator (CTH)",h1:"JAZZ · accuracy calculator",
intro:"Core <code>AccuracyRangeCTH</code> plus <code>CalcChanceToHit</code> combat factors. A sight is not a flat +CTH: it shifts the <b>E</b> zone, enables AimAccuracy% after AimLevel, and applies a close-range (near) tax as soon as it is mounted. Reflex sights soften the weapon close zone. Target visibility is also reduced by optics after unlock. A possible shot is 2–100%; 0 means out of WeaponRange.",
family:"Family",search:"Search",searchPh:"AKM, SVD, Glock…",all:"All",
cardShooter:"Shooter and aiming",dex:"Dexterity",mrk:"Marksmanship",lvl:"Level",str:"Strength",aimClicks:"Aim clicks",distance:"Distance, tiles",fullAim:"Full aim",
cardOptic:"Sight and attachments",scope:"Sight",barrel:"Barrel",stock:"Stock",grip:"Grip / handguard",mag:"Magazine",side:"Laser / side",
emptyIrons:"Iron sights",emptyBase:"Weapon default",emptyNone:"Default / none",none:"None",factory:"Factory",
cardCombat:"Combat",cover:"Cover / target stance",
coverOpen:"Open, standing",coverCrouch:"Crouched, no cover (−12)",coverProne:"Prone, no cover (−23)",coverExposed:"Weak / exposed (−12)",coverHalf:"Partial (~mid)",coverFull:"Full cover (−45)",
dust:"Dust storm on cover (−40 to cover)",vis:"Visibility",
visOff:"No visibility penalty",visDay:"Day, clear",visHeat:"Heat (×0.9 vis distance)",visRain:"Rain (×1.1)",visFog:"Heavy rain / fog (×1.3)",visStorm:"Storm (×1.5)",
visNight:"Night / underground (×1.6)",visNightLit:"Night, target lit",visNightNV:"Night, shooter NV (×1.3 irons penalty)",visSpotter:"Blind fire, team sees (−10)",visBlind:"Blind fire (−60)",visNoLos:"No LoS (−50)",
sight:"Sight range, tiles (Aware 46)",supp:"Shooter suppression",
suppLight:"Light (−10)",suppMed:"Medium (−20)",suppHeavy:"Heavy (−30)",suppHeavy2:"Heavy 2 (−50)",suppPinned:"Pinned (−70)",
pain:"Pain stacks",conc:"Concussion",yes15:"Yes (−15)",tarms:"Arm trauma",thead:"Head trauma",
tierMed20:"Medium (−20)",tierHvy50:"Heavy (−50)",tierMed15:"Medium (−15)",tierHvy40:"Heavy (−40)",
drunk:"Drunk stacks",morale:"Morale (−3…+3)",tracers:"Tracers on target",extra:"Other, points",
oa:"Opportunity / interrupt",supported:"MG supported / bipod / setup",stance:"Shooter stance (recoil / support)",
stanceStand:"Standing",stanceCrouch:"Crouch",stanceProne:"Prone",autoW:"AutoWeapons perk (recoil ×0.85)",
cardBreak:"Shot breakdown",colStage:"Stage",colValue:"Value",colMeaning:"Meaning",
cardCompare:"Sight comparison",cmpAim:"Aim in table",cmpCurrent:"As slider",cmpSnap:"Snap / MinAim",cmpPlus1:"+1 click",cmpFull:"Full aim",
onlyFit:"This gun's slot + irons only",withCombat:"Apply current combat modifiers",
cmpNote:"Δ is versus iron sights at the same distance and aim mode. Grey AA% is still locked. Near tax applies immediately.",
cardChart:"CTH vs distance",chartNote:"Grey = irons. Gold = selected sight. Vertical line = current distance. Dashed = end of effective zone E.",
heroCore:"Core",heroAfterRange:"After range",heroOverflow:"Overflow → crit",heroE:"E / BDR / R",heroAim:"Aim",heroAA:"Eff. AA",heroMiss:"Miss→graze",heroCoverG:"Cover→graze",
aimNoteMin:"This sight has MinAim: a zero click counts as 1. MaxAim after attachments: {n}.",
aimNote:"Snap = 0 clicks (Dexterity). Full aim reveals Marksmanship. MaxAim: {n}.",
rowSnap:"Dexterity / snap",rowPrec:"Marksmanship / precision",rowGain:"Aim gain",rowCore:"Core before cap",rowRange:"Range",
metaDex:"Dex channel",metaMark:"Mark channel",metaGain:"clicks × AA × mastery {n}",metaOverflow:"overflow +{n} to crit",metaCap:"cap 100 on hit",metaOor:"beyond WeaponRange",
queue:"Burst (recoil eff {er}, retention {ret}%): {shots}",shotN:"r{n}",
cmpScope:"Sight",cmpFam:"Family",
fSpotter:"Seen by spotter",fBlind:"Blind fire",fNoLos:"No LoS",fVisOptic:"Visibility (optic {mag}×)",fVisLit:"Visibility (lit)",fVisNV:"Visibility (NV)",fVisNight:"Visibility (night)",fVis:"Target visibility",
fTgtCrouch:"Target crouched",fTgtProne:"Target prone",fCover:"Cover",fCoverDust:"Cover (dust)",fWeak:" weak",fFull:" full",fHalf:" partial",
fLaser:"Laser",fLaserFall:"Laser (falloff)",fSupp:"Suppression",fPain:"Pain ×{n}",fConc:"Concussion",fArms:"Arm trauma",fHead:"Head trauma",fDrunk:"Drunk ×{n}",fMorale:"Morale",fTracers:"Tracers",fExtra:"Other",
fNightIrons:"Night irons",fComp:"Component",fPistol:"Pistol close",fUnsup:"Unsupported",fCloseW:"Weapon close zone",fCloseO:"Optic close zone",
aaOn:" (on)",aaWait:" (needs aim≥{n})",wpnClose:"weapon Close",
onGun:" · on gun"
}
};
let LANG = "ru";
try { LANG = localStorage.getItem("jazz-cth-lang") || "ru"; } catch (e) {}
if (LANG !== "en") LANG = "ru";
function t(k, vars){
  let s = (I18N[LANG] && I18N[LANG][k]) || (I18N.ru && I18N.ru[k]) || k;
  if (vars) Object.keys(vars).forEach(p => { s = s.split("{"+p+"}").join(String(vars[p])); });
  return s;
}
function famName(id){
  const w = DATA.weapons.find(x => x.fam === id);
  return LANG === "en" ? (FAM_EN[id] || id) : ((w && w.famRu) || id);
}
function archLabel(a){
  return LANG === "en" ? (a.labelEn || a.label) : a.label;
}
function applyStaticI18n(){
  document.documentElement.lang = LANG;
  document.title = t("title");
  document.querySelectorAll("[data-i18n]").forEach(el => { el.textContent = t(el.getAttribute("data-i18n")); });
  document.querySelectorAll("[data-i18n-html]").forEach(el => { el.innerHTML = t(el.getAttribute("data-i18n-html")); });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => { el.setAttribute("placeholder", t(el.getAttribute("data-i18n-placeholder"))); });
  document.querySelectorAll(".lang button").forEach(b => b.classList.toggle("on", b.getAttribute("data-lang") === LANG));
}
function setLang(lang){
  LANG = lang === "en" ? "en" : "ru";
  try { localStorage.setItem("jazz-cth-lang", LANG); } catch (e) {}
  const fam = $("fam").value;
  applyStaticI18n();
  initFam();
  $("fam").value = fam;
  syncSlots();
  renderList();
  render();
}
const FS = 1000, FLOOR = 250, MG_SPAN = 16, SLAB = 1200;
const CMP_D = [5,10,12,20,25,30,40,50];
const SLOTS = ["Scope","Barrel","Stock","Handgrip","Handguard","Magazine","Side","Muzzle","Bipod","Under"];
const $ = id => document.getElementById(id);
const clamp = (v,lo,hi) => Math.min(hi, Math.max(lo,v));
function roundH(v){ return v>=0 ? Math.floor(v+0.5) : Math.ceil(v-0.5); }
function mulDivRound(a,b,c){ if(!c) return 0; const n=a*b; return n>=0 ? Math.floor((n+Math.floor(c/2))/c) : Math.ceil((n-Math.floor(c/2))/c); }
function isqrt(n){
  n = Math.max(0, Math.floor(Number(n)||0));
  let lo=0, hi=n;
  while(lo<hi){
    const mid = Math.floor((lo+hi+1)/2);
    if(mid<=0) lo=mid;
    else if(mid>n/mid) hi=mid-1;
    else if(mid*mid<=n) lo=mid;
    else hi=mid-1;
  }
  return lo;
}
function skillCurve(value){
  value = Math.max(0, value||0);
  if(!value) return 20;
  const root2 = isqrt(value * 100000000);
  const root4 = isqrt(root2);
  return 20 + mulDivRound(value * root4, 1, 400);
}
function aimMastery(m){
  m = clamp(m,0,100);
  return Math.min(100,
    mulDivRound(Math.min(m,60),20,60)
    + mulDivRound(clamp(m-60,0,20),20,20)
    + mulDivRound(clamp(m-80,0,10),20,10)
    + mulDivRound(clamp(m-90,0,6),20,6)
    + mulDivRound(clamp(m-96,0,4),20,4)
  );
}
function pctToFactor(v){ return clamp(FS + roundH((v||0)*10), 50, 2000); }
function factorToPct(f){ return roundH(((f||FS)-FS)/10); }

function hasFx(c, id){ return c && c.fx && c.fx.indexOf(id)>=0; }
function pget(c,k,d){ if(!c||!c.p||c.p[k]==null) return d; return c.p[k]; }

function applyComp(w, c){
  if(!c) return;
  const p = c.p || {};
  if(hasFx(c,"IncreaseAimAccuracy15Percent") && p.AimAccuracyPercent!=null) w.aa *= p.AimAccuracyPercent/100;
  if(hasFx(c,"ReduceAimAccuracy15Percent") && p.AimAccuracyPercent!=null) w.aa *= p.AimAccuracyPercent/100;
  if(hasFx(c,"IncreaseAimAccuracy") && p.AimAccuracyIncrease!=null) w.aa += p.AimAccuracyIncrease;
  if(hasFx(c,"DecreaseMaxAimActions")) w.maxAim -= p.MaxAimActionsDecrease||0;
  if(hasFx(c,"IncreaseMaxAimActions")) w.maxAim += p.IncreaseMaxAimActions||p.MaxAimActionsIncrease||0;
  if(hasFx(c,"MinAim")) w.minAim = true;
  if(hasFx(c,"CloseRangeFactorIncrease")) w.closeF += p.CloseRangeFactorIncrease||0;
  if(hasFx(c,"CloseRangeFactorDecrease")) w.closeF -= p.CloseRangeFactorDecrease||0;
  if(hasFx(c,"CloseRangeIncrease")) w.close += p.CloseRangeIncrease||0;
  if(hasFx(c,"CloseRangeDecrease")) w.close = Math.max(0, w.close - (p.CloseRangeDecrease||0));
  if(hasFx(c,"BarrelBulletDropIncrease") && p.BulletDropIncrease) w.bdr = roundH(w.bdr * p.BulletDropIncrease / 100);
  if(hasFx(c,"BarrelBulletDropReduce") && p.BulletDropReduce) w.bdr = roundH(w.bdr * p.BulletDropReduce / 100);
  if(hasFx(c,"BarrelRangeIncrease")) w.r += p.BarrelRangeIncrease||0;
  if(hasFx(c,"BarrelRangeReduce") || hasFx(c,"ReduceRange")) w.r -= p.BarrelRangeReduce||p.RangeDecrease||0;
  if(hasFx(c,"BarrelGroupingReduce") && p.BarrelGroupingReduce) w.g = roundH(w.g * p.BarrelGroupingReduce / 100);
  if(hasFx(c,"BarrelGroupingIncrease") && p.SilencerGroupingReduce) w.g = roundH(w.g * p.SilencerGroupingReduce / 100);
  if(hasFx(c,"RecoilIncrease") && p.Recoil!=null) w.recoil += p.Recoil;
  if(hasFx(c,"RecoilDecrease") && p.Recoil!=null) w.recoil -= p.Recoil;
  if(hasFx(c,"BarrelRecoilIncrease")) w.recoil += p.BarrelRecoilIncrease||0;
  if(hasFx(c,"BarrelRecoilRecude")) w.recoil -= p.BarrelRecoilRecude||0;
  if(hasFx(c,"LaserMark")) w.laser = {cth:p.LaserCTH||0, dist:p.LaserDistance||0, full:p.LaserFullRange||5, nightOnly:!!p.NightOnly};
  if(hasFx(c,"OpportunityAttackBonusCth")) w.oaBonus += p.bonus_cth||0;
  if(hasFx(c,"NightsIronsBonus")) w.nightIrons += p.NightsIronsBonus||0;
  if(hasFx(c,"IgnoreInTheDark")) w.ignoreDark = true;
  if(hasFx(c,"IgnoreInTheDarkWhenFullyAimed")) w.nvFull = true;
  if(hasFx(c,"ShotsBeforeRecoilProne")) w.bipodShots += p.ShotsBeforeRecoilProne||0;
  if(hasFx(c,"MinorAccuracyBonus")) w.bonusCth += p.BonusCTH||0;
  if(hasFx(c,"ScopeMagnification") || hasFx(c,"SmallMagnification") || /Reflex|Collimator|HOLO|Коллиматор/.test(c.id+" "+c.name))
    w.opticComps.push(c);
}

function resolveWeapon(base, sel){
  const w = Object.assign({}, base);
  w.aa = base.aa; w.maxAim = base.maxAim; w.r = base.r; w.bdr = base.bdr; w.g = base.g;
  w.close = base.close; w.closeF = base.closeF; w.recoil = base.recoil;
  w.minAim = false; w.opticComps = []; w.laser = null; w.oaBonus = 0; w.nightIrons = 0;
  w.ignoreDark = false; w.nvFull = false; w.bipodShots = 0; w.bonusCth = 0;
  w.scopeId = sel.Scope || null;
  SLOTS.forEach(s => { const id = sel[s]; if(id && DATA.comps[id]) applyComp(w, DATA.comps[id]); });
  w.closeF = clamp(w.closeF, 25, 150);
  w.maxAim = Math.max(0, w.maxAim);
  w.r = Math.max(0, w.r);
  w.recoil = Math.max(0, w.recoil);
  w.aa = Math.max(0, w.aa);
  return w;
}

function buildOpticFromFx(c, aim, kind){
  const magKey = kind==="small" ? "SmallMagnification" : "ScopeMagnification";
  if(!hasFx(c, magKey) && kind!=="scope") return null;
  if(kind==="scope" && !hasFx(c,"ScopeMagnification")) return null;
  const subKey = kind==="small" ? "SmallSubMagnification" : "ScopeSubMagnification";
  const lvlKey = kind==="small" ? "SmallAimLevel" : "ScopeAimLevel";
  let mag = pget(c, magKey, null);
  if(mag==null) return null;
  mag = Math.max(1, mag + pget(c, subKey, 0)/10);
  const aimLevel = pget(c, lvlKey, 0);
  const aimOk = (aim||0) >= aimLevel;
  const explReach = c.p && c.p.OpticReach!=null ? c.p.OpticReach : null;
  const explMin = c.p && c.p.OpticMinRange!=null ? c.p.OpticMinRange : null;
  const explNear = c.p && c.p.OpticNearFactor!=null ? c.p.OpticNearFactor : null;
  const reach = aimOk ? (explReach!=null ? explReach : Math.max(0,(mag-1)*3)) : 0;
  const minR = explMin!=null ? explMin : (mag>=4 ? roundH(mag*0.9) : 0);
  let near = explNear!=null ? explNear*10 : (mag>=4 ? roundH(Math.max(0.35, 1-(mag-2)*0.09)*FS) : FS);
  near = clamp(near, 250, FS);
  return {id:c.id, mag, aimLevel, aimOk, reach, minR, near};
}

function fallbackOptic(c, aim){
  if(!c) return {id:false, mag:1, aimLevel:0, aimOk:true, reach:0, minR:0, near:FS};
  const blob = c.id+" "+c.name;
  if(/Reflex|Collimator|HOLO|Коллиматор/.test(blob)){
    return {id:c.id, mag:1.2, aimLevel:0, aimOk:true, reach:2, minR:0, near:FS};
  }
  return {id:c.id, mag:1, aimLevel:0, aimOk:true, reach:0, minR:0, near:FS};
}

function mergeOptic(scope, aux){
  if(!scope && !aux) return {id:false, mag:1, aimLevel:0, aimOk:false, reach:0, minR:0, near:FS};
  if(!scope) return aux;
  if(!aux) return scope;
  let nearSrc = scope;
  if(aux.mag > scope.mag) nearSrc = aux;
  let reach = 0, reachSrc = nearSrc;
  if(scope.reach > reach){ reach = scope.reach; reachSrc = scope; }
  if(aux.reach > reach){ reach = aux.reach; reachSrc = aux; }
  return {id: reachSrc.id||nearSrc.id, mag: nearSrc.mag, aimLevel: reachSrc.aimLevel||nearSrc.aimLevel, aimOk: reach>0, reach, minR: nearSrc.minR, near: nearSrc.near};
}

function opticProfile(w, aim){
  let scope=null, aux=null;
  (w.opticComps||[]).forEach(c => {
    const s = buildOpticFromFx(c, aim, "scope");
    const a = buildOpticFromFx(c, aim, "small");
    if(s) scope = s;
    if(a) aux = a;
    if(!s && !a && !scope) scope = fallbackOptic(c, aim);
  });
  if(scope || aux) return mergeOptic(scope, aux);
  return {id:false, mag:1, aimLevel:0, aimOk:false, reach:0, minR:0, near:FS};
}

function opticAAPercent(w, aim){
  let pct=null, unlock=0;
  (w.opticComps||[]).forEach(c => {
    if(hasFx(c,"IncreaseAimAccuracy15Percent")) return;
    if(c.p && c.p.AimAccuracyPercent!=null){
      pct = c.p.AimAccuracyPercent;
      if(hasFx(c,"ScopeMagnification")) unlock = pget(c,"AimAccuracyAimLevel", pget(c,"ScopeAimLevel",0));
      else if(hasFx(c,"MinAim")) unlock = pget(c,"AimAccuracyAimLevel",1);
      else unlock = pget(c,"AimAccuracyAimLevel",0);
    }
  });
  if(pct==null) return {pct:100, active:false};
  const active = (aim||0) >= unlock;
  return {pct: active?pct:100, active, unlock, raw:pct};
}

function shooterCore(dex, mrk, lvl, aim, w){
  const snapRaw = (dex*4 + mrk + lvl*5)/6;
  const precRaw = (mrk*4 + dex + lvl*5)/6;
  const snap = skillCurve(snapRaw);
  const prec = skillCurve(precRaw);
  const maxAim = Math.max(0, w.maxAim);
  const aimC = clamp(aim, 0, maxAim);
  const prog = maxAim ? clamp(aimC/maxAim,0,1) : 0;
  const shotSkill = snap + prog * Math.max(prec-snap,0);
  const mastery = aimMastery(mrk);
  const aaInfo = opticAAPercent(w, aimC);
  const aa = w.aa * aaInfo.pct / 100;
  const gain = Math.max(0,aimC) * aa * mastery / 100;
  const uncapped = shotSkill + gain;
  return {snapRaw, precRaw, snap, prec, precision:prec, shotSkill, mastery, aa, aaInfo, gain, prog, maxAim, aimC, uncapped, core: clamp(uncapped,0,100)};
}

function rangeProfile(w, d, aim){
  const R = w.r;
  const tiles = Math.max(0, d);
  if(!R || tiles>=R) return {possible:false, factor:0, E:0, rf:0, closeF:FS, opticF:FS, unaided:0, optic:opticProfile(w,aim), power:0, falloffEnd:R};
  const BDR = clamp(w.bdr, 0, R);
  const G = w.g||50;
  const prog = w.maxAim ? clamp(aim/w.maxAim,0,1) : 0;
  const optic = opticProfile(w, aim);
  const eps = 0.01;
  let E = Math.min(R-eps, BDR + optic.reach * prog);
  E = clamp(E, 0, R-eps);
  const power = Math.max(1.25, BDR*0.05 + G/100);
  const isMg = w.mg || w.lmg;
  const fallEnd = (from) => isMg ? Math.min(R, from+MG_SPAN) : R;
  const falloffEnd = fallEnd(E);
  const falloff = t => roundH(FLOOR + (FS-FLOOR)*(1 - Math.pow(t, power)));
  let factor;
  if(tiles<=E) factor = FS;
  else {
    const t = clamp((tiles-E)/Math.max(falloffEnd-E,eps),0,1);
    factor = falloff(t);
  }
  let unaided = factor;
  if(optic.id && optic.reach>0){
    const uE = Math.min(R-eps, BDR);
    if(tiles<=uE) unaided = FS;
    else {
      const uEnd = fallEnd(uE);
      const t = clamp((tiles-uE)/Math.max(uEnd-uE,eps),0,1);
      unaided = falloff(t);
    }
  }
  let opticF = FS;
  if(optic.id && optic.minR>0 && tiles<optic.minR){
    const prox = clamp((optic.minR-tiles)/optic.minR,0,1);
    opticF = roundH(FS + (optic.near-FS)*prox);
  }
  let closeF = FS;
  if(w.close>0 && tiles<w.close){
    const f0 = roundH(w.closeF*10);
    const prox = clamp((w.close-tiles)/w.close,0,1);
    closeF = roundH(FS + (f0-FS)*prox);
  }
  return {possible:true, factor, E, rf:factor/FS, closeF, opticF, unaided, optic, power, falloffEnd, BDR};
}

function visPenalty(d, sightTiles, vis, w, aim){
  if(vis==="off") return {apply:false, value:0};
  if(d < 3) return {apply:false, value:0};
  if(vis==="spotter") return {apply:true, value:-10, name:t("fSpotter")};
  if(vis==="blind") return {apply:true, value:-60, name:t("fBlind")};
  if(vis==="nolos") return {apply:true, value:-50, name:t("fNoLos")};
  let dist = d;
  const night = vis==="night" || vis==="nightNV";
  const lit = vis==="nightLit";
  const flashlight = w.ignoreDark && d<15;
  const nvFull = w.nvFull && w.maxAim && aim>=w.maxAim;
  if(night && !lit && !flashlight && !nvFull) dist *= 1.6;
  if(vis==="heat") dist *= 0.9;
  if(vis==="rain") dist *= 1.1;
  if(vis==="fog") dist *= 1.3;
  if(vis==="storm") dist *= 1.5;
  const sight = Math.max(1,(sightTiles||46)*SLAB);
  const cth = mulDivRound(35, SLAB*100, sight);
  const optic = opticProfile(w, aim);
  const fullyLit = !night || lit || flashlight || nvFull;
  if(fullyLit && optic.id && optic.aimOk && optic.mag>1){
    const calc = (optic.mag*10) * 1.5/2;
    const v = -mulDivRound(dist, cth, 10*calc);
    return {apply:true, value:v, name:t("fVisOptic", {mag:optic.mag})};
  }
  let iron = -mulDivRound(dist, cth, 100);
  if(night && (flashlight||lit||nvFull)) return {apply:true, value:iron, name:t("fVisLit")};
  if(vis==="nightNV"){ iron = Math.floor(iron*1.3); return {apply:true, value:iron, name:t("fVisNV")}; }
  if(night) return {apply:true, value:iron, name:t("fVisNight")};
  return {apply:true, value:iron, name:t("fVis")};
}

function coverValue(kind, dust){
  const COVER=-45, EXPOSED=-12, CROUCH=-12, PRONE=-23;
  if(kind==="open") return {v:0, name:null};
  if(kind==="crouch") return {v:CROUCH, name:t("fTgtCrouch")};
  if(kind==="prone") return {v:PRONE, name:t("fTgtProne")};
  let full=COVER, exp=EXPOSED, name=t("fCover");
  if(dust){ full+=-40; exp+=-40; name=t("fCoverDust"); }
  if(kind==="exposed") return {v:exp, name:name+t("fWeak")};
  if(kind==="full") return {v:full, name:name+t("fFull")};
  if(kind==="half") return {v:roundH((full+exp)/2), name:name+t("fHalf")};
  return {v:0, name:null};
}

function laserValue(w, d, vis){
  const L = w.laser;
  if(!L || !L.cth) return null;
  const night = vis==="night"||vis==="nightNV"||vis==="nightLit";
  if(L.nightOnly && !(night||vis==="nolos")) return null;
  if(d > L.dist) return null;
  if(d <= L.full) return {v:L.cth, name:t("fLaser")};
  const span = Math.max(1, L.dist-L.full);
  const fall = mulDivRound(d-L.full, 1000, span);
  const scaled = Math.max(1, mulDivRound(L.cth, 1000 - mulDivRound(600,fall,1000), 1000));
  return {v:scaled, name:t("fLaserFall")};
}

function oaValue(dex, mrk, lvl, bonus){
  const maxP=-30, minP=0;
  return maxP + mulDivRound(minP-maxP, dex+mrk+lvl*5, 100) + (bonus||0);
}

function applyFactors(core, factors, possible){
  if(!possible) return {final:0, before:0, product:0};
  const capped = clamp(core,0,100);
  const sorted = factors.slice().sort((a,b)=> (a.id<b.id?-1:a.id>b.id?1:0));
  let product = 1.0;
  let diag = capped;
  sorted.forEach(f => {
    f.before = diag;
    product *= f.factor / FS;
    diag = diag * f.factor / FS;
    f.after = diag;
  });
  const before = capped * product;
  return {final: clamp(roundH(before), 2, 100), before, product, factors:sorted};
}

function combatAdds(ctx){
  const adds = [];
  const cov = coverValue(ctx.cover, ctx.dust);
  if(cov.v) adds.push({id:"Cover", name:cov.name, value:cov.v});
  const vis = visPenalty(ctx.d, ctx.sight, ctx.vis, ctx.w, ctx.aim);
  if(vis.apply && vis.value) adds.push({id:"Distance", name:vis.name, value:vis.value});
  if(+ctx.supp) adds.push({id:"Suppression", name:t("fSupp"), value:+ctx.supp});
  if(ctx.pain) adds.push({id:"Pain", name:t("fPain", {n:ctx.pain}), value:-5*ctx.pain});
  if(+ctx.conc) adds.push({id:"Concussion", name:t("fConc"), value:+ctx.conc});
  if(+ctx.tarms) adds.push({id:"TraumaArms", name:t("fArms"), value:+ctx.tarms});
  if(+ctx.thead) adds.push({id:"TraumaHead", name:t("fHead"), value:+ctx.thead});
  if(ctx.drunk) adds.push({id:"Drunk", name:t("fDrunk", {n:ctx.drunk}), value:-15*ctx.drunk});
  if(ctx.morale) adds.push({id:"Morale", name:t("fMorale"), value:ctx.morale*3});
  if(ctx.tracers) adds.push({id:"MarkedTraccers", name:t("fTracers"), value:5*ctx.tracers});
  if(ctx.extra) adds.push({id:"Extra", name:t("fExtra"), value:+ctx.extra});
  if(ctx.oa) adds.push({id:"OpportunityAttack", name:"Opportunity Attack", value:oaValue(ctx.dex,ctx.mrk,ctx.lvl,ctx.w.oaBonus)});
  const night = ctx.vis==="night"||ctx.vis==="nightNV"||ctx.vis==="nightLit";
  if(ctx.w.nightIrons && night) adds.push({id:"NightsIronsBonus", name:t("fNightIrons"), value:ctx.w.nightIrons});
  const las = laserValue(ctx.w, ctx.d, ctx.vis);
  if(las) adds.push({id:"Laser", name:las.name, value:las.v});
  if(ctx.w.bonusCth) adds.push({id:"Component", name:t("fComp"), value:ctx.w.bonusCth});
  if(ctx.w.pistol && ctx.d<10) adds.push({id:"WeaponPistol_PointBlank", name:t("fPistol"), value:mulDivRound(20,11-ctx.d,10)});
  if((ctx.w.mg||ctx.w.lmg) && !ctx.supported){
    const base = ctx.w.mg && !ctx.w.lmg ? -50 : -25;
    const pen = mulDivRound(base, Math.max(0,100-ctx.str), 100);
    if(pen) adds.push({id:"UnsupportedMG", name:t("fUnsup"), value:pen});
  }
  return adds;
}

function shot(base, sel, env){
  const w = resolveWeapon(base, sel);
  let aim = env.aim;
  if(w.minAim && aim<1) aim = 1;
  aim = clamp(aim, 0, w.maxAim);
  const sk = shooterCore(env.dex, env.mrk, env.lvl, aim, w);
  const rp = rangeProfile(w, env.d, aim);
  const coreAfterRange = sk.core * (rp.factor/FS);
  const factors = [];
  if(rp.closeF !== FS) factors.push({id:"WeaponCloseRange", name:t("fCloseW"), factor:rp.closeF});
  if(rp.opticF !== FS) factors.push({id:"OpticNearRange", name:t("fCloseO"), factor:rp.opticF});
  const ctx = Object.assign({w, aim}, env);
  combatAdds(ctx).forEach(a => {
    if(!a.value) return;
    factors.push({id:a.id, name:a.name, factor:pctToFactor(a.value), ui:a.value});
  });
  const applied = applyFactors(coreAfterRange, factors, rp.possible);
  const overflow = Math.max(0, roundH(sk.uncapped)-100);
  const missCap = env.d<8 ? 50 - mulDivRound(25, env.d, 8) : 25;
  const missGraze = rp.possible ? Math.min(missCap, Math.floor(missCap * Math.pow((100-applied.final)/100,2))) : 0;
  let coverGraze = 0;
  const cov = coverValue(env.cover, env.dust);
  if(cov.v && cov.v < -12) coverGraze = clamp(roundH((-cov.v)*100/45),0,100);
  return {w, aim, sk, rp, coreAfterRange, applied, overflow, missGraze, coverGraze, factors};
}

function colorFor(v){
  if(v<=0) return "var(--muted)";
  if(v>=75) return "var(--good)";
  if(v>=45) return "var(--accent)";
  if(v>=20) return "var(--warn)";
  return "var(--bad)";
}
function pillFam(f){
  if(!f||f==="irons") return "irons";
  if(f.startsWith("reflex")) return "reflex";
  if(f==="combat") return "combat";
  if(f==="long") return "long";
  if(f==="night") return "night";
  return "irons";
}

let selectedId = "DragunovSVD";
let sel = {};

function weaponById(id){ return DATA.weapons.find(w=>w.id===id) || DATA.weapons[0]; }

function fillSelect(el, options, emptyLabel){
  el.innerHTML = "";
  if(emptyLabel!=null){
    const o=document.createElement("option"); o.value=""; o.textContent=emptyLabel; el.appendChild(o);
  }
  options.forEach(opt => {
    const o=document.createElement("option");
    o.value = opt.id;
    o.textContent = opt.name;
    el.appendChild(o);
  });
}

function slotOptions(wid, slot){
  const ids = (DATA.slots[wid]&&DATA.slots[wid][slot]) || [];
  return ids.map(id => DATA.comps[id]).filter(Boolean);
}

function syncSlots(){
  const w = weaponById(selectedId);
  const empty = DATA.emptyable[w.id]||{};
  const def = DATA.defaults[w.id]||{};
  const setSlot = (el, slot, emptyLab) => {
    const opts = slotOptions(w.id, slot);
    const canEmpty = empty[slot] || !opts.length;
    fillSelect(el, opts, canEmpty ? emptyLab : null);
    const prefer = sel[slot] && opts.some(o=>o.id===sel[slot]) ? sel[slot] : (def[slot]||"");
    if(!canEmpty && !prefer && opts[0]) el.value = opts[0].id;
    else el.value = prefer || "";
    sel[slot] = el.value || "";
    el.closest(".field").classList.toggle("hidden", !opts.length && slot!=="Scope");
  };
  setSlot($("scope"), "Scope", t("emptyIrons"));
  setSlot($("barrel"), "Barrel", t("emptyBase"));
  setSlot($("stock"), "Stock", t("emptyNone"));
  const grips = slotOptions(w.id,"Handgrip").concat(slotOptions(w.id,"Handguard"));
  fillSelect($("grip"), grips, t("none"));
  const gPref = sel.Handgrip || sel.Handguard || "";
  $("grip").value = grips.some(g=>g.id===gPref) ? gPref : "";
  setSlot($("mag"), "Magazine", t("factory"));
  const sides = slotOptions(w.id,"Side").concat(slotOptions(w.id,"Muzzle")).concat(slotOptions(w.id,"Bipod")).concat(slotOptions(w.id,"Under"));
  fillSelect($("side"), sides, t("none"));
  const sPref = sel.Side || sel.Muzzle || sel.Bipod || sel.Under || "";
  $("side").value = sides.some(s=>s.id===sPref) ? sPref : "";
}

function readSel(){
  sel = {
    Scope: $("scope").value,
    Barrel: $("barrel").value,
    Stock: $("stock").value,
    Handgrip: "",
    Handguard: "",
    Magazine: $("mag").value,
    Side: "",
    Muzzle: "",
    Bipod: "",
    Under: ""
  };
  const g = $("grip").value;
  if(g && DATA.comps[g]){
    if(DATA.comps[g].slot==="Handguard") sel.Handguard=g; else sel.Handgrip=g;
  }
  const s = $("side").value;
  if(s && DATA.comps[s]) sel[DATA.comps[s].slot] = s;
  return sel;
}

function envFromUI(){
  return {
    dex:+$("dex").value, mrk:+$("mrk").value, lvl:+$("lvl").value, str:+$("str").value,
    aim:+$("aim").value, d:+$("dist").value,
    cover:$("cover").value, dust:$("dust").checked, vis:$("vis").value, sight:+$("sight").value||46,
    supp:$("supp").value, pain:+$("pain").value||0, conc:$("conc").value,
    tarms:$("tarms").value, thead:$("thead").value, drunk:+$("drunk").value||0,
    morale:+$("morale").value||0, tracers:+$("tracers").value||0, extra:+$("extra").value||0,
    oa:$("oa").checked, supported:$("supported").checked, stance:$("stance").value, autoW:$("autoW").checked
  };
}

function aimForMode(mode, w){
  const envAim = +$("aim").value;
  if(mode==="current") return w.minAim ? Math.max(1, envAim) : envAim;
  if(mode==="snap") return w.minAim ? 1 : 0;
  if(mode==="plus1") return Math.min(w.maxAim, (w.minAim?1:0)+1);
  return w.maxAim;
}

function renderList(){
  const fam = $("fam").value;
  const q = $("q").value.trim().toLowerCase();
  const box = $("wlist");
  box.innerHTML = "";
  DATA.weapons.filter(w => {
    if(fam && w.fam!==fam) return false;
    if(q && !(w.id.toLowerCase().includes(q) || w.name.toLowerCase().includes(q))) return false;
    return true;
  }).forEach(w => {
    const div = document.createElement("div");
    div.className = "item"+(w.id===selectedId?" on":"");
    div.innerHTML = '<div><div class="n">'+w.name+'</div><div class="s">'+w.id+' · '+famName(w.fam)+' '+w.tier+'</div></div><div class="m">AA'+w.aa+' R'+w.r+'</div>';
    div.onclick = () => {
      selectedId=w.id; sel={}; syncSlots();
      const wr = resolveWeapon(w, readSel());
      $("aim").max = Math.max(1, wr.maxAim);
      $("aim").value = wr.maxAim;
      $("dist").max = Math.max(20, wr.r);
      if(+$("dist").value >= wr.r) $("dist").value = Math.max(0, wr.r-1);
      renderList(); render();
    };
    box.appendChild(div);
  });
}

function fmtPct(v){ return (v>0?"+":"")+v; }

function render(){
  ["dex","mrk","lvl","str","aim","dist"].forEach(id => $(id+"V").textContent = $(id).value);
  const base = weaponById(selectedId);
  readSel();
  const env = envFromUI();
  const r = shot(base, sel, env);
  $("aim").max = Math.max(1, r.w.maxAim);
  if(+ $("aim").value > r.w.maxAim) $("aim").value = r.w.maxAim;
  const final = r.applied.final;
  let cls = "big";
  if(final>=75) cls+=" good"; else if(final>=45) cls+=" mid"; else if(final>0) cls+=" bad";
  $("hero").innerHTML = [
    ["CTH", final+"%", cls],
    [t("heroCore"), roundH(r.sk.uncapped)+"%", ""],
    [t("heroAfterRange"), roundH(r.coreAfterRange)+"%", ""],
    [t("heroOverflow"), r.overflow, ""],
    [t("heroE"), roundH(r.rp.E)+" / "+r.w.bdr+" / "+r.w.r, ""],
    [t("heroAim"), r.aim+" / "+r.w.maxAim, ""],
    [t("heroAA"), r.sk.aa.toFixed(1), ""],
    [t("heroMiss"), r.missGraze+"%", ""],
    [t("heroCoverG"), r.coverGraze+"%", ""]
  ].map(x => '<div class="stat '+x[2]+'"><b>'+x[1]+'</b><span>'+x[0]+'</span></div>').join("");

  const op = r.rp.optic;
  const aa = r.sk.aaInfo;
  $("opticMeta").innerHTML =
    (sel.Scope && DATA.comps[sel.Scope] ? '<span class="pill '+pillFam(DATA.comps[sel.Scope].fam)+'">'+(DATA.comps[sel.Scope].fam||"scope")+'</span> ' : '<span class="pill irons">irons</span> ')+
    'mag '+op.mag+' · unlock aim '+op.aimLevel+' · reach '+(op.reach||0)+
    ' · near '+(op.minR||0)+'@'+roundH(op.near/10)+'%'+
    (aa.raw? ' · AA% '+aa.raw+(aa.active? t("aaOn"): t("aaWait", {n:aa.unlock})) : '')+
    '<br>'+t("wpnClose")+' '+r.w.close+' @ '+r.w.closeF+'% · Grouping '+r.w.g+' · Recoil '+r.w.recoil;

  $("aimNote").textContent = r.w.minAim
    ? t("aimNoteMin", {n:r.w.maxAim})
    : t("aimNote", {n:r.w.maxAim});

  const rows = [];
  rows.push([t("rowSnap"), roundH(r.sk.snap)+"%", t("metaDex")]);
  rows.push([t("rowPrec"), roundH(r.sk.prec)+"%", t("metaMark")]);
  rows.push([t("rowGain"), "+"+roundH(r.sk.gain), t("metaGain", {n:r.sk.mastery})]);
  rows.push([t("rowCore"), roundH(r.sk.uncapped)+"%", r.overflow? t("metaOverflow", {n:r.overflow}) : t("metaCap")]);
  rows.push([t("rowRange"), factorToPct(r.rp.factor)>0? "+"+factorToPct(r.rp.factor): factorToPct(r.rp.factor), r.rp.possible? ("E="+r.rp.E.toFixed(1)+" p="+r.rp.power.toFixed(2)): t("metaOor")]);
  (r.applied.factors||[]).forEach(f => {
    const ui = f.ui!=null ? f.ui : factorToPct(f.factor);
    rows.push([f.name, fmtPct(ui), "×"+(f.factor/FS).toFixed(3)+"  "+roundH(f.before)+"→"+roundH(f.after)]);
  });
  $("brk").innerHTML = rows.map(x => '<tr><td class="l">'+x[0]+'</td><td class="mono">'+x[1]+'</td><td class="l">'+x[2]+'</td></tr>').join("");

  const rec = recoilLine(r, env);
  $("post").textContent = rec;

  renderCompare(base, env);
  drawChart(base, env);
}

function recoilLine(r, env){
  if(!(r.w.burst||r.w.auto) && r.applied.final<=0) return "";
  const strength = clamp(env.str,0,100), mark=clamp(env.mrk,0,100);
  const sf = clamp(1.25 - strength/200, 0.75, 1.25);
  const mf = clamp(1.25 - mark/200, 0.75, 1.25);
  const shooter = 0.5*sf+0.5*mf;
  const stance = env.stance==="Prone"?0.75: env.stance==="Crouch"?0.90:1;
  let support = 1, prot = 0;
  if(env.supported || (env.stance==="Prone" && r.w.bipodShots)){ support=0.65; prot += r.w.bipodShots; }
  const perk = env.autoW ? 0.85 : 1;
  let cls = 1;
  if((r.w.mg||r.w.lmg) && !env.supported && !(env.stance==="Prone" && r.w.bipodShots))
    cls = r.w.lmg ? 1.5 : 2.0;
  const er = r.w.recoil * shooter * stance * support * perk * cls;
  const ret = clamp(1 - er/100, 0.15, 1);
  const n = Math.max(r.w.burst||0, Math.min(r.w.auto||0, 8), 1);
  const bullets = [];
  for(let i=1;i<=n;i++){
    const exp = Math.max(0, i-1-prot);
    const ch = i===1 || exp===0 ? r.applied.final : clamp(roundH(r.applied.final * Math.pow(ret, exp)), 2, 100);
    if(!r.rp.possible) bullets.push(0); else bullets.push(ch);
  }
  return t("queue", {er:er.toFixed(1), ret:(ret*100).toFixed(0), shots:bullets.map((b,i)=>t("shotN",{n:i+1})+" "+b+"%").join(" · ")});
}

function compareList(wid){
  const fit = new Set(((DATA.slots[wid]||{}).Scope)||[]);
  const only = $("onlyFit").checked;
  const rows = [];
  DATA.archetypes.forEach(a => {
    if(a.id && !DATA.comps[a.id]) return;
    if(only && a.id && !fit.has(a.id)) return;
    rows.push({id:a.id, label:archLabel(a), fam:a.family, tier:a.tier, onGun:!a.id || fit.has(a.id)});
  });
  if(!only){
    Object.values(DATA.comps).forEach(c => {
      if(c.slot!=="Scope") return;
      if(rows.some(r=>r.id===c.id)) return;
      rows.push({id:c.id, label:c.name, fam:c.fam||"other", tier:"", onGun:fit.has(c.id)});
    });
  }
  return rows;
}

function renderCompare(base, env){
  const mode = $("cmpAim").value;
  const useCombat = $("withCombat").checked;
  const env0 = Object.assign({}, env);
  if(!useCombat){
    env0.cover="open"; env0.dust=false; env0.vis="day"; env0.supp="0";
    env0.pain=0; env0.conc="0"; env0.tarms="0"; env0.thead="0"; env0.drunk=0;
    env0.morale=0; env0.tracers=0; env0.extra=0; env0.oa=false;
  }
  $("cmpHead").innerHTML = "<tr><th class='l'>"+t("cmpScope")+"</th><th class='l'>"+t("cmpFam")+"</th><th>Aim</th><th>AA</th><th>E</th><th>Near</th>"+CMP_D.map(d=>"<th>@"+d+"</th>").join("")+"<th>Δ@"+env.d+"</th></tr>";
  const ironSel = Object.assign({}, sel, {Scope:""});
  const ironW = resolveWeapon(base, ironSel);
  const ironAim = aimForMode(mode, ironW);
  const ironAt = {};
  CMP_D.concat([env.d]).forEach(d => {
    const e = Object.assign({}, env0, {d, aim:ironAim});
    ironAt[d] = shot(base, ironSel, e).applied.final;
  });
  const tb = $("cmpBody");
  tb.innerHTML = "";
  compareList(base.id).forEach(row => {
    const s = Object.assign({}, sel, {Scope: row.id||""});
    const wr = resolveWeapon(base, s);
    const aim = aimForMode(mode, wr);
    const vals = CMP_D.map(d => shot(base, s, Object.assign({}, env0, {d, aim})).applied.final);
    const here = shot(base, s, Object.assign({}, env0, {d:env.d, aim}));
    const tr = document.createElement("tr");
    if((row.id||"") === (sel.Scope||"")) tr.className = "sel";
    if(row.onGun) tr.classList.add("fit");
    const near = here.rp.optic.minR ? here.rp.optic.minR+"@"+roundH(here.rp.optic.near/10)+"%" : "—";
    const aa = here.sk.aaInfo;
    const aaTxt = aa.raw ? (aa.active? aa.raw+"%" : "("+aa.raw+"%)") : "—";
    tr.innerHTML = '<td class="l">'+row.label+'</td><td class="l"><span class="pill '+pillFam(row.fam)+'">'+(row.fam||"—")+'</span> '+row.tier+'</td><td class="mono">'+aim+'/'+wr.maxAim+'</td><td class="mono">'+aaTxt+'</td><td class="mono">'+here.rp.E.toFixed(1)+'</td><td class="mono">'+near+'</td>'+
      vals.map(v => '<td class="cell" style="color:'+colorFor(v)+'">'+v+'</td>').join("")+
      '<td class="mono">'+(here.applied.final - ironAt[env.d]>=0?"+":"")+(here.applied.final - ironAt[env.d])+'</td>';
    tr.onclick = () => { $("scope").value = row.id||""; render(); };
    tb.appendChild(tr);
  });
}

function drawChart(base, env){
  const c = $("chart"); const ctx=c.getContext("2d");
  const W=c.width, H=c.height;
  ctx.clearRect(0,0,W,H);
  const pad={l:36,r:12,t:12,b:28};
  const pw=W-pad.l-pad.r, ph=H-pad.t-pad.b;
  const R = resolveWeapon(base, sel).r;
  const maxD = Math.min(Math.max(R, 20), 80);
  const xs = [];
  for(let d=0; d<=maxD; d++) xs.push(d);
  const series = [
    {sel: Object.assign({}, sel, {Scope:""}), col:"#6b7280", name:"irons"},
    {sel: sel, col:"#c4a35a", name:"selected"}
  ];
  ctx.strokeStyle="#3a3f4a"; ctx.fillStyle="#9aa0a6"; ctx.font="11px sans-serif";
  for(let p=0;p<=100;p+=25){
    const y=pad.t+ph*(1-p/100);
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(W-pad.r,y); ctx.stroke();
    ctx.fillText(String(p),4,y+3);
  }
  [0,10,20,30,40,50,60].filter(d=>d<=maxD).forEach(d=>{
    const x=pad.l+(d/maxD)*pw; ctx.fillText(String(d), x-6, H-8);
  });
  series.forEach(s => {
    ctx.beginPath(); ctx.strokeStyle=s.col; ctx.lineWidth = s.name==="selected"?2:1;
    xs.forEach((d,i) => {
      const e = Object.assign({}, env, {d});
      const v = shot(base, s.sel, e).applied.final;
      const x=pad.l+(d/maxD)*pw, y=pad.t+ph*(1-v/100);
      if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
    });
    ctx.stroke();
  });
  const cur = pad.l+(env.d/maxD)*pw;
  ctx.strokeStyle="#e8eaed55"; ctx.beginPath(); ctx.moveTo(cur,pad.t); ctx.lineTo(cur,pad.t+ph); ctx.stroke();
  const Er = shot(base, sel, env).rp.E;
  const ex = pad.l+(Er/maxD)*pw;
  ctx.setLineDash([4,4]); ctx.strokeStyle="#c4a35a88"; ctx.beginPath(); ctx.moveTo(ex,pad.t); ctx.lineTo(ex,pad.t+ph); ctx.stroke();
  ctx.setLineDash([]);
}

function initFam(){
  const fams = [...new Set(DATA.weapons.map(w=>w.fam))];
  $("fam").innerHTML = '<option value="">'+t("all")+'</option>'+fams.map(f=>{
    return '<option value="'+f+'">'+famName(f)+'</option>';
  }).join("");
}

function bind(){
  ["fam"].forEach(id => $(id).addEventListener("change", ()=>{ renderList(); }));
  $("q").addEventListener("input", renderList);
  ["dex","mrk","lvl","str","aim","dist","cover","dust","vis","sight","supp","pain","conc","tarms","thead","drunk","morale","tracers","extra","oa","supported","stance","autoW","scope","barrel","stock","grip","mag","side","cmpAim","onlyFit","withCombat"]
    .forEach(id => { const el=$(id); if(!el) return; el.addEventListener("input", render); el.addEventListener("change", render); });
  document.querySelectorAll("[data-aim]").forEach(btn => {
    btn.addEventListener("click", () => {
      const w = resolveWeapon(weaponById(selectedId), readSel());
      $("aim").value = aimForMode(btn.getAttribute("data-aim"), w);
      render();
    });
  });
  document.querySelectorAll(".lang button").forEach(b => {
    b.addEventListener("click", () => setLang(b.getAttribute("data-lang")));
  });
}

applyStaticI18n();
initFam();
if(!DATA.weapons.some(w=>w.id===selectedId)) selectedId = DATA.weapons[0].id;
syncSlots();
bind();
renderList();
render();
</script>
</body>
</html>
"""


def main() -> int:
    if not JSON.is_file():
        subprocess.check_call([sys.executable, str(EXPORT)])
    data = JSON.read_text(encoding="utf-8")
    html = HTML.replace("__DATA__", data)
    OUT.write_text(html, encoding="utf-8")
    print("Wrote", OUT, "bytes", OUT.stat().st_size)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
