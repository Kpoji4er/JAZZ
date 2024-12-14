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


function GrenadeAOEVisuals:RecreateAoeTiles(data)
	self.data = data
	local mesh_pstr = CreateAOETiles(data.step_positions, data.step_objs, data.los_values)
	local aoe_tiles_mesh = self.aoe_tiles_mesh
	if not aoe_tiles_mesh then
		aoe_tiles_mesh = Mesh:new({})
		self.aoe_tiles_mesh = aoe_tiles_mesh
		aoe_tiles_mesh:SetAttachOffset(point(0,0,-10))
		aoe_tiles_mesh:SetMeshFlags(aoe_tiles_mesh:GetMeshFlags() | const.mfSortByPosZ | const.mfWorldSpace)
		self:Attach(aoe_tiles_mesh)
	end
	aoe_tiles_mesh:SetMesh(mesh_pstr)
	local m = CRM_SphereAOETilesMaterial:GetById("GrenadeTilesCast"):Clone()
	m.center = data.explosion_pos
	m.radius = data.range
	m.dirty = true
	aoe_tiles_mesh:SetCRMaterial(m)
	if data.min_range then
		local aoe_tiles_mesh2 = self.aoe_tiles_mesh2
		if not aoe_tiles_mesh2 then
			aoe_tiles_mesh2 = Mesh:new({})
			self.aoe_tiles_mesh2 = aoe_tiles_mesh2
			aoe_tiles_mesh2:SetAttachOffset(point(0,0,-10))
			aoe_tiles_mesh2:SetMeshFlags(aoe_tiles_mesh2:GetMeshFlags() | const.mfSortByPosZ | const.mfWorldSpace)
			self:Attach(aoe_tiles_mesh2)
		end
		local m2 = CRM_SphereAOETilesMaterial:GetById("GrenadeTilesCast"):Clone()
		m2.center = data.explosion_pos
		m2.radius = data.min_range
		m2.dirty = true
		aoe_tiles_mesh:SetCRMaterial(m2)
	end
end



function Grenade:GetAreaAttackParams(action_id, attacker, target_pos, step_pos)
	target_pos = target_pos or self:GetPos()
	local aoeType = self.aoeType
	local max_range = self.AreaOfEffect
	if aoeType == "fire" then
		max_range = 2
	end
	local params = {
		attacker = false,
		weapon = self,
		target_pos = target_pos,
		step_pos = target_pos,
		stance = "Prone",
		min_range = self.CenterAreaOfEffect,
		max_range = self.AreaOfEffect,
		center_range = self.CenterAreaOfEffect,
		damage_mod = 100,
		attribute_bonus = 0,
		can_be_damaged_by_attack = true,
		aoe_type = aoeType,
		explosion = true, -- damage dealt depends on target stance
		explosion_fly = self.DeathType == "BlowUp",
	}
	if self.coneShaped then
		params.cone_length = self.AreaOfEffect * const.SlabSizeX
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
			local chance = self:GetMishapChance(attacker, target_pos)
			if CheatEnabled("AlwaysMiss") or attacker:Random(100) < chance then
				mishap = true

				-- Try a couple of times to get a valid deviated position
				local validPositionTries = 0
				local maxPositionTries = 5
				while validPositionTries < maxPositionTries do
					local dv = self:GetMishapDeviationVector(attacker, target_pos)
					local deviatePosition = target_pos + dv
					local trajectory = self:GetTrajectory(attack_args, attack_pos, deviatePosition, "mishap")
					local finalPos = #trajectory > 0 and trajectory[#trajectory].pos
					if finalPos and self:ValidatePos(finalPos, attack_args) then
						target_pos = deviatePosition
						break
					end
					validPositionTries = validPositionTries + 1
				end
				attacker:ShowMishapNotification(action)
			end
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
		for _, hit in ipairs(results) do
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

