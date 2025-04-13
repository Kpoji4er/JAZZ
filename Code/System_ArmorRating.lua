DefineClass.ArmorPlates = {
	__parents = { "Armor"},
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "Coverage",
    name = "Coverage percent",
    help = "% защиты",
    editor = "number",
    default = 100,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "ArmorRating",
    name = "Armor Rating",
    help = "Снижение урона при 100% состоянии при попадании пули соответсвующего класса",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "MeleeArmorRating",
    name = "Melee Armor Rating",
    help = "Защита от холодного оружия",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "ExplosiveArmorRating",
    name = "Explosive Armor Rating",
    help = "Защита от взрывов",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "CamouflagePercent",
    name = "Camouflage Percent",
    help = "Процент маскировки",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = -100,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "CanHoldPlate",
    name = "CanHoldPlate",
    help = "Может ли держать плиту",
    editor = "bool",
    default = false,
    modifiable = true,
    template = true,
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "BlockFaceSlot",
    name = "BlockFaceSlot",
    help = "Блокирует ли лицо",
    editor = "bool",
    default = false,
    modifiable = true,
    template = true,
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "Deterioration",
    name = "Deterioration",
    help = "Уровень износа",
    editor = "number",
    default = 0,
    template = false,
	modifiable = false,
    min = 0,
    max = 100,
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "Weight",
    help = "Вес",
    editor = "number",
    name = function(self) return "Weight: " .. (ArmorWeightIds[self.Weight] or "") end, slider = true,
    default = 1,
    template = true,
    min = 1,
    max = 5,
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "NightVision",
    name = "NightVision",
    help = "Баф/Дебаф к ночному зрению в %",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = -100,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "Vision",
    name = "Vision",
    help = "Баф/Дебаф к зрению в %",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = -100,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "DustStormProtection",
    name = "DustStorm Protection",
    help = "Защита от песчанных бурь в %",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "StunGrenadeProtection",
    name = "StunGrenadeProtection",
    help = "% защиты от СШГ",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor System",
    id = "SuppressionProtection",
    name = "SuppressionProtection",
    help = "% защиты от Подавления",
    editor = "number",
    default = 0,
    template = true,
    slider = true,
    min = 0,
    max = 100,
    modifiable = true
}





ArmorWeightIds = { "None", "Light", "Medium", "Heavy", "Super-Heavy" }
ArmorWeightText = { T(60169593798251, --[[Weapon Penetration Class: None]] "Нет"),T(73727036345951, --[[Weapon Penetration Class: Light]] "Легкий"), T(55733836475451, --[[Weapon Penetration Class: Medium]] "Средний"), T(44697586415051, --[[Weapon Penetration Class: Heavy]] "Тяжелый"), T(69836067433751, --[[Weapon Penetration Class: Super Heavy]] "Очень тяжелый")}

function GetArmorWeightUIText(id)
	return ArmorWeightText[id]
end


