# -*- coding: utf-8 -*-
"""Merge UNITS-006 Batch3-6 into System_NamedPerks_006.lua; put Benny/Simon/Miguel auras in Personal folders; add ModItemCode.

Run from jazz root:
  python docs/tools/_merge_units006_namedperks.py
  python docs/tools/_validate_items_quick.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "Code"
HUB = CODE / "System_NamedPerks_006.lua"
BATCHES = [
    CODE / "System_NamedPerks_006_Batch3.lua",
    CODE / "System_NamedPerks_006_Batch4.lua",
    CODE / "System_NamedPerks_006_Batch5.lua",
    CODE / "System_NamedPerks_006_Batch6.lua",
]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"


def merge_code() -> None:
    hub = HUB.read_text(encoding="utf-8")
    marker = "local function lInstallAllNamedPerks006()"
    idx = hub.find(marker)
    if idx < 0:
        raise SystemExit("lInstallAllNamedPerks006 not found")
    head = hub[:idx].rstrip() + "\n\n"
    if head.startswith("-- JAZZ-UNITS-006"):
        head = (
            "-- JAZZ-UNITS-006 named perks runtime (batches 1-6 merged into this file).\n"
            + head[head.find("\n") + 1 :]
        )

    parts = []
    for path in BATCHES:
        if not path.exists():
            print("skip missing", path.name)
            continue
        text = path.read_text(encoding="utf-8")
        parts.append(f"-- === merged from {path.name} ===\n{text.rstrip()}\n")

    if not parts:
        print("batches already merged?")
    else:
        body = "\n".join(parts)
        tail = """
local function lInstallAllNamedPerks006()
\tlInstallNamedPerks006()
\tlInstallNamedPerks006Batch2()
\tif type(Jazz_InstallNamedPerks006Batch3) == "function" then
\t\tJazz_InstallNamedPerks006Batch3()
\tend
\tif type(Jazz_InstallNamedPerks006Batch4) == "function" then
\t\tJazz_InstallNamedPerks006Batch4()
\tend
\tif type(Jazz_InstallNamedPerks006Batch5) == "function" then
\t\tJazz_InstallNamedPerks006Batch5()
\tend
\tif type(Jazz_InstallNamedPerks006Batch6) == "function" then
\t\tJazz_InstallNamedPerks006Batch6()
\tend
end

OnMsg.ModsReloaded = function()
\tlInstallAllNamedPerks006()
end
OnMsg.DataLoaded = function()
\tlInstallAllNamedPerks006()
end
OnMsg.NewGame = function()
\tlInstallAllNamedPerks006()
end
OnMsg.LoadGame = function()
\tlInstallAllNamedPerks006()
end

