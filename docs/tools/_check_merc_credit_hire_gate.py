# -*- coding: utf-8 -*-
"""Static check: MERC credit hire gate (CanAffordMerc wrap + medical waive)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Code" / "System_MERC_Account.lua"


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    checks = [
        ("g_JAZZ_MERC_CanAffordFn", "wrap flag declared"),
        ("CanAffordMerc", "CanAffordMerc referenced"),
        ("lInstallCanAffordMercWrap", "install helper"),
        ("Affiliation == \"MERC\"", "MERC affiliation gate"),
        ("MedicalPaidWhenHired", "medical deposit waive"),
        ("JAZZ_MERC_OnHired", "refund path"),
    ]
    failed = []
    for needle, label in checks:
        if needle not in text:
            failed.append(label)
    # Wrap must return true for MERC before calling base.
    if not re.search(
        r"lIsMERCUnit\(merc\).*?\n\s*return true",
        text,
        re.S,
    ):
        failed.append("MERC CanAfford returns true")
    if failed:
        print("FAIL", SRC.as_posix())
        for f in failed:
            print(" -", f)
        return 1
    print("OK", SRC.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
