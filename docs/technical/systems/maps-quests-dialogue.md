# Карты, квесты и диалоги

## Назначение и эффект для игрока

`jazz-maps` является campaign/content-пакетом: он задаёт карту мира, тактические карты, сектора, квесты, разговоры, banters, loot, guardpost objectives и setpieces. Текущая публичная версия полностью ориентирована на остров Эрни; остальная кампания содержит незавершённые материалы. Именованный снимок квестов, секторов и вражеских squad refs — в [каталоге контента](maps-quests-content-catalog.md); пользовательский обзор Эрни — в wiki.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | Campaign/sector/map schemas, Map Editor serialization, quests, conversations, banters, setpieces, loot и loyalty APIs |
| CommonLib | Общая инфраструктура модов; прямых одноимённых коллизий с единственным loaded map code-файлом не подтверждено |
| JAZZ | 317 каталогов карт, generated campaign content, изменённые сектора/квесты/диалоги и loyalty helper |

## Реализация и load-state

- `jazz-maps/Code/Rebels_Loyalty.lua` — loaded runtime; определяет `FactionGrantLoyalty`.
- `jazz-maps/Code/System_JAZZ_CrocodilePatrol.lua` — loaded; патч `CampCrocodile_CirclingPatrol`: нейтрализует vanilla `OnMsg.ReachSectorCenter` из `HotDiamonds.lua` (иначе `for` по `nil` place, когда патруль не на G13–G14), переопределяет `SetupCrocodilePatrolSquad` на дом `I19` и маршрут `I18→I19→J19`. **Crash-guard в core:** `jazz/Code/SatelliteSquad.lua` перед `Msg("ReachSectorCenter")` временно снимает `enemy_squad_def`, если сектор вне vanilla G13–G14 (InitialSquad spawn на I19 больше не зависит от Msg wrap). Maps экспортирует `JAZZ_UpdateCrocodilePatrolOnReachSectorCenter` для remapped route; Msg wrap через `rawset(_G,"Msg",…)` остаётся как defense-in-depth. `Setup` всегда через RealTimeThread после `IsChangingMap` (TCE на M1 + sync `AssignSatelliteSquadRoute` иначе может столлить `NetSyncEventFence` на loading screen). Триггер квеста `ReduceCrocodileCampStrength` в JAZZ — сектор `M1` (ваниль: `I1`). Статический анализ; полный баланс/маршрут wetlands — отдельная задача.
- `jazz-maps/Code/AIMechanism.lua` — dormant/unlisted; содержит варианты AIM/stealth options, но metadata его не загружает.
- MapItem/ModItem definitions, `mapdata.lua`, `objects.lua`, grids и patches — generated and loaded согласно metadata/Map Editor.

Папка содержит 849 Lua-файлов и 2071 `.grid`; подавляющее большинство — данные, а не ручной runtime-код. Не форматировать и не переписывать их массово.

## Снимок данных

В metadata/items зарегистрировано:

- 1 campaign;
- 245 sectors;
- 110 quests;
- 41 banters;
- 24 conversations;
- 18 loot definitions;
- 4 guardpost objectives;
- 4 XTemplates;
- 4 InventoryItem definitions;
- 2 ChangeProp и 2 UnitData;
- 2 setpiece (`M1Landing` на стартовом M1 / map `EPA7FVN`, `EncounterHerman`);
- 1 camera preset и 9 constants.

Старт кампании: `InitialSector = M1` («Зона высадки»), не ванильный I1. На диске — примерно 317–321 map directories. Количество каталогов не равно количеству активных campaign sectors: служебные, варианты, underground и незавершённые карты могут не быть связаны с текущей кампанией. Около 23 секторов помечены как Эрни (`Label`/`City`/`WeatherZone=Erny` / `Rebels_Ernie`, включая J7 с `Label1=Ernie`); 74 сектора имеют хотя бы одну ссылку на enemy squad list.

## Campaign и sector schema

Sector definition связывает:

- sector ID и координату на satellite map;
- tactical map, underground/above-ground связь и входы;
- side/faction/control/conflict;
- region, POI, income и travel edges;
- guardpost/objectives;
- quests, events, conversations и banters;
- spawners, UnitData, squads и loot;
- weather/lightmodel и deployment markers.

Sector ID является публичным ключом savegame, quest state, strategic code и ссылок соседних пакетов. Переименование без миграции не допускается.

## Map runtime flow

1. Campaign создаёт sectors и strategic state.
2. SatelliteSquad выбирает вход/маршрут и инициирует tactical transition.
3. Deployment читает markers и размещает player/enemy/civilian units.
4. Map objects, grids, spawners и quest logic формируют tactical state.
5. Conversations/banters/setpieces реагируют на quest/sector/unit условия.
6. Conflict result, loyalty, loot и control возвращаются в strategic state/save.

## Квесты, разговоры и banters

110 Quest definitions хранят условия и эффекты, связанные с sector/unit/item/variable IDs. 24 conversations содержат ветвление и последствия; 41 banter — контекстные реплики. Активные mod-only строки синхронизируются в `Russian.csv` и `English.csv`; новый текст должен иметь один numeric ID, обе переведённые строки и проверку на коллизии.

Разговор нельзя безопасно менять изолированно: проверить speaker UnitData, map placement, quest variables, item rewards, loyalty/control effects и повторный вход в сектор.

### Контракт ремонта квестов Эрни (JAZZ-QUESTS-001)

