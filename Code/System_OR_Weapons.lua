
if FirstLoad then

	MapVar("g_SuppressionApplyThread", {})

    g_SuppressionApplyQueue = false
end

function QueueSuppressionApplication(unit, wp_dmg)
    if not g_SuppressionApplyQueue then
        g_SuppressionApplyQueue = {}
    end
    if not g_SuppressionApplyThread or not IsValidThread(g_SuppressionApplyThread) then
        g_SuppressionApplyThread = CreateGameTimeThread(function()
            while true do
                if g_SuppressionApplyQueue and #g_SuppressionApplyQueue > 0 then
                    local entry = table.remove(g_SuppressionApplyQueue, 1)
                    local u, dmg = entry.unit, entry.damage
                    if IsValid(u) then
						Sleep(10)
                        local old_wp = u.WillPoints
                        u.WillPoints = Max(0, old_wp - dmg)
                        if u.WillPoints ~= old_wp then
                            u:ApplySuppressionStatus()
                        end
                    end
                    Sleep(10)
                else
                    Sleep(10)
                end
            end
        end)
    end

    if IsValid(unit) and not HasPerk(unit, "Psycho") and wp_dmg > 0 then
        table.insert(g_SuppressionApplyQueue, {unit=unit, damage=wp_dmg})
    end
end



local function compile_ignore_colliders(killed_colliders, colliders)
	if #(killed_colliders or empty_table) == 0 then
		return colliders
	end
	local list = table.icopy(killed_colliders)
	if IsValid(colliders) then
		table.insert_unique(list, colliders)
	else
		for _, obj in ipairs(colliders) do
			table.insert_unique(list, obj)
		end
	end
	return list
end

local function find_first_hit(attack_results, hit_obj)
	for si, shot in ipairs(attack_results.shots) do
		for hi, hit in ipairs(shot.hits) do
			if hit.obj == hit_obj then
				return hit
			end
		end
	end
end

local function PerkHaveABlastAttackAndWeapon(unit)
	local actions = { "ThrowGrenadeA", "ThrowGrenadeB", "ThrowGrenadeC", "ThrowGrenadeD","ThrowGrenadeAG", "ThrowGrenadeBG", "ThrowGrenadeCG", "ThrowGrenadeDG","ThrowGrenadeAO", "ThrowGrenadeBO" }
	for _, id in ipairs(actions) do
		local action = CombatActions[id]
		local weapon = action:GetAttackWeapons(unit)
		if weapon then
			return action, weapon
		end
	end
end

function Firearm:GetOverwatchConeParam(param)
	if param == "Angle" then
		return self.OverwatchAngle
	elseif param == "MinRange" then
		--return IsKindOfClasses(self, "MachineGun") and self.WeaponRange or Max(2,MulDivRound(self.WeaponRange, 20, 100))
		return IsKindOfClasses(self, "BrowningM2HMG") and self.WeaponRange or Max(2,MulDivRound(self.WeaponRange, 20, 100))
	elseif param == "MaxRange" then
		--return IsKindOfClasses(self, "MachineGun") and self.WeaponRange or MulDivRound(self.WeaponRange, 80, 100)
		return MulDivRound(self.WeaponRange, 80, 100)	
	end
	assert(false, string.format("unknown Overwatch parameter '%s'", param))
end

local function CaliberModPropsCombo()
	local items = ClassModifiablePropsNonTranslatableCombo(g_Classes.Firearm)
	-- filter by category
	for i = #items, 1, -1 do
		local meta = Firearm:GetPropertyMetadata(items[i])
		if meta.category ~= "Caliber" then
			table.remove(items, i)
		end
	end
	return items
end

function FirearmBase:GetAutofireShots(action)
	if type(action) == "string" then
		action = CombatActions[action]
	end
	local shots = action:ResolveValue("num_shots") or 1
    --print(self.BurstShots)
	local shotsBoost = GetComponentEffectValue(self, "ExtraBurstShots", action.id)

    if (action.id) == "AutoFire" then 
		shots = self.AutoShots 
		if shotsBoost then shotsBoost = shotsBoost  end
	end
    if (action.id) == "BurstFire" then 
		shots = self.BurstShots 
		if shotsBoost then shotsBoost = shotsBoost  end
	end
	if (action.id) == "MGBurstFire" then 
		shots = self.AutoShots 
		if shotsBoost then shotsBoost = shotsBoost  end
	end
--	if IsKindOf(self, "Shotgun") then 
--		shots = self.AutoShots
--		if shotsBoost then shotsBoost = shotsBoost  end
--	end

--	print(action.id)
--	print(shots)

	--if shotsBoost then
	--	shots = shots + shotsBoost
	--end 
	return shots
end


function FirearmGetGrouping(item,dist_slab)
	local factory = item:GetFactoryResource()
	local max_res = item:GetMaxResource() or factory
	local curr_res = item:GetCurrentResource() or max_res

	if max_res <= 0 then max_res = 1 end
	if factory <= 0 then factory = 1 end

	local condition_mult = Clamp((curr_res + 0.2) / max_res, 0.0, 1)

	local repair_mult = Clamp(0.8 + 0.2 * max_res / factory, 0.1, 1)


	local grouping = item.Grouping or 10
	local effective_grouping = grouping * condition_mult * repair_mult

--	print("grouping debug")
--	print(curr_res/max_res)
--	print(factory,max_res,curr_res)
--	print(condition_mult,repair_mult)
--	print(grouping,effective_grouping)

	local groupingPerSlab = effective_grouping * 10
	local groupingResult = groupingPerSlab
	if dist_slab then
		groupingResult = DivRound(groupingPerSlab, dist_slab)
	end	

	return groupingResult
end

function FirearmBase:GetConditionPercent()
    local max_res = self:GetMaxResource()
    if max_res <= 0 then max_res = 1 end
    return Clamp(MulDivRound(self:GetCurrentResource(), 100, max_res), 0, 100)
end

function FirearmBase:GetBaseJamChanceRaw()
	local item = self.parent_weapon or self

	local resource = item:GetCurrentResource() or 1
	local max_resource = item:GetMaxResource() or item:GetFactoryResource() or 1000
	local factory = item:GetFactoryResource()

	if max_resource <= 0 then max_resource = 1 end

	local resourcefactor = factory * 0.25 + max_resource * 0.75

	local condition_percent = MulDivRound(resource, 100, resourcefactor)
	local reliability = item.Reliability or 50
	local base = item.BaseJamChance or 5

	-- ступенчатый множитель износа
	local degrade_mult = 1 + ((100 - condition_percent) / 100)^2.25 * 6

	if condition_percent <= 15 then degrade_mult = 24.0 end
	if condition_percent <= 40 then degrade_mult = 16.0 end
	if condition_percent <= 60 then degrade_mult = 8.0 end
	if condition_percent <= 80 then degrade_mult = 4.0 end

	local raw_chance = ((100 - reliability) + base) * degrade_mult



	-- модификаторы погоды
	if (GameState.RainHeavy or GameState.RainLight) and not item.indoors then
		raw_chance = MulDivRound(raw_chance, 100 + const.EnvEffects.RainJamChanceMod, 100)
	end

	return raw_chance
end

function FirearmBase:GetJamChance(attacker)
	local item = self.parent_weapon or self
	local jam_chance = self:GetBaseJamChanceRaw()
	

	if IsMerc(attacker) then
		local skill_bonus = ((attacker.Mechanical * 4 + attacker.Marksmanship + attacker.Wisdom + attacker:GetLevel())  / 3)
		jam_chance = jam_chance - skill_bonus
	else
		jam_chance = jam_chance - attacker.Mechanical * 3
	end

	return Clamp(jam_chance, 0, 10000)
end

function FirearmBase:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot
end

function FirearmBase:ReliabilityCheck(attacker, num_shots)
	local item = self.parent_weapon or self
	local resource = item:GetCurrentResource() or 1
	local max_resource = item:GetMaxResource() or item:GetFactoryResource() or 1000
	if max_resource <= 0 then max_resource = 1 end

	local loss = item:GetBaseDegradePerShot() or 1
	local jammed = false

	if not attacker.infinite_condition then
		local jam_chance = item:GetJamChance(attacker) -- уже учитывает ресурс и reliability
		local seed = Unit:Random()
		local random = BraidRandomCreate(seed)

		-- Погодные модификаторы увеличивают износ
		if (GameState.RainHeavy or GameState.DustStorm or GameState.FireStorm) and not attacker.indoors then
			loss = loss * 1.3
		elseif GameState.RainLight and not attacker.indoors then
			loss = loss * 1.1
		end

		--[[ Боты не теряют ресурс
		if not IsMerc(attacker) then
			loss = 0
		end]]

		if num_shots == 1 then
			jam_chance = jam_chance / 2
		end

		local base_roll = 1000
		local jam_roll = random(base_roll)

		if item.num_safe_attacks <= 0 and jam_roll < (jam_chance - attacker.Mechanical * 3) then
			jammed = true
		end

		-- Всегда теряем ресурс за каждый выстрел, даже если заклинило
		resource = Max(0, resource - num_shots * loss)
	end

	item.WeaponResource = resource
	local condition_percent = MulDivRound(resource, 100, max_resource)
	return jammed, condition_percent
