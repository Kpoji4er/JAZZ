# UNITS-006 named perks — shipping notes

Runtime: one Code module `Code/System_NamedPerks.lua` (ModItemCode `System_NamedPerks`).
Tunables: ModItem CharacterEffect Parameters / unit_reactions; Code uses Jazz_NamedPerkParam / ResolveValue.

## Rollback (owner 2026-08-11): vanilla JA3 personal perks restored

Removed JAZZ CE overrides for: Hitman (`DedicatedCamper`), Buns, Sidney, Raven (`Spotter`), Raider (`TagTeam`), Len (`OnMyTarget`), Scully (`ShoulderToShoulder`), Magic (`SecondStoryMan`), Ivan (`YouSeeIgor`), Gus (`WeGotThis`), Nails, Ice — plus jazz-units `TheGrim` (Reaper). Tex/Shadow/Mouse/Omryn/Fox/Blood had no jazz CE. Tool: `docs/tools/_rollback_units006_vanilla_merc_perks.py`.

Historical batch notes below (implementation order only; rolled-back Ids below are superseded by stock JA3).

# _units006_batch2_notes.md

# UNITS-006 batch 2 notes (§C combat CHANGE)

Shipped in working tree / commit after this note.

## Done

| Id | Effect |
| --- | --- |
| `ExplodingPalm` | Unarmed HP-tier statuses; sat debt +30%; blocks WoundInfected; Passive CA |
| `GruntyPerk_JAZZ` | Passive CA + `perk_grunty_perk`; combat start +50% AP; later turns `10%×max(0,GetPersonalMorale())` → same buff; AdditionalAP via OnCalcStartTurnAP/OnAdded only |
| `GrizzlyPerk` | Signature only: WEAPONS-012 ignore + `GetAutofireShots` = 2× MGBurstFire length + `dmg_penalty=0` + suppression ×2 |
| `JackOfAllTrades` | Keep vanilla param `activityDurationMod`=33 (SectorOperation.ProgressPerTick); no GetOperationTimeLeft wrap; hire co-group ignores ETA match (`SatelliteSquad`) |
| `SteroidPunch` | Passive: all melee CTH from Strength; successful melee → KnockDown+Unconscious; OnCalcStimmedTiredness=0; Burning DoT ×70% (`EnvEffectBurningTick` wrap); signature CA hidden |

## Soft cuts / deferred

- **Steroid fire dmg**: Burning DoT via `EnvEffectBurningTick` TakeDirectDamage ×70 (−30%); instant fire hits via OnCalcDamageAndEffects ×70.
- **Wolf ops**: vanilla `activityDurationMod` on `JackOfAllTrades` (SectorOperation.ProgressPerTick); no `GetOperationTimeLeft` wrap. Hire co-group without equal ETA in `LocalSetArrivingMercSector`.

## Validate

`python docs/tools/_validate_items_quick.py` → OK after apply.

---

# _units006_batch3_notes.md

# UNITS-006 batch 3 notes (§C signatures / CD-kill)

## Done

| Id | Effect |
| --- | --- |
| `VengefulTemperament` | Meltdown: **active** fear AoE ≤5 Panic/Berserk (Wisdom); CombatAction id=`VengefulTemperament`; **no** RunAndGun |
| `BulletHell` | Signature recharge **on kill**; COMBAT-006 v2: FirearmAttack + cone-arc real projectiles (CTH/strays), no AlwaysHits AOE |
| `MakeThemBleed` | +10% dmg per bleeding enemy in sight, cap +50%; HUD `Jazz_MakeThemBleedBuff` stacks = visible count |
| `HawksEye` | Sniper Overwatch **1 AP** (keep leftover AP); PinDown min 1; OnMercHired Cookies; sniper Will suppress ×2 |
| `HaveABlast` | Toggle on: grenade retaliate hit/miss; explosion dmg taken ×50% (once-flag); hands+inventory pull |
| `DangerClose` | Larry List2: explosives ≥8 +40% dmg; explosions +2 Bleeding; stim immune; wrap `ExplosionPrecalcDamageAndStatusEffects` (nil-safe) |
| `KillingWind` | ≥2 enemies via `hit_objs` → +8 Grit **each**; armor FM ÷2 once (w/ Ironclad); cumbersome keeps FreeMove |
| `BuildingConfidence` | Inspired (+4 AP) turns 2/5/8…; heal ±10% per level diff vs patient (cap ±50%) via OnCalcHealAmount + CalcHealAmount wrap |

Loc IDs: remaining batch3 IDs after vanilla rollback purge.

## Soft cuts

- GloryHog recruit / non-straight charge — **wired** (`Jazz_PierreRecruit` + GloryHog CE)
- RecklessAssault 4-attack rewrite — **wired** (SMG/carbine/AR, +15 CTH, no Tiredness)
- BuildingConfidence heal ±10%/level-diff combat+sat (**wired**)
- MakeThemBleed groin/animal bleed apply (aura only)

## Tools

- `docs/tools/_gen_units006_batch3.py`
- `docs/tools/_fix_units006_batch3_loc.py`
- `docs/tools/_rollback_units006_vanilla_merc_perks.py`

---

# _units006_batch4_notes.md

# UNITS-006 batch 4 notes (§B JA12 stubs)

## Priority (wired)

| Id | Before | After |
| --- | --- | --- |
| `Jazz_Perk_Flo` | «Барахольщица» WIP stub | «Теоретически подкована»: −12% Bobby Ray buy / +12% CashIn; Flo in player squad; additive with Negotiator (ops/boat stay Negotiator) |
| `Jazz_Perk_Static` | «Экономия запчастей» WIP stub | «Собрал на коленке»: Parts −5%×Level repair/craft estimate + ModifyWeaponDlg, cap −25% |
| `Jazz_Perk_Cougar` | «Мягкая лапа» WIP stub | Shots −33% noise (`PushUnitAlert`); Stealth Kill → Inspired 1×/turn (not AP) |

