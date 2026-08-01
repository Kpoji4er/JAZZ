# -*- coding: utf-8 -*-
"""Finish workshop AIM merc import gaps (idempotent).

Fixes:
  - CombatAction Icon → Mod/e6L4ECj/Images/WorkshopMercs/<Slug>_Perk_Passive.png
  - ju CharacterEffect Icon → e6L4ECj WorkshopMercs perk PNGs
  - Carol UnitData companion + metadata code entry
  - Inject ModItemVoiceResponse from source mods into ju items folders
  - Remove ju ModItemCode for CombatAction (files live in jazz)
  - Ensure jazz metadata CombatAction ModResourcePreset for each perk
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

MODS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods")
JAZZ = MODS / "jazz"
JU = MODS / "jazz-units"

MERCS = [
    {
        "folder": "Merc_ Annie Dubois",
        "id": "Merc_AnnieDubois",
        "slug": "Annie",
        "perk": "Merc_AnnieDubois_Perk",
    },
    {
        "folder": "Merc_ Carol Thompson",
        "id": "Merc_CarolThompson",
        "slug": "Carol",
        "perk": "Merc_CarolThompson_Perk",
    },
    {
        "folder": "Merc_ Hector Sanchez",
        "id": "Merc_HectorSanchez",
        "slug": "Hector",
        "perk": "Merc_HectorSanchez_Perk",
    },
    {
        "folder": "Merc_ Jerry Sinclair",
        "id": "Merc_JerrySinclair",
        "slug": "Jerry",
        "perk": "Merc_JerrySinclair_Perk",
    },
    {
        "folder": "Merc_ Mildred Patterson",
        "id": "Merc_MildredPatterson",
        "slug": "Mildred",
        "perk": "Merc_MildredPatterson_Bookworm",
    },
    {
        "folder": "Merc_ Samuel Nkosi",
        "id": "Merc_SamuelNkosi",
        "slug": "Samuel",
        "perk": "Merc_SamuelNkosi_Perk",
    },
]

OLD_MOD_IDS = ("sH5nmG", "Q6ivSk4", "jkp5GEJ", "E5rtcCe", "QkMtGCa", "HgzATh3")


def extract_placeobj_at(text: str, start: int) -> str | None:
    """Return full PlaceObj(...) call starting at start (must point at PlaceObj).

    Skips Lua long comments `--[[ ]]` and line comments `--` so apostrophes inside
    T() annotations (e.g. player's) do not break the scanner.
    """
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
        # long comment
        if text.startswith("--[[", k):
            end = text.find("]]", k + 4)
            if end < 0:
                return None
            k = end + 2
            continue
        # line comment
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


def find_moditem(text: str, kind: str, unit_id: str) -> str | None:
    needle = f"PlaceObj('{kind}',"
    idx = 0
    while True:
        j = text.find(needle, idx)
        if j < 0:
            return None
        block = extract_placeobj_at(text, j)
        if not block:
            return None
        if f'id = "{unit_id}"' in block or f"'Id', \"{unit_id}\"" in block:
            return block
        idx = j + len(needle)


def convert_unitdata_companion(placeobj_block: str, unit_id: str) -> str:
    """ModItemUnitDataCompositeDef PlaceObj → UndefineClass/DefineClass companion."""
    m = re.match(
        r"PlaceObj\('ModItemUnitDataCompositeDef',\s*\{([\s\S]*)\}\)\s*,?\s*$",
        placeobj_block.strip(),
    )
    if not m:
        raise SystemExit(f"Cannot parse UnitData PlaceObj for {unit_id}")
    inner = m.group(1)
    # drop ModItem-only fields at any depth carefully: only top-level Group/Id
    out: list[str] = []
    i = 0
    depth = 0
    in_str = False
    quote = ""
    esc = False
    while i < len(inner):
        ch = inner[i]
        if in_str:
            out.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
            i += 1
            continue
        if ch in ("'", '"'):
            # top-level key?
            if depth == 0 and ch == "'":
                km = re.match(r"'([A-Za-z_][A-Za-z0-9_]*)',\s*", inner[i:])
                if km:
                    key = km.group(1)
                    i += km.end()
                    if key in ("Group", "Id"):
                        # skip value until next top-level comma / end
                        # value may be string, number, table, PlaceObj
                        while i < len(inner) and inner[i] in " \t\r\n":
                            i += 1
                        if i < len(inner) and inner[i] in ("'", '"'):
                            q = inner[i]
                            i += 1
                            while i < len(inner):
                                if inner[i] == "\\" and i + 1 < len(inner):
                                    i += 2
                                    continue
                                if inner[i] == q:
                                    i += 1
                                    break
                                i += 1
                        elif inner.startswith("PlaceObj(", i):
                            blk = extract_placeobj_at(inner, i)
                            i += len(blk or "")
                        else:
                            # number / ident / bool
                            while i < len(inner) and inner[i] not in ",\n":
                                i += 1
                        if i < len(inner) and inner[i] == ",":
                            i += 1
                        continue
                    out.append(f"{key} = ")
                    continue
            in_str = True
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "{":
            depth += 1
            out.append(ch)
        elif ch == "}":
            depth -= 1
            out.append(ch)
        elif ch == "(":
            depth += 1
            out.append(ch)
        elif ch == ")":
            depth -= 1
            out.append(ch)
        else:
            out.append(ch)
        i += 1

    body = "".join(out).strip()
    # normalize leading indent to one tab for class fields
    lines = body.splitlines()
    cleaned = []
    for ln in lines:
        cleaned.append(ln.rstrip())
    body = "\n".join(cleaned)
    if body and not body.endswith("\n"):
        body += "\n"
    # indent body with one tab
    indented = "\n".join(("\t" + ln) if ln.strip() else ln for ln in body.splitlines())
    return (
        f"UndefineClass('{unit_id}')\n"
        f"DefineClass.{unit_id} = {{\n"
        f"\t__parents = {{ \"UnitData\" }},\n"
        f"\t__generated_by_class = \"ModItemUnitDataCompositeDef\",\n"
        f"\n"
        f"{indented}\n"
        f"}}\n"
    )


def fix_combat_action_icons() -> None:
    mapping = {m["id"]: m["slug"] for m in MERCS}
    for mid, slug in mapping.items():
        path = JAZZ / "Code" / "WorkshopMercs" / f"{mid}_CombatAction.lua"
        if not path.exists():
            print("MISSING CombatAction", path)
            continue
        text = path.read_text(encoding="utf-8")
        new_icon = f'Mod/e6L4ECj/Images/WorkshopMercs/{slug}_Perk_Passive.png'
        new_text, n = re.subn(
            r'Icon\s*=\s*"[^"]+"',
            f'Icon = "{new_icon}"',
            text,
            count=1,
        )
        # also rewrite any other old-mod Images refs
        for oid in OLD_MOD_IDS:
            new_text = new_text.replace(f"Mod/{oid}/", "Mod/e6L4ECj/")
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print("CombatAction Icon", mid, "→", new_icon, f"(subs={n})")
        else:
            print("CombatAction Icon OK", mid)


def fix_ju_perk_icons(items: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return f"'Icon', \"Mod/e6L4ECj/Images/WorkshopMercs/{m.group(1)}\""

    new, n = re.subn(
        r"'Icon',\s*\"Mod/Dv3mFVN/Images/WorkshopMercs/((?:Annie|Carol|Hector|Jerry|Mildred|Samuel)_Perk\.png)\"",
        repl,
        items,
    )
    print(f"ju perk Icon rewires: {n}")
    return new


def ensure_carol_unitdata(items: str) -> None:
    out = JU / "UnitData" / "Merc_CarolThompson.lua"
    block = find_moditem(items, "ModItemUnitDataCompositeDef", "Merc_CarolThompson")
    if not block:
        raise SystemExit("Carol UnitData missing from ju items.lua")
    companion = convert_unitdata_companion(block, "Merc_CarolThompson")
    # force portrait paths + FallbackMissingVR
    companion = re.sub(
        r'Portrait\s*=\s*"[^"]+"',
        'Portrait = "Mod/Dv3mFVN/MercPortraits/Carol.png"',
        companion,
    )
    companion = re.sub(
        r'BigPortrait\s*=\s*"[^"]+"',
        'BigPortrait = "Mod/Dv3mFVN/MercPortraits/Carol_Big.png"',
        companion,
    )
    companion = re.sub(
        r'FallbackMissingVR\s*=\s*"[^"]+"',
        'FallbackMissingVR = "Ice"',
        companion,
    )
    if out.exists() and out.read_text(encoding="utf-8") == companion:
        print("Carol UnitData companion already up to date")
    else:
        out.write_text(companion, encoding="utf-8")
        print("Wrote", out)


def ensure_meta_code(meta_path: Path, rel: str, after_rel: str) -> None:
    text = meta_path.read_text(encoding="utf-8")
    if f'"{rel}"' in text:
        print("meta code OK", rel)
        return
    anchor = f'"{after_rel}",'
    if anchor not in text:
        raise SystemExit(f"meta anchor missing for {rel}: {after_rel}")
    text = text.replace(anchor, anchor + f'\n\t\t"{rel}",', 1)
    meta_path.write_text(text, encoding="utf-8")
    print("meta code+", rel)


def ensure_combat_action_presets() -> None:
    meta_path = JAZZ / "metadata.lua"
    text = meta_path.read_text(encoding="utf-8")
    added = 0
    for m in MERCS:
        perk = m["perk"]
        # already have CombatAction preset?
        if re.search(
            rf"PlaceObj\('ModResourcePreset',\s*\{{\s*'Class',\s*\"CombatAction\",\s*'Id',\s*\"{perk}\"",
            text,
        ):
            continue
        # insert before CharacterEffect preset for same Id
        needle = (
            f"PlaceObj('ModResourcePreset', {{\n"
            f"\t\t\t'Class', \"CharacterEffectCompositeDef\",\n"
            f"\t\t\t'Id', \"{perk}\","
        )
        # tolerate indentation variants
        pat = re.compile(
            rf"(PlaceObj\('ModResourcePreset',\s*\{{\s*'Class',\s*\"CharacterEffectCompositeDef\",\s*'Id',\s*\"{perk}\")"
        )
        mm = pat.search(text)
        if not mm:
            print("WARN no CE preset to anchor CombatAction", perk)
            continue
        insert = (
            f"PlaceObj('ModResourcePreset', {{\n"
            f"\t\t\t'Class', \"CombatAction\",\n"
            f"\t\t\t'Id', \"{perk}\",\n"
            f"\t\t\t'ClassDisplayName', \"Combat Actions\",\n"
            f"\t\t}}),\n\t\t"
        )
        text = text[: mm.start()] + insert + text[mm.start() :]
        added += 1
        print("meta CombatAction preset+", perk)
    if added:
        meta_path.write_text(text, encoding="utf-8")
    else:
        print("CombatAction presets OK")


def remove_ju_combat_action_moditemcode(items: str) -> str:
    n = 0
    for m in MERCS:
        mid = m["id"]
        pat = re.compile(
            rf"PlaceObj\('ModItemCode',\s*\{{[^{{}}]*?'name',\s*\"{mid}_CombatAction\"[^{{}}]*?\}}\),?\s*",
            re.S,
        )
        items2, c = pat.subn("", items)
        if c:
            n += c
            items = items2
            print("removed ju ModItemCode", f"{mid}_CombatAction")
        else:
            # broader: extract_placeobj scan
            needle = f"'name', \"{mid}_CombatAction\""
            idx = items.find(needle)
            if idx < 0:
                continue
            start = items.rfind("PlaceObj('ModItemCode'", 0, idx)
            if start < 0:
                continue
            block = extract_placeobj_at(items, start)
            if block:
                items = items[:start] + items[start + len(block) :]
                # clean double blank
                items = re.sub(r"\n{3,}", "\n\n", items)
                n += 1
                print("removed ju ModItemCode", f"{mid}_CombatAction")
    print(f"removed CombatAction ModItemCode count={n}")
    return items


def inject_voice_responses(items: str) -> str:
    for m in MERCS:
        mid = m["id"]
        if find_moditem(items, "ModItemVoiceResponse", mid):
            print("VR already in ju items", mid)
            continue
        src_items = (MODS / m["folder"] / "items.lua").read_text(encoding="utf-8")
        vr = find_moditem(src_items, "ModItemVoiceResponse", mid)
        if not vr:
            print("WARN source missing VR", mid)
            continue
        # ensure trailing comma
        vr = vr.rstrip()
        if not vr.endswith(","):
            vr += ","
        # find folder children close: after UnitData for this merc, before next folder or end
        # Prefer insert after ModItemUnitDataCompositeDef for this id
        ud = find_moditem(items, "ModItemUnitDataCompositeDef", mid)
        if not ud:
            print("WARN no UnitData to insert VR after", mid)
            continue
        pos = items.find(ud)
        if pos < 0:
            print("WARN UnitData position lost", mid)
            continue
        insert_at = pos + len(ud)
        # skip whitespace
        items = items[:insert_at] + "\n" + vr + "\n" + items[insert_at:]
        print("injected VR", mid, "chars", len(vr))
    return items


def grep_old_ids() -> None:
    for root in (JAZZ, JU):
        hits = []
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".lua", ".csv", ".md", ".txt"}:
                continue
            if "_tmp_" in p.name or "/.git/" in str(p).replace("\\", "/"):
                continue
            try:
                t = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for oid in OLD_MOD_IDS:
                if oid in t:
                    hits.append((str(p.relative_to(root)), oid))
        if hits:
            print(f"OLD IDS in {root.name}:")
            for h in hits[:40]:
                print(" ", h)
        else:
            print(f"OLD IDS in {root.name}: none")


def main() -> int:
    fix_combat_action_icons()

    items_path = JU / "items.lua"
    items = items_path.read_text(encoding="utf-8")
    items = fix_ju_perk_icons(items)
    ensure_carol_unitdata(items)
    ensure_meta_code(
        JU / "metadata.lua",
        "UnitData/Merc_CarolThompson.lua",
        "Code/WorkshopMercs/Merc_CarolThompson_Voices.lua",
    )
    items = remove_ju_combat_action_moditemcode(items)
    items = inject_voice_responses(items)
    items_path.write_text(items, encoding="utf-8")
    print("Wrote", items_path)

    ensure_combat_action_presets()
    grep_old_ids()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
