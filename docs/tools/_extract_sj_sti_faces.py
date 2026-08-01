# -*- coding: utf-8 -*-
"""Extract JA2 STCI (.sti) face frames from Shady Job to PNG face refs.

Usage (jazz/):
  python docs/tools/_extract_sj_sti_faces.py
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

SJ_FACES = Path(r"C:\Users\SsAnd\Downloads\SJ\data\faces")
OUT = Path(
    r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz"
    r"\docs\design\mercs-ja12\_face-source\sj"
)

# STCI flags (JA2)
STCI_ETRLE_COMPRESSED = 0x0020
STCI_INDEXED = 0x0008


def decode_etrle(data: bytes, width: int, height: int) -> list[int]:
    """JA2 ETRLE: per-scanline; byte 0 = EOL (do not also wrap mid-run)."""
    out = [0] * (width * height)
    i = 0
    for y in range(height):
        x = 0
        while i < len(data):
            b = data[i]
            i += 1
            if b == 0:
                break  # end of scanline
            if b & 0x80:
                x += b & 0x7F
            else:
                run = b
                for _ in range(run):
                    if i >= len(data):
                        break
                    if 0 <= x < width:
                        out[y * width + x] = data[i]
                    i += 1
                    x += 1
    return out


def read_sti(path: Path) -> list[Image.Image]:
    """Indexed STCI: header(64) → palette → subimage headers → pixel data."""
    raw = path.read_bytes()
    if raw[:4] != b"STCI":
        raise ValueError(f"not STCI: {path}")

    _orig, _stored, _trans, flags = struct.unpack_from("<IIII", raw, 4)
    us_height, us_width = struct.unpack_from("<HH", raw, 20)
    ui_number_of_colours, us_number_of_sub_images = struct.unpack_from("<IH", raw, 24)
    print(
        f"{path.name}: hdr={us_width}x{us_height} flags=0x{flags:x} "
        f"colors={ui_number_of_colours} subs={us_number_of_sub_images}"
    )

    pos = 64
    ncolors = ui_number_of_colours or 256
    pal: list[tuple[int, int, int]] = []
    for _i in range(ncolors):
        r, g, b = raw[pos], raw[pos + 1], raw[pos + 2]
        pal.append((r, g, b))
        pos += 3

    subs: list[tuple[int, int, int, int, int, int]] = []
    for _n in range(us_number_of_sub_images):
        off_i, length, ox, oy, sh, sw = struct.unpack_from("<IIhhHH", raw, pos)
        subs.append((off_i, length, ox, oy, sh, sw))
        pos += 16
        print(f"  sub: {sw}x{sh} off={off_i} len={length}")

    data_base = pos
    frames: list[Image.Image] = []
    for off_i, length, _ox, _oy, sh, sw in subs:
        chunk = raw[data_base + off_i : data_base + off_i + length]
        if flags & STCI_ETRLE_COMPRESSED:
            pixels = decode_etrle(chunk, sw, sh)
        else:
            pixels = list(chunk[: sw * sh])
            if len(pixels) < sw * sh:
                pixels.extend([0] * (sw * sh - len(pixels)))
        img = Image.new("RGBA", (sw, sh))
        px = img.load()
        for y in range(sh):
            for x in range(sw):
                idx = pixels[y * sw + x]
                if idx == 0:
                    px[x, y] = (0, 0, 0, 0)
                else:
                    r, g, b = pal[idx]
                    px[x, y] = (r, g, b, 255)
        frames.append(img)
    return frames


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    design = Path(
        r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz"
        r"\docs\design\mercs-ja12"
    )
    jobs = [
        # bigfaces/NN.sti = best identity ref (106×122); bNN = laptop 90×100
        ("bigfaces/66.sti", "simon", True),
        ("bigfaces/67.sti", "benny", True),
        ("b66.sti", "simon-laptop", False),
        ("b67.sti", "benny-laptop", False),
        ("66.sti", "simon-small", False),
        ("67.sti", "benny-small", False),
    ]
    for rel, stem, is_canon in jobs:
        src = SJ_FACES / rel
        if not src.exists():
            print("MISSING", src)
            continue
        frames = read_sti(src)
        for i, im in enumerate(frames):
            out = OUT / f"{stem}_f{i}.png"
            im.save(out)
            print("wrote", out, im.size)
        if frames and is_canon:
            best = max(frames[:1], key=lambda im: im.size[0] * im.size[1])
            canon_png = design / f"{stem}.ja2-face.png"
            best.save(canon_png)
            print("canon", canon_png, best.size)
            # Also keep under _face-source/sj for SJ batch pattern
            (OUT / f"{stem}.face.png").write_bytes(canon_png.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
