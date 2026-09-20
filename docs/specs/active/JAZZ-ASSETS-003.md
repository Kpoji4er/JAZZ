---
id: JAZZ-ASSETS-003
status: approved
owner: project-owner
systems:
  - assets-entities
  - generated-data-validation
repositories:
  - jazz
  - jazz_assets
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-ASSETS-003.md
  - jazz/docs/technical/systems/assets-entities.md
  - jazz/.agents/skills/export-jazz-character-element/**
  - jazz_assets/Sources/Character/**
  - jazz_assets/Entities/JazzHat_*.ent
  - jazz_assets/Entities/JazzHat_*.lua
  - jazz_assets/Entities/Meshes/**
  - jazz_assets/Entities/Materials/**
  - jazz_assets/Entities/Textures/**
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
exclusive_resources:
  - jazz_assets/items.lua
  - jazz_assets/metadata.lua
  - jazz_assets/Entities
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-ASSETS-003: собственные Character Elements через HG Blender Exporter (wave 1 — головной убор)

## Проблема

В `jazz_assets` нет ни одного собственного character element: все entity — оружие и его навесное. Одежда и головные уборы для юнитов JAZZ берутся из vanilla либо (по `JAZZ-APPEAR-001`) из чужих asset-паков, и этот spec явно вынес свои `CharacterHat`/`CharacterArmor` меши в non-goals wave 1. Пайплайн официального тулчейна при этом полностью доступен локально и ни разу не прогонялся: `ModTools/BlenderExport.py`, аддон `HG Blender Exporter` (установлен в Blender 4.1 / 4.4 / 5.2), `ModTools/AssetsProcessor/AssetsProcessor.exe`, риггнутые сэмплы `Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend` и `SampleFemaleModel/BlenderMOD_Apperance_Female.blend`, доки `ModItemEntity.md.html` и `ModItemAppearancePreset.md.html`.

Без проверенного end-to-end маршрута каждая попытка сделать свою одежду упирается в неизвестные: какой класс entity ставить, как наследовать анимации торса, где хранить исходный `.blend`, как переживает пересборку `mtlbin`.

## Цели

- Прогнать полный маршрут Blender → `.ent` → `Entities/` → `ModItemEntity` → dropdown `AppearancePreset` на одном простом элементе — каске СШ-68 для мужского рига (entity `JazzHat_SSh68`).
- Зафиксировать маршрут как воспроизводимый skill с headless-экспортом (`blender -b <scene>.blend -P <script>.py`), а не как последовательность кликов.
- Задать контракт хранения: исходные `.blend` и текстуры в `jazz_assets/Sources/Character/`, игровые артефакты в `jazz_assets/Entities/`.
- Закрепить именование entity с префиксом `JazzHat_*`, исключающее коллизию с vanilla и с Wardrobe-паками из `JAZZ-APPEAR-001`.

## Non-goals

- Женский вариант того же убора и любые `CharacterBody` / `CharacterPants` / `CharacterArmor` меши (следующие волны).
- Подключение убора к appearance мерков и юнитов `jazz-units`: wave 1 доказывает наличие entity в dropdown, не меняет ни один существующий `AppearancePreset`.
- Пересмотр `JAZZ-APPEAR-001`: soft-Wardrobe слой и Mod Option остаются как есть.
- Собственная анимация или state: шапка — жёсткий attach на спот Head, без `<inherit entity="Male">` и без `.hga`.
- Colorization-слоты и `ColorizationPropSet` на новом entity.
- Художественный high-poly: wave 1 — чистый low-poly блокаут с корректной топологией и UV, финальный арт-проход отдельно.

## Требования

- `JAZZ-ASSETS-003-REQ-001` — исходная сцена собирается на базе официального `SampleMaleModel/BlenderScene_Appearance.blend` (риг и пропорции vanilla) и сохраняется в `jazz_assets/Sources/Character/JazzHat_<Name>/`; сам сэмпл из установки игры не модифицируется.
- `JAZZ-ASSETS-003-REQ-002` — шапка экспортируется без `inherit_animation` (`None`); origin empty стоит в location кости `Bip001 Head` без её поворота. В `.ent` нет `<inherit entity="Male">`.
- `JAZZ-ASSETS-003-REQ-003` — вершины шапки в Head-local space (после parenting к origin на Head); skinned-веса и `hgskeleton` не используются.
- `JAZZ-ASSETS-003-REQ-004` — имя entity соответствует `JazzHat_<Name>`, `[A-Za-z0-9_]` без пробелов; entity не перекрывает ни один vanilla ID и ни один ID из asset-модов, перечисленных в `JAZZ-APPEAR-001`.
- `JAZZ-ASSETS-003-REQ-005` — `ModItemEntity` объявляет `class_parent = "CharacterHat"` (как vanilla `EquipmentBlood_Hat`, без суффикса Male/Female); это единственный класс, который попадает в dropdown Hat.
- `JAZZ-ASSETS-003-REQ-006` — текстуры новых элементов подчиняются контракту имён из `JAZZ-ASSETS-002`: `JazzHat_<Name>_Base.dds`, `_Norm`, `_RM`; numeric basenames запрещены.
- `JAZZ-ASSETS-003-REQ-007` — экспорт выполняется headless-скриптом без GUI Blender; скрипт принимает путь к `.blend`, имя entity и выходную папку, и завершается ненулевым кодом при ошибках валидации экспортёра.
- `JAZZ-ASSETS-003-REQ-008` — skill `export-jazz-character-element` документирует весь маршрут, включая прогон `AssetsProcessor` и пересборку `mtlbin` в Mod Editor владельцем; шаги, требующие Ged, помечены как human-шаги.

## Инварианты и ограничения

- Существующие entity `jazz_assets` (оружие и навесное) не трогаются: ни ID, ни материалы, ни текстуры.
- `BinAssets/*.mtlbin` не редактируется вручную; пересборка только через Mod Editor.
- Файлы в установке игры (`ModTools`, `Samples`) доступны только на чтение.
- Пакеты, зависящие от `jazz_assets` (`pDGDhr`), должны грузиться без изменений: новый entity аддитивен.
- Load order и save-формат не затрагиваются: appearance parts не назначаются ни одному юниту в wave 1.
- Агент не кликает в Mod Editor; импорт entity, rebuild `mtlbin` и визуальная приёмка — за владельцем.

## Acceptance criteria

- `JAZZ-ASSETS-003-AC-001` — после headless-экспорта в `jazz_assets/Entities/` присутствуют `JazzHat_<Name>.ent` и `JazzHat_<Name>.lua`, все ссылки `.ent` на mesh/material/текстуры разрешаются на диске (static).
- `JAZZ-ASSETS-003-AC-002` — `check-asset-integrity.ps1` проходит без новых ошибок относительно базы до изменения (static).
- `JAZZ-ASSETS-003-AC-003` — в Mod Editor entity виден в выпадающем списке Hat `AppearancePreset` (класс `CharacterHat`, без пола) (editor/human).
- `JAZZ-ASSETS-003-AC-004` — на тестовом юните убор отрисовывается, держится на голове в idle, ходьбе и беге, без missing texture и без assert в логе (runtime/human).
- `JAZZ-ASSETS-003-AC-005` — повторный запуск скрипта из исходного `.blend` даёт тот же набор файлов без ручных шагов между запусками (static).
- `JAZZ-ASSETS-003-AC-006` — skill содержит команду headless-экспорта, список human-шагов и критерии провала; сторонний исполнитель проходит маршрут по нему без обращения к этому spec (static/human).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: новый entity аддитивен, override нет; пересечения слоёв не возникает.
- Saves: appearance не назначается, save-контракт не меняется.
- Network/determinism: визуальный ассет, RNG и боевые расчёты не затрагиваются.
- Generated data: `items.lua` (новый `ModItemEntity`), `metadata.lua` (revision, `last_changes`), `Entities/**`, `mtlbin` после rebuild.
- Cross-package references: потребители `Mod/pDGDhr/...` не меняются; будущая привязка к мерцам пойдёт отдельным spec в `jazz-units`.
- Rollback: удалить `ModItemEntity` из `items.lua` и файлы `JazzHat_*`; на зависимые пакеты это не влияет.

## План и ownership

- Пакет-владелец: `jazz_assets` (entity, текстуры, `items.lua`); `jazz` (spec, skill, technical docs).
- Исполнитель: agent (скрипты, экспорт, Lua), owner (Mod Editor, визуальная приёмка).
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: `jazz_assets/items.lua`, `jazz_assets/metadata.lua`, `jazz_assets/Entities`.
- Волны: (1) головной убор male + skill → (2) женский вариант и второй слот (Body/Armor) → (3) привязка к appearance юнитов отдельным spec.

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner
- Дата: 2026-09-15
- Зафиксировано в обсуждении: класс `CharacterHat` (правка владельца, 2026-09-16); wave 1 — каска СШ-68, entity `JazzHat_SSh68`; HatSpot default = Head, поэтому origin на кости Head.

## Evidence

- `JAZZ-ASSETS-003-AC-001`: `PASS` (static) — `Entities/JazzHat_SSh68.ent` + `.lua`; `.ent` без `<inherit>`, state `idle`, bbox Z 4..20 см (Head-local); материал — `_Base` / `_Norm` / `_RM`; `class_parent = "CharacterHat"`.
- `JAZZ-ASSETS-003-AC-002`: `PASS` (static) — `check-asset-integrity.ps1`: `RESULT: PASSED`, registered=491, errors=0; все 19 warnings — унаследованный dormant-долг M60/PKM/G36/Chevy из `JAZZ-ASSETS-001/002`.
- `JAZZ-ASSETS-003-AC-003`: `BLOCKED` — требует Mod Editor у владельца (агент не видит Ged). Класс уже `CharacterHat` (правка владельца).
- `JAZZ-ASSETS-003-AC-004`: `BLOCKED` — требует прогона в игре у владельца после переэкспорта 2026-09-16 (Head-local, без inherit). Первая попытка с `inherit Male` и origin у ног дала каску на полроста выше головы и задом наперёд.
- `JAZZ-ASSETS-003-AC-005`: `PASS` (static) — повторный export после удаления `ExportedEntities/JazzHat_SSh68*` восстановил `.ent` / mesh / mtl; `Vertices: 827`, `Bones: 0`.
- `JAZZ-ASSETS-003-AC-006`: `PASS` (static) — skill различает skinned одежду и жёсткий `CharacterHat` (HatSpot=Head, origin на Head, +Y = лицо).

## Documentation delta

- `docs/technical/systems/assets-entities.md` — добавлен раздел «Character elements» (классы, наследование анимаций, `hgskeleton`, расположение исходников) и обновлён snapshot: 491 registered, 504 `.ent`, 1370 DDS, 523 `.mtl`, 517 `.hgm`.
- Новый skill `.agents/skills/export-jazz-character-element/` со ссылкой из `work-on-jazz-mod`.
- Player-facing документация не требуется: в wave 1 элемент не виден игроку.
