# Combat and accuracy

[Overview](home.md) · [Weapon classes](weapon-classes.md) · [Combat actions](combat-actions.md) · [Русский](../ru/combat-and-accuracy.md)

## Essentials

- A possible shot has a chance from `2%` to `100%`.
- `0%` means the shot is physically impossible: no valid trajectory or the target is beyond the attack limit.
- `100%` is reachable for a skilled shooter against an open standing target with full aiming at optimal range.
- Skill/aim core above 100 spills **1:1** into crit chance (hit chance still caps at 100%; cover only cuts the hit chance).
- Cover, small target size, poor visibility, suppression, and awkward optics cut into the ideal chance.

## Snap shooting vs prepared fire

Shots with no aim clicks lean primarily on **Agility**.

Each aim click gradually unlocks **Marksmanship**. An extra click never makes the chance worse. Full aiming matters most for snipers and prepared long-range fire.

The IMP **Sniper** perk grants +1 maximum aim clicks with any weapon.

The weapon sets how many aim clicks you get, how much each click is worth, where range falloff begins, how accuracy holds past the effective zone, and how bursts lose accuracy to recoil.

Melee: knives use **Agility**; machetes, bayonets, shovels, and fists use **Strength**. Aimed fire trains **Marksmanship**; snap shots and knives train **Agility**. Combat XP raises level only.

The legacy `Handling` stat has been removed and is not used in hit chance.

## Range and optics

- **BDR** — end of the base effective zone.
- **Range** — hard limit of a normal shot.

Inside BDR there is no range penalty. Past it, chance falls gently at first and then faster; a still-possible shot at the end of that falloff retains about a quarter of its range profile instead of dropping to zero.

**Machine guns** (light and heavy): after the effective zone, that drop to a quarter takes about **16 tiles**, not the full maximum range. You can still fire farther, just not as a sniper burst. Mid-range on bipod/setup stays full until BDR (plus optic shift).

Weapons also have a close-range profile: pistols and compact guns are comfortable at point-blank range, while long rifles and long barrels can be weaker across the nearest tiles — rough zone lengths: SMG ~3, carbine/shotgun ~5, assault/MG ~8 (StG-44), battle rifle ~11, sniper ~16. A short barrel shifts that comfort closer and boosts close-range effectiveness (weapon card row **Close range** shows the barrel-style `+N` after base + attachments); a long barrel shifts it farther away. A base near-zone penalty without a boosting barrel also appears as its own labeled row (`−N%` and zone length), not as a hint bullet.

Optics do not make the bullet travel farther — they change weapon **specialization**: reflex raises effectiveness vs irons, combat scopes own mid-range, full optics reward max aim. Effective-zone shift and optic AimAccuracy% apply only after that aim threshold. Strong scopes help at medium and long range and **hurt up close just by being mounted** — the optic near penalty applies even on snap shots and stacks with the weapon’s close-range profile.

## Cover and multipliers

Penalties are multipliers: high skill does not flat-absorb cover.

**Full cover** leaves roughly **half** of the open-target chance (rule of thumb: a solid rifle shot at mid range drops from about ~80% open to ~40–50% behind full cover). Partial cover and crouch/prone without cover cut less. In a **dust storm**, cover cuts harder: about **−40** extra CTH on top of the cover penalty (dust alone does not turn hits into grazes).

Chance can be affected by cover and visible target size, stance, visibility/smoke/darkness, suppression and statuses, weapon condition and components, the chosen action, and perks. The same effect should not be applied twice.

## Suppression, retaliation, and Lightning Reactions

- Suppression cuts the shooter’s accuracy at any range (about −10 to −70 by tier).
- A **Pinned** unit cannot counterattack and, on gaining the status and on its own turns while pinned, loses Overwatch (including a permanent machine-gun sector), Pin Down, and Bombard; a partially suppressed unit keeps prepared fire but suffers the accuracy penalty, and counterattack chance falls (**×90→×60** by tier).
- **Lightning Reactions:** base about **50%**, once per combat; suppression gently cuts the chance (**45→30** by tier), **Pinned = 0%**; does **not** trigger on a stealth kill / Hidden attack.
- **Will:** recovers a little at the start of the turn. A nearby ally with high **Leadership** (within **11** tiles) speeds that up — the strongest neighbour counts, not the sum; **Negotiator** on that ally stretches the range. **Psycho** skips this and loses 4 Will per turn instead (unless Berserk); after combat everyone is back to full Will.

## Bleeding, pain, trauma, and medicine

