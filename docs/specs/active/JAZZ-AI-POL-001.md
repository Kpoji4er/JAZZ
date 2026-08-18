---
id: JAZZ-AI-POL-001
status: approved
owner: project-owner
systems:
  - tactical-ai
  - jazz-units-archetypes
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-POL-001.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/tactical-ai-roles-playtest.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/Code/AIPolicy.lua
  - jazz-units/items.lua
exclusive_resources:
  - jazz-units/items.lua
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-PERF-001.md
approved_by: project-owner
---

# JAZZ-AI-POL-001: TakeCover threat-weight, Proximity ScoreMode, role Weight rebalance

## Проблема

Cover почти не читается в бою: `AIPolicyTakeCover` усредняет по всем видимым врагам при низком Weight против `DealDamage`; `AIPolicyProximity` возвращает дистанцию (больше = дальше) при комментарии «ближе лучше», из‑за чего ally-кластеры разъезжаются. Три боевые роли (Frontliner / Assaulter / Flanker) не различаются по cover/proximity.

Design source: `docs/design/tactical-ai-archetypes.md` §4.1, §4.3, план POL-001.

## Цели

- Threat-weighted cover + cover×shot composite в `AIPolicyTakeCover:EvalDest`.
- Явный `ScoreMode = closer_better | farther_better` у `AIPolicyProximity` (default `farther_better` = текущая математика).
- Weight rebalance TakeCover/Proximity на `Legion_*` и `Rebels_*` Frontliner / Assaulter / Flanker.
- Ally Proximity на этих шести archetype → `closer_better`.

## Non-goals

- `AIPolicyAllyRoleAnchor` / AvoidPeekVoxel (POL-002).
- Shared PickCustom / panic / melee AP (ROLE-002).
- LowVis multipliers, flare/OW gates (CTX-001).
- Officer aura (CMD-001), medic freeze (MED-001), smoke LOS-break (ACT-001).
- Adonis/Army/Thug archetype Weight pass.
- Смена public archetype ID.

## Требования

- `JAZZ-AI-POL-001-REQ-001` — `AIPolicyTakeCover:EvalDest` считает weighted average по threat (дистанция, `IsThreatened`, best-attack target), не простой average; coverage &lt;30 по-прежнему штрафуется.
- `JAZZ-AI-POL-001-REQ-002` — cover score умножается на shot factor `0.5 + 0.5 * can_shot`, где `can_shot` из `dest_target_score`/`dest_target` либо fallback «видимый враг в EffectiveRange».
- `JAZZ-AI-POL-001-REQ-003` — `AppendClass.AIPolicyProximity` добавляет `ScoreMode`; `closer_better` → utility `1000/(1+dist_score)`; `farther_better` → текущий return distance; omitted → `farther_better`.
- `JAZZ-AI-POL-001-REQ-004` — OptLoc TakeCover authored weights (locked live, owner 2026-08-18): Frontliner **20** (`visibility_mode=team`) **+ 40** (unscoped); Assaulter **10** (team); Flanker **15** (team), `OptLocSearchRadius` **55**. Flank-branch EndTurn TakeCover ≤10 (live Weight **1**). High 80–150 / 20–40 band superseded: dest-cap 200 + TakeCover enemy cap 8 made large TakeCover vs DealDamage noisy/expensive (PERF-001 REQ-007/008), not a forgotten rebalance.
- `JAZZ-AI-POL-001-REQ-005` — на шести faction templates ally `AIPolicyProximity` получают `ScoreMode = "closer_better"`.
- `JAZZ-AI-POL-001-REQ-006` — без нового RNG; существующие PlaceObj без ScoreMode сохраняют прежнюю Proximity-математику.

## Инварианты и ограничения

- Не `UndefineClass` TakeCover/Proximity — только `AppendClass` + EvalDest.
- Determinism: только целочисленная/`MulDivRound` арифметика.
- GuardArea и прочие archetype вне write set не обязаны менять Weights.
- Editor PlaceObj с неизвестным ScoreMode не ломается (default).

## Acceptance criteria

- `JAZZ-AI-POL-001-AC-001` — static: `AIPolicy.lua` содержит threat-weight + cover×shot и `ScoreMode` ветки.
- `JAZZ-AI-POL-001-AC-002` — static: шесть Id (`Legion_`/`Rebels_` × Frontliner/Assaulter/Flanker) — OptLoc TakeCover Weights = live REQ-004; ally Proximity с `closer_better`.
- `JAZZ-AI-POL-001-AC-003` — docs: `ai-awareness.md` описывает threat-weight, ScoreMode, role Weights.
- `JAZZ-AI-POL-001-AC-004` — runtime/human: Frontliner чаще остаётся в cover vs visible shooter; Assaulter всё ещё давит; Flanker не становится «укрывателем»; союзники с Leader/Soldier proximity не разбегаются на край карты из‑за Proximity.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jazz перекрывает EvalDest после CommonLib; AppendClass additive.
- Saves: ок; поведение AI меняется со следующего Think.
- Network/determinism: без RNG.
- Generated data: `jazz-units/items.lua` Weight/ScoreMode only.
- Cross-package: jazz Code + jazz-units presets; maps нет.
- Rollback: revert AIPolicy.lua + items Weight/ScoreMode hunks.

## План и ownership

- Пакет-владелец runtime: `jazz`; presets: `jazz-units`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: `jazz-units/items.lua`.

## Решение владельца

- Статус: **approved** (промежуточный дизайн + playtest ROLE-001 «в целом ок, дальше» 29 июля 2026).
- Кто подтвердил: project-owner.
- Дата: 2026-07-29.
- 2026-08-18: live OptLoc TakeCover weights (Front 20+40 / Assault 10 / Flank 15) are intentional PERF optimizations (OptLoc dest-cap 200, TakeCover enemy cap 8). Lock spec to runtime; do not restore 80–150.

## Evidence

- `JAZZ-AI-POL-001-AC-001`: `PASS` — static: `Code/AIPolicy.lua` — AppendClass `ScoreMode`; TakeCover threat-weight + cover×shot; Proximity closer/farther.
- `JAZZ-AI-POL-001-AC-002`: `PASS` — static: шесть templates; OptLoc TakeCover Front **20+40**, Assault **10**, Flank **15** (radius 55); Flank-branch EndTurn TakeCover Weight 1; ally Proximity `closer_better`. Gate: `docs/tools/_audit_ai_packet1b.py`.
- `JAZZ-AI-POL-001-AC-003`: `PASS` — `ai-awareness.md` + design checklist + playtest POL-001.
- `JAZZ-AI-POL-001-AC-004`: `BLOCKED` — runtime владельца; `docs/design/tactical-ai-roles-playtest.md` §POL-001.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — TakeCover/Proximity POL-001; live OptLoc weights locked 2026-08-18.
- `docs/design/tactical-ai-roles-playtest.md` — POL-001 smokes.
- `docs/design/tactical-ai-archetypes.md` — checklist.
