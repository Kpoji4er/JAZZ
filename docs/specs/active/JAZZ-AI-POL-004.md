---
id: JAZZ-AI-POL-004
status: approved
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-POL-004.md
  - jazz/Code/CombatAI.lua
  - jazz/scripts/test-ai-crowd-scoring.ps1
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/tactical-ai-roles-playtest.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/testing.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/metadata.lua
exclusive_resources:
  - jazz/Code/CombatAI.lua
  - jazz/metadata.lua
related_decisions:
  - JAZZ-AI-POL-003
approved_by: project-owner
---

# JAZZ-AI-POL-004: Casualty-aware anti-stack scoring

## Проблема

`JAZZ-AI-POL-003` запрещает двум AI резервировать один XYZ voxel и добавляет небольшой
фиксированный штраф за живого союзника рядом. Human evidence от 2026-08-06 показывает
последовательное накопление бойцов и трупов в одной выгодной горловине: погибший союзник
исключается из live-spacing, а authored `AIPolicyAvoidDeathZones` недостаточно силён по
сравнению с attack/cover score. Следующий AI снова выбирает ту же огневую точку.

## Цели

- Масштабировать crowd/casualty penalty относительно итогового destination score, а не
  полагаться только на фиксированный additive penalty.
- Учитывать текущие и запланированные позиции живых союзников, а также позиции союзных
  dead/downed/incapacitated units.
- Делать плотные casualty clusters существенно менее привлекательными, сохраняя soft
  fallback для единственного доступного прохода.
- Сохранить детерминизм AI и не вводить новое persistent save/network state.

## Non-goals

- Team-wide assignment всех destinations и формации отряда.
- Резервирование полного маршрута или соседних path voxels.
- Временная память fatal funnel, новые officer directives или принудительный smoke/overwatch.
- Массовое изменение generated AI archetypes в `jazz-units`.
- Карто- или сектор-специфичные BiasMarker/маркерные правки.

## Требования

- `JAZZ-AI-POL-004-REQ-001` — `JazzAI_CrowdDangerModifier(context, dest)` возвращает
  целый percentage modifier: старт 100; живой союзник даёт −60 при distance&lt;1 tile,
  −25 при distance&lt;2 и −10 при distance&lt;3; союзная casualty (dead/downed/incapacitated)
  даёт −45/−30/−15 в тех же диапазонах; каждая casualty после первой в радиусе 3 даёт
  дополнительный −10; итог ограничен диапазоном 25–100.
- `JAZZ-AI-POL-004-REQ-002` — для melee context (`EffectiveRange &lt;= 1` или keyword
  `Melee`) modifier имеет floor 55, чтобы не блокировать обязательный melee approach.
  **Healer/medic floor 55 superseded 2026-08-21 by JAZZ-AI-MED-002:** medic/`can_heal`
  returns crowd modifier 100 (ignore crowding).
- `JAZZ-AI-POL-004-REQ-003` — живой ally использует `ai_destination`, когда он задан,
  иначе snapshot `ally_pack_pos_stance`; casualty всегда использует фактический snapshot.
- `JAZZ-AI-POL-004-REQ-004` — modifier применяется один раз к положительному итоговому
  `AIScoreDest` после policies, sniper stay, bombard и BiasMarker; debug details содержат
  `CROWD/DANGER MOD`. Глобальный additive вызов `JazzAI_AllySpacingScore` из `AIScoreDest`
  удаляется, а explicit `AIPolicyAllySpacing` остаётся доступным для authored tuning.
- `JAZZ-AI-POL-004-REQ-005` — hard same-XYZ dibs из `JAZZ-AI-POL-003` сохраняется;
  casualty tiles не становятся hard-blocked.
- `JAZZ-AI-POL-004-REQ-006` — расчёт не использует RNG, `MapVar`/`GameVar`, unordered
  iteration или полный `MapGet`; он работает по стабильному `context.allies` snapshot.

## Инварианты и ограничения

- Не менять signatures `AICreateContext`, `AIBuildArchetypePaths`, `AIScoreDest` и
  `AIPolicyAllySpacing`.
