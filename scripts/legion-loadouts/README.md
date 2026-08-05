# Legion loadout generator (JAZZ-UNITS-003)

Build-time: **class recipes + catalogs → `jazz-units/items.lua` LootDef**.

Design: `docs/design/legion-loadouts.md` (L1–L23). Spec: `docs/specs/active/JAZZ-UNITS-004.md` (loadout/regen; historical generated markers still say `JAZZ-UNITS-003-GENERATED-*`). Named-perks Wave A lives under a different `JAZZ-UNITS-003` SPEC-ID.

## Layout

| Path | Role |
| --- | --- |
| `data/recipes.json` | 37 combat `JAZZ_Legion_*` recipes (Recruit out of scope). Optional: `arch1_all_subs_from` (Sergeant `11` → all balance `1-x` from that Amount); `exclude_tags` (e.g. `pistol` keeps Autopistol out of SMG primary); `primary_max_tier_label` (SMG cap, e.g. `2-1`); `arch1_early_ids` (named guns into arch1 at Amount; bypasses `exclude_tags`, e.g. M45/`11`, MAC10/`12`, UZI/`13`). |
| `data/packages.json` | Mod packages M0–M4 keyword sets |
| `data/caliber_ammo.json` | Caliber → existing ammo LootDef |
| `data/weapon_tag_overrides.json` | Extra family tags (e.g. M2 `{carbine,assault}`) |
| `generate.py` | Main generator |
| `sync_metadata.py` | Adds `JAZZ_Gen*` to `jazz-units/metadata.lua` `affected_resources` |
| `TESTING.md` | Static + runtime test guide |

## Regenerate

From `jazz/` repo root (game/editor closed):

```powershell
python scripts/legion-loadouts/generate.py --dry-run          # validate only
python scripts/legion-loadouts/generate.py --pilot --dry-run  # Roughneck/Shock/Sniper
python scripts/legion-loadouts/generate.py                    # patch jazz-units/items.lua
python scripts/legion-loadouts/sync_metadata.py --no-bump     # sync new JAZZ_Gen* resources
# first ship / feature commit: omit --no-bump once to bump jazz-units version_minor
```

Markers in `items.lua`:

- `--[[ JAZZ-UNITS-003-GENERATED-BEGIN ]]` … `END` — shared pools + `JAZZ_GenW_*` weapon+ammo combos
- Class `*_Inventory` / `*_Firearm` blocks replaced in place (UnitData Equipment names unchanged)

## Ownership

- Generator + recipes: **jazz**
- Generated LootDef + metadata resources: **jazz-units** (exclusive write)
- Prices for valuables bands: `jazz/Code/LegionUnitPrices.lua`
- Tax/shipment cargo (`DiamondBriefcase`): Global AI `lEnsureMoneyCargo` — **not** emitted by class recipes

## Mod Editor

After hand-edit or regenerate: reload mod from disk; do not save an open editor that still holds pre-generator Legion loot. Prefer re-running `generate.py` over hand-editing marked / generated class blocks.
