# Каталог квестов, локаций и врагов (jazz-maps)

## Назначение и эффект для игрока

Справочник содержимого `jazz-maps` (пакет `FhNNYd`): какие квесты и сектора реально описаны в `items.lua`, какие вражеские squad defs привязаны к секторам, и что из этого относится к поддерживаемому демо-острову Эрни. Страница не заменяет системный контракт [карты, квесты и диалоги](maps-quests-dialogue.md); она фиксирует снимок контента для навигации и регрессии.

Локальная копия и прочая документация пакета maps: `../jazz-maps/docs/` (на диске каталог `JAZZ Maps/docs/`), оглавление `docs/README.md`, каталог контента `docs/content/quests-locations-enemies.md`.

География / атлас (без обхода `Maps/`):

| Документ | Содержание |
|---|---|
| [sector-atlas.md](../maps/sector-atlas.md) | Сетка A–P×32, authored sectors, ссылка на `GrandChien2.png` |
| [sector-transfer.md](../maps/sector-transfer.md) | Трансфер vanilla HotDiamonds → maps ID; quest remap ownership `JAZZ-QUESTS-002` |
| [sector-sheet-vs-runtime.md](../maps/sector-sheet-vs-runtime.md) | Diff Google Sheet «Карта» ↔ `ModItemSector` |
| Player wiki / showcase | [Карта Grand Chien](../../wiki/grand-chien-map.md), showcase slug `grand-chien-map` |

Vanilla quest badges/gates/journal на maps-профиле следуют таблице трансфера (не HotDiamonds ID). Ernie custom `Jazz_*` и maps-local I2/I3 не входят в этот remap. Stub debt: quest refs на `D22`/`F23` при отсутствии полного `ModItemSector`.

Пересборка данных: `python docs/tools/export-jazz-maps-sectors.py` затем `python docs/tools/build-sector-atlas-docs.py` из корня `jazz/` (выход: `docs/technical/maps/`).

## Владелец и runtime-слои

| Слой | Вклад |
|---|---|
| Установленная vanilla | Схема `ModItemSector` / `SatelliteSector`, `ModItemQuestsDef`, campaign `HotDiamonds`, базовые enemy squad IDs (`LegionAttackers_*`, `FortressPierre`, `LegionRaidSquad_01` и др., если не переопределены) |
| CommonLib | Прямых одноимённых коллизий с каталогом квестов/секторов не подтверждено на срезе; зависимость загружается до JAZZ |
| JAZZ | `jazz-maps/items.lua` — сектора, квесты, conversations, banters, setpieces; `jazz-units` — `ModItemEnemySquads` и UnitData архетипов `JAZZ_Legion_*`; loaded helpers `Rebels_Loyalty.lua`, `System_JAZZ_CrocodilePatrol.lua` |

Снимок: **7 августа 2026**, статический разбор `jazz-maps/items.lua`, шести quest-map exports и выборочный разбор `jazz-units/items.lua`. Runtime-прохождение каждой ветки не выполнялось.

## Файлы реализации и load-state

| Путь | Load-state |
|---|---|
| `jazz-maps/items.lua` | generated and loaded — источник секторов, квестов, conversations, banters, campaign override |
| `jazz-maps/metadata.lua` | loaded — `code`, affected resources, campaign `HotDiamonds` |
| `jazz-maps/Maps/<mapName>/` | generated map data; каталог карты связан через `mapName` / `Map` сектора |
| `jazz-maps/MapPatches/SetPieces/` | generated setpiece companions (`M1Landing`, `EncounterHerman`) |
| `jazz-maps/Code/Rebels_Loyalty.lua` | loaded runtime |
| `jazz-maps/Code/System_JAZZ_CrocodilePatrol.lua` | loaded runtime |
| `jazz-maps/UnitData/*.lua` | generated companions для локальных NPC/техники |
| `jazz-units/items.lua` (`ModItemEnemySquads`) | generated and loaded — составы отрядов по ID |

Папку `Maps/` здесь не инвентаризировали рекурсивно: ориентир — `sectorId` + `mapName` из `items.lua`.

## Сводка среза

