---
id: JAZZ-WEAPON-STG44-001
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: not-required
write_set:
  - jazz/InventoryItem/STG44.lua
  - jazz/items.lua
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/showcase/*/weapons-and-ammo.md
  - jazz/docs/tools/*stg44*
  - jazz/docs/tools/README.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner current conversation 2026-09-27
---

# JAZZ-WEAPON-STG44-001: StG44 на Т1-2

## Проблема

В companion/items StG44 имеет comment Tier 2-1, в CSV tier 1-2 и ранний loot Amount 12. Владелец требует единый Т1-2.

## Цели

- StG44 согласованно относится к Т1-2.

## Non-goals

- Статы, цена, Bobby shop Tier, другие предметы и полная регенерация лута.

## Требования

- `JAZZ-WEAPON-STG44-001-REQ-001` — Установить Tier 1-2 в comment предмета и ModItem. Каталог и loot уже 1-2, их не менять.

## Инварианты и ограничения

- Сохранить все боевые параметры, остальные записи и публичные ID.

## Acceptance criteria

- `JAZZ-WEAPON-STG44-001-AC-001` — static: comment и CSV равны 1-2, затронутый loot соответствует генератору; Lua и docs проходят проверки.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: механика не меняется.
- Saves: без миграций.
- Network/determinism: без изменений.
- Generated data: только comment items и companion; metadata/IDs прежние.
- Cross-package references: без изменений.
- Rollback/recovery: backup затронутых файлов.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель: текущая задача.
- Reviewer: статическая сверка точечного diff.
- Declared write set: frontmatter.
- Exclusive resources: jazz/items.lua.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец, «т1-2 нормально», уточнение последним сообщением.
- Дата: 2026-09-27.

## Evidence

- `JAZZ-WEAPON-STG44-001-AC-001`: `PASS` — после закрытия игры владельцем изменены только две строки comment в items/companion; каталог сохраняет Т1-2, loot не менялся. Lua compile и `_validate_items_quick.py` PASS, metadata содержит существующий companion. Diff сверён с резервными копиями. Editor save/reload round-trip ещё не выполнялся; не считать это релизной приёмкой.

## Documentation delta

- Каталог/wiki уже описывают Т1-2; функционального documentation delta нет. Исправляется устаревший comment. README инструмента обновлён.

Последнее решение владельца отменяет Т1-3: оставить существующий каталог/loot Т1-2 и устранить только устаревший comment Т2-1.
