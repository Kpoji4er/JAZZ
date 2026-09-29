---
id: JAZZ-WEAPON-PRESENTATION-001
status: approved
owner: project-owner
systems:
  - weapon-presentation
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - items.lua
  - metadata.lua
  - Code/InventoryUI.lua
  - Code/System_WeaponResourceMaintenance.lua
  - Code/System_WeaponComponent_Set.lua
  - WeaponIcons/Live/*
  - Localization/*
  - Russian.csv
  - English.csv
  - docs/tools/weapon_layer_icons/*
  - docs/tools/README.md
  - docs/design/weapon-layer-icons/live/*
  - docs/technical/systems/ui-audio-fx.md
  - docs/technical/override-matrix.md
  - docs/wiki/weapons-and-ammo.md
  - docs/showcase/ru/weapons-and-ammo.md
  - docs/showcase/en/weapons-and-ammo.md
  - docs/specs/active/JAZZ-WEAPON-PRESENTATION-001.md
exclusive_resources:
  - mod-editor-state
  - items.lua
  - metadata.lua
  - weapon-presentation-hooks
  - localization-runtime-export
approved_by: project-owner
---

# JAZZ-WEAPON-PRESENTATION-001: установка живых иконок и структурных имён

## Проблема

Проверенные снимки и имена существуют только в staged review, игра их не использует.

## Цели

Установить подготовленный набор в рабочий мод и проверить его в живом runtime.

## Non-goals

Отдельный редактор креплений, новые модели, публикация и изменение баланса. Послойная композиция входит в расширение от 29.09.2026. Имена Mosin принадлежат отдельной модельной задаче.

## Требования

- `JAZZ-WEAPON-PRESENTATION-001-REQ-001` — точный снимок по классу, entity и полному эффективному набору компонентов; неизвестное сочетание использует прежнюю иконку.
- `JAZZ-WEAPON-PRESENTATION-001-REQ-002` — подтверждённые структурные имена AK74/AKM/VZ58 доступны на русском и английском; прочие классы и неподтверждённый SVDS сохраняют имя.
- `JAZZ-WEAPON-PRESENTATION-001-REQ-003` — установить файлы с резервными копиями активного мода, сохранить чужие изменения и attachment chips.

## Инварианты и ограничения

Никакого runtime bake, новых ID предметов, изменения инвентаря игрока или RNG. Не использовать ошибочный старый Blender-снимок магазина M4. Metadata/load order и generated item definitions не меняются.

## Acceptance criteria

- `JAZZ-WEAPON-PRESENTATION-001-AC-001` — static: все снятые конфигурации выбирают существующий снимок; неизвестные сочетания и entity возвращают fallback.
- `JAZZ-WEAPON-PRESENTATION-001-AC-002` — static/runtime: смена и возврат приклада меняют имена только поддерживаемых классов; RU/EN без коллизий.
- `JAZZ-WEAPON-PRESENTATION-001-AC-003` — runtime: M4 с прямым магазином и AK с изменённым прикладом возвращают установленный путь; UI загружает PNG, chips сохраняются.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: дополнение существующего InventoryItem icon hook и существующего setter, без второго wrap.
- Saves: производное представление восстанавливается из компонентов, ID предмета прежний.
- Network/determinism: нет RNG и изменения боевых данных.
- Generated data: без изменения items/metadata/companions.
- Cross-package references: только чтение assets/localization для проверки.
- Rollback/recovery: резервные копии каждого затронутого активного файла.

## План и ownership

- Пакет-владелец: jazz.
- Исполнитель и Reviewer: текущий агент, самостоятельная проверка по поручению пользователя; human acceptance отдельно.
- Declared write set: YAML выше; активная копия тех же runtime-файлов.
- Exclusive resources: runtime presentation hooks, localization export; соседняя модельная задача не активна.

## Решение владельца

- Статус: approved.
- Кто подтвердил: пользователь, «ставь», после просмотра staged/review.html.
- Дата: 2026-09-28.

## Evidence

- `JAZZ-WEAPON-PRESENTATION-001-AC-001`: `PASS` — static: 1739 установленных PNG, Lua-harness полного каталога, неизвестные host/component возвращают fallback.
- `JAZZ-WEAPON-PRESENTATION-001-AC-002`: `BLOCKED` — имена не установлены: существующий конфликт RussianManual.csv (AnchorID 890000000020255); файлы локализации не изменялись.
- `JAZZ-WEAPON-PRESENTATION-001-AC-003`: `PASS` — runtime: M4A1 с малым магазином и AK74 со сложенным прикладом отрисованы в XImage/XInventoryItem; chips остаются отдельными дочерними окнами. Evidence: `layer-runtime-verification.json`, `layer-runtime-combinations.png`.

## Documentation delta

UI technical, weapons wiki и showcase RU/EN фиксируют exact-match snapshots и структурные имена с ограничениями.

## Промежуточная установка

Пользователь уточнил «ладно, ставь как есть пока» после разъяснения неполного охвата комбинаций. Установлены снимки и exact-match selector. Полная спецификация остаётся approved: REQ-002 и runtime acceptance ещё не завершены. Не объявлять implemented/accepted. Резервные копии активных двух Lua-файлов сохранены вне репозитория, путь указан в installation-verification и отчёте установки.


Уточнение владельца: отключённое оружие не снимать. AR15, M4Commando и MP5 (`catalog_status=excluded_disabled`) исключены из установки, основной галереи и будущих capture batches. 53 иконки удалены только из WeaponIcons/Live; staged/raw архив сохранён. Проверка селектора после фильтрации: 5281 PASS.


## Исправление масштаба и тона — одобрено владельцем

Основание: скриншот инвентаря, замечания о размере и бледности, «поправь все иконки». REQ-001 дополнен: реальные границы силуэта нормализуются в формат исходного Icon (длинное оружие обычно 324×165, пистолеты 162×110); сохраняются пропорции, прозрачность и безопасный отступ. Все активные снимки проходят одинаковую умеренную коррекцию контраста/насыщенности; raw RGBA не меняется. Смена отступов не меняет game UI или состав оружия. Проверка static: размеры по original Icon, alpha края, покрытие всех установленных иконок; visual: сравнение до/после с оригинальными иконками. Фактическое отображение после обновления требует отдельного runtime подтверждения.


## Цвет v3: ближе к прежним иконкам

Владелец запросил цветокоррекцию ближе к исходным игровым иконкам. Общая формула v2 заменяется фиксированной монотонной кривой яркости и коэффициентом насыщенности для каждого класса, измеренными по default capture и original Icon. Все варианты класса используют одинаковую калибровку, а не auto exposure каждого кадра. Для отсутствующего локального референса — медианный профиль измеренного набора с явным списком fallback. Размер, геометрия, alpha и отступы v2 сохраняются. Проверка: сравнение оригинал/v2/v3, статистика яркости default, прежние проверки установленных файлов.


Дополнительное одобрение владельца: «и обводку еще, да». Усилить контур до 2 px, RGB 5/6/7; сохранять размер холста и масштаб оружия, проверить отсутствие обрезки контура.


Уточнение после v3: DesertEagle и HiPower выглядят пятнисто. Для этих двух семейств заменить резкую квантильную кривую на гладкую степенную аппроксимацию с ограничением усиления контраста до 2; сохранить прежние размеры, alpha и обводку. Основание — замечание владельца «дигл и хайпаур странные». Проверить все варианты двух классов и сравнить оригинал/до/после.


## Полные сочетания модулей — 29.09.2026

Решение владельца: «надо сделать все комбинации аттачей у оружия чтоб были видны». Это разрешает расширить прежний exact-match scope: все допустимые сочетания активного оружия должны одновременно отображать установленные видимые детали. Отключённое оружие и служебный DebugAuto не снимать. Невидимые механические модификации не требуют отдельного изображения.

- `JAZZ-WEAPON-PRESENTATION-001-REQ-004`: подготовить зарегистрированные слои из настоящих visual objects игры; использовать фактические entity, parent/spot, transform и состояние корпуса. Зависимость модуля от ствола/цевья/крепления учитывается в ключе. Не вычитать детали из старых полных снимков.
- `JAZZ-WEAPON-PRESENTATION-001-REQ-005`: композиция обновляется в существующем image binder без изменения предмета/сохранения; единое кадрирование по объединённому силуэту, единые профили цвета, приближённые к исходным иконкам, обводка под всеми цветными слоями. Неактуальные слои удаляются при замене, снятии, смене оружия и закрытии UI.
- `JAZZ-WEAPON-PRESENTATION-001-REQ-006`: крепления имеют отдельные layer IDs и зависимости, пригодные для последующей переделки. На этом этапе не меняется их игровая модульность.
- `JAZZ-WEAPON-PRESENTATION-001-AC-004`: runtime/visual — АК с магазином + прицелом + прикладом одновременно; сравнить целый игровой снимок с композицией, включая перекрытия, отверстия и размеры.
- `JAZZ-WEAPON-PRESENTATION-001-AC-005`: static/runtime — аудит всех активных классов и доступных визуальных вариантов; проверка зависимых пар, пустых слотов, A→B→A и отсутствия устаревших слоёв. Отдельно перечислить незакрытые конфигурации, не объявлять частичное покрытие полным.

Стратегия: сначала подтвердить native layer capture на АК; затем общий каталог слоёв и зависимостей, интеграция существующего binder и проверка полного арсенала. Полный плоский декартов продукт не является выбранным форматом хранения. Прежние запреты runtime bake, компрессорных hooks и изменения боевых данных сохраняются. Файлы разработки/сырой съёмки остаются в docs/design/weapon-layer-icons/live и docs/tools/weapon_layer_icons; установка готовых слоёв — WeaponIcons/Live. Игра уже запущена владельцем, подтверждён ModEditor и read-only live DAP, без initialize/pause.

Evidence AC-004/005: PASS для native composition — см. итоговое evidence ниже; старые 1739 exact-match PNG остаются fallback.

Уточнение write set для того же одобренного scope: два `run_after` шаблона `UIWeaponDisplay` в `items.lua` вызывают тот же binder, чтобы обе панели оружия сразу показывали состав модулей. У `ModItemXTemplate/UIWeaponDisplay` нет companion Lua; runtime подтвердил `GetCodeFileName() == nil`. Правка выполняется через `CompileFunc`/свойство ModItem и официальный save/reload после завершения съёмки. `metadata.lua` меняется штатным сохранением; порядок кода и другие ModItem не меняются намеренно. Перед сохранением проверить актуальность загруженных items и сохранить внешний baseline, затем проверить scoped diff и round-trip.


Уточнение владельца 29.09.2026: «ещё обработать бы картинки чтоб ± было как раньше выглядело». Для native layers утверждена плавная коррекция по текущим default captures и исходным Icon; один ограниченный профиль яркости/насыщенности на семейство, без усиления отдельных диапазонов бликов. `layer-color-profiles.json`, `calibrate_layers.py` и сравнение original/previous/smooth входят в существующий write set инструментов и visual evidence. Геометрия/alpha/цветовая согласованность модулей сохраняются.

Промежуточное evidence нового scope: AC-004 — runtime PASS на реальных XImage/XInventoryItem для AK74, M4A1, DesertEagle с несколькими модулями одновременно. AC-005 — offline PASS 448950 случаев, 9797 native graphs; 76286 BlockSlots-конфликтов явно исключены. Все 178 активных классов имеют композицию, compile issues=0. Цветовой проход v4 установлен: 1928 PNG, alpha сохранена побайтно, визуально проверены исходные/новые иконки и реальный открытый инвентарь. Evidence: `docs/design/weapon-layer-icons/live/layer-verification.json`. Полная spec остаётся approved из-за открытого AC-002 по именам; завершение иконок не означает выполнение переименований.
