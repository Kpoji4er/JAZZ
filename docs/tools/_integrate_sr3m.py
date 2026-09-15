"""Install the tested SR3M export and matching ModItems as a bounded transaction.

python docs/tools/_integrate_sr3m.py --export-root <ExportedEntities> --build <build>
Requires the game/editor closed. Original core files are backed up under build.
"""
import argparse
import csv
import io
import re
import shutil
import subprocess
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT.parent / 'jazz_assets'
ENTITIES = ['SR3M', 'SR3M_Handguard', 'SR3M_Magazine', 'SR3M_Muzzle', 'SR3M_Stock', 'SR3M_StockFolded']
TEXTS = {
    'DisplayName': (761915300101, 'СР-3М', 'SR-3M'),
    'DisplayNamePlural': (761915300102, 'СР-3М', 'SR-3M'),
    'Description': (761915300103,
        'Компактный автомат под патрон 9×39 мм со складным прикладом и магазином на 30 патронов. В этой комплектации установлен штатный дульный насадок, без глушителя.',
        'A compact 9x39 mm carbine with a folding stock and a 30-round magazine. This configuration uses the standard muzzle device, without a suppressor.'),
}

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as f:
        f.write(text.replace('\r\n', '\n').replace('\n', '\r\n'))

def matching(text, start, opener='(', closer=')'):
    """Balanced delimiters, skipping Lua quoted/long strings and comments."""
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
                if i < 0: raise ValueError('Unclosed expression')
            continue
        if c in '\"\'':
            quote = c
            i += 1
            while i < len(text):
                if text[i] == '\\': i += 2
                elif text[i] == quote: i += 1; break
                else: i += 1
            continue
        long = re.match(r'\[(=*)\[', text[i:]) if c == '[' else None
        if long:
            end = ']' + long[1] + ']'
            i = text.index(end, i + len(long[0])) + len(end)
            continue
        if c == opener: depth += 1
        if c == closer:
            depth -= 1
            if depth == 0: return i+1
        i += 1
    raise ValueError('Unbalanced Lua')

def append_root_item(text, item):
    pos = text.rfind('}')
    assert pos > 0 and text[:pos].rstrip().endswith(',')
    return text[:pos] + item + '\n' + text[pos:]

def add_metadata(text, key, lines):
    match = re.search(r"'" + key + r"',\s*\{", text)
    assert match, key
    pos = match.end()
    return text[:pos] + '\n' + ''.join('\t\t' + line + ',\n' for line in lines) + text[pos:]