end

function FirearmBase:RepairJammed(condition, unit_owner)
	self.jammed = false
	NetUpdateHash("WeaponUnjam", self.class, self.id, self.Condition, condition or self.Condition)
	if condition then
		self.Condition = condition
		if self.WeaponResourceMax then
			local max = self.WeaponResourceMax > 0 and self.WeaponResourceMax or self:GetFactoryResource() or 1
			self.WeaponResource = MulDivRound(max, condition, 100)
		end
	end
	if unit_owner then
		CreateFloatingText(unit_owner, T(123820160317, "Unjammed"))
		--CombatLog("important", T{276992233611, "Jammed weapon was <em>clumsily fixed</em> by <DisplayName> (<Mechanical> Mechanical): <condLoss> condition lost", SubContext(unit, {condLoss = condLoss})})
		Msg("InventoryChange", unit_owner) 
		if IsKindOf(unit_owner, "Unit") then unit_owner:RecalcUIActions() end
		ObjModified(unit_owner)
		PlayFX("UnjamWeapon", "start", unit_owner, self.class)
	end
end

function Firearm:PrecalcAmmoUse(attacker, num, prediction, isShotgun)
	local fired = num	
	local jammed, condition
	if not prediction then
		jammed, condition = self:ReliabilityCheck(attacker, num)
	end
	
	local ammo_type = self.ammo and self.ammo.class
	if jammed or (not attacker.infinite_ammo and not self.ammo) then
		fired = false
	elseif self.ammo.Amount < num and isShotgun ~= true then
		fired = self.ammo.Amount
	elseif self.ammo.Amount < 1 and isShotgun == true then
		fired = 1
	end
	
	return fired, jammed, condition, ammo_type
end

function Firearm:GetAttackResults(action, attack_args)
	PauseInfiniteLoopDetection("CTHCalc")
	-- unpack some params & init default values
	local attacker = attack_args.obj
	local anim = attack_args.anim
	local prediction = attack_args.prediction
	local lof_idx = table.find(attack_args.lof, "target_spot_group", attack_args.target_spot_group or "Torso")
	local lof_data = attack_args.lof and attack_args.lof[lof_idx or 1]
    local cth_loss_per_shot = attack_args.cth_loss_per_shot
    local shots_before_cth_loss = attack_args.shots_before_recoil or 0
	local target = attack_args.target or lof_data.target_pos
	local target_pos = lof_data.target_pos or (IsValid(target) and target:GetPos())
	if not target_pos:IsValidZ() then
		target_pos = target_pos:SetTerrainZ()
	end
	local target_unit = IsKindOf(target, "Unit") and target
	local aoe_target_pos = target_unit and target_unit:GetPos() or target_pos -- target_pos is where the shot lands. For AOE attacks we want the object position.
	assert(target)
	assert(target_pos)

	local num_shots = attack_args.num_shots or 0


	local seed = Unit:Random()
	local random = BraidRandomCreate(seed)

    --print(lof_data.action_id)



	local aoe_params = attack_args.aoe_params or (attack_args.aoe_action_id and self:GetAreaAttackParams(attack_args.aoe_action_id, attacker, aoe_target_pos, attack_args.step_pos ))
	local consumed_ammo = attack_args.consumed_ammo
	if not consumed_ammo then
		consumed_ammo = 1
		consumed_ammo = Max(consumed_ammo, num_shots)
		consumed_ammo = Max(consumed_ammo, aoe_params and aoe_params.used_ammo or 0)
	end

	if action.id == "BulletHell" then
		target_pos = attack_args.step_pos + SetLen2D((target_pos - attack_args.step_pos):SetZ(0), aoe_params.max_range * const.SlabSizeX)
		if not target_pos:IsValidZ() then
			target_pos = target_pos:SetTerrainZ()
			target = target_pos
		end
	end
    --print(attack_args)
    --print(attack_args.weapon.BoltingAP)
  
	local shot_attack_args = table.copy(attack_args)
	shot_attack_args.num_shots = num_shots
	shot_attack_args.target_pos = target_pos
	shot_attack_args.target_spot_group = shot_attack_args.target_spot_group or target_unit and g_DefaultShotBodyPart
	shot_attack_args.aim = shot_attack_args.aim or 0
	shot_attack_args.damage_bonus = shot_attack_args.damage_bonus or 0
	shot_attack_args.cth_loss_per_shot = cth_loss_per_shot or 0
	shot_attack_args.stealth_kill_chance = shot_attack_args.stealth_kill_chance or 0
	shot_attack_args.stealth_bonus_crit_chance = shot_attack_args.stealth_bonus_crit_chance or 0
	shot_attack_args.prediction = prediction
	shot_attack_args.occupied_pos = shot_attack_args.occupied_pos or attacker:GetOccupiedPos()
	shot_attack_args.can_use_covers = false
	shot_attack_args.output_collisions = true
	shot_attack_args.additional_colliders = target -- Non-units (such as mines) need to be added manually.
	shot_attack_args.require_los = nil

   -- local bolted = attack_args.weapon.bolted
   --print(consumed_ammo)
	local fired, jammed, condition, ammo_type = self:PrecalcAmmoUse(attacker, consumed_ammo, prediction)
	--Проверка на шотганы
--	if action.id == "Buckshot" then 
--		--fired = shot_attack_args.num_shots 
--		fired, jammed, condition, ammo_type = self:PrecalcAmmoUse(attacker, consumed_ammo, prediction, true)
--	end


--	if  action.id ~= "Buckshot" then 
		if type(fired) == "number" and num_shots > 0 then
			num_shots = Min(fired, num_shots)
			shot_attack_args.num_shots = fired
   		--     if (attack_args.weapon.BoltingAP > 0) then attack_args.weapon.bolted = true end
		end
--	end

if action.id == "Buckshot"  then 
	num_shots = self.AutoShots
end

if action.id == "DoubleBarrel" then 
	num_shots = self.AutoShots * 2
end

if action.id == "BuckshotBurst" then 
	num_shots = self.AutoShots
