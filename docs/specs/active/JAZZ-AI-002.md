---
id: JAZZ-AI-002
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
  - jazz/Code/AiActions.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiAction_ThrowFlare.lua
  - jazz/Code/AIPolicy.lua
  - jazz/docs/specs/active/JAZZ-AI-002.md
  - jazz/docs/technical/systems/ai-awareness.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-AI-002: Commit → Dump → Disengage / BunkerDown

## Проблема

JAZZ заменяет большую часть tactical AI. Статический аудит и сравнение с vanilla показывают два класса дефектов, плюс player-facing дыру: StandardAI часто выглядит как «подошёл, выстрелил, остался торчать», а leftover-`restart` пытался чинить это полным re-Think и давал thrash.

### A. Leftover-AP «цикл» + хрупкий bunker/stance

Vanilla `AIPlayAttacks` делает **одну** последовательность signature → basic и возвращает `"restart"` только при:

- `TargetChangePolicy == "restart"` и цель стала невалидной;
- unpack `StationedMachineGun` → `"restart"`.

JAZZ добавил хвост: при leftover AP и `dest ~= unit_stance_pos` → до 3× `"restart"` (полный `Think` снова). Закомментирован локальный `while`. Итог: дорого, часто лишний move вместо «дострел / спрятаться».

Параллельно `TryChangeStance` в конце хода («bunker down») работает кое-как:

- hardcoded AP `1000`/`2000` вместо `GetStanceToStanceAP`;
- возможный double-spend AP после `AIPlayChangeStance`;
- вызывается и из leftover-хвоста, и всегда в хвосте `AIPlayAttacks`, плюс vanilla `AITakeCover` после `AIExecuteUnitBehavior` — три конкурирующих end-turn пути;
- нет явного приоритета TakeCover vs crouch-behind-low vs prone-in-open vs archetype `PrefStance`;
- не отличает «только что стрелял из открытой клетки» от «уже в хорошей стойке после Commit».

Дополнительно: typo `context.max_attack = …` не декрементит `max_attacks`; `PickBestAttack` + `AP/cost` пачка расходится с предсказуемым дострелом.
### B. Correctness-баги

| # | Симптом | Место |
| --- | --- | --- |
| 1 | `GameState.state` вместо `GameState[state]` | `AISignatureAction:MatchUnit` |
| 2 | `math.random()`; отсев `total_cost == AP` | `PickBestAttack` |
| 3 | `visible = true` hardcoded | `AIFindDestinations` |
| 4 | aim-loop: `remaining -= 1` + снаружи `-= aim_cost` | `AICalcAttacksAndAim` |
| 5 | `TryEquip` без присвоения `ammo` → nil | `AIReloadWeapons` |
| 6 | `TargetLastAttackPos or true`; noise → nil `target_pts` | `AIActionThrowFlare` |
| 7 | Weight умножается в Eval и снова в `AIScoreDest` | Flanking / HighGround / IndoorsOutdoors |

### C. Желаемое поведение владельца

AI должен совершать **осознанные цепочки** за ход, а не «сжёг AP как получилось». Два канонических примера:

1. **Выбег → выстрел → укрытие / bunker / stance** (Commit → Dump → Disengage).
2. **Выбег → выстрел по цели A → выстрел по цели B** (Commit → Dump с дешёвым retarget, без второго Think).

«Bunker down» = осознанный end-turn: `TakeCover` (`Protected`) и/или смена стойки (crouch/prone) по правилам Disengage, а не случайный вызов `TryChangeStance` в трёх местах.
Не цель: хаотичный полный replan на каждый leftover AP. Динамические архетипы — отдельный рычаг роли; этот spec чинит **execution**, чтобы такие цепочки были стабильно возможны.
## Слои «умного» AI

| Слой | Что даёт | Этот spec |
| --- | --- | --- |
| Execution: Commit / Dump / **Disengage** | связный ход: выбег + дострел/2 цели + укрытие | **да** |
| Situation restart | kill → полный replan | сохранить vanilla |
| Dynamic archetype | смена набора правил | follow-up |
| Scoring weights | куда выбегать | Weight² fix; тюнинг позже |

