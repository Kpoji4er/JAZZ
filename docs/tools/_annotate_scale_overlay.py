"""Stamp a metre ruler and measured lengths onto _overlay_weapon_length.py renders.

python docs/tools/_annotate_scale_overlay.py --out <overlay folder> [--reference <label>]

Reads overlay-report.json for pixels-per-metre, so ticks are real distances and
not eyeballed. Writes annotated_<frame>.png next to the raw renders.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BACKDROP = (42, 42, 42)
INK = (236, 236, 236)
TICK = (150, 205, 255)
ACCENT = (255, 196, 92)


def font(size):
    for name in ('segoeui.ttf', 'arial.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--reference', default=None, help='label used as the 1.00x baseline')
    args = p.parse_args()
    report = json.loads((args.out / 'overlay-report.json').read_text(encoding='utf-8'))
    weapons = {k: v for k, v in report.items() if not k.startswith('_')}
    baseline = args.reference or next(iter(weapons))
    ruler, label, small = font(26), font(30), font(22)

    for frame, meta in report['_frames'].items():
        render = Image.open(meta['file']).convert('RGBA')
        ppm = meta['pixels_per_metre']
        pad_top, pad_left, pad_bottom = 56, 250, 92
        canvas = Image.new('RGBA', (render.width + pad_left + 24, render.height + pad_top + pad_bottom), (*BACKDROP, 255))
        draw = ImageDraw.Draw(canvas)

        # Ruler across the shared metre frame; the render is ortho, so px/m is constant.
        axis = canvas.height - pad_bottom + 34
        origin = pad_left
        draw.line([(origin, axis), (origin + render.width, axis)], fill=TICK, width=2)
        step = 0.10
        index = 0
        while origin + index * step * ppm <= origin + render.width:
            x = origin + index * step * ppm
            major = index % 5 == 0
            draw.line([(x, axis - (14 if major else 7)), (x, axis + (14 if major else 7))], fill=TICK, width=2 if major else 1)
            if major:
                draw.text((x, axis + 20), f'{index * step:.1f} m', fill=TICK, font=small, anchor='ma')
            index += 1

        canvas.alpha_composite(render, (pad_left, pad_top))
        mode, view = frame.split('_')
        draw.text((24, 18), f'{view.upper()} view — aligned at {"muzzle" if mode == "muzzle" else "left-hand grip"}'
                            f'   ·   {ppm:.0f} px/m   ·   orthographic, true relative scale',
                  fill=INK, font=label)

        bands = meta.get('rows') or [{'label': n, 'centre_px': (i + 0.5) * render.height / len(weapons)}
                                     for i, n in enumerate(weapons)]
        for band in bands:
            name = band['label']
            data = weapons[name]
            centre = pad_top + band['centre_px']
            ratio = data['length_m'] / weapons[baseline]['length_m']
            draw.text((24, centre - 34), name, fill=ACCENT, font=label)
            draw.text((24, centre + 2), f"{data['length_m'] * 1000:.0f} mm", fill=INK, font=ruler)
            draw.text((24, centre + 32),
                      f"{ratio:.3f}x {baseline}" if name != baseline else 'reference', fill=INK, font=small)
        target = args.out / ('annotated_' + frame + '.png')
        canvas.convert('RGB').save(target)
        print('WROTE', target)


if __name__ == '__main__':
    main()
