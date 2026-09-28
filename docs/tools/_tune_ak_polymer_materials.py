"""Tune installed AK74M/AK105 BC1 materials, including every mip and fallback.

Dry-run by default. --output holds immutable originals, staged DDS and report.
--apply accepts original or already-applied hashes only; never compounds edits.
No geometry, material references, metallic channels or registrations change.
"""
import argparse
import hashlib
import io
import json
import struct
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PAIRS = {'AK74M': [(2, 3), (5, 6)], 'AK105': [(2, 3), (5, 6), (8, 9), (11, 12)]}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def words(data):
    assert data[:4] == b'DDS ' and data[84:88] == b'DX10'
    assert struct.unpack_from('<I', data, 128)[0] in (71, 72)
    h, w = struct.unpack_from('<II', data, 12)
    mips = struct.unpack_from('<I', data, 28)[0]
    size = sum(max(1, ((w >> n) + 3) // 4) * max(1, ((h >> n) + 3) // 4) * 8 for n in range(mips))
    assert len(data) == 148 + size
    return np.frombuffer(data, dtype='<u2', offset=148).reshape(-1, 4).copy()


def unpack(colors):
    return np.stack((colors >> 11, (colors >> 5) & 63, colors & 31), axis=-1).astype(float) / [31, 63, 31]


def encode(data, rgb):
    original = words(data)
    result = original.copy()
    q = np.rint(np.clip(rgb, 0, 1) * [31, 63, 31]).astype(np.uint16)
    colors = (q[..., 0] << 11) | (q[..., 1] << 5) | q[..., 2]
    opaque = original[:, 0] > original[:, 1]
    swap = ((colors[:, 0] < colors[:, 1]) & opaque) | ((colors[:, 0] > colors[:, 1]) & ~opaque)
    colors[swap] = colors[swap, ::-1]
    indices = original[:, 2].astype(np.uint32) | (original[:, 3].astype(np.uint32) << 16)
    indices[swap & opaque] ^= np.uint32(0x55555555)
    for shift in range(0, 32, 2):
        flip = swap & ~opaque & (((indices >> shift) & 3) < 2)
        indices[flip] ^= np.uint32(1 << shift)
    # If endpoints collapse, retain the entire original block, including mode.
    collapsed = opaque & (colors[:, 0] == colors[:, 1])
    result[:, :2] = colors
    result[:, 2] = indices & 65535
    result[:, 3] = indices >> 16
    result[collapsed] = original[collapsed]
    output = data[:148] + result.tobytes()
    assert len(output) == len(data) and output[:148] == data[:148]
    return output


def decoded(data):
    header = bytearray(data)
    struct.pack_into('<I', header, 128, 71)
    return np.asarray(Image.open(io.BytesIO(header))).copy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, default=ROOT.parent / 'jazz_assets')
    parser.add_argument('--output', type=Path, default=ROOT / 'tmp/ak-material/tune-v1')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    textures = args.assets / 'Entities/Textures'
    prepared, report = [], []
    for folder in ('', 'Fallbacks'):
        for weapon, pairs in PAIRS.items():
            for base_id, rm_id in pairs:
                names = [Path(folder) / f'AKR_{weapon}_{i}_{kind}.dds' for i, kind in ((base_id, 'Base'), (rm_id, 'RM'))]
                originals = []
                for name in names:
                    backup = args.output / 'before' / name
                    if not backup.exists():
                        backup.parent.mkdir(parents=True, exist_ok=True)
                        backup.write_bytes((textures / name).read_bytes())
                    originals.append(backup.read_bytes())
                base, rm = originals
                b_rgb, r_rgb = unpack(words(base)[:, :2]), unpack(words(rm)[:, :2])
                assert b_rgb.shape == r_rgb.shape
                # Blue is metallic. Smooth block mask avoids hard texture seams.
                metal = np.clip((r_rgb[..., 2].mean(axis=1) - .25) / .5, 0, 1)
                m = metal[:, None]
                if weapon == 'AK74M':
                    r_rgb[..., 0] += .08 * m + .16 * (1 - m)
                    b_rgb *= (.85 * m + .90 * (1 - m))[..., None]
                else:
                    r_rgb[..., 0] += -.035 * m + .08 * (1 - m)
                    b_rgb = b_rgb * (1.30 * m + 1.12 * (1 - m))[..., None] + ((4 * m + 2 * (1 - m)) / 255)[..., None]
                after_rm, after_base = encode(rm, r_rgb), encode(base, b_rgb)
                # Check all mip levels: G/B are byte-exact up to endpoint swaps.
                old, new = words(rm), words(after_rm)
                assert np.array_equal(np.sort(old[:, :2] & 2047, axis=1), np.sort(new[:, :2] & 2047, axis=1))
                before_pixels, after_pixels = decoded(rm), decoded(after_rm)
                assert np.array_equal(before_pixels[..., 1:], after_pixels[..., 1:])
                for name, before, after in zip(names, originals, (after_base, after_rm)):
                    dest = textures / name
                    assert digest(dest.read_bytes()) in (digest(before), digest(after)), f'Unexpected concurrent change: {name}'
                    staged = args.output / 'after' / name
                    staged.parent.mkdir(parents=True, exist_ok=True)
                    staged.write_bytes(after)
                    assert np.array_equal(decoded(before)[..., 3], decoded(after)[..., 3])
                    prepared.append((dest, after))
                    report.append({'path': name.as_posix(), 'before': digest(before), 'after': digest(after), 'bytes': len(after)})
                print(f'{folder or "full"}/{weapon}/{rm_id}: roughness mean {before_pixels[..., 0].mean()/255:.3f} -> {after_pixels[..., 0].mean()/255:.3f}; metallic unchanged')
    (args.output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    if args.apply:
        for dest, data in prepared:
            dest.write_bytes(data)
        assert all(dest.read_bytes() == data for dest, data in prepared)
    print(f'{"Installed" if args.apply else "Staged"} {len(prepared)} DDS; headers, dimensions, mips and alpha preserved.')


if __name__ == '__main__':
    main()
