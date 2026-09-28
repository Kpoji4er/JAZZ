"""JAZZ-WEAPON-M14-FAMILY-001: copy unique donor meshes/textures to a temp build.

Does not write to jazz or jazz_assets. Archives are read-only.

  python docs/tools/_extract_m14_family_sources.py --output D:/jazz_m14_build/src
"""
import argparse
import hashlib
import zipfile
from pathlib import Path

ARCHIVES = Path(r'E:\JaWeapons\Weapons\M14')
ZIPS = {
    'lego': 'M14 Lego.zip',
    'uniq': 'M14 UNIQ.zip',
    'mk14': 'Mk 14 Custom.zip',
}


def unique_objs(zf):
    seen = {}
    order = []
    for info in zf.infolist():
        if info.is_dir() or not info.filename.lower().endswith('.obj'):
            continue
        data = zf.read(info)
        key = hashlib.sha1(data).hexdigest()[:12]
        if key in seen:
            continue
        seen[key] = info.filename
        order.append((info.filename, data))
    return order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    for key, name in ZIPS.items():
        dest = out / key
        dest.mkdir(exist_ok=True)
        with zipfile.ZipFile(ARCHIVES / name) as zf:
            objs = unique_objs(zf)
            for i, (fname, data) in enumerate(objs):
                (dest / ('part_%02d.obj' % i)).write_bytes(data)
                print(key, 'part_%02d' % i, fname, len(data) // 1024, 'KB')
            for info in zf.infolist():
                if info.is_dir():
                    continue
                low = info.filename.lower()
                if low.endswith('.png') or low.endswith('.tga'):
                    (dest / Path(info.filename).name).write_bytes(zf.read(info))
                    print(key, 'tex', Path(info.filename).name)
    print('EXTRACT_OK', out)


if __name__ == '__main__':
    main()
