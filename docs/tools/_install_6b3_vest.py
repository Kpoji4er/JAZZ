"""Install the staged 6B3 vest entity, runtime map and isolated test unit.

python docs/tools/_install_6b3_vest.py --build-root <qa folder>
python docs/tools/_install_6b3_vest.py --build-root <qa folder> --apply

Requires the game/editor closed for --apply. Does not overwrite ArmorIcons/6b3.png.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from lupa import LuaRuntime
from _install_soft_legion_armor import validate
from _integrate_sr3m import add_metadata, append_root_item

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT.parent / 'jazz_assets'
UNITS = ROOT.parent / 'jazz-units'
ITEM = '6B3'
ENTITY = 'JAZZ_6B3_Male'
UID = 'JAZZ_Legion_ArmorTest_6B3'
ARMOR = 'JazzArmor_6B3'
MARKER = 'local armor_entities = {'
MAPPING = '\n\tJazzArmor_6B3 = { Male = "JAZZ_6B3_Male" },'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build-root', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--refresh', action='store_true', help='Replace only an existing, registered 6B3 resource graph')
    args = parser.parse_args()
    running = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         'Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],
        capture_output=True, text=True)
    if args.apply:
        assert not running.stdout.strip(), 'Game/editor is open; cannot install over its loaded data'
    build = args.build_root / 'build'
    stage = validate(build, ENTITY, ITEM)
    if args.refresh:
        pose = json.loads((args.build_root / 'poses/pose-check.json').read_text())
        compiled = json.loads((args.build_root / 'compiled-audit.json').read_text())
        assert pose['status'] == 'PASS_SKIN_STRUCTURE' and compiled['pass']
        assert ENTITY in (ASSETS / 'metadata.lua').read_text(encoding='utf-8')
        assert ENTITY in (ASSETS / 'items.lua').read_text(encoding='utf-8')
        writes = {}
        for source in stage.rglob('*'):
            if not source.is_file() or source.suffix == '.lua':
                continue
            assert source.name.startswith('JAZZ_6B3'), source
            target = ASSETS / 'Entities' / source.relative_to(stage)
            assert target.is_file(), ('Expected existing resource', target)
            writes[target] = source.read_bytes()
        if not args.apply:
            print('DRY RUN: replace', len(writes), 'existing 6B3 resources')
            return
        backup = args.build_root / 'refresh-backup'
        assert not backup.exists(), 'Refresh backup already exists'
        before = {path: path.read_bytes() for path in writes}
        for path, data in before.items():
            destination = backup / path.relative_to(ASSETS)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        try:
            for path, data in writes.items():
                assert path.read_bytes() == before[path], ('Concurrent edit', path)
                path.write_bytes(data)
            for path, data in writes.items():
                assert path.read_bytes() == data
        except Exception:
            for path, data in before.items():
                path.write_bytes(data)
            raise
        (args.build_root / 'refresh-installation.json').write_text(json.dumps({
            'installed': True, 'runtime': 'NOT_RUN', 'entity': ENTITY,
            'sha256': {str(path.relative_to(ASSETS)): hashlib.sha256(data).hexdigest()
                       for path, data in writes.items()},
        }, indent=2), encoding='utf-8')
        print('INSTALLED', len(writes), '6B3 resources; registration, unit, icon preserved')
        return
    icon = ROOT / 'ArmorIcons' / '6b3.png'
    assert icon.is_file() and icon.stat().st_size > 0, icon
    paths = [ASSETS / 'items.lua', ASSETS / 'metadata.lua',
             UNITS / 'items.lua', UNITS / 'metadata.lua',
             ROOT / 'Code/System_LegionArmorVisuals.lua']
    before = {path: path.read_bytes() for path in paths}
    texts = {path: data.decode('utf-8-sig') for path, data in before.items()}
    assert ENTITY not in texts[ASSETS / 'items.lua'], 'Already registered'
    assert UID not in texts[UNITS / 'items.lua'], 'Test unit already registered'
    assert MARKER in texts[ROOT / 'Code/System_LegionArmorVisuals.lua']
    assert 'JazzArmor_6B3 =' not in texts[ROOT / 'Code/System_LegionArmorVisuals.lua']
    texts[ROOT / 'Code/System_LegionArmorVisuals.lua'] = texts[
        ROOT / 'Code/System_LegionArmorVisuals.lua'].replace(MARKER, MARKER + MAPPING, 1)
    template = (UNITS / 'UnitData/JAZZ_Legion_ArmorTest.lua').read_text(encoding='utf-8-sig')
    companion = (template.replace('JAZZ_Legion_ArmorTest', UID)
                 .replace('JazzArmor_ImprovisedCuirass', ARMOR)
                 .replace('cuirass + MP40', '6B3 + MP40'))
    props = companion[companion.index('    comment ='):companion.rfind('}')]
    props = re.sub(r'^    (\w+) = ', r"    '\1', ", props, flags=re.M)
    record = ("PlaceObj('ModItemUnitDataCompositeDef', {\n"
              "    'Group', \"JAZZ Tests\",\n"
              f"    'Id', \"{UID}\",\n" + props + '}),')
    text = texts[UNITS / 'items.lua']
    pos = text.rfind('}')
    texts[UNITS / 'items.lua'] = text[:pos] + record + '\n' + text[pos:]
    texts[UNITS / 'metadata.lua'] = add_metadata(
        texts[UNITS / 'metadata.lua'], 'code', ['"UnitData/' + UID + '.lua"'])
    texts[UNITS / 'metadata.lua'] = add_metadata(
        texts[UNITS / 'metadata.lua'], 'affected_resources',
        ["PlaceObj('ModResourcePreset', { 'Class', \"UnitDataCompositeDef\", "
         f"'Id', \"{UID}\", 'ClassDisplayName', \"Unit\" }})"])
    entity_item = ("PlaceObj('ModItemEntity', {\n"
                   f"    'name', \"{ENTITY}\",\n"
                   "    'ClassParents', { \"CharacterArmorMale\" },\n"
                   f"    'entity_name', \"{ENTITY}\",\n}}),")
    texts[ASSETS / 'items.lua'] = append_root_item(texts[ASSETS / 'items.lua'], entity_item)
    texts[ASSETS / 'metadata.lua'] = add_metadata(
        texts[ASSETS / 'metadata.lua'], 'code', ['"Entities/' + ENTITY + '.lua"'])
    texts[ASSETS / 'metadata.lua'] = add_metadata(
        texts[ASSETS / 'metadata.lua'], 'entities', ['"' + ENTITY + '"'])
    writes = {}
    writes[UNITS / 'UnitData' / (UID + '.lua')] = companion.encode()
    for path in stage.rglob('*'):
        if path.is_file():
            writes[ASSETS / 'Entities' / path.relative_to(stage)] = path.read_bytes()
    writes[ASSETS / 'Entities' / (ENTITY + '.lua')] = (
        'EntityData["' + ENTITY + '"] = { editor_artset = "Mods", '
        'entity = { class_parent = "CharacterArmorMale" } }\n').encode()
    for path, text in texts.items():
        writes[path] = text.encode('utf-8')
    lua = LuaRuntime()
    for path, data in writes.items():
        if path.suffix == '.lua':
            lua.compile(data.decode('utf-8-sig'))
    for path, data in before.items():
        assert path.read_bytes() == data, 'Concurrent edit ' + str(path)
    if not args.apply:
        prepared = args.build_root / 'prepared-install'
        for path, data in writes.items():
            target = prepared / path.relative_to(ROOT.parent)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (args.build_root / 'planned-install.json').write_text(
            json.dumps({'installed': False,
                        'files': [str(path.relative_to(ROOT.parent)) for path in writes]},
                       indent=2), encoding='utf-8')
        print('PASS staging resources and Lua compilation; complete transaction prepared in',
              prepared)
        return
    backup = args.build_root / 'installation-backup'
    assert not backup.exists(), 'Backup already exists'
    snapshot = {path: path.read_bytes() if path.exists() else None for path in writes}
    for path, data in snapshot.items():
        if data is not None:
            dest = backup / path.relative_to(ROOT.parent)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
    try:
        for path, data in writes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        for path, data in writes.items():
            assert path.read_bytes() == data
    except Exception:
        for path, data in snapshot.items():
            if data is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(data)
        raise
    manifest = {
        'installed': True,
        'runtime': 'NOT_RUN',
        'units': [UID],
        'entity': ENTITY,
        'icon_preserved': str(icon.relative_to(ROOT)),
        'sha256': {str(path.relative_to(ROOT.parent)): hashlib.sha256(data).hexdigest()
                   for path, data in writes.items()},
    }
    (args.build_root / 'installation.json').write_text(
        json.dumps(manifest, indent=2), encoding='utf-8')
    print('INSTALLED', len(writes), 'files; entity', ENTITY, 'and test unit', UID)


if __name__ == '__main__':
    main()
