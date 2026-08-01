"""Batch finalize fix-pass icons: FAMAS/SIG/G36/SVT/AUG/AR10 + M72 WeaponIcon."""
from __future__ import annotations

import importlib.util
import shutil
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
ASSETS = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\assets"
)
RAW_DIR = ROOT / "Icons" / "Upgrades" / "_review" / "icon_style_B" / "_raw"
PREV_DIR = ROOT / "Icons" / "Upgrades" / "_review" / "icon_style_B"
WC = ROOT / "WeaponComponents"
WI = ROOT / "WeaponIcons"

spec = importlib.util.spec_from_file_location(
    "fin", ROOT / "docs" / "tools" / "_finalize_icon_style_b.py"
)
fin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fin)

punch_spec = importlib.util.spec_from_file_location(
    "punch", ROOT / "docs" / "tools" / "_punch_enclosed_dark_holes.py"
)
punch = importlib.util.module_from_spec(punch_spec)
punch_spec.loader.exec_module(punch)


def paint_enclosed_dark_to_magenta(im: Image.Image, luma_max: int = 70) -> Image.Image:
    """Turn closed dark fills (skeleton holes painted shut) into chroma."""
    im = im.convert("RGBA")
    w, h = im.size
    pix = list(im.getdata())
    dark = [False] * (w * h)
    for i, (r, g, b, a) in enumerate(pix):
        # skip already-magenta
        if fin.dist_mag(r, g, b) <= fin.BG_SEED:
            continue
        if a >= 8 and (r + g + b) <= luma_max:
            dark[i] = True
    visited = [False] * (w * h)
    hole = [False] * (w * h)
    nbr = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for i0 in range(w * h):
        if not dark[i0] or visited[i0]:
            continue
        q: deque[int] = deque([i0])
        visited[i0] = True
        comp: list[int] = []
        touch = False
        while q:
            i = q.popleft()
            comp.append(i)
            x, y = i % w, i // w
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                touch = True
            for dx, dy in nbr:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                ni = ny * w + nx
                if visited[ni] or not dark[ni]:
                    continue
                visited[ni] = True
                q.append(ni)
        if (not touch) and len(comp) >= 80:
            for i in comp:
                hole[i] = True
    out = []
    for i, (r, g, b, a) in enumerate(pix):
        if hole[i]:
            out.append((255, 0, 255, 255))
        else:
            out.append((r, g, b, a))
    res = Image.new("RGBA", (w, h))
    res.putdata(out)
    print(f"  painted magenta holes: {sum(1 for h0 in hole if h0)}")
    return res


def process_component(raw_name: str, dest: Path, *, pre_punch: bool = False, rotate: float = 0.0) -> None:
    src = ASSETS / raw_name
    raw = Image.open(src).convert("RGBA")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if pre_punch:
        raw = paint_enclosed_dark_to_magenta(raw)
    raw_path = RAW_DIR / raw_name
    raw.save(raw_path)
    keyed = fin.magenta_key(raw)
    keyed_path = RAW_DIR / raw_name.replace("raw_", "keyed_")
    keyed.save(keyed_path)
    final = fin.finalize_icon(keyed, size=100, fill=0.78)
    if abs(rotate) > 0.1:
        final = final.rotate(rotate, expand=True, resample=Image.Resampling.BICUBIC)
        # re-fit to 100
        bbox = final.getbbox()
        if bbox:
            cropped = final.crop(bbox)
            final = fin.fit_with_margin(cropped, size=100, fill=0.78)
            final = fin.anaconda_soft_silhouette(
                final, body_soft=0.35, edge_blur=0.85, fringe_black_below=170
            )
    final = punch.punch(final, luma_max=55)
    preview = PREV_DIR / raw_name.replace("raw_", "preview_").replace("_v2", "")
    if "MagLarge" in raw_name:
        preview = PREV_DIR / "preview_SVT_MagLarge.png"
    final.save(preview)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(preview, dest)
    opaque = sum(1 for p in final.getdata() if p[3] > 200)
    print(f"{dest.name}: opaque={opaque} -> {dest}")


def process_m72(*, flip: bool = False) -> None:
    src = ASSETS / "raw_M72LAW_WeaponIcon.png"
    im = Image.open(src).convert("RGBA")
    # WeaponIcons face right (muzzle right). Only flip when source faces left.
    if flip:
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    # soft-key near-black bg already black; ensure alpha
    w, h = im.size
    pix = list(im.getdata())
    out = []
    for r, g, b, a in pix:
        if r + g + b < 12:
            out.append((0, 0, 0, 0))
        else:
            out.append((r, g, b, 255))
    keyed = Image.new("RGBA", (w, h))
    keyed.putdata(out)
    # fit into 324x165 like other WeaponIcons
    target_w, target_h = 324, 165
    bbox = keyed.getbbox()
    if not bbox:
        raise RuntimeError("M72 empty")
    crop = keyed.crop(bbox)
    # letterbox with margin
    margin = 0.92
    cw, ch = crop.size
    scale = min((target_w * margin) / cw, (target_h * margin) / ch)
    nw, nh = max(1, int(cw * scale)), max(1, int(ch * scale))
    resized = crop.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))
    canvas.paste(resized, ((target_w - nw) // 2, (target_h - nh) // 2), resized)
    # soft AA fringe like other icons (simple)
    alpha = canvas.getchannel("A").filter(ImageFilter.GaussianBlur(0.6))
    canvas = Image.merge("RGBA", (*canvas.convert("RGB").split(), alpha))
    dest = WI / "M72LAW.png"
    canvas.save(dest)
    PREV_DIR.mkdir(parents=True, exist_ok=True)
    canvas.save(PREV_DIR / "preview_M72LAW_WeaponIcon.png")
    print(f"M72LAW WeaponIcon {dest} size={canvas.size}")


def main() -> None:
    process_component(
        "raw_FAMAS_Mag25_v2.png",
        WC / "Magazine" / "FAMAS_Mag25.png",
    )
    # UnFolded: items.lua wires *_v2.png only (do not recreate orphan UnFolded.png).
    process_component(
        "raw_Sig_Stock_UnFolded_v2.png",
        WC / "Stock" / "Sig_Stock_UnFolded_v2.png",
        pre_punch=True,
    )
    # G36: raw already has magenta cutouts — do NOT pre_punch (eats frame).
    process_component(
        "raw_G36_Stock_Normal_v2.png",
        WC / "Stock" / "G36_Stock_Normal.png",
        pre_punch=False,
    )
    process_component(
        "raw_SVT_Mag10_v3.png",
        WC / "Magazine" / "SVT_Mag10.png",
    )
    process_component(
        "raw_SVT_MagLarge_v2.png",
        WC / "Magazine" / "SVT_MagLarge.png",
    )
    process_component(
        "raw_AUG_Mag42_v3.png",
        WC / "Magazine" / "AUG_Mag42.png",
        rotate=-32.0,  # more diagonal lean like AK45
    )
    ar10 = ASSETS / "raw_AR10_Mag20_v2.png"
    if ar10.exists():
        process_component(
            "raw_AR10_Mag20_v2.png",
            WC / "Magazine" / "AR10_Mag20.png",
        )
    else:
        print("skip AR10 (no raw)")
    process_m72(flip=False)


if __name__ == "__main__":
    main()
