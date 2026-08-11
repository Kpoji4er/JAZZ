"""Rebuild stock ChipIcons as flat beige glyphs (match Icons/Upgrades/Chips style).

Uses GenerateImage drafts (or pass --from-hud) → finalize 64×64 → solid #C8C0A8.
Also wires ChipIcon in items.lua for Folded/UnFolded/No when missing.

Typical:
  1) Generate drafts via $create-jazz-chip-icons (stock attachment only, not photo).
  2) python docs/tools/_rebuild_stock_chip_glyphs.py --finalize-dir <assets>
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CHIPS = ROOT / "Icons" / "Upgrades" / "Chips"
COLOR = (0xC8, 0xC0, 0xA8)
SIZE = 64
FINALIZE = ROOT / ".agents" / "skills" / "create-jazz-chip-icons" / "scripts" / "finalize-chip-icon.ps1"

# draft stem → output ComponentId(s)
DRAFT_MAP = {
	"chip_stock_folded_draft.png": ("JAZZ_StockLightFolded", "JAZZ_StockFolded"),
	"chip_stock_unfolded_draft.png": ("JAZZ_StockLightUnFolded", "JAZZ_StockLight"),
	"chip_stock_no_draft.png": ("JAZZ_StockNo",),
}


def flatten_solid(path: Path) -> None:
	arr = np.array(Image.open(path).convert("RGBA"))
	out = np.zeros_like(arr)
	for y in range(arr.shape[0]):
		for x in range(arr.shape[1]):
			r, g, b, a = map(int, arr[y, x])
			if a < 8:
				continue
			mx, mn = max(r, g, b), min(r, g, b)
			if mx <= 40 and (mx - mn) <= 12:
				continue
			if mx < 90:
				out[y, x] = (30, 28, 24, a)
				continue
			out[y, x] = (*COLOR, a if a > 180 else max(a, 200))
	Image.fromarray(out, "RGBA").save(path)
	print(f"flattened {path.name}")


def finalize(draft: Path, component_id: str) -> Path:
	cmd = [
		"powershell",
		"-NoProfile",
		"-File",
		str(FINALIZE),
		"-SourceDraft",
		str(draft),
		"-ComponentId",
		component_id,
		"-Recolor",
		"#C8C0A8",
		"-BlackKeyMax",
		"55",
	]
	subprocess.check_call(cmd)
	out = CHIPS / f"{component_id}.png"
	flatten_solid(out)
	return out


def main() -> None:
	ap = argparse.ArgumentParser()
	ap.add_argument(
		"--finalize-dir",
		type=Path,
		default=None,
		help="Directory with chip_stock_*_draft.png",
	)
	ap.add_argument("--flatten-only", action="store_true")
	args = ap.parse_args()

	if args.flatten_only:
		for name in (
			"JAZZ_StockLightFolded.png",
			"JAZZ_StockFolded.png",
			"JAZZ_StockLightUnFolded.png",
			"JAZZ_StockLight.png",
			"JAZZ_StockNo.png",
		):
			p = CHIPS / name
			if p.exists():
				flatten_solid(p)
		return

	if not args.finalize_dir:
		raise SystemExit("pass --finalize-dir <assets> or --flatten-only")

	for draft_name, ids in DRAFT_MAP.items():
		draft = args.finalize_dir / draft_name
		if not draft.exists():
			print(f"skip missing {draft}")
			continue
		for cid in ids:
			finalize(draft, cid)


if __name__ == "__main__":
	main()
