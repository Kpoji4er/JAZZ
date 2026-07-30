# Разработка

## AI-first-модель

25 июля 2026 года JAZZ перешёл от полностью ручной разработки к AI-first-процессу для всех четырёх пакетов. AI-агент является основным исполнителем исследования, реализации, рефакторинга, документации и статических проверок; владелец проекта сохраняет продуктовые решения, приёмку и runtime-проверку. Полная граница периодов и ответственности зафиксирована в [решении о переходе](ai-first-development.md).

AI-first не расширяет полномочия задачи и не превращает существующую ручную кодовую базу в «AI-generated» задним числом.

## Экономия контекста

- Исследование начинается с точного ID, `metadata.lua`, профильной документации и узкого поиска.
- Большие файлы читаются диапазонами; повторное чтение неизменившегося источника и полные дампы не используются без необходимости.
- Generated/binary каталоги исключаются из обзорных обходов.
- `jazz-maps/Maps/` не анализируется рекурсивно без прямого указания на эту папку, конкретную карту, сектор или map patch. Для явно картографической задачи поиск начинается с названного пути; полный обход остаётся крайней мерой.

## Базовые источники

Перед изменением поведения использовать официальный GitHub для истории и установленный ModTools для текущего runtime. `<JA3_ROOT>` означает корень игры на машине разработчика; его абсолютное значение не хранится в репозитории:

- <https://github.com/THQNordic/JaggedAlliance3Modding> — versioned-история официальных source drops;
- `<JA3_ROOT>\ModTools\Src` — актуальные экспортированные Lua-исходники и данные установленной игры;
- `<JA3_ROOT>\ModTools\Docs\index.md.html` — индекс официальной документации;
- `<JA3_ROOT>\ModTools\Samples` — официальные примеры;
- <https://gitlab.com/injto4ka/ja3_commonlib> — текущий upstream CommonLib. Перед каждой задачей проверить HEAD `main` и metadata; перед релизом обновить `version_major`/`version_minor` объявленной зависимости до текущих значений upstream. JAZZ не поддерживает закреплённые старые версии.

Особенно полезны `LuaStartup`, `LuaMessages`, `LuaReactions`, `LuaClasses`, `LuaVars`, `LuaSavegame`, `LuaThreads`, `LuaRepeats`, `LuaCObject`, `LuaMapEnumeration`, `LuaUI`, `ModItemCode`, `ModItemLocTable`, `ModItemEntity`, `MapEditor`, `GridMarkers`, `Pathfinding`, `Destruction` и `JA3_AI`. Сводный обязательный контракт вынесен в [runtime, загрузку и инструменты](systems/runtime-editor-integration.md).

## Spec-Driven рабочий цикл

1. Сформулировать problem, goals и non-goals в `docs/specs/active/<SPEC-ID>.md`.
2. Зафиксировать `REQ-*`, invariants, `AC-*`, package ownership, declared write set и exclusive resources.
3. Получить решение владельца проекта и пройти DoR через `$specify-jazz-change`.
4. Только после approval исследовать точные vanilla/CommonLib/JAZZ symbols и построить минимальный implementation plan.
5. Внести изменение в package-owner, не выходя за write set без ревизии spec.
6. Выполнить профильные static/generated/editor/runtime проверки и записать evidence для каждого `AC-*`.
7. Синхронизировать `docs/technical/` с фактически загруженным состоянием.
8. Пройти DoD, независимое conformance review и human acceptance.

Read-only диагностика и исправление явной опечатки в документации могут не создавать spec, если не меняют контракт.

## Исследование реализации

- Начинать с exact ID/path и narrow `rg`.
- Использовать свежий CommonLib snapshot аудитора; обновлять upstream при истёкшем snapshot или compatibility/dependency/release scope.
- Сравнивать только затронутые symbols, а не повторять полный трёхслойный аудит без impact.
- Проверять `metadata.lua.code`, package ownership и межпакетные ссылки.
- Не читать целиком `items.lua`, metadata или generated каталоги, когда достаточно индексированного slice.
## Lua runtime

