---
id: JAZZ-AI-ACT-005
status: approved
owner: project-owner
systems:
  - tactical-ai
  - combat-actions
repositories:
  - jazz
  - jazz-units
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-ACT-005.md
  - jazz/Code/AiActions.lua
  - jazz/Code/CombatAI.lua
  - jazz/Code/System_OR_Unit.lua
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/tools/_audit_ai_mobile_shot.py
  - jazz/docs/tools/_audit_ai_rng_wiring.py
  - jazz/docs/tools/_apply_ai_act005_mobile_signatures.py
  - jazz/docs/tools/README.md
  - jazz/metadata.lua
  - jazz-units/items.lua
  - jazz-units/metadata.lua
exclusive_resources:
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - docs/design/tactical-ai-archetypes.md
  - docs/technical/weapons/combat-actions.md
  - docs/specs/active/JAZZ-AI-002.md
  - docs/specs/active/JAZZ-AI-003.md
approved_by: project-owner
---

# JAZZ-AI-ACT-005: AI mobile resolve + real AvailableAttacks in PickBestAttack

## Проблема

1. `MatchUnit` режет `RunAndGun`/`BurstFire`/`AutoFire` по `unit.ui_actions` → AI почти не берёт RnG.
2. Мобильные signatures хардкодят `action_id` / keywords (`Control`) вместо выбора по оружию.
3. Gate не смотрит реальный `AvailableAttacks` → возможен RnG на болтовке с keyword `Control`.
4. `GetBasicAttackModes` / `PickBestAttack` знают только Single/Burst/Auto/Buck/Dual — Zipper, Sweep, DoubleTap и прочие class techniques из `AvailableAttacks` в Dump не попадают.

## Цели

- Огневой availability gate по оружию + `GetUIState`, не `ui_actions`.
- `AIActionMobileShot` сам резолвит mobile ID по оружию.
- `GetBasicAttackModes` возвращает **реальные** enabled атаки из `AvailableAttacks` (кроме mobile / positional / utility).
- Не-mobile абилки из этого пула идут через `PickBestAttack` (Dump); тюнинг весов/перков — later.
- Болтовка без mobile ID не проходит mobile signature.

## Non-goals

- Perk-unlock class techniques (будущий слой; сейчас всё, что уже в `AvailableAttacks` + enabled).
- Tier-scaling весов.
- Массовое добавление отдельных Signature PlaceObj на каждый `JAZZ_*`.
- Player CTH/AP/recharge; wiki/showcase.

## Требования

- `JAZZ-AI-ACT-005-REQ-001` — `JazzAI_IsAttackActionAvailable(unit, action_id)`: активное оружие; ID в `AvailableAttacks` **или** (`RunAndGun` + `EnableRunNGun`); `CombatActions[id]:GetUIState({unit}) == "enabled"`. Не читать `ui_actions`.
- `JAZZ-AI-ACT-005-REQ-002` — `JazzAI_ResolveMobileAttackId(unit)` приоритет: `JAZZ_MobileShotgun` → `RunAndGun` → `RunAndGun_Carbine` → `MobileShot` (каждый через REQ-001; `EnableRunNGun` → кандидат `RunAndGun`).
- `JAZZ-AI-ACT-005-REQ-003` — `AISignatureAction:MatchUnit`: для `AIActionMobileShot` — resolve ≠ false; для прочих с `action_id` в `CombatActions` — REQ-001; GameState/keywords без регрессии AI-002.
- `JAZZ-AI-ACT-005-REQ-004` — wrap `AIActionMobileShot` Precalc/Execute: подставить resolved ID (не оставлять stale preset `action_id` если оружие другое); restore preset field после Precalc.
- `JAZZ-AI-ACT-005-REQ-005` — `Unit:GetBasicAttackModes`: `result.all` = все ID из `AvailableAttacks` с REQ-001 true, **кроме** mobile set и exclude-list (`MGSetup`/`MGPack`/`Overwatch`/`PinDown`/`Reload`/…). Сохранить named keys single/burst/auto/… где есть.
- `JAZZ-AI-ACT-005-REQ-006` — `PickBestAttack`: для неизвестных mode ID оценивать shots (autofire helper / heuristic); не дропать class techniques из-за отсутствия ветки Burst/Auto.
- `JAZZ-AI-ACT-005-REQ-007` — `jazz-units`: убрать `RequiredKeywords={"Control"}` с mobile RnG entries; mobile keyword `RunAndGun`/`MobileShot` не обязателен для weapon gate (можно снять с mobile PlaceObj).
- `JAZZ-AI-ACT-005-REQ-008` — determinism: без нового RNG; без Selection/UI refresh.

