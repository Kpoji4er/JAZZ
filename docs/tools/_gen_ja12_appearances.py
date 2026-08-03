#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate JA12 Jazz merc AppearancePreset by combining same-gender donors.

JAZZ-UNITS-002 appearance gap: many UnitData point at preset ids (Colby, Blade, …)
that were never shipped. This tool clones a Body donor and swaps Head/Hair/Hat from
same-gender donors — never mix male/female meshes.

Compatibility policy (important):
  - AIM Equipment* kits are **poorly compatible with each other** (unique proportions /
    neck/collar). Prefer: faction/NPC/Thug/Civ **body** + one head donor, OR a pure
    AIM clone (same body+head id). Avoid AIM-body × different-AIM-head mixes.
  - Donors may be AIM, Rebels, Militia, Army/GrandChien, Adonis, Thugs, Civ/NPC.
  - Prefer non–war-paint heads for hireables (named / NPC heads over Legion paint).

Usage (jazz/):
  python docs/tools/_gen_ja12_appearances.py --dry-run
  python docs/tools/_gen_ja12_appearances.py
  python docs/tools/_gen_ja12_appearances.py --only Lynx,Colby,Ira

Does not overwrite KEEP_HANDCRAFTED ids unless --force.
Writes ModItemAppearancePreset into jazz-units/items.lua (+ metadata resources).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

JAZZ = Path(__file__).resolve().parents[2]
JU = JAZZ.parent / "jazz-units"
ITEMS = JU / "items.lua"
META = JU / "metadata.lua"
VANILLA_AP = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Data\AppearancePreset.lua"
)
MAP_OUT = JAZZ / "docs" / "design" / "mercs-ja12" / "ja12-appearance-map.json"

SECTION = "JAZZ-UNITS-002-JA12-APP"
ITEMS_BEGIN = f"-- {SECTION}-BEGIN"
ITEMS_END = f"-- {SECTION}-END"
META_BEGIN = f"\t\t-- {SECTION}-META-BEGIN"
META_END = f"\t\t-- {SECTION}-META-END"

# Handcrafted / already-good presets — skip unless --force.
KEEP_HANDCRAFTED = {
    "Lynx",
    "Buzz",
    "Spider",
    "Mike",
    "Horg",
    "JAZZ_Spouke",
    "Ivanov",
    "Biff",  # vanilla Biff exists
    "Hitman",  # vanilla Hitman exists
    "Shadow",  # Simon UnitData points at vanilla Shadow
    "Simon",  # do not duplicate — keep UnitData → Shadow
}

# preset_id -> recipe
# body: donor id for Body/Pants/Shirt/Chest/Armor/colors (kit)
# head: donor id for Head (+ HeadColor)
# hair: optional donor for Hair (+ HairColor/params); "" = clear hair; None = keep body donor hair
# hat: optional donor for Hat/Hat2; "" = clear hats; None = keep body donor hats
# gender: Male|Female — hard gate
Recipe = dict  # typed loosely

# Visual cues: portraits + docs/design/mercs-ja12/_appearance-sheet.md
# Pool: AIM + Rebels/Militia/Army/Adonis/Thugs/Civ/NPC kits (same-gender only).
# Prefer non-AIM body + head swap; AIM×AIM cross only if handcrafted/accepted.

# Known AIM hireable / named Equipment* presets — cross-mixing these bodies/heads
# is fragile (neck/collar scale). Faction Male_Body / Female_Body kits mix better.
AIM_NAMED = {
    "Barry", "Biff", "Blood", "Buns", "DrQ", "Fauda", "Fidel", "Flay", "Fox",
    "Grizzly", "Gus", "Hitman", "Ice", "Igor", "Ivan", "Kalyna", "Larry", "Len",
    "Livewire", "Magic", "MD", "Meltdown", "Mouse", "Nails", "Omryn", "Raider",
    "Raven", "Reaper", "Red", "Scope", "Shadow", "Sidney", "Steroid", "Tex",
    "Thor", "Vicki", "Wolf",
}


