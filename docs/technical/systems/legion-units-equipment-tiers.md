# Легион: схема юнитов и тиры снаряжения

Целевой дизайн лоадаутов (arch/sub, силуэты классов, модули, ammo grade, маппинг на `weapons.csv` `X-Y` ↔ `XY`): [`docs/design/legion-loadouts.md`](../../design/legion-loadouts.md). Spec реализации: [`JAZZ-UNITS-003`](../../specs/active/JAZZ-UNITS-003.md). Эта страница — **current-state** реализации, не target.

## Назначение и наблюдаемый эффект

Легион реализован как фиксированный каталог из **38** `JAZZ_Legion_*` классов `UnitData` (37 боевых линий + `JAZZ_Legion_Recruit` для recruiter/manpower). Боевые классы разделены на шесть семейств: штурмовики, стрелки, фланкеры, пулемётчики, командиры и гранатомётчики. Семейство определяет тактическую роль, AI archetype и линию усиления, а конкретный класс — стартовый уровень, характеристики, perks, appearance и корневой equipment preset.

Снаряжение прогрессирует независимо от класса юнита. Quest-переменная `JAZZ_LegionTier.JAZZ_Legion_Tier` открывает новые записи в weapon/ammo/armor/utility LootDef. Поэтому один и тот же `UnitData` при новой генерации может получить более сильный вариант экипировки, но не превращается в следующий класс своей линии.

**JAZZ-UNITS-003 (loaded):** боевые `*_Inventory` / `*_Firearm` для 37 классов **генерируются** из recipes в `jazz/scripts/legion-loadouts/` (не ручной суффикс-зоопарк как основной процесс). Shared pools: `JAZZ_Gen_NightEquipment`, `JAZZ_Gen_Sidearm`, `JAZZ_Gen_FlareGun`, `JAZZ_Gen_MiscGear`, `JAZZ_Gen_Valuables_*`, плюс `JAZZ_GenW_*` (оружие+патроны). Public UnitData Equipment **имена** сохранены. Recruit без combat recipe. Cargo `tax`/`shipment` (`lEnsureMoneyCargo` / `DiamondBriefcase`) **не** эмитится class recipe.

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
| `jazz` (`e6L4ECj`) | Quest `JAZZ_LegionTier`, переменная `JAZZ_Legion_Tier`, Maps/NoMaps progression в `Code/LegionTierProgression.lua` (legacy sector TCE gated off) и deferred-регенерация через `Code/UtilityFunc.lua` |
| `jazz-units` (`Dv3mFVN`) | 38 классов `JAZZ_Legion_*` (incl. Recruit), их equipment presets и 739 condition references к `JAZZ_Legion_Tier` в generated LootDef snapshot |

## Файлы реализации и load-state

| Путь | Состояние | Назначение |
| --- | --- | --- |
| `jazz/items.lua` | generated and loaded | `ModItemQuestsDef` с ID `JAZZ_LegionTier`, TCE и quest variables |
| `jazz/metadata.lua` | generated and loaded | регистрирует quest ModItem и загружает `Code/UtilityFunc.lua` |
| `jazz/Code/UtilityFunc.lua` | loaded runtime | ставит отложенный флаг и пересоздаёт starting equipment |
| `jazz-units/UnitData/JAZZ_Legion_*.lua` | generated and loaded | 38 публичных UnitData классов Легиона (incl. Recruit) |
| `jazz-units/items.lua` | generated and loaded | equipment, firearm, ammo, armor, valuable и utility LootDef с tier conditions |
| `jazz-units/metadata.lua` | generated and loaded | явно регистрирует все 38 `JAZZ_Legion_*` файлов |
| `jazz-units/Code/Legion.lua` | loaded runtime | пул имён для `eliteCategory = "Legion"`; не владеет таксономией и equipment tier |
| `jazz/Code/LegionUnitPrices.lua` | loaded runtime | strategic `$` каталог на 38 `JAZZ_Legion_*` (JAZZ-STRATEGY-004); используется generator/spawn (008) |
| `jazz/Code/LegionSquadComposition.lua` | loaded runtime | officer density + T4 MercCaptain gate (JAZZ-STRATEGY-005); medic density Bonemaker (JAZZ-STRATEGY-015); подключён к generator (008) |
| `jazz/scripts/legion-loadouts/` | build-time tooling | JAZZ-UNITS-003: recipes/catalogs → regenerate Legion LootDef in `jazz-units/items.lua` |

