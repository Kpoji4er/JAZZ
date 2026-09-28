---
id: JAZZ-WEAPON-R4-001
status: implemented
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
  - jazz/docs/design/references/weapon-feedback-20260928/*
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/.agents/docs/playbooks/model-export-qa-handoff.md
  - jazz/docs/tools/_weapon_feedback_*
  - jazz/docs/design/weapon-visual-feedback-20260927.md
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz/docs/design/legion-weapon-availability-by-tier.md
  - jazz/docs/tools/_integrate_r4_loot.py
  - jazz/InventoryItem/VektorR4.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/WeaponIcons/VektorR4.png
  - jazz/Localization/*
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/docs/tools/*r4*
  - jazz/docs/tools/README.md
  - jazz/docs/specs/active/JAZZ-WEAPON-R4-001.md
  - jazz/docs/technical/weapons/data/*
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/systems/file-coverage.md
  - jazz/docs/wiki/weapons/*
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities/JAZZ_VektorR4*
  - jazz_assets/Entities/Meshes/JAZZ_VektorR4*
  - jazz_assets/Entities/Materials/JAZZ_VektorR4*
  - jazz_assets/Entities/Textures/JAZZ_VektorR4*
  - jazz_assets/Entities/Textures/Fallbacks/JAZZ_VektorR4*
exclusive_resources:
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - localization VektorR4
related_decisions:
  - JAZZ-WEAPON-ROLLOUT-001
approved_by: project-owner in current conversation 2026-09-26
---

# JAZZ-WEAPON-R4-001: Vektor R4, начало Т2

## Проблема

Дополнение 27.09.2026: владелец возобновил отложенный визуальный ремонт словами «можнго править». Основание и скриншоты: `docs/design/weapon-visual-feedback-20260927.md`. Немного затемнить металл Vektor R4, сохранить дерево и форму; обновить иконку.

- `JAZZ-WEAPON-R4-001-REQ-VISUAL-027`: Немного затемнить металл Vektor R4, сохранить дерево и форму; обновить иконку. Игровой баланс, публичные ID и регистрация сохраняются; работа только в jazz/jazz_assets, отдельная сборка и backup перед установкой при закрытой игре.
- `JAZZ-WEAPON-R4-001-AC-VISUAL-027`: static/offline — проверены точечные изменения, карты/меши и сборки, иконки 324×165 RGBA, исходные ресурсы сохранены. Runtime/human — подтверждение владельцем после нового запуска; offline PASS его не заменяет.


Владелец предоставил архив R4 Assault Rifle (SADF).zip и попросил импортировать оружие в начало Т2.

Источник: [R4 Assault Rifle (SADF), ARMSCor Studios](https://sketchfab.com/3d-models/r4-assault-rifle-sadf-da13b6b522634d33994a033be0e22b09). SHA256 предоставленного архива: `057c9e3da4e2bd4e711c9fde1e0e60386fd969fd17cf738f1cc1f35ee613ba63`. Архив не изменялся. Из него взяты OBJ, UV и BaseColor/Normal/Roughness/Metallic/AO; отсутствующий MTL восстановлен назначением этих карт, текстуры не генерировались.

## Цели

- Новый VektorR4, AssaultRifle, балансный Tier 2-1, 5.56, родная модель и текстуры.
- Надёжный, тяжёлый автомат с ограниченной штатной модульностью.

## Non-goals

- R5, новый калибр, изменение других стволов, изменение составов отрядов, публикация.

## Требования

- `JAZZ-WEAPON-R4-001-REQ-001`: сохранить исходный архив; проверить UV, карты и экспортные нормали; штатная длина 1.005 м, привязка к оружейному grip и проверка масштаба.
- `JAZZ-WEAPON-R4-001-REQ-002`: синхронно добавить предмет, entity, иконку 324x165, RU/EN и метаданные. Штатная сборка без выдуманных планок; модули только при пригодной геометрии.
- `JAZZ-WEAPON-R4-001-REQ-003`: Tier 2-1, магазин 35, Damage 21, ShootAP 6000, ReloadAP 6000, Reliability 85, Recoil 18, BDR 15, Range 46, Grouping 50, AimAccuracy 11, масса 43, RPM 650, очередь 3/6. Bobby in: Tier 2, RW 70, MaxStock 2, Cost 5500, AssaultRifles. Это стартовый баланс для плейтеста.

## Инварианты и ограничения

- Уточнение владельца в текущей беседе: R4 массовый в лут-таблицах, наравне с АК. Добавить в обычные подходящие пулы Легиона от Amount=21 с обычным весом 101000 (АК среднего Т2 имеет 103000); не в unique/rare. Генератор каталога должен воспроизводить добавление, без посторонней mass regen.

- Сохранить посторонние изменения рабочего дерева. Нет новых runtime hooks и globals.
- Нормали только пересчитанные, без custom/split; источники и build вне репозитория.

## Acceptance criteria

- `JAZZ-WEAPON-R4-001-AC-001`: static/visual offline — UV, полный ресурсный граф, масштаб, нормали, два бока и иконка без дефектов.
- `JAZZ-WEAPON-R4-001-AC-002`: static — items/metadata/companion, локализация и каталог согласованы, профильные валидаторы проходят.
- `JAZZ-WEAPON-R4-001-AC-003`: editor/runtime/human — save/reload, оружие в руках/на земле, стрельба, звук, перезарядка и визуальные детали приняты в игре.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новый предмет на существующем AssaultRifle, FX от существующего 5.56 оружия; зависимости без изменения.
- Saves: добавочный контент, старые ID сохранены.
- Network/determinism: новые статические данные, без RNG/hook изменений.
- Generated data: jazz и jazz_assets, единая ограниченная транзакция с backup.
- Cross-package references: VektorR4 -> JAZZ_VektorR4.
- Rollback/recovery: backup изменённых файлов до установки, откат только собственной вставки.

## План и ownership

- Пакет-владелец: jazz — предмет и баланс; jazz_assets — ресурсы.
- Исполнитель: текущая задача.
- Reviewer: project-owner, игровая приёмка.
- Declared write set: frontmatter.
- Exclusive resources: frontmatter; editor закрыт перед ручной установкой.

## Решение владельца

- Статус: approved.
- Кто подтвердил: владелец, «импортнем его? куда-нибудь в начало т2».
- Дата: 2026-09-26. Это разрешение реализации без повторного согласования.

## Evidence

Повторная визуальная правка 27.09.2026 по команде «можнго править»: `JAZZ-WEAPON-R4-001-AC-VISUAL-027` — PASS static/offline: RGB metal mask ×0.88 у JAZZ_VektorR4_3_Base.dds и fallback; дерево вне маски сохранено до сжатия, RM/Normal/меш не менялись. Иконка переснята. BLOCKED runtime/editor/human. Сборка `jazz_weapon_feedback_20260927`: `compiled-report.json`, `components/component-report.json`, `install-manifest.json`, `installation.json`. В общей транзакции установлены 21 существующий файл, backup и SHA256 проверены; изменения jazz/jazz_assets незакоммичены. Допускается только удаление измеренных микрограней, которые становятся вырожденными в HGM; это не оптимизация видимой геометрии. Подробности — `docs/design/weapon-visual-feedback-20260927.md`.


- `JAZZ-WEAPON-R4-001-AC-001`: `PASS` — static/visual offline: `_build_r4_assets.py`, `_build_weapon_scale_overlay.py`, `_audit_compiled_weapon_mesh.py`. Удалены 14 нулевых/вырожденных граней, осталось 13509; custom normals отсутствуют. R4 1.005 м против АК74М 0.9418 м. Compiled HGM: те же 13509 граней, max vertex error 0.026 мм; два бока и 3/4 просмотрены, native карты корректно назначены; иконка 324x165. AssetsProcessor выдал стандартное несовпадение версий FBX/SDK, но завершил экспорт; геометрия проверена отдельно.
- `JAZZ-WEAPON-R4-001-AC-002`: `PASS` — static: `_check_r4.py` включая три RU/EN строки, Lua compile всех шести core-файлов, `_validate_items_quick.py` трёх пакетов, Legion static suite, docs/wiki checks. Канонический экспорт выполнен из одного снимка; добавлены только три новых ID, старые runtime CSV записи сохранены. У новых строк needs-russian/needs-english/collisions = 0; совпадают ID обоих языков. Полный старый каталог имеет посторонние collisions и не объявляется исправленным.
- `JAZZ-WEAPON-R4-001-AC-003`: `BLOCKED` — редактор/игра ещё не проверялись.

Исходный полный sync-аудит уже не проходил: jazz — 6241 errors / 1635 warnings; jazz_assets — 142 / 15; jazz-units — 81 / 0. Среди причин: legacy compact serialization, несопоставленные companion и временные backup-каталоги. Эти посторонние расхождения не исправлялись. Узкий R4-аудит отдельно проверяет значения всех полей items/companion, metadata, entity/MTL/DDS/fallback и ссылки лут-комбинаций.

Повторный Strict: jazz 6241 / 1635; jazz_assets 142 / 13; jazz-units 81 / 0; ошибок с VektorR4 нет. Общий gate остаётся красным из-за исходного состояния. Сравнение с backup: шесть core-файлов получили только вставки, без удаления прежних строк. Editor/runtime AC остаётся открытым, поэтому полный DoD не закрыт и статус accepted не выставлен.

Clone-aware localization Plan выполнен без Apply: ambiguous vanilla matches 0; существующие миграции не применялись. Три mod-only строки R4 используют диапазон `890000000019401..890000000019403`, проверенный на отсутствие конфликтов до вставки.

Отчёты и сохранённые сборки находятся во внешнем build-каталоге `Weapons/_r4_jazz_20260926`: `build-report.json`, `compiled-audit.json`, `scale/scale-overlay.json`, `integration-report.json`, `loot-report.json`, `validation-report.json`, PNG и `integration-backup/`. Абсолютные пути игры не включены в репозиторий.

## Documentation delta

- Обновлены `docs/technical/systems/weapons-ammo-components.md`, generated-file note в `file-coverage.md`, каталог `weapons.csv`, generated wiki README/assault-rifle, showcase RU/EN и таблица доступности Легиона. Везде отмечена ещё не выполненная игровая приёмка.

## Коррекция экспорта 27.09.2026

Запрос владельца: исправить исчезающие поверхности (скриншоты VZ58/R4), сделать материал мебели VZ58 спокойнее, проверить открытую игру. Прежняя offline проверка AC-001 не обнаруживала неверную сторону граней: её вывод о визуальной корректности не распространялся на backface culling.

- Исправлены совпадающие UV-швы и пересчёт наружу; открытым островам оставлена авторская сторона. Нет custom normals, изменения количества треугольников или position/UV пар.
- `PASS` offline: `_check_weapon_surface_uv.py`, донорский winding audit (расхождение менее 0.1% площади с учётом мелких ошибок самого OBJ), HGM surface + winding audit, native Blender previews. У VZ58 обновлены две atlas BaseColor и wood roughness floor 0.72.
- Существующие mesh/DDS и иконки установлены через `_refresh_weapon_surfaces.py`, с резервными копиями и сохранением всех имён/регистраций. Это ресурсное обновление; items/metadata/companion не переписывались.
- `BLOCKED` для повторной визуальной runtime-приёмки AC-003: DAP read-only probe подтвердил debug / ModEditor, но Computer Use был остановлен владельцем через Escape. К попытке штатного reload ресурсов порт 8165 уже возвращал ConnectionRefused; reload в игре не выполнен. На диске исправления установлены и будут загружены при следующем запуске. Не считать полным игровым PASS.

Повторный общий `_check_r4.py` остановился на ожидании `BurstShots=3`: текущее определение предмета уже не содержит этого явного поля. Визуальное исправление не редактировало items/companion; стороннее изменение сохранено. Отдельные surface/UV, recalc и compiled HGM winding gates прошли.

## Повторная игровая приёмка 2026-09-28

Решение владельца: approved; «дальше делай, вроде пока все».

- `JAZZ-WEAPON-R4-001-REQ-VISUAL-028` — Переместить VektorR4 в папку редактора к автоматам. Остаточную мятость проверить; владелец разрешил сохранить текущий улучшенный металл, если дальнейшее изменение не обосновано.
- `JAZZ-WEAPON-R4-001-AC-VISUAL-028` — адресные static/compiled проверки и сопоставление до/после; игровая приёмка и editor save/reload отдельно.

Evidence: `JAZZ-WEAPON-R4-001-AC-VISUAL-028`: `BLOCKED` — изменения ещё готовятся; runtime не подтверждён.

Установка 28.09.2026: 19 файлов в jazz/jazz_assets, SHA256 исходников/backup/установленных файлов проверены. PASS static: editor ancestry совпадает с AK47, полная запись ModItem семантически/текстово сохранена. Металл оставлен без дальнейшей коррекции по разрешению владельца. Полная сводка и ссылки — `docs/design/weapon-visual-feedback-20260927.md`. `AC-VISUAL-028`: static PASS; editor/runtime/human BLOCKED до новой приёмки владельца.
