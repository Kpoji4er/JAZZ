---
id: JAZZ-STRATEGY-023
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - regions
repositories:
  - jazz
  - jazz-maps
  - jazz-nomaps
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-023.md
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/tools/_apply_great_forest_region.py
  - jazz/docs/tools/README.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/grand-chien-map.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/grand-chien-map.md
  - jazz/docs/showcase/en/grand-chien-map.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz-maps/items.lua
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
  - jazz-nomaps/AGENTS.md
exclusive_resources:
  - jazz/items.lua Regions folder
  - jazz-maps/items.lua G22 K21 sectors
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-023: GreatForest dual-outpost + shared region resources

## Проблема

Нужен регион **Великий лес** с двумя аванпостами. Сейчас каждый managed outpost хранит `$`/manpower отдельно и orphan-отряды возвращаются только на свой `home_sector` — второй лагерь региона не подхватывает потери и не делит казну.

## Цели

1. Region `GreatForest` («Великий лес»): сектора K21–K24, J20–J24, I20–I24, H20–H24, G22–G25; outposts **G22** + **K21**; late-awaken 21.
2. **Общая логика** (все multi-outpost Regions): `$`, manpower и diamond stock шарятся между enabled ManagedOutposts региона; пассивный доход/майны начисляются один раз на регион.
3. При потере аванпоста его регулярные отряды **переходят** под control другого enabled outpost того же региона (rehome); ресурсы сливаются выжившему. Если выживших нет — orphan как сейчас.

## Non-goals

- Перенос казны между разными Region Id.
- UI отображения «общей казны» (достаточно sync на outpost state).
- Специализации GreatForest (export patrol / Major priority) — отдельно.

## Требования

- `JAZZ-STRATEGY-023-REQ-001` — `GreatForest` preset + G22/K21 Global AI lists + NoMaps disable.
- `JAZZ-STRATEGY-023-REQ-002` — regions с ≥2 ManagedOutposts: shared money/manpower/diamond; economy once per region.
- `JAZZ-STRATEGY-023-REQ-003` — lose outpost → merge resources + rehome orphans to sibling; restore on sibling command window.

## Инварианты

- Single-outpost regions (Ernie, …) без behavioral change beyond no-op sync.
- Late-awaken / Major priority / export patrol unchanged.
- Schema GameVar без bump (поля outpost уже есть; sync in-memory).

## Acceptance criteria

- `JAZZ-STRATEGY-023-AC-001` — static: GreatForest + G22/K21 lists + metadata.
- `JAZZ-STRATEGY-023-AC-002` — static: share/rehome helpers in Guardpost_Patrols.
- `JAZZ-STRATEGY-023-AC-003` — runtime/human: lose one GreatForest outpost → other keeps shared pool and adopts orphans. BLOCKED until playtest.

## Impact

- Vanilla/CommonLib: none (JAZZ Legion AI only).
- Saves: existing dual-outpost (none yet) N/A; first dual is GreatForest.
- Network: NetSync via existing outpost/squad state.
- Cross-package: jazz-maps sector lists; jazz-nomaps disable.

## Решение владельца

- Статус: **approved** (owner brief 2026-08-05: Великий лес + shared resources + take orphans).
- Дата: 2026-08-05.

## Evidence

- `JAZZ-STRATEGY-023-AC-001`: `PASS (static)` — GreatForest + G22/K21 lists + metadata.
- `JAZZ-STRATEGY-023-AC-002`: `PASS (static)` — share/rehome helpers in Guardpost_Patrols.
- `JAZZ-STRATEGY-023-AC-003`: `BLOCKED` — human playtest.

## Documentation delta

- technical strategy-squads-sectors; wiki + showcase RU/EN grand-chien + legion-strategy; roadmap.
