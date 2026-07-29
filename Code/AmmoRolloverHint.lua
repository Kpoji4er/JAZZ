translatedModifications = {
	["Damage"]  = T(287944595070, "Damage"),	
    ["ObjDamageMod"]  = T(28794459507035, "Урон по объектам"),	
    ["OverwatchAngle"]  = T(608975559432, "Overwatch Width"),	
    ["WeaponRange"]  = T(890000000000402, "WeaponRange"),
    ["AimAccuracy"]  = T(126266115368, "Aiming Bonus"),	
    ["PenetrationClass"]  = T(528512796972, "Penetration"),	
    ["AutoShots"]  = T(890000000001385, "Дробь"),
    ["CritChance"]  = T(711037452737, "Crit chance"),	
    ["Reliability"]  = T(754196064298, "Reliability"),	
    ["Recoil"]  = T(287944595070111, "Отдача"),	
    ["BulletDropRange"]  = T(890000000001384, "Настильность"),
    ["Grouping"]  = T(890000000001386, "Кучность"),
    ["BaseJamChance"]  = T(890000000001387, "Шанс клина"),
    ["PenetrationBonus"]  = T(890000000001399, "Бонус пробития"),	
    
}

function Ammo:GetRolloverHint()
	local hint = {} 	
	local penbonus = 0
	local pen = 0
	local penname = ""

	for _, val in sorted_pairs(self.Modifications) do
		local mod_mul = ""
		local mod_add = ""
		local target_prop = val.target_prop
		local display_prop = translatedModifications[target_prop] or target_prop
		local skip = false

		if val.mod_add and val.mod_add > 0 then
			mod_add = "+" .. val.mod_add
		elseif val.mod_add and val.mod_add < 0 then
			mod_add = "-" .. (-val.mod_add)
		end
		if val.mod_mul and val.mod_mul ~= 1000 and val.mod_mul ~= 0 then
			mod_mul = " " .. DivRound(val.mod_mul, 10) .. "% "
		end

		-- BaseJamChance is JamScore units (0..1000); display as % via /10.
		if target_prop == "BaseJamChance" then
			mod_add = (val.mod_add >= 0 and "+" or "") .. DivRound(val.mod_add, 10) .. "%"
		end
		if target_prop == "CritChance" then
			mod_add = (val.mod_add >= 0 and "+" or "") .. val.mod_add .. "%"
		end
		if target_prop == "PenetrationBonus" then
			penbonus = val.mod_add or 0
			skip = true
		end
		if target_prop == "PenetrationClass" then
			-- CaliberModification: 1000 = ×1. Display class as mod_mul/1000 (e.g. 2000 → 2.0).
			pen = ((val.mod_mul or 1000) + 0.0) / 1000
			penname = Untranslated(display_prop)
			skip = true
		end

		local has_mul = val.mod_mul and val.mod_mul ~= 1000 and val.mod_mul ~= 0
		if (val.mod_add ~= 0 or has_mul) and not skip then
			hint[#hint + 1] = T{
				890000000001390,
				"<bullet_point> <target_prop>: <mod_add> <mod_mul>",
				target_prop = Untranslated(display_prop),
				mod_add = Untranslated(mod_add),
				mod_mul = Untranslated(mod_mul),
			}
		end
	end

	-- Combined pen: class + tenths from PenetrationBonus (e.g. 2.0 + 2 → 2.2).
	if penname ~= "" then
		local display_pen = pen + penbonus * 0.1
		display_pen = floatfloor(display_pen * 10 + (display_pen >= 0 and 0.5 or -0.5)) / 10
		hint[#hint + 1] = T{
			890000000001388,
			"\n<bullet_point> <target_prop>: <pen>",
			target_prop = Untranslated(penname),
			pen = display_pen,
		}
	end

	local effects = {}
	for _, val in sorted_pairs(self.AppliedEffects) do
		effects[#effects + 1] = g_Classes[val].DisplayName
	end
	if effects[1] then
		hint[#hint + 1] = T{
			890000000001389,
			"\n<bullet_point> Эффекты при попадании: <effects>",
			effects = table.concat(effects, ", "),
		}
	end

	return table.concat(hint, "\n")
end
