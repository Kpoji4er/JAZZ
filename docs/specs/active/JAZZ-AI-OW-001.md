---
id: JAZZ-AI-OW-001
status: implemented
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-OW-001.md
  - jazz/Code/AiActions.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/design/tactical-ai-archetypes.md
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
approved_by: project-owner
---

# JAZZ-AI-OW-001: Fallback Overwatch — без random aim

## Проблема

Vanilla `AIPlaceFallbackOverwatch` при no-sight целится в случайный угол 0–360° вокруг врага / случайную дверь / лицо союзника. JAZZ вызывает этот path чаще (`JAZZ_AIDisengage` + `AIPlayAttacks`), поэтому AI без LOS ставит Overwatch «в стену» / вразнобой.

## Цели

- Fallback OW только с **осмысленной** целью.
- Если точки нет — **не** ставить OW (`return false` → revert / Unaware path как у `FallbackAction`).
- Убрать random 360° jitter и random door/ally-front как sole aim.

## Non-goals

- Менять signature `AIConeAttack` Overwatch / MGSetup scoring.
- Менять `FallbackAction` на archetypes (Skirmisher и т.д. остаются `overwatch`).
- OpeningAttack Overwatch на UnitData.

## Требования

- `JAZZ-AI-OW-001-REQ-001` — override `AIPlaceFallbackOverwatch` в `jazz/Code/AiActions.lua`.
- `JAZZ-AI-OW-001-REQ-002` — порядок выбора `target_pt` (первый валидный):
  1. `unit.last_known_enemy_pos` (если slab/pos валиден);
  2. ближайший живой enemy из `context.enemies` по `GetDist` (даже без LOS к юниту — known map position);
  3. каждый кандидат: **CheckLOS** unit→pos; **Night/Underground**: принять только если voxel **освещён** (`vsFlagIlluminated`) **или** `dist ≤` night `GetSightRadius` к этой точке;
  4. ночь, если primary кандидаты отпали: ближайшая **освещённая** pass-slab в ±4 тайла вокруг якоря (last_known / nearest enemy), с LOS, без RNG;
  5. иначе `false` — **не** ставить OW.
- `JAZZ-AI-OW-001-REQ-003` — **не** использовать: `InteractionRand(360°)`, weighted door/window, ally-front scout points.
- `JAZZ-AI-OW-001-REQ-004` — deterministic apart from existing InteractionRand in `AIPlayCombatAction` path; no new RNG for aim.
- `JAZZ-AI-OW-001-REQ-005` — сохранить firearm / PreparedAttackType gates и `AIGetAttackArgs` + `AIPlayCombatAction("Overwatch")` как vanilla.

## Инварианты и ограничения

- Не ломать AP / weapon PreparedAttackType checks.
- Deterministic aim selection.
- Saves: ephemeral.

## Acceptance criteria

- `JAZZ-AI-OW-001-AC-001` — static: override + no 360°/door/ally-front branches.
- `JAZZ-AI-OW-001-AC-002` — runtime/human: no-sight AI с `last_known` / known enemy faces that direction.
- `JAZZ-AI-OW-001-AC-003` — runtime/human: no known point → no fallback OW (revert).
- `JAZZ-AI-OW-001-AC-004` — docs: technical + wiki/showcase RU/EN.

## Impact и совместимость

- Vanilla/CommonLib: late override of `AIPlaceFallbackOverwatch`.
- Saves: ephemeral combat only.
- Network/determinism: distance-only aim, no new RNG.
- Generated data: нет.
- Cross-package: только jazz.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель: agent; reviewer: project-owner.

## Решение владельца

- Статус: implemented — aim last_known → nearest enemy; **LOS**; night **lit / night-sight** (+ lit-cell retarget ±4); **no point → revert** (owner 2026-08-08 / night filter 2026-08-11).
- Кто подтвердил: project-owner
- Дата: 2026-08-11

## Evidence

- `JAZZ-AI-OW-001-AC-001`: `PASS` — static.
- `JAZZ-AI-OW-001-AC-002`: `BLOCKED` — runtime/human.
- `JAZZ-AI-OW-001-AC-003`: `BLOCKED` — runtime/human.
- `JAZZ-AI-OW-001-AC-004`: `PASS` — docs.

## Documentation delta

- `docs/technical/systems/ai-awareness.md`
- `docs/wiki/combat-and-accuracy.md`
- `docs/showcase/ru|en/combat-and-accuracy.md`
- `docs/design/tactical-ai-archetypes.md`
