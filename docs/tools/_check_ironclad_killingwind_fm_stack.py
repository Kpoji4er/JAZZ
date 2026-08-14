# Static: Ironclad and KillingWind each −50% armor FM tax (additive to 0).
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
unit = (root / "Code/System_OR_Unit.lua").read_text(encoding="utf-8")
iron = (root / "CharacterEffect/Ironclad.lua").read_text(encoding="utf-8")
kw = (root / "CharacterEffect/KillingWind.lua").read_text(encoding="utf-8")
meta = (root / "metadata.lua").read_text(encoding="utf-8")
items = (root / "items.lua").read_text(encoding="utf-8")

fail = []

if 'HasPerk(self, "Ironclad") or HasPerk(self, "KillingWind")' in unit:
    fail.append("System_OR_Unit.lua: shared OR half still present")
if "fm_mul = fm_mul - 50" not in unit:
    fail.append("System_OR_Unit.lua: missing additive fm_mul - 50")
if unit.count("fm_mul = fm_mul - 50") < 2:
    fail.append("System_OR_Unit.lua: expected two −50 FM perk steps")
if 'HasPerk(self, "Ironclad")' not in unit or 'HasPerk(self, "KillingWind")' not in unit:
    fail.append("System_OR_Unit.lua: missing perk checks")
if "ap = ap / 2" not in unit:
    fail.append("System_OR_Unit.lua: Ironclad AP ÷2 missing")
if "not self.using_cumbersome or HasPerk(self, \"KillingWind\")" not in unit:
    fail.append("BeginTurn: KillingWind cumbersome FreeMove path missing")

if "890000000013124" not in iron:
    fail.append("Ironclad.lua: missing Description ID 890000000013124")
if "890000000009876" not in kw:
    fail.append("KillingWind.lua: missing Description ID")
if "вместе с Железной кожей" not in kw:
    fail.append("KillingWind.lua: stacking sentence missing")
if '"CharacterEffect/Ironclad.lua"' not in meta:
    fail.append("metadata.lua: Ironclad companion not loaded")
if "'Id', \"Ironclad\"" not in items:
    fail.append("items.lua: Ironclad ModItem missing")
if "вместе с Железной кожей" not in items:
    fail.append("items.lua: KillingWind stacking sentence missing")

ru = (root / "Russian.csv").read_text(encoding="utf-8")
en = (root / "English.csv").read_text(encoding="utf-8")
for lid in ("890000000013124", "890000000009876"):
    if not any(line.startswith(lid + ",") for line in ru.splitlines()):
        fail.append(f"Russian.csv missing {lid}")
    if not any(line.startswith(lid + ",") for line in en.splitlines()):
        fail.append(f"English.csv missing {lid}")

if fail:
    print("FAIL:")
    for m in fail:
        print(" ", m)
    sys.exit(1)
print("OK Ironclad -50% + KillingWind -50% armor FM (stack to 0); cumbersome BeginTurn unchanged")
sys.exit(0)
