"""Downscale _render_weapon_icons.py output to exact icon size and build review sheets.

python docs/tools/_finalize_weapon_icons.py --out <icon folder> [--reference AK74]

Writes <label>.png at the target size plus review/<label>_vs_<reference>.png: the new
icon and the hand-made reference on the same #2a2a2a panel, so the contour can be
compared directly. Does not touch WeaponIcons/; installation is a separate step.
"""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
PANEL = (42, 42, 42)
INK = (232, 232, 232)
DIM = (150, 150, 150)


def font(size):
    for name in ('segoeui.ttf', 'arial.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def contour_profile(image):
    """Fraction of near-black pixels at each depth inside the silhouette, 1..6 px.

    Same measurement used to read the hand-made icons, so 'matches AK74' is a number
    rather than an impression.
    """
    alpha = image.getchannel('A').load()
    rgb = image.convert('RGB').load()
    w, h = image.size
    solid = [[alpha[x, y] > 128 for x in range(w)] for y in range(h)]

    def inside(x, y):
        return 0 <= x < w and 0 <= y < h and solid[y][x]

    depth = {}
    for y in range(h):
        for x in range(w):
            if not solid[y][x]:
                continue
            d = 1
            while d < 8 and all(inside(x + dx, y + dy)
                                for dx in range(-d, d + 1) for dy in range(-d, d + 1)):
                d += 1
            depth.setdefault(d, []).append(max(rgb[x, y]) < 31)
    return {d: round(sum(v) / len(v), 2) for d, v in sorted(depth.items()) if d <= 6}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--reference', default='AK74')
    args = p.parse_args()
    report = json.loads((args.out / 'icons-report.json').read_text(encoding='utf-8'))
    width, height = report['target']
    review = args.out / 'review'
    review.mkdir(parents=True, exist_ok=True)
    reference = Image.open(ROOT / 'WeaponIcons' / (args.reference + '.png')).convert('RGBA')
    label_font, small = font(26), font(20)
    summary = {}

    for label in report['icons']:
        raw = Image.open(args.out / (label + '_icon_2x.png')).convert('RGBA')
        icon = raw.resize((width, height), Image.Resampling.LANCZOS)
        icon.save(args.out / (label + '.png'))
        box = icon.getchannel('A').getbbox()
        summary[label] = {'size': list(icon.size), 'content_bbox': list(box),
                          'content': [box[2] - box[0], box[3] - box[1]],
                          'fill_width_pct': round(100 * (box[2] - box[0]) / width, 1),
                          'contour_dark_fraction': contour_profile(icon)}

        pad, gap, header, caption = 20, 40, 46, 34
        sheet = Image.new('RGBA', (width * 2 + pad * 2 + gap,
                                   height + header + pad * 2 + caption), (*PANEL, 255))
        draw = ImageDraw.Draw(sheet)
        draw.text((pad, pad - 4), f'{label} — new', fill=INK, font=label_font)
        draw.text((pad + width + gap, pad - 4), f'{args.reference} — hand-made',
                  fill=DIM, font=label_font)
        sheet.alpha_composite(icon, (pad, header + pad))
        sheet.alpha_composite(reference, (pad + width + gap, header + pad))
        profile = summary[label]['contour_dark_fraction']
        draw.text((pad, header + pad + height + 8),
                  f'{width}x{height} RGBA  ·  backdrop #2a2a2a  ·  contour dark fraction by depth '
                  + ' '.join(f'{d}px:{v}' for d, v in profile.items()),
                  fill=DIM, font=small)
        sheet.convert('RGB').save(review / f'{label}_vs_{args.reference}.png')

    summary[args.reference + ' (reference)'] = {
        'size': list(reference.size), 'contour_dark_fraction': contour_profile(reference)}
    (args.out / 'finalize-report.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print('FINALIZE=' + json.dumps(summary))


if __name__ == '__main__':
    main()
