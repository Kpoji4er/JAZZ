# -*- coding: utf-8 -*-
"""Ensure JAZZ-IMP-001 metadata code + ModResourcePreset entries; bump revision."""
from pathlib import Path

path = Path(r"C:/Users/SsAnd/AppData/Roaming/Jagged Alliance 3/Mods/jazz/metadata.lua")
text = path.read_text(encoding="utf-8")

# Code entries after SatelliteSquad
needle_code = '\t\t"Code/SatelliteSquad.lua",\n'
insert_code = (
    '\t\t"Code/SatelliteSquad.lua",\n'
    '\t\t"Code/System_IMP_StartingGear.lua",\n'
    '\t\t"Code/System_IMP_Perks.lua",\n'
)
if "Code/System_IMP_StartingGear.lua" not in text:
    if needle_code not in text:
        raise SystemExit("SatelliteSquad code entry not found")
    text = text.replace(needle_code, insert_code, 1)
    print("added Code IMP entries")
else:
    print("Code IMP entries already present")

# CharacterEffect companions after Conrad
needle_ce = '\t\t"CharacterEffect/Jazz_Perk_Conrad.lua",\n'
insert_ce = (
    '\t\t"CharacterEffect/Jazz_Perk_Conrad.lua",\n'
    '\t\t"CharacterEffect/Jazz_Perk_Mimicry.lua",\n'
    '\t\t"CharacterEffect/Jazz_Perk_Veteran.lua",\n'
    '\t\t"CharacterEffect/Jazz_Perk_Sniper.lua",\n'
)
if "CharacterEffect/Jazz_Perk_Mimicry.lua" not in text:
    if needle_ce not in text:
        raise SystemExit("Conrad CharacterEffect entry not found")
    text = text.replace(needle_ce, insert_ce, 1)
    print("added CharacterEffect IMP entries")
else:
    print("CharacterEffect IMP entries already present")

# ModResourcePreset after Jazz_Perk_Lynx CharacterEffect
needle_res = """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CharacterEffectCompositeDef\",
\t\t\t'Id', \"Jazz_Perk_Lynx\",
\t\t\t'ClassDisplayName', \"Character effect\",
\t\t}),
"""
insert_res = needle_res + """\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CharacterEffectCompositeDef\",
\t\t\t'Id', \"Jazz_Perk_Mimicry\",
\t\t\t'ClassDisplayName', \"Character effect\",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CharacterEffectCompositeDef\",
\t\t\t'Id', \"Jazz_Perk_Veteran\",
\t\t\t'ClassDisplayName', \"Character effect\",
\t\t}),
\t\tPlaceObj('ModResourcePreset', {
\t\t\t'Class', \"CharacterEffectCompositeDef\",
\t\t\t'Id', \"Jazz_Perk_Sniper\",
\t\t\t'ClassDisplayName', \"Character effect\",
\t\t}),
"""
if "'Id', \"Jazz_Perk_Mimicry\"" not in text:
    if needle_res not in text:
        raise SystemExit("Jazz_Perk_Lynx ModResourcePreset not found")
    text = text.replace(needle_res, insert_res, 1)
    print("added ModResourcePreset IMP entries")
else:
    print("ModResourcePreset IMP entries already present")

# Bump version
import re
m = re.search(r"'version',\s*(\d+)", text)
if not m:
    raise SystemExit("version not found")
ver = int(m.group(1))
text = text.replace(m.group(0), f"'version', {ver + 1}", 1)
print("version", ver, "->", ver + 1)

# Append last_changes
bullet = "- IMP-001: JA2-style starting gear from stats/perks; Mimicry/Veteran/Sniper; no empty ammo packs on hire [new game recommended]\n"
lc = re.search(r"'last_changes',\s*\"", text)
if not lc:
    raise SystemExit("last_changes not found")
# find start of string value
start = lc.end()
# only append if not already there
if "IMP-001:" not in text[start : start + 400]:
    text = text[:start] + bullet + text[start:]
    print("appended last_changes")
else:
    print("last_changes already has IMP-001")

path.write_text(text, encoding="utf-8")
print("metadata.lua written")
