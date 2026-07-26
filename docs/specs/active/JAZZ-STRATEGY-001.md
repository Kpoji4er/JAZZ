---
id: JAZZ-STRATEGY-001
status: draft
owner: project-owner
systems:
  - legion-global-ai
  - regions-sectors
  - guardposts-squads
repositories:
  - jazz
  - jazz-maps
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-STRATEGY-001.md
  - jazz/Code/Guardpost_Patrols.lua
  - jazz/Code/Guardpost.lua
  - jazz/Code/Regions_Sectors.lua
  - jazz/Code/POI Extension.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/docs/technical/systems/strategy-squads-sectors.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/compatibility.md
  - jazz/docs/technical/override-matrix.md
  - jazz-maps/items.lua
  - jazz-maps/metadata.lua
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz-maps/items.lua
  - jazz-maps/metadata.lua
  - ModItemRegion:ErnieIsland
  - SatelliteSector:I7
  - GameVar:gv_JAZZ_LegionAI
related_decisions:
  - none
approved_by: pending
---

# JAZZ-STRATEGY-001: региональный Global AI Легиона — пилот ErnieIsland

## Проблема

В JAZZ уже существует часть заготовок стратегического AI, но они не образуют одну работающую систему:

- `Code/Regions_Sectors.lua` определяет Region и sector/region Heat, однако runtime Heat региона меняется прямо в preset-объекте и не имеет явного save-state;
- создан только один Region preset `ErnieIsland`;
- `Code/Guardpost.lua` использует vanilla-подобную глобальную агрессию и заранее подготовленные атаки, не учитывая ресурсы, регион, разведданные и жизненный цикл отрядов;
- sector properties уже содержат списки patrol/recon/QRF, но scheduler их не потребляет;
- `PatrollingSquadSetDestination` использует статические `EnemySquadDefs.waypoints`, а не ключевые точки региона;
- загруженный `Code/Guardpost_Patrols.lua` пуст;
- семь готовых изображений `legion_BASE/SUPPLY/SHIPMENT/RECON/QRF/PATROL/GARRISON_squad.png` не используются runtime;
- девять guardpost-секторов в `jazz-maps` не привязаны к полной системе Region presets;
- legacy global aggro может создавать атаки независимо от будущего регионального директора и тем самым дублировать спавн.

Игрок поэтому не видит на спутниковой карте автономную логистику и постоянно действующие силы Легиона, а потеря аванпоста не разрушает управление связанными отрядами.

## Цели

- реализовать детерминированного регионального директора Легиона с persistent save-state;
- проверить полный вертикальный срез на существующем регионе `ErnieIsland` и аванпосте `I7`;
- связать ресурсы аванпоста, supply/diamond convoys, лимиты и стоимость спавна;
- реализовать patrol, recon, garrison, QRF/retake и Major response как явные задачи;
- выдавать новые задачи только в командное окно аванпоста, кроме аварийного возврата разведки и реакции на потерю аванпоста;
- ограничить число завершённых задач каждого отряда и возвращать исчерпавший ресурс отряд на базу;
- сделать потерю `I7` фактически парализующей связанные регулярные отряды;
- сохранить quest-forced guardpost attacks и совместимые публичные функции legacy aggro;
- подготовить data-driven архитектуру, которую можно расширить на остальные регионы отдельным data-rollout change set.

## Non-goals

- одновременное включение всех девяти guardposts до runtime-приёмки пилота;
- AI фракций Army, Adonis, Rebels и нейтральных групп;
- новые UnitData, новые составы EnemySquads или перебалансировка существующих бойцов;
- тактический AI внутри боя, autoresolve-формулы и tactical vehicles;
- ручное изменение `jazz-maps/Maps/**`, mapdata, objects или grids;
- новый пользовательский экран управления AI;
- миграция или переименование существующих EnemySquad IDs;
- физический груз снабжения, выпадающий как новый InventoryItem: supply cargo в пилоте абстрактный, diamond shipment использует существующий `DiamondBriefcase`;
- окончательный баланс чисел пилота: значения ниже являются стартовым контрактом для runtime-теста и могут быть изменены новой ревизией spec.

