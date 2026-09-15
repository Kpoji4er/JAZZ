#!/usr/bin/env python3
"""Locate XTemplate idContainer sites in items.lua."""
from pathlib import Path

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
