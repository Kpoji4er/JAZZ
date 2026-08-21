# Static smoke for JAZZ-STRATEGY-024 support compositions.
# Run from jazz/: python docs/tools/_check_legion_support_024.py

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def must(cond: bool, msg: str, fails: list[str]) -> None:
    if not cond:
        fails.append(msg)


def main() -> int:
    fails: list[str] = []
    comp = read(ROOT / "Code" / "LegionSquadComposition.lua")
    gen = read(ROOT / "Code" / "LegionSquadGenerator.lua")
    dir_lua = read(ROOT / "Code" / "Guardpost_Patrols.lua")
    regions = read(ROOT / "Code" / "Regions_Sectors.lua")

    must("support = {" in comp, "recipe support missing", fails)
    must('tier_bias = "specialty"' in comp, "specialty bias missing", fails)
    must("JAZZ_LegionSupportArchetypes" in comp, "archetypes table missing", fails)
    must("sniper" in comp and "mortar" in comp and "mg =" in comp, "archetype keys missing", fails)

    must("lTryBuildSupport" in gen, "builder missing", fails)
    must("lCollectSupportSpecialists" in gen, "mixed specialist pool missing", fails)
    must('support_archetype = "mixed"' in gen, "mixed archetype stamp missing", fails)
    must("lPickSupportArchetype" not in gen, "mono-archetype picker still present", fails)
    must('recipe_role == "support"' in gen, "generator branch missing", fails)
    must('or role == "support"' in gen, "UsesCompositionGenerator missing support", fails)

    must("support = true" in dir_lua, "regular role missing", fails)
    must("legion/legion_SUPPORT_squad.png" in dir_lua, "icon path missing", fails)
    must("lSupportTarget" in dir_lua, "support target missing", fails)
    must('lSpawnRegularRole(root, region, region_state, outpost, "support")' in dir_lua, "spawn order missing", fails)
    must("SupportCap" in dir_lua and "SupportCost" in dir_lua, "cap/cost maps missing", fails)

    must('id = "SupportCap"' in regions, "Region SupportCap missing", fails)
    must('id = "SupportCost"' in regions, "Region SupportCost missing", fails)
    must('id = "SupportMissions"' in regions, "Region SupportMissions missing", fails)

    icon = ROOT / "SquadsIcons" / "Enemy" / "legion" / "legion_SUPPORT_squad.png"
    must(icon.is_file(), "legion SUPPORT icon missing", fails)
    for faction in ("army", "adonis", "rebels", "smugglers"):
        must(
            (ROOT / "SquadsIcons" / "Enemy" / faction / f"{faction}_SUPPORT_squad.png").is_file(),
            f"{faction} SUPPORT icon missing",
            fails,
        )

    ru = read(ROOT / "Russian.csv")
    en = read(ROOT / "English.csv")
    for lid in ("890000000001651", "890000000001652", "890000000001653"):
        must(lid in ru, f"RU missing {lid}", fails)
        must(lid in en, f"EN missing {lid}", fails)

    # Size band: early == mature 4..7
    m = re.search(r"support\s*=\s*\{([^}]+)\}", comp, re.S)
    must(bool(m), "cannot parse support recipe block", fails)
    if m:
        block = m.group(1)
        must("size_min = 4" in block and "size_max = 7" in block, "support size not 4-7", fails)
        must("size_early_min = 4" in block and "size_early_max = 7" in block, "support early size not fixed 4-7", fails)

    if fails:
        print("FAIL STRATEGY-024 static:")
        for f in fails:
            print(" -", f)
        return 1
    print("OK STRATEGY-024 static checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
