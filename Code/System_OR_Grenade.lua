function Grenade:CalcTrajectory(attack_args, target_pos, angle, max_bounces)
	local attacker = attack_args.obj
	local anim_phase = attacker:GetAnimMoment(attack_args.anim, "hit") or 0
	local attack_offset = attacker:GetRelativeAttachSpotLoc(attack_args.anim, anim_phase, attacker, attacker:GetSpotBeginIndex("Weaponr"))
	local step_pos = attack_args.step_pos
	if not step_pos:IsValidZ() then
		step_pos = step_pos:SetTerrainZ()
	end
	local pos0 = step_pos:SetZ(step_pos:z() + attack_offset:z())
	if not angle then
		if target_pos:z() - pos0:z() > const.SlabSizeZ / 2 then
			angle = const.Combat.GrenadeLaunchAngle_Incline
		else
			angle = const.Combat.GrenadeLaunchAngle
		end
	end
	local sina, cosa = sincos(angle)
	local aim_pos = pos0 + Rotate(point(cosa, 0, sina), CalcOrientation(pos0, target_pos))
	local grenade_pos = GetAttackPos(attack_args.obj, step_pos, axis_z, attack_args.angle, aim_pos, attack_args.anim, anim_phase, attack_args.weapon_visual)
	if grenade_pos:Equal2D(target_pos) then
		return empty_table
	end

	local dir = target_pos - grenade_pos
	local bounce_diminish = 40
	local vec
	local can_bounce = self.CanBounce
	if attack_args.can_bounce ~= nil then
		can_bounce = attack_args.can_bounce
	end
	max_bounces = can_bounce and max_bounces or 0
	if can_bounce then
		max_bounces = 1
	end
	if max_bounces > 0 then
		local coeff = 1000
		local d = 10 * bounce_diminish
		for i = 1, max_bounces do
			coeff = coeff + d
			d = MulDivRound(d, bounce_diminish, 100)
		end
		local bounce_target_pos = grenade_pos + MulDivRound(dir, 1000, coeff)
		vec = CalcLaunchVector(grenade_pos, bounce_target_pos, angle, const.Combat.Gravity)
	else
		vec = CalcLaunchVector(grenade_pos, target_pos, angle, const.Combat.Gravity)
	end
	local time = MulDivRound(grenade_pos:Dist2D(target_pos), 1000, Max(vec:Len2D(), 1))
	if time == 0 then
		return empty_table
	end
	local trajectory = CalcBounceParabolaTrajectory(grenade_pos, vec, const.Combat.Gravity, time, 20, max_bounces, bounce_diminish)
	return trajectory
end


function Grenade:GetAreaAttackParams(action_id, attacker, target_pos, step_pos)
	target_pos = target_pos or self:GetPos()
	local aoeType = self.aoeType
	local max_range = self.AreaOfEffect
	if aoeType == "fire" then
		max_range = 2
	end
	local center_range = self.CenterAreaOfEffect
	local area_range = self.AreaOfEffect
	-- Jazz_Perk_Colby: +20% explosion radius when Colby initiates the blast
	if IsKindOf(attacker, "Unit") and HasPerk(attacker, "Jazz_Perk_Colby") then
		center_range = MulDivRound(center_range, 120, 100)
		area_range = MulDivRound(area_range, 120, 100)
		if aoeType ~= "fire" then
			max_range = area_range
		end
	end
	local params = {
		attacker = false,
		weapon = self,
		target_pos = target_pos,
		step_pos = target_pos,
		stance = "Prone",
		min_range = center_range,
		max_range = max_range,
		center_range = center_range,
		damage_mod = 100,
		attribute_bonus = 0,
		can_be_damaged_by_attack = true,
		aoe_type = aoeType,
		explosion = true, -- damage dealt depends on target stance
		explosion_fly = self.DeathType == "BlowUp",
	}
	if self.coneShaped then
		params.cone_length = area_range * const.SlabSizeX
		params.cone_angle = self.coneAngle * 60
		params.target_pos = RotateRadius(params.cone_length, CalcOrientation(step_pos or attacker, target_pos), target_pos)
		if not params.target_pos:IsValidZ() or params.target_pos:z() - terrain.GetHeight(params.target_pos) <= 10*guic then
			params.target_pos = params.target_pos:SetTerrainZ(10*guic)
		end
	end
	if IsKindOf(attacker, "Unit") then
		params.attacker = attacker
		--params.attribute_bonus = GetGrenadeDamageBonus(attacker) -- already applied in GetBaseDamage
	end
	return params
end