## Термины и модель

- **Region** — статический preset с перечнем секторов и настройками регионального директора.
- **Outpost** — guardpost-сектор, принадлежащий Легиону и включённый в Region.
- **Major HQ** — стратегический источник supply convoys и Major response.
- **Role** — долговременная специализация отряда: `garrison`, `patrol`, `recon`, `qrf`, `supply`, `shipment`, `major`.
- **Task** — одна конечная работа отряда: перейти и удерживать, посетить POI, провести разведку, отреагировать на report, доставить груз или вернуться.
- **Command window** — дискретное время, когда конкретный Outpost завершает готовые задачи и назначает новые.
- **Report** — target-specific разведданные с sector ID, временем получения и сроком годности.
- **Ready for orders** — отряд завершил задачу и ждёт следующего командного окна своего Outpost.

## Архитектура

### Статические данные

`Region` и свойства guardpost-сектора содержат только authoring/config data. Runtime не изменяет preset.

Для пилота:

- Region: `ErnieIsland`;
- управляемый Outpost: `I7`;
- Major HQ: `B28`;
- остальные guardposts продолжают legacy-поведение.

`B28` выбран как стартовое предположение: в `HotDiamonds` он имеет label `Boss` и initial squad `A20_TheMajorsCamp`, тогда как сектор `A20` сейчас `Blocked`, `neutral` и без карты. Перед `approved` владелец подтверждает `B28` либо указывает другой фактически проходимый сектор.

Пилот переиспользует существующие squad definitions:

| Назначение | Предварительный EnemySquad ID |
| --- | --- |
| garrison | `LegionJAZZSquadT1` |
| patrol | `LegionAttackers_Balanced_Easy_Assault` |
| recon | `LegionOutlook_Easy` |
| qrf / retake | `LegionJAZZSquadT2` |
| Major response | `LegionJAZZSquadT3`, fallback `LegionHeavyTroops` |
| supply convoy | `LegionDefenders_Mobile_Easy` |
| diamond shipment | `DiamondBriefcase` |

IDs принадлежат `jazz-units`; в этой spec они только читаются и проходят cross-package spawn/autoresolve validation. Изменение их состава требует новой ревизии write set и generated-data транзакции в `jazz-units`.

### Runtime state

Единственный source of truth для новой системы — `GameVar("gv_JAZZ_LegionAI", ...)` со schema version. Он хранит только сериализуемые значения и ID:

```text
schema_version
major:
  hq_sector, reserve, next_supply_time, next_response_time
regions[region_id]:
  heat, intel_points, reports, outposts
outposts[sector_id]:
  enabled, supply, diamond_stock, next_command_time, reboot_until
squads[squad_id]:
  region_id, home_sector, role, state, missions_left, payload, task
```

Preset/object references, functions, threads и transient UI objects в GameVar не сохраняются. Записи squad state ссылаются на `gv_Squads` только по `UniqueId`.

Допустимые squad states:

```text
idle_at_base -> en_route -> working -> ready_for_orders
ready_for_orders -> en_route
ready_for_orders -> returning -> retired
any_regular_state -> orphaned
```

`retired` означает, что отряд достиг home Outpost, удалён с карты штатным `RemoveSquad`, а его state очищен по `SquadDespawned`.

### Tick и события

- Один лёгкий `OnMsg.NewHour` начисляет ресурсы, старит reports, проверяет recon observation и запускает просроченные command windows.
- Command window хранится абсолютным `next_command_time`, а не вычисляется через `hours % interval`, чтобы корректно переживать time skips и save/load.
- Обработчики `SquadFinishedTraveling`, `SquadDespawned`, `SectorSideChanged` и `ConflictEnd` только переводят state и не спят.
- Маршруты назначаются существующим network-safe route contract.
- Все custom messages имеют префикс `JAZZ_`.
- Все обходы выполняются по stable sorted IDs.

### Ресурсы и логистика

