---
id: JAZZ-AI-ACT-004
status: approved
owner: project-owner
systems:
  - tactical-ai
  - combat-actions
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-ACT-004.md
  - jazz/Code/AiActions.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/metadata.lua
exclusive_resources:
  - none
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/specs/active/JAZZ-AI-002.md
  - docs/specs/active/JAZZ-AI-ACT-003.md
approved_by: project-owner
---

# JAZZ-AI-ACT-004: MG AI — Dump при permanent OW + приоритет ближних целей

## Проблема

Пулемётчики AI после `MGSetup` почти не стреляют и «игнорируют» угрозы в упоре: берут сектор на дальнюю цель, пока рядом стоит враг.

Корневая причина Dump: `JAZZ_AICanDump` режет весь Dump при любом `g_Overwatch[unit]` и `HasPreparedAttack()`. У MG сектор **permanent** (`OverwatchAction` behavior) → Dump не стартует на следующих ходах → `AIActionMGBurstFire` / basic fire не вызываются (vanilla `AIPlayAttacks` такого gate нет). Interrupts остаются единственным огнём.

Вторая часть: `AIEvalZones` считает врагов в конусе плоско (один `enemy_score`), без дистанции; Priority `AIActionMGSetup` часто выигрывает у прямой атаки по ближней цели.

## Цели

- Permanent MG/emplacement OW **не** блокирует Dump: stationed gunner может выбрать `AIActionMGBurstFire` / basic attack по целям в конусе (как vanilla).
- Временный (не-permanent) Overwatch / прочие prepared attacks по-прежнему блокируют Dump.
- При видимой близкой угрозе (≤ `JazzAI_MGCloseFireTiles`) первый `MGSetup` не ставится — Dump стреляет напрямую.
- Scoring зон MGSetup предпочитает конусы, покрывающие близких врагов; зоны, игнорирующие близких, штрафуются (rotate/pack вместо дальнего сектора).

## Non-goals

- Полный ребаланс `Legion_Machinegunner` / `Rebels_Machinegunner` Weight Positioning vs Standard (отдельный units change).
- Менять player `MGBurstFire` / cone filter / interrupt AP.
- ACT-003 halfcover predicate.
- Wiki/showcase (AI-only; player contract unchanged).

## Требования

- `JAZZ-AI-ACT-004-REQ-001` — `JAZZ_AICanDump`: если `g_Overwatch[unit].permanent`, Dump разрешён при AP/`max_attacks`; иначе сохраняются блоки `HasPreparedAttack` и non-permanent OW.
- `JAZZ-AI-ACT-004-REQ-002` — `AIActionMGSetup` (не stationed): при видимом враге в `JazzAI_MGCloseFireTiles` Precalc не планирует setup (нет `has_ap` / early return).
- `JAZZ-AI-ACT-004-REQ-003` — при eval зон MGSetup близкий враг в зоне получает score bonus; близкий видимый враг **вне** зоны даёт penalty зоне.
- `JAZZ-AI-ACT-004-REQ-004` — MGPack: (a) recovery если `StationedMachineGun` без OW; (b) **vanilla** pack+`restart` если Dump-секвенция с permanent OW **не** сделала attack (`not did_attack`) — иначе gunner залипает в тыловом секторе когда бой ушёл вперёд. Не паковать сразу после `MGSetup` в той же секвенции (`did_attack` от setup). ACT-003 halfcover path без регрессий; temporary OW по-прежнему не Dump-ит.

## Инварианты и ограничения

- Determinism: без нового `InteractionRand` в close/zone path.
- `CombatActionTargetFilters.MGBurstFire` (только конус при permanent) не менять — вне конуса сначала rotate/pack.
- Saves: ephemeral AI only.
- CommonLib: только override `AiActions.lua`.

## Acceptance criteria

- `JAZZ-AI-ACT-004-AC-001` — **static**: permanent-OW Dump gate; close-fire skip setup; zone close bonus/penalty present.
- `JAZZ-AI-ACT-004-AC-002` — **runtime/human S1**: stationed MG с врагом в конусе на своём ходу стреляет (`MGBurstFire` / Dump), не только interrupt.
- `JAZZ-AI-ACT-004-AC-003` — **runtime/human S2**: не-stationed MG с врагом ≤ close tiles — атакует, не ставит OW на дальнюю цель.
- `JAZZ-AI-ACT-004-AC-004` — **runtime/human S3**: stationed с близким вне конуса и дальним в конусе — rotate (или pack) к ближнему, не держит только дальний сектор.
- `JAZZ-AI-ACT-004-AC-005` — **runtime/human S4**: stationed в тылу, врагов в конусе нет (бой ушёл вперёд) — на своём ходу `MGPack` и replan, не остаётся «позади» до конца боя.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: восстанавливает Dump для permanent OW ближе к vanilla `AIPlayAttacks`.
- Saves / network: нет нового persistent contract; score детерминирован.
- Generated data: нет.
- Rollback: revert Code + docs + metadata bullet.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: see frontmatter

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (chat 2026-08-06: пулемётчики не стреляют / OW на дальнего при ближней угрозе — «надо чтоб в ближних он стрелял»)
- Дата: 2026-08-06

## Evidence

- `JAZZ-AI-ACT-004-AC-001`: `PASS` (static) — `JAZZ_AICanDump` permanent-OW exception; `JazzAI_MGPreferDirectFire` / close zone bonus+penalty; PositioningAI MGSetup score patch; pack-when-`not did_attack` in `Code/AiActions.lua`.
- `JAZZ-AI-ACT-004-AC-002`: `BLOCKED` — runtime/human S1.
- `JAZZ-AI-ACT-004-AC-003`: `BLOCKED` — runtime/human S2.
- `JAZZ-AI-ACT-004-AC-004`: `BLOCKED` — runtime/human S3.
- `JAZZ-AI-ACT-004-AC-005`: `BLOCKED` — runtime/human S4 (rear pack).

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — ACT-004 Dump permanent OW + close-fire MG doctrine.
- `docs/design/tactical-ai-archetypes.md` — MGSetup audit row ACT-004.
