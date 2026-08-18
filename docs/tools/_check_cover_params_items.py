#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confirm RangeAttackTargetStanceCover params in items.lua."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
text = (ROOT / "items.lua").read_text(encoding="utf-8", errors="replace")
i = text.find('id = "RangeAttackTargetStanceCover"')
if i < 0:
	raise SystemExit("RangeAttackTargetStanceCover not found")
chunk = text[max(0, i - 900) : i + 80]
params = re.findall(r"'Name', \"(\w+)\"[^']*'Value', (-?\d+)", chunk)
print("params:", params)
expected = {"Cover": "-45", "ExposedCover": "-12", "CrouchPenalty": "-12", "PronePenalty": "-23"}
got = dict(params)
for k, v in expected.items():
	if got.get(k) != v:
		raise SystemExit(f"FAIL {k}: got {got.get(k)!r} expected {v!r}")
print("OK cover params match owner soften (-45/-12/-12/-23)")

dust_ids = len(re.findall(r'id = "DustStormCoverCTHPenalty"', text))
if dust_ids != 1:
	raise SystemExit(f"FAIL DustStormCoverCTHPenalty count={dust_ids} expected 1")
dust = re.search(
	r'id = "DustStormCoverCTHPenalty",\s*scale = "%",\s*value = (-?\d+)',
	text,
)
if not dust or dust.group(1) != "-40":
	raise SystemExit(f"FAIL DustStormCoverCTHPenalty value {dust.group(1) if dust else None!r} expected -40")
print("OK DustStormCoverCTHPenalty unique -40")
