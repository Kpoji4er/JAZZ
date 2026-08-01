# Стратегия, отряды и сектора

## Связанные specs

- `JAZZ-HOTFIX-001` — исправление cold-load globals, vanilla MapVar ownership и sector context для отсутствующего Region.
- `JAZZ-HOTFIX-002` — снять duplicate `OnMsg.SatelliteTick` из полного копипаста `SatelliteSquad.lua`; `GetMineIncome` возвращает `nil` при нулевом доходе.

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

`OnMsg` в движке **накапливает** handlers. Полный копипаст файла поэтому опасен: повторная регистрация того же `OnMsg.*` удваивает работу. JAZZ-HOTFIX-002 **не регистрирует** `OnMsg.SatelliteTick` (тело было идентично vanilla); единственный handler остаётся у vanilla и вызывает актуальные global overrides (`SatelliteUnitsTick` и др.). Другие duplicate `OnMsg` в том же файле пока не сняты — отдельный follow-up.

## Guardposts и патрули

`Guardpost.lua` реагирует на `SatelliteTick`, `LoadSessionData`, `ConflictEnd`, squad travel/spawn/attack, new day/hour и sector/intel changes. Система вычисляет aggression, objectives, attack scheduling и patrol destinations.

`PatrollingSquadSetDestination` одновременно присутствует в loaded `Guardpost.lua` и dormant `PatrollingFix.lua`; итог runtime сейчас задаёт только loaded-файл. Нельзя переносить второй вариант без diff и тестов.

Maps добавляет четыре `GuardpostObjective` ModItems. Units предоставляет enemy squads/roles/UnitData, которые guardpost должен уметь создать.

### Пилот Legion Global AI: `ErnieIsland` / `I7`

Пилот включён только для Region `ErnieIsland`, управляемого аванпоста `I7` и штаба Майора `B28`; остальные guardposts продолжают legacy-путь. Статическая конфигурация находится в Region/SatelliteSector presets, а изменяемый source of truth — versioned `GameVar("gv_JAZZ_LegionAI", ...)` со schema **`3`** ($ + manpower). Existing save со schema `1` мигрирует на `$` (v2), затем на manpower pools (v3). Начальный Heat региона — максимум Heat секторов с clamp `0..1000`; director сверяет существующие и исчезнувшие отряды.

Почасовой tick: base passive `$` (default **0**) пишется в `outpost.money` (capacity **120000**); mine `$` копятся в `diamond_stock` и едут shipment’ом. City/farm `$` **не** льются hourly в аванпост — копятся в `region_state.poi_money` пульсом раз в 3 суток (`POIGenerationInterval`; city **$2500** / farm **$800**; stock cap `PoiMoneyCap` **12000**) и доезжают ролью `tax`. Hourly tick в `major.money` не пишет. Major capacity **1200000**, starting **120000** (≥ одного supply cargo **12000**). Outpost starting **12000** (&lt; 40% supply-trigger) — supply-конвой легален сразу, spawn не форсируется. TaxCap **1**, TaxThreshold **1000**, TaxCargoMax **12000**, cooldown 24h. Раз в 6 часов командное окно завершает работы, обновляет retake-цели, назначает задачи и спавнит regular-отряды **только при нужде** и наличии `$`/manpower. Роли пилота:

