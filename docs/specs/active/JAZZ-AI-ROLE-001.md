---
id: JAZZ-AI-ROLE-001
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
  - jazz/docs/specs/active/JAZZ-AI-ROLE-001.md
  - jazz/docs/design/tactical-ai-archetypes.md
  - jazz/docs/technical/systems/ai-awareness.md
  - jazz/docs/technical/systems/legion-units-equipment-tiers.md
  - jazz-units/items.lua
  - jazz-units/metadata.lua
  - jazz-units/UnitData/JAZZ_Legion_Flanker*.lua
  - jazz-units/UnitData/RebelFlanker.lua
exclusive_resources:
  - jazz-units/items.lua
  - jazz-units/metadata.lua
related_decisions:
  - docs/design/tactical-ai-archetypes.md
approved_by: project-owner
---

# JAZZ-AI-ROLE-001: Legion/Rebels_Flanker как первоклассный archetype

## Проблема

Семья Flanker (`JAZZ_Legion_FlankerT*`, `RebelFlanker`) существует в UnitData, но **нет** public `AIArchetype` ID. Юниты сидят на `Legion_Assaulter` / `Legion_Frontliner` / `Rebels_Assaulter`, а фланговая тактика — keyword-ветки внутри чужих presets. Игрок не читает «разведчик обходит» как отдельную роль.

Design source: `docs/design/tactical-ai-archetypes.md` (F1).

## Цели

- Зарегистрировать `Legion_Flanker` и `Rebels_Flanker` как `ModItemAIArchetype`.
- Все Flanker UnitData и `RebelFlanker` ссылаются на эти ID (base + `RepositionArchetype`).
- Flank-primary PositioningAI / OptLoc с высоким `AIPolicyFlanking` живут в Flanker presets; Assaulter/Frontliner больше не несут Flank-only behavior с Weight ~1000 как основную ветку для keyword `Flank`.
- Technical docs отражают четвёртый faction template (Flanker ≠ Machinegunner).

## Non-goals

- Shared `PickCombatStance` / panic tiers / melee AP-reach (ROLE-002).
- TakeCover threat-weight / Proximity closer_better (POL-001).
- Officer aura, LowVis multipliers, anti-peek, smoke LOS-break, Medic freeze.
- Смена Assault/Front UnitData archetype.
- Adonis/Army/Thug retarget.
- Mass regenerate unrelated items.lua noise.

## Требования

- `JAZZ-AI-ROLE-001-REQ-001` — существуют public archetype ID `Legion_Flanker` и `Rebels_Flanker`, зарегистрированные в `jazz-units` metadata resources.
- `JAZZ-AI-ROLE-001-REQ-002` — каждый `JAZZ_Legion_FlankerT*` companion имеет `archetype` и `RepositionArchetype` = `Legion_Flanker` (если Reposition задан).
- `JAZZ-AI-ROLE-001-REQ-003` — `RebelFlanker` использует `Rebels_Flanker`.
- `JAZZ-AI-ROLE-001-REQ-004` — Flanker preset: Behaviors/OptLoc ориентированы на flank (высокий `AIPolicyFlanking`, keyword `Flank` не обязателен для основного PositioningAI «Flanker AI»), signature включают MobileShot/RunAndGun/Basic/grenade-smoke/flare; TakeCover weight ниже Assaulter frontline hold.
- `JAZZ-AI-ROLE-001-REQ-005` — `Legion_Assaulter` / `Legion_Frontliner` / Rebel зеркала: убрать или сильно ослабить Flank-only PositioningAI с Weight ≥1000 / RequiredKeywords только `Flank` или `Nova` label «Flanker AI», чтобы фланговая роль не дублировалась.
- `JAZZ-AI-ROLE-001-REQ-006` — `items.lua` + `metadata.lua` + companions в одной транзакции; sync-аудит без orphan ID.

## Инварианты и ограничения

