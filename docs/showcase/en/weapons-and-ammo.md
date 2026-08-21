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
| Penetration | Armor class scale 1–5; ammo sets class plus a fractional tenth-step bonus. A loaded weapon shows the same number as its ammo (e.g. `.30 Cal` **1.6**). |
| Mag | Magazine capacity. |
| AP shot / reload | Attack tempo and upkeep cost. |
| Aim | Aim clicks × value per click. |
| BDR / range | End of the effective zone / hard shot limit. |
| Accuracy hold | How well precision holds past the effective zone (read with BDR and range). |
| Recoil | How hard follow-up bullets lose accuracy; lower is easier to control. Platform mass, size, and cyclic rate differentiate guns in the same caliber (compact/high-RPM SMGs climb harder than heavy low-RPM ones). |
| Modes | Single, burst, auto, and special actions. |

The `Handling` weapon stat has been removed from weapons and UI.

## Resource and servicing
Regular repair restores current resource only; it does not restore lost reliability capacity. Ordinary **Parts** in Item Repair are billed from **condition percent** (about 1 Part per ~5% restored), not from the large absolute weapon-resource pool. **Barrel Parts** are used for barrel work; if a removable scope is installed, repair also costs **Scope Parts**. Scrapping a firearm yields ordinary **Parts** (from the weapon’s scrap value) into the squad bag; a successful Mechanical roll can also grant **Barrel Parts** equal to the barrel’s install cost (typically 1–3), not the modification price. The weapon card shows effective jam chance: it respects the **weapon’s own Reliability** (about 5…95; at **95** even poor ammo adds no base jam) and its ammunition, but peaks near 5% on a perfect gun (and at most ~7-10% in the high-80s band) even with poor ammo. Current condition and permanently lost maximum resource add risk through soft steps (full worse wear + half the other); an MP40 is roughly 0% / 2% / 7% at 100% / 90% / 80% condition after a smooth -5pp softener at perfect service, mid wear on a reliable gun stays around ~8% dry / ≤~20% in rain, and reaches 100% only when fully broken. Mechanical reduces the result. **Unjam** costs **4…1 AP** by Mechanical. A failed merc unjam can cut max resource by 1–3%; NPC/AI clear jams without that wear. Removable attachments become inventory items when successfully removed; the rollover title lists which firearms they fit (including magazines), and hovering or dragging highlights compatible weapons. Identical modules (several bipods of the same type) stack in the squad bag and survive bag sort and save/load; different modules (collimator vs compensator) do not merge. Reinstall via the modification cabinet or drag-and-drop (Mechanical ≥30, grenade launcher ≥40 — best Mechanical in the squad). A failed removal always cuts max by 1%; on a worn gun the module may **break** (scopes salvage as Scope Parts). An **integrated suppressor** (PB, Val, MP5SD, etc.) is part of the gun: it cannot be removed and is not ejected when the weapon is scrapped.

## Per-round top-up
Tube-fed shotguns, break-actions, and revolvers use normal Reload when empty. Once they hold at least one round, that same slot becomes **Top up** and loads exactly one round for a rounded-up share of the full reload cost (minimum 1 AP). AA12 and USAS-12 retain full reloads because they use detachable magazines.

**12-gauge shells:** ammo type sets the pellet packet — buckshot ≈9, birdshot/salt ≈20; slug is a single projectile. **Saltshot** immediately fills **Pain** to the cap (8) on a non-graze hit, even when armor absorbs all damage.

## Disposable launchers
**M72 LAW** has one embedded shot: it cannot be reloaded or repaired. After any shot that is fired, including a mishap, the launcher leaves the inventory and a visible empty tube remains on the ground. The **RPG-7** remains reusable and reloads separate rounds from the backpack. The last round is fully consumed: no leftover `0/1` dummy, and Reload will not spend AP on an empty stack.

Loadout ammo stacks do not grow past the pocket cap. If a stack is already over that cap, the extra rounds go to the **squad bag** instead of disappearing.

## Components

- **Optics** — change weapon **specialization**, not flat CTH: aim clicks, zone shift and optic AimAccuracy% **only after** enough aim; strong scopes hurt up close even on snap.
- **Reflex sights** — better **vs irons**: `MinAim` + −1 MaxAim + CloseRange soft; AimAccuracy% 120→160 from aim≥1 (~+20% CQB at top); **overwatch** without AA% (Open/Pistol get **2** OW shots). **Eotech** Universal T4: 135 + mid OW.
- **Combat scopes** (2–4×) — **mid** specialization; AimAccuracy% 125→155 gated by AimLevel; mild near; no ShotAP/crit. ACOG unlocks earlier than PSO; at full aim PSO ≈ ACOG.
- **Long scopes** — buff **max aim** (+ long plateau): T1 vintage (PU/2×, AA% ~110); T2 PSO (AA% 155 @ AimLevel 3); T3+ 6×…10× (mild AA% 115→125). ShotAP, crit, near tax.
- **Night scopes** — dark + near/OW tax.
- **Barrels** — effective distance: short better up close (−BDR, near↑, Recoil↑); long better far (+BDR, near-tax, Recoil↓); R ±1 only.
- **Muzzle devices** — compensator = Recoil; suppressor ladder = quiet + StealthKill↑ by tier (pay Grouping/Rel/Jam, no Recoil); M2/M3 flash hider = Recoil + StealthKill, does not silence; chokes = buckshot pattern. No range from muzzle.
- **Bipods** — single `Bipod`: prone CTH+10 and +1 shot before recoil while prone (Under variants match).
- **Side** — flashlight = dark ignore + light (on/off); tac device = light + OW/Mark; laser = distance-capped CTH with falloff after 5 tiles; UV = night laser + stealth.
- **Stocks** — Normal = empty default; Heavy Recoil−5+AimAccuracy%; Light≡Unfolded Recoil+2 (Light cannot fold); folded/no-stock = ShootAP−1 + Recoil+5 + AA↓ + OW+2.
- **Grips** — small & cheap: vertical = Recoil−1 (queue control); tactical / wrap = CloseFactor+5 up close; ergo = AimAccuracy 105%.
- **Magazines** — the number on a magazine is its exact capacity: small = fewer rounds + Reload**−1**/Rel↑; expanded = more rounds + Reload**+1** (no Rel/AA); large = Reload**+2** + Rel−/AA−.

Full tables:

- [Weapon catalog by tier](../../wiki/weapons/README.md) (currently Russian)
- [All components](../../wiki/weapons/components.md)

Numbers are built from canonical CSVs via `scripts/docs/weapons-docs.mjs` and published to the GitHub Wiki with the showcase — do not hand-edit them on the wiki.
