---
id: JAZZ-AI-PERF-003
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
  - jazz/docs/specs/active/JAZZ-AI-PERF-003.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/VanillaDesyncFixes.lua
  - jazz/Code/ExecFirearmAttacks.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/performance-vanilla-report.md
  - jazz/docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-003-dual-path-optloc.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/testing.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - docs/specs/active/JAZZ-AI-PERF-001.md
  - docs/specs/active/JAZZ-AI-PERF-002.md
approved_by: project-owner chat 2026-08-15 делай M3 enemy-turn freeze
---

# JAZZ-AI-PERF-003: AI CombatPath restrict + StartAI yield

## Проблема

На большой карте (M3 Водопад, `isJdmPy`, 513×513) ход `enemy1` с ~34 живыми AI выглядит как зависание. DAP 2026-08-15: `Combat:AITurn` стартует; `AIEnumValidDests` без debugger-hook ~95–163 ms (uncapped 1485–2650, cap 200 работает). После нескольких `StartAI` Lua-поток перестаёт отвечать на DAP evaluate/pause на минуты при живом CPU — блок в C `GetCombatPathPositions` (`CombatPath:RebuildPaths`), не в OptLoc cap.

Ванильный `AIExecutionController:Execute` зовёт `Unit:StartAI` по **всем** aware юнитам до первого действия. Каждый `StartAI` → `AIBuildArchetypePaths` → до двух `RebuildPaths` с `restrict_area = false` (вся карта). `PauseInfiniteLoopDetection("AiCalc")` глушит watchdog. OptLoc radius резать нельзя (ломало снайперские крыши, PERF-002 Strategy reserve).

## Цели

- C-pathfinding AI на больших картах ограничен AP-достижимым bbox, не всей картой.
- Между `StartAI` юнитов есть yield, UI/DAP не клинят на всё время пачки.
- Gated `[JAZZ-AI-PERF] RebuildPaths` показывает ms / AP / dest count.
- M3 `enemy1` AITurn не уходит в многоминутный C-stall.
- `OptLocSearchRadius` и PERF-002 Strategy reserve не меняются.

## Non-goals

- Менять `OptLocSearchRadius` пресетов или cap 200 / Strategy reserve 48.
- Переписывать `GetCombatPathPositions` (engine).
- Менять player `CombatPath:RebuildPaths` (клик-ход наёмника).
- Гарантия ≤20 s при ~100 юнитах (остаётся PERF-001-AC-003).
- Убирать ванильный dual RebuildPaths, когда MoveStance ≠ PrefStance.

## Требования

- `JAZZ-AI-PERF-003-REQ-001` — Для AI-юнита (`team.control == "AI"`) `CombatPath:RebuildPaths` без уже заданного `restrict_area` ставит bbox вокруг start pos: радиус в тайлах = `AP / walk_cost + margin` (`JAZZ_AI_PERF_PATH_RESTRICT_MARGIN_TILES` = **8**), потолок `JAZZ_AI_PERF_PATH_RESTRICT_MAX_TILES` = **64**. `walk_cost` как у ванили (Walk const × move modifier), но не ниже 25% Walk, чтобы нулевой cost не раздувал flood fill на всю карту. Уже заданный `restrict_area` (маркеры и т.п.) не перезаписывать. Player-controlled не трогать.
- `JAZZ-AI-PERF-003-REQ-002` — `Unit:StartAI`: после базового think, только если `IsGameTimeThread()` и режим не `IModeAIDebug`, `Sleep(1)` — yield между юнитами стартовой пачки Execute. Не звать `Sleep` из Msg/procall (LoadGame `RecalcUIActions`).
- `JAZZ-AI-PERF-003-REQ-003` — `CombatPath:RebuildPaths` **не** делает `Sleep`. Yield только из `StartAI` (REQ-002). Load/UI (`GetClosestMeleeRangePos` / bandage `GetUIState`) тоже ходят в `RebuildPaths`.
- `JAZZ-AI-PERF-003-REQ-004` — `config.JAZZ_AIPerfLog` → `[JAZZ-AI-PERF] RebuildPaths unit=… ms=… ap=… stance=… dests=… restricted=1`.
- `JAZZ-AI-PERF-003-REQ-005` — Обёртки ставятся на load и на `ModsReloaded` / `DataLoaded` / `ClassesBuilt` без double-wrap (тот же паттерн, что `Combat:AITurn`). Класс брать из `g_Classes` (`CombatPath`, `Unit`): `rawget(_G, name)` на DefineClass даёт nil (metamethod `_G` не срабатывает).
- `JAZZ-AI-PERF-003-REQ-006` — `AIPickScoutLocation` bbox = vanilla **`5 * guim`** (не `80 * guim`). `AICalcAOETargetPoints` зовёт scout-scan только если нет `last_known_enemy_pos` **и** нет точек с видимых врагов. Dump signature `PrecalcAction` логируется (`SigPrecalc` / `ScoutLoc`) при `config.JAZZ_AIPerfLog`.
- `JAZZ-AI-PERF-003-REQ-007` — **Dump / AI targeting only:** `AIGetAttackTargetingOptions` считает CTH через `CalcChanceToHit`, не `GetActionResults`/`GetLoFData` (M3 PickBest вис на одном body-part луче). Dump execute (`args.jazz_ai_dump`): `PrepareAttackArgs` не зовёт `GetLoFData`; `GetAttackResults` не повторяет `CalcShotVectors` 50×20 и не зовёт `GetLoFData` на пулю — синтетический LoF / miss `stuck_pos`; `ProjectileFly` без vegetation `Collide`, sleep ≤400 ms. Игрок и не-Dump execute — ванильный пайплайн (в т.ч. пол LoF 100 тайлов).