| Объект | Количество |
|---|---|
| Campaign | `HotDiamonds`, `InitialSector = M1`, `sector_bottomright = P32`, `map_file = GrandChien2.png` |
| ModItemSector | 245 (surface 227 + underground 18; regen: `docs/tools/export-jazz-maps-sectors.py`) |
| Сектора с любыми enemy squad refs (`InitialSquads` / patrol / strong / extra) | 74 |
| Guardpost-сектора | 9 |
| Сектора Эрни (label/city/`WeatherZone=Erny` / Rebels_Ernie) | 23 (J7: `Label1=Ernie`, 26 июля 2026) |
| ModItemQuestsDef | 110 (83 видимых, 27 hidden) |
| Conversations | 24 |
| Banters | 41 |
| GuardpostObjective | 4 (`Bunker`, `EmeraldCoast`, `H4_copy`, `Bastien`) |
| SetpiecePrg | 2 (`M1Landing` → map `EPA7FVN`, `EncounterHerman` → `qJApdx`) |
| Локальные UnitData в maps | 3 (`JAZZ_Ernie_Locals_M2_SaveMyFamily_*`, `JAZZ_CombatHMMWV`) |
| Уникальные squad IDs, на которые ссылаются сектора | 87 |

Квесты по `Chapter`: Intro 12, Act1 24, Act2 8, Ernie_Rebels 3, Utility 7, без chapter 56.

Квесты по `QuestGroup`: Ernie Island 10, Savanah 12, Jungle 13, Pantagruel 10, The Fate Of Grand Chien 10, Wetlands 6, Port Cacao 5, Farmlands/Highlands/Other — остальное.

## Модель данных

Одна локация в данных = связка:

1. `ModItemSector` (`sectorId`, `mapName`, comment);
2. вложенный `SatelliteSector` (`display_name`, `InitialSquads`, `EnemySquadsList`, `StrongEnemySquadsList`, `ExtraDefenderSquads`, Events, POI-флаги);
3. каталог `Maps/<mapName>/` (геометрия не разбиралась в этом срезе);
4. при необходимости дубль в `CampaignPreset.Sectors`.

Враги на локации задаются прежде всего:

- **`InitialSquads`** — гарнизон при входе / conflict;
- **`EnemySquadsList` / `StrongEnemySquadsList`** — пул патрулей и атак с guardpost;
- **`ExtraDefenderSquads`** — дополнительные защитники outpost;
- map spawners внутри карты (не извлечены из `objects.lua` в этом срезе).

Составы отрядов резолвятся в `jazz-units` по ID squad def → слоты `EnemySquadUnit` с `unitType` (`JAZZ_Legion_*`) и диапазоном `UnitCountMin`/`Max`. Часть ID остаётся vanilla/не найдена в units package (`FortressPierre`, `LegionRaidSquad_01`, `LegionAttackers_Balanced_Easy` на срезе).

## Остров Эрни — локации и враги

Поддерживаемое демо. Старт: сектор **M1** («Зона высадки»), setpiece `M1Landing`.

