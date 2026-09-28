"""Mosin visual repair: preserve BC1 layout/mips; recolor reddish wood endpoints.

Default writes a preview DDS pair into --output; --apply installs it and grip X=8.
Source hashes pin the original textures, preventing accidental double correction.
Requires numpy and Pillow (preview only). Does not regenerate any ModItem.
"""
import argparse
import hashlib
import io
from pathlib import Path
import struct

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    "MOSIN_7_Base.dds": "324e25e9d974bfd2f98f831284f3fd4c3dfeb2a71237602c3dd1de3c8421b5b9",
    "Fallbacks/MOSIN_7_Base.dds": "33c5d5d976ca9be0c4d255d6805c2748065ec72579a654e8d073b551780ace3a",
}


def recolor(data):
    assert data[:4] == b"DDS " and data[84:88] == b"DX10"
    assert struct.unpack_from("<I", data, 128)[0] == 72, "Expected BC1 sRGB"
    height, width = struct.unpack_from("<II", data, 12)
    mips = struct.unpack_from("<I", data, 28)[0]
    expected = sum(max(1, (width >> n) + 3 >> 2) * max(1, (height >> n) + 3 >> 2) * 8 for n in range(mips))
    assert len(data) == 148 + expected
    words = np.frombuffer(data, dtype="<u2", offset=148).reshape(-1, 4).copy()
    colors = words[:, :2].copy()
    rgb = np.stack(((colors >> 11) * (255 / 31), ((colors >> 5) & 63) * (255 / 63), (colors & 31) * (255 / 31)), axis=-1)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # Neutral steel and yellow brass have no red excess and remain unchanged.
    red_excess = r / np.maximum(g, 1)
    warmth = g / np.maximum(b, 1)
    strength = np.clip((red_excess - 1.4) / .65, 0, 1) * np.clip((warmth - 1.05) / .35, 0, 1)
    corrected = rgb.copy()
    # Compress red excess monotonically, avoiding hue inversions in dark grain.
    corrected[..., 0] -= .78 * np.maximum(r - 1.4 * g, 0) * np.clip((warmth - 1.05) / .35, 0, 1)
    corrected[..., 2] += .13 * np.maximum(g - b, 0) * strength
    q = np.rint(np.clip(corrected, 0, 255) * np.array([31, 63, 31]) / 255).astype(np.uint16)
    encoded = (q[..., 0] << 11) | (q[..., 1] << 5) | q[..., 2]
    # Preserve BC1's opaque/transparent mode and its exact interpolation weights.
    opaque = colors[:, 0] > colors[:, 1]
    swap = (encoded[:, 0] < encoded[:, 1]) & opaque
    swap |= (encoded[:, 0] > encoded[:, 1]) & ~opaque
    encoded[swap] = encoded[swap, ::-1]
    indices = words[:, 2].astype(np.uint32) | (words[:, 3].astype(np.uint32) << 16)
    indices[swap & opaque] ^= np.uint32(0x55555555)
    transparent_swap = swap & ~opaque
    for shift in range(0, 32, 2):
        flip = transparent_swap & (((indices >> shift) & 3) < 2)
        indices[flip] ^= np.uint32(1 << shift)
    collapsed = opaque & (encoded[:, 0] == encoded[:, 1])
    # Constant blocks keep their corrected color without introducing transparency.
    nonblack = collapsed & (encoded[:, 0] > 0)
    encoded[nonblack, 1] -= 1
    indices[nonblack] = 0
    black = collapsed & ~nonblack
    encoded[black, 0] = 1
    indices[black] = np.uint32(0x55555555)
    words[:, :2] = encoded
    words[:, 2] = indices & 65535
    words[:, 3] = indices >> 16
    result = data[:148] + words.tobytes()
    assert len(result) == len(data) and result[:148] == data[:148]
    neutral = np.all(strength == 0, axis=1)
    assert np.array_equal(words[neutral], np.frombuffer(data, dtype="<u2", offset=148).reshape(-1, 4)[neutral])
    print(f"{width}x{height}, {mips} mips: {np.count_nonzero(np.any(encoded != colors, axis=1))} recolored blocks; {neutral.sum()} neutral blocks byte-identical")
    return result


def preview(data, path):
    linear_header = bytearray(data)
    struct.pack_into("<I", linear_header, 128, 71)  # Pillow lacks the sRGB alias.
    Image.open(io.BytesIO(linear_header)).save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets", type=Path, default=ROOT.parent / "jazz_assets")
    parser.add_argument("--output", type=Path, default=ROOT / "tmp/mosin-visual/corrected")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    prepared = []
    for name, expected in SOURCES.items():
        target = args.assets / "Entities/Textures" / name
        original = target.read_bytes()
        assert hashlib.sha256(original).hexdigest() == expected, f"Source changed/already corrected: {target}"
        corrected = recolor(original)
        out = args.output / name
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(corrected)
        preview(corrected, out.with_suffix(".png"))
        backup = args.output / "before" / name
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_bytes(original)
        prepared.append((target, corrected))
    if args.apply:
        entity = args.assets / "Entities/MOSIN_Obrez.ent"
        original = entity.read_bytes()
        old = b'name="Hand_l_grip" spot_pos="5.000,0.000,1.500"'
        new = b'name="Hand_l_grip" spot_pos="8.000,0.000,1.500"'
        assert original.count(old) == 1 or original.count(new) == 1
        for target, corrected in prepared:
            target.write_bytes(corrected)
        entity.write_bytes(original.replace(old, new))
        print("Installed texture pair and Obrez grip X=8; registrations unchanged.")


if __name__ == "__main__":
    main()
