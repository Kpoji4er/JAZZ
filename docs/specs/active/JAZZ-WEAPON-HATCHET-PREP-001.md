---
id: JAZZ-WEAPON-HATCHET-PREP-001
status: implemented
owner: project-owner
systems:
  - weapon-assets
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: not-required
write_set:
  - jazz/docs/specs/active/JAZZ-WEAPON-HATCHET-PREP-001.md
  - jazz/docs/tools/_prepare_hatchet_source.py
  - jazz/docs/tools/README.md
  - jazz/docs/design/weapons-import-plan-jaweapons.md
  - external/JaWeapons/Weapons/_hatchet_jazz_build/**
exclusive_resources:
  - external/JaWeapons/Weapons/_hatchet_jazz_build
related_decisions:
  - none
approved_by: project-owner (2026-09-23 request to begin weapons list)
---

# JAZZ-WEAPON-HATCHET-PREP-001: подготовка исходника топора

## Проблема

Пункт A5 очереди ещё не подготовлен. Архив содержит два OBJ без текстур и MTL;
перед игровым импортом нужно установить состав геометрии и получить проверяемую сцену.

## Цели

- Выполнить первый законченный офлайн-этап одного оружия из списка.
- Сохранить воспроизводимую clean-сцену и диагностические виды.

## Non-goals

- Игровая интеграция, новый InventoryItem, баланс, иконка и экспорт HGM.
- Изготовление отсутствующих текстур, патронов .380 ACP и работа над другими стволами.

## Требования

- `JAZZ-WEAPON-HATCHET-PREP-001-REQ-001` — исходный ZIP неизменен; извлечь копию в отдельный build-каталог, сохранить SHA256 и состав архива.
- `JAZZ-WEAPON-HATCHET-PREP-001-REQ-002` — сохранить геометрию и UV, пересчитать нормали общим helper, сохранить clean blend и отчёт по каждому мешу; не выдавать отсутствие текстур за готовый материал.
- `JAZZ-WEAPON-HATCHET-PREP-001-REQ-003` — получить три ортографических вида, отметить остаток работы в очереди; не запускать JA3.

## Инварианты и ограничения

- Исходный масштаб не интерпретировать как метры без проверки. На этом этапе сохранить исходные координаты.
- Не сваривать разные детали; не менять существующие dirty-файлы за пределами write set.
- Generated data и игровые пакеты остаются вне этого этапа.

## Acceptance criteria

- `JAZZ-WEAPON-HATCHET-PREP-001-AC-001` — static: SHA256 архива до и после совпадает; источник, меши, UV и отсутствие текстур отражены в JSON.
- `JAZZ-WEAPON-HATCHET-PREP-001-AC-002` — static: clean blend повторно открывается; нет custom normals, результат аудита треугольников записан без скрытия дефектов.
- `JAZZ-WEAPON-HATCHET-PREP-001-AC-003` — offline visual: три PNG созданы, геометрия осмотрена; очередь различает подготовку исходника и игровой импорт.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ, saves, network: runtime не меняется.
- Generated data: не меняются.
- Cross-package references: отсутствуют.
- Rollback/recovery: внешняя сцена производная, повторно собирается скриптом из исходного архива.

## План и ownership

- Пакет-владелец tooling: jazz; производные исходники: внешний build-каталог.
- Исполнитель: Codex. Reviewer: последующая проверка владельцем перед интеграцией.
- Declared write set и exclusive resources перечислены выше.
- Подготовить копию, clean blend, аудит и виды, затем зафиксировать результат.

## Решение владельца

- Статус: approved для первого офлайн-этапа списка.
- Кто подтвердил: владелец в текущем разговоре — «потихоньку начинай его делать».
- Дата: 2026-09-23. Дополнительное ограничение: «игру не запускай».

## Evidence

- `JAZZ-WEAPON-HATCHET-PREP-001-AC-001`: PASS static — `Weapons/_hatchet_jazz_build/prepare-report.json`: SHA256 `c6a3e1264c7fd9f9e3aac7dfbd7918af26e7c758b38c995eb3dca89e928a7375` до и после совпадает. Два OBJ, без MTL/текстур, оба с UVMap. Голова 780 треугольников, рукоять 5404.
- `JAZZ-WEAPON-HATCHET-PREP-001-AC-002`: PASS static — Blender 4.2.14 сохранил и повторно открыл `clean/Hatchet.blend`; оба mesh_audit пусты, custom_normals=false. `_check_mesh_export_normals.py`: OK. Исходные координаты сохранены, игровой масштаб не назначен.
- `JAZZ-WEAPON-HATCHET-PREP-001-AC-003`: PASS offline visual — осмотрены `review/Hatchet_axis_x.png`, `Hatchet_axis_y.png`, `Hatchet_axis_z.png`: голова и рукоять образуют один топор. На голове заметны переходы гладкого затенения; это не финальный материал. Очередь дополнена статусом подготовки. JA3 не запускалась.

Независимое ревью владельцем ещё не выполнено; статус accepted не установлен.

Последующее решение владельца 2026-09-23: «Где нет [материалов] — reject».
Архив Hatchet отклонён для дальнейшего импорта. Завершённая подготовка остаётся
доказательством проверки исходника, но не основанием изготавливать отсутствующие материалы.

## Documentation delta

Обновить очередь и README инструментов. Technical/wiki/showcase не меняются: новое оружие в runtime ещё не подключено.
