# Static check: JAZZ-AI-009 FallBack peel Overwatch on vacated tile.
# Exit 0 = OK.
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
combat = (ROOT / "Code" / "CombatAI.lua").read_text(encoding="utf-8")
ctx = (ROOT / "Code" / "AIContextProfiles.lua").read_text(encoding="utf-8")
actions = (ROOT / "Code" / "AiActions.lua").read_text(encoding="utf-8")
docs = {
    "ai-awareness": (ROOT / "docs" / "technical" / "systems" / "ai-awareness.md").read_text(encoding="utf-8"),
    "override": (ROOT / "docs" / "technical" / "override-matrix.md").read_text(encoding="utf-8"),
    "wiki": (ROOT / "docs" / "wiki" / "officer-aura.md").read_text(encoding="utf-8"),
    "showcase_ru": (ROOT / "docs" / "showcase" / "ru" / "officer-aura.md").read_text(encoding="utf-8"),
    "showcase_en": (ROOT / "docs" / "showcase" / "en" / "officer-aura.md").read_text(encoding="utf-8"),
}

failed = []

for name, blob, pat in [
    ("JazzAI_CollectBreakLosSpotters", combat, r"function JazzAI_CollectBreakLosSpotters\s*\("),
    ("JazzAI_BreakLosOwMaxTiles", combat, r"function JazzAI_BreakLosOwMaxTiles\s*\("),
    ("JazzAI_BreakLosOwApCost", combat, r"function JazzAI_BreakLosOwApCost\s*\("),
    ("JazzAI_UnitCanBreakLosOverwatch", combat, r"function JazzAI_UnitCanBreakLosOverwatch\s*\("),
    ("JazzAI_DestIsBreakLosOverwatch", combat, r"function JazzAI_DestIsBreakLosOverwatch\s*\("),
    ("JazzAI_PickBestBreakLosOverwatchDest", combat, r"function JazzAI_PickBestBreakLosOverwatchDest\s*\("),
    ("JazzAI_ApplyBreakLosOverwatchDestination", combat, r"function JazzAI_ApplyBreakLosOverwatchDestination\s*\("),
    ("fallback gate", combat, r"context\.jazz_fallback"),
    ("exclude Medic", combat, r'arch_id:find\("Medic"'),
    ("exclude Deserter", combat, r'arch_id:find\("Deserter"'),
    ("exclude Melee", combat, r'arch_id:find\("Melee"'),
    ("exclude Regroup", combat, r'arch_id:find\("Regroup"'),
    ("stationed MG skip", combat, r'StationedMachineGun'),
    ("008 perch skip", combat, r"JazzAI_ContextStayIsEgressPerch"),
    ("HasVisibilityTo spotter", combat, r"HasVisibilityTo\(p, unit\)"),
    ("dest_ap vs OW cost", combat, r"ap_left < ow_cost"),
    ("farther from enemy", combat, r"stance_pos_dist\(dest, epos\) <= stance_pos_dist\(stay, epos\)"),
    ("band min", combat, r"band_min = Max\(4, ow_tiles - 4\)"),
    ("wrap after sniper hold", combat, r"dest = JazzAI_ApplySniperHoldDestination\(context, dest\)\s*\n\s*dest = JazzAI_ApplyBreakLosOverwatchDestination\(context, dest\)"),
    ("set peel anchor", combat, r"context\.jazz_break_los_ow_anchor = JazzAI_PackedDestPoint\(context\.unit_stance_pos\)"),
    ("score +220 label", combat, r'"BREAK LOS OW"'),
    ("dest bonus const", ctx, r"JazzAI_BreakLosOwDestBonus\s*=\s*220"),
    ("OW aim peel first", actions, r"context\.jazz_break_los_ow_anchor"),
    ("Disengage peel skip cover", actions, r"AIPlaceFallbackOverwatch\(unit, context\)\s*\n\s*return"),
    ("BunkerDown peel skip", actions, r"function JAZZ_AIBunkerDown[\s\S]{0,180}jazz_break_los_ow_anchor"),
]:
    if not re.search(pat, blob, re.M):
        failed.append(name)

peel_start = combat.find("function JazzAI_CollectBreakLosSpotters")
peel_end = combat.find("function JazzAI_InstallAIScoreReachableVoxelsWrap")
if peel_start < 0 or peel_end < 0 or peel_end <= peel_start:
    failed.append("peel helper span")
elif re.search(r"GetLoFData", combat[peel_start:peel_end]):
    failed.append("009 helpers must not call GetLoFData")

ow_fn = actions.find("function JazzAI_FallbackOverwatchTargetPos")
ow_end = actions.find("function AIPlaceFallbackOverwatch")
if ow_fn < 0 or ow_end <= ow_fn:
    failed.append("FallbackOverwatchTargetPos span")
elif "jazz_break_los_ow_anchor" not in actions[ow_fn:ow_end]:
    failed.append("Fallback OW must prefer peel anchor")

for key, needle in [
    ("ai-awareness", "JAZZ-AI-009"),
    ("override", "JAZZ-AI-009"),
    ("wiki", "оторваться из обзора"),
    ("showcase_ru", "клетку, которую бросил"),
    ("showcase_en", "tile they vacated"),
]:
    if needle not in docs[key]:
        failed.append(f"docs {key}")

if failed:
    print("FAIL JAZZ-AI-009:", ", ".join(failed))
    sys.exit(1)
print("OK JAZZ-AI-009 static")
sys.exit(0)