- `garrison` — занимает key/POI (Outpost → City → Mine → Farm), только если сектор Легиона без обороны: нет managed garrison-задачи и нет уже стоящего Legion/enemy отряда (включая pre-placed);
- `patrol` — ходит по key/POI **включая player Side**; dwell **6–24h** в каждом секторе маршрута (`PatrolSectorDwellMin/Max`); предпочитает пустые сектора (нет player squad);
- `recon` — только при sector Heat ≥ `ReconHeatThreshold` («шум»); выходит к нагретому сектору, наблюдает; при обнаружении merc squad возвращает report (task UI называет сектор); при observation timeout без контакта один раз снижает Heat наблюдаемого сектора на `ReconNoContactHeatReduction` (default 50, clamp `0..1000`); **если своей задачи нет** — может взять assist `garrison`/`reinforce` (роль остаётся recon);
- `qrf` — только при угрозе: retake player key-сектора или свежий recon report; **если своей задачи нет** — тот же garrison assist;
- `reinforce` — пограничное усиление: Legion key/POI, соседний с player Side или player squad; иконка REINFORCE;
- `supply` — доставляет из `B28` `$` (`payload.money`); task UI показывает сумму; маршрут **может воду** (`land_water_boatless`, исключение для Major↔outpost); после сдачи → return HQ → rest; idle reuse;
- `tax` — обходит Legion economic POI с `region_state.poi_money` (не каждый City-tagged wilderness), собирает `$` до cargo max, сдаёт на аванпост (cap 1, threshold 1000, cooldown 24h); **не despawn** — rest на базе и reuse; city/farm `$` и recruits накапливаются пульсом раз в 3 суток (`POIGenerationInterval`); stock на POI capped (`PoiMoneyCap` 12000); missed pulses catch-up max 1 cycle;
- `recruiter` — спавнит `JAZZ_Legion_Recruit`; на базе strip всех Recruit → `outpost.manpower` (cap 32), излишек → `outbound_manpower`; **эскорт не retire** — rest + reuse; **не** делит суточный combat spawn-slot аванпоста (свой `RecruiterCooldown` / cap);
- `manpower` — Major→outpost **только при manpower=0**; обратный караван outpost→Major забирает `outbound_manpower`; после сдачи → rest, не RemoveSquad; тоже без combat spawn-slot;
- Combat spawn (`garrison`/`patrol`/`recon`/`qrf`/`reinforce`/`major`): только composition generator; без affordable состава — не спавнит; всегда списывает `$` + manpower по числу тел (без free EnemySquadDef fallback).
- garrison cap runtime = число важных Legion-секторов + 1; ослабленный гарнизон (≤10 living) возвращается на базу;
- максимум 1 managed spawn / сутки / аванпост;
- unlocked Hospital бафает managed Legion squads (`Inspired`, 24h; без HP-heal на satellite);
- `shipment` — везёт `$` shipment-stock из `I7` в `B28`; inventory = `lEnsureMoneyCargo`; после сдачи → return outpost → rest/reuse;
- `major` (Retribution) — при Heat региона 800+ создаёт/reuse ответ с HQ `B28`; после hold → return → rest; cooldown 72 часа.

**Lifecycle (JAZZ-STRATEGY-013):** happy-path **без RemoveSquad** (retire только living==0). После исчерпания `missions_left` отряд возвращается на home → state `resting` **12–36h** (`BaseRestMin/Max`, heal+top-up; **garrison без обязательного rest**) → refresh budget → `ready_for_orders`. Idle на базе только если после отдыха **нечего делать**. Recon/QRF без primary request могут assist гарнизон. Field understrength/wounded → retreat (012) → rest/wounded без despawn. Routing: land-first; water fallback; Major convoys exempt. `lRetireSquad` снимает отряд **сразу** на sync-пути планировщика (без `CreateRealTimeThread` / deferred RemoveSquad).
- Idle ready squads at home top-up toward optimal when resources allow, then take new orders.

У регулярных ролей есть mission budget; после исчерпания — return + rest (не удаление). Потеря `I7` переводит связанные регулярные отряды в `orphaned`, прекращает экономику и выдачу приказов; после возвращения контроля действует reboot delay 12 часов. Quest-forced attacks остаются в legacy `Guardpost.lua`, а обычный legacy spawn/patrol для managed `I7` блокируется, чтобы не было двойных отрядов.

### UI managed squad (JAZZ-STRATEGY-002)

