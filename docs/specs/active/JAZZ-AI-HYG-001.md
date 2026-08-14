---
id: JAZZ-AI-HYG-001
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
  - jazz/docs/specs/active/JAZZ-AI-HYG-001.md
  - jazz/docs/technical/technical-debt.md
  - jazz/docs/technical/override-matrix.md
  - jazz/Code/CombatAI.lua
  - jazz/Code/AiActions.lua
  - jazz/Code/AIBehaviours.lua
  - jazz/Code/UnitAwareness.lua
exclusive_resources:
  - none
related_decisions:
  - docs/technical/technical-debt.md
approved_by: project-owner 2026-08-14 implement in order
---

# JAZZ-AI-HYG-001: Careful CombatAI fork unwrap

## Проблема

JAZZ держит крупные копии vanilla `CombatAI` / `AiActions` / `UnitAwareness`, чтобы не запутаться в точечных правках. Соседний нетронутый ванильный текст отстаёт от патчей JA3 и CommonLib (`AISelectAction`, `AIChooseSignatureAction`, `UpdateSuspicion`). Это долг, не фича.

Владелец: вычищать **можно, но аккуратно**; так уже делалось руками.

## Цели

- Правило сопровождения: при правке функции, где JAZZ меняет узкий кусок, выносить JAZZ в wrap/`rawget` поверх текущей vanilla/CLib, а не держать соседние сотни строк «на всякий случай».
- Один символ за change set. Перед unwrap — трёхстороннее сравнение vanilla ModTools Src + CommonLib `FixAI.lua` + JAZZ.
- Обновлять override-matrix в том же коммите.

## Non-goals

- Большой PR «вычистить CombatAI.lua».
- Смешивать unwrap с CMD-002 / PERF-002 / POL-* в одном коммите.
- Менять наблюдаемое поведение «заодно» (если поведение должно измениться — отдельный spec).
- Трогать `items.lua` / archetypes / UnitData.

## Требования

- `JAZZ-AI-HYG-001-REQ-001` — разрешённый метод: (1) найти функцию, где diff vs vanilla/CLib локальный; (2) сохранить JAZZ-логику как wrap вокруг `g_JAZZ_*Base` / поздней CLib; (3) удалить только доказанно идентичный ванильный хвост; (4) `NetUpdateHash` / сигнатура без изменения, если spec поведения нет.
- `JAZZ-AI-HYG-001-REQ-002` — запрещено в этом spec: массовый delete, переименование публичных `AI*` без matrix, смена load order, правки `AISelectAction` / `UpdateSuspicion` без отдельного approved behavior spec (высокий CLib риск).
- `JAZZ-AI-HYG-001-REQ-003` — каждый unwrap-коммит: запись в `override-matrix.md` + строка в `technical-debt.md` «Крупные копии vanilla» (что снято).
- `JAZZ-AI-HYG-001-REQ-004` — не стартовать unwrap, пока в том же working tree незакоммичены CMD-002 / PERF-002 code changes.

## Инварианты и ограничения

- Поведение до/после unwrap совпадает при одинаковом save/seed, кроме явно описанного в другом spec.
- Детерминизм и MP hashes не меняются unwrap’ом.
- Образец уже в дереве: wrap `AIScoreReachableVoxels` (SNIPER-001) — повторять этот паттерн, не копировать модуль целиком.

## Acceptance criteria

- `JAZZ-AI-HYG-001-AC-001` — spec + debt/matrix правило записаны (этот файл + technical-debt абзац HYG-001).
- `JAZZ-AI-HYG-001-AC-002` — каждый будущий unwrap: static diff функции ≤ заявленного символа; matrix обновлён.
- `JAZZ-AI-HYG-001-AC-003` — human: после unwrap нет регресса StartAI / Dump на одном знакомом бою (owner smoke, не чеклист «done» заранее).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: цель — **меньше** коллизий, не новые.
- Saves: none, если поведение не меняется.
- Network/determinism: hashes должны совпасть с pre-unwrap на одном replay, иначе FAIL и откат.
- Generated data: none.
- Rollback: revert одного символа.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent, только когда функция и так в write set **или** owner явно сказал «unwrap X»
- Reviewer: project-owner
- Не feature-gate для CMD-002 / PERF-002.

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (2026-08-14) — «реализовывай все спеки по очереди»; unwrap не в одном дереве с PERF/CMD code.
- Дата: 2026-08-14

## Evidence

- `JAZZ-AI-HYG-001-AC-001`: `PASS` — static: this spec + `docs/technical/technical-debt.md` HYG-001 process paragraph + `override-matrix.md` unwrap rule. No CombatAI unwrap in this working tree (REQ-004).
- `JAZZ-AI-HYG-001-AC-002`: `BLOCKED` — нет unwrap-коммита (намеренно; следующий символ — отдельный change set).
- `JAZZ-AI-HYG-001-AC-003`: `BLOCKED` — human: owner smoke after a future unwrap.

## Documentation delta

- `docs/technical/technical-debt.md` — ссылка на HYG-001 как процесс, не как «уже вычищено»
- `docs/technical/override-matrix.md` — только вместе с фактическим unwrap
