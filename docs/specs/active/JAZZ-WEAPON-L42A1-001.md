---
id: JAZZ-WEAPON-L42A1-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/L42A1.lua
  - jazz/WeaponIcons/L42A1*.png
  - jazz/WeaponComponents/Optics/JAZZ_L42A1_Scope.png
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/*rifle*
  - jazz/docs/tools/*mosin*
  - jazz/docs/tools/*l42a1*
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-queue.md
  - jazz/docs/specs/active/JAZZ-WEAPON-L42A1-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/L42A1*
  - jazz_assets/Entities/Meshes/L42A1*
  - jazz_assets/Entities/Materials/L42A1*
  - jazz_assets/Entities/Textures/L42A1*
  - jazz_assets/Entities/Textures/Fallbacks/L42A1*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - L42A1 localization IDs and Blender build
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-15
---

# JAZZ-WEAPON-L42A1-001: L42A1 с родным прицелом

## Проблема

Исходные OBJ и текстуры есть в локальном архиве Weapons/Sniper; MTL отсутствуют, экспорт и предмет пока отсутствуют.

## Цели

- Подготовить рабочую сборку и добавить тестовый предмет непосредственно в JAZZ.

## Non-goals

- Публикация и массовая замена существующего оружия. Выдача расширена решением 2026-09-16 в JAZZ-WEAPON-ROLLOUT-001.

## Требования

- `JAZZ-WEAPON-L42A1-001-REQ-001` — Новый L42A1: SniperRifle, тестовый Т2-1, 7.62x51; корпус и собственный прицел, минимальная модульность, звуки от M24Sniper.
- `JAZZ-WEAPON-L42A1-001-REQ-002` — сохранить исходники; экспортировать отдельные entities с attachment spots, согласовать ModItem, metadata, companion и локализацию.
- `JAZZ-WEAPON-L42A1-001-REQ-003` — иконка из Blender, направление слева направо, прозрачный фон и обводка.

## Инварианты и ограничения

- Чужие изменения сохранять. Общие файлы не записывать при пересечении с задачей «Изучить мод JAZZ»; при прерывании дождаться освобождения ресурса.
- Первоначальное исключение из магазина заменено одобренным вводом в JAZZ-WEAPON-ROLLOUT-001.
- Рабочие копии хранятся отдельно в Weapons/_l42a1_jazz_build.

## Acceptance criteria

- `JAZZ-WEAPON-L42A1-001-AC-001` — static: материалы восстановлены, геометрия и точки крепления согласованы; исходники сохранены.
- `JAZZ-WEAPON-L42A1-001-AC-002` — static: Lua и ссылки проходят проверки; RU/EN, иконка и граф ресурсов присутствуют.
- `JAZZ-WEAPON-L42A1-001-AC-003` — editor/runtime: загрузка, предмет в руках/на земле, смена доступных компонентов, выстрел/перезарядка со звуком и save/reload без ошибок.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: существующие классы, штатные компоненты без новых hooks.
- Saves: новый предмет; прежние экземпляры не меняются.
- Network/determinism: штатные данные компонентов.
- Generated data: items + metadata + companions.
- Cross-package references: jazz -> jazz_assets через существующую зависимость.
- Rollback/recovery: удалить только новые записи и ресурсы; исходные ZIP/OBJ сохранены.

## План и ownership

- Пакет-владелец: jazz — предмет и компоненты; jazz_assets — геометрия и текстуры.
- Исполнитель: текущая оружейная задача.
- Reviewer: владелец проекта.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter; перед записью перепроверить параллельную задачу.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец поручил L42A1 с собственным прицелом, затем «продолжай работу, в том числе над мосинками».
- Дата: 2026-09-15.

## Evidence

- `JAZZ-WEAPON-L42A1-001-AC-001`: `BLOCKED` — подготовка геометрии продолжается.
- `JAZZ-WEAPON-L42A1-001-AC-002`: `BLOCKED` — интеграция ещё не выполнена.
- `JAZZ-WEAPON-L42A1-001-AC-003`: `BLOCKED` — требуется игровая проверка.

## Documentation delta

- После интеграции обновить профильные страницы; непроверенное игровое поведение отмечать явно.
