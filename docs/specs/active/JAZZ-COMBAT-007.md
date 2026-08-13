---
id: JAZZ-COMBAT-007
status: implemented
owner: project-owner
systems:
  - armor-damage-wounds-will
  - combat-cth-actions
  - strategy-squads-sectors
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/System_EnergyLadder.lua
  - Code/SatelliteSquad.lua
  - Code/CombatBadge_DeathRoll.lua
  - Code/Systems_Medicine.lua
  - CharacterEffect/Fit.lua
  - CharacterEffect/Winded.lua
  - CharacterEffect/Fatigued.lua
  - CharacterEffect/Tired.lua
  - CharacterEffect/Exhausted.lua
  - CharacterEffect/WellRested.lua
  - CharacterEffect/FreeMove.lua
  - Icons/StatusEffects/Fit.png
  - Icons/StatusEffects/Winded.png
  - Icons/StatusEffects/Fatigued.png
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - docs/specs/active/JAZZ-COMBAT-007.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/technical/systems/file-coverage.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
  - docs/tools/_apply_combat_007_energy_items.py
  - docs/tools/README.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-007: Energy ladder (Fit → Exhausted)

## Проблема

Ванильный Tired разом забирает Free Move и −1 ОД; `FreeMove` не выдаётся при `Tiredness > 0`. Travel-метр почти невидимый — сектор→сектор и отряд внезапно слабо боеспособен.

## Цели

- Лестница энергии −1…4 с плавным FM и предсказуемым travel.
- Fit/WellRested: ОД-бафф + FM×120%; отдельно opening FM на первые 1 / 3 хода боя.
- Варны 50%/20% + лог смены ступени; travel/rest const под длину лестницы.

## Non-goals

- UI-метр TravelTime на карте; AI directive fatigue; второй positive CE ниже WellRested.

## Требования

- `JAZZ-COMBAT-007-REQ-001` — Шкала: `utWellRested=-1`, `utNormal=0`→CE `Fit`, `utWinded=1`, `utFatigued=2`, `utTired=3`, `utExhausted=4`. Unconscious не на лестнице. `SetTired` clamp −1…4; при 0 вешает `Fit`.
- `JAZZ-COMBAT-007-REQ-002` — Таблица: WellRested +2 AP / FM×120% / opening 3 хода; Fit +1 AP / FM×120% / opening 1 ход; Winded 0/100%; Fatigued 0/75%; Tired −1/50%; Exhausted −2 AP + FM0 + travel stop. Opening: `data.add += opening_fm_bonus` (default 2) при `g_Combat.current_turn` в окне.
- `JAZZ-COMBAT-007-REQ-003` — `FreeMove` Condition: `Tiredness < utExhausted` (не `<= 0`).
- `JAZZ-COMBAT-007-REQ-004` — Satellite: `UnitTirednessTravelTime` ≈½ vanilla (~8h/шаг); `UnitTirednessRestTime` ≈¾ vanilla (~6h/шаг); cap `Tiredness < utExhausted`; варны ~50% и ~20%; CombatLog при смене ступени.
- `JAZZ-COMBAT-007-REQ-005` — Loc RU/EN, badge/energy UI включают Fit/Winded/Fatigued; docs technical+wiki+showcase.

## Инварианты

- Публичные Id `Tired`/`Exhausted`/`WellRested`/`FreeMove` сохраняются (override).
- Armor-weight FM (COMBAT-005) отдельно.
- Soft migrate: старый Tiredness 1/2 → Winded/Fatigued.

## Acceptance criteria

- `JAZZ-COMBAT-007-AC-001` — Static: `UnitTirednessEffect` 0…4 = Fit/Winded/Fatigued/Tired/Exhausted; FreeMove Condition использует `utExhausted`.
- `JAZZ-COMBAT-007-AC-002` — Static: Fit/WR `OnCalcFreeMove` mul 120 + opening add; Tired mul 50; Exhausted max 0.
- `JAZZ-COMBAT-007-AC-003` — Static: satellite travel/rest const patched; warn stages 50/20; step log.
- `JAZZ-COMBAT-007-AC-004` — Runtime/human: первый travel-хит → Winded, merc боеспособен; Exhausted стопит travel.
- `JAZZ-COMBAT-007-AC-005` — Docs/loc: RU/EN + wiki/showcase согласованы.

## Impact

- Vanilla energy ladder overridden in JAZZ.
- Saves: soft remap of numeric Tiredness meaning; `[no new game]`.

## Решение владельца

- Статус: `approved` (implement request 2026-08-13)
- Кто: project-owner

## Evidence

- `JAZZ-COMBAT-007-AC-001`: `PASS` — static: `System_EnergyLadder.lua` remaps `UnitTirednessEffect` 0…4; `FreeMove.lua` Condition uses `utExhausted`
- `JAZZ-COMBAT-007-AC-002`: `PASS` — static: Fit/WR mul 120 + opening; Tired mul 50; Exhausted max 0
- `JAZZ-COMBAT-007-AC-003`: `PASS` — static: travel/rest patched once; `JazzEnergyTravelWarn` 50/20; step log helpers; SatelliteSquad cap `utExhausted`
- `JAZZ-COMBAT-007-AC-004`: `BLOCKED` — runtime/human playtest pending
- `JAZZ-COMBAT-007-AC-005`: `PASS` — static: wiki + showcase RU/EN + technical + loc CSV applied

## Documentation delta

- `docs/technical/systems/armor-damage-wounds-will.md`, `file-coverage.md`
- `docs/wiki/combat-and-accuracy.md`, showcase RU/EN
