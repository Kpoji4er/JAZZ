---
id: JAZZ-AI-010
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
  - jazz/docs/specs/active/JAZZ-AI-010.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiDebugLog.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/tools/_check_ai_010_shot_reserve.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - jazz/Code/CombatAI.lua
related_decisions:
  - docs/specs/active/JAZZ-AI-002.md
  - docs/specs/active/JAZZ-AI-SNIPER-001.md
  - docs/specs/active/JAZZ-AI-008.md
  - docs/specs/active/JAZZ-AI-009.md
  - docs/specs/active/JAZZ-AI-007.md
  - docs/specs/active/JAZZ-AI-DBG-001.md
  - docs/specs/active/JAZZ-AI-ROLE-004.md
approved_by: pending
---

# JAZZ-AI-010: Резерв ОД на выстрел и stay, если stay уже бьёт

## Проблема

Владелец (2026-09-08): ИИ иногда **ходит и не стреляет**, хотя цель видна.

Разбор кода (тот же день): пайплайн `Think → Move → Dump → Disengage` (JAZZ-AI-002). Часть ходов без выстрела задумана (Отход/peel, creeper, perch без тела, reposition в укрытие). Другая часть — дыра Commit:

1. В `AIFindDestinations` при **командном vis** `reserved_AP = 0`, затем только `disengage_reserve` (2 ОД). Комментарий рядом считает `desired_move_ap = min(AP − attack_cost, safe_stride)`, но ветка `visible and 0` это выкидывает. Пути строятся почти на весь бюджет. EndTurn (укрытие / высота / фланг) выбирает дальнюю клетку. После хода leftover ≈ 2 ОД → Dump abort `no-ap`.
2. SNIPER-001 hold (`dest_target_score[stay] > 0` → stay) есть только у `Sniper`/`Marksman` (+ 008 perch). Остальные роли **уходят с клетки, с которой уже есть выстрел**, на dest без выстрела или без ОД на атаку.

Это ломает канон AI-002 «выбег → выстрел → укрытие»: выбег съедает выстрел.

## Цели

- При командном vis путь **оставляет ОД на атаку** (плюс уже существующий DisengageReserve 2 ОД), не больше `safe_stride` на ход.
- Если с **stay** уже можно стрелять (`dest_target_score[stay] > 0`) и выбранный dest **не** даёт живой выстрел с leftover ≥ стоимости атаки — **остаться**. Не только снайпер.
- Один существующий wrap `AIScoreReachableVoxels` (после 001/008 hold и 009 peel). Без второго wrap.
- `AIDebugLog`: причина dest `stay-shot`, если сработал этот override.

## Non-goals

- Чинить Dump abort `no-lof` / `no-team-vis` / cheap ray (PERF-004) — отдельный контракт, если понадобится.
- Менять веса TakeCover / DealDamage / HighGround (POL-001, ROLE-004 крыши).
- Расширять SNIPER-001 hold на perch / useless streak; не менять 008/009 предикаты.
- Creeper 007, Medic walk-to-patient, FallBack peel, Burning / `context.reposition`.
- Животные (`JazzAI_UsesJazzCombatAI` false).
- Leftover-`restart`, SoftDumpCap, BunkerDown (уже AI-002).
- Новые public ID, MapVar, GameVar, второй wrap на `AIScoreReachableVoxels` / `AIFindDestinations`.
- ROLE-004 (семьи, фланговые снайпера, кит, крыши).

## Канон резерва

`attack_cost` = `context.attack_AP_reserved` или `context.default_attack_cost` или `floor(AP/2)` — как сейчас в `AIFindDestinations`.  
`disengage_reserve` = `2 * const.Scale.AP` (AI-002 SoftDisengageTiles).  
`safe_stride` = `context.safe_stride_ap` или `8 * const.Scale.AP`.  
`min_move_ap` = `context.min_move_ap` или 0.

| Командный vis | Норматив `reserved_AP` |
| --- | --- |
| **Есть** (`enemy_visible_by_team`) | `Max(attack_cost, reserve_from_stride) + disengage_reserve`. Ветка `visible and 0` **запрещена**. `desired_move_ap` / `reserve_from_stride` как в текущем комментарии: не тратить больше `safe_stride`, оставить `attack_cost`. |
| **Нет** | Как сейчас: `Max(attack_cost, reserve_from_stride, half) + disengage_reserve` (разведка / creeper, Dump в модель и так запрещён). |

После расчёта: `reserved_AP = Min(reserved_AP, Max(0, AP − min_move_ap))`, затем `Max(0, …)`. Временно урезать `unit.ActionPoints` на время `AIBuildArchetypePaths`, **всегда** вернуть.

Так дальняя клетка не попадает в набор, если после подхода не хватит на выстрел. Близкий Commit (≤ stride) с leftover на Dump — можно.

## Канон stay-if-shot

После `AIScoreReachableVoxels` base + `JazzAI_ApplySniperHoldDestination` + `JazzAI_ApplyBreakLosOverwatchDestination`:

`JazzAI_ApplyStayIfShotDestination(context, dest)`:

1. Нет context/dest/stay → dest без изменений.
2. `context.reposition` или Burning → dest.
3. `context.jazz_break_los_ow_anchor` (peel 009 уже сработал) → dest.
4. Creeper `JazzAI_RecontactCreeperShouldHide` / assigned creeper think → dest.
5. `context.can_heal` → dest.
6. Иначе если `dest_target_score[stay] > 0` и dest ≠ stay:
   - `dest_ap[dest] < attack_cost` **или** `dest_target_score[dest] ≤ 0` → **stay**;
   - иначе dest (лучшая клетка с живым выстрелом и ОД).
