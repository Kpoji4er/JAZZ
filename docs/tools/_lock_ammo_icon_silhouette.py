# -*- coding: utf-8 -*-
"""Lock ammo icons to a per-caliber RGBA silhouette (+ structure / plate-first).

Rule: one canonical silhouette PER CALIBER.
Pass that caliber's base icon as --silhouette (e.g. 9x18.png, 919FMJ.png).

Modes:
  --structure 0.7   keep plate lightness (form), chroma from draft
  --plate-first     plate mesh 100%; tint/band/text from draft (strongest)
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def alpha_bbox(a: np.ndarray, athr: int = 8) -> tuple[int, int, int, int]:
    mask = a > athr
    ys, xs = np.where(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def content_rgba_from_rgb(im: Image.Image, thr: int = 28) -> Image.Image:
    rgba = im.convert("RGBA")
    arr = np.array(rgba)
    lum = arr[:, :, :3].astype(np.int16).sum(axis=2)
    arr[:, :, 3] = np.where(lum > thr, 255, 0).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def dist_magenta(rgb: np.ndarray) -> np.ndarray:
    """Euclidean distance to #FF00FF per pixel."""
    r = rgb[:, :, 0].astype(np.float32)
    g = rgb[:, :, 1].astype(np.float32)
    b = rgb[:, :, 2].astype(np.float32)
    return np.sqrt((r - 255.0) ** 2 + g**2 + (b - 255.0) ** 2)


def looks_like_magenta_bg(im: Image.Image, sample: int = 12) -> bool:
    arr = np.array(im.convert("RGBA"))
    h, w = arr.shape[:2]
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
        d = float(np.sqrt(
            (float(arr[y, x, 0]) - 255) ** 2
            + float(arr[y, x, 1]) ** 2
            + (float(arr[y, x, 2]) - 255) ** 2
        ))
        if d <= 55:
            ok += 1
    return ok >= 4


def content_rgba_from_magenta(
    im: Image.Image,
    *,
    seed: float = 42.0,
    walk: float = 64.0,
) -> Image.Image:
    """Chroma-key solid magenta plate (#FF00FF) → RGBA subject.

    Better than black-BG luminance key: carton shadows no longer merge with void.
    Returns feathered alpha near the key boundary (vanilla-like soft edge).
    """
    rgba = im.convert("RGBA")
    arr = np.array(rgba)
    rgb = arr[:, :, :3].copy()
    d = dist_magenta(rgb)
    # Core BG: near-magenta. Grow slightly into fringe.
    bg = d <= seed
    m = bg.copy()
    for _ in range(4):
        pad = np.pad(m, 1, constant_values=False)
        neigh = (
            pad[0:-2, 0:-2]
            | pad[0:-2, 1:-1]
            | pad[0:-2, 2:]
            | pad[1:-1, 0:-2]
            | pad[1:-1, 1:-1]
            | pad[1:-1, 2:]
            | pad[2:, 0:-2]
            | pad[2:, 1:-1]
            | pad[2:, 2:]
        )
        m = m | (neigh & (d <= walk))
    # Subject = not BG. Feather by distance-to-magenta.
    subject = ~m
    alpha = np.zeros(d.shape, dtype=np.float32)
    alpha[subject] = 255.0
    # Pixels near magenta get partial alpha even if classified subject
    near = subject & (d < walk + 40)
    if near.any():
        # closer to magenta → more transparent
        t = np.clip((d[near] - seed) / max(1.0, (walk + 40) - seed), 0.0, 1.0)
        alpha[near] = 255.0 * t
    # Despill magenta on remaining subject
    excess = np.minimum(rgb[:, :, 0], rgb[:, :, 2]).astype(np.int16) - rgb[:, :, 1].astype(
        np.int16
    )
    pull = np.clip(excess.astype(np.float32) / 70.0, 0, 1) * 0.65
    pull = np.where(subject, pull, 0.0)
    for c in (0, 2):
        ch = rgb[:, :, c].astype(np.float32)
        rgb[:, :, c] = np.clip(
            ch * (1.0 - pull) + rgb[:, :, 1].astype(np.float32) * pull, 0, 255
        ).astype(np.uint8)
    # Darken outermost subject ring (kills beige fringe on black UI)
    solid = alpha >= 200
    rim = solid & ~erode_mask(solid, 1)
    if rim.any():
        rgb_f = rgb.astype(np.float32)
        rgb_f[rim] *= 0.82
        rgb = np.clip(rgb_f, 0, 255).astype(np.uint8)
    a8 = np.clip(alpha, 0, 255).astype(np.uint8)
    out = np.dstack([rgb, a8])
    out[a8 <= 8] = 0
    return Image.fromarray(out, "RGBA")


