# -*- coding: utf-8 -*-
"""Remove withdrawn JAZZ_SpecOpsBody_Male + JAZZ_Legion_SpecOpsTest (JAZZ-APPEAR-001-REQ-023)."""
from __future__ import annotations

import sys
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
ASSETS = JAZZ.parent / "jazz_assets"
UNITS = JAZZ.parent / "jazz-units"

ASSET_FILES = (
    ASSETS / "Entities" / "JAZZ_SpecOpsBody_Male.ent",
    ASSETS / "Entities" / "JAZZ_SpecOpsBody_Male.lua",
    ASSETS / "Entities" / "Materials" / "JAZZ_SpecOpsBody_Male_mesh.mtl",
    ASSETS / "Entities" / "Meshes" / "JAZZ_SpecOpsBody_Male_mesh.m.hgm",
    ASSETS / "Entities" / "Textures" / "JAZZ_SpecOpsBody_1_Norm.dds",
    ASSETS / "Entities" / "Textures" / "JAZZ_SpecOpsBody_2_Base.dds",
    ASSETS / "Entities" / "Textures" / "JAZZ_SpecOpsBody_3_RM.dds",
    ASSETS / "Entities" / "Textures" / "Fallbacks" / "JAZZ_SpecOpsBody_1_Norm.dds",
    ASSETS / "Entities" / "Textures" / "Fallbacks" / "JAZZ_SpecOpsBody_2_Base.dds",
    ASSETS / "Entities" / "Textures" / "Fallbacks" / "JAZZ_SpecOpsBody_3_RM.dds",
)
UNIT_FILES = (UNITS / "UnitData" / "JAZZ_Legion_SpecOpsTest.lua",)

REPLACEMENTS = (
    (
        ASSETS / "metadata.lua",
        (
            '\t\t"JAZZ_SpecOpsBody_Male",\n\n',
            '\t\t"Entities/JAZZ_SpecOpsBody_Male.lua",\n\n',
        ),
    ),
    (
        UNITS / "metadata.lua",
        (
            '\t\t"UnitData/JAZZ_Legion_SpecOpsTest.lua",\n\n',
            '\t\tPlaceObj(\'ModResourcePreset\', { \'Class\', "UnitDataCompositeDef", \'Id\', "JAZZ_Legion_SpecOpsTest", \'ClassDisplayName\', "Unit" }),\n\n',
            '\t\tPlaceObj(\'ModResourcePreset\', { \'Class\', "AppearancePreset", \'Id\', "JAZZ_Legion_SpecOpsTest", \'ClassDisplayName\', "Appearance preset" }),\n\n',
        ),
    ),
    (
        ASSETS / "items.lua",
        (
            'PlaceObj(\'ModItemEntity\', { \'name\', "JAZZ_SpecOpsBody_Male", \'entity_name\', "JAZZ_SpecOpsBody_Male", \'ClassParents\', { "CharacterBodyMale" } }),\n',
        ),
    ),
)


def replace_once(path: Path, needles: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            raise SystemExit(f"FAIL missing needle in {path}: {needle[:80]!r}")
        text = text.replace(needle, "", 1)
        if needle in text:
            raise SystemExit(f"FAIL needle still present in {path}: {needle[:80]!r}")
    path.write_text(text, encoding="utf-8", newline="\n")


def strip_units_items() -> None:
    path = UNITS / "items.lua"
    text = path.read_text(encoding="utf-8")
    start = text.find("PlaceObj('ModItemAppearancePreset', {\n    Head = \"\",\n    Pants = \"\",\n    Hat = \"\",\n    Hat2 = \"\",\n    Hair = \"\",\n    Armor = \"\",\n    Shirt = \"\",\n    Chest = \"\",\n    Hip = \"\",\n    Body = \"JAZZ_SpecOpsBody_Male\",")
    if start < 0:
        raise SystemExit(f"FAIL SpecOps AppearancePreset not found in {path}")
    end_marker = "PlaceObj('ModItemUnitDataCompositeDef', {\n    'Group', \"JAZZ Tests\",\n    'Id', \"JAZZ_Legion_ArmorTest_FlakM1955\","
    end = text.find(end_marker, start)
    if end < 0:
        raise SystemExit(f"FAIL FlakM1955 marker not found after SpecOps in {path}")
    path.write_text(text[:start] + text[end:], encoding="utf-8", newline="\n")


def unlink(paths: tuple[Path, ...]) -> int:
    removed = 0
    for path in paths:
        if path.is_file():
            path.unlink()
            removed += 1
        else:
            print(f"SKIP missing {path}")
    return removed


def main() -> int:
    for path, needles in REPLACEMENTS:
        replace_once(path, needles)
    strip_units_items()
    removed = unlink(ASSET_FILES) + unlink(UNIT_FILES)
    print(f"OK removed files={removed}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"FAIL: {exc}\n")
        raise SystemExit(1)
