"""Install an AssetsProcessor entity into jazz_assets/Entities.

AssetsProcessor writes textures under hash names; JAZZ-ASSETS-002 requires
``<Entity>_<MapSuffix>.dds``, so the maps are renamed and the .mtl is rewritten to
match while the files are copied out of ExportedEntities.

Usage:
    python install_character_element.py --entity JazzHat_SSh68 --mesh mesh \
        --mod-dir "<Mods>/Jazz Assets" [--exported "<AppData>/.../ExportedEntities"] [--dry-run]
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

MAP_SUFFIX = {
    "BaseColorMap": "Base",
    "NormalMap": "Norm",
    "RMMap": "RM",
    "AOMap": "AO",
    "SpecialMap": "SPEC",
    "SIMap": "SI",
    "ColorizationMap": "Color",
}
DEFAULT_EXPORTED = Path(os.getenv("APPDATA", "")) / "Jagged Alliance 3" / "ExportedEntities"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entity", required=True)
    parser.add_argument("--mesh", default="mesh")
    parser.add_argument("--mod-dir", required=True, type=Path)
    parser.add_argument("--exported", default=DEFAULT_EXPORTED, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def copy(src: Path, dst: Path, dry_run: bool):
    print(f"  {src.name} -> {dst}")
    if dry_run:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    args = parse_args()
    entity, mesh = args.entity, args.mesh
    stem = f"{entity}_{mesh}"
    entities = args.mod_dir / "Entities"

    ent_src = args.exported / f"{entity}.ent"
    mesh_src = args.exported / "Meshes" / f"{stem}.m.hgm"
    mtl_src = args.exported / "Materials" / f"{stem}.mtl"
    missing = [p for p in (ent_src, mesh_src, mtl_src) if not p.is_file()]
    if missing:
        print("missing exporter output: " + ", ".join(str(p) for p in missing), file=sys.stderr)
        return 1

    print(f"[install] {entity}")
    copy(ent_src, entities / f"{entity}.ent", args.dry_run)
    copy(mesh_src, entities / "Meshes" / f"{stem}.m.hgm", args.dry_run)

    mtl_text = mtl_src.read_text(encoding="utf-8")
    for slot, suffix in MAP_SUFFIX.items():
        match = re.search(rf'<{slot} Name="([^"]+)"', mtl_text)
        if not match:
            continue
        source_name = match.group(1)
        target_name = f"{entity}_{suffix}.dds"
        texture = args.exported / "Textures" / source_name
        if not texture.is_file():
            print(f"missing texture {texture}", file=sys.stderr)
            return 1
        copy(texture, entities / "Textures" / target_name, args.dry_run)
        mtl_text = mtl_text.replace(f'<{slot} Name="{source_name}"', f'<{slot} Name="{target_name}"')

    mtl_dst = entities / "Materials" / f"{stem}.mtl"
    print(f"  {mtl_src.name} -> {mtl_dst} (map names rewritten)")
    if not args.dry_run:
        mtl_dst.parent.mkdir(parents=True, exist_ok=True)
        mtl_dst.write_text(mtl_text, encoding="utf-8")

    lua_dst = entities / f"{entity}.lua"
    lua_text = (
        f'EntityData["{entity}"] = {{\n'
        f'\teditor_artset = "Mods",\n'
        f'\tentity = {{\n'
        f'\t\tclass_parent = "CharacterHat",\n'
        f'\t}},\n'
        f'}}'
    )
    print(f"  {lua_dst.name} (EntityData companion)")
    if not args.dry_run:
        lua_dst.write_text(lua_text, encoding="utf-8")

    print("[install] done; Mod Editor still owns items.lua registration and mtlbin rebuild")
    return 0


if __name__ == "__main__":
    sys.exit(main())
