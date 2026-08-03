---
id: JAZZ-AI-PERF-001
status: approved
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-PERF-001.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
  - jazz/Code/AIPolicy.lua
  - jazz/docs/technical/performance-vanilla-report.md
  - jazz/docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-001-dest-los-cache.md
  - jazz/docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-002-precalc-damage-lof.md
  - jazz/docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-003-dual-path-optloc.md
  - jazz/docs/technical/systems/ai-awareness.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner chat 2026-07-31 implement AI 100-unit scale plan
---

# JAZZ-AI-PERF-001: AI turn spatial shortlists (DestLos + Precalc)

## Проблема

На картах размера M1 при десятках AI-юнитов (цель продукта — до ~100) non-player `AITurn` занимает минуты без Lua ERROR: `AIUpdateDestLosCache` делает `CheckLOS` по **всем** reachable dest × **всем** `context.enemies`, затем `AIPrecalcDamageScore` платит `GetLoFData` по широкой матрице. Release-логи пустые; JA3Debug показывает busy CPU. Live repro: ~10 rebels + ~30 Legion + player.

Не ждать Asphalt/engine fix V-AI-001/002 — JAZZ уже владеет overrides.

## Цели

- Non-player `AITurn` (одна сторона) **≤ 20 s** wall-clock на M1-class с ~100 living combatants (JA3Debug + `config.JAZZ_AIPerfLog`).
- DestLos/Precalc масштабируются по **in-range** парам (детерминированный shortlist).
- In-range engagement quality сохраняется; far/out-of-range candidates могут отличаться от vanilla full matrix.

## Non-goals

- Rewrite OptLoc / EndTurn policies.
- Change player CTH formulas.
- Fix V-VIS-001 `UpdateUnitsLOS` O(n²) FPS (отдельный follow-up).
- Guarantee ≤20 s при pathological open slabs × 100 in-range enemies *and* OptLoc scoring still too wide after dest caps (further radius/policy work).

## Требования

- `JAZZ-AI-PERF-001-REQ-001` — `AIUpdateDestLosCache`: use full `context.enemies` (sorted by `handle`); far-skip dests beyond sight (2D) from all enemies. *(Range enemy shortlist rolled back 2026-07-31 — smarter LOS; owner request.)*
- `JAZZ-AI-PERF-001-REQ-002` — DestLos: dest farther than sight (2D) from all enemies → cache `false`, skip `CheckLOS`.
- `JAZZ-AI-PERF-001-REQ-003` — Keep batching + `Sleep(10)` yield + compact-visible; `NetUpdateHash` includes enemy count/handles, check-dest count, capped-out count, dest-cap.
- `JAZZ-AI-PERF-001-REQ-004` — `AIPrecalcDamageScore`: soft target prune only when `#targets > 12` (weapon range + wide margin; was 24, tightened 2026-08-02 for dense ally/rebel turns); early-out dest when `g_AIDestEnemyLOSCache[dest] == false`; do not expand to `all_destinations` when Think passed a subset.
- `JAZZ-AI-PERF-001-REQ-005` — Gated timing: `config.JAZZ_AIPerfLog` → per-unit DestLos/Precalc ms + side AITurn ms.
- `JAZZ-AI-PERF-001-REQ-006` — DestLos CheckLOS dest-cap (`JAZZ_AI_PERF_DESTLOS_CAP`, default 320): prefer stay / important_dests / destinations, then nearest to unit; remainder stay cache `false`.
- `JAZZ-AI-PERF-001-REQ-007` — `AIEnumValidDests`: after CollapsePoints, cap `all_destinations` to `JAZZ_AI_PERF_OPTLOC_DEST_CAP` (default **400**) with the same priority helper; hash `AIEnumValidDests_Cap`. Cuts OptLoc TakeCover×enemies over open M1 slabs (was 2k–3k dests).
- `JAZZ-AI-PERF-001-REQ-008` — Gated OptLoc/EnumDests timing via `config.JAZZ_AIPerfLog`. **TakeCover far-skip of `GetCoverPercentage` reverted 2026-08-03** (owner: AI hugged cover without threat-facing). Full POL-001 `GetCoverPercentage` for all visible enemies restored. Cap helper fills remaining slots by **nearest threat**, not nearest-to-self.
- `JAZZ-AI-PERF-001-REQ-009` — `AIPrecalcDamageScore`: cap scored dests to `JAZZ_AI_PERF_PRECALC_DEST_CAP` (default **80**) via same helper; never drop stay; hash includes capped count. Runtime evidence: ally AITurn 216 s with Precalc peaks 12–27 s on 200–400 dests × ~20 targets.

