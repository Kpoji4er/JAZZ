# UNITS-006 batch 5 notes (HARD / satellite)

## Wired

| Id | Before | After |
| --- | --- | --- |
| `Jazz_Perk_Rothman` | «Шахтёрский надзор» stub | «Я вас научу работать!»: garrison mine → income +10…+40% (stronger at low loyalty) via `_GetMineIncome` wrap |
| `Jazz_Perk_Miguel` | WIP stub | Aura 30: `Jazz_MiguelAuraUp` (+15 CTH / +30 Will) or `Jazz_MiguelAuraDown` (−15 / −30) |
| `Jazz_Perk_Meat` | Morale floor only | + Will dmg → Grit (`QueueSuppressionApplication`); unsuppressible |
| `Jazz_Perk_Carlos` | Text partial | Detection −33% (`UpdateSuspicion` + apply modifier); failed SK 50% keep Hidden |
| `Jazz_Perk_Cord` | WIP stub | City sector repair −15% time / −10% Parts (bar POI soft) |
| `Jazz_Perk_Conrad` | WIP stub | Trainer Leadership floor 90 on TrainMilitia/TrainMercs pace |
| `DesignerExplosives` | vanilla only | JAZZ CE: CraftAmmo/CraftExplosives Parts −30% |
| `DangerClose` | vanilla close-range UI | CE Parameters minRange 8 +40% dmg reaction; bleed stacks on attack ≥8 (stim soft) |
| `ExplodingPalm` | vanilla | CE: heal_modifier +30% (fist HP statuses / infection soft) |
| `InnerInfo_JAZZ` | «Пока недоступно» | Text: intel + city money op pending ECON-001 |

## Text + helpers (soft call-sites)

| Id | Notes |
| --- | --- |
| `Jazz_Perk_Ira` | Militia Completes → +20 random primary (`Jazz_IraBoostMilitiaInSector`) |
| `Jazz_Perk_Biff` | Paid MERC troopers theme text; full economy soft-cut |
| `Nazdarovya` | CE companion + sheet text; hangover retune soft |
| `NaturalHealing` | CE companion + joints text; craft recipes soft-cut |

## Soft cuts → later / ECON-001

- Biff full paid-trooper economy (move/attach/guard/daily pay/mass leave)
- Livewire city money SectorOperation (ECON-001 still draft)
- Thor joints craft recipes + sat/combat joint effects
- Nazdarovya hangover 8–10h retune
- DangerClose stim-pen removal; ExplodingPalm fist HP-tier statuses + infection
- Cord bar-POI gate (any city for now)
- Rothman full 2-day mine overseer operation (loyalty passive shipped instead)

## Tools

- `docs/tools/_gen_units006_batch5.py`
- Loc: reuse JA12 CE IDs; new `9885+` / `9920+` for vanilla overrides + §D; upsert refuses VoiceResponse
