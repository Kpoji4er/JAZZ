"""Finalize style-B attachment Icon previews / production Icons.

Preferred cut: rembg (neural), like portrait BiRefNet path.
Fallback: magenta #FF00FF flood soft-key (dark metal cannot use #504633 — too close).

Then: fit ~78% of canvas + thin black silhouette outline.

Output default: 100x100 RGBA under Icons/Upgrades/_review/icon_style_B/
Canon rules: WeaponComponents/references/PROMPT.md
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

try:
    from rembg import remove as rembg_remove
except ImportError:
    rembg_remove = None

BG_SEED = 80.0
BG_WALK = 110.0
SIZE = 100
OUTLINE_WIDTH = 2
OUTLINE_COLOR = (0, 0, 0, 255)
# Anaconda-like soft silhouette (see WeaponComponents/references/style_B_edge_ref_Anaconda.png)
BODY_SOFT = 0.45          # mild overall soften (less harsh)
EDGE_AA_BLUR = 1.15       # alpha ramp width ~ like Anaconda 25→255 over ~4px
FRINGE_BLACK_BELOW = 200  # alpha < this → RGB forced black (soft AA fringe)

SRC = Path(
    r"C:\Users\SsAnd\.cursor\projects\c-Users-SsAnd-AppData-Roaming-Jagged-Alliance-3-Mods-jazz\assets"
)
OUT = Path(
    r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz\Icons\Upgrades\_review\icon_style_B"
)
RAW_OUT = OUT / "_raw"

# Default batch; pass raw_*.png names as argv to process a subset.
NAMES = [
    "raw_JAZZ_Reflex_Eotech.png",
    "raw_JAZZ_MagNormal.png",
    "raw_JAZZ_MagLarge_30_45.png",
    "raw_JAZZ_Reflex_PKAS.png",
]


def dist_mag(r: int, g: int, b: int) -> float:
    return ((r - 255) ** 2 + (g - 0) ** 2 + (b - 255) ** 2) ** 0.5


def magenta_key(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    pix = list(im.getdata())
    bg = [False] * (w * h)
    q: deque[int] = deque()

    def rgb(i: int):
        return pix[i][0], pix[i][1], pix[i][2]

    def seed(x: int, y: int) -> None:
        if not (0 <= x < w and 0 <= y < h):
            return
        i = y * w + x
        if bg[i]:
            return
        if dist_mag(*rgb(i)) <= BG_SEED:
            bg[i] = True
            q.append(i)

    for x in range(w):
        seed(x, 0)
        seed(x, h - 1)
    for y in range(h):
        seed(0, y)
        seed(w - 1, y)

    nbr = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))
    while q:
        i = q.popleft()
        x, y = i % w, i // w
        for dx, dy in nbr:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            ni = ny * w + nx
            if bg[ni]:
                continue
            if dist_mag(*rgb(ni)) <= BG_WALK:
                bg[ni] = True
                q.append(ni)

    out_px = []
    for i, (r, g, b, _a) in enumerate(pix):
        if bg[i]:
            out_px.append((0, 0, 0, 0))
            continue
        excess = min(r, b) - g
        if excess > 8:
            pull = min(1.0, excess / 80.0) * 0.55
            r = int(r * (1 - pull) + g * pull)
            b = int(b * (1 - pull) + g * pull)
        out_px.append((r, g, b, 255))
    out = Image.new("RGBA", (w, h))
    out.putdata(out_px)
    alpha = out.getchannel("A").filter(ImageFilter.GaussianBlur(0.6))
    return Image.merge("RGBA", (*out.convert("RGB").split(), alpha))


def looks_like_magenta_plate(im: Image.Image, sample: int = 12) -> bool:
    """True if image corners are solid magenta chroma (prefer flood-key over rembg)."""
    im = im.convert("RGBA")
    w, h = im.size
    pts = [
        (2, 2),
        (w - 3, 2),
        (2, h - 3),
        (w - 3, h - 3),
        (w // 2, 2),
        (2, h // 2),
    ]
    ok = 0
    for x, y in pts:
        r, g, b, _a = im.getpixel((x, y))
        if dist_mag(r, g, b) <= 55:
            ok += 1
    return ok >= 4


def cut(im: Image.Image) -> Image.Image:
    # Dark metal + rembg often chews thin edges; magenta plates key cleaner.
    if looks_like_magenta_plate(im):
        return magenta_key(im)
    if rembg_remove is not None:
        cut_im = rembg_remove(im.convert("RGBA"))
        if not isinstance(cut_im, Image.Image):
            cut_im = Image.open(cut_im).convert("RGBA")
        else:
            cut_im = cut_im.convert("RGBA")
        px = list(cut_im.getdata())
        cleaned = []
        for r, g, b, a in px:
            if a < 8:
                cleaned.append((0, 0, 0, 0))
                continue
            if dist_mag(r, g, b) < 70 and min(r, b) > g + 30:
                cleaned.append((0, 0, 0, 0))
                continue
            excess = min(r, b) - g
            if excess > 10 and a < 250:
                pull = min(1.0, excess / 90.0) * 0.5
                r = int(r * (1 - pull) + g * pull)
                b = int(b * (1 - pull) + g * pull)
            cleaned.append((r, g, b, a))
        out = Image.new("RGBA", cut_im.size)
        out.putdata(cleaned)
        return out
    return magenta_key(im)


def fit_with_margin(im: Image.Image, size: int = SIZE, fill: float = 0.78) -> Image.Image:
    a = im.getchannel("A")
    mask = a.point(lambda v: 255 if v > 24 else 0)
    bbox = mask.getbbox()
    if not bbox:
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cropped = im.crop(bbox)
    target = max(8, int(round(size * fill)))
    scale = min(target / cropped.width, target / cropped.height)
    nw = max(1, int(round(cropped.width * scale)))
    nh = max(1, int(round(cropped.height * scale)))
    resized = cropped.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.paste(resized, ((size - nw) // 2, (size - nh) // 2), resized)
    return canvas


def harden_alpha(im: Image.Image, thresh: int = 16) -> Image.Image:
    """Binary alpha so soft rembg fringe cannot leave a halo gap."""
    im = im.convert("RGBA")
    px = list(im.getdata())
    out = []
    for r, g, b, a in px:
        if a < thresh:
            out.append((0, 0, 0, 0))
        else:
            out.append((r, g, b, 255))
    res = Image.new("RGBA", im.size)
    res.putdata(out)
    return res


def remove_light_fringe(im: Image.Image, lum_max: int = 85) -> Image.Image:
    """Drop bright rembg AA fringe before soft silhouette."""
    im = im.convert("RGBA")
    w, h = im.size
    px = list(im.getdata())
    a = [p[3] for p in px]

    def lum(i: int) -> int:
        r, g, b, _ = px[i]
        return (r + g + b) // 3

    def is_edge(i: int) -> bool:
        if a[i] < 8:
            return False
        x, y = i % w, i // w
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    return True
                if a[ny * w + nx] < 8:
                    return True
        return False

    out = []
    for i, (r, g, b, alpha) in enumerate(px):
        if alpha < 8:
            out.append((0, 0, 0, 0))
            continue
        if is_edge(i) and lum(i) >= lum_max:
            out.append((0, 0, 0, 0))
            continue
        out.append((r, g, b, 255 if alpha >= 8 else 0))
    res = Image.new("RGBA", (w, h))
    res.putdata(out)
    return res


def anaconda_soft_silhouette(
    im: Image.Image,
    body_soft: float = BODY_SOFT,
    edge_blur: float = EDGE_AA_BLUR,
    fringe_black_below: int = FRINGE_BLACK_BELOW,
) -> Image.Image:
    """Match JA3 Anaconda icon edge: soft alpha ramp, black fringe, slightly soft body.

    Ref edge profile (Anaconda): alpha 25→64→128→207→255 with RGB black in the
    outer fringe, then opaque metal — no hard pixel outline, no staircase ring.
    """
    im = im.convert("RGBA")
    # Mild body soften (filmic, less razor-sharp)
    if body_soft > 0:
        blurred = im.filter(ImageFilter.GaussianBlur(radius=body_soft))
        body = Image.blend(im, blurred, 0.55)
    else:
        body = im

    # Clean hard sil from alpha, then soft AA ramp
    sil = im.getchannel("A").point(lambda v: 255 if v > 28 else 0)
    # tiny dilate so soft ramp has room outside the opaque core
    dil = sil.filter(ImageFilter.MaxFilter(3))
    soft_a = dil.filter(ImageFilter.GaussianBlur(radius=edge_blur))

    bp = list(body.getdata())
    ap = list(soft_a.getdata())
    out_px = []
    for (r, g, b, _oa), a in zip(bp, ap):
        if a < 10:
            out_px.append((0, 0, 0, 0))
            continue
        if a < fringe_black_below:
            # Anaconda outer fringe: pure black + partial alpha
            out_px.append((0, 0, 0, a))
        else:
            out_px.append((r, g, b, 255 if a >= 250 else a))
    out = Image.new("RGBA", im.size)
    out.putdata(out_px)
    return out


def heal_silhouette(im: Image.Image, close_iters: int = 4, edge_blur: float = 2.4) -> Image.Image:
    """Heal rembg 'chewed' edges (esp. thin spines) at hi-res before downscale.

    Morphological close fills small bites; light alpha blur softens remaining jaggies.
    RGB unchanged under new alpha.
    """
    im = im.convert("RGBA")
    rgb = im.convert("RGB")
    a = im.getchannel("A")
    sil = a.point(lambda v: 255 if v > 20 else 0)
    closed = sil
    for _ in range(max(1, close_iters)):
        closed = closed.filter(ImageFilter.MaxFilter(3))
    for _ in range(max(1, close_iters)):
        closed = closed.filter(ImageFilter.MinFilter(3))
    # Soften mask edge, keep core solid
    soft = closed.filter(ImageFilter.GaussianBlur(radius=edge_blur))
    # Premultiply-friendly: RGB black where we're only in soft fringe outside hard sil
    hard = closed
    rp, gp, bp = rgb.split()
    ap = list(soft.getdata())
    hp = list(hard.getdata())
    r0 = list(rp.getdata())
    g0 = list(gp.getdata())
    b0 = list(bp.getdata())
    out = []
    for r, g, b, sa, ha in zip(r0, g0, b0, ap, hp):
        if sa < 8:
            out.append((0, 0, 0, 0))
        elif ha > 200:
            out.append((r, g, b, 255))
        else:
            # soft fringe outside healed core → black AA like Anaconda
            out.append((0, 0, 0, sa))
    res = Image.new("RGBA", im.size)
    res.putdata(out)
    return res


def scrub_magenta(im: Image.Image) -> Image.Image:
    """Remove leftover magenta spill on keyed edges."""
    im = im.convert("RGBA")
    px = list(im.getdata())
    out = []
    for r, g, b, a in px:
        if a < 8:
            out.append((0, 0, 0, 0))
            continue
        if dist_mag(r, g, b) < 90 and min(r, b) > g + 25:
            out.append((0, 0, 0, 0))
            continue
        excess = min(r, b) - g
        if excess > 12:
            pull = min(1.0, excess / 90.0) * 0.6
            r = int(r * (1 - pull) + g * pull)
            b = int(b * (1 - pull) + g * pull)
        out.append((r, g, b, a))
    res = Image.new("RGBA", im.size)
    res.putdata(out)
    return res


def finalize_icon(keyed: Image.Image, size: int = SIZE, fill: float = 0.78) -> Image.Image:
    # Heal chewed rembg edges at source res, then downscale (LANCZOS keeps soft edge)
    hi = scrub_magenta(keyed.convert("RGBA"))
    hi = heal_silhouette(hi, close_iters=4, edge_blur=2.4)
    fitted = fit_with_margin(hi, size=size, fill=fill)
    # Gentle final AA only — no light-fringe eat that chews spines/highlights
    return anaconda_soft_silhouette(
        fitted,
        body_soft=0.35,
        edge_blur=0.85,
        fringe_black_below=170,
    )


def main() -> None:
    import sys

    names = [Path(a).name for a in sys.argv[1:]] or list(NAMES)
    OUT.mkdir(parents=True, exist_ok=True)
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    print("cutter:", "rembg" if rembg_remove else "magenta-flood")
    print("edge: Anaconda soft silhouette AA")
    for name in names:
        keyed_name = name.replace("raw_", "keyed_")
        keyed_path = RAW_OUT / keyed_name
        src = SRC / name
        if keyed_path.exists():
            keyed = Image.open(keyed_path).convert("RGBA")
            print(f"reuse keyed {keyed_name}")
        elif src.exists():
            raw = Image.open(src).convert("RGBA")
            raw.save(RAW_OUT / name)
            keyed = cut(raw)
            keyed.save(keyed_path)
        else:
            print("missing", name)
            continue
        final = finalize_icon(keyed, SIZE, fill=0.78)
        out_name = name.replace("raw_", "preview_")
        final.save(OUT / out_name)
        opaque = sum(1 for p in final.getdata() if p[3] > 200)
        print(f"{out_name}: opaque={opaque}")


if __name__ == "__main__":
    main()
