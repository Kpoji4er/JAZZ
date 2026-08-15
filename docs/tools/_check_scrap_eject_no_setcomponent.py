# -*- coding: utf-8 -*-
"""Static: scrap eject must not SetWeaponComponent (breaks SCRAP ALL on loaded loot)."""
from pathlib import Path

JAZZ = Path(__file__).resolve().parents[2]
maint = (JAZZ / "Code" / "System_WeaponResourceMaintenance.lua").read_text(encoding="utf-8")
inv = (JAZZ / "Code" / "Inventory.lua").read_text(encoding="utf-8")

start = maint.find("function JAZZ_EjectRemovableAttachmentsForScrap")
assert start > 0, "eject function missing"
end = maint.find("\nfunction ", start + 1)
body = maint[start:end if end > 0 else None]
if "weapon:SetWeaponComponent" in body:
    raise SystemExit("FAIL: JAZZ_EjectRemovableAttachmentsForScrap still calls SetWeaponComponent")
if "JAZZ_CreateRemovableAttachment" not in body or "JAZZ_DepositRemovableAttachment" not in body:
    raise SystemExit("FAIL: scrap eject no longer clones remountables into the bag")

if "JAZZ_EjectRemovableAttachmentsForScrap" not in inv:
    raise SystemExit("FAIL: ScrapItem does not call eject")
if "additional = additional or empty_table" not in inv:
    raise SystemExit("FAIL: ScrapItem next(nil) guard missing")
if "gv_Squads[squadId].units" in inv:
    raise SystemExit("FAIL: ScrapItem still indexes gv_Squads[squadId] unsafely")

print("OK scrap eject does not mutate weapon; ScrapItem special-scrap is nil-safe")
