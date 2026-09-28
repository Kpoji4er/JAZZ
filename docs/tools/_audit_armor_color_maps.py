"""Decode installed armor albedo for review (normalizes sRGB DDS header for Pillow)."""
import argparse
import io
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image

def decode(path):
    data = bytearray(path.read_bytes())
    if data[84:88] == b'DX10':
        fmt = struct.unpack_from('<I', data, 128)[0]
        if fmt in (72, 75, 78, 99):
            struct.pack_into('<I', data, 128, fmt - 1)
    return Image.open(io.BytesIO(data))

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    root = a.assets / 'Entities'
    for family in ('Chainmail', 'GuardianLight', 'TwaronLight', 'ZylonLight'):
        tree = ET.parse(root / ('JAZZ_' + family + '_Male.ent'))
        for i, ref in enumerate(sorted({n.get('file') for n in tree.findall('.//material')})):
            name = ET.parse(root / ref).find('.//BaseColorMap').get('Name')
            im = decode(root / 'Textures' / name)
            im.save(a.output / (family + str(i) + '.png'))
            print(family, ref, name, im.size)
