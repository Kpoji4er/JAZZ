# Legion on the strategic map

[Overview](home.md) · [Legion units](legion-units.md) · [Ernie campaign](ernie-campaign.md) · [Русский](../ru/legion-strategy.md)

On **Ernie**, the Legion runs Fort L'Eau Bleu (sector I7) through a regional HQ. On the satellite map, squads show a **role** icon and a **current task** on hover.

Without the maps package (**JAZZ Vanilla Maps**) the same Global AI runs vanilla mainland outposts: Major HQ at A20, **one region per Guardpost by nearest outpost** (full land coverage, no orphan sectors, no half-map mega-regions with foreign camps), starting defenders adopted as garrison, tax/recruiting from city/farm stockpiles. Enemy gear and container loot scale with Legion tier (mine + 3 days → II, World Flip → III). Before tier II, map legionaries stay **class T1 only** (no day-one jump to veterans/mercenaries); Stronger_Elite → T4 only after World Flip — see [Legion units](legion-units.md).

## Squad roles

| Role | What it does | Typical size |
| --- | --- | ---: |
| Garrison | Holds key points | 25–40 |
| Patrol | Moves between key points, **including yours**; prefers empty ones | small early (~5–8), grows to 12–18 |
| Recon | Deploys on noticeable “noise”; return names the sector where you were spotted | ~4–6 → 8–12 |
| QRF | Only under threat: recon report or a key point you took | grows with time/Heat |
| Reinforcement | Holds border key points near you | grows with time/Heat |
| Tax collector | Tours towns/farms and brings `$` to the fort; loot matches the run’s `$` | small escort early |
| Recruiter | Tours towns/farms and brings recruits to the fort | small escort |
| Reinforcement convoy | People from HQ to the fort | small escort |
| Supply convoy | Money ($) from HQ to the fort; amount visible in the task; loot matches `$` | small escort |
| Diamond / cash convoy | `$` from fort to HQ; loot is briefcase/diamonds for that sum | small escort (not a day-one platoon) |
| Retaliation | Heavy strike from the Major’s HQ at very high regional Heat | large dedicated force |

Bloodied squads may fall back to the fort and wait for replacements. After a run of orders a squad **returns to base to rest and refill**, then goes out again. Patrols **linger** in route sectors and travel **over land** when a land path exists.

Legion mine/town/farm income and starting cash pools are about **4× lower** than before, and new squads spawn less often — the map should not fill with heavy convoys immediately.

## Factions and logistics

- Whoever captures a fort owns it; after World Flip, Adonis/Army lanes can keep ownership.
- Before Flip, Adonis/Army do not open sat conflict on your sectors; after Flip they are hostile on sat and in combat.
- Convoys route around your sectors; if there is no bypass, a new convoy does not spawn (one already en route finishes). Patrol / recon / retaliation can still enter your territory.

## Recon and Heat

If recon does not find your squad, sector Heat drops a little. If it spots you, it leaves with a report (“player in sector XXX”) and the empty-sector Heat drop does not apply. QRF and retaliation can read those reports.

## What to check in-game

- Ernie Legion squads use distinct role icons and **their own names**, not one shared preset label.
- Cash convoy tasks show `$`; returning recon shows the sector.
- Patrols can enter your sectors, especially empty ones.
- Without high Heat and a real threat, the fort does not spam extra recon/QRF on top of squads already present.
