---
id: JAZZ-WEAPON-AEK-001
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
  - jazz/InventoryItem/AEK971.lua
  - jazz/Code/Weapon_AEKModular.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/WeaponIcons/AEK*.png
  - jazz/docs/tools/*aek*
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-plan-jaweapons.md
  - jazz/docs/design/aek-import.md
  - jazz/docs/specs/active/JAZZ-WEAPON-AEK-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/technical/weapons/data/*.csv
  - jazz/docs/wiki/weapons/**
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/*/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/JAZZ_AEK*
  - jazz_assets/Entities/Meshes/JAZZ_AEK*
  - jazz_assets/Entities/Materials/JAZZ_AEK*
  - jazz_assets/Entities/Textures/JAZZ_AEK*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_AEK*
exclusive_resources:
  - items.lua
  - metadata.lua
  - localization-runtime-export
  - mod-editor-state
approved_by: project-owner
---

# JAZZ-WEAPON-AEK-001: единое семейство АЕК-971 / АЕК-973С

## Проблема

Новая очередь владельца начинается с АЕК. Предмет отсутствует; у исходника 971
после пакетного импорта не назначены два материала, 973С имеет исходный PBR.

## Цели

Один предмет AEK971, смена калибра, имени и модели конфигурацией 973С.
Подготовить исходные поверхности и доступные модули без искусственного изменения
авторских цветов и normal maps.

## Non-goals

Публикация, изменение других семейств, массовая фракционная выдача и запуск игры
до возобновления отложенной владельцем игровой проверки.

## Требования

- `JAZZ-WEAPON-AEK-001-REQ-001`: модели обоих архивов, UV и исходные PBR; RM=(roughness,roughness,metallic), никаких полных RGB-инверсий или ослабления Normal. Проверить mesh winding после компиляции.
- `JAZZ-WEAPON-AEK-001-REQ-002`: один экземпляр с обратимой сменой 5,45×39 / 7,62×39, названия АЕК-971 / АЕК-973С; переключение не оставляет патронов другого калибра и не теряет состояние экземпляра.
- `JAZZ-WEAPON-AEK-001-REQ-003`: рабочие статы из плана: Damage 26/30 (971 сохранён; 973С = АК-103 +1), Range 50/42, Recoil 13/17 со штатным разложенным прикладом до модификаторов боеприпаса, AimAccuracy 12/11, RPM 900, Magazine 30, ShootAP 5000, ReloadAP 6000, Reliability 90, Resource 8000; прочие по аналогам АК-74М/АК-103. Т3-2. Отдельные типы магазинов/приклада/дульных/прицелов включать только с проверенной геометрией.
- `JAZZ-WEAPON-AEK-001-REQ-004`: согласованные items/metadata/companion, RU/EN, иконки; Bobby in: Tier 4, RestockWeight 25, MaxStock 1, Cost 22000, CategoryPair AssaultRifles — редкий современный автомат выше АК-74М.

## Инварианты и ограничения

Архивы read-only. Существующие ID и чужие правки сохраняются. Scale по АК-74М,
не по заниженному легаси АК-74. Не создавать custom/split mesh normals.
Фракционная доступность остаётся прежней; новый предмет не внедряется в loadouts.

## Acceptance criteria

- `JAZZ-WEAPON-AEK-001-AC-001`: source/UV/material audit, оба боковых и верхний виды с масштабной линейкой; HGM/DDS и нормали проходят проверки.
- `JAZZ-WEAPON-AEK-001-AC-002`: executable Lua проверка смены конфигураций, патронов, сохранения Condition/id; без накопления модификаторов.
- `JAZZ-WEAPON-AEK-001-AC-003`: согласованы три слоя регистрации и RU/EN, Lua/refs проверены; editor round-trip и runtime/human проверяются отдельно при возобновлении игры.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: native FirearmBase setter, отдельные методы класса; без второго глобального wrap.
- Saves: новый ID, старые экземпляры не меняются.
- Network/determinism: смена штатным компонентным действием, без RNG.
- Generated data: jazz и jazz_assets одной ограниченной транзакцией.
- Cross-package references: jazz AEK971 → jazz_assets JAZZ_AEK*.
- Rollback/recovery: staging, хэши исходных файлов и backup до установки.

