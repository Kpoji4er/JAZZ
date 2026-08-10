# Perks

[Overview](home.md) · [Mercenaries](mercenaries.md) · [Combat actions](combat-actions.md) · [Русский](../ru/perks.md)

Sourced from `CharacterEffect/Jazz_Perk_*.lua`, `items.lua`, and `Code/*` (jazz). Class weapon buttons (`JAZZ_Fanning`, etc.) live on [combat actions](combat-actions.md); this page is **named / personal**.

## Layers

1. Named merc perk (`Jazz_Perk_*` in StartingPerks).
2. Personal combat action (button id = perk / `GrizzlyPerk`) — only where toggle/active is needed.
3. Status/aura (`Jazz_Perk_OfficerAura*`, `Jazz_OrderCTH`, `Jazz_OrderAP`, `Jazz_CombatMedicBuff`) — markers, not AIM picks.

## What actually works in code

| Id | Who | Runtime effect |
| --- | --- | --- |
| `Jazz_Perk_00` | Spouke | Toggle: timed explosives detonate at enemy turn start |
| `Jazz_Perk_Buzz` | Tosca | +50% autofire bullet count |
| `Jazz_Perk_Lynx` | Lynx | +8 daytime sight; that vision softens range accuracy (Range CTH) |
| `Jazz_Perk_Spider` | Spider | ×2 Medical on sector heal ops |
| `Jazz_Perk_Colby` | Colby | +20% grenade AoE; 20% panic on wounded in blast |
| `Jazz_Perk_Madman` | Madman | Melee crit/kill → −10 Will to everyone ≤5 (including allies) |
| `Jazz_Perk_Blade` | Blade | Brutalize: each successful hit in the chain deals one extra hit |
| `Jazz_Perk_Nervous` | Nervous | Burst/autofire hit stacks +1 bullet on next burst (cap +10) |
| `Jazz_Perk_Henning` | Henning | Allies ≤10: +3 AP (`Jazz_OrderAP`) |
| `Jazz_Perk_Vicious` | Vicious | +1 AP per woman in squad (cap 3) at combat start |
| `Jazz_Perk_Dynamo` | Dynamo | Lockpicking does not trigger lock traps |
| `Jazz_Perk_Eskimo` | Eskimo | <50% HP: no Panic; Wounded does not cut firearm CTH |
| `Jazz_Perk_Lucky` | Lucky | CTH≥70% miss → shot reroll |
| `Jazz_Perk_Shank` | Shank | 50% melee defense; melee miss vs him → knife throwback ≤8 |
| `Jazz_Perk_Vilde` | Vilde | Night/underground auto/burst +15 CTH |
| `Jazz_Perk_Laura` | Laura | After healing an ally: +15 CTH and crit until end of next turn |
| `Jazz_Perk_Vince` | Vince | While in squad: ~−25% medkit/Meds spend (chance to skip a charge) |
| `Jazz_Perk_Steiger` | Steiger | Night/underground: allies ≤10 get +5 CTH |
| `Jazz_Perk_Mike` | Mike | Overwatch/PinDown +2 attacks; reactions when available |
| `GrizzlyPerk` | Grizzly | Signature MG: ignore unsupported; **2×** shots and **2×** suppression; −dmg / recoil control |
| `GruntyPerk_JAZZ` | Grunty | Combat start → +50% AP; later turns `10%×morale` chance for the same buff |
| `YouSeeIgor` | Ivan | Kill → **+3 AP** |
| `WeGotThis` | Gus | Kill → **+10 Grit** to whole squad |
| `NailsPerk` | Nails | After first kill in combat **+20%** damage |
| `JackOfAllTrades` | Wolf | Satellite ops **−33%** time (not arrival/travel) |
| `SecondStoryMan` | Magic | From high ground **+50%** crit |
| `ShoulderToShoulder` | Scully | End turn next to ally: **+15 Grit** to self and neighbors |
| `SteroidPunch` | Steroid | Melee CTH from Strength; melee crit → Unconscious; no stim pen; **30%** fire damage taken |
| `IcePerk` | Ice | Signature: five limb shots (text; shot-list runtime deferred) |
| `MakeThemBleed` | Flay | +10% damage per bleeding enemy in LOS (cap +50%) |
| `DedicatedCamper` | Hitman | Stationary: +25% damage; ≥25 damage → +15 Grit |
| `TagTeam` | Raider | +15 CTH vs ally Pin Down targets |
| `BunsPerk` | Buns | +10 CTH vs targets already damaged by an ally this turn |
| `HawksEye` | Scope | Pin Down **1 AP**; sniper suppress ×2 |
| `Spotter` | Raven | Pin Down → Marked; next hit 100% crit |
| `HaveABlast` | Red | Toggle grenade; **50%** damage from own blasts |
| `KillingWind` | Fauda | ≥2 targets hit → +8 Grit (+ existing FM/armor) |
| `BuildingConfidence` | MD | Inspired on turn 2 and every 3rd (heal%-by-level partial) |
| `SidneyPerk` | Sidney | +2 AP/turn until miss/damage taken |
| `BulletHell` | Spike | CD **on kill** |
| `OnMyTarget` | Len | Squad attacks marked target; **10 AP** |
| `Jazz_Perk_Flo` | Flo | Squad: **−12%** Bobby Ray buy / **+12%** cash-in (additive with Negotiator) |
| `Jazz_Perk_Static` | Static | Repair/craft Parts **−5%/level** (cap **−25%**) |
| `Jazz_Perk_Cougar` | Cougar | Shots **−33%** noise; Stealth Kill → Inspired **1×/turn** |
| `Jazz_Perk_Grace` | Grace | First knife throw/turn auto-hit ≤**12** |
| `Jazz_Perk_Kulba` | Kulba | US autos **−50%** recoil |
| `Jazz_Perk_Grom` | Grom | GL/mortar/AT Will suppress **×2** |
| `Jazz_Perk_Ricochet` | Ricochet | Melee splash to enemy ≤1 from target |
| `Jazz_Perk_Highball` | Highball | Heal **±50%** if ally doctor Med≥80 within 5 |
| `Jazz_Perk_Meat` | Meat | Morale never drops Will (partial) |
| `Jazz_Perk_OfficerAura` / `…Influence` | AI officers | Commander aura; tooltip shows the **current order**. Details: [Command aura](officer-aura.md) |
| `Jazz_Perk_Mimicry` | IMP (personal) | Conversation options for Negotiator/Scoundrel/Psycho without their combat/economy effects |
| `Jazz_Perk_Veteran` | IMP (personal) | +10 to all skill/stat checks |
| `Jazz_Perk_Sniper` | IMP (tactical) | +1 max aim level (any weapon) |

