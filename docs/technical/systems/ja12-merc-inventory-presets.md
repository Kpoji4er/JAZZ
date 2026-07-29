# JA12 merc inventory presets

Current-state hire kits for the JA12 merc wave.

- Root: `Loot_JAZZ_<Nick>`
- Children: `JAZZ_<Nick>50` / `35` / `25` / `20` (weights 50000 / 35000 / 25000 / 20000)
- Runtime: `jazz-units/items.lua`
- Design source: `docs/design/mercs-ja12/<slug>.md` loot section

## Invariants

1. Any tier with a firearm or M79 includes matching ammo (`JAZZ_AMMO_*`, or `JAZZ_AMMO_40mmFragGrenade` for M79).
2. Article `(Double)` ammo uses `Double = true` on the loot entry.
3. Melee / demo / crowbar kits may omit ammo (Vicious, Ricochet, Shank, Dynamo, Meat, Devin knives/explosives).
4. Generate-time aliases: `HK G3` -> `G3A3`, `M14` -> `M14SAW`, `JAZZ_AMMO_308_*` -> `JAZZ_AMMO_762x51_*`, `JazzArmor_NightCamoJacket` -> `JazzArmor_LeatherJacketBlk`, bare `Detonator` -> `Combination_Detonator_Time`.
5. Omitted (no stable mod item id): `NVGoggles`, `Radio`, `Scarf`, `US_Passport`, `Unarmed`.

Script: `.agents/scripts/fill-ja12-merc-loot-tiers.ps1` (Medium/Low refresh).

## High + Rothman

| Merc | Root | *50 |
| --- | --- | --- |
| Colby | `Loot_JAZZ_Colby` | MP5A4 + `JAZZ_AMMO_9x19_FMJ`x60, ShapedCharge/C4, leather vest, smoke, remote detonator combo |
| Blade | `Loot_JAZZ_Blade` | see `JAZZ_Blade50` in items.lua |
| Ira | `Loot_JAZZ_Ira` | see `JAZZ_Ira50` |
| Dimitri | `Loot_JAZZ_Dimitri` | see `JAZZ_Dimitri50` |
| Madman | `Loot_JAZZ_Madman` | see `JAZZ_Madman50` |
| Conrad | `Loot_JAZZ_Conrad` | see `JAZZ_Conrad50` |
| Mike | `Loot_JAZZ_Mike` | see `JAZZ_Mike50` |
| Grom | `Loot_JAZZ_Grom` | see `JAZZ_Grom50` |
| Rothman | `Loot_JAZZ_Rothman` | FNFAL + `JAZZ_AMMO_762x51_Match`x40 (Double), uniform, shaped charge, FAK |

## Medium / Low (*50)

