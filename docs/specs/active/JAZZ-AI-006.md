---
id: JAZZ-AI-006
status: draft
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
  - jazz/metadata.lua
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
approved_by: pending
---

# JAZZ-AI-006: Brush — малый flat + множитель camo (draft)

## Проблема

Сейчас трава имба: `BrushSightMod −50` + prone×2 (−60) без camo уже упирают Hidden в пол (~9 Aware) — тот же порядок, что Shadow в полном камуфляже. Нужна трава как **слабый фон** и **усилитель camo**, а не бесплатный стелс.

Зависит от / уточняет цели `JAZZ-AI-005` (стена 8–10, Stealthy ~15, open без camo ~Aware edge).

## Предложение владельцу (ещё не approved)

| Параметр | Сейчас | Предложение |
|---|---|---|
| `BrushSightMod` | **−50** | **−10** (маленький flat) |
| Camo в траве, Hidden | ×**3** | ×**3** (оставить — множит camo) |
| Camo в траве, не Hidden | ×50% | ×**100%** (полный camo vs ×25% на открытом) |
| Prone в траве | `SightModHiddenProne ×2` | **×1** (как на открытом; без double-dip) |
| `SightModMinValue` (день) | **20** (~9 тайлов Aware) | **9** (~**4** тайла Aware) |
| Ночной floor `JAZZ_NightSightModMinValue` | **12** (~5.5) | **9** (тот же пол ~4) или убрать отдельный night min |

### Ожидаемые дистанции (Aware 46, static model)

| Профиль | День |
|---|---:|
| Без camo, стоя в траве | **~41** (был ~23) |
| Без camo, prone в траве | **~28** (был ~9) |
| Shadow + camo 45, открыто | **~16** |
| Shadow + camo 45 + стена | **~9** |
| **Shadow + camo 45 + трава (stand/prone)** | **~4** |
| Stealthy + camo 40, открыто | **~16** |
| Без всего, открыто | **46** |

Unaware: те же %, база 22 → Shadow в траве пол **~2**.

## Цели

- Трава сама по себе почти не прячет.
- Camo в траве заметно сильнее, чем на открытом.
- Shadow в полном носимом camo в траве может подползти до **~4** клеток (Aware).
- Стена / Stealthy open / «голый» open из AI-005 не ломаются qualitatively.

## Non-goals

- Новые binary kit / camo≥N пороги.
- Combat facing.
- Менять Aware/Unaware base (46/22).

## Требования (draft — ждут утверждения)

- `JAZZ-AI-006-REQ-001` — `BrushSightMod = -10`.
- `JAZZ-AI-006-REQ-002` — Hidden в траве: `modifier -= camo * 3` (без изменения множителя, если не решим иначе).
- `JAZZ-AI-006-REQ-003` — не Hidden в траве: camo **100%** (не 50%).
- `JAZZ-AI-006-REQ-004` — prone в траве без ×2.
- `JAZZ-AI-006-REQ-005` — `SightModMinValue = 9` (Aware пол ~4); night floor согласовать (=9).

## Acceptance criteria (draft)

- `JAZZ-AI-006-AC-001` — static: ConstDef/код соответствуют REQ.
- `JAZZ-AI-006-AC-002` — static model: no-camo brush stand ≥40; Shadow full brush ~4; Shadow full wall ~9; open no-camo ~46.
- `JAZZ-AI-006-AC-003` — tables в `visibility-weather-appearance.md` пересчитаны.
- `JAZZ-AI-006-AC-004` — human playtest трава / стена / open.

## Решение владельца

- Статус: **`draft`** — код не начинать, пока не `approved`.
- Открытые вопросы:
  1. Flat травы **−10** ок, или **−15** (ближе к vanilla)?
  2. Hidden camo в траве оставить **×3** или снизить до **×2**?
  3. Пол **9** (~4 тайла) — ок, что ночь тоже упрётся в ~4?
  4. Stealthy+camo40+трава тоже упрётся в ~4 — приемлемо?

## Evidence

- Все AC: `BLOCKED` — до approval и реализации.

## Documentation delta

- После approval: technical visibility tables + ConstDef comments; bump `version_minor` в том же change set, что код.
