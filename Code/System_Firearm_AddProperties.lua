FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Autofire",
    id = "Recoil",
    name = "Recoil",
    help = "Падение CTH на каждый последующий выстрел в очереди",
    editor = "number",
    default = 100,
    template = true,
    min = 0,
    max = 100,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "MaxAimActions",
    name = "Max Aim Actions",
    help = "Количество кликов прицеливания",
    editor = "number",
    template = true,
    min = 0,
    max = 10,
    modifiable = true
}


FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "Caliber",
    id = "BoltingAP",
    name = "BoltingAP",
    help = "Количество ОД на передергивание затвора",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 1,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    id = "Bolted",
    name = "Bolted",
    editor = "bool",
    default = false,
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Autofire",
    id = "BurstShots",
    name = "BurstShots",
    help = "Количество патрон в короткой очереди",
    editor = "number",
    default = 3,
    template = true,
    min = 0,
    max = 20,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System - Autofire",
    id = "AutoShots",
    name = "AutoShots",
    help = "Количество патрон в длинной очереди",
    editor = "number",
    default = 10,
    template = true,
    min = 0,
    max = 25,
    modifiable = true
}
--deprecated
--FirearmProperties.properties[#FirearmProperties.properties+1] = {
--    category = "New Weapon System",
--    id = "EffectiveRange",
--    name = "EffectiveRange",
--    help = "Расстояние 100% точности",
--    editor = "number",
--    default = 0,
--    template = true,
--    min = -10,
--    max = 50,
--    modifiable = true
--}

--FirearmProperties.properties[#FirearmProperties.properties+1] = {
--    category = "New Weapon System",
--    id = "Deterioration",
--    name = "Deterioration",
--    help = "Уровень износа",
--    editor = "number",
--    default = 0,
--    template = false,
--    min = 0,
--    max = 100,
--    modifiable = false
--}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "OverwatchAngle",
    name = "Overwatch Angle",
    help = "overwatch area cone angle",
    editor = "number",
    default = 2400,
    template = true,
    scale = "deg",
    slider = true,
    min = 1,
    max = 5400,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "Handling",
    name = "Handling",
    help = "Эргономика",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 120,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "BulletDropRange",
    name = "Bullet Drop Range",
    help = "Дальность падения пули",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 100,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "Grouping",
    name = "Grouping",
    help = "Кучность",
    editor = "number",
    default = 0,
    template = true,
    min = 0,
    max = 1000,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "BaseJamChance",
    name = "Jam Chance",
    help = "Базовый шанс клина (1 = 1/100)",
    editor = "number",
    default = 0,
    template = true,
    min = -100,
    max = 100,
    modifiable = true
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon System",
    id = "PenetrationBonus",
    name = "Penetration Bonus",
    help = "Бонус к пробитию брони",
    editor = "number",
    default = 0,
    template = true,
    min = -100,
    max = 100,
    modifiable = true
}

WeaponComponent.properties[#WeaponComponent.properties+1] = {
    category = "Scope Visuals",
    id = "ReticleInner",
    name = "Reticle Inner",
    help = "Сетка прицела",
    editor = "ui_image",
    template = true,
    default =  "",
    image_preview_size = 75
}

WeaponComponent.properties[#WeaponComponent.properties+1] = {
    category = "Scope Visuals",
    id = "ReticleInnerSub",
    name = "Reticle Inner (Sub)",
    help = "Сетка прицела (для доп прицела)",
    editor = "ui_image",
    template = true,
    default =  "",
    image_preview_size = 75
}

WeaponComponent.properties[#WeaponComponent.properties+1] = {
    category = "Scope Visuals",
    id = "ReticleOuter",
    name = "Reticle Outer",
    help = "Обводка прицела",
    editor = "ui_image",
    default = 0,
    template = true,
    default =  "",
    image_preview_size = 75
}

FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon Condition",
    id = "WeaponResource",
    name = "Weapon Resource",
    help = "Ресурс оружия",
    editor = "number",
    default = 1000,
    template = true,
    min = 0,
    max = 50000,
    modifiable = true
}


FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon Condition",
    id = "WeaponResourceMax",
    name = "Weapon Resource",
    help = "Ресурс оружия Макс",
    editor = "number",
    default = -1,
    template = false,
    min = -1,
    max = 50000,
    modifiable = true
}
FirearmProperties.properties[#FirearmProperties.properties+1] = {
    category = "New Weapon Condition",
    id = "DegradePerShot",
    name = "Degrade per shot",
    help = "Деградация за выстрел",
    editor = "number",
    default = 1,
    template = true,
    min = 1,
    max = 10,
    modifiable = true
}


WeaponComponentVisual.properties[#WeaponComponentVisual.properties+1] = {
    id = "WeaponName",
    name = "Weapon Name",
    help = "Изменение названия оружия",
    editor = "text",
    default = "",
}

WeaponComponentVisual.properties[#WeaponComponentVisual.properties+1] = {
    id = "WeaponIconMod",
    name = "WeaponIcon Mod",
    help = "Доп иконка модификации",
    editor = "ui_image",
    default = 0,
    template = true,
    default =  "",
    image_preview_size = 75
}






function FirearmBase:GetFactoryResource()
	return InventoryItemDefs[self.class]:GetProperty("WeaponResource") or 1000
end

function FirearmBase:GetMaxResource()
    local WeaponResourceMax = 0
    if self.WeaponResourceMax and self.WeaponResourceMax >= 0 then
        WeaponResourceMax = self.WeaponResourceMax
    else
        WeaponResourceMax = self:GetFactoryResource()
    end
	return WeaponResourceMax 
end

function FirearmBase:GetCurrentResource()
	return self.WeaponResource or self:GetFactoryResource()
end