Passive Lynx/Buzz/Spider/Colby have **no** HUD toggle (buttons hidden). Toggle remains Spouke-only (`Jazz_Perk_00`).

## §A / §C / §B / §D (UNITS-006)

§A + §C batch2/3 match List2. Soft-cut batch3: GloryHog recruit, RecklessAssault rewrite, MD heal%-by-level, Flay groin/animal apply (dmg aura only), Ice shot-list.

§B batch4: **Flo / Static / Cougar** + Grace/Kulba/Grom/Ricochet/Highball.

**Batch5 HARD/satellite:** Rothman (loyalty-scaled mine income), Miguel (aura 30 Will/CTH), Ira (+20 primary on militia she trains), Barry craft −30% Parts, Meat Will→Grit, Carlos detection/Hidden, Cord city repair, Conrad Leadership≥90 as trainer. Soft: Biff trooper economy, Livewire money op (ECON-001), Thor joints recipes, Nazdarovya hangover.

**Batch6 §D:** `Jazz_Perk_Benny` (“Package for You”) and `Jazz_Perk_Simon` (“Absolute Sniper”) — CE + StartingPerks; CombatAction soft-cut. Statuses: `Jazz_MiguelAuraUp`/`Down`, `Jazz_OrderAP`, `Jazz_OrderCTH`, …

## IMP starting gear

After the IMP test, loadout is built from stats and perks (JA2-style): primary from AutoWeapons/Heavy/Stealthy/Marksmanship, **JazzArmor_*** by Health (not vanilla Kevlar), tools from Mechanical/Medical, etc. Details in design `imp-starting-gear.md`.

## Still stubs

Monk/Horg/Manuel/Hitman JA12 signatures, Bull inventory, Iggy bombard call-site, full Biff/Livewire/Thor ops — see `_units006_batch5_notes.md` / `_units006_batch6_notes.md`.

## Player takeaway

Working named effects: **Spouke, Tosca, Lynx, Spider, Colby** + §A + §C batch2/3 + §B batch4 + batch5 (Rothman/Miguel/Barry/Meat/Carlos/…) + §D Benny/Simon (helpers).