| Merc | Root | *50 |
| --- | --- | --- |
| Quinten | `Loot_JAZZ_Quinten` | PoliceVest, HiPower x2, 9x19 x48 (Double), Meds x50, FAK, CombatStim x2 |
| Vicious | `Loot_JAZZ_Vicious` | LeatherJacketBlk, Knife_Sharpened x2, Knife_Balanced x2, Smoke, CombatStim x2 (melee) |
| Biff | `Loot_JAZZ_Biff` | PoliceVest, Makarov, 9x18 x16 (Double), FAK |
| Nervous | `Loot_JAZZ_Nervous` | LeatherArmor, UZI, 9x19 x80 (Double), Smoke |
| Flo | `Loot_JAZZ_Flo` | LeatherJacketBrn, Makarov, 9x18 x16 (Double), FAK |
| Cougar | `Loot_JAZZ_Cougar` | LeatherJacketBlk, MP5SD, 9x19 x60 (Double), Lockpick |
| Miguel | `Loot_JAZZ_Miguel` | Uniform, HiPower, 9x19 x32 (Double), FAK, Meds x10 |
| Gamos | `Loot_JAZZ_Gamos` | LeatherArmor, SKS, 7.62x39 x30 (Double), Machete, Lockpick |
| Dynamo | `Loot_JAZZ_Dynamo` | LeatherJacketBrn, Crowbar, Lockpick, Parts x15, CombatStim (no gun) |
| Gaston | `Loot_JAZZ_Gaston` | LeatherJacketBlk, DragunovSVD, 7.62x51 Match x20 (Double), CombatScope 2x |
| Horg | `Loot_JAZZ_Horg` | FlakM1955, M79 + 40mm x8, M16A1 + 5.56 x60 (Double) |
| Manuel | `Loot_JAZZ_Manuel` | LeatherJacketBrn, SKS, 7.62x39 x30 (Double), Lockpick |
| Monk | `Loot_JAZZ_Monk` | SovietAssaultArmor, VSS, 9x39 AP x30 (Double), Knife_Sharpened |
| Allik | `Loot_JAZZ_Allik` | LeatherArmor, Sig550, 5.56 x60 (Double), Lockpick, Parts, ShapedCharge |
| Henning | `Loot_JAZZ_Henning` | Uniform, Sig550, 5.56 x80 (Double), FAK, Meds |
| Static | `Loot_JAZZ_Static` | LeatherJacketBrn, Lockpick, Wirecutter, MicroUZI, 9x19 x32 (Double), Parts |
| Highball | `Loot_JAZZ_Highball` | LeatherVest, Meds, FAK, CombatStim, SWModel19, .357 x18 (Double) |
| Bull | `Loot_JAZZ_Bull` | LeatherVest, Knife, M2Carbine, .30 x20 (Double) |
| Cord | `Loot_JAZZ_Cord` | LeatherArmor, Lockpick, Wirecutter, TT33, 7.62x25 x24 (Double), Parts |
| Hobbit | `Loot_JAZZ_Hobbit` | LeatherArmor, demo kit, M2Carbine, .30 x20 (Double) |
| Ricochet | `Loot_JAZZ_Ricochet` | CamoBalaclava, knives / machete (melee) |
| Meat | `Loot_JAZZ_Meat` | LeatherJacketBrn, TNT/PipeBomb/detonator combo, Machete (demo) |
| Carlos | `Loot_JAZZ_Carlos` | CamoBalaclava, Knife_Balanced x3, Scorpion, 7.62x25 x24 (Double) |
| Devin | `Loot_JAZZ_Devin` | LeatherJacketBrn, C4/detonator combos, Wirecutter, Knife_Sharpened |
| Shank | `Loot_JAZZ_Shank` | UniformPants, Knife x3 (melee) |
| Vince | `Loot_JAZZ_Vince` | PoliceVest, med kit, HiPower x2, 9x19 x32 (Double) |
| Hitman | `Loot_JAZZ_Hitman` | CamoBalaclava, DragunovSVD, 7.62x54 Match x20 (Double) |
| Biggens | `Loot_JAZZ_Biggens` | UniformPants, demo + M1Garand, .30-06 x20 (Double) |
| Kulba | `Loot_JAZZ_Kulba` | UniformPants, M60, 7.62x51 x100 (Double), Parts, Wirecutter |
| Vilde | `Loot_JAZZ_Vilde` | LeatherJacketBlk, RPK, 7.62x39 x80 (Double) |
| Grace | `Loot_JAZZ_Grace` | LeatherJacketBrn, knives + machete (melee *50; guns on lower tiers) |
| Steiger | `Loot_JAZZ_Steiger` | PoliceVest, G3A3, 7.62x51 Match x40 (Double) |
| Lucky | `Loot_JAZZ_Lucky` | LeatherJacketBrn, FAMAS, 5.56 x60 (Double), Knife |
| Laura | `Loot_JAZZ_Laura` | LeatherVest, meds/FAK/Medkit, PipeBomb+detonator, MicroUZI, 9x19 x24 (Double) |
| Eskimo | `Loot_JAZZ_Eskimo` | UniformPants, M24Sniper, 7.62x51 Match x20 (Double) |

Lower tiers (`35`/`25`/`20`) live next to each `*50` block in `items.lua`.