7. `dest_target_score[stay] ≤ 0` → dest (можно идти к укрытию / last known; после подхода Dump стреляет, если leftover и LoF есть).

MGSetup: если `JazzAI_ContextNeedsMGHalfCoverBias` и dest — half-cover setup, stay-if-shot **не** отменяет (setup не пишется в `dest_target_score`). Close-fire MG (ACT-004, враг ≤ 8) — обычное stay-if-shot (стрелять с места, не уходить на дальний сектор).

Порядок wrap (один символ): base → sniper/perch hold → peel → **stay-if-shot**. Peel важнее stay-if-shot.

## Требования

- `JAZZ-AI-010-REQ-001` — `AIFindDestinations` (human Jazz path, не vanilla beasts): при командном vis нет `reserved_AP = 0`; резерв по таблице «Канон резерва».
- `JAZZ-AI-010-REQ-002` — `JazzAI_ApplyStayIfShotDestination` в существующем wrap `AIScoreReachableVoxels` после 001/008 и 009; без второго wrap.
- `JAZZ-AI-010-REQ-003` — исключения stay-if-shot: peel, creeper, medic, Burning/reposition, MGSetup half-cover dest (не close-fire).
- `JAZZ-AI-010-REQ-004` — `JazzAI_DebugLogDest`: если dest заменён stay-if-shot, `why` = `stay-shot` (RU/EN как остальные причины DBG-001). Скоринг не менять ради лога.
- `JAZZ-AI-010-REQ-005` — static gate `docs/tools/_check_ai_010_shot_reserve.py`: нет `visible and 0` в резерве; helper stay-if-shot вызывается в wrap после peel; нет второго wrap.

## Инварианты и ограничения

- Детерминизм: без нового RNG.
- Не второй wrap на `AIScoreReachableVoxels` / `SelectArchetype` / `AIFindDestinations`.
- Не ломать 001 hold, 008 perch, 009 peel, 007 creeper hide.
- `dest_ap` / `attack_cost` — уже существующие поля context.
- Exclusive `jazz/Code/CombatAI.lua` пересекается с draft **JAZZ-AI-ROLE-004**. Реализация 010 — **после** правок ROLE-004 в этом файле или одной транзакцией того же агента, не параллельно.
- Сейвы: следующий StartAI, `[no new game]`.
- Животные — `JazzAI_VanillaFindDestinations` / beast dest, без этих правил.

## Acceptance criteria

- `JAZZ-AI-010-AC-001` — static: vis-ветка резерва не обнуляет `reserved_AP`; есть `attack_cost` + `disengage_reserve`; gate `_check_ai_010_shot_reserve.py` exit 0.
- `JAZZ-AI-010-AC-002` — static: `JazzAI_ApplyStayIfShotDestination` после peel в том же wrap; stay если stay-score > 0 и (dest-score ≤ 0 или dest_ap < attack_cost); исключения REQ-003.
- `JAZZ-AI-010-AC-003` — static: DBG `stay-shot`; нет второго wrap (в т.ч. `_check_lua_wrap_cycles.py`).
- `JAZZ-AI-010-AC-004` — runtime/human: юнит с командным vis и выстрелом со stay **не** уходит на дальнее укрытие и не заканчивает ход с `no-ap` при живой цели в LoF.
- `JAZZ-AI-010-AC-005` — runtime/human: FallBack peel по-прежнему уходит и ставит OW (009); creeper с vis прячется, не Dump.
- `JAZZ-AI-010-AC-006` — docs: `ai-awareness.md` + override-matrix отражают резерв при vis и stay-if-shot.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только jazz `AIFindDestinations` + существующий ScoreReachable wrap; beasts без изменений.
- Saves: `[no new game]`.
- Network/determinism: без нового RNG; тот же `attack_cost` / `dest_target_score`.
- Generated data: нет.
- Cross-package: нет. ROLE-004 владеет тем же `CombatAI.lua` до своего implement.
- Rollback: revert 010 diff.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: `jazz/Code/CombatAI.lua`.

## Решение владельца

- Статус: **draft** — ждёт approve.
- Кто подтвердил: pending.
- Дата: 2026-09-08.
- Запрос владельца: отдельный контракт на резерв ОД и «не уходить с выстрела, если stay уже бьёт» (не ROLE-004).

## Evidence

- `JAZZ-AI-010-AC-001`: `BLOCKED` — нет реализации.
- `JAZZ-AI-010-AC-002`: `BLOCKED` — нет реализации.
- `JAZZ-AI-010-AC-003`: `BLOCKED` — нет реализации.
- `JAZZ-AI-010-AC-004`: `BLOCKED` — runtime.
- `JAZZ-AI-010-AC-005`: `BLOCKED` — runtime.
- `JAZZ-AI-010-AC-006`: `BLOCKED` — docs after implement.

## Documentation delta

После implement (не сейчас): `ai-awareness.md` (резерв при vis; stay-if-shot после hold/peel); `override-matrix.md` (тот же wrap + helper). Wiki/showcase не обязательны: игрок видит «подошёл и выстрелил», без новой механики в UI.