def prepare_draft_rgba(im: Image.Image, *, key: str = "auto", thr: int = 28) -> Image.Image:
    """Pick cut method: magenta chroma, black luminance, or existing alpha."""
    rgba = im.convert("RGBA")
    arr = np.array(rgba)
    has_alpha = float(arr[:, :, 3].mean()) > 5 and float(arr[:, :, 3].min()) < 250
    mode = key
    if mode == "auto":
        if looks_like_magenta_bg(rgba):
            mode = "magenta"
        elif has_alpha:
            mode = "alpha"
        else:
            mode = "black"
    if mode == "magenta":
        return content_rgba_from_magenta(rgba)
    if mode == "alpha":
        return rgba
    return content_rgba_from_rgb(rgba, thr=thr)


def choke_alpha(rgba: Image.Image, px: int) -> Image.Image:
    """Erode solid content to drop AI light-fringe; keep soft AA fringe if present."""
    if px <= 0:
        return rgba
    arr = np.array(rgba.convert("RGBA"))
    a = arr[:, :, 3]
    soft = (a > 8) & (a < 200)
    solid = a >= 200
    if not solid.any():
        solid = a > 8
        soft = np.zeros_like(solid)
    m = solid.copy()
    for _ in range(px):
        pad = np.pad(m, 1, constant_values=False)
        m = (
            pad[0:-2, 0:-2]
            & pad[0:-2, 1:-1]
            & pad[0:-2, 2:]
            & pad[1:-1, 0:-2]
            & pad[1:-1, 1:-1]
            & pad[1:-1, 2:]
            & pad[2:, 0:-2]
            & pad[2:, 1:-1]
            & pad[2:, 2:]
        )
    # Keep original soft fringe pixels that still touch the choked solid.
    keep_soft = soft.copy()
    if keep_soft.any() and m.any():
        pad = np.pad(m, 1, constant_values=False)
        touch = (
            pad[0:-2, 0:-2]
            | pad[0:-2, 1:-1]
            | pad[0:-2, 2:]
            | pad[1:-1, 0:-2]
            | pad[1:-1, 1:-1]
            | pad[1:-1, 2:]
            | pad[2:, 0:-2]
            | pad[2:, 1:-1]
            | pad[2:, 2:]
        )
        keep_soft = soft & touch
    new_a = np.zeros_like(a)
    new_a[m] = 255
    new_a[keep_soft] = a[keep_soft]
    arr[:, :, 3] = new_a
    arr[new_a <= 8, :3] = 0
    return Image.fromarray(arr, "RGBA")


def erode_mask(mask: np.ndarray, px: int) -> np.ndarray:
    m = mask.astype(bool)
    for _ in range(max(0, px)):
        pad = np.pad(m, 1, constant_values=False)
        m = (
            pad[0:-2, 0:-2]
            & pad[0:-2, 1:-1]
            & pad[0:-2, 2:]
            & pad[1:-1, 0:-2]
            & pad[1:-1, 1:-1]
            & pad[1:-1, 2:]
            & pad[2:, 0:-2]
            & pad[2:, 1:-1]
            & pad[2:, 2:]
        )
    return m


