---
id: JAZZ-MED-007
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
  - strategy-squads-sectors
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-MED-007.md
  - jazz/docs/specs/active/JAZZ-MED-006.md
  - jazz/docs/specs/active/JAZZ-COMBAT-008.md
  - jazz/Code/System_Medicine_MED006.lua
  - jazz/Code/System_Medicine_MED007.lua
  - jazz/Code/System_EnergyLadder.lua
  - jazz/Code/Systems_Medicine.lua
  - jazz/Code/SatelliteSquad.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/RussianManual.csv
  - jazz/items.lua
  - jazz/Localization/EnglishManual.csv
  - jazz/docs/design/medicine.md
  - jazz/docs/technical/systems/armor-damage-wounds-will.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/tools/_audit_med007_debt_fatigue.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - localization-id-allocation
related_decisions:
  - none
related_specs:
  - JAZZ-MED-001
  - JAZZ-MED-006
  - JAZZ-COMBAT-007
  - JAZZ-COMBAT-008
approved_by: project-owner
---

# JAZZ-MED-007: долг макс. ОЗ после боя; усталость от текущих ОЗ

Design thread (Discord 2026-08-17…20) + chat 2026-08-23: аптечка должна работать против нока **в этом бою**; травма — долг на глобалку. Владелец: отложенный долг (не Grit) **и** накопление travel-усталости от **текущего уровня ОЗ**, не от стата Health.

Меняет момент MaxHP debt из [JAZZ-MED-006](JAZZ-MED-006.md) и HP-ветку travel из [JAZZ-COMBAT-008](JAZZ-COMBAT-008.md) `REQ-003`. Тиры, stabilize, kit heal%, TreatWounds, Legs foot-slow — без пересмотра. **Ribs travel-mul COMBAT-008 REQ-002 снят** (owner 2026-08-23): рёбра не ускоряют Tired в пути.

Supersedes MED-006 non-goal «долг только после боя — отклонено».  
Supersedes COMBAT-008 `REQ-003` (`GetHPAdditionalTiredTime` всегда 0).  
Supersedes COMBAT-008 `REQ-002` (Ribs travel tiredness mul).

## Проблема

1. Долг 10/30/60% режет потолок **сразу** и клампит ОЗ. После пули −15 и средней травмы мерк 80→**56/56**; кит хилит 0. Боевая роль аптечки пропадает.
2. Grit на размер долга ломает `*shot` / trauma roll (`TempHitPoints > 0`).
3. Ванильный `GetHPAdditionalTiredTime(HitPoints)` сравнивает **абсолютные** ОЗ с `UnitTirednessTravelTimeHP` (**75**). MaxHP ≈ Health → высокий стат Health на полном баре устаёт медленнее. COMBAT-008 обнулил мод целиком. Нужен **уровень** (доля живого пула), не стат.

## Цели

- В тактическом бою потолок без trauma debt; кит хилит `%` MED-006 от полного MaxHP.
- На `CombatEnd` долг наступает, ОЗ клампятся.
- Вне боя долг сразу.
- Тултип в бою: долг **после боя**; вне боя — уже применён.
- Travel-усталость от **текущих ОЗ** (`HitPoints`) против порога **100**. Стат Health не читается. Health 90 при 50 ОЗ = Health 50 при 50 ОЗ. На полном баре 90 ≠ 50.

## Non-goals

- Менять kit heal%, gates, stabilize, Pain/bleed, TreatWounds, Legs foot-slow таблицу.
- CombatStart grit 25% (MED-001).
- Hospital instant Trauma clear.
- Новые Trauma* ID / CE «долг».
- Перк-Grit как носитель долга.

## Модель

### Долг макс. ОЗ

`JazzTraumaMaxHpDebtPercent` без изменений. Wrap `RecalcMaxHitPoints` **не** вычитает долг, если у `session_id` есть живой `g_Units[id]` и активен `g_Combat` (кроме force-path).

На `CombatStart` — recalc участников (потолок поднимается до базы, текущие ОЗ не растут).  
На `CombatEnd` — force-recalc с долгом и кламп.

Вне боя / чужой сектор / exploration: долг сразу.

Пример (Health 80, Medical 100, Medium kit 60%):

| Момент | Max | HP | Medium kit |
| --- | ---: | ---: | --- |
| Пуля −15 + средняя травма, бой | 80 | 65 | +48 → 80/80 |
| `CombatEnd` | 56 | 56 | — |
| Сателлит без боя, та же травма | 56 | кламп | — |

### Усталость в пути

Ваниль: `diff = Clamp(HitPoints - 75, -50, 25)`.

JAZZ (owner 2026-08-23: **порог 100 ОЗ**, вход = текущие `HitPoints`, не стат Health, не % бара):

```text
diff      = Clamp(HitPoints - 100, -50, 25)
threshold = UnitTirednessTravelTime * (100+diff)/100
```

| Состояние | HitPoints | diff | Смысл |
| --- | ---: | ---: | --- |
| Health 100, 100/100 | 100 | **0** | порог |
| Health 90, 90/90 | 90 | −10 | полный бар крепче Health 50 |
| Health 50, 50/50 | 50 | −50 | полный бар, но мало ОЗ |
| Health 90, 50/90 | 50 | −50 | **как** Health 50 @ 50 |

Ribs **не** множат порог (COMBAT-008 REQ-002 superseded). `GetHPAdditionalTiredTime` остаётся 0 (мод живёт в `JazzGetTirednessTravelThreshold`, иначе double-apply).

