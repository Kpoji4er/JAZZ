"""Install the AK-103 export as one bounded transaction across jazz + jazz_assets.

    python docs/tools/_integrate_ak103.py --export-root <ExportedEntities> \
        --build <_ak103_jazz_build> --game-root <JA3_ROOT> [--apply]

Dry run by default. Requires the game and Mod Editor closed. Core files are
backed up under <build>/integration-backup before anything is written.

Spec: JAZZ-WEAPON-AK103-001. Geometry: "AK 103" by Frostoise, CC Attribution.
`--replace-assets` restages entities and icons over an already installed AK103
without touching items.lua, metadata or the companion.
"""

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from _integrate_sr3m import ROOT, ASSETS, matching, write, add_metadata, append_root_item

WEAPON = "AK103"
ENTITY = "AKR_" + WEAPON
ENTITIES = [
    ENTITY,
    ENTITY + "_Handguard",
    ENTITY + "_Magazine",
    ENTITY + "_Muzzle",
    ENTITY + "_Stock",
    ENTITY + "_StockFolded",
]

TEXTS = {
    "DisplayName": (761915304101, "АК-103", "AK-103"),
    "DisplayNamePlural": (761915304102, "АК-103", "AK-103"),
    "Description": (
        761915304103,
        "Автомат сотой серии под патрон 7,62x39 мм с полимерным складным прикладом. "
        "Использует общие магазины АКМ на 30, 40 и 75 патронов.",
        "A 100-series rifle in 7.62x39 mm with a folding polymer stock. "
        "It feeds from the shared AKM 30-, 40- and 75-round magazines.",
    ),
}

# Owner decision 2026-09-19: top of the 7.62x39 line for the higher tier
# (AK47 28, AKM 27), otherwise between AKM and AK74M.
STATS = {
    "comment": '"Tier 3-1"',
    "Damage": "29",
    "WeaponRange": "42",
    "AimAccuracy": "11",
    "ShootAP": "5000",
    "ReloadAP": "6000",
    "Recoil": "24",
    "CyclicRPM": "600",
    "MagazineSize": "30",
    "Noise": "55",
    "WeaponMass": "34",
    "Cost": "15000",
    "CanAppearInShop": "true",
    "Tier": "4",
    "MaxStock": "1",
    "RestockWeight": "40",
    "Entity": f'"{ENTITY}"',
    "Icon": f'"Mod/e6L4ECj/WeaponIcons/{WEAPON}.png"',
}

# Folding polymer stock, as on AK74M/AK105 rather than AKM's fixed wood.
STOCK_SLOT = (
    "PlaceObj('WeaponComponentSlot', {\n"
    "\t\t\t'SlotType', \"Stock\",\n"
    "\t\t\t'AvailableComponents', {\n"
    "\t\t\t\t\"JAZZ_StockLightUnFolded\",\n"
    "\t\t\t\t\"JAZZ_StockLightFolded\",\n"
    "\t\t\t},\n"
    "\t\t\t'DefaultComponent', \"JAZZ_StockLightUnFolded\",\n"
    "\t\t})"
)
MUZZLE_SLOT = (
    "PlaceObj('WeaponComponentSlot', {\n"
    "\t\t\t'SlotType', \"Muzzle\",\n"
    "\t\t\t'AvailableComponents', {\n"
    "\t\t\t\t\"JAZZ_DefMuzzle\",\n"
    "\t\t\t\t\"JAZZ_Compensator\",\n"
    "\t\t\t\t\"JAZZ_Suppressor\",\n"
    "\t\t\t\t\"JAZZ_SuppressorImproved\",\n"
    "\t\t\t},\n"
    "\t\t\t'DefaultComponent', \"JAZZ_DefMuzzle\",\n"
    "\t\t})"
)

VISUALS = {
    "JAZZ_MagNormal": (ENTITY + "_Magazine", "Magazine"),
    "JAZZ_Handguard": (ENTITY + "_Handguard", "Handguard"),
    "JAZZ_DefMuzzle": (ENTITY + "_Muzzle", "Muzzle"),
    "JAZZ_StockLightUnFolded": (ENTITY + "_Stock", "Stock"),
    "JAZZ_StockLightFolded": (ENTITY + "_StockFolded", "Stock"),
}