def dilate_mask(mask: np.ndarray, px: int) -> np.ndarray:
    m = mask.astype(bool)
    for _ in range(max(0, px)):
        pad = np.pad(m, 1, constant_values=False)
        m = (
            pad[0:-2, 0:-2]
            | pad[0:-2, 1:-1]
            | pad[0:-2, 2:]
            | pad[1:-1, 0:-2]
            | pad[1:-1, 1:-1]
            | pad[1:-1, 2:]
            | pad[2:, 0:-2]
            | pad[2:, 1:-1]
            | pad[2:, 2:]
        )
    return m


def apply_soft_outline(
    rgba: np.ndarray,
    *,
    strength: float = 0.4,
    width: int = 1,
    color: tuple[int, int, int] = (22, 20, 18),
    outer: bool = False,
) -> np.ndarray:
    """Very soft dark outline on the carton edge (vanilla-like rim).

    Outer fringe is off by default: on black UI it is invisible / looks like dirt.
    """
    if strength <= 0:
        return rgba
    out = rgba.copy()
    a = out[:, :, 3]
    solid = a > 8
    if not solid.any():
        return out
    # Prefer solid body pixels (skip previous soft outer fringe).
    solid = a >= 200 if (a >= 200).any() else solid
    inner = solid & ~erode_mask(solid, max(1, width))
    s = float(np.clip(strength, 0.0, 1.0))
    c = np.array(color, dtype=np.float32)
    rgb = out[:, :, :3].astype(np.float32)
    # Soft darken of edge pixels — comparable to vanilla 9x18/919 rim.
    mix = 0.72 * s
    rgb[inner] = (1.0 - mix) * rgb[inner] + mix * c
    out[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)

    if outer:
        fringe = dilate_mask(solid, max(1, width)) & ~solid
        if fringe.any():
            oa = np.clip(int(round(55 * s)), 0, 100)
            out[fringe, 0] = color[0]
            out[fringe, 1] = color[1]
            out[fringe, 2] = color[2]
            out[fringe, 3] = np.maximum(out[fringe, 3], oa)
    return out


