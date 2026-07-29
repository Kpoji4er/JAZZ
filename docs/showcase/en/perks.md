# Perks

[Overview](home.md) · [Mercenaries](mercenaries.md) · [Combat actions](combat-actions.md) · [Русский](../ru/perks.md)

Sourced from `CharacterEffect/Jazz_Perk_*.lua`, `items.lua`, and `Code/*` (jazz). Class weapon buttons (`JAZZ_Fanning`, etc.) live on [combat actions](combat-actions.md); this page is **named / personal**.

## Layers

1. Named merc perk (`Jazz_Perk_*` in StartingPerks).
2. Personal combat action (button id = perk / `GrizzlyPerk`).
3. Status/aura (`Jazz_Perk_OfficerAura*`) — not an AIM build pick.

## What actually works in code

| Id | Who | Runtime effect |
| --- | --- | --- |
| `Jazz_Perk_00` | Spouke (`JAZZ_Merc_Spouke`) | Toggle: timed explosives detonate at enemy turn start |
| `Jazz_Perk_Buzz` | Tosca (`Jazz_Buzz`) | +50% autofire bullet count (WeaponAttacks / items hooks) |
| `Jazz_Perk_Lynx` | Lynx | +8 sight (`System_OR_Unit`); range-CTH text is **not** backed by code |
| `Jazz_Perk_Spider` | Spider | ×2 Medical on sector heal ops |
| `Jazz_Perk_Colby` | Colby | +20% grenade AoE; 20% panic on wounded in blast |
| `GrizzlyPerk` | Grizzly | Personal MG attack + CTH/recoil hooks |
| `GruntyPerk_JAZZ` | Grunty (+ Doctor_Leevsy) | On combat start → +50% AP first turn |
| `Jazz_Perk_OfficerAura` / `…Influence` | AI officers | Commander aura markers (`AIContextProfiles`) |

**Note:** Lynx/Buzz/Spider/Colby HUD buttons currently copy-paste the `Jazz_Perk_00` toggle. The passive may still work; the button does not.

`JAZZ_VovaVist` has full attack code but **no UnitData grant path** found.

## Stubs

Other wave `Jazz_Perk_*` (Allik, Blade, Ira, Miguel, … — **~40** files): empty `unit_reactions`, WIP text, no `Code/` gameplay refs. Slot exists on the merc; no combat effect yet.

Orphan: `Jazz_Perk_44840` — file present, not registered in `items.lua`/`metadata`.

## Player takeaway

Expect working named effects from **Spouke, Tosca, Lynx, Spider, Colby** (+ Grizzly/Grunty). The rest of the wave is hireable, but the “signature” perk is still empty.
