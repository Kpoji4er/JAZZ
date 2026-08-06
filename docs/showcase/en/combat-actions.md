# Combat actions

[Overview](home.md) · [Combat and accuracy](combat-and-accuracy.md) · [Weapon classes](weapon-classes.md) · [Русский](../ru/combat-actions.md)

## Where the button comes from

An attack appears when all of these hold:

1. the weapon physically supports the mode;
2. the class and weapon state allow the action;
3. the character has the required perk or personal ability (if any);
4. AP, ammo, and stance/setup conditions are met.

A perk can unlock an action or change AP, bullet count, suppression, or recoil control. Accuracy still goes through the same pipeline as a normal attack.

## Reload / Top up
Tube-fed shotguns, break-actions, and revolvers keep one reload button that changes with the load: empty uses full Reload; a partially loaded weapon shows **Top up** and adds exactly one round for a rounded-up share of the full cost (minimum 1 AP); a full weapon disables the button.

### Unjam

When the active firearm is jammed, **Unjam** appears on the regular action bar. It requires enough AP, does not fire a shot, and disappears once the jam is cleared.

## Core modes

| Action | What it does |
| --- | --- |
| Single shot | One direct shot, no burst recoil chain. |
| Burst | Short burst; first bullet normal, then retention; misses climb upward along the string. |
| Auto | Long burst: denser fire for ammo and stacked recoil; climb stronger on the tail. |
| MG burst | Costs +1 AP at burst length or +2 AP for the longer automatic string; uses full weapon recoil, so Strength and support remain critical. |
| Buckshot / buckshot burst / double barrel | Pellet packet (buckshot ≈9); same hit chance per pellet, no in-packet recoil or queue-climb. |
| Overwatch | Cone control; each interrupt resolves from the real position. |
| Pin Down | Keeps a target under reaction threat (not a hit guarantee). |
| Mobile Shot / Run and Gun | Shot or packets during/after movement. |
| MG Setup | Sets up the gun position; does not fire by itself. |

## Example JAZZ class techniques

| Technique | Class | Payoff |
| --- | --- | --- |
| Fanning | revolver | fast fan series with heavy recoil weight |
| Bullseye | sniper | expensive prepared head shot |
| SMG Storm | autopistol | very dense close series with heavy recoil and suppression |
| Mozambique | pistol | two body + final head, each with its own CTH |
| Zipper | SMG | short bursts walking up the target |
| Double Tap | pistol | cheap controlled pair |
| Salvo | battle rifle | powerful fast pair |
| Controllable Burst | AR / LMG | short burst where the first two bullets keep the original CTH |
| Mobile Shotgun | shotgun | close in, then area shot |
| MG Suppression | machine gun | two suppressing bursts into one zone |

Full ID tables and edge cases live in the repository `docs/wiki/combat-actions.md`.
