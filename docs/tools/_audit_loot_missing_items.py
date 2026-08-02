"""Audit jazz-units loot item= refs against known InventoryItem class IDs."""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
UNITS = JAZZ.parent / "jazz-units" / "items.lua"
VANILLA = Path(
    r"F:\SteamLibrary\steamapps\common\Jagged Alliance 3"
    r"\ModTools\Src\Data\InventoryItemCompositeDef"
)


def main() -> int:
    defined: set[str] = set()
    inv_dir = JAZZ / "InventoryItem"
    for p in inv_dir.rglob("*.lua"):
        text = p.read_text(encoding="utf-8", errors="replace")
        defined.update(re.findall(r"UndefineClass\('([^']+)'\)", text))

    items = (JAZZ / "items.lua").read_text(encoding="utf-8", errors="replace")
    defined.update(
        re.findall(
            r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{[^}]*?'Id',\s*\"([^\"]+)\"",
            items,
            flags=re.S,
        )
    )
    # Fallback: any 'Id' immediately after composite def open with Group line
    defined.update(
        re.findall(
            r"PlaceObj\('ModItemInventoryItemCompositeDef',\s*\{\s*"
            r"(?:'Group',\s*\"[^\"]+\",\s*)?'Id',\s*\"([^\"]+)\"",
            items,
        )
    )

    if VANILLA.exists():
        for p in VANILLA.glob("*.lua"):
            defined.add(p.stem)

    units = UNITS.read_text(encoding="utf-8", errors="replace")
    refs = Counter(re.findall(r'item\s*=\s*"([^"]+)"', units))

    missing = sorted(i for i in refs if i not in defined)
    print(f"defined={len(defined)} loot_refs={len(refs)} missing={len(missing)}")
    for i in missing[:100]:
        print(f"  MISSING {i} x{refs[i]}")

    for i in ("JAZZ_Bandage", "JAZZ_Morphine", "JAZZ_SurgicalKit"):
        print(f"{i}: defined={i in defined} refs={refs.get(i, 0)}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