- `RebelsSavior` завершается только после сдачи 4×`ZastavaM76` и 4×`Medkit`; после сдачи у палаток K5 появляется `Merc_BarrySeal` из `jazz-units`, которого бесплатно присоединяет разговор `BarrySeal_Recruit`.
- `Jazz_Doctor_need_Help` забирает ресурсы из player squads и требует независимо стабилизировать три wounded-маркера I2.
- `RescueTeam` считает спасение только при живом `Rebel_Hostage`; смерть заложника фиксирует failed outcome.
- `Jazz_DeadPigs` защищает аванс и выдачу боеприпасов от повторов; после принятия в K6 появляются четыре союзника группы `DeadPigs_Reinforcements`, не входящие в `Pigs`.
- `JAZZ_REBELS_1_SeizeTheOutlook` использует состояние `M4_UnderControl`; payoff-маркеры K4/M4 привязаны к собственным секторам и не despawn в тот же tick.
- `RescueHerMan` использует J7 в TCE и journal, marker Германа входит в группы `HermanShaking` и `Herman`, а обе sector-копии J7 вызывают `EncounterHerman`.
- `Jazz_Alkatraz` имеет заголовок и journal flow «L6 Underground → отчёт в L1»; фактическое runtime-условие зачистки всё ещё требует smoke-подтверждения.
- Кики (`JAZZ_Ernie_Locals_M2_SaveMyFamily_Woman`) загружается как `immortal` + `ImportantNPC`; Psycho-ветка выдаёт обещанный `BigDiamond`.

Generated source синхронизирован между `items.lua`, `ModTextsMaps.csv`, InventoryItem/UnitData companions и шестью `objects.lua`. Уровень evidence на 7 августа 2026: static PASS (`docs/tools/_audit_maps_quest_contract.py`); Map Editor round-trip и runtime-прохождение остаются обязательными acceptance-проверками.

### Vanilla quest sector remap (JAZZ-QUESTS-002)

Mainland / campaign vanilla quest clone’ы в `jazz-maps` ссылаются на **maps** sector IDs из [`sector-transfer.md`](../maps/sector-transfer.md) (+ runtime `I3→J7`, crocodile `H14→P17`). Ownership — только `jazz-maps` (`items.lua`, `ModTextsMaps.csv`); `jazz-nomaps` не меняется.

- Apply: `docs/tools/_apply_maps_vanilla_quest_sector_remap.py --apply`
- Audit: `docs/tools/_audit_maps_vanilla_quest_sectors.py --strict`
- Overloads: mine `H7→H14` ≠ crocodile `H14→P17`; custom `Jazz_*` keep maps-local I2/I3; `04_Betrayal` I3→J7 — временный долг до redesign World Flip; `D22`/`F23` — quest refs по таблице при `missing_moditem` sector stubs.
- Static evidence (2026-08-07): audit `--strict` OK после Wave A+B apply. Runtime smoke landmark chains — open.

## Setpiece и guardposts

Зарегистрированы setpiece `M1Landing` (высадка на M1) и `EncounterHerman` (линия Германа / map `qJApdx`). Четыре `GuardpostObjective` (`Bunker`, `EmeraldCoast`, `H4_copy`, `Bastien`) потребляются core `Guardpost.lua`. Их map markers и sector associations должны совпадать с runtime IDs.

## Loyalty

Loaded `Rebels_Loyalty.lua` добавляет `FactionGrantLoyalty`. Он работает рядом с core `Regions_Sectors.lua`, hourly updates и quest effects. Вызов должен корректно выбрать faction/region, ограничить диапазон и вызвать ожидаемое UI/state update.

## Межпакетные зависимости

- units: прямые ссылки на UnitData, squads, appearances, voices и banter speakers;
- core: items, effects, actions, guardpost/strategy/deployment APIs;
- assets: map props, weapon/unit entities, materials и textures.

Maps package не объявлен обязательной dependency в core metadata, хотя runtime-ссылки существуют. Поддерживаемая установка требует его наличия.

Найм Barry добавляет прямую ссылку maps → `jazz-units/UnitData/Merc_BarrySeal.lua`; поддерживаемый порядок профиля остаётся `assets → units → maps → jazz`.

## Generated data workflow

- карты, objects, grids и patches изменять через Map Editor;
- quests/conversations/banters/sectors — через соответствующие Mod Editor presets;
- после сохранения проверять metadata/items и все изменённые generated-файлы;
- не удалять каталог только потому, что он не связан с текущим сектором: сначала проверить variants, setpieces, quests и cross-package references;
- не активировать `AIMechanism.lua` случайным добавлением в metadata.

## Проверка

- вход/выход каждого поддерживаемого сектора Эрни с разных направлений;
- new game и existing save, surface/underground transitions;
- deployment markers, enemy/civilian spawns и loot;
- каждую изменённую quest branch, conversation choice и banter condition;
- `EncounterHerman`, guardpost objectives и conflict result;
- loyalty changes и satellite UI;
- отсутствие missing map/entity/unit/item/localization IDs;
- Map Editor load/save без непреднамеренной массовой регенерации.

## Сопровождение

Новый или изменённый sector/quest/conversation/banter/setpiece обновляет эту страницу, [каталог контента](maps-quests-content-catalog.md) при затронутых ID/привязках, strategy/wiki docs и профильные smoke tests. Load-state loaded Code-файлов maps всегда фиксировать явно.