- Outpost генерирует local supply каждый час до capacity.
- Legion-controlled City и Farm в Region дают настраиваемый бонус supply.
- Legion-controlled Mine в Region создаёт diamond stock Outpost.
- Создание регулярного отряда атомарно проверяет local supply и role/total cap; стоимость списывается только после успешного spawn и валидного route/task state.
- Supply convoy создаётся в Major HQ, если Outpost ниже trigger threshold, нет другого inbound convoy, HQ имеет reserve и существует маршрут.
- Supply convoy доставляет абстрактный payload, после разгрузки возвращается в HQ и там retire.
- Diamond shipment создаётся в Outpost из существующего `DiamondBriefcase`, если накоплен shipment threshold и нет другого outbound shipment. Stock списывается только после успешного spawn/route.
- Доставленный shipment увеличивает Major reserve; уничтоженный shipment не возвращает stock.
- Захваченный или непроходимый HQ не создаёт supply convoys и Major response.

### Задачи регулярных отрядов

**Patrol**

- выбирает следующий target только из Region;
- eligible targets: Outpost, City, Mine, Farm;
- текущий сектор исключается, предыдущий target не исключается;
- после прибытия задача завершена, `missions_left` уменьшается, sector получает `LastPatrolledTime`, squad ждёт command window;
- target выбирается детерминированным weighted random с учётом POI priority, sector Heat и времени с последнего patrol.

**Recon**

- выбирает staging sector рядом с самым горячим eligible sector, но не входит намеренно в player-held target;
- во время observation раз в час видит player squad только в своём или соседнем surface sector;
- при контакте создаёт report с last-known sector и немедленно получает аварийную задачу `return_with_intel`, не ожидая command window;
- без контакта завершает observation по timeout, возвращается с меньшим количеством generic intel;
- report становится доступен QRF только после возвращения recon в home Outpost;
- report истекает через настроенное время и не даёт директору omniscient tracking после перемещения игрока.

**QRF / retake**

- fresh report создаёт QRF task на last-known sector;
- `SectorSideChanged` для приоритетного Region POI создаёт известную Outpost задачу retake без требования recon report;
- один report не может породить более одного QRF;
- QRF завершает задачу после `ConflictEnd`, после подтверждённого удержания target либо после признания target stale/unreachable в command window.

**Garrison**

- приоритет target: Outpost → City → Mine → Farm;
- player-held target сначала создаёт retake task для QRF; garrison не отправляется в заведомо вражеский сектор;
- Legion-controlled target без достаточного friendly presence может получить garrison;
- garrison task считается завершённой после одного полного command interval подтверждённого удержания, затем squad либо продолжает службу как новая задача, либо возвращается.

**Major response**

- при превышении регионального critical Heat и отсутствии активного Major response HQ создаёт один большой squad;
- target — самый горячий player-held или содержащий player squad сектор Region;
- response не зависит от local Outpost supply, но тратит Major reserve и имеет глобальный cooldown;
- потеря Outpost не отменяет уже созданный Major response, потому что им управляет HQ;
- уничтожение/потеря HQ блокирует новые response.

### Потеря аванпоста

Если `I7` перестал принадлежать Легиону:

- новые command windows, regular spawns и regular orders блокируются;
- squad в конфликте завершает конфликт;
- travelling regular squad отменяет продолжение route в первой безопасной sector-center точке и переходит в `orphaned`;
- idle/working regular squad остаётся в текущем секторе без новой задачи;
- inbound supply возвращается в HQ, outbound shipment продолжает путь в HQ;
- новый Major response всё ещё может быть создан HQ;
- после возвращения `I7` Легиону действует reboot delay, затем scheduler восстанавливает управление orphaned squads;
- уничтоженные или отсутствующие squads не воскрешаются при восстановлении.

### Task budget

- `missions_left` уменьшается только при терминальном завершении задачи, а не при каждом tick;
- при нуле squad получает `returning`;
- после достижения home Outpost squad retire и освобождает cap;
- если home Outpost потерян, squad остаётся `orphaned` и не выбирает другую базу автоматически в пилоте.

