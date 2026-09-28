"""Wire visible AR15 barrels / A4 handguard / RIS / carry handle (JAZZ-WEAPON-AR15-FAMILY-001).

  python docs/tools/_wire_ar15_visible_modules.py --build <build> [--apply]

Assumes the remaster hosts are already installed. Adds the new module entities, two
component IDs, A4 Handguard slot, and visuals. Dry-run by default.
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from lupa import LuaRuntime

from _integrate_sr3m import ASSETS, ROOT, add_metadata, matching, write
from _integrate_ar15_family import item_block, wire_visuals

NEW_ENTITIES = {
    'M16A4': ['M16R_M16A4_Handguard', 'M16R_M16A4_HandguardRIS',
              'M16R_M16A4_Barrel', 'M16R_M16A4_BarrelShort',
              'M16R_M16A4_Handgrip', 'M16R_M16A4_DefMuzzle',
              'M16R_M16A4_Stock', 'M16R_M16A4_StockLight',
              'M16R_M16A4_Magazine20'],
    'M4A1': ['M4R_M4A1_Barrel', 'M4R_M4A1_BarrelShort', 'M4R_M4A1_BarrelLong',
             'M4R_M4A1_HandguardRifle', 'M4R_M4A1_Handgrip', 'M4R_M4A1_DefMuzzle',
             'M4R_M4A1_Magazine20'],
}
HOST = {'M16A4': 'M16R_M16A4', 'M4A1': 'M4R_M4A1'}
WIRING = {
    'M16A4': {
        'JAZZ_BarrelNormal': ('Barrel', 'Barrel'),
        'JAZZ_BarrelShort': ('Barrel', 'BarrelShort'),
        'JAZZ_Handguard': ('Handguard', 'Handguard'),
        'JAZZ_Handguard_RIS': ('Handguard', 'HandguardRIS'),
        'JAZZ_CarryHandle_AR15': ('Scope', 'CarryHandle'),
        'JAZZ_Handgrip_Default': ('Handgrip', 'Handgrip'),
        'JAZZ_Handgrip_Ergo': ('Handgrip', 'Handgrip'),
        'JAZZ_DefMuzzle': ('Muzzle', 'DefMuzzle'),
        'JAZZ_StockNormal': ('Stock', 'Stock'),
        'JAZZ_StockHeavy': ('Stock', 'Stock'),
        'JAZZ_StockLight': ('Stock', 'StockLight'),
        'JAZZ_MagSmall30_20': ('Magazine', 'Magazine20'),
        'JAZZ_Compensator': ('Muzzle', 'WeaponAttA_CompensatorM4'),
    },
    'M4A1': {
        'JAZZ_BarrelNormal': ('Barrel', 'Barrel'),
        'JAZZ_BarrelShort': ('Barrel', 'BarrelShort'),
        'JAZZ_BarrelLong': ('Barrel', 'BarrelLong'),
        'JAZZ_Handguard_RIS': ('Handguard', 'HandguardRIS'),
        'JAZZ_CarryHandle_AR15': ('Scope', 'CarryHandle'),
        'JAZZ_Handgrip_Default': ('Handgrip', 'Handgrip'),
        'JAZZ_Handgrip_Ergo': ('Handgrip', 'Handgrip'),
        'JAZZ_DefMuzzle': ('Muzzle', 'DefMuzzle'),
        'JAZZ_MagSmall30_20': ('Magazine', 'Magazine20'),
        'JAZZ_Compensator': ('Muzzle', 'WeaponAttA_CompensatorM4'),
    },
}
A4_HANDGUARD = """		PlaceObj('WeaponComponentSlot', {
			'SlotType', "Handguard",
			'AvailableComponents', {
				"JAZZ_Handguard",
				"JAZZ_Handguard_RIS",
			},
			'DefaultComponent', "JAZZ_Handguard",
		}),
"""
RIS_COMPONENT = """					PlaceObj('ModItemWeaponComponent', {
						ChipIcon = "Mod/e6L4ECj/Icons/Upgrades/Chips/JAZZ_Handguard_RIS.png",
						Cost = 50,
						DisplayName = T(266664626516, --[[ModItemWeaponComponent JAZZ_Handguard_RIS DisplayName]] "Цевьё с рельсой"),
						Icon = "UI/Icons/Upgrades/default_grenadelauncher",
						ModificationDifficulty = 10,
						Slot = "Handguard",
						Visuals = {
						},
						comment = "--Цевья",
						group = "Underslung",
						id = "JAZZ_Handguard_RIS",
					}),
