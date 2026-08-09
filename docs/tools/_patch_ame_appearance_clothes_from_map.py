#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch AME AppearancePresets from map donors (jazz-units Legion* canon + Rebels/GC).

JAZZ-UNITS-005 appearance lean:
  - Canon Legion look = jazz-units handcrafted Legion* (not vanilla Legion_*).
  - Clothing clone from donor; preserve Head + BodyColor C1 + HeadColor from current AME.
  - One AME-blue accent; Legion red / extra blue → slate.
  - Female Hair: NPCFemale_Hair_* only (no AIM Equipment*_Hair).
  - If Hat or Hat2 has a mesh → Hair = "" (anti-collision).

Usage (jazz/):
  python docs/tools/_patch_ame_appearance_clothes_from_map.py --dry-run
  python docs/tools/_patch_ame_appearance_clothes_from_map.py
  python docs/tools/_patch_ame_appearance_clothes_from_map.py --write-map-only
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
JU = JAZZ.parent / "jazz-units"
ITEMS = JU / "items.lua"
MAP_PATH = JAZZ / "docs" / "design" / "ame-appearance-map.json"
GEN_PATH = JAZZ / "docs" / "tools" / "_gen_ame_appearances.py"
VANILLA_AP = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Data\AppearancePreset.lua"
)

SECTION_BEGIN = "-- JAZZ-UNITS-005-AME-APP-BEGIN"
SECTION_END = "-- JAZZ-UNITS-005-AME-APP-END"

NPC_FEMALE_HAIR = [
    "NPCFemale_Hair_01",
    "NPCFemale_Hair_02",
    "NPCFemale_Hair_03",
    "NPCFemale_Hair_04",
]

# Headwear policy (owner feedback):
# - Strip: helmets, turbans, most caps, balaclavas/face masks, AIM Equipment*_Hat
# - Keep: glasses, headbands, scarves
# - Partial berets: FactionMale_Hat_01 / NPCCostumeMale_Hat_03 (slate, never blue)
_HELMET_RE = re.compile(
    r"Helmet|WW2Helmet|SkullHat|LarryAddicted_Hat|"
    r"^FactionMale_Hat_08$|^FactionMale_Hat_09$",
    re.I,
)
_BALACLAVA_RE = re.compile(
    r"MilitiaCostumeMale_Mask_|Faction_Thugs_Mask_|Mask_0",
    re.I,
)
_BERET_MESHES = frozenset(
    {
        "FactionMale_Hat_01",  # Adonis/Rebel beret
        "NPCCostumeMale_Hat_03",  # olive/brown beret
    }
)
_STRIP_HEADWEAR_RE = re.compile(
    r"Helmet|WW2Helmet|SkullHat|LarryAddicted_Hat|"
    r"TraditionalMale_Hat|TraditionalFemale_Hat|"
    r"NPCCostumeFemale_Hat|"
    r"FactionMale_Hat_|"
    r"NPCCostumeMale_Hat_|"  # strip all then re-add berets selectively
    r"NPCHyenaGilbert_Hat|"
    r"Equipment\w+_Hat|"
    r"Equipment\w+_Cap|"
    r"MilitiaCostumeMale_Mask_|"
    r"Faction_Thugs_Mask_",
    re.I,
)
# Urban/woodland camo shirts+pants — keep earth tones; never AME-blue these meshes.
_CAMO_MESH_RE = re.compile(
    r"Equipment(?:Male|Female)_(?:Shirt|Pants)_02|"
    r"MilitiaCostume|"
    r"Faction_Militia_Top|"
    r"Faction_Militia_Bottom",
    re.I,
)
# Olive / brown camo channels (not blue, not slate-grey).
_CAMO_EARTH = [
    ((48, 54, 30), (58, 48, 28), (36, 40, 22)),
    ((52, 46, 28), (62, 52, 32), (40, 36, 22)),
    ((42, 50, 28), (54, 44, 26), (34, 38, 20)),
    ((56, 50, 32), (46, 42, 24), (38, 34, 20)),
    ((44, 48, 26), (60, 50, 30), (32, 36, 18)),
]
# Neutral beret colors (never AME blue).
_BERET_COLORS = [
    (28, 32, 24),
    (40, 28, 22),
    (22, 26, 20),
    (48, 36, 28),
    (34, 38, 30),
]
# Slots that get a beret (~1/3 of male roster, prefers leaders/officers).
_BERET_SLOTS = frozenset({8, 16, 24, 27, 35, 39, 45, 47, 51, 55, 57, 60})