SUFFIXES = {
    "BaseColorMap": "Base",
    "NormalMap": "Norm",
    "RMMap": "RM",
    "AOMap": "AO",
    "SpecialMap": "SPEC",
    "SIMap": "SI",
    "ColorizationMap": "Color",
}


def replace_slot(text, slot, replacement):
    match = re.search(r"'SlotType',\s*\"" + slot + '"', text)
    assert match, slot
    start = text.rfind("PlaceObj('WeaponComponentSlot'", 0, match.start())
    end = matching(text, text.index("(", start))
    return text[:start] + replacement + text[end:]


def companion():
    """AK-103 grows out of AKM: same calibre, same magazines, same FX."""
    text = (ROOT / "InventoryItem/AKM.lua").read_text(encoding="utf-8")
    text = text.replace("UndefineClass('AKM')", f"UndefineClass('{WEAPON}')")
    text = text.replace("DefineClass.AKM =", f"DefineClass.{WEAPON} =")

    for field, (ident, russian, _) in TEXTS.items():
        text, n = re.subn(
            r"^\t" + field + r" = .*$",
            f'\t{field} = T({ident}, --[[ModItemInventoryItemCompositeDef {WEAPON} {field}]] "{russian}"),',
            text,
            flags=re.M,
        )
        assert n == 1, field
    text = re.sub(r"^\tAdditionalHint = .*\n", "", text, flags=re.M)

    for field, value in STATS.items():
        text, n = re.subn(r"^\t" + field + r" = [^\n]+", f"\t{field} = {value},", text, flags=re.M)
        assert n == 1, field

    # AKM has no explicit fxClass, so name it here to inherit the whole profile.
    text = text.replace(f'\tEntity = "{ENTITY}",', f'\tEntity = "{ENTITY}",\n\tfxClass = "AKM",')
    text = replace_slot(text, "Stock", STOCK_SLOT)
    text = replace_slot(text, "Muzzle", MUZZLE_SLOT)

    props = text[text.index("\tcomment ="): text.rfind("}")]
    props = re.sub(r"^\t([A-Za-z_][A-Za-z_0-9]*) = ", r"\t'\1', ", props, flags=re.M)
    item = (
        "\tPlaceObj('ModItemInventoryItemCompositeDef', {\n"
        "\t\t'Group', \"JAZZ - Firearm - Rifles-AR\",\n"
        f"\t\t'Id', \"{WEAPON}\",\n" + props + "\t}),"
    )
    return text, item


def stage_assets(export, build, game_root):
    """Numeric export DDS get stable names before they ever reach the package."""
    staged = build / "mod-assets-stage"
    if staged.exists():
        assert staged.resolve().parent == build.resolve(), "Stage escaped build directory"
        assert not staged.is_symlink(), "Refusing a linked staging directory"
        shutil.rmtree(staged)
    staged.mkdir(parents=True)
    convert = str(Path(game_root) / "ModTools/hgimgcvt.exe")
    assert Path(convert).is_file(), convert

    names = {}
    for ent in ENTITIES:
        tree = ET.parse(export / (ent + ".ent"))
        tree.getroot().set("name", ent)
        for lod in tree.findall(".//lod"):
            for src in list(lod.findall("src")):
                lod.remove(src)
        for node in tree.findall(".//mesh"):
            rel = node.attrib["file"]
            dest = staged / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(export / rel, dest)
        for node in tree.findall(".//material"):
            rel = node.attrib["file"]
            mtl = ET.parse(export / rel)
            for tag in mtl.getroot().iter():
                name = tag.get("Name")
                if not name or tag.tag not in SUFFIXES:
                    continue
                src = export / "Textures" / name
                assert src.is_file(), src
                key = (SUFFIXES[tag.tag], hashlib.sha256(src.read_bytes()).hexdigest())
                if key not in names:
                    names[key] = f"{ENTITY}_{len(names)}_{SUFFIXES[tag.tag]}.dds"
                new = names[key]
                dest = staged / "Textures" / new
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    subprocess.run(
                        [convert, str(src), str(dest), "--truncate", "2048"],
                        check=True, capture_output=True,
                    )
                    fallback = staged / "Textures/Fallbacks" / new
                    fallback.parent.mkdir(parents=True, exist_ok=True)
                    subprocess.run(
                        [convert, str(dest), str(fallback), "--truncate", "64"],
                        check=True, capture_output=True,
                    )
                tag.set("Name", new)
            dest = staged / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            mtl.write(dest, encoding="utf-8", xml_declaration=True)
        tree.write(staged / (ent + ".ent"), encoding="utf-8", xml_declaration=True)
        write(staged / (ent + ".lua"), f'EntityData["{ent}"] = {{\n\teditor_artset = "Mods",\n}}\n')
    return staged, sorted({n for n in names.values()})


