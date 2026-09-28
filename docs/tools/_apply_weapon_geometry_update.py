"""Install a geometry-only entity update: mesh HGM plus corrected .ent, nothing else.

python docs/tools/_apply_weapon_geometry_update.py --export-root <ExportedEntities>
    --backup <folder> --entity SR3M --entity L42A1 [--apply]

Used when a rebuild changed only vertices and attach spots. Materials, .mtl files and
DDS are deliberately left untouched, so the freshly exported numeric texture names never
enter the mod and `$rename-jazz-weapon-textures` is not needed. Dry-run by default.

AssetsProcessor leaves two things that must never reach the repository: an empty
`name` attribute and an absolute `<src>` path to the local FBX. Both are fixed here.
"""
import argparse
import hashlib
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT.parent / 'jazz_assets'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def clean_ent(source, name):
    tree = ET.parse(source)
    root = tree.getroot()
    root.set('name', name)
    for lod in root.findall('.//lod'):
        for src in list(lod.findall('src')):
            lod.remove(src)
    return tree


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--export-root', type=Path, required=True)
    p.add_argument('--backup', type=Path, required=True)
    p.add_argument('--entity', action='append', required=True)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    target = ASSETS / 'Entities'
    args.backup.mkdir(parents=True, exist_ok=True)

    plan = []
    for name in args.entity:
        ent = args.export_root / (name + '.ent')
        assert ent.is_file(), ent
        tree = clean_ent(ent, name)
        root = tree.getroot()
        mesh_rel = root.find('.//mesh').get('file')
        material_rel = root.find('.//material').get('file')
        new_mesh = args.export_root / mesh_rel
        assert new_mesh.is_file(), new_mesh
        installed_ent = target / (name + '.ent')
        installed_mesh = target / mesh_rel
        assert installed_ent.is_file(), 'Not an update: %s is not installed' % name
        assert installed_mesh.is_file(), installed_mesh
        # The kept .mtl must still describe the same material slots as the new mesh.
        assert (target / material_rel).is_file(), material_rel
        kept = len(ET.parse(target / material_rel).getroot().findall('Material'))
        fresh = len(ET.parse(args.export_root / material_rel).getroot().findall('Material'))
        assert kept == fresh, (name, 'material slot count changed', kept, fresh)
        box = root.find('.//box')
        spots = sorted(n.get('name') for n in root.findall('.//attach'))
        plan.append({'name': name, 'tree': tree, 'ent': installed_ent,
                     'mesh_src': new_mesh, 'mesh_dst': installed_mesh,
                     'materials': kept, 'spots': spots,
                     'box': (box.get('min'), box.get('max'))})

    for item in plan:
        old_spots = sorted(n.get('name') for n in
                           ET.parse(item['ent']).getroot().findall('.//attach'))
        added = [s for s in item['spots'] if s not in old_spots]
        removed = [s for s in old_spots if s not in item['spots']]
        print(f"{item['name']}: mesh {digest(item['mesh_dst'])} -> {digest(item['mesh_src'])}"
              f"  materials={item['materials']}  box={item['box'][0]} .. {item['box'][1]}")
        print(f"    spots {len(item['spots'])}: {' '.join(item['spots'])}")
        if added:
            print('    + added:', ' '.join(added))
        if removed:
            print('    - removed:', ' '.join(removed))

    if not args.apply:
        print('\nDry run. Re-run with --apply, game and Mod Editor closed.')
        return

    for item in plan:
        for path in (item['ent'], item['mesh_dst']):
            stamp = args.backup / f'{path.name}.{digest(path)}'
            if not stamp.exists():
                shutil.copy2(path, stamp)
        shutil.copy2(item['mesh_src'], item['mesh_dst'])
        item['tree'].write(item['ent'], encoding='utf-8', xml_declaration=True)
        written = ET.parse(item['ent']).getroot()
        assert written.get('name') == item['name']
        assert not written.findall('.//src'), 'Absolute source path leaked'
        print(f"applied {item['name']}: {item['mesh_dst'].name} + {item['ent'].name}")
    print('\nDone. Reload the mod from disk and check the editor message panel.')


if __name__ == '__main__':
    main()
