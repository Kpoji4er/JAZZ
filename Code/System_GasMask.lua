function EnvEffectToxicGasTick(unit, voxels, combat_moment)
	local inside, protected, attacker
	if next(g_SmokeObjs) ~= nil then
		if not voxels then
			voxels = unit:GetVisualVoxels()
		end
		local smoke
		for _, voxel in ipairs(voxels) do
			local smoke_obj = g_SmokeObjs[voxel]
			if smoke_obj and smoke_obj:GetGasType() == "toxicgas" then
				smoke = smoke_obj
				inside = true
				break
			end
		end
		if inside then
			local mask = unit:GetItemInSlot("Head", "GasMaskBase") or unit:GetItemInSlot("HeadGear", "GasMaskBase")
			protected = mask and mask.Condition > 0
			for _, zone in ipairs(smoke.zones) do
				if zone.owner then
					attacker = zone.owner
					break
				end
			end
		end
	end
	
	if inside and protected and attacker then
		-- awareness reactions (there will be no damage/negative effects)
		PushUnitAlert("attack", attacker, unit)
	end
	
	inside = inside and not protected
	
	local effect = unit:GetStatusEffect("Choking")
	if effect then
		local start_time = effect:ResolveValue("choking_start_time")
		if (combat_moment == "end turn") or (not g_Combat and not g_StartingCombat and GameTime() >= start_time + 5000) then			
			local damage = Choking:ResolveValue("damage")
			unit:TakeDirectDamage(damage, T{698692719911, "<damage> (Choking)", damage = damage})
			EnvEffectReaction("toxicgas", attacker, unit, damage)
			if g_Combat or g_StartingCombat then
				start_time = GameTime()
			else
				start_time = start_time + 5000
			end
			if inside then
				effect:SetParameter("choking_start_time", start_time)
			else
				unit:RemoveStatusEffect("Choking")
			end
			local tiredness = RollSkillCheck(unit, "Health") and 1 or 2
			unit:ChangeTired(tiredness)
		end
	elseif inside then
		unit:AddStatusEffect("Choking")
		EnvEffectReaction("toxicgas", attacker, unit, 0)
	end	
end

function EnvEffectTearGasTick(unit, voxels, combat_moment)
	local inside, protected, attacker
	if next(g_SmokeObjs) ~= nil then
		if not voxels then
			voxels = unit:GetVisualVoxels()
		end
		local smoke
		for _, voxel in ipairs(voxels) do
			local smoke_obj = g_SmokeObjs[voxel]
			if smoke_obj and smoke_obj:GetGasType() == "teargas" then
				smoke = smoke_obj
				inside = true
				break
			end
		end
		if inside then
			local mask = unit:GetItemInSlot("Head", "GasMaskBase") or unit:GetItemInSlot("HeadGear", "GasMaskBase")
			protected = mask and mask.Condition > 0
			for _, zone in ipairs(smoke.zones) do
				if zone.owner then
					attacker = zone.owner
					break
				end
			end
		end
	end
	
	if inside and protected and attacker then
		-- awareness reactions (there will be no damage/negative effects)
		PushUnitAlert("attack", attacker, unit)
	end
	inside = inside and not protected
	
	local effect = unit:GetStatusEffect("Blinded")
	if effect then
		local start_time = effect:ResolveValue("blinded_start_time")
		if (combat_moment == "end turn") or (not g_Combat and not g_StartingCombat and GameTime() >= start_time + 5000) then
			-- choking damage/end will happen on end turn in combat		
			if g_Combat or g_StartingCombat then
				start_time = GameTime()
			else
				start_time = start_time + 5000
			end
			if inside then
				effect:SetParameter("blinded_start_time", start_time)
			else
				unit:RemoveStatusEffect("Blinded")
			end
		elseif combat_moment == "start turn" and inside then
			if not RollSkillCheck(unit, "Health") then
				unit:AddStatusEffect("Panicked")
			end
		end
	elseif inside then
		unit:AddStatusEffect("Blinded")
		EnvEffectReaction("teargas", attacker, unit, 0)
	end	
end


function AnyInterruptsAlongPath(unit, path, allInterrupts, action)
	local gotoDummies = unit:GenerateTargetDummiesFromPath(path)
	
	local mask = unit:GetItemInSlot("Head", "GasMaskBase") or unit:GetItemInSlot("HeadGear", "GasMaskBase")
	local check_gas = (not mask or mask.Condition <= 0) and (next(g_SmokeObjs) ~= nil)
	local check_fire = next(g_Fire) ~= nil
	
	if check_gas or check_fire then
		local voxels = {}

		for i, dummy in ipairs(gotoDummies) do
			local _, headVoxel = unit:GetVisualVoxels(dummy.pos, dummy.stance, voxels)
			local smoke = g_SmokeObjs[headVoxel]
			if smoke and smoke:GetGasType() ~= "smoke" then
				if unit:GetDist(dummy.pos) < const.SlabSizeX / 2 then
					-- target dummies come in order of distance from the start, if we're already inside the gas there's no need to give off warnings
					break
				end
				return true
			end
			if 	AreVoxelsInFireRange(voxels) then
				if unit:GetDist(dummy.pos) < const.SlabSizeX / 2 then
					-- target dummies come in order of distance from the start, if we're already inside the gas there's no need to give off warnings
					break
				end
				return true
			end
		end
	end
	
	local interrupts = unit:CheckProvokeOpportunityAttacks(action or CombatActions.Move, "move", gotoDummies, true, allInterrupts and "all" or "any")
	if interrupts then
		return interrupts
	end
	return false
end
