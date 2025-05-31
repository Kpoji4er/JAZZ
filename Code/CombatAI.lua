const.AIFriendlyFire_MaxRange = 20 * const.SlabSizeX	-- max range to ally for it to be considered in danger
const.AIFriendlyFire_LOFWidth = 100*guic 					-- max distance from an ally to the line between position and target considered in danger
const.AIFriendlyFire_LOFConeNear = 100*guic 				-- same as above for cone attacks (near side of the cone, positioned at attacker)
const.AIFriendlyFire_LOFConeFar = 300*guic 				-- same as above for cone attacks (far side of the cone, positioned at AIFriendlyFire_MaxRange)
const.AIFriendlyFire_ScoreMod = 15							-- % of damage score evaluation remanining when an ally is in danger

const.AIDecisionThreshold = 85 -- targets/locations up to this percent of max scored target/location can be selected
const.AIShootAboveCTH = 0

local function lClearPredictedExplosions(list)
	for i, m in ipairs(list) do
		DoneObject(m)
	end
end

local function lClearPredictedAOE(list)
	for _, obj in ipairs(list) do
		if IsValid(obj) then
			if IsKindOf(obj, "Unit") then
				obj:SetHighlightReason("area target", false)
			elseif not IsKindOf(obj, "DamagePredictable") then
				SetInteractionHighlightRecursive(obj, false, true)
			else
				obj:SetObjectMarking(-1)
			end
		end
	end
end


function AICreateContext(unit, context)
    PauseInfiniteLoopDetection("AiCalc")
	local gx, gy, gz = unit:GetGridCoords()
	local weapon = unit:GetActiveWeapons()
	local default_attack = unit:GetDefaultAttackAction(nil, "ungrouped", nil, "sync")
	local enemies = table.icopy(GetEnemies(unit))
	
	for _, groupname in ipairs(unit.Groups) do
		local group_modifiers = gv_AITargetModifiers[groupname]
		for target_group, mod in pairs(group_modifiers) do
			for _, obj in ipairs(Groups[target_group]) do
				if IsKindOf(obj, "Unit") then
					table.insert_unique(enemies, obj)
				end
			end
		end
	end
	
	if not g_BiasMarkers then
		InitAIBiasMarkers()
	end
	
	-- fallback when our whole team doesn't have a visual on the enemy but we're still aware
	if #(enemies or empty_table) == 0 then
        ResumeInfiniteLoopDetection("AiCalc")
		enemies = table.ifilter(GetAllEnemyUnits(unit), function(idx, enemy) return not enemy:HasStatusEffect("Hidden") end)
	end
	
	-- special-case when having ManningEmplacement status - filter out non targetable enemies
	if unit:HasStatusEffect("ManningEmplacement") then
        ResumeInfiniteLoopDetection("AiCalc")
		enemies = table.ifilter(enemies, function(idx, enemy) return enemy:IsThreatened({unit}) end)
	end
	
	table.sortby_field(enemies, "handle")
	
	local pos = GetPassSlab(unit)
	if not pos then -- can happen if the unit is on impassable for some reason	
		--assert(false, "GetPassSlab failed for unit " .. unit.session_id)		
		local x, y, z = unit:GetPosXYZ()
		local gx, gy, gz = WorldToVoxel(x, y, z)
		if not z then
			gz = nil
		end
		pos = point(VoxelToWorld(gx, gy, (gz)))
	end
	local wx, wy, wz = pos:xyz()
	
	context = context or {}
	
	context.unit = unit
	context.unit_pos = pos
	context.start_ap = unit.ActionPoints
	context.archetype = unit:GetArchetype()
	context.unit_grid_voxel = point_pack(gx, gy, gz)
	context.unit_world_voxel = point_pack(pos)
	context.unit_stance_pos = stance_pos_pack(wx, wy, wz, StancesList[unit.stance])
	context.max_attacks = unit.MaxAttacks
	context.dest_target = {}						-- dest -> picked target (if any)
	context.dest_target_score = {}				-- dest -> estimated damage
	context.weapon = weapon
	context.default_attack = default_attack
	context.default_attack_cost = default_attack:GetAPCost(unit)
	context.EffectiveRange = IsKindOf(weapon, "Firearm") and weapon.BulletDropRange and MulDivRound(weapon.BulletDropRange+weapon.WeaponRange, 50, 100) or IsKindOf(weapon, "Firearm") and MulDivRound(weapon.WeaponRange, 50, 100) or 1 
	--if not IsKindOf(weapon,"SniperRifle") and GameState.DustStorm or GameState.FireStorm or GameState.Underground or GameState.Night or GameState.Fog then context.EffectiveRange = Min(context.unit:GetSightRadius(),context.EffectiveRange) end
	if  IsKindOf(weapon, "Firearm") and (GameState.DustStorm or GameState.FireStorm or GameState.Underground or GameState.Night or GameState.Fog) then context.EffectiveRange = Min(context.unit:GetSightRadius(),context.EffectiveRange) end

	--context.EffectiveRange = IsKindOf(weapon, "Firearm") and GetAccuracy80DistAim(weapon,unit) or 1
	context.ExtremeRange = IsKindOf(weapon, "Firearm") and weapon.WeaponRange or 1
	context.enemies = enemies
	context.enemy_visible = {} -- [enemy] -> true/false
	context.enemy_visible_by_team = {} -- [enemy] -> true/false
	context.enemy_pos = {}
	context.enemy_grid_voxel = {}
	context.enemy_pack_pos_stance = {}
	context.enemy_dir = {}
	context.stance_pos_to_vis_enemies = {}
	context.allies = unit.team.units
	context.ally_grid_voxel = {}
	context.ally_pack_pos_stance = {}
	context.ally_pos = {}
	context.voxel_heal_target = {}
	context.voxel_heal_score = {}
	context.forced_signature_action = false
	context.apply_bias = true
	context.disable_actions = {} -- support for custom filtering for signature action selection by BiasId
	
	NetUpdateHash("AICreateContext", unit, pos, unit.stance, context.start_ap, context.archetype.id, context.max_attacks, weapon and weapon.class, weapon and weapon.id, default_attack.id)
	
	if unit:HasStatusEffect("Stimmed") then
		context.max_attacks = context.max_attacks + 1
	end
	
	for _, action in ipairs(context.archetype.SignatureActions) do
		context.can_heal = context.can_heal or IsKindOf(action, "AIActionBandage")
	end
	if not context.can_heal then
		for _, behavior in ipairs(context.archetype.Behaviors) do
			for _, action in ipairs(behavior.SignatureActions) do
				context.can_heal = context.can_heal or IsKindOf(action, "AIActionBandage")
			end
		end
	end

	for i, enemy in ipairs(enemies) do
		local x, y, z = enemy:GetGridCoords()
		context.enemy_grid_voxel[enemy] = point_pack(x, y, z)
		context.enemy_pack_pos_stance[enemy] = GetPackedPosAndStance(enemy)
		local enemy_pos = GetPassSlab(enemy) or SnapToVoxel(enemy:GetPos())
		context.enemy_pos[enemy] = enemy_pos
		if not pos:Equal2D(enemy_pos) then
			local dir = enemy_pos - pos
			dir = dir:SetInvalidZ()
			context.enemy_dir[enemy] = SetLen(dir, guim)
		else
			context.enemy_dir[enemy] = point(0, 0, guim)
		end
		context.enemy_visible[enemy] = HasVisibilityTo(unit, enemy)
		context.enemy_visible_by_team[enemy] = HasVisibilityTo(unit.team, enemy)
	end
	if context.behavior then
		context.behavior:EnumDestinations(unit, context)
	else
		AIFindDestinations(unit, context)
	end
	AIUpdateDestLosCache(unit, context)
	
	for i, ally in ipairs(context.allies) do
		local x, y, z = ally:GetGridCoords()
		context.ally_grid_voxel[ally] = point_pack(x, y, z)
		context.ally_pack_pos_stance[ally] = GetPackedPosAndStance(ally)
		context.ally_pos[ally] = ally:GetPos()
	end

    ResumeInfiniteLoopDetection("AiCalc")
	unit.ai_context = context
	return context
