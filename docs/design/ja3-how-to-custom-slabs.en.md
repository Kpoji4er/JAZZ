# How to make a custom slab in JA3

[Русский](ja3-how-to-custom-slabs.md)

How-to for the Jagged Alliance 3 engine: what a slab is, which room pieces exist, and which names the engine looks up. This is **not** JAZZ current-state: the suite still has no custom `SlabMaterials`.

Sources: installed `<JA3_ROOT>\ModTools\Src` (`CommonLua/Libs/Volumes/Slab.lua`, `RoomRoof.lua`, `Classes/Destroyable.lua`, `Data/SlabPreset.lua`) and official `ModTools/Docs` (Entity, Map Editor). Evidence level: **static**. Editor/runtime acceptance comes after the first imported set.

Below, `{id}` is the material token, e.g. `JazzBrick`. No spaces or hyphens.

## What it is

**A slab is a room cell, not a free prop.**

A prop can be dropped anywhere with the mouse. A slab is placed by the room (`Room`, Map Editor: **Ctrl-Shift-N**): you pick wall / floor / roof materials, and the engine fills the voxels.

The engine **does not store a model path on the preset**. It **composes the entity name** from the material `id` + piece role + variant + suffix `01` / `02` / …

```text
Room.wall_mat = "JazzBrick"
        ↓
Presets.SlabPreset.SlabMaterials.JazzBrick
        ↓  ComposeEntityName()
WallExt_JazzBrick_Wall_ExEx_01
        ↓
EntityData["WallExt_JazzBrick_Wall_ExEx_01"] + .ent + mesh + .mtl + DDS
```

If the preset exists but the expected entity name does not, the cell becomes an InvisibleObject and the log reports a missing entity. Renaming the entity “to look nicer” is not allowed: the name **is** the contract.

Voxel size:

| Constant | Size |
|---|---|
| `const.SlabSizeX` / `Y` | **1.2 m** |
| `const.SlabSizeZ` | **0.7 m** |

| Class | What it builds |
|---|---|
| `WallSlab` | wall 1.2 × 0.7 |
| `FloorSlab` / `CeilingSlab` | floor / ceiling 1.2 × 1.2 |
| `RoofSlab` | slope, eave, ridge |
| `RoomCorner` | corner post + joint caps |
| `StairSlab` | stairs |
| `SlabWallObject` | window / door (cuts a hole in the wall) |

The preset only stores `id`, suffix lists, and combat properties (`obj_material`, `strength`). The model is never bound to the preset by hand.

## How a room is assembled

A 3×3 box of cells. Each cell gets its own mesh with a canonical name:

```text
        roof Roof_*
   ┌────┬────┬────┐
   │Cap │Wall│Cap │   corners: Corner
   │ L  │    │ T  │
   ├────┼────┼────┤
   │Wall│flr │Wall│   floor: Floor_*
   │    │    │    │
   ├────┼────┼────┤
   │    │    │CapX│   wall cross: CapX
   └────┴────┴────┘
        door/window cuts a hole in Wall
```

Without the corner and caps, two walls meet but there is no post / end-cap — the room is full of holes even if the facade looks finished.

## How to read the name

```text
WallExt_JazzBrick_Wall_ExEx_01
│      │         │    │    └─ subvariant (01, 02, …)
│      │         │    └────── which faces: ExEx / ExIn / InIn
│      │         └─────────── piece role: Wall / Corner / CapL
│      └───────────────────── material id = preset id
└──────────────────────────── family: exterior wall
```

The subvariant suffix is two digits. An empty `SlabMaterialSubvariant` on the preset means `suffix = "01"`, `chance = 100`.

In Blender the object must **already** use the full in-game name (`WallExt_JazzBrick_Wall_ExEx_01`), not a short `JazzBrick` or `wall_slab_brick`. After export the game will not rename it.

## Piece catalog

### 1. Wall — `Wall`

A one-cell facade (typically a box ~1.2 × 0.2 × 0.7 m).

