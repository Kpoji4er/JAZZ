# Static: BulletHell GetUIState wrap accepts AbakanAutoFire / JAZZ_LargeAutoFire.
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
path = root / "Code" / "System_OR_Weapons.lua"
text = path.read_text(encoding="utf-8")
needles = [
    "JazzWrapBulletHellAutofireGate",
    "JazzFirearmHasBulletHellAutofire",
    'AbakanAutoFire',
    "JAZZ_LargeAutoFire",
    "JazzAutofireGateWrapped",
    "CombatActions.BulletHell",
]
missing = [n for n in needles if n not in text]
if missing:
    print("FAIL missing:", missing)
    sys.exit(1)
# AN94 still must not list AutoFire (regression of wrong fix path)
an94 = (root / "InventoryItem" / "AN94.lua").read_text(encoding="utf-8")
import re

m = re.search(r"AvailableAttacks\s*=\s*\{([^}]*)\}", an94, re.S)
atts = re.findall(r'"([^"]+)"', m.group(1)) if m else []
if "AutoFire" in atts:
    print("FAIL AN94 has AutoFire (should stay Abakan-only modes)")
    sys.exit(1)
if "AbakanAutoFire" not in atts:
    print("FAIL AN94 missing AbakanAutoFire")
    sys.exit(1)
print("OK BulletHell autofire gate + AN94 attacks")
