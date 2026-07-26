# Runtime, загрузка и инструменты

## Связанные specs

- `JAZZ-HOTFIX-001` — controlled manual transaction для load/runtime asserts и generated UI.

## Назначение

Эта страница описывает не отдельную механику, а условия, при которых все системы JAZZ действительно работают: четыре Git-репозитория, dependency/load order, metadata, generated files, engine messages, NetSync, Mod Editor и dormant-код.

## Пакеты и IDs

| Пакет | ID | Роль |
|---|---|---|
| `jazz` | `e6L4ECj` | core runtime, items, combat, UI, strategy, sound/FX |
| `jazz_assets` | `pDGDhr` | entities/resources |
| `jazz-maps` | `FhNNYd` | campaign/maps/sectors/quests/dialogue |
| `jazz-units` | `Dv3mFVN` | UnitData/squads/archetypes/loot/voices |
| CommonLib | `JA3_CommonLib` | dependency infrastructure/fixes |

Рабочий каталог может называться иначе у каждого автора. В документации используются только repository-relative paths и `<JA3_ROOT>`.

## Источники и их приоритет

1. Installed `<JA3_ROOT>\ModTools\Src` — текущий runtime reference.
2. [THQNordic/JaggedAlliance3Modding](https://github.com/THQNordic/JaggedAlliance3Modding) — история официального source drop.
3. Последний upstream `main` [ja3_commonlib](https://gitlab.com/injto4ka/ja3_commonlib) — dependency layer. Проверять HEAD и metadata перед каждой задачей; старые версии не являются целью совместимости.
4. Четыре текущих working tree JAZZ — product layer.

Проверенный GitHub source: HEAD `e8af7ec`, drop 1.5.0.349775 от 6 февраля 2024 года. Установленный ModTools новее. Из 4067 общих файлов 4020 совпали после нормализации EOL, 47 отличаются по содержимому; GitHub содержит ещё 412 файлов, installed source — один дополнительный. GitHub удобен для history/diff, но не заменяет installed source.

## Загрузка

Высокоуровневая последовательность:

```text
installed vanilla -> CommonLib/dependencies -> sibling JAZZ packages -> jazz core -> later third-party mods
```

Фактическую зависимость определяют metadata и Mod Manager. Внутри пакета Lua загружается строго в порядке массива `code` из `metadata.lua`, не по имени и не по файловой системе. Последнее объявление глобальной функции/метода обычно выигрывает, но `OnMsg`, presets, class mutations и delayed callbacks могут накапливаться.

Поддерживаемая установка требует последнюю опубликованную CommonLib и все четыре пакета, даже если metadata отмечает часть dependencies optional или не объявляет maps. Локальная или Workshop-копия CommonLib должна совпадать с текущим upstream; датированный commit в документации не закрепляет версию.

Dependency в Mod Editor задаёт минимальную пару `version_major.version_minor`; автоматически увеличиваемый revision/build в проверке зависимости не участвует. Выбор зависимости в редакторе может заново записать version fields, поэтому после editor save их нужно повторно сверять с текущей metadata CommonLib.

### Startup и hot reload

Официальный `LuaStartup` задаёт для модов следующий контракт:

1. Lua игры и DLC загружается раньше Mod Lua.
2. Моды упорядочиваются зависимостями; внутри мода сначала выполняется `options.lua`, затем файлы из `metadata.code`.
3. Во время mod-item reload Lua-код выполняется до загрузки ModItem. Доступ к editor-generated presets на верхнем уровне файла поэтому ненадёжен.
4. `ReloadLua` переиспользует существующий Lua-state и перезаписывает определения. Старые globals, таблицы, обработчики и потоки не исчезают только потому, что файл выполнился заново.
5. `FirstLoad` внутри mod sandbox не следует смешивать с глобальной lifecycle-семантикой vanilla.

Strict globals, существование которых не гарантировано на cold load, проверяются через `rawget(_G, "Name")`, а не выражением `Name or fallback`: второе само падает до применения fallback. Для hot reload сохранённую base-ссылку нельзя заменять текущей wrapper-функцией.

На верхнем уровне ручного `Code/*.lua` регистрируются definitions, class extensions и handlers. Работу с построенными классами и данными переносить на точную lifecycle-стадию:

| Стадия | Использование |
|---|---|
| `Autorun` | Завершение выполнения autorun Lua; данные ModItem ещё нельзя считать готовыми |
| `ClassesBuilt` | Работа с уже построенными классами |
| `DataLoaded` | Работа с загруженными presets и игровыми данными первого полного старта |
| `ModsReloaded` | Повторная настройка после reload модов, когда это поддерживает конкретная система |

Изменение lifecycle-стадии является изменением поведения, даже если тело обработчика не менялось.

## Generated data

Через Mod Editor/Map Editor создаются или регистрируются:

- `items.lua`, `metadata.lua` и ModItem files;
- InventoryItem, CharacterEffect, CombatAction, components, recipes и presets;
- UnitData, appearances, squads, loot и voices;
- sectors, maps, grids, objects, quests, conversations, banters и setpieces;
- entities и resource metadata.

Изменять generated object через редактор, если тип поддерживается. После сохранения проверять все связанные сериализованные файлы. Не смешивать функциональный refactor ручного Lua с массовой регенерацией.

Транзакция `JAZZ-HOTFIX-001` точечно меняет существующие `AttackShotgun`, `ParticlesThompson`, `ActionCameraCrosshair`, `RolloverInventoryWeaponBase` и `SatelliteViewMapContextMenu` в `items.lua`. `metadata.lua`, IDs, companions и `metadata.code` проверяются вместе, но не меняются при отсутствии contract delta. Перед следующим editor save мод нужно reload с диска, иначе открытое устаревшее состояние перезапишет hotfix.

Mod Editor является companion UI, но загрузку, сохранение и тест мода выполняет основная игра. Закрытие игры без сохранения теряет изменения. После открытия, загрузки, сохранения и reload обязательно просматривать панель сообщений: ignored mod, load error, runtime error или assert означают, что round-trip не подтверждён.

Preset определяется парой group/ID; совпавший ID способен заменить исходный preset. Команда Copy from перезаписывает свойства ModItem, а наличие ModItem само по себе не гарантирует эффекта без runtime-ссылки, spawn или loot registration.

Generated companion полной замены vanilla-класса обязан сохранять исходный class name/preset ID и заголовок `UndefineClass('<Id>')` → `DefineClass.<Id> = { ... }`. Префикс или другое имя создают параллельный класс. Отсутствие любой строки пары означает незавершённую generated-транзакцию и должно блокировать сохранение/релиз.

Entity export является инкрементальным и не удаляет устаревшие экспортированные части. После изменения структуры Entity очищать согласованный export state, повторно импортировать и перезапускать игру: уже загруженная Entity не обязана обновиться в текущем процессе.

## Ручные integration-модули

- `Code/EditorExtension.lua` — loaded editor/development helper; добавляет доступные ModItem preset types.
- `Code/InfiniteLoopFix.lua` — loaded runtime guard thresholds.
- `Code/Debug.lua` — loaded empty placeholder.
- `Code/UtilityFunc.lua` — loaded utility с gameplay side effect при satellite open.
- `Code/Savefix.lua` — dormant/unlisted.
- `Code/EmptySquadFix.lua` — dormant/unlisted.
- `Code/PatrollingFix.lua` — dormant/unlisted.
- `Code/AimHiringScreen_Template.lua` — dormant/unlisted.
- `Code/AIPolicyAttackAP.lua` — dormant empty placeholder.
- `jazz-maps/Code/AIMechanism.lua` — dormant/unlisted.

Loaded empty placeholders: `AIPolicyAttackAP.lua` не loaded; зато `Debug.lua`, `Guardpost_Patrols.lua`, `PushUnitAlert.lua` и `SatelliteSquadFixes.lua` входят в соответствующие категории по metadata/содержимому. Точный перечень — в [file coverage](file-coverage.md).

## Engine messages и NetSync

Крупные entry points:

- `ClassesBuilt`: enemy squad/class extensions;
- `DataLoaded`: specialization assignments;
- `LoadSessionData`: guardpost/satellite restoration;
- `NewHour`, new day, `SatelliteTick`: regions, income, attacks, patrols;
- conflict/turn/exploration/combat messages: awareness, Will, Grit;
- hire/despawn/container messages: inventory/squad bag;
- `OpenSatelliteView`: utility loot regeneration;
- NetSync: deployment, container open, squad/travel/hiring и другие satellite mutations.

Message handler не заменяется так же просто, как глобальная функция: несколько слоёв могут выполнить обработчики. Перед удалением JAZZ handler проверить vanilla/CommonLib side effects и ordering.

Официальная семантика сообщений:

- `Msg` синхронно завершает все handlers до возврата отправителю;
- handlers выполняются в порядке регистрации, поэтому порядок `metadata.code` влияет на наблюдаемый результат;
- `OnMsg` выполняется под защищённым вызовом, не должен спать, а ошибка одного handler не останавливает остальные;
- `PostMsg` откладывает отправку;
- `MsgClear` удаляет все handlers сообщения, включая vanilla, CommonLib и сторонние моды, поэтому для общих сообщений запрещён без доказанного владения;
- custom message, `MsgDef` и reaction IDs должны иметь префикс `JAZZ_` и совпадающие params.

## Сохранения, переменные и потоки

Savegame surfaces включают custom item/unit properties, resource/max resource, statuses, Will, squad/travel/guardpost/region state, sector/quest IDs, generated names и campaign data. Network surfaces включают `NetSyncEvents`, action payloads и детерминированный RNG (`BraidRandom`/engine mechanisms).

| Механизм | Жизненный цикл и риск |
|---|---|
| `GameVar` | Инициализируется для новой игры, сохраняется и получает default в старом save; не присваивать `nil` |
| `MapVar` | Сбрасывается на новой карте; не присваивать `nil` и не регистрировать повторно имя, уже объявленное vanilla. `gameOverState` принадлежит vanilla, JAZZ только использует его |
| `GlobalVar` | Использовать только после проверки конкретной save/map-семантики установленного source; для mutable table нужен новый initializer, а не общая таблица |
| game-time thread | Следует simulation time, удаляется при смене карты и сериализуется в save вместе со стеком, upvalues и байткодом |
| real-time thread | Подходит UI/application lifetime, не сериализуется как game-time thread и переживает паузу игры |

Сохранение способно возобновить спящий game-time thread со старым байткодом после обновления JAZZ. Поэтому рефакторинг coroutine/thread body проверяется не только новым вызовом: нужен existing save, созданный до изменения. Для периодической map-scoped работы предпочтительны `MapGameTimeRepeat` и `MapRealTimeRepeat`, если подходит их lifecycle: после reload/save они вызывают актуальную функцию. Repeat с `interval <= 0` обязан самостоятельно спать, иначе заморозит игру.

Рефакторинг без изменения поведения обязан сохранить:

- имена полей/IDs и значения по умолчанию;
- тип и lifecycle declared variables;
- game-time/real-time clock и точки yield/wakeup;
- порядок mutations/messages;
- RNG stream и число random calls;
- function signatures/returns;
- metadata order;
- side effects при clean start, load, new game и mod reload.

## CObject, map enumeration и UI context

Обычный `CObject` получает временную Lua-таблицу по мере обращения из Lua. Поля, записанные только в неё, могут исчезнуть после GC. Долгоживущее Lua-state должно принадлежать `Object`, declared state или другому устойчивому владельцу движка.

Map enumeration оптимизирован прежде всего для XY. Если логика зависит от высоты, после пространственного запроса нужен отдельный Z-фильтр. Для производительности:

- задавать максимально узкие area, class и flags;
- применять `MapCount` вместо `#MapGet`, если нужен только count;
- применять `MapForEach` или dedicated enum/flag operation вместо создания списка и Lua-цикла;
- не создавать массово временные Lua wrappers для декоративных `CObject` в hot path AI, visibility или UI.

В X UI `SubContext()` объединяет lookup нескольких объектов, но не становится владельцем их mutable state. Mutating-метод нужно вызывать на настоящем объекте, а не на результате `SubContext()`, иначе функция получит неправильный `self`. XTemplate/XWindow framework владеет переходом `new → open`; `OnContextUpdate` не должен повторно вызывать `Open` уже открытого child window. Именованные `XWindow:CreateThread` являются real-time threads и автоматически удаляются вместе с окном.

## Project skills и обязательная документация

Центральные repo skills:

- `.agents/skills/work-on-jazz-mod/SKILL.md` — процесс анализа и изменений;
- `.agents/skills/document-jazz-systems/SKILL.md` — обязательное обновление системной документации.

Документация — часть definition of done. Изменённая система, файл, load-state, dependency или collision обновляется в той же задаче. Read-only проверки:

```powershell
.agents/skills/work-on-jazz-mod/scripts/audit-project.ps1
.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1
```

## Проверка

- metadata paths существуют и порядок соответствует намерению;
- upstream HEAD/metadata CommonLib проверен, установленная копия является последней, четыре packages + CommonLib загружаются без errors/asserts;
- clean process, hot reload, new game и existing save, включая save со спящим game-time thread;
- панель сообщений Mod Editor не содержит ignored mod, load/runtime errors или asserts;
- lifecycle handlers не читают ModItem до готовности данных, порядок `OnMsg` подтверждён;
- `GameVar`/`MapVar`/`GlobalVar` сохраняют заявленный lifecycle и defaults;
- NetSync events в multiplayer;
- UI context mutations выполняются на настоящем объекте, XWindow threads удаляются с окном;
- map enumeration не создаёт лишние списки/wrappers в hot path;
- `git diff --check` отдельно в каждом репозитории;
- no absolute local paths в Markdown;
- dormant files не считаются active;
- system docs checker проходит;
- game runtime/Mod Editor тесты помечены отдельно от static audit.

## Ограничения и сопровождение

Standalone Lua compiler/linter в исходном аудите не использовался; runtime syntax подтверждается игрой/Mod Editor. CommonLib проверяется перед каждой задачей, а изменение её HEAD требует повторить source/collision audit и обновить датированный снимок в документации. Любое обновление JA3 также требует повторного аудита.