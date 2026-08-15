# Static: Pierre Jazz_PierreRecruit uses HUD TargetChoice (first working iteration).
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
ca = (root / "Code/CombatActions.lua").read_text(encoding="utf-8")
items = (root / "items.lua").read_text(encoding="utf-8")
fail = []

install = ca.split("function Jazz_InstallPierreRecruitCombatAction")[1][:3500]
if "ShowCombatActionTargetChoice" not in install:
    fail.append("CombatActions.lua install missing ShowCombatActionTargetChoice")
if 'SetInGameInterfaceMode("IModeCombatAttack"' in install or "CombatActionAttackStart(self, units, args, \"IModeCombatAttack\")" in install:
    fail.append("CombatActions.lua install still starts IModeCombatAttack")
if "lInstallPierreRecruitTargetingWraps" in ca or "function CombatActionAttackStart(self, units, args, mode" in ca:
    fail.append("CombatActions.lua must not wrap CombatActionAttackStart for recruit")
if "Jazz_PierreRecruitRestoreUI" not in ca:
    fail.append("CombatActions.lua: Jazz_PierreRecruitRestoreUI missing")
if 'ca.Icon = "UI/Icons/Hud/talk"' not in ca:
    fail.append("CombatActions.lua: recruit Icon should be HUD talk")

idx = items.find('id = "Jazz_PierreRecruit"')
if idx < 0:
    fail.append("items.lua: Jazz_PierreRecruit ModItem missing")
else:
    block = items[max(0, idx - 4500) : idx + 200]
    if "ShowCombatActionTargetChoice" not in block:
        fail.append("items.lua: Jazz_PierreRecruit UIBegin missing ShowCombatActionTargetChoice")
    if 'CombatActionAttackStart(self, units, args, "IModeCombatAttack")' in block:
        fail.append("items.lua: Jazz_PierreRecruit UIBegin still IModeCombatAttack")
    if 'Icon = "UI/Icons/Hud/talk"' not in block:
        fail.append("items.lua: Jazz_PierreRecruit Icon not HUD talk")

if fail:
    print("FAIL:")
    for m in fail:
        print(" ", m)
    sys.exit(1)
print("OK Pierre recruit: TargetChoice HUD list (talk icon), no IModeCombatAttack")
sys.exit(0)
