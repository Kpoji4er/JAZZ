# -*- coding: utf-8 -*-
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
ids = ["AK74", "AKM", "FNFAL", "MicroUZI", "MP5K", "MP5", "Sterling", "BerettaM12", "M16A2", "AN94"]
for wid in ids:
    path = root / "InventoryItem" / f"{wid}.lua"
    if not path.exists():
        print(wid, "MISSING FILE")
        continue
    t = path.read_text(encoding="utf-8")
    def grab(name):
        m = re.search(rf"{name}\s*=\s*([^\n,]+)", t)
        return m.group(1).strip().strip('"') if m else "?"
    print(
        f"{wid}: Recoil={grab('Recoil')} Mass={grab('WeaponMass')} RPM={grab('CyclicRPM')} "
        f"Size={grab('WeaponSizeClass')} Burst={grab('BurstShots')} Auto={grab('AutoShots')} Lim={grab('BurstLimiter')}"
    )
