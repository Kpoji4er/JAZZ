---
id: JAZZ-INV-003
status: implemented
owner: project-owner
systems:
  - inventory-items-loot-crafting
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/VanillaDesyncFixes.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/docs/specs/active/JAZZ-INV-003.md
  - jazz/docs/technical/systems/inventory-items-loot-crafting.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/explosives-traps-heavy-weapons.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/tools/_audit_craft_ammo_homemade.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-INV-002
approved_by: project-owner
---

# JAZZ-INV-003: CraftAmmo только кустарные патроны JAZZ

## Проблема

Операция «Изготовление патронов» показывает фабричные ванильные рецепты (`556_Basic`, `9mm_AP`, `12gauge_Buckshot`, …). Папка `RemoveCraft` прячет часть из них через фейковый `_TestQuest`, но не полный список Ammo-группы. Игрок крафтит заводской FMJ/AP вместо кустарных `JAZZ_AMMO_*_Crafted`.

## Цели

- В `CraftAmmo` видны только кустарные рецепты JAZZ (`ResultItem` = `JAZZ_AMMO_*_Crafted`) и JAZZ-соль (`JAZZ_AMMO_12gauge_Saltshot`).
- Фабричные ванильные и `RemoveCraft`-override рецепты не попадают в picker.
- `CraftExplosives` не меняется.
- Предметы фабричных патронов (лут, Bobby, сейвы) остаются.

## Non-goals

- Не удалять `RemoveCraft` ModItems (остаются как override ванильных ID).
- Не трогать `RecipeDef` брони.
- Не менять боевые статы кустарных предметов / `AmmoCraftedColor`, кроме Rel/jam (owner 2026-08-23: между Poor и FMJ, см. WEAPONS-008 REQ-005).

## Требования

- `JAZZ-INV-003-REQ-001` — `Jazz_IsAllowedCraftAmmoRecipe`: true только для `JAZZ_AMMO_*_Crafted` и `JAZZ_AMMO_12gauge_Saltshot`.
- `JAZZ-INV-003-REQ-002` — `SectorOperationFillItemsToCraft` при `CraftAmmo` не кладёт в `g_RecipesCraftAmmo` рецепты вне allow-list.
- `JAZZ-INV-003-REQ-003` — `SectorOperations_CraftAdditionalResources` при `CraftAmmo` суммирует ингредиенты только allow-list рецептов.
- `JAZZ-INV-003-REQ-004` — есть рецепт `JAZZ_9x39_Crafted` → `JAZZ_AMMO_9x39_Crafted` (калибр был без крафта).
- `JAZZ-INV-003-REQ-005` — technical + wiki + showcase RU/EN описывают, что крафт патронов — только кустарные / соль, и батч = 100 Parts + порох, выход от калибра.
- `JAZZ-INV-003-REQ-006` — каждый `JAZZ_Ammo` рецепт: **100 Parts** + BlackPowder; `ResultItem.amount` по калибру (owner 2026-08-23): 9×18=50, 9×19=40, .45=30, 5.45/5.56/7.62×39=30, 7.62×51/54=20, 9×39=20, соль=20. Порох: пистолет/соль 1, промежуточные + 9×39 + 7.62×51 = 2, 7.62×54R = 3.

## Инварианты и ограничения

- `CraftExplosives` и гранаты/миномёты без изменений.
- Кустарные предметы и `AmmoCraftedColor` без смены статов, кроме Rel/jam (WEAPONS-008, 2026-08-23).
- Старый сейв с очередью фабричного рецепта может докрафтить уже поставленную позицию; новые позиции не добавить.
- Публичные ID кустарных рецептов не переименовывать.

## Acceptance criteria

- `JAZZ-INV-003-AC-001` — static: helper + FillItemsToCraft filter + AdditionalResources wrap.
- `JAZZ-INV-003-AC-002` — static: `items.lua` JAZZ_Ammo recipes все allow-list; есть `JAZZ_9x39_Crafted`; все 100 Parts + qty по REQ-006; `_validate_items_quick.py` OK.
- `JAZZ-INV-003-AC-003` — runtime/human: CraftAmmo показывает кустарные (+ соль), без ванильного 5.56/9mm FMJ.
- `JAZZ-INV-003-AC-004` — docs sync в том же change set.
- `JAZZ-INV-003-AC-005` — static: 7.62×51/54 имеют `ResultItem.amount` (не default 1).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ уже заменяет `SectorOperationFillItemsToCraft`; filter на этом override. AdditionalResources — wrap ванили.
- Saves: новые крафты фабричных патронов недоступны. Предметы в инвентаре валидны.
- Network/determinism: тот же allow-list на всех клиентах.
- Generated data: один новый `ModItemCraftOperationsRecipeDef` + `ModResourcePreset`.
- Cross-package: нет.
- Rollback/recovery: снять filter в `VanillaDesyncFixes.lua`.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `items.lua`, `metadata.lua`

## Решение владельца

- Статус: approved → implemented (запрос 2026-08-23: оставить только кустарные JAZZ, остальные убрать)
- Цены (2026-08-23): батч = 100 Parts + порох, количество от калибра (REQ-006)
- Кто подтвердил: project-owner
- Дата: 2026-08-23

## Evidence

- `JAZZ-INV-003-AC-001`: `PASS` (static) — `_audit_craft_ammo_homemade.py`
- `JAZZ-INV-003-AC-002`: `PASS` (static) — audit + `_validate_items_quick.py` (100 Parts + qty)
- `JAZZ-INV-003-AC-003`: `BLOCKED` (runtime) — нужна проверка в игре
- `JAZZ-INV-003-AC-004`: `PASS` (docs) — technical / wiki / showcase RU+EN
- `JAZZ-INV-003-AC-005`: `PASS` (static) — 7.62×51/54 `amount` 20

## Documentation delta

- `docs/technical/systems/inventory-items-loot-crafting.md`
- `docs/technical/systems/weapons-ammo-components.md`
- `docs/technical/systems/explosives-traps-heavy-weapons.md`
- `docs/wiki/weapons-and-ammo.md`
- `docs/showcase/ru/weapons-and-ammo.md`
- `docs/showcase/en/weapons-and-ammo.md`
