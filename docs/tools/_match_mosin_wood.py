"""Match short Mosin wood to the long rifle's diffuse material, without rebaking.

Preview by default; --apply installs four DDS files. Hash-pinned backups in the
same --output make reruns idempotent. Requires numpy/Pillow. This is an offline
material approximation, not proof of equal appearance in the engine lighting.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
HASHES = {
    "MOSIN_7_Base.dds": "09cea278250f4119c938d4ee90c1e165432360ba9f6c5090adac2ed52683e456",
    "Fallbacks/MOSIN_7_Base.dds": "be8fa22134623ef11a93a4076559ba0e1263a8df63882d23aa496e9dc3dc44d1",
    "MOSIN_11_Base.dds": "601c7c6c006c5294668263495497eae02267f3a11ff0d268a79b0e7c3f12ee7e",
    "Fallbacks/MOSIN_11_Base.dds": "22438dd5d9a6e16c9a3cd1a1dc67ff8fca89a42ac05642fa04cf42af60e91059",
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    data = bytearray(data)
    if struct.unpack_from('<I', data, 128)[0] == 72:
        struct.pack_into('<I', data, 128, 71)  # Pillow alias only, never installed.
    return np.array(Image.open(io.BytesIO(data)).convert('RGB'), dtype=float)


def levels(data):
    assert data[:4] == b'DDS ' and data[84:88] == b'DX10'
    assert struct.unpack_from('<I', data, 128)[0] in (71, 72)
    height, width = struct.unpack_from('<II', data, 12)
    offset = 148
    for _ in range(struct.unpack_from('<I', data, 28)[0]):
        size = max(1, (width + 3) // 4) * max(1, (height + 3) // 4) * 8
        header = bytearray(data[:148])
        struct.pack_into('<II', header, 12, height, width)
        struct.pack_into('<I', header, 28, 1)
        yield offset, size, decode(header + data[offset:offset + size])
        offset += size
        width, height = max(1, width // 2), max(1, height // 2)
    assert offset == len(data)


def wood(base, rm):
    # Metallic blue excludes steel/brass, including brown rusty metal pixels.
    # Use material identity, not albedo: dark grain and pale scratches are wood too.
    return (rm[..., 2] < 24) & (rm[..., 0] > 24)


def srgb(linear):
    return 255 * np.where(linear <= .0031308, 12.92 * linear,
                          1.055 * np.maximum(linear, 0) ** (1 / 2.4) - .055)


def correct(data, mask_image, source_median, target):
    output = bytearray(data)
    unchanged = changed = 0
    for offset, size, base in levels(data):
        # Derive every mip/fallback mask from the same full-resolution material,
        # so small mixed mip texels cannot silently lose their wood correction.
        mask = np.array(mask_image.resize((base.shape[1], base.shape[0]), Image.Resampling.BOX), dtype=float) / 255
        height, width = mask.shape
        mask = np.pad(mask, ((0, (-height) % 4), (0, (-width) % 4)), mode='edge')
        coverage = mask.reshape(mask.shape[0] // 4, 4, mask.shape[1] // 4, 4).mean((1, 3)).ravel()
        weight = coverage
        original = np.frombuffer(data, dtype='<u2', offset=offset, count=size // 2).reshape(-1, 4)
        words = original.copy()
        colors = words[:, :2].copy()
        rgb = np.stack(((colors >> 11) * (255 / 31), ((colors >> 5) & 63) * (255 / 63),
                        (colors & 31) * (255 / 31)), axis=-1)
        lum_weights = np.array([.2126, .7152, .0722])
        lum = rgb @ lum_weights
        median_lum = source_median @ lum_weights
        # Keep grain and scratches; compress extreme dark contrast while bringing
        # both source palettes to the same reference diffuse reflectance.
        mapped = target * (np.maximum(lum, 0) / median_lum)[..., None] ** .65
        mapped += .25 * (rgb - lum[..., None] * source_median / median_lum)
        adjusted = rgb + weight[:, None, None] * (mapped - rgb)
        q = np.rint(np.clip(adjusted, 0, 255) * np.array([31, 63, 31]) / 255).astype(np.uint16)
        encoded = (q[..., 0] << 11) | (q[..., 1] << 5) | q[..., 2]
        opaque = colors[:, 0] > colors[:, 1]
        swap = ((encoded[:, 0] < encoded[:, 1]) & opaque) | ((encoded[:, 0] > encoded[:, 1]) & ~opaque)
        encoded[swap] = encoded[swap, ::-1]
        indices = words[:, 2].astype(np.uint32) | (words[:, 3].astype(np.uint32) << 16)
        indices[swap & opaque] ^= np.uint32(0x55555555)
        for shift in range(0, 32, 2):
            flip = swap & ~opaque & (((indices >> shift) & 3) < 2)
            indices[flip] ^= np.uint32(1 << shift)
        collapsed = opaque & (encoded[:, 0] == encoded[:, 1])
        nonblack = collapsed & (encoded[:, 0] > 0)
        encoded[nonblack, 1] -= 1
        indices[nonblack] = 0
        black = collapsed & ~nonblack
        encoded[black, 0] = 1
        indices[black] = np.uint32(0x55555555)
        words[:, :2] = encoded
        words[:, 2], words[:, 3] = indices & 65535, indices >> 16
        # Boundary/background/metal-only blocks stay byte-for-byte intact.
        words[weight == 0] = original[weight == 0]
        assert np.array_equal(words[weight == 0], original[weight == 0])
        changed += int(np.any(words != original, axis=1).sum())
        unchanged += int((weight == 0).sum())
        output[offset:offset + size] = words.tobytes()
    assert output[:148] == data[:148] and len(output) == len(data)
    return bytes(output), {'changed_blocks': changed, 'protected_blocks': unchanged}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, default=ROOT.parent / 'jazz_assets')
    parser.add_argument('--output', type=Path, default=ROOT / 'tmp/mosin-wood-match')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    textures = args.assets / 'Entities/Textures'
    args.output.mkdir(parents=True, exist_ok=True)
    reference = (textures / 'Mosin_BASE.dds').read_bytes()
    assert sha(reference) == '8e57635c53078337135c2521c3c4c49768f93cd0a1fa00fdf64a70f0c5316cad'
    assert struct.unpack_from('<I', reference, 128)[0] == 98, 'Reference must be linear BC7'
    base = decode(reference)
    ref_rm = decode((textures / 'Mosin_RM.dds').read_bytes())
    assert sha((textures / 'Mosin_RM.dds').read_bytes()) == 'a603d725ee2b882718f37dc136dc143f62ce5e73e67021462f99342a15f00cf4'
    # Interior of the broad old stock UV island; no brass or edge padding.
    crop = np.zeros(base.shape[:2], dtype=bool)
    crop[420:660, 140:1370] = True
    crop &= (base[..., 0] > base[..., 1] * 1.25) & (base[..., 1] > base[..., 2] * 1.2)
    # Old material has partial metallic wood. Preserve new dielectric RM maps,
    # match its diffuse share instead of introducing metallic wood to new models.
    target = srgb(np.median(base[crop] / 255 * (1 - ref_rm[crop, 2:3] / 255), axis=0))
    report = {'reference_diffuse_srgb': target.tolist(), 'files': {}}
    prepared = []
    for stem, rm_name in [('MOSIN_7_Base.dds', 'MOSIN_8_RM.dds'), ('MOSIN_11_Base.dds', 'MOSIN_12_RM.dds')]:
        for prefix in ['', 'Fallbacks/']:
            name = prefix + stem
            installed = (textures / name).read_bytes()
            backup = args.output / 'before' / name
            original = backup.read_bytes() if backup.exists() else installed
            assert sha(original) == HASHES[name], f'Unexpected baseline: {name}'
            rough = (textures / (prefix + rm_name)).read_bytes()
            if not prefix:
                expected_rm = {'MOSIN_8_RM.dds': 'fe0a764627529eb49bd2382ae48e91acbe5edf447768b6451eff22730e2bdb85',
                               'MOSIN_12_RM.dds': 'a88b4c12da5e2382d2b0e93e8e5b31491b6a36c584b94991422b09ea8cb26acb'}
                assert sha(rough) == expected_rm[rm_name], 'Material mask changed'
                image = decode(original)
                material_mask = wood(image, decode(rough))
                median = np.median(image[material_mask], axis=0)
                mask_image = Image.fromarray(material_mask.astype('uint8') * 255)
            result, metrics = correct(original, mask_image, median, target)
            assert installed in (original, result), f'Concurrent texture edit: {name}'
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_bytes(original)
            out = args.output / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(result)
            Image.fromarray(decode(result).astype('uint8')).save(out.with_suffix('.png'))
            metrics.update(before=sha(original), after=sha(result), source_median=median.tolist())
            report['files'][name] = metrics
            prepared.append((textures / name, installed, result))
    if args.apply:
        for path, installed, _ in prepared:
            assert path.read_bytes() == installed, f'Concurrent edit: {path}'
        for path, _, result in prepared:
            path.write_bytes(result)
    (args.output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
    print('Installed.' if args.apply else 'Preview only; inspect before --apply.')


if __name__ == '__main__':
    main()
