---
id: JAZZ-AI-ACT-002
status: implemented
owner: project-owner
systems: [tactical-ai]
repositories: [jazz]
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-ACT-002.md
  - jazz/Code/AiActions.lua
  - jazz/Code/AIContextProfiles.lua
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/tactical-ai-roles-playtest.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/metadata.lua
exclusive_resources: [none]
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-ACT-001.md
approved_by: project-owner
---

# JAZZ-AI-ACT-002: Smoke curtain on exit corner / post-turn self-cover

## Проблема

Smoke signature scoring (`enemy −100`, `team +100`, `self +1000`) и ACT-001 proxy (юниты *в* облаке) толкают ИИ накрывать своих шапкой. В JAZZ дым режет vision (−70 на линии) и превращает выстрелы сквозь облако в незначительные попадания — ослепление своих до хода вредно. Нужна доктрина: занавес на угол выхода под вражеский OW; прямо на своих — только после их хода.

## Цели

- Smoke target points и score предпочитают **curtain** на отрезке вражеский OW → planned exit союзника.
- Прямое накрытие союзника разрешено только если союзник **уже сходил** в этом combat turn.
- Team ephemeral: кто уже сходил (`JazzAI_TeamActed`), planned `ai_destination`, `g_Overwatch`.
- Не кидать дым «в пустоту» и не окутывать ещё не ходивших стрелков.

## Non-goals

- Новые гранаты / archetype BiasId rename.
- Полный pre-think dest для всей команды до первого хода.
- Tear/toxic doctrine.
- Player-merc smoke UI.

## Требования

- `JAZZ-AI-ACT-002-REQ-001` — при `AllowedAoeTypes.smoke` кандидаты точек включают midpoints / точки у planned exit на линиях `OW origin → ally exit` (ally exit = `ai_destination` или мягкий offset к угрозе).
- `JAZZ-AI-ACT-002-REQ-002` — smoke zone score: большой bonus если `target_pos` лежит у отрезка OW→exit; штраф за союзников **без** acted в зоне; bonus за acted-союзников в зоне (self-cover); штраф за врагов в зоне.
- `JAZZ-AI-ACT-002-REQ-003` — `JazzAI_TeamActed` отмечается после `AIPlayAttacks`; сбрасывается на `CombatStart` и при смене `g_Combat.current_turn`.
- `JAZZ-AI-ACT-002-REQ-004` — ACT-001 weak in-zone +40/+20 proxy для smoke заменяется curtain/post-turn logic (не дублировать).

## Инварианты и ограничения

- Determinism; no new RNG in smoke path.
- Non-smoke `AIActionThrowGrenade` (frag/molotov/…) scoring unchanged.
- MapVars cleared on CombatStart; turn table keyed to `current_turn`.
- Friendly-fire / AP / MaxDist / MinDist presets respected.

## Acceptance criteria

- `JAZZ-AI-ACT-002-AC-001` — static: curtain collect + score helpers + TeamActed mark/reset present; smoke eval path no longer uses ACT-001 +40/+20-only proxy.
- `JAZZ-AI-ACT-002-AC-002` — runtime/human: S1 — дым на угол/LOS под OW при выходе союзника; S2 — шапка на своих только после их хода; S3 — не ослепляет ещё не ходивших своих без curtain-причины.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides `AIActionThrowGrenade` smoke precalc/eval and wraps `AIPlayAttacks` mark; no CLib symbol conflict beyond existing AiActions.
- Saves: ephemeral MapVars only.
- Network/determinism: no InteractionRand in new path.
- Generated data: none (archetype presets unchanged).
- Cross-package: reads `g_Overwatch`, ally `ai_context.ai_destination` from units package runtime.
- Rollback: revert Code + docs + metadata minor.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: see frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (chat 2026-07-30: curtain on exit corner; on allies only after their turn; team intent context)
- Дата: 2026-07-30

## Evidence

- `JAZZ-AI-ACT-002-AC-001`: `PASS` (static) — `JazzAI_CollectSmokeCurtainTargets` / `JazzAI_ScoreSmokeZone` / `JazzAI_EnsureSmokeZones` in `Code/AiActions.lua`; `JazzAI_TeamActed` mark/reset in `Code/AIContextProfiles.lua`; ACT-001 +40/+20 smoke proxy removed from `AIEvalZones`.
- `JAZZ-AI-ACT-002-AC-002`: `BLOCKED` — runtime/human playtest S1–S3

## Documentation delta

- `docs/design/tactical-ai-archetypes.md` §8 updated to ACT-002 doctrine
- `docs/design/tactical-ai-roles-playtest.md` ACT-002 smokes
- `docs/technical/systems/ai-awareness.md` smoke current-state