Three variants — how many faces of the mesh are “street / room”:

| Room variant | Token | What it is |
|---|---|---|
| `Outdoor` | `ExEx` | Two exterior faces. Fence, shed, wall with no interior lining. |
| `OutdoorIndoor` | `ExIn` | Exterior mesh of its own; the engine attaches `WallInt_*` on the inside. A normal house. |
| `IndoorIndoor` | `InIn` | Two interior faces. Partition between rooms. |

```text
WallExt_{id}_Wall_ExEx_01
WallExt_{id}_Wall_ExIn_01
WallExt_{id}_Wall_InIn_01
```

`ExEx_01` is enough for the first room. Without ExIn/InIn you cannot make “a house with wallpaper inside”, but the exterior box is already visible.

Base name without suffix (the engine appends `_01`):

```text
WallExt_{id}_Wall_{variant}
```

Code sources: `Slab:GetBaseEntityName`, `variantToVariantName`.

### 2. Corner — `Corner`

A vertical post where two walls meet.

```text
WallExt_{id}_Corner_01
WallInt_{id}_Corner_01      only if you have indoor lining
```

Function: `ComposeCornerBeamName`.

### 3. Joint caps — `CapL` / `CapT` / `CapX`

These are not roof eaves. They are **end-caps** where walls meet in a letter shape:

| Name | Joint | When it appears |
|---|---|---|
| `CapL` | L-shape | building corner, two walls |
| `CapT` | T-shape | a third wall hits the middle |
| `CapX` | cross | four walls in one voxel |

```text
WallExt_{id}_CapL_01
WallExt_{id}_CapT_01
WallExt_{id}_CapX_01
```

Function: `ComposeCornerPlugName`.

### 4. Floor and ceiling — `Floor`

One 1.2 × 1.2 tile. The ceiling (`CeilingSlab`) uses the **same** entities; separate `Ceiling_*` names are not needed.

```text
Floor_{id}_01
```

A custom floor is optional: walls can use your material while the floor stays vanilla `Planks` / `Adobe`.

### 5. Interior lining — `WallInt`

A separate preset in group `SlabIndoorMaterials` (the room’s Inner Wall Material), **not** the same `id` as the facade. Vanilla: `CityTiles`, `Colonial`, `Concrete`, `Planks`, `Wood`.

```text
WallInt_{indoor_id}_Wall_01
```

Attached to an `OutdoorIndoor` / `ExIn` wall. Without this set the inside of the house is empty or a missing entity. An `Outdoor` / ExEx room works without wallpaper.

### 6. Roof — `Roof`

The name is built from the preset field **`EntitySet`**, not from `id` (in vanilla they often match; the **display name can lie** — Adobe roofs are labeled “Concrete”, Straw roofs “Tin”).

```text
Roof_{EntitySet}_{component}_{NN}
```

These `roof_comp` tokens come from `RoomRoof.lua` (`roofCompToSubvariantArr`). They are Haemimont names, not invented labels.

**The room actually places these** (`obj.roof_comp = …`) and vanilla ships meshes for them:

| Component | What it is | Vanilla example |
|---|---|---|
| `Plane` | slope, main surface | `Roof_Adobe_Plane_01` |
| `Eave` | eave / overhang | `Roof_Adobe_Eave_01`, `_02` |
| `Rake` | gable-end of the slope | `Roof_Adobe_Rake_01`, `_02` |
| `Ridge` | ridge | `Roof_Adobe_Ridge_01` |
| `RakeEave` | rake–eave joint | `Roof_Adobe_RakeEave_01` |
| `RakeRidge` | rake–ridge joint | `Roof_Adobe_RakeRidge_01` |
| `Gable` | gable face | `Roof_Tiles_Gable_01` (Adobe has none) |
| `RakeGable` | rake–gable joint | `Roof_Tiles_RakeGable_01` (Adobe has none) |

