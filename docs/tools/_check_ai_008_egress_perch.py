# Static check: JAZZ-AI-008 egress perch hold.
# Exit 0 = OK.
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
combat = (ROOT / "Code" / "CombatAI.lua").read_text(encoding="utf-8")
ctx = (ROOT / "Code" / "AIContextProfiles.lua").read_text(encoding="utf-8")
actions = (ROOT / "Code" / "AiActions.lua").read_text(encoding="utf-8")

failed = []

for name, blob, pat in [
    ("JazzAI_UnitIsLinePerchHolder", combat, r"function JazzAI_UnitIsLinePerchHolder\s*\("),
    ("JazzAI_DestIsEgressPerch", combat, r"function JazzAI_DestIsEgressPerch\s*\("),
    ("JazzAI_ContextStayIsEgressPerch", combat, r"function JazzAI_ContextStayIsEgressPerch\s*\("),
    ("perch stay hold", combat, r"stay_score > 0 or perch"),
    ("useless skip on perch", combat, r"stay_score <= 0 and not perch"),
    ("Frontliner keyword", combat, r'arch_id:find\("Frontliner"'),
    ("exclude Assaulter", combat, r'arch_id:find\("Assaulter"'),
    ("HasLosToPos global", actions, r"^function JazzAI_HasLosToPos\s*\("),
    ("DestSeesPos", actions, r"^function JazzAI_DestSeesPos\s*\("),
    ("Fallback OW pos global", actions, r"^function JazzAI_FallbackOverwatchTargetPos\s*\("),
    ("stay bonus const", ctx, r"JazzAI_EgressPerchStayBonus\s*=\s*180"),
    ("ScoreRecontact perch", ctx, r"JazzAI_ContextStayIsEgressPerch"),
    ("EGRESS PERCH details", combat, r'"EGRESS PERCH"'),
]:
    if not re.search(pat, blob, re.M):
        failed.append(name)

if re.search(r"GetLoFData", combat[combat.find("function JazzAI_DestIsEgressPerch"):
        combat.find("function JazzAI_ContextStayIsEgressPerch")]):
    failed.append("DestIsEgressPerch must not call GetLoFData")

if failed:
    print("FAIL JAZZ-AI-008:", ", ".join(failed))
    sys.exit(1)
print("OK JAZZ-AI-008 static")
sys.exit(0)
