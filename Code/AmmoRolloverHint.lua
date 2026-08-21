translatedModifications = {
	["Damage"]  = T(287944595070, "Damage"),	
    ["ObjDamageMod"]  = T(28794459507035, "Урон по объектам"),	
    ["OverwatchAngle"]  = T(608975559432, "Overwatch Width"),	
    ["WeaponRange"]  = T(890000000000402, "WeaponRange"),
    ["AimAccuracy"]  = T(126266115368, "Aiming Bonus"),	
    ["PenetrationClass"]  = T(528512796972, "Penetration"),	
    ["BuckshotProjectiles"] = T(890000000001385, "Дробь"),
    ["AutoShots"]  = T(890000000001385, "Дробь"), -- legacy alias; 12g mods use BuckshotProjectiles
    ["CritChance"]  = T(711037452737, "Crit chance"),	
    ["Reliability"]  = T(754196064298, "Reliability"),	
    ["Recoil"]  = T(287944595070111, "Отдача"),	
    ["BulletDropRange"]  = T(890000000001384, "Настильность"),
    ["Grouping"]  = T(890000000001386, "Кучность"),
    ["BaseJamChance"]  = T(890000000001387, "Шанс клина"),
    ["PenetrationBonus"]  = T(890000000001399, "Бонус пробития"),	
    
}

-- Ammo AppliedEffects often concatenate several status ids into one string
-- (e.g. "ExposedMarkedTraccers"). Longest-first so BleedingChance > Bleeding.
local JazzAmmoEffectTokens = {
	"BleedingChance",
	"MarkedTraccers",
	"Exposed",
	"Burning",
	"Bleeding",
}

function JazzExpandAmmoAppliedEffect(compound)
	if type(compound) ~= "string" or compound == "" then
		return empty_table
	end
	if g_Classes and g_Classes[compound] then
		return { compound }
	end
	local out, s = {}, compound
	while s ~= "" do
		local matched
		for _, tok in ipairs(JazzAmmoEffectTokens) do
			if string.sub(s, 1, #tok) == tok then
				out[#out + 1] = tok
				s = string.sub(s, #tok + 1)
				matched = true
				break
			end
		end
		if not matched then
			break
		end
	end
	return out
end

function JazzAmmoHasAppliedEffect(ammo, effect_id)
	if not ammo or not effect_id then
		return false
	end
	for _, compound in ipairs(ammo.AppliedEffects or empty_table) do
		if compound == effect_id then
			return true
		end
		for _, tok in ipairs(JazzExpandAmmoAppliedEffect(compound)) do
			if tok == effect_id then
				return true
			end
		end
	end
	return false
end

-- Ammo pen UI: work in integer tenths, never put a Lua float into T{} <number>
-- (JA3 truncates toward zero → 0.9 shows as 0). See skill jazz-penetration-scales.
function FormatAmmoPenetrationDisplay(mod_mul, mod_add)
	local mul = mod_mul
	if mul == nil then
		mul = 1000
	end
	-- tenths: mod_mul 1000 → 10 (=1.0), bonus +2 → +2 tenths (=0.2)
	local tenths = DivRound(mul, 100) + (mod_add or 0)
	local sign = ""
	if tenths < 0 then
		sign = "-"
		tenths = -tenths
	end
	local whole = floatfloor(tenths / 10)
	local frac = tenths - whole * 10
	return sign .. whole .. "." .. frac
end

function FormatWeaponPenetrationDisplay(weapon)
	if not weapon then
		return "0.0"
	end
	local class = 1
	if weapon.HasMember and weapon:HasMember("PenetrationClass") then
		class = weapon.PenetrationClass or 1
	elseif weapon.PenetrationClass then
		class = weapon.PenetrationClass
	end
	local bonus = 0
	if weapon.HasMember and weapon:HasMember("PenetrationBonus") then
		bonus = weapon.PenetrationBonus or 0
	elseif weapon.PenetrationBonus then
		bonus = weapon.PenetrationBonus
	end
	return FormatAmmoPenetrationDisplay((class or 1) * 1000, bonus or 0)
end

function Ammo:GetRolloverHint()
	local hint = {} 	
	local penbonus = 0
	local pen_mul = nil
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
			pen_mul = val.mod_mul
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

	if penname ~= "" then
		hint[#hint + 1] = T{
			890000000001388,
			"\n<bullet_point> <target_prop>: <pen>",
			target_prop = Untranslated(penname),
			pen = Untranslated(FormatAmmoPenetrationDisplay(pen_mul, penbonus)),
		}
	end

	local effects = {}
	local seen = {}
	for _, compound in sorted_pairs(self.AppliedEffects) do
		for _, effect_id in ipairs(JazzExpandAmmoAppliedEffect(compound)) do
			if not seen[effect_id] then
				seen[effect_id] = true
				local cls = g_Classes and g_Classes[effect_id]
				local name = cls and cls.DisplayName
				if name and name ~= "" then
					effects[#effects + 1] = name
				end
			end
		end
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
