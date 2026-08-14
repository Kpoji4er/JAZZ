---
id: JAZZ-COMBAT-006
status: implemented
owner: project-owner
systems:
  - combat-cth-actions
  - armor-damage-wounds-will
  - weapons
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/CombatActions.lua
  - Code/System_OR_Weapons.lua
  - Code/ExecFirearmAttacks.lua
  - docs/specs/active/JAZZ-COMBAT-006.md
  - docs/technical/weapons/combat-actions.md
  - docs/wiki/combat-actions.md
  - docs/showcase/ru/combat-actions.md
  - docs/showcase/en/combat-actions.md
  - docs/tools/_check_bullethell_projectiles.py
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-COMBAT-006: Bullet Hell — снаряды по дуге конуса с CTH

> **v2 2026-08-12 (owner):** «как раньше» = `FirearmAttack` (стреляет), но **реальные прожектайлы по дуге** конуса с CTH: попадают в тех, кто в секторе; промахи могут шально задеть. Не SingleShot round-robin dump (v1 FAIL playtest).

## Проблема

Сигнатура Спайка `BulletHell` — vanilla cone **AlwaysHits AOE**: урон и статусы `Suppressed` / `SuppressionChangeStance` идут из `GetAreaAttackResults`, а веер пуль (`BulletHellOverwriteShots`) в основном косметический. В JAZZ это:

1. обходит обычный Firearm CTH / броню / graze;
2. вешает **vanilla** подавление вместо Will → `suppressionLight`…`suppressionPinned`.

Playtest: нужен конусный прицел **и** реальные пули по дуге с шансом попасть / шальными.

## Цели

- Конусный aim UI + исполнение через `FirearmAttack` (как vanilla wiring).
- Урон — Firearm-пули с CTH; aim points размазаны по дуге **до** LoF (не только FX).
- Попадание по юнитам в луче дуги; промахи — обычный stray/LoF.
- Подавление — JAZZ Will **всем врагам в конусе** (не только попадания); без AOE `applied_status` vanilla Suppressed.
- Расход `min_ammo`…`max_ammo` (15…30); AN94 / `JAZZ_LargeAutoFire` gate.

## Non-goals

- Менять `JAZZ_VovaVist`, `DanceForMe`, `JAZZ_TargetSweep`.
- Новый public CombatAction ID.
- SingleShot round-robin dump (v1 superseded).

## Требования

- `JAZZ-COMBAT-006-REQ-001` — `AlwaysHits = false`; GetActionResults без AOE-урона / `applied_status`.
- `JAZZ-COMBAT-006-REQ-002` — `Unit:BulletHell` → `FirearmAttack`; дуга в `GetAttackResults` (`jazz_bh_arc_sprayed`) до LoF.
- `JAZZ-COMBAT-006-REQ-003` — Will-подавление **всем врагам в конусе** (не только primary / не только попадания); без forced vanilla Suppressed AOE.
- `JAZZ-COMBAT-006-REQ-004` — docs technical + wiki + showcase RU/EN.

## Acceptance criteria

- `JAZZ-COMBAT-006-AC-001` — static: FirearmAttack + Install wrap + arc spray flag; check script.
- `JAZZ-COMBAT-006-AC-002` — runtime/human: конус с врагами — пули по дуге, промахи/попадания/шальные; Will-тиры.
- `JAZZ-COMBAT-006-AC-003` — runtime/human: AN94/MG gate не регрессирует.

## Решение владельца

- Статус: approved (v2)
- Кто: project-owner — FirearmAttack + real arc projectiles + strays (2026-08-12)
- v1 dump: superseded FAIL

## Evidence

- `JAZZ-COMBAT-006-AC-001`: `PASS (static)` — `docs/tools/_check_bullethell_projectiles.py`
- `JAZZ-COMBAT-006-AC-002` / `AC-003`: `BLOCKED` — runtime/human
- **Hotfix 2026-08-15:** vanilla leftover `target = SetTerrainZ(far)` + CTH at cone-max (`GetMin/MaxAimRange` = `WeaponRange`) made honest JAZZ CTH 0% and miss-rays ignore the primary / climb into the sky. CTH now vs resolved unit at their range; miss-rays can still hit anyone in the sector; no recoil-climb on the cone spray. Cone-wide Will via `JazzCollectBulletHellConeEnemies` (same total as primary × shot count).

## Documentation delta

- `docs/technical/weapons/combat-actions.md`, wiki, showcase RU+EN
- `_check_bullethell_projectiles.py`
