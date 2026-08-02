# Static checks for JAZZ-STRATEGY-019 global spawn pool + logistics delay.
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
patrols = (ROOT / "Code" / "Guardpost_Patrols.lua").read_text(encoding="utf-8")

assert "lCanConsumeGlobalSpawn" in patrols
assert "lConsumeGlobalSpawn" in patrols
assert "lGlobalSpawnSlotCap" in patrols
assert "lLogisticsOpen" in patrols
assert "logistics_open_at" in patrols
assert "72 * lHourScale()" in patrols
assert "global_spawn" in patrols
assert "lCanConsumeGlobalSpawn(root)" in patrols

# Command window order: tax → recruiter → combat → supply
start = patrols.find("local function lRunCommandWindow")
end = patrols.find("local function lParalyzeOutpost", start)
assert start > 0 and end > start
window = patrols[start:end]
tax_pos = window.find("lTryTaxCollector(root, region, region_state, outpost)")
recruiter_pos = window.find("lTryRecruiter(root, region, region_state, outpost)")
patrol_pos = window.find('lSpawnRegularRole(root, region, region_state, outpost, "patrol")')
supply_pos = window.find("lTrySupplyConvoy(root, region, region_state, outpost)")
assert 0 <= tax_pos < recruiter_pos < patrol_pos < supply_pos, (
	"command window must be tax → recruiter → combat → supply"
)

print("OK STRATEGY-019 global spawn pool + logistics delay static checks")