### Иконки

Runtime устанавливает существующее saveable поле `SatelliteSquad.image`:

| Role/state | Image |
| --- | --- |
| major | `Mod/e6L4ECj/SquadsIcons/Enemy/legion_BASE_squad` |
| supply | `Mod/e6L4ECj/SquadsIcons/Enemy/legion_SUPPLY_squad` |
| shipment | `Mod/e6L4ECj/SquadsIcons/Enemy/legion_SHIPMENT_squad` |
| recon | `Mod/e6L4ECj/SquadsIcons/Enemy/legion_RECON_squad` |
| qrf / retake | `Mod/e6L4ECj/SquadsIcons/Enemy/legion_QRF_squad` |
| patrol | `Mod/e6L4ECj/SquadsIcons/Enemy/legion_PATROL_squad` |
| garrison | `Mod/e6L4ECj/SquadsIcons/Enemy/legion_GARRISON_squad` |

### Legacy bridge

- Для managed Outpost `I7` обычный primed/aggro spawn `Guardpost.lua` выключен, чтобы не создавать бесплатные дубли.
- Quest-forced и queued script attacks сохраняют текущий путь и не требуют AI resources.
- Остальные восемь guardposts продолжают legacy `Guardpost`/global aggro behavior.
- `ModifySatelliteAggression`, `GetAggroAttackThreshold`, `SatelliteAggroInitiateAttack`, `gv_SatelliteAggro`, `gv_SatelliteAttacksHalted` и `gv_SatelliteAttacksHaltedFor` не удаляются и сохраняют сигнатуры.
- Global aggro не выбирает `I7` как источник legacy attack, пока пилот включён.
- Managed patrol squads не используют `EnemySquadDefs.patrolling=true`, чтобы `PatrollingSquadSetDestination` не назначил им старые static waypoints в `SquadSpawned`.

## Стартовые tuning values пилота

| Параметр | Значение |
| --- | ---: |
| Command interval | 6 h |
| Outpost reboot delay | 12 h |
| Starting supply / capacity | 150 / 500 |
| Passive supply | 5 / h |
| City / Farm supply bonus | 2 / 3 per h |
| Mine diamond production | 5 / h |
| Supply convoy trigger / cargo | 40% / 100 |
| Diamond shipment threshold | 50 |
| Major starting reserve | 1000 |
| Total regular squad cap | 6 |
| Role caps | garrison 2, patrol 2, recon 1, qrf 1 |
| Spawn costs | garrison 60, patrol 40, recon 30, qrf 80 |
| Default missions | garrison 3, patrol 3, recon 2, qrf 2 |
| Recon Heat threshold | 250 |
| Recon observation | 3 h |
| Report expiry | 24 h |
| Major response Heat / cost / cooldown | 800 / 200 / 72 h |
| Sector Heat decay | 10 every 7 h |
| Region Heat decay | 5 every 7 h |

Все Heat значения ограничены диапазоном `0..1000`. Existing `ErnieIsland.Heat = 1528` не используется как mutable runtime state; new game начинает с 0, а existing save migration выводит региональный Heat из сохранённых sector Heat с clamp.

## Требования

