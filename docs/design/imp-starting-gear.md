# IMP: динамический стартовый экип (JA2-style)

Design contract for **JAZZ-IMP-001**. Runtime owner: `Code/System_IMP_StartingGear.lua` + hire hook in `CreateImpMercData`.

## Когда собирается

| Момент | Что происходит |
| --- | --- |
| Campaign `CreateUnitData` | Vanilla `Equipment = { "IMP_equipment_basic" }` → placeholder loot |
| `HireIMPMerc` → `CreateImpMercData(..., "sync")` | После статов/перков: clear inventory → `JazzBuildImpStartingGear` → `EquipStartingGear` |

## Приоритет primary

1. `Stealthy` → `MP5SD` (+ `JazzArmor_ZylonLight` в броню)
2. `HeavyWeaponsTraining` + `AutoWeapons` + Strength ≥ 80 → `BAR` (Mark ≥ 60) / `RPD` (Mark ≥ 80); `M79` остаётся secondary
3. `AutoWeapons` → Mark 50/70/85: `MPL` / `TMP` / `CAR15`
4. Иначе Mark 50/70/85: `TT33` / `R870` / `SKS`

Secondary: Melee/CQC сайдарм (Mark 50/70/85) `APS` / `MicroUZI` / `Glock17` → Handheld B или Inventory.  
Heavy alone (без LMG-ветки): `M79` + 2×`JAZZ_AMMO_40mmFlashbangGrenade` + 3×`JAZZ_AMMO_40mmFragGrenade`.

## Статы

| Stat | Thresholds | Items |
| --- | --- | --- |
| Health | 60 / 70 | `JazzArmor_FlakM1955` → +`JazzArmor_M1Helm`+`JazzArmor_LeatherPants` |
| Agility | 70 / 80 | 2 / 4 `FlareStick` |
| Dexterity | 70 / 80 | `Knife` / 3×`Knife_Balanced` |
| Strength | 70 / 80 | 2×`FragGrenade` / +`Crowbar` |
| Leadership | 80 | 3×`SkillMag_Leadership` |
| Wisdom | — | — |
| Mechanical | 40 / 60 / 80 | `Wirecutter` / +`Lockpick` / +100 `Parts` |
| Explosives | 50 / 80 | 2×`PipeBomb` / 2×`TNT` |
| Medical | 30 / 60 / 80 | `FirstAidKit` / `Medkit` / `Medkit`+100 `Meds` |

## Personality quirks

| Perk | Items |
| --- | --- |
| `Psycho` | 2×`Molotov` |
| `Negotiator` | 2×`SmokeGrenade` |
| `Scoundrel` («Калач») | 2×`ConcussiveGrenade` |

## Specialization skills

| Perk | Items |
| --- | --- |
| `MartialArts` | +2 `Knife_Balanced` |
| `CQCTraining` | `Machete` |
| `MrFixit` | +100 `Parts` |
| `NightOps` | +3 `FlareStick` |
| `Teacher` | 3× `SkillMag_*` (Wisdom/Mechanical/Medical) — **stacks** with Leadership |
| `Throwing` | +2 `FragGrenade` |
| `Stealthy` | см. primary override |
| `AutoWeapons` / `HeavyWeaponsTraining` / `MeleeTraining` | см. оружие |

`MeleeTraining` → sidearm ladder (APS→MicroUZI→Glock17).  
`CQCTraining` → `Machete`.

## Ammo

For each equipped firearm: spare stack ≈ `max(MagazineSize × 4, 60)` (prefer FMJ over LOT surplus). Magazines are filled from a disposable clone in `EquipStartingGear` so spare packs are never drained to `0/MaxStacks`.

## New IMP perks (Personality pool)

| Id | Effect |
| --- | --- |
| `Jazz_Perk_Mimicry` | Dialogue-only: passes `Negotiator`/`Scoundrel`/`Psycho` gates |
| `Jazz_Perk_Veteran` | +10 to `SkillCheck` / `RollSkillCheck` / `UnitHasStat` |
| `Jazz_Perk_Sniper` | +1 `OnCalcMaxAimActions` any weapon |

Selectable on the IMP certificate: Mimicry/Veteran via wrapped `ImpGetPersonalPerks()` (personal row); Sniper via `Perk-Specialization` (tactical grid).
