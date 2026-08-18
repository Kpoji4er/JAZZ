# Legion on the strategic map

[Overview](home.md) · [Legion units](legion-units.md) · [Ernie campaign](ernie-campaign.md) · [Русский](../ru/legion-strategy.md)

On **Ernie**, the Legion runs Fort L'Eau Bleu (sector I7) through a regional HQ. With the maps package the same Global AI also runs **Port Cacao environs** (**P17**), the **Great Desert** (**E10**), the **Mountain Steppe** (**D18**), **Fleatown environs** (**H19**), **La Barrier** (**L15**, patrols into Cacao/Fleatown, larger garrison), and the **Great Forest** (**G22**+**K21**, shared treasury); Major HQ is **B28**. Major supply order: Ernie → La Barrier → poorest others. Until gear tier **T2-1**, mainland regions accrue resources very slowly, rarely order combat squads, and send no QRF; recruiters unlock only after the first Major delivery. On the satellite map, squads show a **role** icon and a **current task** on hover; sector **fill** is ownership, and a **colored outline** marks region borders.

Without the maps package (**JAZZ Vanilla Maps**) the same Global AI runs vanilla mainland outposts: Major HQ at A20, **one region per Guardpost by nearest outpost** (full land coverage, no orphan sectors, no half-map mega-regions with foreign camps), starting defenders adopted as garrison, tax/recruiting from city/farm stockpiles. **Managed squads are smaller on the mainland** than on Ernie. Enemy gear and container loot scale with Legion tier (mine + 3 days → II, World Flip → III). Before tier II, map legionaries stay **class T1 only** (no day-one jump to veterans/mercenaries); Stronger_Elite → T4 only after World Flip — see [Legion units](legion-units.md). **With the maps package**, gear tier on Ernie rises by campaign time (~2 weeks to T1-3), jumps to II when you **occupy** mainland land, and to III at **5 mines** (details on the units page). Named story NPCs such as **Bastien**, **Pierre** (fort squad `FortressPierre`), and **Captain Pierrot** on Côte d'Azur are not replaced by random legionaries. On Vanilla Maps the Diamond Red opening fight and the evening well squad (G6) also keep vanilla compositions — otherwise miners die in bunches and the well shows a conflict with nobody there. The scripted village counterattack after liberating Ernie (`Ernie_CounterAttack`) still launches from the fort; ordinary vanilla periodic Guardpost sorties from managed outposts stay **off**.

Vanilla-map starting squads whose compositions are replaced by `jazz-units` are capped at **30 soldiers** when a new campaign creates them. Dynamic squads and squads already present in a save are unchanged.

## Squad roles

| Role | What it does | Typical size |
| --- | --- | ---: |
| Garrison | Holds key points | 25–40 (NoMaps: **12–20**) |
| Patrol | Moves between key points, **including yours**; prefers empty ones | small early (~5–8), grows to 12–18; **NoMaps ~4–6 → 8–12** |
| Recon | Deploys on noticeable “noise”; return names the sector where you were spotted | ~4–6 → 8–12; **NoMaps ~3–5 → 6–9** |
| QRF | Only under threat: recon report or a key point you took | grows with time/Heat |
| Reinforcement | Holds border key points near you | grows with time/Heat |
| Support | Small specialist detachment (snipers / MGs / mortar, T3–T4) attached to an existing garrison or reinforcement on the border | **4–7** |
| Tax collector | Tours towns/farms and brings `$` to the fort; loot matches the run’s `$` | small escort early: regular line may stack; no dedicated marksmen |
| Recruiter | Tours towns/farms and brings recruits to the fort | small escort |
| Reinforcement convoy | People from HQ to the fort | small escort |
| Supply convoy | Money ($) from HQ to the fort; amount visible in the task; loot matches `$` | small escort |
| Diamond / cash convoy | `$` from fort to HQ; loot is briefcase/diamonds for that sum | small escort (not a day-one platoon) |
| Retaliation | Heavy strike from the Major’s HQ at very high regional Heat | large dedicated force |

Bloodied squads may fall back to the fort for replacements **when** the outpost can afford `$`/manpower; otherwise they heal at the nearest Legion city/bunker (or at the outpost itself). After a run of orders a squad rests at the **nearest** valid site — city, bunker, or its home outpost (if already there, it does not ride to the fort just to rest); topping up bodies happens only at the outpost. Then it goes out again. Patrols **linger** in route sectors and travel **over land** when a land path exists. On **Mission Impossible** the per-class copy limit is off (sniper/MG caps stay).

Legion mine/town/farm income and starting cash pools are about **4× lower** than before, and new squads spawn less often — the map should not fill with heavy convoys immediately. On the mainland, tax/recruiters from a new fort wait ~3 days, and the daily cap on **new** Legion squads map-wide scales with tier (1 → 2 → 3).

## Factions and logistics

- Whoever captures a fort owns it; after World Flip, Adonis/Army lanes can keep ownership.
- Before Flip, Adonis/Army do not open sat conflict on your sectors; after Flip they are hostile on sat and in combat.
- Convoys route around your sectors; if there is no bypass, a new convoy does not spawn (one already en route finishes). Patrol / recon / retaliation can still enter your territory. Reinforcement and support may spawn and wait for a safe path.

## Recon and Heat

If recon does not find your squad, sector Heat drops a little. If it spots you, it leaves with a report (“player in sector XXX”) and the empty-sector Heat drop does not apply. QRF and retaliation can read those reports.

## What to check in-game

- Ernie Legion squads use distinct role icons and **their own names**, not one shared preset label.
- Cash convoy tasks show `$`; returning recon shows the sector.
- Patrols can enter your sectors, especially empty ones.
- Without high Heat and a real threat, the fort does not spam extra recon/QRF on top of squads already present.
