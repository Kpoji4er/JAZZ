---
id: JAZZ-INV-001
status: implemented
owner: project-owner
systems:
  - inventory-items-loot-crafting
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - Code/System_InventoryStacks.lua
  - Code/Inventory.lua
  - Code/System_OR_SquadBag.lua
  - Code/System_OR_ItemContainer.lua
  - Code/System_OR_Weapons.lua
  - Code/System_UnitInventory.lua
  - InventoryItem/_*.lua
  - items.lua
  - metadata.lua
  - docs/specs/active/JAZZ-INV-001.md
  - docs/technical/systems/inventory-items-loot-crafting.md
  - docs/technical/systems/file-coverage.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-INV-001: большие стеки в SquadBag/SectorStash, обычные в разгрузке

## Проблема

`MaxStacks` — один лимит для всех контейнеров. Чтобы squad bag не дробился, у части vanilla ammo выставлен `MaxStacks = 5000`, из‑за чего в разгрузке мерка тоже можно держать тысячи патронов в одной ячейке. UI `Amount/MaxStacks` с четырёхзначным max выглядит плохо. Нужно: склад (bag/stash) — крупные стеки без отображения max; разгрузка — текущие personal-стеки с `Amount/max`.

### Known issue (не scope этого change, но зафиксировано)

Плавающий баг **визуального** пропадания предметов в `SquadBag`: тайлы/иконки могут исчезнуть из UI bag, пока данные в `gv_Squads[…].squad_bag` / runtime inventory остаются. Восстанавливается после регенерации UI bag (закрытие/открытие инвентаря, `InventoryUIResetSquadBag` / `SortItemsInBag` / rebind). Не путать с реальной потерей предметов из save/squad_bag. При правках bag UI/sort в этом change set — не усугублять; отдельный fix выносится в follow-up spec, если понадобится.

## Цели

- В `SquadBag` и `SectorStash` все `InventoryStack` сливаются до hard cap `10000` на экземпляр.
- В слотах мерка (разгрузка и прочий unit inventory) действует `item.MaxStacks` как сейчас у нормальных personal-стеков.
- В bag/stash UI показывает только `Amount` (без `/max`); в разгрузке — `Amount/MaxStacks` как сейчас.
- Перенос склад → мерк заливает до personal `MaxStacks`; остаток остаётся на складе / дробится по правилам MoveItem.
- Underscore ammo с костыльным `MaxStacks = 5000` получают personal-scale значения (в духе семейства `JAZZ_AMMO*` / калибра).

## Non-goals

- Не менять вместимость слотов (число ячеек) и class/slot filters.
- Не трогать shop `ShopStackSize` / BobbyRay мета сверх необходимости для editor max.
- Не менять loot spawn formula beyond clamping к personal `MaxStacks` (как сейчас).
- Не вводить per-item `BagMaxStacks` property в generated data (один runtime const).
- Не менять network protocol сверх уже существующих inventory NetSync путей.
- Не чинить плавающий visual-disappear баг SquadBag (см. Known issue); только не регрессировать и не принимать AC «bag UI всегда стабилен».

## Требования

- `JAZZ-INV-001-REQ-001` — `const.JazzStorageStackMax = 10000` (или эквивалент): effective max для `InventoryStack` внутри `SquadBag` и `SectorStash`.
- `JAZZ-INV-001-REQ-002` — effective max в любом unit inventory / не-storage контейнере = `item.MaxStacks`.
- `JAZZ-INV-001-REQ-003` — все пути merge/CanAddItem/AddAndStack/SortItemsInBag для storage используют storage max; для unit — personal `MaxStacks`.
- `JAZZ-INV-001-REQ-004` — `InventoryStack:GetItemSlotUI` в storage показывает только количество; вне storage — `Amount/MaxStacks` (с colorStyle как сейчас).
- `JAZZ-INV-001-REQ-005` — scope: любой `InventoryStack` (ammo, meds, parts, grenades, misc, valuables stack и т.д.).
- `JAZZ-INV-001-REQ-006` — `SectorStash` = тот же storage-режим, что `SquadBag`.
- `JAZZ-INV-001-REQ-007` — предметы с `MaxStacks = 5000` (underscore ammo костыль) переводятся на personal-scale `MaxStacks` в том же change set (`items.lua` + companion).
- `JAZZ-INV-001-REQ-008` — существующие сейвы с `Amount > MaxStacks` в разгрузке не ломаются: oversized stack допускается до взаимодействия; новый merge/transfer в unit не увеличивает выше personal max.

