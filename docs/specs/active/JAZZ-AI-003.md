---
id: JAZZ-AI-003
status: implemented
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/AiActions.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/System_OR_Unit.lua
  - jazz/docs/specs/active/JAZZ-AI-003.md
  - jazz/docs/technical/systems/ai-awareness.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-AI-003: SameTarget / Пристрелка в AI score + sticky fire mode

## Проблема

`AIPrecalcDamageScore` добавляет только плоский `SameTarget.Bonus` и игнорирует `TakeAim` (Пристрелка) и `AccuracyBonusSameTarget` с обвеса. `PickBestAttack` на каждом Dump-step заново крутит top-K и часто меняет режим при том же AP/цели, хотя score dest уже предполагал пачку одного режима.

## Цели

- Approximate target score учитывает полный SameTarget-слой (preset + Пристрелка + same-target компоненты), когда `GetLastAttack() == target`.
- Внутри Dump по одной цели режим огня липкий: повторный выбор предпочитает прежний mode, если он всё ещё влезает в AP и score ≥ threshold от best.
- Исправить `Dualshot`/`DualShot` в basic modes.

## Non-goals

- Полный переход approximate score на `CalcChanceToHit` для всех модификаторов.
- Тюнинг `TargetBaseScore` / archetype MaxAttacks.
- Изменение SoftDumpCap / Disengage из `JAZZ-AI-002`.

## Требования

- `JAZZ-AI-003-REQ-001` — SameTarget в `AIPrecalcDamageScore`: `CalcValue` + `GatherCTHModifications("SameTarget")` (Пристрелка) + component gather для эффектов same-target на оружии, только при применимости к last attack.
- `JAZZ-AI-003-REQ-002` — Dump sticky: после первого basic `PickBestAttack` контекст помнит mode/action для текущей цели; следующие step предпочитают его при `score >= best * AIDecisionThreshold/100` и `cost <= AP`; смена цели сбрасывает sticky.
- `JAZZ-AI-003-REQ-003` — `GetBasicAttackModes` находит `DualShot` (и legacy `Dualshot`); `PickBestAttack` обрабатывает оба id как dual (shots=2).
- `JAZZ-AI-003-REQ-004` — только `InteractionRand` / существующий combat RNG; без `math.random`.

## Инварианты и ограничения

- Public ID / load order AI без изменений.
- Preferred-target lock и SoftDumpCap из `JAZZ-AI-002` сохраняются.
- Network hash: вызовы `NetUpdateHash` в precalc не ломать смыслом.

## Acceptance criteria

- `JAZZ-AI-003-AC-001` — static: SameTarget path использует CalcValue/Gather, не только ResolveValue Bonus.
- `JAZZ-AI-003-AC-002` — static: sticky mode fields + reset on target change в Dump/`PickBestAttack`.
- `JAZZ-AI-003-AC-003` — static: DualShot id covered in modes + PickBestAttack.
- `JAZZ-AI-003-AC-004` — interim smoke (owner): вражеский ход без crash/Lua error; полноценный регресс targeting/режимов — later. Full: юнит с TakeAim / повтор по той же цели не недооценивает её vs fresh target; второй Dump-shot чаще сохраняет режим при достаточном AP.
- `JAZZ-AI-003-AC-005` — docs: `ai-awareness.md` отмечает SameTarget/sticky.

## Impact и совместимость

- Vanilla/CLib/JAZZ: только JAZZ overrides `AIPrecalcDamageScore` / `PickBestAttack` / `GetBasicAttackModes`.
- Saves: нет новой схемы.
- Network: AI outcomes могут чуть стабилизироваться; RNG path остаётся InteractionRand.
- Generated data: нет.
- Rollback: revert write set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (SsAnd) — verbal go-ahead «сможешь?» после разбора PickBestAttack/пристрелки
- Дата: 2026-07-30

## Evidence

- `JAZZ-AI-003-AC-001`: `PASS` — static: `AICalcSameTargetScoreBonus` uses SameTarget `CalcValue` + `GatherCTHModifications` + `AccuracyBonusSameTarget` components; wired in `AIPrecalcDamageScore`.
- `JAZZ-AI-003-AC-002`: `PASS` — static: `dump_attack_mode` / `dump_attack_target` in `AIPlayAttacks`; `PickBestAttack(..., preferred_mode)` sticky ≥ `AIDecisionThreshold`.
- `JAZZ-AI-003-AC-003`: `PASS` — static: `DualShot`/`Dualshot` in `GetBasicAttackModes` and `PickBestAttack`.
- `JAZZ-AI-003-AC-004`: `PASS` — smoke (owner 2026-07-30): вражеский ход без crash; полный регресс режимов/SameTarget later.
- `JAZZ-AI-003-AC-005`: `PASS` — static: `ai-awareness.md` SameTarget/sticky note.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — SameTarget/Пристрелка в precalc + sticky fire mode в Dump.
