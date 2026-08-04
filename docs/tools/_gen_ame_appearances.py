#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Clone unique AME Appearance presets from Rebels/Legion/Militia (+ GrandChien for Hardened).

JAZZ-UNITS-005-REQ-019:
  - one ModItemAppearancePreset per slot: id = JAZZ_AME_NN
  - donor from faction pools (unique males; females may reuse donor mesh)
  - exactly ONE AME-blue accent (Hat > Hat2 > Shirt > BodyC2); never Pants/boots
  - other Legion red → muted slate (not blue); Body Color1 dark African; HeadColor (0,0,0)
  - Caucasian/Asian/AIM/Male_Head/Legion painted → narrow Af bank / Head_F_Af_NPC (see ame-appearance-assets.md)
  - source presets never edited

Usage (jazz/):
  python docs/tools/_gen_ame_appearances.py
  python docs/tools/_gen_ame_appearances.py --dry-run
  python docs/tools/_audit_patch_ame_heads.py --sync-map
  python docs/tools/_gen_ame_roster_60.py
  python docs/tools/_gen_ame_unitdata.py
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
ROSTER_SCRIPT = JAZZ / "docs" / "tools" / "_gen_ame_roster_60.py"
ITEMS = JU / "items.lua"
META = JU / "metadata.lua"
VANILLA_AP = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Data\AppearancePreset.lua"
)
MAP_OUT = JAZZ / "docs" / "design" / "ame-appearance-map.json"

SECTION = "JAZZ-UNITS-005-AME-APP"
ITEMS_BEGIN = f"-- {SECTION}-BEGIN"
ITEMS_END = f"-- {SECTION}-END"
META_BEGIN = f"\t\t-- {SECTION}-META-BEGIN"
META_END = f"\t\t-- {SECTION}-META-END"
AME_END = "-- JAZZ-UNITS-005-AME-END"

# Cloth blues (Militia-like + darker/navy variants for variety).
BLUE_PALETTE = [
    (49, 89, 163),
    (36, 72, 140),
    (28, 58, 120),
    (55, 100, 175),
    (40, 70, 130),
    (22, 48, 100),
    (60, 110, 180),
    (32, 64, 128),
]

# Dark African skin bank (near-black browns — forced on Body/Head Color1).
SKIN_BANK = [
    (6, 2, 1),
    (8, 3, 1),
    (10, 4, 2),
    (12, 5, 2),
    (14, 5, 3),
    (16, 5, 5),
    (17, 6, 3),
    (18, 7, 4),
    (19, 8, 4),
    (20, 7, 3),
]

# Ethnicity lives in the Head *mesh* + HeadColor (0,0,0) like vanilla.
# Do NOT tint HeadColor to skin RGB — that washes Male_Head faces to chalk-white.
# Do NOT use Faction_Legion_Head_* — war-paint / painted Legion faces.
# Male Af bank: player-verified dark African meshes only (see ame-appearance-assets.md).
# NEVER bank: Flay/Fidel/Magic/Blood (AIM, read Caucasian on AME).
# Never: Head_Fauda / Head_Lami (female) — Hat attach breaks / gender mesh mix.
# Never: Head_Omryn (Asian) — reads as pale/"white" on AME.
MALE_AF_HEADS = [
    "Head_Chimurenga",
    "Head_Pierre",
    "Head_Jackhammer",
    "Head_M_IMP_01",
    "Faction_Rebels_M_HeadMedic",
]
FEMALE_AF_HEADS = [f"Head_F_Af_NPC_{i:02d}" for i in range(1, 11)]

# AIM / ethnicity-coded / pale generic heads that must be swapped for AME.
# Includes former false-"Af" AIM heads (Flay/Fidel/Magic/Blood) and female-on-male risks.
_HEAD_FORCE_REPLACE = re.compile(
    r"^Head_(M|F)_(Ca|As|Senior|IMP)_"
    r"|^Male_Head_"
    r"|^Female_Head_"
    r"|^Head_(Vicki|Buns|Fox|Meltdown|Mouse|MD|Magic|Blood|Flay|Fauda|Lami|Fidel|"
    r"Barry|Ivan|Omryn|Livewire|Ice|Grizzly|Scope|Kalyna|Igor|"
    r"Faucheux|Major|Shadow|Raven|Tex|Scully|Steroid|DrQ|Gus|Len|Larry|"
    r"Red|Thor|Wolf|Sidney|Nails|Hitman|Grunty|Spike|Raider|Razor|"
    r"Reaper|Biff|Lynx)$",
    re.I,
)