# Curated donor shuffle (plan proportions). Keys = slot int.
# Irregulars lean jazz Legion*; Fighters mix; Hardened mostly GC; Spec swap vanilla Legion_* → canon.
CURATED_DONORS: dict[int, str] = {
    # Irregulars male — jazz Legion* base/alt
    1: "LegionGoon",
    2: "LegionGoon_alt",
    3: "LegionGoon_alt_2",
    4: "LegionGoon_alt_3",
    5: "LegionButcher",
    6: "LegionButcher_alt",
    7: "LegionButcher_alt_2",
    8: "LegionButcher_alt_3",
    9: "LegionRaider",
    10: "LegionRaider_alt",
    11: "GrandChien_CommanderFemale",  # keep ♀
    12: "LegionRaider_alt_2",
    13: "Artillery_Rebels",  # keep Rebel
    14: "LegionScout",
    15: "LegionScout_alt",
    16: "Commander_Rebels",  # keep
    17: "MilitiaRookie_Female_01",  # keep ♀
    18: "Demolitions_Rebels",  # keep
    19: "LegionMedic",
    20: "LegionSharpShooter_alt",
    # Fighters — Rebels keep + Legion* inserts
    21: "LegionGunner",
    22: "Heavy_Rebels_02",
    23: "LegionGunner_alt",
    24: "Marksman_Rebels",
    25: "LegionSniper",
    26: "Marksman_Rebels_03",
    27: "Medic_Rebels",
    28: "LegionMedic_alt",
    29: "Medic_Rebels_03",
    30: "Recon_Rebels",
    31: "LegionScout_alt_2",
    32: "MilitiaRookie_Female_02",
    33: "Recon_Rebels_03",
    34: "LegionManiac",
    35: "Soldier_Rebels_02",
    36: "Soldier_Rebels_03",
    37: "LegionManiac_alt",
    38: "Stormer_Rebels",
    # Hardened — mostly GC; 2 Legion*
    39: "GrandChien_Artillery",
    40: "LegionGrenadir_alt",
    41: "GrandChien_Heavy",
    42: "GrandChien_Marksman",
    43: "GrandChien_Medic",
    44: "RebelFemaleSniper",
    45: "GrandChien_Officer",
    46: "GrandChien_Recon",
    47: "LegionRaidLeader_alt",
    48: "GrandChien_Stormer",
    # Specialists — replace vanilla Legion_* with canon; light shuffle
    49: "RebelFemaleSniper_1",
    50: "RebelFemaleSniper_1",
    51: "LegionSharpShooter",
    52: "MilitiaRookie_Female_01",
    53: "MilitiaRookie_Female_02",
    54: "Stormer_Rebels_03",
    55: "LegionRaidLeader",
    56: "GrandChien_CommanderFemale",
    57: "LegionGrenadir",
    58: "MilitiaRookie_Female_02",
    59: "LegionScout_Stronger_alt",
    60: "LegionRaider_Stronger_alt",
}


