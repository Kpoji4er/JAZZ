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
  - jazz/Code/CombatAI.lua
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

- Sgt 15 / Lt 25 / Capt map; Leaders WriteOfficerAura; stance reacts to directive.
- Directives: HoldLine / Push / Envelop / LowVisHold / FallBack / FocusFire / OccupyBuildings / OccupyHeights / TakeCover / GoHidden.
- Distance bands: Push ≤12, HoldLine 13–23, Envelop ≥24 (tiles from officer to nearest enemy).
- Score-picker + directive fatigue; FallBack = dead≥2 & ≥30% (no sticky wounds).
- FocusFire = threat priority (sniper/MG/close/finish); bias ×2.
- Influence buffs by directive; aura assigns `semi_sniper` / `pseudo_mg` fill-ins in radius.
- На командире — видимый System-`Perk` **Командная аура**; на союзниках в радиусе — **Под влиянием ауры**.

## Non-goals

- Squad pathfinding.
- Полные weight-множители cover/OW/smoke по директиве (поэтапно; сейчас stance + FocusFire targeting bias).
- Финальный art иконок (заглушка PNG).

## Требования

- `JAZZ-AI-CMD-001-REQ-001` — radii F8 (Sgt 15 / Lt 25 / Capt map).
- `JAZZ-AI-CMD-001-REQ-002` — MapVar team directives (`directive` / `source` / `radius` / optional `focus_target`).
- `JAZZ-AI-CMD-001-REQ-003` — PickCombatStance respects Push/Envelop/FallBack/TakeCover/OccupyBuildings/GoHidden.
- `JAZZ-AI-CMD-001-REQ-004` — `Jazz_Perk_OfficerAura` / `Jazz_Perk_OfficerAuraInfluence`; Apply/Remove по радиусу; RemoveOnEndCombat; RU+EN loc.
- `JAZZ-AI-CMD-001-REQ-005` — Score-picker + fatigue; FallBack dead≥2&≥30%; FocusFire threat-score; OccupyHeights; TakeCover/GoHidden as before; bands Push≤12 / Envelop≥24.
- `JAZZ-AI-CMD-001-REQ-006` — FocusFire `focus_target` + attack bias ×2; Influence CTH/AP/defense by directive.
- `JAZZ-AI-CMD-001-REQ-007` — GoHidden → `JazzAI_TryUnitGoHidden` on WriteOfficerAura + UnitBeginTurn.
- `JAZZ-AI-CMD-001-REQ-008` — WriteOfficerAura assigns `semi_sniper` / `pseudo_mg` among aura allies when no dedicated role.

## Инварианты и ограничения

- Ephemeral combat state; clear on CombatStart/CombatEnd.
- Иконки: stub paths под `Icons/StatusEffects/`.
- Loc IDs 890000000006100–6124.

## Acceptance criteria

- `JAZZ-AI-CMD-001-AC-001` — static aura helpers + picker bands/new directives.
- `JAZZ-AI-CMD-001-AC-002` — static Leader WriteOfficerAura call.
- `JAZZ-AI-CMD-001-AC-003` — runtime aura feel.
- `JAZZ-AI-CMD-001-AC-004` — static Perk companions + metadata/items + loc IDs 890000000006100–6117.
- `JAZZ-AI-CMD-001-AC-005` — runtime/human: на Sgt perk badge «Командная аура», на союзнике в 15 тайлах «Под влиянием ауры» + текущий приказ.
- `JAZZ-AI-CMD-001-AC-006` — static: stance Frontliner under FallBack/TakeCover/OccupyBuildings/GoHidden; FocusFire score bias + MapVar focus_target.
- `JAZZ-AI-CMD-001-AC-007` — static: GoHidden → `JazzAI_TryUnitGoHidden` / `Hide()` outside PickCustom.

## Impact и совместимость

- jazz Code + CharacterEffect generated + localization; jazz-units AICombatStance.

## План и ownership

- agent; project-owner.

## Решение владельца

- approved 2026-07-29; visible System Perks (не StatusEffect) 2026-07-29.
- owner 2026-08-21: FocusFire target score ×2 (was 1.8); apply in CreateContext and Dump `AIPrecalcDamageScore`; lock preferred dest target to `focus_target`.

## Evidence

- `JAZZ-AI-CMD-001-AC-001`: `PASS` (static) — picker helpers + 12/24 + new directives in `AIContextProfiles.lua`.
- `JAZZ-AI-CMD-001-AC-002`: `PASS`
- `JAZZ-AI-CMD-001-AC-003`: `BLOCKED`
- `JAZZ-AI-CMD-001-AC-004`: `PASS` — companions + items + metadata + RU/EN through 6117.
- `JAZZ-AI-CMD-001-AC-005`: `BLOCKED` — smoke.
- `JAZZ-AI-CMD-001-AC-006`: `PASS` (static) — `AICombatStance.lua` + CombatAI FocusFire bias.
- `JAZZ-AI-CMD-001-AC-007`: `PASS` (static) — `JazzAI_TryUnitGoHidden` / Apply on WriteOfficerAura + UnitBeginTurn.

## Documentation delta

- `docs/design/tactical-ai-archetypes.md` §6
- `docs/technical/systems/ai-awareness.md`
- `docs/showcase/ru|en/perks.md`
- `docs/tools/_apply_officer_aura_loc.py` / README
