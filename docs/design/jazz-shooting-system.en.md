# How Shooting Works in JAZZ (detailed)

Shareable English overview of the JAZZ firearm attack pipeline: chance to hit (CTH), range, optics, cover, bursts, grazing, combat actions, ordnance, AI, and post-hit effects.

Canonical systems docs (may be more current for numbers): `docs/wiki/combat-and-accuracy.md`, `docs/wiki/combat-actions.md`, `docs/technical/systems/combat-cth-actions.md`, `docs/technical/weapons/accuracy-model.md`.

---

## 1. End-to-end flow

JAZZ replaces vanilla’s main hit-chance loop and much of firearm attack execution. One pipeline feeds the **crosshair**, **AI**, and the **real shot**.

1. UI or AI picks a `CombatAction` and targeting args (aim clicks, target, cone, body part, etc.).
2. Crosshair / area-aim resolves AP, ammo, LoF/LOS hints, and modifiers.
3. `Unit:CalcChanceToHit` builds skill/aim core → range profile → product of situational factors → clamp.
4. Firearm executor builds the shot sequence; bursts apply recoil retention (and miss climb).
5. Hits feed damage / armor / wounds / suppression; tracers mark per produced shot with CTH > 0.
6. UI updates combat badge, ammo, overwatch, action queue.

```text
validity
  → weapon / action / perk compatibility
  → shooter skill + aim
  → weapon range profile (+ optics / close range)
  → product of situational factors
  → per-bullet recoil (bursts)
  → single final round + clamp (2…100 for valid shots)
```

**Invariants**

| Result | Meaning |
| --- | --- |
| **0%** | Physically impossible: no valid trajectory, or beyond attack limit |
| **2…100%** | Possible shot floor/ceiling |
| **100%** | Reachable for a skilled shooter vs open standing target, full aim, optimal range |
| Core > 100 | Does **not** eat cover; overflow goes **1:1** into **crit chance** |

Legacy **`Handling`** is deleted from CTH and weapon UI.

---

## 2. Skill: snap vs prepared fire

Two channels (Dexterity ↔ Marksmanship), blended by aim progress:

```text
snap_raw      = (Dexterity × 4 + Marksmanship + Level × 5) / 6
precision_raw = (Marksmanship × 4 + Dexterity + Level × 5) / 6
skill(x)      = 20 + x^1.25 × 0.25

aim_progress  = aim_clicks / MaxAimActions
shot_skill    = snap + aim_progress × max(precision − snap, 0)
```

- **0 aim clicks** ≈ Dexterity (snap / hip).
- **Full aim** unlocks Marksmanship; an extra click **never** makes chance worse.
- Aim mastery is nonlinear in Marksmanship; weapon `AimAccuracy` scales click value.
- IMP **Sniper** perk: **+1** max aim clicks on any weapon.
- Aimed fire trains Marksmanship; snap / knives train Dexterity; combat XP raises **level** only.

Melee (related): knives = Dexterity; machete / bayonet / shovel / fists = Strength.

Non-firearm actions still use the older skill + preset path, then apply pain/trauma/concussion **after** the 0–100 clamp so melee accuracy reserve cannot erase those penalties.

---

## 3. Crit overflow (skill surplus)

```text
uncapped_core = skill/aim core before Clamp(…, 100) and before situational factors
core_overflow = Max(0, Round(uncapped_core) − 100)   → +1:1 to crit chance
hit chance    = capped_core × factors, then clamp 2…100
```

Cover still only cuts **hit** chance. Grazes never crit. Opportunity / `guaranteed_noncrit` → crit 0.

---

## 4. Range profile

Weapons expose two hard concepts:

- **BDR (`BulletDropRange`)** — end of the base effective zone.
- **`WeaponRange`** — physical max of a normal shot.

```text
floor = 0.25
p = max(1.25, BDR × 0.05 + Grouping / 100)
E = min(R − ε, BDR + optic_reach × aim_progress)   # effective aim zone with optic
falloff_end = R
if MachineGun or LightMachineGun:
    falloff_end = min(R, E + 16)                   # ~16 tiles to floor, not full R

if d ≤ E:  range_factor = 1
else:      range_factor = floor + (1 − floor) × (1 − t^p)
           where t = clamp((d − E) / (falloff_end − E), 0, 1)

P_core = (shot_skill + aim_gain) × range_factor
```

