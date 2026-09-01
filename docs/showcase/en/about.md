# What is JAZZ

[Overview](home.md) · [Русский](../ru/about.md)

## In short

**JAZZ** is a full tactical overhaul for *Jagged Alliance 3*. It is not a pile of new guns and a few balance tweaks: four packages together rework combat, weapons, armor, injuries, inventory, AI, enemies, maps, and the strategic layer.

The goal is to make **decisions** matter more than raw stat growth. Position, range, merc skills, weapons, ammo, gear condition, weather, and resources should change fights in a noticeable way. Difficulty comes from how systems interact, not only from more enemy HP.

> Install only as the full four-package suite with the latest published `JA3_CommonLib`.

## Status

Demo. **Ernie Island** is the fully supported campaign slice; content beyond Ernie may be unfinished. Start a new game for a first run and after major updates. JA3 **Advanced Rules** are hidden in New Game (Ammo Scarcity, Body Count, Heavy Wounds, and the rest); only the base Game Rules remain.

Player-facing content is currently stronger in Russian; English localization is not treated as complete yet.

## Suite packages

| Package | Role |
| --- | --- |
| `jazz` | Core: mechanics, items, effects, UI |
| `jazz_assets` | Models, materials, textures |
| `jazz-maps` | Maps, sectors, quests, dialogue, setpieces |
| `jazz-units` | UnitData, AI archetypes, squads, loot, progression |

This is one mod suite, not four independent mods. Partial installs are unsupported.

## What changes in play

### Combat and arsenal

- Weapons by **role** and range, not one linear “just stronger” ladder.
- Hit chance from weapon, range, aiming, skills, visibility, and conditions; the UI shows `+` / `−` instead of a raw percent.
- Bursts with sequential recoil; Strength, stance, and attachments affect control.
- Reliability, wear, jams; reworked ammo, components, shotguns, heavy weapons, and suppression.
- Eleven firearm classes plus class combat actions on top of core fire modes.

### Armor, injuries, and resources

- Armor: coverage, damage type, weight, condition, camo, replaceable plates.
- Carried weight hits mobility.
- Injuries, body parts, treatment, and strategic recovery are linked.
- Specialized inventory slots; ammo and consumables really limit what you can do.

### AI, visibility, and enemies

- Tactical AI for position, targets, cover, flanks, and special actions — [how the AI works](tactical-ai.md).
- On large fights (including the **M1** landing with rebels), allied turns are sped up: shorter AI deliberation and auto fast-forward for ally animations when Fast Forward is enabled.
- Clearer enemy roles and loadouts.
- Light, night, smoke, and weather affect spotting and fire.
- In real-time, the suspicion bubble behind a sentry is shorter (about 10 tiles): approaching from the rear is easier than walking into their full forward view.
- Stealth: camo, Stealthy, and cover stack; brush barely hides by itself but strongly boosts camo (a specialist in grass can close to about 4 tiles). Indoors slightly reduces sight for everyone.
- Optics, flashlights, and NVG are real choices, not cosmetics.

### Maps and strategy

- Demo = **Ernie Island** (start M1); mainland exists in data, playthrough not promised — [Ernie campaign](ernie-campaign.md).
- Village, fort, Herman, rebels, lighthouse, and villa quest lines.
- On the satellite map Legion shows **roles** and **tasks** — [strategy](legion-strategy.md).
- In fights: T1–T4 class catalog plus a separate gear tier from your sectors — [Legion units](legion-units.md).

### Mercenaries and perks

- **48** hireable Jazz mercs in `jazz-units` (AIM/MERC) — full roster: [mercenaries](mercenaries.md).
- Named perks with code: Spouke, Tosca, Lynx, Spider, Colby (+ Grizzly/Grunty); other wave slots are stubs — [perks](perks.md).
- Class weapon techniques are separate: [combat actions](combat-actions.md).

## This wiki

A bilingual guide to the mod’s aspects (rules, demo map, arsenal, people, Legion). Weapon stat tables publish alongside. Not a replacement for in-game tooltips. Formulas and IDs live in the repo technical docs.

Discord: <https://discord.gg/XBc498AFdj>