## Цели

- Модель **Commit → Dump → Disengage** вместо leftover-restart.
- Осознанные цепочки за один ход: (а) выбег → атака(и) → укрытие/bunker/stance; (б) выбег → атака A → атака B с локальным retarget.
- Единый end-turn **BunkerDown** вместо конкурирующих `TryChangeStance` + хвост leftover + случайный `AITakeCover`.
- `"restart"` только target-change / MGPack / explicit status (полный replan по событию, не по leftover AP).
- Correctness B1–B7 + deterministic `PickBestAttack`.
- Docs sync.

## Non-goals

- Полный rewrite CombatAI / AOE/scout copies.
- `jazz-units` archetype data / keywords в этом change set.
- `JAZZ-AI-001` policy cleanup.
- Большой perf-rewrite LOS/damage score.
- Тюнинг числовых Weight/MaxAttacks в data.
- Awareness load-time constants.
- Произвольный multi-hop move-shoot-move-shoot.
- Dynamic archetype transitions — follow-up.
- **Re-engage** (снова выбежать стрелять при no LOF) — follow-up; здесь приоритет **Disengage**.

## Рекомендуемая модель

```text
Think (1×) → Move out (0..1×) → Attack Dump (N×) → Disengage (0..1×) → stance/OW
                ↑
                └── restart только: TargetChangePolicy / MGPack / status
```

Осознанные действия за ход — либо **дострел / смена цели с места**, либо **укрытие**. Не «ещё раз всё передумай».

После каждой атаки Dump: если есть вторая валидная цель + AP + `max_attacks` → следующий выстрел; иначе → Disengage. Не чередовать шаг-выстрел-шаг в одном PlayAttacks.

### Фаза 1 — Commit (выбежал)

`Think` + один `BeginMovement`.

**DisengageReserveAP** при построении путей / dest_ap:

- если огневая dest **без** good cover → резерв ≈ `SoftDisengageTiles * Scale.AP` (**SoftDisengageTiles = 2**), не больше `AP - attack_cost`, не ломая min_move;
- если dest уже в good cover → резерв 0 (хватит TakeCover/stance на месте).

Так после выстрела остаётся AP на «спрятаться», а не только на подход.

### Фаза 2 — Attack Dump (выстрелил)

Пока юнит может действовать, нет prepared/OW, `max_attacks > 0`, AP хватает на атаку:

1. update enemies / context;
2. `AIPrecalcDamageScore` только текущая клетка;
3. одно действие: signature **или** один basic volley (`PickBestAttack`);
4. декремент `max_attacks`;
5. kill → restart policy **или** дешёвый retarget;
6. no LOF/target → выход в Disengage.

SoftDumpCap = **4**.

### Фаза 3 — Disengage + BunkerDown (спрятался)

Один post-attack блок. Сначала опциональный **cover-move**, затем **BunkerDown** на финальной клетке. Не больше одного cover-move (`context.disengage_used`).

**3a. Cover-move (если нужно)**

Если клетка слабая (нет cover / плохой cover vs visible enemies) и leftover AP ≥ 1 тайл → один short cover-move (reachable + cover score, без полного OptLoc Think). Иначе остаёмся.

**3b. BunkerDown / stance (всегда пытаемся осознанно, один раз)**

Приоритет на финальной клетке (пропуск если prepared attack / active overwatch / non-Human / MG stationed):