- `JAZZ-STRATEGY-001-REQ-001` — runtime-владелец системы находится в `jazz/Code/Guardpost_Patrols.lua`; sector authoring принадлежит `jazz-maps`, EnemySquad IDs — `jazz-units`.
- `JAZZ-STRATEGY-001-REQ-002` — static Region/sector config и mutable runtime GameVar разделены; runtime не изменяет preset.
- `JAZZ-STRATEGY-001-REQ-003` — `gv_JAZZ_LegionAI` имеет schema version, deterministic defaults, load reconciliation и existing-save migration.
- `JAZZ-STRATEGY-001-REQ-004` — scheduler использует `NewHour`, absolute next times и неблокирующие event handlers.
- `JAZZ-STRATEGY-001-REQ-005` — Outpost supply, diamond stock и Major reserve начисляются/списываются атомарно и имеют capacity/threshold.
- `JAZZ-STRATEGY-001-REQ-006` — spawn невозможен без ресурсов, role cap, total cap, существующего preset и валидного sector/route.
- `JAZZ-STRATEGY-001-REQ-007` — patrol выбирает Region POI динамически и ждёт command window после завершения каждой задачи.
- `JAZZ-STRATEGY-001-REQ-008` — recon наблюдает локально, возвращается с report/generic intel и не передаёт report до home arrival.
- `JAZZ-STRATEGY-001-REQ-009` — QRF потребляет не более одного fresh report и поддерживает известные retake tasks.
- `JAZZ-STRATEGY-001-REQ-010` — garrison соблюдает приоритет Outpost → City → Mine → Farm и не входит в player-held target до retake.
- `JAZZ-STRATEGY-001-REQ-011` — Major response имеет отдельный reserve, один active response на Region и cooldown.
- `JAZZ-STRATEGY-001-REQ-012` — supply и diamond convoys имеют раздельные роли, payload, interception loss и destination handling.
- `JAZZ-STRATEGY-001-REQ-013` — каждый regular squad имеет конечный mission budget, возвращается home и retire.
- `JAZZ-STRATEGY-001-REQ-014` — потеря Outpost парализует regular command chain и восстанавливается только после Legion recapture и reboot.
- `JAZZ-STRATEGY-001-REQ-015` — все семь существующих Legion squad icons подключены через `SatelliteSquad.image`.
- `JAZZ-STRATEGY-001-REQ-016` — managed AI не дублируется legacy guardpost/aggro, но forced quest attacks и публичные legacy symbols сохраняются.
- `JAZZ-STRATEGY-001-REQ-017` — new game, existing save, save/load mid-route и reload reconciliation не создают дубли squads/resources/reports.
- `JAZZ-STRATEGY-001-REQ-018` — random/iteration/route mutations детерминированы и совместимы с multiplayer NetSync.
- `JAZZ-STRATEGY-001-REQ-019` — debug diagnostics показывают Region, Outpost resources, managed squads, tasks, reports и причины отказа spawn без нового player-facing UI.
- `JAZZ-STRATEGY-001-REQ-020` — пилот включён только для `ErnieIsland`/`I7`; расширение на остальные регионы выполняется после приёмки отдельным data-rollout spec.

## Инварианты и ограничения

- Не сканировать и не изменять `jazz-maps/Maps/**`.
- Не менять составы и IDs в `jazz-units` этой spec.
- Не создавать real-time/game-time sleeping thread; scheduler событийный.
- Не присваивать `nil` GameVar и не хранить persistent state только в `CObject`.
- Не выполнять random iteration через `pairs` в ветках, влияющих на spawn, target или route.
- Не считать static analysis заменой runtime/editor/multiplayer evidence.
- Не менять quest-forced attack timing/payload без отдельного требования.
- Не удалять legacy GameVar/functions, потенциально доступные vanilla effects или saves.
- Не назначать новый task squad в конфликте, mid-route или до terminal completion.
- Не списывать resource/cargo до подтверждённого создания squad и валидного route.
- Существующие незакоммиченные изменения во всех пакетах не входят в change set.

## Acceptance criteria

