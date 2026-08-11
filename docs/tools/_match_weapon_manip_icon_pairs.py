"""Match Flash on/off and Stock fold/unfold chip silhouettes (54x54).

Masters: weapon_flash_on.png, weapon_stock_fold.png
Derived:
  - flash off = same body, beams removed (grow from handle seed)
  - stock unfold = same rifle CC + fold-arrow CC rotated 180° (reverse indicator)
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

HUD = Path(__file__).resolve().parents[2] / "Icons" / "Hud"


def rgba(path: Path) -> np.ndarray:
	return np.array(Image.open(path).convert("RGBA"))


def save(arr: np.ndarray, path: Path) -> None:
	Image.fromarray(arr, "RGBA").save(path)
	print(f"wrote {path.name} {arr.shape[1]}x{arr.shape[0]}")


def visible(arr: np.ndarray) -> np.ndarray:
	return (arr[:, :, 3] > 20) & (arr[:, :, 0:3].max(axis=2) > 40)


def components(vis: np.ndarray) -> list[list[tuple[int, int]]]:
	h, w = vis.shape
	seen = np.zeros_like(vis)
	comps: list[list[tuple[int, int]]] = []
	for y in range(h):
		for x in range(w):
			if not vis[y, x] or seen[y, x]:
				continue
			q = deque([(y, x)])
			seen[y, x] = True
			cells: list[tuple[int, int]] = []
			while q:
				cy, cx = q.popleft()
				cells.append((cy, cx))
				for dy in (-1, 0, 1):
					for dx in (-1, 0, 1):
						ny, nx = cy + dy, cx + dx
						if ny < 0 or nx < 0 or ny >= h or nx >= w:
							continue
						if seen[ny, nx] or not vis[ny, nx]:
							continue
						seen[ny, nx] = True
						q.append((ny, nx))
			comps.append(cells)
	comps.sort(key=len, reverse=True)
	return comps


def flood(seed_mask: np.ndarray, allow: np.ndarray) -> np.ndarray:
	h, w = allow.shape
	out = np.zeros_like(allow, dtype=bool)
	ys, xs = np.where(seed_mask & allow)
	q = deque(zip(ys.tolist(), xs.tolist()))
	for y, x in q:
		out[y, x] = True
	while q:
		y, x = q.popleft()
		for dy in (-1, 0, 1):
			for dx in (-1, 0, 1):
				ny, nx = y + dy, x + dx
				if ny < 0 or nx < 0 or ny >= h or nx >= w:
					continue
				if out[ny, nx] or not allow[ny, nx]:
					continue
				out[ny, nx] = True
				q.append((ny, nx))
	return out


def flash_off_from_on(on: np.ndarray) -> np.ndarray:
	h, w = on.shape[:2]
	vis = visible(on)
	seed = np.zeros_like(vis)
	seed[int(h * 0.45) :, : int(w * 0.55)] = True
	body = flood(seed, vis)
	changed = True
	guard = 0
	while changed and guard < 40:
		changed = False
		guard += 1
		ys, xs = np.where(vis & ~body)
		for y, x in zip(ys.tolist(), xs.tolist()):
			y0, y1 = max(0, y - 1), min(h, y + 2)
			x0, x1 = max(0, x - 1), min(w, x + 2)
			if not body[y0:y1, x0:x1].any():
				continue
			if int(vis[y0:y1, x0:x1].sum()) >= 5:
				body[y, x] = True
				changed = True
	off = np.zeros_like(on)
	off[body] = on[body]
	print(f"flash body={int(body.sum())} rays={int((vis & ~body).sum())}")
	return off


def stock_unfold_from_fold(fold: np.ndarray) -> np.ndarray:
	h, w = fold.shape[:2]
	comps = components(visible(fold))
	print(f"stock comps={[len(c) for c in comps[:4]]}")
	if len(comps) < 2:
		raise SystemExit("expected rifle + arrow components on weapon_stock_fold.png")
	body_cells, arrow_cells = comps[0], comps[1]
	body = np.zeros_like(visible(fold))
	for y, x in body_cells:
		body[y, x] = True

	unfold = np.zeros_like(fold)
	unfold[body] = fold[body]

	xs = [x for _, x in arrow_cells]
	ys = [y for y, _ in arrow_cells]
	cx = (min(xs) + max(xs)) / 2
	cy = (min(ys) + max(ys)) / 2
	# 180° rotate around arrow center → reverse direction, same under-stock band
	for y, x in arrow_cells:
		nx = int(round(2 * cx - x))
		ny = int(round(2 * cy - y))
		if 0 <= nx < w and 0 <= ny < h and not body[ny, nx]:
			unfold[ny, nx] = fold[y, x]
	return unfold


def main() -> None:
	on = rgba(HUD / "weapon_flash_on.png")
	off = flash_off_from_on(on)
	save(off, HUD / "weapon_flash_off.png")
	vm, vd = visible(on), visible(off)
	print(
		f"flash: overlap={int((vm & vd).sum())} "
		f"only_on={int((vm & ~vd).sum())} only_off={int((vd & ~vm).sum())}"
	)

	fold = rgba(HUD / "weapon_stock_fold.png")
	unfold = stock_unfold_from_fold(fold)
	save(unfold, HUD / "weapon_stock_unfold.png")
	body = np.zeros_like(visible(fold))
	for y, x in components(visible(fold))[0]:
		body[y, x] = True
	uv = visible(unfold)
	print(
		f"stock body: match={int((body & uv).sum())} "
		f"missing={int((body & ~uv).sum())} arrow_extra={int((uv & ~body).sum())}"
	)


if __name__ == "__main__":
	main()
