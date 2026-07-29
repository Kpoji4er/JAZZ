---
id: JAZZ-AI-REG-001
status: approved
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-REG-001.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/tactical-ai-roles-playtest.md
  - jazz-units/Code/AICombatStance.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
exclusive_resources:
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - docs/design/tactical-ai-archetypes.md
approved_by: project-owner
---

# JAZZ-AI-REG-001: Isolated Legion regroup to ally cluster

## Проблема

Одиночный (или пара) солдат Легиона на одном конце карты продолжает локальный бой/hold, пока основная толпа союзников стоит далеко. Нужно, чтобы он **убегал к своим**, а не Deserter’ом на exit и не геройствовал один против игрока.

Design adjacent: `FallBack` directive (F8) — это офицерский приказ; изоляция — **локальный** триггер без офицера.

## Цели

- Isolated Legion (локальный карман ≤2 живых, далеко от крупного кластера союзников) в `JazzAI_PickCombatStance` переключается на `Legion_Regroup`.
- `Legion_Regroup` тянет OptLoc/EndTurn к ally cluster (`AIPolicyProximity` allies, `ScoreMode=closer_better`, высокий Weight), cover умеренный, без агрессивного Press/Flank.
- Не despawn / не entrance Retreat; после сближения с кластером снова обычный stance.

## Non-goals

- Rebels / Army / Adonis (можно зеркалом позже).
- Officer `FallBack` directive wiring (CMD-001; отдельно).
- Новый visible perk/badge для «иду к своим» (v1 без UI).
- Замена panic→`Deserter` (panic остаётся приоритетнее при roll).
- Pathfinding «через всю карту» вне OptLocSearchRadius archetype.

## Требования

- `JAZZ-AI-REG-001-REQ-001` — helper `JazzAI_NeedsRegroup(unit)` (или эквивалент): true только для `Affiliation` Legion (и Legion-prefix archetype), если **локальный карман** ≤ `LocalMax` живых allies в радиусе `LocalRadius` тайлов (включая себя) **и** существует **дальний кластер** ≥ `ClusterMin` живых allies команды, до ближайшего члена которого ≥ `ClusterGap` тайлов.
- `JAZZ-AI-REG-001-REQ-002` — предложенные пороги (утвердить владельцем): `LocalMax=2`, `LocalRadius=8`, `ClusterMin=3`, `ClusterGap=18`.
- `JAZZ-AI-REG-001-REQ-003` — при NeedsRegroup `JazzAI_PickCombatStance` возвращает `Legion_Regroup` **после** medic/melee checks, **до** обычного Scout/Pusher assign; panic→Deserter остаётся последним override.
- `JAZZ-AI-REG-001-REQ-004` — `ModItemAIArchetype` `Legion_Regroup`: Positioning/StandardAI с Proximity(allies, closer_better, Weight≥800), TakeCover moderate, AvoidDeathZones; OptLocSearchRadius ≥80; без DespawnAllowed RetreatAI.
- `JAZZ-AI-REG-001-REQ-005` — `items.lua` + `metadata.lua` + (если companion) в одной транзакции; stance code в `jazz-units/Code/AICombatStance.lua`.

## Инварианты и ограничения

- Deterministic (без `math.random` в NeedsRegroup).
- Не менять vanilla `Deserter` / `Panicked`.
- Не трогать UnitData base archetype assignment — только runtime PickCustom.
- Leaders / Medic early switch не ломать: Leader пишет aura и выходит; Medic bleed/heal раньше regroup.

## Acceptance criteria

- `JAZZ-AI-REG-001-AC-001` — static: `Legion_Regroup` в metadata/items; `JazzAI_NeedsRegroup` + stance branch существуют.
- `JAZZ-AI-REG-001-AC-002` — static: sync jazz-units без orphan для нового Id.
- `JAZZ-AI-REG-001-AC-003` — runtime/human: 1–2 Legion далеко от основной группы (≥3) двигаются к кластеру, не на map exit.
- `JAZZ-AI-REG-001-AC-004` — runtime/human: в плотном отряде (≥3 в 8 тайлах) Regroup **не** срабатывает.
- `JAZZ-AI-REG-001-AC-005` — docs: playtest строка + design note в archetypes.

## Impact и совместимость

- Vanilla/CommonLib: новый ModItem archetype + stance hook.
- Saves: ephemeral combat only.
- Generated data: jazz-units archetype.
- Cross-package: jazz design/spec only; runtime в jazz-units (+ уже загруженный jazz если aura helpers, не обязателен).

## План и ownership

- Пакет-владелец: jazz-units (archetype + stance); jazz (spec/design/playtest).
- Исполнитель: agent; reviewer: project-owner.

## Решение владельца

- Статус: approved — пороги LocalMax=2 / LocalRadius=8 / ClusterMin=3 / ClusterGap=18; Legion-only.
- Кто подтвердил: project-owner
- Дата: 2026-07-29

## Evidence

- `JAZZ-AI-REG-001-AC-001`: `PASS` — static: `Legion_Regroup` items+metadata; `JazzAI_NeedsRegroup` + stance branch.
- `JAZZ-AI-REG-001-AC-002`: `BLOCKED` — full sync audit optional (owner SaveWholeMod).
- `JAZZ-AI-REG-001-AC-003`: `BLOCKED` — runtime/human.
- `JAZZ-AI-REG-001-AC-004`: `BLOCKED` — runtime/human.
- `JAZZ-AI-REG-001-AC-005`: `PASS` — design + playtest updated.

## Documentation delta

- `docs/design/tactical-ai-archetypes.md` — секция isolated regroup.
- `docs/design/tactical-ai-roles-playtest.md` — smoke Regroup.
- technical `ai-awareness` — после реализации.
