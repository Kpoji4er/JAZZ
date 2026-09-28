"""JAZZ-WEAPON-M14-FAMILY-001: install seated entities and register the new rifles.

  python docs/tools/_integrate_m14_family.py --export-root D:/ExportedEntities --build D:/jazz_m14_build --game-root <JA3_ROOT>

Requires the game/editor closed. Backs up items.lua/metadata.lua under the build.
"""
import argparse
import hashlib
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT.parent / 'jazz_assets'
ENTITIES = ['JAZZ_M14', 'JAZZ_M14_ART', 'MK14EBR', 'JAZZ_M14_MkIII']
LOC = {
    'ebr_name': (990002710, 'Mk 14 EBR', 'Mk 14 EBR'),
    'ebr_plural': (990002711, 'Mk 14 EBR', 'Mk 14 EBRs'),
    'ebr_desc': (990002712,
                 'Mk 14 EBR на шасси Sage: пистолетная рукоять, складной AR-приклад и рейки. Тот же 7.62x51, но уже не ложка USGI.',
                 'Mk 14 EBR on a Sage chassis: pistol grip, folding AR stock and rails. Same 7.62x51, no USGI wood.'),
    'ebr_hint': (990002713, 'Современное шасси \\nОчередь и авто', 'Modern chassis \\nBurst and auto'),
    'mk_name': (990002714, 'M14 Mk III', 'M14 Mk III'),
    'mk_plural': (990002715, 'M14 Mk III', 'M14 Mk III'),
    'mk_desc': (990002716,
                'Кастомный M14 с рельсой Mk III, своим камуфляжем и обвесом. Не путать с золотым Gold Fever.',
                'A custom M14 with a Mk III rail, its own camo and furniture. Not Gold Fever.'),
    'mk_hint': (990002717, 'Уник \\nНе в Bobby Ray', 'Unique \\nNot in Bobby Ray'),
    'art': (990002718, 'ART / Leatherwood', 'ART / Leatherwood'),
}
ICON = '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120>'


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace('\r\n', '\n'), encoding='utf-8', newline='\n')


def matching(text, start, opener='(', closer=')'):
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if text.startswith('--', i):
            long = re.match(r'--\[(=*)\[', text[i:])
            if long:
                end = ']' + long[1] + ']'
                i = text.index(end, i + len(long[0])) + len(end)
            else:
                i = text.find('\n', i)
                if i < 0:
                    raise ValueError('Unclosed expression')
            continue
        if c in '"\'':
            quote = c
            i += 1
            while i < len(text):
                if text[i] == '\\':
                    i += 2
                elif text[i] == quote:
                    i += 1
                    break
                else:
                    i += 1
            continue
        long = re.match(r'\[(=*)\[', text[i:]) if c == '[' else None
        if long:
            end = ']' + long[1] + ']'
            i = text.index(end, i + len(long[0])) + len(end)
            continue
        if c == opener:
            depth += 1
        if c == closer:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError('Unbalanced Lua')


def append_root_item(text, item):
    pos = text.rstrip().rfind('}')
    assert pos > 0
    head = text[:pos].rstrip()
    if not head.endswith(',') and not head.endswith('{'):
        head += ','
    return head + '\n' + item + '\n' + text[pos:]


def add_metadata(text, key, lines):
    match = re.search(r"'" + key + r"',\s*\{", text)
    assert match, key
    pos = match.end()
    return text[:pos] + '\n' + ''.join('\t\t' + line + ',\n' for line in lines) + text[pos:]


def find_item_block(text, item_id):
    needle = '\'Id\', "%s",' % item_id
    at = text.find(needle)
    if at < 0:
        raise SystemExit('item not found: %s' % item_id)
    start = text.rfind("PlaceObj('ModItemInventoryItemCompositeDef', {", 0, at)
    end = matching(text, text.index('(', start))
    return start, end


def companion_from_items(block, item_id):
    """Turn a ModItemInventoryItemCompositeDef body into a companion file."""
    inner = block[block.index('{') + 1:block.rfind('}')]
    # drop Group / Id keys that belong only to the ModItem wrapper
    inner = re.sub(r"\n\t+'Group', \"[^\"]+\",", '', inner)
    inner = re.sub(r"\n\t+'Id', \"[^\"]+\",", '', inner)
    props = re.sub(r"^(\t+)'([A-Za-z_][A-Za-z_0-9]*)', ", r"\1\2 = ", inner, flags=re.M)
    return (
        "UndefineClass('%s')\nDefineClass.%s = {\n"
        "\t__parents = { \"%s\" },\n"
        "\t__generated_by_class = \"ModItemInventoryItemCompositeDef\",\n"
        "%s}\n" % (item_id, item_id, object_class(block), props)
    )


