# -*- coding: utf-8 -*-
from pathlib import Path
import re
from PIL import Image
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
src = ROOT / ".tmp/ui-extract/Icons/Items/fine_steel_pipe.dds"
out = ROOT / "Icons/Items/JAZZ_BarrelParts.png"

im = Image.open(src).convert("RGBA")
arr = np.array(im, dtype=np.float32)
rgb, a = arr[..., :3], arr[..., 3]
lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
# darker charcoal steel (black-gray)
gray = np.clip(lum * 0.38 + 18.0, 0, 255)
r = np.clip(gray * 0.90, 0, 255)
g = np.clip(gray * 0.93, 0, 255)
b = np.clip(gray * 1.02, 0, 255)
Image.fromarray(np.dstack([r, g, b, a]).astype(np.uint8), "RGBA").save(out)
print("wrote", out, out.stat().st_size)

icon = 'Mod/e6L4ECj/Icons/Items/JAZZ_BarrelParts.png'
items = ROOT / "items.lua"
text = items.read_text(encoding="utf-8")
pat = re.compile(
    r"('Id',\s*\"JAZZ_BarrelParts\",\s*'object_class',\s*\"ResourceItem\",\s*'Icon',\s*)\"[^\"]*\""
)
new_text, n = pat.subn(rf'\1"{icon}"', text, count=1)
print("items replacements", n)
if n:
    items.write_text(new_text, encoding="utf-8")

comp = ROOT / "InventoryItem/JAZZ_BarrelParts.lua"
ct = comp.read_text(encoding="utf-8")
ct2 = re.sub(r'Icon = "[^"]*"', f'Icon = "{icon}"', ct, count=1)
comp.write_text(ct2, encoding="utf-8")
print("companion:", [ln for ln in ct2.splitlines() if "Icon" in ln][0])
