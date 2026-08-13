# -*- coding: utf-8 -*-
"""Rollback Scope HawksEye to vanilla JA3 (remove JAZZ CE override + OW/suppress hooks)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ITEMS = ROOT / "items.lua"
META = ROOT / "metadata.lua"
CE = ROOT / "CharacterEffect" / "HawksEye.lua"


def remove_items_ce() -> None:
    text = ITEMS.read_text(encoding="utf-8")
    # Remove ModItemCharacterEffectCompositeDef HawksEye block
    pat = re.compile(
        r"\t\t\t\tPlaceObj\('ModItemCharacterEffectCompositeDef', \{\s*"
        r"'Group', \"Perk-Personal\",\s*"
        r"'Id', \"HawksEye\",.*?"
        r"'Tier', \"Personal\",\s*"
        r"\}\),\n",
        re.S,
    )
    text2, n = pat.subn("", text, count=1)
    if not n:
        # tolerate weird whitespace from prior edits
        pat2 = re.compile(
            r"\s*PlaceObj\('ModItemCharacterEffectCompositeDef', \{\s*"
            r"'Group', \"Perk-Personal\",\s*"
            r"'Id', \"HawksEye\",.*?"
            r"'Tier', \"Personal\",\s*"
            r"\}\),",
            re.S,
        )
        text2, n = pat2.subn("", text, count=1)
        if not n:
            raise SystemExit("HawksEye ModItem CE not found in items.lua")
    text = text2
    print("items.lua: removed HawksEye CE ModItem")

    # Remove JAZZ Overwatch GetAPCost HawksEye branch
    ow_branch = """\t\t\t\t\t\t-- Scope HawksEye: sniper Overwatch costs 1 AP (keep remaining AP).
\t\t\t\t\t\tif HasPerk(unit, "HawksEye") and IsKindOf(weapon, "SniperRifle") then
\t\t\t\t\t\t\tlocal ap = (CharacterEffectDefs.HawksEye and CharacterEffectDefs.HawksEye:ResolveValue("overwatchCostOverwrite") or 1) * const.Scale.AP
\t\t\t\t\t\t\treturn ap, ap
\t\t\t\t\t\tend
"""
    if ow_branch in text:
        text = text.replace(ow_branch, "", 1)
        print("items.lua: removed Overwatch HawksEye 1 AP branch")
    else:
        print("WARN: Overwatch HawksEye branch not found (maybe already gone)")

    ITEMS.write_text(text, encoding="utf-8")


def remove_metadata() -> None:
    meta = META.read_text(encoding="utf-8")
    changed = False
    line = '\t\t"CharacterEffect/HawksEye.lua",\n'
    if line in meta:
        meta = meta.replace(line, "", 1)
        changed = True
        print("metadata.code: removed HawksEye.lua")
    # ModResourcePreset for HawksEye CE
    preset = re.compile(
        r"\t\tPlaceObj\('ModResourcePreset', \{\s*"
        r"'Class', \"CharacterEffectCompositeDef\",\s*"
        r"'Id', \"HawksEye\",.*?"
        r"\}\),\n",
        re.S,
    )
    meta2, n = preset.subn("", meta, count=1)
    if n:
        meta = meta2
        changed = True
        print("metadata.presets: removed HawksEye")
    m = re.search(r"'version',\s*(\d+)", meta)
    if not m:
        raise SystemExit("version missing")
    ver = int(m.group(1)) + 1
    meta = meta[: m.start(1)] + str(ver) + meta[m.end(1) :]
    bullet = (
        "- UNITS-006: Scope HawksEye — rollback to vanilla "
        "(PinDown+Exposed+biscuits; drop JAZZ OW 1AP / suppress×2) [no new game]\\n"
    )
    marker = "'last_changes', \""
    i = meta.find(marker) + len(marker)
    if "Scope HawksEye — rollback" not in meta[i : i + 220]:
        meta = meta[:i] + bullet + meta[i:]
    chunk = meta[i : meta.find('",', i)]
    if "\n" in chunk or "\r" in chunk:
        raise SystemExit("raw newline in last_changes")
    META.write_text(meta, encoding="utf-8", newline="\n")
    print(f"metadata version={ver}")


def delete_ce() -> None:
    if CE.exists():
        CE.unlink()
        print("deleted CharacterEffect/HawksEye.lua")
    else:
        print("CE already absent")


def main() -> None:
    remove_items_ce()
    remove_metadata()
    delete_ce()
    print("OK HawksEye rollback (code hooks still need manual strip)")


if __name__ == "__main__":
    main()
