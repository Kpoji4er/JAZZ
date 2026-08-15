# Static: Pierre Jazz_PierreRecruit is one targeted signature, not a choice strip.
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[2]
ca = (root / "Code/CombatActions.lua").read_text(encoding="utf-8")
items = (root / "items.lua").read_text(encoding="utf-8")
fail = []

if "ShowCombatActionTargetChoice" in ca.split("function Jazz_InstallPierreRecruitCombatAction")[1][:2500]:
    fail.append("CombatActions.lua install still uses ShowCombatActionTargetChoice")
if 'self.id == "Jazz_PierreRecruit"' not in ca or "SetInGameInterfaceMode(\"IModeCombatAttack\"" not in ca:
    fail.append("CombatActions.lua: missing IModeCombatAttack start for Jazz_PierreRecruit")
if "Jazz_PierreRecruitRestoreUI" not in ca or "RestoreDefaultMode" not in ca:
    fail.append("CombatActions.lua: Jazz_PierreRecruit must restore UI after Interrupt/SetSide")
if "CheckAndReportImpossibleAttack" not in ca or "g_JAZZ_PierreRecruitImpossibleAttackWrapped" not in ca:
    fail.append("CombatActions.lua: missing CheckAndReportImpossibleAttack wrap")
if 'ca.Icon = "UI/Icons/Hud/talk"' not in ca:
    fail.append("CombatActions.lua: recruit Icon should be HUD talk, not GloryHog")

# items.lua ModItem: UIBegin AttackStart, no choice strip, talk icon, IsTargetableAttack
idx = items.find('id = "Jazz_PierreRecruit"')
if idx < 0:
    fail.append("items.lua: Jazz_PierreRecruit ModItem missing")
else:
    block = items[max(0, idx - 4000) : idx + 200]
    if "ShowCombatActionTargetChoice" in block:
        fail.append("items.lua: Jazz_PierreRecruit still uses ShowCombatActionTargetChoice")
    if 'Icon = "UI/Icons/Hud/talk"' not in block:
        fail.append("items.lua: Jazz_PierreRecruit Icon not HUD talk")
    if "IsTargetableAttack = true" not in block:
        fail.append("items.lua: Jazz_PierreRecruit missing IsTargetableAttack")
    if 'CombatActionAttackStart(self, units, args, "IModeCombatAttack")' not in block:
        fail.append("items.lua: Jazz_PierreRecruit UIBegin not IModeCombatAttack")

if fail:
    print("FAIL:")
    for m in fail:
        print(" ", m)
    sys.exit(1)
print("OK Pierre recruit: one hotbar button, IModeCombatAttack click target")
sys.exit(0)
