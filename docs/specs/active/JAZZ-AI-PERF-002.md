---
id: JAZZ-AI-PERF-002
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
  - jazz/docs/specs/active/JAZZ-AI-PERF-002.md
  - jazz/docs/specs/active/JAZZ-AI-PERF-001.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/performance-vanilla-report.md
  - jazz/docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-003-dual-path-optloc.md
  - jazz/Code/CombatAI.lua
exclusive_resources:
  - none
related_decisions:
  - docs/specs/active/JAZZ-AI-PERF-001.md
  - ModTools/Docs/JA3_AI.md.html
approved_by: project-owner 2026-08-14 implement in order
---

# JAZZ-AI-PERF-002: OptLoc cap keeps Strategy candidates

## Проблема

Официальный AI гайд: OptLoc = Strategy (цель на бой, например высота для снайпера), EndTurn = Execution (этот ход). Связка — path distance до `best_dest` как база скора reachable клеток.

`JAZZ_AICapDestLosCandidates` после stay/important/behavior добирает cap **nearest threat**. Один helper обслуживает DestLos, Precalc **и** `AIEnumValidDests`. Дальняя крыша / якорь роли, ради которых Strategy существует, систематически выпадает из 200 клеток. Stay-hold (SNIPER-001) при этом **правильный**: если со стоячей клетки уже есть выстрел — не уезжать. Ломается только многоходовой подход, когда стрелять отсюда ещё нельзя.

## Цели

- Cap `JAZZ_AI_PERF_OPTLOC_DEST_CAP` (**200**) сохраняется.
- OptLoc shortlist **сначала** резервирует стратегических кандидатов (высота, якоря роли, кольцевая выборка радиуса), **потом** nearest-threat.
- DestLos CheckLOS cap и Precalc dest cap **не** меняют fill: для стрелкового hot path nearest-threat остаётся верным.
- Дешёвые эвристики до `AIScoreDest` (курица-яйцо: `best_dest` ещё нет).

## Non-goals

- Поднимать cap / `OptLocSearchRadius`.
- Полный policy score на uncapped 2k–3k slabs.
- Менять SNIPER-001 stay-hold.
- Менять EndTurn `DealDamage` vs `OptLocWeight` (отдельный playfeel, не этот spec).
- V-VIS-001 / полный dest×enemy LoF.

## Требования

- `JAZZ-AI-PERF-002-REQ-001` — `AIEnumValidDests` больше не вызывает общий `JAZZ_AICapDestLosCandidates`. Новый `JAZZ_AICapOptLocCandidates(unit, context, dests, cap)` только для OptLoc. DestLos (`JAZZ-AI-PERF-001-REQ-006`) и Precalc (`REQ-009`) остаются на старом helper с nearest-threat.
- `JAZZ-AI-PERF-002-REQ-002` — порядок заполнения OptLoc cap:
  1. stay / `important_dests` / `destinations` (reachable Execution set) — как сейчас, sort packed dest
  2. **Strategy reserve** до `JAZZ_AI_PERF_OPTLOC_STRATEGY_RESERVE` (default **48**) из оставшихся dests
  3. хвост — nearest threat, tie-break packed dest (как PERF-001)
- `JAZZ-AI-PERF-002-REQ-003` — Strategy reserve, детерминированный набор (можно пересекаться, unique dest):
  - **High ground:** dest Z > unit Z (stance unpack); брать до 16 самых высоких, tie packed dest
  - **Role anchors:** если есть ally с keyword Sniper/Marksman/Leader (или aura `semi_sniper` / officer `source`) — до 16 dests ближайших к линии `anchor → nearest threat` (2D dist to segment), иначе skip
  - **Ring sample:** 8 компасов (N/NE/E/SE/S/SW/W/NW относительно unit); в каждом секторе самый дальний dest в радиусе OptLoc; добивает reserve если высота/якоря не набрали 48
