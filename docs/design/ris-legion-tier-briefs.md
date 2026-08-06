# R.I.S. Legion supply briefs (canon for Email)

Player-facing copy for `JAZZ_Legion_Tier` raises. **No raw tier numbers** in letters — these are intelligence-desk notes about what the Major is buying and issuing.

Runtime maps value → Email id `RIS_LegionBrief_<value>` (see `Code/System_RIS_Mail.lua`).

Weapon gossip must track **new primary unlocks** for line troops (Assault / Front / Flanker / Gunner / Heavy) from `scripts/legion-loadouts` + `weapons.csv` `tier_label`. Ignore elites and sergeants/leaders. PPSh is **not** day-one (unlocks at 13).

| Value | Arch | Style notes (weapons as gossip, not LootDef) |
| ---: | --- | --- |
| 11 | 1-1 | Warehouse scrap: Mosin / MAS-36, MAT-49 / MP40, Winchester, double-barrels, DP-27 era; thin ammo |
| 12 | 1-2 | Grease Gun / Sterling, Garand / M2 / StG 44, better pistols (Luger, TT-33) |
| 13 | 1-3 | Peak early kit: PPSh / PPS-43 / Thompson, FG 42 / SVT-40, MG 42, 1911 / Makarov |
| 21 | 2-1 | Second wave: UZI / MAC-10 / Hi-Power; early M16A1 / Type 56; pipe bombs on thugs |
| 22 | 2-2 | CAR-15, FAMAS, M70, M14 SAW, 870; FR F2 / M76 glass |
| 23 | 2-3 | AK-47 / AKM / AKS-74U / Bizon; FAL; RPK / M60 — “proper rifles” |
| 24 | 2-4 | MP5 family, M4A1, HK33 / AK-74 / Galil; Dragunov / M700 |
| 25 | 2-5 | Late second wave: G36 / G36c, VSS, AUG, G3, Minimi / PKM |
| 31 | 3-1 | Third wave: Sig 550 / 552, MP5SD, M60E4, M1A |
| 32 | 3-2 | Custom Sigs, MP7 / P90, SVU, Arctic Warfare, HK21 |
| 33 | 3-3 | Barrett / PSG-1 / AS Val / AA-12 — top-shelf threats |

Full Email body text lives in loc IDs `890000000011300`…`11321` (RU/EN) wired to `ModItemEmail`; this table is the design checklist so copy stays aligned with loadout unlock bands.

Detailed unlock lists: [`legion-weapon-availability-by-tier.md`](legion-weapon-availability-by-tier.md).

Rewrite tool: `docs/tools/_rewrite_ris_legion_briefs.py`.
