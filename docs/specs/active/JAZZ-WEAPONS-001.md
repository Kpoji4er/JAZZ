---
id: JAZZ-WEAPONS-001
status: implemented
owner: project-owner
systems:
  - weapons-ammo-components
  - combat-cth-actions
repositories:
  - jazz
risk: medium
generated_data: false
runtime_validation: required
write_set:
  - jazz/Code/System_OR_Weapons.lua
  - jazz/Code/System_OR_Grenade.lua
  - jazz/Code/System_Firearm_AddProperties.lua
  - jazz/Code/GetScrapParts.lua
  - jazz/Code/WeaponClasses.lua
  - jazz/Code/AmmoRolloverHint.lua
  - jazz/items.lua
  - jazz/docs/specs/active/JAZZ-WEAPONS-001.md
  - jazz/docs/technical/systems/weapons-ammo-components.md
  - jazz/docs/technical/weapons/accuracy-model.md
exclusive_resources:
  - jazz/items.lua
related_decisions:
  - none
approved_by: project-owner
---

# JAZZ-WEAPONS-001: клин, scrap, Handling hide

## Проблема

Шанс клина считается на смешанной float-шкале со сломанными ступенями износа и непрозрачным влиянием Mechanical. Приведённый `%` в ammo rollover (`BaseJamChance / 10`) не совпадает с фактическим roll. Scrap штрафует Condition дважды. Heavy weapons игнорируют `DegradePerShot` из-за позднего override. Legacy `Handling` («Эргономика») всё ещё влияет на CTH и overwatch, хотя по CTH-контракту должен быть inert; удалять поле нельзя — ломает сейвы.

## Цели

- единая integer-шкала JamScore `0..1000` = единицы roll; display `%` = `DivRound(score, 10)`;
- rollover показывает приведённый jam `%`; окно модификации — Reliability;
- Mechanical сильно снижает клин пропорционально, не обнуляя любой ствол flat-вычетом;
- скрыть Эргономику из CTH и overwatch, сохранив сериализованное поле `Handling`;
- исправить scrap, heavy degrade, grouping integer path и мёртвый `ExtraBurstShots` noop.

## Non-goals

- массовый ребаланс `BaseJamChance` / `Reliability` / удаление `Handling` из InventoryItem;
- перепрошивка component effects `*Handling*` на другие статы;
- rewrite `Firearm:GetAttackResults` / полный CTH;
- FX/sounds/maps/units.

## Требования

- `JAZZ-WEAPONS-001-REQ-001` — JamScore ∈ `[0, 1000]`; `jam_roll < score` с `attacker:Random(1000)`; display `%` = `DivRound(score, 10)`.
- `JAZZ-WEAPONS-001-REQ-002` — condition multipliers: `>80` ×1, `<=80` ×4, `<=60` ×8, `<=40` ×16, `<=15` ×24 via `elseif`.
- `JAZZ-WEAPONS-001-REQ-003` — Mechanical reduces score proportionally (merc `/120` + small secondary; AI `/150`); single shot halves score via `DivRound`.
- `JAZZ-WEAPONS-001-REQ-004` — ammo rollover keeps `BaseJamChance/10` as `%`; modify UI keeps Reliability only.
- `JAZZ-WEAPONS-001-REQ-005` — `Handling` property and data remain; CTH modifier `Handling` returns false; overwatch cone uses only `OverwatchAngle`.
- `JAZZ-WEAPONS-001-REQ-006` — scrap Condition&lt;50 penalty applied once; heavy `GetBaseDegradePerShot` honors `self.DegradePerShot`.

## Инварианты и ограничения

- не удалять id `Handling` из property defs / GameTerm / InventoryItem companions;
- `ExtraBurstShots` остаётся отключённым;
- deterministic integer math (`MulDivRound` / `DivRound`);
- vanilla source не изменяется — только JAZZ overrides.

## Acceptance criteria

- `JAZZ-WEAPONS-001-AC-001` — static: jam tier chain uses `elseif`; condition 10% gets ×24 not ×4.
- `JAZZ-WEAPONS-001-AC-002` — static: `GetJamChance` and `ReliabilityCheck` share one Mechanical application; roll uses `attacker:Random(1000)`.
- `JAZZ-WEAPONS-001-AC-003` — static: ammo hint uses `mod_mul` (not `mod_mull`); BaseJamChance display `/10`.
- `JAZZ-WEAPONS-001-AC-004` — static: CTH Handling modifier inert; overwatch without Handling term.
- `JAZZ-WEAPONS-001-AC-005` — static: scrap `/20` once; WeaponClasses heavy degrade uses `self.DegradePerShot or const`.
- `JAZZ-WEAPONS-001-AC-006` — runtime/human: save/load weapon with Handling and reduced WeaponResourceMax; CTH UI without «Эргономика».

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: overrides in jazz Code + inert items.lua CTH modifier.
- Saves: Handling field preserved; jam formula change affects future rolls only.
- Network/determinism: integer RNG path aligned with attacker:Random.
- Generated data: no companion mass rewrite; items.lua CTH CalcValue only.
- Cross-package: none beyond jazz.
- Rollback/recovery: revert listed write set.

## План и ownership

- Пакет-владелец: jazz
- Исполнитель: agent
- Reviewer: project-owner
- Declared write set: see frontmatter
- Exclusive resources: items.lua

## Решение владельца

- Статус: approved
- Кто подтвердил: project-owner (plan implement request)
- Дата: 2026-07-28

## Evidence

- `JAZZ-WEAPONS-001-AC-001`: `PASS` — static: `GetBaseJamChanceRaw` uses elseif tiers (15→24, 40→16, 60→8, 80→4)
- `JAZZ-WEAPONS-001-AC-002`: `PASS` — static: Mechanical only in `GetJamChance`; roll `attacker:Random(1000)`
- `JAZZ-WEAPONS-001-AC-003`: `PASS` — static: `AmmoRolloverHint` uses `mod_mul`; BaseJamChance `/10`
- `JAZZ-WEAPONS-001-AC-004`: `PASS` — static: Handling CTH inert; overwatch without Handling term
- `JAZZ-WEAPONS-001-AC-005`: `PASS` — static: scrap penalty once in `AmountOfScrapPartsFromItem`; heavy degrade honors `self.DegradePerShot`
- `JAZZ-WEAPONS-001-AC-006`: `PASS (runtime/human) - owner playtest accepted 2026-07-28`

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — jam scale, tiers, Mechanical, Handling, scrap/degrade load order
- `docs/technical/weapons/accuracy-model.md` — Handling inert in CTH and overwatch
