#!/usr/bin/env python3
"""Static: NoMaps wrap globals must be predeclared at file top before OnMsg writes."""
from __future__ import annotations

import re
import sys
from pathlib import Path

NOMAPS = Path(__file__).resolve().parents[2].parent / "jazz-nomaps" / "Code" / "NoMaps_Autonomy.lua"

REQUIRED = [
	"g_JAZZ_NoMapsGenerateEnemySquadWrapped",
	"g_JAZZ_NoMapsBaseGenerateEnemySquad",
	"g_JAZZ_NoMapsWorldFlipGuarded",
	"g_JAZZ_NoMapsBaseWorldFlip",
	"JAZZ_NoMaps_CreateUnitDataWrapped",
	"JAZZ_NoMaps_BaseCreateUnitData",
	"JAZZ_NoMaps_UnitMarkerWrapped",
	"JAZZ_NoMaps_BaseUnitMarkerSpawnObjects",
	"g_JAZZ_NoMapsSkipUnitRemap",
]


def main() -> int:
	if not NOMAPS.is_file():
		print("FAIL — missing", NOMAPS)
		return 1
	text = NOMAPS.read_text(encoding="utf-8")
	# Top-of-file region before first GameVar / local function
	head = text.split("GameVar(", 1)[0]
	errors = []
	for name in REQUIRED:
		if not re.search(rf"^{re.escape(name)}\s*=", head, re.M):
			errors.append(f"not predeclared at file top: {name}")
		if f'rawset(_G, "{name}"' not in text and f"rawset(_G, '{name}'" not in text:
			# flags that are only read via rawget may still need rawset on write
			if name.endswith("Wrapped") or name.startswith("g_JAZZ_NoMapsBase") or "Base" in name:
				if f'rawset(_G, "{name}"' not in text:
					errors.append(f"no rawset write for {name}")
		if name == "g_JAZZ_NoMapsSkipUnitRemap" and f'rawset(_G, "{name}"' not in text:
			errors.append(f"no rawset write for {name}")
	if "lQuestVarSafeSet" not in text:
		errors.append("missing lQuestVarSafeSet")
	if errors:
		print("FAIL")
		for e in errors:
			print(" -", e)
		return 1
	print("OK — NoMaps wrap globals predeclared + rawset + safe quest set")
	return 0


if __name__ == "__main__":
	sys.exit(main())
