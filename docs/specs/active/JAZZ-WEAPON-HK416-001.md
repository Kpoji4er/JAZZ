---
id: JAZZ-WEAPON-HK416-001
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
  - jazz/InventoryItem/HK416.lua
  - jazz/Code/Weapon_HK416Modular.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/WeaponIcons/HK416*.png
  - jazz/docs/technical/**
  - jazz/docs/wiki/**
  - jazz/docs/showcase/**
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/JAZZ_HK416*
  - jazz_assets/Entities/Meshes/JAZZ_HK416*
  - jazz_assets/Entities/Materials/JAZZ_HK416*
  - jazz_assets/Entities/Textures/**
  - jazz/docs/tools/*hk416*
  - jazz/docs/tools/README.md
  - jazz/docs/design/hk416-import.md
  - jazz/docs/specs/active/JAZZ-WEAPON-HK416-001.md
  - external/JaWeapons/Weapons/_weapon_import_20261003/hk416/**
  - external/JaWeapons/Weapons/_hk416_jazz_build/**
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-WEAPON-HK416-001: модульный HK416, подготовка

## Проблема

Очередь №2: 26 анонимных OBJ без MTL. model_17 без UV, model_25 имеет иной масштаб. Перед интеграцией требуется восстановить состав и совместимость.

## Цели

- Один HK416 с вариантами ствола, цевья, приклада, рукояти, оптики и дульных; подготовленная сцена и явная матрица совместимости.

## Non-goals

- Установка неподтверждённых моделей, закрытие игры, публикация.

## Требования

- `JAZZ-WEAPON-HK416-001-REQ-001` — Исходники read-only; сохранить UV/normal и цвета. Восстановить только доказанные bindings; specular/gloss не объявлять metallic/roughness.

## Инварианты и ограничения

- Архивы и действующие предметы неизменны. Отдельные модификации не создают отдельные предметы.

## Acceptance criteria

- `JAZZ-WEAPON-HK416-001-AC-001` — Проверяемый пакет: части, источники, hashes, материал/UV аудит, scene и ограничения модулей.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: additive HK416 item; existing shared component effects reused.
- Saves: no migration; one item ID, component choices serialized by native firearm system.
- Network/determinism: native component setter; presentation derived only from component IDs.
- Generated data: items/metadata plus HK416 companion and six asset entity companions synchronized.
- Cross-package references: jazz owns item/code/icons/localization; jazz_assets owns six entities and their meshes/materials/textures.
- Rollback/recovery: hash-guarded install receipt, initial backup and separate asset refresh backups in external build directory.

## План и ownership

- Пакет-владелец: jazz; resource owner jazz_assets.
- Исполнитель: Codex, текущий чат.
- Reviewer: владелец, визуальная приёмка впереди.
- Declared write set: front matter; scoped installation and documentation only.
- Exclusive resources: items.lua/metadata.lua both packages, three HK416 localization IDs, six entity IDs.

## Решение владельца

- Статус: approved, подготовка.
- Кто подтвердил: владелец, «подготовь пока следующее оружие», «значит надо модулями», «делай».
- Дата: 2026-10-03

## Evidence

- `JAZZ-WEAPON-HK416-001-AC-001`: `BLOCKED` — preparation and offline installation complete: six entities, three barrels/two stocks/five optics, nine configuration checks PASS, compiled geometry/winding PASS. Authored MLOD sharp boundaries recovered after owner's rejected preview. RM remains an explicit legacy-shader approximation. Magazine orientation corrected from owner's reference; final asset refresh and runtime/human acceptance must be verified separately. Additional handguards/grips remain pending. Evidence: docs/design/hk416-import.md.

## Documentation delta

- Установлен кандидат HK416; canonical weapon CSV/wiki обновлены. Evidence и незавершённая визуальная приёмка: docs/design/hk416-import.md.

## Установка, решение владельца

2026-10-03: «416 уже в игре? если нет то вставь». Установка одного HK416 разрешена, запуск игры запрещён до отдельного запроса. Первый кандидат: базовый D14.5, короткий D10, длинный D20; штатный/CTR приклад, магазин STANAG 30, прицелы. Не выдавать неподготовленные варианты цевья за игровые модули. Рабочие статы по M4A1: Damage 23, Range 46, AimAccuracy 12, Recoil 17, Reliability 90, RPM 850, Т3-1; Bobby Tier4, Cost18000, RW30, MaxStock1. Калибр 5.56. Материалы legacy Super адаптируются явно, не объявляются точным shader match. Исходные CO/NM неизменны. Generated layers синхронизируются, compiled mesh/winding и смены модулей проверяются offline; runtime требует отдельной проверки владельцем.


## Дополнение владельца 03.10: оптика и обвес

Решение: approved, прямой запрос владельца в текущем чате.

- `JAZZ-WEAPON-HK416-001-REQ-ATT-031`: Исправить внутрь направленные наружные поверхности при MLOD→Blender; сохранить UV и текстуры. Опустить Scope/Mount с 0.165 до 0.145 м по измеренной верхней плоскости планки. Добавить нижний слот рукоятки/M203 и боковой слот лазера/фонаря на всех трёх стволах.
- `JAZZ-WEAPON-HK416-001-AC-ATT-031`: синхронные items/companion, существующие ID компонентов, offline Lua смены/снятия, проверка spots и geometry. Runtime/editor и визуальная посадка — отдельно, игру не запускать.

Exclusive resources: items.lua, companion и экспорт HK416. Backup/hash guards; не затрагивать посторонние изменения.

`JAZZ-WEAPON-HK416-001-AC-ATT-031`: PASS static/offline/install; items syntax, companion sync, native setter tests, backups/hashes. Runtime/editor/human NOT_RUN. Evidence: docs/design/weapon-shading-recheck-20261003.md.

## Посадка обвеса после релиза 0.20-6244

Решение владельца 04.10: approved — «подствольник надо подальше», «фонарик надо повернуть», «у аека планки нет — от акма», затем «после релиза доделай».

- `JAZZ-WEAPON-HK416-001-REQ-FIT-041`: Сдвинуть только M203 вперёд, сохранив рукоятки на прежнем месте; повернуть боковые фонари/лазеры вокруг продольной оси для посадки крепления на боковую планку. Изменения выполняются в существующем HK416:UpdateVisualObj, без новых hooks и правки материалов.
- `JAZZ-WEAPON-HK416-001-AC-FIT-041`: offline render реальной геометрии, повторное UpdateVisualObj без накопления смещения, смена/снятие модулей и все варианты оружия. Игровая визуальная приёмка остаётся за владельцем; игру не запускать.

Write set: существующий Code/Weapon_HK416Modular.lua, items.lua для AEK Mount visuals, профильные tools/spec/design/technical. Exclusive resource: items.lua; закрытая игра/редактор, резервная копия перед установкой. Новых ID и companion-записей нет.

`JAZZ-WEAPON-HK416-001-AC-FIT-041`: PASS static/offline/install — native visual selection, повторные обновления, снятие модулей, все конфигурации, 15 ракурсов реальной геометрии и hash-guarded установка. Runtime/editor/human: NOT_RUN; владелец проверит в игре. Дополнение реализовано локально после релиза.
