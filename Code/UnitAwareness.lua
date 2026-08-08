

MapVar("JazzRaisedAlarm", false)

function OnMsg.ConflictEnd(sector, _, playerAttacked, playerWon, autoResolve, isRetreat, startedFromMap)
  -- Проверяем, есть ли сектор
  JazzRaisedAlarm = false
  if not sector then return end

  -- 1) Если игрок выиграл
  local base_heat = 20 + (MulDivRound(sector.CombatHeat, 10, 100) or 0)  -- базовое значение, можешь сделать динамическим
  sector.CombatHeat = 0
  if playerWon then
	-- Поднять heat в секторе
   
	sector.Heat = sector.Heat + base_heat

	-- Поднять heat в регионе
	local region = GetRegionForSector(sector.Id)
	if region then
	  local regional_heat = MulDivRound(base_heat, 10, 100) -- 10% от heat сектора
	  region:IncreaseHeat(regional_heat)
	end

	-- Поднять heat в соседних секторах
	ForEachSectorAround(sector.Id, 1, function(neighbor_id)
	  if neighbor_id ~= sector.Id then
		local neighbor = gv_Sectors[neighbor_id]
		if neighbor then
		  local neighbor_heat = MulDivRound(base_heat, 40, 100) -- например, 25% от heat сектора
		  neighbor.Heat = neighbor.Heat + neighbor_heat
		end
	  end
	end)
	ForEachSectorAround(sector.Id, 2, function(neighbor_id)
	  if neighbor_id ~= sector.Id then
		local neighbor = gv_Sectors[neighbor_id]
		if neighbor then
		  local neighbor_heat = MulDivRound(base_heat, 10, 100) -- например, 25% от heat сектора
		  neighbor.Heat = neighbor.Heat + neighbor_heat
		end
	  end
	end)
  end

  -- 2) При поражении или отступлении тоже можно сделать свою логику heat
  if not playerWon or isRetreat then
	-- Например, сильно поднимать heat за проигрыш
	local penalty_heat = base_heat
	sector.Heat = sector.Heat + penalty_heat

	local region = GetRegionForSector(sector.Id)
	if region then
	  local regional_heat = MulDivRound(penalty_heat, 20, 100)
	  region:IncreaseHeat(regional_heat)
	end
  end
end




function OnMsg.TurnStart()

  local sector = gv_Sectors and gv_Sectors[gv_CurrentSectorId]
  if not sector then return end

  local totalheat = (sector.Heat or 0) + (sector.CombatHeat or 0)
  if totalheat > 500 then

	local valid_noises = {}
	local units = GetCurrentMapUnits("enemy")
	for _, unit in ipairs(units) do
	TriggerUnitAlert("script", unit, "suspicious")
	if g_NoiseSources and #g_NoiseSources > 0 and not unit.last_known_enemy_pos then

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
	end
  end
  end
   -- JazzRaisedAlarm = true
  end

end


function OnMsg.ExplorationTick()
  if JazzRaisedAlarm then return end
  local sector = gv_Sectors and gv_Sectors[gv_CurrentSectorId]
  if not sector then return end

  local totalheat = (sector.Heat or 0) + (sector.CombatHeat or 0)
  if totalheat > 500 then

	local valid_noises = {}
	local units = GetCurrentMapUnits("enemy")
	for _, unit in ipairs(units) do
	  TriggerUnitAlert("script", unit, "suspicious")
	  if g_NoiseSources and #g_NoiseSources > 0 and not unit.last_known_enemy_pos then

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
	  end
	end
	end
	JazzRaisedAlarm = true
  end

