# Static: Trauma* clear/apply must sync Unit and UnitData (sat portrait icons).
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
med = (root / "Code/Systems_Medicine.lua").read_text(encoding="utf-8")

fail = []
for needle in (
    "local function lJazzStatusTwins",
    "function JazzPushTraumaToTwin",
    "function JazzPullTraumaHealingFromTwin",
    "function JazzSyncOpenMapTraumaTwins",
    "JazzPushTraumaToTwin(unit)",
    "JazzPullTraumaHealingFromTwin(unit)",
    "JazzSyncOpenMapTraumaTwins()",
):
    if needle not in med:
        fail.append(f"missing {needle}")

clear_start = med.find("function JazzClearZoneTrauma")
clear_end = med.find("\nfunction ", clear_start + 1)
clear_body = med[clear_start:clear_end]
if "lJazzStatusTwins" not in clear_body:
    fail.append("JazzClearZoneTrauma does not use Unit/UnitData twins")
if "lJazzClearZoneTraumaOne" not in clear_body:
    fail.append("JazzClearZoneTrauma missing one-object helper")

newhour = med.find("function OnMsg.NewHour()")
newhour_end = med.find("\nfunction OnMsg.", newhour + 1)
nh = med[newhour:newhour_end]
if "JazzPushTraumaToTwin(unit)" not in nh:
    fail.append("NewHour does not push trauma to UnitData twin")
if "JazzPullTraumaHealingFromTwin" not in nh:
    fail.append("NewHour does not pull jazz_healing from twin")

if fail:
    print("FAIL:")
    for m in fail:
        print(" ", m)
    sys.exit(1)
print("OK trauma Unit/UnitData twin sync (clear/push/NewHour/LoadGame)")
sys.exit(0)