"""
CARRY_COMPONENT = """					PlaceObj('ModItemWeaponComponent', {
						ChipIcon = "Mod/e6L4ECj/Icons/Upgrades/Chips/JAZZ_CarryHandle_AR15.png",
						Cost = 0,
						DisplayName = T(890000000020597, --[[ModItemWeaponComponent JAZZ_CarryHandle_AR15 DisplayName]] "Ручка для переноски"),
						Icon = "UI/Icons/Upgrades/ironsights_hands",
						ModificationDifficulty = 0,
						Slot = "Scope",
						Visuals = {
						},
						group = "AR15 Specific",
						id = "JAZZ_CarryHandle_AR15",
					}),
"""


def add_component_option(block: str, slot: str, component: str) -> tuple[str, bool]:
    """Insert component id into an existing slot's AvailableComponents if missing."""
    pattern = re.compile(
        r"('SlotType',\s*\"" + slot + r"\".*?'AvailableComponents',\s*\{)(.*?)(\s*\})",
        re.S)
    match = pattern.search(block)
    if not match:
        return block, False
    if f'"{component}"' in match.group(2):
        return block, False
    insert = match.group(2).rstrip() + f'\n\t\t\t\t"{component}",\n\t\t\t'
    return block[: match.start()] + match.group(1) + insert + match.group(3) + block[match.end():], True


def _slot_span(text: str, slot: str) -> tuple[int, int] | None:
    token = f"'SlotType', \"{slot}\""
    pos = text.find(token)
    if pos < 0:
        token = f"'SlotType', \"{slot}\""
        pos = text.find(token)
    if pos < 0:
        return None
    start = text.rfind('PlaceObj(', 0, pos)
    if start < 0:
        return None
    return start, matching(text, text.index('(', start))


def set_slot_default(text: str, slot: str, component: str) -> tuple[str, bool]:
    span = _slot_span(text, slot)
    if not span:
        return text, False
    start, end = span
    body = text[start:end]
    if re.search(r"'DefaultComponent',\s*\"" + component + r'"', body):
        return text, False
    if re.search(r"'DefaultComponent',", body):
        body = re.sub(r"'DefaultComponent',\s*\"[^\"]+\"",
                      f"'DefaultComponent', \"{component}\"", body, count=1)
    else:
        close = body.rfind('}')
        body = (body[:close]
                + f"\n\t\t\t\t'DefaultComponent', \"{component}\",\n\t\t\t"
                + body[close:])
    return text[:start] + body + text[end:], True


def set_slot_can_be_empty(text: str, slot: str, value: bool) -> tuple[str, bool]:
    span = _slot_span(text, slot)
    if not span:
        return text, False
    start, end = span
    body = text[start:end]
    token = 'true' if value else 'false'
    if re.search(r"'CanBeEmpty',\s*" + token + r'\b', body):
        return text, False
    if re.search(r"'CanBeEmpty',", body):
        body = re.sub(r"'CanBeEmpty',\s*(true|false)",
                      f"'CanBeEmpty', {token}", body, count=1)
    elif value:
        close = body.rfind('}')
        body = (body[:close]
                + f"\n\t\t\t\t'CanBeEmpty', {token},\n\t\t\t"
                + body[close:])
    else:
        return text, False
    return text[:start] + body + text[end:], True


def add_companion_option(text: str, slot: str, component: str) -> tuple[str, bool]:
    pattern = re.compile(
        r"('SlotType',\s*\"" + slot + r"\".*?'AvailableComponents',\s*\{)(.*?)(\s*\})",
        re.S)
    match = pattern.search(text)
    if not match:
        return text, False
    if f'"{component}"' in match.group(2):
        return text, False
    insert = match.group(2).rstrip() + f'\n\t\t\t\t"{component}",\n\t\t\t'
    return text[: match.start()] + match.group(1) + insert + match.group(3) + text[match.end():], True


def insert_after_id(items: str, after_id: str, snippet: str) -> str:
    found = re.search(r'\bid\s*=\s*"' + after_id + r'"', items)
    assert found, after_id
    start = items.rfind("PlaceObj('ModItemWeaponComponent'", 0, found.start())
    end = matching(items, items.index('(', start))
    # Skip the closing `}),` of this component.
    close = items.find('\n', end)
    return items[: close + 1] + snippet + items[close + 1 :]


