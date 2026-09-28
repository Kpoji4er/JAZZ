"""Stage approved M14 visual/Under/T3-1 revision; apply only with JA3/Ged closed.

--output DIR --build DIR --game-root DIR [--apply]
Build contains the audited repair-*-20260927 directories. Keeps original bytes,
source hashes and backups; changes no registration, IDs, price or shop tier.
"""
import argparse, hashlib, io, json, re, shutil, struct, subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
from _integrate_m14_family import find_item_block, matching

ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT.parent

def stage_docs(out, manifest):
    notes = {
        'docs/technical/systems/weapons-ammo-components.md':
            'Локальная правка M14 от 27.09.2026 (`JAZZ-WEAPON-M14-FAMILY-001`, REQ-013–015): '
            '`MK14EBR` маркирован Т3-1, отдельный Bobby shop Tier=4 сохранён. '
            'В M14SAW Under допускаются только `JAZZ_Bipod_Under` и пустой вариант; '
            'существующий setter и LoadGame/NewGame удаляют старые недопустимые компоненты с их эффектами. '
            'M14SAW больше не добавляет SideMountM14, фонари/лазеры используют прямой Side. '
            'В общем хосте M14/M21 исправлены Scope/Bipod/Side/Under spots: '
            '`jazz_assets/Entities/JAZZ_M14.ent`. Roughness деревянных участков '
            '`jazz_assets/Entities/Textures/JAZZ_M14_RM.dds` уменьшена на 12/255; '
            'линейный BC7 и fallback сохранены, Base/Norm/metalness не редактировались. '
            'Пересобраны `Entities/Meshes/MK14EBR{,_BarrelNormal}_Mesh.m.hgm` и '
            '`Entities/Meshes/JAZZ_M14_MkIII{,_BarrelNormal,_MagazineNormal,_MagazineShort}_Mesh.m.hgm` '
            'в jazz_assets. Число треугольников и loop UV сохранены, custom normals отсутствуют. '
            'Compiled geometry/winding и Lua harness PASS; editor save/reload и runtime/human ещё не подтверждены. '
            'Регистрации metadata/EntityData не менялись; WeaponComponent visuals хранятся в items.lua.',
        'docs/wiki/weapons-and-ammo.md':
            'Локальная правка семейства M14 от 27.09.2026: Mk14 EBR относится к Т3-1. '
            'У обычного M14 нижний слот оставлен для сошек; рукояти и гранатомёт убраны, '
            'фонари крепятся у ствола без отдельной планки. Уточнена посадка навесного, '
            'дереву добавлен небольшой блеск. Исправлены грани Mk14 EBR и M14 Mk III. '
            'Изменения проверены офлайн и ещё требуют подтверждения в игре.',
        'docs/showcase/ru/weapons-and-ammo.md':
            'Правка M14 от 27.09.2026: Mk14 EBR — Т3-1; у обычного M14 снизу остаются '
            'только сошки, фонари размещены у ствола без отдельной планки. Подогнано навесное, '
            'дереву добавлен лёгкий блеск, исправлены грани EBR и Mk III. Повторная игровая приёмка ещё требуется.',
        'docs/showcase/en/weapons-and-ammo.md':
            'The local M14 update dated 27 September 2026 assigns Mk14 EBR to T3-1. '
            'The standard M14 keeps only a bipod in its underbarrel slot; lights sit by the barrel '
            'without a separate rail. Attachment placement and a subtle wood sheen were adjusted, '
            'and EBR/Mk III mesh faces were repaired. In-game acceptance is still pending.',
    }
    for rel, note in notes.items():
        source = ROOT/rel; data = source.read_bytes(); split = data.index(b'\n')+1
        nl = b'\r\n' if data[:split].endswith(b'\r\n') else b'\n'
        dest = out/'jazz'/rel; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data[:split]+nl+note.encode('utf-8')+nl+data[split:])
        manifest['jazz/'+rel] = {'before': digest(source), 'after': digest(dest)}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def stage(args):
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    manifest = {}
    def put(path, data):
        rel = path.relative_to(SUITE).as_posix()
        dest = out / rel; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        manifest[rel] = {'before': digest(path), 'after': digest(dest)}
    def under(text):
        at = text.index("'SlotType', \"Under\"")
        start = text.rfind("PlaceObj('WeaponComponentSlot'", 0, at)
        end = matching(text, text.index('(', start))
        block = text[start:end]
        for name in ('JAZZ_GrenadeLauncher_M14', 'JAZZ_TacGrip_M14', 'JAZZ_VerticalGrip_M14'):
            block, count = re.subn(r'^[ \t]*"'+name+r'",\r?\n', '', block, flags=re.M)
            assert count == 1, name
        assert 'JAZZ_Bipod_Under' in block and "'CanBeEmpty', true" in block
        return text[:start] + block + text[end:]

    path = ROOT/'items.lua'; text = path.read_bytes().decode('utf-8')
    start, end = find_item_block(text, 'M14SAW')
    text = text[:start] + under(text[start:end]) + text[end:]
    old = 'Tier 4 - JAZZ-WEAPON-M14-FAMILY-001'
    new = 'Tier 3-1 - JAZZ-WEAPON-M14-FAMILY-001'
    assert text.count(old) == 1
    text = text.replace(old, new)
    visual_changes = []
    def visual(m):
        block = m.group()
        before = block
        # Specific empty Mountside overrides prevent the old floating rail.
        block = block.replace('Entity = "WeaponAttA_SideMountM14"', 'Entity = ""')
        # On/laser variants previously depended on the removed rail's Side1.
        if 'Slot = "Side1"' in block:
            block = block.replace('Slot = "Side1"', 'Slot = "Side"')
        if block != before:
            visual_changes.append(re.sub(r'\s+', ' ', before))
        return block
    text = re.sub(r"PlaceObj\('WeaponComponentVisual',\s*\{[^{}]*?ApplyTo = \"M14SAW\",[^{}]*?\}\)", visual, text, flags=re.S)
    assert len(visual_changes) == 13, len(visual_changes)
    put(path, text.encode('utf-8'))
    path = ROOT/'InventoryItem/M14SAW.lua'
    put(path, under(path.read_bytes().decode('utf-8')).encode('utf-8'))
    path = ROOT/'InventoryItem/MK14EBR.lua'
    data = path.read_bytes(); assert old.encode() in data
    put(path, data.replace(old.encode(), new.encode()))

    path = ROOT/'Code/System_WeaponComponent_Set.lua'
    text = path.read_bytes().decode('utf-8'); nl = '\r\n' if '\r\n' in text else '\n'
    anchor = '\tif not slot then'
    guard = '''\t-- M14 wood stock: Under accepts only a bipod or no component.
\tif self.class == "M14SAW" and slot == "Under" and id ~= "JAZZ_Bipod_Under" then
\t\tid = ""
\t\tdef = nil
\tend
'''.replace('\n', nl)
    assert text.count(anchor) == 1
    text = text.replace(anchor, guard + nl + anchor, 1)
    anchor = '\t\t\tJazzReseatObsoleteMagazineOnFirearm(item)'
    migration = '''\t\t\tif item.class == "M14SAW" and item.components
\t\t\t\tand (item.components.Under or "") ~= ""
\t\t\t\tand item.components.Under ~= "JAZZ_Bipod_Under" then
\t\t\t\titem:SetWeaponComponent("Under", "", "init")
\t\t\tend
'''.replace('\n', nl)
    assert text.count(anchor) == 1
    put(path, text.replace(anchor, migration + anchor, 1).encode('utf-8'))

    # Shared host: align scope shoe over its rail; place bipod and light at barrel.
    path = SUITE/'jazz_assets/Entities/JAZZ_M14.ent'
    text = path.read_bytes().decode('utf-8')
    positions = {'Scope': '18.500,0.000,14.300', 'Bipod': '56.000,0.000,7.100',
                 'Side': '61.000,-0.900,9.500', 'Under': '56.000,0.000,7.100'}
    for name, pos in positions.items():
        pattern = r'(<attach name="'+name+r'" spot_pos=")[^"]+'
        text, count = re.subn(pattern, lambda m: m[1]+pos, text)
        assert count == 1, name
    text, count = re.subn(r'(<attach name="Side"[^>]*spot_rot=")[^"]+',
                         lambda m: m[1]+'1.000000,0.000000,0.000000,90.0000', text)
    assert count == 1
    put(path, text.encode('utf-8'))

    # Repaired geometry only: keep installed .ent spots, materials and DDS.
    entities = {'MK14EBR': args.build/'repair-ebr-winding-20260927',
                'JAZZ_M14_MkIII': args.build/'repair-mkiii-winding-20260927'}
    for name in ('JAZZ_M14_MkIII_BarrelNormal', 'JAZZ_M14_MkIII_MagazineNormal',
                 'JAZZ_M14_MkIII_MagazineShort', 'MK14EBR_BarrelNormal'):
        entities[name] = args.build/'repair-parts-20260927'/name
    for name, build in entities.items():
        audit = json.loads((build/'compiled-audit.json').read_text())
        assert audit['pass'] and audit['entity'] == name, audit
        prepared = json.loads((build/'winding-report.json').read_text())
        assert not prepared['issues'] and prepared['after']['loop_uvs_preserved']
        decoded = json.loads((build/'compiled.json').read_text())
        exported = build.parent.parent/'ExportedEntities'  # AssetsProcessor uses two levels above FBX.
        source = exported/'Meshes'/(name+'_Mesh.m.hgm')
        assert source.is_file(), source
        from _decode_vz58_hgm import decode
        assert decode(source) == decoded, 'Compiled file changed after audit: '+name
        put(SUITE/'jazz_assets/Entities/Meshes'/source.name, source.read_bytes())

    # Numerical material map edit: -12/255 roughness on brown wood only.
    def read_dds(path):
        data = bytearray(path.read_bytes())
        if data[84:88] == b'DX10':
            fmt = struct.unpack_from('<I', data, 128)[0]
            if fmt in (72, 75, 78, 99): struct.pack_into('<I', data, 128, fmt-1)
        return np.array(Image.open(io.BytesIO(data)).convert('RGBA'))
    textures = SUITE/'jazz_assets/Entities/Textures'
    base = read_dds(textures/'JAZZ_M14_Base.dds').astype(float)
    rm = read_dds(textures/'JAZZ_M14_RM.dds'); edited = rm.copy()
    mask = (base[:,:,0] > base[:,:,1]*1.25) & (base[:,:,1] > base[:,:,2]*1.15) & (base[:,:,0] > 20)
    mask[base.shape[0]//2:] = False  # Authored wood islands occupy upper atlas half.
    assert .15 < mask.mean() < .25
    edited[:,:,0][mask] = np.maximum(0, rm[:,:,0][mask].astype(int)-12)
    assert np.array_equal(edited[~mask], rm[~mask])
    assert np.array_equal(edited[:,:,1:], rm[:,:,1:])
    material = out/'material'; material.mkdir(exist_ok=True)
    png = material/'JAZZ_M14_RM.png'; Image.fromarray(edited).save(png)
    cvt = args.game_root/'ModTools/hgimgcvt.exe'
    dds = material/'JAZZ_M14_RM.dds'
    subprocess.run([str(cvt), str(png), str(dds), '--compression', 'BC7', '--profile', 'slow', '--mips', '0'], check=True, capture_output=True)
    assert dds.is_file()
    # hgimgcvt tags PNG exports sRGB; roughness/metalness are linear data.
    raw = bytearray(dds.read_bytes())
    assert raw[84:88] == b'DX10' and struct.unpack_from('<I', raw, 128)[0] in (98, 99)
    struct.pack_into('<I', raw, 128, 98)
    dds.write_bytes(raw)
    fallback = material/'fallback.dds'
    subprocess.run([str(cvt), str(dds), str(fallback), '--truncate', '64'], check=True, capture_output=True)
    put(textures/'JAZZ_M14_RM.dds', dds.read_bytes())
    put(textures/'Fallbacks/JAZZ_M14_RM.dds', fallback.read_bytes())
    (out/'material-report.json').write_text(json.dumps({'wood_fraction': float(mask.mean()),
        'roughness_delta': -12/255, 'before_median': float(np.median(rm[:,:,0][mask]))/255,
        'after_median': float(np.median(edited[:,:,0][mask]))/255,
        'other_channels_preserved_before_compression': True}, indent=2))
    stage_docs(out, manifest)
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2))
    print('STAGED', len(manifest), 'files;', len(visual_changes), 'M14 visual overrides')

def apply(args):
    running = subprocess.run(['powershell', '-NoProfile', '-Command',
        'Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],
        capture_output=True, text=True)
    assert not running.stdout.strip(), 'Close game and editor before applying'
    manifest = json.loads((args.output/'manifest.json').read_text())
    for rel, hashes in manifest.items():
        assert digest(SUITE/rel) == hashes['before'], 'Source changed; restage: '+rel
        assert digest(args.output/rel) == hashes['after'], 'Staging changed: '+rel
    backup = args.output/'backup'
    assert not backup.exists(), 'Backup already exists; inspect previous application'
    for rel in manifest:
        saved = backup/rel; saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(SUITE/rel, saved)
    for rel in manifest:
        shutil.copy2(args.output/rel, SUITE/rel)
    print('APPLIED', len(manifest), 'files; original files retained in backup')

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for key in ('output', 'build', 'game-root'): p.add_argument('--'+key, type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    apply(args) if args.apply else stage(args)