## Text + cheap hooks

| Id | Hook |
| --- | --- |
| `Jazz_Perk_Grace` | First `KnifeThrow`/turn CTH=100 if ≤12 |
| `Jazz_Perk_Kulba` | US autos −50% via `JAZZ_CTHGetRecoilProfile` wrap |
| `Jazz_Perk_Grom` | GL/mortar/AT suppress ×2 (`Jazz_ApplyGromSuppression`) |
| `Jazz_Perk_Ricochet` | Melee splash ~35% to enemy ≤1 from target |
| `Jazz_Perk_Highball` | `OnCalcHealAmount` ±50% if ally Med≥80 within 5 |
| `Jazz_Perk_Meat` | `OnCalcPersonalMorale` floors negative morale |
| `Jazz_Perk_Carlos` | Text only (detection / failed-SK stay Hidden deferred) |
| `Jazz_Perk_Iggy` | Text + helper `Jazz_ApplyIggyMortarScatter` (bombard call-site soft) |
| `Jazz_Perk_Monk` / `Horg` / `Manuel` / `Hitman` | Text only — active signatures TBD |
| `Jazz_Perk_Bull` | Text only — fist trauma / +2 slots TBD |

## Soft cuts → batch5 / later

- Rothman mine op, Biff paid troopers, Ira militia train, Miguel aura, Livewire money, Barry craft, Thor NaturalHealing (sat debt + Will)
- Carlos detection −33% + failed SK stay Hidden
- Iggy mortar scatter wired into bombard path
- Meat Will→Grit + unsuppressible
- Highball satellite-in-squad path
- Bull inventory slots + body-part fist trauma
- Monk / Horg / Manuel / Hitman JA12 CombatAction signatures (CD on kill)
- Local sector-merchant buy/sell (JA3 has no Negotiator shop pipeline; Flo = Bobby Ray + CashIn)

## Tools

- `docs/tools/_gen_units006_batch4.py`
- Loc: reuse existing CE IDs (3000/4100/3100/…); upsert refuses VoiceResponse overwrite

---

# _units006_batch5_notes.md

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
| `DesignerExplosives` | vanilla ShapedCharge + JAZZ | 2× ShapedCharge / 168h; CraftExplosives; CraftAmmo/CraftExplosives Parts −30% (SectorOps inline) |
| `DangerClose` | ≥8 tiles | wrap ExplosionPrecalc +40% dmg; +2 Bleeding on blast hits; stim CTH/tiredness immune; aim HUD ≥8 |
| `ExplodingPalm` | DrQ | Unarmed HP-tier statuses; sat debt +30%; blocks WoundInfected; Passive CA |
| `InnerInfo_JAZZ` | Livewire (Фаза): Passive CA `InnerInfo_JAZZ` + HUD `perk_inners_info`; reveal+intel+hack; money op soft ECON-001 |

## Text + helpers (soft call-sites)

| Id | Notes |
| --- | --- |
| `Jazz_Perk_Ira` | Militia Completes → +20 random primary (`Jazz_IraBoostMilitiaInSector`) |
| `Jazz_Perk_Biff` | Paid MERC troopers theme text; full economy soft-cut |
| `Nazdarovya` | Wired: every-turn drink (2 AP, no signature CD); heal 15–20 HP; clear Pain; Drunk stacks≤5 (−15 CTH / +20 flat melee); sat −1 stack / 3h |
| `NaturalHealing` | Wired: HerbalMedicine 1×/48h; sat squad +15% trauma/burn/HP debt (not infection); bandage Will 20–25 |

## Soft cuts → later / ECON-001

- Biff full paid-trooper economy (move/attach/guard/daily pay/mass leave)
- Livewire city money SectorOperation (ECON-001 still draft)
- Nazdarovya hangover 8–10h retune → **shipped** as Drunk 3h/stack sat decay (typical ~3 stacks ≈ 9h)
- DangerClose Larry List2 (grenades ≥8 +40%, blast +2 bleed, stim immune); ExplodingPalm fist HP-tier statuses + infection
- Cord bar-POI gate (any city for now)
- Rothman full 2-day mine overseer operation (loyalty passive shipped instead)

## Tools

- `docs/tools/_gen_units006_batch5.py`
- Loc: reuse JA12 CE IDs; new `9885+` / `9920+` for vanilla overrides + §D; upsert refuses VoiceResponse

---

# _units006_batch6_notes.md

# UNITS-006 batch 6 notes (§D Benny / Simon)

## Shipped

| Id | Deliverable |
| --- | --- |
| `Jazz_Perk_Benny` | CE «Вам посылка» + loc RU/EN (`9920/9921`) + helpers `Jazz_BennyDecoyReady` / `Jazz_BennyPickLureTarget` |
| `Jazz_Perk_Simon` | CE «Абсолютный снайпер» + loc (`9922/9923`) + optic≥4× helpers + CD clear on kill |
| UnitData | `Jazz_Benny` / `Jazz_Simon` StartingPerks prepend named perk (jazz-units companion + items) |

## Soft cuts

- Full CombatAction decoy lure (explosion on arrival AI path)
- Full CombatAction perfect shot (forced hit / no scatter) — helpers only
- Personal perk PNG icons (temporary `DesignerExplosives` / `HawksEye` UI icons)

## Tools

- `docs/tools/_gen_units006_batch5.py` (also emits §D CEs)
- `docs/tools/_units006_batch6_startingperks.py`
- Runtime: `Code/System_NamedPerks_006.lua` (merged; was `_Batch6.lua`)
