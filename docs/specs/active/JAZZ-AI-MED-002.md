---
id: JAZZ-AI-MED-002
status: approved
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-MED-002.md
  - jazz/docs/specs/active/JAZZ-AI-POL-004.md
  - jazz-units/Code/AICombatStance.lua
  - jazz/Code/CombatAI.lua
  - jazz/scripts/test-ai-crowd-scoring.ps1
  - jazz/docs/tools/_check_ai_medic_bandage.py
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/testing.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - jazz/Code/CombatAI.lua
  - jazz-units/Code/AICombatStance.lua
related_decisions:
  - JAZZ-AI-MED-001
  - JAZZ-AI-POL-004
  - JAZZ-AI-ROLE-002
approved_by: project-owner
---

# JAZZ-AI-MED-002: Dedicated medic switch, ignore crowd, cover spacing

## Проблема

На M5 все 12 повстанцев с бинтами переключались в archetype `Medic`, как только в отряде был раненый или кровь. `JazzAI_PickCombatStance` возвращал `Medic` любому носителю `JAZZ_Bandage` при `JazzAI_TeamHasBleeding`. Медик-архетип тянет к союзникам (`HealingRange` / `CloseToTeammates`), POL-004 для `can_heal` только смягчает crowd (floor 55%), а не отключает его. В результате куча на одной пальме: 9 из 12 с ≥4 своими в радиусе 3.

## Цели

- Медиками становятся только dedicated medic (Bonemaker / family Medic / `allow_medic`) и не больше одного fill-in, если dedicated нет, а лечить кого-то надо.
- Скор dest медика не режется crowd/casualty modifier: подход к раненому важнее spacing.
- Остальные AI продолжают anti-stack и предпочитают свободные укрытия, а не соседнюю клетку уже занятого куста.

## Non-goals

- Team-wide assignment всех dest / формации.
- Mass edit generated archetypes / OptLoc Proximity weights в `items.lua`.
- Новые Medic preset ID, Bandage AP, MED-001 Healer score.
- Изменение REG-001 regroup.

## Требования

- `JAZZ-AI-MED-002-REQ-001` — `JazzAI_ShouldBecomeMedic(unit, opts)` true только если `JazzAI_TryMedicSwitch(unit)` и (dedicated medic или единственный fill-in). Dedicated: `opts.allow_medic` или `JazzAI_InferRoleFamily(unit) == "Medic"`. Fill-in: нет живого capable dedicated medic в команде, у юнита есть usable medicine, юнит — ближайший (затем меньший `handle`) носитель medicine к neediest patient. Blanket `carrying_bleed_medicine → Medic` удаляется.
- `JAZZ-AI-MED-002-REQ-002` — `JazzAI_CrowdDangerModifier` для medic/healer (`can_heal` или `current_archetype` Medic/Medic_Low) возвращает 100 без вычета danger. Melee floor 55 из POL-004 сохраняется. POL-004 REQ-002 healer floor 55 для medic superseded этим REQ.
- `JAZZ-AI-MED-002-REQ-003` — после crowd modifier положительный `AIScoreDest` non-medic dest с cover дополнительно умножается на `JazzAI_CoverSpacingModifier`: 100 если нет живого союзника с cover dest в `<2` тайла; 55 если один; 30 если двое и больше. Medic/healer пропускает этот modifier (100). Casualty tiles по-прежнему soft. Debug details: `COVER SPACING MOD (%)`.
- `JAZZ-AI-MED-002-REQ-004` — расчёт детерминированный: без RNG, `MapVar`/`GameVar`, `MapGet`; fill-in tie-break `handle`; allies из context snapshot.

## Инварианты и ограничения

- Hard same-XYZ dibs POL-003 не трогать.
- Узкий единственный проход остаётся проходимым (soft modifiers, не hard-block).
- Несколько dedicated medic в одном паке могут одновременно стать Medic, если есть пациент.
- Save/network state не добавляется.

## Acceptance criteria

- `JAZZ-AI-MED-002-AC-001` — static: PickCombatStance вызывает `JazzAI_ShouldBecomeMedic`; нет blanket `carrying_bleed_medicine` return Medic; fill-in/dedicated helpers live.
- `JAZZ-AI-MED-002-AC-002` — static: medic/healer crowd modifier 100; melee floor 55; cover spacing 100/55/30; one integration after crowd; no RNG in helpers.
- `JAZZ-AI-MED-002-AC-003` — runtime/human: не-медики не все становятся Medic при крови в отряде; медик подходит к раненому сквозь кучу; остальные занимают разные укрытия, если они есть.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ overrides PickCustom + AIScoreDest.
- Saves: ephemeral stance/dest scoring; old saves OK after ReloadLua.
- Network/determinism: no new persistent state.
- Generated data: not changed.
- Cross-package: jazz-units stance, jazz CombatAI.
- Rollback: restore carrying_bleed branch and healer floor 55.

## План и ownership

- Пакет-владелец: jazz (CombatAI) + jazz-units (stance).
- Исполнитель: agent.
- Reviewer: project-owner, runtime AC-003.
- Declared write set: front matter.
- Exclusive resources: CombatAI.lua, AICombatStance.lua.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner (playtest: только нужные медики; медики игнорируют скученность; остальные по укрытиям).
- Дата: 2026-08-21.

## Evidence

- `JAZZ-AI-MED-002-AC-001`: `PASS` — static: `JazzAI_ShouldBecomeMedic` in PickCombatStance; `carrying_bleed_medicine` absent; fill-in/dedicated helpers live (`docs/tools/_check_ai_medic_bandage.py`).
- `JAZZ-AI-MED-002-AC-002`: `PASS` — static: `scripts/test-ai-crowd-scoring.ps1` model=14; medic/healer crowd 100; melee floor 55; cover spacing 100/55/30; crowd then cover after BiasMarker; no RNG in CrowdDanger helper.
- `JAZZ-AI-MED-002-AC-003`: `BLOCKED` — runtime/human: ReloadLua, skip turn on M5 — not all 12 Medic; medic can stand on the patient; others take separate cover.

## Documentation delta

- `docs/technical/systems/ai-awareness.md`, `docs/technical/testing.md`
- `docs/design/tactical-ai-archetypes.md`
- `docs/wiki/combat-and-accuracy.md`, `docs/showcase/ru/combat-and-accuracy.md`, `docs/showcase/en/combat-and-accuracy.md`
- POL-004 REQ-002 healer floor note superseded for medic
