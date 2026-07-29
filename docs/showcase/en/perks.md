# Perks

[Overview](home.md) · [Mercenaries](mercenaries.md) · [Combat actions](combat-actions.md) · [Русский](../ru/perks.md)

## Three different “perks” in JAZZ

Do not mix these layers:

1. **Weapon class techniques** — buttons like Fanning, Bullseye, Mozambique, Controllable Burst. They depend on the weapon class / unlocks. Details: [combat actions](combat-actions.md).
2. **Named merc perks** — `Jazz_Perk_*` on AIM hireables (one signature effect per character).
3. **Status effects / auras** — in-combat CharacterEffects (suppression, officer aura, etc.): not an AIM build pick, a battlefield state.

Accuracy impact always goes through the **same** CTH pipeline as a normal shot (multipliers; no separate “showcase math”).

## Named perks (how to read them)

| Example | Merc | Design intent |
| --- | --- | --- |
| Chain Panic | Colby | ~+20% blast radius; panic chance on wounded targets in the blast |
| People's Commander / Teacher stack | Ira | Faster locals militia training |
| Blade Storm | Blade | Signature close-combat technique |
| Lynx's Eye | Lynx | Named sniper ability |
| Field Surgery | Spider | Field medicine |
| Lead Rain / SMG-storm line | Tosca | Dense automatic fire |

Combat also has personal actions like `JAZZ_VovaVist` and `GrizzlyPerk` — character grant-paths, not the shared AIM pool.

## Readiness

- The mod’s CharacterEffect catalog is large (dozens of perks and statuses).
- JA1/2 wave mercs have named-perk **slots**, but many runtime hooks are still **empty stubs**. Do not expect every nick’s design article to already reshape combat.
- Class weapon actions are generally closer to “pressable in a fight”; named perks — verify in your build.

When a perk ships for real, this page and the merc blurb get updated together.
