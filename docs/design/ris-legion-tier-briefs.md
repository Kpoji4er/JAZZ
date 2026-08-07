# R.I.S. Legion supply briefs (canon for Email)

Player-facing copy for `JAZZ_Legion_Tier` raises. **No raw tier numbers** in letters — these are intelligence-desk notes about what the Major is buying and issuing.

Runtime maps value → Email id `RIS_LegionBrief_<value>` (see `Code/System_RIS_Mail.lua`).

Weapon gossip must track **new primary unlocks** for line troops (Assault / Front / Flanker / Gunner / Heavy) from `scripts/legion-loadouts` + `weapons.csv` `tier_label`. Ignore elites and sergeants/leaders. PPSh is **not** day-one (unlocks at 13).

## Review checklist

- [x] Every named weapon appears in the matching unlock band in [`legion-weapon-availability-by-tier.md`](legion-weapon-availability-by-tier.md).
- [x] Chance-based utility is described as possible, never as guaranteed.
- [x] The note says what changed and what it means in a fight; it does not read like a changelog or inventory dump.
- [x] No player-facing `tier`, `arch`, `wave`, internal ID, weapon tag, or progression terminology.
- [x] Weapon categories stay accurate: rifles are not “optics,” magazine-fed guns do not get “belts,” and unrelated SMGs are not called Kalashnikovs.
- [x] English uses a concise field-analyst voice; Russian is idiomatic and does not copy English syntax.
- [x] RU and EN name the same equipment, preserve uncertainty, and land on the same tactical conclusion.
- [x] The Email sender already establishes the brand; headers and signatures do not drown the actual report.

Editorial review completed 7 August 2026. This records source-copy approval only;
the revised wording has not been applied to runtime files in this stage.

## Unlock notes

| Value | Arch | Style notes (weapons as gossip, not LootDef) | EN | RU |
| ---: | --- | --- | --- | --- |
| 11 | 1-1 | Old warehouse stock: Mosin / MAS-36, MAT-49 / MP40, Winchester, double-barrels; DP-27 / MAC 24/29 support | PASS | PASS |
| 12 | 1-2 | Grease Gun / Sterling, Garand / M2 / StG 44, better pistols (Luger, TT-33) | PASS | PASS |
| 13 | 1-3 | PPSh / PPS-43 / Thompson / MPL, FG 42 / G43 / SVT-40, Auto-5, MG 42, 1911 / Makarov / P38 | PASS | PASS |
| 21 | 2-1 | UZI / MAC-10 / Micro UZI / Agram, M16A1 / Type 56 / Mini-14; Roughneck pipe bombs are possible, not universal | PASS | PASS |
| 22 | 2-2 | CAR-15, FAMAS, M70, M14, Remington 870; FR F2 / M76 precision rifles | PASS | PASS |
| 23 | 2-3 | AK-47 / AKM / AKS-74U and M16A2; Bizon / Spectre for close assault; M21 marksmen; RPK / M60 support | PASS | PASS |
| 24 | 2-4 | MP5A2 / MP5K / TMP, M4A1, HK33 / AK-74 / Galil, SPAS-12; Dragunov / M700; RPK-74 / M60E3 | PASS | PASS |
| 25 | 2-5 | G36 / G36c, AUG, VSS, G3; Minimi / MAG / PKM support | PASS | PASS |
| 31 | 3-1 | Sig 550 / 552, MP5SD, M60E4, M1A rifle | PASS | PASS |
| 32 | 3-2 | Custom Sigs, MP7 / P90, SVU / Arctic Warfare, USAS-12, HK21 / HK23 | PASS | PASS |
| 33 | 3-3 | Barrett / PSG-1 / AS Val / AA-12 — high-end threats | PASS | PASS |

Full Email body text lives in loc IDs `890000000011300`…`11321` (RU/EN) wired to `ModItemEmail`; this table is the design checklist so copy stays aligned with loadout unlock bands.

Detailed unlock lists: [`legion-weapon-availability-by-tier.md`](legion-weapon-availability-by-tier.md).

Rewrite tool: `docs/tools/_rewrite_ris_legion_briefs.py`.
