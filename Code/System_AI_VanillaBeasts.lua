-- JAZZ-AI beasts: vanilla CombatAI copies.
-- Non-human units (Crocodile / Hyena / Hen) must not run JAZZ Dump, dest caps,
-- cover-disengage, or firearm Ensure. StandardAI:Think still calls these
-- globals; wrappers in CombatAI.lua / AiActions.lua dispatch here.

function JazzAI_UsesJazzCombatAI(unit)
	return IsValid(unit) and unit.species == "Human"
end

function JazzAI_ContextUsesJazzCombatAI(context)
	return JazzAI_UsesJazzCombatAI(context and context.unit)
end

function JazzAI_BeastPickNearestEnemy(unit, enemies)
	local best, best_d
	for _, enemy in ipairs(enemies or empty_table) do
		if IsValidTarget(enemy) and not (IsKindOf(enemy, "Unit") and enemy:IsIncapacitated()) then
			local d = unit:GetDist(enemy)
			local eh = enemy.handle or 0
			if not best or d < best_d or (d == best_d and eh < (best.handle or 0)) then
				best, best_d = enemy, d
			end
		end
	end
	return best
end

function JazzAI_BeastLockNearestEnemy(context)
	if type(context) ~= "table" or not IsValid(context.unit) then
		return false
	end
	local locked = JazzAI_BeastPickNearestEnemy(context.unit, context.enemies)
	context.target_locked = locked or false
	return locked
end

function JazzAI_BeastClosestDestToTarget(dests, target, fallback)
	if not target then
		return fallback
	end
	local tpos = GetPackedPosAndStance(target)
	if not tpos then
		return fallback
	end
	local best, best_d = fallback, fallback and stance_pos_dist(fallback, tpos) or nil
	for _, dest in ipairs(dests or empty_table) do
		if dest then
			local d = stance_pos_dist(dest, tpos)
			if not best_d or d < best_d then
				best, best_d = dest, d
			end
		end
	end
	return best
end

function JazzAI_BeastFindOptimalLocation(context)
	JazzAI_BeastLockNearestEnemy(context)
	local dest = JazzAI_BeastClosestDestToTarget(
		context.all_destinations,
		context.target_locked,
		context.unit_stance_pos
	)
	context.best_dest = dest
	return dest
end

function JazzAI_BeastScoreNearestEnemyDest(context)
	JazzAI_BeastLockNearestEnemy(context)
	local stay = context.unit_stance_pos
	if context.voxel_to_dest and context.unit_world_voxel then
		stay = context.voxel_to_dest[context.unit_world_voxel] or stay
	end
	local dest = JazzAI_BeastClosestDestToTarget(context.destinations, context.target_locked, stay)
	context.ai_destination = dest
	context.best_end_dest = dest
	return dest, 100
end

function JazzAI_VanillaGetAttackTargetingOptions(unit, context, target, action, targeting)
	local body_parts
	targeting = targeting or context.archetype.BaseAttackTargeting
	if IsKindOf(target, "Unit") and targeting then
		action = action or context.default_attack
		local args = { target = target, aim = 0 }
		local parts = target:GetBodyParts(context.weapon)
		local valid, fallback
		for _, part in ipairs(parts) do
			args.target_spot_group = part.id
			local results = action:GetActionResults(unit, args)
			body_parts = body_parts or {}
			results.chance_to_hit = results.chance_to_hit or 0
			table.insert(body_parts, {id = part.id, chance = results.chance_to_hit})
			if results.chance_to_hit > 0 then
				fallback = fallback or {id = part.id, chance = results.chance_to_hit}
				if targeting[part.id] then
					valid = true
				end
			end			
		end
		if not valid then
			table.insert(body_parts, fallback)
		end
	end
	return body_parts
end

