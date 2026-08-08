# docs/tools/_insert_combat_005_pain_move.py
from pathlib import Path

p = Path("Code/Systems_Medicine.lua")
t = p.read_text(encoding="utf-8")
needle = "function JazzTraumaPainZoneTurnKey(zone, turn)"
fn = """-- JAZZ-COMBAT-005: severe armor encumbrance (FM >= 6) -> +1 Pain on first move this turn.
function JazzArmorWeightPainOnMove(unit)
	if not unit or not g_Combat then
		return false
	end
	if HasPerk(unit, "KillingWind") then
		return false
	end
	if (unit.jazz_armor_fm_penalty or 0) < 6 then
		return false
	end
	local turn = JazzTraumaCurrentTurnKey()
	if unit.jazz_armor_weight_pain_turn == turn then
		return false
	end
	if JazzAddPainStacks(unit, 1) <= 0 then
		return false
	end
	unit.jazz_armor_weight_pain_turn = turn
	return true
end

"""
if "function JazzArmorWeightPainOnMove" in t:
	print("already present")
elif needle not in t:
	raise SystemExit("anchor missing")
else:
	p.write_text(t.replace(needle, fn + needle, 1), encoding="utf-8")
	print("inserted JazzArmorWeightPainOnMove")