A sloped Adobe-style roof needs Plane + Eave + Rake + Ridge + the two rake joints. Gable / RakeGable are extra for gable roofs (Tiles, Tin, Wood, Sticks, Straw, PalmLeaves).

**Reserved in the name formula only.** Present in `roofCompToSubvariantArr` and as editor fields (`RakeGableCrestBot Subvariants`, …). Vanilla never assigns these `roof_comp` values and ships **no** `EntityData` for them. `Bot` = **Bottom**, not “bot”. Skip unless you are extending the engine.

| Token | Preset field |
|---|---|
| `GableCrest` | `crest_subvariants` |
| `RakeGableCrestTop` | `crest_top_subvariants` |
| `RakeGableCrestBot` | `crest_bot_subvariants` |
| `GableSlope` | `slope_subvariants` |
| `RakeGableSlopeTop` | `slope_top_subvariants` |
| `RakeGableSlopeBot` | `slope_bot_subvariants` |

A room without a roof is fine in the editor. Do this after the walls join cleanly.

Fallback in code if the preset has no `EntitySet` / subvariants: `Roof_{id}_{component}_01` (uses `self.material`). Safer to set `EntitySet` equal to `id` from the start.

### 7. Stairs — `Stairs`

A separate `StairsSlabMaterials` preset. It does not appear from the wall material.

```text
Stairs_{id}_01
```

### 8. Window and door

Separate entities (`SlabWallObject`). They **cut a hole** in `Wall`. Until an entity of that name exists, you cannot insert a window into that material. Vanilla `Window_Adobe_Single_01` will not stick to your `JazzBrick`.

Pattern: `{Type}_{id}_{width}_{NN}`  
Function: `SlabWallObjectName`.

| Cell height | Window | Door |
|---|---|---|
| 1 | `WindowVent` | `WindowVent` |
| 2 | `Window` | `Window` |
| 3 | `WindowBig` | `Door` |
| 4 | `TallWindow` | `TallDoor` |

Widths: `Small` (0), `Single`, `Double`, `Triple`, `Quadruple`.

```text
WindowVent_{id}_Single_01
Window_{id}_Single_01
WindowBig_{id}_Single_01
TallWindow_{id}_Single_01
Door_{id}_Single_01
TallDoor_{id}_Double_01
```

### 9. Destruction — `Broken` / `BrokenDec` / `Damaged`

When a neighbor cell is blown out, the engine **swaps the entity**; it does not deform the mesh. Base = `GetBaseEntityName()` **without** `_{NN}`.

| Suffix | What it is |
|---|---|
| `_Broken_T` | broken from the top |
| `_Broken_B` | from the bottom |
| `_Broken_R` | from the side (left/right via mirroring) |
| `_Broken_RT` / `_Broken_RB` | corner: top+side / bottom+side |
| `_BrokenDec_T` / `_B` / `_R` | break decal/attach on the neighboring intact wall |
| `_Damaged` | battered but still whole (if the preset has `use_damaged`) |

```text
WallExt_{id}_Wall_ExEx_Broken_T_01
WallExt_{id}_Wall_ExEx_Broken_B_01
WallExt_{id}_Wall_ExEx_Broken_R_01
WallExt_{id}_Wall_ExEx_Broken_RT_01
WallExt_{id}_Wall_ExEx_Broken_RB_01
WallExt_{id}_Wall_ExEx_BrokenDec_T_01
WallExt_{id}_Wall_ExEx_BrokenDec_B_01
WallExt_{id}_Wall_ExEx_BrokenDec_R_01
WallExt_{id}_Wall_ExEx_Damaged_01
```

Floors and indoor lining break the same way: `Floor_{id}_Broken_R_01`, `WallInt_{id}_Wall_Broken_R_01`, `Roof_{EntitySet}_Plane_Broken_T_01`.

Without these meshes a shot becomes a missing entity in the log. Fine for a prototype. A combat set is dozens of meshes per material (vanilla Brick also has `_02` / `_03` on many sides).

