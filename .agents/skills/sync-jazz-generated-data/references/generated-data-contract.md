# Контракт generated data Jagged Alliance 3

## Официальные источники

Текущее runtime/editor-поведение проверять в установленной версии игры:

- `<JA3_ROOT>/ModTools/Src/CommonLua/Classes/Mod.lua`
- `<JA3_ROOT>/ModTools/Src/CommonLua/Classes/ModItem.lua`
- `<JA3_ROOT>/ModTools/Src/CommonLua/Classes/GedModEditor.lua`

Историю официального source drop смотреть в <https://github.com/THQNordic/JaggedAlliance3Modding>. Установленный `<JA3_ROOT>/ModTools/Src` имеет приоритет для текущего runtime; GitHub удобен для истории и diff.

## Что делает сохранение

`ModDef:SaveWholeMod()` вызывает `SaveDef()`, затем `SaveItems()`, затем сохранение options.

`SaveDef()`:

1. обновляет entity, localization и code-списки;
2. повышает счётчики версии/сохранения;
3. сериализует `metadata.lua`.

`SaveItems()`:

1. вызывает `PreSave()` для ModItem;
2. сериализует весь граф элементов в `items.lua`;
3. вызывает `PostSave()` для ModItem;
4. пишет `items.lua`.

`ModItemPreset:PostSave()` генерирует и перезаписывает companion, возвращаемый `GetCodeFileName()`. Для обычного preset это каталог класса preset и безопасное имя ID. `BaseModItemEntity:PostSave()` пишет `Entities/<entity_name>.lua`.

Редактор проверяет внешнее изменение `items.lua` перед сохранением и может показать предупреждение. Отдельной защиты внешней ручной правки каждого companion-файла нет: `PostSave()` способен молча заменить её данными из памяти редактора.

## Роли файлов

| Слой | Роль | Источник изменения | Основной риск |
| --- | --- | --- | --- |
| Состояние редактора / `items.lua` | Полный сериализованный граф ModItem | Mod Editor и `SaveItems()` | Устаревший открытый редактор перезапишет внешнюю правку |
| `metadata.lua` | Dependency metadata, `code`, `entities`, `loctables`, ресурсы, ревизии и производные индексы | `SaveDef()` | Пропущенный или переставленный путь меняет загрузку |
| Preset companions | Runtime-определения `InventoryItem`, `CharacterEffect`, `UnitData` и других preset | `ModItemPreset:PostSave()` | Ручная правка исчезает при следующем сохранении |
| `Entities/*.lua` | Runtime `EntityData` | `BaseModItemEntity:PostSave()` | Имя entity расходится с items/metadata/путём |
| `Code/*.lua` | Ручная runtime-логика | Разработчик | Файл отсутствует в `metadata.code` или загружается не в том порядке |

`metadata.lua` не является полной копией `items.lua`. Сверять следует контракт, а не побайтовое равенство:

- каждый активный runtime Lua-путь существует;
- generated companion связан с ModItem по `class + Id`;
- entity совпадает по имени в ModItem, `metadata.entities`, `metadata.code` и `EntityData`;
- ручной `Code/*.lua` зарегистрирован намеренно и стоит в правильном месте;
- зависимости и load order соответствуют текущему проектному контракту.

## Границы транзакции

Минимальная транзакция изменения preset:

```text
ModItem в памяти редактора
        ↓ SaveItems
items.lua
        ↓ PostSave
<PresetClass>/<Id>.lua
        ↘ SaveDef / UpdateCode
          metadata.lua: code
```

Минимальная транзакция Entity:

```text
ModItemEntity: entity_name
   ├─ items.lua
   ├─ metadata.lua: entities
   ├─ metadata.lua: code
   └─ Entities/<entity_name>.lua: EntityData["<entity_name>"]
```

Снимок времени записи не является доказательством корректности, но полезен как индикатор незавершённой транзакции. При штатном полном сохранении `metadata.lua` обычно записывается раньше generated companions и `items.lua`. Companion новее `items.lua` или metadata новее items без объяснимого полного save требует проверки.

## Сценарии восстановления

### Исправлен только companion

1. Не открывать и не сохранять устаревший Mod Editor.
2. Найти соответствующий `class + Id` в `items.lua`.
3. Перенести смысловое изменение в редактор или эквивалентную запись ModItem.
4. Выполнить полный save/reload round-trip.
5. Убедиться, что regenerated companion сохранил изменение.

### `items.lua` изменён при открытом редакторе

1. Не подтверждать перезапись автоматически.
2. Сохранить внешний diff отдельно.
3. Закрыть редактор без сохранения либо перезагрузить мод с диска.
4. Повторить изменение на свежем состоянии.

### Companion отсутствует в `metadata.code`

1. Определить, активен ли ModItem или файл намеренно dormant.
2. Для активного generated ModItem выполнить полный save через редактор.
3. Проверить место файла в `metadata.code`; не вставлять его алфавитно без понимания порядка.

### Остался файл со старым ID

1. Проверить Git-историю и ссылки во всех четырёх пакетах.
2. Сравнить старый и новый `class + Id`.
3. Исключить alias, совместимость с save, намеренный override и незавершённую работу.
4. Только после этого удалить orphan в отдельном осознанном изменении.

### Конфликт generated-файлов

Не выбирать автоматически сторону `items.lua` или companion. Выделить смысловые различия, определить более свежее авторское состояние, восстановить его в ModItem и дать редактору снова сгенерировать все слои. После этого проверить diff и runtime.

## Что проверяет аудитор

`check-generated-sync.ps1` выполняет только чтение и проверяет:

- наличие `metadata.lua` и `items.lua` у четырёх пакетов;
- существование и уникальность путей `metadata.code`;
- связь generated companion с ModItem по class/ID;
- наличие generated companion в `metadata.code`;
- согласованность Entity между items, metadata и `EntityData`;
- признаки orphan и незавершённой транзакции;
- подозрительный порядок времени записи.

Regex-аудит не заменяет загрузку Lua движком и полный editor round-trip. Вложенные таблицы, вычисляемые значения, карты и бинарные ресурсы требуют профильной проверки.

## Пакеты JAZZ

Аудит всегда охватывает комплект:

| Пакет | Каталог | Основные generated data |
| --- | --- | --- |
| `jazz` | `..\jazz` | Items, effects, UI/runtime presets |
| `jazz_assets` | `..\jazz_assets` | Entities и asset metadata |
| `jazz-maps` | `..\jazz-maps` | Map/sector/quest presets |
| `jazz-units` | `..\jazz-units` | UnitData, AI и squad presets |

Соседнее имя каталога assets исторически использует подчёркивание. Не переименовывать его ради единообразия.