## Инварианты и ограничения

- Детерминизм: bbox считается из AP, pos, Walk const и move modifier; без нового RNG.
- Не менять OptLoc radius / dest cap / Strategy reserve.
- Reachable dests AI не должны обрезаться внутри реального AP-радиуса (margin 8 тайлов). Потолок 64 тайла — только safety на нулевой walk cost / pathological AP; обычный ход (≤20 ОД при Walk=1000) ≈ 20 тайлов.
- Player path overlay без изменений.
- Sync: оба MP-клиента с модом считают один bbox.

## Acceptance criteria

- `JAZZ-AI-PERF-003-AC-001` — static: wrap `CombatPath:RebuildPaths` только для AI; player и preset `restrict_area` не переписываются; константы margin 8 / max 64; `AIPickScoutLocation` = `5 * guim`; AOE scout только при пустом target pool.
- `JAZZ-AI-PERF-003-AC-002` — static: `Unit:StartAI` yield `Sleep(1)` only if `IsGameTimeThread()`; `RebuildPaths` wrap has no `Sleep`; gated RebuildPaths / SigPrecalc / ScoutLoc log.
- `JAZZ-AI-PERF-003-AC-003` — runtime: сейв M3 ход 1, End Turn, `enemy1` AITurn доходит до исполнения без многоминутного DAP timeout; лог `RebuildPaths` ms на юнит ≪ 5000; после Dump `Precalc dests=1` идут `SigPrecalc` (не тишина); `evaluate` отвечает во время пачки StartAI.
- `JAZZ-AI-PERF-003-AC-004` — docs: V-AI-003, ai-awareness, performance-vanilla-report, testing, wiki + showcase RU/EN combat-and-accuracy.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap в `jazz/Code/CombatAI.lua`; vanilla `CombatPath.lua` / `CombatCamera.lua` не патчим файлом.
- Saves: none.
- Network/determinism: одинаковый bbox на обоих клиентах; множество dests может стать строгим подмножеством ванильного unrestricted flood fill на огромной карте (намеренно).
- Generated data: none.
- Rollback: revert wrap + docs.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner
- Дата: 2026-08-15
- Подтверждение: «делай / перезапускай сейв если надо» после DAP-диагностики M3 freeze

## Evidence

- `JAZZ-AI-PERF-003-AC-001`: `PASS` (static) — wrap + scout radius `5*guim` + AOE skip in `Code/CombatAI.lua`.
- `JAZZ-AI-PERF-003-AC-002`: `PASS` (static) — StartAI yield gated; RebuildPaths has no Sleep; SigPrecalc/ScoutLoc logs.
- `JAZZ-AI-PERF-003-AC-003`: `PASS` (runtime) — M3 turn 1 End Turn after Dump-only LoF skip: no GetLoFData hang; Marauder `SingleShot` Dump `skipLoF` → `DumpFire end ok=true`; player firearms stay vanilla (`CalcMissVectors` wrap uninstalled).
- `JAZZ-AI-PERF-003-AC-004`: `PASS` (static) — technical + wiki + showcase RU/EN updated for scout/AOE/miss-vector hang.

## Documentation delta

- `docs/technical/systems/ai-awareness.md`
- `docs/technical/performance-vanilla-report.md`
- `docs/technical/performance/vanilla-unfixed-by-commonlib/V-AI-003-dual-path-optloc.md`
- `docs/technical/override-matrix.md`
- `docs/technical/testing.md`
- `docs/technical/systems/combat-cth-actions.md`
- `docs/wiki/combat-and-accuracy.md`
- `docs/showcase/ru/combat-and-accuracy.md`
- `docs/showcase/en/combat-and-accuracy.md`