| Сектор | Название | Роль / заметки | InitialSquads | Patrol / Strong / Extra |
|---|---|---|---|---|
| M1 | Зона высадки | Старт кампании; ForceConflict; event `JAZZ_LegionTier` | — | — |
| M2 | Скалистый берег | ForceConflict; квест «Спасти Кики» | — | — |
| M4 | Смотровая площадка | Label Ernie; ForceConflict; квест повстанцев | `LegionOutlook_Easy` | — |
| M5 | Береговая линия | ForceConflict | `LegionAttackers_JazzBalanced_Easy_Assault`, `LegionExtraSquadFireArms_T2` | — |
| M6 | Старый порт | Прибрежный бой | 2×`LegionExtraSquadFireArms_T2`, `LegionAttackers_Marksmen_Easy`, `LegionHeavyTroops_Gunners` | — |
| I2 | Лечебница в маяке | City ErnieVillage; три независимых wounded-маркера квеста доктора | 2×Marksmen_Easy, 2×Balanced_Easy, Mobile_Easy | — |
| I3 | Дорога к маяку | Блокпост / тайник для квеста доктора | 3×`LegionAttackers_Balanced_Easy` | — |
| I5 | Деревня Эрни | Главный хаб; ForceConflict; setpieces `ErnieReturn_FirstEnter`, `PierreLucTalk` | `LegionErnieVillage`, `LegionExtraSquadFireArms` | — |
| I6 | Жестянка | Связан с liberate / fortify | — | — |
| I6_Underground | Бункер FB45-68 | Underground I6; ForceConflict | — | — |
| I7 | Форт Ло-Блё | Guardpost; ForceConflict; цель `TakeTheFortress`; Global AI outpost (`ErnieIsland`) | `FortressPierre`, `FortressDefenders`, `LegionFortressDefenders`, `LegionAttackers_Ordnance_Easy` | Global AI: `LegionGlobalAI_Garrison` / `_Patrol` / `_Recon`, QRF `LegionJAZZSquadT2`; legacy Patrol/Strong/Extra списки без изменений |
| J4 | Дорога в Эрни | Переход | — | — |
| J5 | Фермы Эрни | City ErnieVillage | FireArms, 2×Shooters_Easy, Balanced_Easy | — |
| J7 | Изумрудный берег | Label Ernie; `EncounterHerman` / RescueHerMan; Herman groups `HermanShaking` + `Herman`; music Ernie_* | — | — |
| K4 | Флаговый холм | Label Ernie; ForceConflict; пять payoff-маркеров `Rebels_Help` привязаны к K4 | — | — |
| K5 | Походный лагерь Легиона | RescueTeam / RebelsSavior; после сдачи снабжения у палаток появляется `Merc_BarrySeal` | `JAZZ_Legion_SentrySquad_AroundVilla`, `JAZZ_Legion_VillaAttackers_K5` | — |
| K6 | Запасной лагерь контрабандистов | City ErnieVillage; `Jazz_DeadPigs`, четыре союзника Балумбы после принятия | — | — |
| L1 | База партизан | City Rebels_Ernie; квест MeetTheRebels | `LegionRaidSquad_01`, Heavy, `LegionJAZZSquadT2`, FireArms | — |
| L2 | Непроходимая местность | Rebels_Ernie | MeleeV2, Melee_T2, RaidSquad_01 | — |
| L5 | Походный лагерь Легиона | Около виллы | Sentry AroundVilla, `JAZZ_Legion_VillaAttackers_L5` | — |
| L6 | Заброшенный вход в бункер | Rebels_Ernie; Luigi / underground | `Legion_Patrol_1`, Melee_T2 | — |
| L6_Underground | Бункер партизан | Ground L6 | FireArms_T2, 2×RaidSquad_01, MeleeV2 | — |
| L7 | Рыбацкая деревня | City ErnieVillage | — | — |

Сектора `K3`/`L3`/`L4` упоминаются квестом `Jazz_ClearTheWay`, но не попали в фильтр Erny/Ernie label; проверять отдельно при работе с виллой.

### Ключевые squad defs Эрни (jazz-units)

Кратко по слотам (min–max : типы). Полные weighted lists — в `JAZZ Units/items.lua`.

| Squad ID | Смысл для локации | Типичный состав (сжато) |
|---|---|---|
| `LegionErnieVillage` | Гарнизон I5 | Много assault/pillager/crusher, marksmen, gunners (~десятки бойцов суммарно по слотам) |
| `LegionOutlook_Easy` | M4 смотровая | Veteran + 5 gunners + assault + marksman + flankers |
| `LegionAttackers_JazzBalanced_Easy_Assault` | M5 | Крупный штурмовой пакет (лидеры, assault, gunners, grenadiers) |
| `JAZZ_Legion_SentrySquad_AroundVilla` | K5/L5 охрана | Flankers/scouts + front T1 + optional gunner |
| `JAZZ_Legion_VillaAttackers_K5` / `_L5` | Атакующие у виллы | Captain/Headsman + pillagers/raiders + gunner; L5 тяжелее (mortarman) |
| `FortressDefenders` | I7 | Sniper, gunners, pillager, grenadier, captain, rocketeer |
| `LegionJAZZSquadT1` / `T2` | Патруль/strong I7 и L1 | Смешанные JAZZ_Legion tiers + bombard на T1 |
| `LegionJAZZSquadT1_Early` | NoMaps default remap (COMPAT-005) | **Только** class T1; alias → T2/T3 при gear major II/III |
| `LegionExtraSquadFireArms` / `_T2` | Доборы | Front/flanker/assault firearms packs |
| `LegionDefenders_Shooters_Easy` | J5 | Крупная стрелковая оборона + snipers + gunners |
| `LegionDefenders_Mobile_Easy` | I2 | Front/assault/flankers + hyenas |