OnMsg.CombatStart = function()
\tif type(Jazz_NamedPerks006Batch3OnCombatStart) == "function" then
\t\tJazz_NamedPerks006Batch3OnCombatStart()
\tend
\tif type(Jazz_NamedPerks006Batch4OnCombatStart) == "function" then
\t\tJazz_NamedPerks006Batch4OnCombatStart()
\tend
\tif type(Jazz_NamedPerks006Batch5OnCombatStart) == "function" then
\t\tJazz_NamedPerks006Batch5OnCombatStart()
\tend
\tif type(Jazz_NamedPerks006Batch6OnCombatStart) == "function" then
\t\tJazz_NamedPerks006Batch6OnCombatStart()
\tend
end
OnMsg.TurnStart = function()
\tif type(Jazz_NamedPerks006Batch3OnTurnStart) == "function" then
\t\tJazz_NamedPerks006Batch3OnTurnStart()
\tend
\tif type(Jazz_NamedPerks006Batch4OnTurnStart) == "function" then
\t\tJazz_NamedPerks006Batch4OnTurnStart()
\tend
\tif type(Jazz_NamedPerks006Batch5OnTurnStart) == "function" then
\t\tJazz_NamedPerks006Batch5OnTurnStart()
\tend
end
"""
        HUB.write_text(head + body + "\n" + tail.lstrip("\n"), encoding="utf-8", newline="\n")
        print("merged hub", HUB.stat().st_size)
        for path in BATCHES:
            if path.exists():
                path.unlink()
                print("deleted", path.name)


def extract_moditem_block(text: str, class_id: str) -> tuple[str, str]:
    needle = f"'Id', \"{class_id}\""
    idx = text.find(needle)
    if idx < 0:
        raise SystemExit(f"ModItem {class_id} missing")
    start = text.rfind("PlaceObj('ModItemCharacterEffectCompositeDef'", 0, idx)
    if start < 0:
        raise SystemExit(f"PlaceObj start missing for {class_id}")
    # Include leading indent on the same line so removal does not leave orphan tabs.
    line_start = text.rfind("\n", 0, start) + 1
    start = line_start
    brace_open = text.find("{", start)
    if brace_open < 0:
        raise SystemExit(f"table {{ missing for {class_id}")
    depth = 0
    j = brace_open
    while j < len(text):
        ch = text[j]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                j += 1
                break
        j += 1
    # closing ) of PlaceObj(
    if j >= len(text) or text[j] != ")":
        # allow whitespace
        while j < len(text) and text[j].isspace():
            j += 1
        if j >= len(text) or text[j] != ")":
            raise SystemExit(f"PlaceObj ) missing for {class_id} at {j}")
    j += 1
    end = j
    if end < len(text) and text[end] == ",":
        end += 1
    if end < len(text) and text[end] == "\r":
        end += 1
    if end < len(text) and text[end] == "\n":
        end += 1
    block = text[start:j]
    if not block.endswith(","):
        block += ","
    block += "\n"
    rest = text[:start] + text[end:]
    return block, rest


def folder_wrap(name: str, *blocks: str) -> str:
    body = "".join(blocks)
    return (
        f"\t\t\tPlaceObj('ModItemFolder', {{\n"
        f"\t\t\t\t'name', \"{name}\",\n"
        f"\t\t\t}}, {{\n"
        f"{body}"
        f"\t\t\t\t}}),\n"
    )


def fix_items() -> None:
    text = ITEMS.read_text(encoding="utf-8")

    if "'name', \"Benny\"" in text and "'Id', \"Jazz_Perk_Benny\"" in text[text.find("'name', \"Benny\"") : text.find("'name', \"Benny\"") + 800]:
        print("Benny folder already present — skip relocate")
    else:
        moved: dict[str, str] = {}
        for cid in (
            "Jazz_Perk_Benny",
            "Jazz_Perk_Simon",
            "Jazz_MiguelAuraUp",
            "Jazz_MiguelAuraDown",
        ):
            block, text = extract_moditem_block(text, cid)
            moved[cid] = block
            print("extracted", cid)

        # Expand Miguel folder: insert auras before folder close preceding Gamos.
        # Actual boundary (4-tab perk close + 4-tab folder close + Gamos folder):
        mperk = text.find("'Id', \"Jazz_Perk_Miguel\"")
        if mperk < 0:
            raise SystemExit("Jazz_Perk_Miguel missing")
        gamos = text.find("'name', \"Gamos\"", mperk)
        if gamos < 0:
            raise SystemExit("Gamos folder missing after Miguel")
        # Back up to the PlaceObj('ModItemFolder' that opens Gamos.
        gamos_place = text.rfind("PlaceObj('ModItemFolder'", mperk, gamos)
        if gamos_place < 0:
            raise SystemExit("Gamos PlaceObj missing")
        # Include the Miguel folder closer immediately before Gamos PlaceObj.
        # ... perk }), <folder }>), <Gamos PlaceObj
        folder_close = text.rfind("}),", mperk, gamos_place)
        if folder_close < 0:
            raise SystemExit("Miguel folder closer missing")
        # folder_close points at `}` of `}),` — include through comma
        insert_at = folder_close  # replace from folder closer onward through Gamos name line start
        # Keep Gamos PlaceObj; replace only the bare folder closer with: auras + closer + Benny + Simon.
        # Structure before Gamos PlaceObj should end with Miguel folder `}),`
        closer_end = folder_close + 3  # `}),`
        while closer_end < len(text) and text[closer_end] in "\r\n":
            closer_end += 1
        replacement = (
            moved["Jazz_MiguelAuraUp"]
            + moved["Jazz_MiguelAuraDown"]
            + "\t\t\t\t}),\n"
            + folder_wrap("Benny", moved["Jazz_Perk_Benny"])
            + folder_wrap("Simon", moved["Jazz_Perk_Simon"])
        )
        text = text[:insert_at] + replacement + text[closer_end:]
        print("relocated Benny/Simon folders + Miguel auras")

    # ModItemCode for the merged runtime file
    code_needle = "'CodeFileName', \"Code/System_NamedPerks_006.lua\""
    if code_needle not in text:
        soft = "'CodeFileName', \"Code/System_OR_Unit.lua\","
        sidx = text.find(soft)
        if sidx < 0:
            raise SystemExit("System_OR_Unit ModItemCode not found")
        end = text.find("}),", sidx) + 3
        insert_code = (
            "\n\t\t\tPlaceObj('ModItemCode', {\n"
            "\t\t\t\t'name', \"System_NamedPerks_006\",\n"
            "\t\t\t\t'comment', \"UNITS-006 named perks runtime (all batches)\",\n"
            "\t\t\t\t'CodeFileName', \"Code/System_NamedPerks_006.lua\",\n"
            "\t\t\t}),"
        )
        text = text[:end] + insert_code + text[end:]
        print("added ModItemCode System_NamedPerks_006")
    else:
        print("ModItemCode already present")

    tmp = ITEMS.with_suffix(".lua.tmp_merge")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    tmp.replace(ITEMS)
    print("wrote items.lua")


def fix_metadata() -> None:
    meta = META.read_text(encoding="utf-8")
    for name in (
        "System_NamedPerks_006_Batch3.lua",
        "System_NamedPerks_006_Batch4.lua",
        "System_NamedPerks_006_Batch5.lua",
        "System_NamedPerks_006_Batch6.lua",
    ):
        meta = meta.replace(f'\t\t"Code/{name}",\n', "")
    if '"Code/System_NamedPerks_006.lua"' not in meta:
        raise SystemExit("hub missing from metadata.code")
    META.write_text(meta, encoding="utf-8", newline="\n")
    print("metadata.code cleaned")


def patch_docs() -> None:
    cov = ROOT / "docs/technical/systems/file-coverage.md"
    if cov.exists():
        t = cov.read_text(encoding="utf-8")
        t2 = t
        for name in (
            "System_NamedPerks_006_Batch3.lua",
            "System_NamedPerks_006_Batch4.lua",
            "System_NamedPerks_006_Batch5.lua",
            "System_NamedPerks_006_Batch6.lua",
        ):
            # remove table rows mentioning batch files
            lines = []
            for line in t2.splitlines(True):
                if f"`{name}`" in line:
                    continue
                lines.append(line)
            t2 = "".join(lines)
        t2 = t2.replace(
            "UNITS-006 install hub (Batch3–6)",
            "UNITS-006 named perks runtime (batches 1–6 merged)",
        )
        if t2 != t:
            cov.write_text(t2, encoding="utf-8", newline="\n")
            print("updated file-coverage.md")

    readme = ROOT / "docs/tools/README.md"
    if readme.exists():
        r = readme.read_text(encoding="utf-8")
        row = (
            "| `_merge_units006_namedperks.py` | Merge Batch3–6 into `System_NamedPerks_006.lua`; "
            "relocate Benny/Simon/Miguel aura ModItems; add ModItemCode. |\n"
        )
        if "_merge_units006_namedperks.py" not in r:
            # insert after batch5 gen row if present
            key = "| `_gen_units006_batch5.py`"
            if key in r:
                i = r.find(key)
                eol = r.find("\n", i) + 1
                r = r[:eol] + row + r[eol:]
            else:
                r += "\n" + row
            readme.write_text(r, encoding="utf-8", newline="\n")
            print("README tools row")


def main() -> None:
    merge_code()
    fix_items()
    fix_metadata()
    patch_docs()
    print("OK merge")


if __name__ == "__main__":
    main()
