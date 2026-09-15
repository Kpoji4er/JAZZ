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

## Инварианты и ограничения

- Чужие изменения сохранять. Общие файлы не записывать при пересечении с задачей «Изучить мод JAZZ»; при прерывании дождаться освобождения ресурса.
- Первоначальное исключение AK74M/AK105 из магазина заменено JAZZ-WEAPON-ROLLOUT-001; доступность существующих AK74/AKM не меняется.
- Рабочие копии хранятся отдельно в Weapons/_ak_jazz_build.

## Acceptance criteria

- `JAZZ-WEAPON-AK-FAMILY-001-AC-001` — static: материалы восстановлены, геометрия и точки крепления согласованы; исходники сохранены.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-002` — static: Lua и ссылки проходят проверки; RU/EN, иконка и граф ресурсов присутствуют.
- `JAZZ-WEAPON-AK-FAMILY-001-AC-003` — editor/runtime: загрузка, предмет в руках/на земле, смена доступных компонентов, выстрел/перезарядка со звуком и save/reload без ошибок.

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