- Bleeding tiers **3 / 6 / 12** HP/stack/turn. Hotbar: **Field Bandage** (one use spends **one bandage per bleed stack**, each step −1 tier; **AP 5/4/3/2/1** at Medical **0/20/40/60/80**, no skill gate) and kit **Bandage**: full bleed clear, pain, infection clear, downed rally; **stabilizes** one eligible trauma (penalties one tier lighter — not healing). HP restore is **% of max HP** (at Medical 100: Small **30%** / Medium **60%** / Large **100%**; at the kit’s Medical gate — **30% of those**). Real trauma **healing** is only the field Treat Wounds operation. **Hospital Treatment** restores HP for money and does **not** instantly clear zone trauma. Trauma also applies **max HP debt** **10 / 30 / 60%** (full ceiling in combat; debt lands **after the fight**). Icons distinguish untreated / stabilized / healing. Starting hire loot: Medical **&lt; 20** → bandages only; kits by skill (AME Small only).
- **Heavy** bleed from hits comes from **expanding** ammo (JHP).
- **Pain** cuts AP and accuracy including **melee** (−1 stack/turn; **clears fully when combat ends**): each solid damaging hit adds **+1** Pain (grazing scratches do not). **Morphine** immediately **clears Pain** and **blocks new stacks** while Analgesia lasts; it also refunds, once, the AP Pain already withheld at the start of the current turn. It **can rally a downed ally** (like a medkit — no HP heal) and does not stop bleeding or trauma. **AP 3/2/1** at Medical **0/40/80** (no skill gate).
- **Blood loss** statuses by HP% (below **50 / 40 / 30 / 20 / 10 / 5 / 1%**): **−1…−7** start AP. Cleared only by raising HP. Max AP no longer scales down directly from missing HP.
- **Wound infection**: an untreated **heavy** trauma that fails its improvement check gains **Infected Wound** (the trauma stays). The status icon shows on party portraits in combat and on the satellite map. Infection checks about every **16 h** either clear it or **kill** the merc. Field Treat Wounds healing prevents infection from that check.
- **Zone trauma** (arms / legs / ribs / head): light / medium / heavy. Tier comes from **this hit’s after-armor damage**: below **20** — none; **≥ 20** into a clear zone — light; another qualifying hit to the same zone steps the tier up; **≥ 50%** max HP or **going down** — heavy immediately. Grazes never apply trauma. Using an injured zone adds Pain stacks once per zone per turn: light **+1**, medium **+2**, heavy **+3**. A melee swing or thrown knife counts as using the **arms**. Each **unused heavy** zone still adds **+1** Pain at end of turn. Medium+ also adds zone penalties (−accuracy, move cost, start AP, sight). **If armor stops the round**, you can still take **behind-armor trauma** (light trauma + pain, no bleeding). Going down applies a **heavy** trauma package; combat **Wounded** stacks from HP loss stay off. Bandages do not heal trauma. Status Information shows **hours until the next progress check**; skipping time **catches up** missed checks. A squad **field Treat Wounds** operation does not clear trauma instantly — it marks traumas as **healing**: faster checks, **each check improves** the tier (light clears / medium→light / heavy→medium), no worsening. When the log says trauma **cleared**, the squad-portrait cross on the satellite map goes away too. On the campaign map, HP recovers slowly — about **1** HP/hour (Treat Wounds patients faster; R&R faster still).
- In combat, party portraits show the same statuses as satellite (not only Wounded).
- Leg hits apply zone trauma (`Legsshot`), not the old **Slowed** status.
- Combat-start grit (~25% Temp HP) is **removed**. Max HP is full **Health** again (not the old 75% base under grit).
- **Armor weight:** reduces Free Move (status stacks = Free Move AP lost). A heavy kit may also cut up to **2** start-of-turn AP. **Ironclad** −50% armor FM tax (and halves the start-AP tax); **KillingWind** another −50% (together: no armor FM tax). Strength also reduces the tax. KillingWind keeps Free Move with cumbersome weapons. At **6+** weight stacks, the first move this turn adds **+1 Pain** (at most one stack per turn from weight).
- **Energy:** **Fit** (+1 AP, FM ×120%, +2 FM on combat turn 1) → **Winded** → **Fatigued** (75% FM) → **Tired** (−1 AP, 50% FM) → **Exhausted** (−2 AP, no FM, travel stop). **Well Rested:** +2 AP, ×120% FM, FM bonus for the first 3 combat turns. Satellite travel warns around 50% / 20% before the next step. Travel fatigue scales from **current HP** versus **100 HP** (not the Health stat and not bar %). **Leg trauma** (light/medium/heavy) slows **foot** travel only by **+10 / +20 / +30%** (worst in squad; not vehicle / water / shortcut). **Rib trauma** does not speed travel fatigue — satellite cost is **max HP debt**. The card’s **16+1 AP** is regular AP (Fit/morale), not Free Move; remaining FM is on the status icon, its tooltip, and beside AP as `(N FM)`.

