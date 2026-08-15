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
| `GrizzlyPerk` | Grizzly | MG signature: **2×** long-burst shots, **full** damage, ignore unsupported CTH/recoil, **2×** suppression |
| `GruntyPerk_JAZZ` | Grunty | Combat start → +50% AP; later turns `10%×personal morale` (0…5; CombatLog roll) |
| `JackOfAllTrades` | Wolf | Satellite ops about **33% faster** (vanilla `activityDurationMod`) |
| `SteroidPunch` | Steroid | Passive: melee CTH from Strength; unarmed hit → vanilla Smash knockback; Passive hotbar icon; no stim tiredness; Burning DoT **−30%** |
| `ExplodingPalm` | DrQ | Unarmed hit → status by target HP (KO / concussion / ribs / arms / legs / groin); sat **+30%** trauma debt; **blocks** infection |
| `MakeThemBleed` | Flay | +10% damage per bleeding enemy in LOS (cap +50%); HUD stack “Blood Trail” = visible count |
| `DangerClose` | Larry / Larry_Clean | Explosives ≥**8** tiles: **+40%** damage; explosions **+2** Bleeding stacks; no combat stim penalties |
| `GloryHog` | PierreMerc | Machete **Charge** (non-straight) +**15** Grit; active **Recruit** — one button, click a visible enemy → AI ally / combat (not bosses) |
| `RecklessAssault` | Smiley | Improved Run and Gun: **4** attacks with SMG/carbine/AR, **+15** CTH; **no** Energy loss; **recharge on kill** (like RnG) |
| `HawksEye` | Scope | With sniper: Overwatch **1 AP** (keeps leftover AP); Pin Down min 1 AP; sniper suppress **×2**; every **96 h** — **7** biscuits; also bakes on hire |
| `HaveABlast` | Red | Toggle: grenade retaliate on hit **or** miss (hands / **grenade pockets** / backpack); **−50%** explosion damage taken while active |
| `Nazdarovya` | Igor | Active **2 AP**, CD **on kill**: clears Pain, heals **15–20** HP, intoxication stack ≤**5** (−15 CTH / +20 melee per stack); −1 stack / **3 h** |
| `VengefulTemperament` | Meltdown | Active “Hurricane Norma”: enemies ≤5 tiles — Panic or Berserk (Wisdom). **No** Run and Gun. |

| `KillingWind` | Fauda | ≥2 enemies: **+8 Grit each**; armor FM pen **another −50%** (with Ironclad: **0**); cumbersome **keeps** Free Move |
| `DoubleToss` | Fidel | Twin throw (≥2 in stack): hands **or** grenade pockets |
| `BuildingConfidence` | MD | Inspired (+4 AP) on turns **2/5/8…**; heal **±10%** per level difference vs patient (cap **±50%**), combat and satellite |
| `BulletHell` | Spike | Cone dump 15–30 rounds **with no recoil**; CTH on an enemy in the cone; **Will dump on everyone in the cone**; CD **on kill** |
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

Passive Lynx/Buzz/Spider/Colby show on the signature hotbar (info-only Passive buttons; HUD icons from `Perks/SignatureAbilities/`). Toggle remains Spouke-only (`Jazz_Perk_00`).

## §A / §C / §B / §D (UNITS-006)

§A + §C batch2/3 match List2. Soft-cut batch3: Flay groin/animal apply (dmg aura only). **GloryHog recruit** and **RecklessAssault** wired. **MD** heal%-by-level wired. **Reaper `TheGrim`:** recharges after **5** kills (not one). **Owner 2026-08-11:** personal perks for Hitman/Tex/Shadow/Buns/Sidney/Raven/Mouse/Omryn/Raider/Len/Fox/Scully/Magic/Ivan/Gus/Nails/Ice/Blood are **stock JA3** again (JAZZ CE overrides removed; Reaper CHANGE is CD×5 only).

§B batch4: **Flo / Static / Cougar** + Grace/Kulba/Grom/Ricochet/Highball.

**Batch5 HARD/satellite:** Rothman (loyalty-scaled mine income), Miguel (aura 30 Will/CTH), Ira (+20 primary on militia she trains), **Barry** (`DesignerExplosives`): every **168 h** produces **2× Shaped Charge**; craft via Craft Explosives; **−30% Parts** on CraftAmmo/CraftExplosives while Barry is in the sector (assigned or Idle). Meat Will→Grit, Carlos detection/Hidden, Cord city repair, Conrad Leadership≥90 as trainer. **Igor** (`Nazdarovya`): drink 2 AP, CD on kill — heal/Pain/Drunk stacks. **Thor** (`NaturalHealing`): joints every 48 h; sat squad +15% trauma/burn/HP debt recovery (not infection); bandage restores 20–25 Will. Soft: Biff trooper economy, Livewire money op (ECON-001).

**Batch6 §D:** `Jazz_Perk_Benny` (“Package for You”) and `Jazz_Perk_Simon` (“Absolute Sniper”) — CE + StartingPerks; CombatAction soft-cut. Statuses: `Jazz_MiguelAuraUp`/`Down`, `Jazz_OrderAP`, `Jazz_OrderCTH`, …

## IMP starting gear

After the IMP test, loadout is built from stats and perks (JA2-style): primary from AutoWeapons/Heavy/Stealthy/Marksmanship, **JazzArmor_*** by Health (not vanilla Kevlar), tools from Mechanical/Medical, etc. Details in design `imp-starting-gear.md`.

## Still stubs

Monk/Horg/Manuel/Hitman JA12 signatures, Bull inventory, Iggy bombard call-site, full Biff/Livewire ops — see `_units006_batch5_notes.md` / `_units006_batch6_notes.md`.

## Player takeaway

Working named effects: **Spouke, Tosca, Lynx, Spider, Colby** + §A + §C batch2/3 + §B batch4 + batch5 (Rothman/Miguel/Barry/Meat/Carlos/…) + §D Benny/Simon (helpers).
