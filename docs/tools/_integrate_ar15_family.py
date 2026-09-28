"""Install the staged M16A4 / M4A1 remasters (JAZZ-WEAPON-AR15-FAMILY-001, phase 2).

  python docs/tools/_integrate_ar15_family.py --build <build> [--apply]

Dry run by default: prints the planned edits and validates that every text still compiles.
With --apply it backs up every touched file under <build>/integration-backup first and
refuses to write if any of them changed since it read them (concurrent editor save).

Scope: repoint both hosts at the new entity graphs and wire the modules that already have
component IDs (magazine, M4 stock pair, M4 handguard, iron sights). The rail handguard and
the detachable carry handle need new component IDs plus RU/EN strings and are deliberately
left for a follow-up; their entities are staged and registered, unused for now.
"""
import argparse
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

from lupa import LuaRuntime

from _integrate_sr3m import ASSETS, ROOT, add_metadata, append_root_item, matching, write

ENTITIES = {
    'M16A4': ['M16R_M16A4', 'M16R_M16A4_Magazine', 'M16R_M16A4_CarryHandle',
              'M16R_M16A4_RearSight', 'M16R_M16A4_Handguard', 'M16R_M16A4_HandguardRIS',
              'M16R_M16A4_Barrel', 'M16R_M16A4_BarrelShort'],
    'M4A1': ['M4R_M4A1', 'M4R_M4A1_Magazine', 'M4R_M4A1_Handguard', 'M4R_M4A1_HandguardRIS',
             'M4R_M4A1_HandguardRifle', 'M4R_M4A1_Stock', 'M4R_M4A1_StockFolded',
             'M4R_M4A1_CarryHandle', 'M4R_M4A1_RearSight', 'M4R_M4A1_Barrel',
             'M4R_M4A1_BarrelShort', 'M4R_M4A1_BarrelLong'],
}
HOST = {'M16A4': 'M16R_M16A4', 'M4A1': 'M4R_M4A1'}
# component id -> (slot, entity suffix). Only IDs that already exist.
WIRING = {
    'M16A4': {
        'JAZZ_MagNormal': ('Magazine', 'Magazine'),
        'JAZZ_MagNormalG18': ('Magazine', 'Magazine'),
        'JAZZ_DefaultIronsight_AR15': ('Scope', 'RearSight'),
        'JAZZ_BarrelNormal': ('Barrel', 'Barrel'),
        'JAZZ_BarrelShort': ('Barrel', 'BarrelShort'),
        'JAZZ_Handguard': ('Handguard', 'Handguard'),
        'JAZZ_Handguard_RIS': ('Handguard', 'HandguardRIS'),
        'JAZZ_CarryHandle_AR15': ('Scope', 'CarryHandle'),
    },
    'M4A1': {
        'JAZZ_MagNormal': ('Magazine', 'Magazine'),
        'JAZZ_MagNormalG18': ('Magazine', 'Magazine'),
        'JAZZ_Handguard': ('Handguard', 'Handguard'),
        'JAZZ_Handguard_RIS': ('Handguard', 'HandguardRIS'),
        'JAZZ_StockLightUnFolded': ('Stock', 'Stock'),
        'JAZZ_StockLightFolded': ('Stock', 'StockFolded'),
        'JAZZ_UnfoldStocks': ('Stock', 'Stock'),
        'JAZZ_IronSight': ('Scope', 'RearSight'),
        'JAZZ_BarrelNormal': ('Barrel', 'Barrel'),
        'JAZZ_BarrelShort': ('Barrel', 'BarrelShort'),
        'JAZZ_BarrelLong': ('Barrel', 'BarrelLong'),
        'JAZZ_CarryHandle_AR15': ('Scope', 'CarryHandle'),
    },
}
HANDGUARD_SLOT = """		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'AvailableComponents', {
				"JAZZ_Handguard",
			},
			'DefaultComponent', "JAZZ_Handguard",
		}),
"""


def item_block(text, ident):
    m = re.search(r"'Id',\s*\"" + ident + r"\",", text)
    assert m, ident
    start = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef'", 0, m.start())
    return start, matching(text, text.index('(', start))


