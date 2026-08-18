---
id: JAZZ-MED-002
status: implemented
owner: project-owner
systems:
  - armor-damage-wounds-will
repositories:
  - jazz
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/Systems_Medicine.lua
  - Code/System_OR_Unit.lua
  - CharacterEffect/Analgesia.lua
  - CharacterEffect/Pain.lua
  - CharacterEffect/WoundInfected.lua
  - CharacterEffect/BloodLoss50.lua
  - CharacterEffect/BloodLoss40.lua
  - CharacterEffect/BloodLoss30.lua
  - CharacterEffect/BloodLoss20.lua
  - CharacterEffect/BloodLoss10.lua
  - CharacterEffect/BloodLoss5.lua
  - CharacterEffect/BloodLoss1.lua
  - Icons/StatusEffects/WoundInfected.png
  - Icons/StatusEffects/BloodLoss50.png
  - Icons/StatusEffects/BloodLoss40.png
  - Icons/StatusEffects/BloodLoss30.png
  - Icons/StatusEffects/BloodLoss20.png
  - Icons/StatusEffects/BloodLoss10.png
  - Icons/StatusEffects/BloodLoss5.png
  - Icons/StatusEffects/BloodLoss1.png
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-MED-002: morphine clears Pain; WoundInfected; BloodLoss AP ladder

## Проблема

Морфий только глушит Pain; боль копится дальше. Heavy trauma не имеет нагноения (worsen=0 deferred). Текущие `HitPoints` режут max AP напрямую — нет читаемого статуса «потеря крови».

## Цели

- Морфий снимает все стаки Pain и блокирует набор, пока висит Analgesia.
- Untreated Heavy fail improve → `WoundInfected` (Trauma* не меняются); Infected fail → смерть на глобалке.
- BloodLoss статусы при HP% &lt;50/40/30/20/10/5/1 → −1…−7 start AP; GetMaxAP от Health; без move cost.
- Status icons (infection + 7-color BloodLoss ladder).

## Non-goals

- Hospital instant Trauma clear (**deferred**, locked 2026-08-18: **not loaded**; не описывать как current-state).
- Surgical kit clear Infected (v1: progress pass / TreatWounds blocks entry).
- Soften stay% on Heavy (v1: not-improve → Infected).

## Требования

- `JAZZ-MED-002-REQ-001` — Analgesia clears Pain stacks; JazzAddPainStacks no-op while Analgesia.
- `JAZZ-MED-002-REQ-002` — Untreated Heavy progress not-improve → add `WoundInfected` (Heavy remains). Healing path never infects.
- `JAZZ-MED-002-REQ-003` — WoundInfected progress every **16h**: survive → remove Infected; fail → merc death (satellite-safe).
- `JAZZ-MED-002-REQ-004` — GetMaxActionPoints uses Health, not current HitPoints.
- `JAZZ-MED-002-REQ-005` — BloodLoss50…1 mutually exclusive; APLoss 1…7; sync from HP%; only cured by raising HP.
- `JAZZ-MED-002-REQ-006` — Icons wired; loc RU/EN; technical+wiki+showcase.

## Инварианты

- Trauma* IDs unchanged; Pain RemoveOnEndCombat remains.
- Deterministic Random / InteractionRand for progress.
- Supersedes MED-001 REQ-004/016 suppress-only Pain wording for morphine.

## Acceptance criteria

- `JAZZ-MED-002-AC-001` — static: Analgesia clears Pain; JazzAddPainStacks gated.
- `JAZZ-MED-002-AC-002` — static: Heavy stay→WoundInfected; Infected fail→kill helper.
- `JAZZ-MED-002-AC-003` — static: BloodLoss ladder + GetMaxAP Health-only.
- `JAZZ-MED-002-AC-004` — static: companions/items/metadata/icons/loc present.
- `JAZZ-MED-002-AC-005` — runtime/human: morphine clears pain; low HP shows BloodLoss; infection path.

## Impact

- Saves: old Pain stacks after combat already cleared; new statuses appear when HP low / Heavy fails.
- Network: unit:Random / InteractionRand.
- Generated data: yes.

## Решение владельца

- Статус: **implemented** (2026-08-18; code loaded; AC-005 runtime BLOCKED). Instant Hospital Trauma clear **не** в shipped 002.
- Кто: project-owner («делай, собирай, пушься»)
- Дата: 2026-08-07
- 2026-08-18: instant Hospital Trauma clear **остаётся deferred**. Technical/wiki не обещают clear по концу Hospital Treatment. Не реализовывать, пока владелец явно не попросит. Shipped 002 = morphine / WoundInfected / BloodLoss AP.

## Evidence

- `JAZZ-MED-002-AC-001`: `PASS` — static: Analgesia clears Pain; JazzAddPainStacks gated under Analgesia.
- `JAZZ-MED-002-AC-002`: `PASS` — static: Heavy stay→WoundInfected; Infected fail→JazzKillMercFromInfection.
- `JAZZ-MED-002-AC-003`: `PASS` — static: BloodLoss ladder + GetMaxAP Health-only.
- `JAZZ-MED-002-AC-004`: `PASS` — static: companions/items/metadata/icons/loc; `_validate_items_quick.py` OK.
- `JAZZ-MED-002-AC-005`: `BLOCKED` — runtime/human smoke pending.

status note: **implemented** 2026-08-18 — morphine / WoundInfected / BloodLoss loaded. AC-005 runtime BLOCKED. Hospital instant Trauma clear stays deferred.

## Documentation delta

- docs/technical/systems/armor-damage-wounds-will.md
- docs/wiki/combat-and-accuracy.md
- docs/showcase/ru|en/combat-and-accuracy.md
- docs/design/medicine.md
- 2026-08-18: hospital instant Trauma clear documented as **deferred / not loaded** (wiki+showcase: Hospital Treatment ≠ trauma clear).
