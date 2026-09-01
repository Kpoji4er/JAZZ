#!/usr/bin/env python3
"""JAZZ-INV-005 static: field bandage/morphine salvage yield is 1 Meds; kits not in the table."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Code" / "System_JazzStackableMedicine.lua"


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    if "function Jazz_FieldMedicineSalvageMeds" not in text:
        print("FAIL: Jazz_FieldMedicineSalvageMeds missing", file=sys.stderr)
        return 1
    body = re.search(
        r"function Jazz_FieldMedicineSalvageMeds\(class_id\)\s*(.*?)\nend",
        text,
        re.S,
    )
    if not body:
        print("FAIL: could not parse Jazz_FieldMedicineSalvageMeds body", file=sys.stderr)
        return 1
    fn = body.group(1)
    if 'class_id == "JAZZ_Bandage" or class_id == "JAZZ_Morphine"' not in fn or "return 1" not in fn:
        print("FAIL: bandage/morphine yield is not 1", file=sys.stderr)
        return 1
    for kit in ("FirstAidKit", "Medkit", "Reanimationsset", "SurgicalKit"):
        if kit in fn:
            print(f"FAIL: {kit} listed in field salvage yield", file=sys.stderr)
            return 1
    if "Jazz_InstallFieldMedsSalvageWrap" not in text or "Jazz_PatchInventoryFieldMedsSalvageUI" not in text:
        print("FAIL: salvage wrap or InventoryContextMenu patch missing", file=sys.stderr)
        return 1
    print("OK INV-005 field meds salvage (1/1, kits excluded)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
