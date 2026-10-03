"""Repack installed weapon RM through uncompressed TGA and official hgimgcvt.

stage --assets PATH --game-root PATH --build NEW_PATH [--prefix NAME ...]
apply --assets PATH --build PATH (requires JA3/editor closed); audit --build PATH
Preserves decoded R/B as input, replaces G with R, keeps BC1/BC7 and all mips.
Does not rebuild geometry or claim to fix tangent-space normals.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image

DEFAULT_PREFIXES = ('JAZZ_VZ58', 'JAZZ_VektorR4', 'AKR_AK103')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def header(path):
    b = path.read_bytes()
    assert b[:4] == b'DDS ', path
    h, w = struct.unpack_from('<II', b, 12)
    mips = struct.unpack_from('<I', b, 28)[0]
    fourcc = b[84:88]
    fmt = struct.unpack_from('<I', b, 128)[0] if fourcc == b'DX10' else None
    assert (fourcc == b'DX10' and fmt in (71,98)) or fourcc == b'DXT1', (path, fourcc, fmt)
    offset = 148 if fourcc == b'DX10' else 128
    block_size = 16 if fmt == 98 else 8
    expected = offset + sum(max(1, (max(1,w>>i)+3)//4)*max(1, (max(1,h>>i)+3)//4)*block_size for i in range(mips))
    assert len(b) == expected, (path, len(b), expected)
    assert mips == 1 + int(math.log2(max(w,h))), (path, mips)
    return {'width':w, 'height':h, 'mips':mips, 'fourcc':fourcc.decode(), 'dxgi':fmt}


def pixels(path):
    with Image.open(path) as im:
        return np.array(im.convert('RGB'))


def run_converter(exe, source, dest, *flags):
    result = subprocess.run([str(exe),str(source),str(dest),*flags], capture_output=True, text=True)
    if result.returncode or not dest.exists():
        raise RuntimeError(result.stdout + result.stderr)


def stage(a):
    a.build.mkdir(parents=True, exist_ok=False)
    tex = a.assets/'Entities/Textures'
    refs, guards = {}, {}
    for prefix in a.prefix or DEFAULT_PREFIXES:
        materials = sorted((a.assets/'Entities/Materials').glob(prefix+'*.mtl'))
        assert materials, prefix
        for mat in materials:
            guards[str(mat.relative_to(a.assets))] = sha(mat)
            for node in ET.parse(mat).getroot().iter():
                name = node.get('Name')
                if not name or not name.endswith('.dds'):
                    continue
                assert Path(name).name == name, name
                if node.tag == 'RMMap':
                    refs.setdefault(name, []).append(mat.name)
                else:
                    for p in (tex/name, tex/'Fallbacks'/name):
                        assert p.is_file(), p
                        guards[str(p.relative_to(a.assets))] = sha(p)
        for folder, pattern in [('Entities',prefix+'*.ent'), ('Entities/Meshes',prefix+'*.hgm')]:
            for p in (a.assets/folder).glob(pattern):
                guards[str(p.relative_to(a.assets))] = sha(p)
    exe = a.game_root/'ModTools/hgimgcvt.exe'
    report = {'converter_sha256':sha(exe), 'prefixes':list(a.prefix or DEFAULT_PREFIXES),
              'guards':guards, 'maps':[], 'files':[], 'applied':False}
    for name, materials in sorted(refs.items()):
        src = tex/name
        old = pixels(src); meta = header(src)
        rg = np.abs(old[:,:,0].astype(np.int16)-old[:,:,1].astype(np.int16))
        if rg.mean() <= 3 and np.percentile(rg,99) <= 12:
            for unchanged in (src,tex/'Fallbacks'/name):
                guards[str(unchanged.relative_to(a.assets))] = sha(unchanged)
            continue
        new = old.copy(); new[:,:,1] = new[:,:,0]
        tga = a.build/'tga'/Path(name).with_suffix('.tga')
        tga.parent.mkdir(exist_ok=True)
        Image.fromarray(new).save(tga, compression=None)
        assert tga.read_bytes()[2] == 2 and tga.read_bytes()[16] == 24
        assert np.array_equal(pixels(tga),new)
        full = a.build/'staged/Entities/Textures'/name
        full.parent.mkdir(parents=True,exist_ok=True)
        compression = 'BC7' if meta['dxgi'] == 98 else 'BC1'
        run_converter(exe,tga,full,'--compression',compression,'--alpha','0','--mips',str(meta['mips']))
        # hgimgcvt labels BC7 color output sRGB by default; RM is numeric data.
        raw = bytearray(full.read_bytes())
        if raw[84:88] == b'DX10' and struct.unpack_from('<I',raw,128)[0] == 99:
            struct.pack_into('<I',raw,128,98)
            full.write_bytes(raw)
        out_meta = header(full)
        assert (out_meta['width'],out_meta['height']) == (meta['width'],meta['height'])
        dec = pixels(full).astype(np.int16)
        delta = np.abs(dec-new.astype(np.int16))
        # BC1's shared indices can move values on re-encode. Fail on broad drift.
        errors = {c:{'mean':float(delta[:,:,i].mean()),'p99':float(np.percentile(delta[:,:,i],99)),
                     'max':int(delta[:,:,i].max())} for i,c in enumerate('RGB')}
        assert all(errors[c]['mean'] <= 3 and errors[c]['p99'] <= 12 for c in 'RB'), (name,errors)
        assert float(np.abs(dec[:,:,0]-dec[:,:,1]).mean()) < 3, name
        fallback = full.parent/'Fallbacks'/name; fallback.parent.mkdir(exist_ok=True)
        old_fb = header(tex/'Fallbacks'/name)
        assert old_fb['width'] == old_fb['height'] == min(64,meta['width'])
        run_converter(exe,full,fallback,'--truncate',str(old_fb['width']))
        fb_meta = header(fallback)
        assert fb_meta['width'] == fb_meta['height'] == old_fb['width']
        report['maps'].append({'name':name, 'materials':materials, 'before':meta,'after':out_meta,
             'tga_sha256':sha(tga),'source_g_max':int(old[:,:,1].max()),'compression_error':errors})
        for dest in (full,fallback):
            rel = dest.relative_to(a.build/'staged'); original = a.assets/rel
            backup = a.build/'backup'/rel; backup.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(original,backup)
            report['files'].append({'path':str(rel),'before':sha(original),'after':sha(dest)})
    (a.build/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'maps':len(report['maps']),'files':len(report['files']),'build':str(a.build)}))


def audit(a):
    report = json.loads((a.build/'manifest.json').read_text(encoding='utf-8'))
    inspect_header = header
    if report.get('kind') == 'author-textures':
        from _audit_recent_weapon_textures import dds
        inspect_header = dds
    for item in report['files']:
        for folder,key in [('backup','before'),('staged','after')]:
            p = a.build/folder/item['path']; assert sha(p) == item[key], p; inspect_header(p)
    print('PASS: staged DDS, complete mip chains, backups and manifest hashes')
    return report


def apply(a):
    report = audit(a)
    ps = subprocess.run(['powershell','-NoProfile','-Command',
        "@(Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True,check=True)
    assert ps.stdout.strip() == '0', 'Close JA3 and Mod Editor before apply'
    for rel,h in report['guards'].items():
        assert sha(a.assets/rel) == h, 'Concurrent resource change: '+rel
    for f in report['files']:
        assert sha(a.assets/f['path']) == f['before'], 'Concurrent RM change: '+f['path']
    done = []
    try:
        for f in report['files']:
            dest = a.assets/f['path']; done.append(f)
            shutil.copy2(a.build/'staged'/f['path'],dest)
            assert sha(dest) == f['after'], dest
    except BaseException:
        for f in done:
            shutil.copy2(a.build/'backup'/f['path'],a.assets/f['path'])
        raise
    for rel,h in report['guards'].items():
        assert sha(a.assets/rel) == h, rel
    report['applied'] = True
    (a.build/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('PASS: installed; all guarded resources and material bindings unchanged')


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=('stage','apply','audit'))
    p.add_argument('--assets',type=Path)
    p.add_argument('--game-root',type=Path)
    p.add_argument('--build',type=Path,required=True)
    p.add_argument('--prefix',action='append')
    a=p.parse_args()
    if a.mode in ('stage','apply') and not a.assets:p.error('--assets required')
    if a.mode=='stage' and not a.game_root:p.error('--game-root required')
    {'stage':stage,'apply':apply,'audit':audit}[a.mode](a)
