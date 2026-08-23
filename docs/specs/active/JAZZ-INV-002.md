---
id: JAZZ-INV-002
status: implemented
owner: project-owner
systems:
  - inventory-items-loot-crafting
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_LootDrops.lua
  - jazz/scripts/test-loot-ammo-cap.ps1
  - jazz/docs/technical/systems/inventory-items-loot-crafting.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/specs/active/JAZZ-INV-002.md
exclusive_resources:
  - none
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-013
  - JAZZ-WEAPONS-012
approved_by: project-owner
---

# JAZZ-INV-002: заряженные патроны в луте NPC по сложности

## Проблема

`EquipStartingGear` заряжает ствол на полный `MagazineSize`. У пулемёта (ПКМ 100, ДП-27, ленты 80+) боец часто умирает с почти полной лентой. Оружие падает всегда (если `drop_chance > 0`), поэтому труп стабильно дарит полную ленту. Это второй рычаг нерфа плотности после JAZZ-WEAPONS-013: не точность очереди, а сколько патронов игрок уносит с трупа.

## Цели

- На дропе **NPC** заряженные патроны в `Firearm.ammo.Amount` режутся потолком `% × MagazineSize` от игровой сложности.
- Пулемёты (`MachineGun`, `LightMachineGun`) режутся сильнее прочих стволов.
- Если в стволе уже меньше потолка (отстреляли), остаток не увеличивается.
- Боевая зарядка AI / стартовый кит мерка / IMP не меняются.

## Non-goals

- Authored `stack_min` / `stack_max` в `LootDef` (`*_mg_ammo` 100–300 и прочие).
- Шанс дропа запасных стеков (Ammo 5%, Ordnance 15%).
- Контейнерный `GenerateLoot` (ящики, NpcGive).
- Hipfire, CTH, BDR, `WeaponRange` (это WEAPONS-012/013).
- Сейв-миграция уже лежащего лута.

## Требования

- `JAZZ-INV-002-REQ-001` — только `Unit:DropLoot` и только `is_npc`; мерки не режутся.
- `JAZZ-INV-002-REQ-002` — потолок = `Max(1, MulDivRound(MagazineSize, keep_pct, 100))` при `ammo.Amount > 0`; итог `min(Amount, потолок)`.
- `JAZZ-INV-002-REQ-003` — `keep_pct` по `Game.game_difficulty` (`Normal` / `Hard` / `VeryHard`; неизвестный id → `Normal`):

  | id | Речь / display RU | Прочие Firearm | MG / LMG |
  | --- | --- | --- | --- |
  | `Normal` | лёгкий / Первая кровь | 80 | 50 |
  | `Hard` | нормальный / Коммандос | 60 | 30 |
  | `VeryHard` | сложный / Миссия невыполнима | 45 | 18 |

- `JAZZ-INV-002-REQ-004` — MG-класс: `IsKindOf(..., "MachineGun")` или `IsKindOf(..., "LightMachineGun")` (sibling-классы, не parent/child).
- `JAZZ-INV-002-REQ-005` — без нового RNG: тот же детерминизм, что у уже существующих roll'ов дропа.
- `JAZZ-INV-002-REQ-006` — technical + wiki + showcase RU/EN в том же change set.

## Инварианты и ограничения

- Пустой ствол (`Amount` 0 / нет `ammo`) остаётся пустым.
- `EquipStartingGear` по-прежнему кладёт полный магазин (клон, не drain стека).
- `AiActions` по-прежнему доливает AI до `MagazineSize`.
- IMP / наёмники: стартовые патроны не через этот хук.
- Публичные ID предметов и LootDef не меняются.
- Три игровых сложности, без `Easy`.

## Acceptance criteria

- `JAZZ-INV-002-AC-001` — static/automated: таблица 80/60/45 и 50/30/18; неизвестный id = `Normal`.
- `JAZZ-INV-002-AC-002` — static/automated: магазин 100, MG → 50 / 30 / 18; при остатке 12 потолок не поднимает.
- `JAZZ-INV-002-AC-003` — static/automated: не-MG магазин 30 → 24 / 18 / 14.
- `JAZZ-INV-002-AC-004` — static: вызов капа только при `is_npc` в `System_LootDrops.lua`; `EquipStartingGear` / `AiActions` refill не правятся.
- `JAZZ-INV-002-AC-005` — automated: `scripts/test-loot-ammo-cap.ps1` PASS.
- `JAZZ-INV-002-AC-006` — docs: inventory-items-loot-crafting + wiki/showcase weapons-and-ammo согласованы.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override `Unit:DropLoot` уже в JAZZ; добавляется пост-обработка заряженного магазина.
- Saves: уже лежащий лут не пересчитывается; новые трупы — да.
- Network/determinism: без нового Random; те же `Amount` на всех пирах.
- Generated data: нет.
- Cross-package: нет (runtime `jazz`).
- Rollback: откат change set.
- Playtest: труп пулемётчика на трёх сложностях; не блокирует static DoD.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: front matter.
- Exclusive resources: none.

## Решение владельца

- Статус: `implemented`
- Кто подтвердил: project-owner («доп рычаг нерфа — уменьшать заряженные патроны в луте, особенно в пулемёты; можно к сложности»)
- Дата: 2026-08-23

## Evidence

- `JAZZ-INV-002-AC-001`: `PASS` — automated: `scripts/test-loot-ammo-cap.ps1` table 80/60/45 and 50/30/18; unknown id → Normal.
- `JAZZ-INV-002-AC-002`: `PASS` — automated: mag 100 MG → 50/30/18; remainder 12 stays 12; empty stays 0.
- `JAZZ-INV-002-AC-003`: `PASS` — automated: non-MG mag 30 → 24/18/14.
- `JAZZ-INV-002-AC-004`: `PASS` — static: cap call is `if is_npc and IsKindOf(item, "Firearm")` in `System_LootDrops.lua`; `EquipStartingGear` still fills `MagazineSize`; `AiActions` refill unchanged.
- `JAZZ-INV-002-AC-005`: `PASS` — automated: `scripts/test-loot-ammo-cap.ps1`.
- `JAZZ-INV-002-AC-006`: `PASS` — docs: inventory-items-loot-crafting + wiki/showcase weapons-and-ammo.

## Documentation delta

- `docs/technical/systems/inventory-items-loot-crafting.md`
- `docs/wiki/weapons-and-ammo.md`
- `docs/showcase/ru/weapons-and-ammo.md`
- `docs/showcase/en/weapons-and-ammo.md`