Role icons — PNG в `SquadsIcons/Enemy/*.png` (без vanilla `_2`/`_s`), включая REINFORCE и RETRIBUTION для managed ролей. Каталог с превью и смыслом ролей (включая asset-only иконки и порты фракций): [squad-role-icons.md](squad-role-icons.md). Иконка резолвится по managed `role` через `JAZZ_GetLegionAISquadIcon` / `jazz_squad_icon`, не только по потенциально устаревшему `SatelliteSquad.image`. Фактический bind на карте: `SquadWindow:SpawnSquadIcon` → `GetSatelliteIconImagesSquad` → `XMapRollerableContextImage:SetImage` (draw читает `self.Image`, не `GetImage`). Перед `GenerateEnemySquad` director выставляет `g_JAZZ_LegionAIPendingSquadImage`, а `Guardpost.lua`/`GenerateEnemySquad` кладёт его в `CreateNewSatelliteSquad` predef — как diamond/weapon shipment — чтобы `Msg("SquadSpawned")` уже видел role PNG. После регистрации managed state вызывается явный `idSquadIcon:SetImage` refresh. `Guardpost_Patrols.lua` захватывает base `GetSatelliteIconImages*` через `rawget(_G, ...)`; после `POI Extension.lua` wrappers переустанавливаются на `ModsReloaded` / `LoadGame` / `InitSatelliteView` без recursive chain.

`SquadWindow:CreateRolloverWindow` после создания `SquadRolloverMap` добавляет `idJAZZLegionAITask` в стабильный VList под `idCurrentSquadCont`. Блок показывает `JAZZ_GetLegionAISquadTaskText` только для managed squad. Заголовок/имя: `lApplySquadRoleIcon` ставит `SatelliteSquad.Name` на role title (`Гарнизон`, `Вербовщик`, …), а не shared EnemySquadDef DisplayName (часто «Конвой»). Reconcile после load обновляет Name. Строки ролей/задач локализованы (`890000000001424`–`447`, `631`–`639`, `644`–`646`).

Планировщик использует абсолютный CampaignTime, сортированный обход и `InteractionRand`; интервалы защищены минимумом в один игровой час, а пропущенные интервалы снижения Heat догоняются после скачка времени. Public diagnostics `JAZZ_LegionAIGetDiagnostics()` / `JAZZ_LegionAIGetEconomy()` / `JAZZ_LegionAIPrintEconomy()` возвращают caps, costs, active counts и снимок `$`/manpower (Major, outposts, POI stocks).

## Enemy squads и autoresolve

Core `EnemySquad.lua` задаёт runtime/power и связи с autoresolve. Units содержит generated enemy squad definitions, включая четыре role presets `LegionGlobalAI_*` (JAZZ-STRATEGY-002). Squad composition соединяет UnitData, faction, archetype, loot и стратегическую силу; тактический spawn и autoresolve должны использовать совместимый состав.

Diamond shipment: vanilla `InitDiamondBriefcaseSquads` (`Lua/DiamondBriefcase.lua`, вызов из Campaign `Initialize`) требует `EnemySquadDefs.DiamondBriefcase.DiamondBriefcaseCarrier`. Текущий committed preset `DiamondBriefcase` в `jazz-units` имеет `DiamondBriefcase = true`, но не объявляет carrier; это существующее cross-package расхождение и отдельный риск new-game инициализации. Director пилота для динамического shipment использует `LegionGlobalAI_Convoy` и `lEnsureMoneyCargo`: полные $12000 → DiamondBriefcase, остаток → TinyDiamonds @$500 (округление вверх). Этот fallback обеспечивает груз пилота, но не считается исправлением общего vanilla startup-контракта. Managed Legion AI routes: **land_only first**, `land_water_boatless` только если суши нет; исключение — `supply`/`shipment`/`manpower` (конвои Major↔аванпост) сразу `land_water_boatless`.

## Regions, loyalty, heat и panic

`Regions_Sectors.lua` обновляет региональные показатели на `NewHour`. Maps загружает `Code/Rebels_Loyalty.lua`, содержащий `FactionGrantLoyalty`. Loyalty, heat и panic связаны с control/conflict/POI и квестовыми последствиями.

