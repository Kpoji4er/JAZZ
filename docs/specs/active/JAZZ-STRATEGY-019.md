---
id: JAZZ-STRATEGY-019
status: implemented
owner: project-owner
systems:
  - legion-global-ai
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-019.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/docs/specs/active/JAZZ-STRATEGY-LEGION-AI-ROADMAP.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
exclusive_resources:
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: project-owner chat 2026-08-02 — gradual tax/recruiter + global spawn pool by Legion tier
---

# JAZZ-STRATEGY-019: gradual logistics + global spawn pool by tier

## Проблема

На NoMaps/материке при многих аванпостах tax/recruiter и combat спавнятся пачкой в первые окна (bootstrap `poi_money` + независимые cooldowns). Нет общего лимита «сколько новых отрядов Легиона может появиться одновременно на карте».

## Цели

- Tax / recruiter **не** в первый же день: сначала аванпост копит/отдаёт ресурсный цикл, потом логистика.
- **Глобальный пул** новых managed-спавнов (все роли через `lSpawnManaged`).
- Размер пула растёт с **major tier** Легиона.
- В командном окне: tax/recruiter → **combat** → supply/shipment/manpower.

## Non-goals

- Despawn уже существующих отрядов.
- Изменение TaxThreshold / POI pulse rates (016).
- Faction overlay (014).

## Locked defaults (owner 2026-08-02)

| Param | Value |
| --- | ---: |
| Global spawn window | **24h** |
| Concurrent new spawns @ tier I (major 1) | **1** |
| Concurrent new spawns @ tier II (major 2) | **2** |
| Concurrent new spawns @ tier III (major 3+) | **3** |
| Tax/recruiter first open after outpost enable | **72h** (`logistics_open_at`) |
| Consumes pool | любой **новый** `lSpawnManaged` |
| Does **not** consume | idle reuse / re-dispatch existing squad |
| Command window order | tax → recruiter → **combat** → supply → shipment → manpower |

Tier signal: same as gear — `JAZZ_GetLegionTier()` tens → major 1/2/3.

## Требования

- `JAZZ-STRATEGY-019-REQ-001` — global spawn window + used counter on `gv_JAZZ_LegionAI`.
- `JAZZ-STRATEGY-019-REQ-002` — slots by Legion major tier 1/2/3 → 1/2/3.
- `JAZZ-STRATEGY-019-REQ-003` — tax/recruiter blocked until `outpost.logistics_open_at` (enable + 72h).
- `JAZZ-STRATEGY-019-REQ-004` — command window: tax/recruiter → combat → supply/shipment/manpower.
- `JAZZ-STRATEGY-019-REQ-005` — docs wiki/showcase/technical.

## Инварианты и ограничения

- Idle reuse / re-dispatch existing squads не жрёт global pool.
- Outpost-local combat gate 48h (016) остаётся.
- Existing saves без `logistics_open_at` → open immediately (`0`); только **новые** outposts получают +72h.

## Acceptance criteria

- `JAZZ-STRATEGY-019-AC-001` — static: helpers + 72h gate + tier slots table present.
- `JAZZ-STRATEGY-019-AC-002` — runtime/human: day-1 no tax/recruiter flood across many Auto outposts.
- `JAZZ-STRATEGY-019-AC-003` — runtime/human: at most N new managed spawns / 24h by tier.
- `JAZZ-STRATEGY-019-AC-004` — docs updated.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: Legion AI spawn density only.
- Saves: additive `global_spawn`, `outpost.logistics_open_at` — no schema bump.
- Network/determinism: gates on sync path.
- Generated data: нет.
- Cross-package: `jazz` only.
- Rollback: revert Guardpost_Patrols helpers.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Exclusive: `gv_JAZZ_LegionAI`.

## Решение владельца

- Статус: **implemented** (chat 2026-08-02; runtime AC still open).

## Evidence

- `JAZZ-STRATEGY-019-AC-001`: `PASS (static)` — `docs/tools/_test_legion_spawn_pool.py`.
- `JAZZ-STRATEGY-019-AC-002`: `BLOCKED (runtime/human)`.
- `JAZZ-STRATEGY-019-AC-003`: `BLOCKED (runtime/human)`.
- `JAZZ-STRATEGY-019-AC-004`: `PASS (static)` — technical + wiki + showcase.

## Documentation delta

- technical strategy, wiki, showcase, roadmap §10, tools test.
