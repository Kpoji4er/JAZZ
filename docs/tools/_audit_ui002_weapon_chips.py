from pathlib import Path
import re

text = Path("items.lua").read_text(encoding="utf-8")
for aid in ["FoldStock", "UnFoldStock", "FlashlightOn", "FlashlightOff", "Unjam"]:
    i = text.find(f'id = "{aid}"')
    assert i > 0, aid
    chunk = text[max(0, i - 900) : i + 40]
    m = re.search(r"ShowIn = ([^,\n]+)", chunk)
    print(aid, "ShowIn", m.group(1) if m else "MISSING")
    if aid == "Unjam":
        assert m and '"CombatActions"' in m.group(1)
    else:
        assert m and m.group(1).strip() == "false"

assert "idFoldStockButton" in text and "idFlashlightButton" in text
fold_i = text.find("idFoldStockButton")
assert "'GridX', 2" in text[fold_i : fold_i + 500]
flash_i = text.find("idFlashlightButton")
assert "'GridX', 2" in text[flash_i : flash_i + 500]
assert "System_WeaponCompHUD" in text
assert "Code/System_WeaponCompHUD.lua" in Path("metadata.lua").read_text(encoding="utf-8")

hud = Path("Code/System_WeaponCompHUD.lua").read_text(encoding="utf-8")
assert "JazzWeaponCompHasFoldingPair" in hud
assert "JazzResolveFoldStockAction" in hud

fs = text.find('id = "FoldStock"')
chunk = text[text.rfind("PlaceObj", 0, fs) : fs]
assert "JazzWeaponCompHasFoldingPair" in chunk
assert "JazzWeaponCompIdLooksUnfolded" in chunk
print("static AC checks OK")
