"""Quick palette/size stats for Chip PNGs."""
from pathlib import Path
from collections import Counter

try:
    from PIL import Image
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CHIPS = ROOT / "Icons" / "Upgrades" / "Chips"

sizes = Counter()
opaque_colors = Counter()
has_green = 0
samples = 0
jazz = list(CHIPS.glob("JAZZ_*.png"))
for p in jazz:
    im = Image.open(p).convert("RGBA")
    sizes[im.size] += 1
    samples += 1
    px = list(im.getdata())
    greens = 0
    sands = 0
    for r, g, b, a in px:
        if a < 200:
            continue
        # green glass?
        if g > r + 20 and g > b + 20 and g > 60:
            greens += 1
        # sand-ish
        if abs(r - g) < 25 and abs(g - b) < 40 and r > 140 and r < 230:
            sands += 1
            opaque_colors[(r // 8 * 8, g // 8 * 8, b // 8 * 8)] += 1
    if greens > 20:
        has_green += 1

print(f"JAZZ_ chip count: {len(jazz)}")
print(f"sizes: {dict(sizes)}")
print(f"with green accent pixels: {has_green}")
print("top sand-ish quantized colors:")
for color, n in opaque_colors.most_common(8):
    print(f"  #{color[0]:02X}{color[1]:02X}{color[2]:02X}  hits={n}")

# compare a few wired vs unwired
wired_examples = [
    "JAZZ_Reflex_Eotech",
    "JAZZ_MagQuick",
    "JAZZ_SuppressorImproved",
    "JAZZ_VerticalGrip_Commando",
]
for name in wired_examples:
    p = CHIPS / f"{name}.png"
    if p.exists():
        im = Image.open(p)
        print(f"{name}: size={im.size} mode={im.mode}")