- Не менять target selection, attack scoring, cover formulas, awareness и movement AP.
- Не менять `items.lua`, generated archetypes, public IDs или load order.
- Не делать трупы непроходимыми: одноклеточный маршрут должен оставаться доступным.
- Одинаковый save/seed/context должен давать одинаковый modifier и destination ordering.

## Acceptance criteria

- `JAZZ-AI-POL-004-AC-001` — static model: isolated=100; one adjacent live ally=75;
  two adjacent live allies=50; one same-voxel casualty=55; two same-voxel casualties=25;
  one adjacent casualty=70; dense melee floor=55. Healer/medic crowd exemption is MED-002.
- `JAZZ-AI-POL-004-AC-002` — static source: modifier интегрирован ровно один раз в конце
  `AIScoreDest`; прежний глобальный additive ally-spacing отсутствует; hard XYZ dibs сохранён.
- `JAZZ-AI-POL-004-AC-003` — static determinism: implementation не содержит RNG,
  persistent variables или map-wide enumeration; тестовый сценарий воспроизводим.
- `JAZZ-AI-POL-004-AC-004` — runtime/human: в воспроизводимой горловине ranged AI после
  одной casualty реже выбирает ту же/соседнюю клетку, после двух casualties предпочитает
  безопасную destination/hold при наличии альтернативы; при единственном проходе не теряет
  возможность двигаться; melee и medic сохраняют подход.
- `JAZZ-AI-POL-004-AC-005` — documentation/generated/static checks проходят без новых
  diagnostics в declared write set.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ уже полностью заменяет vanilla `AIScoreDest`; CommonLib
  main `f023a0310e8e3c4dd2a8e5769fdb4ab09fd696ce` не определяет `AIScoreDest`,
  `AIBuildArchetypePaths` или `AIPolicyAvoidDeathZones`.
- Saves: новое состояние не добавляется; существующие tactical saves используют расчёт
  после загрузки нового кода.
- Network/determinism: RNG и persistent state не добавляются; входы берутся из
  детерминированного context snapshot.
- Generated data: не меняется; `metadata.lua` получает только обязательный Revision bump
  и append `last_changes` при коммите.
- Cross-package references: отсутствуют; `jazz-units` authored policies остаются совместимы.
- Rollback/recovery: удалить helper и единственный вызов modifier; вернуть глобальный
  additive ally-spacing call.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: Codex.
- Reviewer: project-owner по runtime/human evidence.
- Declared write set: только пути из front matter.
- Exclusive resources: `Code/CombatAI.lua`, `metadata.lua`.

## Решение владельца

- Статус: approved.
- Кто подтвердил: project-owner в Codex task.
- Дата: 2026-08-06.

## Evidence

- `JAZZ-AI-POL-004-AC-001`: `PASS` — static/model: `scripts/test-ai-crowd-scoring.ps1`; `model=10`, normative values and role floors match.
- `JAZZ-AI-POL-004-AC-002`: `PASS` — static/source: one final modifier call after BiasMarker, legacy global additive call absent, hard same-XYZ dibs retained.
- `JAZZ-AI-POL-004-AC-003`: `PASS` — static/determinism: local top-level helper, ordered `context.allies` snapshot, no RNG, persistent variables or `MapGet`; shooting regression passed (`active_weapons=161`).
- `JAZZ-AI-POL-004-AC-004`: `BLOCKED` — runtime/human JA3 playtest required for one/two casualties, sole passage, melee and medic approach.
- `JAZZ-AI-POL-004-AC-005`: `BLOCKED` — profile tests and `git diff --check` pass; generated errors=0 but strict reports expected metadata/items timestamp warning without editor round-trip; full docs audit has pre-existing backlog and only one unchanged changed-file hit (`tactical-ai-archetypes.md:129` trailing spaces from `origin/main`).

## Documentation delta

- Current state: `docs/technical/systems/ai-awareness.md`, `docs/technical/testing.md`.
- Design/playtest: `docs/design/tactical-ai-archetypes.md`,
  `docs/design/tactical-ai-roles-playtest.md`.
- Player-facing: `docs/wiki/combat-and-accuracy.md`,
  `docs/showcase/ru/combat-and-accuracy.md`,
  `docs/showcase/en/combat-and-accuracy.md`.
