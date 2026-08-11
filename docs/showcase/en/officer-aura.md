# Officer aura

[Overview](home.md) · [Legion units](legion-units.md) · [Perks](perks.md) · [Русский](../ru/officer-aura.md)

In combat, AI officers show **Command aura**; nearby allies get **Under aura influence**. The tooltip shows the **current order** and a small order buff. You do not pick the order — the officer changes it from the situation, and a repeated order gradually loses weight so the squad tries other orders.

## Radius

| Officer | Tiles |
| --- | ---: |
| Sergeant / Leader | **15** |
| Lieutenant | **25** |
| Captain / merc captain / named (e.g. **Ghost**) | **whole map** |

Outside the radius or after the commander dies, influence drops. With several officers, the larger radius wins.

## Orders

| Order | When | Feel |
| --- | --- | --- |
| **Hold the line** | default range | default roles; **+2 CTH** |
| **Push** | enemy ≤ **12** | scouts assault; **+1 AP** |
| **Envelop** | enemy ≥ **24** | flank; **+2 CTH** |
| **Fall back** | ≥2 dead and ≥30% of squad | cover; **−5 CTH** vs them |
| **Focus fire** | sniper / MG / close / wounded threat | finish that target; **+5 CTH** |
| **Occupy buildings** | urban | fight from buildings; **+2 CTH** |
| **Take the high ground** | hills / elevation | high ground; **+2 CTH** |
| **Take cover** | losing a long firefight | cover; **−3 CTH** vs them |
| **Go hidden** | night/fog or stealth OK | **Hidden** |
| **Low visibility — hold** | night/fog, no mass stealth | hold; **+2 CTH** |

If the squad has no dedicated sniper / MG, the commander **assigns via aura** one optics/bolt or SMG/AR fighter (inside the radius). On **Push**, one assigned `pusher` assaults — not the whole squad. Rocketeers stay in the rear. **Mortarmen** stay outdoors — they cannot Bombard from indoors.