def weapon():
    text = (ROOT / 'InventoryItem/AS_Val.lua').read_text(encoding='utf-8')
    text = text.replace('AS_Val', 'SR3M').replace('ASVal', 'SR3M').replace('ASVAL.png','SR3M.png')
    text = text.replace('"Carbine"', '"SubmachineGun"')
    for field, (ident, ru, en) in TEXTS.items():
        text = re.sub(r'^\t' + field + r' = .*$',
            f'\t{field} = T({ident}, --[[ModItemInventoryItemCompositeDef SR3M {field}]] "{ru}"),', text, flags=re.M)
    text = re.sub(r'^\tAdditionalHint = .*\n', '', text, flags=re.M)
    values = {'comment':'"Tier 3-2"',
        'CanAppearInShop':'false', 'RestockWeight':'0', 'MagazineSize':'30', 'Noise':'30',
        'Cost':'18000', 'AimAccuracy':'10', 'WeaponRange':'26', 'WeaponMass':'27',
        'Damage':'32', 'Recoil':'20', 'Grouping':'58', 'BulletDropRange':'11',
        'ReloadAP':'5000', 'CloseRange':'3', 'CloseRangeFactor':'95',
        'WeaponSizeClass':'"Compact"', 'CategoryPair':'"SubmachineGuns"'}
    for field, val in values.items():
        text, n = re.subn(r'^\t' + field + r' = [^\n]+', f'\t{field} = {val},', text, flags=re.M)
        assert n == 1, field
    # Existing unsuppressed AK74 FX avoids a silent weapon without introducing FX hooks.
    text = text.replace('\tEntity = "SR3M",', '\tEntity = "SR3M",\n\tfxClass = "AK74",')
    text = text.replace('"RunAndGun_Carbine"', '"RunAndGun"').replace('"JAZZ_TargetSweep"','"JAZZ_Zipper"')
    text = text.replace('\tAimAccuracy = 10,','\tAimAccuracy = 10,\n\tMaxAimActions = 2,')
    a = text.index('\tComponentSlots = {')
    b = matching(text, text.index('{', a), '{', '}')
    slots = [('Magazine',['JAZZ_MagNormal'],'JAZZ_MagNormal'),
             ('Handguard',['JAZZ_Handguard'],'JAZZ_Handguard'),
             ('Muzzle',['JAZZ_DefMuzzle'],'JAZZ_DefMuzzle'),
             ('Stock',['JAZZ_StockLightFolded','JAZZ_StockLightUnFolded'],'JAZZ_StockLightUnFolded')]
    block = '\tComponentSlots = {\n'
    for slot, components, default in slots:
        comps = ', '.join('"'+c+'"' for c in components)
        block += f"\t\tPlaceObj('WeaponComponentSlot', {{\n\t\t\t'SlotType', \"{slot}\",\n\t\t\t'Modifiable', false,\n\t\t\t'AvailableComponents', {{ {comps} }},\n\t\t\t'DefaultComponent', \"{default}\",\n\t\t}}),\n"
    text = text[:a] + block + '\t}' + text[b:]
    props = text[text.index('\tcomment ='):text.rfind('}')]
    # Only top-level named properties become ModItem's alternating key/value array.
    props = re.sub(r'^\t([A-Za-z_][A-Za-z_0-9]*) = ', r"\t'\1', ", props, flags=re.M)
    item = "\tPlaceObj('ModItemInventoryItemCompositeDef', {\n\t\t'Id', \"SR3M\",\n" + props + '\t}),'
    return text, item

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--export-root', required=True)
    p.add_argument('--build', required=True)
    p.add_argument('--game-root', required=True)
    args = p.parse_args()
    export = Path(args.export_root).resolve()
    build = Path(args.build).resolve()
    items = (ROOT/'items.lua').read_text(encoding='utf-8')
    assert not re.search(r"'Id',\s*\"SR3M\"", items), 'Already integrated; review before rerun'
    for ident, _, _ in TEXTS.values():
        assert str(ident) not in items, 'Localization ID collision'
    for ent in ENTITIES:
        assert (export/(ent+'.ent')).is_file(), ent
    backup = build/'integration-backup'
    for package in [ROOT, ASSETS]:
        for name in ['items.lua','metadata.lua']:
            target = backup/package.name/name
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                assert target.read_bytes() == (package/name).read_bytes(), 'Source changed since backup'
            else:
                shutil.copy2(package/name, target)

    # Resolve the complete resource graph before installing it. Numeric export DDS
    # get stable names in the private staging graph, before first mod import.
    staged = build/'mod-assets-stage'
    staged.mkdir(exist_ok=True)
    suffixes = {'BaseColorMap':'Base','NormalMap':'Norm','RMMap':'RM','AOMap':'AO',
                'SpecialMap':'SPEC','SIMap':'SI','ColorizationMap':'Color'}
    texture_names = {}
    for ent in ENTITIES:
        tree = ET.parse(export/(ent+'.ent'))
        tree.getroot().set('name', ent)
        for lod in tree.findall('.//lod'):
            for src in list(lod.findall('src')): lod.remove(src)
        for node in tree.findall('.//mesh'):
            rel = node.attrib['file']
            dest = staged/rel
            dest.parent.mkdir(exist_ok=True, parents=True)
            shutil.copy2(export/rel, dest)
        for node in tree.findall('.//material'):
            rel = node.attrib['file']
            mtl = ET.parse(export/rel)
            for tag in mtl.getroot().iter():
                name = tag.get('Name')
                if name and tag.tag in suffixes:
                    src = export/'Textures'/name
                    assert src.is_file(), src
                    key = (suffixes[tag.tag], hashlib.sha256(src.read_bytes()).hexdigest())
                    new = texture_names.get(key, ent + '_' + suffixes[tag.tag] + '.dds')
                    texture_names[key] = new
                    dest = staged/'Textures'/new
                    dest.parent.mkdir(exist_ok=True, parents=True)
                    # Use official mip truncation; keep at most 2048px for the test asset.
                    cvt = str(Path(args.game_root)/'ModTools/hgimgcvt.exe')
                    subprocess.run([cvt,str(src),str(dest),'--truncate','2048'],check=True,capture_output=True)
                    fallback = staged/'Textures/Fallbacks'/new
                    fallback.parent.mkdir(exist_ok=True,parents=True)
                    subprocess.run([cvt,str(dest),str(fallback),'--truncate','64'],check=True,capture_output=True)
                    tag.set('Name',new)
            dest = staged/rel
            dest.parent.mkdir(exist_ok=True, parents=True)
            mtl.write(dest,encoding='utf-8',xml_declaration=True)
        tree.write(staged/(ent+'.ent'),encoding='utf-8',xml_declaration=True)
        write(staged/(ent+'.lua'), f'EntityData["{ent}"] = {{\n\teditor_artset = "Mods",\n}}\n')

    companion, item = weapon()
    items = append_root_item(items, item)
    visuals = {'JAZZ_MagNormal':('SR3M_Magazine','Magazine'),
        'JAZZ_Handguard':('SR3M_Handguard','Handguard'), 'JAZZ_DefMuzzle':('SR3M_Muzzle','Muzzle'),
        'JAZZ_StockLightUnFolded':('SR3M_Stock','Stock'), 'JAZZ_StockLightFolded':('SR3M_StockFolded','Stock')}
    for ident, (entity, slot) in visuals.items():
        m = re.search(r'\bid\s*=\s*"'+ident+'"',items)
        assert m, ident
        start = items.rfind("PlaceObj('ModItemWeaponComponent'", 0, m.start())
        end = matching(items, items.index('(',start))
        block = items[start:end]
        assert re.search(r'\bid\s*=\s*"'+ident+'"',block)
        block, n = re.subn(r'Visuals\s*=\s*\{', 'Visuals = {\n' +
            f"\t\t\tPlaceObj('WeaponComponentVisual', {{ ApplyTo = \"SR3M\", Entity = \"{entity}\", Slot = \"{slot}\", param_bindings = false }}),", block, count=1)
        assert n == 1
        items = items[:start]+block+items[end:]

    asset_items=(ASSETS/'items.lua').read_text(encoding='utf-8')
    folder="\tPlaceObj('ModItemFolder', { 'name', \"SR3M\" }, {\n"
    for ent in ENTITIES:
        folder += f"\t\tPlaceObj('ModItemEntity', {{ 'name', \"{ent}\", 'ClassParents', {{}}, 'entity_name', \"{ent}\" }}),\n"
    folder+='\t}),'
    asset_items=append_root_item(asset_items,folder)
    asset_meta=(ASSETS/'metadata.lua').read_text(encoding='utf-8')
    asset_meta=add_metadata(asset_meta,'entities',['"'+e+'"' for e in ENTITIES])
    asset_meta=add_metadata(asset_meta,'code',['"Entities/'+e+'.lua"' for e in ENTITIES])
    meta=add_metadata((ROOT/'metadata.lua').read_text(encoding='utf-8'),'code',['"InventoryItem/SR3M.lua"'])
    meta=add_metadata(meta,'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"InventoryItemCompositeDef\", 'Id', \"SR3M\", 'ClassDisplayName', \"Inventory item\" })"])

    for path in staged.rglob('*'):
        if path.is_file():
            dest=ASSETS/'Entities'/path.relative_to(staged)
            assert not dest.exists(), dest
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,dest)
    write(ROOT/'InventoryItem/SR3M.lua',companion)
    write(ROOT/'items.lua',items)
    write(ROOT/'metadata.lua',meta)
    write(ASSETS/'items.lua',asset_items)
    write(ASSETS/'metadata.lua',asset_meta)
    image=Image.open(build/'SR3M_preview.png').convert('RGBA')
    image=image.crop(image.getchannel('A').getbbox())
    image.thumbnail((480,230),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(512,256))
    canvas.alpha_composite(image,((512-image.width)//2,(256-image.height)//2))
    canvas.save(ROOT/'WeaponIcons/SR3M.png')
    print('Installed SR3M: 6 entities, 5 component visuals, synchronized ModItems and companion.')

if __name__ == '__main__': main()
