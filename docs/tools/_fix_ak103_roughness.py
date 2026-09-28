"""Rescale AK-103 roughness and reinstall RM DDS through the official pipeline.

    python docs/tools/_fix_ak103_roughness.py --build <_ak103_jazz_build> \
        --game-root <JA3_ROOT> [--target 0.45] [--apply]

hgimgcvt --truncate accepts DDS only, not TGA. This script therefore:

1. backs up the original RM TGA
2. rescales the R channel to the accepted AK family mean (default 0.45)
3. writes TARGA_RAW through Blender so AssetsProcessor can read the files
4. recompiles the existing FBX
5. copies the new RM DDS over the already installed named files
6. rebuilds 64px fallbacks with hgimgcvt from those DDS

Metallic and base colour are not touched. Geometry, spots and items stay as is.
"""

import argparse
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image

from _integrate_sr3m import ASSETS

ENTITY = "AKR_AK103"
WEAPON = "AK103"


def rm_sources(build):
    return sorted((build / "Textures").glob(f"{ENTITY}_*_RM.tga"))


def backup_originals(build):
    backup = build / "roughness-backup"
    backup.mkdir(exist_ok=True)
    for src in rm_sources(build):
        dest = backup / src.name
        if not dest.is_file():
            shutil.copy2(src, dest)
            print(f"backed up {src.name}")
        else:
            shutil.copy2(dest, src)
            print(f"restored {src.name} from backup")


def preview(path, target):
    image = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32)
    rough = image[..., 0] / 255.0
    metal = image[..., 2] / 255.0
    mean = float(rough.mean()) or 1.0
    factor = target / mean
    after = float(np.clip(rough * factor, 0.0, 1.0).mean())
    return mean, after, factor, float(metal.mean())


def write_scaled(path, target):
    image = np.asarray(Image.open(path).convert("RGBA")).astype(np.float32)
    rough = image[..., 0] / 255.0
    mean = float(rough.mean()) or 1.0
    image[..., 0] = np.clip(rough * (target / mean), 0.0, 1.0) * 255.0
    Image.fromarray(image.astype(np.uint8)).save(path)


def rewrite_targa_raw(blender, paths):
    script = (
        "import bpy, sys\n"
        "from pathlib import Path\n"
        "paths = [Path(p) for p in sys.argv[sys.argv.index('--')+1:]]\n"
        "for path in paths:\n"
        "    im = bpy.data.images.load(str(path))\n"
        "    im.file_format = 'TARGA_RAW'\n"
        "    im.filepath_raw = str(path)\n"
        "    im.save()\n"
        "    bpy.data.images.remove(im)\n"
        "    print('targa', path.name)\n"
    )
    tmp = paths[0].parent / "_rewrite_targa.py"
    tmp.write_text(script, encoding="utf-8")
    try:
        subprocess.run(
            [str(blender), "--background", "--factory-startup", "--python", str(tmp),
             "--", *[str(p) for p in paths]],
            check=True,
        )
    finally:
        tmp.unlink(missing_ok=True)


def run_processor(game_root, fbx):
    exe = game_root / "ModTools/AssetsProcessor/AssetsProcessor.exe"
    assert exe.is_file(), exe
    subprocess.run(
        [str(exe), str(fbx), "-gamepath", str(game_root)],
        cwd=str(fbx.parents[3]),
        check=True,
    )


def rm_maps(mtl_path):
    return [n.get("Name") for n in ET.parse(mtl_path).findall(".//RMMap")]


def reinstall_rm(export, convert):
    unique = {}
    for mtl in sorted((ASSETS / "Entities/Materials").glob(f"{ENTITY}*_Mesh.mtl")):
        installed = rm_maps(mtl)
        exported = rm_maps(export / "Materials" / mtl.name)
        assert len(installed) == len(exported), mtl.name
        for old, new in zip(installed, exported):
            unique[old] = new
    copied = []
    for installed, numeric in unique.items():
        src = export / "Textures" / numeric
        dest = ASSETS / "Entities/Textures" / installed
        assert src.is_file(), src
        assert dest.is_file(), dest
        shutil.copy2(src, dest)
        fallback = ASSETS / "Entities/Textures/Fallbacks" / installed
        subprocess.run(
            [str(convert), str(dest), str(fallback), "--truncate", "64"],
            check=True,
            capture_output=True,
        )
        copied.append({"installed": installed, "from": numeric, "bytes": dest.stat().st_size})
    return copied


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--build", required=True, type=Path)
    p.add_argument("--game-root", required=True, type=Path)
    p.add_argument("--target", type=float, default=0.45)
    p.add_argument("--apply", action="store_true")
    p.add_argument(
        "--blender",
        type=Path,
        default=Path(r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"),
    )
    args = p.parse_args()
    build = args.build.resolve()
    game = args.game_root.resolve()
    convert = game / "ModTools/hgimgcvt.exe"
    fbx = build / "rigged" / f"{WEAPON}_JA3.fbx"
    export = Path(r"E:\JaWeapons\Weapons\ExportedEntities")
    assert convert.is_file(), convert
    assert fbx.is_file(), fbx
    assert args.blender.is_file(), args.blender

    sources = rm_sources(build)
    assert sources, "no RM maps"
    if args.apply:
        backup_originals(build)
        sources = rm_sources(build)
    for path in sources:
        before, after, factor, metal = preview(path, args.target)
        print(
            f"{path.name}: roughness {before:.2f} -> {after:.2f} "
            f"(x{factor:.2f}), metallic {metal:.2f} unchanged"
        )
    if not args.apply:
        print("dry-run, TGA and installed DDS not written")
        return

    for path in sources:
        write_scaled(path, args.target)
    rewrite_targa_raw(args.blender, sources)
    run_processor(game, fbx)
    copied = reinstall_rm(export, convert)
    print("reinstalled", copied)
    print("Roughness rescaled through AssetsProcessor. Reload the mod to see it.")


if __name__ == "__main__":
    main()
