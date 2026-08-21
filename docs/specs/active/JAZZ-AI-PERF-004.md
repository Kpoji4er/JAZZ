---
id: JAZZ-AI-PERF-004
status: implemented
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: high
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-PERF-004.md
  - jazz/docs/specs/active/JAZZ-AI-PERF-003.md
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/AiActions.lua
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/performance-vanilla-report.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/technical/testing.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - docs/specs/active/JAZZ-AI-PERF-003.md
  - docs/specs/active/JAZZ-AI-002.md
approved_by: project-owner chat 2026-08-21 угу (cheap dump ray; unpenetrable no damage)
---

# JAZZ-AI-PERF-004: Dump CTH hit must damage; unpenetrable must not

## Проблема

Dump (`args.jazz_ai_dump`, JAZZ-AI-PERF-003) пропускает `GetLoFData` и кладёт синтетический луч с `hits = {}`. `Jazz_ReuseTargetingAttackData` переиспользует этот пустой луч. `CheapProjectileFly` по пустому списку всегда играет `TargetMissed`.

DAP на сейве M5 (ход 1, повстанцы ally vs Legion): повстанец `CalcChanceToHit` 90% и ванильный `GetLoFData` `stuck=false`, но Dump `GetActionResults` даёт `hit_objs=0` / `total_damage=0`. Тот же выстрел без `jazz_ai_dump` — 16 урона. ИИ стреляет «в молоко» по открытой цели, в том числе AI↔AI.

Слепой хит по CTH без луча прошил бы непробиваемую скалу. Владелец: чистая/пробиваемая линия — урон по CTH; непробиваемое (скала/утёс/плита) — не давать хит в цель и не тратить выстрел в стену.

## Цели

- Dump execute при CTH-попадании наносит урон, если дешёвый луч доходит до цели.
- Непробиваемое препятствие не получает хит в цель; Dump не вызывает `AIPlayCombatAction` в стену (Disengage / смена цели, JAZZ-AI-002).
- По-прежнему **нет** `GetLoFData` / vegetation `Collide` на Dump targeting и на каждую пулю (M3 waterfall).
- Игрок и не-Dump execute без изменений.

## Non-goals

- Полный ванильный LoF / пробитие промежуточных объектов как у игрока.
- Вернуть `GetLoFData` в `AIGetAttackTargetingOptions` или per-bullet Dump.
- Переписывать CTH, grazing, cover factors.
- WeGotThis / skip-turn asserts.

## Требования

- `JAZZ-AI-PERF-004-REQ-001` — `Jazz_DumpCheapLineOfFire`: один луч attacker aim (muzzle/torso) → target torso. Блокер: `terrain.IntersectSegment` до цели (край у origin/dest игнорировать) **или** другой живой юнит на сегменте (`SegmentIntersectsSphere`, радиус ½ тайла) — союзник в LoF у ванили даёт `stuck`. Юниты-цель не блокер. Растительность не проверяется этим лучем. Slab/проп через `GetLoFData` не зовём (M3). CombatObject без отдельного object-ray: пробитие Dump грубее ванили.
- `JAZZ-AI-PERF-004-REQ-002` — `Jazz_ReuseTargetingAttackData` на Dump: если луч чистый/пробиваемый — `hits` содержит цель; `stuck=false`. Если непробиваемый — `hits={}`, `stuck=true`, `stuck_pos` в точке блока. Не звать `GetLoFData`.
- `JAZZ-AI-PERF-004-REQ-003` — DumpFire: непробиваемый луч → не `AIPlayCombatAction`; лог; сброс sticky target; выход в Disengage (как JAZZ-AI-002 no LOF).
- `JAZZ-AI-PERF-004-REQ-004` — Targeting по-прежнему `CalcChanceToHit` без `GetLoFData`. Player / non-Dump — ванильный пайплайн.

## Инварианты и ограничения

- Детерминизм: тот же луч из позиций/оружия, без нового RNG.
- Не раздувать Dump до per-body-part / per-bullet `CheckLOF`.
- Пробитие Dump грубее ванили (нет урона по промежуточной стене с pen); непробиваемое не прошивается.

## Acceptance criteria

- `JAZZ-AI-PERF-004-AC-001` — static: cheap line helpers + Reuse fills hits/stuck; DumpFire skips unpenetrable; no new Dump `GetLoFData`.
- `JAZZ-AI-PERF-004-AC-002` — runtime DAP M5: Dump `GetActionResults` на паре с ванильным `stuck=false` и CTH>0 даёт `hit_objs≥1` и `total_damage>0`; на паре `stuck=true` — `hit_objs=0` / нет урона в цель.
- `JAZZ-AI-PERF-004-AC-003` — docs: technical + wiki + showcase RU/EN.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только jazz Dump execute / Reuse.
- Saves: none.
- Network/determinism: тот же луч на обоих клиентах с модом.
- Generated data: none.
- Cross-package references: none.
- Rollback/recovery: revert PERF-004 Lua + docs.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: implemented
- Кто подтвердил: project-owner
- Дата: 2026-08-21
- Подтверждение: фидбек M5 «всё в молоко»; вопрос «а если там препятствие?» → «угу» на контракт cheap ray / unpenetrable no hit

## Evidence

- `JAZZ-AI-PERF-004-AC-001`: `PASS` (static) — `Jazz_DumpCheapLineOfFire` terrain + unit-sphere; `Jazz_ReuseTargetingAttackData` fills hits/stuck; DumpFire abort in `AiActions.lua`; no Dump `GetLoFData`.
- `JAZZ-AI-PERF-004-AC-002`: `PASS` (runtime DAP, M5 `52(2)` hotpatch+file) — RebelFlanker vs Lieutenant: cheap `clear`, vanilla `stuck=false`, Dump `cth=90` `hits=1` `dmg=26`. RebelGrenadier vs Roughneck: cheap `unit` (ally on line), vanilla `stuck=true`, Dump `cth=0` `hits=0` `dmg=0`.
- `JAZZ-AI-PERF-004-AC-003`: `PASS` (static) — technical + wiki + showcase RU/EN.

## Documentation delta

- `docs/technical/systems/combat-cth-actions.md`
- `docs/technical/systems/ai-awareness.md`
- `docs/technical/performance-vanilla-report.md`
- `docs/technical/override-matrix.md`
- `docs/technical/testing.md`
- `docs/wiki/combat-and-accuracy.md`
- `docs/showcase/ru/combat-and-accuracy.md`
- `docs/showcase/en/combat-and-accuracy.md`
- `docs/specs/active/JAZZ-AI-PERF-003.md` — REQ-007 pointer to PERF-004 execute hits