- `JAZZ-STRATEGY-001-AC-001` — на новой игре создаётся ровно один runtime state `ErnieIsland`/`I7`, повторная инициализация/ReloadLua не дублирует state или squads.
- `JAZZ-STRATEGY-001-AC-002` — existing save без `gv_JAZZ_LegionAI` мигрирует без ошибки; Heat находится в `0..1000`, отсутствующие IDs очищаются.
- `JAZZ-STRATEGY-001-AC-003` — за фиксированный интервал I7 получает ожидаемый supply/diamond income с cap и одинаковым результатом после save/load.
- `JAZZ-STRATEGY-001-AC-004` — при недостатке supply или достигнутом cap spawn не происходит и resource не меняется.
- `JAZZ-STRATEGY-001-AC-005` — patrol I7 последовательно посещает eligible Ernie POI, не выбирает текущий sector и получает новый target только в command window.
- `JAZZ-STRATEGY-001-AC-006` — recon у hot sector обнаруживает локальный player squad, возвращает один report в I7, после чего report становится доступен QRF.
- `JAZZ-STRATEGY-001-AC-007` — QRF потребляет report один раз, идёт в last-known sector и корректно завершает/stale-отменяет task.
- `JAZZ-STRATEGY-001-AC-008` — player-held priority POI получает retake до garrison; после Legion capture туда может быть назначен garrison.
- `JAZZ-STRATEGY-001-AC-009` — при critical regional Heat из B28 создаётся не более одного Major response, reserve списывается один раз и cooldown соблюдается.
- `JAZZ-STRATEGY-001-AC-010` — supply convoy доставляет payload из B28 в I7; уничтожение до прибытия не увеличивает I7 supply.
- `JAZZ-STRATEGY-001-AC-011` — diamond shipment вычитает stock один раз, использует `DiamondBriefcase`, доходит до B28 и пополняет Major reserve либо теряет cargo при уничтожении.
- `JAZZ-STRATEGY-001-AC-012` — squad с нулём `missions_left` возвращается в I7, despawn/retire освобождает cap и очищает state.
- `JAZZ-STRATEGY-001-AC-013` — при player capture I7 regular squads становятся orphaned и не получают orders/spawns; после Legion recapture и 12 h reboot управление восстанавливается без resurrection.
- `JAZZ-STRATEGY-001-AC-014` — все семь roles отображают предназначенные изображения после spawn и после save/load.
- `JAZZ-STRATEGY-001-AC-015` — I7 не создаёт legacy primed/global-aggro дубли, но существующий forced quest attack проходит.
- `JAZZ-STRATEGY-001-AC-016` — одинаковый save/seed даёт одинаковые spawn IDs, targets, resource totals и routes; multiplayer host/client не расходятся.
- `JAZZ-STRATEGY-001-AC-017` — Mod Editor round-trip сохраняет `ErnieIsland` и `I7` data; strict generated sync проходит для `jazz` и `jazz-maps`.
- `JAZZ-STRATEGY-001-AC-018` — spawn/autoresolve/tactical entry проверены для каждого переиспользованного EnemySquad ID без изменения `jazz-units`.
- `JAZZ-STRATEGY-001-AC-019` — static checks не находят коллизий GameVar, custom Msg, class properties и public signatures; metadata подтверждает load order.
- `JAZZ-STRATEGY-001-AC-020` — technical current-state docs, compatibility/override matrix, file coverage и evidence синхронизированы с фактической реализацией.

## Impact и совместимость

- **Vanilla/CommonLib/JAZZ:** меняются loaded override `Guardpost.lua` и Region runtime semantics. Перед реализацией требуется свежий vanilla/CommonLib symbol audit для guardpost lifecycle, route assignment, `SatelliteSquad` serialization и diamond shipment.
- **Saves:** добавляется versioned GameVar и migration. Старые `gv_SatelliteAggro*` сохраняются. Region preset Heat перестаёт быть runtime storage.
- **Network/determinism:** spawn, route, target selection, resources и task transitions влияют на simulation; обязательны sorted iteration, engine deterministic RNG и multiplayer validation.
- **Generated data:** `ErnieIsland` в `jazz/items.lua` и sector `I7` в `jazz-maps/items.lua` меняются через Mod Editor одной транзакцией со своими metadata/companion layers.
- **Cross-package references:** core читает `EnemySquadDefs` из `jazz-units` и sector data из `jazz-maps`. Missing optional package не должен приводить к assert loop: AI отключается с одной диагностикой.
- **Assets:** используются уже существующие repository-relative PNG; бинарные assets не меняются.
- **Rollback/recovery:** feature flag Region выключает пилот и оставляет legacy guardposts. Полный rollback удаляет новый GameVar consumer, возвращает legacy I7 scheduling и сохраняет unknown save field без присваивания `nil`.

## План и ownership

