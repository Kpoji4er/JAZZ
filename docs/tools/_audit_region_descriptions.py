# -*- coding: utf-8 -*-
"""Audit Region DisplayName/Description in jazz/items.lua."""
from pathlib import Path
import re

text = (Path(__file__).resolve().parents[2] / "items.lua").read_text(encoding="utf-8")
ids = [
	"ErnieIsland",
	"PortCacaoEnvirons",
	"GreatDesert",
	"MountainSteppe",
	"FleatownEnvirons",
	"LaBarrier",
	"GreatForest",
	"SeagullIsland",
]
for rid in ids:
	# Slice from this region's PlaceObj to the next ModItemRegion / end of list.
	start = text.find(f"id = \"{rid}\"")
	if start < 0:
		# alternate key style
		start = text.find(f"'id', \"{rid}\"")
	if start < 0:
		print(f"{rid}: NOT FOUND")
		continue
	# walk back to PlaceObj('ModItemRegion'
	block_start = text.rfind("PlaceObj('ModItemRegion'", 0, start)
	block_end = text.find("PlaceObj('ModItemRegion'", start + 1)
	if block_end < 0:
		block_end = start + 4000
	block = text[block_start:block_end]
	dn = re.search(r'DisplayName = "([^"]*)"', block) or re.search(
		r"'DisplayName', \"([^\"]*)\"", block
	)
	desc = re.search(r'Description = "([^"]*)"', block) or re.search(
		r"'Description', \"([^\"]*)\"", block
	)
	dn_s = dn.group(1) if dn else None
	desc_s = desc.group(1) if desc else ""
	print(f"{rid}: DisplayName={dn_s!r} Description_len={len(desc_s)}")
