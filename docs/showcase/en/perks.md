# Perks

[Overview](home.md) · [Mercenaries](mercenaries.md) · [Combat actions](combat-actions.md) · [Русский](../ru/perks.md)

Sourced from `CharacterEffect/Jazz_Perk_*.lua`, `items.lua`, and `Code/*` (jazz). Class weapon buttons (`JAZZ_Fanning`, etc.) live on [combat actions](combat-actions.md); this page is **named / personal**.

## Layers

1. Named merc perk (`Jazz_Perk_*` in StartingPerks).
2. Personal combat action (button id = perk / `GrizzlyPerk`) — only where toggle/active is needed.
3. Status/aura (`Jazz_Perk_OfficerAura*`, `Jazz_OrderCTH`) — markers, not AIM picks.

## What actually works in code

| Id | Who | Runtime effect |
| --- | --- | --- |
| `Jazz_Perk_00` | Spouke | Toggle: timed explosives detonate at enemy turn start |
| `Jazz_Perk_Buzz` | Tosca | +50% autofire bullet count |
| `Jazz_Perk_Lynx` | Lynx | +8 daytime sight; that vision softens range accuracy (Range CTH) |
| `Jazz_Perk_Spider` | Spider | ×2 Medical on sector heal ops |
| `Jazz_Perk_Colby` | Colby | +20% grenade AoE; 20% panic on wounded in blast |
| `Jazz_Perk_Madman` | Madman | Point-blank kill → Inspired |
| `Jazz_Perk_Blade` | Blade | Melee +20 CTH, no crits |
| `Jazz_Perk_Nervous` | Nervous | Autofire/burst +2 bullets |
| `Jazz_Perk_Henning` | Henning | Allies ≤5 tiles: +5 CTH next attack |
| `Jazz_Perk_Vicious` | Vicious | +1 AP per woman in squad (cap 3) at combat start |
| `Jazz_Perk_Dynamo` | Dynamo | Head hit: 25% Blinded |
| `Jazz_Perk_Eskimo` | Eskimo | <50% HP: no Panic; Wounded does not cut firearm CTH |
| `Jazz_Perk_Lucky` | Lucky | 1×/combat: first firearm miss → hit |
| `Jazz_Perk_Shank` | Shank | Melee vs him −50 CTH |
| `Jazz_Perk_Vilde` | Vilde | Night/underground auto/burst +15 CTH |
| `Jazz_Perk_Laura` | Laura | After bandaging an ally, becomes Hidden again |
| `Jazz_Perk_Vince` | Vince | 1×/combat: first ally bandage → target +4 AP |
| `Jazz_Perk_Steiger` | Steiger | At night: allies ≤5 get +5 CTH |
| `GrizzlyPerk` | Grizzly | Personal MG attack + CTH/recoil |
| `GruntyPerk_JAZZ` | Grunty | Combat start → +50% AP first turn |
| `Jazz_Perk_OfficerAura` / `…Influence` | AI officers | Commander aura |

Passive Lynx/Buzz/Spider/Colby have **no** HUD toggle (buttons hidden). Toggle remains Spouke-only (`Jazz_Perk_00`).

## Still stubs

Other wave named perks (Ira, Miguel, Grom, Biff, …) — Wave B/C; see `docs/design/mercs-ja12/_named-perks-plan.md` and `JAZZ-UNITS-003`.

## Player takeaway

Working named effects: **Spouke, Tosca, Lynx, Spider, Colby** + Wave A (**Madman, Blade, Nervous, Henning, Vicious, Dynamo, Eskimo, Lucky, Shank, Vilde, Laura, Vince, Steiger**) and Grizzly/Grunty.