1. `jazz` — выполнить compatibility audit и реализовать state/config boundary в `Regions_Sectors.lua`.
2. `jazz` — реализовать director в загруженном пустом `Guardpost_Patrols.lua`.
3. `jazz` — добавить минимальный legacy bridge в `Guardpost.lua`, не переписывая quest attack path.
4. `jazz` — добавить/уточнить editor properties в `POI Extension.lua`.
5. `jazz` + `jazz-maps` — через Mod Editor настроить `ErnieIsland` и `I7`, затем выполнить strict generated sync.
6. `jazz-units` — read-only validate перечисленные EnemySquad IDs, spawn, tactical/autoresolve и diamond carrier contract.
7. Выполнить static, editor, runtime, save/load и multiplayer сценарии по AC.
8. Обновить current-state technical docs и записать evidence.

- Пакет-владелец runtime: `jazz`.
- Пакет-владелец Region preset: `jazz`.
- Пакет-владелец sector `I7`: `jazz-maps`.
- Пакет-владелец EnemySquad IDs: `jazz-units` (read-only в этой spec).
- Исполнитель: Codex после approved DoR.
- Reviewer: независимый reviewer.
- Declared write set: только front matter `write_set`.
- Exclusive resources: только front matter `exclusive_resources`.

## Решение владельца

Для перевода в `approved` владелец проекта должен одним решением подтвердить или изменить:

1. пилот сначала только на `ErnieIsland`/`I7`, затем отдельный rollout остальных guardposts;
2. `B28` как Major HQ вместо blocked `A20`;
3. стартовые tuning values и предварительные EnemySquad mappings из этой spec.

- Статус: ожидает решения.
- Кто подтвердил: pending.
- Дата: pending.

## Evidence

- `JAZZ-STRATEGY-001-AC-001`: `BLOCKED` — реализация не начата.
- `JAZZ-STRATEGY-001-AC-002`: `BLOCKED` — migration не реализована.
- `JAZZ-STRATEGY-001-AC-003`: `BLOCKED` — runtime economy test не выполнен.
- `JAZZ-STRATEGY-001-AC-004`: `BLOCKED` — cap/resource test не выполнен.
- `JAZZ-STRATEGY-001-AC-005`: `BLOCKED` — patrol runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-006`: `BLOCKED` — recon runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-007`: `BLOCKED` — QRF runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-008`: `BLOCKED` — retake/garrison runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-009`: `BLOCKED` — Major response runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-010`: `BLOCKED` — supply convoy runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-011`: `BLOCKED` — diamond shipment runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-012`: `BLOCKED` — task budget/retire runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-013`: `BLOCKED` — Outpost capture/recapture runtime test не выполнен.
- `JAZZ-STRATEGY-001-AC-014`: `BLOCKED` — icon/save-load visual test не выполнен.
- `JAZZ-STRATEGY-001-AC-015`: `BLOCKED` — legacy/forced attack test не выполнен.
- `JAZZ-STRATEGY-001-AC-016`: `BLOCKED` — deterministic multiplayer test не выполнен.
- `JAZZ-STRATEGY-001-AC-017`: `BLOCKED` — editor round-trip/generated sync не выполнен.
- `JAZZ-STRATEGY-001-AC-018`: `BLOCKED` — cross-package squad validation не выполнена.
- `JAZZ-STRATEGY-001-AC-019`: `BLOCKED` — static/load-order audit не выполнен.
- `JAZZ-STRATEGY-001-AC-020`: `BLOCKED` — documentation delta не реализована.

## Documentation delta

- `docs/technical/systems/strategy-squads-sectors.md` — фактическая state machine, economy, events, legacy bridge и validation state.
- `docs/technical/systems/file-coverage.md` — `Guardpost_Patrols.lua` перестаёт быть empty placeholder.
- `docs/technical/compatibility.md` — save/network/CommonLib и optional package behavior.
- `docs/technical/override-matrix.md` — изменённые guardpost/region symbols и load order.
- Пользовательская wiki отсутствует и не входит в DoD.
