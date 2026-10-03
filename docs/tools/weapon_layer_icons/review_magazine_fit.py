"""Arrange real full-weapon magazine photographs for side/oblique fit review."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np
from scipy import ndimage
from process_live import extract
from icon_layout import ROOT, colorize, fit

p = argparse.ArgumentParser(__doc__)
p.add_argument('--captures', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
receipt = json.loads((a.captures / 'capture-report.json').read_text(encoding='utf-8'))
assert receipt['phase'] == 'done' and receipt['disposed'] and not receipt['errors']
rows = [r for r in receipt['rows'] if r['status'] == 'captured' and not r.get('layer')]
weapons = list(dict.fromkeys(r['weapon'] for r in rows))
profiles = json.loads((ROOT / 'docs/design/weapon-layer-icons/live/layer-color-profiles.json').read_text(encoding='utf-8'))
sheet = Image.new('RGB', (1600, len(weapons) * 220), (42, 46, 50))
draw = ImageDraw.Draw(sheet)
for y, weapon in enumerate(weapons):
    for x, row in enumerate(r for r in rows if r['weapon'] == weapon):
        raw, _, _ = extract(a.captures, row)
        if receipt.get('recipe', {}).get('view') == 'oblique':
            # Review-only crop cleanup: side-on library inputs are never changed.
            rgba = np.array(raw)
            labels, count = ndimage.label(ndimage.binary_dilation(rgba[..., 3] > 25, iterations=15))
            if count > 1:
                keep = labels == np.argmax(np.bincount(labels.ravel())[1:]) + 1
                rgba[~keep] = 0
                raw = Image.fromarray(rgba, 'RGBA')
        icon = fit(colorize(raw, weapon, profiles), (390, 195))
        sheet.paste(icon, (x * 400, y * 220 + 25), icon)
        draw.text((x * 400 + 5, y * 220 + 4),
                  weapon + ' ' + row['label'].replace('Magazine-JAZZ_Mag', ''), fill='white')
a.output.parent.mkdir(parents=True, exist_ok=True)
sheet.save(a.output)
print(json.dumps({'weapons': len(weapons), 'photos': len(rows), 'output': str(a.output)}))