Для Region с `LegionAIEnabled` методы Heat читают/меняют `gv_JAZZ_LegionAI`; legacy Region продолжает хранить Heat в preset. Sector Heat и Region Heat пилота ограничены диапазоном `0..1000`. Старый hourly decay пропускает managed-регион, чтобы его не применяли одновременно два владельца; director снижает sector Heat на 10 и region Heat на 5 каждые 7 часов.

Generated `SatelliteViewMapContextMenu` считает отсутствие Region preset допустимым состоянием: скрывает region-блок, очищает его текст и не вызывает методы на `nil`. Loyalty показывается только для city-сектора без отдельного region-блока.

Изменение tick interval или порядка updates может переиграть экономику существующего save, поэтому его нужно считать балансным и migration-sensitive.

## POI и экономика

`POI Extension.lua` добавляет/расширяет mine, farm, wood, slon и donations income, travel price и sector editor properties. Income зависит от sector/region state и времени. Данные являются одновременно gameplay rules и editor schema.

`GetMineIncome(id, showEvenIfUnowned)` суммирует пять источников и **возвращает `nil` при сумме 0** (JAZZ-HOTFIX-002), чтобы vanilla `SectorsTick` мог early-out: в Lua `if 0 then` истинно, поэтому старый stub `(a or 0)+…` гонял income-ветку по всем секторам. Аргумент `showEvenIfUnowned` пробрасывается во все источники.

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

### Optional: `jazz-nomaps` / **JAZZ Vanilla Maps** (JAZZ-COMPAT-002)

Пакет `jazz-nomaps` (`7MsJ2Eq`, каталог `..\jazz-nomaps`, display title **JAZZ Vanilla Maps**) — **вместо** `jazz-maps`. Runtime: `Code/NoMaps_Autonomy.lua`.

Без maps (с nomaps):

- отключает maps-only Region `ErnieIsland` (I7/B28) и **очищает `Sectors`/`ManagedOutposts`**, чтобы I2–I7 не shadow'или `JAZZ_Auto_*` в `GetRegionForSector`;
- строит `JAZZ_Auto_<guardpost>` по vanilla Guardpost (A20, D10, E16, F7, F19, G10, H4, H14);
- Major HQ = **A20** (The Eagle's Nest);
- auto-region economy (COMPAT-003 / nomaps **0.7+**): `StartingManpower=40` (≥ garrison `size_min` 25), `TaxCap=1`, `RecruiterCap=1`, `ManpowerCapacity=64`, `MajorStartingManpower=120`, `PassiveSupplyPerHour=50`; saves мигрируют через `gv_JAZZ_NoMaps.ai_economy_rev`;
- COMPAT-004 (nomaps **0.9**): после bootstrap **force** `major.hq_sector=A20` (jazz `JAZZ_LegionAIForceMajorHQ`; EnsureState не latch'ит Ernie `B28` при NoMaps-профиле); adopt InitialSquads на managed outpost как garrison (`JAZZ_LegionAIAdoptOutpostDefenders`); seed `poi_money`/`poi_recruits` (`JAZZ_LegionAISeedPoiEconomy`); generic vanilla Legion UnitData → random `JAZZ_Legion_*` пул (named skip `_Jose`; `LegionRaider_WeakFlagHill`→assault T1 Roughneck; `*_Tutorial`→T1; `*_Stronger_Elite`→T4); container loot packs по major `JAZZ_Legion_Tier`;
- wiring/remap EnemySquad + loot inject + gear refresh;
- WorldFlip: `Code/WorldFlipSpawnUnits.lua` использует vanilla sector IDs и jazz-units Adonis/Army defs; nil-safe; fortress `H4` (fallback `I7`); nomaps ставит guard-wrap на `SpawnWorldFlipAttackSquads`;
- при загруженном `FhNNYd` — полный no-op.

`GetRegionForSector` (jazz) при нескольких совпадениях предпочитает region с `LegionAIEnabled`.

В core `jazz` встроенного StandaloneNoMapsFallback больше нет.

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