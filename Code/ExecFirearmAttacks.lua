function Unit:ExecFirearmAttacks(action, cost_ap, attack_args, results)
	NetUpdateHash("ExecFirearmAttacks", action, cost_ap, not not g_Combat)
	local lof_idx = table.find(attack_args.lof, "target_spot_group", attack_args.target_spot_group or "Torso")
	local lof_data = attack_args.lof[lof_idx or 1]
	local target = attack_args.target
	local target_unit = IsKindOf(target, "Unit") and IsValidTarget(target) and target
	local interrupt = attack_args.interrupt
	if interrupt then
		if ActionCameraPlaying then
			RemoveActionCamera(true)
			WaitMsg("ActionCameraRemoved", 1000)
		end
		self:PushDestructor(function()
			Msg("InterruptAttackEnd") 
		end)

		Msg("InterruptAttackStart", self, target_unit, action) 
	end
	
	NetUpdateHash("ExecFirearmAttacks_After_Interrupt_Cam_Wait")
	
	results.attack_from_stealth = not not self:HasStatusEffect("Hidden")
	for _, attack in ipairs(results.attacks or {results}) do
		if attack.fired then
			self:AttackReveal(action, attack_args, results)
			break
		end
	end

	local can_provoke_opportunity_attacks = not action or (action.id ~= "CancelShot" and action.id ~= "CancelShotCone")
	if can_provoke_opportunity_attacks then
		self:ProvokeOpportunityAttacks(action, "attack interrupt")
	end
	self:PrepareToAttack(attack_args, results)
	if can_provoke_opportunity_attacks then
		self:ProvokeOpportunityAttacks(action, "attack interrupt")
	end
	local was_interruptable = self.interruptable
	if not was_interruptable then
		self:EndInterruptableMovement()
	end

	NetUpdateHash("ExecFirearmAttacks_Start_Action_Cam")
	-- camera effects
	if attack_args.opportunity_attack_type ~= "Retaliation" then
		local cinematicKill = false
		local dontPlayForLocalPlayer = false
		if g_Combat and IsEnemyKill(self, results) then
			g_Combat:CheckPendingEnd(results.killed_units)
			
			local isKillCinematic 
			isKillCinematic, dontPlayForLocalPlayer = IsEnemyKillCinematic(self, results, attack_args)
			if isKillCinematic then
				cameraTac.SetForceMaxZoom(false)
				SetAutoRemoveActionCamera(self, results.killed_units[1], nil, nil, nil, nil, nil, dontPlayForLocalPlayer)
				cinematicKill = true
			end
		elseif interrupt then -- the attack is from enemy pindown or overwatch
			--[[if self.team.side == "enemy" then
				SetAutoRemoveActionCamera(target_unit, self, 1000, true) -- todo: should this use the anim duration?
			else
				SetAutoRemoveActionCamera(self, target_unit, 1000, true)
			end--]]
		end
		if not cinematicKill and IsKindOf(target, "Unit") then
			local cinematicAttack, interpolation = IsCinematicAttack(self, results, attack_args, action)
			if cinematicAttack then
				local playerUnit = (IsKindOf(target, "Unit") and target:IsLocalPlayerTeam() and target) or (self:IsLocalPlayerTeam() and self)
				local enemyUnit = playerUnit and (playerUnit == target and self or target)
				if playerUnit and enemyUnit then
					SetAutoRemoveActionCamera(playerUnit, enemyUnit, false, false, false, interpolation and default_interpolation_time, nil, dontPlayForLocalPlayer)
				end
			end
		end
	end
	NetUpdateHash("ExecFirearmAttacks_After_Action_Cam")
	-- animspeed modifier & cmd destructor
	local asm = self:GetAnimSpeedModifier()
	local anim_speed_mod = attack_args.anim_speed_mod or 1000
	self:SetAnimSpeedModifier(anim_speed_mod)
	self:PushDestructor(function(self)
		self:SetAnimSpeedModifier(asm)
		if IsValid(target) and target:HasMember("session_id") then
			self.last_attack_session_id = target.session_id
		else
			self.last_attack_session_id = false
		end
		

		if IsValid(target) then
			ObjModified(target)
		end
		
		table.remove(g_CurrentAttackActions) -- pop the pushed attack action
	end)
	
	local ap = (cost_ap and cost_ap > 0) and cost_ap or action:GetAPCost(self, attack_args)
	table.insert(g_CurrentAttackActions, { action = action, cost_ap = ap, attack_args = attack_args, results = results })

	-- start anim, wait hit moment, apply ammo/condition results
	local 	chance_to_hit =  results.chance_to_hit
	local 	missed        =  results.miss
	local critical = results.crit
	local chance_crit = results.crit_chance
	local aim_state = self:GetStateText()
	
	local fired = false	
	if results.attacks then --- multi-weapon attacks (DualShot)
		local shots = results.attacks[1] and results.attacks[1].shots
		self:StartFireAnim(shots and shots[1], attack_args)
		for _, attack in ipairs(results.attacks) do
			attack.weapon:ApplyAmmoUse(self, attack.fired, attack.jammed, attack.condition)
			fired = fired or attack.fired
		end
	else
		self:StartFireAnim(results.shots and results.shots[1], attack_args)
		results.weapon:ApplyAmmoUse(self, results.fired, results.jammed, results.condition)
		fired = results.fired
	end
	
	if not fired then
		-- none of the weapons fired, abort
		if not was_interruptable then
			self:BeginInterruptableMovement()
		end
		Sleep(self:TimeToAnimEnd())
		self:PopAndCallDestructor()
		if interrupt then
			self:PopAndCallDestructor()
		end
		NetUpdateHash("ExecFirearmAttacks_early_out")
		return
	end


	local shot_threads = {}	
	
	local attacks = results.attacks or {results}
	local attackArgs = results.attacks_args or {attack_args}
	
	if results.shots and #results.shots > 5 and g_Combat and not g_Combat:ShouldEndCombat(results.killed_units) then
		if (not results.killed_units or #results.killed_units == 1) then
			local vr = IsMerc(self) and "Autofire" or "AIAutofire"
			PlayVoiceResponse(self, vr)
		end
	end
	
	local lowChanceShot
	local base_weapon_damage = 0
	for attackIdx, attack in ipairs(attacks) do
		local attackArg = attackArgs[attackIdx]
		local fx_action = attackArg.fx_action
		if action.id == "BulletHell" then
			BulletHellOverwriteShots(attack)
		end
		local shots_per_animation = results.weapon.AutoShots / 2
		if action.id == "BurstFire" or action.id == "MGBurstFire" then
			shots_per_animation = results.weapon.AutoShots / 2
		end
        if action.id == "Buckshot" or action.id == "DoubleBarrel" then
			shots_per_animation = 500
		end
        if action.id == "BuckshotBurst" then
			shots_per_animation = 1500
		end
		if action.id == "AbakanBurst"  then
			shots_per_animation = 10
		end

        
		for i, shot in ipairs(attack.shots) do

			PushUnitAlert("noise", self, results.weapon.Noise, Presets.NoiseTypes.Default.Gunshot.display_name)


			if action.id == "AbakanAutoFire" and i < 2 then shots_per_animation = 10 end
			if action.id == "AbakanAutoFire" and i >= 2 then	shots_per_animation = results.weapon.AutoShots / 2 end

			-- shot visuals
			attack.weapon:FireBullet(self, shot, shot_threads, results, attackArg)
			if attackArg.single_fx then
				fx_action = ""
			end
			if i < #attack.shots then -- more shots to fire
				if i % shots_per_animation == 0 then
					local shotAnimDelay = attackArg.attack_anim_delay or self:TimeToAnimEnd()
					self:StartFireAnim(attack.shots[i+1], attackArg, nil, shotAnimDelay) -- fire next shot
				else
					Sleep(self:GetAnimDuration() / shots_per_animation)
				end
			elseif attackIdx < #attacks then
				Sleep(MulDivRound(self:GetAnimDuration() / shots_per_animation, 30, 100))
			end
			if IsMerc(self) and attack.target_hit then
				if attack.chance_to_hit <= 20 then
					lowChanceShot = true
				end
			end
		end
		attack.weapon:FireSpread(attack, attackArg) -- deal the area damage, if any
		base_weapon_damage = base_weapon_damage + attack.weapon.Damage
	end

	-- additional damage (e.g. from DualShot perk)
	for _, packet in ipairs(results.extra_packets) do	
		if IsValidTarget(packet.target) then
			if packet.damage then
				packet.target:TakeDirectDamage(packet.damage, false, "short", packet.message)
			end
			if packet.effects then
				packet.target:ApplyDamageAndEffects(false, false, packet)
			end
		end
	end

	-- wait end moment and restore animation
	local time_to_fire_end = self:TimeToAnimEnd()
	if not attack_args.dont_restore_aim then
		if self:CanAimIK(results.weapon) then
			local restore_aim_delay = Min(300, time_to_fire_end)
			Sleep(restore_aim_delay)
			self:SetIK("AimIK", lof_data.lof_pos2, nil, nil, 0)
			Sleep(time_to_fire_end - restore_aim_delay)
			self:SetState(aim_state, const.eKeepComponentTargets)
		else
			Sleep(time_to_fire_end)
			self:SetState(aim_state, const.eKeepComponentTargets)
		end
	end

	-- special-case: interrupt neutral units with neutral_retaliate flag attacked by player units,
	-- so they don't look ridiculous minding their own business for several more seconds until the attack resolves
	if self.team.player_team and not g_Combat then
		if IsValid(target_unit) and target_unit.team.neutral and target_unit.neutral_retaliate and not target_unit:IsIncapacitated() then
			target_unit.neutral_retal_attacked = true
			target_unit:SetBehavior()
			target_unit:SetCommand("Idle")
		end
		
		local hits = #results > 0 and results or results.area_hits
		for _, hit in ipairs(hits) do
			local unit = IsKindOf(hit.obj, "Unit") and not hit.obj:IsIncapacitated() and hit.obj
			if IsValid(unit) and unit.team.neutral and unit.neutral_retaliate then
				unit.neutral_retal_attacked = true
				unit:SetBehavior()
				unit:SetCommand("Idle")
			end
		end
	end
	
	self.interruptable = false
	self:PushDestructor(function()
		self.interruptable = was_interruptable
	end)
	
	if attack_args.external_wait_shots then
		table.iappend(attack_args.external_wait_shots, shot_threads)
	else
		Firearm:WaitFiredShots(shot_threads)
	end

	-- wait target dodge anim
	while target_unit and target_unit.command == "Dodge" do
		WaitMsg("Idle")
	end
	-- play voices
	base_weapon_damage = MulDivRound(base_weapon_damage, 120, 100)
	if attacks and next(attacks)then
		--count shots fired per team for Voice Response
		self.team.tactical_situations_vr.shotsFired = self.team.tactical_situations_vr.shotsFired and self.team.tactical_situations_vr.shotsFired + 1 or 1
		self.team.tactical_situations_vr.shotsFiredBy = self.team.tactical_situations_vr.shotsFiredBy  or {}
		self.team.tactical_situations_vr.shotsFiredBy[self.session_id] = true
		PlayVoiceResponseTacticalSituation(table.find(g_Teams, self.team), "now")
		if missed then
		
			--count missed shots per team for Voice Response
			self.team.tactical_situations_vr.missedShots = self.team.tactical_situations_vr.missedShots and self.team.tactical_situations_vr.missedShots + 1 or 1
			PlayVoiceResponseTacticalSituation(table.find(g_Teams, self.team), "now")


			
			if chance_to_hit >= 70 then
				if not target_unit or not target_unit:IsCivilian() then
					PlayVoiceResponseMissHighChance(self)
				end
			elseif target_unit and chance_to_hit>=50 and base_weapon_damage>=target_unit:GetTotalHitPoints() then
				if IsMerc(target_unit) then
					target_unit:SetEffectValue("missed_by_kill_shot", true)
				end
			end
		elseif not missed then
			if results.stealth_kill and IsMerc(self) and results.killed_units and #results.killed_units > 0 then	
				
			elseif lowChanceShot and target_unit and not self:IsOnAllySide(target_unit) and not target_unit:IsCivilian() then
				PlayVoiceResponse(self, "LowChanceShot")
			end
		end
	end
	
	for i, attack in ipairs(attacks) do
		if target_unit and chance_to_hit > 0 then
			for _,effect in pairs(attack.weapon.ammo.AppliedEffects) do
			
				if effect == 'Exposed' 
				then
					target_unit:AddStatusEffect(effect)
				end
			end
				
			end
		
		local holdXpLog = i ~= #attacks
		self:OnAttack(action, target_unit, attack, attack_args, holdXpLog)
	end
		
	LogAttack(action, attack_args, results)
	AttackReaction(action, attack_args, results, "can retaliate")
	
	if not action or (action.id ~= "CancelShot" and action.id ~= "CancelShotCone") then
		self:ProvokeOpportunityAttacks(action, "attack reaction")
	end

	if not was_interruptable then
		self:BeginInterruptableMovement()
	end
	self:PopAndCallDestructor()
	self:PopAndCallDestructor()
	if interrupt then
		self:PopAndCallDestructor()
	end
end


function Unit:PrepareAttackArgs(action_id, args)
	action_id = action_id or self:GetDefaultAttackAction("ranged")
	args = args or empty_table
	local action = CombatActions[action_id]
	local weapon = args.weapon or action and action:GetAttackWeapons(self)
	local target = args.target
	local prediction = args.prediction or args.prediction == nil
	local aim_type = action and action.AimType
	local thermal_aim = IsKindOf(weapon, "Firearm") and IsFullyAimedAttack(args) and weapon:HasComponent("IgnoreGrazingHitsWhenFullyAimed")

	local attack_args = table.copy(args)
	attack_args.action_id = action_id
	attack_args.obj = self
	attack_args.weapon = weapon
	attack_args.target_pos = attack_args.target_pos or IsPoint(target) and target
	attack_args.step_pos = attack_args.step_pos or self.return_pos or self:GetOccupiedPos() or GetPassSlab(self) or self:GetPos()
	attack_args.ignore_smoke = thermal_aim
	if attack_args.fire_relative_point_attack == nil then
		attack_args.fire_relative_point_attack = self.WeaponType == "Shotgun"
	end
	attack_args.prediction = prediction

	if aim_type ~= "melee" then
		attack_args.prediction = true
		local attack_data
		if IsPoint(target) and attack_args.target_height_range then
			if not target:IsValidZ() then
				target = target:SetTerrainZ()
			end
			local min_dist
			for h = 0, attack_args.target_height_range, guim/2 do
				local pt = target:SetZ(target:z() + h)
				local data = GetLoFData(self, pt, attack_args)
				if data then
					local dist
					for _, lof_data in ipairs(data.lof) do
						for _, hit in ipairs(lof_data.hits) do
							local d = target:Dist(hit.pos)
							if not dist or dist > d then
								dist = d
							end
						end
					end
					if dist and (not attack_data or min_dist > dist) then
						attack_data, min_dist = data, dist
					end
				end
			end
		else
			attack_data = GetLoFData(self, target, attack_args)
		end
		if attack_data then
			for k, v in pairs(attack_data) do
				attack_args[k] = v
			end
		else
			attack_args.stuck = true
		end
		attack_args.prediction = prediction
	end

	attack_args.num_shots = attack_args.num_shots or 1 -- number of direct shots (with simulated projectiles
	attack_args.aoe_action_id = attack_args.aoe_action_id or false -- defines cone area for collateral/aoe damage (as used in Firearm:GetAreaAttackParams)
	attack_args.aoe_fx_action = attack_args.aoe_fx_action or false -- fx action to play for the aoe part of the attack, if any
	attack_args.aoe_damage_type = attack_args.aoe_damage_type or "default" -- "default", "fixed" or "percent", defines how the aoe damage is calculated
	attack_args.aoe_damage_value = attack_args.aoe_damage_value or false -- when "fixed" or "percent" type is used
	attack_args.applied_status = attack_args.applied_status or false -- status effect on hit
	attack_args.damage_bonus = attack_args.damage_bonus or false -- bonus damage applied by the attack (0/false = no change, 100 = x2, -100 = x0)
	attack_args.consumed_ammo = attack_args.consumed_ammo or false -- defaults to num_shots/used_ammo (from aoe params)
	attack_args.aoe_damage_bonus = attack_args.aoe_damage_bonus or false -- same as above for collateral/aoe damage
	attack_args.cth_loss_per_shot = attack_args.cth_loss_per_shot or false -- for attacks with num_shots > 1, defines the accuracy of the follow-up shots based on the attack roll
	attack_args.fx_action = attack_args.fx_action or false -- fx action to play in the hit moment(s) of the attack anim (defaults to WeaponFire)
	attack_args.single_fx = attack_args.single_fx or false -- if set to true, attacks will not play their fx_action more than once per attack

	if weapon and aim_type == "cone" then
		local aoe_params = weapon:GetAreaAttackParams(action_id, self, attack_args.target_pos, attack_args.step_pos)
		for k, v in pairs(aoe_params) do
			attack_args[k] = v
		end
	end

	-- Stealth kill
	local is_stealth = attack_args.stealth_attack or self:HasStatusEffect("Hidden")
	local lethal_weapon = (attack_args.target_spot_group == "Neck") and IsKindOf(weapon, "MeleeWeapon") and (weapon.NeckAttackType == "lethal")
	if action and (is_stealth or lethal_weapon)  then
		local stealth_targeted = is_stealth and action.StealthAttack and IsKindOf(target, "Unit") and IsValidTarget(target)
		local stealth_aoe, chance
		if stealth_targeted or stealth_aoe then
			local crosshair = GetInGameInterfaceModeDlg().crosshair
			local aim = args.aim or (crosshair and crosshair.aim) or 0
			chance = self:CalcStealthKillChance(weapon, target, attack_args.target_spot_group, aim)
			attack_args.stealth_attack = true
		end
		if lethal_weapon then
			local lethal_chance = 5 + Max(0, (self.Strength - target.Health) / 2)
			chance = Max(chance or 0, lethal_chance)
		end
		if stealth_targeted or lethal_weapon then
			if target:IsNPC() and not target.villain then
				attack_args.stealth_kill_chance = chance
				attack_args.stealth_bonus_crit_chance = 0
			else
				attack_args.stealth_kill_chance = 0
				attack_args.stealth_bonus_crit_chance = chance
			end
		end
	end

	return attack_args
end

function Unit:ShotgunBurst(action_id, cost_ap, args)
	local target = args.target
--	if not IsKindOf(target, "Unit") then return end
	
	local action = CombatActions["Buckshot"]
	local weapon = self:GetActiveWeapons()
    
		
	for i = 1,2,3 do
		if not self:CanUseWeapon(weapon, 1) then break end
        args.attack_anim_delay = 5000
        WaitMsg("Idle", 500)
		self:FirearmAttack(action_id, 0, args)
	end
	
	return
end