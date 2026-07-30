---
id: JAZZ-AI-004
status: implemented
owner: project-owner
systems:
  - tactical-ai
  - visibility
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/UnitAwareness.lua
  - jazz/docs/specs/active/JAZZ-AI-004.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/systems/visibility-weather-appearance.md
  - jazz/docs/showcase/ru/about.md
  - jazz/docs/showcase/en/about.md
  - jazz/metadata.lua
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-AI-004: Realtime rear detection radius cap (10 tiles)

## Проблема

После увеличения общего sight (`AwareSightRange` 46 / `UnawareSightRange` 22) suspicion в exploration использует тот же `GetSightRadius`. Подход к часовому **со спины** идёт через полный пузырь (до ~46 тайлов): даже с frontness floor 30% путь набирает suspicion быстрее порога. Снижение Unaware ломает пошаговый бой (стелс в TB). Нужен рычаг «со спины проще в realtime», не режущий combat sight.

## Цели

- В **exploration / realtime** (`not g_Combat`) радиус накопления suspicion **со спины** наблюдателя ≤ **10 тайлов**.
- Спереди / в бою поведение suspicion и `GetSightRadius` не менять этим spec.
- Сохранить возможность снять часового подходом сзади без имбы стелса лицом в большой пузырь.

## Non-goals

- Изменение combat/turn suspicion или TB facing rules (отложено: укрытия, нет чёткого facing UI).
- Снижение `AwareSightRange` / `UnawareSightRange`.
- Переписывание `GetSightRadius` / LOS / fog для facing.
- Тюнинг Agility−Wisdom / Heat-alarm порогов.

## Требования

- `JAZZ-AI-004-REQ-001` — в `UpdateSuspicion`, если нет активного боя и цель в задней полусфере наблюдателя (`abs(angle) >= 90°`), эффективный `sightRad` для in-range suspicion = `Min(sightRad, 10 * SlabSizeX)`.
- `JAZZ-AI-004-REQ-002` — передняя полусфера и существующий front outer-20% cut-off без регрессии.
- `JAZZ-AI-004-REQ-003` — в `g_Combat` кап не применяется.

## Инварианты и ограничения

- Детерминизм MP: только geometry/facing, без wall-clock RNG.
- `JazzRaisedAlarm` / Night tick amounts / пороги без изменений.
- `closeInTheLight` и frontness multipliers без изменений этим spec.

## Acceptance criteria

- `JAZZ-AI-004-AC-001` — static: в `UpdateSuspicion` есть кап `10 * SlabSizeX` для rear + guard `not g_Combat`.
- `JAZZ-AI-004-AC-002` — human/runtime exploration: Hidden подход сзади к unaware часовому с дистанции >10 тайлов не поднимает suspicion, пока не войдёшь в 10 тайлов сзади.
- `JAZZ-AI-004-AC-003` — human/runtime: спереди на открытом suspicion по-прежнему растёт на дальнем радиусе (не «стелс-имба лицом»).
- `JAZZ-AI-004-AC-004` — static/runtime: в бою путь `UpdateSuspicion` не применяет rear-кап (код под `not g_Combat`).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override `UpdateSuspicion` уже JAZZ; локальное поведение exploration.
- Saves: нет новых MapVar.
- Network/determinism: facing/dist only.
- Generated data: нет.
- Cross-package: нет.
- Rollback: откат `UnitAwareness.lua` блока капа.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: cloud agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner (запрос: realtime rear ≤10 клеток; бой отдельно)
- Дата: 2026-07-30

## Evidence

- `JAZZ-AI-004-AC-001`: `PASS` — static: `lSuspicionRearSightCap = 10 * SlabSizeX`; guard `not g_Combat` + `abs(angle) >= 90*60` in `UpdateSuspicion`.
- `JAZZ-AI-004-AC-002`: `BLOCKED` — runtime/human exploration approach from behind.
- `JAZZ-AI-004-AC-003`: `BLOCKED` — runtime/human front long-range suspicion.
- `JAZZ-AI-004-AC-004`: `PASS` — static: rear cap wrapped in `not g_Combat`.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — realtime rear cap.
- `docs/technical/systems/visibility-weather-appearance.md` — ссылка, что кап в suspicion, не в `GetSightRadius`.
- `docs/showcase/ru|en/about.md` — кратко для игрока про подход сзади в exploration.