## Инварианты и ограничения

- Публичные class/ID предметов не меняются.
- Save schema: только `Amount`/`MaxStacks` уже сериализуются; новый property на instance не обязателен.
- Determinism: лимиты константные, без RNG.
- Loot/shop продолжают опираться на personal `MaxStacks`, не на storage cap.
- Не смешивать с mass reformatting unrelated InventoryItem.
- Visual-disappear SquadBag остаётся known floating defect до отдельного fix; evidence потери предметов должна отличать UI-only от data loss.

## Acceptance criteria

- `JAZZ-INV-001-AC-001` — static: есть единый helper effective max по контейнеру; storage call sites не читают сырой `MaxStacks` для merge cap.
- `JAZZ-INV-001-AC-002` — runtime: два стека одного ammo в SquadBag сливаются до суммарного Amount ≤ 10000; третий стек появляется только при превышении.
- `JAZZ-INV-001-AC-003` — runtime: тот же ammo в `AmmoInventory` не сливается выше personal `MaxStacks`.
- `JAZZ-INV-001-AC-004` — runtime: перенос из bag в разгрузку заполняет до personal max, остаток в bag.
- `JAZZ-INV-001-AC-005` — runtime/UI: в bag/stash на тайле только число; в разгрузке `cur/max`.
- `JAZZ-INV-001-AC-006` — runtime: SectorStash ведёт себя как bag по merge и UI.
- `JAZZ-INV-001-AC-007` — sync-audit: companion + `items.lua` + `metadata.lua` согласованы; underscore `MaxStacks=5000` убраны.
- `JAZZ-INV-001-AC-008` — human: existing save открывается; oversized personal stack не крашит UI.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: last-writer override точек merge/`CanAddItem`/`GetItemSlotUI` уже в JAZZ-owned files; новый companion code file.
- Saves: `Amount` может временно превышать новый personal `MaxStacks` после data cleanup — REQ-008.
- Network/determinism: без нового RNG; те же MoveItem/NetSync пути.
- Generated data: правка `MaxStacks` у underscore ammo + регистрация нового `Code/*.lua`.
- Cross-package: нет обязательных правок `jazz-units`/`jazz-maps` (loot Amount уже clamp к MaxStacks).
- Rollback/recovery: откат companion + MaxStacks data; сейвы с Amount≤10000 остаются валидны.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`

## Решение владельца

- Статус: `implemented`
- Кто подтвердил: project-owner
- Дата: 2026-07-30
- Зафиксированные решения:
  1. Storage cap = `10000`; UI без `/max`.
  2. Scope = все `InventoryStack`.
  3. `SectorStash` = storage как bag.
  4. Плавающий visual-disappear предметов в SquadBag (до регенерации UI) — known issue, **вне** DoD этого change; не маскировать под «предметы удалены».
- Human acceptance: owner playtest PASS 2026-07-30 (bag OK; storage→merc clamp OK after JazzClampMoveStorageToPersonal).

## Evidence

- `JAZZ-INV-001-AC-001`: `PASS` — static: `JazzGetStackMax` / storage call sites
- `JAZZ-INV-001-AC-002`: `PASS (runtime/human)` — owner: SquadBag merge/large stacks OK
- `JAZZ-INV-001-AC-003`: `PASS (runtime/human)` — owner: personal loadout stacks OK
- `JAZZ-INV-001-AC-004`: `PASS (runtime/human)` — owner: bag→merc fills to personal max, remainder in bag
- `JAZZ-INV-001-AC-005`: `PASS (runtime/human)` — owner: bag UI amount-only; loadout `cur/max`
- `JAZZ-INV-001-AC-006`: `PASS (runtime/human)` — owner: storage behavior accepted (SectorStash same path as bag)
- `JAZZ-INV-001-AC-007`: `PASS` — static sync: companion + items + metadata; underscore `MaxStacks=5000` cleared
- `JAZZ-INV-001-AC-008`: `PASS (runtime/human)` — owner: loaded from save, playtest OK

## Documentation delta

- `docs/technical/systems/inventory-items-loot-crafting.md` — dual stack limits + UI rule; кратко known visual-disappear SquadBag (не data loss).
- `docs/technical/systems/file-coverage.md` — `System_InventoryStacks.lua` loaded.
- Player-facing wiki/showcase: отдельной inventory-страницы нет; не добавлять known UI-баг в витрину.
