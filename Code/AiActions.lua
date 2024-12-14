function AIActionThrowGrenade:PrecalcAction(context, action_state)
	local action_id, grenade
	local actions = { "ThrowGrenadeA", "ThrowGrenadeB", "ThrowGrenadeC", "ThrowGrenadeD" }
	for _, id in ipairs(actions) do
		local caction = CombatActions[id]
		local cost = caction and caction:GetAPCost(context.unit) or -1
		if cost > 0 and context.unit:HasAP(cost) then
			action_id = id
			local weapon = caction:GetAttackWeapons(context.unit)
			local aoetype = weapon.aoeType or "none"
			if (IsKindOf(weapon, "Grenade") or IsKindOf(weapon, "Flare")) and self.AllowedAoeTypes[aoetype] then
				grenade = weapon			
				break
			end
		end
	end
	
	if not action_id or not grenade then
		return
	end
	
	local max_range = Min(self.MaxDist, grenade:GetMaxAimRange(context.unit) * const.SlabSizeX)
	local blast_radius = grenade.AreaOfEffect * const.SlabSizeX
	local target_pts
	if self.TargetLastAttackPos then 
		-- collect enemy last attack positions and pass them as target_pos array to AIPrecalcGrenadeZones
		for _, enemy in ipairs(context.enemies) do
			if enemy.last_attack_pos then
				target_pts = target_pts or {}
				target_pts[#target_pts + 1] = enemy.last_attack_pos
			end
		end
	end
	local zones = AIPrecalcGrenadeZones(context, action_id, self.MinDist, max_range, blast_radius, grenade.aoeType, target_pts)
	local zone, score = self:EvalZones(context, zones)
	if zone then
		action_state.action_id = action_id
		action_state.target_pos = zone.target_pos
		action_state.score = score * 10
	end
end

function AIReloadWeapons(unit)
	if IsMerc(unit) then return end

	local action = unit:GetDefaultAttackAction()
	local weapon1, weapon2 = action:GetAttackWeapons(unit)
	if weapon1 and weapon1.jammed then weapon1:RepairJammed(weapon1.Condition, unit) end
	if weapon2 and weapon2.jammed then weapon2:RepairJammed(weapon2.Condition, unit) end
--	target:SetActionCommand("ChangeStance", nil, nil, "Prone")
	--if weapon1 and weapon1.jammed then unit:SetActionCommand("UnjamWeapon", self.id, nil)  end
		--unit:SetActionCommand("UnjamWeapon", self.id, ap, args) 
	--if weapon2 and weapon2.jammed then unit:SetActionCommand("UnjamWeapon", self.id, nil)  end


	local firearms = select(3, unit:GetActiveWeapons("Firearm"))
	table.iappend(firearms, select(3, unit:GetActiveWeapons("HeavyWeapon")))
	for _, firearm in ipairs(firearms) do
		if not firearm.ammo then
			local ammos = unit:GetAvailableAmmos(firearm) or empty_table
			local ammo
			if #ammos > 0 then
				--ammo = ammos[1]
				ammo = PlaceInventoryItem(ammos[1].id)
				ammo.Amount = firearm.MagazineSize
				--ammo.Amount = Max(ammo.Amount, firearm.MagazineSize)
				unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
				CreateFloatingText(unit, T(160472488023, "Reload"))
				ObjModified(unit)
			else
				ammos = GetAmmosWithCaliber(firearm.Caliber, "sorted")
				if #ammos > 0 then
					ammo = PlaceInventoryItem(ammos[1].id)
					ammo.Amount = firearm.MagazineSize
					unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
					CreateFloatingText(unit, T(160472488023, "Reload"))
					DoneObject(ammo)
					ObjModified(unit)
				end
			end
		elseif firearm.ammo.Amount < Max(1, firearm.MagazineSize / 2) then
			local ammo = firearm.ammo
			ammo.Amount = firearm.MagazineSize
			unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
			CreateFloatingText(unit, T(160472488023, "Reload"))
			ObjModified(unit)
		end
	end
end

function AICalcAttacksAndAim(context, ap, target)
	local aim_cost = const.Scale.AP
	--if GameState.RainHeavy then
	--	aim_cost = MulDivRound(aim_cost, 100 + const.EnvEffects.RainAimingMultiplier, 100)
	--end
	local min_aim, max_aim = context.unit:GetBaseAimLevelRange(context.default_attack, false)


	local 	cost = context.default_attack_cost
	local num_attacks = Min(ap / cost, context.max_attacks)
	

	
	local remaining = ap - num_attacks * cost
	local aims = {}


	local attack_idx = 1
	local unit = context.unit

	if target then
		if context.force_max_aim 
		or (IsKindOfClasses(context.weapon,"SniperRifle","MachineGun") and (ap - cost * max_aim) > 0 and unit:GetDist(target) >= 2*const.SlabSizeX)
		or ((IsKindOf(context.weapon,"AssaultRifle")) and (ap - cost * max_aim) > 0 and unit:GetDist(target) >= (8) * const.SlabSizeX) 
		   then
			num_attacks = Min(Max(1,(ap / (cost + aim_cost * max_aim))), context.max_attacks)
			local aim = max_aim
			aims[attack_idx] = aim
			return num_attacks, aims
		end

		if unit:GetDist(target) <= 6*const.SlabSizeX then
			local num_attacks = Min(ap / cost)	
			local aim = min_aim or 0
			aims[attack_idx] = aim
			return num_attacks, aims
		end
	end


	local bonusaim = DivRound(context.weapon.AimAccuracy, 10)

	while remaining > aim_cost do
		local aim = (aims[attack_idx] or min_aim or 0) + bonusaim
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
	
	NetUpdateHash("AICalcAttacksAndAim", num_attacks, aims, aim_cost, context.force_max_aim)
	return num_attacks, aims
end

function AIPlayAttacks(unit, context, dbg_action, force_or_skip_action)
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
	--table.insert(g_AIDamageScoreLog, string.format("[%s] AIPlayAttacks (%s)", _InternalTranslate(unit.Name or ""), context.archetype.id))
	context.dest_ap[dest] = context.dest_ap[dest] or unit.ActionPoints	
	AIPrecalcDamageScore(context, {dest}, context.target_locked or (context.dest_target or empty_table)[dest])

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
		AIPrecalcDamageScore(context, {dest})
		target = context.dest_target[dest]		
	end

	if IsValidTarget(target) then
		if g_AIExecutionController then
			g_AIExecutionController:Log("  Target: %s", IsKindOf(target, "Unit") and target.unitdatadef_id or target.class)
		end
		-- revert to basic attacks
		local attacks, aim = AICalcAttacksAndAim(context, unit.ActionPoints, target)
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
		local body_parts = AIGetAttackTargetingOptions(unit, context, target)
		
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
				AIPrecalcDamageScore(context, {dest})
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



function AIPrecalcDamageScore(context, destinations, preferred_target, debug_data)
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

	local max_check_range, is_melee = AIGetWeaponCheckRange(unit, weapon, action)
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
						local attacks, aims = AICalcAttacksAndAim(context, ap, target)
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
						NetUpdateHash("AIPrecalcDamageScore_mod",target_score[target], mod, threshold)


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
				NetUpdateHash("AIPrecalcDamageScore_total",target_score[target], total)
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

