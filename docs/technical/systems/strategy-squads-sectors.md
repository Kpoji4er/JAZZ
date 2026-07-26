# Стратегия, отряды и сектора

## Связанные specs

- `JAZZ-HOTFIX-001` — исправление cold-load globals, vanilla MapVar ownership и sector context для отсутствующего Region.

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

- `Code/SatelliteSquad.lua` — крупный центральный runtime отрядов;
- `Code/Guardpost.lua` — guardpost attacks, objectives, aggression и patrols;
- `Code/Guardpost_Patrols.lua` — региональный director Legion Global AI, persistent state, экономика, задачи, маршруты, role icons и squad rollover;
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

`gameOverState` объявляет установленная vanilla через `MapVar`. JAZZ использует это же значение в скопированном game-over flow, но не регистрирует имя повторно: duplicate `MapVar` блокирует холодную загрузку ещё до выполнения логики.

## Guardposts и патрули

`Guardpost.lua` реагирует на `SatelliteTick`, `LoadSessionData`, `ConflictEnd`, squad travel/spawn/attack, new day/hour и sector/intel changes. Система вычисляет aggression, objectives, attack scheduling и patrol destinations.

`PatrollingSquadSetDestination` одновременно присутствует в loaded `Guardpost.lua` и dormant `PatrollingFix.lua`; итог runtime сейчас задаёт только loaded-файл. Нельзя переносить второй вариант без diff и тестов.

Maps добавляет четыре `GuardpostObjective` ModItems. Units предоставляет enemy squads/roles/UnitData, которые guardpost должен уметь создать.

### Пилот Legion Global AI: `ErnieIsland` / `I7`

Пилот включён только для Region `ErnieIsland`, управляемого аванпоста `I7` и штаба Майора `B28`; остальные guardposts продолжают legacy-путь. Статическая конфигурация находится в Region/SatelliteSector presets, а изменяемый source of truth — versioned `GameVar("gv_JAZZ_LegionAI", ...)` со schema `1`. Existing save создаёт состояние лениво, начальный Heat региона получает как максимум Heat его секторов с clamp `0..1000`, затем director сверяет существующие и исчезнувшие отряды.

Почасовой tick даёт `I7` supply и алмазный stock от удерживаемых Легионом городов, ферм и шахт. Раз в 6 часов командное окно завершает готовые работы, обновляет retake-цели, назначает следующие задачи и создаёт отряды до общего/ролевых лимитов при наличии supply. Роли пилота:

- `garrison` — занимает ключевые сектора по приоритету Outpost → City → Mine → Farm;
- `patrol` — после каждой точки заново выбирает город, шахту, ферму или базу;
- `recon` — выходит к нагретому сектору, наблюдает, при обнаружении merc squad возвращает target-specific report;
- `qrf` — расходует свежий report либо получает retake-задачу на занятую игроком ключевую точку;
- `supply` — доставляет из `B28` абстрактный supply и при возврате недоставленного груза восстанавливает резерв Майора;
- `shipment` — везёт накопленные алмазы из `I7` в `B28`;
- `major` — при Heat региона 800+ и наличии резерва создаёт отдельный тяжёлый ответ с cooldown 72 часа.

У регулярных ролей есть mission budget; после исчерпания отряд возвращается на базу и удаляется. Потеря `I7` переводит связанные регулярные отряды в `orphaned`, прекращает экономику и выдачу приказов; после возвращения контроля действует reboot delay 12 часов. Quest-forced attacks остаются в legacy `Guardpost.lua`, а обычный legacy spawn/patrol для managed `I7` блокируется, чтобы не было двойных отрядов.

Managed squad хранит role image из `SquadsIcons/Enemy`. `Guardpost_Patrols.lua` сохраняет vanilla base-функции через `rawget(_G, ...)` с fallback на текущую функцию, поэтому cold load не читает отсутствующий strict global, а hot reload не перезаписывает уже сохранённую base-ссылку. Его финальная `GetSatelliteIconImagesSquad` возвращает исходный 64×64 файл без vanilla-суффиксов `_2`/`_s`; более поздний по `metadata.code` `POI Extension.lua` владеет итоговой `GetSatelliteIconImages` и также возвращает `squad.image` напрямую. `SquadWindow:GetRolloverText` для managed squad добавляет строку `Задача:`; unmanaged squad получает исходный context без изменений.

Планировщик использует абсолютный CampaignTime, сортированный обход и `InteractionRand`; интервалы защищены минимумом в один игровой час, а пропущенные интервалы снижения Heat догоняются после скачка времени. Public diagnostics доступны через `JAZZ_LegionAIGetDiagnostics()`.

## Enemy squads и autoresolve

Core `EnemySquad.lua` задаёт runtime/power и связи с autoresolve. Units содержит 69 generated enemy squad definitions. Squad composition соединяет UnitData, faction, archetype, loot и стратегическую силу; тактический spawn и autoresolve должны использовать совместимый состав.

Diamond shipment: vanilla `InitDiamondBriefcaseSquads` (`Lua/DiamondBriefcase.lua`, вызов из Campaign `Initialize`) требует `EnemySquadDefs.DiamondBriefcase.DiamondBriefcaseCarrier`. Текущий committed preset `DiamondBriefcase` в `jazz-units` имеет `DiamondBriefcase = true`, но не объявляет carrier; это существующее cross-package расхождение и отдельный риск new-game инициализации. Director пилота не меняет units preset: для своего динамического shipment он детерминированно кладёт реальный `DiamondBriefcase` первому созданному юниту, задаёт drop chance 100% и помечает squad. Этот fallback обеспечивает груз пилота, но не считается исправлением общего vanilla startup-контракта.

## Regions, loyalty, heat и panic

`Regions_Sectors.lua` обновляет региональные показатели на `NewHour`. Maps загружает `Code/Rebels_Loyalty.lua`, содержащий `FactionGrantLoyalty`. Loyalty, heat и panic связаны с control/conflict/POI и квестовыми последствиями.

Для Region с `LegionAIEnabled` методы Heat читают/меняют `gv_JAZZ_LegionAI`; legacy Region продолжает хранить Heat в preset. Sector Heat и Region Heat пилота ограничены диапазоном `0..1000`. Старый hourly decay пропускает managed-регион, чтобы его не применяли одновременно два владельца; director снижает sector Heat на 10 и region Heat на 5 каждые 7 часов.

Generated `SatelliteViewMapContextMenu` считает отсутствие Region preset допустимым состоянием: скрывает region-блок, очищает его текст и не вызывает методы на `nil`. Loyalty показывается только для city-сектора без отдельного region-блока.

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

Сателлитные машины (парковка / сесть / выйти / ускорение по дорогам) — `Code/System_JAZZ_Vehicles.lua`. Тактический Unit в `System_JAZZ_VehicleCombat.lua` сейчас dormant (`tactical_enabled=false`). Runtime: [Автотранспорт](satellite-vehicles.md). Целевая модель боя (ещё не в коде): [JAZZ Maps — combat-vehicle-design](../../../JAZZ%20Maps/docs/combat-vehicle-design.md).

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