--Add property to weapon modification menu
function GetWeaponModifyProperties(item)		
	local statList = {}
	local dmgPreset = Presets.WeaponPropertyDef.Default.Damage
	statList[#statList + 1] = { max = dmgPreset.max_progress, bind_to = dmgPreset.bind_to }
	
	local baseAttack = item:GetBaseAttack(false, "force")
	local baseAction = CombatActions[baseAttack]
	local baseAttackPreset = Presets.WeaponPropertyDef.Default.ShootAP
	statList[#statList + 1] = { 
		GetShootAP = function(it)
			return baseAttackPreset:GetProp(it or item)/const.Scale.AP
		end,
		Getbase_ShootAP = function(it)
			return baseAttackPreset:Getbase_Prop(it or item)/const.Scale.AP
		end,
		max = 10,
		display_name = T{310685041358, "Attack Cost (<Name>)", Name = baseAction.DisplayNameShort or baseAction.DisplayName},
		id = "ShootAP",
		reverse_bar = true,
		description = baseAttackPreset.description
	}

	local rangePreset = Presets.WeaponPropertyDef.Default.WeaponRange
	statList[#statList + 1] = { max = rangePreset.max_progress, bind_to = rangePreset.bind_to }

	local GroupingPreset = Presets.WeaponPropertyDef.Default.Grouping
	statList[#statList + 1] = { max = GroupingPreset.max_progress, bind_to = GroupingPreset.bind_to }

	local HandlingPreset = Presets.WeaponPropertyDef.Default.Handling
	statList[#statList + 1] = { max = HandlingPreset.max_progress, bind_to = HandlingPreset.bind_to }

    if (item.BulletDropRange > 0) then
    local effRange = Presets.WeaponPropertyDef.Default.BulletDropRange
	statList[#statList + 1] = { max = effRange.max_progress, bind_to = effRange.bind_to } 
    end

  --  print(item.AvailableAttacks)

    local aimAcc = Presets.WeaponPropertyDef.Default.AimAccuracy
    statList[#statList + 1] = { max = aimAcc.max_progress, bind_to = aimAcc.bind_to }

    local MaxAimActions = Presets.WeaponPropertyDef.Default.MaxAimActions
    statList[#statList + 1] = { max = MaxAimActions.max_progress, bind_to = MaxAimActions.bind_to }

	local critPreset = item.owner and Presets.WeaponPropertyDef.Default.CritChance or Presets.WeaponPropertyDef.Default.MaxCritChance
	local weaponModDlg = GetDialog("ModifyWeaponDlg").idModifyDialog
	local crit = 0
	local unit_id = weaponModDlg.context.owner
	statList[#statList + 1] = {
		GetCritChance = function(it)
			return critPreset:GetProp(it or item, unit_id )
		end,
		Getbase_CritChance = function(it)
			return critPreset:Getbase_Prop(it or item, unit_id )
		end,
		max = critPreset.max_progress,
		display_name = critPreset.display_name,
		id = "CritChance",
		description = critPreset.description
	}


    --print('baseAction')
    --print(baseAttackPreset.description)
    if ((baseAction.id == "AutoFire") or (baseAction.id == "BurstFire") or (baseAction.id == "MGBurstFire"))
    then
    local recoil = Presets.WeaponPropertyDef.Default.Recoil
	statList[#statList + 1] = { max = recoil.max_progress, bind_to = recoil.bind_to }
	local BurstShots = Presets.WeaponPropertyDef.Default.BurstShots
	statList[#statList + 1] = { max = BurstShots.max_progress, bind_to = BurstShots.bind_to }
    end

  --  if (("AutoFire" in ipairs item.AvailableAttacks)) then

    for i,v in ipairs(item.AvailableAttacks) do
     --print(i..": "..v)
     if v == "AutoFire" then 
        --print (v)
    	local AutoShots = Presets.WeaponPropertyDef.Default.AutoShots
	    statList[#statList + 1] = { max = AutoShots.max_progress, bind_to = AutoShots.bind_to }
        end
     end


 --   end
    
--  local OverwatchAngle = Presets.WeaponPropertyDef.Default.OverwatchAngle
--	statList[#statList + 1] = { max = rangePreset.max_progress, bind_to = OverwatchAngle.bind_to }

--  local BuckshotConeAngle = Presets.WeaponPropertyDef.Default.BuckshotConeAngle
--	statList[#statList + 1] = { max = rangePreset.max_progress, bind_to = BuckshotConeAngle.bind_to }

    local Reliability = Presets.WeaponPropertyDef.Default.Reliability
	statList[#statList + 1] = { max = Reliability.max_progress, bind_to = Reliability.bind_to }

    local Noise = Presets.WeaponPropertyDef.Default.Noise
	statList[#statList + 1] = { max = Noise.max_progress, bind_to = Noise.bind_to }

	return statList
end

--[[
function GetWeaponComponentDescription(componentPreset)
	local data = GetWeaponComponentDescriptionData(componentPreset)
	local lines = {}

    local headerText = _InternalTranslate(
        T{987654321, "<style WeaponModHeader><display_name></style>", componentPreset}
      )
      table.insert(lines, { display = Untranslated(headerText) })

	if componentPreset.Description then
		lines[#lines + 1] = T{componentPreset.Description, componentPreset}
	end
	
	local indices = {}
	for modName, mod in sorted_pairs(data) do
		local text = Untranslated("<bullet_point> " .. _InternalTranslate(mod.display, mod))
		lines[#lines + 1] = text
		
		local effect = WeaponComponentEffects[modName]
		if effect then
			indices[text] = effect.SortKey
		end
	end
	
	if #lines == 0 then
		return T(575725466022, "No changes")
	end
	
	table.sort(lines, function(a, b)
		local indexA = indices[a] or 0
		local indexB = indices[b] or 0
		return indexA < indexB
	end)
	
	return table.concat(lines, "\n"), data
end
]]
