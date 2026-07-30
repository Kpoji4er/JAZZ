---
id: JAZZ-AI-005
status: implemented
owner: project-owner
systems:
  - visibility
  - tactical-ai
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Unit.lua
  - jazz/items.lua
  - jazz/CharacterEffect/Stealthy.lua
  - jazz/docs/specs/active/JAZZ-AI-005.md
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

# JAZZ-AI-005: Hidden sight balance — cover, day/night floors

## Проблема

После роста Aware sight (46) стелс в бою/подкрадывании плохо тюнится: укрытие при Hidden почти noop (`coverage × 10%`), а `SightModMinValue=20` даёт пол ~9 тайлов и днём и ночью. Нужны целевые дистанции обнаружения Hidden.

## Цели (Aware base 46, день открыто / укрытие / трава)

| Профиль | День | Ночь (без NV у наблюдателя) |
|---|---|---|
| Shadow + полный носимый camo + (стена **или** prone в траве) | **8–10** тайлов | **5–6** тайлов |
| Обычный мерк + Stealthy + лёгкий camo (форма/штаны) | **~15** тайлов | короче за счёт darkness |
| Нестелсовый / неловкий / без camo (и тяжёлая броня) | **почти край Aware (~40–46)** даже в траве/за стеной | всё ещё заметно дальше специалистов |

`stealth_kit` = `camo ≥ 20` **или** Stealthy **или** FleetingShadow. Без кита: слабое укрытие (scale 10%) + пол modifier **85** день / **50** ночь.

## Non-goals

- Combat facing / rear hemisphere в TB (`JAZZ-AI-004` остаётся exploration-only).
- Снижение `UnawareSightRange` / `AwareSightRange`.
- CrocodileHide и прочий non-player camo как баланс-эталон.
- Переписывание suspicion tick amounts.

## Требования

- `JAZZ-AI-005-REQ-001` — при Hidden + `stealth_kit`: coverage scale **35%**; без кита — **10%** (legacy).
- `JAZZ-AI-005-REQ-002` — пол modifier: день `SightModMinValue` (20); ночь/`Underground` (`night_time`) — **12** (~5.5 тайла на Aware46).
- `JAZZ-AI-005-REQ-003` — `Stealthy.stealthy_detection`: **25** (было 20).
- `JAZZ-AI-005-REQ-004` — без `stealth_kit`: после всех штрафов `modifier = Max(modifier, night_time and 50 or 85)` → день ~39+ тайлов у края Aware.
- `JAZZ-AI-005-REQ-005` — `FleetingShadow` +20 camo и brush/prone формулы без изменения (кроме взаимодействия с REQ-004).

## Инварианты

- Illuminated цель ночью: `night_time=false` — дневной пол.
- Observer NV ослабляет `DarknessSightMod`, не отменяет night min floor отдельно.
- MP: только integer MulDivRound / Clamp.

## Acceptance criteria

- `JAZZ-AI-005-AC-001` — static: Hidden cover scale 35 для kit / 10 без; night `sight_min` 12; Stealthy 25; clumsy floor 85/50.
- `JAZZ-AI-005-AC-002` — static model: Shadow camo≥60 + wall/brush → day ~9; night ~5.5.
- `JAZZ-AI-005-AC-003` — static model: Stealthy + camo~40 open day → ~15–16; no-kit open/wall/brush day → **≥39** тайлов.
- `JAZZ-AI-005-AC-004` — human: плейтест Shadow день/ночь, Stealthy день, clumsy open.

## Impact

- Vanilla/CLib/JAZZ: `GetSightRadius` уже JAZZ override.
- Saves/network: нет новых vars.
- Generated: `items.lua` Stealthy Parameters + `CharacterEffect/Stealthy.lua` при необходимости.

## Решение владельца

- Статус: `approved` (запрос владельца: Shadow 8–10 день / 5–6 ночь; Stealthy ~15; плохие условия ≈ не стелс)
- Дата: 2026-07-30

## Evidence

- `JAZZ-AI-005-AC-001`: `PASS` — static `System_OR_Unit.lua` + `items.lua` Stealthy=25.
- `JAZZ-AI-005-AC-002`: `PASS` — static model Aware46 / min20|12.
- `JAZZ-AI-005-AC-003`: `PASS` — static model no-kit floor 85 → ~39; open 46.
- `JAZZ-AI-005-AC-004`: `BLOCKED` — human playtest.

status note: mark `implemented` after commit; runtime AC-004 remains BLOCKED.


## Documentation delta

- visibility-weather-appearance.md — cover Hidden 35%, night min 12, целевые сценарии.
- ai-awareness.md — ссылка на AI-005.
- showcase about RU/EN — кратко дистанции стелса.
