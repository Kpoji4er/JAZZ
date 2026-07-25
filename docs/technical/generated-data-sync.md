# Синхронизация metadata, items и generated Lua

## Назначение

Один editor-owned объект Jagged Alliance 3 представлен сразу в нескольких местах:

- сериализованный ModItem в `items.lua`;
- производные индексы и порядок загрузки в `metadata.lua`;
- runtime companion: `InventoryItem/*.lua`, `CharacterEffect/*.lua`, `UnitData/*.lua`, `Entities/*.lua` или аналогичный файл;
- состояние открытого Mod Editor.

Эти представления образуют одну транзакцию. Правка не считается устойчивой, пока редактор не загрузил её с диска, не сохранил повторно и не оставил смысловой результат неизменным.

## Происхождение поведения

| Слой | Результат аудита | Следствие |
| --- | --- | --- |
| Vanilla JA3 | `SaveWholeMod`, `SaveDef`, `SaveItems` и `PostSave` реализованы в `<JA3_ROOT>/ModTools/Src/CommonLua/Classes/Mod.lua` и `ModItem.lua` | ModTools задаёт порядок записи и регенерации |
| Последняя CommonLib | В проверенном snapshot 1.11, build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c` целевые методы не переопределены; Mod Manager вызывает vanilla `SaveWholeMod()` | Перед каждой задачей всё равно повторно проверять текущий `main`; snapshot не является pin |
| JAZZ | Четыре пакета не заменяют save pipeline и поставляют ModItem, companions, Entities и ручной `Code/` | Рассинхронизацию исправлять в данных и editor workflow |

Историю source drop смотреть в <https://github.com/THQNordic/JaggedAlliance3Modding>, текущий runtime — в установленном `<JA3_ROOT>/ModTools/Src`.

## Официальный save pipeline

`ModDef:SaveWholeMod()` выполняет:

1. `SaveDef()` обновляет `entities`, `loctables`, `code` и пишет `metadata.lua`.
2. `SaveItems()` вызывает `PreSave()` и сериализует граф ModItem.
3. `PostSave()` каждого preset/Entity перезаписывает его companion.
4. Завершается запись `items.lua` и save callbacks.

```text
Mod Editor / ModItem
   ├─ SaveDef ───────────→ metadata.lua
   └─ SaveItems
        ├─ PostSave ─────→ <PresetClass>/<Id>.lua или Entities/<name>.lua
        └────────────────→ items.lua
