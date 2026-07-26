---
name: sync-jazz-generated-data
description: Безопасная синхронизация generated data модов JAZZ между metadata.lua, items.lua и companion Lua-файлами. Использовать при создании, изменении, переименовании, удалении или переносе ModItem, preset, InventoryItem, CharacterEffect, UnitData, Entity, XTemplate, ActionFX, кода, dependency metadata и любых editor-generated данных; перед сохранением Mod Editor, после ручного diff и перед релизом. Предотвращает перезапись изменений устаревшим слоем и проверяет все четыре пакета как единый комплект.
---

# Синхронизация generated data JAZZ

## Контракт

Считать `metadata.lua`, `items.lua` и generated companion Lua-файлы одной транзакцией. Не принимать изменение одного слоя за завершённую правку.

- `items.lua` хранит сериализованное состояние ModItem, загружаемое редактором.
- `metadata.lua` хранит производные списки загрузки, сущностей, ресурсов, локализации и зависимостей.
- Companion-файлы (`InventoryItem/*.lua`, `CharacterEffect/*.lua`, `UnitData/*.lua`, `Entities/*.lua` и аналоги) генерируются из ModItem и используются runtime.
- Ручные модули `Code/*.lua` не являются companion-файлами, но обязаны присутствовать в массиве `code` в правильном порядке.

Официальный `SaveWholeMod()` сначала обновляет и пишет `metadata.lua`, затем сериализует `items.lua`; во время `SaveItems()` каждый ModItem выполняет `PostSave()` и может перезаписать свой companion-файл. Поэтому ручная правка только companion-файла недолговечна и может исчезнуть при следующем editor save. Mod Editor является companion UI, но сохранение выполняет основная игра: не закрывать её до завершения save и всегда проверять панель сообщений после load/save/reload.

По умолчанию аудитор не обходит тяжёлый `jazz-maps/Maps/`. Использовать `-IncludeMapsContent` только по прямому указанию на эту папку, конкретную карту, сектор или map patch.

Перед работой полностью прочитать [generated-data-contract.md](references/generated-data-contract.md).

## Начало задачи

1. Прочитать применимые `AGENTS.md` и skill `$work-on-jazz-mod`.
2. Проверить последнюю upstream-версию CommonLib по правилам проекта.
3. Зафиксировать `git status`, существующий diff и владельца данных во всех четырёх пакетах.
4. Запустить read-only аудит:

   ```powershell
   .agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1
   ```

   Для прямо указанной картографической задачи:

   ```powershell
   .agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1 -Package jazz-maps -IncludeMapsContent
   ```

5. Классифицировать каждый затронутый файл:
   - ручной runtime-модуль `Code/*.lua`;
   - `items.lua`;
   - `metadata.lua`;
   - generated preset companion;
   - generated entity companion;
   - карта, бинарный ресурс или другой editor-owned файл.
6. Для конкретного ModItem определить стабильный ключ `class + Id`, ожидаемый companion-путь и его записи в `items.lua` и `metadata.lua`.

## Предпочтительный editor workflow

1. Закрыть или перезагрузить редактор, если файлы менялись снаружи после его открытия.
2. Изменить объект в Mod Editor, Preset Editor, Map Editor или Entity Editor, владеющем данными.
3. Выполнить одно логическое сохранение всего мода. Не чередовать ручные правки generated-файлов с сохранением устаревшего состояния редактора и не закрывать основную игру до завершения записи.
4. Проверить панель сообщений: ignored mod, load/runtime error или assert блокирует принятие round-trip.
5. Просмотреть единый diff `metadata.lua`, `items.lua` и всех companion-файлов изменённого объекта.
6. Отделить ожидаемую сериализацию от необъяснённого editor noise. Не форматировать generated-файлы массово.
7. Для dependency metadata повторно сверить `version_major`/`version_minor` с текущим upstream: dependency ограничивает минимальную major/minor, а revision (`version`/build) в проверке не участвует.
8. Запустить строгий аудит и профильные проверки:

   ```powershell
   .agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1 -Strict
   ```