1. **TakeCover** — если `CanTakeCover()` и есть cover vs хотя бы одного visible enemy → `AIPlayCombatAction("TakeCover")` (даёт `Protected` / crouch). Шанс: `max(behavior.TakeCoverChance, 100)` после атаки в этом PlayAttacks (после осознанного выстрела bunker не бросаем на 20% RNG); если атак не было — уважать `TakeCoverChance` как vanilla.
2. **Crouch за low cover** — есть low cover, нет high / TakeCover недоступен, stance не Crouch/Prone → `StanceCrouch` / `AIPlayChangeStance("Crouch")` со стоимостью `GetStanceToStanceAP`.
3. **Prone в открытом** — нет cover вовсе, leftover AP хватает → prone через `GetStanceToStanceAP` (учёт `HitTheDeck`); это «hit the dirt», не TakeCover.
4. **PrefStance archetype** — если ещё Standing и AP хватает и PrefStance ∈ {Crouch, Prone} → один переход к PrefStance.
5. Иначе — ничего (не жечь AP).

Правила стоимости:

- только `GetStanceToStanceAP` / штатные combat actions — **запрет** hardcoded `1000`/`2000`;
- не вычитать AP вручную после `AIPlayChangeStance` / `AIPlayCombatAction` (engine списывает сам);
- один BunkerDown-исход за ход execution (флаг `context.bunker_used`).

**3c. Конкуренты убрать**

- Удалить/заменить вызовы `TryChangeStance` в `AIPlayAttacks` на единый Disengage/BunkerDown.
- `AIExecuteUnitBehavior` → `… or AITakeCover(unit)`: либо no-op если `context.bunker_used`, либо делегировать в тот же BunkerDown helper (без второго независимого шанса).

После Disengage-move **нового Dump нет**. Overwatch fallback (`FallbackAction`) — только если не bunker’нулись и no sight, как отдельная ветка после 3b.
### Не делаем

| Идея | Почему |
| --- | --- |
| Leftover → полный Think | thrash |
| Свободный move-shoot-move-shoot | хаос |
| `dest ~= start` как proxy цикла | ломаный |
| Post-dump re-engage | конкурирует со «спрятался» |

## Контракт (при approve)

1. Удалить leftover-AP `"restart"`.
2. Dump: SoftDumpCap=4, бюджет `max_attacks`, одно действие/step.
3. DisengageReserveAP на Commit; после dump — cover-move (0..1) + **BunkerDown** (TakeCover/stance по приоритету); заменить `TryChangeStance`.
4. `"restart"` только vanilla-события.
5. После Disengage-move атак в том же PlayAttacks нет; `AITakeCover` хвост Execute не дублирует bunker.
6. `PickBestAttack` / correctness B / Weight² по REQ.
## Требования

- `JAZZ-AI-002-REQ-001` — leftover AP ≠ `"restart"`; Attack Dump с SoftDumpCap=4 и бюджетом `max_attacks`.
- `JAZZ-AI-002-REQ-002` — `"restart"` только target-change / MGPack / explicit status.
- `JAZZ-AI-002-REQ-003` — декремент `max_attacks` (fix typo).
- `JAZZ-AI-002-REQ-004` — `MatchUnit` → `GameState[state]`.
- `JAZZ-AI-002-REQ-005` — `PickBestAttack`: `InteractionRand`; `0 < total_cost <= AP` ок.
- `JAZZ-AI-002-REQ-006` — `visible` по team visibility.
- `JAZZ-AI-002-REQ-007` — aim_cost один раз на шаг.
- `JAZZ-AI-002-REQ-008` — reload всегда валидный `ammo`.
- `JAZZ-AI-002-REQ-009` — flare: флаг + init `target_pts`.
- `JAZZ-AI-002-REQ-010` — policies без двойного Weight.
- `JAZZ-AI-002-REQ-011` — dump retarget после каждого действия.
- `JAZZ-AI-002-REQ-012` — DisengageReserveAP (SoftDisengageTiles=2) когда dest без good cover.
- `JAZZ-AI-002-REQ-013` — после dump: optional один cover-move + BunkerDown (TakeCover → crouch-low → prone-open → PrefStance) с `GetStanceToStanceAP`; без hardcoded AP и без ручного double-spend.
- `JAZZ-AI-002-REQ-014` — `TryChangeStance` не остаётся параллельным end-turn путём; `AITakeCover` после Execute не дублирует уже выполненный bunker.
- `JAZZ-AI-002-REQ-015` — docs: Commit/Dump/Disengage/BunkerDown.
## Инварианты и ограничения