## Два разных значения слова «тир»

| Контракт | Значения | Меняется у существующего юнита | Что контролирует |
| --- | --- | --- | --- |
| Tier класса в ID | `T1`–`T4` | Нет | фиксированные stats, perks, role, archetype, appearance и корневой inventory preset |
| Campaign equipment tier | `11`–`13`, `21`–`25`, `31`–`33` | Да, после regeneration | допустимые LootEntry и их веса внутри оружия, патронов, брони и расходников |

Стрелка на диаграмме означает линию дизайна/эскалации состава. В runtime нет функции, которая заменяет объект `JAZZ_Legion_*T1*` объектом `*T2*`. Конкретный public UnitData ID выбирается squad/map/spawn data.

Strategic generator (STRATEGY-005 / 015): class-tiers **дополняют** друг друга (T3/T4 добавляются к line, не вычищают T1/T2). Офицеры по density: Sergeant `/8`, Lieutenant `/15–20`, Captain `/30`; `MercenaryCaptain` обязателен для T4-отрядов. Медики: `Bonemaker` — при размере отряда `n≥10` минимум 1, далее `floor(n/15)` (≈1 на 10–20).

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
- `Bonemaker` — отдельная медицинская роль без стрелки повышения; combat generator резервирует слоты по STRATEGY-015 (не только random line).

### Фланкеры

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_FlankerT1_Warden` | Дозорный | 3 | `Recon` | `Legion_Flanker` | `Warden_Inventory` |
| T2 | `JAZZ_Legion_FlankerT2_Scout` | Скаут | 6 | `Recon` | `Legion_Flanker` | `Scout_Inventory` |
| T2 | `JAZZ_Legion_FlankerT2_Skirmisher` | Застрельщик | 6 | `Recon` | `Legion_Flanker` | `Skirmisher_Inventory` |
| T3 | `JAZZ_Legion_FlankerT3_Recon` | Разведчик | 10 | `Recon` | `Legion_Flanker` | `Recon_Inventory` |
| T3 | `JAZZ_Legion_FlankerT3_Pathfinder` | Следопыт | 10 | `Recon` | `Legion_Flanker` | `Pathfinder_Inventory` |
| T4 | `JAZZ_Legion_FlankerT4_Ranger` | Рейнджер | 18 | `Recon` | `Legion_Flanker` | `Ranger_Inventory` |

Ветви диаграммы:

- `Warden → Scout → Recon → Ranger`;
- `Warden → Skirmisher → Pathfinder → Ranger`.

`Skirmisher_Inventory` следует стрелковой ветке: battle rifles, rifle-пакеты модификаций и Match ammo; старая SMG/flanker-ветка не используется.

### Пулемётчики

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_GunnerT1_Gunner` | Пуляло | 3 | `Heavy` | `Legion_Machinegunner` | `Gunner_Inventory` |
| T2 | `JAZZ_Legion_GunnerT2_GMPG` | Пулемётчик | 6 | `Heavy` | `Legion_Machinegunner` | `GMPG_Inventory` |
| T2 | `JAZZ_Legion_GunnerT2_AssaultGunner` | Коммандо | 8 | `Heavy` | `Legion_Machinegunner` | `AssaultGunner_Inventory` |
| T3 | `JAZZ_Legion_GunnerT3_VeteranGunner` | Подавитель | 14 | `Heavy` | `Legion_Machinegunner` | `VeteranGunner_Inventory` |
| T4 | `JAZZ_Legion_GunnerT4_MercGunner` | Наемник Пулеметчик | 16 | `Heavy` | `Legion_Machinegunner` | `MercGunner_Inventory` |

Обе ветви `Gunner → GMPG` и `Gunner → AssaultGunner` сходятся в `VeteranGunner → MercGunner`. `AssaultGunner_Inventory` гарантированно выдаёт Коммандо Machete (100% в каждом arch band) и один Molotov; `CustomEquipGear` ставит melee в `Handheld B`.

### Командиры

