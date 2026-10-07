---
id: JAZZ-MERC-MERGE-001
status: implemented
owner: project-owner
systems:
  - units-progression-specializations
  - localization
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - ../jazz-units/items.lua
  - ../jazz-units/metadata.lua
  - ../jazz-units/UnitData/*.lua
  - ../jazz-units/Russian.csv
  - ../jazz-units/English.csv
  - Localization/*.csv
  - Russian.csv
  - English.csv
  - metadata.lua
  - docs/tools/_merge_merc_archive*
  - docs/tools/README.md
  - docs/specs/active/JAZZ-MERC-MERGE-001.md
  - docs/technical/systems/units-progression-specializations.md
  - docs/wiki/merc-recruiting-center.md
  - docs/showcase/ru/mercenaries.md
  - docs/showcase/en/mercenaries.md
exclusive_resources:
  - jazz-units/items.lua
  - mercenary profile localization IDs
approved_by: project-owner, explicit request 2026-10-07
---

# JAZZ-MERC-MERGE-001: выборочное слияние анкет из jazz-units.rar

## Проблема

Владелец предоставил jazz-units.rar и запросил перенос имён, описаний/биографий,
статов, классов и цен только наёмников с исправлением строк.

## Цели

Перенести смысловые отличия анкет, сохранив текущий комплект и двуязычность.

## Non-goals

NPC, перки, снаряжение, внешность, диалоги найма, AI, фракции и load order;
полная замена архива, mass regeneration, push.

## Требования

- JAZZ-MERC-MERGE-001-REQ-001 — сопоставить существующие IsMercenary по стабильному ID;
  перенести профильные тексты, характеристики, StartingLevel, Specialization, Tier
  и денежные поля. Пропуски сериализатора трактовать по подтверждённым defaults.
- JAZZ-MERC-MERGE-001-REQ-002 — синхронно менять items.lua и companions;
  сохранить существующие локализационные ID, кроме реальных vanilla-коллизий.
- JAZZ-MERC-MERGE-001-REQ-003 — исправить строки, сохранить vanilla English source
  для эквивалентных переводов; изменённые mod-only строки завершить RU+EN.

## Инварианты и ограничения

Другие поля и не-наёмники сохраняются. Архив используется только как данные.
Изменения текста не переносят структуру чат-условий. Maps/ не сканируется.

## Acceptance criteria

- JAZZ-MERC-MERGE-001-AC-001 — static: ограниченный diff и повторный merge без изменений.
- JAZZ-MERC-MERGE-001-AC-002 — static: структурная валидность и generated sync без новых ошибок.
- JAZZ-MERC-MERGE-001-AC-003 — static: изменённые строки полны на RU/EN и не имеют коллизий.
- JAZZ-MERC-MERGE-001-AC-004 — editor/runtime: чистый load/save/reload и проверка анкет.

## Impact и совместимость

Vanilla/CommonLib API не меняются. Данные существующих наёмников в save могут
сохранить старые статы; миграции сохранений нет. RNG/network не меняются.
Generated transaction: items.lua + существующие UnitData; load graph прежний.
При запрошенном коммите metadata обоих пакетов получает только Revision +1 и
буллет last_changes. Локализация принадлежит jazz с синхронизацией таблиц jazz-units.
Rollback: выборочный Git diff/revert. Изменения фиксируются связанными локальными
коммитами jazz-units (данные) и jazz (локализация, tooling, документация).
Данные jazz-units: `be62c3ced9dcdbb50f2cb29c5471e799a75c7929`.

## План и ownership

Пакет-владелец: jazz-units. Исполнитель: Codex. Reviewer: владелец проекта.
Declared write set и exclusive resources указаны выше.

## Решение владельца

Подтверждено владельцем 2026-10-07 прямым запросом на слияние из архива.
2026-10-08 владелец дополнительно поручил закоммитить завершённое слияние.

## Evidence

- JAZZ-MERC-MERGE-001-AC-001: PASS — static: `_merge_merc_archive_check.py --data-only`;
  70 полей / 43 наёмника, companions совпадают, прочие поля и объекты сохранены.
  Повторный merge: 0 полей, 0 наёмников. План: 41 Title, 15 Email, Bio Волка,
  три поля имени Хряпа, 7 StartingLevel, 2 Agility, 1 Dexterity.
  Дополнительная локализация исправляет старые runtime overrides: всего 164 ID
  у 50 наёмников, включая 48 Bio. Их исходники уже совпадали с архивом в Lua,
  но CSV подменял многие из них техническими описаниями со статами.
- JAZZ-MERC-MERGE-001-AC-002: PASS — static: `_validate_items_quick.py ../jazz-units`,
  strict generated sync (0 errors, 0 warnings), компиляция 44 Lua через lupa,
  AME copy audit (60 RU/EN анкет), локальная документация (5 Markdown).
- JAZZ-MERC-MERGE-001-AC-003: PASS — static: канонический парный экспорт и
  `_merge_merc_archive_check.py`; 164 одинаковых ID RU/EN, все переводы заполнены,
  нет коллизий выбранных ID; источники совпадают с items/companions. Посторонние
  CSV-записи сохранены. Центральные runtime CSV: по 11532 строки.
- JAZZ-MERC-MERGE-001-AC-004: BLOCKED — editor/runtime round-trip не проводился.

Clone-aware Plan выполнен до назначения новых ID. Для четырёх изменённых
vanilla-текстов он определил `assign-mod-id`; неоднозначностей этих строк нет.
Общий план имеет 15 посторонних ambiguities (карты, подсказки, роли); глобальный
Apply не выполнялся. Выбран свободный диапазон 890000000020601–890000000020604.
Исходный общий аудит: 15411 active IDs, 12175 catalog rows,
needs-russian=102, needs-english=25, active collisions=0, game collisions=607,
Russian CSV collisions=0, dormant conflicts=1571. Это исходный долг вне scope,
не результат текущего слияния; временные копии включены аудитором в dormant.

После полного экспорта: 12179 catalog rows, needs-russian=102, needs-english=23;
общие collision counts не изменились. После commit Revision bump generated sync
имеет 0 errors и один ожидаемый mtime warning (`metadata.lua` новее `items.lua`);
до bump строгий аудит проходил без warnings. Финально компилируются все 45
изменённых Lua пакета units. Revision: jazz 6249, jazz-units 2341; major/minor
и производные saved/code_hash не менялись. Editor/runtime AC остаётся открытым,
поэтому полный DoD/релизная приёмка не заявляются.

## Documentation delta

Профильная technical-страница, wiki и showcase RU/EN фиксируют фактическое слияние
и границу static/editor evidence. Asset contract не меняется.
