---
id: JAZZ-AI-006
status: implemented
owner: project-owner
systems:
  - visibility
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Unit.lua
  - jazz/items.lua
  - jazz/docs/specs/active/JAZZ-AI-006.md
  - jazz/docs/technical/systems/visibility-weather-appearance.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/showcase/ru/about.md
  - jazz/docs/showcase/en/about.md
  - jazz/metadata.lua
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-AI-006: Brush + indoors — малый flat, camo-множитель в траве

## Проблема

1. Трава имба: `BrushSightMod −50` + prone×2 (−60) без camo уже упирают Hidden в пол (~9 Aware) — порядок Shadow в полном камуфляже.
2. Помещения сейчас **не** дают отдельного sight-штрафа в `GetSightRadius` (есть только `unit.indoors` для дождя/jam и AI indoors scoring).

Нужна трава как **слабый фон** + **усилитель camo**, и помещение как **очень маленький flat для всех** (Hidden и нет).

Зависит от / уточняет `JAZZ-AI-005` (стена 8–10, Stealthy ~15, open без camo ~Aware edge).

## Утверждённые параметры

| Параметр | Сейчас | Предложение |
|---|---|---|
| `BrushSightMod` | **−50** | **−10** (маленький flat) |
| Camo в траве, Hidden | ×**3** | ×**3** (множит camo) |
| Camo в траве, не Hidden | ×50% | ×**100%** (полный camo vs ×25% open) |
| Prone в траве | `×2` | **×1** |
| `SightModMinValue` (день) | **20** (~9) | **9** (~**4** Aware) |
| Night floor | **12** (~5.5) | **9** (~4) |
| **Помещение (indoors)** | нет | **−5** flat к modifier, если цель indoors; **независимо от Hidden/camo/Stealthy** |

Детект помещения (после approval): `other.indoors` и/или check по `step_pos` — смысл: **цель в комнате**, не «наблюдатель в комнате».

### Ожидаемые дистанции (Aware 46, static model)

| Профиль | День |
|---|---:|
| Без camo, стоя в траве | **~41** |
| Без camo, prone в траве | **~28** |
| Без всего, открыто | **46** |
| Без всего, **в помещении** (−5) | **~44** |
| Shadow + camo 45, открыто | **~16** |
| Shadow + camo 45 + стена | **~9** |
| **Shadow + camo 45 + трава** | **~4** |
| Shadow + camo 45 + помещение (без травы/стены) | **~14** |
| Stealthy + camo 40, открыто | **~16** |

## Цели

- Трава сама почти не прячет; camo в траве сильнее, чем на открытом.
- Shadow full camo в траве → **~4** клетки (Aware).
- Помещение → крошечный бонус **всем**, без синергии со стелсом.
- Стена / Stealthy open / голый open qualitatively как в AI-005.

## Non-goals

- Binary kit / camo≥N.
- Combat facing.
- Менять Aware/Unaware base.
- Штраф за «наблюдатель indoors» (только цель), пока владелец не попросит иначе.
- Отдельная синергия room×Hidden или room×camo.

## Требования

- `JAZZ-AI-006-REQ-001` — `BrushSightMod = -10`.
- `JAZZ-AI-006-REQ-002` — Hidden в траве: `camo * 3`.
- `JAZZ-AI-006-REQ-003` — не Hidden в траве: camo **100%**.
- `JAZZ-AI-006-REQ-004` — prone в траве без ×2.
- `JAZZ-AI-006-REQ-005` — `SightModMinValue = 9`; night floor = 9.
- `JAZZ-AI-006-REQ-006` — если цель indoors: `modifier -= 5` (ConstDef вроде `IndoorSightMod`), **всегда**, не только Hidden.

## Acceptance criteria

- `JAZZ-AI-006-AC-001` — static: ConstDef/код = REQ (brush, prone, min, indoor flat).
- `JAZZ-AI-006-AC-002` — static model: no-camo brush ≥40; Shadow full brush ~4; wall ~9; open 46; indoors open ~44 (Hidden или нет — тот же −5).
- `JAZZ-AI-006-AC-003` — tables в visibility docs пересчитаны.
- `JAZZ-AI-006-AC-004` — human: трава / стена / open / комната.

## Решение владельца

- Статус: **`approved`** (владелец: «Апрув», 2026-07-30).
- Defaults из draft: brush **−10**, Hidden camo ×**3**, visible brush camo **100%**, prone ×**1**, min **9**, indoor **−5** только на цель.

## Evidence

- `JAZZ-AI-006-AC-001`: `PASS` — static: BrushSightMod −10, IndoorSightMod −5, SightModMinValue 9; prone×1 in brush; visible brush camo 100%.
- `JAZZ-AI-006-AC-002`: `PASS` — static model: no-camo brush ~41; Shadow full brush ~4; wall ~9; open 46; indoors ~44.
- `JAZZ-AI-006-AC-003`: `PASS` — visibility tables updated.
- `JAZZ-AI-006-AC-004`: `BLOCKED` — human playtest.

## Documentation delta

- После approval: visibility tables + ConstDef; `version_minor` в том же change set, что код.
