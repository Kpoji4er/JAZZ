# Стратегия, отряды и сектора

## Назначение и эффект для игрока

JAZZ заменяет значительную часть satellite-логики: создание и перемещение отрядов, найм/увольнение, split/join, guardposts и патрули, нападения, регионы, POI-экономику, sector operations, deployment и World Flip. Это самый крупный cross-package и savegame-чувствительный контур.

## Происхождение по слоям

| Слой | Вклад |
|---|---|
| Vanilla | `SatelliteSquad`, sectors/regions, guardposts, conflicts, travel, deployment, operations, economy и game-over rules |
| CommonLib | Определяет `GetRandomSquadLogo` в `Code/ModItems.lua`; JAZZ позже заменяет его. Общие mod hooks могут добавлять события/данные |
| JAZZ | Крупные варианты SatelliteSquad/Guardpost/Deployment, новые POI/regions/operations, enemy power, world-flip spawns и maps/unit data |

## Реализация и load-state

Загружаемые core-файлы:

- `Code/SatelliteSquad.lua` — 4323 строки, центральный runtime отрядов;
- `Code/Guardpost.lua` — guardpost attacks, objectives, aggression и patrols;
- `Code/Guardpost_Patrols.lua` — loaded empty placeholder;
- `Code/SatelliteSquadFixes.lua` — loaded empty placeholder;
- `Code/EnemySquad.lua` — enemy squad definitions/power/autoresolve integration;
- `Code/Regions_Sectors.lua` — heat, panic, loyalty и hourly updates;
- `Code/POI Extension.lua` — точки интереса, доход и editor properties;
- `Code/System_SectorOperations.lua` — operations;
- `Code/Deployment.lua` — tactical deployment/return to exploration;
- `Code/WorldFlipSpawnUnits.lua` — spawning/attacks при world flip;
- `Code/UtilityFunc.lua` — utility side effects, включая Legion loot при открытии satellite view.

Dormant/unlisted core-файлы:

- `Code/EmptySquadFix.lua` — не загружается;
- `Code/PatrollingFix.lua` — не загружается; содержит дубль `PatrollingSquadSetDestination`, активная версия находится в `Guardpost.lua`;
- `Code/Savefix.lua` — не загружается.

Наличие этих файлов не означает, что fix применяется. Активация потребует отдельного анализа порядка и save migration.

## SatelliteSquad

Модуль заменяет/расширяет:

- создание, удаление, split/join и выбор отряда;
- hire status, assignment и squad membership;
- travel routes, arrival, retreat, rest и цены/время пути;
- intel/reveal и взаимодействие с sector state;
- death, despawn, revive и game-over paths;
- NetSync events и восстановление состояния при load/new game.

Он содержит множество `NetSyncEvents` и handlers `LoadSessionData`, new-game/hiring/travel/intel/death. Это делает сигнатуры событий, payload и порядок мутаций публичным сетевым/savegame контрактом.

## Guardposts и патрули

`Guardpost.lua` реагирует на `SatelliteTick`, `LoadSessionData`, `ConflictEnd`, squad travel/spawn/attack, new day/hour и sector/intel changes. Система вычисляет aggression, objectives, attack scheduling и patrol destinations.

`PatrollingSquadSetDestination` одновременно присутствует в loaded `Guardpost.lua` и dormant `PatrollingFix.lua`; итог runtime сейчас задаёт только loaded-файл. Нельзя переносить второй вариант без diff и тестов.

Maps добавляет четыре `GuardpostObjective` ModItems. Units предоставляет enemy squads/roles/UnitData, которые guardpost должен уметь создать.

## Enemy squads и autoresolve

Core `EnemySquad.lua` задаёт runtime/power и связи с autoresolve. Units содержит 69 generated enemy squad definitions. Squad composition соединяет UnitData, faction, archetype, loot и стратегическую силу; тактический spawn и autoresolve должны использовать совместимый состав.

Diamond shipment: vanilla `InitDiamondBriefcaseSquads` (`Lua/DiamondBriefcase.lua`, вызов из Campaign `Initialize`) делает `assert(EnemySquadDefs.DiamondBriefcase.DiamondBriefcaseCarrier)`. Carrier — индекс слота в `Units[]` с `UnitCountMin == UnitCountMax == 1`. Override `DiamondBriefcase` / `StartingShipments` в jazz-units обязан задавать `DiamondBriefcaseCarrier` (иначе assert `squadDefCarrier` на new game).

## Regions, loyalty, heat и panic

`Regions_Sectors.lua` обновляет региональные показатели на `NewHour`. Maps загружает `Code/Rebels_Loyalty.lua`, содержащий `FactionGrantLoyalty`. Loyalty, heat и panic связаны с control/conflict/POI и квестовыми последствиями.

Изменение tick interval или порядка updates может переиграть экономику существующего save, поэтому его нужно считать балансным и migration-sensitive.

## POI и экономика

`POI Extension.lua` добавляет/расширяет mine, farm, wood, slon и donations income, travel price и sector editor properties. Income зависит от sector/region state и времени. Данные являются одновременно gameplay rules и editor schema.

## Sector operations и лечение

`System_SectorOperations.lua` расширяет operations, включая взаимодействие с wounds/healing. Стоимость, длительность, merc assignment и результат должны согласоваться с tactical statuses и переходом времени.

## Deployment и World Flip

`Deployment.lua` — изменённый аналог vanilla deployment. NetSync `DeploymentToExploration` участвует в смене режима. `WorldFlipSpawnUnits.lua` создаёт attacks/units при смене состояния мира. Оба модуля зависят от map markers, sector IDs и UnitData.

## Прямое пересечение CommonLib

`GetRandomSquadLogo`: vanilla `SatelliteSquad.lua` → CommonLib `Code/ModItems.lua` → JAZZ `Code/SatelliteSquad.lua`. Обновления CommonLib могут добавлять поддержку custom logos, которую JAZZ-версия затем скрывает.

## Автотранспорт (maps)

Сателлитные машины (парковка / сесть / выйти / ускорение по дорогам) — `Code/System_JAZZ_Vehicles.lua`. Тактический Unit в `System_JAZZ_VehicleCombat.lua` сейчас dormant (`tactical_enabled=false`). Подробности: [Автотранспорт](satellite-vehicles.md).

## Межпакетные зависимости

- maps: campaign, 245 sectors, geography, quests, guardpost objectives, placed markers и satellite vehicles;
- units: UnitData, factions, 69 enemy squads, roles/archetypes;
- assets: map/entity resources;
- core: runtime, items, effects, economy, UI и serialization.

Основной metadata объявляет assets обязательным, CommonLib/units — optional, maps не объявлен, хотя прямые ссылки существуют. Поддерживаемая конфигурация требует все четыре пакета и CommonLib.

## Проверка

- new game и existing save;
- создание/split/join/rename/logo отряда, hire/fire/death/despawn/revive;
- travel, price/time, rest, route interruption и simultaneous squads;
- guardpost tick, patrol, attack, conflict end и objective;
- autoresolve против tactical spawn одного состава;
- hourly/new-day loyalty, heat, panic и income;
- sector operations, wounds и смена времени;
- deployment из разных входов и возврат в exploration/satellite;
- World Flip spawn;
- multiplayer NetSync и reconnect/load;
- отсутствие обращения к dormant fix-файлам как к активным.

## Ограничения и сопровождение

Satellite/guardpost files являются крупными изменёнными vanilla-копиями. После обновления игры выполнять трёхсторонний diff. Изменения events, GameVars, squad/sector IDs, travel state или операции всегда обновляют compatibility/testing и эту страницу.