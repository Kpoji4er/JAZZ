UnitProperties.properties[#UnitProperties.properties+1] = {
    category = "XP", id = "StartingLevel", name = "Starting Level", help = "The level at which this merc starts in a new game", 
	editor = "number", default = 1, template = true, slider = true, min = 1, max = 20,
    modifiable = true
}


local function add_weapon_attacks(actions, unit, weapon)
	if IsKindOf(weapon, "MachineGun") and not unit:HasStatusEffect("StationedMachineGun") then
		table.insert_unique(actions, "MGSetup")
	elseif IsKindOf(weapon, "HeavyWeapon") then
		table.insert_unique(actions, weapon:GetBaseAttack())
	elseif IsKindOf(weapon, "Firearm") then
		for _, id in ipairs(weapon.AvailableAttacks or empty_table) do
			table.insert_unique(actions, id)
		end
	elseif IsKindOf(weapon, "MeleeWeapon") then
		if weapon.Charge then
			table.insert_unique(actions, "Charge")
		else
			table.insert_unique(actions, "Brutalize")
		end
	elseif not weapon then
		table.insert_unique(actions, "Brutalize")
	end
end


local _resolve_default_firing_mode_actions = {}
local _is_attack_available_units = {}

function Unit:ResolveDefaultFiringModeAction(firingMode, ui, sync)
	local actions = _resolve_default_firing_mode_actions
	table.iclear(actions)
	local firing_id = firingMode.id

	local weapon = firingMode:GetAttackWeapons(self)
	if IsKindOf(weapon, "Firearm") then
		for _, id in ipairs(weapon.AvailableAttacks) do
			if CombatActions[id].FiringModeMember == firing_id then
				actions[#actions + 1] = CombatActions[id]
			end
		end
	else
		for id, action in pairs(CombatActions) do
			if action.FiringModeMember == firing_id then
				actions[#actions + 1] = action
			end
		end
	end

	-- special casea
	if firing_id == "AttackDual" then
		table.insert_unique(actions, CombatActions.LeftHandShot)
		table.insert_unique(actions, CombatActions.RightHandShot)
	elseif firing_id == "Attack" and weapon:HasComponent("TwoHanded") then
		if table.find(actions, "id", "AttackDual") then
		table.remove(actions, CombatActions.AttackDual) end
	elseif firing_id == "Attack" then
		if weapon:HasComponent("EnableFullAuto") then
		table.insert_unique(actions, CombatActions.AutoFire) 
		end
		if weapon:HasComponent("EnableBurst") then
		table.insert_unique(actions, CombatActions.BurstFire) 
		end
	end
	table.sort(actions, function(a, b)
		return a.SortKey < b.SortKey
	end)

	if  weapon:HasComponent("EnableRunNGun") then
		table.insert_unique(actions, CombatActions.RunAndGun)
	end

	if self:HasStatusEffect("Hidden") then
		if table.find(actions, "id", "SingleShot") then
			return "SingleShot", actions
		end
	end
	_is_attack_available_units[1] = self
	if ui and self.lastFiringMode and table.find(actions, "id", self.lastFiringMode) then
		local action = CombatActions[self.lastFiringMode]
		if action:GetUIState(_is_attack_available_units) == "enabled" then
			if self:HasAP(action:GetAPCost(self), action.id) then
				return action.id, actions
			end
		end
	end
	for _, action in ipairs(actions) do
		if action:GetUIState(_is_attack_available_units) == "enabled" then
			if not ui or self:HasAP(action:GetAPCost(self), action.id) then
				return action.id, actions
			end
		end
	end
	return actions[1] and actions[1].id, actions
end

local voxel_radius = const.SlabBox:Radius2D()
local offsetz = const.SlabSizeZ / 2
local WorldToVoxel = WorldToVoxel
local point_pack = point_pack
local GetHeight = terrain.GetHeight
local abs = abs
local point = point
local Lerp = Lerp

function IsLineInSmoke(from_unit, to_unit)
    local smokes = g_SmokeObjs 
    if not next(smokes) then
        return -- no smokes on the whole map
    end
    --local st = GetPreciseTicks()
    local x0, y0, z0 = from_unit:GetPosXYZ()
    local x1, y1, z1 = to_unit:GetPosXYZ()
    if z1 ~= z0 then
        -- not vary accurate but will work most of the time
        z0 = (z0 or GetHeight(x0, y0)) + offsetz
        z1 = (z1 or GetHeight(x1, y1)) + offsetz
    end
    local adx, ady = abs(x1 - x0), abs(y1 - y0)
    if adx == 0 and ady == 0 then return end
    local from = point(x0, y0, z0)
    local to = point(x1, y1, z1)
    local dist = from:Dist(to)
    local steps = 1 + dist / voxel_radius -- check the line roughly on every half voxel
    local has_smoke
    --DbgClear(true) DbgAddSegment(from, to, yellow)
    for i=0,steps do
        local pt = Lerp(from, to, i, steps)
        local voxel = point_pack(WorldToVoxel(pt)) -- convert to voxel space and pack the coordinates to a single number
        local smoke = smokes[voxel]
        if smoke then -- approximate the voxel by a circle
            --DbgAddCircle(pt, voxel_radius, red) DbgAddVector(point(x, y, z), 10*guim, red)
            has_smoke = true
            break
        end
        --DbgAddCircle(pt, voxel_radius, smoke and green or black)
    end
    --print("IsLineInSmoke", has_smoke, " | ", GetPreciseTicks() - st)
    return has_smoke
end


function Unit:GetSightRadius(other, base_sight, step_pos)
	--print('getSightRadius '..self.Name)
--	ic()
	-- base sight radius, based on awareness (in-combat only) and illumination	
	local modifier = 100
	local camo = 0
	local visionbonus = 0
	local DustStormProtection = 0

	local other_is_unit = other and IsKindOf(other, "Unit") or false
	local hidden = other_is_unit and other:HasStatusEffect("Hidden")
	--local sight = base_sight or (not hidden and self:IsAware() and const.Combat.AwareSightRange or const.Combat.UnawareSightRange)
	local sight = base_sight or (self:IsAware() and const.Combat.AwareSightRange or const.Combat.UnawareSightRange)
	local night_time = GameState.Night or GameState.Underground
	if night_time and other and IsIlluminated(other, nil, nil, step_pos) then
		night_time = false
	end

	if HasPerk(self, "Jazz_Perk_Lynx") then
		sight = sight + 8
	end

	local force_min_sight = self:CallReactions_Or("OnCheckForceMinSight", self, other, step_pos, night_time)
	force_min_sight = force_min_sight or (IsKindOf(other, "Unit") and other:CallReactions_Or("OnCheckForceMinSight", self, other, step_pos, night_time))
	if force_min_sight then
		return MulDivRound(sight, const.Combat.SightModMinValue, 100) * const.SlabSizeX, hidden, night_time
	end
	modifier = self:CallReactions_Modify("OnCalcSightModifier", modifier, self, other, step_pos, night_time)
	if IsKindOf(other, "Unit") then
		modifier = other:CallReactions_Modify("OnCalcSightModifier", modifier, self, other, step_pos, night_time)
	end
	
	if other_is_unit and not other:IsDead() and not other:IsDowned() then
		if hidden then
			-- add (clamped) attrib difference as modifier
			local steath_mod = Max(0, MulDivRound(other.Agility - self.Wisdom, const.Combat.SightModStealthStatDiff, 100))		
			--if self:IsAware() and other.stance ~= "Prone"  then steath_mod = DivRound(steath_mod,2) end

			modifier = modifier - steath_mod
		end


		if other:HasStatusEffect("FleetingShadow") then 
			camo = camo + 20
		end


	
		other:ForEachItem("Armor", function(item, slot)
			if slot ~= "Inventory" 	and item.CamouflagePercent then camo = camo + MulDivRound(item.CamouflagePercent,item:GetConditionPercent()*item:GetDegradationMultiplier(),100)
			end
		end)
		

--		if (armor and armor.Camouflage) or other:HasStatusEffect("FleetingShadow") then

--		end

	end

	self:ForEachItem("Armor", function(item, slot)
		if slot ~= "Inventory" and item.Vision then visionbonus = visionbonus + MulDivRound(item.Vision,item:GetConditionPercent()*item:GetDegradationMultiplier(),100) end
	end)


	--cover
	if other_is_unit then
		local cover, any, coverage = other:GetCoverPercentage(self)
		local coverbuff = 0
		if hidden and coverage then coverage = coverage * 0.1 end
		if cover and coverage > 0 then
			-- full cover
			if cover == const.CoverHigh then
				if other.stance == "Standing" then
					coverbuff = coverage * 0.30 -- цель торчит больше
				elseif other.stance == "Crouch" then
					coverbuff = coverage * 0.35 -- сидит, меньше видно
				elseif other.stance == "Prone" then
					coverbuff = coverage * 0.50 -- лежит за фулл кавером = почти невидим
				end
				-- half cover
			elseif cover == const.CoverLow then
				if other.stance == "Standing" then
					coverbuff = coverage * 0.15 -- половинка прикрыта
				elseif other.stance == "Crouch" then
					coverbuff = coverage * 0.20 -- сидит за половинкой — норм
				elseif other.stance == "Prone" then
					coverbuff = coverage * 0.35 -- лег, всё ещё видно, но хуже
				end
			end
		end
		if hidden then coverbuff = coverbuff * 1.5 end
		if other:HasStatusEffect("Protected") then coverbuff = coverbuff * 1.25 end
		modifier = modifier - coverbuff
	end

	if self:HasStatusEffect("Protected") then
		modifier = modifier - 10
	end

	if self:HasStatusEffect("Blinded") then
		modifier = modifier - 100
	end

	

	-- environmental factors
	if other then
		local env_factors = GetVoxelStealthParams(step_pos or other) or 0
		if band(env_factors, const.vsFlagTallGrass) ~= 0 then
			modifier = modifier + const.EnvEffects.BrushSightMod

			if hidden then
				modifier = modifier - camo*3
			else
				modifier = modifier - camo*0.5
			end

			if other.stance == "Prone" then
				modifier = modifier - const.Combat.SightModHiddenProne*2
			end

		else
			if hidden then
				modifier = modifier - camo
			else
				modifier = modifier - camo*0.25
			end

			if other.stance == "Prone" then
				modifier = modifier - const.Combat.SightModHiddenProne
			end
		end
	end

	---Smoke

	if other_is_unit and IsLineInSmoke(self,other) then
		modifier = modifier - 70
	end
	
	--[[if self:HasStatusEffect("Smoked") then
		modifier = modifier - 40 
	  end
	if other_is_unit and other:HasStatusEffect("Smoked") then
		modifier = modifier - 50
	end]]


	if night_time and other then
		local darknessMod = const.EnvEffects.DarknessSightMod
		if self:HasNightVision() then
			local penaltyReduce = 0
			if HasPerk(self, "NightOps") then
				penaltyReduce = CharacterEffectDefs.NightOps:ResolveValue("night_vision_penalty_reduction")
			end
			self:ForEachItem("Armor", function(item, slot)
				if slot ~= "Inventory" and item.NightVision then
					 penaltyReduce = penaltyReduce + MulDivRound(item.NightVision,item:GetConditionPercent()*item:GetDegradationMultiplier(),100) end
			end)

			if penaltyReduce > 100 then penaltyReduce = 100 end
			--penaltyReduce = 100 - penaltyReduce
			
			darknessMod = MulDivRound(darknessMod, 100-penaltyReduce, 100)
		end
		modifier = modifier + darknessMod
		--if visionbonus < 0 then modifier = modifier + visionbonus end
	else
		modifier = modifier + visionbonus
	end	
	if GameState.Fog then
		modifier = modifier + const.EnvEffects.FogSightMod
	end
	if GameState.DustStorm then

		self:ForEachItem("Armor", function(item, slot)
			if slot ~= "Inventory" and item.DustStormProtection then DustStormProtection = DustStormProtection + MulDivRound(item.DustStormProtection,item.Condition,100) end
		end)
		modifier = modifier + const.EnvEffects.DustStormSightMod + DustStormProtection
	end
	if GameState.FireStorm then
		modifier = modifier + const.EnvEffects.FireStormSightMod
	end

	if GameState.RainLight then
		modifier = modifier - 5
	end

	if GameState.RainHeavy then
		modifier = modifier - 15
	end

	if other_is_unit then	-- height difference check
		local ox, oy, oz
		if step_pos then
			ox, oy, oz = PosToGridCoords(step_pos:xyz())
		else
			ox, oy, oz = other:GetGridCoords()
		end
		local x, y, z = self:GetGridCoords()
		if oz >= z + const.EnvEffects.SightHeightDiffThreshold then
			modifier = modifier + const.EnvEffects.SightHeightDiffMod
		elseif oz + const.EnvEffects.SightHeightDiffThreshold < z  then
			modifier = modifier + -(const.EnvEffects.SightHeightDiffMod * 2)
		end
	end
	
	--print(modifier)
	--print(camo)
	modifier = Clamp(floatfloor(modifier,0.5), const.Combat.SightModMinValue, const.Combat.SightModMaxValue)
	
	local sightAmount = MulDivRound(sight, modifier, 100) * const.SlabSizeX
	
	-- Prevent going in and out of sus state due to Pos/VisualPos differences.
	if self.command == "IdleSuspicious" then
		sightAmount = sightAmount + const.SlabSizeX / 4
	end
	
	return sightAmount, hidden, night_time
end

function Unit:OnGearChanged(isLoad)
	self.using_cumbersome = false
	NetUpdateHash("CumbersomeReset", self)
	self:ForEachItem(false, function(item, slot)
		
		if slot ~= "Inventory" and item:IsCumbersome() and not (item:IsKindOf("MachineGun") and HasPerk(self, "Merc_SamuelNkosi_Perk")) then
			self.using_cumbersome = true
			NetUpdateHash("CumbersomeSet", self)
		end
		item:ApplyModifiersList(item.applied_modifiers)
	end)
	Msg("UnitAPChanged", self)
	self:CalculateArmorWeight()
	ObjModified(self)
	ObjModified(self.Inventory)
end



function UnitProperties:EquipStartingGear(items)
	local func = empty_func
	if IsKindOf(self, "UnitData") then
		local template= UnitDataDefs[self.class]
		func = template and template.CustomEquipGear or self.CustomEquipGear
	end
	
	-- priority custom gearing rules
	func(self, items)
	
	-- default gearing rules:
	-- make sure there's an equipped weapon if possible
	if not self:GetItemInSlot("Handheld A", "BaseWeapon") then
		local has_weapon = self:TryEquip(items, "Handheld A", "Firearm")
		has_weapon = has_weapon or self:TryEquip(items, "Handheld A", "MeleeWeapon")
		has_weapon = has_weapon or self:TryEquip(items, "Handheld A", "HeavyWeapon")
	end

	if not self:GetItemInSlot("Handheld B", "BaseWeapon") then
		local has_weapon = self:TryEquip(items, "Handheld B", "Firearm")
		has_weapon = has_weapon or self:TryEquip(items, "Handheld B", "MeleeWeapon")
		has_weapon = has_weapon or self:TryEquip(items, "Handheld B", "HeavyWeapon")
	end
	
	local equipped = {}

	self:TryEquip(items, "AmmoInventory", "Ammo")
	self:TryEquip(items, "AmmoInventory", "Ammo")
	self:TryEquip(items, "AmmoInventory", "Ammo")
	self:TryEquip(items, "AmmoInventory", "Ammo")
	self:TryEquip(items, "GrenadesInventory", "GrenadeItem")
	self:TryEquip(items, "GrenadesInventory", "Flare")
	self:TryEquip(items, "OrdnanceInventory", "ThrowableTrapItem")
	self:TryEquip(items, "MedicalInventory", "Medicine")
	self:TryEquip(items, "PocketInventory", "ToolItem")
	self:TryEquip(items, "KnifeInventory", "StackableMeleeWeapon")

	-- locked items that are not weapons add to the first inventory slot
	--for i, item in ipairs(items) do
	--	if item.locked and not item:IsWeapon() and not IsKindOf(item, "Armor") then -- lock to the first inventory slot
	--		if self:CanAddItem("Inventory", item) then
	--			self:AddItem("Inventory", item)
	--			equipped[i] = true
	--		end
	--	end				
	--end
	-- equip the rest of the equppable items when possible

	
	
	for i, item in ipairs(items) do
		if not equipped[i] then
			local slot
			if IsKindOf(item, "QuickSlotItem") then
				if self:CanAddItem("Handheld A", item) then
					slot = "Handheld A"
				elseif self:CanAddItem("Handheld B", item) then
					slot = "Handheld B"
				end
			elseif IsKindOf(item, "Armor") and not self:GetItemInSlot(item.Slot) then
				slot = item.Slot
			end
			if slot and self:CanAddItem(slot, item) then
				self:AddItem(slot, item)
				equipped[i] = true
			end
		end
	end
	
	-- make sure all equipped firearms have ammo
	local function reload_weapon(weapon)
		if  (not weapon.ammo or weapon.ammo.Amount <= 0) then

			local ammoObj = self:GetAvailableAmmos(weapon)[1]
			if not ammoObj then
				local ammoDef = GetAmmosWithCaliber(weapon.Caliber, "sort")[1]
				if ammoDef and ammoDef.id then
					ammoObj = PlaceInventoryItem(ammoDef.id)
				end
			end

			if ammoObj then
				--local tempAmmo = PlaceInventoryItem(ammo.id)
				--print(ammo)
				local tempAmmo = self:GetAvailableAmmos(weapon)[1]
				--print(g_Classes[ammo.id] or "error")
				if not tempAmmo or tempAmmo.Amount < weapon.MagazineSize then
				  tempAmmo = PlaceInventoryItem(ammoObj.class)   -- создаём клон, если стека нет
				  tempAmmo.Amount = weapon.MagazineSize
				  weapon:Reload(tempAmmo, "suspend_fx")
				 -- DoneObject(tempAmmo)                     -- удалить можно: это клон
				else
				  weapon:Reload(tempAmmo, "suspend_fx")
				  -- НИКАКОГО DoneObject здесь!  Стек останется в items → позже
				  -- AddItem("Inventory", item) положит его в карман правильно.
				end
			end
		end
	end
	--print('reloading')
	self:ForEachItemInSlot("Handheld A", "Firearm", reload_weapon)
	self:ForEachItemInSlot("Handheld B", "Firearm", reload_weapon)
	
	-- place the rest in Inventory slot
	for i, item in ipairs(items) do
		if not equipped[i] then
			local pos, reason = self:AddItem("Inventory", item)
			if not pos then
				print("Couldn't add starting item \'", item.class, "\' to unit", self.class, "because", reason, "max slots", self:GetMaxTilesInSlot("Inventory"))
			end		
		end
	end
end

function Unit:GetAttackAPCost(action, weapon, action_ap_cost, aim, delta)
	if not weapon then 
		return 0
	end
	
	local min, max = self:GetBaseAimLevelRange(action, weapon)
	aim = Clamp(aim or 0, min, max) - min -- only charge for aiming above min level
	delta = delta or 0
	local aimCost = const.Scale.AP
	local rain_penalty = GameState.RainHeavy and not self.indoors
	--if rain_penalty then
	--	aimCost = MulDivRound(aimCost, 100 + const.EnvEffects.RainAimingMultiplier, 100)
	--end
	
	local ap = action_ap_cost or weapon.AttackAP or weapon.ShootAP or 0
	ap = ap + delta 
	ap = self:CallReactions_Modify("OnCalcAPCost", ap, action, weapon, aim)

	if IsKindOf(weapon, "HeavyWeapon") then
	elseif IsKindOf(weapon, "Firearm") or IsKindOf(weapon, "Grenade") or IsKindOf(weapon, "MeleeWeapon") then
		ap = ap + aim * aimCost
	else
		ap = -1
	end
	
	-- legal cheat: during heavy rain last possible aim costs 1 AP regardless of the penalty
	local remainingAP = (self:GetUIActionPoints() / 1000) * 1000
	if rain_penalty and ap > remainingAP and aim > 0 then 
		local diff = abs(remainingAP - ap)
		if diff < aimCost and diff >= const.Scale.AP then
			ap = remainingAP
			aimCost = 1000
		end
	end
	
	return ap, aimCost
end


function Unit:CalcChanceToHit(target, action, args, chance_only)
	-- Argument validation and fallbacks
	if not (IsPoint(target) or IsValid(target) and IsKindOf(target, "CombatObject")) then
		return 0
	end
	local weapon1, weapon2 = action:GetAttackWeapons(self)
	local weapon = args and args.weapon or weapon1
	if not weapon or IsKindOf(weapon, "Medicine") then
		return 0
	end

	local modifiers = not chance_only and {}
	
	if CheatEnabled("AlwaysHit") then
		if modifiers then 
			modifiers[#modifiers + 1] = {
				name = T(521586645369, "Cheat: Always Hit"),
				value = 100,
				id = "cheat"
			}
		end
		return 100, 100, modifiers
	elseif CheatEnabled("AlwaysMiss") then
		if modifiers then
			modifiers[#modifiers + 1] = {
				name = T(455715392693, "Cheat: Always Miss"),
				value = 0,
				id = "cheat"
			}
		end
		return 0, 0, modifiers
	end

	local target_spot_group = args and args.target_spot_group or nil
	if type(target_spot_group) == "table" then
		target_spot_group = target_spot_group.id
	end
	target_spot_group = target_spot_group or g_DefaultShotBodyPart
	if type(target_spot_group) == "string" then
		target_spot_group = Presets.TargetBodyPart.Default[target_spot_group]
	end

	local aim = args and args.aim or 0
	local opportunity_attack = args and args.opportunity_attack
	local attacker_pos = args and (args.step_pos or args.goto_pos) or self:GetPos()
	local target_pos = args and args.target_pos or IsPoint(target) and target or target:GetPos()


	local base = 0

	-- Base CTH
	local wpn_skill = self[weapon.base_skill]
	local subskill = weapon and IsKindOf(weapon, "MachineGun") and self.Strength  or self.Dexterity
	local dexdestr = weapon  and IsKindOf(weapon, "MachineGun")  and self:GetPropertyMetadata("Strength") or self:GetPropertyMetadata("Dexterity")
	local lvl = self:GetLevel()



	local skill = (wpn_skill * 4 + subskill * 2 + lvl * 5) / 6
	skill =  20 + (skill ^ 1.2) * 0.25

		if weapon and IsKindOf(weapon,"MeleeWeapon") then 
		skill = (wpn_skill * 2 + subskill * 4 + lvl * 5) / 6
		end

	skill = floatfloor(skill,0.5)



--	end

	if action.id == "SteroidPunch" then
		skill = self["Strength"]
	end
	base = base + skill
	
	if args and not args.prediction then
		local effects = {}
		for i, effect in ipairs(self.StatusEffects) do
			effects[i] = effect.class
		end
		effects = table.concat(effects, ",")
		local target_effects = "-"
		if IsKindOf(target, "Unit") then
			target_effects = {}
			for i, effect in ipairs(target.StatusEffects) do
				target_effects[i] = effect.class
			end
			target_effects = table.concat(target_effects, ",")
		end
		NetUpdateHash("CalcChanceToHit_Base", self, target, action.id, weapon.class, weapon.id, base, effects, target_effects,
			weapon1 and weapon1.class, weapon1 and weapon1.id, weapon1 and weapon1.Condition, weapon1 and weapon1.MaxCondition,
			weapon2 and weapon2.class, weapon2 and weapon2.id, weapon2 and weapon2.Condition, weapon2 and weapon2.MaxCondition
		)
	end
	
	if modifiers then
		self.combat_cache = self.combat_cache or {}
		local key = "base_cth_" .. weapon.base_skill
		local skillmod = self.combat_cache[key]
		if not skillmod then
			local prop_meta = self:GetPropertyMetadata(weapon.base_skill)
			if prop_meta then
				--print(prop_meta)
					skillmod =
					{
						name = T{4621434559001, "Навыки (<name>, <sub>)", name = prop_meta.name, sub = dexdestr.name},
						value = skill
					}
			else
				assert(false, "weapon base skill '" .. weapon.base_skill .. "' property metadata not found!")
				skillmod =
				{
					name = T(462143455900, "Marksmanship"),
					value = skill
				}
			end
			self.combat_cache[key] = skillmod
		end
		table.insert(modifiers, skillmod)
	end

	local mod_data = {
		attacker = self,
		target = target,
		target_spot_group = target_spot_group,
		action = action, 
		weapon1 = weapon1, 
		weapon2 = weapon2, 
		aim = aim, 
		opportunity_attack = opportunity_attack, 
		attacker_pos = attacker_pos, 
		target_pos = target_pos,
		min = 0,
		max = 100,
	}


	-- Evaluate all modifiers
	ForEachPreset("ChanceToHitModifier", function(mod)
		if mod.RequireTarget and not IsValidTarget(target) then
			return
		end
		local req_action = mod.RequireActionType
		if req_action == "Any Attack" then
			if action.ActionType == "Other" then
				return
			end
		elseif req_action == "Any Melee Attack" then
			if action.ActionType ~= "Melee Attack" then
				return
			end
		elseif req_action == "Any Ranged Attack" then
			if action.ActionType ~= "Ranged Attack" then
				return
			end
		elseif req_action ~= action.id then
			return
		end
		
		local lof = false -- Currently unused by any modifier
		local apply, value, nameOverride, metaText, idOverride = mod:CalcValue(self, target, target_spot_group, action, weapon, weapon2, lof, aim, opportunity_attack, attacker_pos, target_pos)
		if args and not args.prediction then
			NetUpdateHash("CalcChanceToHit_Modifier", mod.id, apply, value)
		end
		if not apply then
			return
		end
		-- automated GatherCTHModifications provide a standard mechanism for replacing display name & adding meta text (only for the applicable mods)
		mod_data.display_name = nameOverride or mod.display_name
		mod_data.meta_text = (IsT(metaText) and {metaText} or metaText) or nil
		value = self:GatherCTHModifications(mod.id, value, mod_data)
		if args and not args.prediction then
			NetUpdateHash("CalcChanceToHit_Modifier_Mods", mod.id, value)
		end
		local nameOverride = mod_data.display_name
		local metaText = #mod_data.meta_text > 0 and mod_data.meta_text
		base = base + value
		if mod_data.enabled and modifiers then
			table.insert(modifiers, 
			{ 
				name = nameOverride or mod.display_name,
				value = value,
				id = idOverride or mod.id,
				metaText = metaText
			})
		end
	end)
	
	-- cycle status effects, running GatherCTHModifications() for every one of them, using the effect class/id as mod id
		-- this way status effects can implement their own cth modifiers via the same mechanism
	for _, effect in ipairs(self.StatusEffects) do
		mod_data.display_name = effect.DisplayName
		mod_data.meta_text = nil
		local value = self:GatherCTHModifications(effect.class, 0, mod_data)
		if args and not args.prediction then
			NetUpdateHash("CalcChanceToHit_Effect_Mods", effect.class, value)
		end
		if value and value ~= 0 then
			base = base + value
			if mod_data.enabled and modifiers then
				table.insert(modifiers, 
				{ 
					name = mod_data.display_name,
					value = value,
					id = effect.id,
					metaText = mod_data.meta_text
				})
			end
		end
	end
	
	-- process weaponcomponenteffects
	mod_data.weapon1 = nil
	mod_data.weapon2 = nil
	local weapons = {weapon1, weapon2}
	for _, weapon in ipairs(weapons) do
		if IsKindOf(weapon, "Firearm") then		
			for slot_id, component_id in sorted_pairs(weapon.components) do
				local def = WeaponComponents[component_id]
				local effects = def and def.ModificationEffects or empty_table
				if next(effects) ~= nil then
					mod_data.weapon1 = weapon
					mod_data.display_name = def.DisplayName
					mod_data.meta_text = nil
					local value = self:GatherCTHModifications(component_id, 0, mod_data)
					if args and not args.prediction then
						NetUpdateHash("CalcChanceToHit_Component_Mods", weapon.id, component_id, value)
					end
					if value and value ~= 0 then
						base = base + value
						if mod_data.enabled and modifiers then
							table.insert(modifiers, 
							{ 
								name = mod_data.display_name,
								value = value,
								id = component_id,
								metaText = mod_data.meta_text
							})
						end
					end
				end
			end
		end
	end
	
	mod_data.modifiers = modifiers
	self:CallReactions("OnCalcChanceToHit", self, action, target, weapon1, weapon2, mod_data)
	if IsKindOf(target, "Unit") then
		target:CallReactions("OnCalcChanceToHit", self, action, target, weapon1, weapon2, mod_data)
	end
	base = Max(0, mod_data.enabled and MulDivRound(base + mod_data.mod_add, mod_data.mod_mul, 100) or 0)

	local dist = Max(1,attacker_pos:Dist(target_pos)/const.SlabSizeX)

	local MaxCTH = 100

	if weapon1 and weapon1.Grouping then
		local groupingResult = FirearmGetGrouping(weapon1,dist)
		if groupingResult < 100 then
			MaxCTH = groupingResult
			--print(MaxCTH)
		end
	end

	local target_pos = IsPoint(target) and target or target:GetPos()
	local knife_throw = IsKindOf(weapon, "MeleeWeapon") and (action.ActionType == "Ranged Attack")
	local penalty = weapon:GetAccuracy(attacker_pos:Dist(target_pos), self, action, knife_throw) - 100
	local final = Clamp(base + penalty, 0, MaxCTH)
	final = Clamp(final, mod_data.min, mod_data.max)
		



	if args and not args.prediction then
		NetUpdateHash("CalcChanceToHit_Final", final)
	end
	
	if chance_only then
		return final
	end
	if penalty < 0 then
		if action.ActionType == "Melee Attack" then
			modifiers[#modifiers + 1] = {
				name = T(660754354729, "Weapon Accuracy"),
				value = penalty,
				id = "Accuracy"
			}
		elseif penalty <= -100 then
			modifiers[#modifiers + 1] = {
				name = T(162704513413, "Out of Range"),
				value = penalty,
				id = "Range"
			}
		else
			modifiers[#modifiers + 1] = {
				name = T(30158603055711, "Bullet Drop"),
				value = penalty,
				id = "Range"
			}
		end
	end


	--print('final '..final)
	--print('base '..base)

	return final, base, modifiers, penalty
end


function Unit:GetInteractionPosWith(target, ignore_occupied)
	if not target then return end
	if  not target:GetInteractionPos(self) then return end
	local positions = target:GetInteractionPos(self)
	if not positions then
		return
	end
	if type(positions) == "table" then
		if #positions == 0 then
			return
		end
		if ignore_occupied == nil then
			ignore_occupied = positions.ignore_occupied
		end
	end
	local pfflags = self:GetPathFlags()
	if ignore_occupied then
		pfflags = pfflags & ~const.pfmDestlock
	end
	local has_path, closest_pos = pf.HasPosPath(self, positions, nil, 0, 0, self, 0, nil, pfflags)
	-- Could path to
	if has_path and closest_pos then
		if closest_pos == positions or type(positions) == "table" and table.find(positions, closest_pos) then
			return closest_pos
		-- Couldnt path, but unit is close enough
		elseif self:CloseEnoughToInteract(positions, target) then
			return closest_pos
		end
	end
end



function UnitBase:GetPersonalMorale()
	local teamMorale = self.team and self.team.morale or 0
	local personalMorale = 0
	
	if IsMerc(self) then
		--reduce morale for at least one disliked merc in team
		local isDisliking = false
		for _, dislikedMerc in ipairs(self.Dislikes) do
			local dislikedIndex = table.find(self.team.units, "session_id", dislikedMerc)
			if dislikedIndex and not self.team.units[dislikedIndex]:IsDead() then
				personalMorale = personalMorale - 1
				isDisliking = true
				break
			end
		end
		--increase morale for no disliked and at least one liked merc
		if not isDisliking then
			for _, likedMerc in ipairs(self.Likes) do
				local likedIndex = table.find(self.team.units, "session_id", likedMerc)
				if likedIndex and not self.team.units[likedIndex]:IsDead()  then
					personalMorale = personalMorale + 1
					break
				end
			end
		end
	end
	--lower morale if below 50% or 3+ wounds (REVERT for psycho perk)
	local isWounded = false
	local idx = self:HasStatusEffect("Wounded")
	if idx and self.StatusEffects[idx].stacks >= 3 then
		isWounded = true
	end
	if self.HitPoints then
		if self.HitPoints < MulDivRound(self.MaxHitPoints, 50, 100) or isWounded then
			if HasPerk(self, "Psycho") then
				personalMorale = personalMorale + 1
			else
				personalMorale = personalMorale - 1
			end
		end
	end
	--lower morale if liked merc has died recently
	for _, likedMerc in ipairs(self.Likes) do
		local ud = gv_UnitData[likedMerc]
		if ud and ud.HireStatus == "Dead" then
			local deathDay = ud.HiredUntil
			if deathDay + 7 * const.Scale.day > Game.CampaignTime then
				personalMorale = personalMorale - 1
				break
			end
		end
	end
	
	personalMorale = self:CallReactions_Modify("OnCalcPersonalMorale", personalMorale)
	
	return Clamp(personalMorale + teamMorale, -5, 5)
end

function UnitProperties:GetMaxActionPoints()
	local base = 8 * const.Scale.AP

	local level = self:GetLevel()
	local agi = MulDivRound(self:GetProperty("Agility"),1,10)
	--local hp = MulDivRound(self:GetProperty("Health"),1,10)
	local hp = MulDivRound(self:GetProperty("Health"),1,10)
	if self.HitPoints then
		hp = MulDivRound(self.HitPoints,1,10)
	end


	local statsScale = MulDivRound(2*agi+1*hp,const.Scale.AP,3)
	local statsScaleAP = MulDivRound(statsScale,level,10)

	local ap = base + MulDivRound(statsScale,7,10) + MulDivRound(statsScaleAP,3,10)

	--print(base.."Stats "..statsScale.."agi "..agi.."HP "..hp.."AP "..ap)
	return ap
	--return ((3 + self:GetProperty("Agility") / 10) + (level / 3)) * const.Scale.AP
end



function Unit:CalculateArmorWeight()
	local TotalAPDebuff = const.Scale.AP
	local TotalFreeMoveDebuff = 0
		self:ForEachItem("Armor", function(item, slot)
			--print(item)
			if slot ~= "Inventory" and item.Weight then
				--print(item)
				--print(item.Weight)
				 if item.Weight == 2 then 
					--TotalAPDebuff = TotalAPDebuff + 0.25 * const.Scale.AP
					TotalFreeMoveDebuff = TotalFreeMoveDebuff + 0.5
				 end
				 if item.Weight == 3 then 
					--TotalAPDebuff = TotalAPDebuff + 0.5 * const.Scale.AP
					TotalFreeMoveDebuff = TotalFreeMoveDebuff + 1 
				 end
				 if item.Weight == 4 then 
					--TotalAPDebuff = TotalAPDebuff + 1 * const.Scale.AP
					TotalFreeMoveDebuff = TotalFreeMoveDebuff + 2
				 end
				 if item.Weight == 5 then 
					--TotalAPDebuff = TotalAPDebuff + 1.5 * const.Scale.AP
					TotalFreeMoveDebuff = TotalFreeMoveDebuff + 3
				 end
			end
		end)
	--print(TotalAPDebuff..".."..TotalFreeMoveDebuff.."..")
	if HasPerk(self, "Ironclad") then 
		TotalAPDebuff = TotalAPDebuff/2
		TotalFreeMoveDebuff = TotalFreeMoveDebuff/2 
	end
	if HasPerk(self, "KillingWind") then 
		TotalAPDebuff = TotalAPDebuff/5
		TotalFreeMoveDebuff = TotalFreeMoveDebuff/5 end

	if self.using_cumbersome then TotalFreeMoveDebuff = MulDivRound(TotalFreeMoveDebuff,1,2) end

		if self.Strength > 60 then
			local StrBuff = MulDivRound(self.Strength-60,1,20)
			TotalFreeMoveDebuff = TotalFreeMoveDebuff - StrBuff 
			TotalAPDebuff = TotalAPDebuff - StrBuff * 2 * const.Scale.AP
		end

		TotalAPDebuff = floatfloor(TotalAPDebuff,0.5)
		TotalFreeMoveDebuff = floatfloor(TotalFreeMoveDebuff)

		--print(TotalFreeMoveDebuff.." "..TotalAPDebuff)

		TotalFreeMoveDebuff = Clamp(TotalFreeMoveDebuff, 0, 12*const.Scale.AP)
		TotalAPDebuff = Clamp(TotalAPDebuff, 0, 5*const.Scale.AP)

		--print(TotalFreeMoveDebuff.." "..TotalAPDebuff)
		
		self:ConsumeAP(TotalFreeMoveDebuff, "Move")
		self:ConsumeAP(Min(self.ActionPoints, TotalAPDebuff))
		
		local armor = self:GetItemInSlot("Torso", "Armor")
		local plate = self:GetItemInSlot("Torso", "ArmorPlate") or armor
		local armorclass = 1
		local plateclass = 1
		if armor then armorclass = armor.PenetrationClass end
		if plate and plate.Condition > 0 then plateclass = plate.PenetrationClass  or 0 end
 		
		armorclass = Max(armorclass,plateclass)



		self:RemoveStatusEffect("Weight_1Class", "all")
		self:RemoveStatusEffect("Weight_2Class", "all")
		self:RemoveStatusEffect("Weight_3Class", "all")
		self:RemoveStatusEffect("Weight_4Class", "all")
		self:RemoveStatusEffect("Weight_5Class", "all")
		--print(TotalFreeMoveDebuff)
		if TotalFreeMoveDebuff > 1 then
			local count = floatfloor(TotalFreeMoveDebuff)
			--print(count)
			for i = 1, count do
				self:AddStatusEffect("Weight_"..armorclass.."Class")
			end
		end

	return 
end


function Unit:RecalcWillPoints()

	if HasPerk(self, "Psycho") and not self:HasStatusEffect("Berserk") then
		self.WillPoints = Clamp(self.WillPoints - 5, 0, self.MaxWillPoints)
		self:ApplySuppressionStatus()
		return end		

	local leadership = 0
	local animalsnearby = 0

	local units = g_Units
	units = table.ifilter(units, function(k, v)
		return v.HireStatus ~= "Dead"
	end)

	for _, unit in ipairs(units) do
		
		local dist = DivRound(self:GetPos():Dist(unit:GetPos()),const.SlabSizeX)
		if unit.species ~= "Human" and dist < 11  then animalsnearby = animalsnearby + 1 end
		if self ~= unit and self.side == unit.side then


			if HasPerk(unit, "Negotiator") then dist = Max(1,dist-3) end
			if dist < 11 then
				leadership = Max(leadership,(unit.Leadership + 5 * Clamp(unit:GetPersonalMorale(),0,5))*(11-dist))
			end
			--ObjModified(unit)
		end
		--end
	end

	local buff = 8 + DivRound(leadership,50)

	if IsMerc(self) and (self.Dislikes or self.Likes) then
		for _, dislikedMerc in ipairs(self.Dislikes) do
			local dislikedIndex = table.find(self.team.units, "session_id", dislikedMerc)
			if dislikedIndex and not self.team.units[dislikedIndex]:IsDead() then
				if dislikedIndex and DivRound(self:GetPos():Dist(self.team.units[dislikedIndex]:GetPos()),const.SlabSizeX) < 3 and not self.team.units[dislikedIndex]:IsDead() then
					local dislikedIndex = table.find(self.team.units, "session_id", dislikedMerc)
						buff = buff - 1
					end
			end
		end
		for _, likedMerc in ipairs(self.Likes) do
			local likedIndex = table.find(self.team.units, "session_id", likedMerc)
			if likedIndex and not self.team.units[likedIndex]:IsDead()  then
				if likedIndex and DivRound(self:GetPos():Dist(self.team.units[likedIndex]:GetPos()),const.SlabSizeX) < 3 and not self.team.units[likedIndex]:IsDead() then
					local likedIndex = table.find(self.team.units, "session_id", likedMerc)
						buff = buff + 1
				end
			end
		end
	end


	--print("wpbuffleadership"..buff)

	if HasPerk(self, "Optimist") then
		local chance = CharacterEffectDefs.Optimist:ResolveValue("procChance")
		local roll = InteractionRand(100, "Optimist")
		if roll < chance then
			PlayVoiceResponse(self, "Optimist")
			buff = buff + 5
		end
		buff = buff + 1
	end

	if HasPerk(self, "Pessimist") then
		local chance = CharacterEffectDefs.Pessimist:ResolveValue("procChance")
		local roll = InteractionRand(100, "Pessimist")
		if roll < chance then
			PlayVoiceResponse(self, "Pessimist")
			buff = buff - 4
		end
		buff = buff - 1
	end

	if HasPerk(self, "Spiritual") then
		buff = buff + 5
	end

	if IsSectorUnderground(gv_CurrentSectorId) and self:HasStatusEffect("ClaustrophobicChecked") then
		buff = buff - 10
	end

	local loner_bonus = 10
	for _, other in ipairs(self.team.units) do
		if self ~= other and DivRound(self:GetDist(other), const.SlabSizeX) <= CharacterEffectDefs.Loner:ResolveValue("loner_radius") then
			loner_bonus = 0
		end
	end
	buff = buff + loner_bonus 


	if self:HasStatusEffect("ZoophobiaChecked") then
		buff = buff - 10 * animalsnearby
		else buff = buff - 3 * animalsnearby
	end



	
	if HasPerk(self, "Hemophobic") and self:HasStatusEffect("Bleeding") then
		local chance = CharacterEffectDefs.Hemophobic:ResolveValue("procChance")
		local roll = InteractionRand(100, "Hemophobic")
		if roll < chance then
			PlayVoiceResponse(self, "Hemophobic")
			--CombatLog("debug", T{Untranslated("<em>Hemophobic</em> proc on <unit>"), unit = self.Name})

			--PanicOutOfSequence({self})
			buff = buff - 50
		end
	end

	if self:HasStatusEffect("Protected") then
		buff = buff + 20
	end


	if self:HasStatusEffect("SuppressionPinned") then
		buff = buff + 5
	end

    buff = buff + Clamp(3*self:GetPersonalMorale(),-3,10)


	local wp_delta = MulDivRound(self.MaxWillPoints, buff, 100)
	
	self.WillPoints = Clamp(self.WillPoints + wp_delta, 0, self.MaxWillPoints)
	--self:ApplySuppressionStatus()
	--print("wpbuff"..buff)

	--print("WillPointsRegen." .. (self.Nick or self.Name) .. " " .. wp_delta)

end


function Unit:GetNumMGInterruptAttacks(skip_check)
	if not skip_check and not self:HasStatusEffect("StationedMachineGun") and not self:HasStatusEffect("ManningEmplacement") then
		return 0
	end
	local action = self:GetDefaultAttackAction()
	local ap_cost = action:GetAPCost(self)
	if ap_cost <= 0 then
		return 0
	end
	local ap = g_Combat and self:GetUIActionPoints() or self:GetMaxActionPoints()

	local PerkBonus = (HasPerk(self, "HeavyWeaponsTraining")) and 2 or 0
	
	return const.Combat.MGFreeInterruptAttacks + PerkBonus + ap / ap_cost
end

function Unit:BeginTurn(new_turn)	
	NetUpdateHash("BeginTurn_Start")
	self:SetAttackReason()
	local should_interrupt = true
	local pindown = g_Pindown[self]
	local overwatch = g_Overwatch[self]
	if pindown and IsValidTarget(pindown.target) and self:HasPindownLine(pindown.target, pindown.target_spot_group) then
		-- pindown will be handled differently when the attack is executed
		should_interrupt = false
	elseif overwatch and (overwatch.permanent or not g_Combat or overwatch.expiration_turn > g_Combat.current_turn) then
		should_interrupt = false
	elseif self.prepared_bombard_zone then
		should_interrupt = false
	end	
	if new_turn and should_interrupt then 
		self:InterruptPreparedAttack("begin turn")
		pindown = false
	end
	self:UpdateMeleeTrainingVisual()
	self:IsThreatened() -- update the is_melee_aim_last_turn flag for the vr
	
	if self.is_melee_aim_last_turn and IsMerc(self) then		
		PlayVoiceResponse(self, "MeleeEnemiesClosing")
		self.is_melee_aim_last_turn = false
	end


	self.perks_activated = {}
	NetUpdateHash("BeginTurn_Progress")
	if new_turn then
		self:RemoveStatusEffect("FreeMove")
		if g_Overwatch[self] and not g_Overwatch[self].permanent then
			self.ActionPoints = 0 -- special-case for carrying an overwatch from exploration mode
		else
			local ap = self:GetMaxActionPoints()
			ap = self:CallReactions_Modify("OnCalcStartTurnAP", ap)
			self.ActionPoints = Max(0, ap)
			
--			if g_Combat.current_turn == 1 and self:IsMerc() then --use this to test lower AP during the first turn
--				self.ActionPoints = MulDivRound(self.ActionPoints, 75, 100)
--			end
		end
		if g_Overwatch[self] then
			table.clear(g_Overwatch[self].triggered_by) -- reset triggers in case somebody already triggered in our turn
			if self:HasStatusEffect("ManningEmplacement") or self:HasStatusEffect("StationedMachineGun") then
				g_Overwatch[self].num_attacks = self:GetNumMGInterruptAttacks()
				self:UpdateOverwatchVisual()
			end
		end
		g_Pindown[self] = nil -- clear from the global table to stop the prepared attack blocking any AP gains
		self.ui_reserved_ap = 0
		
		if self:GetEffectValue("missed_by_kill_shot") and not self:IsDead() and not self:IsDowned() then
			PlayVoiceResponse(self, "MissedByKillShot")
			self:SetEffectValue("missed_by_kill_shot", nil)
		end
		
		self:UpdateHidden()
		
		local voxels = self:GetVisualVoxels()
		local fire, dist = AreVoxelsInFireRange(voxels)
		if fire then
			local min, max = const.BurnDamageMin, const.BurnDamageMax
			local damage = self:RandRange(min, max)
			self:TakeDirectDamage(damage)
			if not self:IsIncapacitated() and not self:HasStatusEffect("Unconscious") and not RollSkillCheck(self, "Health") then
				self:ChangeTired(1)
			end
			if dist < const.SlabSizeX then
				self:AddStatusEffect("Burning")
			end
		end
		
		self.attacked_this_turn = false
		self.hit_this_turn = false
		self.wounded_this_turn = false
		NetUpdateHash("BeginTurn", self, self.using_cumbersome, HasPerk(self, "KillingWind"),
								HasPerk(self, "Ironclad"))


		
		if not self.using_cumbersome or HasPerk(self, "KillingWind") then
			self:AddStatusEffect("FreeMove")
		elseif self:CanUseIroncladPerk() then
			self:AddStatusEffect("FreeMove")
			--self:ConsumeAP(DivRound(self.free_move_ap, 2), "Move")
		end

		

--
		--self:ForEachItem("Armor", function(item, slot)
		--	print(item)
		--end)

		--print(TotalFreeMoveDebuff)
		--TotalFreeMoveDebuff = MulDivRound(TotalFreeMoveDebuff,50,100-self.Strength)
		--TotalAPDebuff = MulDivRound(TotalAPDebuff,50,100-self.Strength)
		


		
		local effect = self:GetStatusEffect("Wounded", "all")
		local wounds = 0
		if effect then
			wounds = effect.stacks 
		end
		if wounds > 0 then
			self:ConsumeAP(wounds * const.Scale.AP)
		end


		self:SetWeaponLightFx(true)



		
		-- ConsumeAP will flag this only when an action is given, so it is safe to mark this a bit earlier to allow OnBeginTurn effects to alter it
		self.performed_action_this_turn = false
		
		Msg("UnitBeginTurn", self)
		self:CallReactions("OnBeginTurn")
		
		local morale = self:GetPersonalMorale() or 0
	--	if morale > 0 then
	--		self:GainAP(morale * const.Scale.AP)
	--	elseif morale < 0 then
	--		self:ConsumeAP(Min(self.ActionPoints, -morale * const.Scale.AP))
	--	end


		self:RecalcWillPoints()
		RecalcMaxWillPoints(self)

		self:CalculateArmorWeight()
		
		if self:GetItemInSlot("HeadGear", "GasMaskBase") then
			self:ConsumeAP(const.Scale.AP)
		end

		-- special-case: if the unit dies as a result of a status effect, show them and wait the command to end
		-- doing this here makes sure the camera will not immediately jump to another unit (dying or selected)
		-- similarly, executing the pindown attack has to be waited until it finishes
		if self.command == "Die" then
			SnapCameraToObj(self)
			while self.command == "Die" do
				WaitMsg("UnitDied", 20) -- can also go in VillainDefeat instead, so wait with timeout
			end
		elseif pindown then
			pindown.target:ProvokeOpportunityAttack_Pindown(self, pindown)
		elseif self.prepared_bombard_zone then
			self:StartBombard()
		end
	end
	
	if self.dummy or self:IsDowned() then
		self.ActionPoints = 0
	end

	self.start_turn_pos = self:GetVisualPos()
		
	NetUpdateHash("BeginTurn", self, self:GetPos())
	
	Msg("UnitAPChanged", self)
end


function Unit:MGSetup(action_id, cost_ap, args)
	local target = args.target or self
	self.interruptable = false
	local cover, any, coverage = self:GetCoverPercentage(target)
	local halfcover = cover and cover == const.CoverLow and coverage > 80
	--print(coverage)
	if halfcover then self:AddStatusEffect("BipodUnfolded") else self:RemoveStatusEffect("BipodUnfolded")  end
	if self.stance ~= "Prone" and not halfcover then
		self:DoChangeStance("Prone")
	end
	self:AddStatusEffect("StationedMachineGun")
	self:UpdateHidden()
	self:FlushCombatCache()
	self:RecalcUIActions(true)
	ObjModified(self)
	return self:MGTarget(action_id, cost_ap, args)
end 		

function Unit:MGPack()
	self:InterruptPreparedAttack()
	self:RemoveStatusEffect("StationedMachineGun")
	self:RemoveStatusEffect("BipodUnfolded")
	self:UpdateHidden()
	self:FlushCombatCache()
	self:RecalcUIActions(true)
	if HasPerk(self, "KillingWind") then
		self:RemoveStatusEffect("FreeMove")
		self:AddStatusEffect("FreeMove")
	end
	ObjModified(self)
end

function Unit:UpdateMeleeTrainingVisual()
	local contour_visible
	if g_Combat and #GetEnemies(self) > 0 and not HasCombatActionInProgress(self) then
		contour_visible = self:CanUseMeleeTraining() and (self:IsNPC() or IsCompetitiveGame() and NetPlayerSide() ~= self.team.side and (self:SeenByTeam("player1") or self:SeenByTeam("player2")))
	end
	
	if contour_visible then
		local pos = self:GetPos()
		if not IsValid(self.melee_threat_contour) or self.melee_threat_contour:GetDist(pos) > 0 then
			local voxels = GetMeleeRangePositions(self)
			voxels = voxels or { }
			table.insert(voxels, point_pack(self:GetPos()))
			local is_ally = self.team.side == "player1" or self.team.side == "player2"
			if not IsValid(self.melee_threat_contour) then
				self.melee_threat_contour = MeleeAOEVisuals:new({vstate = "Deployed"}, nil, {voxels = voxels, pos = pos, mode =  is_ally and "Ally" or "Enemy"})
			else
				self.melee_threat_contour:Init({voxels = voxels, pos = pos, mode =  is_ally and "Ally" or "Enemy"})
			end
		end
	elseif not contour_visible and IsValid(self.melee_threat_contour) then
		DoneObject(self.melee_threat_contour)
		self.melee_threat_contour = nil
	end
end

function Unit:GetOverwatchAttacksAndAim(action, args, unit_ap)
	action = action or CombatActions.Overwatch
	local weapon = action:GetAttackWeapons(self)
	local attack = self:GetDefaultAttackAction()
	unit_ap = unit_ap or (g_Combat and self:GetUIActionPoints() or self:GetMaxActionPoints())
	args = table.copy(args)
	args.action_cost_only = true


	local minAim, maxAim = self:GetBaseAimLevelRange(attack)

	local aim = Min(minAim + 1,maxAim)

--	if IsKindOf(weapon, "SniperRifle") then
--		aim = maxAim
--	end

	if IsKindOf(weapon, "AssaultRifle", "MachineGun") then
		aim = Min(aim + 1,maxAim)
	end
	if IsKindOfClasses(weapon, "SniperRifle") then
		aim = Min(aim + 2,maxAim)
	end


	if IsKindOfClasses(weapon, "SniperRifle") then
		aim = maxAim
	end



	local cost = action:GetAPCost(self, args) 
	if cost < 0 then
		return 1
	end

	args.aim = aim


	local ap = unit_ap - cost
	--local atk_cost = attack:GetAPCost(self, args) 
	local atk_cost = attack:GetAPCost(self, args) 
	--print(atk_cost)

	local attacks = 1 + ap / atk_cost

	if IsKindOf(weapon, "SniperRifle") then
		attacks = 1
	end
	attacks = self:CallReactions_Modify("OnCalcOverwatchAttacks", attacks, action, args)
	--print(weapon.DisplayName..' aim '..aim.." maxAim "..maxAim)
	
	return attacks, aim or minAim or 0
end

local l_get_throwable_knife

function Unit:GetThrowableKnife()
	l_get_throwable_knife = nil
	self:ForEachItemInSlot(self.current_weapon, function(item)
		if IsKindOf(item, "MeleeWeapon") and item.CanThrow then
			l_get_throwable_knife = item
			return "break"
		end
	end)
	if not l_get_throwable_knife then
		local alt_set = self.current_weapon == "Handheld A" and "Handheld B" or "Handheld A"
		self:ForEachItemInSlot(alt_set, function(item)
			if IsKindOf(item, "MeleeWeapon") and item.CanThrow then
				l_get_throwable_knife = item
				return "break"
			end
		end)
		self:ForEachItemInSlot("KnifeInventory", function(item)
			if IsKindOf(item, "MeleeWeapon") and item.CanThrow then
				l_get_throwable_knife = item
				return "break"
			end
		end)

		
	end
	return l_get_throwable_knife
end

itemCombatSkillsList = {
	"ThrowGrenadeA",
	"ThrowGrenadeB",
	"ThrowGrenadeC",
	"ThrowGrenadeD",
	"ThrowGrenadeAG",
	"ThrowGrenadeBG",
	"ThrowGrenadeCG",
	"ThrowGrenadeDG",
	"ThrowGrenadeAO",
	"ThrowGrenadeBO",
	"Bandage",
	"ChangeWeapon",
	"RemoteDetonation"
}


function Unit:EnumUIActions()
	local actions = {}
	
	if g_Combat or (IsUnitPrimarySelectionCoOpAware(self) and not g_Overwatch[self]) then
		-- weapon attacks (from first weapon only)
		local action = self:GetDefaultAttackAction()
		actions[1] = action.id
		
		local main_weapon, offhand_weapon = self:GetActiveWeapons()		
		add_weapon_attacks(actions, self, main_weapon)
		
		-- allow dual-wielding with a flare gun
		if IsKindOf(main_weapon, "FlareGun") or IsKindOf(offhand_weapon, "FlareGun") then
			add_weapon_attacks(actions, self, offhand_weapon)
		end
		
		if self:GetThrowableKnife() then
			actions[#actions + 1] = "KnifeThrow"
			
		end

		if self:GetThrowableKnife() and g_Combat then
			actions[#actions + 1] = "MeleeAttack"
		end
		
		
		if table.find(actions, "DualShot") then
			-- special case: add left/right hand shot modes automatically
			table.insert_unique(actions, "LeftHandShot")
			table.insert_unique(actions, "RightHandShot")
		end
		
		if IsKindOf(main_weapon, "FirearmBase") then
			for slot, sub in sorted_pairs(main_weapon.subweapons) do
				add_weapon_attacks(actions, self, sub)
			end
			if main_weapon:HasComponent("EnableFullAuto") then
				table.insert_unique(actions, "AutoFire")
			end
			if main_weapon:HasComponent("EnableBurst") then
				table.insert_unique(actions, "BurstFire")
			end
		end
				
		if #actions == 0 then
			actions[1] = "UnarmedAttack"
		end
	end
	
	-- add signature abilities (if any)
	for _, skill in ipairs(Presets.CombatAction.SignatureAbilities) do
		local id = skill.id
		if string.match(id, "DoubleToss") then 
			id = "DoubleToss"
		end
		if id and self:HasStatusEffect(id) then
			actions[#actions + 1] = skill.id
		end
	end
	
	-- common actions
	ForEachPresetInGroup("CombatAction", "Default", function(def)
		actions[#actions + 1] = def.id
	end)

	if g_Combat or IsUnitPrimarySelectionCoOpAware(self) then
		-- actions from consumables
		if self:GetItemInSlot("Handheld A", "Grenade", 1, 1) then actions[#actions + 1] = "ThrowGrenadeA" end
		if self:GetItemInSlot("Handheld A", "Grenade", 2, 1) then actions[#actions + 1] = "ThrowGrenadeB" end
		if self:GetItemInSlot("Handheld B", "Grenade", 1, 1) then actions[#actions + 1] = "ThrowGrenadeC" end
		if self:GetItemInSlot("Handheld B", "Grenade", 2, 1) then actions[#actions + 1] = "ThrowGrenadeD" end
		if self:GetItemInSlot("GrenadesInventory", "Grenade", 1, 1) then actions[#actions + 1] = "ThrowGrenadeAG" end
		if self:GetItemInSlot("GrenadesInventory", "Grenade", 2, 1) then actions[#actions + 1] = "ThrowGrenadeBG" end
		if self:GetItemInSlot("GrenadesInventory", "Grenade", 3, 1) then actions[#actions + 1] = "ThrowGrenadeCG" end
		if self:GetItemInSlot("GrenadesInventory", "Grenade", 4, 1) then actions[#actions + 1] = "ThrowGrenadeDG" end
		if self:GetItemInSlot("OrdnanceInventory", "Grenade", 1, 1) then actions[#actions + 1] = "ThrowGrenadeAO" end
		if self:GetItemInSlot("OrdnanceInventory", "Grenade", 2, 1) then actions[#actions + 1] = "ThrowGrenadeBO" end

		if GetUnitEquippedMedicine(self) then
			actions[#actions + 1] = "Bandage"
		end
		
		if GetUnitEquippedDetonator(self) then
			actions[#actions + 1] = "RemoteDetonation"
		end
		
		-- todo: merc-related actions (perk/adrenaline skills)
	end

	actions[#actions + 1] = "ItemSkills"
	
	return actions
end


---Для контекста чтобы знать какие базовые атаки есть среди одиночный-очередь-автоогонь и тд
function Unit:GetBasicAttackModes()
	local result = {}
	local weapon, weapon2 = self:GetActiveWeapons()
	if not weapon then return result end

	local default_attack = self:GetDefaultAttackAction()

	local function find_mode(id, fallback_shots)
		for _, attack_id in ipairs(weapon.AvailableAttacks or empty_table) do
			if attack_id == id then
				local action = CombatActions[attack_id]
				if action:GetUIState({self}) == "enabled" then
					return {
						action = action,
						ap = action:GetAPCost(self),
						shots = fallback_shots or 1,
						mode = id
					}
				end
			end
		end
		return false
	end

	-- Основные режимы
	result.single = find_mode("SingleShot", 1)
	result.burst  = find_mode("BurstFire", weapon.BurstShots or 3) or find_mode("MGBurstFire", weapon.BurstShots or 3)
	result.auto   = find_mode("AutoFire", weapon.AutoShots or 5)
	result.buck   = find_mode("Buckshot", 1)
	result.double = find_mode("DoubleBarrel", 2)
	result.dual = find_mode("Dualshot", 2)

	-- Собрать всё
	result.all = {}
	for _, mode in pairs({result.single, result.burst, result.auto, result.buck, result.double,result.dual}) do
		if type(mode) == "table" and mode.mode then
			table.insert(result.all, mode)
		end
	end

	-- Если вообще ничего не найдено — fallback по default_attack
	if #result.all == 0 and default_attack then
		local mode = default_attack.id
		local shots = 1
		
		if mode == "BurstFire" then
			shots = weapon.BurstShots or 3
		elseif mode == "AutoFire" then
			shots = weapon.AutoShots or 5
		elseif mode == "Buckshot" then
			shots = weapon.BuckshotProjectiles or 6
		elseif mode == "DoubleBarrel" then
			local b = weapon.BuckshotProjectiles or 1
			shots = b * 2
		elseif mode == "DualShot" then
			shots = 2
		end

		table.insert(result.all, {
			action = default_attack,
			ap = default_attack:GetAPCost(self),
			shots = shots,
			mode = mode
		})
	end

	return result
end




function Unit:RecalcUIActions(force)
	local actions
	
	if self:GetBandageTarget() then
		actions = { "StopBandaging" }
	elseif self:HasStatusEffect("StationedMachineGun") or self:HasStatusEffect("ManningEmplacement") then
		actions = {}
		local action = self:GetDefaultAttackAction()
		actions[#actions + 1] = action.id
		ForEachPresetInGroup("CombatAction", "MachineGun", function(def)
			if def.id ~= "MGSetup" then
				actions[#actions + 1] = def.id
			end
		end)
		
		-- additional available actions
		actions[#actions + 1] = "Reload"
		actions[#actions + 1] = "Unjam"
	else
		actions = self:EnumUIActions() 
		if not actions then -- EnumUIActions decided to swap
			return
		end
	end
	
	-- move hidden actions to the back and mark actions visible in ui
	local ui_actions = {}
	local vis_idx = 1
	local old_actions = self.ui_actions
	self.ui_actions = ui_actions

	if actions then
		table.sort(actions, function(a, b)
			local actionA = CombatActions[a]
			local actionB = CombatActions[b]
			return actionA.SortKey < actionB.SortKey
		end)

		-- First pass, find actions which combine into firing modes.
		-- This should setup the right default attack action as well.
		local firingModes = {}
		for i = 1, #actions do
			local id = actions[i]
			local caction = CombatActions[id]
			local state = "hidden"
			
			local firingModeId = caction.FiringModeMember
			if not firingModeId then goto continue end

			if caction.ShowIn == "CombatActions" and (g_Combat or (#(Selection or empty_table) == 1 or caction.MultiSelectBehavior ~= "hidden")) then
				local target = caction.RequireTargets and caction:GetDefaultTarget(self)
				state = caction:GetVisibility({self}, target)
			end

			if state ~= "hidden" then
				if not firingModes[firingModeId] then
					firingModes[firingModeId] = {}
				end
				table.insert(firingModes[firingModeId], id)
				ui_actions[id] = state
			end

			::continue::
		end
		
		-- Check if dual shot attack mode is active.
		-- This has higher priotity because it disables other firing modes
		local dual_shot_state
		for modeName, mode in pairs(firingModes) do
			if modeName == "AttackDual" then
				for i, m in ipairs(mode) do
					if ui_actions[m] == "enabled" then
						dual_shot_state = "enabled"
					end
				end
			end
		end
		
		-- Show firing mode action only if more than one action is available.
		for modeName, mode in pairs(firingModes) do
			local defaultFireMode = mode[1]
			if #mode > 1 and (modeName ~= "AttackDual" or dual_shot_state ~= "hidden") then
				ui_actions[modeName] = "enabled"
				
				-- Weapon default
				local defaultAction = self:GetDefaultAttackAction(false, "force_ungrouped")
				if defaultAction.FiringModeMember == modeName and ui_actions[defaultAction.id] == "enabled" then
					defaultFireMode = defaultAction.id
				else
					-- First enabled.
					for i, m in ipairs(mode) do
						if ui_actions[m] == "enabled" then
							defaultFireMode = m
							break
						end
					end
				end
			else
				ui_actions[modeName] = "disabled"
			end
			
			-- When showing dual attacking hide other firing modes
			if modeName ~= "AttackDual" and dual_shot_state == "enabled" then
				ui_actions[modeName] = "hidden"
				for i, m in ipairs(mode) do
					ui_actions[m] = "hidden"
				end
			elseif dual_shot_state ~= "enabled" and modeName == "AttackDual" then
				for i, m in ipairs(mode) do
					ui_actions[m] = "hidden"
				end
			end

			mode.take_idx_from = mode[1]
			ui_actions[modeName .. "default"] = defaultFireMode
			assert(ui_actions[modeName .. "default"])	
		end

		local doubleTossCount = 0
		local grenadeModes = {}
		for i = 1, #actions do
			local id = actions[i]
			local caction = CombatActions[id]
			
			local state = "hidden"
			if caction.ShowIn == "CombatActions" or caction.ShowIn == "SignatureAbilities" then
				if ui_actions[id] then
					state = ui_actions[id]
				elseif g_Combat or (#(Selection or empty_table) == 1 or caction.MultiSelectBehavior ~= "hidden") then
					local target = caction.RequireTargets and CombatActionGetOneAttackableEnemy(caction, self)
					state = caction:GetVisibility({self}, target)
				end
			end

			-- special-case grenade throws in case multiple identical grenades are equipped
			if state ~= "hidden" then -- todo: remove this special case, make it generic, it causes issues with displaying signatures
				local action_type
				if string.match(id, "DoubleToss") then 
					action_type = "DoubleToss"
				elseif string.match(id, "ThrowGrenade") then
					action_type = "ThrowGrenade"
				end
				if action_type then
					grenadeModes[action_type] = grenadeModes[action_type] or {}
					local weapon = caction:GetAttackWeapons(self)
					if not weapon or grenadeModes[action_type][weapon.class] then
						state = "hidden"
						if action_type == "DoubleToss" then
							doubleTossCount = doubleTossCount + 1
							if doubleTossCount == 4 then
								state = "disabled"
							end
						end
					end
					if weapon then
						grenadeModes[action_type][weapon.class] = grenadeModes[action_type][weapon.class] or {}
						local equipped = self.current_weapon == "Handheld A" and (id == "ThrowGrenadeA" or  id == "ThrowGrenadeB") or
						                 self.current_weapon == "Handheld B" and (id == "ThrowGrenadeC" or  id == "ThrowGrenadeD") or
										 (id == "ThrowGrenadeAG" or  id == "ThrowGrenadeBG" or  id == "ThrowGrenadeCG" or  id == "ThrowGrenadeDG"
										or id == "ThrowGrenadeAO" or  id == "ThrowGrenadeBO")
						grenadeModes[action_type][weapon.class][id] = equipped
					end
				end
			end

			if state ~= "hidden" then
				local firingModeId = caction.FiringModeMember
				if firingModeId and ui_actions[firingModeId] == "enabled" then
					-- Firing mode actions are shown in the position of the first action in the mode,
					-- the mode actions themselves are not shown.
					if firingModes[firingModeId].take_idx_from == id then
						table.insert(ui_actions, vis_idx, firingModeId)
						vis_idx = vis_idx + 1
					end
				elseif CombatActions[id].group ~= "Hidden" then
					table.insert(ui_actions, vis_idx, id)
					vis_idx = vis_idx + 1
				end
				ui_actions[id] = state
			elseif caction.ShowIn ~= "Special" and not caction.ShowIn then
				ui_actions[#ui_actions + 1] = id
			end
		end
		
		--go through the grenade modes to place equipped in ui_actions with priority (to first consume from equipped nades)
		for action, _ in pairs(grenadeModes) do
			for grenadeType, _ in pairs(grenadeModes[action]) do
				for actionName, _ in pairs (grenadeModes[action][grenadeType]) do
					if grenadeModes[action][grenadeType][actionName] and not table.find(ui_actions, actionName) then
						for otherActionName, _ in pairs (grenadeModes[action][grenadeType]) do
							if table.find(ui_actions, otherActionName) then
								ui_actions[otherActionName] = nil
								ui_actions[actionName] = "enabled"
								ui_actions[table.find(ui_actions, otherActionName)] = actionName
								break
							end
						end
					end
				end
			end
		end
	end
	
	-- Put the signature ability in the 13th place always
	for i, id in ipairs(ui_actions) do 
		local caction = CombatActions[id]
		if caction.group == "SignatureAbilities" then
			if ui_actions[13] then
				local swapped = table.remove(ui_actions, 13)
				ui_actions[i] = swapped
				ui_actions[13] = id
			else
				table.remove(ui_actions, i)
				if #ui_actions < 12 then
					for j = #ui_actions + 1, 12 do
						ui_actions[j] = "empty"
					end
				end
				ui_actions[13] = id
			end
			break
		end
	end
	
	if vis_idx >30 then
		-- Remove item skills. They will be represented by ItemSkills.
		for i, itemSkill in ipairs(itemCombatSkillsList) do
			if ui_actions[itemSkill] then
				local actionIdx = table.find(ui_actions, itemSkill)
				if actionIdx then
					table.remove(ui_actions, actionIdx)
					vis_idx = vis_idx - 1
				end
			end
		end
		vis_idx = vis_idx + 1
	else
		ui_actions["ItemSkills"] = false
	end
	
	assert(vis_idx <= 30, "This unit has too many actions - they cant fit on the UI! (12)")

	if self == Selection[1] then
		local allMatch = false
		-- Verify that any actions have changed.
		if old_actions then
			allMatch = true
			for i, a in ipairs(old_actions) do
				if ui_actions[i] ~= a or old_actions[a] ~= ui_actions[a] then
					allMatch = false
					break
				end
			end
		end
		if not allMatch or force then ObjModified("combat_bar") end
	end
	return ui_actions
end

function Unit:GetActiveWeapons(class, strict_order)
	if class == "UnarmedWeapon" then
		self.unarmed_weapon = self.unarmed_weapon or g_UnarmedWeapon
		return self.unarmed_weapon, nil, { self.unarmed_weapon }
	end

	if self:GetStatusEffect("ManningEmplacement") then
		local handle = self:GetEffectValue("hmg_emplacement")
		local obj = HandleToObject[handle]
		if obj and obj.weapon and (not class or IsKindOf(obj.weapon, class)) then
			obj.weapon.emplacement_weapon = true
			return obj.weapon, nil, { obj.weapon }
		end
	end
	
	local slot
	if IsSetpiecePlaying() and IsSetpieceActor(self) then
		slot = "SetpieceWeapon"
	else
		slot = self.current_weapon
	end

	self.combat_cache = self.combat_cache or {}
	local key = string.format("%s_%s%s", slot, class or "all", strict_order and "-strict" or "")
	local weapons = self.combat_cache[key]
	if not weapons then
		weapons = {}
		local firearms = {}
		self.combat_cache[key] = weapons
		local equipped = self:GetEquippedWeapons(slot)
		if slot == "SetpieceWeapon" and (#(equipped or empty_table) == 0) then
			equipped = self:GetEquippedWeapons(self.current_weapon)
		end

		for _, o in ipairs(equipped) do
			local match = not class or (class ~= "Firearm") or not IsKindOfClasses(o, "HeavyWeapon", "FlareGun")
			match = match and (not class or IsKindOf(o, class))
			if match then
				table.insert(weapons, o)
			end
			if IsKindOf(o, "FirearmBase") then
				table.insert(firearms, o)
			end
		end		
		-- second pass to add subweapons at the end of the list
		for _, item in ipairs(firearms) do
			for slot, weapon in sorted_pairs(item.subweapons) do
				local match = not class or (class ~= "Firearm") or not IsKindOfClasses(weapon, "HeavyWeapon", "FlareGun")
				match = match and (not class or IsKindOf(weapon, class))
				if match then
					table.insert(weapons, weapon)
				end
			end
		end
	end
	
	-- If weapon1 is exhausted and weapon 2 isnt then weapon2 is the main weapon
	if not strict_order then
		local weapon1Exhausted = not self:CanUseWeapon(weapons[1])
		local weapon2Exhausted = not self:CanUseWeapon(weapons[2])
		local weapon2IsntSubWeapon = weapons[1] and weapons[2] and not weapons[2].parent_weapon
		if weapons[1] and weapons[2] and weapon1Exhausted and not weapon2Exhausted and weapon2IsntSubWeapon then
			weapons[1], weapons[2] = weapons[2], weapons[1]
		end
	end
	
	return weapons[1], weapons[2], weapons
end


local function lGetUnitQuickSlotItem(unit, item_id)
local	l_get_unit_quick_slot_item = nil
	
	local filter = function(o)
		if o.Condition > 0 and (not l_get_unit_quick_slot_item or o.Condition < l_get_unit_quick_slot_item.Condition) then
			l_get_unit_quick_slot_item = o
		end
	end
	
	unit:ForEachItemInSlot("Handheld A", item_id, filter)
	unit:ForEachItemInSlot("Handheld B", item_id, filter)
	unit:ForEachItemInSlot("Inventory", item_id, filter)
	unit:ForEachItemInSlot("PocketInventory", item_id, filter)
	
	return l_get_unit_quick_slot_item
end

function GetUnitLockpick(unit)
	local tool = lGetUnitQuickSlotItem(unit, "LockpickBase")
	return tool and not tool:IsCondition("Broken") and tool
end

function GetUnitCrowbar(unit)
	local tool = lGetUnitQuickSlotItem(unit, "CrowbarBase")
	return tool and not tool:IsCondition("Broken") and tool
end

function GetUnitWirecutter(unit)
	local tool = lGetUnitQuickSlotItem(unit, "WirecutterBase")
	return tool and not tool:IsCondition("Broken") and tool
end


local constRandomizationStats = 3
function UnitData:RandomizeStats(seed)
	local stats = GetUnitStatsCombo()
	local unit_def = UnitDataDefs[self.class]

	

	local rand
	for _, stat in ipairs(stats) do
		if stat == "Marksmanship" or stat == "Agility" or stat == "Dexterity" or stat == "Strength" or stat == "Health" then constRandomizationStats = 3 else constRandomizationStats = 12 end

		rand, seed = BraidRandom(seed, 2 * constRandomizationStats + 1)
		
		-- If the stat will be brought to or below 0 then
		-- clamp it to 0 if it was already 0 or 1 if it wasn't.
		local unitStat = self[stat]
		local modValue = rand - constRandomizationStats
		if unitStat - modValue <= 0 then
			modValue = unitStat == 0 and 0 or -(self[stat] - 1)
		end
		
		self:AddModifier("randstat", stat, false, modValue)

		if Game.game_difficulty == "VeryHard" then
			rand, seed = BraidRandom(seed, 20)
			local modValue = rand+10
			self:AddModifier("randstat", stat, false, modValue)
		end
	end
end




function GainStat(unit, stat, gainAmount, modId, reason)
	assert(stat)
	if unit:IsDead() then return end
	local unitData = gv_UnitData[unit.session_id]
	local unit = g_Units[unit.session_id]
	gainAmount = gainAmount or 1
	reason = reason or "FieldExperience"
	
	modId = modId or string.format("StatGain-%s-%s-%d", stat, unitData.session_id, GetPreciseTicks())
	local mod = unitData:AddModifier(modId, stat, false, gainAmount)
	if unit then
		unit:AddModifier(modId, stat, false, gainAmount)
	end
	Msg("ModifierAdded", unitData, stat, mod)
	
	local unitName = unitData:GetLogName()
	local statName = table.find_value(UnitPropertiesStats:GetProperties(), "id", stat).name
	if reason ~= "Training" then
		CombatLog("important", T{124938068325, "<em><unit></em> gained +<amount> <em><stat></em>",
			unit = unitName,
			stat = statName,
			amount = gainAmount
		})
	end
	if stat == "Health" then
		if unit then
			RecalcMaxHitPoints(unit)
		end
		RecalcMaxHitPoints(unitData)
	end

	if stat == "Will" then
		if unit then
			RecalcMaxWillPoints(unit)
		end
		RecalcMaxWillPoints(unitData)
	end

	ObjModified(unit)
	ObjModified(unitData)
	
	Msg("StatIncreased", unitData, stat, gainAmount, reason)
	PlayFX("StatIncreased", "start", stat)
	return stat
end


function Unit:ApplySuppressionStatus()
	


		--local unitData = gv_UnitData[self.session_id]
		if self.species ~= "Human" then return end
		RecalcMaxWillPoints(self)
		local MaxWillPoints =  self.MaxWillPoints or self.Will


--		print(self.WillPoints)
--		print(MaxWillPoints)
		
		local WPpercent = MulDivRound(self.WillPoints, 100, MaxWillPoints) or 0
		WPpercent = Clamp(WPpercent, 0, 100)
		local morale = self:GetPersonalMorale() or 0
		WPpercent = WPpercent - morale*3
--		print(WPpercent)

		

	if HasPerk(self, "Psycho") and (self.WillPoints) <= 10 then
	    self:AddStatusEffect("Berserk")
		self.WillPoints = self.MaxWillPoints
		return
	end		

	if HasPerk(self, "Psycho")  then
		return
	end	

		
	local suppression_levels = {
		{threshold = 10, effect = "suppressionPinned"},
		{threshold = 25, effect = "suppressionHeavy2"},
		{threshold = 40, effect = "suppressionHeavy"},
		{threshold = 55, effect = "suppressionMedium"},
		{threshold = 70, effect = "suppressionLight"},
	}

	local applied = false
	for i, data in ipairs(suppression_levels) do
		if WPpercent <= data.threshold then
			if not self:HasStatusEffect(data.effect) then
				self:AddStatusEffect(data.effect)
			end
			applied = data.effect
			break
		end
	end

	-- Удалим все прочие suppression-эффекты
	local effects = {
		"suppressionLight", "suppressionMedium", "suppressionHeavy",
		"suppressionHeavy2", "suppressionPinned"
	}
	for _, fx in ipairs(effects) do
		if fx ~= applied then
			self:RemoveStatusEffect(fx, "all")
		end
	end

	--	if self.WillPoints <= 10 then
	--		self:SetActionCommand("TakeCover")
	--	end
	ObjModified(self)
end


	--function OnMsg.OnAttack()
	--	for _, unit in ipairs(g_Units) do
	--		unit:ApplySuppressionStatus()
	--	end
	--end

	

	local KeepAimIKCommands = {
		Idle = true,
		AimIdle = true,
		OpportunityAttack = true,
		PreparedAttackIdle = true,
		ExecFirearmAttacks = true,
		HeavyWeaponAttack = true,
		FirearmAttack = true,
	}
	
	
	---
--- Called at the start of a unit's command.
--- This function performs various setup and initialization tasks at the start of a unit's command, such as:
--- - Interrupting the current command if the unit was previously interrupted
--- - Resetting various state variables related to the unit's movement and visual styles
--- - Unblocking any tunnels the unit may have been traversing
--- - Setting the unit's gravity to 0 and stopping any current movement
--- - Clearing the unit's path and adjusting its position if it was traversing a tunnel
--- - Disabling weapon light effects and aim IK if the current command does not require them
--- - Setting the unit's foot plant state and beginning interruptable movement if the command is interruptable
--- - Setting the unit's aim FX and combat action state
---
--- @function Unit:OnCommandStart
--- @return nil
function Unit:OnCommandStart()
	if self.interrupted then
		self:InterruptEnd()
	end
	self.cur_idle_style = false
	self.cur_move_style = false
	self.goto_target = false
	self.goto_stance = false
	self.goto_hide = false
	self.visibility_override = false
	self.passed_interrupts = nil
	self:TunnelsUnblock()
	self.action_visual_weapon = false
	if IsValid(self) then
		self:SetGravity(0)
		self:StopMoving()
		self.interrupted = false
		if not self:IsDead() and not IsActivePaused() and not IsSetpieceActor(self) then
			self:ClearPath()
			if self.traverse_tunnel then
				local tpos = self.traverse_tunnel:GetExit()
				if tpos then
					local pos = GetPassSlab(tpos) or FindPassable(tpos, 0, -1, -1, const.pfmVoxelAligned) or tpos
					self:SetPos(pos)
				end
			end
		end
		if not KeepAimIKCommands[self.command] then
			--self:SetWeaponLightFx(false)
			self:SetIK("AimIK", false)
		end
		self:SetIK("LookAtIK", false)
		if not self.interruptable and self.command then
			self:BeginInterruptableMovement()
		end
		self:SetFootPlant(true)
	end
	self.traverse_tunnel = false
	self:SetAimFX(false, self.command and "delayed")
	if self.action_command then
		SetCombatActionState(self, self.command == self.action_command and "start" or nil)
	end
end


function Unit:Idle()
	self:WaitResumeOnCommandStart()
	assert(self:IsValidPos())
	SetCombatActionState(self, nil)
	self.being_interacted_with = false
	if not self.move_attack_in_progress then
		self.move_attack_target = nil
	end	
	self:SetQueuedAction()
	ExplorationClearExclusiveAction(self)

	if self:IsDead() then
		if self.behavior == "Despawn" then
			self:SetCommand("Despawn")
		elseif self.behavior ~= "Hang" and self.behavior ~= "Dead" then
			self:SetBehavior("Dead")
			self:SetCombatBehavior("Dead")
		end
	else
		if self.stance == "Prone" and self:GetValidStance("Prone") ~= "Prone" then
			self:DoChangeStance("Crouch")
		end
		if g_Combat and self:CanCower() and (self.team.side == "neutral" or self:HasStatusEffect("ForceCower")) and not g_Combat:ShouldEndCombat() then
			self:SetCommand("Cower")
		end
	end
	self:UpdateInWaterFX()

	if self:IsDead() then
		if self.behavior == "Hang" then
			self:SetCommand("Hang")
		else
			assert(not self.Squad or IsMerc(self))
			self:SetCommand("Dead")
		end
	end
	FallDownCheck(self)
	if self:HasStatusEffect("Unconscious") then
		self:SetCommand("Downed")
	elseif IsSetpieceActor(self) then
		self:SetCommand("SetpieceIdle", true)
	elseif self:HasStatusEffect("Suspicious") then
		if g_Combat then
			self:RemoveStatusEffect("Suspicious")
		else
			return self:SuspiciousRoutine()
		end
	elseif self:HasCommandsInQueue() then
		return
	elseif g_Combat and self.combat_behavior then
		self:SetCommand(self.combat_behavior, table.unpack(self.combat_behavior_params or empty_table))
	elseif not g_Combat and self.behavior and not self:HasStatusEffect("Suspicious") then
		local enemy = self:GetCommandParam("idle_forcing_dist")
		if not IsValid(enemy) or not self:IdleForcingDist(enemy) then
			self:SetCommandParamValue(self.command, "idle_forcing_dist", nil)
			self:SetCommand(self.behavior, table.unpack(self.behavior_params or empty_table))
		end
	end

	-- setup target dummy
	local anim_style = self:GetIdleStyle()
	local base_idle = anim_style and anim_style:GetMainAnim() or self:GetIdleBaseAnim()
	local can_reposition = not (g_Combat and self:IsAware()) -- if large units can change angle (occupied tiles)
	local pos, orientation_angle
	if self.return_pos and not self.play_sequential_actions then
		pos = self.return_pos
		local voxel = SnapToVoxel(self)
		if not pos:Equal2D(voxel) then
			orientation_angle = CalcOrientation(pos, voxel)
		end
	else
		pos = GetPassSlab(self) or self:GetPos()
	end
	local dummy_orientation_angle = self:GetPosOrientation(pos, nil, self.stance, true, can_reposition)
	if not orientation_angle then
		orientation_angle = self.auto_face and dummy_orientation_angle or self:GetPosOrientation(pos, nil, self.stance, false, can_reposition)
	end
	self:SetTargetDummy(pos, dummy_orientation_angle, base_idle, 0)

	if g_Combat and (not self:IsNPC() or self:IsAware()) then
		Msg("Idle", self)
	end
	if self.aim_action_id and not HasCombatActionInProgress(self) then
		self:SetCommand("AimIdle")
	end
	--self:SetWeaponLightFx(false)
	self:SetIK("AimIK", false)
	if self.play_sequential_actions then
		self:SetCommand("SequentialActionsIdle")
	end

	-- orient
	if not GameTimeAdvanced then
		self:SetOrientationAngle(orientation_angle)
	else
		self:EndInterruptableMovement()
		self:PlayTransitionAnims(base_idle, orientation_angle)
		self:AnimatedRotation(orientation_angle, base_idle)
		self:BeginInterruptableMovement()
	end

	self:SetCommandParamValue("Idle", "move_anim", "WalkSlow")
	if self:ShouldBeIdle() then
		-- one animation cycle
		-- play current style end animation
		self.cur_idle_style = anim_style and anim_style.Name or nil
		if anim_style then
			local anim = self:GetStateText()
			if anim_style:HasAnimation(anim) then
				if self:GetAnimPhase() ~= 0 and not self:IsAnimEnd() then
					Sleep(self:TimeToAnimEnd())
				end
			elseif anim == anim_style.Start then
				Sleep(self:TimeToAnimEnd())
			elseif (anim_style.Start or "") ~= "" and IsValidAnim(self, anim_style.Start) then
				self:SetState(anim_style.Start, const.eKeepComponentTargets)
				Sleep(self:TimeToAnimEnd())
			end
			self:SetState(anim_style:GetRandomAnim(self), const.eKeepComponentTargets)
			if not GameTimeAdvanced then
				self:RandomizeAnimPhase()
			end
		else
			if self:GetAnimPhase(1) == 0 or self:IsAnimEnd() or not IsAnimVariant(self:GetStateText(), base_idle) then
				self:SetRandomAnim(base_idle, const.eKeepComponentTargets, nil, true)
			end
		end
		Sleep(self:TimeToAnimEnd())
	else
		self:IdleRoutine()
	end
end


	---
--- Rolls a skill check for the given unit and skill, with optional modifiers.
---
--- @param unit UnitPropertiesStats The unit performing the skill check.
--- @param skill string The name of the skill being checked.
--- @param modifier number (optional) A percentage modifier to apply to the skill value.
--- @param add number (optional) A value to add to the skill value.
--- @return boolean True if the skill check passes, false otherwise.
---
function RollSkillCheck(unit, skill, modifier, add)
	assert(IsKindOf(unit, "UnitPropertiesStats"))
	
	modifier = modifier or 100
	add = add or 0
	
	local roll = 1 + unit:Random(100)
	--adjust roll based on diff
	--local adjustRoll = GameDifficulties[Game.game_difficulty]:ResolveValue("rollSkillCheckBonus") or 0
	local adjustRoll = 5 * unit:GetPersonalMorale()
	roll = roll + adjustRoll
	roll = Min(roll, 100)
	
	local value = MulDivRound(unit[skill], modifier, 100) + add
	local pass = roll < value or CheatEnabled("SkillCheck")
	
	--CombatLog("debug", 
	local t_res = pass and Untranslated("<em>Pass</em>") or Untranslated("<em>Fail</em>")
	local meta = unit:GetPropertyMetadata(skill)
	local t_skill = meta.name
	if modifier ~= 100 then
		if add > 0 then
			t_skill = T{816405633181, "<percent(n1)> <skill>+<n2>", n1 = modifier, n2 = add, skill = meta.name}
		elseif add < 0 then
			t_skill = T{656059859333, "<percent(n1)> <skill><n2>", n1 = modifier, n2 = add, skill = meta.name}
		else
			t_skill = T{570928040607, "<percent(number)> <skill>", number = modifier, skill = meta.name}
		end
	elseif add > 0 then
		t_skill = T{481345361355, "<skill>+<number>", number = add, skill = meta.name}
	elseif add < 0 then
		t_skill = T{945399039468, "<skill><number>", number = add, skill = meta.name}
	end
	
	CombatLog("debug", T{Untranslated("<em><name><em> Skill check (<em><skill></em>) <roll>/<target>: <result>"), 
		name = unit:GetLogName(),
		skill = t_skill,
		roll = roll, 
		target = value,
		result = t_res,
	})
	return pass
end

function SkillCheck(unit, skill, threshold,dont_report_fails)
	if not unit or not IsKindOf(unit, "UnitPropertiesStats") then return "error" end
	local stat = unit[skill] + 5 * unit:GetPersonalMorale()
	if not stat then return "error" end
	if threshold <= stat or CheatEnabled("SkillCheck") then
		CombatLog("debug", "(success) " .. unit.session_id .. " " .. skill.. " check (" .. stat.. " / " ..threshold .. ")")
		PlayFX("SkillCheck", "success", unit, skill)
		return "success", stat - threshold, stat
	end	
	if not dont_report_fails then
		PlayFX("SkillCheck", "fail", unit, skill)
		CombatLog("debug", "(fail) " .. unit.session_id .." " .. skill.. " check (" .. stat.. " / " ..threshold .. ")")
	end
	return "fail", threshold - stat, stat
end




function Unit:UpdateMoveSpeed()
	local modifier = self:CalcMoveSpeedModifier()
	local speed
	if not g_Combat and self:IsMerc() then
		local move_anim = GetStateName(self:GetMoveAnim())
		local is_running = string.match(move_anim, ".*Run.*") and true or false
		if is_running then
			-- fixed speed for mercs
			if self.stance == "Standing" then
				speed = const.UnitMoveSpeed.MercStandingStance
			elseif self.stance == "Crouch" then
				speed = const.UnitMoveSpeed.MercCrouchStance
			elseif self.stance == "Prone" then
				speed = const.UnitMoveSpeed.MercProneStance
			end
		else
			if self.stance == "Standing" then
				speed = const.UnitMoveSpeed.MercWalk
			end
		end
	end
	if speed then
		local mod = MulDivRound(modifier, self:GetAnimSpeedModifier(), 1000)
		if g_Combat and not self:isMerc() then
			mod = mod * 2
		end
		speed = MulDivRound(speed, mod, 1000)
		self:SetSpeed(speed)
	else
		self:SetMoveSpeed(modifier)
	end
	-- debug set speed on zero speed animations
	if self:GetSpeed() == 0 then
		self:SetSpeed(self.fallback_walk_speed)
	end
end


---
--- Handles the death of a unit, including determining if the unit should get downed instead of dying.
---
--- @param attacker Unit|Trap The attacker that caused the unit's death.
--- @param hit_descr table The hit description containing information about the damage that caused the death.
---
function Unit:OnDie(attacker, hit_descr)
	CombatActionInterruped(self)
	RemoveFloatingTextsFrom(self, "DamageFloatingText")
	self.on_die_attacker = IsKindOf(attacker, "Trap") and attacker.attacker or attacker
	self.on_die_hit_descr = table.copy(hit_descr)
	self.on_die_hit_descr.armor_decay = nil
	self.on_die_hit_descr.armor_pen = nil
	
	if self:ShouldGetDowned(hit_descr) then
		hit_descr.explosion_fly = nil -- never do this when downing
		self.HitPoints = 1 -- make sure the unit is not considered dead and evicted from the UI
		local value = MulDivRound(self.Health,50,100) or 30
		if g_Combat then self:ApplyTempHitPoints(value) end
		--count downed units for tacticalsituation vr
		if attacker and IsKindOf(attacker, "Unit") and attacker.team.side ~= self.team.side then
			self.team.tactical_situations_vr.downedUnits = self.team.tactical_situations_vr.downedUnits and self.team.tactical_situations_vr.downedUnits 
			attacker.team.tactical_situations_vr.downedUnitsByTeam = attacker.team.tactical_situations_vr.downedUnitsByTeam and (attacker.team.tactical_situations_vr.downedUnitsByTeam + 1) or 1
			PlayVoiceResponseTacticalSituation(table.find(g_Teams, attacker.team), "now")
		end
		self:SetCommand("GetDowned")
	else
		--printf("%s dies", _InternalTranslate(self.Name or ""))
		self.on_die_hit_descr = self.on_die_hit_descr or {}
		 -- Roam is considered visiting but doesn't have a last_visit
		 if self:IsVisiting() and self.last_visit and self.visit_reached then
			self.on_die_hit_descr.die_pos = self.last_visit:GetPos()
		end
		if string.match(self.session_id, "ClonedFootballPartner") then
			self.SetCommand = Unit.SetCommand
			self.zone.player_killed = true
		end
		if IsKindOf(self.last_visit, "AL_Football") then
			self.last_visit.player_killed = true
		end
		self:SetCommand("Die")
	end
end


---
--- Provokes an opportunity attack from the given object (obj) against the current unit.
--- This function handles the logic for triggering an overwatch attack, including setting the attack reason,
--- interrupting the current unit's movement, and setting up the attack arguments.
---
--- @param obj Unit The unit that is performing the opportunity attack.
--- @param attack_args table The attack arguments to be used for the opportunity attack.
--- @param target_dummy boolean Whether the current unit is a target dummy.
---
function Unit:ProvokeOpportunityAttack_Overwatch(obj, attack_args, target_dummy)
	local overwatch = g_Overwatch[obj]
	if not overwatch then return end
	--local action = CombatActions[overwatch.action_id]
	overwatch.triggered_by[self.handle] = true
	CombatLog("short", T{353305209140, "<LogName> was revealed by enemy overwatch", self})
	self:RemoveStatusEffect("Hidden")
	self:InterruptBegin()

	local reason = T(484641340197, "Overwatch")
	obj:SetAttackReason(reason, true)

	local cmd_thread = CurrentThread() == self.command_thread
	if cmd_thread then
		self:PushDestructor(function(self)
			obj:FinishOpportunityAttack_Overwatch()
		end)
	end
	attack_args.aim = overwatch.aim
	attack_args.origin_action_id = overwatch.origin_action_id
	assert(attack_args.target == self)
	attack_args.target_dummy = target_dummy
	attack_args.opportunity_attack = true
	attack_args.opportunity_attack_type = "Overwatch"
	if overwatch.cone_angle > 180*60 then
		attack_args.circular_overwatch = true
	end
	local lof_data, highestCth, highestCthPart
	for _, data in ipairs(attack_args.lof) do
		if data.ally_hits_count == 0 and data.target_spot_group == attack_args.target_spot_group then
			local cth = data.chance_to_hit
			if not highestCthPart or cth > highestCth then
				highestCthPart = data.target_spot_group
				highestCth = highestCth
				lof_data = data
			end
			
			break
		end
	end
	lof_data = lof_data or attack_args.lof[1]
	table.clear(attack_args.lof)

--	print(highestCthPart)
	lof_data.target_spot_group = highestCthPart
	--lof_data.target_spot_group = "Torso" -- treat resulting hits as if they hit the target in the torso
	attack_args.lof[1] = lof_data
	attack_args.target_spot_group = highestCthPart
	--attack_args.target_spot_group = "Torso"

	local status
	local num_attacks = HasPerk(obj, "Killzone") and 2 or 1

	for i = 1, num_attacks do
		local weapon = obj:GetActiveWeapons("Firearm")
		local default_action = obj:GetDefaultAttackAction("ranged", "ungrouped", nil, true, "ignore", {skip_ap_check = true})
		if not weapon or not default_action or not obj:CanAttack(self, weapon, default_action, 0, nil, "skip_ap_check") then
			break
		end
		overwatch.action_id = default_action.id
		if IsValidTarget(self) then
			if IsKindOf(obj.prepared_attack_obj, "AOEActionVisuals") then
				obj.prepared_attack_obj:SetState("activate", self:GetPos())
			end
			obj:SetCommand("OpportunityAttack", default_action.id, attack_args, status)
			if attack_args.circular_overwatch and obj.combat_behavior == "OverwatchAction" then
				local shot_vector = self:GetPos() - obj:GetPos()
				local target_pos = (obj:GetPos() + SetLen(shot_vector, overwatch.dist)):SetZ(overwatch.target_pos:z())
				local args = obj.combat_behavior_params[3]
				if args then 
					args.target = target_pos 
				end
 			end
			while not obj:IsIdleCommand() do
				WaitMsg("Idle", 100)
			end
		end
	end

	if cmd_thread then
		self:PopDestructor()
	end
	obj:FinishOpportunityAttack_Overwatch()
end


function MarksmanshipInfluence(mrk)
  mrk = Clamp(mrk or 0, 0, 100)
  local infl = 0
  infl = infl + MulDivRound(Min(mrk, 60), 20, 60)
  if mrk > 60 then infl = infl + MulDivRound(Min(mrk - 60, 20), 20, 20) end
  if mrk > 80 then infl = infl + MulDivRound(Min(mrk - 80, 10), 20, 10) end
  if mrk > 90 then infl = infl + MulDivRound(Min(mrk - 90, 6),  20, 6)  end
  if mrk > 96 then infl = infl + MulDivRound(Min(mrk - 96, 4),  20, 4)  end
  return Clamp(infl, 0, 100)
end

function ScopeSkillEffPct(mrk)
  mrk = Clamp(mrk or 0, 0, 100)
  if mrk < 90 then return 50 end
  local t = mrk - 90 -- 0..10
  return 50 + DivRound(50 * t * t, 100)
end