- Inside `E`: no range penalty.
- Past falloff end to `R`: still possible at **~25%** range factor floor.
- Beyond `R`: impossible (`0%`).
- **MGs**: mid-range on bipod/setup stays full until BDR (+ optic when aimed); past that, accuracy collapses over ~16 tiles — not “sniper MG” out to max range.
- **`Grouping`** shapes post-BDR falloff; compare only together with BDR/R (SVD vs AK is intentional).
- **Damage vs range** uses the same profile via `GetRangeDamageReduction` (result clamped **0…100%** of base damage — never over 100%, never negative).

---

## 5. Close-range weapon / barrel profile

Separate from long-range falloff:

- `CloseRange` — length of the near zone (tiles).
- `CloseRangeFactor` — CTH multiplier at `d = 0` (runtime clamp ~25…150; >100 = CQB buff).

Inside the zone, factor lerps back to 1.0; outside, neutral.

Rough base ladder (tiles / Factor%): pistol `0/100`, SMG `3/95`, carbine·shotgun `5/90`, AR·MG `8/85` (StG-44 anchor), battle rifle `11/80`, sniper `16/70`.

Barrels shift BDR (short ×~70%, long ×~130%, heavy ×~115%), near zone (± tiles / factor), and recoil. Weapon card shows **Close range** as `+N` buff or `−N%` at point-blank.

---

## 6. Optics (specialization, not flat +CTH)

Optics do **not** raise `WeaponRange` or rewrite `BDR`/`Grouping`. They:

1. Shift effective zone via **`optic_reach`** (unlocks with aim level).
2. Multiply click value via optic **`AimAccuracyPercent`** only after `aim ≥ AimAccuracyAimLevel`.
3. Apply a **near penalty** (`OpticMinRange` / `OpticNearFactor`) whenever the optic is mounted — **even on snap shots** — stacked on the weapon close-range factor.

| Family | Role |
| --- | --- |
| Reflex / collimator | CQB / short aim; mild or no near tax; early AA unlock |
| Combat scope | Mid-range; earlier unlock; milder near (~88–92%) |
| Long / sniper optic | Max-aim payoff; harsh near; often ShotAP / crit on full aim |

Old flat optic CTH bonuses (`ScopeCTHBonus`, etc.) were removed so one scope is not double-counted. High mag defaults to harsh near (e.g. ~10× ≈ 35% factor at d=0 if no explicit params).

**Example intent:** SVD beats AK-47 on prepared mid/long shots; it is not required to win every CQB duel with a big scope mounted.

---

## 7. Situational multipliers (one product)

After core is capped at 100, factors multiply once (fixed-point; no per-factor rounding):

```text
P = P_core_capped
  × Cover × Target × Visibility × Suppression
  × MoraleAndStatus × Action × Perk × Component × WeaponCondition
→ clamp(round(P), 2, 100)
```

Neutral = `1.00`. Penalties ∈ (0, 1]. Bonuses can be >1 but still hit the final ceiling.

### Cover / stance (current soft values)

| Situation | Approx CTH factor |
| --- | --- |
| Full cover | ×0.55 (preset −45) |
| Exposed / weak cover | ×0.88 (−12) |
| Crouch, no cover | ×0.88 (−12) |
| Prone, no cover | ×0.77 (−23) |
| Partial cover | interpolate coverage |
| **Dust storm** on cover | extra **−40** CTH on Cover / ExposedCover |

Rule of thumb: solid mid rifle ~80% open → ~40–50% full cover. High skill does **not** flat-absorb cover.

Other rough bands: suppression steps ~0.90…0.30; blind fire ~0.40.

Also: target size, smoke/darkness (visibility), weapon condition/grouping wear, chosen action, perks/components. Same effect must not apply twice.

---

## 8. Suppression, retaliation, Lightning Reaction

