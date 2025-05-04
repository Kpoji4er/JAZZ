
translatedModifications = {
	["Damage"]  = T(287944595070, "Damage"),	
    ["ObjDamageMod"]  = T(28794459507035, "Урон по объектам"),	
    ["OverwatchAngle"]  = T(608975559432, "Overwatch Width"),	
    ["WeaponRange"]  = T(353401714895, "WeaponRange"),	
    ["AimAccuracy"]  = T(126266115368, "Aiming Bonus"),	
    ["PenetrationClass"]  = T(528512796972, "Penetration"),	
    ["AutoShots"]  = T(287944595070112, "Дробь"),	
    ["CritChance"]  = T(711037452737, "Crit chance"),	
    ["Reliability"]  = T(754196064298, "Reliability"),	
    ["Recoil"]  = T(287944595070111, "Отдача"),	
    ["BulletDropRange"]  = T(287944595070112, "Настильность"),	
    ["Grouping"]  = T(287944595070113, "Кучность"),	
    ["BaseJamChance"]  = T(287944595070113, "Шанс клина"),	
    ["PenetrationBonus"]  = T(28794459507011311, "Бонус пробития"),	
    
}

function Ammo:GetRolloverHint()
	local hint = {} 	
	local parts = {}

	for part,val in sorted_pairs(self.Modifications) do

     --   print(val)
       -- local preset = Presets.WeaponPropertyDef.Default[val.target_prop]
       local mod_mul = ""
       local mod_add = ""
       local target_prop = val.target_prop
       local meta = g_Classes.Firearm:GetPropertyMetadata(target_prop)
       local name = meta.name


    --   for i,def in sorted_pairs(Presets.WeaponPropertyDef.Default) do
    --    print(def)
    --    if target_prop == def.id then 
    --        target_prop = def.display_name
    --    end
    --   end

        local target_prop = translatedModifications[target_prop] or target_prop




        if val.mod_add and val.mod_add > 0 then mod_add = mod_add.."+"..val.mod_add end
        if val.mod_add and val.mod_add < 0 then mod_add = mod_add.."-"..(-val.mod_add) end
        if val.mod_mul and val.mod_mul ~= 1000 and val.mod_mul ~= 0 then 
            mod_mul = "*"..((val.mod_mul + .0) / 1000)        
        end
        if val.mod_add and val.mod_mull then mod_add = "("..mod_add..")" end
       -- print(preset)
		--local preset= Presets.TargetBodyPart.Default[part]

       if target_prop == translatedModifications["BaseJamChance"] then mod_add = "+0.0"..val.mod_add.."%" end
     
        if val.mod_add ~= 0 or (val.mod_mull ~= 1000 and val.mod_mul ~= 0) then
        hint[#hint+1] = T{378508273050111, "<bullet_point> <target_prop>: <mod_add> <mod_mul>",target_prop = target_prop, mod_add = mod_add, mod_mul = mod_mul}
        end
		--parts[#parts+1] = val.target_prop
	end

    local effects = {} 
	for effect,val in sorted_pairs(self.AppliedEffects) do

 --       print(val)
 --       local preset= Presets.CharacterEffect.Default[part]
 --       print(preset.display_name)

        effects[#effects+1] = g_Classes[val].DisplayName
      --  local effect = self:GetStatusEffect(val)


	end
        if effects[1] then
       hint[#hint+1] = T{378508273050111, "\n<bullet_point> Эффекты при попадании: <effects>", effects = table.concat(effects, ", ")}
        end
	--hint[#hint+1] = T{378508273050111, "<bullet_point> Body parts - <parts>", parts = table.concat(parts, ", ")}
	--hint[#hint+1] = self.AdditionalHint or ""
	return table.concat(hint, "\n")
end	