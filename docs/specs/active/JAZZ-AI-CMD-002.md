---
id: JAZZ-AI-CMD-002
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
  - jazz/docs/specs/active/JAZZ-AI-CMD-002.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/tactical-ai-roles-playtest.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/wiki/officer-aura.md
  - jazz/docs/showcase/ru/officer-aura.md
  - jazz/docs/showcase/en/officer-aura.md
  - jazz/Code/AIContextProfiles.lua
  - jazz/Code/AIBehaviours.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-CMD-001.md
  - docs/specs/active/JAZZ-AI-MED-001.md
  - docs/specs/active/JAZZ-AI-ACT-002.md
approved_by: project-owner 2026-08-14 implement in order
---

# JAZZ-AI-CMD-002: Cheap team turn sequencer

## Проблема

CMD-001 пишет директиву (что делать отряду). Каждый юнит всё ещё ходит в порядке ванильного `turn_phase` + камера/этаж. Нет дешёвого «кто действует раньше»: дым/flare после штурма, MG setup после того как пушеры уже выбежали.

Официальный гайд (`JA3_AI.md.html`) даёт только Early/Normal/Late. JAZZ Medic Early (MED-001) уже ломает ванильный Late-медик; остальная команда фазы почти не использует как доктрину.

## Цели

- Один раз за сторону хода, **после** `JazzAI_WriteOfficerAura`, назначить каждому живому AI-союзнику слот `Early` / `Normal` / `Late` по роли и намерению этого хода.
- Порядок доктрины: support (flare / smoke / MG setup / bleed-medic) → линия Hold/OW / stationed MG / sniper → Press (Assaulter / Flanker).
- Flare: все носители с реальной тьмой/Underground — **Early**, без unique-слота (несколько карманов тьмы).
- Smoke: по-прежнему **один** curtain-носитель на команду в ход (ACT-002).
- Осколочные/зажигательные гранаты: **не** unique и **не** отдельная Early-роль; кидают в фазе своей роли. Мягкий лимит бросков команды за ход: First Blood **1** полный + 2-й ×25%; Commando **3** полных + **4-й и 5-й** ×25%; Mission Impossible **без лимита**.
- Ванильный `GetTurnPhase`: `IsThreatened()` → Late сохраняется (не кормить OW первыми).

## Non-goals

- GOAP, общий pathfind за отряд, смена OptLoc/EndTurn политик (это PERF-002 / POL-*).
- Новые директивы ауры (CMD-001 набор без изменений).
- Менять stay-hold снайпера (SNIPER-001): если со стоячей клетки есть выстрел — не уезжать на крышу.
- Возвращать Medic на Late.
- Satellite / global AI.
- UnitData-поля под AI (семья роли читается из archetype / keywords / aura assigns).

## Требования

- `JAZZ-AI-CMD-002-REQ-001` — `JazzAI_AssignTeamActSlots(team)` пишет ephemeral `MapVar JazzAI_TeamActSlots` (ключ юнита = `session_id` / `handle`): `{ phase, kind, source }`. Вызов из того же места, что запись ауры (первый офицер стороны); если офицера нет — тот же assign по ролям без директивы. Clear на CombatStart / CombatEnd / смене стороны хода.
- `JAZZ-AI-CMD-002-REQ-002` — фаза по `kind` (первое совпадение, сверху вниз):
  1. `heal` — нужен bandage/bleed (MED-001 predicate) → **Early**
  2. `flare` — Night/Underground **и** есть throwable flare / flare gun **и** есть тёмная/unlit цель (scoring `AIActionThrowFlare`, не пустой карман) → **Early** (все такие носители)
  3. `smoke` — **назначенный** curtain-носитель этого хода (есть smoke, ACT-002 signals) → **Early**
  4. `mg_setup` — MG/LMG, не stationed, signature MGSetup доступен → **Early**
  5. `line` — Frontliner / Sniper / Marksman / stationed MG / Control Hold → **Normal**
  6. `press` — Assaulter / Flanker / aura `pusher` → **Late**
  7. иначе **Normal**
  Frag/molotov/HE **не** дают отдельный `kind`; юнит остаётся `line`/`press`/`heal`/…
- `JAZZ-AI-CMD-002-REQ-003` — unique assign **только smoke**: max 1 `smoke` на команду в ход. Выбор: живые allies в ауре (иначе вся команда), sort by handle; score = есть smoke + curtain/OW signals; лучший пишется в `JazzAI_TeamDirectives[side].smoke`. Flare **без** unique-поля.
- `JAZZ-AI-CMD-002-REQ-004` — override `AIBehavior:GetTurnPhase`: если `JazzAI_TeamActSlots` задал phase — вернуть его; иначе preset `turn_phase`. Затем ваниль: `unit:IsThreatened()` → `"Late"`.
- `JAZZ-AI-CMD-002-REQ-005` — не менять `AIGetNextPhaseUnits` / камеру / MaxSimultaneousUnits, кроме чтения уже выставленного `GetTurnPhase`. Не pathfind’ить за других. Voxel dibs остаётся POL-003.
- `JAZZ-AI-CMD-002-REQ-006` — Medic с активным heal-need остаётся Early даже под Push/Envelop. Не-heal Medic следует `line`/`press` по текущему stance.
- `JAZZ-AI-CMD-002-REQ-007` — мягкий лимит **обычных** гранат (не smoke, не flare): `MapVar JazzAI_TeamExplosiveThrows` считает Execute `AIActionThrowGrenade` с `aoe_type` explosive/fire/gas за сторону хода. Полный score до бюджета, потом ×**25%** (не hard disable). Бюджет по `Game.game_difficulty` (три пресета, **нет Easy**):
  - `Normal` (First Blood) — **1** полный бросок (окно **1–2**: второй на ×25%)
  - `Hard` (Commando) — **3** полных; **4-й и 5-й** (и далее) ×25%
  - `VeryHard` (Mission Impossible) — **без лимита** (штраф не применяется)
  Неизвестный id → как `Normal`. Счётчик clear вместе с act slots; на VeryHard можно не инкрементировать. Не трогает smoke/flare scoring.

