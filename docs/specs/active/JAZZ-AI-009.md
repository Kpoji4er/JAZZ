---
id: JAZZ-AI-009
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
  - jazz/docs/specs/active/JAZZ-AI-009.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
  - jazz/Code/AIContextProfiles.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/override-matrix.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/wiki/officer-aura.md
  - jazz/docs/showcase/ru/officer-aura.md
  - jazz/docs/showcase/en/officer-aura.md
  - jazz/docs/tools/_check_ai_009_break_los_ow.py
  - jazz/docs/tools/README.md
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-007.md
  - docs/specs/active/JAZZ-AI-008.md
  - docs/specs/active/JAZZ-AI-OW-001.md
  - docs/specs/active/JAZZ-AI-002.md
  - docs/specs/active/JAZZ-AI-CMD-001.md
approved_by: project-owner chat 2026-08-24 (JAZZ-AI-009 делай)
---

# JAZZ-AI-009: Break-LOS retreat Overwatch on vacated tile

## Проблема

При **Отходе** (`FallBack`) боец сейчас либо чуть отступает и берёт укрытие (`TakeCoverChance` 85), либо ставит Fallback OW на **выход игрока** (007 peek-exit). Нет манёвра «оторваться из обзора и держать сектор на клетку, которую только что оставил» — bounding overwatch / peel: игрок идёт в пустую позицию и ловит interrupt с края конуса.

## Цели

- На Отходе стрелок **убегает так, чтобы разорвать LoS** игрока, который его видит.
- С новой клетки ставит Overwatch **на свою старую позицию** (тайл начала хода), не в стену и не random.
- Дистанция dest↔старая клетка — **у максимума конуса OW** (`GetOverwatchConeParam("MaxRange")` / `WeaponRange`), насколько хватает AP с запасом на сам Overwatch.
- 008 perch (высота видит egress) **важнее**: кто держит высоту, не срывается в этот peel.

## Non-goals

- Новый CombatAction / generated `items.lua` archetype.
- Менять порог старта/срыва FallBack (007).
- Farm-relocate 007 (игрок видит, они нет) — отдельный follow-up; в этом spec только `FallBack`.
- Dump/cheap LoF (PERF-004). `GetLoFData` в dest-поиске не звать.
- Deserter / panic / melee / medic heal path.
- Stationed MG / emplacement (свой rotate/pack).
- Полный AntiPeekOW / peek_streak (design §7) — это про чужой last_attack_pos, не про свою vacated tile.

## Требования

- `JAZZ-AI-009-REQ-001` — `JazzAI_UnitCanBreakLosOverwatch(unit, context)`: `context.jazz_fallback`; Human; firearm с `PreparedAttackType` Overwatch/Both; не Medic/Deserter/Melee/Regroup; не stationed MG; не Burning/Reposition; не 008 perch (`JazzAI_ContextStayIsEgressPerch`).
- `JAZZ-AI-009-REQ-002` — якорь `old` = stay dest хода (`context.unit_stance_pos` / pack текущей клетки) **до** Commit. Кэшировать `context.jazz_break_los_ow_anchor` (точка/slab), если выбран qualifying dest.
- `JAZZ-AI-009-REQ-003` — dest **qualifying** только если все:
  1. reachable в этом ходе;
  2. `dest_ap[dest] ≥` AP Overwatch (не оставлять 0 ОД после бега);
  3. дальше от `GetNearestEnemy`, чем stay (направление отхода);
  4. `CheckLOS` dest→`old` в пределах OW max range (как `JazzAI_DestSeesPos`, без `GetLoFData`);
  5. дистанция dest↔old в тайлах ≤ OW max и ≥ `Max(4, OW_max − 4)` если такой dest есть; иначе взять **максимальную** дистанцию среди dest с LOS на old и разрывом LoS (не 2-клеточный Disengage);
  6. **разрыв LoS:** ни один живой `player_team`, который сейчас `HasVisibilityTo(..., unit)`, не имеет `CheckLOS` на dest (тот же sight radius, что DestLos). Игрок, который юнита не видел, не обязан терять гипотетический луч.