## Инварианты и ограничения

- Не ломать AI-002 Commit/Dump/Disengage, AI-003 sticky, ACT-003/004 MG.
- Не менять player `GetUIState` семантику.
- Saves ephemeral; generated data `jazz-units` одной транзакцией.

## Acceptance criteria

- `JAZZ-AI-ACT-005-AC-001` — **static**: helpers + MatchUnit без `ui_actions`; mobile resolve priority; GetBasicAttackModes iterates AvailableAttacks.
- `JAZZ-AI-ACT-005-AC-002` — **static**: units — нет Control keyword на mobile RnG PlaceObj.
- `JAZZ-AI-ACT-005-AC-003` — **static**: non-mobile ID в AvailableAttacks попадает в `basic_attacks.all` path (code).
- `JAZZ-AI-ACT-005-AC-004` — **runtime/human**: SMG Flanker/Assaulter использует RnG заметно чаще.
- `JAZZ-AI-ACT-005-AC-005` — **runtime/human**: FrontT1 Rifleman (болтовка) не исполняет RunAndGun.
- `JAZZ-AI-ACT-005-AC-006` — **runtime/human**: Dump может выбрать class technique из AvailableAttacks (напр. Zipper на ПП), не только Burst/Auto.
- `JAZZ-AI-ACT-005-AC-007` — docs sync.

## Impact и совместимость

- Vanilla/CLib/JAZZ: MatchUnit + GetBasicAttackModes + PickBestAttack + MobileShot wrap.
- Cross-package: runtime `jazz`, data `jazz-units`.

## План и ownership

- Пакет-владелец: `jazz` (+ `jazz-units` data)
- Исполнитель: agent
- Reviewer: project-owner

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (chat 2026-08-10: real AvailableAttacks; all abils now; non-mobile via PickBestAttack; perk/tier later)
- Дата: 2026-08-10

## Evidence

- `JAZZ-AI-ACT-005-AC-001`: `PASS` (static) — helpers + MatchUnit without `ui_actions`; mobile resolve; GetBasicAttackModes iterates AvailableAttacks; PickBestAttack estimates class-technique shots.
- `JAZZ-AI-ACT-005-AC-002`: `PASS` (static) — `_apply_ai_act005_mobile_signatures.py` removed 20 RequiredKeywords blocks; audit Control on mobile = 0.
- `JAZZ-AI-ACT-005-AC-003`: `PASS` (static) — `GetBasicAttackModes` adds non-mobile enabled AvailableAttacks into `result.all`.
- `JAZZ-AI-ACT-005-AC-004`: `BLOCKED` — runtime/human SMG RnG frequency.
- `JAZZ-AI-ACT-005-AC-005`: `BLOCKED` — runtime/human bolt Rifleman no RnG.
- `JAZZ-AI-ACT-005-AC-006`: `BLOCKED` — runtime/human Dump class technique pick.
- `JAZZ-AI-ACT-005-AC-007`: `PASS` (static) — `ai-awareness.md` + design archetypes row.

## Documentation delta

- `docs/technical/systems/ai-awareness.md`
- `docs/design/tactical-ai-archetypes.md`
- `docs/tools/README.md`