| Tier | Public ID | Display name | Level | Role | Archetype | Equipment |
| --- | --- | --- | ---: | --- | --- | --- |
| T1 | `JAZZ_Legion_LeaderT1_Sergeant` | Бригадир | 3 | `Commander` | `Legion_Assaulter` | `Sergeant_Inventory` |
| T2 | `JAZZ_Legion_LeaderT2_Lieutenant` | Командир | 7 | `Commander` | `Legion_Frontliner` | `Lieutenant_Inventory` |
| T3 | `JAZZ_Legion_LeaderT3_Captain` | Советник | 6 | `Marksman` | `Legion_Frontliner` | `Captain_Inventory` |
| T4 | `JAZZ_Legion_LeaderT4_MercenaryCaptain` | Мастер | 8 | `Commander` | `Legion_Frontliner` | `MercenaryCaptain_Inventory` |

`Sergeant_Firearm` (shared T1 commander kit, incl. named M1 **Рафаль**): primary tags **SMG** (`exclude_tags: ["pistol"]` — Autopistol/`Scorpion`/`MicroUZI` out of the normal scan; pistols via `JAZZ_Gen_Sidearm`); `primary_max_tier_label: "2-1"` (true SMG ladder through `M45`/`UZI`/`Agram2000`, no MP5+); `arch1_all_subs_from: 11` so balance `1-x` SMGs (e.g. `MPL`/`Sterling`) roll from day-one Amount `11`; `arch1_early_ids` (bypass `exclude_tags`): `M45`→`11`, `MAC10`→`12` (T1-2), `UZI`/`Agram2000`→`13` (T1-3).

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

Quest `JAZZ_LegionTier` создаётся с `Given = true`, а `JAZZ_Legion_Tier` начинается со значения `11`. Десятки обозначают крупную группу прогрессии, единицы — ступень внутри группы. Значения `20` и `30` используются в LootDef как групповые границы; runtime их не присваивает как «текущий» tier.

Legacy TCE по `PlayerControlSectors` в quest **заглушены** (`CheckExpression` → `false`, JAZZ-COMPAT-008). Оба профиля двигают tier только из `Code/LegionTierProgression.lua` (**только вверх**).

**R.I.S. mail (JAZZ-UI-RIS-001):** desk queue in `gv_JAZZ_RIS` — ≤1 письмо / **5** campaign hours. Welcome `ready +3h` from awake; baseline Legion brief (T1-1) `ready +2h`; raises enqueue `ready +5h` after `lApplyTierRaise` → `JAZZ_RIS_OnTierRaised`. Tab `ris` locked until welcome read. Канон [`ris-legion-tier-briefs.md`](../../design/ris-legion-tier-briefs.md).


### Maps: time + mainland + mines (COMPAT-008)

При **не** `JAZZ_NoMapsIsActive()` — `gv_JAZZ_LegionTierMaps`:

| Major | Как открывается |
| ---: | --- |
| 1 | старт |
| 2 | первая **оккупация** non-Ernie **surface** сектора (`SectorSideChanged` → player1/player2). Найм мерков / travel без смены `Side` не считаются. Ernie = Id из Region `ErnieIsland.Sectors` (+ WeatherZone/City/Label fallback). |
| 3 | **5** player-owned surface `Mine` |

| Major | Шаг подтира | Потолок |
| ---: | --- | ---: |
| 1 | каждые **7** дней | `11`→`12`→`13` (~2 недели до потолка T1) |
| 2 | каждые **30** дней | `21`…`25` |
| 3 | каждые **30** дней | `31`→`32`→`33` |

Без mainland occupation потолок остаётся `13` (даже при долгом сидении на острове). При смене major таймер sub сбрасывается. Existing save с уже player-owned mainland surface latch'ит `mainland_at` без нового захвата.

### NoMaps: time progression (COMPAT-003) — только без maps

На профиле `jazz-nomaps` (`JAZZ_NoMapsIsActive`) — `gv_JAZZ_LegionTierNoMaps` по `Game.CampaignTime`:

| Major | Как открывается |
| ---: | --- |
| 1 | старт |
| 2 | первая player-owned шахта + **3 суток** |
| 3 | WorldFlip (`04_Betrayal` `TriggerWorldFlip` / `WorldFlipDone`, как Bobby Ray T3) |

| Major | Шаг подтира | Потолок |
| ---: | --- | ---: |
| 1 | каждые **3** дня | 13 |
| 2 | каждые **14** дней | 25 |
| 3 | каждые **14** дней | 33 |

При смене major таймер подтира сбрасывается (старт с `x1`). Сектора на NoMaps tier не влияют.

