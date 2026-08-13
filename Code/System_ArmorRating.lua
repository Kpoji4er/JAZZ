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
    min = -20,
    max = 100,
    modifiable = true
}



Armor.properties[#Armor.properties+1] = {
    category = "New Armor Condition",
    id = "ArmorResource",
    name = "Armor Resource",
    help = "Ресурс брони",
    editor = "number",
    default = 100,
    template = true,
    min = 0,
    max = 1000,
    modifiable = true
}

Armor.properties[#Armor.properties+1] = {
    category = "New Armor Condition",
    id = "Repairability",
    name = "Ремонтопригодность",
    help = "Ремонтопригодность (%)",
    editor = "number",
    default = 50,
    template = true,
    min = 0,
    max = 100,
    modifiable = true
}



Armor.properties[#Armor.properties+1] = {
    category = "New Weapon Condition",
    id = "ArmorResourceMax",
    name = "Armor Resource",
    help = "Ресурс оружия Макс",
    editor = "number",
    default = -1,
    template = false,
    min = -1,
    max = 50000,
    modifiable = true
}


--[[
function Armor:Init()
    local factory = self:GetFactoryResource() or 1000
    self.MaxCondition = self.ArmorResourceMax or factory
    local percent = Clamp(self.Condition or 100, 1, 100)
    self.ArmorResource = self.ArmorResource or MulDivRound(self.ArmorResourceMax, percent, 100)
    self.Condition = self.ArmorResource
    self:InitializeItemId()
end
]]

ArmorWeightIds = { "None", "Light", "Medium", "Heavy", "Super-Heavy" }
ArmorWeightText = { T(60169593798251, --[[Weapon Penetration Class: None]] "Нет"),T(73727036345951, --[[Weapon Penetration Class: Light]] "Легкий"), T(55733836475451, --[[Weapon Penetration Class: Medium]] "Средний"), T(44697586415051, --[[Weapon Penetration Class: Heavy]] "Тяжелый"), T(69836067433751, --[[Weapon Penetration Class: Super Heavy]] "Очень тяжелый")}

function GetArmorWeightUIText(id)
	return ArmorWeightText[id]
end

function Armor:GetFactoryResource()
	local def = InventoryItemDefs and self.class and InventoryItemDefs[self.class]
	if not def then
		return 1000
	end
	local val = rawget(def, "ArmorResource")
	if type(val) ~= "number" then
		local ok, prop = pcall(def.GetProperty, def, "ArmorResource")
		if ok then
			val = prop
		end
	end
	if type(val) == "number" and val > 0 then
		return val
	end
	return 1000
end

function Armor:GetMaxResource()
    local ArmorResourceMax = 0
    if self.ArmorResourceMax and self.ArmorResourceMax >= 0 then
        ArmorResourceMax = self.ArmorResourceMax
    else
        ArmorResourceMax = self:GetFactoryResource()
    end
	return ArmorResourceMax 
end

function Armor:GetCurrentResource()
	return self.ArmorResource or self:GetFactoryResource()
end

function Armor:GetDegradationMultiplierPermille()
	local factory = self:GetFactoryResource() or 1
	local max_res = self:GetMaxResource() or factory
	local curr_res = self:GetCurrentResource() or max_res

	if max_res <= 0 then max_res = 1 end
	if factory <= 0 then factory = 1 end

	-- (curr_res + 0.2) / max_res → permille
	local condition_x1000 = Clamp(DivRound(curr_res * 1000 + 200, max_res), 0, 1000)
	-- 0.8 + 0.2 * max_res / factory → permille
	local repair_x1000 = Clamp(800 + MulDivRound(200, max_res, factory), 100, 1000)
	local degrade = MulDivRound(condition_x1000, repair_x1000, 1000)

	local step
	if condition_x1000 <= 150 then
		step = 200
	elseif condition_x1000 <= 400 then
		step = 400
	elseif condition_x1000 <= 600 then
		step = 600
	elseif condition_x1000 <= 800 then
		step = 800
	else
		step = 1000
	end
	return MulDivRound(degrade, step, 1000)
end