Перед изменением ручного Lua определить:

- lifecycle-стадию: file scope, `ClassesBuilt`, `DataLoaded`, `ModsReloaded` или другой точный message;
- registration order обработчиков по `metadata.code`;
- допустимость sleep/yield и game-time/real-time clock;
- declared state (`GameVar`, `MapVar`, `GlobalVar`) и save compatibility;
- возможность возобновления старого thread bytecode из existing save;
- устойчивого владельца mutable state: обычная таблица `CObject` им не является;
- стоимость map enumeration и корректность XY/Z-фильтра;
- настоящий объект-владелец UI mutation вместо `SubContext()`.

File scope используется для definitions и registrations, а не как гарантия готовности ModItem. `ReloadLua` не является clean start. Для точных правил см. [runtime, загрузку и инструменты](systems/runtime-editor-integration.md).

## Mod Editor

Предметы, эффекты, UnitData, Entity и значительная часть metadata создаются редактором. Рекомендуемый процесс:

1. Открыть локальный мод в Mod Editor.
2. Изменить объект в редакторе.
3. Сохранить мод, не закрывая основную игру до завершения записи.
4. Проверить панель сообщений: ignored mod, load/runtime error или assert блокирует принятие round-trip.
5. Проверить изменения в отдельном Lua-файле, `items.lua` и `metadata.lua`.
6. Отделить ожидаемую перегенерацию от случайного шума.
7. Не выполнять параллельно массовый рефакторинг сгенерированных файлов.

### Правило изменения metadata

- `metadata.lua` является generated data и изменяется через Mod Editor.
- Центральная версия релиза читается из committed `jazz/metadata.lua`: `version_major.version_minor-version`; отдельный version-файл не ведётся.
- `version_major`/`version_minor` меняются только по правилам совместимости, read-only `version` вручную не редактируется.
- Dependency проверяет минимальную пару `version_major.version_minor`; автоматически увеличиваемый revision/build зависимостью не ограничивается. После выбора dependency в редакторе повторно проверить записанные version fields.
- Изменения load order, dependencies, loctables, resources и registrations коммитятся вместе с соответствующими файлами-владельцами и документацией.
- После editor save проверяются `metadata.lua`, `items.lua` и отдельные generated definitions; необъяснённый editor noise не коммитится.
- Metadata-only изменение допустимо только как намеренное изменение ModDef или core release marker для выпуска изменений sibling-пакетов.
- Versions/revisions четырёх пакетов не синхронизируются искусственно; они фиксируются в центральном release manifest.
- Номер версии не дублируется в `title`/`description`, потому что JA3 отображает его из metadata.

Полный контракт сохранения описан в [синхронизации generated data](generated-data-sync.md), правила номера версии — в [релизах и версионировании](systems/release-versioning.md).

### Согласование реализации и документации

- Код, generated data, technical и wiki входят в один change set и проверяются по одному фактическому поведению.
- Реализацию нельзя считать готовой или коммитить как завершённую с заведомо устаревшей документацией.
- Документацию нельзя представлять как описание текущей версии, если соответствующее поведение ещё не реализовано или не загружается.
- Межрепозиторное изменение может состоять из нескольких коммитов, но они перечисляются как единая связанная поставка и не должны оставлять код либо документацию отстающими.
- Перед коммитом сопоставить diff реализации и документации, затем запустить профильные read-only проверки.

Для нового предмета проверить class ID, родительский класс, entity, icon, localization ID, caliber, компоненты, рецепты и loot.

Для нового юнита проверить UnitData, appearance, affiliation, AI archetype, role, equipment/loot, voice/portrait и ссылки из squads.

## Map Editor

- Новый или заменяемый сектор оформляется через `SatelliteSector`.
- Изменение существующей карты другого пакета оформляется map patch и должно иметь требуемую зависимость от владельца карты.
- `mapdata.lua`, `objects.lua`, grids и marker debug files не редактировать вручную.
- После изменения карты проверить входы, deployment, conflict markers, setpieces, квестовые маркеры и переходы на стратегическую карту.

