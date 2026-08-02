# Static checks for JAZZ-STRATEGY-016 squad growth + economy scale.
# Run: python docs/tools/_test_legion_squad_growth.py

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
comp = (ROOT / "Code" / "LegionSquadComposition.lua").read_text(encoding="utf-8")
gen = (ROOT / "Code" / "LegionSquadGenerator.lua").read_text(encoding="utf-8")
patrols = (ROOT / "Code" / "Guardpost_Patrols.lua").read_text(encoding="utf-8")
regions = (ROOT / "Code" / "Regions_Sectors.lua").read_text(encoding="utf-8")

assert "JAZZ_GetLegionSquadGrowthProgress" in comp, "growth progress helper missing"
assert "JAZZ_ResolveLegionRoleRecipe" in comp, "resolve recipe missing"
assert "size_early_min = 5" in comp and "patrol" in comp, "patrol early sizes missing"
assert "size_early_min = 4" in comp, "escort early sizes missing"
assert "JAZZ_ResolveLegionRoleRecipe" in gen, "generator must use resolved recipe"
assert 'or role == "shipment"' in gen or 'role == "shipment"' in gen, "logistics composition gate"
assert "lEscortUnitTemplates" in patrols, "escort template helper missing"
assert "JAZZ_LegionEconomyScalePct" in patrols, "economy scale missing"
assert "or 25" in patrols, "scale must default to 25 (÷4)"
assert 'default = 12 * const.Scale.h' in regions or "default = 12 * const.Scale.h" in regions, "CommandInterval 12h"
assert "48 * const.Scale.h" in regions, "Tax/Recruiter 48h"
assert "96 * const.Scale.h" in regions, "POI pulse 96h"
assert "48 * lHourScale()" in patrols, "combat spawn gate 48h"

# Mirror lerp early→mature for patrol at p=0 and p=1000
def lerp(a, b, p):
    return a + ((b - a) * p + 500) // 1000

assert lerp(5, 12, 0) == 5
assert lerp(8, 18, 0) == 8
assert lerp(5, 12, 1000) == 12
assert lerp(8, 18, 1000) == 18

print("OK STRATEGY-016 squad growth + economy scale static checks")