The preset lists the suffixes that exist: `subvariants`, `corner_subvariants`, `broken_*_subvariants`, `broken_attaches_*`, `damaged_subvariants`. Flags `use_damaged` / `use_damaged_first_floor` show Damaged instead of a break.

### 10. Decor — not a slab

`WallDec_*`, friezes, plinths — ordinary props. They link to the wall via a collection (C). They are not part of the material preset and do not appear from it.

## Which names you need, by wave

Example `id = JazzBrick`. Substitute your token.

### MVP — see a room box

Presets: `SlabMaterials` with `id = "JazzBrick"`; optionally `FloorSlabMaterials` with the same `id`.

```text
WallExt_JazzBrick_Wall_ExEx_01      wall
WallExt_JazzBrick_Corner_01         corner post
WallExt_JazzBrick_CapL_01           L-joint
WallExt_JazzBrick_CapT_01           T-joint
WallExt_JazzBrick_CapX_01           cross
Floor_JazzBrick_01                  floor (if custom)
```

That is enough: Map Editor → room → Wall Material = JazzBrick → a box with no holes at the corners.

### Wave 2 — house with interior lining

```text
WallExt_JazzBrick_Wall_ExIn_01
WallExt_JazzBrick_Wall_InIn_01
WallInt_{indoor_id}_Wall_01
WallInt_{indoor_id}_Corner_01
```

### Wave 3 — combat destruction

`Broken_*` / `BrokenDec_*` / optionally `Damaged_*` for every base you use (`ExEx`, then ExIn/InIn, floor, indoor).

### Wave 4 — roof

`Roof_{EntitySet}_Plane_01` plus Eave / Rake / Ridge / RakeEave / RakeRidge. Add Gable / RakeGable only if you want a gable roof. Do not make Crest/Slope/`*Bot` meshes for a first roof.

### Wave 5 — openings for this material

`Window_*` / `Door_*` / `WindowVent_*` of the height and width you need.

### Wave 6 — subvariants

`_02`, `_03` and matching `subvariants` on the preset so walls do not clone one-to-one.

## Files required per name

One in-game name = one Entity:

| File | Why |
|---|---|
| `Entities/WallExt_{id}_Wall_ExEx_01.ent` | mesh + states (`idle` is required) |
| `Entities/WallExt_{id}_Wall_ExEx_01.lua` | `EntityData` (`fade_category = Never`, `material_type`) |
| `.mtl` + DDS | Base / Norm / RM / AO / Colorization |
| Collision surface in `.ent` | bullets, LOS, cover |
| row in `items.lua` | `ModItem` Entity |
| `SlabMaterials` preset with the same `id` | the room sees the material in the list |

Textures can be shared between wall, corner, and caps if the UV is shared. Entity names cannot — each one is unique.

## Vanilla materials (do not reuse these ids)

Walls (`SlabMaterials`): `Adobe`, `Brick`, `City`, `Colonial`, `ColonialFence1`, `ColonialFence2`, `Concrete`, `ConcreteThin`, `MetalScaff`, `Planks`, `RedBrick`, `Shanty`, `Sticks`, `Tin`, `Warehouse`, `Wood`, plus `PalmLeaves`.

Floors (`FloorSlabMaterials`): `Adobe`, `Colonial`, `ColonialTiles`, `Concrete`, `MetalScaff`, `Planks`, `WoodScaff`.

Roofs (`RoofSlabMaterials`): `Adobe`, `Concrete`, `PalmLeaves`, `Plywood`, `Sticks`, `Straw`, `Tiles`, `Tin`, `Wood`.

Indoor (`SlabIndoorMaterials`): `CityTiles`, `Colonial`, `Concrete`, `Planks`, `Wood`.

A preset with one of those ids is a vanilla override, not a new material.

## Preset in the Mod Editor

Right-click the mod tree → **New → Buildings**:

