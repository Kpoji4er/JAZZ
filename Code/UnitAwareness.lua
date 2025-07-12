function PushUnitAlert(trigger_type, ...)
	if trigger_type == "discovered" and CheatEnabled("DisableDiscoveryAlert") then
		return
	end
	local param1, param2 = ...
	NetUpdateHash("PushUnitAlert", trigger_type, param1 and param1.class or "", param2 or 0)

	local pov_team = GetPoVTeam()
	local enemies = pov_team and pov_team.units and GetAllEnemyUnits(pov_team.units[1] or false)
	local enemies_alive
	for _, unit in ipairs(enemies) do
		if IsValidTarget(unit) then
			enemies_alive = true
			break
		end
	end
	if not enemies_alive then
		return 0, 0
	end

	local alerted
	local suspicious = 0
	local surprised = 0

	if trigger_type == "attack" then -- make target and damaged units aware
		local attacker, alerted_obj, from_stealth, hit_objs = ...
		local aware_state = (from_stealth or HasPerk(attacker, "FoxPerk")) and "surprised" or "aware"
		dbg_awareness_log(attacker, " alerts: attack")
		local units = IsValid(alerted_obj) and {alerted_obj} or alerted_obj
		for _, unit in ipairs(units) do
			local state = (g_Combat and unit:HasStatusEffect("Surprised")) and "aware" or aware_state
			local is_aware = unit:IsAware() or unit.pending_aware_state == "aware"
			local reason_id
			if state == "surprised" and not is_aware or (hit_objs and not table.find(hit_objs, unit)) then
				reason_id = "arSurprised"
			else
				reason_id = "arAttack"
			end
			local reason = T{Presets.AwareReasons.Default[reason_id].display_name, enemy = unit.Name, merc = attacker.Nick or attacker.Name}
			if unit:SetPendingAwareState(state, reason, attacker) then
				if state ~= "aware" then
					surprised = surprised + 1
				else
					if not alerted then alerted = {} end
					alerted[#alerted + 1] = unit
				end
				dbg_awareness_log("  ", unit, " alerted")
			end
			if unit.pending_aware_state == "aware" then
				local action = g_CurrentAttackActions[1]
				if action and action.attack_args and action.attack_args.target == unit then
					unit.pending_awareness_role = state == "surprised" and "surprised" or "attacked"
				end
			end
		end
	elseif trigger_type == "death" then
		local actor = ...
		dbg_awareness_log(actor, " alerts: dead")
		-- check units based on their sight/los toward actor
		local units
		for _, team in ipairs(g_Teams) do
			if not team.neutral then
				for _, u in ipairs(team.units) do
					if not u.dummy and not u:IsIncapacitated() and not u:IsAware() then
						local sight = u:GetSightRadius(actor)
						if IsCloser(u, actor, sight + 1) then
							if not units then units = {} end
							units[#units + 1] = u
						end
					end
				end
			end
		end
		if units then
			local los_any, los_targets = CheckLOS(units, actor)
			if los_any then
				for i, los_value in ipairs(los_targets) do
					if los_value then
						local unit = units[i]
						local reason = T{Presets.AwareReasons.Default.arSawDying.display_name, enemy = unit.Name}
						if unit:SetPendingAwareState("surprised", reason) then
							dbg_awareness_log("  ", unit, " is surprised")
							surprised = surprised + 1
						end
					end
				end
			end
		end
	elseif trigger_type == "dead body" then
		local actor, _units = ...
		local units
		for _, unit in ipairs(_units) do
            --print((unit.seen_bodies ~= {}) and (unit.seen_bodies ~= false))
            if unit.seen_bodies then
		    	if  not unit.seen_bodies[actor]
		    		and not (unit.dummy or unit.team.neutral or unit:IsDead() or unit:IsAware()) -- SetPendingAwareState ignores these units
		    		and IsCloser(unit, actor, unit:GetSightRadius(actor) + 1)
		    	then
		    		if not units then units = {} end
		    		units[#units + 1] = unit
		    	end
            end
		end
		if units then
			local los_any, los_targets = CheckLOS(units, actor)
			if los_any then
				local aware_state = g_Combat and "surprised" or "suspicious"
				for i, los_value in ipairs(los_targets) do
					if los_value then
						local unit = units[i]
						if unit:SetPendingAwareState(aware_state) then
							unit.suspicious_body_seen = actor:GetHandle()
							unit.seen_bodies[actor] = true
							dbg_awareness_log("  ", unit, " is suspicious")
							suspicious = suspicious + 1
						end
					end
				end
			end
		end
	elseif trigger_type == "noise" then -- aware/suspicious based on range, current awareness
		local actor, radius, soundName, attacker = ... -- actor can be unit or another object (grenade, mine, etc.)
		-- log noise sources (will reset on new turn)
		if GameState.RainLight or GameState.RainHeavy then
			radius = MulDivRound(radius, Max(0, 100 + const.EnvEffects.RainNoiseMod), 100)
		end
		dbg_awareness_log(actor, " alerts: noise ", radius)
		g_NoiseSources[#g_NoiseSources + 1] = {
			actor = actor,
			pos = actor and actor:GetPos(),
			noise = radius,
		}
		radius = radius * const.SlabSizeX
		local alerter = IsKindOf(actor, "Unit") and actor or nil
		if IsKindOf(attacker, "Unit") then
			alerter = attacker
		end
		local state = alerter and HasPerk(alerter, "FoxPerk") and "surprised" or "aware"
		for _, team in ipairs(g_Teams) do
			local side = team.side
			if side ~= "neutral" and (g_Combat or side == "enemy1" or side == "enemy2") then
				for _, unit in ipairs(team.units) do
					if unit ~= actor
						and IsCloser(unit, actor, radius + 1)
						and (not unit:HasStatusEffect("Distracted") or IsCloser(unit, actor, MulDivRound(radius, 66, 100) + 1))
					then
						local sector = gv_Sectors and gv_Sectors[gv_CurrentSectorId]
                        if sector then
                              sector.CombatHeat = (sector.CombatHeat or 0) + 1
                        end
						local reason = T{Presets.AwareReasons.Default.arNoise.display_name, enemy = unit.Name, noise = soundName}
						if unit:SetPendingAwareState(state, reason, alerter) then
							if actor then
								unit.last_known_enemy_pos = actor:GetPos()
							end
							if state == "aware" then
								if not alerted then alerted = {} end
								alerted[#alerted + 1] = unit
							else
								surprised = surprised + 1
							end
							dbg_awareness_log("  ", unit, " alerted")
						end
					end
				end
			end
		end
	elseif trigger_type == "projector" then
		local actor, units, projector = ...
		for i, unit in ipairs(units) do
			if IsCloser(unit, projector, ProjectorSuspiciousApplyRange) then
				local reason = T{Presets.AwareReasons.Default.arProjector.display_name, enemy = unit.Name}
				if unit:SetPendingAwareState("aware", reason, actor) then
					surprised = surprised + 1
				end
			end
		end
	elseif trigger_type == "sight" then -- sight: make unaware units suspicious
		local actor, seen = ... -- actor is unaware unit who saw an enemy. seen is enemy unit seen by actor
		local aware = actor:IsAware() or actor.pending_aware_state == "aware"
		local surprised = actor:HasStatusEffect("Surprised") or actor.pending_aware_state == "surprised"
		if actor:IsOnEnemySide(seen) and not aware and not surprised and actor:SetPendingAwareState("surprised") then
			suspicious = suspicious + 1
			dbg_awareness_log(actor, " is alerted (sight)")
		end
	elseif trigger_type == "thrown" then
		local obj, attacker = ...  --  obj is thrown object
		local units
		for _, team in ipairs(g_Teams) do
			if not team.neutral and (not attacker or attacker.team and team:IsEnemySide(attacker.team)) then
				for _, unit in ipairs(team.units) do
					if not unit:IsDead() and not unit:IsAware("pending") then
						local sight = unit:GetSightRadius(obj)
						if IsCloser(unit, obj, sight + 1) then
							if not units then units = {} end
							units[#units + 1] = unit
						end
					end
				end
			end
		end
		if units then
			local los_any, los_targets = CheckLOS(units, obj)
			if los_any then
				for i, los_value in ipairs(los_targets) do
					if los_value then
						local unit = units[i]
						local reason = T{Presets.AwareReasons.Default.arThrownObject.display_name, enemy = unit.Name}
						if unit:SetPendingAwareState("surprised", reason) then
							dbg_awareness_log("  ", unit, " is surprised")
							surprised = surprised + 1
						end
					end
				end
			end
		end
	elseif trigger_type == "script" then --should this be included in the aware_reason
		local _units, state = ...  -- units to become suspicious/aware
		local units = table.ifilter(_units, function(idx, unit)
			return unit.team and not unit.team.neutral
		end)
		for _, unit in ipairs(units) do	
			unit.pending_aware_state = state
			dbg_awareness_log(unit, " is alerted (script): ", state)
		end
		if state == "aware" then
			alerted = units
		end
	elseif trigger_type == "surprise" then
		local unit, from_suspicious = ...
		local reason
		if from_suspicious then
			reason = T{Presets.AwareReasons.Default.arDeadBody.display_name, enemy = unit.Name}
		end
		if unit:SetPendingAwareState("aware", reason) then
			dbg_awareness_log(unit, " is alerted (surprise)")
			if not alerted then alerted = {} end
			alerted[#alerted + 1] = unit
		end
	elseif trigger_type == "discovered" then -- Alert all enemies who have sight of unit.
		local unit = ...
		local enemyUnits = GetAllEnemyUnits(unit)
		local alertedPeople = 0
		for i, enemyUnit in ipairs(enemyUnits) do
			if not enemyUnit:IsAware() and HasVisibilityTo(enemyUnit, unit) then
				alertedPeople = alertedPeople + 1
				CombatStarDetectedtVR(unit)
				if enemyUnit.pending_aware_state ~= "aware" then
					if not enemyUnit:HasStatusEffect("Surprised") then -- unit has already spotted someone and is now surprised, dont try to make it aware again
						local reason = T{Presets.AwareReasons.Default.arNotice.display_name, enemy = enemyUnit.Name, merc = unit.Nick or unit.Name}
						if enemyUnit:SetPendingAwareState("aware", reason, unit) then
							if not alerted then alerted = {} end
							alerted[#alerted + 1] = enemyUnit
							dbg_awareness_log(enemyUnit, " is alerted (combat-walk)")
						end
					end
				end
			end
		end
		if alertedPeople > 0 then
			unit:RemoveStatusEffect("Hidden")
		end
	else
		assert(false, string.format("unknown alert trigger '%s' used", tostring(trigger_type)))
	end

	if alerted then
		alerted = table.ifilter(alerted, function(idx, unit)
			return not unit.dummy and unit.pending_aware_state == "aware"
		end)
	end
	local alerted_count = alerted and #alerted or 0

	if alerted_count > 0 then
		local roles = {}
		PropagateAwareness(alerted, roles)
		for _, unit in ipairs(alerted) do
			if unit.pending_aware_state ~= "aware" and unit:SetPendingAwareState("aware") or roles[unit] == "alerter" then
				unit.pending_awareness_role = roles[unit] or "alerted"
			end
		end
	end
	
	if alerted_count + surprised > 0 then
		local pendingType = alerted_count > 0 and "alert" or "sus"
		if not g_UnitAwarenessPending or pendingType == "alert" then
			g_UnitAwarenessPending = pendingType
		end
	end

	return alerted_count + surprised, suspicious
end


function AIUpdateScoutLocation(unit)
	if not unit.last_known_enemy_pos then
		return
	end

	-- Используем константный sight радиус, как ты решил
	local sight = MulDivRound(const.Combat.AwareSightRange, 50, 100)

	-- Если цель всё ещё на виду — меняем на шум или сбрасываем
	if CheckLOS(unit.last_known_enemy_pos, unit, sight) then
		if g_NoiseSources and #g_NoiseSources > 0 then
			local valid_noises = {}

			-- Фильтруем шумы, которые исходят от врагов
			for i = 1, #g_NoiseSources do
				local src = g_NoiseSources[i]
				if src.Actor and src.Actor:IsOnEnemySide(unit) then
					valid_noises[#valid_noises + 1] = i
				end
			end

			if #valid_noises > 0 then
				local index = valid_noises[InteractionRand(#valid_noises, "AlarmNoise") + 1]
				local noise = g_NoiseSources[index]

				-- Назначаем новую позицию и удаляем шум
				unit.last_known_enemy_pos = noise.pos
				table.remove(g_NoiseSources, index)
			else
				-- Все шумы от союзников — сбрасываем
				unit.last_known_enemy_pos = nil
			end
		else
			unit.last_known_enemy_pos = nil
		end
	end
end