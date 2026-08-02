---
id: JAZZ-WEAPONS-006
status: implemented
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
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/AmmoRolloverHint.lua
  - jazz/InventoryItem/*.lua
  - jazz/InventoryItem/vanillunique/*.lua
  - jazz/items.lua
  - jazz/docs/specs/active/JAZZ-WEAPONS-006.md
  - jazz/docs/specs/active/JAZZ-WEAPONS-003.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/combat-actions.md
  - jazz/docs/technical/weapons/data/weapons.csv
  - jazz/docs/tools/_rebalance_recoil_physical.py
  - jazz/docs/tools/_fix_shotgun_pellet_autoshots.py
  - jazz/docs/tools/_apply_buckshot_projectiles.py
  - jazz/docs/tools/README.md
  - jazz/docs/wiki/weapons-and-ammo.md
  - jazz/docs/wiki/combat-actions.md
  - jazz/docs/showcase/ru/weapons-and-ammo.md
  - jazz/docs/showcase/en/weapons-and-ammo.md
  - jazz/docs/showcase/ru/combat-actions.md
  - jazz/docs/showcase/en/combat-actions.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
related_specs:
  - JAZZ-WEAPONS-003
approved_by: project-owner
---

# JAZZ-WEAPONS-006: `BuckshotProjectiles` — отдельная база дроби

## Проблема

1. Разлёт дроби в `Firearm:GetAttackResults` (`System_OR_Weapons.lua`) берёт `num_shots = self.AutoShots` для `Shotgun`.
2. 12g патроны (`Buckshot` / `Birdshot` / `Saltshot` / …) модифицируют `AutoShots` через `CaliberModification` (`mod_mul` 9000 → ×9 картечи при базе 1).
3. `JAZZ-WEAPONS-003` authorит `AutoShots = 0` при отсутствии `AutoFire`. Apply обнулил базу дробовиков → `0 × mul = 0` дробин → **0 урона**, выстрел мёртвый (playtest 2026-08-03).
4. Hotfix `AutoShots = 1` на всех SG конфликтует с WEAPONS-003 и смешивает «длину автоочереди» с «числом дробин».

## Цели

1. Ввести / закрепить публичное свойство **`BuckshotProjectiles`** (modifiable) — база числа дробин на один патрон.
2. Runtime Buckshot / DoubleBarrel / CancelShotCone (и UI damage) читают **`BuckshotProjectiles`**, не `AutoShots`.
3. 12g ammo `CaliberModification` переносит `target_prop` с `AutoShots` на `BuckshotProjectiles` (те же `mod_mul` / семантика).
4. Authored shotguns: `BuckshotProjectiles = 1`; `AutoShots` / `BurstShots` снова по WEAPONS-003 (обычно 0 без AutoFire/BurstFire).
5. `_rebalance_recoil_physical` не трогает `BuckshotProjectiles` и не держит SG-исключение `AutoShots=1`.
6. Docs/wiki/showcase sync.

## Non-goals

- Возврат cone-AOE `FillConeAttackAoeParams` / `aoe_action_id` для Buckshot.
- Баланс числа дробин / урона патронов (только wiring; mul остаются: Buckshot 9000, Birdshot/Saltshot 20000).
- Новые типы патронов 12g.
- AI policy сверх уже существующего чтения `BuckshotProjectiles` в `System_OR_Unit`.
- Менять `BuckshotConeAngle` / choke effects.

## Контракт свойства

```text
BuckshotProjectiles  # FirearmProperties, modifiable, template
  default authored on Shotgun: 1
  effective = MulDivRound(base + mod_add, mod_mul, 1000)   # vanilla CaliberModification scale
  Buckshot ammo mod_mul=9000  → 9 pellets at base 1
  Birdshot/Saltshot mod_mul=20000 → 20 pellets at base 1
  Slug / APSlug: no AutoShots/BuckshotProjectiles mul (1 projectile via damage path)
```

`AmmoRolloverHint` label **«Дробь»** / EN pellet label binds to `BuckshotProjectiles` (не `AutoShots`).

## Требования

- `JAZZ-WEAPONS-006-REQ-001` — `BuckshotProjectiles` объявлен на `FirearmProperties` (`modifiable=true`, default 1, editor number).
- `JAZZ-WEAPONS-006-REQ-002` — `GetAttackResults`: для `Shotgun` `num_shots = self.BuckshotProjectiles` (DoubleBarrel по-прежнему ×2 поверх этого).
- `JAZZ-WEAPONS-006-REQ-003` — CombatAction `Buckshot` / `DoubleBarrel` / `CancelShotCone` `GetActionResults` / `GetActionDamage` / description используют `BuckshotProjectiles` (fallback ≥1, не `AutoShots or 12`).
- `JAZZ-WEAPONS-006-REQ-004` — все live 12g ammo mods, что целили `AutoShots`, целят `BuckshotProjectiles`.
- `JAZZ-WEAPONS-006-REQ-005` — все active `Shotgun` companions: `BuckshotProjectiles = 1`; `AutoShots`/`BurstShots` соответствуют WEAPONS-003 (не пеллетная база).
- `JAZZ-WEAPONS-006-REQ-006` — CSV колонка `buckshot_projectiles`; tooling apply/export; recoil physical script не обнуляет пеллеты через AutoShots.
- `JAZZ-WEAPONS-006-REQ-007` — technical + wiki + showcase RU/EN описывают дробь через `BuckshotProjectiles`.
- `JAZZ-WEAPONS-006-REQ-008` — пакет дробин (`Buckshot` / `DoubleBarrel` / `CancelShotCone` / `BuckshotBurst` внутри одного выстрела) **не** очередь: каждая дробина имеет **одинаковый** CTH = шанс первой пули; **нет** recoil retention между дробинами (`JAZZ_CTHGetBulletChance` с index 1 / без profile).

## Инварианты и ограничения

- Deterministic pellet count from authored base + ammo mods (no RNG length).
- WEAPONS-003 RPM→Auto/Burst остаётся для нарезного; дробовики без AutoFire снова `AutoShots=0`.
- Пеллетный пакет ≠ autofire: recoil/CTH decay между дробинами запрещён.
- Не ломать slug (одно тело без mul на projectiles).
- Exclusive `items.lua` — не параллелить с другими WEAPONS-* writes.
- Saves: новое поле default 1; старые сейвы без поля → default / companion reload.

## Acceptance criteria

- `JAZZ-WEAPONS-006-AC-001` — static: ни один active Shotgun companion не имеет `AutoShots` как единственный источник дроби; у всех `BuckshotProjectiles = 1` (или >0).
- `JAZZ-WEAPONS-006-AC-002` — static: `GetAttackResults` / Buckshot CombatAction не читают `AutoShots` для pellet count; ammo mods `target_prop = "BuckshotProjectiles"`.
- `JAZZ-WEAPONS-006-AC-003` — static: `_rebalance_recoil_physical.authored_profile` для Shotgun даёт `auto=0` (нет AutoFire) и **не** пишет `BuckshotProjectiles`.
- `JAZZ-WEAPONS-006-AC-004` — runtime/human: R870 + картечь в прицеле показывает ненулевой урон (ожид. ~9×base с mods) и выстрел расходует 1 патрон / наносит урон.
- `JAZZ-WEAPONS-006-AC-005` — docs: technical combat-actions + weapons-ammo-components + wiki/showcase обновлены.
- `JAZZ-WEAPONS-006-AC-006` — static: в `GetAttackResults` pellet_pack ветка вызывает `JAZZ_CTHGetBulletChance(..., 1, nil, ...)`; нет `shot_cth` cap по `i > 1` для Buckshot.

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: JAZZ property + OR_Weapons override; AI уже ожидал `BuckshotProjectiles`.
- Saves: безопасный default 1.
- Network/determinism: тот же multishot braid, другое source поле.
- Generated data: InventoryItem companions + `items.lua` CombatAction funcs + ammo companions; CSV.
- Cross-package: none.
- Rollback: revert property wiring + ammo target_prop + AutoShots=1 hotfix.

## План и ownership

- Пакет-владелец: `jazz`
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: см. frontmatter
- Exclusive resources: `jazz/items.lua`

## Решение владельца

- Статус: `approved` (чат 2026-08-03: «делай спек и реализовывай»)
- Кто подтвердил: project-owner
- Дата: 2026-08-03

## Evidence

- `JAZZ-WEAPONS-006-AC-001`: `PASS` — static `docs/tools/_verify_buckshot_projectiles.py` (12 SG companions + CSV `buckshot_projectiles=1`, `auto_shots=0`).
- `JAZZ-WEAPONS-006-AC-002`: `PASS` — static verify: `GetAttackResults` + CombatAction + ammo `target_prop=BuckshotProjectiles`.
- `JAZZ-WEAPONS-006-AC-003`: `PASS` — static: `_rebalance_recoil_physical` shotgun Auto=0; no AutoShots=1 exception.
- `JAZZ-WEAPONS-006-AC-004`: `PASS` — human: владелец подтвердил в бою («все ок», 2026-08-03).
- `JAZZ-WEAPONS-006-AC-005`: `PASS` — technical + wiki + showcase RU/EN обновлены в этом change set.
- `JAZZ-WEAPONS-006-AC-006`: `PASS` — static: `pellet_pack` + bullet_index 1 / nil recoil_profile в `System_OR_Weapons.lua`.

## Documentation delta

- `docs/technical/weapons/combat-actions.md` — Buckshot читает `BuckshotProjectiles`.
- `docs/technical/systems/weapons-ammo-components.md` — свойство + ammo mods.
- `docs/technical/weapons/data/weapons.csv` — колонка.
- `docs/wiki/` + `docs/showcase/ru|en` — игрок: число дробин от патрона/ствола, не «автоочередь».
- `JAZZ-WEAPONS-003` — пометка: дробь не через AutoShots (см. 006).
