---
id: JAZZ-STRATEGY-020
status: implemented
owner: project-owner
systems:
  - legion-global-ai
  - regions
repositories:
  - jazz
  - jazz-maps
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-020.md
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/wiki/grand-chien-map.md
  - jazz/docs/showcase/ru/grand-chien-map.md
  - jazz/docs/showcase/en/grand-chien-map.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
  - jazz-maps/items.lua
  - jazz-nomaps/Code/NoMaps_Autonomy.lua
exclusive_resources:
  - ModItemRegion:PortCacaoEnvirons
  - ModItemSector:P17
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-STRATEGY-020: Legion AI Region Port Cacao environs

## Проблема

Global AI на maps-профиле управлял только `ErnieIsland` / `I7`. Материковый аванпост **Камп Де Крокодиль** (`P17`) оставался на legacy Guardpost-пути, хотя география Порта Какао уже в `jazz-maps`.

## Цели

- Authored Region `PortCacaoEnvirons` с `LegionAIEnabled`, outpost `P17`, штаб Майора `B28` (как у Эрни).
- Сектора региона: `P8`–`P20`, `O10`–`O20`, `N11`–`N16` (без zero-pad в ID).
- `P17` получает Global AI role lists (garrison/patrol/recon/QRF) по образцу `I7`.
- NoMaps: maps-only region не shadow'ит `JAZZ_Auto_*` и не latch'ит Major HQ.

## Non-goals

- Новые EnemySquad presets / баланс размеров материковых отрядов (STRATEGY-016 NoMaps table).
- Авто-покрытие всех остальных Guardpost maps.
- Правка `Maps/` бинарей.

## Требования

- `JAZZ-STRATEGY-020-REQ-001` — `ModItemRegion` `PortCacaoEnvirons`: `DisplayName` «Окрестности Порта Какао», `LegionAIEnabled=true`, `ManagedOutposts={P17}`, `MajorHQSector=B28`, полный список `Sectors` по диапазонам выше; convoy/major response squads как у `ErnieIsland`.
- `JAZZ-STRATEGY-020-REQ-002` — оба представления `P17` в `jazz-maps/items.lua` (ModItemSector + CampaignPreset) имеют `EnemySquadsGarrisonList` / `Patrool` / `Recon` / `QRF` как у `I7`.
- `JAZZ-STRATEGY-020-REQ-003` — NoMaps disable path и `lMayAdoptMajorHQ` учитывают `PortCacaoEnvirons` наравне с `ErnieIsland`.
- `JAZZ-STRATEGY-020-REQ-004` — `metadata.lua` содержит `ModResourcePreset` Class Region Id `PortCacaoEnvirons`.

## Инварианты и ограничения

- `ErnieIsland` / `I7` без регрессии.
- Публичный Id `PortCacaoEnvirons` стабилен.
- Sector Id без ведущего нуля (`P8`, не `P08`).

## Acceptance criteria

- `JAZZ-STRATEGY-020-AC-001` — static: Region preset в `items.lua` + resource в `metadata.lua` с полным Sectors / P17 / B28.
- `JAZZ-STRATEGY-020-AC-002` — static: `P17` role lists bound; `GetRegionForSector("P17")` / `N12` resolve to enabled `PortCacaoEnvirons` when maps loaded (runtime).
- `JAZZ-STRATEGY-020-AC-003` — static: NoMaps disable + Major HQ guard include `PortCacaoEnvirons`.
- `JAZZ-STRATEGY-020-AC-004` — human/runtime: new game with maps — director manages `P17` (garrison adopt / role icons). `BLOCKED` until playtest.

## Impact и совместимость

- Vanilla/CommonLib: нет.
- Saves: existing campaigns без `PortCacaoEnvirons` state создают region state лениво; **new game recommended** для полного bootstrap экономики outpost.
- Generated data: `jazz/items.lua`, `jazz/metadata.lua`, `jazz-maps/items.lua`.
- Cross-package: Region в `jazz`; Guardpost wiring в `jazz-maps`; NoMaps safety в `jazz-nomaps`.

## План и ownership

- Пакет-владелец Region: **jazz**; P17 lists: **jazz-maps**; NoMaps gate: **jazz-nomaps**.
- Declared write set: см. frontmatter.

## Решение владельца

- Статус: **implemented** (static); runtime AC open
- Кто подтвердил: project-owner (direct region brief)
- Дата: 2026-08-05

## Evidence

- `JAZZ-STRATEGY-020-AC-001`: `PASS (static)` — `PortCacaoEnvirons` in `jazz/items.lua` + `metadata.lua`; sectors P8–P20 / O10–O20 / N11–N16; outpost P17; HQ B28.
- `JAZZ-STRATEGY-020-AC-002`: `PASS (static binding)` / `BLOCKED (runtime)` — P17 ModItemSector + CampaignPreset role lists mirror I7; in-game `GetRegionForSector` pending.
- `JAZZ-STRATEGY-020-AC-003`: `PASS (static)` — `lMayAdoptMajorHQ` + NoMaps `lDisableMapsOnlyRegions` include `PortCacaoEnvirons`.
- `JAZZ-STRATEGY-020-AC-004`: `BLOCKED` — human playtest (new game + maps).

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — второй managed region.
- `docs/wiki/legion-global-ai.md`, `docs/wiki/grand-chien-map.md`
- `docs/showcase/ru|en/grand-chien-map.md`, `legion-strategy.md`
