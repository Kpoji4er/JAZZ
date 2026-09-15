---
id: JAZZ-WEAPON-SR3M-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/SR3M.lua
  - jazz/WeaponIcons/SR3M.png
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/*sr3m*
  - jazz/docs/tools/README.md
  - jazz/docs/specs/active/JAZZ-WEAPON-SR3M-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/SR3M*
  - jazz_assets/Entities/Meshes/SR3M*
  - jazz_assets/Entities/Materials/SR3M*
  - jazz_assets/Entities/Textures/SR3M*
  - jazz_assets/Entities/Textures/Fallbacks/SR3M*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - localization SR3M strings
  - SR3M Blender export state
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-15
---

# JAZZ-WEAPON-SR3M-001: СР-3М из исходной Blender-сцены

## Проблема

В Weapons/SMG/SR_3M/SR_3M.blend есть 10 mesh-объектов и пять упакованных текстур. Игровые SR3M entities не найдены. Нет spots, у Barrel нет материала. Подготовленные UMP45 и AS_Val служат локальными образцами структуры.

## Цели

- Собрать СР-3М и добавить его непосредственно в JAZZ по образцу существующего оружия.

## Non-goals

- Отдельный мод отменён владельцем. Массовая обработка оружейного архива, публикация и изменение отрядов не входят в задачу.

## Требования

- `JAZZ-WEAPON-SR3M-001-REQ-001` — исходник сохраняется; новая сборка получает отдельные корпус, магазин, приклад и дульный модуль с согласованными spots.
- `JAZZ-WEAPON-SR3M-001-REQ-002` — предмет SR3M — предварительно SubmachineGun Т3, JAZZ_Caliber_9x39; компоненты подключаются штатными WeaponComponentVisual. Без интегрированного глушителя. Тестовый под-тир 3-2, Compact, SMG attacks; FX от AK74. Последнее уточнение владельца оставляет выбор ПП/карабин за игровыми потребностями: класс ПП — проверяемая гипотеза, а не окончательное утверждение.
- `JAZZ-WEAPON-SR3M-001-REQ-003` — items, metadata, companions и ресурсы синхронны; название и описание RU/EN, иконка из модели.

## Инварианты и ограничения

- Исходные .blend и чужой dirty state сохраняются. Existing IDs и зависимости пакетов не меняются.
- Первоначальное ограничение Bobby out / без автоматической выдачи заменено одобренным вводом 2026-09-16 в JAZZ-WEAPON-ROLLOUT-001.
- Базовые числа берутся относительно AS_Val, с явным обычным шумом без глушителя. Это первый тестовый баланс.

## Acceptance criteria

- `JAZZ-WEAPON-SR3M-001-AC-001` — static: исходник сохранён, новая сцена и экспорт содержат все выбранные детали, текстуры и attachment spots; модульная сборка геометрически совпадает.
- `JAZZ-WEAPON-SR3M-001-AC-002` — static: все runtime-ссылки разрешаются, generated sync и Lua validation проходят для добавленных данных.
- `JAZZ-WEAPON-SR3M-001-AC-003` — editor/runtime: save/reload сохраняет предмет; модель видна в инвентаре, руках и на земле; магазин и приклад не пропадают; стрельба и перезарядка работают.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: существующая модель SubmachineGun без новых hooks. Для теста выбран ближний штурм в движении с RunAndGun и JAZZ_Zipper; альтернативный Carbine предполагает роль ближняя–средняя дистанция, RunAndGun_Carbine и JAZZ_TargetSweep. Выбор сверяется с docs/technical/weapons/class-roles.md.
- Saves: новый предмет, существующие экземпляры не изменяются.
- Network/determinism: штатные presets и components.
- Generated data: два пакета, полная транзакция.
- Cross-package references: jazz -> jazz_assets по существующей зависимости.
- Rollback/recovery: убрать только добавленные SR3M записи и файлы; исходники сохранены.

## План и ownership

- Пакет-владелец: jazz_assets — геометрия; jazz — предмет и визуалы компонентов.
- Исполнитель: текущая задача Codex.
- Reviewer: владелец проекта, визуальная приёмка.
- Declared write set: перечислен в frontmatter; Blender-рабочая копия в отдельном каталоге Weapons/_sr3m_jazz_build вне канонических репозиториев.
- Exclusive resources: перечислены в frontmatter.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец в текущем разговоре: «давай сразу по образу и подобию в игору втсорем» после выбора СР-3М.
- Дата: 2026-09-15.

## Evidence

- `JAZZ-WEAPON-SR3M-001-AC-001`: частично проверено — отдельная Blender-сборка экспортирована официальным AssetsProcessor; шесть entities, пять привязок визуалов, четыре пары DDS/fallback. Исходник сохранён. Компилятор завершился успешно, но сообщил о двух нулевых нормалях корпуса; вид в игровом renderer ещё не принят.
- `JAZZ-WEAPON-SR3M-001-AC-002`: `PASS` для добавленных данных — python docs/tools/_check_sr3m.py: равенство ModItem/companion, Lua, ссылки entities/materials/textures, spots и RU/EN. Общая проверка пакетов имеет прежние ошибки; глобальный generated sync не объявляется пройденным.
- `JAZZ-WEAPON-SR3M-001-AC-003`: `BLOCKED` — успешный editor/runtime тест пока отсутствует; руки, земля, звук, стрельба, перезарядка и save/reload требуют проверки.

Тестовый профиль: урон 32, дальность 26, магазин 30, выстрел 4 AP, перезарядка 5 AP, отдача 20, очереди 4/9, темп 900. Усиленный патрон компенсируется короткой дистанцией и отдачей; превосходство над другими ПП ещё не проверено в бою.

## Documentation delta

- После реализации: профильная technical-страница, file coverage и краткое описание тестового предмета RU/EN; непроверенный runtime помечается явно.
