

		

---
--- Gets the initial maximum hit points for the unit.
---
--- If the unit is a villain, the maximum hit points are modified by the `const.Combat.LieutenantHpMod` constant. Otherwise, the maximum hit points are the unit's `Health` property.
--- If the unit has the "BeefedUp" perk, the maximum hit points are further increased by the bonus specified in the `CharacterEffectDefs.BeefedUp:ResolveValue("bonus_health")` value.
---
--- @return number The initial maximum hit points for the unit.
---
function UnitProperties:GetInitialMaxHitPoints()
	local mod = self:GetProperty("villain") and const.Combat.LieutenantHpMod or 75
	local maxhp = MulDivRound(self:GetProperty("Health"), mod, 100)
	if HasPerk(self, "BeefedUp") then
		maxhp = MulDivRound(maxhp, 100 + CharacterEffectDefs.BeefedUp:ResolveValue("bonus_health"), 100)
	end
	return maxhp
end
