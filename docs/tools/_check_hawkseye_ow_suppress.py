# Static: Scope HawksEye sniper OW 1 AP, suppress ×2, biscuits 96h×7.
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
ce = (root / "CharacterEffect/HawksEye.lua").read_text(encoding="utf-8")
named = (root / "Code/System_NamedPerks.lua").read_text(encoding="utf-8")
orw = (root / "Code/System_OR_Weapons.lua").read_text(encoding="utf-8")
items = (root / "items.lua").read_text(encoding="utf-8")
meta = (root / "metadata.lua").read_text(encoding="utf-8")
ru = (root / "Russian.csv").read_text(encoding="utf-8")
en = (root / "English.csv").read_text(encoding="utf-8")

fail = []

if "'Value', 96" not in ce or "'Value', 7" not in ce:
    fail.append("HawksEye.lua: hoursToProduce=96 / amountToProduce=7 missing")
if "overwatchCostOverwrite" not in ce or "pindownCostOverwrite" not in ce:
    fail.append("HawksEye.lua: cost overwrite params missing")
if 'Event = "OnNewHour"' not in ce or 'Event = "OnMercHired"' not in ce:
    fail.append("HawksEye.lua: OnNewHour / OnMercHired missing")
if 'PlaceItemInInventory("Cookie"' not in ce:
    fail.append("HawksEye.lua: Cookie production missing")
if "890000000009870" not in ce:
    fail.append("HawksEye.lua: Description ID missing")

if "function Jazz_ApplyHawksEyeSuppression" not in named:
    fail.append("System_NamedPerks.lua: Jazz_ApplyHawksEyeSuppression missing")
if "function Jazz_HawksEyeSniperOverwatchAP" not in named:
    fail.append("System_NamedPerks.lua: Jazz_HawksEyeSniperOverwatchAP missing")
if "lInstallHawksEyeOverwatchCost" not in named:
    fail.append("System_NamedPerks.lua: Overwatch wrap install missing")

if "Jazz_ApplyHawksEyeSuppression" not in orw:
    fail.append("System_OR_Weapons.lua: HawksEye suppress hook missing")

if "Scope HawksEye: sniper Overwatch costs 1 AP" not in items:
    fail.append("items.lua: Overwatch HawksEye 1 AP branch missing")
if "'Id', \"HawksEye\"" not in items:
    fail.append("items.lua: HawksEye ModItem missing")
if "hoursToProduce" not in items[items.find("'Id', \"HawksEye\"") : items.find("'Id', \"HawksEye\"") + 4000]:
    fail.append("items.lua: HawksEye hoursToProduce missing")

if '"CharacterEffect/HawksEye.lua"' not in meta:
    fail.append("metadata.lua: HawksEye companion not loaded")

for lid in ("890000000009869", "890000000009870"):
    if not any(line.startswith(lid + ",") for line in ru.splitlines()):
        fail.append(f"Russian.csv missing {lid}")
    if not any(line.startswith(lid + ",") for line in en.splitlines()):
        fail.append(f"English.csv missing {lid}")
if "Каждые <hoursToProduce> ч" not in ru:
    fail.append("Russian.csv: periodic biscuit sentence missing")
if "Every <hoursToProduce> h" not in en:
    fail.append("English.csv: periodic biscuit sentence missing")

if fail:
    print("FAIL:")
    for m in fail:
        print(" ", m)
    sys.exit(1)
print("OK HawksEye: sniper OW 1 AP keep leftover; suppress x2; biscuits 96h x7 + hire")
sys.exit(0)