- Shooter accuracy cut at **any** range: about **−10 / −20 / −30 / −50 / −70** by tier.
- **Pinned**: cannot retaliate (Hotblood / Shatterhand / HaveABlast / Killzone, etc.); on gain and on own turns while pinned, loses Overwatch (incl. permanent MG sector), Pin Down, Bombard. Weaker suppression does **not** strip prepared fire.
- Partial suppression: retaliation chance ×**90 / 80 / 70 / 60**; accuracy still cut.
- **Lightning Reaction**: base **~50%** once per combat; suppression soft-cuts (**45→30**); Pinned = **0%**; no trigger on Hidden / stealth kill; not on own team turn / already prone / manning emplacement.

**Will:** slight self-recovery each turn; nearby high **Leadership** (≤11 tiles; Negotiator stretches) speeds it; **Psycho** skips ally restore and loses 4 Will/turn unless Berserk. After combat, Will is full.

---

## 9. Grazing (only two sources)

| Source | When | Rule |
| --- | --- | --- |
| **Miss → graze** | Valid shot (`shot_cth > 0`) and miss | Cap **25%** (≥8 tiles); point-blank rises toward **50%**; chance = `min(cap, floor(cap × ((100−CTH)/100)²))` |
| **Cover → graze** | Hit, aware target, not Exposed / aim-shooting / melee / AoE | Proportional to cover CTH bonus; up to **100%** in full cover |

**Removed as graze sources:** flat near-miss bands; fog/dust env graze; C++ LoF smoke/gas graze (`ignore_smoke`). Smoke still hurts **visibility/CTH**. Dust **amplifies cover**, so cover-grazes rise indirectly.

**Graze effect:** ~**40%** damage; no crit; no trauma / Medium+ bleed / hit Pain; **~15%** light bleed only. Thermal full aim (`IgnoreGrazingHitsWhenFullyAimed`) ignores **cover-graze only**.

---

## 10. Bursts, recoil, miss climb

First bullet = normal final CTH. Later bullets:

```text
effective_recoil =
    Recoil
  × (0.5×StrengthFactor + 0.5×MarksmanshipFactor)
  × Stance × Support × ComponentRecoil × action severity…

recoil_retention = clamp(1 − effective_recoil/100, min_retention, 1)
P_bullet(i)      = clamp(round(P_first × retention^(i−1)), 2, 100)
```

- Strength and Marksmanship share control 50/50; stance, bipod/setup, components, perks, actions help retention.
- **`Recoil`** is authored from mass / RPM / platform class (not double-counted in runtime).
- Recoil changes probability **once**. Miss geometry is separate.

### Unsupported MG

No Setup / bipod / deployed sector:

- First-bullet CTH penalty **−50** (heavy) / **−25** (light), scaled by Strength → **0 at Str 100**.
- Recoil class factor **×2.0 / ×1.5**.
- **Grizzly signature only** ignores both; normal `MGBurstFire` does not. Signature also **2×** long burst length, full damage, **2×** suppression.

### Protected bullets / specials

- AN-94 `AbakanBurst` / `AbakanAutoFire`: second bullet (pair) protected from normal retention falloff.
- `JAZZ_ControllableBurst`: first two bullets keep original CTH.
- `BulletHell` (Spike): **action recoil = 0** → every round keeps first-shot CTH.
- Compact high-RPM platforms hold bursts worse than heavy/slow same caliber.

### Miss climb (rifled multishot, not pellets)

After protected windows, true misses climb **up** from aim; offset scales with bullet index × `effective_recoil` (/400). Hits and near-target grazes are **not** shifted. Fire order follows CTH index (no dispersion sort).

### Shotgun pellets

`Buckshot` / `DoubleBarrel` / etc.: **packet**, not a queue. All pellets share `P_first`; each rolls separately; **no** retention between pellets; **no** queue-climb. Buck ≈9 pellets; birdshot/salt ≈20. `BuckshotBurst` = several shells, each with its own packet.

---

## 11. Combat actions (what you can fire)

Button needs all four: weapon supports mode → class/state allows → perk/signature if required → AP/ammo/stance-setup OK.

### Core modes

