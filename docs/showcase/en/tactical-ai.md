# Tactical AI

[Overview](home.md) · [Command aura](officer-aura.md) · [Combat and accuracy](combat-and-accuracy.md) · [Legion units](legion-units.md) · [Русский](../ru/tactical-ai.md)

Enemies do not wander at random. Each fighter has a **role**, the squad follows an **officer order**, and tiles and shots use the same hit-chance rules you do. On the satellite map the Legion is a different system — [Legion on the strategic map](legion-strategy.md).

You do not issue the order. The officer changes the fight style on their own; radii and the order table live on [Command aura](officer-aura.md).

## How the enemy turn plays

1. **Support before the push.** The medic, flares, **one** smoke curtain, and machine-gun setup act first.
2. **The line.** Riflemen, snipers, and the commander take a tile and shoot.
3. **The press.** Assaulters and flankers come later — after the line has planted.
4. **After the shot.** Anyone who should break contact moves to cover or plants a cone instead of standing on the same tile.

On large fights (**M1** landing, the waterfall) **allied** turns are sped up: less “thinking” pause and auto fast-forward of ally animations when Fast Forward is on. Crocodiles and hyenas do not use this AI — they go for the nearest enemy, as in vanilla.

## Roles

| Role | What they do |
| --- | --- |
| **Assault** | Presses, throws grenades, and sometimes wraps a flank if the front is jammed. A knife in the second hand slot means they cut if they have enough AP to reach and hit once. |
| **Line** | Holds range, cover, and height. A sniper / marksman will not crawl into point-blank under a long scope. |
| **Flanker** | Walks around for a wrap. On **Push** they may hit you head-on. |
| **Machine gun** | Plants a cone. Behind low cover they crouch and unfold the bipod — not always prone. If you are already within **8** tiles they shoot first instead of spinning a distant sector. After setup they can still dump a burst. |
| **Medic** | Treats **before** the rest. Bleeding beats a high HP percent; they walk up to the patient and ignore crowding. Not every bandage carrier becomes a medic — usually the dedicated bone-setter, or one fill-in. |
| **Commander** | Stays off the tip. Writes the aura and the order. Sergeant — **15** tiles, lieutenant — **25**, captain — **the whole map**. |
| **Heavies** | The rocketeer stays in the rear and shoots. The mortar looks for **open ground**: Bombard does not work indoors. |

No dedicated sniper or gunner — the commander **assigns via aura** one optics/bolt or SMG/AR fighter. On **Push** they assign **one** assaulter, not the whole squad.

Rebels use the same role scheme.

## Tiles

The AI wants a tile it can shoot from **and** that is not open ground.

- Cover is scored against the people who can actually see and shoot, not an average of everyone.
- Two fighters do not share a tile. Shoulder-to-shoulder on one bush loses to free cover next door.
- Ground where their own just dropped is less attractive; several casualties nearby make it worse. This is a preference, not a wall: a narrow passage still works. Melee is penalized less.
- The line and snipers climb. Nearby assaulters more often stand **between** the sniper and you than leave them alone in a field.
- The retinue stays near the commander instead of scattering across the map.
- A lone Legionnaire far from the pack runs to the group. Rocketeers and mortars do not — they stay back and shoot.

On large maps the AI only paths within **this turn’s** reach. A clear line can hit (same math as the crosshair). Shots into rock, cliff, or wall stop there.

Empty human hands: they pull a firearm from the other hand slot or from inventory and reload it. Heavy weapons and the flare pistol are not grabbed this way.

## Shooting and specials

- Hit chance is the same calculation you use. There is no separate “AI accuracy”.
- **Focus fire** shoots the named target (the aura tooltip shows **who**).
- **Smoke** is a curtain on an overwatch exit, or on an ally who has **already** acted. It is not a hat on people who have not moved yet. Smoke cuts sight; it does **not** turn the shot into a graze.
- **Flares** exist only at **night** and underground. At night a sniper **holds** until the others light the ground, then shoots. **Fog and dust** have no “wait for light” plan: shorter range, cover, a cone on the last sound.
- Frag grenades per team turn: **First Blood** — **1** full throw (the next is much weaker), **Commando** — **3** full throws, **Mission Impossible** — no cap. Smoke and flares are outside that budget.

## When they cannot see you

- The line will not sit in a corner to be farmed. They close to firing range of the last sound (**14–20** tiles, not onto your tile). Two scouts / pressers may come closer.
- A no-sight cone covers the tile **where you can step into view** (house corner, doorway, rock edge), not the wall.
- A **sniper / firing line on high ground** that can see that exit **stays** and holds the cone there — they do not drop down “closer to the sound”. An assaulter at the foot still relocates.
- Anyone you can already see while they cannot see you must move.
- On **Fall back**, a shooter you still see peels behind a corner/rock and overwatches the **tile they vacated**, at the edge of cone range.

## Medic, panic, deserters

Any bleed tier is treated even if HP is still high. A dedicated medic acts early and does not switch to assault while someone needs a bandage.

Low-tier Legion (T1–T2) breaks more often; elites almost never run. Rebels are calmer than low-tier Legion.

A panicked fighter may reach a map exit and **despawn**. While your mercs are within about **16** tiles they will not vanish behind the nearest rock — they keep running in plain sight.

## Out of combat

- Approaching a sentry **from behind**: the suspicion bubble is shorter — about **10** tiles. From the front the long view stays. The cap is off in combat.
- Stealth: camo, Stealthy, and cover stack. Brush barely hides by itself but strongly boosts camo.
- High sector Heat makes sentries meaner: suspicion builds faster.

## Shouts

A visible enemy sometimes shouts over their head: a new order, panic, a grenade, a weapon-class swap, MG setup, a long dash. Same speech bubble as voiced attacks — no audio. At most **two** shouts per team per turn. Fast-forward and out-of-sight stay quiet.

## What this is not

- There is no “give order” button.
- The officer does not path the whole squad tile by tile — they set the style, the focus-fire target, heights, and cover.
- Satellite patrols, QRF, and convoys are [Legion on the strategic map](legion-strategy.md), not this AI.
- Animals stay vanilla.

See also: [command aura](officer-aura.md), [combat and accuracy](combat-and-accuracy.md), [Legion units](legion-units.md).
