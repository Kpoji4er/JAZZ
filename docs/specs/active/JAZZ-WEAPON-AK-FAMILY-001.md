---
id: JAZZ-WEAPON-AK-FAMILY-001
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
  - jazz/InventoryItem/AK*.lua
  - jazz/WeaponIcons/AK*.png
  - jazz/WeaponComponents/Magazine/AK*.png
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/*rifle*
  - jazz/docs/tools/*mosin*
  - jazz/docs/tools/*ak*
  - jazz/docs/tools/_render_weapon_icons.py
  - jazz/docs/tools/_finalize_weapon_icons.py
  - jazz/docs/tools/_measure_ak_grip.py
  - jazz/docs/tools/_reanchor_ak_grip.py
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-queue.md
  - jazz/docs/specs/active/JAZZ-WEAPON-AK-FAMILY-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/AKR_*
  - jazz_assets/Entities/Meshes/AKR_*
  - jazz_assets/Entities/Materials/AKR_*
  - jazz_assets/Entities/Textures/AKR_*
  - jazz_assets/Entities/Textures/Fallbacks/AKR_*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - AK family localization IDs and Blender build
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-15
---

# JAZZ-WEAPON-AK-FAMILY-001: Ремастер АК и совместимые магазины

## Проблема

Исходники Weapons/AK требуют восстановления материалов, отделения модулей и согласования масштаба. AK74 и AKM уже существуют; AK74M и AK105 пока отсутствуют.

## Цели

- Подготовить рабочую сборку и добавить тестовый предмет непосредственно в JAZZ.

## Non-goals

- Публикация и массовая замена существующего оружия. Выдача и баланс расширены решением 2026-09-16 в JAZZ-WEAPON-ROLLOUT-001.

## Требования

- `JAZZ-WEAPON-AK-FAMILY-001-REQ-001` — Ремастер существующих AK74 и AKM с сохранением ID и базовых статов; новые AK74M и AK105 на базе соответствующих калибра и класса. Общие магазины 5.45: 30/45, 7.62: 30/40/75. Сохранять существующие component IDs, исключить совместимость между калибрами, проверить штатные и увеличенные магазины на всех затронутых АК. Допустимы подходящие vanilla/existing assets. Новые образцы получают тестовые статы и FX от AK74.
- `JAZZ-WEAPON-AK-FAMILY-001-REQ-002` — сохранить исходники; экспортировать отдельные entities с attachment spots, согласовать ModItem, metadata, companion и локализацию.
- `JAZZ-WEAPON-AK-FAMILY-001-REQ-003` — иконка из Blender, направление слева направо, прозрачный фон и обводка.
- `JAZZ-WEAPON-AK-FAMILY-001-REQ-004` — иконки AK74M и AK105 приводятся к формату рукодельных: ровно 324×165 RGBA, дуло вправо, прозрачный фон, сплошное почти чёрное кольцо 3–6 px плюс мягкий ореол, без белой каймы. Рукодельные `AK74.png`, `AKM.png`, `UMP45.png` и геометрия AK74/AKM не затрагиваются.
- `JAZZ-WEAPON-AK-FAMILY-001-REQ-005` — origin корпуса `AKR_AK74M` и `AKR_AK105` сдвигается так, чтобы пистолетная рукоять совпала с принятым AK74: рука на рукояти, не на магазине. Сдвигаются только body mesh и spots; магазины, приклад, цевьё и дуло остаются в своих entity. `ModifyRightHandGrip` не ставится. Решение владельца: скрины idle 2026-09-20.

## Инварианты и ограничения

- Чужие изменения сохранять. Общие файлы не записывать при пересечении с задачей «Изучить мод JAZZ»; при прерывании дождаться освобождения ресурса.
- Первоначальное исключение AK74M/AK105 из магазина заменено JAZZ-WEAPON-ROLLOUT-001; доступность существующих AK74/AKM не меняется.
- Рабочие копии хранятся отдельно в Weapons/_ak_jazz_build.

## Acceptance criteria

- `JAZZ-WEAPON-AK-FAMILY-001-AC-001` — static: материалы восстановлены, геометрия и точки крепления согласованы; исходники сохранены.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-002` — static: Lua и ссылки проходят проверки; RU/EN, иконка и граф ресурсов присутствуют.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-003` — editor/runtime: загрузка, предмет в руках/на земле, смена доступных компонентов, выстрел/перезарядка со звуком и save/reload без ошибок.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-004` — static: `WeaponIcons/AK74M.png` и `AK105.png` имеют размер 324×165 RGBA, а замер доли почти чёрных пикселей по глубине от края силуэта показывает сплошное кольцо не тоньше 3 px.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-005` — static: `.ent` box и spot `Magazine` корпуса сдвинуты на согласованный offset (AK74M +4.63/−1.11 см, AK105 +3.66/+0.35 см по X/Z); human/runtime: в idle правая рука на пистолетной рукояти.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: существующие классы, штатные компоненты без новых hooks.
- Saves: существующие AK74/AKM сохраняют ID; обновлённые визуалы распространяются и на старые экземпляры. AK74M/AK105 новые.
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
- Кто подтвердил: владелец поручил ремастер АК74/АКМ, сборку АК74М/АК105 и общие магазины, затем подтвердил «делай все», с приоритетом задачи по изучению мода.
- Дата: 2026-09-15.

## Evidence

### Хват AK74M/AK105, 2026-09-20

- `JAZZ-WEAPON-AK-FAMILY-001-AC-005`: `PASS` static — idle-скрины показали руку на магазине у AK74M и чуть впереди рукояти у AK105. Центр рукояти относительно origin: AK74 +0.39/−2.21 см, AK74M −4.24/−1.10 см, AK105 −3.27/−2.56 см. Корпус сдвинут на +4.63/−1.11 и +3.66/+0.35 см; новый box AK74M `-4.400 .. 60.369`, Magazine 13.630 (ванильный AK74 Magazine 14.035); AK105 box `-5.647 .. 50.416`, Magazine 12.384. Модули не менялись. Runtime/human — после reload с диска.

### Иконки 324×165 с обводкой, 2026-09-19

- `JAZZ-WEAPON-AK-FAMILY-001-AC-004`: `PASS` static — `docs/tools/_render_weapon_icons.py` рендерит в 2× с композицией `DilateErode` по альфе → почти чёрный слой → `AlphaOver` под картинку, плюс размытая широкая копия как ореол; `_finalize_weapon_icons.py` сводит к 324×165 через LANCZOS и печатает профиль обводки. Доля почти чёрных пикселей по глубине от края силуэта — AK74M: 1 px 1.00, 2 px 1.00, 3 px 0.81, 4 px 0.53; AK105: 1.00 / 1.00 / 0.86 / 0.73; эталон AK74: 1.00 / 0.96 / 0.60 / 0.32. Прежние 512×256 давали около 1.5 px. На глубине от 4 px значение завышено собственной чёрной краской моделей. Геометрия AK74M и AK105 не менялась, рукодельные `AK74.png`, `AKM.png`, `UMP45.png` не тронуты.

### Ванильные референсы и offline fit, 2026-09-16

- Примерка расширена на все пять доступных прицелов: PSO/Kobra/PKAA/tyulpan/NSPU. GP30, GP45, Bipod30 и четыре дополнительных прицела дают 28 отдельных видов для двух АК. У tyulpan в сцене используется основной меш: декодер не поддержал дополнительный пустой submesh; исходный игровой ресурс не изменён. Это ограничение offline-проверки, не исправление игрового HGM.

- Из игровых HPK извлечены 1584 файла Weapon_/WeaponAtt* (31 211 095 байт) в отдельный `_vanilla_reference`, с manifest SHA-256. Игровые архивы не изменялись.
- HGM reader декодировал 410/411 LOD0-мешей в JSON/OBJ; Weapon_CAR15_mesh.hgm остался только исходным HGM из-за неподдержанного layout. UV/материалы в OBJ не перенесены, текстуры не подменялись.
- Ванильные точки АК74/АК47/АКС74У сняты через временные объекты движка в vanilla-spots.tsv; объекты удалены. Для Blender используются калиброванные оси (-Y,-X,Z) и метры.
- Построены AK74M_attachment_fit.blend и AK105_attachment_fit.blend: установленная геометрия и spots, реальные GP/Bipod HGM, существующие PKAA/AKSeriaMount и общий магазин 45. Варианты GP30/GP45/Bipod30 рендерятся раздельно с обеих сторон. Эта проверка не закрывает анимацию удержания, звуки и editor round-trip.

### Исправление замечаний к модулям, 2026-09-15

- АК74М: магазин, приклад и цевьё выделены целыми связными частями исходной сетки. Прежняя отсечка пересекала губки магазина и пистолетную рукоятку; теперь рукоятка сохранена целиком. Убраны случайно попадавшие в магазин торцевые части цевья.
- АК105: цевьё выделено целыми частями; передние металлические детали остаются в корпусе. Прежняя плоскость пересекала цевьё и забирала части переднего узла.
- Для обеих моделей пересчитаны General/Scope/Mount относительно боковой планки, Under/Bipod относительно ствола и размеров донорских модулей. Это новая проверяемая сборка, а не подтверждённая пользователем посадка.
- Обе инвентарные иконки и иконки штатных магазинов перерендерены с меньшей интенсивностью света (25 вместо 85). Исходные иконки АК74/АКМ сохраняются.
- Официальный AssetsProcessor успешно собрал обе семьи; `_apply_ak_visual_revision.py` заменил 18 существующих ресурсов АК74М и 10 АК105 с резервными копиями. Регистрация новых ID не потребовалась.
- `_check_weapon_imports.py`: PASS. Live DAP `AsyncLoadAdditionalEntities` в GameTimeThread загрузил ровно 12 обновлённых сущностей; отчёт `AppData/jazz_ak_visual_revision.txt` подтверждает завершение. Проверка внешнего вида навесного в кабинете пока не закрыта.

- `JAZZ-WEAPON-AK-FAMILY-001-AC-001`: `FAIL` — пользователь подтвердил плохой разрез магазина и посадку ГП, оптики и сошек. Ремастеры АК74/АКМ сняты с активных предметов: возвращены прежние Entity, девять визуальных привязок модулей, дульные слоты и исходные иконки 324×165. Новые ресурсы сохранены для доработки. АК74М/АК105 остаются непроверенными прототипами.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-002`: `PASS` static — после возврата выполнены `_validate_items_quick.py` и `_check_weapon_imports.py`: Lua/ModItem согласованы, графы ресурсов и общие магазины сохранены, активные модули АК74/АКМ больше не ссылаются на AKR_.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-003`: `BLOCKED` — создание временных оружий и смена компонентов проходили в движке, но это не проверка посадки. Визуальная проверка пользователем выявила дефекты; после возврата старых АК требуется reload с диска и повторная проверка. Игра автоматически не перезагружалась.

## Documentation delta

- После интеграции обновить профильные страницы; непроверенное игровое поведение отмечать явно.
