"""Read-only material inventory for every explicit ZIP/RAR/GLB in weaponslist.txt.

Writes JSON evidence and Markdown report; does not extract into source directories,
launch JA3, import models, or infer that loose textures are assigned materials.
"""
import argparse
from collections import Counter
import io
import json
from pathlib import Path
import re
import struct
import subprocess
import zipfile

from PIL import Image

IMAGES = {'.png', '.jpg', '.jpeg', '.tga', '.dds', '.bmp', '.tif', '.tiff', '.webp'}
MODELS = {'.obj', '.fbx', '.blend', '.glb', '.gltf', '.3ds', '.max', '.c4d'}


def glb_info(data):
    magic, version, size = struct.unpack_from('<4sII', data)
    if magic != b'glTF' or version != 2 or size != len(data):
        raise ValueError('Invalid GLB header')
    offset, doc, binary = 12, None, b''
    while offset < size:
        length, kind = struct.unpack_from('<II', data, offset)
        chunk = data[offset + 8:offset + 8 + length]
        if kind == 0x4E4F534A:
            doc = json.loads(chunk)
        elif kind == 0x004E4942:
            binary = chunk
        offset += 8 + length
    images = []
    for im in doc.get('images', []):
        item = dict(im)
        if 'bufferView' in im:
            view = doc['bufferViews'][im['bufferView']]
            start = view.get('byteOffset', 0)
            payload = binary[start:start + view['byteLength']]
            with Image.open(io.BytesIO(payload)) as pic:
                pic.load()
                item['size'] = list(pic.size)
            item['embedded_valid'] = True
        else:
            item['embedded_valid'] = False
        images.append(item)
    primitives = [p for mesh in doc.get('meshes', []) for p in mesh['primitives']]
    return {'materials': doc.get('materials', []), 'images': images,
            'textures': doc.get('textures', []),
            'primitives': [{'material': p.get('material'),
                            'uv': 'TEXCOORD_0' in p['attributes']} for p in primitives]}


def inventory(names, read, prefix='', depth=0):
    result = {'files': [], 'textures': [], 'objects': [], 'mtl': {}, 'containers': [], 'glb': []}
    for name in names:
        full = prefix + name
        suffix = Path(name).suffix.lower()
        result['files'].append(full)
        if suffix in IMAGES:
            entry = {'file': full}
            try:
                with Image.open(io.BytesIO(read(name))) as pic:
                    pic.load()
                    entry.update(size=list(pic.size), mode=pic.mode, readable=True)
            except Exception as exc:
                entry.update(readable=False, error=str(exc))
            result['textures'].append(entry)
        elif suffix == '.obj':
            text = read(name).decode('utf-8', errors='replace')
            result['objects'].append({'file': full,
                'uv_count': len(re.findall(r'^vt\s', text, re.M)),
                'mtllib': re.findall(r'^mtllib\s+(.+)', text, re.M),
                'usemtl': sorted(set(re.findall(r'^usemtl\s+(.+)', text, re.M)))})
        elif suffix == '.mtl':
            result['mtl'][full] = read(name).decode('utf-8', errors='replace')
        elif suffix == '.glb':
            result['glb'].append({'file': full, **glb_info(read(name))})
        elif suffix in {'.blend', '.fbx', '.max', '.c4d', '.gltf'}:
            result['containers'].append(full)
        elif suffix == '.zip' and depth < 3:
            with zipfile.ZipFile(io.BytesIO(read(name))) as nested:
                child = inventory(nested.namelist(), nested.read, full + '!/', depth + 1)
                for key in result:
                    if isinstance(result[key], dict):
                        result[key].update(child[key])
                    else:
                        result[key].extend(child[key])
    return result


def rar_inventory(path, sevenzip):
    proc = subprocess.run([sevenzip, 'l', '-slt', '-sccUTF-8', str(path)],
                          check=True, capture_output=True)
    listing = proc.stdout.decode('utf-8').split('----------', 1)[1]
    names = [re.search(r'^Path = (.+)$', block, re.M).group(1).strip()
             for block in re.split(r'\r?\n\r?\n', listing.strip())
             if re.search(r'^Path = ', block, re.M) and 'Folder = +' not in block]
    def read(name):
        return subprocess.run([sevenzip, 'x', '-so', str(path), name],
                              check=True, capture_output=True).stdout
    return inventory(names, read)


