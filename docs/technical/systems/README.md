# Системы JAZZ

Этот каталог описывает JAZZ как единый продукт из четырёх пакетов. Срез сделан 25 июля 2026 года по текущим working tree; количества объектов являются снимком, а не вечным контрактом.

## Карта систем

| Система | Что описано | Пользовательский слой |
|---|---|---|
| [Бой, CTH и боевые действия](combat-cth-actions.md) | Формула попадания, дальность, прицеливание, очереди, recoil, 53 действия и combat UI | Не ведётся |
| [Оружие, боеприпасы и компоненты](weapons-ammo-components.md) | Классы оружия, ресурс, износ, заклинивание, 27 калибров, 64 component effects и рецепты | Не ведётся |
| [Вырезанный контент (оружие/патроны)](../weapons/cut-content.md) | `Убираем` / `ОТКЛЮЧЕНО` / `TEST.png`, 3 оружия + 38 ammo, замены `JAZZ_AMMO_*` | Не ведётся |
| [Взрывчатка, ловушки и тяжёлое оружие](explosives-traps-heavy-weapons.md) | Гранаты, мины, газ, гранатомёты, миномёты, подавление и AI применения | Не ведётся |
| [Броня, повреждения, ранения и воля](armor-damage-wounds-will.md) | Покрытие, рейтинг, пластины, состояния тела, лечение, Grit и Will Points | Не ведётся |
| [Инвентарь, предметы, loot и crafting](inventory-items-loot-crafting.md) | Слоты, UI, контейнеры, squad bag, таблицы добычи и рецепты | Не ведётся |
| [Тактический AI и awareness](ai-awareness.md) | Выбор действий, политики позиций, роли, укрытия, фланги, suspicion и alert | Не ведётся |
| [Видимость, погода и внешний вид](visibility-weather-appearance.md) | Свет, дым, погода, маски, визуальные состояния оружия и персонажей | Не ведётся |
| [Юниты, прогрессия и специализации](units-progression-specializations.md) | UnitData, squads, archetypes, опыт до 21 уровня, stat gain и AIM-фильтры | Не ведётся |
| [Легион: схема юнитов и тиры снаряжения](legion-units-equipment-tiers.md) | 37 UnitData, шесть боевых семейств, ветви эскалации и campaign equipment tier 11–33 | Не ведётся |
| [Стратегия, отряды и сектора](strategy-squads-sectors.md) | SatelliteSquad, guardposts, POI, регионы, экономика, операции и World Flip | Не ведётся |
| [Иконки ролей отрядов (Global AI)](squad-role-icons.md) | Галерея PNG по ролям и фракциям Legion/Army/Adonis/Rebels/Smugglers | Не ведётся |
| [Автотранспорт (сателлит + тактика)](satellite-vehicles.md) | Парковка / сесть / выйти, ускорение по дорогам; тактический stub dormant | Не ведётся |
| [Боевой автомобиль — указатель](combat-vehicle-design.md) | Канон спеки в **JAZZ Maps** `docs/combat-vehicle-design.md`; код ещё не в runtime | Не ведётся |
| [Карты, квесты и диалоги](maps-quests-dialogue.md) | 317 каталогов карт, 245 секторов, 110 квестов, разговоры, banters и setpiece | Не ведётся |
| [Каталог квестов, локаций и врагов](maps-quests-content-catalog.md) | Снимок quest/sector/squad IDs из jazz-maps; детально остров Эрни | Не ведётся |
| [Атлас / трансфер секторов](../maps/sector-atlas.md) | Сетка A–P×32, transfer vanilla→maps, сверка sheet↔runtime + CSV | Не ведётся |
| [Интерфейс, звук и FX](ui-audio-fx.md) | Crosshair, combat badge, inventory UI, Will bar, sound presets и оружейные FX | Не ведётся |
| [Entities и ресурсы](assets-entities.md) | 490 зарегистрированных Entity ModItems, meshes, materials, textures и контракты имён | Не ведётся |
| [Runtime, загрузка и инструменты](runtime-editor-integration.md) | metadata, Mod Editor, generated data, hooks, placeholders, dormant-код и диагностика | Не ведётся |
| [Debug и читы](../debug.md) | Консоль, Ctrl-T satellite teleport, боевые/стратегические читы, JAZZ diagnostics | Не ведётся |
| [Локализация](localization.md) | Numeric localization ID, приоритет CSV, аудит коллизий и рабочий каталог русского/английского перевода | Технический процесс |
| [Релизы и версионирование](release-versioning.md) | Версия из committed metadata, manifest четырёх repos, GitHub Releases и safeguards | Технический процесс |
| [Сводки изменений в Discord](discord-player-updates.md) | Push range, OpenAI Structured Outputs, фильтрация, fallback и Discord webhook | Технический процесс |
| [Покрытие файлов](file-coverage.md) | Явный владелец документации и load-state каждого `Code/*.lua` | Технический реестр |

## Как читать происхождение поведения

Каждая страница использует три слоя:

1. **Vanilla JA3** — классы, функции, presets и данные установленного билда из `<JA3_ROOT>\ModTools\Src`.
2. **CommonLib** — dependency `JA3_CommonLib`, которая может заменить vanilla-код, добавить hooks или изменить данные до загрузки JAZZ.
3. **JAZZ** — итоговые расширения и замены в `jazz`, `jazz_assets`, `jazz-maps` и `jazz-units`.

Официальный репозиторий [THQNordic/JaggedAlliance3Modding](https://github.com/THQNordic/JaggedAlliance3Modding) удобен для истории, но его source drop 1.5 старее установленного ModTools. Для текущего runtime приоритет имеет установленный исходник. JAZZ всегда ориентирован на последнюю upstream-версию [ja3_commonlib](https://gitlab.com/injto4ka/ja3_commonlib); старые версии не поддерживаются. На дату среза последним был CommonLib 1.11 build 1056, commit `1adf9f232680d3b011248d180fd0ad1e609a8e2c`; это снимок аудита, не pin.

## Статусы реализации

- **loaded runtime** — путь присутствует в массиве `code` соответствующего `metadata.lua`;
- **generated and loaded** — объект сериализован Mod Editor/Map Editor и зарегистрирован в `items.lua`/metadata;
- **dormant/unlisted** — файл существует, но metadata его не загружает;
- **empty placeholder** — зарегистрированный или незарегистрированный файл нулевой длины;
- **loaded but inert** — файл загружается, но активная логика отсутствует или закомментирована;
- **editor/development only** — расширяет редактор или диагностику, а не игровое правило.

## Контракт сопровождения

Любое изменение кода, generated data, публичного ID, зависимости или порядка загрузки должно в той же задаче обновить:

- страницу затронутой системы;
- [покрытие файлов](file-coverage.md), если меняется файл или load-state;
- [матрицу переопределений](../override-matrix.md), если появляется пересечение с vanilla/CommonLib;
- [совместимость](../compatibility.md) и [тестирование](../testing.md), когда меняется соответствующий контракт.

Проверка автоматизирована skill `$document-jazz-systems` и скриптом `.agents/skills/document-jazz-systems/scripts/check-system-docs.ps1`.
