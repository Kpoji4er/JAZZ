# Совместимость

## Проверенная база

Все четыре пакета сохранены с:

- `lua_revision = 233360`;
- `saved_with_revision = 366685`.

Локальная установка игры во время аудита соответствовала Steam app `1084160`, build `17409065`. Экспортированные исходники и документация брались из локальной папки `ModTools`.

JAZZ поддерживает только последнюю опубликованную CommonLib из официальной ветки `main`/Steam Workshop; совместимость со старыми версиями не заявляется. Перед каждой задачей и каждым поддерживаемым тестом upstream и установленная копия сверяются заново. Перед релизом `version_major`/`version_minor` объявленной зависимости `JA3_CommonLib` также обновляются до текущих значений upstream. На 26 июля 2026 года последним был CommonLib 1.11, build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c`; это снимок проверки, не pin. JA3 проверяет у dependency минимальную пару `version_major.version_minor`; автоматически увеличиваемый revision/build не является частью ограничения зависимости.

## Поддерживаемая конфигурация

- актуальная совместимая версия Jagged Alliance 3;
- `JA3_CommonLib`;
- `jazz_assets`;
- `jazz-units`;
- `jazz-maps`;
- основной `jazz`;
- стандартные расширенные настройки сложности;
- новая игра для полноценной проверки кампанийных изменений.

## Текущие расхождения metadata

- В `jazz` обязательным объявлен только `jazz_assets`.
- CommonLib и `jazz-units` указаны с `required = false`.
- Основной `jazz` объявляет минимальную CommonLib `1.11`, совпадающую с последним проверенным upstream/Workshop snapshot; автоматически меняющийся build не закрепляется.
- `jazz-maps` не объявлен зависимостью основного пакета.
- `jazz-maps` не объявляет зависимость от units, хотя содержит прямые ссылки на его ресурсы.
- Основной пакет содержит и загружает `English.csv` для собственных mod-only ID;
  английские строки vanilla остаются в базовой таблице игры.
- `jazz-units` загружает собственный корневой `English.csv` через `metadata.loctables`
  (`Mod/Dv3mFVN/English.csv`) для active mod-only ID пакета, включая пулы элитных имён;
  устаревший `ModTextsJazzUnits.csv` не подключён к loctables.

До исправления metadata документация считает полную коллекцию обязательной для **полного** кампанийного контента. Урезанный профиль без `jazz-maps` — опциональный пакет **`jazz-nomaps`** / display **JAZZ Vanilla Maps** (`7MsJ2Eq`, JAZZ-COMPAT-002): auto-regions по vanilla Guardpost, Major HQ `A20`, wiring отрядов и loot inject; квесты/карты/диалоги maps недоступны.

Playtest 2026-07-30 (Discord): cut loot/`MP5` и неполный remap — **исправлено** в jazz-nomaps **0.5** ([PR #1](https://github.com/Kpoji4er/JAZZ-nomaps/pull/1)); детали — [bugs/nomaps-playtest-2026-07-30.md](bugs/nomaps-playtest-2026-07-30.md).

COMPAT-003 (2026-07-31): NoMaps Global AI economy (nomaps **0.7–0.8**) + Legion gear tier на материке по времени: шахта+3д→II, WorldFlip→III, sub 3д/14д (`Code/LegionTierProgression.lua`); `GetRegionForSector` предпочитает `LegionAIEnabled`. **0.8:** sparse `gv_Squads` gear refresh, missing-def log, Thugs affiliation, tier hook after bootstrap.

COMPAT-004 (2026-08-01): NoMaps Global AI revive + UnitData remap + tiered container loot (nomaps **0.9** + jazz `Guardpost_Patrols` helpers). Major HQ force `A20`; adopt InitialSquads; seed POI; generic vanilla Legion → `JAZZ_Legion_*` pools; inject by `JAZZ_Legion_Tier`. Named/Hyena skip: stem match only with generic suffixes (`_Stronger` / `_Elite` / …), not `LegionRaider_Jose` (Bastien). Spec: [JAZZ-COMPAT-004](../specs/active/JAZZ-COMPAT-004.md).

## Конфликты с другими модами

Особенно высока вероятность конфликта с модами, которые изменяют CTH, оружие, inventory slots, броню, ранения, AI, awareness, UI, satellite squads, сектора, карты, погоду, видимость, те же UnitData, entities, localization IDs, engine messages или declared variables. `OnMsg` накапливается по registration order, а `MsgClear` способен удалить handlers всех слоёв.

Локальный мод JA3 имеет приоритет над подписанным Workshop-модом с тем же ID. Для воспроизводимого теста необходимо знать, какой экземпляр каждого пакета реально активирован.

## Совместимость localization ID

Numeric localization ID глобальны между vanilla и всеми активными модами.
Неизменённые поля клонированных vanilla ModItem используют original ID игры;
случайный ID, выданный редактором при clone, не считается публичным ID JAZZ.
Собственные строки JAZZ используют диапазон
`890000000000000..890000000099999`, предварительно проверенный против текущего
`Game.csv` и всех non-map Lua трёх пакетов. `Russian.csv` и `English.csv`
содержат одно и то же множество активных mod-only ID и не перекрывают vanilla
ID. Карта миграции хранится в
`Localization/IdMigration.csv`; изменение диапазона или повторная перенумерация
требуют нового cross-package аудита и проверки существующего сохранения.
## Совместимость сохранений

Изменения классов, предметов, UnitData, секторов, стратегических отрядов, `GameVar`/`MapVar`/`GlobalVar` и thread lifecycle могут требовать миграции. В репозитории есть незагружаемый `Savefix.lua`, но его присутствие на диске не означает активную поддержку миграций.

Любая намеренная полная замена vanilla-класса сохраняет исходные class name и preset ID и использует `UndefineClass('<Id>')` непосредственно перед `DefineClass.<Id> = { ... }`; переименование создаёт другой класс и не является replacement. `DamageReduction` следует этому общему правилу. Совместимость такого override проверяется по структуре класса, сериализованным данным и всем обращениям к исходному ID, а не по наличию namespace-префикса.

Game-time thread сохраняется вместе со стеком, upvalues и байткодом. Existing save после обновления способен продолжить старое тело функции, тогда как новые вызовы уже используют новый код. Поэтому совместимый рефакторинг coroutine или кода между `Sleep`/`WaitMsg` обязан учитывать обе версии до завершения старых потоков либо вводить явную миграционную границу.

### Save-контракт пилота Legion Global AI

`gv_JAZZ_LegionAI` имеет schema `1` и сериализует только числа, строки, boolean и таблицы ID: Major reserve/cooldown, region Heat/reports, outpost resources/timers и squad role/task/state/payload. На existing save состояние создаётся лениво; уже подготовленный `primed_squad` в `I7` принимается как managed garrison, а отсутствующие squad IDs удаляются reconciliation. Feature flag `Region.LegionAIEnabled` ограничивает новый consumer пилотом `ErnieIsland`.

`Guardpost_Patrols.lua` (JAZZ-STRATEGY-002) сохраняет base через `rawget(_G, ...)`, владеет `GetSatelliteIconImagesSquad` и оборачивает `SquadWindow:CreateRolloverWindow`; `TFormat.SquadNameColored` возвращён сохранённой base-реализации. Wrapper добавляет отдельный task-блок под составом только в совместимый `SquadRolloverMap`, а при отсутствии ожидаемого контейнера оставляет vanilla rollover без изменений. `POI Extension.lua` загружается позже и временно владеет `GetSatelliteIconImages`; Legion AI повторно wraps его после load/reload, резолвя icon по managed role PNG и делегируя unmanaged/POI в сохранённую base. Existing save reconciles `squad.image` по role; schema `gv_JAZZ_LegionAI` не менялась. Fresh CommonLib 1.11 эти символы не переопределяет, но любой более поздний мод может изменить итог.

Отсутствующий EnemySquad ID не вызывает assert/retry loop: соответствующий role spawn пропускается и диагностируется один раз. Полная поддерживаемая конфигурация пилота всё равно требует `jazz-units` и `jazz-maps`. Committed `jazz-units` preset `DiamondBriefcase` не задаёт требуемый vanilla `DiamondBriefcaseCarrier`; director компенсирует это только для своего динамического shipment, поэтому new-game путь `InitDiamondBriefcaseSquads` остаётся отдельным известным риском до исправления в пакете-владельце.

Проверять загрузку сохранения предыдущей поддерживаемой версии, создание новой игры, defaults declared variables, спящие game-time threads/repeats, инвентари существующих юнитов, предметы в контейнерах, стратегические отряды, сектора, активные квесты и setpieces.

## Ограничение asset pipeline

В Entity-описаниях assets обнаружены абсолютные ссылки на исходные FBX, расположенные на разных компьютерах. Runtime-ресурсы присутствуют, но полная воспроизводимая пересборка исходных моделей не гарантируется. Это не обязательно мешает игре, однако влияет на разработку и выпуск новых сборок.
## Сопровождение совместимости

Любое изменение публичного ID, save field, NetSync event, metadata order, dependency, generated schema или vanilla/CommonLib override обновляет профильную страницу [каталога систем](systems/README.md), эту страницу и тесты в той же задаче. Новые одноимённые пересечения заносятся в [override matrix](override-matrix.md).