## План и ownership

jazz владеет предметом/компонентами/локализацией; jazz_assets — визуалами.
Исполнитель — текущий чат; reviewer — последующая игровая проверка владельцем.
Declared write set и exclusive resources перечислены выше; changes uncommitted.

## Решение владельца

Approved 2026-10-03: «дальше новое оружие по этому плану»; дополнительно:
«Взять предложенные числа как рабочие, недостающие подобрать по аналогам».

Текущая установка отдельно от общей очереди явно запрошена: «вставь пока в игру аек».
Первый комплект: Barrel `JAZZ_AEK_545` / `JAZZ_AEK_762`, штатный магазин на 30,
штатный складной приклад через существующую пару StockLight. Оптика и прочие
непроверенные внешние крепления в этот комплект не включаются.
Изменения 973С задаются штатными component effects: калибр 7,62×39,
Damage +4, Range -8, Recoil +4, AimAccuracy -1. Предмет сохраняет ID AEK971.
Для загруженного оружия без владельца/сумки смена калибра запрещена до разгрузки;
при наличии владельца используется штатный ChangeCaliber/UnloadWeapon.

## Evidence

- `JAZZ-WEAPON-AEK-001-AC-001`: PASS (offline) — 8 compiled HGM, triangle/winding comparison; авторские карты и RM; scale overlays обеих конфигураций с АК-74М, CPU PBR previews. Установка выполнена, визуальная приёмка в игре впереди.
- `JAZZ-WEAPON-AEK-001-AC-002`: PASS (offline Lua) — 10 обратных конверсий, native caliber/unload, clone isolation, ownerless guard, Condition/id, presentation restore и stock/mag visuals. Полное native save/load ещё не проверено.
- `JAZZ-WEAPON-AEK-001-AC-003`: BLOCKED — data/assets/ModItemCode установлены, structural и generated checks без новых ошибок; девять RU/EN ID добавлены ограниченным экспортом с сохранением прежних строк. Общий localization audit блокируют существующие чужие коллизии; editor round-trip/runtime ещё не выполнены. Подробности: `docs/design/aek-import.md`.

## Documentation delta

Отчёт source/staging в docs/design/aek-import.md; actual installed состояние
в technical/wiki/showcase после интеграции с явной отметкой отложенного runtime.

## Уточнение владельца 2026-10-03: игровая проверка

Разрешены исправление ошибочного gamma decode BaseColor, урон 26/30 по последнему уточнению владельца, итоговая отдача 13/17 со штатным прикладом, прицелы на обеих конфигурациях. Normal/RM и геометрия остаются исходными. Проверка прицелов включает крепление и сохранение при смене калибра.


## Дополнение владельца 03.10: оптика и обвес

Решение: approved, прямой запрос владельца в текущем чате.

- `JAZZ-WEAPON-AEK-001-REQ-ATT-031`: Добавить съёмные прицелы обоим вариантам через общий Scope: закрытый коллиматор, EOTech, M68, 2x и ACOG; снятие прицела и смена калибра сохраняют корректное состояние.
- `JAZZ-WEAPON-AEK-001-AC-ATT-031`: синхронные items/companion, существующие ID компонентов, offline Lua смены/снятия, проверка spots и geometry. Runtime/editor и визуальная посадка — отдельно, игру не запускать.

Exclusive resources: items.lua, companion и экспорт AEK. Backup/hash guards; не затрагивать посторонние изменения.

`JAZZ-WEAPON-AEK-001-AC-ATT-031`: PASS static/offline/install; items syntax, companion sync, native setter tests, backups/hashes. Runtime/editor/human NOT_RUN. Evidence: docs/design/weapon-shading-recheck-20261003.md.