function Armor:GetDegradationMultiplier()
	-- Keep float API for sight helpers; compute from integer permille.
	return self:GetDegradationMultiplierPermille() / 1000.0
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
	local deg = self:GetDegradationMultiplierPermille()
	weapon_pen_class = Max(1, weapon_pen_class or 1)
	local pen = Max(1, self.PenetrationClass or 1)
	if IsKindOf(self, "ArmorPlates") then
		if pen >= weapon_pen_class then
			return MulDivRound(self.ArmorRating, deg, 1000)
		end
		return MulDivRound(MulDivRound(self.ArmorRating, pen * pen, weapon_pen_class * weapon_pen_class), deg, 1000)
	end

	local ArmorRating
	if pen > weapon_pen_class then
		ArmorRating = self.ArmorRating + MulDivRound(3 * pen, 1, weapon_pen_class)
		return MulDivRound(ArmorRating, deg, 1000)
	end
	return MulDivRound(MulDivRound(self.ArmorRating, pen * pen, weapon_pen_class * weapon_pen_class), deg, 1000)
end

function Armor:CalculateArmorRatingMelee()  
	return MulDivRound(self.MeleeArmorRating, self:GetDegradationMultiplierPermille(), 1000)
end

function Armor:CalculateArmorRatingExplosive()  
	return MulDivRound(self.ExplosiveArmorRating, self:GetDegradationMultiplierPermille(), 1000)
end

function Armor:CalculateStunGrenadeProtection()  
	local StunGrenadeProtection = (self.StunGrenadeProtection + 0) or 0
	return MulDivRound(StunGrenadeProtection, self:GetDegradationMultiplierPermille(), 1000)
end

function Armor:GetConditionPercent()
    local max_res = self:GetMaxResource()
    if max_res <= 0 then max_res = 1 end
	return Clamp(MulDivRound(self:GetCurrentResource(), 100, max_res), 0, 100)
end

function Unit:StunGrenadeProtection()
	local StunGrenadeProtection = 0
	self:ForEachItem("Armor", function(item, slot)
		if slot ~= "Inventory" and item.StunGrenadeProtection then StunGrenadeProtection = StunGrenadeProtection + item:CalculateStunGrenadeProtection() end
	end)
	return StunGrenadeProtection or 0
end