# Legion war-paint / ceremonial bare torsos — never clone onto AME.
_LEGION_WARPAINT_BODY = re.compile(r"^Faction_Legion_Top_", re.I)
# No GrandChien_Top_05 — exposed arms stay pale despite dark BodyColor C1 (Claude report).
_SAFE_MALE_BODY = [
    "Faction_Militia_Top_02",
    "Faction_Militia_Top_03",
    "Faction_Rebels_Top_Comander",
    "Faction_GrandChien_Top_02",
    "Faction_GrandChien_Top_03",
    "Faction_Adonis_Top_01",
]
_FEMALE_HAT = "NPCCostumeFemale_Hat_01"
# Merc-named bottoms/hats that look wrong on AME (esp. Omryn).
_BAD_GEAR_RE = re.compile(r"Omryn|Fauda|Lami", re.I)
_SAFE_MALE_PANTS = [
    "Faction_Militia_Bottom_01",
    "Faction_Rebels_Bottom_01",
    "Faction_GrandChien_Bottom_03",
]


def body_of(block: str) -> str:
    m = re.search(r'Body\s*=\s*"([^"]*)"', block)
    return m.group(1) if m else ""


def is_warpaint_donor(block: str) -> bool:
    return bool(_LEGION_WARPAINT_BODY.match(body_of(block)))


def skin_for_slot(slot: int) -> tuple[int, int, int]:
    return SKIN_BANK[(slot - 1) % len(SKIN_BANK)]


def head_needs_africanize(head: str) -> bool:
    if not head:
        return True
    # Painted Legion war-paint heads — always replace.
    if head.startswith("Faction_Legion_Head_"):
        return True
    if head.startswith("Head_F_Af_NPC_"):
        return False
    if head in MALE_AF_HEADS:
        return False
    if _HEAD_FORCE_REPLACE.match(head):
        return True
    if head.startswith("Faction_") and "Head" in head:
        # Other faction heads (gas masks, Rebel medic, …) — keep unless painted Legion.
        return False
    return True


def african_head_for(slot: int, female: bool) -> str:
    bank = FEMALE_AF_HEADS if female else MALE_AF_HEADS
    return bank[(slot - 1) % len(bank)]


def africanize_head(block: str, slot: int, female: bool) -> tuple[str, str | None]:
    """Swap Caucasian/Asian/AIM heads → African bank. Returns (block, new_head|None)."""
    m = re.search(r'Head\s*=\s*"([^"]+)"', block)
    if not m:
        # Ensure a head exists.
        head = african_head_for(slot, female)
        if re.search(r"^\s*Head\s*=", block, re.M):
            return block, None
        # Insert after Body line if present.
        if re.search(r'Body\s*=\s*"[^"]+"\s*,', block):
            block = re.sub(
                r'(Body\s*=\s*"[^"]+"\s*,)',
                rf'\1\n\tHead = "{head}",',
                block,
                count=1,
            )
            return block, head
        return block, None
    old = m.group(1)
    if not head_needs_africanize(old):
        # Females must always be Af NPC heads (never Vicki/Buns leftovers).
        if female and not old.startswith("Head_F_Af_NPC_"):
            head = african_head_for(slot, True)
            block = re.sub(r'Head\s*=\s*"[^"]+"', f'Head = "{head}"', block, count=1)
            return block, head
        return block, None
    head = african_head_for(slot, female)
    block = re.sub(r'Head\s*=\s*"[^"]+"', f'Head = "{head}"', block, count=1)
    return block, head


def load_roster() -> list[dict]:
    spec = importlib.util.spec_from_file_location("gen_ame_roster_60", ROSTER_SCRIPT)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {ROSTER_SCRIPT}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.ROSTER)


