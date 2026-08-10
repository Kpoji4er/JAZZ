# UNITS-006 named perks — shipping notes

Runtime: one Code module `Code/System_NamedPerks.lua` (ModItemCode `System_NamedPerks`).
Tunables: ModItem CharacterEffect Parameters / unit_reactions; Code uses Jazz_NamedPerkParam / ResolveValue.

Historical batch notes below (implementation order only).

# _units006_batch2_notes.md

# UNITS-006 batch 2 notes (§C combat CHANGE)

Shipped in working tree / commit after this note.

## Done

| Id | Effect |
| --- | --- |
| `GruntyPerk_JAZZ` | Combat start +50% AP; later turns `10%×max(0,GetPersonalMorale())` → same buff |
| `GrizzlyPerk` | Signature only: WEAPONS-012 ignore (existing) + `GetAutofireShots` ×2 + `suppressionbonus` ×2 |
| `YouSeeIgor` | Kill → +3 AP |
| `WeGotThis` | Kill → +10 Grit squad |
| `NailsPerk` | After first kill → +20% damage until combat end |
| `JackOfAllTrades` | `GetOperationTimeLeft` ×(100−33)/100 except Traveling/Arriving; Arriving via `ProgressCompleteThreshold`; hire co-group ignores ETA match |
| `SecondStoryMan` | High ground → +50 crit chance |
| `ShoulderToShoulder` | End turn adjacent ally → +15 Grit self+neighbors |
| `SteroidPunch` | All melee CTH from Strength; melee crit → Prone+Unconscious; Stimmed CTH pen cleared; ~30% fire dmg taken |
| `IcePerk` | DisplayName/Description only |

## Soft cuts / deferred

- **Ice**: five-limb shot list still vanilla CombatAction engine; CE text only (batch 3+ if CA rewrite needed).
- **Steroid fire dmg**: heuristic hit/action/weapon flags; not every Burning surface path guaranteed.
- **Wolf ops**: wraps `GetOperationTimeLeft` (skip Traveling/Arriving double-count) + Arriving `ProgressCompleteThreshold`; `LocalSetArrivingMercSector` co-groups without equal ETA.
- Loc IDs `890000000006500–6515` (outside VR-clogged 6300–6499 exclusive band).

## Validate

`python docs/tools/_validate_items_quick.py` → OK after apply.

---

# _units006_batch3_notes.md

# UNITS-006 batch 3 notes (§C signatures / CD-kill)

## Done

| Id | Effect |
| --- | --- |
| `BulletHell` | Signature recharge **on kill** (`Unit:BulletHell` + `recharge_on_kill` param) |
| `MakeThemBleed` | +10% dmg per bleeding enemy in sight, cap +50% |
| `DedicatedCamper` | Stationary +25% dmg; ≥25 dmg → +15 Grit |
| `TagTeam` | +15 CTH vs ally Pin Down targets |
| `BunsPerk` | +10 CTH vs ally-damaged targets this turn |
| `HawksEye` | `pindownCostOverwrite=1`; sniper Will suppress ×2 |
| `Spotter` | Pin Down → Marked + next hit 100% crit pending |
| `HaveABlast` | Own grenade blast dmg ×50% |
| `KillingWind` | ≥2 hit units → +8 Grit (FM/armor path kept from COMBAT-005) |
| `BuildingConfidence` | Inspired turn 2 and every 3rd turn |
| `SidneyPerk` | +2 AP/turn until miss or damage taken |
| `OnMyTarget` | Text: 10 AP (vanilla ActionPoints already 10000) |

Loc IDs: `890000000009861–9884` (never 6300–6599 VR band). Upsert refuses VoiceResponse overwrite.

## Soft cuts

- GloryHog recruit / non-straight charge
- RecklessAssault 4-attack rewrite
- BuildingConfidence heal ±10%/level combat+sat
- MakeThemBleed groin/animal bleed apply (aura only)
- Ice five-limb shot list
- Buns tracking depends on `Unit.OnAttack` wrap (fallback if missing)

## Tools

- `docs/tools/_gen_units006_batch3.py`
- `docs/tools/_fix_units006_batch3_loc.py`

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

- Rothman mine op, Biff paid troopers, Ira militia train, Miguel aura, Livewire money, Barry craft, Thor joints
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
