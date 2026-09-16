---
id: JAZZ-CI-SPEC-001
status: approved
owner: project-owner
systems:
  - tooling
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: not-required
write_set:
  - .github/workflows/quality-gates.yml
  - docs/specs/active/JAZZ-CI-SPEC-001.md
  - docs/technical/testing.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-CI-SPEC-001: рекомендательная проверка спецификаций

## Проблема

Полный аудит спецификаций блокирует выпуск из-за частично выполненной игровой проверки. Владелец потребовал сделать эту проверку необязательной.

## Цели

Сохранить диагностику, исключив её из обязательных CI-проверок.

## Non-goals

Не отключать проверки документации, generated data, синтаксиса, архивов и контрольных сумм.

## Требования

- `JAZZ-CI-SPEC-001-REQ-001` — только шаг Validate change specifications имеет continue-on-error; при failure создаётся warning и запись в summary.

## Инварианты и ограничения

Phase All и валидатор не меняются. Прочие шаги не получают continue-on-error. Непроверенные AC не становятся PASS.

## Acceptance criteria

- `JAZZ-CI-SPEC-001-AC-001` — YAML содержит advisory только для specifications; failure публикуется в summary.

## Impact и совместимость

Только CI; runtime, saves, metadata и версия пакета не меняются. Rollback — убрать continue-on-error и отчётный шаг.

## План и ownership

Текущий агент, jazz. Правка workflow и технической документации.

## Решение владельца

approved: project-owner, 2026-09-16: «зафорси релиз ... эту проверку надо сделать не обязательной». Это также разрешение выпуска текущего кандидата при известных незакрытых пунктах.

## Evidence

- `JAZZ-CI-SPEC-001-AC-001`: PASS — static: единственный continue-on-error на шаге specifications, сообщение по outcome=failure.

## Documentation delta

В docs/technical/testing.md отражён рекомендательный статус CI-аудита спецификаций.