| Action | Behavior |
| --- | --- |
| `SingleShot` | One shot; no burst recoil chain |
| `BurstFire` | Short burst (`BurstShots`); retention + miss climb |
| `AutoFire` | Long burst (`AutoShots`); denser, heavier stack |
| `AbakanBurst` / `AbakanAutoFire` | AN-94 protected pair |
| `DualShot` | Two-hand / paired; each shot separate |
| `MGBurstFire` | +1 AP at burst length / +2 at long auto string; full Recoil |
| `Buckshot` / `BuckshotBurst` / `DoubleBarrel` | Pellet packets; double barrel = 2 shells, AP like Buckshot |
| `AttackShotgun` | Meta button → actual shotgun mode (`AimType` line) |
| `Overwatch` | Cone interrupts; each from real position. Carbine with autofire module interrupts with **short burst**. HawksEye + SniperRifle: Overwatch **1 AP**, leftover AP kept, 1 interrupt |
| `PinDown` | Reaction threat on a target; own action factor; not a hit guarantee |
| `MobileShot` | Pistol shot after move |
| `RunAndGun` / `_Carbine` | SMG packets while moving / longer carbine variant; damage rollover **N×D**; CD clears on signature kills too |
| `JAZZ_ControllableBurst` | Protected first bullets; recharge on kill |
| `MGSetup` | Deploy support; does not fire. Stationary map MG stays manned after load |
| `CancelShot` / `CancelShotCone` | Strip prepared fire; not on active JAZZ catalog `AvailableAttacks` (cone is perk-gated) |

### Class / signature techniques (examples)

| ID | Class / who | Payoff |
| --- | --- | --- |
| `JAZZ_Fanning` | Revolver | Fast fan; heavy recoil severity |
| `JAZZ_Bullseye` | Sniper | Expensive prepared head shot; crit effect ≠ automatic hit |
| `JAZZ_SmgStorm` / `RunAndSMGStorm` | Autopistol | Dense close fire + suppression / mobile packets |
| `JAZZ_Mozambique` | Pistol | Two body + head; each own CTH |
| `JAZZ_Zipper` | SMG | Short bursts walking up the body |
| `JAZZ_DoubleTap` | Pistol | Cheap controlled pair |
| `JAZZ_Salvo` | Battle rifle | Hard fast pair; 2nd recoils |
| `JAZZ_ManeuverAR` | AR | Two bursts from start, then move |
| `JAZZ_LargeAutoFire` | AR / BR / LMG | Expensive long string |
| `JAZZ_TargetSweep` | Autos | Burst (fallback single) per enemy in cone; refund AP if zero shots |
| `JAZZ_JokerShot` | BR / sniper | Single shot, extreme suppression |
| `JAZZ_MobileShotgun` | Shotgun | Close in, then area shot |
| `JAZZ_MGSuppressionFire` | MG | Two suppressing bursts into one zone |
| `BulletHell` | Spike | 15–30 cone rounds, **no recoil**; Will drain to all in cone even without hits; CD on kill |
| `GrizzlyPerk` | Grizzly | 2× long burst, full damage, ignore unsupported MG taxes, 2× suppression |
| `Jazz_Perk_Buzz` | Passive | +50% bullets on supported burst/auto; does not raise first-shot CTH |
| `Jazz_Perk_Lynx` | Passive | Sight; no confirmed long-range CTH bonus yet |

Named merc actives adjacent to combat: Meltdown panic aura, Igor drinking buff (−CTH / +melee), etc.

Perks may change AP, ammo, suppression, retention, or a single multiplicative **`PerkFactor`**. No hidden flat +CTH. Same factor for UI / AI / shot.

Combat bar is **two rows** (24 + signature slot). **Take Cover** / **Overwatch** stay visible; Take Cover greys without wall (usable at cover, not Prone). Fold stock / flashlight = small buttons by weapon icon, not main row.

### Reload / Unjam

- Box mags: full magazine swap.
- Tube shotguns / break-actions / revolvers: empty = Reload; partial = **Top up** one round for `ceil(full cost / capacity)` AP (min 1); full = disabled.
- **Unjam** on jammed active firearm: **4…1 AP** by Mechanical; `MrFixit` keeps perk AP. Failed player unjam can permanently cut max resource / break; AI clear jam does not wipe resource.

---

## 12. After a hit: damage, armor, wounds