end

function AISelectAction(context, actions, base_weight, dbg_available_actions)
    PauseInfiniteLoopDetection("AiCalc")
	local available = {}
	local weight = base_weight or 0
	
	context.action_states = context.action_states or {}
	

	for _, action in ipairs(actions) do
		--print(action)
		context.action_states[action] = {}		
		local weight_mod, disable, priority = AIGetBias(action.BiasId, context.unit)
		disable = disable or context.disable_actions[action.BiasId or false]
		if not disable then
			action:PrecalcAction(context, context.action_states[action])
			if action:IsAvailable(context, context.action_states[action]) then
				local action_weight = MulDivRound(action.Weight, weight_mod, 100)
				priority = priority or action.Priority
				if dbg_available_actions then
					table.insert(dbg_available_actions, { action = action, weight = action_weight, priority = priority })
				end
				if priority then
                    ResumeInfiniteLoopDetection("AiCalc")
					return action
				end
				available[#available + 1] = action
				available[available] = action_weight
				weight = weight + action_weight
			elseif dbg_available_actions then
				table.insert(dbg_available_actions, { action = action, weight = false })
			end
		end
	end
	if weight > 0 then
		local roll = InteractionRand(weight, "AISignatureAction", context.unit)
		for _, action in ipairs(available) do
			local w = available[action]
			if roll <= weight then
                ResumeInfiniteLoopDetection("AiCalc")
				return action
			end
			roll = roll - weight
		end
	end
    ResumeInfiniteLoopDetection("AiCalc")
	return available[#available]
end


function AIChooseSignatureAction(context)
    PauseInfiniteLoopDetection("AiCalc")
	local weight = context.archetype.BaseAttackWeight
	context.choose_actions = { { action = false, weight = weight, priority = false } },	
	AIUpdateBiases()
	local sig_actions = AIGetSignatureActions(context)
    ResumeInfiniteLoopDetection("AiCalc")    
	return AISelectAction(context, sig_actions, weight, context.choose_actions)
end

function AIChooseMovementAction(context)
    PauseInfiniteLoopDetection("AiCalc")
	local actions = AIGetSignatureActions(context, true)
	AIUpdateBiases()
    ResumeInfiniteLoopDetection("AiCalc")
	return AISelectAction(context, actions, context.archetype.BaseMovementWeight)
end



function AIFindDestinations(unit, context)
    PauseInfiniteLoopDetection("AiCalc")
	local pos = GetPassSlab(unit) or unit:GetPos()
	local destinations, paths, dest_ap, dest_path, voxel_to_dest, closest_free_pos = AIBuildArchetypePaths(unit, pos, context)	
	if not closest_free_pos then
		if unit.ActionPoints == 0 then
			assert(not "AI try to act with 0 action points!!!")
		else
			print("AI can't find unit free destination prints!!!")
			printf("      AP = %d", unit.ActionPoints)
			printf("      Command = %s", unit.command)
			printf("      Status effects: %s", table.concat(table.keys(unit.StatusEffects), ", "))
			printf("      Pos: %s", tostring(unit:GetPos()))
			printf("      Pass slab pos: %s", tostring(GetPassSlab(unit) or ""))
			printf("      Target dummy pos %s", unit.target_dummy and tostring(unit.target_dummy:GetPos()) or "")
			local o = GetOccupiedBy(unit:GetPos(), unit)
			if o then
				printf("Other pos %s", tostring(o:GetPos()))
				printf("Other target dummy pos %s", o.target_dummy and tostring(o.target_dummy:GetPos()) or "")
				printf("Other efResting=%d", o:GetEnumFlags(const.efResting))
				if o.reposition_dest then
					printf("Other reposition dest=%s", tostring(point(stance_pos_unpack(o.reposition_dest))))
				end
			end
			assert(not "AI can't find unit free destination")
		end
	end
	local crouch_idx = StancesList.Crouch
	local important_dests = context.important_dests or {}
	context.important_dests = important_dests
	local change_stance_costs = {}
	for stance_idx in ipairs(StancesList) do
		change_stance_costs[stance_idx] = GetStanceToStanceAP(StancesList[stance_idx], "Crouch")
	end

	-- preprocess destinations to find those where we need to change stance at the dest to take cover
	local low = const.CoverLow
	--local high = const.CoverHigh
	for i, dest in ipairs(destinations) do
		local x, y, z, stance_idx = stance_pos_unpack(dest)
		if stance_idx ~= crouch_idx then
			local cost = change_stance_costs[stance_idx]
			local ap = dest_ap[dest]
			if cost and ap and ap >= cost then
				local up, right, down, left = GetCover(x, y, z)
				if up then
					local cover_low = up == low or right == low or down == low or left == low
					--local cover_high = up == high or right == high or down == high or left == high
					if cover_low then --and not cover_high then
						table.remove_value(important_dests, dest)
						local new_dest = stance_pos_pack(x, y, z, crouch_idx)
						destinations[i] = new_dest
						voxel_to_dest[point_pack(x, y, z)]	= new_dest
						dest_ap[new_dest] = ap - cost
						dest_path[new_dest] = dest_path[dest]
						table.insert_unique(important_dests, new_dest)
					end
				end
			end
		end
	end

	context.destinations = destinations		-- available destinations
	context.dest_ap = dest_ap						-- dest -> available ap
	context.combat_paths = paths
	context.dest_combat_path = dest_path		-- dest -> index in context.combat_paths (to reach this dest)
	context.voxel_to_dest = voxel_to_dest	
	context.closest_free_pos = closest_free_pos

	context.all_destinations = AIEnumValidDests(context)
    ResumeInfiniteLoopDetection("AiCalc")
end


function AIUpdateDestLosCache(unit, context)
    PauseInfiniteLoopDetection("AiCalc")
	assert(CurrentThread()) -- the function will sleep internally due to the amount of calculations performed
	--local tStart = GetPreciseTicks()
	--ic("AIUpdateDestLosCache start", #units)
	local sight = unit:GetSightRadius()
	local all_destinations = context.all_destinations
	local enemies = context.enemies
	if #enemies == 0 then 
        ResumeInfiniteLoopDetection("AiCalc")
        return end
	NetUpdateHash("AIUpdateDestLosCache_Start", GameTime(), sight, #all_destinations, hashParamTable(all_destinations), #enemies, hashParamTable(context.enemy_pack_pos_stance))

	local dests
	local los_cache = g_AIDestEnemyLOSCache
	for _, dest in ipairs(all_destinations) do
		if los_cache[dest] == nil then
			if not dests then dests = {} end
			dests[#dests + 1] = dest
			los_cache[dest] = false
		end
	end
	if dests then
		local max_los_checks = 100
		local targets = {}
		local srcs = {}
		local enemies_count = #enemies
		local next_dest_idx = 1
		local start_dest_idx = 1
		local cur_enemy = 1
		while true do
			local ppos = context.enemy_pack_pos_stance[enemies[cur_enemy]]
			local count = #targets
			local last_dest_idx = Min(#dests, next_dest_idx + max_los_checks - count - 1)
			for i = next_dest_idx, last_dest_idx do
				count = count + 1
				targets[count] = ppos
				srcs[count] = dests[i]
			end
			next_dest_idx = last_dest_idx + 1
			if next_dest_idx > #dests then
				next_dest_idx = 1
				cur_enemy = cur_enemy + 1
			end
			if count >= max_los_checks or cur_enemy > enemies_count then
				local los_any, los_data = CheckLOS(targets, srcs, sight)
				if los_any then
					local visible_dests = 0
					for i, value in ipairs(los_data) do
						if value then
							local dest = srcs[i]
							if not los_cache[dest] then
								los_cache[dest] = true
								visible_dests = visible_dests + 1
							end
						end
					end
					if visible_dests >= #dests then
						break
					end
					if cur_enemy < enemies_count or cur_enemy == enemies_count and next_dest_idx == 1 then
						-- There will be more LOS checks. Remove visible destinations from dests list to not cast more lines from there
						if #targets >= #dests then
							for i = #dests, 1, -1 do
								if los_cache[dests[i]] then
									table.remove(dests, i)
									if i < next_dest_idx then next_dest_idx = next_dest_idx - 1 end
								end
							end
						elseif start_dest_idx <= last_dest_idx then
							for i = last_dest_idx, start_dest_idx, -1 do
								if los_cache[dests[i]] then
									table.remove(dests, i)
									if i < next_dest_idx then next_dest_idx = next_dest_idx - 1 end
								end
							end
						else
							for i = #dests, start_dest_idx, -1 do
								if los_cache[dests[i]] then
									table.remove(dests, i)
									if i < next_dest_idx then next_dest_idx = next_dest_idx - 1 end
								end
							end
							for i = last_dest_idx, 1, -1 do
								if los_cache[dests[i]] then
									table.remove(dests, i)
									if i < next_dest_idx then next_dest_idx = next_dest_idx - 1 end
								end
							end
						end
						if #dests == 0 then
							assert(#dests > 0)
							break
						end
					end
				end
				if cur_enemy > enemies_count then
					break
				end
				start_dest_idx = next_dest_idx
				table.iclear(targets)
				table.iclear(srcs)
				if GetInGameInterfaceMode() ~= "IModeAIDebug" then
					Sleep(10) --yield
				end
			end
		end
	end

	NetUpdateHash("AIUpdateDestLosCache_End", GameTime())
    ResumeInfiniteLoopDetection("AiCalc")
	--printf("AIUpdateDestLosCache: %d ms for %s", GetPreciseTicks() - tStart, unit.unitdatadef_id)
end

function AIBuildArchetypePaths(unit, pos, context)
    PauseInfiniteLoopDetection("AiCalc")
	local stationary = context.stationary
	local paths = {}
	local destinations, dest_path, dest_ap, voxel_to_dest = {}, {}, {}, {}
	if stationary or CombatActions.Move:GetUIState{unit} ~= "enabled" then
		local dest = GetPackedPosAndStance(unit)
		local x, y, z = stance_pos_unpack(dest)
		local voxel = point_pack(x, y, z)
		destinations[1] = dest
		dest_ap[dest] = unit.ActionPoints
		voxel_to_dest[voxel] = dest
        ResumeInfiniteLoopDetection("AiCalc")
		return destinations, paths, dest_ap, dest_path, voxel_to_dest, voxel
	end

	local archetype = unit:GetArchetype()
	local goto_stance = archetype.MoveStance
	local pref_stance = archetype.PrefStance

	--[[local current_stance = unit.stance or pref_stance

	local cover_high, cover_low= GetCover(unit)
	local in_cover = cover_high or cover_low or false

		if CombatActions.Attack:GetUIState{unit} == "enabled" then
			goto_stance = unit.stance or archetype.PrefStance
		else
		-- 10% шанс оставить текущую стойку
		if InteractionRand(100, "KeepCurrentStance") < 3 then
    	goto_stance = current_stance

		else
   	 	-- ЕСЛИ БОТ НАЧИНАЕТ НЕ В УКРЫТИИ
   		 if not in_cover then
        -- 30% шанс ползти (прон)
			if InteractionRand(100, "StartNotInCover") < 10 then
       	     goto_stance = "Prone"
			elseif InteractionRand(100, "StartNotInCover") < 10 then
				pref_stance  = "Prone"
      	  else
     	       goto_stance = pref_stance
    	    end

   		 -- ЕСЛИ БОТ НАЧИНАЕТ В УКРЫТИИ
   		 else
				-- 30% шанс красться (сидя)
				if InteractionRand(100, "StartInCover") < 5 then
    		        goto_stance = "Crouch"
   	  	   else
   	  	       goto_stance = "Standing" -- или PrefStance
   	 	    end
 		   end
		end
	end
]]--


	local move_stance_idx = StancesList[goto_stance] or 0
	local pref_stance_idx = StancesList[pref_stance] or 0

	local ps_ap = (unit.species == "Human") and (unit.ActionPoints - GetStanceToStanceAP(unit.stance, pref_stance)) or unit.ActionPoints
	local ms_ap = (unit.species == "Human") and (unit.ActionPoints - GetStanceToStanceAP(unit.stance, goto_stance)) or unit.ActionPoints

	local move_path = CombatPath:new()
	move_path:RebuildPaths(unit, ms_ap, pos, goto_stance)

	local dest_voxels = table.keys(move_path.destinations, true)

	local pref_path
	if goto_stance == pref_stance then
		pref_path = move_path
	else
		local visited = move_path.destinations
		pref_path = CombatPath:new()
		pref_path:RebuildPaths(unit, ps_ap, pos, pref_stance)
		for voxel in sorted_pairs(pref_path.destinations) do
			if not visited[voxel] then
				dest_voxels[#dest_voxels+1] = voxel
			end
		end
	end

	local important_dests = context.important_dests or {}
	local min_melee_dist = 2 * const.SlabSizeX
	local move_paths_ap = move_path.paths_ap
	local pref_paths_ap = pref_path.paths_ap

	for _, voxel in ipairs(dest_voxels) do
		local x, y, z = point_unpack(voxel)
		local move_ap = move_paths_ap[voxel]
		local pref_ap = pref_paths_ap[voxel]
		local mn_ap = move_ap and (ms_ap - move_ap) or -1
		local pn_ap = pref_ap and (ps_ap - pref_ap) or -1

		local dest
		if pn_ap > mn_ap then
			assert(pref_ap)

			dest = stance_pos_pack(x, y, z, pref_stance_idx)
			destinations[#destinations+1] = dest
			dest_path[dest] = pref_stance_idx
			dest_ap[dest] = pn_ap
		elseif move_ap then
			dest = stance_pos_pack(x, y, z, move_stance_idx)
			destinations[#destinations+1] = dest
			dest_path[dest] = move_stance_idx
			dest_ap[dest] = mn_ap
		else
			dest = stance_pos_pack(x, y, z, StancesList[unit.stance])
			assert(dest == context.unit_stance_pos)
			destinations[#destinations+1] = dest
			dest_path[dest] = move_stance_idx
			dest_ap[dest] = unit.ActionPoints
		end
		voxel_to_dest[voxel] = dest
		if not table.find(important_dests, dest) then
			if context.EffectiveRange <= 1 then
				-- make sure all potential melee positions are included in the end and not cut off by CollapsePoints
				for enemy, enemy_ppos in pairs(context.enemy_pack_pos_stance) do
					if stance_pos_dist(enemy_ppos, dest) < min_melee_dist then
						table.insert_unique(important_dests, dest)
						break
					end
				end
			end
			-- also do the same for allies, since we might wanna heal them
			if context.can_heal then
				for _, ally in ipairs(context.allies) do
					local ppos = GetPackedPosAndStance(ally)
					if stance_pos_dist(ppos, dest) < min_melee_dist then
						table.insert_unique(important_dests, dest)
						break
					end
				end
			end
		end
	end

	destinations = CollapsePoints(destinations, 1)
	context.important_dests = important_dests
	for _, dest in ipairs(important_dests) do
		if dest_ap[dest] and CanOccupy(unit, stance_pos_unpack(dest)) then
			table.insert_unique(destinations, dest)
		end
	end

	-- filter out destinations someone already called dibs for
	for _, u in ipairs(context.allies) do
		if u ~= unit and u.ai_context then
			local idx = table.find(destinations, u.ai_context.ai_destination)
			if idx then
				destinations[idx] = destinations[#destinations]
				destinations[#destinations] = nil
			end
		end
	end

	paths[goto_stance] = move_path
	paths[move_stance_idx] = move_path
	paths[pref_stance] = pref_path
	paths[pref_stance_idx] = pref_path
    ResumeInfiniteLoopDetection("AiCalc")
	return destinations, paths, dest_ap, dest_path, voxel_to_dest, move_path.closest_free_pos
end

function AIScoreDest(context, policies, dest, grid_voxel, base_score, visual_voxels, score_details)
    PauseInfiniteLoopDetection("AiCalc")
	local score = 0
	local x, y, z, stance_idx = stance_pos_unpack(dest)
	if not grid_voxel then
		local vx, vy, vz = WorldToVoxel(x, y, z)
		grid_voxel = point_pack(vx, vy, vz)
	end

	local voxels, head = context.unit:GetVisualVoxels(point_pack(x, y, z), StancesList[stance_idx], visual_voxels)
	if AreVoxelsInFireRange(voxels) then
		score = const.AIAvoidFireWeigth
		if score_details then
			score_details[#score_details + 1] = "ADJACENT FIRE"
			score_details[#score_details + 1] = const.AIAvoidFireWeigth
		end
	elseif g_SmokeObjs[head] then
		score = const.AIAvoidFireWeigth
		if score_details then
			score_details[#score_details + 1] = "GASSED AREA"
			score_details[#score_details + 1] = const.AIAvoidGasWeigth
		end
	end
	
	for _, policy in ipairs(policies) do
		local peval = policy:EvalDest(context, dest, grid_voxel)
		local pscore = MulDivRound(peval or 0, policy.Weight, 100)
		local failed = policy.Required and pscore <= 0
		score = score + pscore
		if score_details then
			score_details[#score_details + 1] = (failed and "[FAILED] " or "") .. policy:GetEditorView()
			score_details[#score_details + 1] = pscore
		end
		if failed then
            ResumeInfiniteLoopDetection("AiCalc")
			return 0
		end
	end
	
	score = (base_score or 0) + score 
	
	-- bombard zone modifier
	for _, zone in ipairs(g_Bombard) do
		local dist = zone:GetDist(x, y, z)
		local radius = zone.radius * const.SlabSizeX
		if dist <= radius then
			local mod = MulDivRound(dist, const.AIAvoidBombardEdge, radius) + MulDivRound(radius - dist, const.AIAvoidBombardCenter, radius)
			local loss = MulDivRound(score, 100 - mod, 100)
			if score_details and loss > 0 then
				score_details[#score_details + 1] = "BOMBARD ZONE"
				score_details[#score_details + 1] = -loss
			end
			score = Max(0, score - loss)
		end
	end
	
	-- apply modifiers from bias markers at the end
	if context.apply_bias then
		local unit = context.unit
		for _, marker in ipairs(g_BiasMarkers) do
			local bias = marker:GetAIBias(unit, dest)
			if bias ~= 100 then
				score = MulDivRound(score, bias, 100)
				if score_details then
					score_details[#score_details + 1] = string.format("Bias Marker %s (%%): ", marker.ID)
					score_details[#score_details + 1] = bias
				end
			end
		end
	end
	ResumeInfiniteLoopDetection("AiCalc")
	return score
end


function AIEnumValidDests(context)
    PauseInfiniteLoopDetection("AiCalc")
	local unit = context.unit
	local r = context.archetype.OptLocSearchRadius * const.SlabSizeX
	local ux, uy, uz = point_unpack(context.unit_grid_voxel)
	local px, py, pz = VoxelToWorld(ux, uy, uz)
	local bbox = box(px - r, py - r, 0, px + r + 1, py + r + 1, MapSlabsBBox_MaxZ)
	
	local dests, dest_added = {}, {}
	local function push_dest(x, y, z, context, dests, dest_added, ux, uy, uz)
		local gx, gy, gz = WorldToVoxel(x, y, z)
		
		if not IsCloser(gx, gy, gz, ux, uy, uz, context.archetype.OptLocSearchRadius) then
            ResumeInfiniteLoopDetection("AiCalc")
			return
		end
		if not CanOccupy(unit, x, y, z) then
            ResumeInfiniteLoopDetection("AiCalc")
			return
		end

		local world_voxel = point_pack(x, y, z)
		local dest = context.voxel_to_dest[world_voxel]
		if not dest then
			dest = stance_pos_pack(x, y, z, StancesList[context.archetype.PrefStance])
		end
		if not dest_added[dest] then
			dests[#dests + 1] = dest
			dest_added[dest] = true
		end
	end

	ForEachPassSlab(bbox, push_dest, context, dests, dest_added, ux, uy, uz)

	-- add current pos
	if not dest_added[context.unit_stance_pos] then
		local x, y, z = stance_pos_unpack(context.unit_stance_pos)
		if CanOccupy(unit, x, y, z) then
			dests[#dests + 1] = context.unit_stance_pos
			dest_added[context.unit_stance_pos] = true
		end
	end

	-- add from context.destinations
	for _, dest in ipairs(context.destinations) do
		if not dest_added[dest] then
			dests[#dests + 1] = dest
		end
	end

	dests = CollapsePoints(dests, 1)
	for _, dest in ipairs(context.important_dests) do
		table.insert_unique(dests, dest)
	end
    ResumeInfiniteLoopDetection("AiCalc")
	return dests
end

function AIFindOptimalLocation(context, dest_score_details)
    PauseInfiniteLoopDetection("AiCalc")
	if context.best_dest then
		-- optimal location doesn't change across behaviors, no need to recalc it
        ResumeInfiniteLoopDetection("AiCalc")
		return context.best_dest
	end

	local unit = context.unit
	context.best_dests = {}

	local r = context.archetype.OptLocSearchRadius * const.SlabSizeX
	local ux, uy, uz = point_unpack(context.unit_grid_voxel)
	local px, py, pz = VoxelToWorld(ux, uy, uz)
	local bbox = box(px - r, py - r, 0, px + r + 1, py + r + 1, MapSlabsBBox_MaxZ)
	context.best_score = 0
	local unit_voxels = {}
	local dest_scores = {}
	
	local policies = table.ifilter(context.archetype.OptLocPolicies, function(idx, policy) return policy:MatchUnit(unit) end)
	
	for _, dest in ipairs(context.all_destinations) do
		local x, y, z = stance_pos_unpack(dest)
		local gx, gy, gz = WorldToVoxel(x, y, z)
		local world_voxel = point_pack(x, y, z)
		local grid_voxel = point_pack(gx, gy, gz)
		--eval_voxel(x, y, z, context, ux, uy, uz)
		
		if not context.voxel_to_dest[world_voxel] then
			context.voxel_to_dest[world_voxel] = dest
		end
		local scores
		if dest_score_details then
			scores = {}
			dest_score_details[dest] = scores
		end
		table.iclear(unit_voxels)
		local score = AIScoreDest(context, policies, dest, grid_voxel, 0, unit_voxels, scores)
		if score > 0 then
			context.best_score = Max(context.best_score, score)
			local threshold = MulDivRound(context.best_score, const.AIDecisionThreshold, 100)
			if score >= threshold then
				dest_scores[dest] = score
				context.best_dests[#context.best_dests + 1] = dest
				for i = #context.best_dests, 1, -1 do		
					local dest = context.best_dests[i]
					if dest_scores[dest] < threshold then
						table.remove(context.best_dests, i)
					end
				end
			end
		end
		if scores then
			scores.final_score = score
		end
	end

	
	
	-- check if a best dest candidate is on our starting voxel, default to it
	for _, dest in ipairs(context.best_dests) do
		if stance_pos_dist(context.unit_stance_pos, dest) == 0 then
			context.best_dest = dest
		end
	end
	
	if not context.best_dest and #(context.best_dests or empty_table) > 0 then
		if #(context.best_dests or empty_table) > 15 then
			context.collapsed = CollapsePoints(context.best_dests, 1)
		else
			context.collapsed = context.best_dests
		end
		local pf_dests = {}
		for i, dest in ipairs(context.collapsed) do
			local x, y, z = stance_pos_unpack(dest)
			pf_dests[i] = point(x, y, z)
		end
		
		context.best_dest_path = pf.GetPosPath(unit, pf_dests)
		if #(context.best_dest_path or empty_table) > 0 then
			local voxel = point_pack(SnapToPassSlabXYZ(context.best_dest_path[1]))
			local dest = context.voxel_to_dest[voxel]
			if not dest then
				-- try non-snapped
				voxel = point_pack(context.best_dest_path[1])
				dest = context.voxel_to_dest[voxel]
			end
			--assert(dest and (not dest_score_details or dest_score_details[dest]))
			context.best_dest = dest 
		end
	end
	
	context.dest_scores = dest_scores
	context.best_dest = context.best_dest or context.voxel_to_dest[context.unit_world_voxel] or context.unit_stance_pos
	if context.dest_combat_path[context.best_dest] then
		table.insert_unique(context.important_dests, context.best_dest)
		table.insert_unique(context.destinations, context.best_dest)
	end
    ResumeInfiniteLoopDetection("AiCalc")
	return context.best_dest
end

function AICalcPathDistances(context)
    PauseInfiniteLoopDetection("AiCalc")
	local unit = context.unit
	local path_voxels, voxel_dist, total_dist
	if context.best_dest_path then 
		path_voxels, voxel_dist, total_dist = CalcPathVoxels(context.best_dest_path)
	end
	context.path_voxels = path_voxels
	context.path_to_target = table.copy(path_voxels or empty_table)
	context.voxel_dist = voxel_dist
	context.total_dist = total_dist
		
	-- calc distance to optimal location from each dest
	if path_voxels and voxel_dist then
		AICalcDistancesFromReachableLocations(context) -- will add path nodes to path_voxels and voxel_dist
	else
		-- no path to target, use default distances on all reachable voxels
		context.dest_dist = {}
	end
    ResumeInfiniteLoopDetection("AiCalc")
end


function ApplyDamagePrediction(attacker, action, args, actionResult)
    PauseInfiniteLoopDetection("AiCalc")
	local target = args and args.target
	local target_spot_group = args and args.target_spot_group
	local targetIsUnit = IsKindOf(target, "Unit")
	local targetIsTrap = IsKindOf(target, "Trap")
	local targetIsPoint = IsPoint(target)
	
	if not target or (not targetIsUnit and not targetIsPoint and not targetIsTrap) then 
        ResumeInfiniteLoopDetection("AiCalc") 
        return end

	-- Save trap explosion meshes from clear to prevent flicker.
	local trapExplosions = s_PredictedTrapExplosions
	s_PredictedTrapExplosions = false
	
	-- Save aoe explosions from clear to prevent flicker.
	local aoeObjs = s_PredictedAOEObjs
	s_PredictedAOEObjs = false
	
	-- Clear old prediction
	ClearDamagePrediction()
	s_PredictedHighlightedObjs = s_PredictedHighlightedObjs or {}
	s_PredictedTrapExplosions = s_PredictedTrapExplosions or {}
	s_PredictedAOEObjs = s_PredictedAOEObjs or {}
	if not targetIsPoint and target:IsDead() then
		lClearPredictedExplosions(trapExplosions)
        ResumeInfiniteLoopDetection("AiCalc")
		return
	end

	-- Additional info needed for prediction icon
	local weapon1, weapon2 = attacker and action:GetAttackWeapons(attacker)
	local ignore_cover = IsKindOf(weapon1, "Firearm") and weapon1.IgnoreCoverReduction > 0 or IsKindOf(weapon2, "Firearm") and weapon2.IgnoreCoverReduction > 0
	local aimType = action.AimType
	local attackerPosition
	if IsPoint(target) and aimType ~= "cone" then
		attackerPosition = target
	elseif args and args.step_pos then
		attackerPosition = args.step_pos
	else
		attackerPosition = attacker:GetPos()
	end
	if not ignore_cover and targetIsUnit then
		ignore_cover = not target:IsAware()
	end
	
	actionResult = actionResult or action:GetActionResults(attacker, args) or empty_table
	local attackResultHits = table.icopy(actionResult)
	table.iappend(attackResultHits, actionResult.area_hits)
	table.iappend(s_PredictionNoLofTargets, actionResult.no_lof_targets or empty_table)
	for _, obj in ipairs(s_PredictionNoLofTargets) do
		if IsKindOf(obj, "Unit") then
			ObjModified(obj)
			if obj.ui_badge then
				obj.ui_badge:SetActive(true, "dmg")
			end
		end
	end
		
	if #attackResultHits == 0 then
		lClearPredictedAOE(aoeObjs)
		lClearPredictedExplosions(trapExplosions)
        ResumeInfiniteLoopDetection("AiCalc")
		return
	end

	local stealthKill = (actionResult.stealth_kill_chance or 0) > 0 and actionResult.stealth_kill_chance
	local hideConditional = false
	if actionResult and actionResult.chance_to_hit then
		hideConditional = CthVisible() and actionResult.chance_to_hit == 0
	end
	
	local results = {}
	if not targetIsPoint then
		results[target] = { total_damage = 0, direct_hit_damage = 0, stray_hit_damage = 0, obstructed = false, death = false }
	end
	local function lApplyResultsToPrediction(hits, action)
		for i, hit in ipairs(hits) do
			local obj = hit.obj
			if IsKindOf(obj, "CombatObject") and obj:IsDead() then goto continue end
			if not IsKindOfClasses(obj, "CombatObject", "Destroyable") then goto continue end
			
			if not IsKindOf(obj, "DamagePredictable") and false then -- Disabled in 184705
				-- highlight only
				if ShouldDestroyObject(obj) then
					SetInteractionHighlightRecursive(obj, true, true)
					s_PredictedHighlightedObjs[#s_PredictedHighlightedObjs + 1] = obj
				end
				goto continue
			end

			-- Special highlight for those hit by aoe
			if hit.aoe or IsOverwatchAction(action.id) then
				if not table.find(aoeObjs, obj) then
					if IsKindOf(obj, "Unit") then
						if (hit.aoe_type or "none") == "none" then
							obj:SetHighlightReason("area target", true)
						end
					elseif not IsKindOf(obj, "DamagePredictable") then
						if ShouldDestroyObject(obj) then
							SetInteractionHighlightRecursive(obj, true, true)
						end
					else
						obj:SetObjectMarking(3)
					end
				end
				
				s_PredictedAOEObjs[#s_PredictedAOEObjs + 1] = obj
			end
			
			if not IsKindOf(obj, "DamagePredictable") then
				goto continue
			end
			
			if IsKindOf(obj, "Trap") then
				if not obj:HitWillDamage(hit) then goto continue end
				SetInteractionHighlightRecursive(obj, true, true)
				s_PredictedHighlightedObjs[#s_PredictedHighlightedObjs + 1] = obj
			end

			local unit_dmg = results[obj] or { total_damage = 0, direct_hit_damage = 0, stray_hit_damage = 0, obstructed = false, death = false }
			results[obj] = unit_dmg
			unit_dmg.total_damage = unit_dmg.total_damage + hit.damage
			if hit.stray then
				unit_dmg.stray_hit_damage = unit_dmg.stray_hit_damage + hit.damage
			elseif not hit.aoe then
				unit_dmg.direct_hit_damage = unit_dmg.direct_hit_damage + hit.damage		
			end
			if hit.stuck then unit_dmg.obstructed = true end
			
			if IsKindOf(obj, "Unit") then
				if not obj:HasStatusEffect("Exposed") and hit.effects.Exposed and not s_PredictedExposedUnits[obj] then
					s_PredictedExposedUnits[obj] = true
					s_PredictedExposedUnits[#s_PredictedExposedUnits + 1] = obj
				end
				
				if not ignore_cover then
					local cover, any, coverage = obj:GetCoverPercentage(attackerPosition)
					if cover then
						-- Mock numbers for testing whether the cover counts as exposed.
						local value = 50
						local exposedValue = 100
						local coverEffectResult = InterpolateCoverEffect(coverage, value, exposedValue)
						-- Place the icon only if not considered exposed.
						if coverEffectResult ~= exposedValue then
							results[obj].cover = true
						end
					end
				end
				
				if not hit.ignore_armor and hit.armor then
					local armor, armorIcon, iconPath = obj:IsArmored(target_spot_group)
					-- It's possible for an aimed aoe shot to hit the armor of another body part.
					-- We don't show the armor icon in this case.
					if armor and armorIcon then
						results[obj].armor = iconPath .. (hit.armor_pen and hit.armor_pen[armor] and "ignored_" or "") .. armorIcon
					end
				end
			end
			
			::continue::
		end
		
		for obj, data in pairs(results) do
			local predictionIcon = false
			if data.obstructed then
				predictionIcon = "ObstructedIcon"
			elseif data.cover then
				predictionIcon = (s_PredictedExposedUnits[obj] or obj:HasStatusEffect("Exposed")) and "CoverExposeIcon" or "CoverIcon"
			elseif data.armor then
				predictionIcon = data.armor
			else
				-- Set a fake icon so the badge can at least activate and show
				-- that the unit is in range of the attack.
				predictionIcon = "InRange"
			end
			obj.SmallPotentialDamageIcon = predictionIcon
			
			local death = false
			obj.PotentialDamage = data.total_damage - data.direct_hit_damage - data.stray_hit_damage		
			if not hideConditional or obj ~= target then
				if args.multishot then
					local shot_damage = data.direct_hit_damage / Max(1, args.num_shots or 1)
					obj.PotentialDamageConditional = shot_damage
					obj.PotentialSecondaryConditional = data.direct_hit_damage - shot_damage
					if targetIsTrap and obj == target then
						death = data.total_damage >= obj:GetTotalHitPoints()
					else
						death = data.total_damage - obj.PotentialSecondaryConditional >= obj:GetTotalHitPoints()
					end
				else
					obj.PotentialDamageConditional = data.direct_hit_damage
					obj.PotentialSecondaryConditional = data.stray_hit_damage
					death = data.total_damage - data.stray_hit_damage >= obj:GetTotalHitPoints()
				end
			end
			data.death = death

			obj.StealthKillChance = stealthKill or -1
			obj.LargePotentialDamageIcon = stealthKill and "PotentialDeathIcon"
			
			table.insert_unique(PredictedDamageUnits, obj)
			ObjModified(obj)
			if obj.ui_badge then
				obj.ui_badge:SetActive(true, "dmg")
			end
		end
	end
	
	lApplyResultsToPrediction(attackResultHits, action)
	
	-- Create trap explosion predictions for traps that will explode due to the attack.
	local traps = {}
	for target, data in pairs(results) do
		if data.death and IsKindOf(target, "Trap") and target.discovered_trap and target.visible and (not IsKindOf(target, "BoobyTrappable") or target.boobyTrapType == const.BoobyTrapExplosive) then
			traps[#traps + 1] = target
		end
	end
	
	local newExplosionMeshes = traps and {}
	for i, t in ipairs(traps) do
		local aoeParams = t:GetAreaAttackParams(nil, attacker)
		local explosion_pos = t:GetPos()
		if not explosion_pos:IsValidZ() then explosion_pos = explosion_pos:SetTerrainZ() end
		
		local range = aoeParams.max_range * const.SlabSizeX
		local step_positions, step_objs, los_values = GetAOETiles(explosion_pos, aoeParams.stance, range)
		local existingMeshIdx = table.find(trapExplosions, "source", t)
		local explosionMesh = CreateAOETilesCircle(step_positions, step_objs, existingMeshIdx and trapExplosions[existingMeshIdx], explosion_pos, range, los_values, "ExplodingBarrelRange_Tiles")
		explosionMesh:SetColorFromTextStyle("GrenadeRange")
		explosionMesh.source = t
		
		newExplosionMeshes[#newExplosionMeshes + 1] = explosionMesh
		if existingMeshIdx then table.remove(trapExplosions, existingMeshIdx) end
	end
	
	local aoeObjectsLeftover = table.subtraction(aoeObjs or empty_table, s_PredictedAOEObjs)
	lClearPredictedAOE(aoeObjectsLeftover)
	
	s_PredictedTrapExplosions = newExplosionMeshes
	lClearPredictedExplosions(trapExplosions)
end



function ApproachInteractableAI:Think(unit, debug_data)
    PauseInfiniteLoopDetection("AiCalc")
	local interactable = unit.ai_context and unit.ai_context.target_interactable
	if not interactable then
		assert(false, "ApproachInteractableAI doesn't have a target_interactable set")
		return
	end
	
	self:BeginStep("think", debug_data)
		local context = unit.ai_context
	
		self:BeginStep("destinations", debug_data)
			AIFindDestinations(unit, context)
		self:EndStep("destinations", debug_data)
	
		-- skip evaluation of optimal locations, use the interactable position
		local interaction_pos = unit:GetInteractionPosWith(interactable) or interactable:GetPos()
		context.best_dest = stance_pos_pack(interaction_pos, unit.stance)
	
		self:BeginStep("end of turn location", debug_data)
			AICalcPathDistances(context)
			AIPrecalcDamageScore(context)
			unit.ai_context.ai_destination = AIScoreReachableVoxels(context, self.EndTurnPolicies, self.OptLocWeight, debug_data and debug_data.reachable_scores)
		self:EndStep("end of turn location", debug_data)
		self:BeginStep("movement action", debug_data)
			context.movement_action = AIChooseMovementAction(context)
		self:EndStep("movement action", debug_data)
	self:EndStep("think", debug_data)
    ResumeInfiniteLoopDetection("AiCalc")
end

function CustomAI:Think(unit, debug_data)
    PauseInfiniteLoopDetection("AiCalc")
	self:BeginStep("think", debug_data)
		local context = unit.ai_context
	
		self:BeginStep("enum dests", debug_data)
			self:EnumDestinations(unit, context)
		self:EndStep("enum dests", debug_data)
		
		self:BeginStep("optimal location", debug_data)
			if not self:PickOptimalLoc(unit, context, debug_data) then
				AIFindOptimalLocation(context, debug_data and debug_data.optimal_scores)
			end
		self:EndStep("optimal location", debug_data)
	
		self:BeginStep("end of turn location", debug_data)
			if self.override_attack_id ~= "" then
				context.override_attack_id = self.override_attack_id
			end
			if self.override_cost_id and CombatActions[self.override_cost_id] then
				context.override_attack_cost = CombatActions[self.override_cost_id]:GetAPCost(unit)
			end
			if not self:EvalDamageScore(unit, context) then
				AIPrecalcDamageScore(context)
			end
			context.override_attack_id = nil
			context.override_attack_cost = nil
			if not self:PickEndTurnLoc(unit, context, debug_data) then
				local policies = self:PickEndTurnPolicies(unit, context) or self.EndTurnPolicies
				unit.ai_context.ai_destination = AIScoreReachableVoxels(context, policies, self.OptLocWeight, debug_data and debug_data.reachable_scores)
			end
		self:EndStep("end of turn location", debug_data)
		self:BeginStep("movement action", debug_data)
			context.movement_action = AIChooseMovementAction(context)
		self:EndStep("movement action", debug_data)
	self:EndStep("think", debug_data)
    ResumeInfiniteLoopDetection("AiCalc")
end


function AIGetWeaponCheckRange(unit, weapon, action)
	if IsKindOf(weapon, "MeleeWeapon") then
		local tiles = unit.body_type == "Large animal" and 2 or 1
		local range = (2 * tiles + 1) * const.SlabSizeX / 2
		return range, true
	elseif IsKindOf(weapon, "Firearm") then
		local max_range = weapon.WeaponRange * const.SlabSizeX
		if action.AimType ~= "cone" then
			max_range = 15 * max_range / 10
		end
		return max_range
	end
end




function AICalcAOETargetPoints(context, min_range, max_range, max_radius)
	local target_pts = {}
	local unit = context.unit
	local enemies = context.enemies
	
	-- add enemy positions
	for i, enemy in ipairs(enemies) do
		if VisibilityCheckAll(unit, enemy, nil, const.uvVisible) then
			target_pts[#target_pts + 1] = context.enemy_pos[enemy]
		end
	end
	
	local num_targets = #target_pts
	-- add midpoints of enemy pairs
	for i = 1, num_targets - 1 do
		for j = i + 1, num_targets do
			local pt = (target_pts[i] + target_pts[j]) / 2
			if not max_radius or pt:Dist(target_pts[i]) <= max_radius then
				target_pts[#target_pts + 1] = pt
			end
		end
	end
	
	-- add midpoints of enemy triples
	for i = 1, num_targets - 2 do
		for j = i + 1, num_targets - 1 do
			for k = j + 1, num_targets do
				local pt = (target_pts[i] + target_pts[j] + target_pts[k]) / 3
				if not max_radius or pt:Dist(target_pts[i]) <= max_radius then
					target_pts[#target_pts + 1] = pt
				end
			end
		end
	end
	--print(target_pts)
	-- filter out target points not in range
	AIFilterTargetPoints(unit, target_pts, min_range, max_range)
	--print(target_pts)
	--print(min_range/ const.SlabSizeX)
	--print(max_range/ const.SlabSizeX)
	
	return target_pts
end


function AIPrecalcConeTargetZones(context, action_id, additional_target_pt, stance)
	if context.target_locked then return {} end
	
	local unit = context.unit
	local weapon = context.weapon
	local params = weapon:GetAreaAttackParams(action_id, unit)

	local min_range = (params.min_range or 2) * const.SlabSizeX
	local max_range = (params.max_range or 10) * const.SlabSizeX

	local target_pts = AICalcAOETargetPoints(context, min_range, max_range)
	if additional_target_pt then
		target_pts[#target_pts + 1] = additional_target_pt
	end

	-- calc cone areas for each remaining target point
	local zones = {}
	local cone_angle = params.cone_angle
	local targets = {}
	local attack_pos = unit:GetPos() -- make sure we're using the current position in case the unit has moved
	local units = table.copy(context.enemies)
	table.iappend(units, GetAllAlliedUnits(unit))
	local unit_sight = unit:GetSightRadius()
	
	for zi, pt in ipairs(target_pts) do
		local dir = pt - attack_pos
		if dir:Len() > 0 then
			local target_pos = (attack_pos + SetLen(dir, max_range)):SetTerrainZ()
			local zone = {
				target_pos = target_pos,
				units = {},
			}
			zones[#zones + 1] = zone
		
			local angle = CalcOrientation(attack_pos, pt)
			local los_any, los_targets = CheckLOS(units, unit, unit:GetDist(target_pos), nil, cone_angle, angle)
			if los_any then
				for i, target_unit in ipairs(units) do
					if los_targets[i] and IsValidTarget(target_unit) then
						zone.units[#zone.units + 1] = target_unit
						table.insert_unique(targets, target_unit)
					end
				end
			end
		end
	end
	
	local check_ally
	if action_id == "Overwatch" then
		local atk_action = context.default_attack
		local aim_type = atk_action.AimType
		local is_aoe = aim_type == "cone" or aim_type == "aoe" or aim_type == "parabola aoe" or aim_type == "line aoe"
		check_ally = not is_aoe
	end
	
	-- filter LOS targets
	--local max_distance = Min(unit_sight, weapon:GetMaxRange())
	local max_distance =  weapon:GetMaxRange()
	local los_any, los_targets = CheckLOS(targets, unit, max_distance)
	if not los_any then
		for _, zone in ipairs(zones) do
			table.iclear(zone.units)
		end
		return zones
	end
	for i = #targets, 1, -1 do
		if not los_any or not los_targets[i] then
			for _, zone in ipairs(zones) do
				table.remove_value(zone.units, targets[i])
			end
			table.remove(targets, i)
		end
	end
	-- check chance to hit
	local targets_attack_data = GetLoFData(unit, targets, {
		obj = unit,
		action_id = context.default_attack.id,
		weapon = weapon,
		stance = unit.stance,
		range = max_distance,
		target_spot_group = "Torso",
		prediction = true,
	})
	local action = CombatActions[action_id]
	local args = { target_spot_group = false, aim = 4 }
	if action.id == "MGSetup" then
		return zones
	end
	for i, attack_data in ipairs(targets_attack_data) do
		local target = targets[i]
		local chance_to_hit = 0
		if attack_data and not attack_data.stuck then
			for j, hit_info in ipairs(attack_data.lof) do
				if not check_ally or hit_info.ally_hits_count == 0 then
					args.target_spot_group = hit_info.target_spot_group
					chance_to_hit = unit:CalcChanceToHit(target, action, args, "chance_only")
					if chance_to_hit > 0 then
						break
					end
				end
			end
		end
		if chance_to_hit == 0 then
			for _, zone in ipairs(zones) do
				table.remove_value(zone.units, target)
			end
		end
	end
	return zones
end



function AIPickScoutLocation(unit)
	local AIScoutLocationSearchRadius = 80 * guim

	-- pick a new position around alive enemy randomly, prefer non-hidden enemies
	local enemies = GetAllEnemyUnits(unit)
	
	if #enemies == 0 then
		return
	end

	local targets
	local nearest, nearby = {}, {}
	for _, enemy in ipairs(enemies) do
		local dist = unit:GetDist(enemy)
		if dist <= AIScoutLocationSearchRadius then
			nearest[#nearest + 1] = enemy
			targets = nearest
		elseif dist <= 2*AIScoutLocationSearchRadius then
			nearby[#nearby + 1] = enemy
			targets = targets or nearby
		end
	end
	targets = targets or enemies
	local enemy = table.interaction_rand(enemies, "Combat")
	
	local ux, uy, uz = enemy:GetGridCoords()
	local px, py, pz = VoxelToWorld(ux, uy, uz)
	local r = AIScoutLocationSearchRadius
	local bbox = box(px - r, py - r, 0, px + r + 1, py + r + 1, MapSlabsBBox_MaxZ)
	
	local dests, dest_added = {}, {}
	local function push_dest(x, y, z, dests, dest_added, ux, uy, uz)
		local gx, gy, gz = WorldToVoxel(x, y, z)
		
		if not IsCloser(gx, gy, gz, ux, uy, uz, AIScoutLocationSearchRadius) then
			return
		end
				
		local world_voxel = point_pack(x, y, z)
		if not dest_added[world_voxel] then
			dests[#dests + 1] = world_voxel
			dest_added[world_voxel] = true
		end		
	end
	
	ForEachPassSlab(bbox, push_dest, dests, dest_added, ux, uy, uz)
	
	if #dests > 0 then
		local voxel = table.interaction_rand(dests, "Combat")
		local x, y, z = point_unpack(voxel)
		return point(x, y, z)
	end	
end
