---
id: JAZZ-IMP-001
status: approved
owner: project-owner
systems:
  - units-progression-specializations
  - inventory-items-loot-crafting
  - combat-cth-actions
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - Code/System_IMP_StartingGear.lua
  - Code/System_IMP_Perks.lua
  - Code/SatelliteSquad.lua
  - Code/System_OR_Unit.lua
  - CharacterEffect/Jazz_Perk_Mimicry.lua
  - CharacterEffect/Jazz_Perk_Veteran.lua
  - CharacterEffect/Jazz_Perk_Sniper.lua
  - items.lua
  - metadata.lua
  - English.csv
  - Russian.csv
  - docs/design/imp-starting-gear.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/systems/units-progression-specializations.md
  - docs/wiki/
  - docs/showcase/
  - ../jazz-units/items.lua
  - ../jazz-units/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz-units/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-IMP-001: динамический экип IMP + перки

## Проблема

IMP получает статичный `IMP_equipment_basic` при `CreateUnitData` (до теста). Финальные статы/перки не влияют на кит — в отличие от JA2.

## Цели

- Стартовый экип IMP зависит от финальных статов и перков (таблица в `docs/design/imp-starting-gear.md`).
- Три новых Personality-перка: Mimicry, Veteran, Sniper.
- Мимикрия открывает dialogue-гейты Negotiator/Scoundrel/Psycho без combat/economy side-effects этих перков.

## Non-goals

- ПП dump-action / panic-from-mag.
- Динамический экип не-IMP мерков.
- Перебаланс порогов статов.
- Blanket wrap глобального `HasPerk`.

## Требования

- `JAZZ-IMP-001-REQ-001` — после `CreateImpMercData(sync)` инвентарь очищается и собирается `JazzBuildImpStartingGear` → `EquipStartingGear`.
- `JAZZ-IMP-001-REQ-002` — primary priority: Stealthy MP5SD > Heavy+Auto+Str LMG (+M79 secondary) > AutoWeapons ladder > Marksmanship ladder.
- `JAZZ-IMP-001-REQ-003` — AutoWeapons mid-tier = `TMP`; LMG path uses `BAR`/`RPD`; Scoundrel → ConcussiveGrenade×2; journals stack Leadership+Teacher.
- `JAZZ-IMP-001-REQ-004` — `Jazz_Perk_Mimicry` passes dialogue conditions for Negotiator/Scoundrel/Psycho only.
- `JAZZ-IMP-001-REQ-005` — `Jazz_Perk_Veteran` adds +10 in SkillCheck, RollSkillCheck, UnitHasStat.
- `JAZZ-IMP-001-REQ-006` — `Jazz_Perk_Sniper` adds +1 via OnCalcMaxAimActions.
- `JAZZ-IMP-001-REQ-007` — Mimicry/Veteran/Sniper appear in `ImpGetPersonalPerks()`; Group `Perk-Personality`.
- `JAZZ-IMP-001-REQ-008` — `IMP_equipment_basic` is a minimal placeholder until hire rebuild.

## Инварианты и ограничения

- Не выдавать реальные Psycho/Negotiator/Scoundrel через Mimicry.
- Deterministic item list from stats/perks (no Random for weapon choice).
- Existing EquipStartingGear slot routing preserved.

## Acceptance criteria

- `JAZZ-IMP-001-AC-001` — static: generator + hooks present; items/metadata load; loc IDs both languages. Evidence: static.
- `JAZZ-IMP-001-AC-002` — hire IMP with AutoWeapons+Mark70 → TMP primary (human/runtime). Evidence: runtime.
- `JAZZ-IMP-001-AC-003` — Mimicry opens a Negotiator dialogue option without boat-discount Psycho Will side-effects. Evidence: runtime/human.
- `JAZZ-IMP-001-AC-004` — Veteran: SkillCheck threshold that fails at raw 80 passes with perk. Evidence: runtime.
- `JAZZ-IMP-001-AC-005` — Sniper: max aim clicks = weapon MaxAimActions+1 in aim UI. Evidence: runtime/human.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides CreateImpMercData path; wraps ImpGetPersonalPerks; overrides UnitHasPerk/UnitSquadHasMerc/UnitHasStat Evaluate paths carefully.
- Saves: mid-campaign IMP already hired keeps old gear; new hires get new kit. `[new game recommended]` for clean IMP start.
- Network: HireIMPMerc already NetSync — gear rebuild must run on sync path only.
- Generated data: CharacterEffect ModItems + jazz-units LootDef.
- Cross-package: jazz code + jazz-units LootDef.

## План и ownership

- Пакет-владелец: jazz (runtime) + jazz-units (LootDef).
- Declared write set: see frontmatter.

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (implement plan request)
- Дата: 2026-08-02

## Evidence

- `JAZZ-IMP-001-AC-001`: `PASS` — static: generator/hooks/CharacterEffects/items+metadata validated (`_validate_items_quick.py` jazz + jazz-units); loc IDs 890000000001931–936 in both CSV.
- `JAZZ-IMP-001-AC-002`: `BLOCKED` — runtime hire IMP with AutoWeapons+Mark70 → TMP.
- `JAZZ-IMP-001-AC-003`: `BLOCKED` — runtime/human Mimicry dialogue gate.
- `JAZZ-IMP-001-AC-004`: `BLOCKED` — runtime Veteran SkillCheck.
- `JAZZ-IMP-001-AC-005`: `BLOCKED` — runtime/human Sniper +1 aim.

## Documentation delta

- `docs/design/imp-starting-gear.md`
- `docs/technical/systems/units-progression-specializations.md`
- `docs/technical/systems/file-coverage.md`
- `docs/wiki/` + `docs/showcase/ru|en` mercenaries/perks