def object_class(block):
    m = re.search(r"'object_class', \"([^\"]+)\"", block)
    return m.group(1) if m else 'Firearm'


def set_field(block, field, value):
    out, n = re.subn(r"'%s', [^,\n]+," % field, "'%s', %s," % (field, value), block, count=1)
    if n != 1:
        raise SystemExit('field %s not replaced' % field)
    return out


def stage_entities(export, staged, game):
    suffixes = {
        'BaseColorMap': 'Base', 'NormalMap': 'Norm', 'RMMap': 'RM',
        'AOMap': 'AO', 'AmbientOcclusionMap': 'AO', 'SpecialMap': 'SPEC',
        'SIMap': 'SI', 'ColorizationMap': 'Color',
    }
    names = {}
    for ent in ENTITIES:
        tree = ET.parse(export / (ent + '.ent'))
        tree.getroot().set('name', ent)
        for lod in tree.findall('.//lod'):
            for src in list(lod.findall('src')):
                lod.remove(src)
        for node in tree.findall('.//mesh'):
            rel = node.attrib['file']
            dest = staged / rel
            dest.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy2(export / rel, dest)
        for node in tree.findall('.//material'):
            rel = node.attrib['file']
            mtl = ET.parse(export / rel)
            for tag in mtl.getroot().iter():
                name = tag.get('Name')
                if name and tag.tag in suffixes:
                    src = export / 'Textures' / name
                    assert src.is_file(), src
                    key = (suffixes[tag.tag], hashlib.sha256(src.read_bytes()).hexdigest())
                    new = names.get(key, '%s_%s.dds' % (ent, suffixes[tag.tag]))
                    names[key] = new
                    dest = staged / 'Textures' / new
                    dest.parent.mkdir(exist_ok=True, parents=True)
                    cvt = str(game / 'ModTools/hgimgcvt.exe')
                    subprocess.run([cvt, str(src), str(dest), '--truncate', '2048'],
                                   check=True, capture_output=True)
                    fallback = staged / 'Textures/Fallbacks' / new
                    fallback.parent.mkdir(exist_ok=True, parents=True)
                    subprocess.run([cvt, str(dest), str(fallback), '--truncate', '64'],
                                   check=True, capture_output=True)
                    tag.set('Name', new)
            dest = staged / rel
            dest.parent.mkdir(exist_ok=True, parents=True)
            mtl.write(dest, encoding='utf-8', xml_declaration=True)
        tree.write(staged / (ent + '.ent'), encoding='utf-8', xml_declaration=True)
        write(staged / (ent + '.lua'), 'EntityData["%s"] = {\n\teditor_artset = "Mods",\n}\n' % ent)


def mirror_visuals(text, src_id, dest_id, empty_slots):
    pattern = re.compile(
        r"([ \t]*)PlaceObj\('WeaponComponentVisual', \{\n"
        r"((?:[ \t]*\w+ = [^\n]*\n)*?)"
        r"[ \t]*ApplyTo = \"%s\",\n"
        r"((?:[ \t]*\w+ = [^\n]*\n)*?)"
        r"([ \t]*)\}\),\n" % src_id)
    out = []
    pos = 0
    count = 0
    for m in pattern.finditer(text):
        whole = m.group(0)
        if dest_id in whole:
            continue
        clone = whole.replace('ApplyTo = "%s",' % src_id, 'ApplyTo = "%s",' % dest_id)
        slot = re.search(r'Slot = \"([^\"]+)\"', clone)
        if slot and slot.group(1) in empty_slots:
            clone = re.sub(r'Entity = \"[^\"]*\"', 'Entity = ""', clone, count=1)
        if dest_id == 'MK14EBR' or dest_id == 'JAZZ_M14_MkIII':
            if slot and slot.group(1) in ('Stock', 'Magazine'):
                clone = re.sub(r'Entity = \"[^\"]*\"', 'Entity = ""', clone, count=1)
        out.append(text[pos:m.end()])
        tail = text[m.end():]
        if tail.startswith(clone):
            pos = m.end() + len(clone)
        else:
            out.append(clone)
            pos = m.end()
            count += 1
    out.append(text[pos:])
    return ''.join(out), count