def load_gen():
    spec = importlib.util.spec_from_file_location("gen_ame_appearances", GEN_PATH)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {GEN_PATH}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def extract_moditem_appearances(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    needle = "PlaceObj('ModItemAppearancePreset'"
    i = 0
    while True:
        start = text.find(needle, i)
        if start < 0:
            break
        brace = text.find("{", start)
        depth = 0
        j = brace
        while j < len(text):
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    if end < len(text) and text[end] == ")":
                        end += 1
                    block = text[start:end]
                    m = re.search(r"\bid\s*=\s*\"([^\"]+)\"", block)
                    if m:
                        out[m.group(1)] = block
                    i = end
                    break
            j += 1
        else:
            break
    return out


def is_canon_legion(aid: str) -> bool:
    return (
        aid.startswith("Legion")
        and not aid.startswith("Legion_")
        and "Armor" not in aid
    )


def mesh_of(block: str, key: str) -> str:
    m = re.search(rf"{key}\s*=\s*\"([^\"]*)\"", block)
    return m.group(1).strip() if m else ""


def set_or_insert_field(inner: str, key: str, value: str) -> str:
    """Set Key = \"value\" inside ModItem/Appearance inner fields."""
    pat = rf"{key}\s*=\s*\"[^\"]*\""
    repl = f'{key} = "{value}"'
    if re.search(pat, inner):
        return re.sub(pat, repl, inner, count=1)
    # Insert after Body line if present, else at start of fields.
    if re.search(r'Body\s*=\s*"[^"]+"\s*,', inner):
        return re.sub(
            r'(Body\s*=\s*"[^"]+"\s*,)',
            rf'\1\n\t\t\t{key} = "{value}",',
            inner,
            count=1,
        )
    return f'\t\t\t{key} = "{value}",\n' + inner


def clear_field(inner: str, key: str) -> str:
    if re.search(rf"{key}\s*=\s*\"[^\"]*\"", inner):
        return re.sub(rf"{key}\s*=\s*\"[^\"]*\"", f'{key} = ""', inner, count=1)
    return set_or_insert_field(inner, key, "")


def extract_propset(block: str, part: str) -> str | None:
    m = re.search(
        rf"{part}\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{{([\s\S]*?)\}}\)",
        block,
    )
    return m.group(0) if m else None


def replace_propset(inner: str, part: str, full_prop: str) -> str:
    pat = rf"{part}\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{{[\s\S]*?\}}\)"
    if re.search(pat, inner):
        return re.sub(pat, full_prop, inner, count=1)
    # Insert after related mesh or BodyColor.
    return inner.rstrip() + (",\n" if not inner.rstrip().endswith(",") else "\n") + f"\t\t\t{full_prop},"


def is_helmet_mesh(mesh: str) -> bool:
    return bool(mesh and _HELMET_RE.search(mesh))


def is_strip_headwear(mesh: str) -> bool:
    """Strip turbans/caps/helmets/balaclavas. Keep glasses/headband/scarf. Berets handled separately."""
    if not mesh:
        return False
    if mesh in _BERET_MESHES:
        return False  # may keep if already present; assign_partial_berets decides
    if re.search(r"Glasses|Headband|Scarf", mesh, re.I):
        return False
    if _BALACLAVA_RE.search(mesh):
        return True
    return bool(_STRIP_HEADWEAR_RE.search(mesh) or _HELMET_RE.search(mesh))


def strip_helmets(inner: str) -> str:
    """Clear Hat/Hat2 helmets, balaclavas, most hats/turbans."""
    for key in ("Hat", "Hat2"):
        if is_strip_headwear(mesh_of(inner, key)):
            inner = clear_field(inner, key)
    return inner


def assign_partial_berets(inner: str, slot: int, female: bool) -> str:
    """Give ~12 male slots a slate/olive beret (never blue). Skip females."""
    if female or slot not in _BERET_SLOTS:
        # Drop leftover berets on non-beret slots.
        for key in ("Hat", "Hat2"):
            if mesh_of(inner, key) in _BERET_MESHES:
                inner = clear_field(inner, key)
        return inner
    # Prefer Hat; if Hat holds glasses, put beret on Hat and move glasses to Hat2.
    hat = mesh_of(inner, "Hat")
    hat2 = mesh_of(inner, "Hat2")
    beret = "FactionMale_Hat_01" if slot % 2 else "NPCCostumeMale_Hat_03"
    if hat and re.search(r"Glasses", hat, re.I):
        if not hat2:
            inner = set_or_insert_field(inner, "Hat2", hat)
        inner = set_or_insert_field(inner, "Hat", beret)
    elif hat2 and re.search(r"Glasses", hat2, re.I):
        inner = set_or_insert_field(inner, "Hat", beret)
    elif not hat or hat in _BERET_MESHES or is_strip_headwear(hat):
        inner = set_or_insert_field(inner, "Hat", beret)
    else:
        # Hat has scarf/headband — beret wins for these slots.
        if not hat2 and re.search(r"Scarf|Headband", hat, re.I):
            inner = set_or_insert_field(inner, "Hat2", hat)
        inner = set_or_insert_field(inner, "Hat", beret)
    # Force earth beret tint (not blue).
    r, g, b = _BERET_COLORS[(slot - 1) % len(_BERET_COLORS)]
    prop = (
        "HatColor = PlaceObj('ColorizationPropSet', {\n"
        f"\t\t\t'EditableColor1', RGBA({r}, {g}, {b}, 255),\n"
        f"\t\t\t'EditableColor2', RGBA({max(r-6,0)}, {max(g-4,0)}, {max(b-4,0)}, 255),\n"
        f"\t\t\t'EditableColor3', RGBA({max(r-10,0)}, {max(g-8,0)}, {max(b-6,0)}, 255),\n"
        "\t\t\t})"
    )
    if re.search(r"HatColor\s*=\s*PlaceObj", inner):
        inner = re.sub(
            r"HatColor\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{[\s\S]*?\}\)",
            prop,
            inner,
            count=1,
        )
    else:
        inner = replace_propset(inner, "HatColor", prop)
    return inner


def is_camo_mesh(mesh: str) -> bool:
    return bool(mesh and _CAMO_MESH_RE.search(mesh))


def choose_blue_accent_clothes(block: str) -> tuple[str, int]:
    """One muted blue on non-camo cloth — never Hat, never Hip pouches, never camo."""
    shirt = mesh_of(block, "Shirt")
    if shirt and not is_camo_mesh(shirt):
        return "ShirtColor", 1
    if mesh_of(block, "Chest"):
        return "ChestColor", 1
    if mesh_of(block, "Armor"):
        return "ArmorColor", 1
    body = mesh_of(block, "Body")
    if body.startswith("Faction_") and not is_camo_mesh(body):
        return "BodyColor", 2
    hat2 = mesh_of(block, "Hat2")
    if hat2 and re.search(r"Scarf", hat2, re.I):
        return "Hat2Color", 1
    # Do NOT use HipColor — blue pouches look bad.
    return "BodyColor", 2


def ensure_blue_accent_carrier(inner: str, female: bool) -> str:
    """Camo-only kits get a chest carrier for blue — never Hip pouches."""
    shirt = mesh_of(inner, "Shirt")
    pants = mesh_of(inner, "Pants")
    body = mesh_of(inner, "Body")
    has_carrier = bool(
        mesh_of(inner, "Chest")
        or mesh_of(inner, "Armor")
        or (shirt and not is_camo_mesh(shirt))
        or (body.startswith("Faction_") and not is_camo_mesh(body))
        or (mesh_of(inner, "Hat2") and re.search(r"Scarf", mesh_of(inner, "Hat2"), re.I))
    )
    camo_kit = is_camo_mesh(shirt) or is_camo_mesh(pants)
    if camo_kit and not has_carrier:
        if not mesh_of(inner, "Chest"):
            # Light recon chest kit — blue tint OK; not hip pouches.
            inner = set_or_insert_field(inner, "Chest", "Faction_Acc_Recon_02")
        elif not mesh_of(inner, "Hat2"):
            inner = set_or_insert_field(inner, "Hat2", "Faction_Militia_Scarf_01")
    # Strip blue-carrier Hip Acc_Soldier we may have added earlier.
    if mesh_of(inner, "Hip") == "Faction_Acc_Soldier":
        # Only clear if it was our camo carrier hack (no other hip role gear needed here).
        # Keep demo/medic/heavy hip if present from donor — Acc_Soldier alone → clear.
        inner = clear_field(inner, "Hip")
    return inner


def force_camo_earth_tones(inner: str, slot: int) -> str:
    """Keep camo Shirt/Pants olive/brown — undo blue or slate wash on those meshes."""
    for key, color_key in (("Shirt", "ShirtColor"), ("Pants", "PantsColor")):
        if not is_camo_mesh(mesh_of(inner, key)):
            continue
        c1, c2, c3 = _CAMO_EARTH[(slot - 1) % len(_CAMO_EARTH)]
        prop = (
            f"{color_key} = PlaceObj('ColorizationPropSet', {{\n"
            f"\t\t\t'EditableColor1', RGBA({c1[0]}, {c1[1]}, {c1[2]}, 255),\n"
            f"\t\t\t'EditableColor2', RGBA({c2[0]}, {c2[1]}, {c2[2]}, 255),\n"
            f"\t\t\t'EditableColor3', RGBA({c3[0]}, {c3[1]}, {c3[2]}, 255),\n"
            "\t\t\t})"
        )
        if re.search(rf"{color_key}\s*=\s*PlaceObj", inner):
            inner = re.sub(
                rf"{color_key}\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{{[\s\S]*?\}}\)",
                prop,
                inner,
                count=1,
            )
        else:
            inner = replace_propset(inner, color_key, prop)
    return inner


def preserve_head_skin(inner: str, old_ame: str) -> str:
    head = mesh_of(old_ame, "Head")
    if head:
        inner = set_or_insert_field(inner, "Head", head)
    for part in ("BodyColor", "HeadColor"):
        prop = extract_propset(old_ame, part)
        if not prop:
            continue
        # Normalize indentation inside prop to match AME style loosely — keep as-is from old.
        # Re-indent: ensure field starts with tabs when we inject via replace.
        prop_n = prop
        inner = replace_propset(inner, part, prop_n)
    # Force HeadColor channels to black if somehow missing after replace.
    if "HeadColor" not in inner:
        inner = (
            inner.rstrip().rstrip(",")
            + ",\n"
            + "\t\t\tHeadColor = PlaceObj('ColorizationPropSet', {\n"
            + "\t\t\t'EditableColor1', RGBA(0, 0, 0, 255),\n"
            + "\t\t\t'EditableColor2', RGBA(0, 0, 0, 255),\n"
            + "\t\t\t'EditableColor3', RGBA(0, 0, 0, 255),\n"
            + "\t\t\t}),"
        )
    return inner


def apply_hair_rules(inner: str, slot: int, female: bool) -> tuple[str, str]:
    """Hat/Hat2 mesh ⇒ empty Hair. Females without hat ⇒ NPCFemale_Hair_*. Strip AIM Equipment*_Hair."""
    hat = mesh_of(inner, "Hat")
    hat2 = mesh_of(inner, "Hat2")
    if hat or hat2:
        inner = clear_field(inner, "Hair")
        return inner, ""

    if female:
        hair = NPC_FEMALE_HAIR[(slot * 3) % len(NPC_FEMALE_HAIR)]
        inner = set_or_insert_field(inner, "Hair", hair)
        dark = [
            (8, 6, 5),
            (12, 9, 7),
            (16, 12, 10),
            (6, 5, 4),
            (20, 14, 11),
            (10, 8, 6),
            (14, 10, 8),
            (18, 12, 9),
            (7, 5, 4),
            (22, 16, 12),
        ][(slot - 1) % 10]
        r, g, b = dark
        hair_color = (
            "HairColor = PlaceObj('ColorizationPropSet', {\n"
            f"\t\t\t'EditableColor1', RGBA({r}, {g}, {b}, 255),\n"
            f"\t\t\t'EditableColor2', RGBA({max(r-4,0)}, {max(g-3,0)}, {max(b-2,0)}, 255),\n"
            f"\t\t\t'EditableColor3', RGBA({max(r-6,0)}, {max(g-4,0)}, {max(b-3,0)}, 255),\n"
            "\t\t\t})"
        )
        if re.search(r"HairColor\s*=\s*PlaceObj", inner):
            inner = re.sub(
                r"HairColor\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{[\s\S]*?\}\)",
                hair_color,
                inner,
                count=1,
            )
        else:
            inner = replace_propset(inner, "HairColor", hair_color)
        return inner, hair

    # Males: never keep AIM Equipment*_Hair on AME.
    hair = mesh_of(inner, "Hair")
    if hair.startswith("Equipment"):
        inner = clear_field(inner, "Hair")
        return inner, ""
    return inner, hair


def apply_female_hair(inner: str, slot: int, female: bool) -> tuple[str, str]:
    """Back-compat alias."""
    return apply_hair_rules(inner, slot, female)


def moditem_inner_from_block(block: str) -> str:
    """Extract inner fields from ModItemAppearancePreset or AppearancePreset PlaceObj."""
    m = re.match(
        r"PlaceObj\('(?:ModItem)?AppearancePreset',\s*\{([\s\S]*)\}\)\s*$",
        block.strip(),
    )
    if not m:
        # brace extract fallback
        brace = block.find("{")
        depth = 0
        for j in range(brace, len(block)):
            if block[j] == "{":
                depth += 1
            elif block[j] == "}":
                depth -= 1
                if depth == 0:
                    return block[brace + 1 : j]
        raise ValueError("cannot parse appearance block")
    return m.group(1)


def strip_group_id(inner: str) -> str:
    inner = re.sub(r"^\s*group\s*=\s*\"[^\"]*\"\s*,?\s*$", "", inner, flags=re.M)
    inner = re.sub(r"^\s*id\s*=\s*\"[^\"]*\"\s*,?\s*$", "", inner, flags=re.M)
    return inner


def format_moditem(inner: str, new_id: str) -> str:
    lines = []
    for ln in inner.splitlines():
        if not ln.strip():
            continue
        stripped = ln.lstrip("\t ")
        lines.append("\t\t\t" + stripped)
    body = "\n".join(lines)
    if body and not body.rstrip().endswith(","):
        body = body.rstrip() + ","
    return (
        "\t\tPlaceObj('ModItemAppearancePreset', {\n"
        f"{body}\n"
        f'\t\t\tgroup = "AME",\n'
        f'\t\t\tid = "{new_id}",\n'
        "\t\t}),"
    )


def build_from_donor(
    gen,
    donor_block: str,
    donor_id: str,
    new_id: str,
    slot: int,
    female: bool,
    old_ame: str,
) -> tuple[str, str | None, str]:
    """Returns (lua_moditem, head_swap_note, hair)."""
    # Start from gen pipeline when donor is vanilla AppearancePreset.
    if donor_block.strip().startswith("PlaceObj('AppearancePreset'"):
        lua, head_swap = gen.to_moditem(donor_block, new_id, donor_id, slot, female=female)
        # Extract inner from produced lua to preserve head/skin + hair.
        inner = moditem_inner_from_block(lua)
        inner = strip_group_id(inner)
        inner = preserve_head_skin(inner, old_ame)
        # Re-apply africanize head from old (preserve already set Head).
        inner = gen.gender_fix_gear(inner, slot, female)
        inner = strip_helmets(inner)
        inner = ensure_blue_accent_carrier(inner, female)
        # Recolor: blue on non-camo carrier — never hats / camo shirt-pants / hip pouches.
        _orig_choose = gen.choose_blue_accent
        gen.choose_blue_accent = choose_blue_accent_clothes
        try:
            tmp = "PlaceObj('AppearancePreset', {\n" + inner + "\n})"
            recolored = gen.recolor_block(tmp, slot)
        finally:
            gen.choose_blue_accent = _orig_choose
        inner = moditem_inner_from_block(recolored)
        inner = strip_group_id(inner)
        inner = preserve_head_skin(inner, old_ame)
        inner = force_camo_earth_tones(inner, slot)
        inner = assign_partial_berets(inner, slot, female)
        inner, hair = apply_hair_rules(inner, slot, female)
        return format_moditem(inner, new_id), head_swap, hair

    # jazz-units ModItemAppearancePreset (canon Legion*)
    inner = strip_group_id(moditem_inner_from_block(donor_block))
    tmp = "PlaceObj('AppearancePreset', {\n" + inner + "\n})"
    m = re.match(r"PlaceObj\('AppearancePreset',\s*\{([\s\S]*)\}\)\s*$", tmp.strip())
    assert m
    inner2 = m.group(1)
    inner2, head_swap = gen.africanize_head(inner2, slot, female)
    inner2 = gen.gender_fix_gear(inner2, slot, female)
    inner2 = strip_helmets(inner2)
    inner2 = ensure_blue_accent_carrier(inner2, female)
    _orig_choose = gen.choose_blue_accent
    gen.choose_blue_accent = choose_blue_accent_clothes
    try:
        tmp2 = "PlaceObj('AppearancePreset', {\n" + inner2 + "\n})"
        tmp2 = gen.recolor_block(tmp2, slot)
    finally:
        gen.choose_blue_accent = _orig_choose
    inner2 = moditem_inner_from_block(tmp2)
    inner2 = strip_group_id(inner2)
    inner2 = preserve_head_skin(inner2, old_ame)
    inner2 = force_camo_earth_tones(inner2, slot)
    if mesh_of(inner2, "Head").startswith("Faction_Legion_Head_"):
        head = mesh_of(old_ame, "Head") or gen.african_head_for(slot, female)
        inner2 = set_or_insert_field(inner2, "Head", head)
    inner2 = assign_partial_berets(inner2, slot, female)
    inner2, hair = apply_hair_rules(inner2, slot, female)
    return format_moditem(inner2, new_id), head_swap, hair


def update_map(rows: list[dict], donors: dict[int, str], hair_by_slot: dict[int, str]) -> list[dict]:
    out = []
    for row in rows:
        slot = int(row["slot"])
        r = dict(row)
        if slot in donors:
            r["donor"] = donors[slot]
        if r.get("female"):
            r["hair"] = hair_by_slot.get(slot, "")
        elif "hair" in r:
            del r["hair"]
        out.append(r)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--write-map-only",
        action="store_true",
        help="Only write curated donors into ame-appearance-map.json",
    )
    args = ap.parse_args()

    gen = load_gen()
    rows = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    if len(rows) != 60:
        raise SystemExit(f"map size {len(rows)}")

    # Apply curated donors onto working copy
    donors = dict(CURATED_DONORS)
    for row in rows:
        slot = int(row["slot"])
        if slot not in donors:
            donors[slot] = row["donor"]

    if args.write_map_only:
        new_map = update_map(rows, donors, {})
        if not args.dry_run:
            MAP_PATH.write_text(
                json.dumps(new_map, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"wrote map donors → {MAP_PATH}")
        else:
            changed = sum(
                1
                for r in rows
                if donors[int(r["slot"])] != r["donor"]
            )
            print(f"dry-run map donor changes={changed}")
        return 0

    if not VANILLA_AP.is_file():
        raise SystemExit(f"missing vanilla AppearancePreset: {VANILLA_AP}")

    items_text = ITEMS.read_text(encoding="utf-8")
    ju_apps = extract_moditem_appearances(items_text)
    van_apps = gen.extract_appearance_blocks(VANILLA_AP.read_text(encoding="utf-8"))

    # Existing AME blocks for preserve
    ame_old = {aid: blk for aid, blk in ju_apps.items() if aid.startswith("JAZZ_AME_")}
    if len(ame_old) != 60:
        print(f"warn: found {len(ame_old)} JAZZ_AME_* presets (expected 60)")

    mod_blocks: list[str] = []
    hair_by_slot: dict[int, str] = {}
    missing = []
    changed = 0
    for row in rows:
        slot = int(row["slot"])
        new_id = row["id"]
        female = bool(row.get("female"))
        donor = donors[slot]
        old = ame_old.get(new_id, "")
        if old and mesh_of(old, "") == "":
            pass
        if donor != row.get("donor"):
            changed += 1

        if is_canon_legion(donor):
            if donor not in ju_apps:
                missing.append(donor)
                continue
            donor_block = ju_apps[donor]
        else:
            if donor not in van_apps:
                # Some female/militia may only exist as vanilla — fail hard
                missing.append(donor)
                continue
            donor_block = van_apps[donor]

        lua, _hs, hair = build_from_donor(
            gen, donor_block, donor, new_id, slot, female, old or donor_block
        )
        mod_blocks.append(lua)
        if female:
            hair_by_slot[slot] = hair

    if missing:
        raise SystemExit(f"missing donors: {missing}")

    body = "\n".join(mod_blocks)
    section = f"{SECTION_BEGIN}\n{body}\n{SECTION_END}"

    if SECTION_BEGIN not in items_text or SECTION_END not in items_text:
        raise SystemExit("AME APP section markers missing in items.lua")

    def _repl(_m: re.Match[str]) -> str:
        return section

    new_items = re.sub(
        re.escape(SECTION_BEGIN) + r".*?" + re.escape(SECTION_END),
        _repl,
        items_text,
        count=1,
        flags=re.S,
    )

    new_map = update_map(rows, donors, hair_by_slot)

    # Stats
    female_hairs = [hair_by_slot[int(r["slot"])] for r in rows if r.get("female")]
    legion_n = sum(1 for s, d in donors.items() if is_canon_legion(d))
    print(
        f"slots=60 curated_donor_changes≈{changed} canon_Legion*_donors={legion_n} "
        f"female_hair={female_hairs}"
    )

    if args.dry_run:
        print("dry-run: no write")
        return 0

    ITEMS.write_text(new_items, encoding="utf-8")
    MAP_PATH.write_text(
        json.dumps(new_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"wrote {ITEMS}")
    print(f"wrote {MAP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