9. Перезагрузить мод из диска, повторно проверить панель сообщений и выполнить runtime/editor smoke test. Только после успешного round-trip считать изменение устойчивым.

## Контролируемая ручная транзакция

Использовать только когда editor workflow недоступен или задача явно разрешает ручную правку generated data.

1. Убедиться, что игра и редактор закрыты.
2. Найти полную запись ModItem в `items.lua`, companion-файл и связанные записи `metadata.lua`.
3. Внести одно и то же смысловое изменение во все представления:
   - свойства объекта — в `items.lua` и companion;
   - появление, удаление или переименование файла — также в `metadata.lua`;
   - entity name — также в `metadata.entities` и `Entities/<name>.lua`;
   - порядок загрузки ручного или generated Lua — в `metadata.code`.
4. Не менять производные хэши и ревизии «по догадке». Пусть их пересчитает официальный редактор.
5. Запустить аудит, затем открыть редактор с чистым состоянием с диска, выполнить save/reload round-trip и повторить аудит.
6. Если round-trip невозможен, явно пометить результат непроверенным и не готовым к релизу.

## Добавление, переименование и удаление

### Добавление

- Создать ModItem через соответствующий редактор.
- Убедиться, что запись появилась в `items.lua`, companion существует и включён в `metadata.code`.
- Для Entity также проверить `metadata.entities` и совпадение ключа `EntityData`.
- После re-export/re-import учесть инкрементальный export, очистить согласованный export state и проверить Entity в новом процессе игры.

### Переименование

- До изменения найти ссылки на старый ID во всех четырёх пакетах.
- После сохранения проверить новый путь, новый ID и удаление старого companion.
- Старый файл не удалять автоматически: сначала исключить намеренный alias, override, dormant-файл и пользовательскую незавершённую работу.

### Удаление

- Подтвердить исчезновение ModItem из `items.lua`, companion из файловой системы и записей из `metadata`.
- Проверить ссылки из кода, maps, units, presets, localization, entities и других пакетов.
- Не удалять orphan только потому, что аудит его обнаружил; сначала изучить Git-историю и runtime-регистрацию.

## Запреты

- Не редактировать только generated companion и не ожидать сохранения правки.
- Не сохранять Mod Editor поверх внешне изменённого `items.lua` без reload и проверки diff.
- Не считать алфавитную сортировку `metadata.code` безопасной: порядок является частью поведения.
- Не добавлять каждый Lua-файл в `metadata.code`: dormant и source-only файлы могут быть намеренно неактивны.
- Не удалять, не переименовывать и не перегенерировать файлы автоматически в read-only аудите.
- Не раскрывать абсолютные локальные пути в tracked-файлах; использовать `<JA3_ROOT>`.
- Не смешивать смысловое изменение с массовой перегенерацией данных.

## Проверка и документация

Активное рассогласование `items.lua`/`metadata.lua`/companion всегда является блокирующей ошибкой и даёт ненулевой exit code. Файл вне активного graph классифицируется warning до решения intentional dormant/orphan; `-Strict` также блокирует warnings. Отсутствие core-файлов или невозможность разбора завершается кодом `1`. Обычный режим выводит компактную сводку warnings; полный список запрашивается через `-DetailedWarnings` и автоматически показывается в `-Strict`.

Для любого изменения generated data использовать `$document-jazz-systems` в той же задаче:

- обновить технический источник истины;
- обновить file coverage при добавлении, удалении, переносе или смене активности файла;
- обновить wiki, если механика заметна игроку;
- указать, какие из трёх представлений изменились и каким round-trip они проверены.

## Ресурсы

- [generated-data-contract.md](references/generated-data-contract.md) — официальный save pipeline, роли слоёв и восстановление после рассинхронизации.
- `scripts/check-generated-sync.ps1` — read-only аудит четырёх пакетов; тяжёлый `jazz-maps/Maps/` исключён, пока явно не передан `-IncludeMapsContent`.