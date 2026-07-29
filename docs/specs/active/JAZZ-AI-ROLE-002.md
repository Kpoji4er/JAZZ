---
id: JAZZ-AI-ROLE-002
status: approved
owner: project-owner
systems:
  - tactical-ai
  - jazz-units-archetypes
repositories:
  - jazz
  - jazz-units
risk: high
generated_data: true
runtime_validation: required
write_set:
  - jazz/docs/specs/active/JAZZ-AI-ROLE-002.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/design/tactical-ai-roles-playtest.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz-units/Code/AICombatStance.lua
  - jazz-units/metadata.lua
  - jazz-units/UnitData/JAZZ_Legion_*.lua
  - jazz-units/UnitData/Rebel*.lua
  - jazz-units/items.lua
exclusive_resources:
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - docs/design/tactical-ai-archetypes.md
approved_by: project-owner
---

# JAZZ-AI-ROLE-002: Shared combat stance (F2–F4, F9, F11) + PickCustom migration

## Проблема

Legion/Rebel `PickCustomArchetype` — copy-paste с мёртвым panic (`local panicshance`), сломанным CQB weapon chain, фикс. 8/10 тайлов вместо AP-reach melee, Hide/ChangeWeapon side-effects, без F2 Flank↔Press.

## Цели

- Shared `JazzAI_PickCombatStance` в `jazz-units/Code/AICombatStance.lua`.
- F2 NeedPush/NeedFlank; F4+F9 melee secondary AP-reach; F3+F11 panic tiers; убрать Hide из PickCustom.
- Тонкие PickCustom у Legion + Rebel UnitData (ROLE-003 включён в ту же миграцию).
- Bonemaker: Medic switch через тот же helper (`allow_medic`).

## Non-goals

- Officer aura writer (CMD-001).
- Medic freeze Bandage fail-safe (MED-001) — только early switch helper.
- POL-002 anchors, CTX LowVis, ACT smoke/OW.

## Требования

- `JAZZ-AI-ROLE-002-REQ-001` — `AICombatStance.lua` зарегистрирован в `metadata.lua` code.
- `JAZZ-AI-ROLE-002-REQ-002` — Flanker\* default Flanker; NeedPush → Assaulter. Assault\* default Assaulter; NeedFlank → Flanker. Prefix Legion_/Rebels_ по Affiliation.
- `JAZZ-AI-ROLE-002-REQ-003` — Melee только при MeleeWeapon в alt slot + `CanReachMeleeAndAttackOnce` (не фикс. тайлы); NeverMelee для Sniper/MG/Heavy/Ordnance без Melee keyword.
- `JAZZ-AI-ROLE-002-REQ-004` — Panic: T1–T2 полная формула без shadowing; T3 cap 10%; T4/Merc ≈0; Rebels ×0.6 (F11).
- `JAZZ-AI-ROLE-002-REQ-005` — Нет `Hide()` в PickCustom; ChangeWeapon только при реальном оружии в alt.
- `JAZZ-AI-ROLE-002-REQ-006` — Companions + items.lua PickCustom синхронизированы для затронутых Id.

## Инварианты и ограничения

- Determinism: только `unit:Random` уже используемый для panic; NeedPush/NeedFlank без нового RNG.
- Leaders: helper no-op (return base archetype) до CMD-001.
- Не ломать base `archetype` / `RepositionArchetype` из ROLE-001.

## Acceptance criteria

- `JAZZ-AI-ROLE-002-AC-001` — static: metadata содержит `Code/AICombatStance.lua`; `JazzAI_PickCombatStance` определён.
- `JAZZ-AI-ROLE-002-AC-002` — static: Legion Flanker/Assault/Front PickCustom вызывают helper; нет `local panicshance` shadowing; нет `Hide()` в PickCustom.
- `JAZZ-AI-ROLE-002-AC-003` — static: Rebel\* без universal `dist < 10` → Melee; вызывают helper.
- `JAZZ-AI-ROLE-002-AC-004` — docs: ai-awareness + playtest ROLE-002.
- `JAZZ-AI-ROLE-002-AC-005` — runtime/human: panic T1 виден; T4 почти нет; knife Roughneck режет при AP-reach; Scout Push→Assaulter.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jazz-units Code + UnitData + items; jazz docs.
- Saves: ок.
- Network/determinism: NeedPush/NeedFlank без RNG; panic через `unit:Random`.
- Generated data: companions + items PickCustom sync.
- Cross-package: Units зависит от helper в своём пакете.
- Rollback: revert helper + PickCustom.

## План и ownership

- Пакет-владелец: `jazz-units`; docs: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: `jazz-units/items.lua`, `metadata.lua`.

## Решение владельца

- Статус: **approved** — «доделаем все, потом смоки» 29.07.2026; промежуточный дизайн принят.
- Кто подтвердил: project-owner.
- Дата: 2026-07-29.

## Evidence

- `JAZZ-AI-ROLE-002-AC-001`: `PASS` — static: `metadata.lua` + `items.lua` ModItemCode `AICombatStance`; `JazzAI_PickCombatStance` в `Code/AICombatStance.lua`.
- `JAZZ-AI-ROLE-002-AC-002`: `PASS` — static: Legion Assault/Front/Flanker/Gunner/Heavy/Recruit PickCustom → helper; нет `Hide()` / shadowed panic в этих companions.
- `JAZZ-AI-ROLE-002-AC-003`: `PASS` — static: Rebel\* PickCustom → helper (ROLE-003 в той же миграции); нет universal Melee@10 в companions.
- `JAZZ-AI-ROLE-002-AC-004`: `PASS` — ai-awareness §12 + playtest ROLE-002.
- `JAZZ-AI-ROLE-002-AC-005`: `BLOCKED` — runtime/smoke владельца.

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — пункт 12 stance helper.
- `docs/design/tactical-ai-roles-playtest.md` — ROLE-002 smokes.
- `docs/design/tactical-ai-archetypes.md` — checklist.
