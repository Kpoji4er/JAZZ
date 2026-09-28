---
id: JAZZ-WEAPON-PRESENTATION-001
status: approved
owner: project-owner
systems:
  - weapon-presentation
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
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

Произвольная композиция слоёв, отдельные крепления, новые модели, публикация и изменение баланса. Имена Mosin принадлежат отдельной модельной задаче.

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
- `JAZZ-WEAPON-PRESENTATION-001-AC-003`: `BLOCKED` — игра закрыта, DAP connection refused. Установка выполнена на диск; live UI не проверен.

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