| Editor item | Class | Who reads it |
|---|---|---|
| Slab material | `SlabMaterials` | walls, `Room.wall_mat` |
| Floor material | `FloorSlabMaterials` | floor / ceiling |
| Roof material | `RoofSlabMaterials` | roof (`EntitySet`!) |
| Stairs material | `StairsSlabMaterials` | stairs |
| Shelter material | `ShelterSlabMaterials` | shelters |

Indoor walls: a preset in group `SlabIndoorMaterials`.

Fields:

- **id** — token in the entity name.
- **display_name** — label in the editor.
- **obj_material** — combat `ObjMaterial` (`Brick`, `Wood`, `ConcreteThin`, `Planks`, `ClayBrick`, `Metal_Inv_Penetrable`, …): HP, penetration, hit FX.
- **strength** — which wall “wins” if two rooms share a voxel.
- **subvariants** — `{suffix, chance}` for random picks.
- roof: **EntitySet**, **roof_additional_height**.

A new `ObjMaterial` is unnecessary if vanilla is enough. If you need one — a separate preset (HP, impenetrable, noise).

Saving the mod writes `items.lua` + companion. That is generated data: one transaction with `metadata.lua`.

Preset meaning (not a 1:1 editor dump):

```lua
PlaceObj('SlabMaterials', {
  id = "JazzBrick",
  display_name = T(...),
  obj_material = "Brick",
  strength = 3,
  subvariants = {
    PlaceObj('SlabMaterialSubvariant', nil), -- 01
    PlaceObj('SlabMaterialSubvariant', { suffix = "02", chance = 40 }),
  },
  corner_subvariants = {
    PlaceObj('SlabMaterialSubvariant', nil),
  },
})
```

The engine will look for `WallExt_JazzBrick_Wall_ExEx_01` and `_02`.

## Model, material, textures

### Entity pipeline

1. Blender 2.93+ and the `ModTools/HGBlenderExporter.zip` add-on (**HGE Tools** panel). A file written in Blender 5.x opens in 4.5 with data loss — stay on one version.
2. Origin (empty/armature) → mesh parented to the origin. An **idle** state is required.
3. Size must match the voxel: wall 1.2 × 0.7, floor 1.2 × 1.2. Pivot like vanilla (**wall on the voxel edge**, not in the tile center). Otherwise the room “floats” or you get double thickness at the joint.
4. Collision surface (type Collision) — without it bullets, cover, and LOS ignore the wall.
5. Turn off `hge_export` on references (human, ground grid), or Export All will drag them into the mod.
6. PBR in Haemimont Material (do not treat Principled as the source of truth):

   | Map | File | Role |
   |---|---|---|
   | Base color | TGA 24/32 | albedo; alpha → Use Alpha Test |
   | Normal | TGA | normals |
   | Roughness/Metallic | TGA | R = roughness, B = metalness |
   | AO | TGA grayscale | occlusion |
   | Colorization | TGA | up to 4 masks (R/G/B/A) → room Color1/2/3 |

   Colorization: black = ignore; R/G/B/A = parts 1–4; no gradients on seams. Paintable areas in BaseColor should be grey (~190–220). Keep UVs in 0–1.

7. Export All → `%AppData%/Jagged Alliance 3/ExportedEntities`.
8. Mod Editor → New → Assets → Entity → Import `.ent`.
9. After re-export the entity **does not hot-reload** — restart the game or use a new name.

After import, normalize DDS (`Entity_MapType`), then Save materials / SaveWholeMod to rebuild `mtlbin`. Do not leave numeric DDS. In JAZZ, weapons use `$rename-jazz-weapon-textures`; slabs follow the same naming rule.

On the Entity: `fade_category = Never` (like vanilla slabs), `material_type` matching `obj_material`, debris optional (`Debris_Wooden_*`, `Debris_ConcreteBrick_*`).

### Practical path: retexture vanilla

A full Adobe set is dozens of meshes. For a new “brick” you usually:

