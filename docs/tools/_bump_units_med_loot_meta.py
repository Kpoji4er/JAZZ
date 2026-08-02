# -*- coding: utf-8 -*-
from pathlib import Path

units_items = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\items.lua")
t = units_items.read_text(encoding="utf-8")
print("brace", t.count("{") - t.count("}"), "paren", t.count("(") - t.count(")"))
print("MedsDrop ids", t.count('id = "MedsDrop"'))
print("JAZZ_Bandage", t.count("JAZZ_Bandage"))

meta = Path(r"C:\Users\SsAnd\AppData\Roaming\Jagged Alliance 3\Mods\jazz-units\metadata.lua")
mt = meta.read_text(encoding="utf-8")
if "'version', 2259," in mt:
    mt = mt.replace("'version', 2259,", "'version', 2260,", 1)
elif "'version', 2260," in mt:
    print("version already 2260")
else:
    # try bump whatever
    import re
    mt2, n = re.subn(r"'version', (\d+),", lambda m: f"'version', {int(m.group(1))+1},", mt, count=1)
    print("version bump via regex", n)
    mt = mt2
note = "- MED-001 loot: Bandage/Morphine/SurgicalKit on medic kits; MedsDrop +bandages\n"
if "MED-001 loot" not in mt:
    mt = mt.replace("'last_changes', \"", "'last_changes', \"" + note, 1)
meta.write_text(mt, encoding="utf-8")
print("metadata OK")
