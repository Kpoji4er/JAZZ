



---
--- Gets the initial maximum hit points for the unit.
---
--- If the unit is a villain, the maximum hit points are modified by the `const.Combat.LieutenantHpMod` constant. Otherwise, the maximum hit points are the unit's `Health` property.
--- If the unit has the "BeefedUp" perk, the maximum hit points are further increased by the bonus specified in the `CharacterEffectDefs.BeefedUp:ResolveValue("bonus_health")` value.
---
--- @return number The initial maximum hit points for the unit.
---
function UnitProperties:GetInitialMaxHitPoints()
	-- Vanilla uses 100% Health. JAZZ briefly used 75% + CombatStart grit (~25% Temp HP);
	-- MED-001 removed grit — restore full Health so Max HP is not left 25% short.
	local mod = self:GetProperty("villain") and const.Combat.LieutenantHpMod or 100
	local maxhp = MulDivRound(self:GetProperty("Health"), mod, 100)
	if HasPerk(self, "BeefedUp") then
		maxhp = MulDivRound(maxhp, 100 + CharacterEffectDefs.BeefedUp:ResolveValue("bonus_health"), 100)
	end
	return maxhp
end

--- Bump Max/current HP after restoring 100% Health base (old saves still had 75% MaxHitPoints).
local function JazzRecalcHiredMercMaxHp()
	if type(RecalcMaxHitPoints) ~= "function" or type(gv_UnitData) ~= "table" then
		return
	end
	for _, ud in sorted_pairs(gv_UnitData) do
		if ud and IsMerc(ud) and (ud.HireStatus == "Hired" or ud.Squad) then
			RecalcMaxHitPoints(ud)
			local u = g_Units and ud.session_id and g_Units[ud.session_id]
			if u then
				RecalcMaxHitPoints(u)
			end
		end
	end
end

function OnMsg.LoadGame()
	JazzRecalcHiredMercMaxHp()
end

function OnMsg.NewGame()
	JazzRecalcHiredMercMaxHp()
end
