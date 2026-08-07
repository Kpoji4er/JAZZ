---
id: JAZZ-ECON-002
status: draft
owner: project-owner
systems:
  - sector-operations
  - economy
  - inventory
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-ECON-002.md
  - jazz/docs/design/economy-ops-and-trade.md
  - jazz/Code/
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/English.csv
  - jazz/Russian.csv
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/file-coverage.md
exclusive_resources:
  - localization ID range (port sell op)
  - ModItemSectorOperation id for port loot sell
related_decisions:
  - none
approved_by: pending
---

# JAZZ-ECON-002: Port sector operation — sell loot (incl. diamonds)

## Проблема

Порт (`sector.Port`) даёт лодки и Bobby Ray delivery, но нет канала **массово сдать лут / алмазы за `$`** на месте. Игрок таскает трофеи или ждёт почтовый Bobby Ray; алмазы из конвоев/лута не имеют явного port-export sink.

Design backlog: [`docs/design/economy-ops-and-trade.md`](../../design/economy-ops-and-trade.md).

## Цели

- Satellite operation в **player-controlled** секторе с `Port` (и не `PortLocked`, если применимо).
- Игрок ставит в очередь предметы (оружие/броня/misc + **алмазы** / money-bag equivalents) → по complete получает `$`.
- Явный haircut vs полная `Cost` / номинал алмазов (числа — до approve).
- Не подменять локальных квестовых торговцев (ECON-003).

## Non-goals

- JA2-style buy UI / quest merchant stock (ECON-003).
- Livewire city income (ECON-001).
- Изменение boat travel / `PricePerTile` / Bobby Ray shop catalog.
- Авто-продажа всего склада без подтверждения игрока.
- Legion AI diamond convoy rewrite.

## Open (зафиксировать до approve)

| Тема | Кандидаты |
| --- | --- |
| Duration | 1 день / пропорционально объёму очереди |
| Payout formula | `%` от `item.Cost` / tier table; алмазы: face value vs haircut. База `Cost` стволов — таблица ECON-004 audit (все active, в т.ч. вне Bobby). |
| Item source | sector stash + assigned merc inventories (как RepairItems queue) |
| Who must be present | any merc / Mechanical gate / none |
| Cooldown / capacity | per-port daily cap $ |
| Locked port | respect `PortLocked` |

## Требования

- `JAZZ-ECON-002-REQ-001` — новый `SectorOperation` только в controlled Port-секторах (gate `Port` + ownership + not locked per open table).
- `JAZZ-ECON-002-REQ-002` — UI очереди предметов (reuse `SectorOperation` items pattern где возможно).
- `JAZZ-ECON-002-REQ-003` — whitelist/blacklist категорий: оружие, броня, ammo?, valuables; **алмазы** (`DiamondBriefcase` / `TinyDiamonds` / эквиваленты) explicitly in.
- `JAZZ-ECON-002-REQ-004` — on complete: remove queued items, credit `$` by locked formula; combatlog/satellite log.
- `JAZZ-ECON-002-REQ-005` — cancel: items return to source; no `$`.
- `JAZZ-ECON-002-REQ-006` — RU/EN loc для op name/descr.
- `JAZZ-ECON-002-REQ-007` — technical + file-coverage; wiki/showcase on ship.

## Инварианты и ограничения

- Не ломать Port travel / arrival / Bobby Ray delivery multipliers.
- Не silently delete quest-unique items (quest-locked → non-sellable или warning).
- Deterministic pricing (no RNG rolls on sell).
- Saves: queue in sector op state; survive save/load mid-op.
- Network: sync item lists like RepairItems.

## Acceptance criteria

- `JAZZ-ECON-002-AC-001` — static: op + gate + pricing helpers.
- `JAZZ-ECON-002-AC-002` — editor: preset loads; loc balanced.
- `JAZZ-ECON-002-AC-003` — runtime: non-port → op unavailable; port owned → queue loot/diamonds → complete → `$` and items gone.
- `JAZZ-ECON-002-AC-004` — runtime: cancel restores items.
- `JAZZ-ECON-002-AC-005` — runtime: quest-locked / blacklisted items rejected.
- `JAZZ-ECON-002-AC-006` — docs match shipped behavior.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: additive op; Port POI semantics preserved.
- Saves: new op progress.
- Network/determinism: fixed prices.
- Generated data: items/metadata + possible Code file.
- Cross-package: diamond item ids may live in jazz / jazz-units — list exact ids before approve.
- Rollback: remove op preset.

## План и ownership

- Пакет-владелец: `jazz`
- Рекомендуемый порядок: после ECON-001
- До approve: закрыть Open table + exact diamond item class list

## Решение владельца

- Статус: **draft**
- Intent confirmed 2026-08-06; numbers pending

## Evidence

- `JAZZ-ECON-002-AC-001`…`006`: `BLOCKED` — not implemented

## Documentation delta

- Design: `docs/design/economy-ops-and-trade.md`
- On ship: strategy technical, file-coverage, wiki/showcase
