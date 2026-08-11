# -*- coding: utf-8 -*-
"""Bump metadata for DrQ ExplodingPalm + ModResourcePreset CA/CE."""
from __future__ import annotations

import re
from pathlib import Path

META = Path(__file__).resolve().parents[2] / "metadata.lua"
text = META.read_text(encoding="utf-8")

presets = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "ExplodingPalm",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "ExplodingPalm",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),
"""

if "'Id', \"ExplodingPalm\"" not in text or "Combat Actions" not in text[text.find("ExplodingPalm") - 80 : text.find("ExplodingPalm") + 40] if "ExplodingPalm" in text else True:
    # insert before GruntyPerk CE preset if present, else before NaturalHealing companion path area
    needle = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CharacterEffectCompositeDef",
\t\t\t'Id', "GruntyPerk",
\t\t\t'ClassDisplayName', "Character effect",
\t\t}),"""
    if needle not in text:
        raise SystemExit("GruntyPerk preset needle missing")
    if "'Id', \"ExplodingPalm\"" not in text:
        text = text.replace(needle, presets + needle, 1)
        print("Inserted ExplodingPalm presets")
    else:
        # only CA missing?
        if "'Class', \"CombatAction\"" not in text[max(0, text.find("ExplodingPalm") - 120) : text.find("ExplodingPalm") + 5]:
            ca_only = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', "CombatAction",
\t\t\t'Id', "ExplodingPalm",
\t\t\t'ClassDisplayName', "Combat Actions",
\t\t}),
"""
            text = text.replace(needle, ca_only + needle, 1)
            print("Inserted ExplodingPalm CA preset only")
        else:
            print("presets already ok")

m = re.search(r"'version',\s*(\d+)", text)
ver = int(m.group(1))
text = text[: m.start(1)] + str(ver + 1) + text[m.end(1) :]
bullet = (
    "- UNITS-006: DrQ ExplodingPalm — unarmed HP-tier statuses; sat debt +30%; "
    "block WoundInfected; Passive hotbar [no new game]"
    + "\\"
    + "n"
)
if "DrQ ExplodingPalm" not in text.split("'last_changes'")[1][:400]:
    text = re.sub(r"('last_changes',\s*\")", lambda mm: mm.group(1) + bullet, text, count=1)
    print("last_changes appended")
else:
    print("last_changes already has DrQ")

META.write_text(text, encoding="utf-8")
print(f"version {ver} -> {ver + 1}")