- Public ID archetype/behavior/policy без изменений.
- Load order AI-файлов без изменений.
- Только `InteractionRand` / существующий combat RNG.
- Только JAZZ overrides.
- Не пересекать `JAZZ-AI-001` write set по смыслу.
- Сохранить skip Unconscious / suppressionPinned и FastForward hook.

## Acceptance criteria

- `JAZZ-AI-002-AC-001` — static: leftover-restart удалён; Dump+Disengage на месте; `"restart"` только vanilla-события.
- `JAZZ-AI-002-AC-002` — static: max_attacks / MatchUnit / reload / flare / aim / visible по REQ.
- `JAZZ-AI-002-AC-003` — static: PickBestAttack без `math.random`.
- `JAZZ-AI-002-AC-004` — static: policies без Weight².
- `JAZZ-AI-002-AC-005` — runtime/human: дострел с той же клетки без второго Think-move; нет leftover-restart в логе.
- `JAZZ-AI-002-AC-006` — runtime/human: (а) выбег → выстрел → TakeCover/stance bunker; (б) выбег → две цели; (в) открытая клетка после выстрела → prone или cover-move+bunker без leftover-restart; kill+restart policy → re-Think; reload/flare без error.
- `JAZZ-AI-002-AC-007` — static: нет живых вызовов старого `TryChangeStance` end-turn path; stance cost только через engine AP API.
- `JAZZ-AI-002-AC-008` — docs обновлены.
## Impact и совместимость

- Vanilla/CLib/JAZZ: JAZZ last override; перепроверить FixAI пересечения.
- Saves: нет новой схемы.
- Network: меньше nondeterminism; outcomes AI изменятся.
- Generated data: нет.
- Cross-package: поведение без правок items; archetype MaxAttacks станет осмысленнее.
- Rollback: revert write set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (SsAnd)
- Дата: 2026-07-28

### Зафиксировано при approve

1. Commit → Dump → Disengage/BunkerDown (SoftDumpCap=4, SoftDisengageTiles=2).
2. После атаки с доступным cover — TakeCover приоритетно (не слабый RNG); без атаки — vanilla `TakeCoverChance`.
3. Weight²: снять Weight из Eval; `visible` по team visibility.
4. Archetype transitions / Re-engage — вне scope (follow-up specs).

## Evidence

- `JAZZ-AI-002-AC-001`: `PASS` — static: leftover-restart хвост удалён; Dump+Disengage/BunkerDown в `AIPlayAttacks`; `"restart"` только target-change/MGPack/status.
- `JAZZ-AI-002-AC-002`: `PASS` — static: `max_attacks` декремент; `MatchUnit`/`reload`/`flare`/`aim_cost`/`visible`+disengage reserve.
- `JAZZ-AI-002-AC-003`: `PASS` — static: `PickBestAttack` uses `InteractionRand`; `total_cost > AP` gate.
- `JAZZ-AI-002-AC-004`: `PASS` — static: Flanking/HighGround/IndoorsOutdoors raw×100 без Weight в Eval.
- `JAZZ-AI-002-AC-005`: `BLOCKED` — runtime/human: дострел без второго Think-move.
- `JAZZ-AI-002-AC-006`: `BLOCKED` — runtime/human: выбег→укрытие / две цели / prone-open; kill+restart; reload/flare.
- `JAZZ-AI-002-AC-007`: `PASS` — static: `TryChangeStance` → `JAZZ_AIBunkerDown`; stance via `GetStanceToStanceAP` / combat actions.
- `JAZZ-AI-002-AC-008`: `PASS` — static: `ai-awareness.md` обновлён под Commit/Dump/Disengage/BunkerDown.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — CombatAI / AIPlayAttacks / риски.
- Wiki не обязательна, если не формулируем отдельный player term.
