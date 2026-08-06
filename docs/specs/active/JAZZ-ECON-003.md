---
id: JAZZ-ECON-003
status: draft
owner: project-owner
systems:
  - economy
  - inventory
  - ui
  - quests
repositories:
  - jazz
  - jazz-maps
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-ECON-003.md
  - jazz/docs/design/economy-ops-and-trade.md
  - jazz/Code/
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/English.csv
  - jazz/Russian.csv
  - jazz-maps/ (quest NPC wiring / conversation hooks as needed)
  - jazz/docs/technical/
exclusive_resources:
  - localization ID range (merchant UI + NPC strings)
  - XTemplate / dialog class ids for sell UI
related_decisions:
  - none
approved_by: pending
---

# JAZZ-ECON-003: JA2-style buy/sell with quest NPCs

## Проблема

В JA2 квестовые торговцы открывали полноценное меню купли-продажи. В JA3/JAZZ — Bobby Ray (почта) и точечные give/dialog; **нет** общего sell menu для NPC. Квестовые персонажи не могут стабильно торговать ассортиментом и принимать лут игрока через единый UX.

Design backlog: [`docs/design/economy-ops-and-trade.md`](../../design/economy-ops-and-trade.md).

## Цели

- Отдельный **buy/sell UI** (инвентарь игрока ↔ инвентарь/кошелёк торговца), вызываемый из conversation / interaction квестового NPC.
- Конфиг торговца: whitelist категорий, buy/sell multipliers, money pool, restock rules (v1 может быть static stock).
- Минимум **один** playable Ernie (или owner-picked) quest NPC wired end-to-end как proof.
- Совместимость с будущим расширением mainland NPC без переписывания UI.

## Non-goals

- Port bulk export operation (ECON-002) — другой канал.
- Livewire city income (ECON-001).
- Полный магазин «всех граждан мира» / замена Bobby Ray.
- Player-to-player / multiplayer economy.
- Полный rewrite AIM/AME browsers.

## Open (зафиксировать до approve)

| Тема | Кандидаты |
| --- | --- |
| UI host | new XTemplate vs extend Give/Inventory dialog |
| First NPC | owner pick (Ernie cast) |
| Buyback | yes / session-only / no |
| Quest-locked items | never sellable / special flag |
| Price base | `Cost` × multiplier; condition scaling |
| Stock persistence | GameVar per NPC vs sector |
| Package split | UI in `jazz`, NPC hooks in `jazz-maps` |

## Требования

- `JAZZ-ECON-003-REQ-001` — public open API: open merchant UI for `merchant_id` / unit / conversation context.
- `JAZZ-ECON-003-REQ-002` — sell: player item → `$` (merchant can afford / pool rules); item moves to merchant stock or despawns per config.
- `JAZZ-ECON-003-REQ-003` — buy: merchant stock → player inventory for `$`.
- `JAZZ-ECON-003-REQ-004` — per-merchant config preset (categories, multipliers, money, stock list).
- `JAZZ-ECON-003-REQ-005` — at least one quest NPC opens UI from conversation (maps or jazz conversation hook).
- `JAZZ-ECON-003-REQ-006` — RU/EN for UI chrome + sample NPC lines.
- `JAZZ-ECON-003-REQ-007` — technical system page (new or economy subsection) + file-coverage; wiki/showcase on ship.
- `JAZZ-ECON-003-REQ-008` — quest-critical items cannot be sold unless explicitly flagged.

## Инварианты и ограничения

- Не ломать Bobby Ray delivery / shop.
- Не ломать vanilla Give item / swap inventory flows outside merchant mode.
- Deterministic prices for same condition/stack.
- Saves: merchant stock/money must persist if restock ≠ full reset each open (policy locked before approve).
- Network: NetSync for transfers.
- Cross-package: maps owns NPC placement/conversation; jazz owns UI + economy helpers.

## Acceptance criteria

- `JAZZ-ECON-003-AC-001` — static: UI + API + merchant preset schema.
- `JAZZ-ECON-003-AC-002` — editor: XTemplate/presets load; loc balanced.
- `JAZZ-ECON-003-AC-003` — runtime: sample NPC → open UI → sell item → money up, item left player inv.
- `JAZZ-ECON-003-AC-004` — runtime: buy from stock → item in inv, money down.
- `JAZZ-ECON-003-AC-005` — runtime: quest-locked item rejected.
- `JAZZ-ECON-003-AC-006` — save/load mid-stock (if persistence required) OK.
- `JAZZ-ECON-003-AC-007` — docs match shipped behavior.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: additive UI + hooks; high UI risk.
- Saves: new GameVars / merchant state possible.
- Network/determinism: synced transfers.
- Generated data: XTemplate, presets, possibly conversation ModItems in maps.
- Cross-package: `jazz` + `jazz-maps` write set.
- Rollback: hide conversation option + unload UI code.

## План и ownership

- Пакет-владелец UI/economy: `jazz`; NPC content: `jazz-maps`
- Рекомендуемый порядок: после ECON-001/002; возможный split UI shell vs NPC wave
- До approve: first NPC id, UI host choice, persistence policy

## Решение владельца

- Статус: **draft**
- Intent confirmed 2026-08-06 (JA2-style sell menu with quest NPCs); details pending

## Evidence

- `JAZZ-ECON-003-AC-001`…`007`: `BLOCKED` — not implemented

## Documentation delta

- Design: `docs/design/economy-ops-and-trade.md`
- On ship: new/updated technical economy/UI page, file-coverage, wiki/showcase
