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

# JAZZ-AI-005: Hidden sight balance — cover + night floor

## Проблема

После роста Aware sight (46) стелс плохо тюнится: укрытие при Hidden почти noop (`coverage × 10%`), дневной и ночной пол modifier одинаковы (~9 тайлов). Нужны целевые дистанции без бинарных порогов camo/kit.

## Цели (Aware base 46, непрерывная формула)

| Профиль | День | Ночь (без NV) |
|---|---|---|
| Shadow + полный носимый camo + стена **или** prone в траве | **8–10** | **5–6** |
| Stealthy + лёгкий camo (форма/штаны) | **~15** | короче от darkness |
| Без перков / без camo на открытом | **почти край Aware (~46)** | darkness режет всем |

Без искусственных floors по «stealth kit» и без порога `camo ≥ 20`. Camo, Stealthy (−25), Shadow (+20 camo), укрытие и трава складываются непрерывно.

## Non-goals

- Бинарный `stealth_kit` / clumsy modifier floor.
- Combat facing (`JAZZ-AI-004` — exploration rear only).
- Снижение Aware/Unaware base ranges.

## Требования

- `JAZZ-AI-005-REQ-001` — Hidden coverage scale **35%** для всех (далее stance mul + Hidden ×150%).
- `JAZZ-AI-005-REQ-002` — пол modifier: день ConstDef **20** (~9 тайлов); `night_time` — **12** (~5.5).
- `JAZZ-AI-005-REQ-003` — `Stealthy.stealthy_detection` **25**.
- `JAZZ-AI-005-REQ-004` — нет порога camo и нет Max-floor для «non-kit».

## Acceptance criteria

- `JAZZ-AI-005-AC-001` — static: cover scale 35; night min 12; Stealthy 25; нет `camo >= 20` / `clumsy_mod_floor`.
- `JAZZ-AI-005-AC-002` — static model: Shadow full+wall/brush → day ~9; night ~5.5.
- `JAZZ-AI-005-AC-003` — static model: Stealthy+camo~40 open ~15–16; no-perk open ~46.
- `JAZZ-AI-005-AC-004` — human playtest.

## Evidence

- `JAZZ-AI-005-AC-001`: `PASS` — static (после снятия kit/floor).
- `JAZZ-AI-005-AC-002`/`003`: `PASS` — static model.
- `JAZZ-AI-005-AC-004`: `BLOCKED` — human.

## Documentation delta

- visibility / ai-awareness / showcase — без stealth_kit wording.
