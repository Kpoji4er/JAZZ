---
id: JAZZ-WEAPON-BATCH-IMPORT-001
status: implemented
owner: project-owner
systems:
  - weapon-assets
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - jazz/docs/specs/active/JAZZ-WEAPON-BATCH-IMPORT-001.md
  - jazz/docs/tools/_import_jaweapons_batch.py
  - jazz/docs/tools/_import_jaweapons_scene.py
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-plan-jaweapons.md
  - jazz/docs/design/weapons-import-batch-results.*
  - external/JaWeapons/Weapons/_batch_jazz_import/**
exclusive_resources:
  - external/JaWeapons/Weapons/_batch_jazz_import
related_decisions:
  - none
approved_by: project-owner (2026-09-23 check and import immediately)
---

# JAZZ-WEAPON-BATCH-IMPORT-001: пакетный офлайн-импорт исходников

## Проблема

51 исходник проверен на наличие карт. Три архива отклонены, четыре содержат OBJ без UV.
У большинства остальных OBJ нет usemtl/MTL. Список файлов не подтверждает пригодность модели.

## Цели

- Импортировать все неотклонённые источники в отдельные воспроизводимые Blender-сцены.
- Восстановить однозначные материалы из существующих карт, проверить UV и геометрию, создать превью.
- Отделить готовность исходника от установки игрового предмета и runtime-приёмки.

## Non-goals

- Этот контракт описывает входной этап общего запроса; регистрация предметов/модулей и entity требует последующей конкретной spec.
- Не генерировать отсутствующие материалы, не запускать JA3/Mod Editor, не откатывать существующее оружие.
- Не создавать дубли InventoryItem, не менять баланс и карты.

## Требования

- `JAZZ-WEAPON-BATCH-IMPORT-001-REQ-001` — обработать все 51 позиции аудита: три REJECT пропустить, остальные импортировать либо записать точную ошибку.
- `JAZZ-WEAPON-BATCH-IMPORT-001-REQ-002` — неизменяемые источники, отдельные каталоги и SHA256; не исполнять скрипты из blend/архивов.
- `JAZZ-WEAPON-BATCH-IMPORT-001-REQ-003` — не придумывать назначения неоднозначных карт; сохранять нативные либо однозначные назначения, отсутствующие помечать.
- `JAZZ-WEAPON-BATCH-IMPORT-001-REQ-004` — пересчитать нормали общим helper без сварки разных деталей; фиксировать дефекты, отсутствие UV и материалов в JSON.
  При подготовке удаляются только треугольники, которые не проходят существующий gate degenerate/zero_normal; число удалённых граней записывается. Spikes, отсутствующие UV и неоднозначные материалы автоматически не исправляются.
- `JAZZ-WEAPON-BATCH-IMPORT-001-REQ-005` — сохранить clean blend, три вида и сводку; записать отдельные решения по четырём спорным комплектам.

## Инварианты и ограничения

- REJECT источники не импортировать. Подготовленные ранее Hatchet/AK103 не удалять.
- Сохранять исходные координаты до модельного этапа; не выдавать их за игровой масштаб.
- Перепривязка нескольких текстурных наборов требует осмотра; magenta означает отсутствующий материал, не финальную текстуру.

## Acceptance criteria

- `JAZZ-WEAPON-BATCH-IMPORT-001-AC-001` — static: итог содержит ровно 51 исходник, ошибки не скрыты, исходные SHA256 совпадают.
- `JAZZ-WEAPON-BATCH-IMPORT-001-AC-002` — offline: успешные импорты имеют clean blend и три PNG, материал/UV/геометрия отражены по каждому объекту.
- `JAZZ-WEAPON-BATCH-IMPORT-001-AC-003` — offline visual: спорные комплекты осмотрены, решение и ограничения записаны; очередь различает импорт в Blender и игровой импорт.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ, saves/network: без runtime-изменений.
- Generated data и cross-package references не меняются на входном этапе.
- Rollback/recovery: изолированные производные файлы, повторное выполнение по SHA256.

## План и ownership

- jazz владеет tooling/spec/report; сцены хранятся вне модов.
- Исполнитель: Codex; reviewer: владелец на последующей визуальной приёмке.
- Declared write set / exclusive resources перечислены выше.

## Решение владельца

- Approved: «проверяй где есть материалы. Где нет — reject», «делай все сразу», «проверь и импортируй сразу».
- Дата: 2026-09-23. Запрет запуска игры сохраняется.
- Ограничение старой очереди «один ствол = один чат» отменено для этого пакетного прохода прямым запросом владельца.

## Evidence

- `JAZZ-WEAPON-BATCH-IMPORT-001-AC-001`: PASS static — `docs/design/weapons-import-batch-results.json` содержит все 51 источника. 48 источников проходили импорт/диагностику; SHA256 в source-state совпал до и после. Три исходных REJECT не извлекались. M240: Blender сообщает FBX 6100 unsupported; эта ошибка сохранена, источник также дубль MG58.
- `JAZZ-WEAPON-BATCH-IMPORT-001-AC-002`: PASS offline — 47 clean-сцен сохранены и повторно открыты, для каждой три PNG и пообъектный JSON. Из них Mk12 оставлен только для диагностики; остальные 46 = 28 IMPORTED_SOURCE + 18 IMPORTED_REVIEW. `custom_normals=false`, незакрытые дефекты сохранены в отчётах. `_check_mesh_export_normals.py`: OK.
- `JAZZ-WEAPON-BATCH-IMPORT-001-AC-003`: PASS offline visual — осмотрены четыре contact sheets всех импортов и повторные превью PPK/Kiparis/Kedr-B. Для каждого спорного комплекта созданы шесть видов no-UV/изоляции, осмотрены характерные проекции изолированных деталей и общий вид Mk12. Mk12 отклонён: без UV основная часть оружия. Kedr-B model_2 — отдельная внутренняя/вспомогательная геометрия; HK416 model_17 — круглая деталь аксессуара; SCAR model_39 — узкая плоская полоска. Последние три не приняты к игровому экспорту, замечания записаны в batch-results.

Выполнен только входной офлайн-этап. Entity/InventoryItem в активные пакеты не установлены; независимое ревью владельцем и игровая приёмка не выполнялись. Статус accepted не установлен.

## Documentation delta

Очередь, batch-results и README tools. Technical/wiki не меняются до фактического подключения runtime.
