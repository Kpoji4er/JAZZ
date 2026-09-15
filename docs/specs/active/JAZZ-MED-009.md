---
id: JAZZ-MED-009
status: approved
owner: project-owner
systems:
  - armor-damage-wounds-will
repositories:
  - jazz
risk: low
generated_data: false
runtime_validation: required
write_set:
  - Code/System_Wounds_OperationHeal.lua
  - docs/specs/active/JAZZ-MED-009.md
  - docs/specs/active/JAZZ-FEEDBACK-001.md
  - docs/tools/_check_hospital_eligibility.py
  - docs/tools/README.md
  - docs/technical/systems/armor-damage-wounds-will.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-MED-009: госпитализация при травмах без Wounded

## Проблема

На gosp пользователь подтвердил пустой выбор пациентов. Vanilla HospitalTreatment.FilterAvailable требует Wounded, который отключён в JAZZ.

## Цели

Госпиталь принимает живых пациентов с нехваткой HP или нелеченной травмой.

## Non-goals

Мгновенное снятие травм, изменение цен, скорости, лояльности и числа мест.

## Требования

- `JAZZ-MED-009-REQ-001` — HospitalTreatment использует JazzUnitNeedsTreatWounds для выбора пациентов; установка при DataLoaded и ModsReloaded независимо от наличия TreatWounds.

## Инварианты и ограничения

Существующие IsEnabled, стоимость, слоты и Tick госпиталя сохраняются. Травма переводится в заживление существующим PatientAddHealWoundProgress, не удаляется мгновенно. Новых globals и T-ID нет.

## Acceptance criteria

- `JAZZ-MED-009-AC-001` — Lua harness: травма без Wounded и недостающее HP допускаются; здоровый, мёртвый и уже заживающая травма при полном HP исключаются; повторная установка безопасна, штатные callbacks сохранены, прогресс переводит травму в заживление.
- `JAZZ-MED-009-AC-002` — в живой игре gosp позволяет назначить пациента и начать госпитализацию.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: переопределяется только фильтр штатного пресета.
- Saves: миграция не требуется.
- Network/determinism: детерминированный фильтр.
- Generated data: нет.
- Cross-package references: нет.
- Rollback/recovery: откат собственного изменения фильтра.

## План и ownership

- Пакет-владелец: jazz; исполнитель: текущий агент; reviewer: владелец.
- Declared write set: frontmatter.
- Exclusive resources: none.

## Решение владельца

- Статус: approved на основании разрешения автономно исправлять фидбек и сообщения о подтверждённом дефекте госпитализации.
- Кто подтвердил: project-owner.
- Дата: 2026-09-15.

## Evidence

- `JAZZ-MED-009-AC-001`: `PASS` — isolated Lua harness фильтра и прогресса лечения, 2026-09-15; не live runtime.
- `JAZZ-MED-009-AC-002`: `PASS` — human/runtime, 2026-09-15: пользователь после исправления подтвердил «госпиталь работает» в контексте проверки gosp. Подробный прогон полного восстановления травмы отдельно не заявлен.

## Documentation delta

Обновить technical и wiki/showcase медицинской системы с границей между выбором пациента и заживлением травмы.