function Grenade:GetAttackResults(action, attack_args)
	local attacker = attack_args.obj
	local explosion_pos = attack_args.explosion_pos
	local trajectory = {}
	local mishap
	if not explosion_pos and attack_args.lof then
		local lof_idx = table.find(attack_args.lof, "target_spot_group", attack_args.target_spot_group)
		local lof_data = attack_args.lof[lof_idx or 1]
		local attack_pos = lof_data.attack_pos
		local target_pos = lof_data.target_pos

		--print(action.id)

		-- mishap & stealth kill checks
		if not attack_args.prediction and IsKindOf(self, "MishapProperties") then
			local attack_pos_local = attack_pos
			target_pos, mishap = self:ApplyImpactDeviation(attacker, target_pos, attack_args, {
				action = action,
				max_tries = 5,
				validate_pos = function(deviatePosition)
					local traj = self:GetTrajectory(attack_args, attack_pos_local, deviatePosition, "mishap")
					local finalPos = #traj > 0 and traj[#traj].pos
					return finalPos and self:ValidatePos(finalPos, attack_args)
				end,
			})
		end
		

		trajectory = self:GetTrajectory(attack_args, attack_pos, target_pos, mishap)
		if #trajectory > 0 then
			explosion_pos = trajectory[#trajectory].pos
		end
		explosion_pos = self:ValidatePos(explosion_pos, attack_args)
	end
	
	local results
	if explosion_pos then
		local aoe_params = self:GetAreaAttackParams(action.id, attacker, explosion_pos, attack_args.step_pos)
		if attack_args.stealth_attack then
			aoe_params.stealth_attack_roll = not attack_args.prediction and attacker:Random(100) or 100
		end
		aoe_params.prediction = attack_args.prediction
		if aoe_params.aoe_type ~= "none" or IsKindOf(self, "Flare") then
			aoe_params.damage_mod = "no damage"
		end
		results = GetAreaAttackResults(aoe_params)
		CompileKilledUnits(results)

		local radius = aoe_params.max_range * const.SlabSizeX
		local explosion_voxel_pos = SnapToVoxel(explosion_pos) + point(0, 0, const.SlabSizeZ / 2)
		local impact_force = self:GetImpactForce()
		local unit_damage = {}
		local stamped_aoe = aoe_params.aoe_type or self.aoeType or "none"
		for _, hit in ipairs(results) do
			hit.aoe_type = stamped_aoe
			hit.weapon = hit.weapon or self
			local obj = hit.obj
			if not obj or hit.damage == 0 then goto continue end
			
			local dist = hit.obj:GetDist(explosion_voxel_pos)
			if IsKindOf(obj, "Unit") then
				if not obj:IsDead() then
					unit_damage[obj] = (unit_damage[obj] or 0) + hit.damage
					if unit_damage[obj] >= obj:GetTotalHitPoints() then
						results.killed_units = results.killed_units or {}
						table.insert_unique(results.killed_units, obj)
					end
				end
			end
			hit.impact_force = impact_force + self:GetDistanceImpactForce(dist)
			hit.explosion = true
			::continue::
		end
	else
		results = {}
	end
	results.trajectory = trajectory
	results.explosion_pos = explosion_pos
	results.weapon = self
	results.mishap = mishap
	results.no_damage = IsKindOf(self, "Flare")
	
	return results
end

function HeavyWeapon:GetJamChance(attacker)
	return FirearmBase.GetJamChance(self, attacker)
end

--- Calculates the attack results for a heavy weapon.
---
--- This function handles the logic for determining the trajectory, mishap, and other attack parameters for a heavy weapon. It takes in the attack arguments and returns the attack results, which include information about the attack such as the trajectory, damage, and whether the weapon jammed.
---
--- @param action table The action being performed.
--- @param attack_args table The arguments for the attack, including the attacker, target, and other relevant information.
--- @return table The attack results, including the trajectory, damage, and other relevant information.
function HeavyWeapon:GetAttackResults(action, attack_args)
	local attacker = attack_args.obj
	local prediction = attack_args.prediction
	local trajectory, stealth_kill
	local lof_idx = table.find(attack_args.lof, "target_spot_group", attack_args.target_spot_group or "Torso")
	local lof_data = (attack_args.lof or empty_table)[lof_idx or 1]
	local target_pos = attack_args.target_pos or lof_data and lof_data.target_pos or (IsValid(attack_args.target) and attack_args.target:GetPos())
	local ordnance = self.ammo

	if not target_pos:IsValidZ() then
		target_pos = target_pos:SetTerrainZ()
	end

	-- mishap & stealth kill checks
	local mishap
	if not prediction and not attack_args.explosion_pos and IsKindOf(self, "MishapProperties") then
		local use_validate = self.trajectory_type == "parabola"
		target_pos, mishap = self:ApplyImpactDeviation(attacker, target_pos, attack_args, {
			action = action,
			max_tries = use_validate and 5 or 1,
			validate_pos = use_validate and function(deviatePosition)
				local traj = Grenade:GetTrajectory(attack_args, nil, deviatePosition, "mishap")
				return traj and #traj > 0
			end or nil,
		})
	end

	if self.trajectory_type == "line" then
		attack_args.max_pierced_objects = 0
		attack_args.can_use_covers = false
		if not prediction then
			attack_args.prediction = false
			attack_args.can_use_covers = false
			attack_args.seed = attacker:Random()
			local attack_data = GetLoFData(attacker, target_pos, attack_args)
			attack_args.lof = attack_data.lof
			lof_idx = table.find(attack_args.lof, "target_spot_group", attack_args.target_spot_group or "Torso")
			lof_data = attack_args.lof[lof_idx or 1]
		end
		-- trajectory from lof (shot origin -> first hit/target_pos)
		if lof_data then
			local hits = lof_data.hits or empty_table
			local hit_pos
			if #hits > 0 then
				hit_pos = hits[1].pos
			else
				hit_pos = target_pos
			end
			hit_pos = attack_args.explosion_pos or hit_pos
			local dist = lof_data.attack_pos:Dist(hit_pos)
			local time = MulDivRound(dist, 1000, const.Combat.RocketVelocity)
			trajectory = {
				{ pos = lof_data.attack_pos, t = 0 },
				{ pos = hit_pos, t = time },
			}
		end
	elseif self.trajectory_type == "parabola" then
		attack_args.can_bounce = ordnance and ordnance.CanBounce
		trajectory = Grenade:GetTrajectory(attack_args, nil, target_pos, mishap)
	elseif self.trajectory_type == "bombard" then
		-- no parabola for bombard
	else
		assert(false, string.format("unknown trajectory type '%s' used in heavy weapon '%s' of class %s", tostring(self.trajectory_type), self.class, self.class))
	end
	
	if not attack_args.explosion_pos and ((not trajectory or #trajectory == 0) and self.trajectory_type ~= "bombard" or not self.ammo or self.ammo.Amount <= 0) then
		return {}
	end
	
	local jammed, condition = false, false
	if prediction then
		attack_args.jam_roll = 0
		attack_args.condition_roll = 0
	else
		attack_args.jam_roll = attack_args.jam_roll or (1 + attacker:Random(100))
		attack_args.condition_roll = attack_args.condition_roll or (1 + attacker:Random(100))
		jammed, condition = self:ReliabilityCheck(attacker, 1, attack_args.jam_roll, attack_args.condition_roll)
	end
	
	if jammed then
		return {jammed = true, condition = condition}
	end
	local impact_pos = attack_args.explosion_pos or (trajectory and #trajectory > 0 and trajectory[#trajectory].pos) or target_pos
	local aoe_params = self:GetAreaAttackParams(action.id, attacker, impact_pos)
	aoe_params.stealth_kill = stealth_kill
	if attack_args.stealth_attack then
		aoe_params.stealth_attack_roll = not prediction and attacker:Random(100) or 100
	end

	aoe_params.prediction = prediction
	local results = GetAreaAttackResults(aoe_params, nil, not prediction and ordnance.AppliedEffects)
	results.trajectory = trajectory
	results.ordnance = ordnance
	results.weapon = ordnance
	results.jammed = jammed
	results.condition = condition
	results.fired = not jammed and 1
	results.mishap = mishap
	results.burn_ground = ordnance.BurnGround
	local stamped_aoe = aoe_params.aoe_type or (ordnance and ordnance.aoeType) or "none"
	for _, hit in ipairs(results) do
		hit.aoe_type = stamped_aoe
		hit.weapon = hit.weapon or ordnance or self
	end
	if self.trajectory_type == "bombard" then
		results.explosion_pos = target_pos
		if not jammed then
			results.fired = Min(attack_args.bombard_shots, ordnance.Amount)
		end
	elseif self.trajectory_type == "line" then
		-- add cone aoe behind attacker
		assert(#trajectory > 1)
		
		local range = self.BackfireRange
		local step_pos = attack_args.step_pos
		local target_pos = step_pos + SetLen(trajectory[1].pos - trajectory[2].pos, range * const.SlabSizeX)	
		
		local cone_params = {
			can_be_damaged_by_attack = false,			
			cone_angle = self.BackfireConeAngle,
			max_range = range,
			target_pos = target_pos,
			attacker = attacker,
			step_pos = step_pos,
			explosion = true,
			weapon = aoe_params.weapon,
			damage_override = self.BackfireDamage,
			damage_mod = 100,
			attribute_bonus = 0,
			prediction = prediction,
		}
		
		
		local cone_results = GetAreaAttackResults(cone_params)
		
		-- merge results from the cone attack into 'results'
		for _, hit in ipairs(cone_results) do
			hit.backfire = true
			results[#results + 1] = hit			
		end
		for _, obj in ipairs(cone_results.hit_objs) do
			results.hit_objs = results.hit_objs or {}
			table.insert_unique(results.hit_objs, obj)
		end
		
		results.total_damage = (results.total_damage or 0) + (cone_results.total_damage or 0)
		results.friendly_fire_dmg = (results.friendly_fire_dmg or 0) + (cone_results.friendly_fire_dmg or 0)
	end
	CompileKilledUnits(results)
	return results
end


function GrenadeLauncher:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot_GrenadeLauncher
end

---
--- Returns the base degradation per shot for the RocketLauncher weapon.
---
--- @return number The base degradation per shot for the RocketLauncher.
---
function RocketLauncher:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot_RocketLauncher
end

---
--- Returns the base degradation per shot for the Mortar weapon.
---
--- @return number The base degradation per shot for the Mortar.
---
function Mortar:GetBaseDegradePerShot()
	return self.DegradePerShot or const.Weapons.DegradePerShot_Mortar
end