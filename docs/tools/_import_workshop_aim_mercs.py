# -*- coding: utf-8 -*-
"""Import six workshop AIM merc mods into jazz-units (+ perk CharacterEffect into jazz).

Keeps Merc_* IDs (voices/T-ids unchanged). Rewires Portrait/BigPortrait to
Mod/Dv3mFVN/MercPortraits/<Id>.png after JA3 portrait regen.

Source folders under Mods/:
  Merc_ Annie Dubois, Merc_ Carol Thompson, Merc_ Hector Sanchez,
  Merc_ Jerry Sinclair, Merc_ Mildred Patterson, Merc_ Samuel Nkosi
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

MODS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")
JAZZ = MODS / "jazz"
JU = MODS / "jazz-units"
ITEMS = JU / "items.lua"
META = JU / "metadata.lua"
JAZZ_ITEMS = JAZZ / "items.lua"
JAZZ_META = JAZZ / "metadata.lua"

MERCS = [
    {
        "folder": "Merc_ Annie Dubois",
        "id": "Merc_AnnieDubois",
        "portrait": "Annie",
        "perk": "Merc_AnnieDubois_Perk",
        "perk_file": "Merc_AnnieDubois_Perk.lua",
    },
    {
        "folder": "Merc_ Carol Thompson",
        "id": "Merc_CarolThompson",
        "portrait": "Carol",
        "perk": "Merc_CarolThompson_Perk",
        "perk_file": "Merc_CarolThompson_Perk.lua",
    },
    {
        "folder": "Merc_ Hector Sanchez",
        "id": "Merc_HectorSanchez",
        "portrait": "Hector",
        "perk": "Merc_HectorSanchez_Perk",
        "perk_file": "Merc_HectorSanchez_Perk.lua",
    },
    {
        "folder": "Merc_ Jerry Sinclair",
        "id": "Merc_JerrySinclair",
        "portrait": "Jerry",
        "perk": "Merc_JerrySinclair_Perk",
        "perk_file": "Merc_JerrySinclair_Perk.lua",
    },
    {
        "folder": "Merc_ Mildred Patterson",
        "id": "Merc_MildredPatterson",
        "portrait": "Mildred",
        "perk": "Merc_MildredPatterson_Bookworm",
        "perk_file": "Merc_MildredPatterson_Bookworm.lua",
    },
    {
        "folder": "Merc_ Samuel Nkosi",
        "id": "Merc_SamuelNkosi",
        "portrait": "Samuel",
        "perk": "Merc_SamuelNkosi_Perk",
        "perk_file": "Merc_SamuelNkosi_Perk.lua",
    },
]


def copy_voices(src: Path) -> int:
    vdir = src / "Voices"
    if not vdir.exists():
        return 0
    dest = JU / "voices"
    dest.mkdir(exist_ok=True)
    n = 0
    for p in vdir.rglob("*.opus"):
        shutil.copy2(p, dest / p.name)
        n += 1
    return n


def copy_unitdata(src: Path, unit_id: str, portrait: str) -> None:
    udir = src / "UnitData"
    if not udir.exists():
        return
    for p in udir.glob("*.lua"):
        text = p.read_text(encoding="utf-8")
        text = re.sub(
            r'Portrait = "[^"]+"',
            f'Portrait = "Mod/Dv3mFVN/MercPortraits/{portrait}.png"',
            text,
        )
        text = re.sub(
            r'BigPortrait = "[^"]+"',
            f'BigPortrait = "Mod/Dv3mFVN/MercPortraits/{portrait}_Big.png"',
            text,
        )
        # FallbackMissingVR should not self-loop badly; Ice is safer
        text = re.sub(
            r'FallbackMissingVR = "[^"]+"',
            'FallbackMissingVR = "Ice"',
            text,
        )
        out = JU / "UnitData" / p.name
        out.write_text(text, encoding="utf-8")
        print("UnitData", out.name)


def copy_effects(src: Path, perk_file: str) -> None:
    # Prefer CharacterEffect/ then root
    candidates = [
        src / "CharacterEffect" / perk_file,
        src / perk_file,
    ]
    # Mildred etc may be only under CharacterEffect with exact name
    for p in (src / "CharacterEffect").glob("*.lua") if (src / "CharacterEffect").exists() else []:
        candidates.append(p)
    seen = set()
    for p in candidates:
        if not p.exists() or p.name in seen:
            continue
        seen.add(p.name)
        dest_dir = JAZZ / "CharacterEffect"
        dest_dir.mkdir(exist_ok=True)
        shutil.copy2(p, dest_dir / p.name)
        print("CharacterEffect", p.name)


def copy_code(src: Path) -> None:
    cdir = src / "Code"
    if not cdir.exists():
        return
    # Perk/combat Code lives in jazz; keep Voices helpers with units if named *Voices*
    for p in cdir.glob("*.lua"):
        if "Voice" in p.name or "Voices" in p.name:
            dest = JU / "Code" / "WorkshopMercs"
        else:
            dest = JAZZ / "Code" / "WorkshopMercs"
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest / p.name)
        print("Code", dest.parent.name + "/" + dest.name + "/" + p.name)


def extract_placeobj_at(text: str, start: int) -> str | None:
    """Balanced PlaceObj(...) extractor; skips Lua `--[[ ]]` / `--` comments."""
    if not text.startswith("PlaceObj(", start):
        return None
    depth = 0
    k = start
    in_str = False
    quote = ""
    esc = False
    n = len(text)
    while k < n:
        ch = text[k]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
            k += 1
            continue
        if text.startswith("--[[", k):
            end = text.find("]]", k + 4)
            if end < 0:
                return None
            k = end + 2
            continue
        if text.startswith("--", k):
            end = text.find("\n", k)
            if end < 0:
                return None
            k = end + 1
            continue
        if ch in ("'", '"'):
            in_str = True
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                end = k + 1
                if end < n and text[end] == ",":
                    end += 1
                return text[start:end]
        k += 1
    return None


def extract_placeobjs(items_text: str) -> list[str]:
    """Split PlaceObj blocks from return { ... } (includes nested; filter downstream)."""
    blocks = []
    i = 0
    while True:
        j = items_text.find("PlaceObj(", i)
        if j < 0:
            break
        block = extract_placeobj_at(items_text, j)
        if not block:
            break
        blocks.append(block.strip())
        i = j + len(block)
    return blocks


def rewire_portraits_in_block(block: str, portrait: str) -> str:
    block = re.sub(
        r"'Portrait',\s*\"[^\"]+\"",
        f"'Portrait', \"Mod/Dv3mFVN/MercPortraits/{portrait}.png\"",
        block,
    )
    block = re.sub(
        r"'BigPortrait',\s*\"[^\"]+\"",
        f"'BigPortrait', \"Mod/Dv3mFVN/MercPortraits/{portrait}_Big.png\"",
        block,
    )
    block = re.sub(
        r"'FallbackMissingVR',\s*\"[^\"]+\"",
        "'FallbackMissingVR', \"Ice\"",
        block,
    )
    # CodeFileName paths → WorkshopMercs (jazz or jazz-units)
    def _code_sub(m: re.Match[str]) -> str:
        name = m.group(1)
        return f"'CodeFileName', \"Code/WorkshopMercs/{name}\""

    block = re.sub(r"'CodeFileName',\s*\"Code/([^\"]+)\"", _code_sub, block)
    return block


def insert_folder(items: str, unit_id: str, blocks: list[str]) -> str:
    if f"'Id', \"{unit_id}\"" in items or f'id = "{unit_id}"' in items:
        print(f"SKIP items already has {unit_id}")
        return items
    body = ",\n".join(blocks)
    folder = (
        f"\t\tPlaceObj('ModItemFolder', {{\n"
        f"\t\t\t'name', \"{unit_id}\",\n"
        f"\t\t}}, {{\n"
        f"{body}\n"
        f"\t\t}}),\n"
    )
    marker = "\t\tPlaceObj('ModItemFolder', {\n\t\t\t'name', \"NewMercs\","
    if marker not in items:
        # fallback before closing
        marker2 = "\tPlaceObj('ModItemLocTable',"
        if marker2 not in items:
            raise SystemExit("insert marker not found")
        return items.replace(marker2, folder + marker2, 1)
    return items.replace(marker, folder + marker, 1)


def ensure_meta_code(path: Path, rel: str) -> None:
    text = path.read_text(encoding="utf-8")
    if f'"{rel}"' in text:
        return
    # insert after first UnitData entry area — after Jazz_Simon if present else Eskimo
    anchor = '"UnitData/Jazz_Simon.lua",'
    if anchor not in text:
        anchor = '"UnitData/Jazz_Eskimo.lua",'
    if anchor not in text:
        print("WARN no code anchor for", rel)
        return
    text = text.replace(anchor, anchor + f'\n\t\t"{rel}",', 1)
    path.write_text(text, encoding="utf-8")
    print("metadata code+", rel)


def ensure_meta_preset(path: Path, class_name: str, pid: str, display: str) -> None:
    text = path.read_text(encoding="utf-8")
    if f"'Id', \"{pid}\"" in text and class_name in text:
        # might exist
        if f"'Class', \"{class_name}\"" in text and f"'Id', \"{pid}\"" in text:
            return
    block = (
        f"\t\tPlaceObj('ModResourcePreset', {{\n"
        f"\t\t\t'Class', \"{class_name}\",\n"
        f"\t\t\t'Id', \"{pid}\",\n"
        f"\t\t\t'ClassDisplayName', \"{display}\",\n"
        f"\t\t}}),\n"
    )
    # before JAZZ_Quinten50 or end of resources
    anchor = "'Id', \"JAZZ_Quinten50\""
    idx = text.find(anchor)
    if idx < 0:
        print("WARN preset anchor missing", pid)
        return
    # find PlaceObj start before this Id
    start = text.rfind("PlaceObj('ModResourcePreset'", 0, idx)
    text = text[:start] + block + text[start:]
    path.write_text(text, encoding="utf-8")
    print("metadata preset+", class_name, pid)


def main() -> int:
    items = ITEMS.read_text(encoding="utf-8")
    for m in MERCS:
        src = MODS / m["folder"]
        if not src.exists():
            print("MISSING", src)
            continue
        print("===", m["id"], "===")
        n = copy_voices(src)
        print("voices", n)
        copy_unitdata(src, m["id"], m["portrait"])
        copy_effects(src, m["perk_file"])
        copy_code(src)

        src_items = (src / "items.lua").read_text(encoding="utf-8")
        blocks = extract_placeobjs(src_items)
        # keep UnitData, VoiceResponse, CharacterEffect, Appearance, InventoryItem, CombatAction, Code
        keep_types = (
            "ModItemUnitDataCompositeDef",
            "ModItemVoiceResponse",
            "ModItemCharacterEffectCompositeDef",
            "ModItemAppearancePreset",
            "ModItemInventoryItemCompositeDef",
            "ModItemCombatAction",
            "ModItemCode",
            "ModItemLootDef",
        )
        kept = []
        for b in blocks:
            if any(t in b for t in keep_types):
                kept.append(rewire_portraits_in_block(b, m["portrait"]))
        print("items blocks kept", len(kept), "/", len(blocks))
        items = insert_folder(items, m["id"], kept)

        # metadata companions
        ud = JU / "UnitData" / f"{m['id']}.lua"
        if ud.exists():
            ensure_meta_code(META, f"UnitData/{m['id']}.lua")
        ensure_meta_preset(META, "UnitDataCompositeDef", m["id"], "Unit")
        ensure_meta_preset(META, "VoiceResponse", m["id"], "Unit voice responses")
        ensure_meta_preset(JAZZ_META, "CharacterEffectCompositeDef", m["perk"], "Effect")
        # code files in jazz-units
        for code in (JU / "Code" / "WorkshopMercs").glob(f"{m['id']}*"):
            ensure_meta_code(META, f"Code/WorkshopMercs/{code.name}")

    ITEMS.write_text(items, encoding="utf-8")
    print("Wrote jazz-units/items.lua")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
