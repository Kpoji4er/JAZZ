# AME Appearance assets (safe / forbidden)

Canonical policy for `JAZZ_AME_01`…`JAZZ_AME_60` AppearancePresets in `jazz-units/items.lua`.
Generators and audits must match this page; player-facing roster lives in [`ame-roster-60.md`](ame-roster-60.md) and the slot map [`ame-appearance-map.json`](ame-appearance-map.json).

## Root cause (pale heads / pale hands)

1. **False “African” head bank** — `_gen_ame_appearances.py` / audit treated AIM heads `Head_Flay`, `Head_Fidel`, `Head_Magic`, `Head_Blood` as safe Af meshes. In-game they read Caucasian on AME kits. Because `head_needs_africanize` returned false for bank members, regen left them in place.
2. **Female heads on males** — map/bank sometimes assigned `Head_Fauda` / `Head_Lami` to male slots (gender mesh mix; hat attach breaks).
3. **Body mesh, not missing Color1** — `BodyColor.EditableColor1` was already dark African for reported mercs. Claude’s white hands came from **`Faction_GrandChien_Top_05`**: exposed arms stay pale despite dark C1. Gloves (`Shirt` = `*Glove*`) can also fake pale hands.
4. **HeadColor must stay black** — ethnicity is the Head *mesh*. Tinting `HeadColor` to skin RGB washes faces chalk-white. Correct: `HeadColor` EditableColor1/2/3 = `RGBA(0,0,0,255)`.

## Safe male heads

Cycle only these (same order in `_gen_ame_appearances.py` `MALE_AF_HEADS` and `_audit_patch_ame_heads.py` `MALE_HEADS`):

| Head mesh | Notes |
|---|---|
| `Head_Chimurenga` | Grand Chien / rebel leader — dark African |
| `Head_Pierre` | Rebel — dark African |
| `Head_Jackhammer` | Named merc — dark African |
| `Head_M_IMP_01` | IMP male African option |
| `Faction_Rebels_M_HeadMedic` | Rebel medic head (not Legion war-paint) |

There is no `Head_M_Af_*` bank in vanilla; do not invent IDs.

## Safe female heads

| Head mesh | Notes |
|---|---|
| `Head_F_Af_NPC_01` … `Head_F_Af_NPC_10` | Only safe female Af bank |

Never put male heads on female bodies or female heads on male bodies.

## Forbidden heads

| Pattern / ID | Why |
|---|---|
| `Head_Flay`, `Head_Fidel`, `Head_Magic`, `Head_Blood` | AIM; read pale/Caucasian on AME |
| `Head_Fauda`, `Head_Lami` | Female meshes — never on male AME |
| `Head_Omryn` | Asian — reads pale/"white" |
| `Faction_Legion_Head_*` | War-paint / ceremonial Legion faces |
| `Head_M_Ca_*`, `Head_M_As_*`, `Head_F_Ca_*`, `Male_Head_*`, AIM Caucasian cast (`Ice`, `MD`, `Ivan`, …) | Pale / wrong ethnicity |
| Any ♀ head on ♂ body (and reverse) | Gender mesh mix — hard gate |

## Color rules

| Channel | Rule |
|---|---|
| `BodyColor.EditableColor1` | Dark African skin from `SKIN_BANK` (near-black browns, channels ≤ ~20). Forced by generator + audit. |
| `BodyColor.EditableColor2/3` | Cloth / accents — never the only “skin” channel for AME policy |
| `HeadColor.*` | Always `RGBA(0,0,0,255)` — do **not** copy skin RGB onto the head |
| AME blue accent | Exactly **one** of Hat / Hat2 / Shirt / BodyC2 — never Pants/boots |
| Legion red / extra blue | → muted slate `(34,38,44)` |

`SKIN_BANK` (shared):

```text
(6,2,1) (8,3,1) (10,4,2) (12,5,2) (14,5,3)
(16,5,5) (17,6,3) (18,7,4) (19,8,4) (20,7,3)
```

## Safe bodies / pants / hats (AME)

**Prefer (male tops):**

- `Faction_Militia_Top_02`, `Faction_Militia_Top_03`
- `Faction_Rebels_Top_Comander`
- `Faction_GrandChien_Top_02`, `Faction_GrandChien_Top_03`
- `Faction_Adonis_Top_01`

**Avoid / auto-swap:**

- Any `Faction_Legion_Top_*` (war-paint / bare ceremonial torsos)
- `Faction_GrandChien_Top_05` — pale hands/arms despite dark BodyColor C1 (Claude)
- `Shirt` meshes matching `*Glove*` — clear Shirt so arm skin shows

**Safe male pants (when replacing bad gear):** `Faction_Militia_Bottom_01`, `Faction_Rebels_Bottom_01`, `Faction_GrandChien_Bottom_03`

**Female hat when donor hat is male:** `NPCCostumeFemale_Hat_01`

**Bad named gear (strip/replace):** mesh names containing `Omryn` / `Fauda` / `Lami`

## How to regenerate / audit

From `jazz/` (game/editor closed for write):

```text
# Full regen from vanilla donors (rewrites AME Appearance section + map)
python docs/tools/_gen_ame_appearances.py

# Repair pass on existing jazz-units/items.lua (preferred for pale-head fixes)
python docs/tools/_audit_patch_ame_heads.py --dry-run
python docs/tools/_audit_patch_ame_heads.py --sync-map

# Validate items.lua parse
python docs/tools/_validate_items_quick.py ../jazz-units
```

- `--sync-map` writes current `Head` into `ame-appearance-map.json` `head_swap`.
- Mid-session live refresh (optional): `_emit_ame_live_patch.py` → DAP dofile; prefer full mod reload.
- AppearancePresets for AME live in `jazz-units/items.lua` (no separate `AppearancePreset/*.lua` companions). UnitData companions still reference `Preset = "JAZZ_AME_NN"`.

## Related docs

- Design map: [`ame-appearance-map.json`](ame-appearance-map.json)
- AME design: [`ame-mercenary-exchange.md`](ame-mercenary-exchange.md)
- Technical current-state: [`../technical/systems/units-progression-specializations.md`](../technical/systems/units-progression-specializations.md)
- Tools index: [`../tools/README.md`](../tools/README.md)