- Не ломать `Legion_Assaulter` / `Frontliner` / `Machinegunner` для Assault/Front/Gunner UnitData.
- Determinism: не вводить `math.random` в AI.
- Public ID новых archetype стабильны; rename только отдельным spec.
- Editor round-trip желателен; если недоступен — пометить AC runtime/editor `BLOCKED` с инструкцией владельцу.

## Acceptance criteria

- `JAZZ-AI-ROLE-001-AC-001` — static: `rg` / metadata содержат Id `Legion_Flanker` и `Rebels_Flanker` как `AIArchetype`.
- `JAZZ-AI-ROLE-001-AC-002` — static: все 6 `JAZZ_Legion_Flanker*` + `RebelFlanker` указывают на новый archetype.
- `JAZZ-AI-ROLE-001-AC-003` — static: sync check `jazz-units` без missing companion/resource для новых Id.
- `JAZZ-AI-ROLE-001-AC-004` — runtime/human: в бою с FlankerT2_Scout (или Recon) юнит использует archetype `Legion_Flanker` (лог/Ged); движение чаще на flank threat, чем лобовой кластер Assaulter на той же карте.
- `JAZZ-AI-ROLE-001-AC-005` — docs: `ai-awareness.md` faction table включает Flanker; `legion-units-equipment-tiers.md` колонка Archetype у Flanker* = `Legion_Flanker`.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только generated presets + UnitData refs в jazz-units; core CombatAI не обязателен в этом spec.
- Saves: юниты в бою получат новый archetype при следующем StartAI; старые saves ок.
- Network/determinism: без нового RNG.
- Generated data: да, jazz-units transaction.
- Cross-package: jazz docs only; maps не трогаем.
- Rollback: revert branch / удалить два preset и вернуть UnitData refs.

## План и ownership

- Пакет-владелец данных: `jazz-units`; docs: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: см. frontmatter.
- Exclusive resources: `jazz-units/items.lua`, `metadata.lua`.

## Решение владельца

- Статус: **approved** (промежуточный дизайн `tactical-ai-archetypes.md` принят владельцем 28 июля 2026; «всё согласовано» для старта ветки `feature/tactical-ai-roles`).
- Кто подтвердил: project-owner.
- Дата: 2026-07-28.

## Evidence

- `JAZZ-AI-ROLE-001-AC-001`: `PASS` — static: `items.lua` id `Legion_Flanker` / `Rebels_Flanker`; `metadata.lua` ModResourcePreset оба Id.
- `JAZZ-AI-ROLE-001-AC-002`: `PASS` — static: 6× `JAZZ_Legion_Flanker*` + `RebelFlanker` companions и items chunks → `Legion_Flanker` / `Rebels_Flanker`; `RepositionArchetype` исправлен (camel case).
- `JAZZ-AI-ROLE-001-AC-003`: `PASS` (ROLE-001 scope) — новые archetype Id и Flanker UnitData согласованы items/metadata/companion. Полный `check-generated-sync` jazz-units сейчас **FAILED** из‑за **посторонних** orphan `UnitData/Jazz_*.lua` mercs (не write set ROLE-001).
- `JAZZ-AI-ROLE-001-AC-004`: `PASS` (human, 2026-07-29) — в бою видны `Legion_Flanker`; часть скаутов кратко на `Legion_Assaulter` через динамический `PickCustomArchetype` (ожидаемо до ROLE-002). Крашей нет.
- `JAZZ-AI-ROLE-001-AC-005`: `PASS` — обновлены `ai-awareness.md` (35 ID, строка Flanker) и `legion-units-equipment-tiers.md` (колонка Flanker*).

## Documentation delta

- `docs/technical/systems/ai-awareness.md` — faction templates + Flanker.
- `docs/technical/systems/legion-units-equipment-tiers.md` — Archetype = `Legion_Flanker`.
- `docs/design/tactical-ai-roles-playtest.md` — playtest.
- `docs/design/tactical-ai-archetypes.md` — design (F12 Night≠Fog отдельно).

## Playtest (для владельца)

См. `docs/design/tactical-ai-roles-playtest.md`.
