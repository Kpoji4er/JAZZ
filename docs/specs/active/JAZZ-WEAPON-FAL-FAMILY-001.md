---
id: JAZZ-WEAPON-FAL-FAMILY-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/FNFAL.lua
  - jazz/InventoryItem/JAZZ_FNFAL_Tactical.lua
  - jazz/InventoryItem/JAZZ_MagLarge_20_30_FAL.lua
  - jazz/InventoryItem/JAZZ_MagNormalFine_FAL.lua
  - jazz/WeaponIcons/JAZZ_FNFAL_Tactical.png
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/Localization/*
  - jazz/docs/specs/active/JAZZ-WEAPON-FAL-FAMILY-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/data/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/design/weapons-import-queue.md
  - jazz/docs/tools/_fal_*
  - jazz/docs/tools/README.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/FNFAL_ParaStk_*
  - jazz_assets/Entities/JAZZ_FNFAL_Tac*
  - jazz_assets/Entities/Meshes/FNFAL_ParaStk_*
  - jazz_assets/Entities/Meshes/JAZZ_FNFAL_Tac*
  - jazz_assets/Entities/Materials/FNFAL_ParaStk_*
  - jazz_assets/Entities/Materials/JAZZ_FNFAL_Tac*
  - jazz_assets/Entities/Textures/FNFAL_ParaStk_*
  - jazz_assets/Entities/Textures/JAZZ_FNFAL_Tac*
  - jazz-units/items.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz-units/items.lua
  - FAL localization IDs and Blender build
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-19
---

# JAZZ-WEAPON-FAL-FAMILY-001: два FAL — классика Tier 2 и тактик Tier 3

## Проблема

В моде один FAL: `FNFAL`, Tier 3, на ванильной сущности `Weapon_FNFAL`. Он занимает единственную ячейку между Tier 2 (AR10, M14SAW) и Tier 4 (G3A3, G3A4) и не различает два очень разных облика оружия — классический с деревянной мебелью и современный на планках.

Отдельно обнаружены два дефекта текущих данных:

- Компоненты `JAZZ_StockLightFolded` и `JAZZ_StockLightUnFolded` уже содержат запись `ApplyTo = "FNFAL"`, но обе указывают на одну и ту же сущность `WeaponAttA_StockFNFal_01`. Складывание визуально не происходит. Сам слот Stock у `FNFAL` эту пару не перечисляет, поэтому записи недостижимы.
- У съёмных предметов `JAZZ_MagLarge_20_30_FAL` и `JAZZ_MagNormalFine_FAL` иконки `InventoryItem` указывают на чужие семейства: `galil_magazine_large` и `m16_magazine`. На уровне самих компонентов иконки уже правильные.

Донорские архивы проверены офлайн: `FN FAL _Tactical_.zip` и `FN FAL 50.63 _Para_.zip` — один комплект одного автора, ядро ствольной коробки совпадает вершина-в-вершину, Para отличается равномерным масштабом 1.9372. Модули приходят отдельными объектами, резать геометрию не требуется.

## Цели

- Развести классический и тактический FAL по тирам и облику, сохранив существующий ID и совместимость сохранений.
- Сделать para-приклад действительно складным через уже существующую механику `JAZZ_StockLightFolded` / `JAZZ_StockLightUnFolded`.
- Починить иконки съёмных FAL-магазинов.

## Non-goals

- Магазины L1A1 и L2A1 из `free-modular-l1a1-slr.zip`. Замер выполнен: губки сходятся в пределах миллиметра, но L2A1 на 21 процент длиннее текущего тридцатиместного и тянет чужое текстурное семейство. Отложено.
- `FN FAL _G-Series_.zip` как донор внешнего вида: две сетки без единой текстуры.
- Para-цевьё и полноразмерная планка из архива Para как отдельные компоненты. Геометрия сохраняется как заготовка, в этот scope не входит.
- Третий weapon ID, в том числе L1A1 SLR.
- Изменение G3A3 и G3A4.

## Требования

- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-001` — `FNFAL` сохраняет ID, класс `BattleRifle` и ванильную сущность `Weapon_FNFAL`, переезжает на Tier 2: `Cost` 6300, `Reliability` 55, `BaseJamChance` 0, `RestockWeight` 70. Урон, дальность, отдача, темп и число слотов не меняются.
- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-002` — слот Stock у `FNFAL` содержит `JAZZ_StockNormal`, `JAZZ_StockLightUnFolded` и `JAZZ_StockLightFolded` при `DefaultComponent = "JAZZ_StockLightUnFolded"`. `JAZZ_StockLight` из списка исключается. Разложенный визуал — ванильный `WeaponAttA_StockFNFal_01`; сложенный — `FNFAL_ParaStk_fld`.
- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-003` — в `jazz_assets` появляются две различные сущности `FNFAL_ParaStk_unfld` и `FNFAL_ParaStk_fld`, построенные из объекта `model_9` архива Para. Сложенное состояние получается поворотом островов тяг и затыльника вокруг петли, без новой лепки. Визуалы `ApplyTo = "FNFAL"` в обоих компонентах переводятся на соответствующие новые сущности.
- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-004` — новый предмет `JAZZ_FNFAL_Tactical`, класс `BattleRifle`, Tier 3, `Cost` 8500, `Reliability` 70, `BaseJamChance` -15, `Recoil` 36, `AimAccuracy` 14, `WeaponRange` 57. `Damage` равен классике и составляет 34. Слот Barrel дополнительно содержит `JAZZ_BarrelLong` и `JAZZ_BarrelLongImproved`. Слот Handguard закрыт с RIS-цевьём в дефолте. Список компонентов слота Scope совпадает с `FNFAL` посимвольно.
- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-005` — Bobby Ray: `JAZZ_FNFAL_Tactical` **in**, Tier 3, `RestockWeight` 60; `FNFAL` остаётся **in** с Tier 2.
- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-006` — иконки `InventoryItem` у `JAZZ_MagLarge_20_30_FAL` и `JAZZ_MagNormalFine_FAL` меняются на ванильные `UI/Icons/Upgrades/fnfal_mag_ergo_large` и `fnfal_mag_ergo_normal`.
- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-007` — лут Легиона содержит оба приклада классического `FNFAL`: обычный `JAZZ_StockNormal` и para `JAZZ_StockLightUnFolded`. Существующий `BattleRifles_FNFALLight` переводится с мёртвого `JAZZ_StockLight` на `JAZZ_StockLightUnFolded` и подключается в `LegionT2_BattleRifle`, `LegionT2_BattleRifle_Elite` и `LegionMercenary_AssaultRifle`. Остальные легионные FAL-дефы явно ставят `JAZZ_StockNormal`, чтобы дефолт Para не закрасил весь пул.
- `JAZZ-WEAPON-FAL-FAMILY-001-REQ-008` — `JAZZ_FNFAL_Tactical` появляется в лутлистах Легиона на T2-4 (`LegionT2_BattleRifle`, `_Elite`, `LegionMercenary_AssaultRifle`) и в пулах Адониса `Adonis_AssaultRifle` / `AdonisElite_AssaultRifle`. Новые LootDef: `BattleRifles_FNFAL_Tactical`, `_AP`, `_Scope`; `Adonis_FNFAL_Tactical`, `_Reflex`.

## Инварианты и ограничения

- Публичный ID `FNFAL` и его `Entity` не меняются; существующие экземпляры в сохранениях остаются валидными.
- Оба FAL имеют одинаковый `Damage` и одинаковый список прицелов. Различие несёт облик, тир, отдача, надёжность и доступность длинного ствола.
- Семейства магазинов не смешиваются: FAL отдельно от AR15 и АК.
- G3A3 и G3A4 остаются Tier 4 и не редактируются.
- В рабочей копии `jazz` присутствует посторонний незакоммиченный рефактор `items.lua`. Его изменения сохраняются; правки вносятся точечно, без массовой перегенерации и переформатирования.
- Шесть дублирующих companion-файлов `InventoryItem/*.lua`, не зарегистрированных в `metadata.code` (`Auto5_quest`, `Galil_FlagHill`, `GoldenGun`, `LionRoar`, `TexRevolver`, `Winchester_Quest`), являются дореформенным дефектом и в этом изменении не трогаются.

## Acceptance criteria

- `JAZZ-WEAPON-FAL-FAMILY-001-AC-001` — static: `FNFAL` в `items.lua` и companion согласованы и несут Tier 2 с новыми `Cost`, `Reliability`, `BaseJamChance`; `_validate_items_quick.py` завершается кодом 0.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-002` — static: `JAZZ_StockLightFolded` и `JAZZ_StockLightUnFolded` для `FNFAL` ссылаются на **разные** сущности; в `jazz_assets` присутствуют `.ent`, `.lua`, материалы и текстуры обеих.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-003` — runtime: в кабинете модификации переключение между сложенным и разложенным прикладом меняет видимую геометрию, приклад сидит на петле без зазора и без пересечений с коробкой.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-004` — static: `JAZZ_FNFAL_Tactical` зарегистрирован в `items.lua`, `metadata.lua` и companion; иконка 324×165 с обводкой присутствует; строки RU и EN заведены.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-005` — runtime: оба FAL берутся в руки, стреляют и перезаряжаются со звуком, смена компонентов во всех слотах проходит без ошибок, save и reload чистые.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-006` — static: иконки обоих съёмных FAL-магазинов указывают на `fnfal_mag_ergo_*`; аудиты цен Bobby Ray проходят.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-007` — static: `BattleRifles_FNFALLight` ставит `JAZZ_StockLightUnFolded`; `BattleRifles_FNFAL` и легионные FAL-дефы с апгрейдами ставят `JAZZ_StockNormal`; `FNFALLight` входит в три легионных пула выше.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-008` — static: три `BattleRifles_FNFAL_Tactical*` зарегистрированы в `jazz-units` metadata и входят в три легионных T2-4 пула; `Adonis_FNFAL_Tactical` и `_Reflex` входят в `Adonis_AssaultRifle` и `AdonisElite_AssaultRifle`.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: используются существующие классы и компоненты, новых hooks нет. Ванильные сущности FAL не переопределяются.
- Saves: `FNFAL` сохраняет ID и сущность. Смена Tier 3 на 2 меняет только витрину и цену. Экземпляры с установленным `JAZZ_StockLight` после исключения компонента из списка получают `DefaultComponent`; поведение проверить в runtime.
- Network/determinism: штатные данные компонентов, собственного RNG нет.
- Generated data: `items.lua`, `metadata.lua` и companion в обоих пакетах — одна транзакция.
- Cross-package references: `jazz` ссылается на `jazz_assets` через существующую зависимость. `jazz-units` ссылается на публичные ID компонентов `JAZZ_StockNormal` / `JAZZ_StockLightUnFolded` и предмета `FNFAL`.
- Rollback/recovery: удалить записи `JAZZ_FNFAL_Tactical` и новые сущности приклада, вернуть `FNFAL` на Tier 3 и прежний список Stock. Исходные архивы не изменялись.

## План и ownership

- Пакет-владелец: `jazz` — предметы, компоненты, витрина, локализация; `jazz_assets` — геометрия, материалы, текстуры; `jazz-units` — лут Легиона (`BattleRifles_FNFAL*`, пулы `LegionT2_*` / `LegionMercenary_*`).
- Исполнитель: текущая оружейная задача.
- Reviewer: владелец проекта.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter. Перед записью в `items.lua` перепроверять посторонний незакоммиченный diff.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец выбрал два ствола (низкотирная классика и хайтирный модульный при G3 тиром выше), подтвердил одинаковый список прицелов, складной para-приклад, понижение надёжности классики и починку иконок магазинов, затем ответил «делай».
- Дата: 2026-09-19; лут Легиона с обоими прикладами — 2026-09-20 («сделай в луте легиона оба варианта»); тактический FAL в лутлистах Легиона и Адониса — 2026-09-20.

## Evidence

### Офлайн-разведка доноров, 2026-09-19

- Ядро ствольной коробки в архивах Tactical, Para и G-Series — одна сетка: после merge by distance крупнейший остров в каждом составляет 1393 вершины с габаритом 4.07 × 27.57 × 8.59; Para отличается равномерным множителем 1.9372, наложение совпадает без остатка.
- Сырые OBJ не сварены: база Para имеет 37 712 вершин и 12 267 несвязных оболочек, после сварки 7 089 вершин и 42 острова. Нарезка по островам допустима только после сварки.
- `model_9` архива Para (складной приклад) после сварки даёт 1238 вершин и 11 островов; тяги с затыльником отделены от шарнирного блока, что делает сложенную позу поворотом, а не лепкой.
- Замер магазинов в сантиметрах: ванильные FAL 20 и 30 местные — толщина 2.61; архивные FAL — 2.86 и 2.67; L1A1 — 2.55 и 2.54. Длина L2A1 составляет 22.2 против 18.3 у текущего тридцатиместного.

### Сборка ресурсов и данных, 2026-09-19

- Споты FNFAL офлайн недоступны: `vanilla-spots.tsv` покрывает только три АК, а в декодированном `Weapon_FNFAL_mesh.json` поле `bones` пустое. Поэтому собранные превью «коробка плюс навесное» недостоверны, и владелец принял решение проверять посадку в игре. Вместо спотов каждая новая деталь посажена по стыковочному торцу соответствующего ванильного навесного меша, который авторен вокруг спота.
- Четыре сущности собраны через `BlenderExport.py` и официальный `AssetsProcessor`, застейджены `_prepare_rifle_assets.py` и установлены в `jazz_assets`: `FNFAL_ParaStk_unfld` (2290 тр.), `FNFAL_ParaStk_fld` (2290 тр.), `JAZZ_FNFAL_TacHandguard` (3874 тр.), `JAZZ_FNFAL_TacStock` (1138 тр.). Передний торец разложенного приклада совпал с ванильным до 0.0001 м. AssetsProcessor выдал предупреждения `normals with 0 length` и `Missmatched FBX file and SDK versions`; обе сборки при этом завершились успешно.
- Тактический ствол не получает собственной сущности оружия: он остаётся на `Weapon_FNFAL` и различается компонентами. Поскольку `WeaponComponentVisual.ApplyTo` сопоставляется с id предмета, все 52 визуала FNFAL зеркалированы на новый id, приклад и цевьё подменены на тактические.

- `JAZZ-WEAPON-FAL-FAMILY-001-AC-001`: `PASS` static — `FNFAL` несёт Tier 2, Cost 6300, Reliability 55, BaseJamChance 0 в `items.lua` и companion; `_validate_items_quick.py` exit 0.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-002`: `PASS` static — `JAZZ_StockLightUnFolded` и `JAZZ_StockLightFolded` ссылаются на разные сущности; `.ent`, `.lua`, материалы и DDS с фолбэками присутствуют в `jazz_assets`.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-003`: `PARTIAL` human — владелец подтвердил, что приклад сидит нормально; formal DAP/runtime кабинет ещё не прогонялся.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-004`: `PARTIAL` — ModItem, companion, `metadata.code` и иконка 324×165 на месте; строки RU/EN 990002700–704 ещё не заведены.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-005`: `BLOCKED` — требует runtime.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-006`: `PASS` static — обе иконки переведены на `fnfal_mag_ergo_*` в `items.lua` и companion.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-007`: `PASS` static — `BattleRifles_FNFALLight` = `JAZZ_StockLightUnFolded`; остальные легионные FAL-дефы = `JAZZ_StockNormal`; `FNFALLight` в `LegionT2_BattleRifle`, `LegionT2_BattleRifle_Elite`, `LegionMercenary_AssaultRifle`; GenW m1/m2 разносят обычный и para. `_validate_items_quick.py` по `jazz-units` exit 0.
- `JAZZ-WEAPON-FAL-FAMILY-001-AC-008`: `PASS` static — `BattleRifles_FNFAL_Tactical`/`_AP`/`_Scope` в T2-4 пулах Легиона; `Adonis_FNFAL_Tactical`/`_Reflex` в `Adonis_AssaultRifle` и `AdonisElite_AssaultRifle`; metadata resources зарегистрированы.

Прочее: `scripts/check-lua-quoted-strings.ps1` даёт OK на 1144 файлах. `_check_weapon_imports.py` падает на ассерте `weapons['Mosin']['CanAppearInShop']`; дефект дореформенный и к этому изменению не относится — в `InventoryItem/Mosin.lua` полей витрины нет вовсе.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — новый предмет, изменённый тир классики, пара складного приклада.
- `docs/technical/weapons/data/*` — строки обоих FAL и опции компонентов.
- `docs/wiki/weapons-and-ammo.md` и обе страницы `docs/showcase/ru` и `docs/showcase/en` — игроку заметны новый ствол, смена тира и складной приклад.
- `docs/design/weapons-import-queue.md` — отметить израсходованные архивы и отложенные заготовки.
