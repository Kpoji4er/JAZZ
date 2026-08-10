---
id: JAZZ-WEAPONS-012
status: approved
owner: project-owner
systems:
  - combat-cth-actions
  - weapons-ammo-components
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/AccuracyRangeCTH.lua
  - jazz/Code/System_OR_Unit.lua
  - jazz/CharacterEffect/GrizzlyPerk.lua
  - jazz/items.lua
  - jazz/Russian.csv
  - jazz/English.csv
  - jazz/scripts/test-shooting-model.ps1
  - jazz/docs/technical/systems/combat-cth-actions.md
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/wiki/combat-and-accuracy.md
  - jazz/docs/wiki/combat-actions.md
  - jazz/docs/showcase/ru/combat-and-accuracy.md
  - jazz/docs/showcase/en/combat-and-accuracy.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-012.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-003
  - JAZZ-WEAPONS-009
approved_by: project-owner
---

# JAZZ-WEAPONS-012: пулемёт без опоры — CTH + отдача

## Проблема

После отключения flat `Autofire` CTH-штрафа стоячий hipfire из `MachineGun`/`LightMachineGun` оставляет первую пулю почти как с упора; class recoil ×1.35/×1.15 слабо чувствуется на короткой очереди и смягчается miss→graze. Гризли «Off the Hip» описывает снятие Setup-штрафа, которого больше нет.

## Цели

- Без опоры: first-bullet CTH-штраф, режется Силой; тяжёлые сильнее лёгких.
- Без опоры: recoil class_factor ×2.0 (`MachineGun`) / ×1.5 (`LightMachineGun`).
- Сигнатурный CombatAction `GrizzlyPerk`: полный игнор обоих unsupported-штрафов; обычный `MGBurstFire` Гризли — нет.
- UI показывает фактор «Без опоры».

## Non-goals

- Возврат старого distance-scaled `Autofire` modifier (`if true then return false`).
- Смена authored `Recoil`/`BurstShots`/`Damage` стволов.
- Отдельный standing-only CTH-штраф сверх «без опоры».
- Изменение suppression / MGSetup AP / permanent OW.

## Требования

- `JAZZ-WEAPONS-012-REQ-001` — опора = permanent OW / `attack_args.deployed` / `BipodUnfolded` / prone+bipod `ShotsBeforeRecoilProne` (тот же predicate, что recoil support).
- `JAZZ-WEAPONS-012-REQ-002` — без опоры base CTH penalty: `MachineGun` **−50**, `LightMachineGun` **−25**; `penalty = MulDivRound(base, Max(0, 100 − Strength), 100)`; фактор через `JAZZ_CTHPercentToFactor`.
- `JAZZ-WEAPONS-012-REQ-003` — без опоры recoil `class_factor`: MG **2.0**, LMG **1.5** (замена прежних 1.35/1.15); cumbersome non-MG **1.10** без изменений.
- `JAZZ-WEAPONS-012-REQ-004` — только `action.id == "GrizzlyPerk"` → penalty 0 и class_factor 1 без опоры; `HasPerk` сам по себе не снимает штраф с `MGBurstFire`.
- `JAZZ-WEAPONS-012-REQ-005` — текст `GrizzlyPerk` описывает игнор штрафа без опоры на сигнатурной атаке + 2× long burst + полный урон (без −50% dmg), не мёртвый Autofire CTH.
- `JAZZ-WEAPONS-012-REQ-006` — technical + wiki + showcase RU/EN обновлены в том же change set.

## Инварианты и ограничения

- Первая пуля и хвост используют один support predicate.
- Сила в CTH-штрафе; Marksmanship не режет unsupported CTH (остаётся в core / recoil shooter_factor).
- Публичные ID CombatAction/perk не меняются.
- RNG order атаки не меняется.

## Acceptance criteria

- `JAZZ-WEAPONS-012-AC-001` — static: MG Str0 unsupported → −50; Str100 → 0; Str50 → −25; LMG base −25 с той же шкалой.
- `JAZZ-WEAPONS-012-AC-002` — static: unsupported recoil class_factor 2.0 / 1.5; supported → 1.0; signature `GrizzlyPerk` → 1.0 unsupported; `MGBurstFire` у носителя перка всё ещё 2.0/1.5.
- `JAZZ-WEAPONS-012-AC-003` — automated: `scripts/test-shooting-model.ps1` PASS.
- `JAZZ-WEAPONS-012-AC-004` — human/runtime: crosshair «Без опоры» на стоячем MG без Setup; после MGSetup/bipod строка исчезает; на сигнатуре Гризли строки нет, на его обычной очереди — есть.
- `JAZZ-WEAPONS-012-AC-005` — docs: combat-cth-actions + accuracy-model + wiki/showcase combat-and-accuracy согласованы.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: только JAZZ CTH/recoil helpers и perk text.
- Saves: миграция не нужна.
- Network/determinism: без нового RNG.
- Generated data: точечный `GrizzlyPerk` Description в `items.lua` + companion.
- Cross-package: нет.
- Rollback: откат change set.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner.
- Declared write set: front matter.
- Exclusive resources: `items.lua`.

## Решение владельца

- Статус: `approved`
- Кто подтвердил: project-owner (Discord hipfire + «−50», recoil ×2/×1.5, Гризли игнор **только сигнатурой**, LMG слабее)
- Дата: 2026-08-08

## Evidence

- `JAZZ-WEAPONS-012-AC-001`: `PASS` — static: constants −50/−25; formula `MulDivRound(base, Max(0,100−Str), 100)` in `JAZZ_CTHGetUnsupportedFirePenalty`.
- `JAZZ-WEAPONS-012-AC-002`: `PASS` — static: class_factor 2.0/1.5; signature `action.id == "GrizzlyPerk"` returns 1; no `HasPerk(..., "GrizzlyPerk")`.
- `JAZZ-WEAPONS-012-AC-003`: `PASS` — automated: `scripts/test-shooting-model.ps1`.
- `JAZZ-WEAPONS-012-AC-004`: `BLOCKED` — runtime/human playtest.
- `JAZZ-WEAPONS-012-AC-005`: `PASS` — docs updated (technical/wiki/showcase).

## Documentation delta

- `docs/technical/systems/combat-cth-actions.md`
- `docs/technical/weapons/accuracy-model.md`
- `docs/technical/weapons/combat-actions.md` (GrizzlyPerk)
- `docs/wiki/combat-and-accuracy.md`, `docs/wiki/combat-actions.md`
- `docs/showcase/ru|en/combat-and-accuracy.md`
