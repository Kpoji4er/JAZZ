# Testing guide — JAZZ-UNITS-003 Legion loadouts

## 0. Preconditions

- Load order: `jazz` + `jazz-units` (+ maps/assets as usual).
- After regenerate: restart game / reload mods from disk so `items.lua` is fresh.
- Quest `JAZZ_LegionTier.JAZZ_Legion_Tier` drives gear (Ernie sector TCEs still apply).

---

## 1. Static (no game)

From `jazz/` (no game):

```powershell
python scripts/legion-loadouts/generate.py --dry-run
python scripts/legion-loadouts/run_static_tests.py
```

Expect: `37/37` OK on dry-run; `RESULT: PASSED (static AC suite)`.

Spot checks in `jazz-units/items.lua`:

| Check | How |
| --- | --- |
| Markers | one `JAZZ-UNITS-003-GENERATED-BEGIN/END` pair |
| Parse health | paren/brace balance `0` on `items.lua`; no stacked `}),),` (buggy replace used to leave these and break the whole chunk — mercs included) |
| Pilot inventory | `Roughneck_Inventory` / `Shocktrooper_Inventory` / `Sniper_Inventory` Comment `JAZZ-UNITS-003 generated` |
| HE specialist | Shock: `FragGrenade` **without** `generate_chance`, exclusive bands `[11,19]` / `[21,29]` / `≥31` |
| HE non-spec | Roughneck: `FragGrenade` **with** `generate_chance` |
| Frontliner GL | `Veteran_Inventory` / `Mercenary_Inventory` include `LegionGL_5pc`; `Legion_GL` lists `M72LAW` |
| Shotgun ammo not weapon pool | GenW combos must not nest `LegionT*_Shotgun`; `caliber_ammo` 12gauge → `Crusher_12g` / `Army_12g` |
| No mid carbine-norm | `Roughneck_Firearm`: no assault/carbine combo with `Amount < 31` (assault only via `arch3_extra_tags`) |
| Tier1 late | no firearm entry with `balance_tier` remnant / early Amount **without** `Condition = "<="` for Amount&lt;30 |
| Remnant ~1% | on Roughneck at mid: `weight = 1400` entries with Amount 20 + `<=` 29; share ≈1% of active mid weights (±0.5 pp) |
| Logistics cargo | no `DiamondBriefcase` inside generated markers; cargo stays Global AI |
| Heavy arty | `Rocketeer_Inventory` / `HeavyGrenadier_Inventory` / `Mortarman_Inventory` still link `*_Launcher` |
| All recipe contracts | 37/37 UnitData `Equipment` → recipe inventory; root inventory → firearm; sidearm/melee/utility/armor/night/flare/misc/valuables materialize exactly from each recipe |
| Commando | `AssaultGunner_Inventory`: Machete in all three arch bands at `generate_chance = 100`, one unconditional Molotov; UnitData equips melee in `Handheld B` |
| Skirmisher | `Skirmisher_Firearm`: battle-only recipe, rifle packages, upgraded ammo combos from `ammo_cap = Match`; no old flanker package |

Recipes count:

```powershell
python -c "import json; print(len(json.load(open('scripts/legion-loadouts/data/recipes.json',encoding='utf-8'))))"
```

Expect `37`.

---

## 2. Runtime smoke — Ernie (AC-008)

1. Start / load campaign with Ernie under player control so `JAZZ_Legion_Tier` is in **11–13** (early / arch1).
2. Enter a fight vs Legion line troops (Roughneck / Rifleman / Warden etc.).
3. Check corpses / live enemies:

| Expect | Notes |
| --- | --- |
| Silhouette by class | Roughneck ≈ pistol/SMG; Shock ≈ SMG/carbine; Sniper ≈ bolt/DMR — not everyone with AK |
| Ammo matches weapon | caliber from spawned gun |
| Light armor on Roughneck | Light torso/legs/helm band |
| Shock has grenades | guaranteed Frag stacks (not empty demo kit) |
| Night | only at **Night** TOD: GlowStick / FlareStick can appear; day fights should not spam lights |

4. Advance campaign (or cheat quest var) to mid **21–25**:

| Expect | Notes |
| --- | --- |
| Better SMG/pistol quality | Roughneck still CQB — **not** carbine/AR as the norm |
| Optional sidearm / knife | delayed unlocks from recipe |
| Pipe on Roughneck | possible from ~21 |
| Remnant WWII/tier1 | rare (~1%), not dominant |

5. Late **31+**:

| Expect | Notes |
| --- | --- |
| No tier1 primary | early scrap guns gone from active pool |
| Roughneck may roll assault | only via `arch3_extra_tags` — still minority vs SMG/pistol identity |
| Shock / Punisher / Merc | carbine/AR + mods packages visible |

Cheat tip (dev console / quest editor): set `JAZZ_LegionTier` / `JAZZ_Legion_Tier`, then trigger Legion loot regen (`RegenerateLegionLoot` + open Satellite) so existing squads refresh.

---

## 3. Logistics intercept (AC-009)

1. Wait for / spawn Legion **tax** or **shipment** squad (Global AI).
2. Intercept and loot the squad.
3. Expect: **payload valuables present** (`DiamondBriefcase` / Tiny matching cargo `$` from `lEnsureMoneyCargo`).
4. Expect: **not** an empty convoy caused by class generator (generator does not strip cargo; class recipes do not emit briefcase).

---

## 4. Regen policy (unchanged)

`RegenerateLegionLoot` behavior is **out of scope** for UNITS-003 — leave as-is. Smoke only that after satellite open, regenerated Legion gear follows **new** LootDef tables (not pre-generator snapshots).

---

## 5. Pass / fail for evidence

| AC | Level | Pass when |
| --- | --- | --- |
| AC-001 | static | README + runnable `generate.py` |
| AC-002 | static | pilot inventories match recipes |
| AC-003 | static | dry-run upgrade check clean |
| AC-004 | static | no tier1 at ≥30; mid remnant ≈1% |
| AC-005 | static | 37 recipes + patched classes; all UnitData/inventory/firearm/optional-entry contracts match |
| AC-006 | static | no class `DiamondBriefcase`; cargo path untouched |
| AC-007 | static | new `JAZZ_Gen*` in metadata `affected_resources`; note pre-existing UnitData orphan audit noise separately |
| AC-008 | human | Ernie smoke table above |
| AC-009 | human | tax/shipment loot has payload |
| AC-010 | docs | `legion-units-equipment-tiers.md` describes generator |

Mark AC-008/009 `BLOCKED` until a human playtest is logged in the spec Evidence section.