## Grazing hits

- **Miss → graze:** lower CTH means a higher chance a miss still clips the target; point-blank misses graze more often, longer ranges less so.
- **Cover:** cover strength in the hit-chance calc sets the chance a hit becomes a graze — up to **100%** in full cover.
- Smoke/fog/dust alone no longer force grazing hits (smoke still hurts visibility). Dust **amplifies the cover penalty** (~**−40** CTH on top of cover), so cover-grazes are more common in a storm.
- A graze deals about **40%** damage, with no crit, no trauma / `Wounded`, and **no +1 Pain from the hit**; about **15%** chance of **light** bleed only.

## Burst recoil

The first bullet uses the normal final chance. Each next bullet keeps only part of the previous accuracy (**recoil retention**).

Strength and Marksmanship equally improve control, alongside stance, bipods/setup, components, perks, and special actions. **Unsupported machine guns** (no Setup / bipod / deployed sector): first-bullet accuracy penalty (**−50** heavy / **−25** light) reduced by Strength (0 at Strength 100), plus heavier burst recoil (**×2** / **×1.5**). Grizzly’s signature attack ignores both penalties; his normal MG burst does not. Compact high-RPM platforms are less controllable than heavier, slower examples in the same caliber. Recoil changes hit probability once; burst misses climb upward further along the string (the same control tightens both chance decay and climb). Hits on the aimed target are not shifted by climb. Shotgun pellet packets have no queue-climb.

## Grenades and launchers

Throws **always** have light scatter — there is no perfect pin-point landing.

- **Up close** (about 1/4 throw/launcher range): light scatter only, no big mishap.
- **By half range** mishap risk already matches the old maximum; farther out the failure chance stays high.
- **At max range**, elites (~**90** Dexterity/Explosives) still throw solidly (~**70–80%** of prior edge accuracy); average throwers do not.
- Skills: hand grenades — **Dexterity + Explosives** (confident around **50**); underslung/GL/rockets — **Marksmanship + Explosives**; pipes/TNT — mostly **Explosives** (~**60**).
- While aiming: ring **size** = damage area; ring and throw-arc **color** = mix of mishap risk and light-scatter size on the same green→red scale as the crosshair. Up close (0% mishap) the color can still warm as scatter grows.
- Frag / HE / flashbang: **guaranteed concussion** on blast-hit units. Zone **trauma** is **one** zone using the same after-armor damage bands as bullets (≥ **20**; heavy at ≥ **50%** Max HP) — not a pile from one grenade. In the **inner aim ring** (`CenterAreaOfEffect`) only, a strong blast can also **knock units back** (mercs included) — **Strength + Health** vs **pre-armor** damage; outer ring has no knockback; already prone units stay put. Smoke / gas / Molotov use their own packages, not concussion/knockback or **bleeding**.

## Enemy positioning

AI units are less eager to crowd around a single ideal firing position. Occupied and already planned allied positions reduce the value of nearby tiles, while dead, downed, or incapacitated allies make the same area less attractive. Several casualties close together increase the penalty.

This remains a soft preference rather than a movement ban: narrow passages stay traversable. Melee units use a gentler crowding floor. **Medics** ignore crowding so they can reach a patient. Other fighters prefer a **free cover tile** over sharing the same bush.

On large maps (the waterfall and similar) the enemy turn should not freeze for minutes. AI pathing uses this-turn reach, not the whole map. A shot from the current tile no longer fires thousands of collision rays through the waterfall mesh: chance uses the same math as the aim UI, and the bullet fly is simplified. **A clear AI shot can still hit** (same CTH as the crosshair). Shots into solid rock, cliff, or wall stop there — they do not punch through unbreakable ground. Your shots and the aim UI are unchanged.

A panicked fighter may flee and **despawn** at a map exit. While your mercs are within about **16** tiles, they will not vanish just by stepping behind the nearest rock — they keep running in plain sight.

A visible enemy sometimes shouts over their head (new order, panic, grenade, weapon swap, long dash). Fast-forward and out-of-sight stays quiet; a team gets at most two shouts per turn.

Without sight, AI will not plant Overwatch into a wall at random: the cone covers the tile **where you can step into view** (house corner, doorway, rock edge). In the open it aims 1–3 tiles off the last sound. At night it prefers lit ground / night-sight, or they skip it. Shots into solid rock stop there. If you can see them and they cannot see you, they will not stand still to be farmed — they relocate and close to firing range of the last sound, not pile onto your tile.

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