function Armor:GetRolloverHint()
	local hint = {} 	
	local parts = {}
	for part,val in sorted_pairs(self.ProtectedBodyParts) do
		local preset= Presets.TargetBodyPart.Default[part]
		parts[#parts+1] = preset.display_name
	end
	--hint[#hint+1] = T{378508273050, "<bullet_point> Body parts - <parts>", parts = table.concat(parts, ", ")}
	hint[#hint+1] = self.AdditionalHint or ""
	return table.concat(hint, "\n")
end	

function Armor:CalculateArmorRating(weapon_pen_class)  
    local ArmorRating = self.ArmorRating
    if IsKindOf(self, "ArmorPlates") then
		if self.PenetrationClass >= weapon_pen_class then 
        return self.ArmorRating
		else return self.ArmorRating * self.PenetrationClass^2/weapon_pen_class^2 end end

    if self.PenetrationClass > weapon_pen_class then
     ArmorRating = (self.ArmorRating + 3*self.PenetrationClass/weapon_pen_class) * self:GetConditionPercent()/100 * (100-self.Deterioration)/100
     else
     ArmorRating = self.ArmorRating * self.PenetrationClass^2/weapon_pen_class^2 * self:GetConditionPercent()/100 * (100-self.Deterioration)/100 --* (self:GetConditionPercent()-self.Deterioration)^2/100^2
    end
   -- print(self.PenetrationClass^2/weapon_pen_class^2)
    --return Min(ArmorRating,100 * self:GetConditionPercent()/100 * (101-self.Deterioration)/100)
	return floatfloor(ArmorRating)
end

function Armor:CalculateArmorRatingMelee()  
    return self.MeleeArmorRating * self:GetConditionPercent()/100 * (101-self.Deterioration)/100
end

function Armor:CalculateArmorRatingExplosive()  
    return self.ExplosiveArmorRating *  self:GetConditionPercent()/100 * (101-self.Deterioration)/100
end

function Armor:StunGrenadeProtection()  
    return self.StunGrenadeProtection *  self:GetConditionPercent()/100 * (101-self.Deterioration)/100
end

function Armor:SuppressionProtection()  
    return self.SuppressionProtection *  self:GetConditionPercent()/100 * (101-self.Deterioration)/100
end

function Unit:SuppressionProtection()
	local SuppressionProtection = 0
	self:ForEachItem("Armor", function(item, slot)
		if slot ~= "Inventory" and item.SuppressionProtection then SuppressionProtection = SuppressionProtection + item:SuppressionProtection() end
	end)
	return SuppressionProtection
end
function Unit:StunGrenadeProtection()
	local StunGrenadeProtection = 0
	self:ForEachItem("Armor", function(item, slot)
		if slot ~= "Inventory" and item.StunGrenadeProtection then StunGrenadeProtection = StunGrenadeProtection + item:StunGrenadeProtection() end
	end)
	return StunGrenadeProtection
end



function Unit:ApplyHitDamageReduction(hit, weapon, hit_body_part, ignore_cover, ignore_armor, record_breakdown)
	--local start = GetPreciseTicks(1000)
	local result = 0
	local damage = hit.damage or 0
	hit.damage = damage
	local drExp = 0
	local drFireArm = 0
	local drMelee = 0
	local drFireArmBreakdown = 0
	local itemscount = 0
	local weapon_pen_class = weapon:HasMember("PenetrationClass") and weapon.PenetrationClass or 1
	local cachedrandom = Unit:Random(100)
	self:ForEachItem("Armor", function(item, slot, left, top, hit, ignore_armor, record_breakdown, weapon_pen_class)
		if hit.damage > 0 and slot ~= "Inventory" and item.ProtectedBodyParts and item.ProtectedBodyParts[hit_body_part] then
            --Нанесенный урон считается по формуле: Урон - Порог урона * (КБ/П) * Сост
            
			--print(item.ProtectedBodyParts)
			--print(item.ProtectedBodyParts[hit_body_part])
			local dr, degrade, pierced
			pierced = false
			if not ignore_armor and item.Condition > 0 then
			--	dr = item.DamageReduction
			--	degrade = item.Degradation
				if weapon_pen_class < item.PenetrationClass then
			--		dr = dr + item.AdditionalReduction
			--		degrade = MulDivRound(degrade, const.Combat.ArmorDegradePercent, 100)
				else
					pierced = true
				end
			else
				pierced = true
			end

			drFireArmBreakdown = drFireArmBreakdown + item:CalculateArmorRating(weapon_pen_class)
		
			if item.Coverage <= cachedrandom then
				weapon_pen_class = weapon_pen_class + 1
			end

			drExp = drExp + item:CalculateArmorRatingExplosive() 
			--if item.ProtectedBodyParts == item.ProtectedBodyParts[hit_body_part] then
			drFireArm = drFireArm + item:CalculateArmorRating(weapon_pen_class)
			drMelee = drMelee + item:CalculateArmorRatingMelee()
			--else
			--	drFireArm = item:CalculateArmorRating(weapon_pen_class)
			--	drMelee =  item:CalculateArmorRatingMelee()
			--end
			--print(drFireArm)
			-- scale DR down on poor condition
			--dr = MulDivRound(dr or 0, Min(100, 50 + item.Condition), 100)
            dr = drExp 
            if IsKindOf(weapon, "Firearm") then
				if record_breakdown then dr = drFireArmBreakdown end
            dr = drFireArm end
            if IsKindOf(weapon, "MeleeWeapon") then
            dr = drMelee end
            

           -- dr = Min(ArmorRating,item.ArmorRating * 2 * item:GetConditionPercent()/100)
--            print(dr)
--            print(ArmorRating)

			--local scaled = hit.damage * (100 - dr)
			--local result = scaled / 100
            result = hit.damage - dr
            if result < 1 then result = 1 end
--            print(result)
            --result = Min(0,result)
			if pierced and result > 0 then
				--round the resulting damage up when pierced only
				--result = result + 1
			end

            degrade = MulDivRound(item.Degradation, hit.damage, 100)
            --degrade = item.Degradation * result / 100
			--print(pierced)
			--print(" "..result.." "..hit.damage.." "..dr)


			--if result > hit.damage/2 then pierced = true end

			if record_breakdown then
				if IsKindOf(weapon, "Firearm") then
					dr = drFireArmBreakdown
					end
				local resultBreakdown = hit.damage - dr
			--	if pierced then
			--		record_breakdown[#record_breakdown + 1] = { name = T{191288543859, "<em><DisplayName></em> (Pierced)", item}, value = -MulDivRound(100,dr,hit.damage) }
			--	else
					record_breakdown[#record_breakdown + 1] = { name = T{516752639882, "<em><DisplayName></em>", item}, value = -MulDivRound(100,dr,hit.damage) }
			--	end
			end

			hit.damage = Min(hit.damage, result)
			if not hit.armor_decay then hit.armor_decay = {} end
			if not hit.armor_pen then hit.armor_pen = {} end
			hit.armor_decay[item] = Min(item.Condition, degrade or 0)
			if pierced then
				hit.armor_pen[item] = true
			end
		end
	end, hit, ignore_armor, record_breakdown, weapon_pen_class)

	local armor_prevented = damage - hit.damage

	-- HoldPosition perk damage reduction
	if HasPerk(self, "HoldPosition") and (g_Overwatch[self] or g_Pindown[self]) then
		local statPercent = CharacterEffectDefs.HoldPosition:ResolveValue("percentHealth")
		local percent_reduction = MulDivRound(self.Health, statPercent, 100)
		if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = CharacterEffectDefs.HoldPosition.DisplayName, value = -percent_reduction } end
		hit.damage = Max(0, MulDivRound(hit.damage, 100 - percent_reduction, 100))
	end

	local armor = next(hit.armor_decay)
	hit.armor = armor and armor.DisplayName
	hit.armor_prevented = armor_prevented
	--print("chipichipichapachapa")
	--print(GetPreciseTicks(1000)- start)
end


function Unit:ApplyDamageAndEffects(attacker, damage, hit, armor_decay)
	if self:IsDead() or not IsValid(self) then return end
--and damage > 0
	if damage or hit.setpiece then
		self:TakeDamage(damage or 0, attacker, hit)	
	end
    local invulnerable = self:IsInvulnerable()
    --if damage and damage > 0 or hit.setpiece then
	    if not invulnerable then --and damage > 3 then
	    	local effects = hit.effects
	    	if type(effects) == "string" and effects ~= "" then
	    		self:AddStatusEffect(effects)
	    	else
	    		for _, effect in ipairs(effects) do
	    			if effect and effect ~= "" then
	    				self:AddStatusEffect(effect)
	    			end
	    		end
	    	end
	    end
    --end
	
	-- blood/soot stains
	local was_wounded = self:HasStatusEffect("Wounded")
	if hit.direct_shot and damage and damage > 3 then -- bullet-simulated firearm attacks
		local spot, params = CalcStainParamsFromShot(self, attacker, hit)
		if spot then
			assert(not params or type(params) == "table")
			self:AddStain("Blood", spot, params)
		end
	elseif not was_wounded then
		-- pick a spot and save it as effect value for the Wounded status to use if it gets applied
		local spot
		if hit.melee_attack then
			spot = GetRandomStainSpot(hit.spot_group)
		else
			spot = GetRandomStainSpot()
		end
		if spot then
			self:SetEffectValue("wounded_stain_spot", spot)
		end
	end
	
	-- cleanup wounded_stain_spot
	self:SetEffectValue("wounded_stain_spot", nil)
	
	-- add soot from explosions (if there's no blood)
	if hit.explosion then --and not self:HasStainType("Blood") then
		local spot = GetRandomStainSpot()
		self:AddStain("Soot", spot)

		willPointsBaseDamage = MulDivRound(100-self:SuppressionProtection(),hit.damage,100)
		self.WillPoints = self.WillPoints - willPointsDamage
		self.WillPoints = Max(0,self.WillPoints)
		self:ApplySuppressionStatus()

	end
		
	if not invulnerable then
		local change = false
		for item, degrade in pairs(armor_decay) do
			item.Condition = self:ItemModifyCondition(item, - degrade)
			if IsKindOf(item, "TransmutedItemProperties") and item.RevertCondition=="damage" then
				item.RevertConditionCounter = item.RevertConditionCounter-1
				if item.RevertConditionCounter== 0 then
					local slot_name = self:GetItemSlot(item)
					local new, prev = item:MakeTransmutation("revert")
					armor_decay[new] = degrade
					armor_decay[item] = false
					self:RemoveItem(slot_name, item)
					self:AddItem(slot_name, new)					
					DoneObject(prev)
					change = true
				end
			end	
		end
		if change then
			self:UpdateOutfit()
		end
	end
end

function Unit:IsArmored(target_spot_group)
	if self:IsDead() then return false end
	local armorFound = false
	self:ForEachItem("Armor", function(item, slot)
		if slot ~= "Inventory" and (not target_spot_group or item.ProtectedBodyParts and item.ProtectedBodyParts[target_spot_group]) then 
			armorFound = item
			return "break"
		end
	end)
	
	local iconName = false
	if armorFound and armorFound.ArmorRating > 0 then
		local classId = PenetrationClassIds[armorFound.PenetrationClass]
		iconName = classId:lower() .. "_armor.png"
       -- print(iconName)
	end
	return armorFound, iconName, "Mod/e6L4ECj/ArmorHudIcons/"
end

function Unit:IsArmorPiercedBy(weapon, aim, target_spot_group, action) -- Can Crit
	local pierced = true
	--if target_spot_group == "Head" then
	--	local helm = self:GetItemInSlot("Head")
	--	if helm and IsKindOf(helm, "IvanUshanka") then
	--		return false
	--	end
	--end
	if action and action.id == "KalynaPerk" then
		return true, "ignored"
	end
	--if action and action.ActionType == "Melee Attack" then
	--	return true, "ignored"
	--end
	self:ForEachItem("Armor", function(item, slot)
		local drFireArm = 0
		if slot ~= "Inventory" and item.Condition > 0 and (item.ProtectedBodyParts or empty_table)[target_spot_group] then
            local damage = 0
            if weapon.Damage then
            damage = weapon.Damage
            else damage = weapon.BaseDamage
            end
            local dr = item:CalculateArmorRatingExplosive()  
			drFireArm = drFireArm + item:CalculateArmorRating(weapon.PenetrationClass)
            if IsKindOf(weapon, "Firearm") then
            dr = drFireArm end
            if IsKindOf(weapon, "MeleeWeapon") then
            dr = item:CalculateArmorRatingMelee()
            end
            --print(damage - dr)
            if ((damage - dr) <= Min(damage/2,10)) then
			    pierced = false
               -- print(pierced)
			    return "break"
            end
		end
        
	end)
	return pierced
end