function JazzAI_VanillaPlayAttacks(unit, context, dbg_action, force_or_skip_action)
	-- filter enemies because they might have been killed by a teammate
	if g_AIExecutionController then
		g_AIExecutionController:Log("Unit %s (%d) start attack sequence", unit.unitdatadef_id, unit.handle)
	end
	local enemies = context.enemies
	for i = #enemies, 1, -1 do
		if not IsValidTarget(enemies[i]) then
			table.remove(enemies, i)
		end
	end
	
	local remaining_free_ap = unit.free_move_ap
	unit:RemoveStatusEffect("FreeMove") -- lose any remaining free movement points, we're going to use actions now
	AIUpdateContext(context, unit)

	if g_AIExecutionController then
		g_AIExecutionController:Log("  Num enemies: %d", #enemies)
		g_AIExecutionController:Log("  Action Points: %d", unit.ActionPoints)
	end
	
	local dest = not force_or_skip_action and context.ai_destination or GetPackedPosAndStance(unit)
		
	-- recalc target to make sure we're firing at a valid target, but prefer the already picked target if there's one
	--table.insert(g_AIDamageScoreLog, string.format("[%s] JazzAI_VanillaPlayAttacks (%s)", _InternalTranslate(unit.Name or ""), context.archetype.id))
	context.dest_ap[dest] = context.dest_ap[dest] or unit.ActionPoints	
	JazzAI_VanillaPrecalcDamageScore(context, {dest}, context.target_locked or (context.dest_target or empty_table)[dest])

	-- archetype signature actions
	local signature_action
	if dbg_action then
		context.action_states = context.action_states or {}
		context.action_states[dbg_action] = {}
		dbg_action:PrecalcAction(context, context.action_states[dbg_action])
		if dbg_action:IsAvailable(context, context.action_states[dbg_action]) then
			signature_action = dbg_action
		elseif force_or_skip_action then
			table.insert(failed_actions, dbg_action.BiasId or dbg_action.class)
			return
		end
	end
	if not context.reposition and not unit:HasStatusEffect("Numbness") then
		signature_action = signature_action or AIChooseSignatureAction(context)
	end
	
	local default_attack = context.default_attack
	local default_attack_vr = "AIAttack"
	if default_attack and default_attack.FiringModeMember and default_attack.FiringModeMember == "AttackShotgun" then
		default_attack_vr = "AIDoubleBarrel"
	end
	local voice_response = signature_action and (signature_action:GetVoiceResponse() or "") or default_attack_vr
	if voice_response == "" then 
		voice_response = nil
	end
	
	if signature_action then
		if g_AIExecutionController then
			g_AIExecutionController:Log("  Signature Action: %s", signature_action:GetEditorView())
		end
		signature_action:OnActivate(unit)
		--printf("[signature] %s (%d)", _InternalTranslate(unit.Name or ""), unit.handle)
		if voice_response then
			context.action_states[signature_action].args = context.action_states[signature_action].args or {}
			context.action_states[signature_action].args.voiceResponse = voice_response
		end
		local status = signature_action:Execute(context, context.action_states[signature_action])
		context.ap_after_signature = unit.ActionPoints
		if status then -- support signature actions that want to restart or stop ai turn execution
			return status
		end
		AIReloadWeapons(unit)
		context.max_attacks = context.max_attacks - 1
	else
		if g_AIExecutionController then
			g_AIExecutionController:Log("  No Signature Action chosen")
		end
	end

	local target = (context.dest_target or empty_table)[dest]
	if signature_action and (not IsValidTarget(target) or (IsKindOf(target, "Unit") and target:IsIncapacitated())) then
		--table.insert(g_AIDamageScoreLog, string.format("[%s] TargetChange (%s)", _InternalTranslate(unit.Name or ""), context.archetype.TargetChangePolicy))
		if context.archetype.TargetChangePolicy == "restart" then
			return "restart"
		end
		context.dest_ap[dest] = unit.ActionPoints
		context.target_locked = nil
		JazzAI_VanillaPrecalcDamageScore(context, {dest})
		target = context.dest_target[dest]		
	end

	if IsValidTarget(target) then
		if g_AIExecutionController then
			g_AIExecutionController:Log("  Target: %s", IsKindOf(target, "Unit") and target.unitdatadef_id or target.class)
		end
		-- revert to basic attacks
		local attacks, aim = JazzAI_VanillaCalcAttacksAndAim(context, unit.ActionPoints)
		if context.default_attack.id == "Bombard" and AICheckIndoors(dest) then
			attacks = 0
		end

		local args = { target = target, voiceResponse = voice_response }
		if attacks > 1 then
			unit:SequentialActionsStart()
		end
		if g_AIExecutionController then
			g_AIExecutionController:Log("  Executing %d attacks...", attacks)
		end
		local body_parts = JazzAI_VanillaGetAttackTargetingOptions(unit, context, target)
		
		for i = 1, attacks do
			args.aim = aim[i]
			args.target_spot_group = nil
			if body_parts and #body_parts > 0 then
				local pick = table.weighted_rand(body_parts, "chance", InteractionRand(1000000, "Combat"))
				if pick then
					args.target_spot_group = pick.id
				end
			end
			Sleep(0)
			local result = AIPlayCombatAction(context.default_attack.id, unit, nil, args)
			context.max_attack = context.max_attacks - 1
			if g_AIExecutionController then
				g_AIExecutionController:Log("  Attack %d result: %s", i, tostring(result))
			end
			if IsSetpiecePlaying() then
				unit:SequentialActionsEnd()
				return
			end
			AIReloadWeapons(unit)
			if not result or i == attacks or not IsValidTarget(unit) or context.max_attacks <= 0 then
				break
			end
			while IsKindOf(target, "Unit") and target:IsGettingDowned() do
				WaitMsg("UnitDowned", 20)
			end
			if not IsValidTarget(target) or (IsKindOf(target, "Unit") and target:IsIncapacitated()) then
				--table.insert(g_AIDamageScoreLog, string.format("[%s] TargetChange (%s)", _InternalTranslate(unit.Name or ""), context.archetype.TargetChangePolicy))
				if context.archetype.TargetChangePolicy == "restart" then
					unit:SequentialActionsEnd()
					return "restart"
				end
				-- look for another target
				context.dest_ap[dest] = unit.ActionPoints
				context.target_locked = nil
				JazzAI_VanillaPrecalcDamageScore(context, {dest})
				target = context.dest_target[dest]
				if not IsValidTarget(target) then
					break
				end
			end
			Sleep(0)
		end
		unit:SequentialActionsEnd()
	elseif unit:HasStatusEffect("StationedMachineGun") and CombatActions.MGPack:GetUIState({unit}) == "enabled" then
		unit:SequentialActionsEnd()
		AIPlayCombatAction("MGPack", unit)
		return "restart"
	else
		if g_AIExecutionController then
			g_AIExecutionController:Log("  No target")
		end		
	end
	unit:SequentialActionsEnd()
	
	while not unit:IsIdleCommand() do
		WaitMsg("Idle", 50)
	end

	if unit.ActionPoints + remaining_free_ap == context.start_ap and not unit:HasStatusEffect("ManningEmplacement") then
		-- no action was taken, use a fallback one
		-- if all fails, move toward optimal loc
		if context.closest_dest then
			unit:GainAP(remaining_free_ap)
			local dest = context.closest_dest
			local x, y, z, stance_idx = stance_pos_unpack(dest)
			local move_stance_idx = context.dest_combat_path[dest]
			local cpath = context.combat_paths[move_stance_idx]
			local pt = SnapToPassSlab(x, y, z)
			local path = pt and cpath and cpath:GetCombatPathFromPos(pt)
			if path then
				local goto_stance = StancesList[move_stance_idx]
				if goto_stance ~= unit.stance then
					AIPlayChangeStance(unit, goto_stance, point(point_unpack(path[2])))
				end
				local goto_ap = unit.ActionPoints -- context.dest_ap[dest] --cpath.paths_ap[point_pack(x, y, z)] or 0
				context.ai_destination = path[1]
				AIPlayCombatAction("Move", unit, goto_ap, { goto_pos = point(point_unpack(path[1])), fallbackMove = true, goto_stance = stance_idx })
			end
		end
		if unit:GetDist(context.unit_pos) < const.SlabSizeX / 2 then
			local revert = true
			if context.archetype.FallbackAction == "overwatch" then
				-- try to place overwatch
				revert = not AIPlaceFallbackOverwatch(unit, context)
			end
			if revert then
				-- we're stuck somewhere and unable to move or act, revert back to being Unaware (only if no sight of any enemies)
				local sight = false
				for _, enemy in ipairs(context.enemies) do
					sight = sight or HasVisibilityTo(unit, enemy)
				end
				if not sight then
					table.insert(g_UnawareQueue, unit)
				end
			end
		end
	end
end

function JazzAI_VanillaExecuteUnitBehavior(unit, force_or_skip_action)
	if not g_Combat or not IsValid(unit) or unit:IsDead() then
		return
	end
	
	if unit.ai_context.behavior then
		local status = unit.ai_context.behavior:Play(unit)
		if g_AIExecutionController then
			g_AIExecutionController:Log("  Behavior %s for unit %s (%d) returned '%s'", unit.ai_context.behavior:GetEditorView(), unit.unitdatadef_id, unit.handle, tostring(status))
		end

		if status then -- support behaviors that want to restart or stop the unit's ai
			return status 
		end
	end

	-- recheck unit, they could be killed or despawned during Play
	if IsValid(unit) and not unit:IsDead() then
		-- use the rest of the ap (if any) in signature actions and basic attacks
		return JazzAI_VanillaPlayAttacks(unit, unit.ai_context, unit.ai_context.forced_signature_action, force_or_skip_action) or JazzAI_VanillaTakeCover(unit)
	end
end

function JazzAI_VanillaTakeCover(unit, context)
	local context = unit.ai_context
	if unit:HasPreparedAttack() or not context or ((context.ap_after_signature or 0) <= 0) then
		return
	end
	local cover_high, cover_low = GetCoverTypes(unit)
	if not cover_high and not cover_low then
		return
	end
	if unit.species == "Human" and unit.stance ~= "Prone" then
		local context = unit.ai_context
		local chance = context and context.behavior and context.behavior.TakeCoverChance or 0
		if chance > 0 and (chance >= 100 or unit:Random(100) < chance) then
			local dest = GetPackedPosAndStance(unit)
			local enemy_visible = context.enemy_visible
			local enemy_pos = context.enemy_pack_pos_stance
			for _, enemy in ipairs(context.enemies) do
				if (enemy_visible[enemy] and GetCoverFrom(dest, enemy_pos[enemy]) or 0) > 0 then
					AIPlayCombatAction("TakeCover", unit, 0)
					return
				end
			end
		end
	end
	if cover_low then
		AIPlayCombatAction("StanceCrouch", unit, 0)
	end
end

function JazzAI_VanillaFindDestinations(unit, context)
	local pos = GetPassSlab(unit) or unit:GetPos()
	local destinations, paths, dest_ap, dest_path, voxel_to_dest, closest_free_pos = JazzAI_VanillaBuildArchetypePaths(unit, pos, context)	
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

	context.all_destinations = JazzAI_VanillaEnumValidDests(context)
end

function JazzAI_VanillaCreateContext(unit, context)
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
		enemies = table.ifilter(GetAllEnemyUnits(unit), function(idx, enemy) return not enemy:HasStatusEffect("Hidden") end)
	end
	
	-- special-case when having ManningEmplacement status - filter out non targetable enemies
	if unit:HasStatusEffect("ManningEmplacement") then
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
	context.default_attack_cost = default_attack and default_attack:GetAPCost(unit) or 0
	context.EffectiveRange = IsKindOf(weapon, "Firearm") and weapon.WeaponRange / 2 or 1
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
	
	NetUpdateHash("AICreateContext", unit, pos, unit.stance, context.start_ap, context.archetype.id, context.max_attacks, weapon and weapon.class, weapon and weapon.id, default_attack and default_attack.id)
	
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
		JazzAI_VanillaFindDestinations(unit, context)
	end
	JazzAI_VanillaUpdateDestLosCache(unit, context)
	
	for i, ally in ipairs(context.allies) do
		local x, y, z = ally:GetGridCoords()
		context.ally_grid_voxel[ally] = point_pack(x, y, z)
		context.ally_pack_pos_stance[ally] = GetPackedPosAndStance(ally)
		context.ally_pos[ally] = ally:GetPos()
	end

	JazzAI_BeastLockNearestEnemy(context)
	unit.ai_context = context
	return context
end

function JazzAI_VanillaUpdateDestLosCache(unit, context)
	assert(CurrentThread()) -- the function will sleep internally due to the amount of calculations performed
	--local tStart = GetPreciseTicks()
	--ic("JazzAI_VanillaUpdateDestLosCache start", #units)
	local sight = unit:GetSightRadius()
	local all_destinations = context.all_destinations
	local enemies = context.enemies
	if #enemies == 0 then return end
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
	--printf("AIUpdateDestLosCache: %d ms for %s", GetPreciseTicks() - tStart, unit.unitdatadef_id)
end

function JazzAI_VanillaCalcAttacksAndAim(context, ap)
	local aim_cost = const.Scale.AP
	if GameState.RainHeavy then
		aim_cost = MulDivRound(aim_cost, 100 + const.EnvEffects.RainAimingMultiplier, 100)
	end
	
	local cost = context.default_attack_cost
	if not cost or cost <= 0 then
		return 1, {}
	end
	local num_attacks = Min(ap / cost, context.max_attacks)
	
	if context.force_max_aim then
		num_attacks = Min(ap / (cost + aim_cost * context.weapon.MaxAimActions), context.max_attacks)
	end
	
	local remaining = ap - num_attacks * cost
	local aims = {}
	
	local attack_idx = 1
	while remaining > aim_cost do
		local aim = (aims[attack_idx] or 0) + 1
		if aim > context.weapon.MaxAimActions then 
			break 
		end
		aims[attack_idx] = aim
		attack_idx = attack_idx + 1
		if attack_idx > num_attacks then
			attack_idx = 1
		end
		remaining = remaining - aim_cost
	end
	
	return num_attacks, aims
end

function JazzAI_VanillaBuildArchetypePaths(unit, pos, context)
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
		return destinations, paths, dest_ap, dest_path, voxel_to_dest, voxel
	end

	local archetype = unit:GetArchetype()
	local goto_stance = archetype.MoveStance
	local pref_stance = archetype.PrefStance

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

	return destinations, paths, dest_ap, dest_path, voxel_to_dest, move_path.closest_free_pos
end

function JazzAI_VanillaScoreDest(context, policies, dest, grid_voxel, base_score, visual_voxels, score_details)
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
		local failed = policy.Required and pscore == 0
		score = score + pscore
		if score_details then
			score_details[#score_details + 1] = (failed and "[FAILED] " or "") .. policy:GetEditorView()
			score_details[#score_details + 1] = pscore
		end
		if failed then
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
	
	return score
end

function JazzAI_VanillaEnumValidDests(context)
	local unit = context.unit
	local r = context.archetype.OptLocSearchRadius * const.SlabSizeX
	local ux, uy, uz = point_unpack(context.unit_grid_voxel)
	local px, py, pz = VoxelToWorld(ux, uy, uz)
	local bbox = box(px - r, py - r, 0, px + r + 1, py + r + 1, MapSlabsBBox_MaxZ)
	
	local dests, dest_added = {}, {}
	local function push_dest(x, y, z, context, dests, dest_added, ux, uy, uz)
		local gx, gy, gz = WorldToVoxel(x, y, z)
		
		if not IsCloser(gx, gy, gz, ux, uy, uz, context.archetype.OptLocSearchRadius) then
			return
		end
		if not CanOccupy(unit, x, y, z) then
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
	return dests
end

function JazzAI_VanillaFindOptimalLocation(context, dest_score_details)
	if context.best_dest then
		-- optimal location doesn't change across behaviors, no need to recalc it
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
		local score = JazzAI_VanillaScoreDest(context, policies, dest, grid_voxel, 0, unit_voxels, scores)
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
	return context.best_dest
end

function AICalcPathDistances(context)
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
end

function JazzAI_VanillaGetWeaponCheckRange(unit, weapon, action)
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

function JazzAI_VanillaPrecalcDamageScore(context, destinations, preferred_target, debug_data)
	local unit = context.unit
	local weapon = context.weapon
	local action = CombatActions[context.override_attack_id or false] or context.default_attack
	local archetype = context.archetype
	local behavior = context.behavior

	if not weapon or context.reposition or unit:HasStatusEffect("Burning") then
		return
	end
	if not destinations and context.damage_score_precalced then
		return
	end

	local action_targets = action:GetTargets({unit})
	local targets = table.ifilter(action_targets, function(idx, target) return unit:IsOnEnemySide(target) end)
	local locked = JazzAI_BeastLockNearestEnemy(context)
	if locked then
		targets = { locked }
		preferred_target = locked
	end
	if #targets == 0 then
		return
	end
	context.damage_score_precalced = true
	local target_score_mod = {}
	local tsr = archetype.TargetScoreRandomization
	for i, target in ipairs(targets) do
		target_score_mod[i] = 100 + ((tsr > 0) and unit:RandRange(-tsr, tsr) or 0)
	end
	context.target_score_mod = target_score_mod

	local base_mod = unit[weapon.base_skill]
	local cost_ap = context.override_attack_cost or context.default_attack_cost

	local max_check_range, is_melee = JazzAI_VanillaGetWeaponCheckRange(unit, weapon, action)
	local is_heavy = IsKindOf(weapon, "HeavyWeapon")

	local hit_modifiers = Presets["ChanceToHitModifier"]["Default"]
	-- stance mod
	local modCrouchBonus = 0
	local modProneBonus = 0
	--if IsKindOf(weapon, "Firearm") then
		--modCrouchBonus = hit_modifiers.AttackerStance:ResolveValue("CrouchBonus")
		--modProneBonus = hit_modifiers.AttackerStance:ResolveValue("ProneBonus")
		local value = GetComponentEffectValue(weapon, "AccuracyBonusProne", "bonus_cth")
		if value then
			modProneBonus = modProneBonus + value
		end
	--end
	-- ground difference mod
	local MinGroundDifference = hit_modifiers.GroundDifference:ResolveValue("RangeThreshold") * const.SlabSizeZ / 100
	local modHighGround = hit_modifiers.GroundDifference:ResolveValue("HighGround")
	local modLowGround = hit_modifiers.GroundDifference:ResolveValue("LowGround")
	-- cover
	local modCover = hit_modifiers.RangeAttackTargetStanceCover:ResolveValue("Cover")
	local modSameTarget = hit_modifiers.SameTarget:ResolveValue("Bonus")
	
	local target_policies = archetype.TargetingPolicies
	if behavior and #(behavior.TargetingPolicies or empty_table) > 0 then
		target_policies = behavior.TargetingPolicies
	end
	
	local dest_target = context.dest_target
	local dest_target_score = context.dest_target_score
	local dest_ap = context.dest_ap
	local aim_mod = Presets.ChanceToHitModifier.Default.Aim
	local dest_cth = {}
	context.dest_cth = dest_cth
	local lof_params
	local attacker_pos = unit:GetPos()
	
	-- script-driven modifiers (based on groups)
	local target_modifiers
	for _, groupname in ipairs(unit.Groups) do
		local group_modifiers = gv_AITargetModifiers[groupname]
		for target_group, mod in pairs(group_modifiers) do
			target_modifiers = target_modifiers or {}
			target_modifiers[target_group] = (target_modifiers[target_group] or 0) + mod
			for _, obj in ipairs(Groups[target_group]) do
				if IsKindOf(obj, "Unit") and not table.find(targets, obj) then				
					table.insert(targets, obj) -- make sure the target is considired regardless if it's an enemy or not
					table.insert(target_score_mod, 100 + ((tsr > 0) and unit:RandRange(-tsr, tsr) or 0))
				end
			end
		end
	end
	
	if unit:HasStatusEffect("StationedMachineGun") or unit:HasStatusEffect("ManningEmplacement") then
		local ow_units = {unit}
		targets = table.ifilter(targets, function(idx, target) return target:IsThreatened(ow_units, "overwatch") end)
	end
	
	if not IsValidTarget(preferred_target) or (IsKindOf(preferred_target, "Unit") and preferred_target:IsIncapacitated() or not table.find(targets, preferred_target)) then
		preferred_target = nil
	end

	if weapon and not is_melee then
		lof_params = {
			obj = unit,
			action_id = action.id,
			weapon = weapon,
			step_pos = false,
			stance = false,
			range = max_check_range,
			prediction = true,
			output_collisions = true,
		}
		if not destinations or #destinations > 1 then
			lof_params.target_spot_group = "Torso"
		end
	end
--[[	local logdata = {}
	if destinations then
		table.insert(g_AIDamageScoreLog, logdata)
	end
	logdata.preferred_target = preferred_target and (IsKindOf(preferred_target, "Unit") and _InternalTranslate(preferred_target.Name or "") or preferred_target.class) or tostring(preferred_target)--]]
	destinations = destinations or context.destinations
	NetUpdateHash("AIPrecalcDamageScore", unit, hashParamTable(destinations), hashParamTable(targets), preferred_target)
	for j, upos in ipairs(destinations) do
		local ux, uy, uz, ustance_idx = stance_pos_unpack(upos)
		local ustance = StancesList[ustance_idx]
		uz = uz or terrain.GetHeight(ux, uy)

		local ap = dest_ap[upos] or 0
		local best_target, best_cth
		local best_score = 0
		local potential_targets, target_score, target_cth = {}, {}, {}
		if weapon and ap >= cost_ap then
			local pos_mod = base_mod
			pos_mod = pos_mod + (ustance_idx == 2 and modCrouchBonus or ustance_idx == 3 and modProneBonus or 0)

			local targets_attack_data
			if not is_melee then
				attacker_pos = point(ux, uy, uz)
				lof_params.step_pos = point_pack(ux, uy, uz)
				lof_params.stance = ustance
				targets_attack_data = GetLoFData(unit, targets, lof_params)
			end
			for k, target in ipairs(targets) do
				local tpos = GetPackedPosAndStance(target)
				local dist = stance_pos_dist(upos, tpos)
				if dist <= (max_check_range or dist) and (is_melee or targets_attack_data[k] and not targets_attack_data[k].stuck) then
					local tx, ty, tz, tstance_idx = stance_pos_unpack(tpos)
					tz = tz or terrain.GetHeight(tx, ty)
					local hit_mod = pos_mod
					if not is_heavy then
						hit_mod = hit_mod + (uz > tz + MinGroundDifference and modHighGround or uz < tz - MinGroundDifference and modLowGround or 0)
						hit_mod = hit_mod + (unit:GetLastAttack() == target and modSameTarget or 0)
					end
					local target_cover = GetCoverFrom(tpos, upos)
					if target_cover == const.CoverLow or target_cover == const.CoverHigh then
						hit_mod = hit_mod + modCover
					end

					local penalty = is_heavy and 0 or (100 - weapon:GetAccuracy(dist))

					local mod = hit_mod - penalty --dist_penalty
					-- environmental modifiers when applicable
					local apply, value, target_spot_group, action, weapon1, weapon2, lof, aim, opportunity_attack
					apply, value = hit_modifiers.Darkness:CalcValue(unit, target, target_spot_group, action, weapon1, weapon2, lof, aim, opportunity_attack, attacker_pos)
					if apply then
						mod = mod + value
					end
					
					if not is_heavy and unit:IsPointBlankRange(target) then
						mod = MulDivRound(mod, 100 + const.AIPointBlankTargetMod, 100)
					end
					mod = Max(0, mod)
					
					if mod > const.AIShootAboveCTH then
						-- calc base score based on cth/attacks/aiming
						local base_mod = mod
						local attacks, aims = JazzAI_VanillaCalcAttacksAndAim(context, ap)
						mod = 0
						for i = 1, attacks do
							local use, bonus
							if (aims[i] or 0) > 0 then
								use, bonus = aim_mod:CalcValue(unit, nil, nil, nil, nil, nil, nil, aims[i])
							end
							mod = mod + base_mod + (use and bonus or 0)
						end
						-- modify score by archetype-specific weight and (optional) targeting policies
						mod = MulDivRound(mod, archetype.TargetBaseScore, 100)
						for _, policy in ipairs(target_policies) do
							local peval = policy:EvalTarget(unit, target)
							mod = mod + MulDivRound(peval or 0, policy.Weight, 100)
						end

						if IsKindOf(target, "Unit") and (target:IsDowned() or target:IsGettingDowned()) then
							mod = MulDivRound(mod, 5, 100)
						end

						local attack_data = targets_attack_data and targets_attack_data[k]
						local ally_in_danger = attack_data and (attack_data.best_ally_hits_count or 0) > 0
												
						if action and action.AimType == "cone" then
							ally_in_danger = ally_in_danger or AIAllyInDanger(context.allies, context.ally_pos, attacker_pos, target, const.AIFriendlyFire_LOFConeNear, const.AIFriendlyFire_LOFConeFar)
						else
							ally_in_danger = ally_in_danger or AIAllyInDanger(context.allies, context.ally_pos, attacker_pos, target, const.AIFriendlyFire_LOFWidth, const.AIFriendlyFire_LOFWidth)
						end
						if ally_in_danger then
							mod = MulDivRound(mod, const.AIFriendlyFire_ScoreMod, 100)
						end
						
						mod = MulDivRound(mod, target_score_mod[k], 100)
						
						-- apply group-based modifiers
						if target_modifiers and IsKindOf(target, "Unit") then
							local group_mod = 0
							for _, groupname in ipairs(target.Groups) do
								group_mod = group_mod + (target_modifiers[groupname] or 0)
							end
							if group_mod > 0 then
								mod = MulDivRound(mod, group_mod, 100)
							end
						end
						
						--[[table.insert(logdata, {
							name = IsKindOf(target, "Unit") and _InternalTranslate(target.Name or "") or target.class,
							score = mod
						})--]]
						
						if mod > 0 and target == preferred_target then
							best_target = target
							best_score = mod
							best_cth = base_mod
							potential_targets = {}
							break
						end

						best_score = Max(best_score, mod)
						target_cth[target] = base_mod
						target_score[target] = mod
						local threshold = MulDivRound(best_score or 0, const.AIDecisionThreshold, 100)
						if mod >= threshold then
							potential_targets[#potential_targets + 1] = target
							for i = #potential_targets, 1, -1 do
								local target = potential_targets[i]
								local score = target_score[target]
								if score < threshold then
									table.remove(potential_targets, i)
								end
							end
							--best_target, best_score, best_cth = target, mod, base_mod
						end
					end
				end
			end
		end
		
		if #potential_targets > 0 then
			local total = 0
			for _, target in ipairs(potential_targets) do
				local score = target_score[target]
				total = total + score
				if debug_data then
					debug_data[target] = score
				end
			end
			local roll = InteractionRand(total, "AIDecision")
			for _, target in ipairs(potential_targets) do
				local score = target_score[target]
				if roll < score then
					best_target = target
					break
				end
				roll = roll - score
			end
			best_target = best_target or potential_targets[#potential_targets] or false
			best_score = target_score[best_target] or 0
			best_cth = target_cth[best_target] or 0
		end
		
		--[[
		if destinations and IsKindOf(best_target, "Unit") then
			if best_target == preferred_target then
				printf("%s (%d) selected target (preferred): %s (score %d)", _InternalTranslate(unit.Name or ""), unit.handle, _InternalTranslate(best_target.Name or ""), best_score)
			else
				printf("%s (%d) selected target: %s (score %d)", _InternalTranslate(unit.Name or ""), unit.handle, _InternalTranslate(best_target.Name or ""), best_score)
				printf("  potential targets:")
				for _, target in ipairs(potential_targets) do
					printf("    %s (score %d)", _InternalTranslate(target.Name or ""), target_score[target])
				end
			end
		end--]]
		
		--logdata.chosen_target = best_target and (IsKindOf(best_target, "Unit") and _InternalTranslate(best_target.Name or "") or best_target.class) or tostring(best_target)
		dest_target_score[upos] = best_score
		dest_target[upos] = best_target
		dest_cth[upos] = best_cth
	end
end

