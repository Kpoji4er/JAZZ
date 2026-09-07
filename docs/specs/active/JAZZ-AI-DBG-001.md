---
id: JAZZ-AI-DBG-001
status: implemented
owner: project-owner
systems:
  - tactical-ai
repositories:
  - jazz
risk: low
generated_data: true
runtime_validation: required
write_set:
  - docs/specs/active/JAZZ-AI-DBG-001.md
  - Code/AiDebugLog.lua
  - Code/AiActions.lua
  - items.lua
  - metadata.lua
  - docs/technical/systems/ai-awareness.md
  - docs/technical/systems/file-coverage.md
  - docs/tools/_check_ai_dbg_001.py
  - docs/tools/README.md
exclusive_resources:
  - items.lua
  - metadata.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-AI-DBG-001: финальные решения ИИ в боевом журнале

## Проблема

На ходе врага не видно, почему юнит остался, куда пошёл и какой шанс
попадания заложил в выстрел. Странные ходы приходится угадывать по
анимации. Нужен узкий лог конечных решений в Snype / боевом журнале,
а не дамп скоринга.

## Цели

- Тумблер в настройках мода `AIDebugLog`, default **off**.
- При включении в боевой журнал (`CombatLog` short, виден в Snype) пишутся
  только финальные решения: dest (кто, куда, почему, ОД до/после хода),
  совершённая атака/signature (режим, цель, CTH, остаток ОД), один обрыв
  если выстрел планировался и не состоялся.
- Выключенный тумблер не пишет в журнал и не меняет dest/атаку/AP.

## Non-goals

- Дамп кандидатов dest, весов политик, Precalc, PERF-логов.
- Второй wrap `AIPlayAttacks` / `AIScoreReachableVoxels`.
- Животные (`JazzAI_UsesJazzCombatAI` false).
- PDA-тред Snype, floating bark, смена скоринга.
- Wiki / showcase (отладочная опция, не боевая механика).

## Требования

- `JAZZ-AI-DBG-001-REQ-001` — `ModItemOptionToggle` `AIDebugLog`, default
  `false` в `metadata.default_options` и в самом toggle.
- `JAZZ-AI-DBG-001-REQ-002` — helper `Code/AiDebugLog.lua`; `CombatLog`
  только если `CurrentModOptions.AIDebugLog == true`.
- `JAZZ-AI-DBG-001-REQ-003` — одна dest-строка на активацию в
  `AIExecuteUnitBehavior` после lock `ai_destination`: имя, роль/директива,
  stay/move + причина (hold / perch / peel-OW / medic / to-shot /
  reposition / stay), ОД сейчас→на dest, цель и `dest_cth` если уже есть.
- `JAZZ-AI-DBG-001-REQ-004` — одна строка на совершённый Dump / signature /
  melee: действие, aim если есть, цель, CTH из уже посчитанного
  `best_attack.cth` / `dest_cth` (без нового `CalcChanceToHit`), остаток ОД.
- `JAZZ-AI-DBG-001-REQ-005` — если Dump/melee не выстрелил, одна abort-строка
  с уже поставленной причиной (`no-target` / `no-lof` / `no-team-vis` /
  `no-ap`) и остатком ОД. Не писать abort без причины.
- `JAZZ-AI-DBG-001-REQ-006` — fallback `closest_dest` логируется как dest
  с причиной `closest`. Скоринг, dest и AP не меняются.

## Инварианты и ограничения

- Опция по умолчанию выключена.
- Нет нового wrap на уже обёрнутые AI-символы.
- Нет новых GameVar/MapVar; abort-причина только в `ai_context`.
- CTH только из уже посчитанных полей контекста / `PickBestAttack`.
- Не больше трёх типов строк на юнита за активацию (dest, атаки, abort).
- Generated data: одна транзакция `items.lua` + `metadata.lua` +
  companion `Code/AiDebugLog.lua`.

## Acceptance criteria

- `JAZZ-AI-DBG-001-AC-001` — static: toggle `AIDebugLog` default false;
  `metadata.default_options.AIDebugLog = false`.
- `JAZZ-AI-DBG-001-AC-002` — static: `CombatLog` в `AiDebugLog.lua` только
  за `JazzAI_DebugLogEnabled`; файл в `metadata.code` и `items.lua`.
- `JAZZ-AI-DBG-001-AC-003` — static: `AiActions.lua` зовёт dest/attack/abort
  helpers; нет второго wrap `AIPlayAttacks`; нет дампа `dest_target_score`.
- `JAZZ-AI-DBG-001-AC-004` — static: `docs/tools/_check_ai_dbg_001.py` exit 0.
- `JAZZ-AI-DBG-001-AC-005` — sync: `items.lua` / `metadata.lua` /
  `Code/AiDebugLog.lua` согласованы (option + code).

## Impact и совместимость

- Vanilla/CLib/JAZZ: только чтение уже принятого dest/атаки + CombatLog.
- Saves: нет.
- Network/determinism: лог не участвует в решениях; CTH/dest не пересчитываются.
- Generated data: да (option + ModItemCode).
- Cross-package: нет.
- Rollback: revert write set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: items.lua, metadata.lua

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (запрос: отладка ИИ в Snype, только
  конечные решения, тумблер в настройках мода)
- Дата: 2026-09-08

## Evidence

- `JAZZ-AI-DBG-001-AC-001`: `PASS` (static) — `items.lua` `AIDebugLog` DefaultValue false; `metadata.default_options.AIDebugLog = false`.
- `JAZZ-AI-DBG-001-AC-002`: `PASS` (static) — `CombatLog` only in `JazzAI_DebugLogEnabled` path (`lSay`); `Code/AiDebugLog.lua` in items + metadata.code.
- `JAZZ-AI-DBG-001-AC-003`: `PASS` (static) — dest/attack/abort hooks in `AiActions.lua`; two `AIPlayAttacks` defs (body + existing ACT-002 wrap); no dest-score dump.
- `JAZZ-AI-DBG-001-AC-004`: `PASS` (static) — `python docs/tools/_check_ai_dbg_001.py` exit 0.
- `JAZZ-AI-DBG-001-AC-005`: `PASS` (static) — option + ModItemCode + `Code/AiDebugLog.lua` + metadata.code/default_options; `_validate_items_quick.py` OK.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — модуль и опция.
- `docs/technical/systems/file-coverage.md` — `AiDebugLog.lua` loaded.
- Wiki / showcase не обновляются: отладочный тумблер, не боевая механика.
