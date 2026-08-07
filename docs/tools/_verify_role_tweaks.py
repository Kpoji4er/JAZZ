import re
from pathlib import Path

text = Path("items.lua").read_text(encoding="utf-8")
for wid in ["FAMAS", "Agram2000", "Sig550", "Sig550Custom", "PSG1"]:
    start = text.find(f"'Id', \"{wid}\"")
    chunk = text[start : start + 4000]
    print("===", wid, "===")
    for key in [
        "ShootAP",
        "Damage",
        "AimAccuracy",
        "MaxAimActions",
        "CritChanceScaled",
        "Recoil",
        "CloseRange",
        "CloseRangeFactor",
        "Grouping",
        "WeaponRange",
    ]:
        hits = re.findall(rf"'{key}',\s*([^,\n]+)", chunk)
        if hits:
            print(f"  {key}: {hits[0]}")
    if wid == "Sig550":
        print("  Side slot:", "'SlotType', \"Side\"" in chunk)