Не найдены как `ModItemEnemySquads` в units package на срезе: `FortressPierre`, `LegionRaidSquad_01`, `LegionAttackers_Balanced_Easy` — вероятно vanilla defs или иное имя пакета.

## Остров Эрни — квесты

### Сюжет / Intro

| ID | Display | Hidden | Секторы (badges/refs) | Коротко |
|---|---|---|---|---|
| `01_Landing` | Встреча с нанимателем | нет | M1, I2, I5, J5, K4, K6, L7 | Клиент на Эрни; пробиться к цели |
| `02_LiberateErnie` | Освободить деревню Эрни | нет | I5, I7, J5 | Деревня / морской вывоз |
| `02A_LiberateErnie_2` | Освобождение острова Эрни | нет | — | Продолжение линии острова |
| `TakeTheFortress` | Fort L'Eau Bleu | нет | I6, I7, J7 | Угроза outpost Легиона |
| `ReduceFortressStrength` | How to reduce the Fort's defenses | да | — | Связка с механикой силы guardpost |
| `RescueHerMan` | Herman is missing | нет | I5, J7 | Похищение; setpiece EncounterHerman |
| `FortifyErnie` | Helping Ernie Village | нет | I5, I6, I6_Underground | Browning .50 для защиты I5 |
| `PierreDefeated` | Pierre | нет | I5, I7, K4, F19 | Пьер и информация о Майоре |
| `JoseFamily` | Bastien | нет | I6, E9 | Bastien |
| `LegionFlag` | Fooling Pierre | да | I7 | Скрытая ветка |
| `Ernie_CounterAttack` | — | да | I5, I7 | Контратака; squad def `ErnieCounterAttack` (~37; 1 RPG + 2 AssaultT1_Grenadier + 1 mortar) |
| `ErnieSideQuests` | — | да | I6, I7, M4 | Side logic Intro |
| `ErnieSideQuests_WorldFlip` | — | да | I5, I7 | Side после betrayal |
| `Demo` | — | нет | I7 | Demo marker |

### Повстанцы и JAZZ side content

| ID | Display | Секторы | Коротко |
|---|---|---|---|
| `JAZZ_REBELS_0_MeetTheRebels` | Повстанцы | L1 | Встреча с лидером |
| `JAZZ_REBELS_1_SeizeTheOutlook` | Атака на Смотровую Площадку | M4 | Захват M4 |
| `Jazz_Doctor_need_Help` | Неугодный доктор | I2, I3 | Медикаменты / мины / боеприпасы |
| `JAZZ_Ernie_Locals_M2_SaveMyFamily` | Спасти Кики | M1, M3 | Локальные NPC UnitData |
| `Jazz_ClearTheWay` | Зачистить лагеря вокруг Виллы | K3–K5, L3–L5 | Зачистка периметра виллы |
| `RescueTeam` | Мы в спасатели не нанимались | K5 | Спасти живого повстанца на пирсе и доложить сержанту |
| `RebelsSavior` | Снабжение для повстанцев | K5 | Сдать 4× Zastava M76 + 4× Medkit; открыть найм Barry Seal |
| `Jazz_LightHouseDefend` | Оборона маяка | — | Оборона от Легиона |
| `Jazz_DeadPigs` | Свинорез | K6 | Зачистка перебежчиков; одноразовый аванс и четыре союзника |
| `Jazz_Alkatraz` | Зачистить бункер | L1, L6_Underground | Зачистить подземный бункер и вернуться с докладом |

Линии Act2 (`04_Betrayal`, `05_TakeDown*`) ссылаются на сектора Эрни, но полный mainland-контент **вне поддерживаемого демо-scope**.

## Кампания за пределами Эрни (индекс, не демо-гарантия)

Полный список 110 квестов и 74 «боевых» сектора см. в рабочем извлечении; ниже — группы для ориентира.

**Основные сюжетные (The Fate Of Grand Chien):** `01_Landing` … `06_Endgame`, `03A_PresidentNotes`, `05_TakeDownMajor` / `Faucheux` / `Corazon`, `04_Betrayal`.