- `JAZZ-AI-009-REQ-004` — после `AIScoreReachableVoxels`: если есть qualifying dest, выбранный dest **заменяется** на лучший qualifying (tie-break: ближе к ideal dist = `Min(OW_max, max_reachable_with_ow_ap)`, затем packed pos). Score-bonus в `AIScoreDest` **+220** на qualifying, чтобы OptLoc/EndTurn сами тянули туда до wrap.
- `JAZZ-AI-009-REQ-005` — если якорь выставлен: после хода на dest **не** BunkerDown/`TakeCover` (иначе сектор не ставится). `JAZZ_AIDisengage` / Fallback OW целится в якорь (старая клетка), не в 007 peek-exit last_known. Конус как ванильный Overwatch на `target_pos = old`. Нет qualifying dest → текущий FallBack (дальше + cover) и 007 peek-exit без изменений.
- `JAZZ-AI-009-REQ-006` — без нового RNG. DestLos/Precalc caps не расширять: фильтр только по уже скоренным dest. Docs: technical + wiki/showcase officer-aura (Отход: оторваться и держать старую клетку с края сектора).

## Инварианты и ограничения

- 008 perch stay не отменяется этим peel.
- 007 peek-exit остаётся default no-sight OW, если peel dest не выбран.
- SoftDisengageTiles=2 (AI-002) не подменяет этот манёвр: peel — Commit dest, не хвост Disengage на 2 клетки.
- Deterministic; ephemeral `context` only (якорь не MapVar).
- Не стрелять Dump «в молоко» ради якоря: нет командного LOS — нет Dump в модель (контракт LoS/LoF).

## Acceptance criteria

- `JAZZ-AI-009-AC-001` — static: helpers + dest predicates + wrap replace + OW aim uses cached old pos; skip TakeCover when anchor set; no GetLoFData.
- `JAZZ-AI-009-AC-002` — runtime/human FallBack: видимый стрелок уходит за угол/скалу, игрок теряет LoS, сектор смотрит на опустевшую клетку с дистанции около max OW, не в упор за ближайший куст.
- `JAZZ-AI-009-AC-003` — runtime/human: 008 perch на высоте не peel; нет dest с разрывом LoS — обычный Отход + peek-exit OW.
- `JAZZ-AI-009-AC-004` — docs: technical + wiki + showcase RU/EN officer-aura.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: dest wrap + Fallback OW aim branch; FallBack TakeCover chance не трогать глобально — только skip при якоре.
- Saves: none.
- Network/determinism: без нового RNG.
- Generated data: нет.
- Cross-package: FallBack stance уже Frontliner (`jazz-units` PickCustom); runtime в `jazz`.
- Rollback/recovery: revert Lua + spec.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: implemented
- Кто подтвердил: project-owner (чат 2026-08-24: «JAZZ-AI-009 делай»)
- Дата: 2026-08-24

## Evidence

- `JAZZ-AI-009-AC-001`: `PASS` (static) — `python docs/tools/_check_ai_009_break_los_ow.py`; peel helpers; dest predicate; wrap after 008 hold; +220 `BREAK LOS OW`; Fallback OW aims cached stay; Disengage/BunkerDown skip TakeCover; no GetLoFData.
- `JAZZ-AI-009-AC-002`: `BLOCKED` — runtime/human FallBack: visible shooter peels behind rock/corner, player loses LoS, cone on vacated tile near max OW.
- `JAZZ-AI-009-AC-003`: `BLOCKED` — runtime/human: 008 perch does not peel; no break-LoS dest → ordinary FallBack + peek-exit OW.
- `JAZZ-AI-009-AC-004`: `PASS` (static) — technical `ai-awareness.md` + override-matrix + wiki/showcase RU/EN officer-aura.

## Documentation delta

- `docs/technical/systems/ai-awareness.md`
- `docs/technical/override-matrix.md`
- `docs/design/tactical-ai-archetypes.md`
- `docs/wiki/officer-aura.md`
- `docs/showcase/ru/officer-aura.md`
- `docs/showcase/en/officer-aura.md`