def warn_aim_cross(preset_id: str, recipe: Recipe) -> None:
    body, head = recipe.get("body"), recipe.get("head")
    if body in AIM_NAMED and head in AIM_NAMED and body != head:
        print(
            f"  WARN {preset_id}: AIM×AIM cross body={body} head={head} "
            f"(poor mesh compat — prefer faction/NPC body or same-id clone)"
        )


RECIPES: dict[str, Recipe] = {
    # --- already handcrafted (kept as documentation of intent) ---
    "Lynx": {"gender": "Male", "body": "Fidel", "head": "Ice", "hair": "Ice", "hat": "", "note": "sniper — Fidel + pale Ice (handcrafted)"},
    "Buzz": {"gender": "Female", "body": "Fauda", "head": "Fox", "hair": "Fox", "hat": "", "note": "LMG — Fauda + Fox (handcrafted)"},
    "Spider": {"gender": "Female", "body": "Mouse", "head": "Buns", "hair": "Buns", "hat": "", "note": "medic — Mouse + Buns (handcrafted)"},
    "Mike": {"gender": "Male", "body": "Ice", "head": "Ice", "hair": "Ice", "hat": "", "note": "dark tac — Ice (handcrafted)"},
    "Horg": {"gender": "Male", "body": "Steroid", "head": "Steroid", "hair": "Steroid", "hat": "", "note": "heavy — Steroid (handcrafted)"},
    # --- generated ---
    "Colby": {"gender": "Male", "body": "WorkingGuy01", "head": "Sidney", "hair": "Sidney", "hat": "", "note": "inventor clutter — WorkingGuy + Sidney"},
    "Blade": {"gender": "Male", "body": "ThugMelee", "head": "Reaper", "hair": "Reaper", "hat": "", "note": "knife psycho — ThugMelee + Reaper"},
    "Ira": {"gender": "Female", "body": "RebelFemaleSniper", "head": "Kalyna", "hair": "Kalyna", "hat": "", "note": "young medic rebel — RebelFemale + Kalyna"},
    "Dimitri": {"gender": "Male", "body": "Soldier_Rebels", "head": "Flay", "hair": "Flay", "hat": "", "note": "Greek rebel / machete — Rebels Soldier + Flay"},
    "Madman": {"gender": "Male", "body": "ThugAssault", "head": "Nails", "hair": "Nails", "hat": "", "note": "torn punk — ThugAssault + Nails"},
    "Grom": {"gender": "Male", "body": "GrandChien_Officer", "head": "Igor", "hair": "Igor", "hat": "", "note": "Soviet major — GC Officer + Igor"},
    "Static": {"gender": "Male", "body": "WorkingGuy02", "head": "Thor", "hair": "Thor", "hat": "Thor", "note": "hippie mechanic — WorkingGuy + Thor band"},
    "Highball": {"gender": "Male", "body": "Doctor_01", "head": "Gus", "hair": "Gus", "hat": "", "note": "alcoholic doctor — Doctor NPC + Gus"},
    "Bull": {"gender": "Male", "body": "Bonecrusher", "head": "Steroid", "hair": "", "hat": "", "note": "bald bruiser — Bonecrusher + Steroid bald"},
    "Cord": {"gender": "Male", "body": "WorkingGuy01", "head": "Tex", "hair": "Tex", "hat": "", "note": "grease monkey — WorkingGuy + Tex"},
    "Hobbit": {"gender": "Male", "body": "VillagerMale_05", "head": "Barry", "hair": "Barry", "hat": "", "note": "pudgy messy — Villager + Barry"},
    "Ricochet": {"gender": "Male", "body": "Gangster_01", "head": "Nails", "hair": "Nails", "hat": "", "note": "punk — Gangster + Nails"},
    "Meat": {"gender": "Male", "body": "Bulldozer", "head": "Grizzly", "hair": "Grizzly", "hat": "", "note": "huge / dumb — Bulldozer + Grizzly"},
    "Carlos": {"gender": "Male", "body": "Soldier_Rebels_02", "head": "Flay", "hair": "Flay", "hat": "", "note": "Latino rebel — Rebels + Flay"},
    "Devin": {"gender": "Male", "body": "BillyBoy", "head": "Red", "hair": "Red", "hat": "", "note": "Irish explosives trader — BillyBoy shirt + Red"},
    "Shank": {"gender": "Male", "body": "Gangster_01", "head": "Ice", "hair": "Ice", "hat": "", "note": "exhausted rich kid — Gangster hoodie + Ice"},
    "Vince": {"gender": "Male", "body": "Doctor_02", "head": "Sidney", "hair": "Sidney", "hat": "", "note": "neat civilian doctor — Doctor NPC + Sidney"},
    "Hitman": {"gender": "Male", "body": "Hitman", "head": "Hitman", "hair": "Hitman", "hat": "", "note": "vanilla Hitman (keep if present)"},
    "Biggens": {"gender": "Male", "body": "DirtyHenri", "head": "Gus", "hair": "Gus", "hat": "Gus", "note": "old colonel beret — DirtyHenri militia shirt + Gus"},
    "Kulba": {"gender": "Male", "body": "BillyBoy", "head": "Len", "hair": "Len", "hat": "", "note": "old American civilian — BillyBoy shirt + Len"},
    "Vilde": {"gender": "Male", "body": "Militia_Officer", "head": "Igor", "hair": "Igor", "hat": "", "note": "militarized leader — Militia Officer + Igor"},
    "Grace": {"gender": "Female", "body": "WorkingGirl01", "head": "Livewire", "hair": "Livewire", "hat": "", "note": "jeans / knives — WorkingGirl + Livewire"},
    "Steiger": {"gender": "Male", "body": "Adonis_Soldier", "head": "Shadow", "hair": "Shadow", "hat": "", "note": "GSG-9 — Adonis kit + Shadow"},
    "Lucky": {"gender": "Male", "body": "Militia_Stormer", "head": "Blood", "hair": "Blood", "hat": "", "note": "muscle AR — Militia Stormer + Blood"},
    "Laura": {"gender": "Female", "body": "Nurse_01", "head": "Scope", "hair": "Scope", "hat": "", "note": "coat / med bag — Nurse + Scope"},
    "Eskimo": {"gender": "Male", "body": "Marksman_Rebels", "head": "Omryn", "hair": "Omryn", "hat": "", "note": "northern scout — Rebels Marksman + Omryn"},
    "Rothman": {"gender": "Male", "body": "Adonis_Officer", "head": "Magic", "hair": "Magic", "hat": "", "note": "security commander — Adonis Officer + Magic"},
    "Quinten": {"gender": "Male", "body": "Adonis_Medic", "head": "Blood", "hair": "Blood", "hat": "", "note": "ripped medic — Adonis Medic + Blood"},
    "Allik": {"gender": "Male", "body": "Militia_Soldier", "head": "Igor", "hair": "Igor", "hat": "", "note": "Estonian AR — Militia + Igor"},
    "Henning": {"gender": "Male", "body": "GrandChien_Officer", "head": "Gus", "hair": "Gus", "hat": "", "note": "German officer — GC Officer + Gus"},
    "Conrad": {"gender": "Male", "body": "GrandChien_Soldier", "head": "Len", "hair": "Len", "hat": "", "note": "Arulco LT — GC Soldier + Len"},
    "Flo": {"gender": "Female", "body": "VillagerFemale_08", "head": "Buns", "hair": "Buns", "hat": "", "note": "negotiator civilian — Villager blouse + Buns"},
    "Gaston": {"gender": "Male", "body": "Adonis_Marksman", "head": "Sidney", "hair": "Sidney", "hat": "", "note": "FMC sniper — Adonis Marksman + Sidney"},
    "Cougar": {"gender": "Male", "body": "Militia_Recon", "head": "Shadow", "hair": "Shadow", "hat": "", "note": "stealth MERC — Militia Recon + Shadow"},
    "Monk": {"gender": "Male", "body": "Recon_Rebels", "head": "DrQ", "hair": "DrQ", "hat": "", "note": "camo mystic — Rebels Recon + DrQ"},
    "Manuel": {"gender": "Male", "body": "Recon_Rebels_02", "head": "Tex", "hair": "Tex", "hat": "", "note": "dirty rebel cover — Rebels Recon + Tex"},
    "Gamos": {"gender": "Male", "body": "Poacher_01", "head": "Flay", "hair": "Flay", "hat": "", "note": "stealth hunter — Poacher + Flay"},
    "Dynamo": {"gender": "Male", "body": "Militia_Soldier", "head": "Blood", "hair": "Blood", "hat": "", "note": "beaten mechanic — Militia + Blood"},
    "Nervous": {"gender": "Male", "body": "ThugAssault", "head": "MD", "hair": "MD", "hat": "", "note": "redneck autorifle — Thug + MD"},
    "Miguel": {"gender": "Male", "body": "Commander_Rebels", "head": "Chimurenga", "hair": "Chimurenga", "hat": "Chimurenga", "note": "rebel leader beret — Commander + Chimurenga"},
    "Vicious": {"gender": "Male", "body": "ThugMelee", "head": "Reaper", "hair": "Reaper", "hat": "", "note": "melee mean — ThugMelee + Reaper"},
    "Benny": {"gender": "Female", "body": "WorkingGirl01", "head": "Fox", "hair": "Fox", "hat": "", "note": "female fixer — WorkingGirl + Fox"},
    "Simon": {"gender": "Male", "body": "Shadow", "head": "Shadow", "hair": "Shadow", "hat": "", "note": "stealth — use vanilla Shadow via UnitData"},
    "Ivanov": {"gender": "Male", "body": "Ivan", "head": "Ivan", "hair": "Ivan", "hat": "", "note": "NPC — Ivan"},
    "JAZZ_Spouke": {"gender": "Male", "body": "Raider", "head": "Ice", "hair": "Ice", "hat": "", "note": "keep handcrafted if present"},
}


