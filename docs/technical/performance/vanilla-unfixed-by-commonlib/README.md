# Vanilla performance issues not fixed by CommonLib

Audit slice: **2026-07-30**. Sources: upstream `JaggedAlliance3Modding` Lua, CommonLib `main` (1.11 / build 1059).

Each file below is one vanilla hot-path problem that **JA3_CommonLib does not resolve**. Partial mitigations in JAZZ (if any) are noted per card; they do not replace an engine/vanilla fix.

Russian index / JAZZ-side notes: [`../../performance-vanilla-report.md`](../../performance-vanilla-report.md).

## Excluded (CommonLib already mitigates)

| Topic | CommonLib mitigation |
| --- | --- |
| Suspicion ally×enemy tick | `Code/FixAI.lua` — `IsCloser` / visibility early-outs before `GetSightRadius` (structural O(allies×enemies) remains) |
| Overwatch visual rebuild spam | `Code/GeneralFixes.lua` — hash cache + `PassVersion` |
| Smoke LOS when map has no smoke | `Code/_Utils.lua` — `IsLineInSmoke` empty `g_SmokeObjs` early-out |
| Mod conflict / editor scans | `Code/_Stubs.lua`, appearance batching, loading-screen skips |

## Issue cards

### P0 — Combat AI turn time

| ID | File |
| --- | --- |
| V-AI-001 | [V-AI-001-dest-los-cache.md](V-AI-001-dest-los-cache.md) |
| V-AI-002 | [V-AI-002-precalc-damage-lof.md](V-AI-002-precalc-damage-lof.md) |
| V-AI-003 | [V-AI-003-dual-path-optloc.md](V-AI-003-dual-path-optloc.md) |
| V-AI-004 | [V-AI-004-score-dest-fire-gas.md](V-AI-004-score-dest-fire-gas.md) |
| V-AI-005 | [V-AI-005-emplacement-mapget.md](V-AI-005-emplacement-mapget.md) |

### P0 — Visibility / LOS

| ID | File |
| --- | --- |
| V-VIS-001 | [V-VIS-001-update-units-los.md](V-VIS-001-update-units-los.md) |
| V-VIS-002 | [V-VIS-002-faded-slab-mapget.md](V-VIS-002-faded-slab-mapget.md) |

### P1 — Satellite / UI / exploration

| ID | File |
| --- | --- |
| V-SAT-001 | [V-SAT-001-satellite-dijkstra.md](V-SAT-001-satellite-dijkstra.md) |
| V-UI-001 | [V-UI-001-interactable-highlight.md](V-UI-001-interactable-highlight.md) |
| V-UI-002 | [V-UI-002-approach-banters.md](V-UI-002-approach-banters.md) |
| V-UI-003 | [V-UI-003-inventory-nested-foreach.md](V-UI-003-inventory-nested-foreach.md) |

### P2 — AmbientLife / GC / leftovers

| ID | File |
| --- | --- |
| V-AL-001 | [V-AL-001-ambient-life-map-sweeps.md](V-AL-001-ambient-life-map-sweeps.md) |
| V-AI-GC-001 | [V-AI-GC-001-ai-temp-allocations.md](V-AI-GC-001-ai-temp-allocations.md) |
| V-VIS-DBG-001 | [V-VIS-DBG-001-experimental-los-branch.md](V-VIS-DBG-001-experimental-los-branch.md) |

## Suggested vanilla/engine fix order

1. V-VIS-001
2. V-AI-001 / V-AI-002
3. V-SAT-001
4. V-VIS-002
5. V-UI-001
