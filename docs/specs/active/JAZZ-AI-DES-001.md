---
id: JAZZ-AI-DES-001
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
  - jazz/docs/specs/active/JAZZ-AI-DES-001.md
  - jazz/Code/AIBehaviours.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
approved_by: project-owner
---

# JAZZ-AI-DES-001: Deserter despawn — не исчезать рядом с игроком

## Проблема

Vanilla `Deserter` (`RetreatAI`, `DespawnAllowed=true`) деспавнит юнита не только на Entrance, но и когда с текущей клетки **нет LOS к врагам** (`RetreatAI:CanDespawn`). Боец может отойти за камень/угол на виду у игрока и мгновенно исчезнуть — выглядит как телепорт, а не побег.

Игрок хочет сохранить сам факт исчезновения (успешный побег), но убрать «исчез за ближайшим укрытием».

## Цели

- LOS-ветка despawn работает **только если** рядом нет живых юнитов стороны игрока.
- Entrance-маркер despawn **без изменений** (убежал к выходу → poof OK).
- `Panicked` (`DespawnAllowed=false`) не затрагивается.

## Non-goals

- Менять шансы panic→`Deserter` / `JazzAI_RollPanicDeserter`.
- Новый archetype / UI / voice.
- Запрет despawn по visibility/camera (только дистанция до player units).
- Rebels/Army отдельно (хук общий на `RetreatAI:CanDespawn`).

## Требования

- `JAZZ-AI-DES-001-REQ-001` — override `RetreatAI:CanDespawn` в `jazz/Code/AIBehaviours.lua` (файл уже в load list): LOS-ветка despawn дополнительно требует отсутствия живого player-side юнита в радиусе `R` тайлов; Entrance без этого gate.
- `JAZZ-AI-DES-001-REQ-002` — порог: **`R = 16`** тайлов (`JazzAI_DeserterSafeDespawnTiles`; `GetDist` ≤ `R × SlabSizeX`).
- `JAZZ-AI-DES-001-REQ-003` — «player-side»: живые юниты с `team.player_team`, не трупы.
- `JAZZ-AI-DES-001-REQ-004` — если юнит в зоне `Entrance` marker — возвращать true **даже** при игроках рядом.
- `JAZZ-AI-DES-001-REQ-005` — deterministic, без RNG.

## Инварианты и ограничения

- Не менять preset `Deserter` / `Panicked` в jazz-units generated data.
- Не ломать intentional despawn на exit.
- Не добавлять save/network state.

## Acceptance criteria

- `JAZZ-AI-DES-001-AC-001` — static: override в `AIBehaviours.lua`; `JazzAI_DeserterSafeDespawnTiles = 16`.
- `JAZZ-AI-DES-001-AC-002` — runtime/human: Deserter за укрытием **в ≤16** от игрока **не** despawn’ится на этом ходе (продолжает RetreatAI движение).
- `JAZZ-AI-DES-001-AC-003` — runtime/human: Deserter **вне 16** без LOS к врагам — по-прежнему может despawn (LOS-path).
- `JAZZ-AI-DES-001-AC-004` — runtime/human: Deserter в зоне Entrance — despawn даже рядом с игроком.
- `JAZZ-AI-DES-001-AC-005` — docs: technical `ai-awareness.md` + player note в wiki/showcase RU/EN.

## Impact и совместимость

- Vanilla/CommonLib: late override `RetreatAI:CanDespawn`; узкий gate.
- Saves: ephemeral combat only.
- Network/determinism: distance-only, sync-safe.
- Generated data: нет.
- Cross-package: только jazz.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель: agent; reviewer: project-owner.

## Решение владельца

- Статус: implemented — **R = 16** (owner: «16 давай» / «апрув, делай»).
- Кто подтвердил: project-owner
- Дата: 2026-08-08

## Evidence

- `JAZZ-AI-DES-001-AC-001`: `PASS` — static: `JazzAI_DeserterSafeDespawnTiles = 16` + `RetreatAI:CanDespawn` in `Code/AIBehaviours.lua`.
- `JAZZ-AI-DES-001-AC-002`: `BLOCKED` — runtime/human.
- `JAZZ-AI-DES-001-AC-003`: `BLOCKED` — runtime/human.
- `JAZZ-AI-DES-001-AC-004`: `BLOCKED` — runtime/human.
- `JAZZ-AI-DES-001-AC-005`: `PASS` — technical + wiki + showcase RU/EN.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — Deserter despawn proximity gate (16).
- `docs/wiki/combat-and-accuracy.md` — player note.
- `docs/showcase/ru/combat-and-accuracy.md` + `docs/showcase/en/combat-and-accuracy.md` — то же.
