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

The weapon sets how many aim clicks you get, how much each click is worth, where range falloff begins, how accuracy holds past the effective zone, and how bursts lose accuracy to recoil.

The legacy `Handling` field is not used in hit chance.

## Range and optics

- **BDR** — end of the base effective zone.
- **Range** — hard limit of a normal shot.

Inside BDR there is no range penalty. Past it, chance falls smoothly; near the hard limit a still-possible shot keeps a minimum chance.

Optics do not make the bullet travel farther. They push the effective aiming zone farther as you aim. Strong scopes help at medium and long range and can hurt up close.

## Cover and multipliers

Penalties are multipliers: high skill does not flat-absorb cover.

Chance can be affected by cover and visible target size, stance, visibility/smoke/darkness, suppression and statuses, weapon condition and components, the chosen action, and perks. The same effect should not be applied twice.

## Burst recoil

The first bullet uses the normal final chance. Each next bullet keeps only part of the previous accuracy (**recoil retention**).

Strength, stance, bipods/setup, components, perks, and special actions improve control. Recoil changes hit probability once; bullet spray after a miss is not a second hidden penalty.

## Grenades and launchers

Throws always have light scatter. Up close you mostly just scatter; at longer range mishap chance rises. Hand grenades use Dexterity + Explosives (confident around 30). Underslung/GL/rockets use Marksmanship + Explosives. Pipe bombs lean harder on Explosives. Blast-ring color while aiming matches the crosshair hit-chance scale (green→red); ring size is the damage area, not a scatter radius.

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