def register_entities(assets_items: str, names: list[str]) -> str:
    missing = [n for n in names if f'entity_name\', "{n}"' not in assets_items]
    if not missing:
        return assets_items
    anchor = "PlaceObj('ModItemEntity', { 'name', \"M4R_M4A1_RearSight\""
    pos = assets_items.find(anchor)
    assert pos >= 0
    line_end = assets_items.find('\n', pos)
    extra = ''.join(
        f"PlaceObj('ModItemEntity', {{ 'name', \"{n}\", 'ClassParents', {{}}, "
        f"'entity_name', \"{n}\" }}),\n" for n in missing)
    return assets_items[: line_end + 1] + extra + assets_items[line_end + 1 :]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--build', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    stage = args.build / 'mod-assets-stage' / 'Entities'
    flat = [e for names in NEW_ENTITIES.values() for e in names]
    assert stage.is_dir(), f'no staged assets in {stage}'
    for entity in flat:
        assert (stage / f'{entity}.ent').is_file(), entity

    chips = ROOT / 'Icons' / 'Upgrades' / 'Chips'
    copies = {
        chips / 'JAZZ_Handguard_RIS.png': chips / 'JAZZ_HandguardM1ARail.png',
        chips / 'JAZZ_CarryHandle_AR15.png': chips / 'JAZZ_DefaultIronsight_AR15.png',
    }

    paths = [ROOT / 'items.lua', ROOT / 'InventoryItem/M16A4.lua', ROOT / 'InventoryItem/M4A1.lua',
             ROOT / 'metadata.lua', ASSETS / 'items.lua', ASSETS / 'metadata.lua']
    before = {path: path.read_bytes() for path in paths}
    texts = {path: raw.decode('utf-8-sig') for path, raw in before.items()}
    log = []

    items = texts[ROOT / 'items.lua']
    if 'id = "JAZZ_Handguard_RIS"' not in items:
        items = insert_after_id(items, 'JAZZ_HandguardM1ARail', RIS_COMPONENT)
        log.append('items.lua: added JAZZ_Handguard_RIS')
    if 'id = "JAZZ_CarryHandle_AR15"' not in items:
        items = insert_after_id(items, 'JAZZ_DefaultIronsight_AR15', CARRY_COMPONENT)
        log.append('items.lua: added JAZZ_CarryHandle_AR15')

    companion_a4 = texts[ROOT / 'InventoryItem/M16A4.lua']
    start, end = item_block(items, 'M16A4')
    block = items[start:end]
    if '"Handguard"' not in companion_a4:
        companion_a4, n = re.subn(r'\tComponentSlots = \{\r?\n',
                                  '\tComponentSlots = {\n' + A4_HANDGUARD, companion_a4, count=1)
        assert n == 1, 'M16A4 companion: ComponentSlots not found'
        block, n = re.subn(r"'ComponentSlots', \{\r?\n",
                           "'ComponentSlots', {\n" + re.sub(r'^\t\t', '\t\t\t\t\t\t',
                                                            A4_HANDGUARD, flags=re.M),
                           block, count=1)
        assert n == 1, 'M16A4 items.lua: ComponentSlots not found'
        log.append('M16A4: Handguard slot added (JAZZ_Handguard default, RIS option)')
    items = items[:start] + block + items[end:]
    texts[ROOT / 'InventoryItem/M16A4.lua'] = companion_a4

    for weapon, extras in (
        ('M4A1', [('Handguard', 'JAZZ_Handguard_RIS'), ('Scope', 'JAZZ_CarryHandle_AR15'),
                  ('Muzzle', 'JAZZ_DefMuzzle')]),
        ('M16A4', [('Scope', 'JAZZ_CarryHandle_AR15'), ('Muzzle', 'JAZZ_DefMuzzle')]),
    ):
        companion = ROOT / f'InventoryItem/{weapon}.lua'
        text = texts[companion]
        start, end = item_block(items, weapon)
        block = items[start:end]
        for slot, component in extras:
            block, changed = add_component_option(block, slot, component)
            text, _ = add_companion_option(text, slot, component)
            if changed:
                log.append(f'{weapon}.{slot}: +{component}')
        items = items[:start] + block + items[end:]
        texts[companion] = text

    for weapon in ('M16A4', 'M4A1'):
        companion = ROOT / f'InventoryItem/{weapon}.lua'
        start, end = item_block(items, weapon)
        block = items[start:end]
        text = texts[companion]
        for fn, fn_args, label in (
            (set_slot_default, ('Scope', 'JAZZ_CarryHandle_AR15'), 'Scope default CarryHandle'),
            (set_slot_can_be_empty, ('Scope', False), 'Scope CanBeEmpty false'),
            (set_slot_default, ('Muzzle', 'JAZZ_DefMuzzle'), 'Muzzle default DefMuzzle'),
        ):
            block, a = fn(block, *fn_args)
            text, b = fn(text, *fn_args)
            if a or b:
                log.append(f'{weapon}: {label}')
        items = items[:start] + block + items[end:]
        texts[companion] = text

    for weapon, table in WIRING.items():
        items, changed = wire_visuals(items, weapon, table)
        log += changed
    items, extra = wire_visuals(items, 'M4A1', {
        'JAZZ_BarrelLong': ('Handguard', 'HandguardRifle'),
    })
    log += extra
    texts[ROOT / 'items.lua'] = items

    meta = texts[ROOT / 'metadata.lua']
    for cid, after in (('JAZZ_Handguard_RIS', 'JAZZ_HandguardM1ARail'),
                       ('JAZZ_CarryHandle_AR15', 'JAZZ_DefaultIronsight_AR15')):
        if f"'Id', \"{cid}\"" in meta:
            continue
        needle = f"'Id', \"{after}\""
        pos = meta.find(needle)
        assert pos >= 0, after
        close = meta.find('}),', pos) + 3
        preset = (
            "\n\t\tPlaceObj('ModResourcePreset', {\n"
            "\t\t\t'Class', \"WeaponComponent\",\n"
            f"\t\t\t'Id', \"{cid}\",\n"
            "\t\t\t'ClassDisplayName', \"Weapon Component\",\n"
            "\t\t}),"
        )
        meta = meta[:close] + preset + meta[close:]
        log.append(f'jazz/metadata.lua: preset {cid}')
    texts[ROOT / 'metadata.lua'] = meta

    texts[ASSETS / 'items.lua'] = register_entities(texts[ASSETS / 'items.lua'], flat)
    assets_meta = texts[ASSETS / 'metadata.lua']
    assets_meta = add_metadata(assets_meta, 'entities', [f'"{e}"' for e in flat
                                                        if f'"{e}"' not in assets_meta])
    assets_meta = add_metadata(assets_meta, 'code',
                               [f'"Entities/{e}.lua"' for e in flat
                                if f'"Entities/{e}.lua"' not in assets_meta])
    texts[ASSETS / 'metadata.lua'] = assets_meta
    log.append(f'jazz_assets: {len(flat)} new entities registered')

    asset_copies = {ASSETS / 'Entities' / src.relative_to(stage): src
                    for src in stage.rglob('*') if src.is_file()}
    log.append(f'jazz_assets/Entities: {len(asset_copies)} staged files (hosts refreshed, modules added)')

    for path, text in texts.items():
        LuaRuntime().compile(text)

    print('\n'.join(log))
    if not args.apply:
        print(f'\nDRY RUN: {len(asset_copies)} asset files and {len(texts)} Lua files. '
              'Re-run with --apply.')
        return
    for path, raw in before.items():
        assert path.read_bytes() == raw, f'Concurrent modification: {path}'
    backup = args.build / 'modules-backup'
    assert not backup.exists(), backup
    for path, raw in before.items():
        package = ROOT if path.is_relative_to(ROOT) else ASSETS
        dest = backup / package.name / path.relative_to(package)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
    for dest, src in copies.items():
        if not dest.exists():
            dest.write_bytes(src.read_bytes())
    for dest, src in asset_copies.items():
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            keep = backup / 'jazz_assets' / dest.relative_to(ASSETS)
            keep.parent.mkdir(parents=True, exist_ok=True)
            keep.write_bytes(dest.read_bytes())
        shutil.copy2(src, dest)
    for path, text in texts.items():
        write(path, text)
    print(f'\nAPPLIED. Backup: {backup}')


if __name__ == '__main__':
    main()