def fit_into(crop: Image.Image, bw: int, bh: int, *, mode: str) -> Image.Image:
    if mode == "cover":
        scale = max(bw / crop.width, bh / crop.height)
    else:
        scale = min(bw / crop.width, bh / crop.height)
    tw = max(1, int(round(crop.width * scale)))
    th = max(1, int(round(crop.height * scale)))
    crop = crop.resize((tw, th), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    ox = (bw - tw) // 2
    oy = (bh - th) // 2
    canvas.paste(crop, (ox, oy), crop)
    return canvas


def apply_structure_lightness(
    draft_rgb: np.ndarray, plate_rgb: np.ndarray, mask: np.ndarray, strength: float
) -> np.ndarray:
    d = draft_rgb.astype(np.float32)
    p = plate_rgb.astype(np.float32)
    d_lum = 0.299 * d[:, :, 0] + 0.587 * d[:, :, 1] + 0.114 * d[:, :, 2]
    p_lum = 0.299 * p[:, :, 0] + 0.587 * p[:, :, 1] + 0.114 * p[:, :, 2]
    scale = np.ones_like(d_lum)
    nz = d_lum > 8.0
    scale[nz] = p_lum[nz] / d_lum[nz]
    scale = np.clip(scale, 0.4, 2.2)
    remapped = np.clip(d * scale[:, :, None], 0, 255)
    draft_cov = draft_rgb.sum(axis=2) > 12
    only_plate = mask & ~draft_cov
    mixed = (1.0 - strength) * d + strength * remapped
    mixed = np.clip(mixed, 0, 255)
    result = draft_rgb.copy().astype(np.float32)
    result[mask] = mixed[mask]
    result[only_plate] = p[only_plate]
    return result.astype(np.uint8)


def plate_first_composite(
    draft_rgb: np.ndarray,
    plate_rgba: np.ndarray,
    *,
    body_mix: float = 0.82,
    band_sat_thr: float = 40.0,
) -> np.ndarray:
    """Plate mesh 100%; body tint + saturated band + ink from draft."""
    plate = plate_rgba[:, :, :3].astype(np.float32)
    a = plate_rgba[:, :, 3]
    mask = a > 8
    draft = draft_rgb.astype(np.float32)

    p_lum = 0.299 * plate[:, :, 0] + 0.587 * plate[:, :, 1] + 0.114 * plate[:, :, 2]
    d_lum = 0.299 * draft[:, :, 0] + 0.587 * draft[:, :, 1] + 0.114 * draft[:, :, 2]
    d_max = draft.max(axis=2)
    d_min = draft.min(axis=2)
    d_sat = np.zeros_like(d_max, dtype=np.float32)
    ok = d_max > 1.0
    d_sat[ok] = (d_max[ok] - d_min[ok]) / d_max[ok] * 255.0

    covered = mask & (draft.sum(axis=2) > 30)
    band = covered & (d_sat > band_sat_thr)
    body = covered & ~band

    out = plate.copy()
    if body.any():
        bc = np.median(draft[body], axis=0)
        bl = float(0.299 * bc[0] + 0.587 * bc[1] + 0.114 * bc[2]) + 1e-3
        shaded = np.clip(bc[None, None, :] * (p_lum[:, :, None] / bl), 0, 255)
        out[mask] = (1.0 - body_mix) * out[mask] + body_mix * shaded[mask]

    if band.any():
        bc = np.median(draft[band], axis=0)
        bl = float(0.299 * bc[0] + 0.587 * bc[1] + 0.114 * bc[2]) + 1e-3
        shaded = np.clip(bc[None, None, :] * (p_lum[:, :, None] / bl), 0, 255)
        out[band] = shaded[band]

    ink = mask & (d_lum < 58) & (d_sat < 95) & (draft.sum(axis=2) > 15)
    bright = mask & (d_lum > 205) & (d_sat < 55) & (draft.sum(axis=2) > 15)
    out[ink] = draft[ink]
    out[bright] = draft[bright]
    return np.clip(out, 0, 255).astype(np.uint8)


def lock_to_silhouette(
    src: Path,
    dst: Path,
    *,
    sil_path: Path,
    canvas: int = 110,
    thr: int = 28,
    fit: str = "contain",
    structure: float = 0.72,
    plate_first: bool = False,
    choke: int = 3,
    rim_plate: int = 2,
    hard_alpha: bool = False,
    alpha_from: str = "sil",
    soft_outline: float = 0.0,
    key: str = "auto",
) -> None:
    sil_im = Image.open(sil_path).convert("RGBA")
    if sil_im.size != (canvas, canvas):
        sil_im = sil_im.resize((canvas, canvas), Image.Resampling.LANCZOS)
    sil_arr = np.array(sil_im)
    sil_a = sil_arr[:, :, 3]
    bb = alpha_bbox(sil_a)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]

    src_im = Image.open(src)
    work = prepare_draft_rgba(src_im, key=key, thr=thr)

    cb = work.split()[-1].getbbox()
    if not cb:
        raise SystemExit(f"no content: {src}")
    # Fit first, then choke at DESTINATION resolution — choke before
    # downscale barely removes AI fringe on 1024 drafts.
    fitted = fit_into(work.crop(cb), bw, bh, mode=fit)
    fitted = choke_alpha(fitted, choke)

    layer = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    layer.paste(fitted, (bb[0], bb[1]), fitted)
    draft = np.array(layer)
    mask = sil_a > 8

    if plate_first:
        rgb = plate_first_composite(draft[:, :, :3], sil_arr)
        mode = "plate-first"
    elif structure > 0:
        rgb = apply_structure_lightness(
            draft[:, :, :3], sil_arr[:, :, :3], mask, strength=structure
        )
        mode = f"struct={structure:.2f}"
    else:
        rgb = draft[:, :, :3].copy()
        empty = mask & (draft[:, :, :3].sum(axis=2) <= 12)
        # Fill gaps with low-saturation cardboard from draft (never global median —
        # AP red bands used to flood the whole silhouette into a flat badge).
        if empty.any():
            covered = mask & ~empty
            d = draft[:, :, :3].astype(np.float32)
            dmax = d.max(axis=2)
            dmin = d.min(axis=2)
            dsat = np.zeros_like(dmax)
            ok = dmax > 1.0
            dsat[ok] = (dmax[ok] - dmin[ok]) / dmax[ok] * 255.0
            cardboard = covered & (dsat < 55)
            if cardboard.any():
                fill = np.median(draft[:, :, :3][cardboard], axis=0).astype(np.uint8)
            elif covered.any():
                # fallback: darkest quartile of covered (usually body, not band)
                lum = 0.299 * d[:, :, 0] + 0.587 * d[:, :, 1] + 0.114 * d[:, :, 2]
                vals = lum[covered]
                thr_l = float(np.percentile(vals, 40))
                body = covered & (lum <= thr_l)
                fill_m = body if body.any() else covered
                fill = np.median(draft[:, :, :3][fill_m], axis=0).astype(np.uint8)
            else:
                fill = np.array([140, 138, 132], dtype=np.uint8)
            rgb[empty] = fill
        mode = "alpha-only"

    # Outer rim: pull color from eroded interior of draft (not plate lid text,
    # not AI fringe). Falls back to plate if interior empty.
    if rim_plate > 0:
        core = erode_mask(mask, rim_plate)
        rim = mask & ~core
        if core.any() and (draft[:, :, :3][core].sum(axis=1) > 12).any():
            d = draft[:, :, :3]
            covered_core = core & (d.sum(axis=2) > 12)
            if covered_core.any():
                # nearest-ish: fill rim with median of core cardboard (low sat)
                dc = d.astype(np.float32)
                dmax = dc.max(axis=2)
                dmin = dc.min(axis=2)
                dsat = np.zeros_like(dmax)
                ok = dmax > 1.0
                dsat[ok] = (dmax[ok] - dmin[ok]) / dmax[ok] * 255.0
                card = covered_core & (dsat < 60)
                src_m = card if card.any() else covered_core
                fill = np.median(d[src_m], axis=0).astype(np.uint8)
                # Always re-paint rim from interior cardboard — kills AI halo.
                rgb[rim] = fill
            else:
                rgb[rim] = sil_arr[:, :, :3][rim]
        else:
            rgb[rim] = sil_arr[:, :, :3][rim]
        mode = f"{mode}+rim{rim_plate}"

    out = np.zeros((canvas, canvas, 4), dtype=np.uint8)
    out[:, :, :3] = rgb
    if alpha_from == "draft":
        # Cut follows the generated box (after choke), not the canon plate.
        # Dilated sil keeps stray BG junk from surviving far outside the slot.
        dil = mask.copy()
        for _ in range(2):
            pad = np.pad(dil, 1, constant_values=False)
            dil = (
                pad[0:-2, 0:-2]
                | pad[0:-2, 1:-1]
                | pad[0:-2, 2:]
                | pad[1:-1, 0:-2]
                | pad[1:-1, 1:-1]
                | pad[1:-1, 2:]
                | pad[2:, 0:-2]
                | pad[2:, 1:-1]
                | pad[2:, 2:]
            )
        da = draft[:, :, 3]
        if hard_alpha:
            out[:, :, 3] = np.where((da > 8) & dil, 255, 0).astype(np.uint8)
        else:
            out[:, :, 3] = np.where(dil, da, 0).astype(np.uint8)
        out[out[:, :, 3] <= 8, :3] = 0
        mode = f"{mode}+A=draft"
    elif hard_alpha:
        out[:, :, 3] = np.where(mask, 255, 0).astype(np.uint8)
        mode = f"{mode}+hardA"
        out[~mask, :3] = 0
    else:
        out[:, :, 3] = sil_a
        out[~mask, :3] = 0

    if soft_outline > 0:
        out = apply_soft_outline(out, strength=soft_outline)
        mode = f"{mode}+ol{soft_outline:.2f}"

    # Soft-alpha ring: only where draft covers — else sil soft edge becomes a ghost halo.
    soft = (out[:, :, 3] > 8) & (out[:, :, 3] < 250)
    if soft.any() and alpha_from == "sil":
        draft_cov = draft[:, :, 3] > 8
        use = soft & draft_cov
        if use.any():
            out[:, :, :3][use] = sil_arr[:, :, :3][use]
        ghost = soft & ~draft_cov
        if ghost.any():
            out[ghost] = 0
        mode = f"{mode}+softRingSil"

    Image.fromarray(out, "RGBA").save(dst)

    iou = float((mask & (out[:, :, 3] > 8)).sum() / max(1, mask.sum()))
    print(f"{src.name} -> {dst.name} IoU={iou:.4f} fit={fit} choke={choke} key={key} {mode}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sources", nargs="+")
    ap.add_argument("--silhouette", default="", help="Canon silhouette (required unless --outline-only).")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--fit", choices=("contain", "cover"), default="contain")
    ap.add_argument("--structure", type=float, default=0.72)
    ap.add_argument(
        "--thr",
        type=int,
        default=28,
        help="RGB sum threshold for black-BG keying (higher = harder cut).",
    )
    ap.add_argument(
        "--plate-first",
        action="store_true",
        help="Keep plate mesh 100%; tint/band/text from draft.",
    )
    ap.add_argument(
        "--choke",
        type=int,
        default=3,
        help="Erode draft alpha (px) to drop AI light fringe before fit.",
    )
    ap.add_argument(
        "--rim-plate",
        type=int,
        default=2,
        help="Replace outer N px of silhouette RGB with plate (canon edge).",
    )
    ap.add_argument(
        "--hard-alpha",
        action="store_true",
        help="Binary alpha from silhouette mask (no soft fringe from plate).",
    )
    ap.add_argument(
        "--alpha-from",
        choices=("sil", "draft"),
        default="sil",
        help="sil=canon outline; draft=cut follows generated box (cleaner when shapes differ).",
    )
    ap.add_argument(
        "--key",
        choices=("auto", "magenta", "black", "alpha"),
        default="auto",
        help="Draft BG cut: magenta chroma (#FF00FF), black luminance, existing alpha, or auto-detect.",
    )
    ap.add_argument(
        "--soft-outline",
        type=float,
        default=0.0,
        help="Very soft dark outline strength 0..1 (vanilla-like rim). Use ~0.35–0.45.",
    )
    ap.add_argument(
        "--outline-only",
        action="store_true",
        help="Only apply soft outline to existing RGBA icons (ignore silhouette composite).",
    )
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for s in args.sources:
        src = Path(s)
        dst = out_dir / src.name
        if args.outline_only:
            arr = np.array(Image.open(src).convert("RGBA"))
            arr = apply_soft_outline(arr, strength=args.soft_outline or 0.4)
            Image.fromarray(arr, "RGBA").save(dst)
            print(f"{src.name} -> {dst.name} outline-only strength={args.soft_outline or 0.4}")
            continue
        if not args.silhouette:
            raise SystemExit("--silhouette is required unless --outline-only")
        lock_to_silhouette(
            src,
            dst,
            sil_path=Path(args.silhouette),
            fit=args.fit,
            thr=args.thr,
            structure=0.0 if args.plate_first else args.structure,
            plate_first=args.plate_first,
            choke=args.choke,
            rim_plate=args.rim_plate,
            hard_alpha=args.hard_alpha,
            alpha_from=args.alpha_from,
            soft_outline=args.soft_outline,
            key=args.key,
        )


if __name__ == "__main__":
    main()
