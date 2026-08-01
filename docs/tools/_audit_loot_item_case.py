# Audit LootEntryInventoryItem item= vs InventoryItem DefineClass IDs (case mismatch).
# Example: CSV slug Mas36 vs class MAS36 → MissingItem at runtime.
import re
import sys
from pathlib import Path

jazz = Path(__file__).resolve().parents[2]
units_items = jazz.parent / "jazz-units" / "items.lua"
classes = set()
for p in (jazz / "InventoryItem").glob("*.lua"):
	t = p.read_text(encoding="utf-8", errors="replace")
	for m in re.finditer(r"UndefineClass\('([^']+)'\)", t):
		classes.add(m.group(1))
	for m in re.finditer(r"DefineClass\.([A-Za-z0-9_]+)", t):
		classes.add(m.group(1))

text = units_items.read_text(encoding="utf-8")
refs = sorted(set(re.findall(r'item\s*=\s*"([^"]+)"', text)))
bad = []
for r in refs:
	if r in classes:
		continue
	real = [c for c in classes if c.lower() == r.lower()]
	if real:
		bad.append((r, real[0]))

print(f"case-mismatch={len(bad)}")
for r, real in bad:
	print(f"{r} -> {real}")
sys.exit(1 if bad else 0)
