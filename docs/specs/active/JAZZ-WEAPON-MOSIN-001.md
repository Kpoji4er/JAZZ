---
id: JAZZ-WEAPON-MOSIN-001
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
repositories:
  - jazz
  - jazz_assets
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/InventoryItem/JAZZ_MosinModular.lua
  - jazz/InventoryItem/Mosin.lua
  - jazz/scripts/legion-loadouts/data/early_variants.json
  - jazz/scripts/legion-loadouts/data/weapon_tag_overrides.json
  - jazz/scripts/legion-loadouts/data/recipes.json
  - jazz/scripts/legion-loadouts/generate.py
  - jazz/docs/technical/weapons/data/weapon-component-options.csv
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz/Code/Weapon_MosinModular.lua
  - jazz/WeaponIcons/MOSIN*.png
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/*rifle*
  - jazz/docs/tools/*mosin*
  - jazz/docs/tools/*l42a1*
  - jazz/docs/tools/_runtime_weapon_imports.lua
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-queue.md
  - jazz/docs/specs/active/JAZZ-WEAPON-MOSIN-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/MOSIN*
  - jazz_assets/Entities/Meshes/MOSIN*
  - jazz_assets/Entities/Materials/MOSIN*
  - jazz_assets/Entities/Textures/MOSIN*
  - jazz_assets/Entities/Textures/Fallbacks/MOSIN*
exclusive_resources:
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - MOSIN localization IDs and Blender build
related_decisions:
  - none
approved_by: project-owner in conversation 2026-09-15
---

# JAZZ-WEAPON-MOSIN-001: Мосинка с тремя вариантами длины

## Проблема

Исходные OBJ и текстуры есть в локальном архиве Weapons/Sniper; MTL отсутствуют, экспорт и предмет пока отсутствуют.

## Цели

- Подготовить рабочую сборку и добавить тестовый предмет непосредственно в JAZZ.

## Non-goals

- Публикация, изменение тиров Легиона, изменение остальных семейств оружия.

## Требования

- `JAZZ-WEAPON-MOSIN-001-REQ-001` — Существующий предмет Mosin (уточнение владельца заменяет отдельный тестовый JAZZ_MosinModular) с вариантами 1891, M38 и Obrez. Согласованные ствол и ложа каждого варианта; единый патрон 7.62x54R, базовые урон/крит от калибра с поправками на вариант. Звуки от Mosin. Сохранить публичный ID Mosin, прежний магазин/тир/доступность; отдельный тестовый ModItem убрать.
- `JAZZ-WEAPON-MOSIN-001-REQ-002` — сохранить исходники; экспортировать отдельные entities с attachment spots, согласовать ModItem, metadata, companion и локализацию.
- `JAZZ-WEAPON-MOSIN-001-REQ-003` — иконка из Blender, направление слева направо, прозрачный фон и обводка.
- `JAZZ-WEAPON-MOSIN-001-REQ-004` — уточнение владельца: Obrez является уникальным вариантом слота Barrel, одновременно изображающим короткий ствол и отсутствие полноценного приклада. Отдельную покупку/установку приклада для него не требовать. Снизить стоимость выстрела в AP, улучшить ближнюю стрельбу без прицеливания, существенно ухудшить прицельную стрельбу и дальность. Урон/крит остаются производными от 7.62x54R с поправкой на конфигурацию.
- `JAZZ-WEAPON-MOSIN-001-REQ-005` — уточнение владельца 2026-09-15: объединить старую и новую мосинки, сохранить прежний ПУ и предпочитаемый вид материалов. Длинная конфигурация использует существующие mesh/material Mosin через MOSIN_1891; M38 и Obrez сохраняют новые модели. Вернуть необязательный Scope/JAZZ_Scope_PU и точки крепления; исправить точки удержания. Исходную новую геометрию 1891 сохранить в build для дальнейшей работы.

- `JAZZ-WEAPON-MOSIN-001-REQ-006` — уточнение владельца: оставить старый item Mosin, убрать отдельный тестовый item; новые конфигурации раздать Легиону через существующий генератор и подходящие слоты. длинная Mosin — только sniper для выдачи; M38 — battle/rifle, как MAS36; Obrez — carbine/smg (в том числе Marauder), без pistol-тега; Obrez весит 100 на T1 и 10 на T2, ниже остальных ПП/карабинов; у Roughneck ещё ниже: 10 на T1 и 1 на T2; без смены класса оружия на автоматический ПП. Сохранить существующие тиры и границы прогрессии; по явному решению владельца обычная винтовка/M38/Obrez используют старый порог T1-2 (12), остаточное оружие T2 (20–29); снайперская PU сохраняет прежний ранний допуск. Каталожный тир самого предмета не меняется.

## Инварианты и ограничения

- Уточнение владельца 2026-09-16: ПУ только на длинной снайперской конфигурации JAZZ_Mosin1891. M38/Obrez блокируют Scope через штатный BlockSlots, как блокировка Muzzle у APS. При установленном ПУ интерфейс требует сначала снять его, затем сменить ствол; при прямой установке короткого ствола штатный setter очищает заблокированный слот. ПУ не переносится на короткие варианты.

- Чужие изменения сохранять. Общие файлы не записывать при пересечении с задачей «Изучить мод JAZZ»; при прерывании дождаться освобождения ресурса.
- Существующий Mosin сохраняет прежние CanAppearInShop, Tier, RestockWeight и стоимость.
- Рабочие копии хранятся отдельно в Weapons/_mosin_jazz_build.

## Acceptance criteria

- `JAZZ-WEAPON-MOSIN-001-AC-001` — static: материалы восстановлены, геометрия и точки крепления согласованы; исходники сохранены.
- `JAZZ-WEAPON-MOSIN-001-AC-002` — static: Lua и ссылки проходят проверки; RU/EN, иконка и граф ресурсов присутствуют.
- `JAZZ-WEAPON-MOSIN-001-AC-003` — editor/runtime: загрузка, предмет в руках/на земле, смена доступных компонентов, выстрел/перезарядка со звуком и save/reload без ошибок.
- `JAZZ-WEAPON-MOSIN-001-AC-004` — static/runtime: выбор Obrez в Barrel одновременно меняет ствол и ложу; по сравнению с длинным вариантом выстрел дешевле, ближний профиль без aim лучше, максимальный aim и дальность хуже. Обратная смена возвращает исходные параметры без накопления модификаторов.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: штатные числовые эффекты компонентов; методы только Mosin выбирают цельную визуальную конфигурацию по Barrel и размер Long/Carbine/Compact. Глобальные классы не оборачиваются. Разные исходные ложи и ствольные коробки не подменяются искусственной общей невидимой геометрией.
- Saves: публичный ID Mosin сохраняется; старый экземпляр без Barrel получает длинную визуальную конфигурацию по умолчанию. Промежуточный тестовый JAZZ_MosinModular удаляется из каталога по указанию владельца.
- Network/determinism: штатные данные компонентов.
- Generated data: items + metadata + companions.
- Cross-package references: jazz -> jazz_assets через существующую зависимость.
- Rollback/recovery: удалить только новые записи и ресурсы; исходные ZIP/OBJ сохранены.

## План и ownership

- Пакет-владелец: jazz — предмет и компоненты; jazz_assets — геометрия и текстуры.
- Исполнитель: текущая оружейная задача.
- Reviewer: владелец проекта.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter; перед записью перепроверить параллельную задачу.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец поручил L42A1 с собственным прицелом, затем «продолжай работу, в том числе над мосинками».
- Дата: 2026-09-15.

## Evidence

- Уточнение ПУ 2026-09-16: static PASS — реальные JAZZ setter и vanilla `GetComponentBlocksAnyOfAttachedSlots`/`GetNumModifySlotOptions` в Lupa: смена на короткий ствол требует снятия ПУ в UI, Scope недоступен на M38/Obrez, снова доступен на длинной конфигурации; прямой setter очищает заблокированный слот. Визуальный smoke обновлён под новые AP 7/5 без ПУ у коротких конфигураций, но не запускался в новом runtime. Metadata/companion без delta, меняются только два WeaponComponent в items.lua.

- `JAZZ-WEAPON-MOSIN-001-AC-001`: `BLOCKED` — подготовка геометрии продолжается.
- `JAZZ-WEAPON-MOSIN-001-AC-002`: `BLOCKED` — интеграция ещё не выполнена.
- `JAZZ-WEAPON-MOSIN-001-AC-003`: `BLOCKED` — требуется игровая проверка.
- `JAZZ-WEAPON-MOSIN-001-AC-004`: `BLOCKED` — конфигурации ещё не подключены.

## Documentation delta

- После интеграции обновить профильные страницы; непроверенное игровое поведение отмечать явно.
