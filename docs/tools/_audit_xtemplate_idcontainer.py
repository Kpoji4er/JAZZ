#!/usr/bin/env python3
"""Locate XTemplate idContainer sites in items.lua.

Live SquadsAndMercs: Id must sit on satellite/inventory/tactical mode windows
(HUDMerc parents), not on the outer VList wrap under idParty.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
lines = (ROOT / "items.lua").read_text(encoding="utf-8").splitlines()

xt_id = "?"
for i, line in enumerate(lines, 1):
	s = line.strip()
	if s.startswith("PlaceObj('ModItemXTemplate'") or (
		s.startswith("PlaceObj('XTemplate'") and "Window" not in s and "Func" not in s
	):
		xt_id = f"(unlabeled @{i})"
		for k in range(i, min(i + 12, len(lines) + 1)):
			ks = lines[k - 1].strip()
			if ks.startswith("id ="):
				xt_id = ks
				break
	if "'Id', \"idContainer\"" in line:
		indent = len(line) - len(line.lstrip("\t"))
		nxt = " | ".join(x.strip() for x in lines[i : i + 4])
		print(f"{i:6d} tabs={indent}  xt={xt_id}")
		print(f"         {nxt[:180]}")

# Contract for live HUD (id = "SquadsAndMercs", not *2 / *_copy).
live_rows = []
xt_id = "?"
for i, line in enumerate(lines, 1):
	s = line.strip()
	if s.startswith("PlaceObj('ModItemXTemplate'"):
		xt_id = "?"
		for k in range(i, min(i + 12, len(lines) + 1)):
			ks = lines[k - 1].strip()
			if ks.startswith("id ="):
				xt_id = ks
				break
	if xt_id == 'id = "SquadsAndMercs",' and "'Id', \"idContainer\"" in line:
		live_rows.append((i, len(line) - len(line.lstrip("\t"))))
errors = []
if len(live_rows) != 3:
	errors.append(f"expected 3 idContainer on live SquadsAndMercs, got {live_rows}")
elif any(tabs != 9 for _, tabs in live_rows):
	errors.append(f"Id must be on mode windows (tabs=9), got {live_rows}")
if errors:
	print("FAIL live SquadsAndMercs:")
	for e in errors:
		print(" -", e)
	sys.exit(1)
print("OK live SquadsAndMercs: 3 mode-window idContainer (tabs=9), no outer wrap Id")
