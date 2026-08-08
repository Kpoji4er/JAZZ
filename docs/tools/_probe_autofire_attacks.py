# List weapons whose AvailableAttacks have jazz autofire aliases but not AutoFire/MGBurstFire.
import re
from pathlib import Path

root = Path(__file__).resolve().parents[2] / "InventoryItem"
for p in sorted(root.glob("*.lua")):
    t = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"AvailableAttacks\s*=\s*\{([^}]*)\}", t, re.S)
    if not m:
        continue
    atts = re.findall(r'"([^"]+)"', m.group(1))
    has_vanilla = "AutoFire" in atts or "MGBurstFire" in atts
    jazz_auto = [
        a
        for a in atts
        if a in ("AbakanAutoFire", "JAZZ_LargeAutoFire", "JAZZ_Autofire")
        or ("Auto" in a and a != "AutoFire")
    ]
    if jazz_auto and not has_vanilla:
        print(f"{p.name}: {atts}")
