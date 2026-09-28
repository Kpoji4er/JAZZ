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
  - jazz/docs/tools/_apply_weapon_geometry_update.py
  - jazz/docs/tools/_overlay_weapon_length.py
  - jazz/docs/tools/_annotate_scale_overlay.py
  - jazz/docs/tools/_render_weapon_icons.py
  - jazz/docs/tools/_finalize_weapon_icons.py
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
- `JAZZ-WEAPON-L42A1-001-REQ-004` — винтовка масштабируется относительно origin entity, поэтому хват правой руки остаётся на месте, а spots `Muzzle`, `Hand_l_grip`, `Trigger`, `Magazine` и `Scope` пересчитываются тем же множителем. Эталон длины — принятый AK74 в его игровом размере; при результате короче AK импорт не выполняется. Масштаб задан владельцем как +10% к исходным 1102 мм, то есть 1212 мм при AK74 847 мм. Это сознательно крупнее натуральной пропорции: реальные 1181 / 943 мм дали бы 1.252×, а принято 1.430×.
- `JAZZ-WEAPON-L42A1-001-REQ-005` — `ModifyRightHandGrip = true` присутствует одновременно в `items.lua` и в `InventoryItem/L42A1.lua`; эталон хвата — `InventoryItem/Mosin.lua`.
- `JAZZ-WEAPON-L42A1-001-REQ-006` — иконка инвентаря ровно 324×165 RGBA, дуло вправо, прозрачный фон, обводка сопоставима с рукодельной `WeaponIcons/AK74.png`: сплошное почти чёрное кольцо 3–6 px плюс мягкий ореол, без белой каймы.

## Инварианты и ограничения

- Чужие изменения сохранять. Общие файлы не записывать при пересечении с задачей «Изучить мод JAZZ»; при прерывании дождаться освобождения ресурса.
- Первоначальное исключение из магазина заменено одобренным вводом в JAZZ-WEAPON-ROLLOUT-001.
- Рабочие копии хранятся отдельно в Weapons/_l42a1_jazz_build.

## Acceptance criteria

- `JAZZ-WEAPON-L42A1-001-AC-001` — static: материалы восстановлены, геометрия и точки крепления согласованы; исходники сохранены.
- `JAZZ-WEAPON-L42A1-001-AC-002` — static: Lua и ссылки проходят проверки; RU/EN, иконка и граф ресурсов присутствуют.
- `JAZZ-WEAPON-L42A1-001-AC-003` — editor/runtime: загрузка, предмет в руках/на земле, смена доступных компонентов, выстрел/перезарядка со звуком и save/reload без ошибок.
- `JAZZ-WEAPON-L42A1-001-AC-004` — static: длина entity `L42A1` соответствует согласованному множителю и превышает длину AK74; spots масштабированы тем же коэффициентом; `ModifyRightHandGrip = true` в обоих представлениях.
- `JAZZ-WEAPON-L42A1-001-AC-005` — human: масштабный оверлей side и top против AK74 в одном метрическом кадре с линейкой подтверждает согласованную длину.
- `JAZZ-WEAPON-L42A1-001-AC-006` — runtime: в руках мерка винтовка читается длиннее AK74, хват правой руки не разъехался, левая рука ложится на `Hand_l_grip`.

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
- `JAZZ-WEAPON-L42A1-001-AC-004`: `PASS` static — пересборка с `--scale 1.10` даёт 1212.1 мм против AK74 847.3 мм, то есть 1.430×; `.ent` box `-42.648 .. 78.558` подтверждает длину. Spots: `Muzzle` 78.54, `Hand_l_grip` 22.0, `Scope` 6.05, `Trigger` 2.75, `Magazine` 9.9 см. `ModifyRightHandGrip = true` уже присутствовал и в `items.lua`, и в companion — правка не требовалась.
- `JAZZ-WEAPON-L42A1-001-AC-005`: `PASS` human — `docs/tools/_overlay_weapon_length.py` и `_annotate_scale_overlay.py`, ортографический кадр 1168 px/м с метровой линейкой, выравнивание по дулу и по `Hand_l_grip`, варианты +5 / +7.2 / +10 % показаны владельцу перед выбором.
- `JAZZ-WEAPON-L42A1-001-AC-006`: `BLOCKED` — в игре не проверялось.

## Documentation delta

- После интеграции обновить профильные страницы; непроверенное игровое поведение отмечать явно.


## Уточнение ремонта 2026-09-26

Владелец разрешил исправление подтверждённых находок («правь», «да»). W02: поднять IK-точку левой руки на 25 мм относительно установленной версии: привязка к нижней поверхности ложи оставляет ладонь ниже оружия в Prone Aim. Геометрию и игровые характеристики не менять. Это корректировка существующего требования хвата. Проверка точки и сохранности остальных ресурсов — static; визуальная приёмка после запуска владельцем — BLOCKED.

Evidence 2026-09-26: PASS static — изменён только Hand_l_grip в существующем .ent; восстановление старой строки даёт побайтное совпадение с backup. Mesh/material/registration не менялись. Runtime BLOCKED до повторной проверки владельцем.