**Class weight (COMPAT-005):** отдельно от gear loot. NoMaps default EnemySquad remap использует `LegionJAZZSquadT1_Early` (только UnitData `*T1_*`) на major I; alias резолвится в `LegionJAZZSquadT2`/`T3` при major II/III. UnitData remap на major I всегда class T1 (`Stronger_Elite`→T4 только major III+).

### Как tier фильтрует LootDef

Боевые class LootDef после JAZZ-UNITS-003 используют **exclusive arch bands** (примерно `[11,19]` / `[21,29]` / `≥31`) плюс веса внутри band. У `QuestIsVariableNum` comparator по умолчанию равен `>=`; явные `<=` задают верхнюю границу. На mid (`20–29`) оружие `balance_tier==1` остаётся редким remnant (~1% веса parent pool, weight `1400`); на late (`≥30`) tier1 primary отсутствует.

Legacy/coarse gates (`1`–`10`) в старых списках при значениях `11`–`33` всегда пройдены; новые generated blocks опираются на arch bands и subtier Amount.

Корневой `<Unit>_Inventory` собирает с `loot = "all"` дочерние LootDef: primary firearm (weapon+ammo combo), optional launcher (heavy), sidearm/melee/utility, night, valuables band ≈ `JAZZ_GetLegionUnitPrice`, armor Light/Middle/Heavy. Статический аудитор проходит все 37 рецептов: проверяет UnitData `Equipment`, связь inventory → firearm и материализацию sidearm/melee/utility. `CreateStartingEquipment` создаёт инвентарь из допустимых записей и весов.

`Veteran` / `Mercenary` дополнительно крутят `LegionGL_5pc` (~15% веса → `Legion_GL`): пул **M79**, **M72 LAW** (одноразовый, LootDef `M72LAW`) и late **ChinaLake**. UnitData `CustomEquipGear` для этих классов ставит Handheld B: `GrenadeLauncher`, затем `HeavyWeapon` (LAW), затем melee. `Rocketeer_Launcher` взвешивает RPG-7 (~70%) и M72 LAW (~30%).

`data/caliber_ammo.json` мапит калибр → **ammo** LootDef (например `Crusher_12g` / `Army_12g` для 12gauge). Нельзя указывать weapon-pool ids вроде `LegionT1_Shotgun`: combo с `loot = "all"` тогда выдаёт второй ствол (симптом: Громила с двумя дробовиками). Jazz `EquipStartingGear` кладёт leftover `Firearm` в пустой Handheld B, поэтому второй ствол оказывается во второй руке.

Регенерация: `python scripts/legion-loadouts/generate.py` из корня `jazz/` (см. `scripts/legion-loadouts/README.md`).

## Runtime flow смены снаряжения

1. `JAZZ_UpdateLegionTierForMaps` / `JAZZ_UpdateLegionTierForNoMaps` (SatelliteTick / OpenSatelliteView / SectorSideChanged / NewGame/LoadGame) поднимает `JAZZ_Legion_Tier` и вызывает `RegenerateLegionLoot()`.
2. `RegenerateLegionLoot()` только ставит локальный boolean `RegenerateLegionLootVar`.
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
- 38 public `JAZZ_Legion_*` ID (incl. Recruit);
- 6 combat family prefixes + logistics Recruit;
- `<Unit>_Inventory` и вложенных LootDef ID, на которые ссылаются UnitData.

Пилот Legion Global AI (JAZZ-STRATEGY-002) потребляет тот же Legion pool через четыре EnemySquad ID в `jazz-units`: `LegionGlobalAI_Recon` (8–12), `_Patrol` (12–18), `_Convoy` (15–25), `_Garrison` (25–40). Составы содержат только `JAZZ_Legion_*`; Recruit используется recruiter/manpower, не combat presets.

Изменение любого из этих ID требует синхронного impact audit обоих репозиториев и generated-data проверки.

## Strategic unit price ($)

Владелец каталога — пакет `jazz` (`Code/LegionUnitPrices.lua`), не поля UnitData в `jazz-units`. Цены заданы в `$` на каждый public ID; полный перечень и шкала — в [JAZZ-STRATEGY-004](../../specs/active/JAZZ-STRATEGY-004.md).

| Accessor | Назначение |
| --- | --- |
| `JAZZ_LegionUnitPrices[id]` | static table |
| `JAZZ_GetLegionUnitPrice(unit_or_id)` | цена одного ID / unit object, иначе `false` |
| `JAZZ_GetLegionSquadUnitPriceSum(unit_ids)` | сумма цен списка ID; `false` при неизвестном ID |