- `JAZZ-AI-PERF-002-REQ-004` — hash `AIEnumValidDests_Cap` включает `strategy_kept` count (число dests из шага 2, попавших в out).
- `JAZZ-AI-PERF-002-REQ-005` — PERF-001 REQ-007/008: для OptLoc fill «nearest threat only» **superseded** этим spec; DestLos/TakeCover enemy cap / Precalc без изменений.

## Инварианты и ограничения

- Тот же cap 200; uncapped 2k+ на M1 по-прежнему режется.
- Нет нового RNG.
- High-ground heuristic = voxel Z, не полный `AIPolicyHighGround`.
- Stay всегда в shortlist (SNIPER-001 hold не теряет стоячую клетку).
- Не считать Strategy reserve для DestLos: дальняя крыша без LOS к врагам не должна съедать CheckLOS бюджет ближних клеток.

## Acceptance criteria

- `JAZZ-AI-PERF-002-AC-001` — static: отдельный `JAZZ_AICapOptLocCandidates`; DestLos/Precalc всё ещё `JAZZ_AICapDestLosCandidates`.
- `JAZZ-AI-PERF-002-AC-002` — static: reserve 48; high-ground / ring / anchor helpers; hash field `strategy_kept`.
- `JAZZ-AI-PERF-002-AC-003` — runtime/human: снайпер **без** stay-shot (нет цели с текущей клетки) за 2+ хода смещается к заметно более высокой / дальней позиции, а не только к ближайшему врагу.
- `JAZZ-AI-PERF-002-AC-004` — runtime/human: M1 OptLoc `scored` ≤ 200; EnumDests не возвращает многоминутный stall (регресс PERF-001 недопустим).
- `JAZZ-AI-PERF-002-AC-005` — docs: PERF-001 REQ-008 пометка superseded-for-OptLoc; V-AI-003 + ai-awareness fill order.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только `jazz/Code/CombatAI.lua` cap path.
- Saves: none.
- Network/determinism: packed dest + handle-stable anchors; Z/compass math integer.
- Generated data: none.
- Rollback: revert CombatAI cap + docs; PERF-001 helper не удалять.
- Cross-package: якоря читают уже существующих allies / MapVar ауры, без правок jazz-units.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Порядок: **первый** из трёх draft (маленький, чинит Strategy). Не смешивать с CMD-002 / HYG-001 в одном коммите.

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (2026-08-14) — «реализовывай все спеки по очереди»
- Дата: 2026-08-14

## Evidence

- `JAZZ-AI-PERF-002-AC-001`: `PASS` — static: `JAZZ_AICapOptLocCandidates` in `Code/CombatAI.lua`; DestLos (`AIUpdateDestLosCache`) and Precalc still call `JAZZ_AICapDestLosCandidates`; `AIEnumValidDests` uses OptLoc helper.
- `JAZZ-AI-PERF-002-AC-002`: `PASS` — static: `JAZZ_AI_PERF_OPTLOC_STRATEGY_RESERVE = 48`; high-ground / ring / anchor fill; hash `AIEnumValidDests_Cap` includes `strategy_kept`.
- `JAZZ-AI-PERF-002-AC-003`: `BLOCKED` — runtime/human: sniper without stay-shot relocates to height / far dest over 2+ turns.
- `JAZZ-AI-PERF-002-AC-004`: `BLOCKED` — runtime/human: M1 OptLoc scored ≤ 200; no PERF-001 stall regression.
- `JAZZ-AI-PERF-002-AC-005`: `PASS` — static: PERF-001 REQ-007/008 superseded-for-OptLoc; V-AI-003 + `ai-awareness.md` fill order.

## Documentation delta

- `docs/specs/active/JAZZ-AI-PERF-001.md` — REQ-008: OptLoc fill superseded by PERF-002
- `docs/technical/systems/ai-awareness.md`
- `docs/technical/performance-vanilla-report.md`
- `docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-003-dual-path-optloc.md`
