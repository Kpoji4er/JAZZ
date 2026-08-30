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

When the active firearm is jammed, **Unjam** appears on the regular action bar. It costs **4…1 AP** by Mechanical (low skill → 4, high → 1), does not fire a shot, and disappears once the jam is cleared.

The combat action bar is **two rows**. **Take Cover** and **Overwatch** stay on it even when many fire modes and medical actions are available. Without a wall **Take Cover** stays on the bar greyed out; it is usable next to cover (not Prone).

### Fold stock and flashlight

Folding stocks and tactical flashlights toggle via **small buttons next to the weapon icon** (second column beside switch-weapon / reload), not on the main combat action row.

## Core modes

| Action | What it does |
| --- | --- |
| Single shot | One direct shot, no burst recoil chain. |
| Burst | Short burst; first bullet normal, then retention; misses climb upward along the string. |
| Auto | Long burst: denser fire for ammo and stacked recoil; climb stronger on the tail. |
| MG burst | Costs +1 AP at burst length or +2 AP for the longer automatic string; uses full weapon recoil, so Strength and support remain critical. |
| Buckshot / buckshot burst / double barrel | Pellet packet (buckshot ≈9); same hit chance per pellet, no in-packet recoil or queue-climb. Double barrel costs the same AP as a normal shotgun shot — you pay in two shells. |
| Overwatch | Cone control: the farther you place it, the narrower it gets (the wedge does not swell first). A pistol up close is a wide fan; a machine gun close in is thicker than at BDR; a rifle at max range is a thin strip. While aiming, cone color is hit chance against a standing full-height target **with the sector's aim** (rifles / MGs get an extra click, snipers use full aim; ignores your debuffs). After you confirm, the cone is the normal overwatch fill. Interrupt CTH is the same shot plus **−30…0** reaction (not a bonus). A carbine with the auto-fire module interrupts with a **short burst**. **Scope + sniper:** Overwatch costs **1 AP**, leftover AP kept. |
| Pin Down | Keeps a target under reaction threat (not a hit guarantee). |
| Mobile Shot / Run and Gun | Shot or packets during/after movement. |
| MG Setup | Same distance-scaled cone as Overwatch (closer is wider). Does not fire by itself. A mapped stationary MG stays under control after loading a save (no remount needed). |

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

Actions that “recharge on kill” also clear after a **signature** kill (Blood’s flying knives, etc.); the killing signature does not recharge itself.

Spike’s **Bullet Hell** keeps cone aiming and dumps 15–30 rounds **with no recoil** (every round keeps first-shot CTH). Hits use a normal CTH **on an enemy in the cone**; misses fan at chest height and can stray. **Drains Will of every enemy in the cone**, even without a hit. CD on kill. Works with machine guns and AN-94 / other JAZZ full-auto rifles.

Full ID tables and edge cases live in the repository `docs/wiki/combat-actions.md`.
