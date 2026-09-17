---
id: JAZZ-WEAPONS-EMPLACEMENT-001
status: approved
owner: project-owner
systems:
  - weapons
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - Code/System_EmplacementAmmo.lua
  - Code/System_OR_Weapons.lua
  - Code/IModeCombatAreaAim.lua
  - Code/CombatAI.lua
  - docs/tools/_check_emplacement_target_distance.py
  - docs/tools/_audit_emplacement_cone_range.py
  - docs/tools/README.md
  - docs/specs/active/JAZZ-WEAPONS-EMPLACEMENT-001.md
  - docs/technical/systems/weapons-ammo-components.md
  - docs/technical/systems/combat-cth-actions.md
  - docs/technical/systems/file-coverage.md
  - docs/technical/override-matrix.md
  - docs/technical/weapons/combat-actions.md
  - docs/technical/weapons/accuracy-model.md
  - docs/wiki/combat-actions.md
  - docs/wiki/combat-and-accuracy.md
  - docs/showcase/ru/combat-actions.md
  - docs/showcase/en/combat-actions.md
  - docs/showcase/ru/combat-and-accuracy.md
  - docs/showcase/en/combat-and-accuracy.md
exclusive_resources:
  - none
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-WEAPONS-EMPLACEMENT-001: станковый сектор = MaxRange ствола × 45°

## Проблема

После COMBAT-009 `MinRange` пулемёта — 50% BDR. Vanilla `MachineGunEmplacement:Update` пишет `target_dist = MinRange`, а `OverwatchAction` / `GetMaxAimRange` дополнительно режут сектор зрением. На картах с коротким authored `target_dist` все станки остаются короткими. Когда длину подняли до MaxRange, COMBAT-009 сжал угол до классовой полоски (~2° у Browning на 95 клетках). Нужна длинная дальность **и** фиксированная ширина 45°.

## Цели

- У каждого `MachineGunEmplacement` runtime-длина сектора = `WeaponRange` / `GetOverwatchConeParam("MaxRange")` ствола.
- Угол сектора станка = **45°** (`45 * 60` engine minutes), не COMBAT-009 `1/d` и не `OverwatchAngle` карточки.
- Переносной Overwatch / MGSetup / MGRotate с рук не менять.

## Non-goals

- Правка `WeaponRange` / `BulletDropRange` / `OverwatchAngle` предметов, формулы CTH, Map Editor preview, геометрия карт.

## Требования

- `JAZZ-WEAPONS-EMPLACEMENT-001-REQ-001` — superseded REQ-004: map `target_dist` больше не задаёт длину боевого сектора.
- `JAZZ-WEAPONS-EMPLACEMENT-001-REQ-002` — сохранить ammo remap, один wrapper Update / EndInteraction, штатное поведение при отсутствии оружия.
- `JAZZ-WEAPONS-EMPLACEMENT-001-REQ-004` — runtime `Jazz_EmplacementConeDist` всегда возвращает MaxRange ствола (не map slider, не MinRange, не sight). Update (вне editor / вложенного updating), EndInteraction и Idle reseat ставят этот dist. `Overwatch.GetMaxAimRange` без зрения только если `emplacement_weapon` или `ManningEmplacement`; иначе ванильный Min(range, sight).
- `JAZZ-WEAPONS-EMPLACEMENT-001-REQ-005` — `Jazz_EmplacementConeAngle` = 45°. `JazzOwApplyPlacedCone`, `Firearm:GetAreaAttackParams` (Overwatch/MGSetup/MGRotate при `emplacement_weapon`), aim preview (`IModeCombatAreaAim`) и AI-зона (`CombatAI`) для станка берут этот угол, не `GetOverwatchConeAngle(d)`.

## Инварианты и ограничения

- Без правок карт и предметов. Editor preview по-прежнему ванильный MinRange. Portable Overwatch остаётся с COMBAT-009 + sight в `GetMaxAimRange`. Один wrap `GetMaxAimRange` (install-once, base только ваниль). `GetOverwatchConeAngle` глобально не менять.

## Acceptance criteria

- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-001` — Lua-harness: любой authored `target_dist` после Update становится MaxRange ствола (95×slab); ammo remap; повторный Update не укорачивает; editor/reentry не трогаем; `Jazz_EmplacementConeAngle() == 2700`.
- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-002` — в игре занятие любого станка даёт длинный сектор по дальности ствола и ширину **45°** (не 155° у упора и не 2° на пределе); save/load; переносной MGSetup/Overwatch как раньше.

## Impact и совместимость

- Vanilla `MachineGunEmplacement.Update` остаётся основой. Runtime `target_dist` после Update = MaxRange ствола; `g_Overwatch.cone_angle` на станке = 45°.
- Saves: без миграции; уже поставленный `g_Overwatch` обновляется при reseat / повторном занятии.
- Network/determinism: без RNG. Generated data: нет. Карты не меняем.
- Rollback: вернуть helper к clamp map dist; снять wrap `GetMaxAimRange`; убрать фиксацию 45°.

## План и ownership

- Пакет jazz; write set выше; exclusive resources none. Независимая игровая приёмка после Lua-harness.

## Решение владельца

- approved: project-owner, 2026-09-16: проблема во **всех** стационарных пулемётах; дальность должна быть существенной (MaxRange ствола), не слайдер карты и не зрение; другое оружие не трогать.
- approved: project-owner, 2026-09-17: при существующей длине держать ширину **45°**.

## Evidence

- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-001`: `PASS` — `_audit_emplacement_cone_range.py` PASSED; `_check_emplacement_target_distance.py` PASS (любой authored dist → 95×slab=114000; `Jazz_EmplacementConeAngle()==2700`; повторный Update; ammo remap; editor/reentry; EndInteraction). `_check_lua_wrap_cycles.py` OK. Статический анализ, не runtime.
- `JAZZ-WEAPONS-EMPLACEMENT-001-AC-002`: `BLOCKED` — живой прогон владельца (длина MaxRange + ширина 45°).

## Documentation delta

- technical: weapons-ammo-components, combat-cth-actions, combat-actions, accuracy-model, file-coverage, override-matrix.
- wiki + showcase RU/EN: combat-actions, combat-and-accuracy.

`REQ-003` (сохранять authored map dist в диапазоне) superseded `REQ-004`.
