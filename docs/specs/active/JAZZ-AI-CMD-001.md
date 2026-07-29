---
id: JAZZ-AI-CMD-001
status: approved
owner: project-owner
systems: [tactical-ai]
repositories: [jazz, jazz-units]
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-CMD-001.md
  - jazz/Code/AIContextProfiles.lua
  - jazz/CharacterEffect/Jazz_Perk_OfficerAura.lua
  - jazz/CharacterEffect/Jazz_Perk_OfficerAuraInfluence.lua
  - jazz/Icons/StatusEffects/Jazz_OfficerAura.png
  - jazz/Icons/StatusEffects/Jazz_OfficerAuraInfluence.png
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz-units/Code/AICombatStance.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Russian.csv
  - jazz/English.csv
related_decisions: [docs/design/tactical-ai-archetypes.md]
approved_by: project-owner
---

# JAZZ-AI-CMD-001: Officer aura directives

## Проблема

Leaders не пишут aura directives (F8).

## Цели

- Sgt 15 / Lt 25 / Capt map; directives HoldLine/Push/Envelop/LowVisHold; Leaders WriteOfficerAura; stance reacts to directive.
- На командире — видимый System-`Perk` **Командная аура** (имя, иконка-заглушка, описание).
- На союзниках в радиусе — видимый System-`Perk` **Под влиянием ауры**.

## Non-goals

- Squad pathfinding.
- Финальный art иконок (заглушка PNG; design в playtest/ответе).

## Требования

- `JAZZ-AI-CMD-001-REQ-001` — radii F8.
- `JAZZ-AI-CMD-001-REQ-002` — MapVar team directives.
- `JAZZ-AI-CMD-001-REQ-003` — PickCombatStance respects Push/Envelop.
- `JAZZ-AI-CMD-001-REQ-004` — `Jazz_Perk_OfficerAura` / `Jazz_Perk_OfficerAuraInfluence` (`object_class=Perk`, Tier=System, Shown); Apply/Remove по радиусу; RemoveOnEndCombat; RU+EN loc.

## Инварианты и ограничения

- Ephemeral combat state; clear on CombatStart/CombatEnd.
- Иконки: stub paths под `Icons/StatusEffects/`.

## Acceptance criteria

- `JAZZ-AI-CMD-001-AC-001` — static aura helpers.
- `JAZZ-AI-CMD-001-AC-002` — static Leader WriteOfficerAura call.
- `JAZZ-AI-CMD-001-AC-003` — runtime aura feel.
- `JAZZ-AI-CMD-001-AC-004` — static Perk companions + metadata/items + loc IDs 890000000006100–6105.
- `JAZZ-AI-CMD-001-AC-005` — runtime/human: на Sgt perk badge «Командная аура», на союзнике в 15 тайлах «Под влиянием ауры».

## Impact и совместимость

- jazz Code + CharacterEffect generated + localization.

## План и ownership

- agent; project-owner.

## Решение владельца

- approved 2026-07-29; visible System Perks (не StatusEffect) 2026-07-29.

## Evidence

- `JAZZ-AI-CMD-001-AC-001`: `PASS`
- `JAZZ-AI-CMD-001-AC-002`: `PASS`
- `JAZZ-AI-CMD-001-AC-003`: `BLOCKED`
- `JAZZ-AI-CMD-001-AC-004`: `PASS` — companions + items + metadata + RU/EN.
- `JAZZ-AI-CMD-001-AC-005`: `BLOCKED` — smoke.

## Documentation delta

- playtest CMD; ai-awareness.
