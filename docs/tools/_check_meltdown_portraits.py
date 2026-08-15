# -*- coding: utf-8 -*-
"""Static: Meltdown squad Portrait/BigPortrait ship as jazz-units MercPortraits PNGs."""
from pathlib import Path

UNITS = Path(__file__).resolve().parents[2].parent / "jazz-units"
portraits = UNITS / "MercPortraits"
need = [
    portraits / "Meltdown.png",
    portraits / "Meltdown_Big.png",
]
for p in need:
    if not p.is_file() or p.stat().st_size < 1000:
        raise SystemExit(f"FAIL missing {p}")

needle = 'Mod/Dv3mFVN/MercPortraits/Meltdown.png'
for rel in ("UnitData/Meltdown.lua", "items.lua"):
    text = (UNITS / rel).read_text(encoding="utf-8")
    if needle not in text:
        raise SystemExit(f"FAIL {rel} does not wire {needle}")
    if 'UI/MercsPortraits/Meltdown"' in text or "UI/MercsPortraits/Meltdown'," in text:
        raise SystemExit(f"FAIL {rel} still points at vanilla UI/MercsPortraits/Meltdown")

print("OK Meltdown Portrait+BigPortrait shipped and wired")
