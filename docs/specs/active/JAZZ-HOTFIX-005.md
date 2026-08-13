---
id: JAZZ-HOTFIX-005
status: approved
owner: project-owner
systems:
  - inventory
  - weapons-ammo
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/System_InventoryStacks.lua
  - Code/System_OR_SquadBag.lua
  - Code/System_WeaponResourceMaintenance.lua
  - Code/Inventory.lua
  - docs/specs/active/JAZZ-HOTFIX-005.md
  - docs/tools/_audit_hotfix_005.py
  - docs/tools/_bump_metadata_hotfix005.py
  - docs/tools/README.md
  - docs/technical/systems/inventory-items-loot-crafting.md
  - docs/technical/systems/weapons-ammo-components.md
  - docs/wiki/weapons-and-ammo.md
  - docs/showcase/ru/weapons-and-ammo.md
  - docs/showcase/en/weapons-and-ammo.md
  - metadata.lua
exclusive_resources:
  - jazz/metadata.lua
related_decisions:
  - none
related_specs:
  - JAZZ-INV-001
  - JAZZ-WEAPONS-002
approved_by: project-owner
---

# JAZZ-HOTFIX-005: identical remountables vanish from squad bag

## Проблема

Игрок (Sergej 1973): все сошки кроме одной исчезают из имущества отряда.

Одинаковые `JAZZ_Bipod` (`MaxStacks = 1`, свой класс) склеиваются сортировкой сумки по `item.class` в один стек `Amount=N`. Затем `JazzMarkSquadBagData` (LoadGame и каждый sort) и `JAZZ_NormalizeRemovableAttachmentStack` обрезают `Amount = 1` — уничтожая N−1 предметов. `MergeStackIntoContainer` запрещал **любой** merge remountable (защита коллиматор+компенсатор на generic class), но sort этот guard не использовал. Каталог `JAZZ_Bipod` / `_Under` / `_Galil` — разные классы, поэтому пропадают только сошки одного типа: «все кроме одной».

## Цели

- Несколько одинаковых съёмных модулей в SquadBag/SectorStash переживают sort и save/load.
- Разные `RemovableComponentId` никогда не сливаются в один стек.
- Personal loadout по-прежнему `MaxStacks` из def (обычно 1).

## Non-goals

- Восстанавливать уже уничтоженные предметы в старых сейвах.
- Менять Bobby Ray `MaxStock`, catalog `MaxStacks` defs, install/remove remount.
- Стекировать разные типы сошек (`JAZZ_Bipod` vs `JAZZ_Bipod_Under`).

## Требования

- `JAZZ-HOTFIX-005-REQ-001` — `JazzInventoryItemsCanStack(a,b)`: тот же `class`; для `JAZZ_RemovableAttachment` ещё тот же `RemovableComponentId` (fallback — class).
- `JAZZ-HOTFIX-005-REQ-002` — `_SortItemsInBag`, `MergeStackIntoContainer`, `InventoryStack:MergeStack`, `Inventory:CanAddItem` мержат только при `JazzInventoryItemsCanStack`.
- `JAZZ-HOTFIX-005-REQ-003` — `JazzMarkSquadBagData` и `JAZZ_NormalizeRemovableAttachmentStack` не обрезают `Amount` до 1 у живых стеков (пол `Amount < 1` → 1 допустим).
- `JAZZ-HOTFIX-005-REQ-004` — `JazzGetStackMax` в storage = `JazzStorageStackMax` и для remountable; на мерке — personal def.

## Инварианты и ограничения

- Public IDs `JAZZ_Bipod`, `JAZZ_RemovableAttachment`, `RemovableComponentId` не меняются.
- Коллиматор и компенсатор на generic class по-прежнему не class-merge.
- Save schema не расширяется; уже потерянные Amount не восстанавливаются.
- Новые `_G` имена только top-level `JazzInventoryItemsCanStack`.

## Acceptance criteria

- `JAZZ-HOTFIX-005-AC-001` — static: CanStack + sort/merge/CanAddItem wiring; нет clip `Amount=1` в Mark/Normalize (кроме floor `< 1`).
- `JAZZ-HOTFIX-005-AC-002` — static: `JazzGetStackMax` не форсит remountable max=1 в storage.
- `JAZZ-HOTFIX-005-AC-003` — technical + wiki + showcase RU/EN: одинаковые модули стекаются в имуществе отряда и переживают sort/load.
- `JAZZ-HOTFIX-005-AC-004` — runtime: 5× `JAZZ_Bipod` в squad bag после sort + save/load остаются Amount=5; коллиматор+компенсатор не сливаются.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ уже владеет stack/sort/merge; CommonLib совпадающего override нет.
- Saves: совместимо; сейвы, где extras уже клипнуты, не чинятся.
- Network/determinism: merge по существующим полям instance.
- Generated data: нет.
- Cross-package references: нет.
- Rollback/recovery: revert коммита `jazz`.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель / Reviewer: project-owner.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter.

## Решение владельца

- Статус: `approved`.
- Кто подтвердил: project-owner — Discord-репорт (Sergej 1973) передан в агент 2026-08-12.
- Дата: 2026-08-12.

## Evidence

- `JAZZ-HOTFIX-005-AC-001`: `PASS` (static) — `python docs/tools/_audit_hotfix_005.py`.
- `JAZZ-HOTFIX-005-AC-002`: `PASS` (static) — тот же auditor.
- `JAZZ-HOTFIX-005-AC-003`: `PASS` (docs) — inventory-items-loot-crafting, weapons-ammo-components, wiki/showcase weapons-and-ammo RU/EN.
- `JAZZ-HOTFIX-005-AC-004`: `BLOCKED` (runtime) — squad-bag sort + save/load smoke требует JA3.

## Documentation delta

- Technical: `inventory-items-loot-crafting.md` (HOTFIX-005 stacks), `weapons-ammo-components.md` (CanStack, no Amount clip).
- Player wiki + showcase RU/EN: `weapons-and-ammo.md` — одинаковые съёмные модули стекаются в имуществе отряда.
