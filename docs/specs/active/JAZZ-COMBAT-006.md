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

# JAZZ-COMBAT-006: Bullet Hell — снаряды с CTH и JAZZ-подавлением

## Проблема

Сигнатура Спайка `BulletHell` — vanilla cone **AlwaysHits AOE**: урон и статусы `Suppressed` / `SuppressionChangeStance` идут из `GetAreaAttackResults`, а веер пуль (`BulletHellOverwriteShots`) в основном косметический. В JAZZ это:

1. обходит обычный Firearm CTH / броню / graze;
2. вешает **vanilla** подавление вместо Will → `suppressionLight`…`suppressionPinned`.

Playtest: нужен конус прицеливания, но **реальные прожектайлы** с шансом попасть и корректным JAZZ-подавлением.

## Цели

- Конусный aim UI сохраняется (`AimType = cone`).
- Урон — только от Firearm-пуль (CTH, броня, LoF), не от AlwaysHits AOE.
- Подавление — только JAZZ Will pipeline (`QueueSuppressionApplication` / `ApplySuppressionStatus`); без `applied_status` vanilla `Suppressed` / `SuppressionChangeStance`.
- Расход патронов в диапазоне vanilla `min_ammo`…`max_ammo` (15…30).
- Gate АН-94 / `JAZZ_LargeAutoFire` (уже в `main`) не регрессирует.

## Non-goals

- Менять `JAZZ_VovaVist`, `DanceForMe`, `JAZZ_TargetSweep` (кроме отсутствия регрессий).
- Новый public CombatAction ID / переименование перка.
- Баланс-пасс урона за пределами «убрать гарантированный AOE».
- Переписывать общий suppression formula.

## Требования

- `JAZZ-COMBAT-006-REQ-001` — `CombatActions.BulletHell.AlwaysHits = false`; `GetActionResults` не задаёт `aoe_action_id` / `aoe_damage_bonus` / `applied_status` для AOE-урона.
- `JAZZ-COMBAT-006-REQ-002` — исполнение: снаряды по врагам в конусе (round-robin), каждый выстрел — обычный Firearm shot с CTH; AP сигнатуры списывается один раз.
- `JAZZ-COMBAT-006-REQ-003` — Will-подавление как у обычного огня (`suppressionbonus` сигнатуры ≥ базового); без forced vanilla `Suppressed`.
- `JAZZ-COMBAT-006-REQ-004` — пустой конус / нет валидных выстрелов → refund AP, без signature recharge.
- `JAZZ-COMBAT-006-REQ-005` — docs: technical + wiki + showcase RU/EN описывают projectile model.

## Инварианты и ограничения

- Public id `BulletHell`, SignatureAbilities group, recharge UX.
- Deterministic NetSync через существующие `FirearmAttack` shot rolls.
- Не ломать `GetUIState` autofire gate (`AutoFire` / `MGBurstFire` / `AbakanAutoFire` / `JAZZ_LargeAutoFire`).

## Acceptance criteria

- `JAZZ-COMBAT-006-AC-001` — static: wrap/override без AlwaysHits AOE path; `Unit:BulletHell` projectile dump present.
- `JAZZ-COMBAT-006-AC-002` — runtime/human: Спайк с АН-94/MG в конусе с врагами — пули с промахами/попаданиями; Will-тиры, не иконка vanilla Suppressed от AOE.
- `JAZZ-COMBAT-006-AC-003` — runtime/human: пустой конус → AP возвращены, сигнатура не уходит в recharge.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: override `Unit:BulletHell` + CombatAction props/results в JAZZ only.
- Saves: нет нового save state.
- Network/determinism: те же FirearmAttack RNG.
- Generated data: false (Code-only).
- Cross-package: Spike perk в jazz-units без изменений.
- Rollback: revert Code + docs.

## План и ownership

- Пакет-владелец: `jazz`
- Declared write set: см. frontmatter
- Exclusive resources: none

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (вариант A + fix suppression; Discord playtest)
- Дата: 2026-08-08

## Evidence

- `JAZZ-COMBAT-006-AC-001`: `PASS (static)` — `Unit:BulletHell` dump + `JazzInstallBulletHellProjectiles` (`AlwaysHits=false`, clear AOE/`applied_status`); `docs/tools/_check_bullethell_projectiles.py`
- `JAZZ-COMBAT-006-AC-002`: `BLOCKED` — runtime/human
- `JAZZ-COMBAT-006-AC-003`: `BLOCKED` — runtime/human

## Documentation delta

- `docs/technical/weapons/combat-actions.md` — BulletHell projectile + Will suppression
- `docs/wiki/combat-actions.md` / showcase RU+EN — player-facing
- `docs/tools/_check_bullethell_projectiles.py` + README
