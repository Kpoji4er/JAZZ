---
id: JAZZ-STRATEGY-028
status: implemented
owner: project-owner
systems:
  - legion-global-ai
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/metadata.lua
  - jazz/docs/specs/active/JAZZ-STRATEGY-028.md
  - jazz/docs/tools/_check_convoy_lifecycle.py
  - jazz/docs/tools/README.md
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/wiki/legion-global-ai.md
  - jazz/docs/showcase/ru/legion-strategy.md
  - jazz/docs/showcase/en/legion-strategy.md
exclusive_resources:
  - jazz/Code/Guardpost_Patrols.lua logistics lifecycle
  - jazz/metadata.lua revision and last_changes only
related_decisions:
  - JAZZ-STRATEGY-026
approved_by: project-owner chat 2026-10-03 fix and commit convoy accumulation
---

# JAZZ-STRATEGY-028: восстановление конвоев и ограничение резерва штаба

## Проблема

В Vanilla Maps A20 является штабом Майора. Конвои при неудаче построения пути переходят в orphaned без повторной попытки. Вернувшаяся охрана tier-pulse остаётся в штабе без ограничения количества.

## Цели

Восстановить движение при появлении пути; ограничить пустой резерв HQ одним supply и одним manpower, включая существующие сохранения.

## Non-goals

Не менять составы, тиры, стартовый гарнизон, количество tier-pulse доставок и их ресурсы. Не менять sibling-пакеты и схемы generated data.

## Требования

- `JAZZ-STRATEGY-028-REQ-001` — supply/manpower/shipment в orphaned с задачей повторяют маршрут каждый час; погрузка при отсутствии пути остаётся loading. Потерянный адресат supply/manpower отменяет доставку и возвращает груз в HQ.
- `JAZZ-STRATEGY-028-REQ-002` — HQ хранит не более одного пустого завершившего рейс supply и manpower; остальные расформировываются на синхронном hourly path. В пути, с грузом, в конфликте и открытой тактике не удалять; HQ должен принадлежать Легиону.
- `JAZZ-STRATEGY-028-REQ-003` — обычный supply проверяет путь до создания; повторное использование supply/manpower учитывает уже активный рейс адресата и обновляет region_id. Повторный arrival не продлевает разгрузку.

## Инварианты и ограничения

Deterministic sorted iteration; no new globals or hooks. Cargo is credited by existing arrival logic exactly once; no schema bump. STRATEGY-026 tier-pulse remains new-spawn, but its completed HQ escorts obey this reserve cap. Existing rest/reuse contract is narrowed only for surplus empty HQ escorts.

## Acceptance criteria

- `JAZZ-STRATEGY-028-AC-001` — executable Lua harness: unavailable-route loading retries, old orphan resumes, lost destination returns without dropping cargo, repeated arrival does not reset unloading.
- `JAZZ-STRATEGY-028-AC-002` — executable Lua harness: old-save excess HQ escorts removed deterministically; cargo, conflict, tactical view, travel and other roles preserved; repeated tick idempotent.
- `JAZZ-STRATEGY-028-AC-003` — executable Lua harness: no-path regular supply does not spawn; active destination prevents reuse; reuse updates region; metadata validation and existing tier convoy smoke pass.

## Impact и совместимость

JAZZ-only internal functions, existing RemoveSquad and routing APIs. Both map profiles use root.major.hq_sector. Existing saves repair on hourly processing, no migration flag. No new assets or public IDs. Metadata changes only Revision/last_changes. Offline Lua scenarios are required; live save and multiplayer checks remain unverified, without claiming in-game acceptance.

## План и ownership

Owner jazz; implement and test in declared write set; reviewer project-owner. Preserve unrelated working tree and staged content.

## Решение владельца

2026-10-03: после отчёта о зависании и накоплении пользователь поручил «пофикси и коммит». Это разрешение на описанное исправление и локальный коммит.

## Evidence

- `JAZZ-STRATEGY-028-AC-001`: PASS — offline executable production Lua, unavailable-route loading over 48 hours, old orphan/return recovery, cancelled cash and manpower delivery refunded once, idempotent unloading deadline.
- `JAZZ-STRATEGY-028-AC-002`: PASS — offline executable Lua: 40 old escorts reduced to two, another 20 removed on later tick; cargo, recruits, movement, tasks, other roles, conflict, tactical view and captured HQ protected.
- `JAZZ-STRATEGY-028-AC-003`: PASS — offline Lua dispatch/reuse scenarios and full-file Lua syntax, `_check_strategy026_tier_convoys.py`, `_validate_items_quick.py`, local four-page documentation contract. Generated audit: zero errors, 12 existing dormant/orphan warnings plus metadata-newer-than-items warning caused by the required revision/changelog-only edit; items/load graph unchanged by this task.

Reproduction: `python docs/tools/_check_convoy_lifecycle.py` (11 scenarios, lupa). No live-game, save-file or multiplayer validation claimed. Owner review remains pending; status is implemented, not accepted.

## Documentation delta

Update strategy technical page, legion-global-ai wiki and legion-strategy RU/EN with retry and bounded empty HQ reserve. Register reproducible test in tools README.