## Требования

- `JAZZ-MED-007-REQ-001` — Пока живой `g_Units[session_id]` в активном `g_Combat` и нет force-флага: `RecalcMaxHitPoints` не вычитает trauma debt.
- `JAZZ-MED-007-REQ-002` — Вне этого условия долг 10/30/60% и кламп — как MED-006. Stabilize долг не трогает.
- `JAZZ-MED-007-REQ-003` — `CombatStart`: recalc участников без долга. `CombatEnd`: force-recalc с долгом (даже если `g_Combat` ещё жив). Детерминированно.
- `JAZZ-MED-007-REQ-004` — `JazzCalcKitHealAmount` без второго max: `%` от актуального `MaxHitPoints` (в бою полный, после — урезанный).
- `JAZZ-MED-007-REQ-005` — Нет `ApplyTempHitPoints` на долг. `JazzTryRollTraumaFromBodyPart` гейтится только существующим перк/действие Grit.
- `JAZZ-MED-007-REQ-006` — Loc RU+EN: в бою T `890000000010293` («после боя −N%»); вне боя T `890000000010292` (текущий долг).
- `JAZZ-MED-007-REQ-007` — Docs: technical + wiki + showcase RU/EN; пометки MED-006 / COMBAT-008 superseded.
- `JAZZ-MED-007-REQ-008` — LoadGame: в бою без долга на MaxHP; без боя — с долгом.
- `JAZZ-MED-007-REQ-009` — Travel: `diff = Clamp(HitPoints - 100, -50, 25)`. Не `unit.Health`, не % бара. Health 90 @ 50 HP == Health 50 @ 50 HP. Ribs не множат порог.

## Инварианты и ограничения

- Публичные Trauma* / kit ID не меняются.
- Floor MaxHP **1** после долга.
- BloodLoss и порог тяжёлой травмы ≥50% в бою — от полного MaxHP.
- `TrueGrit` / KillingWind / Meat не трогать.
- Новых save-полей нет.
- Не выдавать CombatStart Temp HP.

## Acceptance criteria

- `JAZZ-MED-007-AC-001` — static: skip-debt когда `g_Combat` + live `g_Units`; force на CombatEnd; CombatStart recalc.
- `JAZZ-MED-007-AC-002` — static: нет ApplyTempHitPoints(долг); trauma roll по-прежнему `TempHitPoints > 0`.
- `JAZZ-MED-007-AC-003` — static: kit heal без второго max; loc 010292 / 010293.
- `JAZZ-MED-007-AC-004` — static: порог **100 ОЗ**; формула от `HitPoints` (не Health, не %); `GetHPAdditionalTiredTime` == 0.
- `JAZZ-MED-007-AC-005` — runtime: 80 max, HP 65, средняя травма в бою → Max 80; Medium kit Med 100 → 80; CombatEnd → 56/56.
- `JAZZ-MED-007-AC-006` — runtime: та же травма на сателлите → Max сразу 56.
- `JAZZ-MED-007-AC-007` — runtime: перк-Grit по-прежнему блокирует trauma roll; травма Temp HP не добавляет.
- `JAZZ-MED-007-AC-008` — docs: deferred debt + travel from current HitPoints vs 100; COMBAT-008 «HP always 0» superseded.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap Recalc, CombatStart/End, EnergyLadder threshold, trauma tooltip.
- Saves: mid-combat после патча — load recalc (полный max в бою).
- Network: twin Recalc на CombatEnd.
- Generated data: loc 010293 + metadata.code.
- Cross-package: нет jazz-units.
- Rollback: немедленный долг MED-006 + HP additional 0.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive: `metadata.lua`, localization ID 010293

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner (chat 2026-08-23: deferred, не Grit; усталость от **текущих HitPoints** vs **100**; Health 90@50 HP = Health 50@50; на полном баре 90 ≠ 50; рёбра без travel-Tired, только долг макс. ОЗ)
- Дата: 2026-08-23

## Evidence

- `JAZZ-MED-007-AC-001`: `PASS` (static) — `python docs/tools/_audit_med007_debt_fatigue.py`. `BLOCKED` (runtime).
- `JAZZ-MED-007-AC-002`: `PASS` (static) — MED007 has no ApplyTempHitPoints; trauma roll still TempHitPoints-gated.
- `JAZZ-MED-007-AC-003`: `PASS` (static) — kit heal unchanged; loc 010292 / 010293 RU+EN.
- `JAZZ-MED-007-AC-004`: `PASS` (static) — `HP_TIREDNESS_LIMIT = 100` on `HitPoints`; `GetHPAdditionalTiredTime` returns 0.
- `JAZZ-MED-007-AC-005`: `BLOCKED` (runtime)
- `JAZZ-MED-007-AC-006`: `BLOCKED` (runtime)
- `JAZZ-MED-007-AC-007`: `BLOCKED` (runtime)
- `JAZZ-MED-007-AC-008`: `PASS` (static) — technical / wiki / showcase RU/EN + COMBAT-008 superseded note.

## Documentation delta

- `docs/technical/systems/armor-damage-wounds-will.md` — момент долга; HP-level travel.
- `docs/technical/systems/file-coverage.md` — `System_Medicine_MED007.lua`.
- `docs/design/medicine.md` — анти-RPG: кит в бою, потолок после.
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN.
- `JAZZ-MED-006.md` / `JAZZ-COMBAT-008.md` — superseded notes.
