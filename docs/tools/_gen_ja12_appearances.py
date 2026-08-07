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
  - Live gotchas (under-hat hair, skin mismatch, Steroid×Adonis clip, recolors):
    docs/design/mercs-ja12/_appearance-preset-rules.md § Gotchas

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

# Skip unless --force. Never auto-overwrite these ModItems / vanilla shared IDs.
# Handcrafted live outside JA12-APP folder; Biff→vanilla AIM.
# Hitman/Simon get own JA12 mixes — do NOT alias UnitData to flashy AIM kits.
KEEP_HANDCRAFTED = {
    "Lynx",
    "Buzz",
    "Spider",
    "JAZZ_Spouke",
    "Ivanov",
    "Biff",
    "Shadow",
}

# preset_id -> recipe
# body: donor id for Body/Pants/Shirt/Chest/Armor/colors (kit)
# head: donor id for Head (+ HeadColor)
# hair: optional donor for Hair (+ HairColor/params); "" = clear hair; None = keep body donor hair
# hat: optional donor for Hat/Hat2; "" = clear hats; None = keep body donor hats
# gender: Male|Female — hard gate
Recipe = dict  # typed loosely

# Visual cues: MercPortraits/*_Big.png + docs/design/mercs-ja12/_appearance-sheet.md
# Pool: AIM + Rebels/Militia/Army/Adonis/Thugs/Civ/NPC kits (same-gender only).
# Prefer non-AIM body + head swap; AIM×AIM cross only if pure clone or accepted.

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