def classify(row):
    textures = [x for x in row['textures'] if x['readable'] and
                'internal_ground' not in x['file'].lower()]
    if row['glb']:
        good = all(g['materials'] and g['images'] and
                   all(im['embedded_valid'] for im in g['images']) and
                   all(p['material'] is not None and p['uv'] for p in g['primitives'])
                   for g in row['glb'])
        return ('MATERIALS_PRESENT', 'GLB: embedded images decoded; primitive materials and UV present') if good else (
            'REVIEW', 'GLB material/image/UV coverage incomplete')
    if not textures and not row['mtl'] and not row['containers']:
        return 'REJECT', 'No weapon textures or material definitions; geometry only'
    if not textures:
        return 'REVIEW', 'Inspect embedded/procedural materials; no readable loose weapon textures'
    if any(not x['readable'] for x in row['textures']):
        return 'REVIEW', 'Some texture files could not be decoded'
    if any(o['uv_count'] == 0 for o in row['objects']):
        missing = ', '.join(o['file'] for o in row['objects'] if not o['uv_count'])
        return 'REVIEW', f'Textures exist but OBJ lacks UV: {missing}'
    if row['objects'] and not row['mtl']:
        return 'TEXTURES_PRESENT', 'Textures and UV exist; MTL absent, assignments require reconstruction'
    return 'TEXTURES_PRESENT', 'Textures decoded; material assignment/coverage needs model inspection'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--list', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--sevenzip', default='C:/Program Files/7-Zip/7z.exe')
    args = p.parse_args()
    paths = list(dict.fromkeys(re.findall(r'@([^@\r\n]+?\.(?:zip|rar|glb))',
                          args.list.read_text(encoding='utf-8-sig'), re.I)))
    rows = []
    for number, value in enumerate(paths, 1):
        path = Path(value)
        row = {'path': value, 'name': path.name}
        try:
            if path.suffix.lower() == '.zip':
                with zipfile.ZipFile(path) as z:
                    row.update(inventory(z.namelist(), z.read))
            elif path.suffix.lower() == '.rar':
                row.update(rar_inventory(path, args.sevenzip))
            else:
                row.update(inventory([path.name], lambda _: path.read_bytes()))
            row['status'], row['reason'] = classify(row)
        except Exception as exc:
            row.update(status='REVIEW', reason=str(exc))
        rows.append(row)
        print(f'{number}/{len(paths)} {row["status"]} {path.name}', flush=True)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.with_suffix('.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    summary = dict(Counter(r['status'] for r in rows))
    lines = ['# Аудит материалов weaponslist — 2026-09-23', '',
             'Проверены все явно указанные ZIP/RAR/GLB, включая вложенные ZIP. JA3 не запускалась.',
             'REJECT: отсутствуют материалы и текстуры оружия. TEXTURES_PRESENT: карты прочитаны, но это не подтверждение назначения всех материалов. MATERIALS_PRESENT: GLB с материалами, UV и встроенными изображениями. REVIEW: нужна дополнительная проверка.',
             '', f'Всего: {len(rows)}. {summary}', '',
             '| Источник | Статус | Текстур | MTL | Примечание |',
             '| --- | --- | ---: | ---: | --- |']
    for row in rows:
        lines.append(f'| {row["name"]} | {row["status"]} | {len(row.get("textures", []))} | {len(row.get("mtl", {}))} | {row["reason"]} |')
    lines += ['', 'JSON рядом содержит полный состав архивов, размеры изображений, OBJ UV/material references, MTL и GLB material records.',
              'Это входной фильтр источников; не свидетельство готовности геометрии, баланса или игрового импорта.']
    args.out.with_suffix('.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(summary)


if __name__ == '__main__':
    main()
