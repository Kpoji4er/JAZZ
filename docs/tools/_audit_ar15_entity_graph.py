"""Verify the installed AR15 entity graph: meshes, materials, textures, fallbacks, registration."""
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

ASSETS = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz_assets")
ENT = ASSETS / "Entities"
NAMES = ["M16R_M16A4", "M16R_M16A4_Magazine", "M16R_M16A4_Magazine20",
         "M16R_M16A4_CarryHandle", "M16R_M16A4_RearSight",
         "M16R_M16A4_Handguard", "M16R_M16A4_HandguardRIS", "M16R_M16A4_Barrel",
         "M16R_M16A4_BarrelShort", "M16R_M16A4_Handgrip", "M16R_M16A4_DefMuzzle",
         "M16R_M16A4_Stock", "M16R_M16A4_StockLight",
         "M4R_M4A1", "M4R_M4A1_Magazine", "M4R_M4A1_Magazine20",
         "M4R_M4A1_Handguard", "M4R_M4A1_HandguardRIS",
         "M4R_M4A1_HandguardRifle", "M4R_M4A1_Stock", "M4R_M4A1_StockFolded",
         "M4R_M4A1_CarryHandle", "M4R_M4A1_RearSight", "M4R_M4A1_Barrel",
         "M4R_M4A1_BarrelShort", "M4R_M4A1_BarrelLong",
         "M4R_M4A1_Handgrip", "M4R_M4A1_DefMuzzle"]

items = (ASSETS / "items.lua").read_text(encoding="utf-8", errors="replace")
meta = (ASSETS / "metadata.lua").read_text(encoding="utf-8", errors="replace")
problems, textures = [], set()

for name in NAMES:
    ent = ENT / f"{name}.ent"
    if not ent.is_file():
        problems.append(f"{name}: .ent missing")
        continue
    tree = ET.parse(ent)
    if tree.getroot().get("name") != name:
        problems.append(f"{name}: root name attribute is {tree.getroot().get('name')!r}")
    if tree.findall(".//src"):
        problems.append(f"{name}: <src> present")
    for node in tree.findall(".//mesh") + tree.findall(".//material"):
        target = ENT / node.get("file")
        if not target.is_file():
            problems.append(f"{name}: missing {node.get('file')}")
    for node in tree.findall(".//material"):
        material = ET.parse(ENT / node.get("file"))
        for tag in material.getroot().iter():
            if tag.get("Name"):
                textures.add(tag.get("Name"))
    if not (ENT / f"{name}.lua").is_file():
        problems.append(f"{name}: EntityData lua missing")
    if f'\'entity_name\', "{name}"' not in items:
        problems.append(f"{name}: no ModItemEntity in jazz_assets/items.lua")
    if f'"{name}"' not in meta:
        problems.append(f"{name}: not in metadata entities")
    if f'"Entities/{name}.lua"' not in meta:
        problems.append(f"{name}: EntityData not in metadata code")

for texture in sorted(textures):
    for folder, limit in (("Textures", 2048), ("Textures/Fallbacks", 64)):
        path = ENT / folder / texture
        if not path.is_file():
            problems.append(f"{texture}: missing in {folder}")
            continue
        data = path.read_bytes()
        if data[:4] != b"DDS ":
            problems.append(f"{texture}: not a DDS in {folder}")
            continue
        h, w = struct.unpack("<II", data[12:20])
        if max(w, h) > limit:
            problems.append(f"{texture}: {w}x{h} exceeds {limit} in {folder}")

print(f"entities checked: {len(NAMES)}, textures referenced: {len(textures)}")
if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  -", p)
    raise SystemExit(1)
print("PASS: entity graph complete, no <src>, textures within 2048 and fallbacks within 64.")
