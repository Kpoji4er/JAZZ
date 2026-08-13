---
id: JAZZ-HOTFIX-007
status: implemented
owner: project-owner
systems:
  - armor-damage-wounds-will
  - weapons-ammo
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: required
write_set:
  - Code/Systems_Medicine.lua
  - Code/System_ArmorRating.lua
  - InventoryItem/JAZZ_AMMO_12gauge_Saltshot.lua
  - InventoryItem/_12gauge_Saltshot.lua
  - items.lua
  - metadata.lua
  - Ammopics/_gen/ammo_stats.csv
  - docs/specs/active/JAZZ-HOTFIX-007.md
  - docs/tools/_apply_saltshot_pain_cap.py
  - docs/tools/README.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/wiki/weapons-and-ammo.md
  - docs/showcase/ru/weapons-and-ammo.md
  - docs/showcase/en/weapons-and-ammo.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-MED-001
  - JAZZ-MED-002
approved_by: project-owner
---

# JAZZ-HOTFIX-007: 12g saltshot fills Pain to cap

## Проблема

`JAZZ_AMMO_12gauge_Saltshot` (и cut `_12gauge_Saltshot`) имеют мёртвый `AppliedEffects = "HeadshotTorsoshotArmsshotLegsshot"`: компаунд не существует в `CharacterEffectDefs`, поэтому спец-эффект не вешается. Обычный hit Pain даёт только +1 за solid hit. Owner: соль должна сразу заполнять Pain до капа.

## Цели

- Первый non-graze hit соли по юниту заполняет `Pain` до `Pain.max_stacks` (8) через `JazzAddPainStacks`.
- Analgesia по-прежнему блокирует набор.
- Убрать мёртвый `*shot` компаунд; `AppliedEffects = { "Pain" }` для UI/rollover.
- Работает и при полном поглощении бронёй (соль — низкое pen).

## Non-goals

- Травмы / bleed / Inaccurate от соли.
- Менять кап Pain или pellet count (20).
- Баланс урона/дальности соли.

## Требования

- `JAZZ-HOTFIX-007-REQ-001` — `JazzIsSaltshotAmmo` распознаёт `JAZZ_AMMO_12gauge_Saltshot` и `_12gauge_Saltshot`.
- `JAZZ-HOTFIX-007-REQ-002` — non-graze salt hit → `JazzAddPainStacks(unit, max_stacks)` (fill remaining to cap); graze без salt Pain package.
- `JAZZ-HOTFIX-007-REQ-003` — `AppliedEffects` соли = `{ "Pain" }` в companion + `items.lua` (+ ammo_stats.csv).
- `JAZZ-HOTFIX-007-REQ-004` — technical + wiki + showcase RU/EN описывают salt → Pain to cap.

## Инварианты и ограничения

- `JazzAddPainStacks` / Analgesia unchanged.
- Другие 12g ammo без изменений.
- Saves: old dead AppliedEffects string harmless.

## Acceptance criteria

- `JAZZ-HOTFIX-007-AC-001` — static: AppliedEffects Pain; no HeadshotTorsoshot…; helpers present; ArmorRating calls salt path.
- `JAZZ-HOTFIX-007-AC-002` — runtime/human: salt solid hit → Pain stacks at cap (8) unless Analgesia.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ-only ammo effect path.
- Saves: ok.
- Network: status stacks via existing AddStatusEffect.

## Ownership

- Package: `jazz`. Runtime: `Systems_Medicine.lua` + `System_ArmorRating.lua`. Data: salt InventoryItem companions + `items.lua`.

## Documentation delta

- `docs/technical/systems/armor-damage-wounds-will.md`
- `docs/wiki/weapons-and-ammo.md`
- `docs/showcase/ru/weapons-and-ammo.md` + `en/weapons-and-ammo.md`

## Test plan

1. Static: grep AppliedEffects / helpers.
2. `_validate_items_quick.py`.
3. Runtime: load salt, hit enemy → Pain 8; with Analgesia → 0 new stacks.

## Evidence

- `JAZZ-HOTFIX-007-AC-001`: `PASS` — static: AppliedEffects `Pain`; helpers `JazzIsSaltshotAmmo` / `JazzTrySaltshotPain`; ArmorRating Analgesia gate on AppliedEffects Pain; `_validate_items_quick.py` OK.
- `JAZZ-HOTFIX-007-AC-002`: `BLOCKED` — runtime/human playtest pending.