## Entity и asset pipeline

В `jazz_assets` Entity Lua должен соответствовать `.ent` и связанным ресурсам. Во время аудита найдены абсолютные ссылки на FBX с нескольких рабочих машин. До очистки pipeline:

- не считать репозиторий самодостаточным для полной пересборки;
- не заменять существующие пути фиктивными;
- новые исходники хранить в согласованном проектном каталоге;
- документировать инструменты и версии экспортёров;
- проверять entity в Mod Editor и в сцене с оружейными компонентами;
- учитывать инкрементальный export: устаревшие части не удаляются автоматически;
- после re-export/re-import очищать согласованный export state и перезапускать игру, чтобы исключить cached Entity.

## Локализация

Metadata должен ссылаться на реально существующий CSV. Сейчас поддерживается русский язык. При добавлении текста:

- использовать стабильные localization ID;
- не копировать ID между пакетами без проверки конфликтов;
- проверять кодировку UTF-8;
- проверять placeholders и теги форматирования;
- запускать проверку конфликтов CommonLib;
- не объявлять английскую таблицу до появления полного файла.

## Детерминизм

Игровая симуляция JA3 зависит от синхронизируемого состояния. Для случайного результата использовать движковые детерминированные функции и подходящий seed/context. Не применять `math.random` / `AsyncRand` / `GetPreciseTicks` в боевой, AI или стратегической логике, если результат влияет на состояние игры или на NetUpdateHash (например id модификаторов). Мутации `gv_Squads` / inventory / combat не откладывать через `CreateRealTimeThread` без `NetSyncEvent`. Обходы hash-таблиц с RNG — через `sorted_pairs` / `ipairs`.

Ванильные/CLib остатки, которые JAZZ перекрывает точечно: `Code/VanillaDesyncFixes.lua` (`LocalHotDiamonds_SetupEnding`, `UnitStatBoost:__exec`, `GetWeightedRandom`, `Firearm:CalcShotVectors`, `TacticalMap:FindOptimalLocationInAssignedArea`, `Firearm:CalcBuckshotScatter`, `AIUpdateBiases`, `SectorOperationFillItemsToCraft`). Armor decay order — в `System_ArmorRating.lua`. FX-only AsyncRand (stains/VR/UI) не трогаем; buckshot cosmetic — AsyncRand намеренно.

## Git

Заголовок и пояснение каждого нового коммита во всех четырёх репозиториях писать на русском языке. Технические идентификаторы, имена файлов, версии и теги сохранять в исходном виде. Создавать commit только по отдельному разрешению пользователя.

## Рефакторинг

Рефакторинг выполнять небольшими этапами: сначала тесты и фиксация поведения, затем один класс дублей, отдельно изменение структуры, отдельно перегенерация данных и только потом баланс. Порядок `metadata.lua`, registration order сообщений, lifecycle-stage, thread clock/yield points, declared variable type, имена глобальных функций и сообщения являются частью поведения и не должны меняться как косметика. Existing save может возобновить старый thread bytecode, поэтому clean start не является достаточной проверкой.

## Project skills

Для любой разработки в четырёх пакетах использовать:

- .agents/skills/specify-jazz-change/SKILL.md — change spec, DoR, DoD и evidence;
- .agents/skills/work-on-jazz-mod/SKILL.md — маршрутизация ownership, source layers и профильных skills;
- `.agents/skills/sync-jazz-generated-data/SKILL.md` — синхронизация `items.lua`, `metadata.lua` и generated companion;
- `.agents/skills/document-jazz-systems/SKILL.md` — обязательное обновление документации в той же задаче;
- `.agents/skills/release-jazz-suite/SKILL.md` — версия из metadata, release manifest, packaging и GitHub Releases.

Read-only проверки:

```powershell
.agents/skills/work-on-jazz-mod/scripts/audit-project.ps1
.agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1
.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1
```

Definition of Done определяется утверждённой spec: все `AC-*` имеют требуемое evidence, technical current-state docs актуальны, профильные checks пройдены, diff остаётся в declared write set и выполнено независимое conformance review.