end

	local cth, baseCth, modifiers
	local cth_action = shot_attack_args.used_action_id and CombatActions[shot_attack_args.used_action_id] or action
	if action.AlwaysHits then
		cth = 100
	elseif attack_args.chance_to_hit then
		cth, modifiers = attack_args.chance_to_hit, attack_args.chance_to_hit_modifiers
	else
		cth, baseCth, modifiers = attacker:CalcChanceToHit(target, cth_action, shot_attack_args)
	end
	local attack_results = {
		weapon = self,
		fired = fired,
		jammed = jammed,
    --    bolted = bolted,
		condition = condition,
		chance_to_hit = cth,
		chance_to_hit_modifiers = modifiers,
		stealth_attack = shot_attack_args.stealth_attack,
		stealth_kill_chance = shot_attack_args.stealth_kill_chance,
		attack_roll = shot_attack_args.attack_roll,
		crit_roll = shot_attack_args.crit_roll,
		ammo_type = ammo_type,
		aim = shot_attack_args.aim,
		dmg_breakdown = shot_attack_args.damage_breakdown and {} or false
	}

	attack_results.crit_chance = attacker:CalcCritChance(self, target, action, shot_attack_args, shot_attack_args.step_pos)

	-- attack/crit rolls
	if prediction then
		if shot_attack_args.multishot then
			attack_results.attack_roll = {}
			attack_results.crit_roll = {}
			for i = 1, num_shots do
				attack_results.attack_roll[i] = 0
				attack_results.crit_roll[i] = 101
			end
		else
			attack_results.attack_roll = 0
			attack_results.crit_roll = 101
		end
		
		if shot_attack_args.stealth_kill_chance > 0 then
			shot_attack_args.stealth_kill_roll = 101
		end
	else
		if shot_attack_args.multishot then
			if type(attack_results.attack_roll) ~= "table" then
				attack_results.attack_roll = {}
				for i = 1, num_shots do
					attack_results.attack_roll[i] = 1 + random(100)
				end
			end
			if type(attack_results.crit_roll) ~= "table" then
				attack_results.crit_roll = {}
				for i = 1, num_shots do
					attack_results.crit_roll[i] = 1 + random(100)
				end
			end
		else
			attack_results.attack_roll = shot_attack_args.attack_roll or (1 + random(100))
			attack_results.crit_roll = shot_attack_args.crit_roll or (1 + random(100))
		end
		if shot_attack_args.stealth_kill_chance > 0 then
			shot_attack_args.stealth_kill_roll = shot_attack_args.stealth_kill_roll or (1 + random(100))
		end
	end

	-- direct shots
	local step_pos3D = shot_attack_args.step_pos:IsValidZ() and shot_attack_args.step_pos or shot_attack_args.step_pos:SetTerrainZ()
	local distAttackerToTarget = step_pos3D:Dist(target_pos)
	local dispersion = self:GetMaxDispersion(distAttackerToTarget)
	local max_range = shot_attack_args.range
	local point_blank = not prediction and attacker:IsPointBlankRange(target) -- ignore this on prediction to avoid step_pos (CalcShotVectors isn't used on prediction anyway)
	if not max_range then
		max_range = Max(MulDivRound(self.WeaponRange, 150, 100), 20) * const.SlabSizeX
	end
	max_range = Max(max_range, distAttackerToTarget + const.SlabSizeX)
	if not prediction then
		max_range = Max(max_range, 100*const.SlabSizeX)
	end
	shot_attack_args.range = max_range

	local stealth_kill
	local roll = attack_results.attack_roll
	local miss, crit
	if shot_attack_args.multishot then
		miss, crit = true, false -- initial values, actual calculation will happen below based on shot results
	else
		crit = attack_results.crit_roll <= attack_results.crit_chance
		miss = roll > attack_results.chance_to_hit
	end

	local target_hit = false
	local out_of_range = true

	local num_hits, total_damage, friendly_fire_dmg, hit_objs = 0, 0, 0, {}
	local unit_damage = {}

	if not miss and shot_attack_args.stealth_kill_chance > 0 then
		stealth_kill = shot_attack_args.stealth_kill_roll <= shot_attack_args.stealth_kill_chance
	end

	local shot_lof_data = shot_attack_args.lof and shot_attack_args.lof[1]
	attack_results.step_pos = shot_lof_data and shot_lof_data.step_pos or shot_attack_args.step_pos
	attack_results.lof_pos1 = shot_lof_data and shot_lof_data.lof_pos1 or attack_results.step_pos -- segment start point (unit center)
	attack_results.attack_pos = shot_lof_data and shot_lof_data.attack_pos or attack_results.step_pos -- weapon shot pos
	attack_results.shots = {}
	attack_results.hit_objs = hit_objs
	attack_results.stealth_kill = stealth_kill
	attack_results.clear_attacks = 0

	-- count num hits and misses and precalc shot vectors for them
	local sfHit = 0x10000
	local sfCrit = 0x20000
	local sfLeading = 0x40000
	local sfAllowGrazing = 0x80000
	local sfCthMask = 0xFF
	local sfRollMask = 0xFF00
	local sfRollOffset = 8
	local num_hits, num_misses, num_grazing = 0, 0, 0
	local shots_data = {}
	local graze_threshold = point_blank and 6 or 3

    cth_loss_per_shot = shot_attack_args.cth_loss_per_shot

	if (attacker.Strength) > 80 then
		if cth_loss_per_shot > 15 then  cth_loss_per_shot = cth_loss_per_shot - cth_loss_per_shot*(attacker.Strength-80)*1.5/100 end
		else cth_loss_per_shot = cth_loss_per_shot - cth_loss_per_shot*(attacker.Strength-80)/100 end

    if (shot_attack_args.stance) == 'Crouch'
    then
        cth_loss_per_shot = cth_loss_per_shot * 0.9
    elseif (shot_attack_args.stance) == 'Prone'
    then
        cth_loss_per_shot = cth_loss_per_shot * 0.6
		local bipodshots = GetComponentEffectValue(self, "ShotsBeforeRecoilProne", "ShotsBeforeRecoilProne")
		if (bipodshots) then shots_before_cth_loss = shots_before_cth_loss + 1 or 1 end
    end	


local ScopeMagn = GetComponentEffectValue(self, "ScopeMagnification", "ScopeMagnification") or 1
local ScopeAimLevel = GetComponentEffectValue(self, "ScopeMagnification", "ScopeAimLevel")

local SmallMagn = GetComponentEffectValue(self, "SmallMagnification", "SmallMagnification") or 1
local SmallAimLevel = GetComponentEffectValue(self, "SmallMagnification", "SmallAimLevel") 

if ScopeAimLevel and shot_attack_args.aim >= ScopeAimLevel then 
	cth_loss_per_shot = cth_loss_per_shot * Max(ScopeMagn/2,1)
end
if SmallAimLevel and shot_attack_args.aim >= SmallAimLevel then 
	cth_loss_per_shot = cth_loss_per_shot * Max(SmallMagn/2,1)
end

	for i = 1, num_shots do

		local shot_miss, shot_crit, shot_cth

    if (i > shots_before_cth_loss) then
        if (i-shots_before_cth_loss < 5) then
            if (attack_results.chance_to_hit - shot_attack_args.cth_loss_per_shot * (i - shots_before_cth_loss - 1)) > 0 then
		    shot_cth = self:GetShotChanceToHit(attack_results.chance_to_hit - cth_loss_per_shot * (i - shots_before_cth_loss - 1))
            else
            shot_cth = 1
            end
        else
            if ((attack_results.chance_to_hit - cth_loss_per_shot * (5)) > 0) then 
                shot_cth = self:GetShotChanceToHit(attack_results.chance_to_hit - cth_loss_per_shot * (5))
            else shot_cth = 1 end
        end
    else 
        shot_cth = self:GetShotChanceToHit(attack_results.chance_to_hit)
    end

	if 	shot_cth and distAttackerToTarget > ((self.WeaponRange +1) * const.SlabSizeX) then
		shot_cth = shot_cth * 0.5
	end



		shot_cth = attacker:CallReactions_Modify("OnCalcShotChanceToHit", shot_cth, attacker, target, i, num_shots)
		if target_unit then
			shot_cth = target_unit:CallReactions_Modify("OnCalcShotChanceToHit", shot_cth, attacker, target, i, num_shots)
			
		end
		if shot_attack_args.multishot then
			roll = attack_results.attack_roll[i]
			shot_miss = roll > shot_cth
			shot_crit = (not shot_miss) and (attack_results.crit_roll[i] <= attack_results.crit_chance)
			-- update global miss/crit for the attack
			miss = miss and shot_miss
			crit = crit or shot_crit
		else
			shot_miss = (not stealth_kill or i > 1) and roll > shot_cth
			shot_crit = crit and (i == 1)
		end

		local data = band(shot_cth, sfCthMask)
		data = bor(data, band(shift(roll, sfRollOffset), sfRollMask))
		data = bor(data, shot_miss and 0 or sfHit)
		data = bor(data, shot_crit and sfCrit or 0)
		data = bor(data, (shot_attack_args.multishot or (i == 1)) and sfLeading or 0)
		if shot_miss and shot_cth > 0 then
			local shot_graze_threshold = self:GetShotGrazeTheshold(graze_threshold)
			shot_graze_threshold = attacker:CallReactions_Modify("OnCalcShotGrazeThreshold", shot_graze_threshold, attacker, target, i, num_shots)
			if target_unit then
				shot_graze_threshold = target_unit:CallReactions_Modify("OnCalcShotGrazeThreshold", shot_graze_threshold, attacker, target, i, num_shots)
			end
			if roll < shot_cth + shot_graze_threshold then
				data = bor(data, sfAllowGrazing)
				num_grazing = num_grazing + 1
			end
		end
		shots_data[i] = data
		num_hits = num_hits + (shot_miss and 0 or 1)
		num_misses = num_misses + (shot_miss and 1 or 0)
		if not prediction then
			NetUpdateHash("FirearmShot", attacker, target, shot_attack_args.action_id, shot_attack_args.stance, self.class, self.id, self == shot_attack_args.weapon, shot_attack_args.occupied_pos, shot_attack_args.step_pos, shot_attack_args.angle, shot_attack_args.anim, shot_attack_args.can_use_covers, shot_attack_args.ignore_smoke, shot_attack_args.penetration_class, shot_attack_args.range, shot_cth, roll, shot_miss)
		end
	end
	
	-- burst distribution simulation
	local precalc_shots, anyHitsTarget
	if not prediction then
		local hit_target_pts, miss_target_pts, disp_origin, disp_dir
		local lof_data 
		if shot_lof_data then
			lof_data = shot_lof_data
		else
			lof_data = { target_pos = target_pos, lof_pos1 = attack_results.lof_pos1 }
		end

		for i = 1, 20 do
			hit_target_pts, miss_target_pts, anyHitsTarget, disp_origin, disp_dir = self:CalcShotVectors(attacker, action.id, target, 
				shot_attack_args, lof_data, 20*guic, guim, guim, num_hits, num_misses, num_grazing)
			if (#hit_target_pts + #miss_target_pts) >= (num_hits + num_misses) then break end
		end
		
		-- use old code as fallback in case all 20 tries have failed (this shouldn't really happen)	
		if (#hit_target_pts + #miss_target_pts) < (num_hits + num_misses) then
			--assert(false, "simulated burst distribition precomputation failed, falling back to randomized miss vectors")
		else
			-- assign target points to shots based on desired outcome
			precalc_shots = {}
			--[[local lowest
			for i = 1, num_shots do
				local shot_miss = band(shots_data[i], sfHit) == 0
				local target_tbl = shot_miss and miss_target_pts or hit_target_pts
				local shot_vector = table.remove(target_tbl)
				local target_pos = shot_vector.target_pos
				precalc_shots[i] = { lof_pos1 = shot_vector.lof_pos1, attack_pos = shot_vector.attack_pos, target_pos = target_pos, shot_data = shots_data[i], shot_idx = i }
				if not lowest or (lowest:z() > target_pos:z()) then
					lowest = target_pos
				end
			end
			
			table.sort(precalc_shots, function(a, b) return a.target_pos:Dist(lowest) < b.target_pos:Dist(lowest) end)--]]
			for i = 1, num_shots do
				local shot_miss = band(shots_data[i], sfHit) == 0
				local allow_grazing = band(shots_data[i], sfAllowGrazing) ~= 0
				local shot_vector
				if shot_miss then
					if allow_grazing then
						local idx = table.find(hit_target_pts, "accurate", false)
						if idx then
							shot_vector = table.remove(hit_target_pts, idx)
						end
					end
					if not shot_vector then
						shot_vector = table.remove(miss_target_pts)
					end
					if not shot_vector then -- fallback
						shot_vector = table.remove(hit_target_pts)
					end
				else
					local idx = table.find(hit_target_pts, "accurate", true)
					shot_vector = table.remove(hit_target_pts, idx)
					if not shot_vector then -- fallback
						shot_vector = table.remove(miss_target_pts)
					end
				end
				
				local shot_target_pos = shot_vector.target_pos
				local shot_attack_pos = shot_vector.attack_pos
				local t_offset = shot_target_pos - disp_origin
				precalc_shots[i] = { lof_pos1 = shot_vector.lof_pos1, attack_pos = shot_attack_pos, target_pos = shot_target_pos, shot_data = shots_data[i], shot_idx = i, dispersion = shot_vector.idx }--Dot(t_offset, disp_dir) }
			end
			table.sort(precalc_shots, function(a, b)
				return a.dispersion < b.dispersion
			end)
		end
	end

	local misses
	local precalc_damage_data = {}
	local killed_colliders = {}

	local suppression_CTH = attack_results.chance_to_hit



	for i = 1, num_shots do
	
		-- clear dead collide units
		local precalc_shot = precalc_shots and precalc_shots[i]
		local shot_data = precalc_shot and precalc_shot.shot_data or shots_data[i]
		
		local shot_cth, shot_miss, shot_crit, allow_grazing
		shot_cth = band(shot_data, sfCthMask)
		shot_miss = band(shot_data, sfHit) == 0
		shot_crit = band(shot_data, sfCrit) ~= 0
		allow_grazing = band(shot_data, sfAllowGrazing) ~= 0
		roll = shift(band(shot_data, sfRollMask), -sfRollOffset)


		if shot_cth > 100 then shot_cth = 0 end

		--print("shot_cth"..shot_cth)
		--print("distance"..distAttackerToTarget / const.SlabSizeX)
	

		--print(shot_attack_args.target_spot_group)

		if (action.id == "Buckshot" and shot_cth > 90 and i > 1) then shot_cth = 90 end
										--chance to shot in random body part
		--print(shot_cth)
		if (shot_cth < 90 or (action.id == "Buckshot")) and not prediction then 
			local rand = random(shot_cth)
			if shot_attack_args.target_spot_group == "Head" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 3 then shot_attack_args.target_spot_group = "Neck"
					elseif rand < 50 then shot_attack_args.target_spot_group = "Arms"
					else shot_attack_args.target_spot_group = "Torso"
					end
				end
			elseif shot_attack_args.target_spot_group == "Torso" then 
				if rand < 20 then 
					rand = random(shot_cth)
					if rand < 10 then shot_attack_args.target_spot_group = "Head"
					elseif rand < 50 then shot_attack_args.target_spot_group = "Arms"
					elseif rand < 70 then shot_attack_args.target_spot_group = "Groin"	
					elseif rand < 90 then shot_attack_args.target_spot_group = "Legs"	
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			elseif shot_attack_args.target_spot_group == "Arms" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 5 then shot_attack_args.target_spot_group = "Head"
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			elseif shot_attack_args.target_spot_group == "Groin" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 50 then shot_attack_args.target_spot_group = "Legs"
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			elseif shot_attack_args.target_spot_group == "Legs" then 
				if rand < 10 then 
					rand = random(shot_cth)
					if rand < 50 then shot_attack_args.target_spot_group = "Groin"
					else shot_attack_args.target_spot_group = "Torso"													
					end
				end
			end
		

		--	attack_data.target_spot_group = hit_data.target_spot_group
		
		--	local lof_idx = table.find(attack_data.lof, "target_spot_group", attack_data.target_spot_group)
		--	local lof_data = attack_data.lof[lof_idx or 1]
		--	hit_data = attack_data.outside_attack_area_lof or attack_data.lof and attack_data.lof[lof_idx or 1]
		--	hit_data.target_pos = miss_target_pos or lof_data.target_pos
		--	hit_data.attack_pos = lof_data.attack_pos
		end
			--print(shot_attack_args.target_spot_group)


		local leading_shot = band(shots_data[i], sfLeading) ~= 0
		local dmg_target = (leading_shot and not shot_miss) and target or false

		--print(leading_shot)

		


		local attack_data, miss_target_pos, hit_data
		if precalc_shot then
			shot_attack_args.attack_pos = precalc_shot.attack_pos
			shot_attack_args.seed = attacker:Random()
			shot_attack_args.ignore_los = attack_args.ignore_los
			shot_attack_args.inside_attack_area_check = attack_args.inside_attack_area_check
			shot_attack_args.forced_hit_on_eye_contact = attack_args.forced_hit_on_eye_contact
			local shot_target
			if shot_miss then
				shot_target = precalc_shot.target_pos
				miss_target_pos = precalc_shot.target_pos
				if not allow_grazing then
					shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, target_unit)
				end
				shot_attack_args.ignore_los = true
				shot_attack_args.inside_attack_area_check = false
				shot_attack_args.forced_hit_on_eye_contact = false
			else
				shot_target = attack_args.target_dummy or (IsValid(target) and target) or precalc_shot.target_pos
				shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, attack_args.ignore_colliders)
			end
			attack_data = GetLoFData(attacker, shot_target, shot_attack_args)
		elseif shot_miss then
			if not prediction then -- don't simulate misses for prediction, dispersion uses synced random and executing it from UI code will desync	
				

				local lof_idx = table.find(shot_attack_args.lof, "target_spot_group", shot_attack_args.target_spot_group)
				local lof_data = shot_attack_args.outside_attack_area_lof or shot_attack_args.lof[lof_idx or 1]
				local lof_pos1 = lof_data.lof_pos1
				while not misses or (#misses.clear + #misses.obstructed == 0) do
					misses = self:CalcMissVectors(attacker, action.id, target, lof_pos1, lof_data.target_pos, dispersion)
					dispersion = dispersion + 20*guic -- try shooting wider next time to avoid infinitely retrying to find miss vectors very close to the target
				end
				miss_target_pos = self:PickMissTargetPos(attacker, misses, roll, shot_cth)
				-- extend the shot vector to the max range to make sure the bullet doesn't despawn right after passing by the missed target
				local v = miss_target_pos - lof_pos1
				miss_target_pos = lof_pos1 + SetLen(v, max_range - const.SlabSizeX)
				shot_attack_args.fire_relative_point_attack = false
				shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, target_unit)
				shot_attack_args.seed = attacker:Random()
				shot_attack_args.ignore_los = true
				shot_attack_args.inside_attack_area_check = false
				shot_attack_args.forced_hit_on_eye_contact = false
				attack_data = GetLoFData(attacker, miss_target_pos, shot_attack_args)


			end
		else

			shot_attack_args.fire_relative_point_attack = attack_args.fire_relative_point_attack
			shot_attack_args.ignore_colliders = compile_ignore_colliders(killed_colliders, attack_args.ignore_colliders)
			local target_dummy = attack_args.target_dummy or target
			shot_attack_args.seed = prediction and 0 or attacker:Random()
			shot_attack_args.ignore_los = attack_args.ignore_los
			shot_attack_args.inside_attack_area_check = attack_args.inside_attack_area_check
			shot_attack_args.forced_hit_on_eye_contact = attack_args.forced_hit_on_eye_contact
			attack_data = GetLoFData(attacker, target_dummy, shot_attack_args)
		end
		if attack_data then
			local lof_idx
			lof_idx = lof_idx or table.find(attack_data.lof, "target_spot_group", shot_attack_args.target_spot_group)
			hit_data = attack_data.outside_attack_area_lof or attack_data.lof and attack_data.lof[lof_idx or 1]
		else
			local lof_idx = table.find(shot_attack_args.lof, "target_spot_group", shot_attack_args.target_spot_group)
			local lof_data = shot_attack_args.outside_attack_area_lof or shot_attack_args.lof[lof_idx or 1]
			hit_data = {
				obj = attacker,
				hits = empty_table,
				target_pos = miss_target_pos or lof_data.target_pos,
				attack_pos = lof_data.attack_pos
			}
		end

		-- Only used for logging, the modifier isn't displayed anywhere as the
		-- crosshair uses another check.
		if not shot_miss and ((not precalc_shots and hit_data.stuck) or (precalc_shots and not anyHitsTarget)) then
			attack_results.chance_to_hit = 0
			attack_results.obstructed = true
			local mods = attack_results.chance_to_hit_modifiers or {}
			mods[#mods + 1] = {
				{
					id = "NoLineOfFire",
					name = T(604792341662, "No Line of Fire"),
					value = 0
				}
			}
		end

		--if not shot_attack_args.lof and not aoe_params or not fired or jammed or shot_attack_args.chance_only then
		if not fired or jammed or (shot_attack_args.chance_only and not shot_attack_args.damage_breakdown) then
			ResumeInfiniteLoopDetection("CTHCalc")
			return attack_results
		end


		

		hit_data.target = dmg_target
		hit_data.critical = shot_crit
		hit_data.record_breakdown = i == 1 and attack_results.dmg_breakdown or false -- Record mods of the first shot only.




		for k, v in pairs(shot_attack_args) do
			if not hit_data[k] then
				hit_data[k] = v		
			end
		end			
		
		if shot_miss and IsValid(target) then			
			for _, hit in ipairs(hit_data.hits) do
				if hit.obj == target then
					if allow_grazing then
						hit.grazing = true
						hit.grazed_miss = true
					else
						hit.stray = true
					end
				end
			end
		end


		


		--print(hit_data.target_spot_group)
		--print(shot_cth)




		self:BulletCalcDamage(hit_data)

		if shot_attack_args.chance_only then  
			ResumeInfiniteLoopDetection("CTHCalc")
			return attack_results 
		end -- Quick out to avoid calculating other shots when we only wanted the dmg breakdown.

		-- gather hit stats for logging
		local shot_target_hit = false


		for _, hit in ipairs(hit_data.hits) do
			local hit_obj = hit.obj
			if IsKindOf(hit_obj, "Unit") and not hit_obj:IsDead() then
				num_hits = num_hits + 1
				if not hit_objs[hit_obj] then
					hit_objs[#hit_objs + 1] = hit_obj
					hit_objs[hit_obj] = true
				end
				
				
				if hit_obj == dmg_target and hit.grazing then
					stealth_kill = false
					shot_attack_args.stealth_kill_roll = -100
				end	
				
				if stealth_kill and hit_obj == dmg_target then
					hit.damage = MulDivRound(target:GetTotalHitPoints(), 125, 100)
					hit.stealth_kill = true
				end
				total_damage = total_damage + hit.damage
				if not attacker:IsOnEnemySide(hit_obj) then
					friendly_fire_dmg = friendly_fire_dmg + hit.damage
				end
				unit_damage[hit_obj] = (unit_damage[hit_obj] or 0) + hit.damage
				if hit_obj == target_unit then
					shot_target_hit = true
				end
				if shot_attack_args.stealth_bonus_crit_chance > 0 and hit.critical then
					hit.stealth_crit = true
				end
			elseif IsKindOf(hit_obj, "Trap") then
				if hit_obj == target then
					shot_target_hit = true
				end
			end
			
			-- presim damage tracking
			if IsKindOf(hit_obj, "CombatObject") then
				local dmg_data = precalc_damage_data[hit_obj] or {}
				precalc_damage_data[hit_obj] = dmg_data
				local hp, temp_hp = hit_obj:PrecalcDamageTaken(hit.damage, dmg_data.hp, dmg_data.temp_hp)
				dmg_data.hp = hp
				dmg_data.temp_hp = temp_hp
				if hp <= 0 then
					table.insert_unique(killed_colliders, hit_obj)
				end
			elseif IsKindOfClasses(hit_obj, "Destroyable", "Trap") then
				table.insert_unique(killed_colliders, hit_obj)
			end
		end
		target_hit = target_hit or shot_target_hit
		out_of_range = out_of_range and shot_attack_args.outside_attack_area
		--print(hit_data)
		

		attack_results.shots[i] = { 
			miss = shot_miss,
			cth = shot_cth,
			roll = roll,
			attack_pos = hit_data.attack_pos,
			target_pos = hit_data.target_pos,
			stuck_pos = hit_data.stuck_pos or hit_data.lof_pos2,
			hits = {},
			target_hit = shot_target_hit,
			out_of_range = shot_attack_args.outside_attack_area,
			shot_target = not shot_miss and target_unit,
            cth_loss_per_shot = shot_attack_args.cth_loss_per_shot,
			allyHit = hit_data.allyHit,
			ammo_type = ammo_type,
			clear_attacks = hit_data.clear_attacks,
		}
		if hit_data.allyHit then
			if attack_results.allyHit and attack_results.allyHit ~= hit_data.allyHit then
				attack_results.allyHit = "multiple"
			else
				attack_results.allyHit = hit_data.allyHit
			end
		end
		attack_results.clear_attacks = attack_results.clear_attacks + (hit_data.clear_attacks or 0)
		for _, hit in ipairs(hit_data.hits) do
			hit.direct_shot = true
			hit.shot_idx = i
			hit.weapon = self
			if hit.obj or hit.terrain then
				table.insert(attack_results, hit) -- store in attack_results to obey the convention of returning hits in the array part of the results
				table.insert(attack_results.shots[i].hits, hit) -- also store in the shot description for convenience
			end
		end

		--suppression
		if (action.id == "MGBurstFire") then 
			suppression_CTH = suppression_CTH * 1.5
		end


		--if not prediction and g_Combat then
			if not prediction then
				local attacker_is_psycho = HasPerk(attacker, "Psycho")
				local target_is_psycho = IsValid(target_unit) and HasPerk(target_unit, "Psycho")
				local units = table.ifilter(g_Units, function(_, u)
					return u.HireStatus ~= "Dead"
						and u.session_id ~= target.session_id
						and u.session_id ~= attacker.session_id
						and IsKindOf(u, "Unit")
						and u.team and u.team.side ~= attacker.team.side
				end)
			
				local wpBase = Max(self.Damage, 1) * 0.1

				if (action.id == "MGBurstFire") then 
					wpBase = wpBase * 3
				end
			
				for _, hit in ipairs(hit_data.hits) do
					if IsValid(target_unit) and target_unit.team.side ~= attacker.team.side then
						local cthFactor = Clamp((suppression_CTH / 100)^0.5, 0.1, 1.0)
						local willDamage = wpBase * (0.4 + 0.6 * cthFactor)
						if willDamage > 0 then
							if attacker_is_psycho then
								attacker.WillPoints = Max(attacker.MaxWillPoints, attacker.WillPoints + willDamage)
							end
							if not target_is_psycho then
								QueueSuppressionApplication(target_unit, willDamage)
								--target_unit.WillPoints = Max(0, target_unit.WillPoints - willDamage)
								--target_unit:ApplySuppressionStatus()
							end
						end
					end
			
					local hit_pos = hit.pos or hit_data.target_pos
					for _, unit in ipairs(units) do
						local dist = unit:GetPos():Dist2D(hit_pos)
						if dist < 5 * const.SlabSizeX then
							local clamped = Clamp((4 * const.SlabSizeX - dist) / const.SlabSizeX, 0, 4)
							local nearDamage = wpBase * clamped * 0.15
							if nearDamage > 0 then
								if attacker_is_psycho then
									attacker.WillPoints = Max(attacker.MaxWillPoints, attacker.WillPoints + nearDamage)
								end
								if not HasPerk(unit, "Psycho") then
									QueueSuppressionApplication(unit, nearDamage)


									--unit.WillPoints = Max(0, unit.WillPoints - nearDamage)
									--unit:ApplySuppressionStatus()
								end
							end
						end
					end
				end
			end

	end




	
	attack_results.miss = miss
	attack_results.crit = crit

	if num_shots > 0 and IsValid(target) then
		--[[if miss == target_hit then
			DbgClearTexts()
			DbgClearVectors()
			for _, shot in ipairs(attack_results.shots) do
				DbgAddVector(shot.attack_pos, shot.target_pos - shot.attack_pos, const.clrYellow)
				DbgAddText(string.format("cth: %d, roll: %d (%s)", shot.cth, shot.roll, (shot.roll <= shot.cth) and "hit" or "miss"), shot.target_pos + point(0, 0, guim), const.clrWhite)
				for _, hit in ipairs(shot.hits) do
					DbgAddVector(hit.pos, point(0, 0, 2*guim), const.clrGreen)
				end
			end
			WaitNextFrame()
		end--]]
		--assert(miss ~= target_hit)
	end

	

	-- aoe damage
	local targetHitProjectile = target_hit
	if aoe_params then
		local damage_override = GetAoeDamageOverride(shot_attack_args, attacker, self, shot_attack_args.damage_bonus)
		aoe_params.prediction = shot_attack_args.prediction
		local hits, aoe_total_damage, aoe_friendly_fire_dmg = GetAreaAttackResults(aoe_params, shot_attack_args.aoe_damage_bonus, shot_attack_args.applied_status, damage_override)
		attack_results.area_hits = hits
		total_damage = total_damage + aoe_total_damage
		friendly_fire_dmg = friendly_fire_dmg + aoe_friendly_fire_dmg

		for _, hit in ipairs(hits) do
			hit.weapon = self
			if IsKindOf(hit.obj, "CombatObject") and not hit.obj:IsDead() then
				if IsKindOf(hit.obj, "Unit") and hit.damage > 0 then
					unit_damage[hit.obj] = (unit_damage[hit.obj] or 0) + hit.damage
				end
				local objIsTarget = hit.obj == target
				hit.obj_is_target = objIsTarget
				target_hit = target_hit or (objIsTarget)
				if not hit_objs[hit.obj] then
					hit_objs[#hit_objs + 1] = hit.obj
					hit_objs[hit.obj] = true
					num_hits = num_hits + 1
				else
					-- find the first hit on this target, fold the damage there, reset the damage to 0 so it doesn't get processed in FireSpread
					local direct_hit = find_first_hit(attack_results, hit.obj)
					if direct_hit then
						direct_hit.damage = direct_hit.damage + hit.damage
						hit.damage = 0
					end
				end
			end
		end

		if not prediction and (shot_attack_args.buckshot_scatter_fx or 0) > 0 then
			attack_results.cosmetic_hits = self:CalcBuckshotScatter(attacker, action, attack_results.attack_pos, target_pos, shot_attack_args.buckshot_scatter_fx, aoe_params)
		end
	end

	attack_results.num_hits = num_hits
	attack_results.total_damage = total_damage
	attack_results.friendly_fire_dmg = friendly_fire_dmg
	attack_results.target_hit = target_hit
	attack_results.target_hit_projectile = targetHitProjectile
	attack_results.out_of_range = out_of_range
	attack_results.unit_damage = unit_damage
	CompileKilledUnits(attack_results)

	if not prediction then
		--print("Firearm_GetAttackResults", attack_results.fired, attack_results.miss, attack_results.target_hit, attack_results.num_hits)
		NetUpdateHash("Firearm_GetAttackResults", attack_results.fired, attack_results.miss, attack_results.target_hit, attack_results.num_hits)
		g_LastAttackResults = attack_results
	end
	ResumeInfiniteLoopDetection("CTHCalc")
	return attack_results
end




function FirearmBase:Unjam(unit)
	local factory = self:GetFactoryResource() or 1000
	local max = self:GetMaxResource()    
	if max <= 0 then max = 1 end
	if factory <= 0 then factory = 1 end

	-- Проверка успеха починки
	local diff = (100 - MulDivRound(self.WeaponResource or 0, 100, max)) / 10 + (100 - (self.Reliability or 50)) / 10 + (self.Deterioration or 0)
	local pass = RollSkillCheck(unit, "Mechanical", diff, 50)

	local amount = unit:Random(100 - unit.Mechanical)
	self.num_safe_attacks = Max(self.num_safe_attacks, const.Weapons.JamFixNumSafeAttacks)

	if pass then
		self.jammed = false
		CreateFloatingText(unit, T(123820160317, "Unjammed"))
		CombatLog("important", T{255429864106, "Jammed weapon was <em>fixed</em> by <DisplayName> (<Mechanical> Mechanical)", unit})
		Msg("InventoryChange", unit)
		if IsKindOf(unit, "Unit") then unit:RecalcUIActions() end
		ObjModified(unit)
		PlayFX("UnjamWeapon", "start", unit, self.class)
		return
	end

	-- Урон при неудаче
	local condLoss = Clamp(amount * 0.1, 0.1, 3)
	condLoss = floatfloor(condLoss + 0.5)

	local loss = MulDivRound(max * 1.0, condLoss * 1.0, 100) 

	print("jam debug")
	print(max,loss,condLoss,amount)

	self.WeaponResourceMax = Max(1, max - loss)
	self.WeaponResource = Min(self.WeaponResource or 0, self.WeaponResourceMax)

	local newConditionPercent = MulDivRound(self.WeaponResource, 100, self.WeaponResourceMax)
	NetUpdateHash("WeaponUnjam", self.class, self.id, self.WeaponResource, self.WeaponResourceMax)

	if self.WeaponResourceMax <= 1 or newConditionPercent <= 0 then
		CombatLog("important", T{759078917029, "<DisplayName> has <em>broken</em> a jammed weapon in attempt to fix it (<Mechanical> Mechanical)", unit})
		Msg("InventoryChange", unit)
		if IsKindOf(unit, "Unit") then unit:RecalcUIActions() end
		ObjModified(unit)
		PlayFX("BrokeWeapon", "start", unit)
		return
	end

	-- Неудачно, но не сломано
	if IsKindOf(unit, "Unit") then
		CreateFloatingText(unit, T(456744290565, "Jammed"))
	end

	CombatLog("important", T{276992233611, "Jammed weapon was <em>damaged in attempt to fix</em> by <DisplayName> (<Mechanical> Mechanical): <condLoss> condition lost", SubContext(unit, {condLoss = condLoss})})
	Msg("InventoryChange", unit)
	if IsKindOf(unit, "Unit") then unit:RecalcUIActions() end
	ObjModified(unit)
	self.jammed = false
	PlayFX("UnjamWeapon", "start", unit, self.class)
end



TFormat.bullets =  function(context_obj, bullets, max, icon)
	icon = icon or "<image UI/Icons/Rollover/ammo_placeholder 1400>"
	bullets = bullets or GetBulletCount(context_obj)
	if not bullets then return T(994336406701, "<image UI/Icons/Hud/ammo_infinite>") end
	local max = max or context_obj and context_obj.MagazineSize or context_obj.MaxStacks
	local text = bullets == 0 and "<error><bullets></error>" or "<bullets>"
	if not max then
		return T{370913997359, text, bullets = bullets, icon = icon}
	else
		if bullets > 0 then
			if context_obj and context_obj.MagazineSize and context_obj.ammo.colorStyle and bullets ~= 0 then	
			--	text = T{"<style <ammocolor> ><text></style>/<style InventoryItemsCountMax><max></style>", ammocolor = context_obj.ammo.colorStyle, text = text}
				text = Untranslated("<style " .. context_obj.ammo.colorStyle .. ">" .. text .. "</style>/<style InventoryItemsCountMax><max></style>")
				--text = "<style "..context_obj.ammo.colorStyle..">"..text.."</style>" .. "/<style InventoryItemsCountMax><max></style>"
			else
				text = Untranslated(text .. "/<style InventoryItemsCountMax><max></style>")
			end
		else
			text = Untranslated(text .. "/<style InventoryItemsCountMax><max></style>")
		end
		return T{text, bullets = bullets, max = max or 0, icon = icon}
	end		 
end

function InventoryStack:GetItemSlotUI()
	if self.colorStyle then
			return  Untranslated("<style "..self.colorStyle..">"..self.Amount.."<valign bottom 0><style "..self.colorStyle..">/"..self.MaxStacks.."</style>")
	else
			return T{709831548751, "<style InventoryItemsCount><cur><valign bottom 0><style InventoryItemsCountMax>/<max></style>", 
				 cur = self.Amount, max = self.MaxStacks}
	end
end


function SetpieceShoot.ExecThread(state, Actors, TargetType, TargetUnits, TargetBodyPart, TargetPos, NumShots, ShotInterval, InitialDelay, AnimSpeed, TargetOffset, NumMisses)
	local target_pt, target_obj = SetpieceShoot.ResolveTargetPt(state, TargetType, TargetUnits, TargetBodyPart, TargetPos)
	
	for _, actor in ipairs(Actors) do
		actor:SetCommand("SetpieceAimAt", target_pt)
	end
	-- wait aiming
	while true do
		local done = true
		for _, actor in ipairs(Actors) do
			done = done and actor.command == "SetpieceIdle"
		end
		if done then break end
		WaitMsg("SetpieceUnitAimed", 100)
	end
	
	local threads = SetpieceShootThreads
	for _, actor in ipairs(Actors) do
		if IsValidThread(threads[actor]) then
			DeleteThread(threads[actor])
			threads[actor] = nil
		end
		threads[actor] = CreateGameTimeThread(function()
			local weapon = actor:GetActiveWeapons("Firearm") or actor:GetActiveWeapons("RocketLauncher")
			local zooka = IsKindOf(weapon, "RocketLauncher")
			if not weapon then
				StoreErrorSource(actor, string.format("SetpieceShoot trying to fire an unsupported weapon of class '%s' for actor '%s'", weapon and weapon.class or "(nil)", actor.unitdatadef_id or actor.class))
				return
			end
			local ordnance, target_points
			local is_missed = {}
			
			local attack_data, lof_data
			if IsValid(target_obj) then
				attack_data = actor:ResolveAttackParams("SingleShot", target_obj, {target = target_obj, target_spot_group = TargetBodyPart})
				lof_data = attack_data.lof and attack_data.lof[1]
				target_pt = lof_data and lof_data.target_pos or target_pt
			else
				attack_data = actor:ResolveAttackParams("SingleShot", target_pt)
				if not attack_data.anim then
					attack_data.anim = actor:GetAttackAnim("SingleShot", actor.stance)
				end
			end
			actor:SetPos(attack_data.step_pos)
			local visual_obj = weapon:GetVisualObj(actor)
			
			if zooka then
				ordnance = weapon.ammo
				if not ordnance then
					-- find suitable ammo to fire
					for name, class in sorted_pairs(ClassDescendants("Ordnance")) do
						if class.Caliber == weapon.Caliber then
							ordnance = class
						end
					end
				end
				if not ordnance then
					StoreErrorSource(actor, string.format("SetpieceShoot unable to find suitable ordnance to fire from weapon of class '%s' for actor '%s'", weapon.class, actor.unitdatadef_id or actor.class))
					return
				end
			elseif IsValid(target_obj) then
				-- prepare target points in advance using CalcShotVectors
				local step_pos = attack_data.step_pos or actor:GetPos()
				local lof_pos1 = lof_data and lof_data.lof_pos1 or step_pos
				local num_misses = NumMisses or 0
				local num_hits = NumShots - num_misses
				local shot_attack_args = {target_spot_group = TargetBodyPart, stance = actor.stance, step_pos = step_pos}
				local lof_data = {lof_pos1 = lof_pos1, target_pos = target_pt}
				local hit_vectors, miss_vectors = Firearm:CalcShotVectors(actor, "SingleShot", target_obj, shot_attack_args, lof_data, 20*guic, guim, guim, num_hits, num_misses, 0)				
				local lowest
				target_points = {}
				for _, hit in ipairs(hit_vectors) do
					table.insert(target_points, hit.target_pos)
					if not lowest or (hit.target_pos:z() < lowest:z()) then
						lowest = hit.target_pos
					end
				end
				for _, miss in ipairs(miss_vectors) do
					table.insert(target_points, miss.target_pos)
					is_missed[point_pack(miss.target_pos)] = true
					if not lowest or (miss.target_pos:z() < lowest:z()) then
						lowest = miss.target_pos
					end
				end
				while #target_points < NumShots do -- fallback
					table.insert(target_points, target_pt)
					if not lowest or (target_pt:z() < lowest:z()) then
						lowest = target_pt
					end
				end
				table.sort(target_points, function(a, b) return lowest:Dist(a) < lowest:Dist(b) end)
			elseif TargetOffset and TargetOffset > 0 then
				-- prepare target points in advance by adding target offset
				local dir = (target_pt - actor:GetPos()):SetZ(0)
				if dir:Len2D2() > 0 then
					target_points = {}
					for i = 1, NumShots do
						local z = InteractionRand(TargetOffset, "Setpiece")
						local angle = InteractionRand(360*60, "Setpiece")
						target_points[i] = target_pt + RotateAxis(point(0, 0, z), dir, angle)
					end
				end
			end
			
			Sleep(InitialDelay)
			if IsValid(actor) then
				actor:SetAnimSpeedModifier(AnimSpeed*10)
			end
			for si = 1, NumShots do
				if not IsValid(actor) then break end
				local shot_target_pt = target_points and target_points[si] or target_pt
				actor:SetState(attack_data.anim, 0, 0)
				--Sleep(actor:TimeToMoment(1, "hit") or 0)
				if visual_obj then
					assert(visual_obj:IsValidPos())
					local projectile_spawn_pos = GetWeaponSpotPos(visual_obj, "Muzzle")
					local action_dir = SetLen(shot_target_pt - projectile_spawn_pos, 4096)
					local fx_target = visual_obj.parts.Muzzle or visual_obj.parts.Barrel or visual_obj
					PlayFX("WeaponFire", "start", visual_obj, fx_target, projectile_spawn_pos, action_dir)
					if zooka then
						local dist = projectile_spawn_pos:Dist(shot_target_pt)
						local time = MulDivRound(dist, 1000, const.Combat.RocketVelocity)
						local trajectory = {
							{ pos = projectile_spawn_pos, t = 0 }, 
							{ pos = shot_target_pt, t = time },
						}
						local attaches = visual_obj:GetAttaches("OrdnanceVisual")
						local projectile
						if attaches then
							projectile = attaches[1] 
							projectile:Detach()
						else
							projectile = PlaceObject("OrdnanceVisual", {fx_actor_class = ordnance.class})
							local angle = CalcOrientation(projectile_spawn_pos, shot_target_pt)
							projectile:SetAngle(angle)
						end
						weapon:UpdateRocket()
						PlayFX("RocketFire", "start", projectile)
						
						--projectile:ChangeEntity(ordnance.Entity or "MilitaryCamp_Grenade_01")
						--projectile.fx_actor_class = ordnance.class
						
						local rotation_axis = RotateAxis(axis_x, axis_z, CalcOrientation(shot_target_pt, projectile_spawn_pos))
						CreateGameTimeThread(function()
							AnimateThrowTrajectory(projectile, trajectory, rotation_axis, 0)
							DoneObject(projectile)
						end)
					else
						local hit
						if is_missed[point_pack(shot_target_pt)] then
							hit = {
								distance = shot_target_pt:Dist(projectile_spawn_pos),
								pos = shot_target_pt,
								shot_dir = action_dir,
								setpiece = true,
							}
						else
							hit = {
								obj = target_obj,
								distance = shot_target_pt:Dist(projectile_spawn_pos),
								pos = shot_target_pt,
								shot_dir = action_dir,
								spot_group = TargetBodyPart,
								setpiece = true,
							}
						end
						CreateGameTimeThread(Firearm.ProjectileFly, Firearm, actor, projectile_spawn_pos, shot_target_pt, action_dir, const.Combat.BulletVelocity, {hit})
					end
				end
				Sleep(actor:TimeToAnimEnd())
				if si < NumShots and ShotInterval > 0 and not zooka then
					actor:RestoreAiming(shot_target_pt)
					Sleep(ShotInterval)
				end
			end
			if IsValid(actor) then
				actor:SetAnimSpeedModifier(1000)
			end
			threads[actor] = nil
			Msg("SetpieceShootDone")
		end)
	end
	
	while true do
		local all_done = true
		for _, actor in ipairs(Actors) do
			local thread = threads[actor]
			if IsValidThread(thread) then
				all_done = false
				break
			end
		end
		if all_done then break end
		WaitMsg("SetpieceShootDone", 100)
	end
	
	-- go back to aiming anims
	for _, actor in ipairs(Actors) do
		threads[actor] = nil
		if IsValid(actor) then
			actor:RestoreAiming(target_pt)
		end
	end
end


function Firearm:GetAreaAttackParams(action_id, attacker, target_pos, step_pos, stance)
	local params = { 
		attacker = attacker,
		weapon = self,
		target_pos = target_pos,
		step_pos = step_pos,
		used_ammo = 1,
		damage_mod = 100,
		attribute_bonus = 0,
		dont_destroy_covers = true,
	}
	if attacker then
		params.step_pos = step_pos or attacker:IsValidPos() and (GetPassSlab(attacker) or attacker:GetPos())
		params.stance = stance or attacker.stance
	end
	--if action_id == "Buckshot" or action_id == "DoubleBarrel" or action_id == "BuckshotBurst" or action_id == "CancelShotCone" then
	--	self:FillConeAttackAoeParams(params, attacker)
	--else
	if action_id == "EyesOnTheBack" then
		local effect = attacker:GetStatusEffect("EyesOnTheBack")
		params.cone_angle = effect and (effect:ResolveValue("cone_angle")*60)
		params.min_range = self:GetOverwatchConeParam("MinRange")
		params.max_range = self:GetOverwatchConeParam("MaxRange")
	elseif action_id == "Overwatch" or action_id == "MGRotate" or action_id == "MGSetup" then
		params.cone_angle = self.OverwatchAngle
		if self.emplacement_weapon then
			params.min_distance_2d = const.EmplacementWeaponMinDistance2D
		end
		params.min_range = self:GetOverwatchConeParam("MinRange")
		params.max_range = self:GetOverwatchConeParam("MaxRange")
	elseif action_id == "BulletHell" or action_id == "DanceForMe" then
		params.cone_angle = self.OverwatchAngle
		params.min_range = self:GetOverwatchConeParam("MinRange")
		params.max_range = self:GetOverwatchConeParam("MaxRange")
	elseif action_id == "FireFlare" then	
		params.min_range = self.ammo and self.ammo.AreaOfEffect or 0
		params.max_range = self.ammo and self.ammo.AreaOfEffect or 0
	end
	
	return params
end


function BaseWeapon:PrecalcDamageAndStatusEffects(attacker, target, attack_pos, damage, hit, effect, attack_args, record_breakdown, action, prediction)
	local base_damage = damage
	if IsKindOf(target, "Unit") then
		local seed = target:Random()
		local random = BraidRandomCreate(seed)

		local effects = EffectsTable(effect)
		local ignoreGrazing = IsFullyAimedAttack(attack_args) and self:HasComponent("IgnoreGrazingHitsWhenFullyAimed")
		local ignore_cover = (hit.aoe or hit.melee_attack or ignoreGrazing) and 100 or self.IgnoreCoverReduction
		
		-- grazing hits
		local chance = 0
		local base_chance = 0
		-- cover effect based on attack_pos
		if target:IsAware() and not target:HasStatusEffect("Exposed") and target:HasStatusEffect("Protected") and (not ignore_cover or ignore_cover <= 0) then
			local cover, any, coverage = target:GetCoverPercentage(attack_pos)
			base_chance = const.Combat.GrazingChanceInCover
			if target:HasStatusEffect("Protected") then
				base_chance = Protected:ResolveValue("base_chance")
			end
			chance = InterpolateCoverEffect(coverage, base_chance, 0)
			hit.grazing_reason = "cover"
		end

		if not ignoreGrazing and not hit.aoe then
			if target:IsConcealedFrom(attack_pos or attacker) then
				chance = chance + const.EnvEffects.FogGrazeChance
				hit.grazing_reason = "fog"
			end
			if target:IsObscuredFrom(attack_pos or attacker) then
				chance = chance + const.EnvEffects.DustStormGrazeChance
				hit.grazing_reason = "duststorm"
			end
		end		
		
		if not prediction then
			local grazing_roll = random(100)
			if grazing_roll < chance then
				hit.grazing = true
			else
				hit.grazing_reason = false
			end
		elseif chance ~= 0 then
			hit.grazing = true
		end
		-- grazing hits (from cover and gas) cant crit
		if hit.grazing then
			hit.critical = nil
		end
		--local ignore_armor = hit.aoe or IsKindOf(self, "MeleeWeapon")
		local ignore_armor = false
		-- Order/method of damage buff calculations might need a revision. The are quite a few now and they seem to be added arbitrary.
		if not hit.stray or hit.aoe then
			local data = {
				breakdown = record_breakdown or {},
				effects = {},
				base_damage = damage,
				damage_add = 0,
				damage_percent = 100,
				ignore_armor = false,
				ignore_body_part_damage = {},
				action_id = action and action.id,	
				weapon = self,
				prediction = prediction,
				critical = hit.critical,
				critical_damage = const.Weapons.CriticalDamage,
			}
			local mod_attack_args = attack_args or {}
			local mod_hit_data = hit or {}
			local action_id = action and action.id
			Msg("GatherDamageModifications", attacker, target, action_id, self, mod_attack_args, mod_hit_data, data) -- only called for non-stray hits (no misses)
			if IsKindOf(attacker, "Unit") then
				attacker:CallReactions("OnCalcDamageAndEffects", attacker, target, action, self, mod_attack_args, mod_hit_data, data)
			end
			if IsKindOf(target, "Unit") then
				target:CallReactions("OnCalcDamageAndEffects", attacker, target, action, self, mod_attack_args, mod_hit_data, data)
			end
			damage = Max(0, MulDivRound(data.base_damage + data.damage_add, data.damage_percent, 100))
			if data.critical then
				damage = Max(0, MulDivRound(damage, 100 + data.critical_damage, 100))
			end
			hit.critical = data.critical
			for _, effect in ipairs(data.effects) do
				EffectTableAdd(effects, effect)
			end
			ignore_armor = ignore_armor or data.ignore_armor
							
			local part_def = hit.spot_group and Presets.TargetBodyPart.Default[hit.spot_group]
			if part_def then
				if not data.ignore_body_part_damage[part_def.id] then
					damage = MulDivRound(damage, 100 + part_def.damage_mod, 100)
					if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = part_def.display_name, value = part_def.damage_mod } end
				end
				EffectTableAdd(effects, part_def.applied_effect)
			end
			
		else
			damage = MulDivRound(damage, 50, 100)
		end
	
		hit.damage = damage
		target:ApplyHitDamageReduction(hit, self, hit.spot_group or g_DefaultShotBodyPart, nil, ignore_armor, record_breakdown)
		if hit.grazing then
			hit.effects = {}
			hit.damage = Max(1, MulDivRound(hit.damage, const.Combat.GrazingHitDamage, 100))
		else
			hit.effects = effects
		end
	else
		--apply dmg mod for non units
		local obj_dmg_mod = (not hit.ignore_obj_damage_mod and self:HasMember("ObjDamageMod")) and self.ObjDamageMod or 100
		if obj_dmg_mod ~= 100 then
			damage = MulDivRound(damage, obj_dmg_mod, 100)
			if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = T{360767699237, "<em><DisplayName></em> damage modifier to objects", self}, value = obj_dmg_mod } end
		end
		if HasPerk(attacker, "CollateralDamage") and IsKindOfClasses(self, "HeavyWeapon", "MachineGun") then
			local collateralDamage = CharacterEffectDefs.CollateralDamage
			local damageBonus = collateralDamage:ResolveValue("objectDamageMod")
			damage = MulDivRound(damage, 100 + damageBonus, 100)
			if record_breakdown then record_breakdown[#record_breakdown + 1] = { name = collateralDamage.DisplayName, value = damageBonus } end
		end
		--apply armor for non units
		local pen_class = self:HasMember("PenetrationClass") and self.PenetrationClass or #PenetrationClassIds
		local armor_class = target and target.armor_class or 0
		--if self.PenetrationClass then self.PenetrationClass = self.PenetrationClass - 1 end
		if pen_class >= armor_class then
			hit.damage = damage or 0
			hit.armor_prevented = 0
		else
			hit.damage = 0
			hit.armor_prevented = damage or 0
		end
		if record_breakdown then 
			local armor_prevented
			if pen_class >= armor_class then
				armor_prevented = 0
			else
				armor_prevented = base_damage or 0
			end
			if hit.damage > (base_damage/2) then
				record_breakdown[#record_breakdown + 1] = { name = T(478438763504, "Armor (Pierced)") }
			else
				record_breakdown[#record_breakdown + 1] = { name = T(360312988514, "Armor"), value = -hit.armor_prevented }
			end
		end
	end
end



--function FirearmBase:GetRolloverType()
--	return self.ItemType or self.RolloverClassTemplate or self.WeaponType
--end

function ItemWithCondition:AmountOfScrapPartsFromItem()
	local parts = self:GetScrapParts()
	if self.Condition and self.Condition < 50 then
		parts = parts / 20
        --if parts < 1 then parts = 1 end
	end
    --print(parts)
    if parts < 1 then parts = 1 end
	return parts
end

function FirearmBase:GetScrapParts()
	local parts = InventoryItem.GetScrapParts(self)
	parts = parts + (#(self.components or empty_table) * const.Weapons.UpgradeScrapParts)
    if self.Condition and self.Condition < 50 then
		parts = parts / 20
       -- if parts < 1 then parts = 1 end
	end
    --print(parts)
    if parts < 1 then parts = 1 end
	return parts
end

function MishapProperties:GetMishapDeviationVector(unit, target)
	local explosives = unit.Explosives or 50
	local dist_tiles = unit:GetDist(target) / const.SlabSizeX

	-- Значения из префаба
	local min_range = (self.MaxMishapRange or 1) * const.SlabSizeX
	local max_range = (self.MaxMishapRange or 4) * const.SlabSizeX

	-- Модификатор от дистанции: чем дальше — тем выше разброс
	local dist_mod = Clamp(dist_tiles / 6, 1, 4.0)

	-- Модификатор от навыка: плохой скилл = больше разброс
	local skill_mod = Clamp(1 - explosives / 100, 0.1, 1)

	-- Финальные отклонения
	local min_dev = min_range * dist_mod * skill_mod
	local max_dev = max_range * dist_mod * skill_mod

	local deviation = unit:RandRange(min_dev, max_dev)
	return Rotate(point(deviation, 0, 0), unit:Random(360 * 60))
end



function MishapProperties:GetMishapDeviationVectorMin(unit, target)
	local explosives = unit.Explosives or 50
	local dist_tiles = unit:GetDist(target) / const.SlabSizeX

	-- Значения из префаба
	local min_range = 1 * const.SlabSizeX
	local max_range = (self.MinMishapRange or 2) * const.SlabSizeX

	-- Модификатор от дистанции: чем дальше — тем выше разброс
	local dist_mod = Clamp(dist_tiles / 8, 0.5, 3.0)

	-- Модификатор от навыка: плохой скилл = больше разброс
	local skill_mod = Clamp(1 - explosives / 100, 0.1, 1)

	-- Финальные отклонения
	local min_dev = min_range * dist_mod * skill_mod
	local max_dev = max_range * dist_mod * skill_mod

	local deviation = unit:RandRange(min_dev, max_dev)
	return Rotate(point(deviation, 0, 0), unit:Random(360 * 60))
end

function MishapProperties:GetMishapDeviationVectorMax(unit, target)
	local explosives = unit.Explosives or 50
	local dist_tiles = unit:GetDist(target) / const.SlabSizeX

	-- Значения из префаба
	local min_range = (self.MinMishapRange or 1) * const.SlabSizeX
	local max_range = (self.MaxMishapRange or 4) * const.SlabSizeX

	-- Модификатор от дистанции: чем дальше — тем выше разброс
	local dist_mod = Clamp(dist_tiles / 8, 1, 4.0)

	-- Модификатор от навыка: плохой скилл = больше разброс
	local skill_mod = Clamp(1 - explosives / 100, 0.1, 1)

	-- Финальные отклонения
	local min_dev = min_range * dist_mod * skill_mod
	local max_dev = max_range * dist_mod * skill_mod

	local deviation = unit:RandRange(min_dev, max_dev)
	return Rotate(point(deviation, 0, 0), unit:Random(360 * 60))
end