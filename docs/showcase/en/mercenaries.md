# Mercenaries

[Overview](home.md) · [Perks](perks.md) · [Русский](../ru/mercenaries.md)

## What JAZZ adds

AIM gets a wave of JA1/JA2-flavored hireables: nicknames, roles, hire tiers, salaries, and a **named perk**. `jazz-units` owns UnitData / loot / portraits; core owns AIM filters and progression.

- About **44** Ready mercs from the JA1/2 wave (plus references like Lynx, Spider, Tosca/Buzz, Spouke).
- AIM specializations: **Autoriflemen**, **HeavyWeapons**, **Stealth** — usable as hire filters.
- XP progression extended to **level 21**.

## Examples (nick → focus)

| Nick | Role / focus | Named perk (intent) |
| --- | --- | --- |
| Lynx | Sniper | Lynx’s Eye sniper technique |
| Spider | Medic / field surgery | Field Surgery |
| Tosca / Buzz | Autofire / lead rain | Dense fire perk |
| Spouke | Explosives / signature action | Spouke perk |
| Colby | Demolitions | Chain Panic: +blast radius, panic chance on wounded in the blast |
| Blade | Close combat | Blade Storm |
| Ira | Leadership / militia | Faster locals training (stacks with Teacher) |

Full slug / UnitData ID lists live in `docs/design/mercs-ja12/` in the repo; this page is an overview, not every stat block.

## Honesty about readiness

- UnitData, portraits, and perk slots for the wave are **generated**.
- Named-perk **combat hooks are not finished for everyone** — some perks are still empty stubs. Colby is an example with working combat hooks.
- Rich AIM chat / VoiceResponse and some Appearance work are still WIP in places.
- English merc localization is not treated as complete.

Hire them and read the in-game perk text; if a paper effect does not show up in combat, that is unfinished plumbing — not you misreading the UI.