Шкала (class-tier × family): Line T1–T4 = 500/1000/2000/3500; Specialist = 800/1500/2800/4500; Leader = 800/1500/2500/4000. Specialist в каталоге: MG, demo/pyro, medic (`Bonemaker`), arty (`Heavy*`), sniper (`FrontT3_Sniper`, `FrontT4_MercenarySniper`).

Экономический якорь: полный дорогой garrison (~40, T3/T4) ≈ **$120000** ≈ целевой полный пул аванпоста ≈ **10×** Major shipment (`DiamondBriefcase` $12000). Лёгкие recon/patrol ≪ capacity. Combat spawn / `LegionSquadGenerator` (STRATEGY-008) **читает** per-unit prices из этой таблицы.
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

- [ ] Все 38 `JAZZ_Legion_*` зарегистрированы в `jazz-units/metadata.lua` и имеют одноимённый файл UnitData.
- [ ] Каждый UnitData ссылается на существующий корневой equipment LootDef.
- [ ] Quest `JAZZ_LegionTier` загружен из `jazz/items.lua`, initial tier 11; sector TCE gated; Maps/NoMaps формулы в `LegionTierProgression.lua`.
- [ ] При порогах 0/2/3/4/8/9/11 контролируемых секторов наблюдаются tier 11/12/13/21/25/31/33.
- [ ] После перехода флаг не меняет инвентарь до открытия satellite view.
- [ ] После открытия satellite view regenerated equipment соответствует новому tier и флаг больше не вызывает повторный проход.
- [ ] Проверены tactical object и strategic `gv_UnitData` одного живого юнита Легиона.
- [x] Отдельно проверен non-Legion squad: **JAZZ-UNITS-004** — regen больше не трогает non-Legion strategic inventory (static).
- [ ] Save/load между tier transition и открытием satellite view проверен отдельно.

## Известные ограничения и риски

- `_RegenerateLegionLoot()` (**JAZZ-UNITS-004**): только `Affiliation == "Legion"` (strategic `gv_UnitData` + tactical `g_Units`). Pre-004 ошибочно wipe'ил все `gv_Squads` (в т.ч. player mercs).
- Generator replace (`find_moditem_block`): должен consume полный `}),`; иначе stacked closers ломают parse всего `items.lua` (UNITS-004 / static paren guard).
- Каждый generated `*_Firearm` имеет unconditional fallback entry (UNITS-004), низкий вес относительно gated pools.
- Регенерация полностью стирает текущий inventory Легиона и не различает starting gear, подобранные предметы и ручные изменения.
- Deferred-флаг — локальная Lua-переменная, а не `GameVar`; сохранение/перезагрузка между TCE и `OpenSatelliteView` может потерять ожидающую регенерацию.
- Повторно используется `randomization_seed`. При изменившемся пуле выбор пересчитывается детерминированно относительно того же seed, но итоговый набор может измениться.
- Generated LootDef и optional cross-package dependency делают систему чувствительной к частичной установке, load order и несинхронной регенерации `items.lua`/`metadata.lua`.
- Уровни командирской линии в current UnitData не образуют возрастающую последовательность; это задокументированное состояние, не подтверждённое намерение баланса.

## Контракт сопровождения

При изменении схемы класса сначала определить, меняется ли только design diagram или public UnitData/runtime contract. Изменение класса, ID, root equipment, role, archetype, LootDef, quest threshold или dependency является generated-data/compatibility-sensitive изменением: оно требует approved spec, синхронной транзакции `items.lua` + `metadata.lua` + companion files в пакетах-владельцах и профильного sync-аудита четырёх репозиториев.

**Лоадауты Легиона (UNITS-003):** править `jazz/scripts/legion-loadouts/data/recipes.json` (и catalogs), затем `generate.py` + `sync_metadata.py`. Не сопровождать hand-made суффикс-варианты стволов как основной процесс. Не править помеченные `JAZZ-UNITS-003` блоки в `items.lua` вручную без последующей регенерации.

Диаграмму и эту страницу обновлять в одном change. Если diagram revision и generated UnitData расходятся, current-state таблицы отражают загружаемый код, а расхождение сохраняется явно до отдельного решения по балансу.