## Инварианты и ограничения

- Детерминизм: sort by handle; без нового RNG.
- Replay/MP: тот же seed → те же phase assigns.
- Не ломать MED-001 Early bleed.
- Не ломать ACT-002: smoke всё ещё curtain; sequencer даёт **одному** носителю ходить раньше.
- Несколько flare в одном Early-ходе разрешены (разные карманы тьмы).
- Обычные гранаты не монополизируются одним юнитом; difficulty только мягко режет спам.
- Sniper stay-hold не отменяется Late/Normal.
- Threatened → Late важнее assigned Early (юнит под OW не обязан выбегать первым «потому что гренадёр»).

## Acceptance criteria

- `JAZZ-AI-CMD-002-AC-001` — static: `AssignTeamActSlots` + MapVar + GetTurnPhase wrap; unique assign только `smoke`; нет unique flare/frag.
- `JAZZ-AI-CMD-002-AC-002` — static: таблица kind→phase совпадает с REQ-002; medic heal-need → Early; explosive budget Normal1 / Hard3 / VeryHard off + ×25% после бюджета.
- `JAZZ-AI-CMD-002-AC-003` — runtime/human: в одном ходе врага flare/smoke/MG setup видны **до** массового Press; линия не обязана бежать с штурмом.
- `JAZZ-AI-CMD-002-AC-004` — runtime/human: два юнита с дымом не кидают оба в одном ходе, если оба могли (второй ведёт себя как press/line). Два flare-носителя при двух тёмных карманах **могут** оба кинуть Early.
- `JAZZ-AI-CMD-002-AC-005` — runtime/human: под Overwatch (threatened) носитель не форсируется в Early.
- `JAZZ-AI-CMD-002-AC-006` — runtime/human: First Blood — после одного осколочного второй на ×25%; Commando — полные три, 4-й и 5-й на ×25%; Mission Impossible — без штрафа за число бросков.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: wrap `AIBehavior:GetTurnPhase` в `jazz/Code/AIBehaviours.lua`; assign в `AIContextProfiles.lua`; grenade budget wrap `AIActionThrowGrenade` в `AiActions.lua`. `AISelectAction` / Dump не трогать.
- Saves: ephemeral MapVar, clear on combat boundaries.
- Network/determinism: handle-stable assigns; hash via existing NetUpdateHash on StartAI if slots affect dest (phase itself is execution order, not dest score).
- Generated data: none (preset `turn_phase` остаётся fallback).
- Cross-package: jazz only; stance/keywords уже в jazz-units.
- Rollback: revert the Code files + spec/docs.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: none
- Порядок относительно соседних спек: после approve — **после или параллельно PERF-002**; не смешивать с HYG-001 в одном коммите.

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (2026-08-14) — «реализовывай все спеки по очереди»
- Дата: 2026-08-14

## Evidence

- `JAZZ-AI-CMD-002-AC-001`: `PASS` — static: `JazzAI_AssignTeamActSlots` + MapVars; `AIBehavior:GetTurnPhase` wrap; unique assign only `smoke`; no unique flare/frag field.
- `JAZZ-AI-CMD-002-AC-002`: `PASS` — static: `JazzAI_ActKindPhase` heal/flare/smoke/mg_setup→Early, line→Normal, press→Late; medic heal-need first; budget Normal=1 / Hard=3 / VeryHard off; score ×25% after budget in `JazzAI_ScaleExplosiveGrenadeScore`.
- `JAZZ-AI-CMD-002-AC-003`: `BLOCKED` — runtime/human: flare/smoke/MG setup before mass Press.
- `JAZZ-AI-CMD-002-AC-004`: `BLOCKED` — runtime/human: one smoke thrower; two flare carriers may both Early.
- `JAZZ-AI-CMD-002-AC-005`: `BLOCKED` — runtime/human: Threatened → Late overrides assigned Early.
- `JAZZ-AI-CMD-002-AC-006`: `BLOCKED` — runtime/human: First Blood / Commando / Mission Impossible grenade budgets.

## Documentation delta

- `docs/design/tactical-ai-archetypes.md` §11 + sequencer note
- `docs/design/tactical-ai-roles-playtest.md` — чеклист Q1–Q6, не отмечать done до owner smoke
- `docs/technical/systems/ai-awareness.md` — sequencer + grenade budget
- `docs/technical/override-matrix.md` — GetTurnPhase / Combat:AITurn / ThrowGrenade Execute
- `docs/wiki/officer-aura.md` + `docs/showcase/ru|en/officer-aura.md` — порядок хода, дым/фаеры, лимит гранат