def empty_stock_visuals(text, weapon_ids):
    pattern = re.compile(
        r"(PlaceObj\('WeaponComponentVisual', \{(?:[^{}]|\{[^{}]*\})*?ApplyTo = \"(?:%s)\","
        r"(?:[^{}]|\{[^{}]*\})*?Entity = \")WeaponAttA_StockM14_[^\"]+\""
        % '|'.join(weapon_ids),
        re.S,
    )
    return pattern.sub(r'\1"', text)


def build_ebr(block):
    out = block.replace('\'Id\', "M14SAW",', '\'Id\', "MK14EBR",', 1)
    out = out.replace('\'comment\', "Tier 2-2",', '\'comment\', "Tier 3-1 - JAZZ-WEAPON-M14-FAMILY-001",', 1)
    out = out.replace('WeaponIcons/M14.png', 'WeaponIcons/MK14EBR.png')
    out = set_field(out, 'Reliability', '70')
    out = set_field(out, 'Cost', '20000')
    out = set_field(out, 'Tier', '4')
    out = set_field(out, 'RestockWeight', '25')
    out = set_field(out, 'Recoil', '28')
    out = set_field(out, 'Entity', '"MK14EBR"')
    out = out.replace("'ModifyRightHandGrip', true,", "'ModifyRightHandGrip', false,")
    out = re.sub(
        r"'DisplayName', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'DisplayName', T(%d, --[[ModItemInventoryItemCompositeDef MK14EBR DisplayName]] \"%s\")," % (LOC['ebr_name'][0], LOC['ebr_name'][1]),
        out, count=1)
    out = re.sub(
        r"'DisplayNamePlural', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'DisplayNamePlural', T(%d, --[[ModItemInventoryItemCompositeDef MK14EBR DisplayNamePlural]] \"%s\")," % (LOC['ebr_plural'][0], LOC['ebr_plural'][1]),
        out, count=1)
    out = re.sub(
        r"'Description', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'Description', T(%d, --[[ModItemInventoryItemCompositeDef MK14EBR Description]] \"%s\")," % (LOC['ebr_desc'][0], LOC['ebr_desc'][1]),
        out, count=1)
    hint = ICON + ' ' + LOC['ebr_hint'][1].replace(' \\n', ' \\n' + ICON + ' ')
    out = re.sub(
        r"'AdditionalHint', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'AdditionalHint', T(%d, --[[ModItemInventoryItemCompositeDef MK14EBR AdditionalHint]] \"%s\")," % (LOC['ebr_hint'][0], hint),
        out, count=1)
    return out


def build_mkiii(block):
    out = block.replace('\'Id\', "M21",', '\'Id\', "JAZZ_M14_MkIII",', 1)
    out = out.replace('\'comment\', "Tier 2-3",', '\'comment\', "Unique - JAZZ-WEAPON-M14-FAMILY-001",', 1)
    out = out.replace('WeaponIcons/M21.png', 'WeaponIcons/JAZZ_M14_MkIII.png')
    out = set_field(out, 'CanAppearInShop', 'false')
    out = set_field(out, 'RestockWeight', '0')
    out = set_field(out, 'Cost', '28000')
    out = set_field(out, 'Entity', '"JAZZ_M14_MkIII"')
    out = out.replace("'ModifyRightHandGrip', true,", "'ModifyRightHandGrip', false,")
    out = re.sub(
        r"'DisplayName', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'DisplayName', T(%d, --[[ModItemInventoryItemCompositeDef JAZZ_M14_MkIII DisplayName]] \"%s\")," % (LOC['mk_name'][0], LOC['mk_name'][1]),
        out, count=1)
    out = re.sub(
        r"'DisplayNamePlural', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'DisplayNamePlural', T(%d, --[[ModItemInventoryItemCompositeDef JAZZ_M14_MkIII DisplayNamePlural]] \"%s\")," % (LOC['mk_plural'][0], LOC['mk_plural'][1]),
        out, count=1)
    out = re.sub(
        r"'Description', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'Description', T(%d, --[[ModItemInventoryItemCompositeDef JAZZ_M14_MkIII Description]] \"%s\")," % (LOC['mk_desc'][0], LOC['mk_desc'][1]),
        out, count=1)
    hint = ICON + ' ' + LOC['mk_hint'][1].replace(' \\n', ' \\n' + ICON + ' ')
    out = re.sub(
        r"'AdditionalHint', T\(\d+, --\[\[[^\]]*\]\] \"[^\"]*\"\),",
        lambda m: "'AdditionalHint', T(%d, --[[ModItemInventoryItemCompositeDef JAZZ_M14_MkIII AdditionalHint]] \"%s\")," % (LOC['mk_hint'][0], hint),
        out, count=1)
    return out