def wire_visuals(items, weapon, table):
    """Point each listed component at the new entity for this weapon, in jazz/items.lua."""
    changed = []
    for m in reversed(list(re.finditer(r"PlaceObj\('ModItemWeaponComponent'", items))):
        start = m.start()
        end = matching(items, items.index('(', start))
        block = items[start:end]
        found = re.search(r'\bid\s*=\s*"([^"]+)"', block)
        if not found or found[1] not in table:
            continue
        ident = found[1]
        slot, suffix = table[ident]
        entity = suffix if suffix.startswith('WeaponAtt') else f'{HOST[weapon]}_{suffix}'
        replacement = (f"PlaceObj('WeaponComponentVisual', {{\n"
                       f"\t\t\t\t\t\t\t\tApplyTo = \"{weapon}\",\n"
                       f"\t\t\t\t\t\t\t\tEntity = \"{entity}\",\n"
                       f"\t\t\t\t\t\t\t\tSlot = \"{slot}\",\n"
                       f"\t\t\t\t\t\t\t\tparam_bindings = false,\n"
                       f"\t\t\t\t\t\t\t}})")
        hits = []
        for v in re.finditer(r"PlaceObj\('WeaponComponentVisual'", block):
            stop = matching(block, block.index('(', v.start()))
            visual = block[v.start():stop]
            if re.search(r'ApplyTo\s*=\s*"' + weapon + '"', visual) and \
               re.search(r'Slot\s*=\s*"' + slot + '"', visual):
                hits.append((v.start(), stop))
        if hits:
            for vs, ve in reversed(hits):
                block = block[:vs] + replacement + block[ve:]
            changed.append(f'{weapon}.{ident}: {len(hits)} visual(s) -> {entity}')
        else:
            block, n = re.subn(r'Visuals\s*=\s*\{', 'Visuals = {\n' + replacement + ',\n',
                               block, count=1)
            assert n == 1, ident
            changed.append(f'{weapon}.{ident}: visual added -> {entity}')
        items = items[:start] + block + items[end:]
    return items, changed


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--build', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    p.add_argument('--refresh-assets', action='store_true',
                   help='re-copy staged meshes/materials/textures over an existing install, '
                        'without touching any Lua (entity and texture names are unchanged)')
    args = p.parse_args()
    stage = args.build / 'mod-assets-stage' / 'Entities'
    assert stage.is_dir(), f'no staged assets in {stage}'

    if args.refresh_assets:
        files = [src for src in stage.rglob('*') if src.is_file()]
        assert files, 'nothing staged'
        for src in files:
            dest = ASSETS / 'Entities' / src.relative_to(stage)
            assert dest.exists(), f'{dest.name} is not installed yet; run a full install first'
        backup = args.build / 'refresh-backup'
        if not args.apply:
            print(f'DRY RUN: {len(files)} asset files would be refreshed in {ASSETS / "Entities"}')
            return
        assert not backup.exists(), backup
        for src in files:
            rel = src.relative_to(stage)
            dest = ASSETS / 'Entities' / rel
            keep = backup / rel
            keep.parent.mkdir(parents=True, exist_ok=True)
            keep.write_bytes(dest.read_bytes())
            shutil.copy2(src, dest)
        print(f'REFRESHED {len(files)} asset files. Backup: {backup}')
        return

    paths = [ROOT / 'items.lua', ROOT / 'InventoryItem/M16A4.lua', ROOT / 'InventoryItem/M4A1.lua',
             ASSETS / 'items.lua', ASSETS / 'metadata.lua']
    before = {path: path.read_bytes() for path in paths}
    texts = {path: raw.decode('utf-8-sig') for path, raw in before.items()}
    flat = [e for names in ENTITIES.values() for e in names]
    assert HOST['M16A4'] not in texts[ASSETS / 'items.lua'], 'already installed'
    for entity in flat:
        assert (stage / f'{entity}.ent').is_file(), entity
        assert '<src' not in (stage / f'{entity}.ent').read_text(encoding='utf-8'), entity

    log = []
    items = texts[ROOT / 'items.lua']
    for weapon, entity in HOST.items():
        companion = ROOT / f'InventoryItem/{weapon}.lua'
        text = texts[companion]
        text, n = re.subn(rf'\tEntity = "{weapon}",', f'\tEntity = "{entity}",', text)
        assert n == 1, weapon
        start, end = item_block(items, weapon)
        block = items[start:end]
        block, n = re.subn(rf"'Entity', \"{weapon}\",", f"'Entity', \"{entity}\",", block)
        assert n == 1, weapon
        if weapon == 'M4A1':
            # The handguard is now a separate entity, so the slot must exist or the carbine
            # would render without one. These two files differ in line endings, so match the
            # opening brace without one and assert both edits landed.
            assert '"Handguard"' not in text, 'M4A1 already has a Handguard slot'
            text, n = re.subn(r'\tComponentSlots = \{\r?\n',
                              '\tComponentSlots = {\n' + HANDGUARD_SLOT, text, count=1)
            assert n == 1, 'M4A1 companion: ComponentSlots not found'
            block, n = re.subn(r"'ComponentSlots', \{\r?\n",
                               "'ComponentSlots', {\n" + re.sub(r'^\t\t', '\t\t\t\t\t\t',
                                                                HANDGUARD_SLOT, flags=re.M),
                               block, count=1)
            assert n == 1, 'M4A1 items.lua: ComponentSlots not found'
            log.append('M4A1: Handguard slot added (JAZZ_Handguard default)')
        items = items[:start] + block + items[end:]
        texts[companion] = text
        log.append(f'{weapon}: Entity -> {entity} (companion + items.lua)')
    for weapon, table in WIRING.items():
        items, changed = wire_visuals(items, weapon, table)
        log += changed
    texts[ROOT / 'items.lua'] = items

    folder = ("PlaceObj('ModItemFolder', { 'name', \"AR15 remasters\" }, {\n"
              + ''.join("PlaceObj('ModItemEntity', { 'name', \"%s\", 'ClassParents', {}, "
                        "'entity_name', \"%s\" }),\n" % (e, e) for e in flat)
              + '}),')
    texts[ASSETS / 'items.lua'] = append_root_item(texts[ASSETS / 'items.lua'], folder)
    meta = add_metadata(texts[ASSETS / 'metadata.lua'], 'entities', [f'"{e}"' for e in flat])
    texts[ASSETS / 'metadata.lua'] = add_metadata(meta, 'code', [f'"Entities/{e}.lua"' for e in flat])
    log.append(f'jazz_assets: {len(flat)} entities registered (items.lua folder, metadata entities+code)')

    copies = {}
    for src in stage.rglob('*'):
        if src.is_file():
            copies[ASSETS / 'Entities' / src.relative_to(stage)] = src
    log.append(f'jazz_assets/Entities: {len(copies)} files staged in')

    for path, text in texts.items():
        LuaRuntime().compile(text)
    for entity in flat:
        tree = ET.parse(stage / f'{entity}.ent')
        assert tree.getroot().get('name') == entity, entity

    print('\n'.join(log))
    if not args.apply:
        print(f'\nDRY RUN: nothing written. {len(copies)} asset files and '
              f'{len(texts)} Lua files would change. Re-run with --apply.')
        return
    for path, raw in before.items():
        assert path.read_bytes() == raw, f'Concurrent modification: {path}'
    backup = args.build / 'integration-backup'
    assert not backup.exists(), backup
    for path, raw in before.items():
        package = ROOT if path.is_relative_to(ROOT) else ASSETS
        dest = backup / package.name / path.relative_to(package)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
    for dest, src in copies.items():
        if dest.exists():
            rel = dest.relative_to(ASSETS)
            keep = backup / 'jazz_assets' / rel
            keep.parent.mkdir(parents=True, exist_ok=True)
            keep.write_bytes(dest.read_bytes())
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
    for path, text in texts.items():
        write(path, text)
    print(f'\nAPPLIED. Backup: {backup}')


if __name__ == '__main__':
    main()