def extract_blocks(src: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for needle in ("PlaceObj('AppearancePreset'", "PlaceObj('ModItemAppearancePreset'"):
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


def field(block: str, key: str) -> str:
    m = re.search(rf'{key}\s*=\s*"([^"]*)"', block)
    return m.group(1) if m else ""


def gender_of_mesh(name: str) -> str | None:
    n = name or ""
    if not n:
        return None
    if re.search(
        r"(?i)(_F_|Female|Buns|Fox|Vicki|Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|"
        r"Fauda|Corazon|Emma|DrMangel|IMP_Female|Imp_Female|Head_F_)",
        n,
    ):
        return "Female"
    if re.search(
        r"(?i)(_M_|Male_|IMP_Male|Imp_Male|Head_M_|Faction_.*Male|Equipment(?!Buns|Fox|Vicki|Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|Fauda))",
        n,
    ):
        # EquipmentX_Top for male AIM mercs
        if re.search(
            r"(?i)Equipment(Buns|Fox|Vicki|Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|Fauda|Corazon)",
            n,
        ):
            return "Female"
        return "Male"
    # Named male heads
    if n.startswith("Head_") and n not in {
        "Head_Buns",
        "Head_Fox",
        "Head_Vicki",
        "Head_Meltdown",
        "Head_Mouse",
        "Head_Livewire",
        "Head_Kalyna",
        "Head_Raven",
        "Head_Scope",
        "Head_Fauda",
        "Head_Corazon",
        "Head_Emma",
        "Head_Faucheux",  # male
    }:
        if n.startswith("Head_F_"):
            return "Female"
        return "Male"
    if n.startswith("Male_Head"):
        return "Male"
    if n.startswith("Female_") or n.startswith("Female_Body"):
        return "Female"
    return None


def assert_gender_lock(body: str, head: str, expect: str, preset_id: str) -> None:
    bg = gender_of_mesh(body)
    hg = gender_of_mesh(head)
    if bg and bg != expect:
        raise SystemExit(f"{preset_id}: Body {body} gender={bg} != {expect}")
    if hg and hg != expect:
        raise SystemExit(f"{preset_id}: Head {head} gender={hg} != {expect}")
    if bg and hg and bg != hg:
        raise SystemExit(f"{preset_id}: mixed Body/Head gender {body}/{head}")


def replace_field(block: str, key: str, value: str | None) -> str:
    """Set key=\"value\" or remove key line if value is None/empty-clear."""
    pat = rf"(?m)^\s*{key}\s*=\s*\"[^\"]*\"\s*,?\s*\n"
    if value is None:
        return block
    if value == "":
        return re.sub(pat, "", block)
    if re.search(rf"{key}\s*=", block):
        return re.sub(rf'{key}\s*=\s*"[^"]*"', f'{key} = "{value}"', block, count=1)
    # insert after Body line
    return re.sub(
        r'(Body\s*=\s*"[^"]+"\s*,)',
        rf'\1\n\t\t\t{key} = "{value}",',
        block,
        count=1,
    )


def copy_propset(dst: str, src: str, key: str) -> str:
    """Copy `key = PlaceObj('ColorizationPropSet', {...})` from src into dst."""
    m = re.search(
        rf"{key}\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{{[\s\S]*?\}}\)\s*,?",
        src,
    )
    if not m:
        return dst
    chunk = m.group(0).rstrip().rstrip(",") + ","
    if re.search(rf"{key}\s*=\s*PlaceObj\('ColorizationPropSet'", dst):
        return re.sub(
            rf"{key}\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{{[\s\S]*?\}}\)\s*,?",
            chunk,
            dst,
            count=1,
        )
    return re.sub(
        r'(Body\s*=\s*"[^"]+"\s*,)',
        rf"\1\n\t\t\t{chunk}",
        dst,
        count=1,
    )


def copy_simple_num(dst: str, src: str, key: str) -> str:
    m = re.search(rf"{key}\s*=\s*([-\d.]+)\s*,", src)
    if not m:
        return dst
    val = m.group(1)
    if re.search(rf"{key}\s*=", dst):
        return re.sub(rf"{key}\s*=\s*[-\d.]+", f"{key} = {val}", dst, count=1)
    return dst


def to_moditem(block: str, preset_id: str, group: str = "JAZZ_JA12") -> str:
    """Format as folder child ModItemAppearancePreset (same indent as AME-APP)."""
    m = re.match(
        r"PlaceObj\('(?:AppearancePreset|ModItemAppearancePreset)',\s*\{([\s\S]*)\}\)\s*,?\s*$",
        block.strip(),
    )
    if not m:
        raise SystemExit(f"{preset_id}: cannot parse AppearancePreset block")
    inner = m.group(1)
    inner = re.sub(r"^\s*group\s*=\s*\"[^\"]*\"\s*,?\s*$", "", inner, flags=re.M)
    inner = re.sub(r"^\s*id\s*=\s*\"[^\"]*\"\s*,?\s*$", "", inner, flags=re.M)
    # NPC generic heads: keep HeadColor black (avoid chalk).
    if re.search(r'Head\s*=\s*"(Head_M_|Male_Head_|Head_F_)', inner):
        inner = re.sub(
            r"(HeadColor\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{)([\s\S]*?)(\}\))",
            r"\1\n\t\t\t\t'EditableColor1', RGBA(0, 0, 0, 255),\n"
            r"\t\t\t\t'EditableColor2', RGBA(0, 0, 0, 255),\n"
            r"\t\t\t\t'EditableColor3', RGBA(0, 0, 0, 255),\n\t\t\t\3",
            inner,
            count=1,
        )
    lines = []
    for ln in inner.splitlines():
        if not ln.strip():
            continue
        lines.append("\t\t\t" + ln.lstrip("\t"))
    body = "\n".join(lines)
    if body and not body.rstrip().endswith(","):
        body = body.rstrip() + ","
    return (
        "\t\tPlaceObj('ModItemAppearancePreset', {\n"
        f"{body}\n"
        f'\t\t\tgroup = "{group}",\n'
        f'\t\t\tid = "{preset_id}",\n'
        "\t\t}),"
    )


def build_combined(blocks: dict[str, str], preset_id: str, recipe: Recipe) -> str:
    gender = recipe["gender"]
    body_id = recipe["body"]
    head_id = recipe["head"]
    if body_id not in blocks:
        raise SystemExit(f"{preset_id}: body donor missing: {body_id}")
    if head_id not in blocks:
        raise SystemExit(f"{preset_id}: head donor missing: {head_id}")
    body_b = blocks[body_id]
    head_b = blocks[head_id]
    body_mesh = field(body_b, "Body")
    head_mesh = field(head_b, "Head")
    assert_gender_lock(body_mesh, head_mesh, gender, preset_id)

    out = body_b
    out = replace_field(out, "Head", head_mesh)
    out = copy_propset(out, head_b, "HeadColor")

    hair_spec = recipe.get("hair", None)
    if hair_spec == "":
        out = replace_field(out, "Hair", "")
    elif isinstance(hair_spec, str):
        hb = blocks.get(hair_spec, head_b)
        hair = field(hb, "Hair")
        out = replace_field(out, "Hair", hair if hair else "")
        if hair:
            out = copy_propset(out, hb, "HairColor")
            for p in ("HairParam1", "HairParam2", "HairParam3"):
                out = copy_simple_num(out, hb, p)

    hat_spec = recipe.get("hat", None)
    if hat_spec == "":
        out = replace_field(out, "Hat", "")
        out = replace_field(out, "Hat2", "")
    elif isinstance(hat_spec, str):
        ht = blocks.get(hat_spec, body_b)
        hat = field(ht, "Hat")
        hat2 = field(ht, "Hat2")
        out = replace_field(out, "Hat", hat if hat else "")
        out = replace_field(out, "Hat2", hat2 if hat2 else "")
        if hat:
            out = copy_propset(out, ht, "HatColor")

    return to_moditem(out, preset_id)


def replace_marked(text: str, begin: str, end: str, payload: str) -> str:
    block = f"{begin}\n{payload}\n{end}"
    if begin in text and end in text:
        return re.sub(
            re.escape(begin) + r"[\s\S]*?" + re.escape(end),
            block,
            text,
            count=1,
        )
    # Prefer insert just before AME appearances (same root level).
    anchor = "-- JAZZ-UNITS-005-AME-APP-BEGIN"
    if anchor in text:
        return text.replace(anchor, block + "\n\n" + anchor, 1)
    raise SystemExit("cannot find insert anchor for JA12 appearances")


def upsert_meta_resources(meta: str, ids: list[str]) -> str:
    lines = [
        f"\t\t{META_BEGIN}",
        *[
            "\t\tPlaceObj('ModResourcePreset', {\n"
            f"\t\t\t'Class', \"AppearancePreset\",\n"
            f"\t\t\t'Id', \"{i}\",\n"
            f"\t\t\t'ClassDisplayName', \"Appearance\",\n"
            "\t\t}),"
            for i in ids
        ],
        f"\t\t{META_END}",
    ]
    payload = "\n".join(lines)
    if META_BEGIN in meta and META_END in meta:
        return re.sub(
            re.escape(META_BEGIN) + r"[\s\S]*?" + re.escape(META_END),
            payload,
            meta,
            count=1,
        )
    # insert near end of resources / before code hash noise — after AME-APP meta if any
    ame = "-- JAZZ-UNITS-005-AME-APP-META-BEGIN"
    if ame in meta:
        return meta.replace(ame, payload + "\n\t\t" + ame, 1)
    # append before final `})` of ModDef — find last PlaceObj ModResourcePreset block end is hard;
    # insert after ignore_files closing is wrong. Put before 'code' array.
    if "\t'code', {" in meta:
        return meta.replace("\t'code', {", payload + "\n\t'code', {", 1)
    raise SystemExit("cannot insert metadata resources")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite KEEP_HANDCRAFTED")
    ap.add_argument("--only", default="", help="comma preset ids")
    args = ap.parse_args()

    only = {x.strip() for x in args.only.split(",") if x.strip()}
    vanilla = VANILLA_AP.read_text(encoding="utf-8")
    items = ITEMS.read_text(encoding="utf-8")
    blocks = extract_blocks(vanilla)
    blocks.update(extract_blocks(items))

    # Spike exists?
    if "Spike" not in blocks and "Nails" in blocks:
        pass

    built: list[tuple[str, str, dict]] = []
    skipped = []
    for preset_id, recipe in sorted(RECIPES.items()):
        if only and preset_id not in only:
            continue
        warn_aim_cross(preset_id, recipe)
        if preset_id in KEEP_HANDCRAFTED and not args.force:
            # still document
            skipped.append(preset_id)
            continue
        # Ricochet recipe had a hack — fix Spike donor
        if recipe.get("head") == "Spike" or (
            preset_id == "Ricochet" and "Spike" not in blocks
        ):
            recipe = dict(recipe)
            recipe["head"] = "Nails"
            recipe["hair"] = "Nails"
        try:
            moditem = build_combined(blocks, preset_id, recipe)
        except SystemExit as e:
            print("FAIL", e)
            raise
        built.append((preset_id, moditem, recipe))

    print(f"build={len(built)} skip_handcrafted={skipped}")
    for pid, _, r in built:
        print(
            f"  {pid}: {r['gender']} body={r['body']} head={r['head']} "
            f"hair={r.get('hair')} hat={r.get('hat')!r} — {r.get('note','')}"
        )

    if args.dry_run:
        return

    folder = (
        "\tPlaceObj('ModItemFolder', {\n"
        '\t\t\'name\', "JA12_Appearances",\n'
        '\t\t\'comment\', "JAZZ-UNITS-002 same-gender mixes (AIM/Rebels/Militia/Army/Thugs/Civ)",\n'
        "\t}, {\n"
        + "\n".join(m for _, m, _ in built)
        + "\n\t}),"
    )
    new_items = replace_marked(items, ITEMS_BEGIN, ITEMS_END, folder)
    meta = META.read_text(encoding="utf-8")
    new_meta = upsert_meta_resources(meta, [p for p, _, _ in built])

    map_data = {
        pid: {
            "gender": r["gender"],
            "body_donor": r["body"],
            "head_donor": r["head"],
            "hair_donor": r.get("hair"),
            "hat_donor": r.get("hat"),
            "note": r.get("note", ""),
            "handcrafted_kept": False,
        }
        for pid, _, r in built
    }
    for pid in skipped:
        map_data[pid] = {
            "gender": RECIPES[pid]["gender"],
            "handcrafted_kept": True,
            "note": RECIPES[pid].get("note", ""),
        }

    ITEMS.write_text(new_items, encoding="utf-8")
    META.write_text(new_meta, encoding="utf-8")
    MAP_OUT.write_text(json.dumps(map_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", ITEMS)
    print("wrote", META)
    print("wrote", MAP_OUT)


if __name__ == "__main__":
    main()
