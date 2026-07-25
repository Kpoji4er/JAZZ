# Структура проекта и источники истины

## Комплект из четырёх пакетов

| Каталог репозитория | Идентичность мода | Основная ответственность |
|---|---|---|
| `jazz` | JAZZ core | Runtime Lua, предметы, оружие, броня, UI, AI, стратегия, audio/FX presets и общая конфигурация |
| `jazz_assets` или `jazz-assets` | JAZZ assets | Entities, meshes, materials, textures и entity metadata |
| `jazz-maps` | JAZZ maps | Campaign sectors, карты, квесты, conversations, banters, loot, guardpost objectives и setpieces |
| `jazz-units` | JAZZ units | UnitData, appearances, squads, AI archetypes, loot definitions, voices и progression hooks |

Определять фактическое имя соседнего каталога, а не закреплять путь конкретной машины. Пакеты являются отдельными Git-репозиториями, но проверяются как один runtime-продукт.

`jazz-maps/Maps/` — тяжёлый editor-generated каталог. Не включать его в общий inventory, recursive search или обзорный аудит. Читать только по прямому указанию на карты и начинать с конкретного сектора, карты, patch или файла.

## Направление runtime-зависимостей

`Jagged Alliance 3 -> CommonLib -> JAZZ core -> JAZZ assets/maps/units и их перекрёстные ссылки`

Истиной являются фактический порядок Mod Manager и metadata каждого пакета. Пакет может использовать ID соседнего пакета без прямого source import.

Типичные межпакетные связи:

- core items/actions ссылаются на IDs юнитов, секторов, entities, звука и карт;
- units используют core effects, actions, inventory classes, weapons, armor и AI keywords;
- maps создаёт units/squads и использует core strategy/guardpost systems;
- assets предоставляет entity names для items, appearances, maps и FX.

## Приоритет источников

- Текущий runtime игры: `<JA3_ROOT>/ModTools/Src`.
- История официальных исходников: <https://github.com/THQNordic/JaggedAlliance3Modding>.
- Зависимость CommonLib: последняя ветка `main` из <https://gitlab.com/injto4ka/ja3_commonlib>. JAZZ не ориентирован на закреплённые старые версии; перед каждой задачей определять текущие commit и metadata.
- Истина проекта: текущие working tree всех четырёх репозиториев.

Не сохранять абсолютный локальный путь автора в документации или agent-инструкциях. Использовать `<JA3_ROOT>`, repository-relative paths, переменные среды или инструкции по обнаружению.

## Generated и ручное содержимое

К generated-содержимому относятся определения ModItem, `__parents`, файлы `PlaceObj(...)`, entity descriptions, sectors, quests, conversations, appearances, UnitData, loot tables и metadata load lists. Сохранять формат генератора и стабильные IDs.

Ручная runtime-логика обычно находится в `Code/`. Наличие Lua-файла на диске не доказывает его загрузку. Проверять metadata или регистрацию Mod Editor и помечать файл как loaded, dormant/unlisted, generated или inert.