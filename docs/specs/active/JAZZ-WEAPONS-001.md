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
related_specs:
  - JAZZ-WEAPONS-010
  - JAZZ-ATTACH-001
  - JAZZ-CTH-001
approved_by: project-owner
---

# JAZZ-WEAPONS-001: клин, scrap, Handling hide

## Проблема

Шанс клина считается на смешанной float-шкале со сломанными ступенями износа и непрозрачным влиянием Mechanical. Приведённый `%` в ammo rollover (`BaseJamChance / 10`) не совпадает с фактическим roll. Scrap штрафует Condition дважды. Heavy weapons игнорируют `DegradePerShot` из-за позднего override. Legacy `Handling` («Эргономика») в момент 001 ещё влиял на CTH и overwatch, хотя по CTH-контракту должен был быть inert; удалять поле тогда нельзя было из‑за сейвов. **Позже `JAZZ-ATTACH-001` (owner 2026-08-01) удалил property `Handling` целиком** (accepted save break).

## Цели

- единая integer-шкала JamScore `0..1000` = единицы roll; display `%` = `DivRound(score, 10)`;
- rollover показывает приведённый jam `%`; окно модификации — Reliability;
- Mechanical сильно снижает клин пропорционально, не обнуляя любой ствол flat-вычетом;
- скрыть Эргономику из CTH и overwatch, сохранив сериализованное поле `Handling` **в scope 001**; удаление property — follow-up ATTACH-001;
- исправить scrap, heavy degrade, grouping integer path и мёртвый `ExtraBurstShots` noop.

## Non-goals

- массовый ребаланс `BaseJamChance` / `Reliability` / удаление `Handling` из InventoryItem (**удаление property закрыто ATTACH-001**, не 001);
- перепрошивка component effects `*Handling*` на другие статы (**закрыто ATTACH-001**);
- rewrite `Firearm:GetAttackResults` / полный CTH;
- FX/sounds/maps/units.

## Требования

- `JAZZ-WEAPONS-001-REQ-001` — JamScore ∈ `[0, 1000]`; `jam_roll < score` с `attacker:Random(1000)`; display `%` = `DivRound(score, 10)`.
- `JAZZ-WEAPONS-001-REQ-002` — historical condition multipliers via
  `elseif` (original 4/8/16/24; WEAPONS-008 softened to 3/6/12/18);
  **superseded by JAZZ-WEAPONS-010**, which replaces multiplication with
  additive condition/permanent-wear steps.
- `JAZZ-WEAPONS-001-REQ-003` — Mechanical reduces score proportionally (merc `/120` + small secondary; AI `/150`); single shot halves score via `DivRound`.
- `JAZZ-WEAPONS-001-REQ-004` — ammo rollover keeps `BaseJamChance/10` as `%`; modify UI keeps Reliability only.
- `JAZZ-WEAPONS-001-REQ-005` — **superseded 2026-08-01 by `JAZZ-ATTACH-001-REQ-002`:** Firearm property `Handling` **удалён** (не «inert поле»). CTH/overwatch без Handling остаётся. Не восстанавливать поле.
- `JAZZ-WEAPONS-001-REQ-006` — scrap Condition&lt;50 penalty applied once; heavy `GetBaseDegradePerShot` honors `self.DegradePerShot`.

## Инварианты и ограничения

- не удалять id `Handling` из property defs / GameTerm / InventoryItem companions — **superseded ATTACH-001** (property удалён; GameTerm/loc «Эргономика» могут остаться как мёртвые строки);
- `ExtraBurstShots` остаётся отключённым;
- deterministic integer math (`MulDivRound` / `DivRound`);
- vanilla source не изменяется — только JAZZ overrides.

## Acceptance criteria

- `JAZZ-WEAPONS-001-AC-001` — historical static acceptance for the
  multiplicative tier chain; **superseded by JAZZ-WEAPONS-010-AC-001/002**.
- `JAZZ-WEAPONS-001-AC-002` — static: `GetJamChance` and `ReliabilityCheck` share one Mechanical application; roll uses `attacker:Random(1000)`.
- `JAZZ-WEAPONS-001-AC-003` — static: ammo hint uses `mod_mul` (not `mod_mull`); BaseJamChance display `/10`.
- `JAZZ-WEAPONS-001-AC-004` — static: CTH/overwatch without Handling (**ATTACH-001:** property absent, not an inert leftover).
- `JAZZ-WEAPONS-001-AC-005` — static: scrap `/20` once; WeaponClasses heavy degrade uses `self.DegradePerShot or const`.
- `JAZZ-WEAPONS-001-AC-006` — **superseded ATTACH-001:** save/load no longer requires a live Handling field (unknown field ignored).

## Impact и совместимость

- Vanilla/CommonLib/JAZZ: jam/scrap/degrade overrides in jazz Code; Handling CTH modifier **removed** (ATTACH-001).
- Saves: **ATTACH-001** removed Handling; jam formula change affects future rolls only.
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

- Статус: implemented
- Кто подтвердил: project-owner (plan implement request)
- Дата: 2026-07-28
- 2026-08-01 / docs lock 2026-08-18: REQ-005 **superseded** [JAZZ-ATTACH-001](JAZZ-ATTACH-001.md) — property `Handling` удалён, не хранить inert поле. Не возвращать в CTH.

## Evidence

- `JAZZ-WEAPONS-001-AC-001`: `PASS (historical, superseded by
  JAZZ-WEAPONS-010)` — the former multiplicative tier chain was implemented
  and later replaced after runtime balance evidence.
- `JAZZ-WEAPONS-001-AC-002`: `PASS` — static: Mechanical only in `GetJamChance`; roll `attacker:Random(1000)`
- `JAZZ-WEAPONS-001-AC-003`: `PASS` — static: `AmmoRolloverHint` uses `mod_mul`; BaseJamChance `/10`
- `JAZZ-WEAPONS-001-AC-004`: `PASS` — static: no Firearm `Handling` property; CTH/overwatch without Handling (ATTACH-001)
- `JAZZ-WEAPONS-001-AC-005`: `PASS` — static: scrap penalty once in `AmountOfScrapPartsFromItem`; heavy degrade honors `self.DegradePerShot`
- `JAZZ-WEAPONS-001-AC-006`: `PASS (historical)` — playtest 2026-07-28 with inert field; **superseded ATTACH-001** (property removed)

## Documentation delta

- `docs/technical/systems/weapons-ammo-components.md` — jam scale; Handling **removed** (ATTACH-001)
- `docs/technical/weapons/accuracy-model.md` — Handling removed from CTH and as Firearm property