- Penetration is fractional: `PenetrationClass + 0.1×PenetrationBonus` vs armor classes 1–5.
- Ammo grades change jam, crit, bleed, pen (FMJ / JHP / Poor / crafted, etc.).
- **Solid damaging hit:** +1 Pain; can bleed (heavy bleed more from **JHP**); zone trauma (arms/legs/ribs/head) from after-armor damage (≥20 light; ≥50% HP or down → heavy). Grazes skip trauma / hit Pain / Medium+ bleed.
- Armor stop can still apply **behind-armor** light trauma + pain, no bleed.
- Pain cuts AP and accuracy (incl. melee); clears when combat ends. Morphine clears/blocks Pain and can rally downed.
- Suppression applies from volume/fire (tracers mark targets even on miss if `shot_cth > 0`).

Weapon wear: shots degrade `WeaponResource`; bad condition hurts grouping/CTH then raises jam; independent max-wear rolls; jam chance shown on card.

---

## 13. Grenades, GLs, rockets (related fire)

Throws / GL shots **always** have light scatter — no perfect pin-point.

| Ordnance | Skills |
| --- | --- |
| Hand grenades | Strength (range) + Dexterity + Explosives (cleanliness) |
| Underslung / GL / rockets / mortar | Marksmanship + Explosives (~50+ comfortable) |
| Pipes / shaped charge / TNT | Mostly Explosives (~60+ or high mishap) |

Risk rises **smoothly** to circle edge (no green→black cliff). Suppression / Inaccurate worsen mishap and scatter size.

Aim UI: ring **size** = damage AoE; ring/arc **color** = mishap + scatter risk. Frag/HE/flashbang: **guaranteed concussion** on blast hits; **one** zone trauma using bullet thresholds; **knockback** only in inner aim ring (`CenterAreaOfEffect`) via Strength+Health vs pre-armor damage. Smoke/gas/Molotov: no bleed / concussion / knockback package.

---

## 14. LOS vs LoF (sight vs bullet)

- **LOS (`HasVisibilityTo`)**: sight range, darkness, smoke (−70), stealth.
- **LoF**: geometric bullet path.

Team LOS unlocks choosing a unit as a model target; shot still needs clean LoF. Personal LOS is a score bonus for AI, not required for Dump fire if team sees the target. Smoke can block LOS while LoF through smoke remains (no smoke-graze). Shots into solid rock / cliff / wall **stop** — no punching unbreakable ground.

**Player** shots use the normal LoF pipeline. **AI Dump** on large maps uses cheap rays for perf (same CTH as crosshair when line is clear).

---

## 15. AI shooting behavior

- Prefers free cover over stacking in one bush; soft crowding penalty; medics ignore crowding to reach patients; melee softer crowding floor.
- Pathing scoped to this-turn reach (big maps don’t freeze for minutes).
- Without sight: Overwatch aims where you can **step into view** (corner/door), or 1–3 tiles off last sound in the open; night prefers lit / night-sight or skips; won’t plant into a wall/rock.
- If they can’t see you but you can see them, they relocate toward last-sound firing range rather than stand still to be farmed.
- Deserters keep fleeing visibly within ~16 tiles of mercs; despawn only at exit / when far.
- Visible shouts (orders, panic, grenade, MG setup, long dash): max two per team per turn; silent on FF / out of sight.

---

## 16. UI contract

**Normal play** — qualitative signs only (~1 sign per ~10 points of displayed effect strength):

```text
Aiming         +++
Distance       --
Cover          ---
Suppression    --
Recoil         ---
```

Hides exact %, `×0.55`, and intermediate CTH. Stage rows (Aim / Distance / Optic) compare vs the same attack without that stage.

**Debug / modding tools** — final %, `P_core`, each factor %, before→after, per-bullet burst chances. Same math as the executed shot.

---

## 17. Runtime map (for orientation)

| Concern | Where |
| --- | --- |
| CTH / range / optics / recoil core | `Code/AccuracyRangeCTH.lua` |
| Shot sequence / execute | `Code/ExecFirearmAttacks.lua` |
| Actions / FirearmAttack hooks | `Code/CombatActions.lua` |
| Crosshair breakdown | `Code/CrossHairUI.lua` |
| Graze / damage precalc | `Code/System_OR_Weapons.lua` |
| Crit overflow | `Unit:CalcCritChance` + `JAZZ_CTHGetShooterCore` |
| Generated actions / CTH modifiers | ModItems in `items.lua` |
