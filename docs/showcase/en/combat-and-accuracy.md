# Combat and accuracy

[Overview](home.md) · [Weapon classes](weapon-classes.md) · [Combat actions](combat-actions.md) · [Русский](../ru/combat-and-accuracy.md)

## Essentials

- A possible shot has a chance from `2%` to `100%`.
- `0%` means the shot is physically impossible: no valid trajectory or the target is beyond the attack limit.
- `100%` is reachable for a skilled shooter against an open standing target with full aiming at optimal range.
- Cover, small target size, poor visibility, suppression, and awkward optics cut into the ideal chance.

## Snap shooting vs prepared fire

Shots with no aim clicks lean primarily on **Agility**.

Each aim click gradually unlocks **Marksmanship**. An extra click never makes the chance worse. Full aiming matters most for snipers and prepared long-range fire.

The IMP **Sniper** perk grants +1 maximum aim clicks with any weapon.

The weapon sets how many aim clicks you get, how much each click is worth, where range falloff begins, how accuracy holds past the effective zone, and how bursts lose accuracy to recoil.

The legacy `Handling` stat has been removed and is not used in hit chance.

## Range and optics

- **BDR** — end of the base effective zone.
- **Range** — hard limit of a normal shot.

Inside BDR there is no range penalty. Past it, chance falls gently at first and then faster, but a still-possible shot near the hard limit retains about a quarter of its range profile instead of dropping to zero.

Weapons also have a close-range profile: pistols and compact guns are comfortable at point-blank range, while long rifles and long barrels can be weaker across the nearest tiles — rough zone lengths: SMG ~3, carbine/shotgun ~5, assault/MG ~8 (StG-44), battle rifle ~11, sniper ~16. A short barrel shifts that comfort closer and boosts close-range effectiveness (weapon card row **Close range** shows the barrel-style `+N` after base + attachments); a long barrel shifts it farther away. A base near-zone penalty without a boosting barrel also appears as its own labeled row (`−N%` and zone length), not as a hint bullet.

Optics do not make the bullet travel farther — they change weapon **specialization**: reflex raises effectiveness vs irons, combat scopes own mid-range, full optics reward max aim. Effective-zone shift and optic AimAccuracy% apply only after that aim threshold. Strong scopes help at medium and long range and **hurt up close just by being mounted** — the optic near penalty applies even on snap shots and stacks with the weapon’s close-range profile.

## Cover and multipliers

Penalties are multipliers: high skill does not flat-absorb cover.

**Full cover** leaves roughly **half** of the open-target chance (rule of thumb: a solid rifle shot at mid range drops from about ~80% open to ~40–50% behind full cover). Partial cover and crouch/prone without cover cut less.

Chance can be affected by cover and visible target size, stance, visibility/smoke/darkness, suppression and statuses, weapon condition and components, the chosen action, and perks. The same effect should not be applied twice.

## Suppression, retaliation, and Lightning Reactions

- Suppression cuts the shooter’s accuracy at any range (about −10 to −70 by tier).
- A **Pinned** unit cannot counterattack; a partially suppressed unit still can, but with the accuracy penalty.
- **Lightning Reactions:** about **50%**, once per combat; does **not** trigger on a stealth kill / Hidden attack.
- **Psycho:** Will fully recovers after combat; per-turn Will drain is milder than before.

## Bleeding, pain, trauma, and medicine

- Bleeding has three tiers (**3 / 6 / 12** HP per stack per turn). Hotbar: **Field Bandage** (`JazzBandage`, ~1 AP) drops the worst stack by **one tier** (no Medical; stacks to **30**); **Bandage** uses IFAK (stack **5**) / Medkit (stack **3**) — one use = one item (HP heal + stronger bleed clear).
- **Heavy** bleed from hits comes from **expanding** ammo (JHP).
- **Pain** cuts AP and accuracy (−1 stack/turn): each solid damaging hit adds **+1** Pain (grazing scratches do not). **Morphine** (stacks to **10**) suppresses pain penalties and does not stop bleeding or trauma.
- **Zone trauma** (arms / legs / ribs / head): light / medium / heavy. Using an injured zone adds Pain stacks once per zone per turn: light **+1**, medium **+2**, heavy **+3**. Each **unused heavy** zone still adds **+1** Pain at end of turn. Medium+ also adds zone penalties (−accuracy, move cost, start AP, sight). **Armor on the hit zone lowers trauma chance when pierced; if armor stops the round**, you can still take **behind-armor trauma** (light trauma + pain, no bleeding). Going down applies a **heavy** trauma package; combat **Wounded** stacks from HP loss stay off. Bandages do not heal trauma. Status Information shows **hours until the next progress check** (may improve or worsen on the campaign clock). A squad **field Treat Wounds** operation does not clear trauma instantly — it marks traumas as **healing**: faster checks, **each check improves** the tier (light clears / medium→light / heavy→medium), no worsening. On the campaign map, HP recovers slowly — about **1** HP/hour (Treat Wounds patients faster; R&R faster still).
- In combat, party portraits show the same statuses as satellite (not only Wounded).
- Leg hits apply zone trauma (`Legsshot`), not the old **Slowed** status.
- Combat-start grit (~25% Temp HP) is **removed**.

## Grazing hits

- **Miss → graze:** lower CTH means a higher chance a miss still clips the target (square curve, max **50%**; about **32%** at 20% CTH, about **2%** at 80% CTH). High CTH barely grazes.
- **Cover:** cover strength in the hit-chance calc sets the chance a hit becomes a graze — up to **100%** in full cover.
- Smoke/fog/dust alone no longer force grazing hits (smoke still hurts visibility).
- A graze deals about **40%** damage, with no crit, no trauma / `Wounded`, and **no +1 Pain from the hit**; about **15%** chance of **light** bleed only.

## Burst recoil

The first bullet uses the normal final chance. Each next bullet keeps only part of the previous accuracy (**recoil retention**).

Strength and Marksmanship equally improve control, alongside stance, bipods/setup, components, perks, and special actions. Compact high-RPM platforms are less controllable than heavier, slower examples in the same caliber. Recoil changes hit probability once; burst misses climb upward further along the string (the same control tightens both chance decay and climb). Hits on the aimed target are not shifted by climb. Shotgun pellet packets have no queue-climb.

## Grenades and launchers

Throws **always** have light scatter — there is no perfect pin-point landing.

- **Up close** (about half throw/launcher range): light scatter only, no big mishap.
- **Farther out**: mishap chance rises (big deviation + notification). Suppression and Inaccurate worsen both chance and scatter.
- Skills: hand grenades — **Dexterity + Explosives** (confident around **30**); underslung/GL/rockets — **Marksmanship + Explosives**; pipes/TNT — mostly **Explosives** (~**60**).
- While aiming: ring **size** = damage area; ring and throw-arc **color** = mix of mishap risk and light-scatter size on the same green→red scale as the crosshair. Up close (0% mishap) the color can still warm as scatter grows.
- Frag / HE / flashbang: **guaranteed concussion** on blast-hit units, plus a chance of **zone trauma**. Smoke / gas / Molotov use their own packages, not concussion.

## What the UI shows

Without debug:

```text
Aiming         +++
Range          --
Cover          ---
Suppression    --
Recoil         ---
```

More signs means a stronger effect. Crosshair, AI, and the real shot share one calculation.