ART_COMPONENT = """\t\t\t\t\tPlaceObj('ModItemWeaponComponent', {
\t\t\t\t\t\tCost = 2,
\t\t\t\t\t\tDisplayName = T(%(id)d, --[[ModItemWeaponComponent JAZZ_Scope_M21_ART DisplayName]] "%(name)s"),
\t\t\t\t\t\tIcon = "UI/Icons/Upgrades/scope_long",
\t\t\t\t\t\tModificationDifficulty = -25,
\t\t\t\t\t\tSlot = "Scope",
\t\t\t\t\t\tVisuals = {
\t\t\t\t\t\t\tPlaceObj('WeaponComponentVisual', {
\t\t\t\t\t\t\t\tApplyTo = "M21",
\t\t\t\t\t\t\t\tEntity = "JAZZ_M14_ART",
\t\t\t\t\t\t\t\tSlot = "Scope",
\t\t\t\t\t\t\t\tparam_bindings = false,
\t\t\t\t\t\t\t}),
\t\t\t\t\t\t},
\t\t\t\t\t\tcomment = "M21 default Leatherwood ART from Lego",
\t\t\t\t\t\tgroup = "M14 Specific",
\t\t\t\t\t\tid = "JAZZ_Scope_M21_ART",
\t\t\t\t\t}),
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--export-root', required=True, type=Path)
    p.add_argument('--build', required=True, type=Path)
    p.add_argument('--game-root', required=True, type=Path)
    args = p.parse_args()
    export = args.export_root.resolve()
    build = args.build.resolve()
    items_text = (ROOT / 'items.lua').read_text(encoding='utf-8')
    if '\'Id\', "MK14EBR",' in items_text:
        raise SystemExit('MK14EBR already integrated')
    for ent in ENTITIES:
        assert (export / (ent + '.ent')).is_file(), ent

    backup = build / 'integration-backup'
    for package in (ROOT, ASSETS):
        for name in ('items.lua', 'metadata.lua'):
            target = backup / package.name / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                shutil.copy2(package / name, target)

    staged = build / 'mod-assets-stage' / 'Entities'
    if staged.exists():
        shutil.rmtree(staged)
    staged.mkdir(parents=True)
    stage_entities(export, staged, args.game_root)

    # Point classic hosts at the new wood entity.
    items_text = items_text.replace(
        '\'Id\', "M14SAW",',
        '\'Id\', "M14SAW",',
        1)
    # Entity replacements are scoped to the two classic blocks only.
    for wid in ('M14SAW', 'M21'):
        start, end = find_item_block(items_text, wid)
        block = items_text[start:end].replace("'Entity', \"Weapon_M14\",", "'Entity', \"JAZZ_M14\",")
        if wid == 'M21':
            if 'JAZZ_Scope_M21_ART' not in block:
                block = block.replace(
                    '\'SlotType\', "Scope",\n\t\t\t\t\t\t\'CanBeEmpty\', true,\n\t\t\t\t\t\t\'AvailableComponents\', {',
                    '\'SlotType\', "Scope",\n\t\t\t\t\t\t\'CanBeEmpty\', true,\n\t\t\t\t\t\t\'AvailableComponents\', {\n\t\t\t\t\t\t\t"JAZZ_Scope_M21_ART",',
                    1)
                if "'DefaultComponent'" not in block[block.find("'SlotType', \"Scope\""):block.find("'SlotType', \"Scope\"") + 800]:
                    # insert default after AvailableComponents of Scope
                    scope_at = block.find("'SlotType', \"Scope\"")
                    avail_end = matching(block, block.index('{', block.find("'AvailableComponents'", scope_at)), '{', '}')
                    if "'DefaultComponent'" not in block[scope_at:avail_end + 40]:
                        block = block[:avail_end] + ',\n\t\t\t\t\t\t\'DefaultComponent\', "JAZZ_Scope_M21_ART"' + block[avail_end:]
        items_text = items_text[:start] + block + items_text[end:]
        companion = (ROOT / 'InventoryItem' / (wid + '.lua')).read_text(encoding='utf-8')
        companion = companion.replace('Entity = "Weapon_M14",', 'Entity = "JAZZ_M14",')
        if wid == 'M21' and 'JAZZ_Scope_M21_ART' not in companion:
            companion = companion.replace(
                '\'SlotType\', "Scope",\n\t\t\t\'CanBeEmpty\', true,\n\t\t\t\'AvailableComponents\', {',
                '\'SlotType\', "Scope",\n\t\t\t\'CanBeEmpty\', true,\n\t\t\t\'AvailableComponents\', {\n\t\t\t\t"JAZZ_Scope_M21_ART",',
                1)
            if 'DefaultComponent' not in companion[companion.find("'SlotType', \"Scope\""):]:
                scope_at = companion.find("'SlotType', \"Scope\"")
                avail_end = matching(companion, companion.index('{', companion.find("'AvailableComponents'", scope_at)), '{', '}')
                companion = companion[:avail_end] + ',\n\t\t\t\'DefaultComponent\', "JAZZ_Scope_M21_ART"' + companion[avail_end:]
        write(ROOT / 'InventoryItem' / (wid + '.lua'), companion)

    start, end = find_item_block(items_text, 'M14SAW')
    ebr_block = build_ebr(items_text[start:end])
    items_text = items_text[:end] + '\n' + ebr_block + items_text[end:]
    start, end = find_item_block(items_text, 'M21')
    mk_block = build_mkiii(items_text[start:end])
    items_text = items_text[:end] + '\n' + mk_block + items_text[end:]

    if 'id = "JAZZ_Scope_M21_ART",' not in items_text:
        marker = "id = \"JAZZ_M14_Default_Muzzle\","
        at = items_text.find(marker)
        start = items_text.rfind("PlaceObj('ModItemWeaponComponent'", 0, at)
        end = matching(items_text, items_text.index('(', start))
        comp = ART_COMPONENT % {'id': LOC['art'][0], 'name': LOC['art'][1]}
        items_text = items_text[:end] + ',\n' + comp + items_text[end:]

    items_text = empty_stock_visuals(items_text, ('M14SAW', 'M21'))
    for dest in ('MK14EBR', 'JAZZ_M14_MkIII'):
        items_text, n = mirror_visuals(items_text, 'M14SAW', dest, ('Stock', 'Magazine'))
        print('mirrored', n, 'visuals onto', dest)

    write(ROOT / 'InventoryItem/MK14EBR.lua', companion_from_items(ebr_block, 'MK14EBR'))
    write(ROOT / 'InventoryItem/JAZZ_M14_MkIII.lua', companion_from_items(mk_block, 'JAZZ_M14_MkIII'))

    asset_items = (ASSETS / 'items.lua').read_text(encoding='utf-8')
    folder = "\tPlaceObj('ModItemFolder', { 'name', \"M14Family\" }, {\n"
    for ent in ENTITIES:
        folder += "\t\tPlaceObj('ModItemEntity', { 'name', \"%s\", 'ClassParents', {}, 'entity_name', \"%s\" }),\n" % (ent, ent)
    folder += "\t}),"
    asset_items = append_root_item(asset_items, folder)
    asset_meta = (ASSETS / 'metadata.lua').read_text(encoding='utf-8')
    asset_meta = add_metadata(asset_meta, 'entities', ['"%s"' % e for e in ENTITIES])
    asset_meta = add_metadata(asset_meta, 'code', ['"Entities/%s.lua"' % e for e in ENTITIES])
    meta = (ROOT / 'metadata.lua').read_text(encoding='utf-8')
    meta = add_metadata(meta, 'code', ['"InventoryItem/MK14EBR.lua"', '"InventoryItem/JAZZ_M14_MkIII.lua"'])
    meta = add_metadata(meta, 'affected_resources', [
        "PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", 'Id', \"MK14EBR\", 'ClassDisplayName', \"Inventory item\" })",
        "PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", 'Id', \"JAZZ_M14_MkIII\", 'ClassDisplayName', \"Inventory item\" })",
    ])

    for path in staged.rglob('*'):
        if path.is_file():
            dest = ASSETS / 'Entities' / path.relative_to(staged)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)

    write(ROOT / 'items.lua', items_text)
    write(ROOT / 'metadata.lua', meta)
    write(ASSETS / 'items.lua', asset_items)
    write(ASSETS / 'metadata.lua', asset_meta)
    print('Installed', ', '.join(ENTITIES))


if __name__ == '__main__':
    main()