-- Effective attack penetration: whole PenetrationClass + tenths from PenetrationBonus.
function GetAttackPenetrationClass(weapon)
	if not weapon then
		return 0
	end
	local pen = (weapon:HasMember("PenetrationClass") and weapon.PenetrationClass) or 1
	local bonus = (weapon:HasMember("PenetrationBonus") and weapon.PenetrationBonus) or 0
	return pen + 0.1 * bonus
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
	local weapon_pen_class = GetAttackPenetrationClass(weapon)
	local cachedrandom = Unit:Random(100)
	self:ForEachItem("Armor", function(item, slot, left, top, hit, ignore_armor, record_breakdown, weapon_pen_class)
		if hit.damage > 0 and slot ~= "Inventory" and item.ProtectedBodyParts and item.ProtectedBodyParts[hit_body_part] then
			-- KalynaPerk / Bullseye / other ignore_armor: skip JazzArmor absolute DR entirely
			-- (vanilla sets dr=0 when ignore_armor; jazz previously still subtracted CalculateArmorRating).
			if ignore_armor or item.Condition <= 0 then
				if not hit.armor_pen then hit.armor_pen = {} end
				hit.armor_pen[item] = true
				return
			end

            --Нанесенный урон считается по формуле: Урон - Порог урона * (КБ/П) * Сост
            
			--print(item.ProtectedBodyParts)
			--print(item.ProtectedBodyParts[hit_body_part])
			local dr, degrade, pierced
			pierced = false
			if weapon_pen_class < item.PenetrationClass then
			--		dr = dr + item.AdditionalReduction
			--		degrade = MulDivRound(degrade, const.Combat.ArmorDegradePercent, 100)
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
			hit.armor_decay[item] = Min(item.ArmorResource, degrade or 0)
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

	--print(GetPreciseTicks(1000)- start)
end


function Unit:ApplyDamageAndEffects(attacker, damage, hit, armor_decay)
	if self:IsDead() or not IsValid(self) then return end
--and damage > 0
	if damage or hit.setpiece then
		self:TakeDamage(damage and floatfloor(damage) or 0, attacker, hit)	
	end
    local invulnerable = self:IsInvulnerable()
    -- Grazing / scratch: HP + rare light bleed only — no *shot trauma, Medium/Heavy bleed, BAT, or hit effects.
	if not invulnerable then
		if hit and hit.grazing then
			JazzTryRollBleedFromGraze(self, hit, attacker)
		else
			if hit then
				hit.jazz_applied_hp = damage or hit.damage or 0
			end
			self.jazz_pending_trauma_hit = hit
			local effects = hit.effects
			local armor_hit = hit.armor_decay and next(hit.armor_decay) ~= nil
			local armor_pierced = not armor_hit or hit.armor_pen and next(hit.armor_pen) ~= nil
			-- Blast: status effects are not ballistic — apply even if armor
			-- "stopped" pen-class. Bleed still requires pierce. BAT skipped for explosions (trauma
			-- comes from JazzTryApplyExplosionConcussionAndTrauma by hit HP).
			local explosion = hit and hit.explosion
			local function apply_hit_effect(effect)
				if (armor_pierced or explosion) and type(effect) == "string" and effect ~= "" and effect ~= "MarkedTraccers"
					and CharacterEffectDefs[effect] then
					self:AddStatusEffect(JazzRemapHitBleedEffect(effect, hit, attacker))
				end
			end
			if type(effects) == "string" then
				apply_hit_effect(effects)
			else
				for _, effect in ipairs(effects or empty_table) do
					apply_hit_effect(effect)
				end
			end
			if armor_pierced then
				JazzTryRollBleedFromHit(self, hit, attacker)
			elseif armor_hit and not explosion then
				-- Stopped by armor: behind-armor blunt trauma (no bleed / no *shot).
				JazzTryBehindArmorTrauma(self, hit, attacker)
			end
			if explosion then
				JazzTryApplyExplosionConcussionAndTrauma(self, hit, attacker)
				-- JAZZ-GRENADES-002: skill-roll knockback after concussion/trauma package.
				if not self:IsDead() and IsValid(self) then
					JazzTryBlastKnockback(self, hit, attacker)
				end
			end
			self.jazz_pending_trauma_hit = nil
			-- MED-001: solid damaging hits grant +1 Pain (separate from zone-use / heavy ramp).
			JazzPainOnDamagingHit(self, hit, damage)
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

		if HasPerk(self, "Psycho") then
			return 
		end
		
			local willPointsDamage = MulDivRound(hit.damage, 20, 100)
--			local willPointsDamage = MulDivRound(100-self:SuppressionProtection(),hit.damage,200) or DivRound(hit.damage,5)
			self.WillPoints = Max(0,self.WillPoints - willPointsDamage)
			--print("grenadeWP: "..willPointsDamage)
			if willPointsDamage > 1 then 
			self:ApplySuppressionStatus()
			--ObjModified(self)
			end
		
	end
		
	if not invulnerable then
		local change = false
		-- Snapshot+sort: pairs+mutate (transmute) is order-dependent across clients.
		local decay_items = {}
		for item, degrade in pairs(armor_decay) do
			if degrade then
				decay_items[#decay_items + 1] = item
			end
		end
		table.sort(decay_items, function(a, b)
			local ka = string.format("%s:%s", tostring(a.class), tostring(a.id or a.handle or ""))
			local kb = string.format("%s:%s", tostring(b.class), tostring(b.id or b.handle or ""))
			return ka < kb
		end)
		local qi = 1
		while qi <= #decay_items do
			local item = decay_items[qi]
			local degrade = armor_decay[item]
			qi = qi + 1
			if not degrade then
				goto continue_armor_decay
			end
			if IsKindOf(item, "Armor") then
				-- уменьшаем ресурс брони напрямую
				item.ArmorResource = Max(0, item.ArmorResource - degrade)
				item.Condition = item:GetConditionPercent()
			else
				-- fallback для других предметов, если вдруг armor_decay используется не только для брони
				item.Condition = self:ItemModifyCondition(item, - degrade)
			end
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
					decay_items[#decay_items + 1] = new
				end
			end
			::continue_armor_decay::
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
	if action and action.id == "JAZZ_Bullseye" then
		return true, "ignored"
	end
	--if action and action.ActionType == "Melee Attack" then
	--	return true, "ignored"
	--end
	local weapon_pen_class = GetAttackPenetrationClass(weapon)
	self:ForEachItem("Armor", function(item, slot)
		local drFireArm = 0
		if slot ~= "Inventory" and item.Condition > 0 and (item.ProtectedBodyParts or empty_table)[target_spot_group] then
            local damage = 0
            if weapon.Damage then
            damage = weapon.Damage
            else damage = weapon.BaseDamage
            end
            local dr = item:CalculateArmorRatingExplosive()  
			drFireArm = drFireArm + item:CalculateArmorRating(weapon_pen_class)
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