**Региональные группы:** Savanah (`RefugeeBlues`, `HunterHunted`, `DiamondRed`, …), Pantagruel, Jungle (`Sanatorium`, `Beast`, `Hermit`, …), Wetlands (`Elliot`, `Lenore`, crocodile camp helpers), Highlands (`Landsbach`, …), Farmlands (`TwinManors_copy`, …), Port Cacao, Other (MERC rescues, treasure, …).

**Guardposts с патрулями (примеры):** B28 Орлиное гнездо, **D18 Кам-Гран-При** (Global AI `MountainSteppe`), D28 Разлом, **E10 Кам-Саван** (Global AI `GreatDesert`), **G22 Кам-Шьен-Саваж** + **K21 Кам-Бьян-Шьен** (Global AI `GreatForest`, shared), **H19 Флитаун блошиный рынок** (Global AI `FleatownEnvirons`), I7 Форт Ло-Блё (Global AI `ErnieIsland`), **L15 Кам-Ла-Барьер** (Global AI `LaBarrier`, export patrol), **P17 Камп Де Крокодиль** (Global AI `PortCacaoEnvirons`) и др.

**Скрытые helper-квесты силы лагерей:** `Reduce*CampStrength` (Fortress, Crocodile, Barrier, BienChien, Savanna, Crossroads, River, Major).

Наличие записи в `items.lua` ≠ готовность к прохождению. За пределами Эрни ожидать незавершённые карты, баланс и ветки.

## Conversations, banters, локальные юниты

- 24 `ModItemConversation`, 41 `ModItemBanterDef` — полный ID-список в `items.lua`; менять только вместе с speaker UnitData и quest vars. Новая conversation `BarrySeal_Recruit` использует внешний UnitData `Merc_BarrySeal`.
- Maps-local UnitData: гражданские квеста SaveMyFamily (M2), `JAZZ_CombatHMMWV` (транспортный MVP, см. vehicles docs).

## Runtime flow (контент)

1. New game → campaign `HotDiamonds` → `InitialSector` M1 → setpiece `M1Landing`.
2. Satellite перемещение → tactical map по `Map`/`mapName`.
3. `InitialSquads` + map spawners формируют бой; managed Global AI outposts `I7` / `E10` / `D18` / `P17` используют role lists (garrison/patrol/recon/QRF).
4. Quest notes/badges и TCEs читают `QuestId` / sector events.
5. Conflict/loyalty/control возвращаются на сателлит (`FactionGrantLoyalty` и core strategy).

## Зависимости и пересечения

- Squad/UnitData IDs живут в `jazz-units`; переименование ломает сектора maps.
- Crocodile patrol: maps `System_JAZZ_CrocodilePatrol.lua` + core `SatelliteSquad.lua` hide-def guard + quest `ReduceCrocodileCampStrength` (триггер M1 вместо vanilla I1).
- Override matrix: пересечения patrol/setup — [override-matrix](../override-matrix.md); детали setpiece M1 — briefing maps package.

## Чек-лист проверки

- New game: M1 landing setpiece, выход на соседние сектора Эрни.
- I5 liberate + I7 fortress conflict; patrol spawn с I7.
- M4 outlook + L1 rebels quests; K5/L5 villa camps.
- SaveMyFamily NPC на M2/M3; отсутствие missing UnitData/squad ID в log.
- Existing save Эрни: quest vars и sector side.
- Mainland-сектора из каталога — только smoke «загружается», не полный acceptance.

## Известные ограничения и долг

- Снимок статический: map-only spawners и динамические TCEs не дают полный «кто стоит на карте прямо сейчас».
- Quest source strings исторически смешивают русский и английский, но активные mod-only IDs имеют синхронные runtime-переводы RU/EN; UI-smoke обеих локалей остаётся обязательным.
- Дубли/копии (`*_copy`, пустые DisplayName, utility quests без id в T-comment) присутствуют в данных.
- 317+ map directories на диске ≠ 245 campaign sectors и ≠ демо-scope Эрни.
- Temporary extract scripts не являются частью мода и не должны коммититься в `jazz-maps`.

## Контракт сопровождения

При изменении сектора, квеста, squad привязки или setpiece Эрни:

1. обновить эту страницу (таблица локации/квеста);
2. обновить [maps-quests-dialogue.md](maps-quests-dialogue.md) при смене schema/counts;
3. обновить wiki ernie-island-content.md и при необходимости strategy-and-world.md / content-and-limitations.md;
4. прогнать профильные smoke из [testing.md](../testing.md).
