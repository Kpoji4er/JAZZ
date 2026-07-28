# Легион: схема юнитов и тиры снаряжения

## Назначение и наблюдаемый эффект

Легион реализован как фиксированный каталог из 37 `JAZZ_Legion_*` классов `UnitData`. Классы разделены на шесть боевых семейств: штурмовики, стрелки, фланкеры, пулемётчики, командиры и гранатомётчики. Семейство определяет тактическую роль, AI archetype и линию усиления, а конкретный класс — стартовый уровень, характеристики, perks, appearance и корневой equipment preset.

Снаряжение прогрессирует независимо от класса юнита. Quest-переменная `JAZZ_LegionTier.JAZZ_Legion_Tier` открывает новые записи в общих weapon/ammo/armor/utility LootDef. Поэтому один и тот же `UnitData` при новой генерации может получить более сильный вариант экипировки, но не превращается в следующий класс своей линии.

Для игрока это проявляется в двух независимых осях сложности:

1. состав enemy squad выбирает более высокие фиксированные классы Легиона;
2. общий campaign tier меняет доступный пул их оружия, патронов, брони и расходников.

## Связанные источники и уровень подтверждения

- Human design source: [JAZZ Units.drawio, страница `JAZZ Legion`](https://app.diagrams.net/#G1ACFcxt5YuT-Ekw40XstiJiFLh3y6_Vah#%7B%22pageId%22%3A%22c1zTZtVB8CXOZJlONBNN%22%7D), Drive revision modified `2026-03-09T20:24:26.775Z`.
- Static JAZZ evidence: working tree `jazz` и `jazz-units` на 26 июля 2026 года.
- Static vanilla evidence: установленный `PlayerControlSectors` имеет default comparator `>`, а `QuestIsVariableNum` — `>=`.
- Editor и runtime evidence в рамках этого documentation-only аудита не выполнялись.
- Отдельной spec/decision нет: поведение уже реализовано, задача только фиксирует current state.

Диаграмма является источником таксономии и стрелок переходов, но не runtime-источником истины. Текущие значения полей берутся из загружаемых `UnitData` и generated LootDef.

## Владелец и runtime-слои

| Слой | Вклад |
| --- | --- |
| Установленная vanilla | `UnitData`, `ModItemLootDef`, `LootEntry*`, `QuestIsVariableNum`, `PlayerControlSectors`, TCE/quest state и `CreateStartingEquipment` |
| CommonLib | Прямого одноимённого override для описанного контракта в подтверждённом snapshot не зафиксировано |
| `jazz` (`e6L4ECj`) | Quest `JAZZ_LegionTier`, переменная `JAZZ_Legion_Tier`, одиннадцать TCE переходов и deferred-регенерация через `Code/UtilityFunc.lua` |
| `jazz-units` (`Dv3mFVN`) | 37 классов `JAZZ_Legion_*`, их equipment presets и 739 condition references к `JAZZ_Legion_Tier` в generated LootDef snapshot |

## Файлы реализации и load-state

| Путь | Состояние | Назначение |
| --- | --- | --- |
| `jazz/items.lua` | generated and loaded | `ModItemQuestsDef` с ID `JAZZ_LegionTier`, TCE и quest variables |
| `jazz/metadata.lua` | generated and loaded | регистрирует quest ModItem и загружает `Code/UtilityFunc.lua` |
| `jazz/Code/UtilityFunc.lua` | loaded runtime | ставит отложенный флаг и пересоздаёт starting equipment |
| `jazz-units/UnitData/JAZZ_Legion_*.lua` | generated and loaded | 37 публичных UnitData классов Легиона |
| `jazz-units/items.lua` | generated and loaded | equipment, firearm, ammo, armor, valuable и utility LootDef с tier conditions |
| `jazz-units/metadata.lua` | generated and loaded | явно регистрирует все 37 `JAZZ_Legion_*` файлов |
| `jazz-units/Code/Legion.lua` | loaded runtime | пул имён для `eliteCategory = "Legion"`; не владеет таксономией и equipment tier |
| `jazz/Code/LegionUnitPrices.lua` | loaded runtime | strategic `$` каталог на 37 `JAZZ_Legion_*` (JAZZ-STRATEGY-004); пока не подключён к spawn |
| `jazz/Code/LegionSquadComposition.lua` | loaded runtime | officer density + T4 MercCaptain gate (JAZZ-STRATEGY-005); пока не подключён к generator |

## Два разных значения слова «тир»

| Контракт | Значения | Меняется у существующего юнита | Что контролирует |
| --- | --- | --- | --- |
| Tier класса в ID | `T1`–`T4` | Нет | фиксированные stats, perks, role, archetype, appearance и корневой inventory preset |
| Campaign equipment tier | `11`–`13`, `21`–`25`, `31`–`33` | Да, после regeneration | допустимые LootEntry и их веса внутри оружия, патронов, брони и расходников |

Стрелка на диаграмме означает линию дизайна/эскалации состава. В runtime нет функции, которая заменяет объект `JAZZ_Legion_*T1*` объектом `*T2*`. Конкретный public UnitData ID выбирается squad/map/spawn data.

Strategic generator (STRATEGY-005): class-tiers **дополняют** друг друга (T3/T4 добавляются к line, не вычищают T1/T2). Офицеры по density: Sergeant `/8`, Lieutenant `/15–20`, Captain `/30`; `MercenaryCaptain` обязателен для T4-отрядов.

## Таксономия UnitData

Во всех строках файл равен `<Public ID>.lua` и находится в `jazz-units/UnitData/`.

### Штурмовики

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_AssaultT1_Roughneck` | Головорез | 2 | `Stormer` | `Legion_Assaulter` | `Roughneck_Inventory` |
| T1 | `JAZZ_Legion_AssaultT1_Grenadier` | Гренадёр | 3 | `Demolitions` | `Legion_Assaulter` | `Grenadier_Inventory` |
| T1 | `JAZZ_Legion_AssaultT1_Crusher` | Громила | 4 | `Stormer` | `Legion_Assaulter` | `Crusher_Inventory` |
| T2 | `JAZZ_Legion_AssaultT2_Pillager` | Грабитель | 5 | `Stormer` | `Legion_Assaulter` | `Pillager_Inventory` |
| T2 | `JAZZ_Legion_AssaultT2_ShockTrooper` | Штурмовик | 6 | `Stormer` | `Legion_Assaulter` | `Shocktrooper_Inventory` |
| T2 | `JAZZ_Legion_AssaultT2_Pyro` | Пироман | 7 | `Demolitions` | `Legion_Assaulter` | `Pyro_Inventory` |
| T3 | `JAZZ_Legion_AssaultT3_Punisher` | Каратель | 10 | `Stormer` | `Legion_Assaulter` | `Punisher_Inventory` |
| T3 | `JAZZ_Legion_AssaultT3_SkullCrusher` | Череполом | 12 | `Stormer` | `Legion_Assaulter` | `SkullCrusher_Inventory` |
| T4 | `JAZZ_Legion_AssaultT4_Headsman` | Палач | 15 | `Stormer` | `Legion_Assaulter` | `Headsman_Inventory` |

Ветви диаграммы:

- `Roughneck → Pillager`;
- `Grenadier → ShockTrooper → Punisher → Headsman`;
- `Grenadier → Pyro → SkullCrusher`;
- `Crusher → Pyro`.

### Стрелки

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_FrontT1_Rifleman` | Стрелок | 4 | `Marksman` | `Legion_Frontliner` | `Rifleman_Inventory` |
| T1 | `JAZZ_Legion_FrontT1_Bonemaker` | Костоправ | 5 | `Medic` | `Legion_Frontliner` | `Bonemaker_Inventory` |
| T1 | `JAZZ_Legion_FrontT1_Marauder` | Мародёр | 5 | `Soldier` | `Legion_Frontliner` | `Marauder_Inventory` |
| T2 | `JAZZ_Legion_FrontT2_Ambusher` | Засадник | 8 | `Marksman` | `Legion_Frontliner` | `Ambusher_Inventory` |
| T2 | `JAZZ_Legion_FrontT2_Raider` | Налётчик | 8 | `Soldier` | `Legion_Frontliner` | `Raider_Inventory` |
| T2 | `JAZZ_Legion_FrontT2_Marksman` | Охотник | 10 | `Soldier` | `Legion_Frontliner` | `Marksman_Inventory` |
| T3 | `JAZZ_Legion_FrontT3_Sniper` | Снайпер | 12 | `Marksman` | `Legion_Frontliner` | `Sniper_Inventory` |
| T3 | `JAZZ_Legion_FrontT3_Veteran` | Ветеран | 12 | `Soldier` | `Legion_Frontliner` | `Veteran_Inventory` |
| T4 | `JAZZ_Legion_FrontT4_Mercenary` | Наемник | 15 | `Soldier` | `Legion_Frontliner` | `Mercenary_Inventory` |
| T4 | `JAZZ_Legion_FrontT4_MercenarySniper` | Наемник снайпер | 15 | `Marksman` | `Legion_Frontliner` | `MercenarySniper_Inventory` |

Ветви диаграммы:

- `Rifleman → Marksman`;
- `Marauder → Raider → Veteran → Mercenary`;
- `Ambusher → Sniper → MercenarySniper`;
- `Bonemaker` — отдельная медицинская роль без стрелки повышения.

### Фланкеры

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_FlankerT1_Warden` | Дозорный | 3 | `Recon` | `Legion_Frontliner` | `Warden_Inventory` |
| T2 | `JAZZ_Legion_FlankerT2_Scout` | Скаут | 6 | `Recon` | `Legion_Assaulter` | `Scout_Inventory` |
| T2 | `JAZZ_Legion_FlankerT2_Skirmisher` | Застрельщик | 6 | `Recon` | `Legion_Frontliner` | `Skirmisher_Inventory` |
| T3 | `JAZZ_Legion_FlankerT3_Recon` | Разведчик | 10 | `Recon` | `Legion_Assaulter` | `Recon_Inventory` |
| T3 | `JAZZ_Legion_FlankerT3_Pathfinder` | Следопыт | 10 | `Recon` | `Legion_Frontliner` | `Pathfinder_Inventory` |
| T4 | `JAZZ_Legion_FlankerT4_Ranger` | Рейнджер | 18 | `Recon` | `Legion_Assaulter` | `Ranger_Inventory` |

Ветви диаграммы:

- `Warden → Scout → Recon → Ranger`;
- `Warden → Skirmisher → Pathfinder → Ranger`.

### Пулемётчики

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_GunnerT1_Gunner` | Пуляло | 3 | `Heavy` | `Legion_Machinegunner` | `Gunner_Inventory` |
| T2 | `JAZZ_Legion_GunnerT2_GMPG` | Пулемётчик | 6 | `Heavy` | `Legion_Machinegunner` | `GMPG_Inventory` |
| T2 | `JAZZ_Legion_GunnerT2_AssaultGunner` | Коммандо | 8 | `Heavy` | `Legion_Machinegunner` | `AssaultGunner_Inventory` |
| T3 | `JAZZ_Legion_GunnerT3_VeteranGunner` | Подавитель | 14 | `Heavy` | `Legion_Machinegunner` | `VeteranGunner_Inventory` |
| T4 | `JAZZ_Legion_GunnerT4_MercGunner` | Наемник Пулеметчик | 16 | `Heavy` | `Legion_Machinegunner` | `MercGunner_Inventory` |

Обе ветви `Gunner → GMPG` и `Gunner → AssaultGunner` сходятся в `VeteranGunner → MercGunner`.

### Командиры

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_LeaderT1_Sergeant` | Бригадир | 3 | `Commander` | `Legion_Assaulter` | `Sergeant_Inventory` |
| T2 | `JAZZ_Legion_LeaderT2_Lieutenant` | Командир | 7 | `Commander` | `Legion_Frontliner` | `Lieutenant_Inventory` |
| T3 | `JAZZ_Legion_LeaderT3_Captain` | Советник | 6 | `Marksman` | `Legion_Frontliner` | `Captain_Inventory` |
| T4 | `JAZZ_Legion_LeaderT4_MercenaryCaptain` | Мастер | 8 | `Commander` | `Legion_Frontliner` | `MercenaryCaptain_Inventory` |

Линия диаграммы линейна: `Sergeant → Lieutenant → Captain → MercenaryCaptain`. Текущие `StartingLevel` не монотонны и не совпадают с уровнями 8/14/16/20 на diagram revision.

### Гранатомётчики

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_HeavyT1_Rocketeer` | Ракетчик | 5 | `Artillery` | `Legion_Assaulter` | `Rocketeer_Inventory` |
| T2 | `JAZZ_Legion_HeavyT2_Grenadier` | Гранатомётчик | 8 | `Artillery` | `Artillery` | `HeavyGrenadier_Inventory` |
| T3 | `JAZZ_Legion_HeavyT3_Mortarman` | Миномётчик | 8 | `Artillery` | `Artillery` | `Mortarman_Inventory` |

Линия диаграммы линейна: `Rocketeer → HeavyGrenadier → Mortarman`. Diagram revision указывает миномётчику level 10, загружаемый UnitData — level 8.

## Campaign equipment tier

### Кодирование и пороги

Quest `JAZZ_LegionTier` создаётся с `Given = true`, а `JAZZ_Legion_Tier` начинается со значения `11`. Десятки обозначают крупную группу прогрессии, единицы — ступень внутри группы. Значения `20` и `30` используются в LootDef как групповые границы, но сами TCE их не присваивают.

В установленной vanilla у `PlayerControlSectors` comparator по умолчанию равен `>`. Поэтому generated TCE задают следующую зависимость от числа контролируемых игроком секторов:

| Секторы игрока | Условие TCE | Записываемый tier |
| ---: | --- | ---: |
| 0–1 | initial value `11`; отдельный reset TCE срабатывает при `< 1` | 11 |
| 2 | `> 1` | 12 |
| 3 | `> 2` | 13 |
| 4 | `> 3` | 21 |
| 5 | `> 4` | 22 |
| 6 | `> 5` | 23 |
| 7 | `> 6` | 24 |
| 8 | `> 7` | 25 |
| 9 | `> 8` | 31 |
| 10 | `> 9` | 32 |
| 11 и больше | `> 10` | 33 |

Каждому переходу соответствует `QuestVarTCEState`, поэтому это одноразовые quest events, а не формула, вычисляемая при каждом чтении. У перехода в `12` дополнительно стоит guard `JAZZ_Legion_Tier <= 23`; он не даёт поздно сработавшему раннему событию откатить уже достигнутую третью группу.

### Как tier фильтрует LootDef

`jazz-units/items.lua` содержит 739 ссылок на `JAZZ_Legion_Tier` в текущем generated snapshot. У `QuestIsVariableNum` comparator по умолчанию равен `>=`, поэтому запись с `Amount = 22` без явного `Condition` доступна начиная с tier 22. Явные `<` и `<=` задают верхнюю границу и выводят раннее снаряжение из пула.

Пороги `1`, `2`, `3`, `4` и `10` — legacy/coarse gates: при фактически присваиваемых значениях `11`–`33` они всегда пройдены. Пороги `20` и `30` отделяют вторую и третью группы. Для точного окна используются две проверки одной quest variable.

Корневой `<Unit>_Inventory` обычно собирает с `loot = "all"` несколько дочерних LootDef: основное и дополнительное оружие, гранаты, night gear, valuables и броню. Внутри них применяются веса, случайный выбор и tier conditions. Следовательно, tier не выбирает готовый комплект целиком: он меняет множество допустимых записей и веса, из которых `CreateStartingEquipment` создаёт инвентарь.

## Runtime flow смены снаряжения

1. TCE по числу контролируемых секторов записывает новое значение `JAZZ_Legion_Tier`.
2. `ExecuteCode` вызывает `RegenerateLegionLoot()`. Функция только ставит локальный boolean `RegenerateLegionLootVar`.
3. При следующем `OnMsg.OpenSatelliteView` установленный флаг вызывает `_RegenerateLegionLoot()`.
4. Функция проходит все `gv_Squads` и все `squad.units`.
5. Для существующего tactical object живого non-merc юнита Легиона очищается инвентарь объекта и заново вызывается `CreateStartingEquipment(unitdata.randomization_seed)`.
6. Затем, уже вне Legion guard, очищается `gv_UnitData[unit_id].Items` и вызывается тот же генератор starting equipment.
7. После полного обхода флаг сбрасывается.

Флаг объединяет несколько переходов, случившихся до следующего открытия satellite view, в одну регенерацию по последнему записанному tier. Отдельная функция `___RegenerateLegionLoot()` существует и ограничивает обработку enemy sectors/Legion, но активный flow её не вызывает.

## Межпакетный контракт

`jazz` владеет progression signal и runtime trigger, а `jazz-units` — его потребителями в LootDef и самими UnitData. В `jazz/metadata.lua` пакет `Dv3mFVN` объявлен optional dependency; обратной dependency из `jazz-units` на `e6L4ECj` нет. Функционально система требует совместной загрузки пакетов: без core quest условия не имеют корректного progression source, без units package нет каталога юнитов и tier-aware LootDef.

Публичный межпакетный контракт состоит из:

- Mod ID `e6L4ECj` и `Dv3mFVN`;
- quest ID `JAZZ_LegionTier`;
- variable ID `JAZZ_Legion_Tier`;
- функции `RegenerateLegionLoot()`;
- 37 public `JAZZ_Legion_*` ID;
- `<Unit>_Inventory` и вложенных LootDef ID, на которые ссылаются UnitData.

Пилот Legion Global AI (JAZZ-STRATEGY-002) потребляет тот же 37-unit pool через четыре EnemySquad ID в `jazz-units`: `LegionGlobalAI_Recon` (8–12), `_Patrol` (12–18), `_Convoy` (15–25), `_Garrison` (25–40). Новые UnitData не добавляются; составы содержат только `JAZZ_Legion_*`.

Изменение любого из этих ID требует синхронного impact audit обоих репозиториев и generated-data проверки.

## Strategic unit price ($)

Владелец каталога — пакет `jazz` (`Code/LegionUnitPrices.lua`), не поля UnitData в `jazz-units`. Цены заданы в `$` на каждый public ID; полный перечень и шкала — в [JAZZ-STRATEGY-004](../../specs/active/JAZZ-STRATEGY-004.md).

| Accessor | Назначение |
| --- | --- |
| `JAZZ_LegionUnitPrices[id]` | static table |
| `JAZZ_GetLegionUnitPrice(unit_or_id)` | цена одного ID / unit object, иначе `false` |
| `JAZZ_GetLegionSquadUnitPriceSum(unit_ids)` | сумма цен списка ID; `false` при неизвестном ID |

Шкала (class-tier × family): Line T1–T4 = 500/1000/2000/3500; Specialist = 800/1500/2800/4500; Leader = 800/1500/2500/4000. Specialist в каталоге: MG, demo/pyro, medic (`Bonemaker`), arty (`Heavy*`), sniper (`FrontT3_Sniper`, `FrontT4_MercenarySniper`).

Экономический якорь: полный дорогой garrison (~40, T3/T4) ≈ **$120000** ≈ целевой полный пул аванпоста ≈ **10×** Major shipment (`DiamondBriefcase` $12000). Лёгкие recon/patrol ≪ capacity. Spawn (`lSpawnRegularRole` / flat role costs из STRATEGY-003) **пока не читает** эту таблицу; capacity runtime меняется в п.0 money ledger.
## Расхождения diagram revision с current UnitData

| Узел | Diagram revision | Загружаемый UnitData |
| --- | --- | --- |
| `JAZZ_Legion_FlankerT3_Pathfinder` | level 14 | level 10 |
| `JAZZ_Legion_LeaderT1_Sergeant` | level 8 | level 3 |
| `JAZZ_Legion_LeaderT2_Lieutenant` | level 14 | level 7 |
| `JAZZ_Legion_LeaderT3_Captain` | level 16 | level 6, role `Marksman` |
| `JAZZ_Legion_LeaderT4_MercenaryCaptain` | «Капитан наемников», level 20 | «Мастер», level 8 |
| `JAZZ_Legion_HeavyT3_Mortarman` | level 10 | level 8 |

Stats, perks и детальный состав инвентаря с диаграммы не считаются current-state значениями без повторной сверки с generated files: runtime использует UnitData и LootDef. Выше перечислены подтверждённые статические расхождения, а не автоматически исправляемые ошибки.

## Чек-лист проверки

- [ ] Все 37 `JAZZ_Legion_*` зарегистрированы в `jazz-units/metadata.lua` и имеют одноимённый файл UnitData.
- [ ] Каждый UnitData ссылается на существующий корневой equipment LootDef.
- [ ] Quest `JAZZ_LegionTier` загружен из `jazz/items.lua`, имеет initial tier 11 и состояния для всех 11 переходов.
- [ ] При порогах 0/2/3/4/8/9/11 контролируемых секторов наблюдаются tier 11/12/13/21/25/31/33.
- [ ] После перехода флаг не меняет инвентарь до открытия satellite view.
- [ ] После открытия satellite view regenerated equipment соответствует новому tier и флаг больше не вызывает повторный проход.
- [ ] Проверены tactical object и strategic `gv_UnitData` одного живого юнита Легиона.
- [ ] Отдельно проверен non-Legion squad: текущая реализация затрагивает его strategic inventory, что должно быть либо принято как контракт, либо исправлено отдельным change.
- [ ] Save/load между tier transition и открытием satellite view проверен отдельно.

## Известные ограничения и риски

- Название `_RegenerateLegionLoot()` уже имени её фактической области: strategic inventory пересоздаётся для каждого `unit_id` каждого `gv_Squads`, а не только для Легиона. Legion guard ограничивает только ветку tactical object.
- `unitdata.Items = {}` находится вне проверки `unitdata`; некорректная ссылка squad → unit может привести к runtime error.
- Регенерация полностью стирает текущий inventory и не различает starting gear, подобранные предметы и ручные изменения.
- Deferred-флаг — локальная Lua-переменная, а не `GameVar`; сохранение/перезагрузка между TCE и `OpenSatelliteView` может потерять ожидающую регенерацию.
- Повторно используется `randomization_seed`. При изменившемся пуле выбор пересчитывается детерминированно относительно того же seed, но итоговый набор может измениться.
- 739 tier references и optional cross-package dependency делают систему чувствительной к частичной установке, load order и несинхронной регенерации `items.lua`/`metadata.lua`.
- Уровни командирской линии в current UnitData не образуют возрастающую последовательность; это задокументированное состояние, не подтверждённое намерение баланса.

## Контракт сопровождения

При изменении схемы класса сначала определить, меняется ли только design diagram или public UnitData/runtime contract. Изменение класса, ID, root equipment, role, archetype, LootDef, quest threshold или dependency является generated-data/compatibility-sensitive изменением: оно требует approved spec, синхронной транзакции `items.lua` + `metadata.lua` + companion files в пакетах-владельцах и профильного sync-аудита четырёх репозиториев.

Диаграмму и эту страницу обновлять в одном change. Если diagram revision и generated UnitData расходятся, current-state таблицы отражают загружаемый код, а расхождение сохраняется явно до отдельного решения по балансу.