end

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

	local sight = MulDivRound(const.Combat.AwareSightRange, 50, 100)

	if CheckLOS(unit.last_known_enemy_pos, unit, sight) then
		if g_NoiseSources and #g_NoiseSources > 0 then
			local valid_noises = {}

			for i = 1, #g_NoiseSources do
				local src = g_NoiseSources[i]
				if src.Actor and src.Actor:IsOnEnemySide(unit) then
					valid_noises[#valid_noises + 1] = i
				end
			end

			if #valid_noises > 0 then
				local index = valid_noises[InteractionRand(#valid_noises, "AlarmNoise") + 1]
				local noise = g_NoiseSources[index]

				unit.last_known_enemy_pos = noise.pos
				table.remove(g_NoiseSources, index)
			else
				unit.last_known_enemy_pos = nil
			end
		else
			unit.last_known_enemy_pos = nil
		end
	end
end


local lSuspicionTickRate = 100 -- How often to add the tick amount
local lSuspicionTickAmount = 10 -- The amount to add when hidden
local lSuspicionTickAmountProjector = 6 -- The amount to add when hidden
local ProjectorSuspiciousApplyRange = 10 * const.SlabSizeX -- Enemies within this distance of the projector will be alerted
local lSuspicionTickAmountProne = 5 -- The amount to add when hidden and in prone
local lSuspicionTickDownAmount = 2 -- The amount to remove when no unit is in range
local lSuspicionTickMinDist = const.SlabSizeX * 2 -- If this close to an enemy then frontness doesn't matter (unless hidden or in the dark)
-- Exploration only: suspicion range when the ally is in the observer's rear hemisphere (JAZZ-AI-004).
local lSuspicionRearSightCap = const.SlabSizeX * 10
local lCubicInIndex = GetEasingIndex("Cubic in")

function UpdateSuspicion(alliedUnits, enemyUnits, intermediate_update)
	if GameTime() - lastSusUpdate < lSuspicionTickRate then return end
	-- Dynamic thresholds (must not bake JazzRaisedAlarm / Night at load time).
	local SuspicionThreshold = JazzRaisedAlarm and 80 or 160
	local lSuspicionTickAmountNotHidden = GameState.Night and 32 or 16
	local lSuspicionTickDistanceModOuter = JazzRaisedAlarm and (const.SlabSizeX / 2) or (const.SlabSizeX * 4)

	local sneakLights
	if intermediate_update then
		sneakLights = GetSneakProjectorLights()
	end

	local sector = gv_Sectors[gv_CurrentSectorId]
	local anySusUpdated = false
	local susIncreasedBy = {}
	-- Hoist once per tick (CLib FixAI pattern): cheap distance gate before GetSightRadius.
	local max_sight_radius = MulDivRound(GetMaxSightRadius(), 1200, 1000)
	local HasVisibilityTo = HasVisibilityTo
	local IsCloser = IsCloser
	for i, ally in ipairs(alliedUnits) do
		ally.suspicion = ally.suspicion or 0
		
		-- Performing an attack or something
		if not ally:IsIdleCommand() and not ally:IsInterruptable() then
			goto continue
		end
		if not IsValid(ally) or ally:IsDead() then goto continue end
		
		local allyDetectionModifier = 100
		if HasPerk(ally, "Untraceable") then
			allyDetectionModifier = allyDetectionModifier - Untraceable:ResolveValue("enemy_detection_reduction")
		end
		-- JAZZ-UNITS-006 Batch5: Carlos detection builds 33% slower.
		if HasPerk(ally, "Jazz_Perk_Carlos") then
			allyDetectionModifier = allyDetectionModifier - 33
		end
		if ally:HasStatusEffect("Darkness") then
			allyDetectionModifier = allyDetectionModifier + const.EnvEffects.DarknessDetectionRate
		end
		allyDetectionModifier = Max(0, allyDetectionModifier)

		local raiseSusLargest = 0
		local raiseSusEnemy = false
		for i, enemy in ipairs(enemyUnits) do
			if enemy.retreating then goto continue end
			if enemy.command == "ExitCombat" then goto continue end
			if enemy:IsDead() then goto continue end
			if not IsCloser(enemy, ally, max_sight_radius) then
				goto continue
			end
			local seesAlly = HasVisibilityTo(enemy, ally)
			-- try to skip GetSightRadius calculations
			if not seesAlly then
				if raiseSusEnemy or not HasVisibilityTo(ally, enemy) then
					goto continue
				end
			end
			local sightRad, hidden, darkness = enemy:GetSightRadius(ally)
			local angle_to_object = AngleDiff(CalcOrientation(enemy, ally), enemy:GetOrientationAngle())
			-- Realtime: rear hemisphere detection bubble capped at 10 tiles (combat unchanged).
			if not g_Combat and abs(angle_to_object) >= 90 * 60 then
				sightRad = Min(sightRad, lSuspicionRearSightCap)
			end
			local dist = enemy:GetDist(ally)
			local inRad = dist <= sightRad
			if inRad then
				if seesAlly then
					-- If in front of any enemy, add a bonus detection %
					-- If in the behind plane then have a smaller cut off.
					if abs(angle_to_object) < 90*60 then
						local radiusLess = MulDivRound(sightRad, 80, 100)
						if dist > radiusLess then
							goto continue
						end
					end
					
					-- The larger this is, the closer the ally is to the enemy
					local distFromSightRad = sightRad - dist 
					
					-- Decrease sus the further away you are
					local distanceModifier = false
					if distFromSightRad < lSuspicionTickDistanceModOuter then
						distanceModifier = Lerp(10, 100, distFromSightRad, sightRad)
					else
						distanceModifier = 100
					end
					
					-- Modify the value based on how in front you are
					local frontnessModifier = false
					local maxDot = (4096 * 4096) * 2
					local dot = cos(angle_to_object) * 4096
					dot = EaseCoeff(lCubicInIndex, dot + 4096 * 4096, maxDot)
					frontnessModifier = Lerp(hidden and 30 or 40, 100, dot, maxDot)
					
					local closeInTheLight = false
					if hidden and not darkness and dist < lSuspicionTickMinDist and frontnessModifier > 60 then
						closeInTheLight = true
					end
					
					-- Get the base value based on a variety of factors
					local value = 0
					if hidden and not closeInTheLight then
						if ally.stance == "Prone" then
							value = lSuspicionTickAmountProne
						else
							value = lSuspicionTickAmount
						end
					else
						value = lSuspicionTickAmountNotHidden
					end
					
					value = MulDivRound(value, distanceModifier, 100)
					value = MulDivRound(value, frontnessModifier, 100)
					
					if value > raiseSusLargest then
						raiseSusEnemy = enemy
						raiseSusLargest = value
					end
				end
			elseif not raiseSusEnemy and HasVisibilityTo(ally, enemy) then
				local extraRad = MulDivRound(sightRad, 1200, 1000)
				if dist <= extraRad then
					raiseSusEnemy = enemy
				end
			end

			::continue::
		end
		
		if sneakLights and IsMerc(ally) then
			local lightIndex = IsVoxelIlluminatedByObjects(ally:GetPos(), sneakLights)
			local val = lightIndex ~= 0 and lSuspicionTickAmountProjector or 0
			if val > raiseSusLargest then
				raiseSusLargest = val
				
				local light = sneakLights[lightIndex]
				local originalLight = light and light.original_light
				local projector = originalLight and originalLight:GetParent()
				if projector then
					raiseSusEnemy = projector
				end
				
				if ally.suspicion + raiseSusLargest >= SuspicionThreshold and ally:HasStatusEffect("Hidden") then
					ally:RemoveStatusEffect("Hidden")
					-- In this specific case we want this status effect to have a removal message.
					-- Copied from AddStatusEffect's floating text.
					CreateMapRealTimeThread(function()
						WaitPlayerControl()
						CreateFloatingText(ally, T{488962074575, "- <DisplayName>", Hidden}, nil, nil, true)
					end)

					PushUnitAlert("projector", ally, enemyUnits, projector)
				end
			end
		end
		
		-- Apply detection modifiers (Untraceable / Carlos / Darkness) that were previously computed but unused.
		if raiseSusLargest > 0 and allyDetectionModifier ~= 100 then
			raiseSusLargest = Max(0, MulDivRound(raiseSusLargest, allyDetectionModifier, 100))
		end

		local oldSus = ally.suspicion
		if raiseSusLargest > 0 then
			ally.suspicion = ally.suspicion + raiseSusLargest
			susIncreasedBy[#susIncreasedBy + 1] = { unit = raiseSusEnemy, amount = raiseSusLargest, sees = ally }
		else
			ally.suspicion = ally.suspicion - lSuspicionTickDownAmount
			if raiseSusEnemy then
				susIncreasedBy[#susIncreasedBy + 1] = { unit = raiseSusEnemy, amount = -1, sees = ally }
			end
		end
		ally.suspicion = Clamp(ally.suspicion, 0, SuspicionThreshold)
		
		if ally.suspicion ~= oldSus and ally.ui_badge then
			local wasZeroNowIsnt = oldSus == 0 and ally.suspicion > 0
			local wasntZeroNowIs = oldSus > 0 and ally.suspicion == 0
			if wasZeroNowIsnt or wasntZeroNowIs then
				ally.ui_badge:UpdateActive()
				anySusUpdated = true
			end
		end
		
		if ally.suspicion >= SuspicionThreshold then
			if sector.warningStateEnabled and not sector.warningReceived then
				EnterWarningState(enemyUnits, alliedUnits, ally)
				anySusUpdated = true
				break
			else
				TriggerUnitAlert("discovered", ally)
				return
			end
		end
		
		::continue::
	end
	
	if anySusUpdated then
		local igi = GetInGameInterfaceModeDlg()
		if igi.crosshair then
			igi.crosshair:UpdateBadgeHiding()
		end
	end
	
	if not intermediate_update then
		lastSusUpdate = GameTime()
	end
	
	return susIncreasedBy
end