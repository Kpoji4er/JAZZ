# Static check: JAZZ-AI-SNIPER-001 ExtremeRange + sniper hold + soft HighGround decay.
# Exit 0 = OK.
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
combat = (ROOT / "Code" / "CombatAI.lua").read_text(encoding="utf-8")
ctx = (ROOT / "Code" / "AIContextProfiles.lua").read_text(encoding="utf-8")

failed = []

if not re.search(
    r'context\.ExtremeRange\s*=\s*IsKindOf\(weapon,\s*"Firearm"\)\s*and\s*\(weapon\.WeaponRange',
    combat,
):
    failed.append("ExtremeRange from WeaponRange")

m = re.search(r"context\.ExtremeRange\s*=([^\n]+)", combat)
if m and "WeaponRange" not in m.group(1) and "EffectiveRange" in m.group(1):
    failed.append("ExtremeRange collapsed to EffectiveRange only")

for name, blob, pat in [
    ("JazzAI_ApplySniperHoldDestination", combat, r"function JazzAI_ApplySniperHoldDestination\s*\("),
    ("JazzAI_SniperHighGroundWeightPct", combat, r"function JazzAI_SniperHighGroundWeightPct\s*\("),
    ("JazzAI_SniperStayUselessPenalty", combat, r"function JazzAI_SniperStayUselessPenalty\s*\("),
    ("JazzAI_ApplySniperUselessBiasToContext", combat, r"function JazzAI_ApplySniperUselessBiasToContext\s*\("),
    ("HighGround pct in AIScoreDest", combat, r"jazz_sniper_highground_pct"),
    ("AIPolicyHighGround mul", combat, r'IsKindOf\(policy,\s*"AIPolicyHighGround"\)'),
    ("SNIPER USELESS STAY", combat, r"SNIPER USELESS STAY"),
    ("wrap install", combat, r"JazzAI_InstallAIScoreReachableVoxelsWrap"),
    ("MapVar SniperUselessStreak", ctx, r'MapVar\(\s*"JazzAI_SniperUselessStreak"'),
    ("CombatStart clear streak", ctx, r"JazzAI_SniperUselessStreak\s*=\s*\{\}"),
]:
    if not re.search(pat, blob):
        failed.append(name)

if "JazzAI_PickSniperEscapeDest" in combat:
    failed.append("hard PickSniperEscapeDest should be removed")

if 'k == "Sniper"' not in combat or 'k == "Marksman"' not in combat:
    failed.append("Sniper/Marksman keywords")

if failed:
    print("FAIL JAZZ-AI-SNIPER-001:", ", ".join(failed))
    sys.exit(1)
print("OK JAZZ-AI-SNIPER-001 static")
sys.exit(0)