# 2026-08-05 rebuild: match MercPortraits/<id>_Big.png clothing as closely as
# same-gender donor kits allow. Avoid Gangster_01 (incomplete). Clear WorkingGuy
# sunglasses hats unless portrait has eyewear as hat.
RECIPES: dict[str, Recipe] = {
    # --- handcrafted (KEEP; recipe = intent only, not generated) ---
    "Lynx": {
        "gender": "Male",
        "body": "Fidel",
        "head": "Ice",
        "hair": "Ice",
        "hat": "",
        "note": "handcrafted — do not generate",
    },
    "Buzz": {
        "gender": "Female",
        "body": "Fauda",
        "head": "Fox",
        "hair": "Fox",
        "hat": "",
        "note": "handcrafted — do not generate",
    },
    "Spider": {
        "gender": "Female",
        "body": "Mouse",
        "head": "Buns",
        "hair": "Buns",
        "hat": "",
        "note": "handcrafted — do not generate",
    },
    "JAZZ_Spouke": {
        "gender": "Male",
        "body": "Raider",
        "head": "Ice",
        "hair": "Ice",
        "hat": "",
        "note": "handcrafted — do not generate",
    },
    # --- generated (BigPortrait pass) ---
    "Mike": {
        "gender": "Male",
        "body": "Adonis_Officer",
        "head": "Raider",
        "hair": "Raider",
        "hat": "",
        "body_color1": (22, 22, 24),
        "body_color2": (18, 18, 20),
        "body_color3": (12, 12, 14),
        "pants_color": (20, 20, 22),
        "note": "BigPortrait: all-black plate carrier — Adonis Officer + Raider; forced black Body/Pants (donor is olive/grey)",
    },
    "Horg": {
        "gender": "Male",
        "body": "Adonis_Heavy",
        "head": "Hitman",
        "hair": "Hitman",
        "hat": "",
        "hat_mesh": "EquipmentFidel_Cigar",
        "note": "sheet: LT cigar + flak — Adonis_Heavy + Hitman head + Fidel cigar (was Bonecrusher dark torso + pale Hitman)",
    },
    "Colby": {
        "gender": "Male",
        "body": "Barry",
        "head": "Abraham",
        "hair": "Abraham",
        "hat": "",
        "note": "sheet: gadgets in pockets / inventor — Barry tool-vest body + Abraham light head/wavy dark hair; avoids a pure Barry hireable clone",
    },
    "Blade": {
        "gender": "Male",
        "body": "GrandChien_Recon",
        "head": "Reaper",
        "hair": "Reaper",
        "hat": "",
        "note": "sheet: knife fighter harness — GrandChien_Recon + Reaper head (was ThugMelee Male_Body dark-arms + pale Reaper)",
    },
    "Ira": {
        "gender": "Female",
        "body": "Livewire",
        "head": "Fox",
        "hair": "Fox",
        "hat": "",
        "chest": "Adonis_Medic",
        "hip": "Adonis_Medic",
        "note": "sheet: militia instructor — Livewire body + Fox + Adonis medic (was RebelFemale+pale BC1 → white arms like Flo; was Mollie dress)",
    },
    "Dimitri": {
        "gender": "Male",
        "body": "Soldier_Rebels_03",
        "head": "Blood",
        "hair": "Blood",
        "hat": "",
        "pants_color": (55, 68, 40),
        "note": "olive/camo knife rebel — Soldier_Rebels_03 + Blood (Militia_Top_02 has pale baked arms; BodyColor olive does not fix skin)",
    },
    "Madman": {
        "gender": "Male",
        "body": "ThugAssault",
        "head": "Nails",
        "hair": "",
        "hat": "",
        "note": "sheet: torn tee / psycho — ThugAssault + Nails face; Hair cleared (EquipmentNails_Hair needs headband or clips through face)",
    },
    "Grom": {
        "gender": "Male",
        "body": "Igor",
        "head": "Hitman",
        "hair": "Hitman",
        "hat": "",
        "note": "BigPortrait/JA2: telnyashka + thick mustache — Igor body; Head/Hair=Hitman (Head_Igor is clean-shaven in JA3)",
    },
    "Static": {
        "gender": "Male",
        "body": "GreasyBasil",
        "head": "Thor",
        "hair": "Thor",
        "hat": "GreasyBasil",
        "body_color1": (185, 150, 120),
        "note": "hippie mechanic — GreasyBasil tee/pants + welder hat + Thor head/hair (not Thor AIM clone; C1 pale skin for Thor; was pure Thor / WorkingGuy02)",
    },
    "Highball": {
        "gender": "Male",
        "body": "Doctor_01",
        "head": "DrQ",
        "hair": "DrQ",
        "hat": "",
        "chest": "Adonis_Medic",
        "hip": "Adonis_Medic",
        "pants_color": (102, 68, 38),
        "note": "sheet: alcoholic doctor — Doctor_01 + DrQ + Adonis medic Chest/Hip; PantsColor brown (was white mud Pants_04)",
    },
    "Bull": {
        "gender": "Male",
        "body": "Steroid",
        "head": "Steroid",
        "hair": "",
        "hat": "",
        "pants": "Bonecrusher",
        "note": "sheet: white bald bruiser — Steroid pale body+head, Hair cleared; Bonecrusher black cargos (not dark Bonecrusher torso; not bare Steroid clone)",
    },
    "Cord": {
        "gender": "Male",
        "body": "Mario",
        "head": "Sidney",
        "hair": "Sidney",
        "hat": "",
        "body_color1": (185, 150, 120),
        "body_color2": (88, 78, 48),
        "pants_color": (72, 62, 40),
        "note": "grease coveralls — Mario + Sidney; C1=pale skin (Mario C1 is skin, was near-black; do not put olive on C1), C2=dirty khaki overalls",
    },
    "Hobbit": {
        "gender": "Male",
        "body": "Larry_Addicted",
        "head": "Larry",
        "hair": "Larry",
        "hat": "",
        "note": "sheet: pudgy, dirty demolitions slob — Larry_Addicted torn bomb harness + Larry head/hair, football helmet cleared; no Colby clone",
    },
    "Ricochet": {
        "gender": "Male",
        "body": "Nails",
        "head": "Nails",
        "hair": "Nails",
        "hat": "Nails",
        "note": "BigPortrait: biker vest mohawk tattoos — pure Nails (keep headband; Nails hair clips without it)",
    },
    "Meat": {
        "gender": "Male",
        "body": "Grizzly",
        "head": "Grizzly",
        "hair": "Raider",
        "hat": "",
        "note": "BigPortrait/sheet: pale fat bruiser — pure Grizzly body+head (was Bulldozer dark torso); Hair=Raider (Grizzly hair is under-beret)",
    },
    "Carlos": {
        "gender": "Male",
        "body": "Soldier_Rebels_02",
        "head": "Blood",
        "hair": "Blood",
        "hat": "",
        "note": "Arulco rebel scout — Rebels body + Blood head/hair (was Tex = JA3 Asian face; Hair empty)",
    },
    "Devin": {
        "gender": "Male",
        "body": "Adonis_Demolition",
        "head": "Red",
        "hair": "Red",
        "hat": "Red",
        "note": "sheet: Irish demo redhead — Adonis_Demolition + Red head/beret (not pure Red AIM clone; was BillyBoy)",
    },
    "Shank": {
        "gender": "Male",
        "body": "BillyBoy",
        "head": "Scully",
        "hair": "Scully",
        "hat": "",
        "note": "BigPortrait: charcoal civilian + pale exhausted blonde — BillyBoy black tee/jeans + Scully head/hair",
    },
    "Vince": {
        "gender": "Male",
        "body": "Doctor_02",
        "head": "MD",
        "hair": "MD",
        "hat": "",
        "pants_color": (102, 68, 38),
        "note": "BigPortrait: white lab coat + brown chinos — Doctor + MD; PantsColor brown",
    },
    "Hitman": {
        "gender": "Male",
        "body": "Ice",
        "head": "Hitman",
        "hair": "Hitman",
        "hat": "",
        "note": "sheet/portrait: inconspicuous jacket/hoodie — Ice jacket + Hitman face (was alias vanilla pink Hitman kit)",
    },
    "Biggens": {
        "gender": "Male",
        "body": "DirtyHenri",
        "head": "Gus",
        "hair": "Gus",
        "hat": "Adonis_Officer",
        "hat_color": (140, 120, 70),
        "note": "BigPortrait: khaki beret — DirtyHenri + Gus head + Adonis_Officer beret; HatColor khaki",
    },
    "Kulba": {
        "gender": "Male",
        "body": "Gus",
        "head": "Gus",
        "hair": "Gus",
        "hat": "",
        "note": "portrait: elderly gunsmith — pure Gus (was WorkingGuy01 pink/red + Gus → dark-arms bald mess)",
    },
    "Vilde": {
        "gender": "Male",
        "body": "Adonis_Soldier",
        "head": "MD",
        "hair": "MD",
        "hat": "",
        "body_color2": (82, 64, 44),
        "pants_color": (82, 64, 44),
        "note": "young Estonian autorifleman — Adonis_Soldier + MD young head/mid-part hair; separates him from Cougar; fabric slightly browner",
    },
    "Grace": {
        "gender": "Female",
        "body": "Meltdown",
        "head": "Fox",
        "hair": "Meltdown",
        "hat": "",
        "note": "Meltdown jacket/jeans + Fox head + Meltdown dark bob (JA2 mahogany bob; not Buns platinum crown braid / not full Meltdown AIM clone)",
    },
    "Steiger": {
        "gender": "Male",
        "body": "Adonis_Soldier",
        "head": "Red",
        "hair": "Red",
        "hat": "",
        "note": "BigPortrait: olive chest rig auburn beard — Adonis + Red",
    },
    "Lucky": {
        "gender": "Male",
        "body": "Commander_Rebels",
        "head": "Blood",
        "hair": "Blood",
        "hat": "",
        "note": "BigPortrait: full OD chest rig — Commander Rebels + Blood",
    },
    "Laura": {
        "gender": "Female",
        "body": "IMP_Female_02",
        "head": "Raven",
        "hair": "WorkingGirl04",
        "hat": "",
        "chest": "Adonis_Medic",
        "hip": "Adonis_Medic",
        "note": "Roma field doctor — IMP troubleshooter jacket/cargos + Raven head + WorkingGirl04 long dark hair + Adonis medic; no Benny/Livewire clone",
    },
    "Eskimo": {
        "gender": "Male",
        "body": "Marksman_Rebels",
        "head": "Omryn",
        "hair": "Omryn",
        "hat": "",
        "note": "BigPortrait: tan jacket scarf — Marksman Rebels + Omryn",
    },
    "Rothman": {
        "gender": "Male",
        "body": "Sidney",
        "head": "Len",
        "hair": "Len",
        "hat": "",
        "pants": "LuckiVernard",
        "pants_color": (102, 68, 38),
        "note": "mine security — Sidney top (shoulder holster, not blue Veinard bomber) + Len head + NPC pants brown",
    },
    "Quinten": {
        "gender": "Male",
        "body": "Steroid",
        "head": "Steroid",
        "hair": "Steroid",
        "hat": "",
        "chest": "Adonis_Medic",
        "hip": "Adonis_Medic",
        "note": "BigPortrait: muscular medic — Steroid body (Adonis_Top+Steroid head clipped collar) + Adonis medic Chest/Hip",
    },
    "Allik": {
        "gender": "Male",
        "body": "DirtyHenri",
        "head": "Sidney",
        "hair": "Sidney",
        "hat": "",
        "pants_color": (102, 68, 38),
        "body_color1": (185, 150, 120),
        "note": "heavy-weapons bear — DirtyHenri + Sidney; C1=pale skin (shirt C1 is skin; donor brown mismatched pale Sidney); PantsColor brown",
    },
    "Henning": {
        "gender": "Male",
        "body": "Reaper",
        "head": "Hitman",
        "hair": "Hitman",
        "hat": "Adonis_Officer",
        "hat_color": (28, 28, 28),
        "note": "sheet: black shirt/pants + beret — Reaper dark kit + Hitman face + black Adonis beret (was Adonis_Soldier military; Gus hat empty)",
    },
    "Conrad": {
        "gender": "Male",
        "body": "Adonis_Officer",
        "head": "Len",
        "hair": "Len",
        "hat": "",
        "body_color1": (185, 150, 120),
        "body_color2": (62, 72, 40),
        "body_color3": (40, 46, 28),
        "pants_color": (55, 64, 38),
        "note": "German ex-officer olive plate — Adonis_Officer + Len; C1=pale skin (Top_05 C1 is SKIN — olive on C1 = green hands), C2/C3/pants=olive plate",
    },
    "Flo": {
        "gender": "Female",
        "body": "Livewire",
        "head": "Buns",
        "hair": "Buns",
        "hat": "",
        "note": "sheet: civilian-tactical — Livewire body + Buns (was RebelFemale+BC1 pale → white broken arms; not WorkingGirl Mollie)",
    },
    "Gaston": {
        "gender": "Male",
        "body": "Adonis_Marksman",
        "head": "Gus",
        "hair": "Gus",
        "hat": "",
        "note": "BigPortrait: black plate carrier grey hair — Adonis Marksman + Gus",
    },
    "Cougar": {
        "gender": "Male",
        "body": "Adonis_Heavy",
        "head": "Scully",
        "hair": "Scully",
        "hat": "",
        "note": "MERC veteran autorifleman — Adonis_Heavy vest + Scully mature light head/hair; no Vilde recipe clone",
    },
    "Monk": {
        "gender": "Male",
        "body": "Sample_Horatio",
        "head": "GrandChien_Recon",
        "hair": "Raider",
        "hat": "",
        "note": "BigPortrait: charcoal suit + camo face + short dark hair — Sample_Horatio + Camo head + Raider hair",
    },
    "Manuel": {
        "gender": "Male",
        "body": "Commander_Rebels",
        "head": "Chimurenga",
        "hair": "Raider",
        "hat": "",
        "note": "BigPortrait: olive field open shirt — Commander Rebels + Chimurenga; Hair=Raider (Chimurenga hair is under-helmet / bald crown)",
    },
    "Gamos": {
        "gender": "Male",
        "body": "Poacher_01",
        "head": "Blood",
        "hair": "Blood",
        "hat": "",
        "shirt_color": (176, 88, 32),
        "pants_color": (110, 78, 42),
        "note": "Arulco traveler burnt-orange — Poacher + Blood head (was Tex Asian/empty hair); ShirtColor orange + brown pants",
    },
    "Dynamo": {
        "gender": "Male",
        "body": "DirtyHenri",
        "head": "Blood",
        "hair": "Blood",
        "hat": "",
        "body_color1": (28, 14, 8),
        "note": "beaten torn shirt dark skin — DirtyHenri + Blood; C1 dark skin (shirt C1 is skin channel)",
    },
    "Nervous": {
        "gender": "Male",
        "body": "Tex",
        "head": "Tex",
        "hair": "Tex",
        "hat": "",
        "note": "BigPortrait: denim tattoos — pure Tex (was WorkingGuy01 pink + Tex)",
    },
    "Miguel": {
        "gender": "Male",
        "body": "Commander_Rebels",
        "head": "Chimurenga",
        "hair": "Chimurenga",
        "hat": "Chimurenga",
        "note": "BigPortrait: maroon beret gold star — Commander + Chimurenga",
    },
    "Vicious": {
        "gender": "Male",
        "body": "Ivan",
        "head": "Ivan",
        "hair": "",
        "hat": "",
        "chest": "GrandChien_Recon",
        "note": "sheet: bomber + big knife + gloves — Ivan leather jacket (no ushanka) + Recon knife chest; was ThugMelee dark-arms + Hitman mustache/cream shirt",
    },
    "Benny": {
        "gender": "Female",
        "body": "IMP_Female_01",
        "head": "Fox",
        "hair": "Fox",
        "hat": "",
        "note": "BigPortrait: tactical fixer vest/cargos — IMP trooper body + Fox short dark head/hair; male field cap cleared; no Laura/Livewire clone",
    },
    "Simon": {
        "gender": "Male",
        "body": "DirtyHenri",
        "head": "Len",
        "hair": "Len",
        "hat": "Grunty",
        "pants": "Adonis_Soldier",
        "chest": "Adonis_Artillery",
        "body_color1": (185, 150, 120),
        "note": "BigPortrait: field jacket, glasses, goatee, binoculars — DirtyHenri + Len + Grunty glasses + Adonis pants/chest; own preset, not Shadow",
    },
    "Ivanov": {
        "gender": "Male",
        "body": "Ivan",
        "head": "Ivan",
        "hair": "Ivan",
        "hat": "",
        "note": "NPC — keep jazz-units Ivanov handcraft",
    },
    "Biff": {
        "gender": "Male",
        "body": "Biff",
        "head": "Biff",
        "hair": "Biff",
        "hat": "",
        "note": "UnitData → vanilla Biff",
    },
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
        r"Fauda|Corazon|Emma|DrMangel|IMPTrooper|IMPTroublemaker|"
        r"IMP_Female|Imp_Female|Head_F_)",
        n,
    ):
        return "Female"
    if re.search(
        r"(?i)(_M_|Male_|IMP_Male|Imp_Male|Head_M_|Faction_.*Male|"
        r"Equipment(?!Buns|Fox|Vicki|Meltdown|Mouse|Livewire|Kalyna|Raven|Scope|"
        r"Fauda|IMPTrooper|IMPTroublemaker))",
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


def set_propset_color(block: str, key: str, rgb: tuple[int, int, int], channel: int = 1) -> str:
    """Set EditableColor{channel} inside `key = PlaceObj('ColorizationPropSet', ...)`."""
    r, g, b = rgb
    pat = (
        rf"({key}\s*=\s*PlaceObj\('ColorizationPropSet',\s*\{{[\s\S]*?"
        rf"'EditableColor{channel}',\s*)RGBA\(\d+,\s*\d+,\s*\d+,\s*\d+\)"
    )
    repl = rf"\1RGBA({r}, {g}, {b}, 255)"
    new, n = re.subn(pat, repl, block, count=1)
    return new if n else block


def set_propset_color1(block: str, key: str, rgb: tuple[int, int, int]) -> str:
    return set_propset_color(block, key, rgb, 1)


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
    if recipe.get("hat2") == "":
        out = replace_field(out, "Hat2", "")
    hat_mesh = recipe.get("hat_mesh")
    if isinstance(hat_mesh, str):
        out = replace_field(out, "Hat", hat_mesh)

    # Optional gear graft (Chest/Hip/Armor/Pants) from another preset — same-gender body already locked.
    for slot, recipe_key in (("Chest", "chest"), ("Hip", "hip"), ("Armor", "armor"), ("Pants", "pants")):
        gear_id = recipe.get(recipe_key)
        if not isinstance(gear_id, str) or not gear_id:
            continue
        if gear_id not in blocks:
            raise SystemExit(f"{preset_id}: {recipe_key} donor missing: {gear_id}")
        gb = blocks[gear_id]
        mesh = field(gb, slot)
        if mesh:
            out = replace_field(out, slot, mesh)
            out = copy_propset(out, gb, f"{slot}Color")

    if recipe.get("pants_color"):
        out = set_propset_color1(out, "PantsColor", recipe["pants_color"])
    if recipe.get("shirt_color"):
        out = set_propset_color1(out, "ShirtColor", recipe["shirt_color"])
    if recipe.get("hat_color"):
        out = set_propset_color1(out, "HatColor", recipe["hat_color"])
    if recipe.get("body_color2"):
        out = set_propset_color(out, "BodyColor", recipe["body_color2"], 2)
    if recipe.get("body_color1"):
        out = set_propset_color(out, "BodyColor", recipe["body_color1"], 1)
    if recipe.get("body_color3"):
        out = set_propset_color(out, "BodyColor", recipe["body_color3"], 3)

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

    if only and ITEMS_BEGIN in items and ITEMS_END in items:
        # Merge into existing JA12 folder — never wipe siblings when --only is set.
        old_sec = items.split(ITEMS_BEGIN)[1].split(ITEMS_END)[0]
        existing = extract_blocks(old_sec)
        built_map = {pid: moditem for pid, moditem, _ in built}
        ordered_ids: list[str] = []
        for m in re.finditer(r"\bid\s*=\s*\"([^\"]+)\"", old_sec):
            i = m.group(1)
            if i not in ordered_ids:
                ordered_ids.append(i)
        for pid in built_map:
            if pid not in ordered_ids:
                ordered_ids.append(pid)
        merged = []
        for i in ordered_ids:
            if i in built_map:
                block = built_map[i]
            elif i in existing:
                block = existing[i]
                if "ModItemAppearancePreset" not in block[:100]:
                    block = to_moditem(block, i)
                elif not block.startswith("\t\t"):
                    block = "\t\t" + block.lstrip()
            else:
                continue
            # extract_blocks strips the trailing comma after `})` — restore it for folder children.
            block = block.rstrip()
            if block.endswith("})"):
                block += ","
            elif not block.endswith("},") and not block.endswith("}),"):
                block += ","
            merged.append(block)
        folder = (
            "\tPlaceObj('ModItemFolder', {\n"
            '\t\t\'name\', "JA12_Appearances",\n'
            '\t\t\'comment\', "JAZZ-UNITS-002 same-gender mixes (AIM/Rebels/Militia/Army/Thugs/Civ)",\n'
            "\t}, {\n"
            + "\n".join(merged)
            + "\n\t}),"
        )
    else:
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
    # Metadata: on --only, merge resource ids into existing META section list.
    if only and META_BEGIN in meta and META_END in meta:
        old_meta_sec = meta.split(META_BEGIN)[1].split(META_END)[0]
        old_ids = re.findall(r"'Id',\s*\"([^\"]+)\"", old_meta_sec)
        merged_ids = list(dict.fromkeys(old_ids + [p for p, _, _ in built]))
        new_meta = upsert_meta_resources(meta, merged_ids)
        # upsert expects preset ids; keep map merge below
    else:
        new_meta = upsert_meta_resources(meta, [p for p, _, _ in built])

    map_data = {}
    if only and MAP_OUT.exists():
        try:
            map_data = json.loads(MAP_OUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            map_data = {}
    for pid, _, r in built:
        map_data[pid] = {
            "gender": r["gender"],
            "body_donor": r["body"],
            "head_donor": r["head"],
            "hair_donor": r.get("hair"),
            "hat_donor": r.get("hat"),
            "note": r.get("note", ""),
            "handcrafted_kept": False,
        }
    if not only:
        for pid in skipped:
            map_data[pid] = {
                "gender": RECIPES[pid]["gender"],
                "handcrafted_kept": True,
                "note": RECIPES[pid].get("note", ""),
            }
    else:
        for pid in skipped:
            map_data.setdefault(
                pid,
                {
                    "gender": RECIPES[pid]["gender"],
                    "handcrafted_kept": True,
                    "note": RECIPES[pid].get("note", ""),
                },
            )

    ITEMS.write_text(new_items, encoding="utf-8")
    META.write_text(new_meta, encoding="utf-8")
    MAP_OUT.write_text(json.dumps(map_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", ITEMS)
    print("wrote", META)
    print("wrote", MAP_OUT)


if __name__ == "__main__":
    main()