## Инварианты и ограничения

- Sync/determinism: enemy order by `handle`; dest-cap order stable (packed dest / dist); same inputs → same hashes/outcomes.
- No change to CombatAction CTH for player.
- Prefer false-negative far / capped-out dest LOS over multi-minute stalls.

## Acceptance criteria

- `JAZZ-AI-PERF-001-AC-001` — static: shortlist helpers + DestLos/Precalc use them; NetUpdateHash Start includes shortlist counts.
- `JAZZ-AI-PERF-001-AC-002` — runtime/human: M1 ~40 combatants AITurn completes without multi-minute stall (target ≪ 20 s).
- `JAZZ-AI-PERF-001-AC-003` — runtime/human: stretch toward ~100 combatants ≤ 20 s AITurn with `JAZZ_AIPerfLog` evidence (or document FAIL + follow-up).
- `JAZZ-AI-PERF-001-AC-004` — docs: performance-vanilla-report + V-AI-001/002 mod notes updated.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides in jazz `CombatAI.lua` / `AiActions.lua` only.
- Saves: none.
- Network/determinism: shortlist must be hash-stable; MP desync risk if nondeterministic prune.
- Generated data: none.
- Rollback: revert the two Code files + docs.

## План и ownership

- Пакет-владелец: jazz
- Declared write set: see frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто: project-owner
- Дата: 2026-07-31
- Подтверждение: «делай-приступай» на plan AI 100-unit scale

## Evidence

- `JAZZ-AI-PERF-001-AC-001`: `PASS` (static) — DestLos full enemies + far-skip + dest-cap 320; **OptLoc all_destinations cap 400** (rest sorted by nearest threat); TakeCover = full POL-001 `GetCoverPercentage` (far-skip **reverted**); soft Precalc prune gate **12**; `config.JAZZ_AIPerfLog` timing (DestLos/Precalc/EnumDests/OptLoc/AITurn); Medic/Medic_Low OptLoc 45 + runtime clamp; Flanker OptLoc 55 (units package, companion to soft gate).
- `JAZZ-AI-PERF-001-AC-002`: `PASS` (runtime/human) — M1 large fight (JA3Debug + AIPerfLog): after dest-cap AI side completed to player turn; DestLos e.g. RebelFlanker dests≈2781 check_dests≈7 ms≈8; Precalc typically 1–50 ms (Rifleman peaks ~0.5 s). Prior uncapped DestLos hung ~30 min. **2026-08-03 follow-up:** owner reports AITurn still stalls on M1 large maps after DestLos-only fix → OptLoc dest-cap + TakeCover far-skip landed; needs re-verify with `JAZZ_AIPerfLog` (EnumDests/OptLoc lines).
- `JAZZ-AI-PERF-001-AC-003`: `BLOCKED` (runtime/human) — owner ~100 stress.
- `JAZZ-AI-PERF-001-AC-004`: `PASS` (docs) — performance-vanilla-report + V-AI-001/002/003 mod notes.

### Testing

JA3Debug required. In console before combat: `config.JAZZ_AIPerfLog = true`. Reproduce M1 large fight; read `[JAZZ-AI-PERF]` lines for DestLos/Precalc/**EnumDests**/**OptLoc**/AITurn ms. Expect EnumDests `uncapped`≫`dests` on open M1; OptLoc `scored` ≤400.

## Documentation delta

- `docs/technical/performance-vanilla-report.md`
- `docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-001-dest-los-cache.md`
- `docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-002-precalc-damage-lof.md`
- `docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-003-dual-path-optloc.md`
- `docs/technical/systems/ai-awareness.md`
