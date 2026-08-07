---
id: JAZZ-WEAPONS-008
status: approved
owner: project-owner
systems:
  - weapons-ammo-components
  - combat-cth-actions
repositories:
  - jazz
risk: medium
generated_data: true
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/InventoryItem/*.lua
  - jazz/InventoryItem/JAZZ_AMMO_*.lua
  - jazz/items.lua
  - jazz/metadata.lua
  - jazz/docs/tools/_rebalance_recoil_physical.py
  - jazz/docs/tools/_soften_ammo_jam.py
  - jazz/docs/tools/_tmp_audit_smg_jam_feedback.py
  - jazz/docs/tools/_audit_weapon_jam_balance.py
  - jazz/docs/tools/README.md
  - jazz/docs/design/recoil-physical-scale.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/data/weapons.csv
  - jazz/docs/technical/weapons/accuracy-model.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-008.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-001
  - JAZZ-WEAPONS-003
approved_by: project-owner
---

# JAZZ-WEAPONS-008: ПП Recoil authoring fix + soft jam (Discord)

## Проблема

1. Все active `SubmachineGun` залипли на `Recoil=18`: family floor 18 + битые `WeaponMass=80` / `WeaponSizeClass=Long` в CSV/companions. Дифференциация 9×19 из WEAPONS-003 (Sterling < MP5 < Compact/high-RPM) не читается; средний AR (~17) мягче любого ПП.
2. Poor/Crafted ammo + wear×4 при ≤80% дают слишком частый клин даже механикам (Discord: «шанс клина с дерьмовыми патронами запредельный»).

## Цели

1. Восстановить физические mass/RPM/size для всех active ПП; пересчитать `Recoil`/`Burst`/`Auto`.
2. Family floor для SMG = **12** (как AR), не 18; порядок MicroUZI > MP5K ≥ Carbine mid ≥ Sterling.
3. Чуть смягчить jam: wear multipliers и Poor/Crafted `BaseJamChance`/`Reliability` без смены шкалы JamScore 0..1000.

## Non-goals

- Смена retention `/100`, Mechanical `/120`, single-shot `/2`.
- Ребаланс Damage/AP/FMJ/Match.
- Runtime Mass/RPM в CTH.
- Полный ребаланс всех калибров recoil (только SMG authoring + floor/auto_max bug).

## Требования

- `JAZZ-WEAPONS-008-REQ-001` — active SubmachineGun: реалистичные `WeaponMass` (десятые кг), `CyclicRPM`, `WeaponSizeClass` ∈ Compact|Carbine; нет mass=80+Long placeholder; CSV + companion + items согласованы.
- `JAZZ-WEAPONS-008-REQ-002` — SMG Recoil floor 12; 9×19 order: MicroUZI > MP5K и MicroUZI > Sterling; Sterling < MP5A2 или близкий mid Carbine.
- `JAZZ-WEAPONS-008-REQ-003` — якоря WEAPONS-003: AK74∈[14,15], AKM∈[24,26], FNFAL∈[42,44] сохранены.
- `JAZZ-WEAPONS-008-REQ-004` — historical wear multipliers:
  >80×1, ≤80×3, ≤60×6, ≤40×12, ≤15×18; **superseded by
  JAZZ-WEAPONS-010**, which uses separate additive condition and
  permanent-wear steps.
- `JAZZ-WEAPONS-008-REQ-005` — `*_Crafted` BaseJamChance **140** (было 200), Rel **−18** (было −25); `*_Poor` pistol/SMG calibers BaseJamChance **≈2/3** прежнего (9×19: 120, Rel −10); rifle Poor ≈70 jam / Rel −4.
- `JAZZ-WEAPONS-008-REQ-006` — historical perfect-condition exception:
  serviceable 0%, Poor 10%, Crafted 15%; **superseded by
  JAZZ-WEAPONS-010**, где Reliability снова влияет на исправный ствол,
  а общий базовый риск ограничен 10%.
- `JAZZ-WEAPONS-008-REQ-007` — docs: technical jam tiers + design recoil note; wiki/showcase кратко про идеальное состояние, Poor/Crafted и ПП-дифференциацию.

## Инварианты и ограничения

- JamScore 0..1000; display `/10`; Mechanical merc `/120`; ammo mods via Reload `AddModifier`.
- Mass/RPM не читаются повторно в CTH runtime.

## Acceptance criteria

- `JAZZ-WEAPONS-008-AC-001` — static: `_audit_recoil_dist.py` PASS (anchors + MicroUZI>MP5K,Sterling); active SMG Recoil не все равны 18.
- `JAZZ-WEAPONS-008-AC-002` — static: no active SubmachineGun with WeaponMass≥70 and Size Long.
- `JAZZ-WEAPONS-008-AC-003` — historical static acceptance for
  multipliers 3/6/12/18; superseded by JAZZ-WEAPONS-010-AC-001/002.
- `JAZZ-WEAPONS-008-AC-004` — static: Crafted jam+140 Rel−18; 9×19 Poor jam+120 Rel−10; `_validate_items_quick.py` OK.
- `JAZZ-WEAPONS-008-AC-005` — human/runtime: очередь ПП различается; Poor клинит заметно, но не «каждый второй burst» на Mech~80 fresh gun.
- `JAZZ-WEAPONS-008-AC-006` — historical perfect-condition audit;
  superseded by the additive-curve audit in JAZZ-WEAPONS-010.

## Impact и совместимость

- Vanilla/CLib: only JAZZ overrides/data.
- Saves: existing weapons keep instance Condition; new Recoil from class defs on load.
- Generated: items + InventoryItem + CSV transaction.

## План и ownership

- Пакет-владелец: `jazz`.
- Исполнитель: agent.
- Reviewer: project-owner/runtime playtest.
- Declared write set: frontmatter `write_set`.
- Exclusive resources: `jazz/items.lua` для generated-data волн; текущая perfect-condition правка `items.lua` не меняет.

## Решение владельца

- Статус: approved (historical jam decision from 2026-08-06 is superseded
  by the owner-approved JAZZ-WEAPONS-010 contract from 2026-08-07).
- Исполнитель: agent.

## Evidence

- `JAZZ-WEAPONS-008-AC-001`: `PASS` — static: `_audit_recoil_dist.py` PASS; SMG Recoil set `{12,13,14,17,18,19,21}`
- `JAZZ-WEAPONS-008-AC-002`: `PASS` — static: no active SMG mass≥70 / Long after apply
- `JAZZ-WEAPONS-008-AC-003`: `PASS (historical, superseded by
  JAZZ-WEAPONS-010)` — former multipliers 3/6/12/18 were implemented.
- `JAZZ-WEAPONS-008-AC-004`: `PASS` — static: Crafted 140/−18; 9×19 Poor 120/−10; `_validate_items_quick.py` OK
- `JAZZ-WEAPONS-008-AC-005`: `BLOCKED` — runtime/human playtest
- `JAZZ-WEAPONS-008-AC-006`: `PASS (historical, superseded by
  JAZZ-WEAPONS-010)` — former perfect-condition contract was implemented
  before runtime balance evidence replaced it.

status note: recoil scope remains approved/runtime-pending; jam multiplier and
perfect-condition sub-scope is superseded by JAZZ-WEAPONS-010.

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — wear tiers
- `docs/design/recoil-physical-scale.md` — SMG floor 12 + placeholder fix note
- `docs/wiki/weapons-and-ammo.md` + showcase RU/EN — brief
