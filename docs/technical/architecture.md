# Архитектура

## Пакеты

| Пакет | ID | Версия metadata | Основное содержимое |
| --- | --- | --- | --- |
| `jazz` | `e6L4ECj` | 0.11 / build 5938 | Боевые системы, предметы, эффекты, UI и стратегическая логика |
| `jazz_assets` | `pDGDhr` | 0.1 / build 648 | EntityData, модели, текстуры, материалы и анимационные ресурсы |
| `jazz-maps` | `FhNNYd` | 1.6 / build 5102 | Сектора, map patches, квесты, диалоги, banters и setpieces |
| `jazz-units` | `Dv3mFVN` | 0.9 / build 2246 | UnitData, AI-архетипы, loot, enemy squads и имена |

Фактический каталог ассетов называется `jazz_assets` с подчёркиванием.

## Ответственность пакетов

### `jazz`

Основной пакет содержит около 800 загружаемых Lua-объектов. Главные области:

- оружие, боеприпасы, компоненты и рецепты;
- точность, отдача, прицеливание и исполнение атак;
- броня, повреждения, износ и ранения;
- слоты инвентаря и интерфейс;
- AI, awareness, guardposts и стратегические отряды;
- погода, видимость, свет и дым;
- эффекты, способности и специализации.

### `jazz_assets`

Пакет содержит сотни сущностей и несколько тысяч DDS-ресурсов. Он не должен содержать игровую балансную логику. Его публичный контракт — стабильные имена entity и пути `Mod/pDGDhr/...`, на которые ссылаются остальные пакеты.

### `jazz-maps`

Пакет содержит примерно 317 каталогов карт, а также сектора, квесты, разговоры, banters, setpieces и map patches. Карты и grids считаются генерируемым содержимым Map Editor.

### `jazz-units`

Пакет содержит 179 UnitData и связанные наборы loot, squads, appearances и AI archetypes. Ручной код отвечает за генерацию имён, ключевые слова AI, опыт и рост характеристик.

## Слои загрузки

```text
Jagged Alliance 3
        ↓
JA3_CommonLib и другие зависимости
        ↓
jazz_assets / jazz-units / jazz-maps
        ↓
jazz
        ↓
другие моды, загруженные после JAZZ
```

Схема отражает логическую поддержку, но текущие metadata не полностью закрепляют все стрелки. Основной пакет объявляет обязательным только `jazz_assets`; CommonLib и units указаны как необязательные, а maps не объявлен. При этом прямые ссылки между пакетами существуют.

Внутри каждого пакета решающим является порядок массива `code` в `metadata.lua`. Порядок файлов на диске значения не имеет.

## Три происхождения поведения

1. **Vanilla JA3** предоставляет исходные классы, функции, presets, UI и данные.
2. **CommonLib** загружается как постоянно обновляемая зависимость, исправляет vanilla-функции, добавляет инфраструктуру и может переопределять исходные имена. JAZZ целится только в последнюю официальную версию; перед анализом проверяются upstream `main` и metadata.
3. **JAZZ** добавляет собственные системы и намеренно заменяет часть vanilla/CLib-реализаций.

Для глобальных функций и методов действует правило «последнее объявление выигрывает». Для `OnMsg`, presets, реакций и отложенных изменений простой модели недостаточно: обработчики могут накапливаться, а данные — мутировать последовательно. Конкретные совпадения перечислены в [матрице переопределений](override-matrix.md).

## Данные и генерация

| Объект | Источник истины | Производные файлы |
| --- | --- | --- |
| ModItem | Mod Editor | `items.lua`, `metadata.lua`, отдельный Lua-файл |
| InventoryItem | Mod Editor | `InventoryItem/*.lua`, `items.lua`, metadata |
| CharacterEffect | Mod Editor | `CharacterEffect/*.lua`, `items.lua`, metadata |
| UnitData | Mod Editor | `UnitData/*.lua`, `items.lua`, metadata |
| Entity | Mod Editor / asset pipeline | Entity Lua, `.ent`, `.hgm`, `.mtl`, `.dds` |
| Карта | Map Editor | `mapdata.lua`, `objects.lua`, grids, patches |
| Локализация | LocTable/CSV workflow | CSV и ссылки `ModItemLocTable` |

Ручное изменение одной производной копии создаёт рассинхронизацию и может быть уничтожено следующим сохранением редактора.

## Межпакетные ссылки

- `jazz` напрямую использует изображения из `jazz-maps`, например портрет Ивана.
- `jazz-maps` напрямую использует изображения и портреты `jazz-units`.
- оружие основного пакета использует entity из `jazz_assets`.
- все пакеты должны сохранять стабильные mod ID, class ID, preset ID и resource path.

При добавлении новой межпакетной ссылки необходимо обновить metadata владельца ссылки и документацию зависимости.
## Владельцы систем

Подробная архитектура разложена по [каталогу систем](systems/README.md). Краткая карта ответственности:

| Контур | Runtime-владелец | Основные поставщики данных |
|---|---|---|
| CTH, действия, оружие, броня, inventory, UI | `jazz` | `jazz`, `jazz_assets`, `jazz-units` |
| Tactical AI и awareness | `jazz` | `jazz-units`, maps geometry/data |
| Satellite, guardposts, regions, POI, operations | `jazz` | `jazz-maps`, `jazz-units` |
| Campaign, sectors, quests, dialogue | `jazz-maps` | core IDs, units, assets |
| UnitData, squads, archetypes, progression | `jazz-units` | core items/effects/actions, assets |
| Entities, meshes, materials, textures | `jazz_assets` | потребляются остальными пакетами |
| Sound/FX и voices | `jazz` / `jazz-units` | core actions/items, assets entities |

Явный статус каждого ручного Lua-файла находится в [file coverage](systems/file-coverage.md). Пакет-владелец данных и пакет-владелец runtime могут различаться; изменение контракта требует проверить обе стороны.