def replace_installed_assets(staged, textures, build, apply):
    copies = {
        ROOT / f"WeaponIcons/{WEAPON}.png": build / f"{WEAPON}_icon.png",
        ROOT / f"WeaponComponents/Magazine/{WEAPON}_Native30.png": build / f"{WEAPON}_Magazine_icon.png",
    }
    for src in staged.rglob("*"):
        if src.is_file():
            copies[ASSETS / "Entities" / src.relative_to(staged)] = src
    stale = []
    for folder in (
        ASSETS / "Entities/Textures",
        ASSETS / "Entities/Textures/Fallbacks",
    ):
        if not folder.is_dir():
            continue
        for path in folder.glob(f"{ENTITY}_*"):
            if path.name not in textures:
                stale.append(path)
    plan = {
        "apply": apply,
        "mode": "replace-assets",
        "entities": ENTITIES,
        "textures": textures,
        "files": len(copies),
        "stale": [str(p) for p in stale],
    }
    if not apply:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        print("\nDRY RUN: nothing written. Re-run with --apply --replace-assets.")
        return
    running = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "@(Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue).Count"],
        check=True, capture_output=True, text=True,
    )
    assert running.stdout.strip() == "0", "Close JA3 before replacing resources"
    # A texture may have acquired another consumer since the initial import.
    touched_materials = {p.resolve() for p in copies if p.suffix == ".mtl"}
    for material in (ASSETS / "Entities/Materials").glob("*.mtl"):
        if material.resolve() not in touched_materials:
            contents = material.read_text(encoding="utf-8")
            assert not any(p.name in contents for p in stale), material
    for dest in [*copies, *stale]:
        package = ROOT if dest.is_relative_to(ROOT) else ASSETS
        backup = build / "repair-install-backup" / package.name / dest.relative_to(package)
        if dest.exists() and not backup.exists():
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, backup)
    (build / "repair-install-plan.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    for dest, src in copies.items():
        assert src.is_file(), src
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    for path in stale:
        path.unlink()
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    print(f"\nReplaced {WEAPON} assets: {len(ENTITIES)} entities, {len(textures)} textures.")


def insert_assault_item(text, item):
    """Insert next to AK74M in the actual editor folder, not merely preset Group."""
    anchor_id = text.index("'Id', \"AK74M\"")
    anchor = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, anchor_id)
    folder = text.rfind("PlaceObj('ModItemFolder'", 0, anchor)
    assert '"JAZZ - Firearm - Rifles-Assault"' in text[folder:anchor]
    assert matching(text, text.index('(', folder)) > anchor_id
    start = text.rfind('\n', 0, anchor) + 1
    indent = text[start:anchor]
    lines = item.strip('\n').splitlines()
    margin = len(lines[0]) - len(lines[0].lstrip())
    placed = '\n'.join(indent + line[margin:] for line in lines)
    return text[:start] + placed + '\n' + text[start:]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--export-root", required=True, type=Path)
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--game-root", required=True, type=Path)
    p.add_argument("--apply", action="store_true")
    p.add_argument(
        "--replace-assets",
        action="store_true",
        help="overwrite installed AKR_AK103* meshes/textures/icons; leave ModItem alone",
    )
    args = p.parse_args()
    export = args.export_root.resolve()
    build = args.build.resolve()

    items = (ROOT / "items.lua").read_text(encoding="utf-8")
    installed = bool(re.search(r"'Id',\s*\"" + WEAPON + '"', items))
    if args.replace_assets:
        assert installed, "replace-assets needs an already installed AK103"
    else:
        assert not installed, "Already integrated"
        for ident, _, _ in TEXTS.values():
            assert str(ident) not in items, f"Localization ID collision: {ident}"
    for ent in ENTITIES:
        assert (export / (ent + ".ent")).is_file(), ent

    staged, textures = stage_assets(export, build, args.game_root)
    if args.replace_assets:
        replace_installed_assets(staged, textures, build, args.apply)
        return

    text, item = companion()
    items = insert_assault_item(items, item)
    for ident, (entity, slot) in VISUALS.items():
        match = re.search(r'\bid\s*=\s*"' + ident + '"', items)
        assert match, ident
        start = items.rfind("PlaceObj('ModItemWeaponComponent'", 0, match.start())
        end = matching(items, items.index("(", start))
        block = items[start:end]
        visual = (
            "PlaceObj('WeaponComponentVisual', { "
            f'ApplyTo = "{WEAPON}", Entity = "{entity}", Slot = "{slot}", param_bindings = false'
        )
        if slot == "Magazine":
            visual += f', Icon = "Mod/e6L4ECj/WeaponComponents/Magazine/{WEAPON}_Native30.png"'
        visual += " })"
        block, n = re.subn(r"Visuals\s*=\s*\{", "Visuals = {\n\t\t\t" + visual + ",", block, count=1)
        assert n == 1, ident
        items = items[:start] + block + items[end:]

    meta = add_metadata((ROOT / "metadata.lua").read_text(encoding="utf-8"), "code",
                        [f'"InventoryItem/{WEAPON}.lua"'])
    meta = add_metadata(meta, "affected_resources", [
        "PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", "
        f"'Id', \"{WEAPON}\", 'ClassDisplayName', \"Inventory item\" }})"
    ])

    asset_items = (ASSETS / "items.lua").read_text(encoding="utf-8")
    folder = f"\tPlaceObj('ModItemFolder', {{ 'name', \"{WEAPON}\" }}, {{\n"
    for ent in ENTITIES:
        folder += (
            f"\t\tPlaceObj('ModItemEntity', {{ 'name', \"{ent}\", "
            f"'ClassParents', {{}}, 'entity_name', \"{ent}\" }}),\n"
        )
    folder += "\t}),"
    asset_items = append_root_item(asset_items, folder)
    asset_meta = (ASSETS / "metadata.lua").read_text(encoding="utf-8")
    asset_meta = add_metadata(asset_meta, "entities", ['"' + e + '"' for e in ENTITIES])
    asset_meta = add_metadata(asset_meta, "code", ['"Entities/' + e + '.lua"' for e in ENTITIES])

    copies = {
        ROOT / f"WeaponIcons/{WEAPON}.png": build / f"{WEAPON}_icon.png",
        ROOT / f"WeaponComponents/Magazine/{WEAPON}_Native30.png": build / f"{WEAPON}_Magazine_icon.png",
    }
    for src in staged.rglob("*"):
        if src.is_file():
            copies[ASSETS / "Entities" / src.relative_to(staged)] = src
    for dest, src in copies.items():
        assert src.is_file(), src
        assert not dest.exists(), f"Would overwrite: {dest}"

    plan = {
        "apply": args.apply,
        "entities": ENTITIES,
        "textures": textures,
        "files_new": len(copies),
        "lua_edited": [
            "jazz/items.lua", "jazz/metadata.lua", f"jazz/InventoryItem/{WEAPON}.lua",
            "jazz_assets/items.lua", "jazz_assets/metadata.lua",
        ],
        "visuals": {k: v[0] for k, v in VISUALS.items()},
        "stats": STATS,
    }
    if not args.apply:
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        print("\nDRY RUN: nothing written. Re-run with --apply.")
        return

    backup = build / "integration-backup"
    originals = {
        ROOT / "items.lua": None, ROOT / "metadata.lua": None,
        ASSETS / "items.lua": None, ASSETS / "metadata.lua": None,
    }
    for path in originals:
        originals[path] = path.read_bytes()
        package = ROOT if path.is_relative_to(ROOT) else ASSETS
        dest = backup / package.name / path.relative_to(package)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(originals[path])

    for dest, src in copies.items():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    write(ROOT / f"InventoryItem/{WEAPON}.lua", text)
    write(ROOT / "items.lua", items)
    write(ROOT / "metadata.lua", meta)
    write(ASSETS / "items.lua", asset_items)
    write(ASSETS / "metadata.lua", asset_meta)

    stage = build / "mod-data-stage"
    stage.mkdir(exist_ok=True)
    (stage / "texts.json").write_text(
        json.dumps({k: list(v) for k, v in TEXTS.items()}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    print(f"\nInstalled {WEAPON}: {len(ENTITIES)} entities, {len(VISUALS)} component visuals, "
          f"{len(textures)} textures. Localization staged, runtime QA pending.")


if __name__ == "__main__":
    main()
