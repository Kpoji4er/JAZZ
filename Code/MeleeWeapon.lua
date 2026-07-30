-- JAZZ-COMBAT-002: thrown knives/melee ranged — never inherit C++ smoke LoF grazing.

local MeleeWeapon_GetAttackResults_Vanilla = MeleeWeapon.GetAttackResults

function MeleeWeapon:GetAttackResults(action, attack_args)
	local restore
	if action and action.ActionType == "Ranged Attack" then
		restore = GetLoFData
		GetLoFData = function(attacker, targets, params)
			if params then
				params = table.copy(params)
				params.ignore_smoke = true
			end
			return restore(attacker, targets, params)
		end
	end

	local ok, results = pcall(MeleeWeapon_GetAttackResults_Vanilla, self, action, attack_args)
	if restore then
		GetLoFData = restore
	end
	if not ok then
		error(results)
	end
	return results
end
