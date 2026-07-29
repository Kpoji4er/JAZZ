# Weapons and components

[Overview](home.md) · [Weapon classes](weapon-classes.md) · [Русский](../ru/weapons-and-ammo.md)

## Tier and sub-tier

A **tier** is a noticeable power band inside a class. Moving up a major tier raises overall combat value; it does not have to raise every individual stat.

A **sub-tier** orders close variants (magazine, RoF, range, reliability, modules) without a major-tier power jump.

`UNIQ` means a unique variant. Items with no tier are quest/technical or not yet classified.

## How to read the stats

| Field | Meaning |
| --- | --- |
| Damage | Base damage per bullet before armor and other effects. |
| Penetration | Armor class scale 1–5; ammo sets class plus a fractional tenth-step bonus. |
| Mag | Magazine capacity. |
| AP shot / reload | Attack tempo and upkeep cost. |
| Aim | Aim clicks × value per click. |
| BDR / range | End of the effective zone / hard shot limit. |
| Accuracy hold | How well precision holds past the effective zone (read with BDR and range). |
| Recoil | How hard follow-up bullets lose accuracy; lower is easier to control. |
| Modes | Single, burst, auto, and special actions. |

`Handling` is not used in current hit chance.

## Components

- **Optics** — aim clicks, effective-zone shift, overwatch; strong scopes can hurt up close; there is no flat CTH bonus just for having optics.
- **Barrels** — range, BDR, hold, damage, tempo, reliability.
- **Muzzle devices** — noise, recoil, reliability, stealthy fire.
- **Bipods / support** — burst control in stance or after setup.
- **Stocks and grips** — tempo, recoil, modes, mobility.
- **Magazines** — capacity and sometimes reload cost.

Full tables:

- [Weapon catalog by tier](../../wiki/weapons/README.md) (currently Russian)
- [All components](../../wiki/weapons/components.md)

Numbers are built from canonical CSVs via `scripts/docs/weapons-docs.mjs` and published to the GitHub Wiki with the showcase — do not hand-edit them on the wiki.