1. Copy vanilla geometry (`Brick` / `Planks`) into Blender with the same bounds and pivot, then apply your UV/textures.
2. Export under **new names** with your `id`.
3. Do not rely on `inherit_entity` for vanilla slabs: `can_be_inherited` is usually off on walls.

A box from scratch almost always breaks joints: a pivot in the tile center (`X` ±0.6, `Y` ±0.1) is the most common draft mistake.

## Sample `JazzStub`

Public sample: [Kpoji4er/JAZZ-slabs-sample](https://github.com/Kpoji4er/JAZZ-slabs-sample) (id `jSlbStb`, not a suite package). Clone or unzip into `Mods/jazz-slabs`. One box under the six required names: ExEx, Corner, CapL/T/X, Floor. In the Map Editor the material is **Jazz Stub**. No ExIn, indoor, roof, windows, or Broken. The pivot is not vanilla — this is only enough to spawn a room.

## A separate mod, not a prop pack and not `jazz_assets`

Keep slabs in their own package: the mesh set is large, and JAZZ campaigns do not need them until maps pick the `id`.

```text
Mods/jazz-slabs/                    (package name is yours)
  Entities/
    WallExt_JazzBrick_Wall_ExEx_01.lua
    WallExt_JazzBrick_Wall_ExEx_01.ent
    Materials/....mtl
    Textures/WallExt_JazzBrick_*_Base.dds
  items.lua                         -- ModItem Entity + ModItem SlabMaterials
  metadata.lua                      -- your own mod id, not e6L4ECj / pDGDhr / …
```

- Not a fifth required JAZZ package.
- `jazz-maps` adds a dependency **only when** rooms on a map actually pick this `id`.
- Can ship on Steam/Workshop on its own, including without JAZZ.
- Do not put entities in `jazz` or `jazz-maps`.
- If you still put it in the suite: entity + preset go in `jazz_assets` (or a mod that loads before `jazz-maps`); a new public `id` needs a spec + DoR; generated data is one transaction of `items.lua` + `metadata.lua` + companion.

## Check in the Map Editor

1. Enable the mod with the entity **and** the preset, then restart the game.
2. Open a map / patch.
3. Ctrl-Shift-N — room; in Properties: Wall Material = your `id`.
4. Alt-G — voxel grid; Ctrl-Shift-K — collisions; Ctrl-Shift-X — cover.
5. Break a wall in combat — Broken/Damaged, or a missing entity in the log.
6. Change Inner Wall Material — does `WallInt_*` appear?

Search the log for `Failed to load` / missing entity with the **full** name the engine expected.

## Limits and common mistakes

- Entity name = contract. The preset has no model path.
- The roof looks at `EntitySet`, not `id`.
- Indoor ≠ Outdoor: `WallExt_*` and `WallInt_*` are different preset families.
- Windows and doors do not appear from `SlabMaterials`.
- Decor (`WallDec_*`) is props, not part of the preset.
- After re-importing an entity — restart.
- Pivot and thickness — “wall in the floor” / double thickness at the joint.
- Without a Collision surface the wall looks fine but is shoot-through and gives no cover.
- `hge_export` on references — the human and the ground leave with the mod.
- Broken texture paths from another machine (`C:\Users\…`) will not survive moving the Blend file.

## Checklist

1. Short `id` (e.g. `JazzBrick`), no clash with vanilla.
2. Scope: ExEx prototype only, or the full set (ExIn/InIn, indoor, broken, roof, windows).
3. Mesh sized 1.2 × 0.7 (wall) / 1.2 × 1.2 (floor), vanilla pivot, Collision surface.
4. PBR TGA → Blender HGE export → Import Entity.
5. Entity names strictly follow the formulas above.
6. ModItem Slab/Floor/Roof material with the same `id`.
7. `obj_material` on an existing combat material unless you have a reason to add a new one.
8. Save the mod, restart, room in the Map Editor, collisions, one destruction shot.
9. Normalize DDS and rebuild `mtlbin`.
