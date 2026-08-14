---
id: JAZZ-MED-005
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/Systems_Medicine.lua
  - Code/CombatAI.lua
  - InventoryItem/JAZZ_Bandage.lua
  - InventoryItem/JAZZ_Morphine.lua
  - items.lua
  - metadata.lua
  - Russian.csv
  - English.csv
  - docs/specs/active/JAZZ-MED-005.md
  - docs/specs/active/JAZZ-MED-001.md
  - docs/design/medicine.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/ai-awareness.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/tools/_audit_med005_field_ap.py
  - docs/tools/_apply_med005_field_ap_loc.py
  - docs/tools/README.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-MED-001
approved_by: project-owner
---

# JAZZ-MED-005: field bandage/morphine AP by Medical

Owner lock 2026-08-14: even Medical bands, no skill gate. Bandage **5/4/3/2/1** AP; morphine **3/2/1** AP.

## Проблема

`JazzBandage` и `JazzMorphine` стоят фиксированные **1 ОД** (`ActionPoints = 1000`) у всех. Врач и стрелок с Medical 5 перевязываются одинаково дёшево; навык медицины не читается на хотбаре полевой медицины.

## Цели

- Стоимость ОД полевого бинта и морфия зависит от Medical хилера (ровные пороги).
- Skill gate нет: любой может юзать предмет.
- HUD / `GetUIState` / AI reachable / `AISelectHealTarget` читают динамический `GetAPCost`, не статичный `ActionPoints`.

## Non-goals

- Порог Medical на сам предмет (бинты/морфий остаются без `JazzMedicineRequiredMedical`).
- Изменение стоимости kit `Bandage` (аптечка остаётся 2 ОД).
- Изменение эффекта бинта/морфия (стаки крови, Analgesia, DownedRally).
- Пересчёт ОД от Medical цели (пациента), только хилер.

## Требования

- `JAZZ-MED-005-REQ-001` — Field bandage (`JazzBandage`) AP by healer Medical (`>=`): **5** at 0–19, **4** at 20–39, **3** at 40–59, **2** at 60–79, **1** at 80–100. Shared helper; `GetAPCost` returns `ap * const.Scale.AP`.
- `JAZZ-MED-005-REQ-002` — Morphine (`JazzMorphine`) AP by healer Medical (`>=`): **3** at 0–39, **2** at 40–79, **1** at 80–100. Same helper family.
- `JAZZ-MED-005-REQ-003` — No Medical gate: missing item still hides the action; low Medical only raises AP. MED-001 “no skill required” stays; the “low AP for everyone” clause of `JAZZ-MED-001-REQ-003` is superseded by this spec.
- `JAZZ-MED-005-REQ-004` — `GetUIState` combat AP check uses `GetAPCost`, not `self.ActionPoints`. Ally reachability already calls `GetAPCost`.
- `JAZZ-MED-005-REQ-005` — `AISelectHealTarget` field-bandage affordance uses `JazzBandage:GetAPCost(unit)`, not `CombatActions.JazzBandage.ActionPoints`.
- `JAZZ-MED-005-REQ-006` — Player-facing copy (item hint + combat action description, RU+EN) states the AP ladder. Technical + wiki + showcase RU/EN match runtime.

## Инварианты и ограничения

- Public IDs `JazzBandage` / `JazzMorphine` / `JAZZ_Bandage` / `JAZZ_Morphine` unchanged.
- Kit `Bandage` AP and Medical kit gates (30/50/80) unchanged.
- Save/network: no new persisted fields; cost is computed from `unit.Medical`.
- `ActionPoints` preset field may remain 1000 as editor fallback; runtime source of truth is `GetAPCost`.

## Acceptance criteria

- `JAZZ-MED-005-AC-001` — static: helper thresholds match REQ-001/002; `JazzBandage`/`JazzMorphine` `GetAPCost` call the helper; `GetUIState` uses `GetAPCost`; CombatAI field cost uses `GetAPCost`; companion/`items.lua` hint parity (`_audit_med005_field_ap.py`).
- `JAZZ-MED-005-AC-002` — static: RU+EN loc for hint/description IDs; technical + wiki + showcase RU/EN describe the ladder.
- `JAZZ-MED-005-AC-003` — runtime/human: Medical 10 bandage costs 5 AP; Medical 40 morphine costs 2 AP; Medical 80 both cost 1 AP; HUD disables when remaining AP is below the ladder.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: CombatAction `GetAPCost` override only; vanilla kit Bandage untouched.
- Saves: none (derived from Medical).
- Network/determinism: same Medical → same cost.
- Generated data: `items.lua` CombatAction + InventoryItem hints.
- Cross-package references: none (`jazz` only).
- Rollback/recovery: revert helper + `GetAPCost` to `self.ActionPoints`.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: as frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`

## Решение владельца

- Статус: **approved**
- Кто подтвердил: project-owner («годно»; пороги 20/40/60/80 бинт и 40/80 морфий; затем «делай» + push)
- Дата: 2026-08-14

## Evidence

- `JAZZ-MED-005-AC-001`: `PASS` — static: `python docs/tools/_audit_med005_field_ap.py` (threshold table, helpers, GetAPCost/GetUIState, CombatAI GetAPCost, companion/`items.lua` parity).
- `JAZZ-MED-005-AC-002`: `PASS` — static: RU+EN loc IDs `890000000010013` / `010016` / `010028` / `010201`; technical + wiki + showcase RU/EN + design ladder.
- `JAZZ-MED-005-AC-003`: `BLOCKED` — runtime/human playtest of HUD AP vs Medical bands.

## Documentation delta

- `docs/technical/systems/armor-damage-wounds-will.md` — field bandage/morphine AP ladder + GetAPCost
- `docs/technical/systems/ai-awareness.md` — AI field AP from GetAPCost
- `docs/wiki/combat-and-accuracy.md` + showcase RU/EN — player-facing AP by Medical
- `docs/design/medicine.md` — replace “мало ОД” with the ladder
- `docs/specs/active/JAZZ-MED-001.md` — REQ-003 AP clause superseded by MED-005
- `docs/tools/_audit_med005_field_ap.py` / `_apply_med005_field_ap_loc.py` + README
