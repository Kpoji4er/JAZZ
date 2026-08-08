# AME Appearance assets (safe / forbidden)

Canonical policy for `JAZZ_AME_01`…`JAZZ_AME_60` AppearancePresets in `jazz-units/items.lua`.
Generators and audits must match this page; player-facing roster lives in [`ame-roster-60.md`](ame-roster-60.md) and the slot map [`ame-appearance-map.json`](ame-appearance-map.json).

## Legion look canon (donor source)

**Канонический визуальный Легион JAZZ** = handcrafted `ModItemAppearancePreset` in `jazz-units` (`group = "Legion"`): `LegionGoon`, `LegionButcher`, `LegionRaider`, `LegionScout`, … (+ `Stronger` / `Elite` / `alt`). Catalog: [`mercs-ja12/_appearance-donor-visual-catalog.md`](mercs-ja12/_appearance-donor-visual-catalog.md) (jazz-units batch).

- **Preferred AME Legion clothing donors:** those jazz-units `Legion*` kits (Irregulars lean hardest).
- **Not a donor canon:** vanilla `Legion_Soldier` / `Legion_Recon` / … role color twins. They may remain in enemy `AppearancesList` as filler, but new AME clones should not treat them as the Legion brand.
- Source `Legion*` presets are **never edited** for AME — clone into `JAZZ_AME_NN` with blue/slate rules below.

## Donor shuffle (clothing)

Pools: jazz-units `Legion*` · vanilla Rebels · GrandChien · keep some current AME donors.

| Category | Lean |
|---|---|
| Irregulars | mostly jazz `Legion*` (base/`_alt*`) + a few Rebels/keep |
| Fighters | Rebels + some `Legion*` + keep |
| Hardened | GrandChien + Rebels; few `Legion*` |
| Specialists | mostly keep; swap vanilla `Legion_*` → jazz `Legion*` |

Clothing-only patch (`_patch_ame_appearance_clothes_from_map.py`): clone Body/Pants/Shirt/Hat/Hat2/Chest/Hip/Armor from map `donor`; **preserve** Head + `BodyColor` C1 + `HeadColor` from the existing AME preset.

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

## Female hair

| Rule | Detail |
|---|---|
| Bank | **Only** `NPCFemale_Hair_01`…`_04` (and other `NPCFemale_Hair_*` if added). **No** AIM `Equipment*_Hair` (Corazon/Fox/Meltdown/Buns/…) |
| Hat vs Hair | If `Hat` or `Hat2` has a mesh → **`Hair = ""`** (anti-collision). Hair only when both hat slots empty. Hat diversity ≠ hair+hat |
| Map field | `hair` on female rows in [`ame-appearance-map.json`](ame-appearance-map.json) |

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
- Clothed tops from jazz `Legion*` kits after warpaint auto-swap

**Avoid / auto-swap:**

- Any `Faction_Legion_Top_*` (war-paint / bare ceremonial torsos) → clothed safe top
- `Faction_GrandChien_Top_05` — pale hands/arms despite dark BodyColor C1 (Claude)
- `Shirt` meshes matching `*Glove*` — clear Shirt so arm skin shows
- **Hard helmets / hats / turbans** on AME: strip `*Helmet*`, `LarryAddicted_Hat`, `FactionMale_Hat_*`, `NPCTraditional*_Hat*`, `NPCCostumeFemale_Hat*`, `Equipment*_Hat` — keep masks / scarves / glasses / headbands
- **AME blue accent:** on **non-camo** gear only (`Shirt` if not camo → Chest → Hip → Armor → Body C2 → Hat2 scarf) — **never** Hat brim, **never** camo `Equipment*_(Shirt|Pants)_02` / militia camo tops
- **Camo earth tones:** urban/woodland camo shirt+pants stay olive/brown (`_CAMO_EARTH`); if the kit is camo-only, add `Faction_Acc_Soldier` hip pouches (or similar) as the blue carrier so the uniform is not tinted blue

**Safe male pants (when replacing bad gear):** `Faction_Militia_Bottom_01`, `Faction_Rebels_Bottom_01`, `Faction_GrandChien_Bottom_03`

**Female hat when donor hat is male:** `NPCCostumeFemale_Hat_01`

**Bad named gear (strip/replace):** mesh names containing `Omryn` / `Fauda` / `Lami`

## How to regenerate / audit

From `jazz/` (game/editor closed for write):

```text
# Clothing shuffle from map (jazz Legion* + Rebels/GC); preserve head/skin; NPC female hair; strip helmets
python docs/tools/_patch_ame_appearance_clothes_from_map.py --dry-run
python docs/tools/_patch_ame_appearance_clothes_from_map.py
python docs/tools/_audit_ame_appearance_clothes_qa.py

# Full regen from vanilla donors only (rewrites AME Appearance section + map; does not load jazz Legion*)
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