```

Редактор умеет предупредить о внешнем изменении `items.lua`. Отдельной защиты ручной правки companion нет: устаревшее состояние открытого редактора может молча перегенерировать файл.

## Контракт представлений

### Preset

- `items.lua`: запись `ModItem...` с ключом `class + Id`.
- Companion: тот же ID в `UndefineClass`/`DefineClass` и тот же ModItem class в `__generated_by_class`.
- `metadata.code`: существующий companion-путь в намеренной позиции load order.

### Entity

Одинаковое имя должно присутствовать в:

- `ModItemEntity.entity_name` в `items.lua`;
- `metadata.entities`;
- `metadata.code` как `Entities/<name>.lua`;
- `EntityData["<name>"]` в companion.

### Ручной код

`Code/*.lua` не является generated companion, даже если содержит определения классов или скопированные generated-маркеры. Ручной файл меняется непосредственно, но его регистрация и порядок остаются частью `metadata.code`.

## Безопасный workflow

1. Проверить dirty state всех четырёх репозиториев.
2. Запустить обычный read-only аудит до изменения.
3. Перезагрузить Mod Editor, если файлы менялись снаружи после его открытия.
4. Изменить объект в редакторе-владельце и выполнить одно полное сохранение.
5. Просмотреть `items.lua`, `metadata.lua` и companions одним diff.
6. Запустить строгий аудит.
7. Выполнить reload/save round-trip без смысловых правок.
8. Провести профильный runtime test с последней CommonLib.

Ручная транзакция допустима только по явному разрешению, при закрытых игре и редакторе. Смысловое изменение переносится в `items.lua` и companion; metadata меняется только при изменении пути, активности, Entity, dependency или порядка. Без editor round-trip результат помечается непроверенным.

## Структурные операции

| Операция | Синхронный набор | Обязательная проверка |
| --- | --- | --- |
| Добавление preset | ModItem, companion, `metadata.code` | Class/ID, родители, ссылки, load order |
| Переименование preset | Новый ID/путь; старый companion исследован | Поиск старого ID во всех пакетах и saves |
| Удаление preset | Items, metadata-регистрация, companion | Code, maps, units, loot, localization |
| Добавление Entity | `entity_name`, `metadata.entities`, `metadata.code`, `EntityData`, assets | Asset pipeline и сцена |
| Dependency metadata | ModDef и межпакетный контракт | Latest CommonLib и строгий dependency-аудит |

File-only объект может быть orphan или намеренно dormant. Его нельзя автоматически удалять или добавлять в metadata без Git-истории и проверки ссылок.

## Read-only аудитор

Project skill: `.agents/skills/sync-jazz-generated-data/SKILL.md`.

```powershell
# Baseline-диагностика
.agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1

# Gate после editor round-trip и перед релизом
.agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1 -Strict

# Один пакет
.agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1 -Package jazz-units

# Только по прямому указанию на карты
.agents/skills/sync-jazz-generated-data/scripts/check-generated-sync.ps1 -Package jazz-maps -IncludeMapsContent
```

Без `-IncludeMapsContent` аудитор не обходит тяжёлый `jazz-maps/Maps/`, но продолжает проверять metadata и остальные generated layers пакета. Флаг включается только для прямо указанной карты, сектора или map patch.

Коды завершения: `0` — core/parser исправны, обычный режим мог напечатать baseline; `1` — отсутствует core-файл или не разобрана структура; `2` — строгий режим нашёл расхождение или предупреждение.

Regex-аудит не исполняет Lua и не сравнивает сложные вложенные значения. Финальная проверка — editor round-trip и runtime test.

## Снимок от 25 июля 2026

| Пакет | `metadata.code` | ModItem | Preset companions | Entity files | Статический результат |
| --- | ---: | ---: | ---: | ---: | --- |
| `jazz` | 802 | 1916 | 620 | 0 | Шесть file-only preset candidates |
| `jazz_assets` | 490 | 604 | 0 | 503 | 13 Entity вне активного графа; 25 Entity новее `items.lua` |
| `jazz-maps` | 8 | 522 | 6 | 0 | Структурных расхождений не найдено |
| `jazz-units` | 190 | 1879 | 182 | 0 | Структурных расхождений не найдено |

Preset-кандидаты `jazz`:

- `CharacterEffect/ThreePointer.lua`;
- `InventoryItem/JAZZ_AMMO_9x19_JHP_copy.lua`;
- `InventoryItem/_MortarShell_Gas.lua`, `_MortarShell_HE.lua`, `_MortarShell_Smoke.lua`;
- `UnitData/Ivan.lua` с runtime ID `Ivan_1`.

Entity-кандидаты `jazz_assets`: `Chevy_S10_SM`, `G36Mag`, `Hamvee`, `M60E3BipodUnfld`, `M60E4BipodUnfld`, `M60_OldBipodFld`, `MP5MagVar2`, `PKMDefHandGrip`, `PKMDefIronSight`, `PKMDefMuzzle`, `PKMDefStock`, `PKMFoldBipod`, `PKMMag`.

Это очередь исследования, а не разрешение на удаление. Группа из 25 более новых P210/P226 Entity требует editor round-trip; timestamp сам по себе не доказывает ошибку.

## Definition of done

- Latest CommonLib повторно проверена.
- Все представления просмотрены одним diff.
- Строгий аудит не показывает новых необъяснённых расхождений.
- Выполнены editor reload/save и runtime test либо явно отмечено их отсутствие.
- Technical-документация обновлена; wiki обновлена только при пользовательском эффекте.