def extract_appearance_blocks(src: str) -> dict[str, str]:
    out: dict[str, str] = {}
    needle = "PlaceObj('AppearancePreset'"
    i = 0
    while True:
        start = src.find(needle, i)
        if start < 0:
            break
        brace = src.find("{", start)
        depth = 0
        j = brace
        while j < len(src):
            c = src[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    # Include trailing ')' of PlaceObj(...).
                    end = j + 1
                    if end < len(src) and src[end] == ")":
                        end += 1
                    block = src[start:end]
                    m = re.search(r'\bid\s*=\s*"([^"]+)"', block)
                    if m:
                        out[m.group(1)] = block
                    i = end
                    break
            j += 1
        else:
            break
    return out


def is_excluded(aid: str) -> bool:
    low = aid.lower()
    if "gasmask" in low or "_test" in low or "infected" in low:
        return True
    if aid.startswith("IMP_") or aid.startswith("Villager"):
        return True
    if aid in ("Faucheux", "GrandChien_Demolition_test"):
        return True
    return False


def classify(aid: str) -> str | None:
    if is_excluded(aid):
        return None
    if aid.startswith("Legion") or aid == "Legionraider":
        return "legion"
    if aid.startswith("Militia"):
        return "militia"
    if (
        aid.endswith("_Rebels")
        or "_Rebels_" in aid
        or aid.startswith("Rebel")
        or aid.endswith("Rebels")
    ):
        return "rebels"
    if aid.startswith("GrandChien"):
        return "grandchien"
    return None


def is_female_id(aid: str) -> bool:
    return "Female" in aid or "female" in aid


def is_red(r: int, g: int, b: int) -> bool:
    if r < 28:
        return False
    if r >= 40 and r > g + 12 and r > b + 12:
        return True
    if r >= 70 and g < 55 and b < 55:
        return True
    return False


def is_ame_blue(r: int, g: int, b: int) -> bool:
    return b >= 90 and b > r + 20 and b >= g


# Muted non-blue replacement for excess Legion red / leftover blues.
SLATE = (34, 38, 44)


def mesh_assigned(block: str, key: str) -> bool:
    m = re.search(rf'{key}\s*=\s*"([^"]*)"', block)
    return bool(m and m.group(1).strip())


def choose_blue_accent(block: str) -> tuple[str, int]:
    """Exactly one blue piece: prefer hat/scarf/shirt/torso — never pants (boots)."""
    if mesh_assigned(block, "Hat"):
        return "HatColor", 1
    if mesh_assigned(block, "Hat2"):
        return "Hat2Color", 1
    if mesh_assigned(block, "Shirt"):
        return "ShirtColor", 1
    body = re.search(r'Body\s*=\s*"([^"]*)"', block)
    if body and body.group(1).startswith("Faction_"):
        return "BodyColor", 2
    if mesh_assigned(block, "Chest"):
        return "ChestColor", 1
    if mesh_assigned(block, "Armor"):
        return "ArmorColor", 1
    # Fallback torso tint (still not pants).
    return "BodyColor", 2


def rgba_replacer(slot: int, part: str, channel: int, accent: tuple[str, int]):
    blue = BLUE_PALETTE[(slot + hash(accent[0]) + accent[1]) % len(BLUE_PALETTE)]
    skin = skin_for_slot(slot)
    accent_part, accent_ch = accent

    def _sub(m: re.Match[str]) -> str:
        r, g, b, a = (int(m.group(i)) for i in range(1, 5))
        if part == "HeadColor":
            return f"RGBA(0, 0, 0, {a})"
        if part == "BodyColor" and channel == 1:
            sr, sg, sb = skin
            return f"RGBA({sr}, {sg}, {sb}, {a})"
        # Single AME-blue accent only.
        if part == accent_part and channel == accent_ch:
            br, bg, bb = blue
            return f"RGBA({br}, {bg}, {bb}, {a})"
        # Never blue the pants/boots stack.
        if part == "PantsColor":
            if is_ame_blue(r, g, b) or is_red(r, g, b):
                sr, sg, sb = SLATE
                return f"RGBA({sr}, {sg}, {sb}, {a})"
            return m.group(0)
        # Other cloth: strip Legion red and any extra blues → slate.
        if part != "HairColor" and (is_red(r, g, b) or is_ame_blue(r, g, b)):
            sr, sg, sb = SLATE
            return f"RGBA({sr}, {sg}, {sb}, {a})"
        return m.group(0)

    return _sub


def recolor_block(block: str, slot: int) -> str:
    """One blue accent; red/extra-blue elsewhere → slate; dark Body C1; HeadColor 0."""
    accent = choose_blue_accent(block)

    def recolor_propset(full: str, part: str) -> str:
        def ch_sub(cm: re.Match[str]) -> str:
            n = int(cm.group(1))
            inner = cm.group(2)
            new_inner = re.sub(
                r"RGBA\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)",
                rgba_replacer(slot, part, n, accent),
                inner,
                count=1,
            )
            return f"'EditableColor{n}', {new_inner}"

        return re.sub(
            r"'EditableColor(\d+)',\s*(RGBA\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\))",
            ch_sub,
            full,
        )

    def prop_sub(m: re.Match[str]) -> str:
        part = m.group(1)
        body = m.group(2)
        return f"{part} = PlaceObj('ColorizationPropSet', {{{recolor_propset(body, part)}}})"

    return re.sub(
        r"(\w+Color)\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{([\s\S]*?)\}\)",
        prop_sub,
        block,
    )


# Bodies whose exposed arms stay pale despite dark BodyColor C1 (player report: Claude).
_PALE_HAND_BODY = {"Faction_GrandChien_Top_05"}


def gender_fix_gear(inner: str, slot: int, female: bool) -> str:
    """Swap Legion war-paint / pale-hand tops, male hats on female kits, Omryn/Fauda/Lami gear."""
    body_m = re.search(r'Body\s*=\s*"([^"]*)"', inner)
    body = body_m.group(1) if body_m else ""
    if not female and body and (
        _LEGION_WARPAINT_BODY.match(body) or body in _PALE_HAND_BODY
    ):
        new_b = _SAFE_MALE_BODY[(slot - 1) % len(_SAFE_MALE_BODY)]
        inner = re.sub(r'Body\s*=\s*"[^"]*"', f'Body = "{new_b}"', inner, count=1)
    hat_m = re.search(r'Hat\s*=\s*"([^"]*)"', inner)
    hat = hat_m.group(1) if hat_m else ""
    if female and hat and ("Male" in hat or hat.startswith("FactionMale")):
        inner = re.sub(r'Hat\s*=\s*"[^"]*"', f'Hat = "{_FEMALE_HAT}"', inner, count=1)
    if hat and _BAD_GEAR_RE.search(hat):
        if female:
            inner = re.sub(r'Hat\s*=\s*"[^"]*"', f'Hat = "{_FEMALE_HAT}"', inner, count=1)
        else:
            # Drop named merc hat — leave empty (optional headwear).
            inner = re.sub(r'Hat\s*=\s*"[^"]*"\s*,?\s*\n', "", inner, count=1)
    pants_m = re.search(r'Pants\s*=\s*"([^"]*)"', inner)
    pants = pants_m.group(1) if pants_m else ""
    if pants and _BAD_GEAR_RE.search(pants):
        new_p = _SAFE_MALE_PANTS[(slot - 1) % len(_SAFE_MALE_PANTS)]
        if female:
            new_p = "Female_Pants_01"
        inner = re.sub(r'Pants\s*=\s*"[^"]*"', f'Pants = "{new_p}"', inner, count=1)
    # Gloves hide arm skin / can read as pale hands — clear so Body C1 shows.
    shirt_m = re.search(r'Shirt\s*=\s*"([^"]*)"', inner)
    shirt = shirt_m.group(1) if shirt_m else ""
    if not female and shirt and re.search(r"Glove", shirt, re.I):
        inner = re.sub(r'Shirt\s*=\s*"[^"]*"', 'Shirt = ""', inner, count=1)
    return inner


def to_moditem(
    block: str, new_id: str, donor: str, slot: int, female: bool = False
) -> tuple[str, str | None]:
    # Strip PlaceObj('AppearancePreset', { ... }) → inner
    m = re.match(r"PlaceObj\('AppearancePreset',\s*\{([\s\S]*)\}\)\s*$", block.strip())
    if not m:
        raise ValueError(f"bad block for donor {donor}")
    inner = m.group(1)
    # Drop original group/id lines.
    inner = re.sub(r"^\s*group\s*=\s*\"[^\"]*\"\s*,?\s*$", "", inner, flags=re.M)
    inner = re.sub(r"^\s*id\s*=\s*\"[^\"]*\"\s*,?\s*$", "", inner, flags=re.M)
    inner, head_swap = africanize_head(inner, slot, female)
    inner = gender_fix_gear(inner, slot, female)
    inner = recolor_block(inner, slot)
    # Normalize leading tabs to two tabs for folder children fields.
    lines = []
    for ln in inner.splitlines():
        if not ln.strip():
            continue
        stripped = ln.lstrip("\t")
        lines.append("\t\t\t" + stripped)
    body = "\n".join(lines)
    # Ensure trailing comma style
    if body and not body.rstrip().endswith(","):
        body = body.rstrip() + ","
    lua = (
        "\t\tPlaceObj('ModItemAppearancePreset', {\n"
        f"{body}\n"
        f'\t\t\tgroup = "AME",\n'
        f'\t\t\tid = "{new_id}",\n'
        "\t\t}),"
    )
    return lua, head_swap


def build_pools(blocks: dict[str, str]) -> dict[str, list[str]]:
    pools: dict[str, list[str]] = {
        "legion_m": [],
        "militia_m": [],
        "rebels_m": [],
        "grandchien_m": [],
        "female": [],
    }
    for aid in sorted(blocks):
        kind = classify(aid)
        if not kind:
            continue
        if is_female_id(aid):
            if kind in ("rebels", "militia", "grandchien"):
                pools["female"].append(aid)
            continue
        key = {
            "legion": "legion_m",
            "militia": "militia_m",
            "rebels": "rebels_m",
            "grandchien": "grandchien_m",
        }[kind]
        pools[key].append(aid)
    return pools


def prefer_for(m: dict) -> list[str]:
    """Ordered pool keys for this merc.

    Prefer Militia/Rebels/GrandChien over Legion. Legion war-paint donors may still
    be taken last; gender_fix_gear swaps Faction_Legion_Top_* → safe tops.
    """
    cat = m.get("cat", "")
    role = m.get("role", "")
    if m.get("female"):
        return ["female"]
    if cat == "Hardened":
        return ["grandchien_m", "rebels_m", "militia_m", "legion_m"]
    if cat == "Specialists":
        if role in ("Instructor", "Medic"):
            return ["grandchien_m", "rebels_m", "militia_m", "legion_m"]
        if role in ("Sniper", "Sapper", "Mechanic"):
            return ["rebels_m", "militia_m", "grandchien_m", "legion_m"]
        return ["rebels_m", "grandchien_m", "militia_m", "legion_m"]
    if cat == "Irregulars":
        return ["militia_m", "rebels_m", "grandchien_m", "legion_m"]
    # Fighters — militia/rebels first (AME blue accent); Legion last.
    if role in ("Machinegunner", "Autorifleman", "Grenadier"):
        return ["militia_m", "rebels_m", "grandchien_m", "legion_m"]
    return ["rebels_m", "militia_m", "grandchien_m", "legion_m"]


def assign_donors(
    roster: list[dict], pools: dict[str, list[str]], blocks: dict[str, str]
) -> list[str]:
    used: set[str] = set()
    bags = {k: list(v) for k, v in pools.items()}
    assigned: list[str] = []

    def take(keys: list[str], allow_reuse: bool) -> str:
        # Prefer unused non-warpaint donors, then any unused, then reuse (females).
        for require_safe in (True, False):
            for k in keys:
                bag = bags[k]
                for i, aid in enumerate(bag):
                    if aid in used:
                        continue
                    if require_safe and is_warpaint_donor(blocks.get(aid, "")):
                        continue
                    used.add(aid)
                    if not allow_reuse:
                        bag.pop(i)
                    return aid
        if allow_reuse:
            for k in keys:
                bag = bags[k]
                if bag:
                    # Prefer non-warpaint on reuse too.
                    safe = [a for a in bag if not is_warpaint_donor(blocks.get(a, ""))]
                    pick = safe if safe else bag
                    aid = pick[len(assigned) % len(pick)]
                    used.add(aid)
                    return aid
        raise RuntimeError(f"no donor for keys={keys}")

    for m in roster:
        female = bool(m.get("female"))
        donor = take(prefer_for(m), allow_reuse=female)
        assigned.append(donor)
    return assigned


def replace_marked(text: str, begin: str, end: str, body: str) -> str:
    block = f"{begin}\n{body}\n{end}"
    if begin in text and end in text:
        return re.sub(
            re.escape(begin) + r".*?" + re.escape(end),
            block,
            text,
            count=1,
            flags=re.S,
        )
    if AME_END in text:
        idx = text.find(AME_END) + len(AME_END)
        return text[:idx] + "\n" + block + "\n" + text[idx:]
    return text.rstrip() + "\n" + block + "\n"


def meta_resources(ids: list[str]) -> str:
    rows = []
    for aid in ids:
        rows.append(
            "\t\tPlaceObj('ModResourcePreset', {\n"
            '\t\t\t\'Class\', "AppearancePreset",\n'
            f'\t\t\t\'Id\', "{aid}",\n'
            '\t\t\t\'ClassDisplayName\', "Appearance preset",\n'
            "\t\t}),"
        )
    return "\n".join(rows)


def upsert_meta(text: str, ids: list[str]) -> str:
    body = meta_resources(ids)
    block = f"{META_BEGIN}\n{body}\n{META_END}"
    if META_BEGIN in text and META_END in text:
        return re.sub(
            re.escape(META_BEGIN) + r".*?" + re.escape(META_END),
            block,
            text,
            count=1,
            flags=re.S,
        )
    # Insert before closing of resources table — find last AppearancePreset resource
    anchor = "'ClassDisplayName', \"Appearance preset\","
    idx = text.rfind(anchor)
    if idx < 0:
        raise SystemExit("metadata AppearancePreset anchor not found")
    # after the PlaceObj closing for that entry
    close = text.find("}),", idx)
    insert_at = close + 3
    return text[:insert_at] + "\n" + block + text[insert_at:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not VANILLA_AP.is_file():
        raise SystemExit(f"missing vanilla AppearancePreset: {VANILLA_AP}")

    roster = load_roster()
    if len(roster) != 60:
        raise SystemExit(f"roster size {len(roster)}")

    blocks = extract_appearance_blocks(VANILLA_AP.read_text(encoding="utf-8"))
    pools = build_pools(blocks)
    warpaint_in_pools = sum(
        1
        for k, ids in pools.items()
        if k != "female"
        for aid in ids
        if is_warpaint_donor(blocks[aid])
    )
    print(
        "pools:",
        {k: len(v) for k, v in pools.items()},
        f"warpaint_donors_in_pools={warpaint_in_pools} (body swapped at emit)",
    )

    donors = assign_donors(roster, pools, blocks)
    unique_male = len({d for d, m in zip(donors, roster) if not m.get("female")})
    unique_female_donors = len({d for d, m in zip(donors, roster) if m.get("female")})
    print(f"assigned unique male donors={unique_male}/50 female donor kinds={unique_female_donors}")

    mapping = []
    mod_blocks = []
    app_ids = []
    head_swaps = 0
    for i, (m, donor) in enumerate(zip(roster, donors), start=1):
        if donor not in blocks:
            raise SystemExit(f"donor missing: {donor}")
        new_id = f"JAZZ_AME_{i:02d}"
        app_ids.append(new_id)
        female = bool(m.get("female"))
        lua, head_swap = to_moditem(blocks[donor], new_id, donor, i, female=female)
        mod_blocks.append(lua)
        if head_swap:
            head_swaps += 1
        mapping.append(
            {
                "slot": i,
                "id": new_id,
                "donor": donor,
                "name": m["name"],
                "cat": m["cat"],
                "female": female,
                "head_swap": head_swap,
            }
        )
    print(f"africanized heads={head_swaps}")

    folder = (
        "\tPlaceObj('ModItemFolder', {\n"
        '\t\t\'name\', "AME_Appearances",\n'
        "\t}, {\n"
        + "\n".join(mod_blocks)
        + "\n\t}),"
    )

    items_text = ITEMS.read_text(encoding="utf-8")
    new_items = replace_marked(items_text, ITEMS_BEGIN, ITEMS_END, folder)
    meta_text = META.read_text(encoding="utf-8")
    new_meta = upsert_meta(meta_text, app_ids)

    print(f"items {len(items_text)} -> {len(new_items)}")
    print(f"meta  {len(meta_text)} -> {len(new_meta)}")
    print(f"map entries={len(mapping)}")

    if args.dry_run:
        print("dry-run: no writes")
        print("sample", mapping[0], mapping[40])
        return 0

    ITEMS.write_text(new_items, encoding="utf-8")
    META.write_text(new_meta, encoding="utf-8")
    MAP_OUT.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {ITEMS}")
    print(f"wrote {META}")
    print(f"wrote {MAP_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
