#!/usr/bin/env python3
"""Static AC-005 checks for JAZZ-UNITS-005 AME pool."""
from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT.parent / "jazz-units"


def load_roster():
    path = Path(__file__).resolve().parent / "_gen_ame_roster_60.py"
    spec = importlib.util.spec_from_file_location("ame_roster", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod.ROSTER


def main() -> int:
    problems: list[str] = []
    roster = load_roster()
    if len(roster) != 60:
        problems.append(f"roster len {len(roster)} != 60")
    cats = Counter(m["cat"] for m in roster)
    expect = {"Irregulars": 20, "Fighters": 18, "Hardened": 10, "Specialists": 12}
    if dict(cats) != expect:
        problems.append(f"category counts {dict(cats)} != {expect}")
    fh = [m for m in roster if m["cat"] in ("Fighters", "Hardened")]
    combat = sum(
        1
        for m in fh
        if m["role"] in ("Autorifleman", "Machinegunner", "Grenadier")
    )
    if not fh or combat / len(fh) < 0.30:
        problems.append(f"combat roles in F+H {combat}/{len(fh)} < 30%")
    gc = sum(1 for m in roster if m["nat"] == "GrandChien")
    if not (0.20 * 60 <= gc <= 0.35 * 60):
        problems.append(f"GrandChien share {gc}/60 outside 20-35%")
    for i in range(1, 61):
        uid = f"JAZZ_AME_{i:02d}"
        if not (UNITS / "UnitData" / f"{uid}.lua").exists():
            problems.append(f"missing companion {uid}")
        for suf in ("", "_Big"):
            p = UNITS / "MercPortraits" / f"{uid}{suf}.png"
            if not p.exists():
                problems.append(f"missing portrait {p.name}")
    for name in (
        "f_nigeria.png",
        "f_kenya.png",
        "f_angola.png",
        "f_mali.png",
        "f_congo.png",
        "f_ghana.png",
        "f_senegal.png",
        "f_ethiopia.png",
    ):
        if not (ROOT / "Icons" / "Flags" / name).exists():
            problems.append(f"missing flag {name}")
    nat = (ROOT / "Code" / "System_AME_Nationalities.lua").read_text(encoding="utf-8")
    for nid in (
        "Nigeria",
        "Kenya",
        "Angola",
        "Mali",
        "Congo",
        "Ghana",
        "Senegal",
        "Ethiopia",
    ):
        if f'id = "{nid}"' not in nat:
            problems.append(f"nationality id missing {nid}")
    if problems:
        print("FAIL")
        for p in problems:
            print(" -", p)
        return 1
    print("PASS AC-005 static")
    print(f"  cats={dict(cats)} combat_FH={combat}/{len(fh)} GrandChien={gc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
