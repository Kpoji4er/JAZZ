-- JAZZ-COMBAT-003: stash for LightningReactionCheck during OnFirearmAttackStart
if FirstLoad then
	MapVar("g_JAZZ_FirearmAttacker", false)
	MapVar("g_JAZZ_FirearmAttackArgs", false)
end

--- Rollover-compatible mobile damage for AimType=mobile actions.
--- Vanilla/JAZZ used `return base, base/volleys` → UI shows `volleys × (base/volleys)` (e.g. 3×7),
--- which understates each volley (burst/auto). Match BurstFire convention: total, per_bullet.
--- @param attack_id string|nil fixed attack id (e.g. "JAZZ_SmgStorm"); nil → BurstFire if possible else SingleShot
function Jazz_GetMobileActionDamage(action, unit, args, attack_id)
	local weapon = action:GetAttackWeapons(unit, args)
	if not weapon then
		return 0
	end
	local base = unit:GetBaseDamage(weapon)
	local volleys = Max(1, action:ResolveValue("mobile_num_shots") or 1)
	if not attack_id then
		if IsKindOf(weapon, "Firearm") and weapon:CanBurstfire() then
			attack_id = "BurstFire"
		else
			attack_id = "SingleShot"
		end
	end
	local bullets_per = 1
	if attack_id ~= "SingleShot" then
		bullets_per = weapon:GetAutofireShots(attack_id)
		if not bullets_per or bullets_per < 1 then
			local ca = CombatActions[attack_id]
			bullets_per = (ca and ca:ResolveValue("num_shots")) or 1
		end
		bullets_per = Max(1, bullets_per)
	end
	local total_bullets = volleys * bullets_per
	local total = base * total_bullets
	return total, base, total - base
end

-- Vanilla OnAttack: signature kills (and shots with Signature origin_action_id, e.g. HundredKnives→KnifeThrow)
-- skip UpdateSignatureRecharges entirely. JAZZ WeaponAttacks with recharge_on_kill (ControllableBurst,
-- RnG, Zipper, …) therefore stayed on CD after Blood knives / other signature kills.
-- Fix: on signature kill, still clear other recharge_on_kill abilities; re-apply CD only for the killer.
g_JAZZ_SigRechargeKillWrapped = rawget(_G, "g_JAZZ_SigRechargeKillWrapped") or false
g_JAZZ_SigRechargeKillOnAttackBase = rawget(_G, "g_JAZZ_SigRechargeKillOnAttackBase") or false

local function Jazz_SignatureKillExcludeId(action, attack_args)
	local origin = attack_args and attack_args.origin_action_id and CombatActions[attack_args.origin_action_id]
	if origin and origin.group == "SignatureAbilities" then
		return origin.id
	end
	if type(action) == "string" then
		action = CombatActions[action]
	end
	if action and action.group == "SignatureAbilities" then
		return action.id
	end
end

local function lInstallSigRechargeKillFix()
	if rawget(_G, "g_JAZZ_SigRechargeKillWrapped") then
		return
	end
	if not Unit or type(Unit.OnAttack) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_SigRechargeKillOnAttackBase", Unit.OnAttack)
	rawset(_G, "g_JAZZ_SigRechargeKillWrapped", true)

	function Unit:OnAttack(action, target, results, attack_args, ...)
		local ret = g_JAZZ_SigRechargeKillOnAttackBase(self, action, target, results, attack_args, ...)
		local kill = results and #(results.killed_units or empty_table) > 0
		if not kill then
			return ret
		end
		local exclude_id = Jazz_SignatureKillExcludeId(action, attack_args)
		if not exclude_id then
			return ret
		end
		if string.match(exclude_id, "DoubleToss") then
			exclude_id = "DoubleToss"
		end
		local keep = self:GetSignatureRecharge(exclude_id)
		self:UpdateSignatureRecharges("kill")
		if keep and keep.on_kill then
			local remain = Max(1, (keep.expire_campaign_time or Game.CampaignTime) - Game.CampaignTime)
			self:AddSignatureRechargeTime(exclude_id, remain, true)
		end
		return ret
	end
end

function OnMsg.ModsReloaded()
	lInstallSigRechargeKillFix()
	if type(rawget(_G, "Jazz_InstallPierreRecruitCombatAction")) == "function" then
		Jazz_InstallPierreRecruitCombatAction()
	end
	if type(rawget(_G, "Jazz_EnsureRecklessAssaultRechargeOnKill")) == "function" then
		Jazz_EnsureRecklessAssaultRechargeOnKill()
	end
	if type(rawget(_G, "Jazz_EnsureNazdarovyaRechargeOnKill")) == "function" then
		Jazz_EnsureNazdarovyaRechargeOnKill()
	end
	if type(rawget(_G, "Jazz_EnsureTheGrimRechargeOnKill")) == "function" then
		Jazz_EnsureTheGrimRechargeOnKill()
	end
end

function OnMsg.DataLoaded()
	lInstallSigRechargeKillFix()
	if type(rawget(_G, "Jazz_InstallPierreRecruitCombatAction")) == "function" then
		Jazz_InstallPierreRecruitCombatAction()
	end
	if type(rawget(_G, "Jazz_EnsureRecklessAssaultRechargeOnKill")) == "function" then
		Jazz_EnsureRecklessAssaultRechargeOnKill()
	end
end

lInstallSigRechargeKillFix()

function GetMeleeAttackAPCost(action, unit, args)
	local cost
	if action.CostBasedOnWeapon then
		local weapon = action:GetAttackWeapons(unit, args)	
		local knife = unit:GetItemInSlot("KnifeInventory", "StackableMeleeWeapon", 1, 1)
		if knife then weapon = knife end
		--print(knife)
		cost = (weapon) and unit:GetAttackAPCost(action, weapon, nil, args and args.aim or 0, action.ActionPointDelta) or -1
	else
		cost = action.ActionPoints
	end
	if args and args.action_cost_only then
		return cost
	end
	local goto_pos = args and args.goto_pos
	if not goto_pos and args and args.target then
		goto_pos = unit:GetClosestMeleeRangePos(args.target)
	end
	local attack_cost = cost
	local move_cost = 0
	if cost >= 0 and goto_pos then
		local path = GetCombatPath(unit)
		move_cost = path:GetAP(goto_pos)
		cost = cost + Max(0, move_cost or 0)
	end
	if args and type(args.ap_cost_breakdown) == "table" then
		args.ap_cost_breakdown.attack_cost = attack_cost
		args.ap_cost_breakdown.move_cost = move_cost
		args.ap_cost_breakdown.total_cost = cost
	end
	return cost
end


--Combat Actions

function GetMobileShotResults_EndingPos(action, unit, args)
	local weapon = action:GetAttackWeapons(unit)

	args = table.copy(args)
	args.step_pos = args.goto_pos -- needed in PrepareAttackArgs
	local shot_positions, shot_targets, shot_ch, shot_canceling_reason = CalcMobileShotAttacks(unit, action, args.goto_pos)
	local attacks = {}
	local attack_args

	-- resolve attack action
	local attack_id, atk_action	
	if args.attack_id and args.attack_id ~= action.id then
		attack_id = args.attack_id
		atk_action = CombatActions[attack_id] or CombatActions.SingleShot
	else
		attack_id = "SingleShot"
		atk_action = CombatActions.SingleShot
	end
	local canceling_reason

	for i, pos in ipairs(shot_positions) do
		local target = shot_targets[i]
		local results, attack_args
		if pos and IsValidTarget(target) and not shot_canceling_reason[#shot_positions] and shot_positions[#shot_positions] then
			--[[ 
				In prediction mode we need to presim the attacks (and merge the results later) for UI / damage prediction.
				When simulating the actual attack this extra work isn't needed as Unit:RunAndGun needs to recalculate it anyway after movement.
				Thus, we only pack the relevant data - the position and target. The target can also change, but we have it anyway and we prefer
				to stick to it so the gameplay effects better reflect what we show the user in prediction.
			--]]
			if args.prediction then
				args.target = target
				args.step_pos = point(point_unpack(shot_positions[#shot_positions]))
				args.attack_roll = args.attack_rolls and args.attack_rolls[i]
				args.crit_roll = args.crit_rolls and args.crit_rolls[i]
				args.stealth_kill_roll = args.stealth_kill_rolls and args.stealth_kill_rolls[i]
				args.used_action_id = action.id -- so that cth is calculated for the master/parent action instead of the actual attack action
				args.stance = "Standing"
				args.can_use_covers = false
				local results, attack_args = atk_action:GetActionResults(unit, args)
				attacks[i] = results
				attacks[i].mobile_attack_id = attack_id
				attacks[i].mobile_attack_pos = shot_positions[#shot_positions]
				attacks[i].mobile_attack_target = target
				attacks[i].attack_args = attack_args
			else
				attacks[i] = {
					mobile_attack_id = attack_id,
					mobile_attack_pos = shot_positions[#shot_positions],
					mobile_attack_target = target,
				}
			end
		else
			attacks[i] = {}
		end
	end

	local results
	if args.prediction then
		results = MergeAttacks(attacks)
		results.shot_canceling_reason = shot_canceling_reason and shot_canceling_reason[#shot_canceling_reason]
	else
		results = { attacks = attacks }
	end
	return results, attack_args
end


function GetMobileShotResults_StartPos(action, unit, args)
	local weapon = action:GetAttackWeapons(unit)

	args = table.copy(args)
	args.step_pos = args.goto_pos -- needed in PrepareAttackArgs
	---local shot_positions, shot_targets, shot_ch, shot_canceling_reason = CalcMobileShotAttacks(unit, action, args.goto_pos)
	local attacks = {}
	local attack_args
	local start_packed = GetPackedPosAndStance(unit)
	local start_point = unit:GetPos()

	-- resolve attack action
	local attack_id, atk_action	
	if args.attack_id and args.attack_id ~= action.id then
		attack_id = args.attack_id
		atk_action = CombatActions[attack_id] or CombatActions.SingleShot
	else
		attack_id = "SingleShot"
		atk_action = CombatActions.SingleShot
	end
	local canceling_reason

	--print(shot_positions[1])
	--print(shot_positions[1] and point(point_unpack(shot_positions[1])))
	--print(unit:GetPos())
	--print(unit:GetPos() and (point_unpack(unit:GetPos())))
	--print(point(point_unpack((shot_positions[1]))))
	--dbgargs = args
	--dbgenemies = action:GetTargets({unit})
	--dbgtargets = FindTargetFromPos(action.id, unit, action, action:GetTargets({unit}), unit:GetPos(), weapon, true)
	local shot_targets = action:GetTargets({unit})

	for i=1, 2 do
		local target = shot_targets[i]
		local results, attack_args
		if target and IsValidTarget(target)  then
			--print("validtarget")
			--[[ 
				In prediction mode we need to presim the attacks (and merge the results later) for UI / damage prediction.
				When simulating the actual attack this extra work isn't needed as Unit:RunAndGun needs to recalculate it anyway after movement.
				Thus, we only pack the relevant data - the position and target. The target can also change, but we have it anyway and we prefer
				to stick to it so the gameplay effects better reflect what we show the user in prediction.
			--]]
			if args.prediction then
				args.target = target
				args.step_pos = start_point
				args.attack_roll = args.attack_rolls and args.attack_rolls[i]
				args.crit_roll = args.crit_rolls and args.crit_rolls[i]
				args.stealth_kill_roll = args.stealth_kill_rolls and args.stealth_kill_rolls[i]
				args.used_action_id = action.id -- so that cth is calculated for the master/parent action instead of the actual attack action
				args.stance = "Standing"
				args.can_use_covers = false
				local results, attack_args = atk_action:GetActionResults(unit, args)
				attacks[i] = results
				attacks[i].mobile_attack_id = attack_id
				attacks[i].mobile_attack_pos = start_packed
				attacks[i].mobile_attack_target = target
				attacks[i].attack_args = attack_args

				--dbgargs = args
				--dbgattacks = attacks
			else
				attacks[i] = {
					mobile_attack_id = attack_id,
					mobile_attack_pos = start_packed,
					mobile_attack_target = target,
				}
				dbgattacks = attacks
			end
		else
			attacks[i] = {}
		end
	end

	local results
	if args.prediction then
		results = MergeAttacks(attacks)
		results.shot_canceling_reason = false
	else
		results = { attacks = attacks }
	end
	return results, attack_args
end


local tf_smooth_sleep = 100
local tf_smooth_thread = false
function SetTimeFactorSmooth(tf, time)
	DeleteThread(tf_smooth_thread)
	tf_smooth_thread = CreateRealTimeThread(function()
		local curr_tf = GetTimeFactor()
		if curr_tf == tf then
			return
		end
		local delta = MulDivRound(tf - curr_tf, tf_smooth_sleep, time)
		local cmp = curr_tf < tf 
		while cmp == (curr_tf + delta < tf) do
			curr_tf = curr_tf + delta
			SetTimeFactor(curr_tf)
			Sleep(tf_smooth_sleep)
		end
		SetTimeFactor(tf)
	end)
end


local smooth_tf_change_duration = 1500
function Unit:MoveThenShoot(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local target = args.goto_pos
	local weapon = action:GetAttackWeapons(self)
	if not weapon then 
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return 
	end
	local aim_params = action:GetAimParams(self, weapon)
	local num_shots = aim_params.num_shots
	
	if self.stance ~= "Standing" then
		self:ChangeStance(action_id, 0, "Standing")
	end
	
	-- do the attack/crit rolls
	args.attack_rolls = {}
	args.crit_rolls = {}
	args.stealth_kill_rolls = {}
	for i = 1, num_shots do
		args.attack_rolls[i] = 1 + self:Random(100)
		args.crit_rolls[i] = 1 + self:Random(100)
		if action.StealthAttack then
			args.stealth_kill_rolls[i] = 1 + self:Random(100)
		end
	end
	args.prediction = false
	NetUpdateHash("RunAndGun_0", self, args)
	local results = action:GetActionResults(self, args)
	local action_camera = false --[[ disable action camera for now ]]
	if #(results.attacks or empty_table) == 0 then
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return 
	end
	
	local pathObj, path
	self:PushDestructor(function(self)
		if pathObj then
			DoneObject(pathObj)
		end
	end)
	pathObj = CombatPath:new()
	
	if action_camera then
		local tf = GetTimeFactor()
		self:PushDestructor(function()
			SetTimeFactorSmooth(tf, smooth_tf_change_duration)
		end)
	end
	local base_idle = self:GetIdleBaseAnim()
	local shot_threads

		local recharge_on_kill = action:ResolveValue("recharge_on_kill")
		if recharge_on_kill then
			self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
		end
	
	pathObj:RebuildPaths(self, aim_params.move_ap)
	path = pathObj:GetCombatPathFromPos(target) -- target = args.goto_pos
	self:CombatGoto(action_id, 0, nil, path, true, args.toDoStance)


	for i, attack in ipairs(results.attacks) do
		if not self:CanUseWeapon(weapon) then -- might jam, run out of ammo, etc
			goto continue
		end
		
		NetUpdateHash("MobileShot_1", self, attack.mobile_attack_pos, attack.mobile_attack_target)		
		if attack.mobile_attack_pos and (not IsValidTarget(attack.mobile_attack_target) or attack.mobile_attack_target:IsIncapacitated()) then
			local enemies = table.ifilter(action:GetTargets({self}), function(idx, u) return IsValidTarget(u) end)
			NetUpdateHash("MobileShot_Branch_1", self, attack.mobile_attack_pos, #enemies)
			attack.mobile_attack_target = FindTargetFromPos(action_id, self, action, enemies, point(point_unpack(attack.mobile_attack_pos)), weapon)
		end
		if attack.mobile_attack_pos and IsValidTarget(attack.mobile_attack_target) then
			if action_camera and i == 1 then
				SetTimeFactorSmooth(tf/2, smooth_tf_change_duration)
			end
			
			-- We need to build the path outside of the function so that it
			-- doesn't refund us the ap cost difference.
			local targetPos = point(point_unpack(attack.mobile_attack_pos))
			local occupiedPos = self:GetOccupiedPos()


			-- recheck target, as they might have died while we were moving
			if not IsValidTarget(attack.mobile_attack_target) or attack.mobile_attack_target:IsIncapacitated() then
				local enemies = table.ifilter(action:GetTargets({self}), function(idx, u) return IsValidTarget(u) end)
				NetUpdateHash("MobileShotn_Branch_1_1", self, attack.mobile_attack_pos, #enemies)
				attack.mobile_attack_target = FindTargetFromPos(action_id, self, action, enemies, point(point_unpack(attack.mobile_attack_pos)), weapon)
				if not IsValidTarget(attack.mobile_attack_target) then
					goto continue
				end
			end

			if action_camera then
				if i == #results.attacks then
					SetTimeFactorSmooth(tf, smooth_tf_change_duration)
				end
				SetActionCamera(self, attack.mobile_attack_target)
			end
			self:SetRandomAnim(base_idle)
			local atk_action = CombatActions[attack.mobile_attack_id] or action
			
			-- rerun simulation to account for changes happened in the meantime (broken covers, etc)
			local atk_args = {
				prediction = false,
				target = attack.mobile_attack_target,
				stance = "Standing",
				can_use_covers = i == #results.attacks,
				used_action_id = action_id, -- so that cth is calculated for the master/parent action instead of the actual attack action
			}			
			
			NetUpdateHash("MobileShot_2", self, atk_args.target, args.goto_pos)
			local atk_results, attack_args = atk_action:GetActionResults(self, atk_args)			
			attack_args.origin_action_id = action_id
			attack_args.keep_ui_mode = true
			attack_args.unit_moved = true
			attack_args.dont_restore_aim = true
			if atk_action.id == "KnifeThrow" then
				self:ExecKnifeThrow(atk_action, cost_ap, attack_args, atk_results)
			else
				shot_threads = shot_threads or {}
				attack_args.external_wait_shots = shot_threads
				self:ExecFirearmAttacks(atk_action, cost_ap, attack_args, atk_results)
			end
		end
		::continue::
	end
	
	local cooldown = action:ResolveValue("cooldown")
	if cooldown then
		self:SetEffectExpirationTurn(action.id, "cooldown", g_Combat.current_turn + cooldown)
	end
	if action_camera then
		RemoveActionCamera()
		self:PopAndCallDestructor() -- camera
	end

	-- if not at target loc, goto there (there mustn't be a target when that happens)	
	local occupiedPos = self:GetOccupiedPos()
	if self.return_pos and self.return_pos:Dist(target) < const.SlabSizeX / 2 then
		self:ReturnToCover()
	elseif self:GetDist(occupiedPos) > const.SlabSizeX / 2 and self:GetDist(target) < const.SlabSizeX / 2 then
		self:SetTargetDummyFromPos()
	else
		pathObj:RebuildPaths(self, aim_params.move_ap)
		path = pathObj:GetCombatPathFromPos(target)
		self:CombatGoto(action_id, 0, nil, path, true)
	end
	if shot_threads then
		Firearm:WaitFiredShots(shot_threads)
	end	
	self:PopAndCallDestructor() -- pathObj 
end


function Unit:ShootThenMove(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local target = args.goto_pos
	local weapon = action:GetAttackWeapons(self)
	if not weapon then 
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return 
	end
	local aim_params = action:GetAimParams(self, weapon)
	local num_shots = aim_params.num_shots
	
	if self.stance ~= "Standing" then
		self:ChangeStance(action_id, 0, "Standing")
	end
	
	-- do the attack/crit rolls
	args.attack_rolls = {}
	args.crit_rolls = {}
	args.stealth_kill_rolls = {}
	for i = 1, num_shots do
		args.attack_rolls[i] = 1 + self:Random(100)
		args.crit_rolls[i] = 1 + self:Random(100)
		if action.StealthAttack then
			args.stealth_kill_rolls[i] = 1 + self:Random(100)
		end
	end
	args.prediction = false
	NetUpdateHash("ShootThenMove_0", self, args)
	local results = action:GetActionResults(self, args)
	local action_camera = false --[[ disable action camera for now ]]
	if #(results.attacks or empty_table) == 0 then
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return 
	end
	
	local pathObj, path
	self:PushDestructor(function(self)
		if pathObj then
			DoneObject(pathObj)
		end
	end)
	pathObj = CombatPath:new()
	
	if action_camera then
		local tf = GetTimeFactor()
		self:PushDestructor(function()
			SetTimeFactorSmooth(tf, smooth_tf_change_duration)
		end)
	end
	local base_idle = self:GetIdleBaseAnim()
	local shot_threads



	for i, attack in ipairs(results.attacks) do
		if not self:CanUseWeapon(weapon) then -- might jam, run out of ammo, etc
			goto continue
		end
		
		NetUpdateHash("ShootThenMove_1", self, attack.mobile_attack_pos, attack.mobile_attack_target)		
		if attack.mobile_attack_pos and (not IsValidTarget(attack.mobile_attack_target) or attack.mobile_attack_target:IsIncapacitated()) then
			local enemies = table.ifilter(action:GetTargets({self}), function(idx, u) return IsValidTarget(u) end)
			NetUpdateHash("ShootThenMove_Branch_1", self, attack.mobile_attack_pos, #enemies)
			attack.mobile_attack_target = FindTargetFromPos(action_id, self, action, enemies, point(point_unpack(attack.mobile_attack_pos)), weapon)
		end
		if attack.mobile_attack_pos and IsValidTarget(attack.mobile_attack_target) then
			if action_camera and i == 1 then
				SetTimeFactorSmooth(tf/2, smooth_tf_change_duration)
			end
			
			-- We need to build the path outside of the function so that it
			-- doesn't refund us the ap cost difference.
			local occupiedPos = self:GetOccupiedPos()
			local targetPos = occupiedPos 


			-- recheck target, as they might have died while we were moving
			if not IsValidTarget(attack.mobile_attack_target) or attack.mobile_attack_target:IsIncapacitated() then
				local enemies = table.ifilter(action:GetTargets({self}), function(idx, u) return IsValidTarget(u) end)
				NetUpdateHash("MobileShotn_Branch_1_1", self, attack.mobile_attack_pos, #enemies)
				attack.mobile_attack_target = FindTargetFromPos(action_id, self, action, enemies, point(point_unpack(attack.mobile_attack_pos)), weapon)
				if not IsValidTarget(attack.mobile_attack_target) then
					goto continue
				end
			end

			if action_camera then
				if i == #results.attacks then
					SetTimeFactorSmooth(tf, smooth_tf_change_duration)
				end
				SetActionCamera(self, attack.mobile_attack_target)
			end
			self:SetRandomAnim(base_idle)
			local atk_action = CombatActions[attack.mobile_attack_id] or action
			
			-- rerun simulation to account for changes happened in the meantime (broken covers, etc)
			local atk_args = {
				prediction = false,
				target = attack.mobile_attack_target,
				stance = "Standing",
				can_use_covers = i == #results.attacks,
				used_action_id = action_id, -- so that cth is calculated for the master/parent action instead of the actual attack action
			}			
			
			NetUpdateHash("MobileShot_2", self, atk_args.target, args.goto_pos)
			local atk_results, attack_args = atk_action:GetActionResults(self, atk_args)			
			attack_args.origin_action_id = action_id
			attack_args.keep_ui_mode = true
			attack_args.unit_moved = true
			attack_args.dont_restore_aim = true
			if atk_action.id == "KnifeThrow" then
				self:ExecKnifeThrow(atk_action, cost_ap, attack_args, atk_results)
			else
				shot_threads = shot_threads or {}
				attack_args.external_wait_shots = shot_threads
				self:ExecFirearmAttacks(atk_action, cost_ap, attack_args, atk_results)
			end
		end
		::continue::
	end
	
	local cooldown = action:ResolveValue("cooldown")
	if cooldown then
		self:SetEffectExpirationTurn(action.id, "cooldown", g_Combat.current_turn + cooldown)
	end
	if action_camera then
		RemoveActionCamera()
		self:PopAndCallDestructor() -- camera
	end

	-- if not at target loc, goto there (there mustn't be a target when that happens)	
	local occupiedPos = self:GetOccupiedPos()
	if self.return_pos and self.return_pos:Dist(target) < const.SlabSizeX / 2 then
		self:ReturnToCover()
	elseif self:GetDist(occupiedPos) > const.SlabSizeX / 2 and self:GetDist(target) < const.SlabSizeX / 2 then
		self:SetTargetDummyFromPos()
	else
		pathObj:RebuildPaths(self, aim_params.move_ap)
		path = pathObj:GetCombatPathFromPos(target)
		self:CombatGoto(action_id, 0, nil, path, true)
	end
	if shot_threads then
		Firearm:WaitFiredShots(shot_threads)
	end	

		local recharge_on_kill = action:ResolveValue("recharge_on_kill")
		if recharge_on_kill then
			self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
		end

	self:PopAndCallDestructor() -- pathObj 
	
	
end

-- Мозамбик - 2 в тело, 1 в голову
function Unit:Mozambique(action_id, cost_ap, args)
  local target = args.target
  if not IsKindOf(target, "Unit") then return end


  local action = CombatActions[action_id]
  local weapon = self:GetActiveWeapons()
  if not weapon then return end

  local bodyParts = { "Torso", "Torso", "Head" }

  for i = 1, #bodyParts do
    if not self:CanUseWeapon(weapon, 1) then break end

    local spot = bodyParts[i]
	if i == #bodyParts then
		args.critchance = 100
	end
	
    args.target_spot_group = spot
    self:FirearmAttack(action_id, 0, args)
  end

		local recharge_on_kill = action:ResolveValue("recharge_on_kill")
		if recharge_on_kill then
			self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
		end
end

-- Даблтап - 2 в тело
function Unit:DoubleTap(action_id, cost_ap, args)
  local target = args.target
  if not IsKindOf(target, "Unit") then return end


  local action = CombatActions[action_id]
  local weapon = self:GetActiveWeapons()
  if not weapon then return end

  local bodyParts = { "Torso", "Torso"}

  for i = 1, #bodyParts do
    if not self:CanUseWeapon(weapon, 1) then break end

    local spot = bodyParts[i]
	if i == #bodyParts then
	end
	
    args.target_spot_group = spot
    self:FirearmAttack(action_id, 0, args)
  end

  local recharge_on_kill = action:ResolveValue("recharge_on_kill") or 0
  --self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
end

-- В яблочко - 1 в голову
function Unit:Bullseye(action_id, cost_ap, args)
  local target = args.target
  if not IsKindOf(target, "Unit") then return end


  local action = CombatActions[action_id]
  local weapon = self:GetActiveWeapons()
  if not weapon then return end
	action.critchance = 100
  local bodyParts = { "Head"}

  for i = 1, #bodyParts do

    if not self:CanUseWeapon(weapon, 1) then break end

    local spot = bodyParts[i]
	if i == #bodyParts then
	end
	
    args.target_spot_group = spot
    self:FirearmAttack(action_id, 0, args)
  end

  local recharge_on_kill = action:ResolveValue("recharge_on_kill") or 0
  self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
end

-- Мозамбик - 2 в тело, 1 в голову
function Unit:Zipper(action_id, cost_ap, args)
  local target = args.target
  if not IsKindOf(target, "Unit") then return end


  local action = CombatActions[action_id]
  local weapon = self:GetActiveWeapons()
  if not weapon then return end

  local bodyParts = { "Legs", "Torso", "Head" }

  for i = 1, #bodyParts do
    if not self:CanUseWeapon(weapon, 1) then break end

    local spot = bodyParts[i]
	if i == #bodyParts then
		--args.critchance = 100
	end
	
    args.target_spot_group = spot
    self:FirearmAttack(action_id, 0, args)
  end

  local recharge_on_kill = action:ResolveValue("recharge_on_kill") or 0
  self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
end

function Unit:RunAndGun(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local target = args.goto_pos
	local weapon = action:GetAttackWeapons(self)
	if not weapon then 
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return 
	end
	local aim_params = action:GetAimParams(self, weapon)
	local num_shots = aim_params.num_shots
	
	if self.stance ~= "Standing" then
		self:ChangeStance(action_id, 0, "Standing")
	end
	
	-- do the attack/crit rolls
	args.attack_rolls = {}
	args.crit_rolls = {}
	args.stealth_kill_rolls = {}
	for i = 1, num_shots do
		args.attack_rolls[i] = 1 + self:Random(100)
		args.crit_rolls[i] = 1 + self:Random(100)
		if action.StealthAttack then
			args.stealth_kill_rolls[i] = 1 + self:Random(100)
		end
	end
	args.prediction = false
	NetUpdateHash("RunAndGun_0", self, args)
	local results = action:GetActionResults(self, args)
	local action_camera = false --[[ disable action camera for now ]]
	if #(results.attacks or empty_table) == 0 then
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return 
	end
	
	local pathObj, path
	self:PushDestructor(function(self)
		if pathObj then
			DoneObject(pathObj)
		end
	end)
	pathObj = CombatPath:new()
	
	if action_camera then
		local tf = GetTimeFactor()
		self:PushDestructor(function()
			SetTimeFactorSmooth(tf, smooth_tf_change_duration)
		end)
	end
	local base_idle = self:GetIdleBaseAnim()
	local shot_threads
	for i, attack in ipairs(results.attacks) do
		if not self:CanUseWeapon(weapon) then -- might jam, run out of ammo, etc
			goto continue
		end
		NetUpdateHash("RunAndGun_1", self, attack.mobile_attack_pos, attack.mobile_attack_target)		
		if attack.mobile_attack_pos and (not IsValidTarget(attack.mobile_attack_target) or attack.mobile_attack_target:IsIncapacitated()) then
			local enemies = table.ifilter(action:GetTargets({self}), function(idx, u) return IsValidTarget(u) end)
			NetUpdateHash("RunAndGun_Branch_1", self, attack.mobile_attack_pos, #enemies)
			attack.mobile_attack_target = FindTargetFromPos(action_id, self, action, enemies, point(point_unpack(attack.mobile_attack_pos)), weapon)
		end
		if attack.mobile_attack_pos and IsValidTarget(attack.mobile_attack_target) then
			if action_camera and i == 1 then
				SetTimeFactorSmooth(tf/2, smooth_tf_change_duration)
			end
			
			-- We need to build the path outside of the function so that it
			-- doesn't refund us the ap cost difference.
			local targetPos = point(point_unpack(attack.mobile_attack_pos))
			local occupiedPos = self:GetOccupiedPos()
			if self:GetDist(occupiedPos) > const.SlabSizeX / 2 and self:GetDist(targetPos) < const.SlabSizeX / 2 then
				-- already at target position because of expose/aim
				self:SetTargetDummy(nil, nil, base_idle, 0)
			else
				pathObj:RebuildPaths(self, aim_params.move_ap)
				path = pathObj:GetCombatPathFromPos(targetPos)			
				self:CombatGoto(action_id, 0, nil, path, true, i == #results.attacks and args.toDoStance)
			end

			-- recheck target, as they might have died while we were moving
			if not IsValidTarget(attack.mobile_attack_target) or attack.mobile_attack_target:IsIncapacitated() then
				local enemies = table.ifilter(action:GetTargets({self}), function(idx, u) return IsValidTarget(u) end)
				NetUpdateHash("RunAndGun_Branch_1_1", self, attack.mobile_attack_pos, #enemies)
				attack.mobile_attack_target = FindTargetFromPos(action_id, self, action, enemies, point(point_unpack(attack.mobile_attack_pos)), weapon)
				if not IsValidTarget(attack.mobile_attack_target) then
					goto continue
				end
			end

			if action_camera then
				if i == #results.attacks then
					SetTimeFactorSmooth(tf, smooth_tf_change_duration)
				end
				SetActionCamera(self, attack.mobile_attack_target)
			end
			self:SetRandomAnim(base_idle)
			local atk_action = CombatActions[attack.mobile_attack_id] or action
			
			-- rerun simulation to account for changes happened in the meantime (broken covers, etc)
			local atk_args = {
				prediction = false,
				target = attack.mobile_attack_target,
				stance = "Standing",
				can_use_covers = i == #results.attacks,
				used_action_id = action_id, -- so that cth is calculated for the master/parent action instead of the actual attack action
			}			
			
			NetUpdateHash("RunAndGun_2", self, atk_args.target, args.goto_pos)
			local atk_results, attack_args = atk_action:GetActionResults(self, atk_args)			
			attack_args.origin_action_id = action_id
			attack_args.keep_ui_mode = true
			attack_args.unit_moved = true
			attack_args.dont_restore_aim = true
			if atk_action.id == "KnifeThrow" then
				self:ExecKnifeThrow(atk_action, cost_ap, attack_args, atk_results)
			else
				shot_threads = shot_threads or {}
				attack_args.external_wait_shots = shot_threads
				self:ExecFirearmAttacks(atk_action, cost_ap, attack_args, atk_results)
			end
		end
		::continue::
	end
	
	local cooldown = action:ResolveValue("cooldown")
	if cooldown then
		self:SetEffectExpirationTurn(action.id, "cooldown", g_Combat.current_turn + cooldown)
	end
	if action_camera then
		RemoveActionCamera()
		self:PopAndCallDestructor() -- camera
	end

	-- if not at target loc, goto there (there mustn't be a target when that happens)	
	local occupiedPos = self:GetOccupiedPos()
	if self.return_pos and self.return_pos:Dist(target) < const.SlabSizeX / 2 then
		self:ReturnToCover()
	elseif self:GetDist(occupiedPos) > const.SlabSizeX / 2 and self:GetDist(target) < const.SlabSizeX / 2 then
		self:SetTargetDummyFromPos()
	else
		pathObj:RebuildPaths(self, aim_params.move_ap)
		path = pathObj:GetCombatPathFromPos(target)
		self:CombatGoto(action_id, 0, nil, path, true)
	end
	if shot_threads then
		Firearm:WaitFiredShots(shot_threads)
	end	

		local recharge_on_kill = action:ResolveValue("recharge_on_kill")
		if recharge_on_kill then
			self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
		end


	self:PopAndCallDestructor() -- pathObj 
	
end

-- Smiley RecklessAssault List2: improved RnG; no Energy/Tiredness loss (vanilla SetTired).
-- recharge_on_kill is on CombatActions.RecklessAssault Parameters; Unit:RunAndGun applies CD.
function Unit:RecklessAssault(action_id, cost_ap, args)
	self:RunAndGun(action_id, cost_ap, args)
end

--- Ensure RecklessAssault has recharge_on_kill=1 (same contract as JAZZ RunAndGun).
function Jazz_EnsureRecklessAssaultRechargeOnKill()
	local ca = CombatActions and CombatActions.RecklessAssault
	if not ca then
		return false
	end
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return false
	end
	local cache = g_PresetParamCache[ca]
	if not cache then
		cache = {}
		g_PresetParamCache[ca] = cache
	end
	if cache.recharge_on_kill == nil or cache.recharge_on_kill < 1 then
		cache.recharge_on_kill = 1
	end
	return true
end

Jazz_EnsureRecklessAssaultRechargeOnKill()

--- Weapon gate for RecklessAssault: SMG / Carbine / AssaultRifle.
function Jazz_RecklessAssaultWeaponOk(weapon)
	if not weapon then
		return false
	end
	if IsKindOfClasses(weapon, "SubmachineGun", "AssaultRifle", "Carbine") then
		return true
	end
	if weapon.WeaponSizeClass == "Carbine" then
		return true
	end
	return false
end

function Jazz_RecklessAssaultGetWeapon(unit, args)
	if args and args.weapon then
		return Jazz_RecklessAssaultWeaponOk(args.weapon) and args.weapon or nil
	end
	if not unit then
		return nil
	end
	local w = unit:GetActiveWeapons("Firearm")
	if Jazz_RecklessAssaultWeaponOk(w) then
		return w
	end
	return nil
end


function Unit:FirearmAttack(action_id, cost_ap, args, applied_status) -- SingleShot/DualShot
	if true then	 -- net debug code
		local effects = {}
		for i, effect in ipairs(self.StatusEffects) do
			effects[i] = effect.class
		end
		effects = table.concat(effects, ",")
		local target_effects = "-"
		if IsKindOf(args.target, "Unit") then
			target_effects = {}
			for i, effect in ipairs(args.target.StatusEffects) do
				target_effects[i] = effect.class
			end
			target_effects = table.concat(target_effects, ",")
		end

		NetUpdateHash("Unit:FirearmAttack", action_id, cost_ap, self, effects, args.target, target_effects)
	end -- end net debug code
	local target = args.target
	-- JAZZ-COMBAT-003: expose attacker/args to LightningReactionCheck (OnFirearmAttackStart is before g_CurrentAttackActions).
	g_JAZZ_FirearmAttacker = self
	g_JAZZ_FirearmAttackArgs = args
	self:CallReactions("OnFirearmAttackStart", self, target, CombatActions[action_id], args)
	if IsKindOf(target, "Unit") then
		target:CallReactions("OnFirearmAttackStart", self, target, CombatActions[action_id], args)
	end
	g_JAZZ_FirearmAttacker = false
	g_JAZZ_FirearmAttackArgs = false
	while not args.opportunity_attack and IsKindOf(target, "Unit") and not target:IsIdleOrRunningBehavior() do
		WaitMsg("Idle", 50)
	end
	if args.replace_action then
		action_id = args.replace_action
	end
	
	if IsPoint(target) or IsValidTarget(target) then
		local action = CombatActions[action_id]
		
		if action.StealthAttack then
			args.stealth_kill_roll = 1 + self:Random(100)
		end
		args.prediction = false
		
		local units_waiting = {}
		
		self:PushDestructor(function()
			for _, unit in ipairs(units_waiting) do
				unit.waiting_attack = false
			end
		end)
		
		if not g_Combat and IsKindOf(target, "Unit") then
			units_waiting[1] = target
			PropagateAwareness(units_waiting)
			for _, unit in ipairs(units_waiting) do
				if unit:IsInterruptable() then
					unit.waiting_attack = true
					unit:InterruptCommand("WaitAttack")
				end
			end
			repeat
				local waiting = false
				for _, unit in ipairs(units_waiting) do
					waiting = waiting or (unit.command == "WaitAttack" and not unit.waiting_attack)
				end
				if waiting then
					Sleep(10)
				end
			until not waiting
		end
		
		local results, attack_args = action:GetActionResults(self, args)
		self:ExecFirearmAttacks(action, cost_ap, attack_args, results)
		self:PopAndCallDestructor()
	else
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
	end
		local action = CombatActions[action_id]
		local cooldown = action:ResolveValue("cooldown")
		if cooldown then
			self:SetEffectExpirationTurn(action_id, "cooldown", g_Combat.current_turn + cooldown)
		end
		local recharge_on_kill = action:ResolveValue("recharge_on_kill")
		if recharge_on_kill then
			self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
		end
end

-- JAZZ_TargetSweep: short burst (or SingleShot) at each LOS enemy in the aim cone.
-- Refund AP + skip signature recharge when nothing fires (vanilla DanceForMe pattern left AP spent).
function Unit:TargetSweep(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local weapon = self:GetActiveWeapons()
	if not weapon then
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return
	end

	local aoeParams = weapon:GetAreaAttackParams(action_id, self)
	local attackData = self:ResolveAttackParams(action_id, args.target, {})

	local attackerPos = attackData.step_pos
	local attackerPos3D = attackerPos
	if not attackerPos3D:IsValidZ() then
		attackerPos3D = attackerPos3D:SetTerrainZ()
	end
	local targetPos = args.target
	local targetAngle = CalcOrientation(attackerPos, targetPos)
	local distance = Clamp(attackerPos3D:Dist(targetPos), aoeParams.min_range * const.SlabSizeX, aoeParams.max_range * const.SlabSizeX)

	local attackAction
	if table.find(weapon.AvailableAttacks, "BurstFire") and CombatActions.BurstFire then
		attackAction = CombatActions.BurstFire
	elseif table.find(weapon.AvailableAttacks, "SingleShot") and CombatActions.SingleShot then
		attackAction = CombatActions.SingleShot
	else
		attackAction = self:GetDefaultAttackAction("ranged")
	end

	local fired_any = false
	local enemies = GetEnemies(self)
	local maxValue, losValues = CheckLOS(enemies, attackerPos, distance, attackData.stance, aoeParams.cone_angle, targetAngle, false)

	if maxValue and attackAction then
		for i, los in ipairs(losValues) do
			if los then
				if not self:CanUseWeapon(weapon, 1) then
					break
				end
				local tempArgs = table.copy(args)
				tempArgs.target = enemies[i]
				tempArgs.target_spot_group = "Torso"
				tempArgs.aim = 0
				tempArgs.distance = nil
				if self:CanAttack(tempArgs.target, weapon, attackAction, nil, nil, "skip_ap_check") then
					self:FirearmAttack(attackAction.id, 0, tempArgs)
					fired_any = true
				end
			end
		end
	end

	if not fired_any then
		self:GainAP(cost_ap)
		CombatActionInterruped(self)
		return
	end

	local recharge_on_kill = action:ResolveValue("recharge_on_kill") or 0
	self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
end

-- Spike BulletHell: FirearmAttack (fires reliably) + real cone-arc projectiles (COMBAT-006 v2).
-- AlwaysHits AOE / vanilla Suppressed cleared in System_OR_Weapons JazzInstallBulletHellProjectiles.
-- Autofire gate for AN94 / JAZZ_LargeAutoFire lives in System_OR_Weapons.lua.
function Unit:BulletHell(action_id, cost_ap, args)
	args = args or {}
	args.attack_anim_delay = 50
	self:SetActionCommand("FirearmAttack", action_id, cost_ap, args)
end

-- Meltdown signature «Ураган Норма»: active fear AoE (not RunAndGun / not on-hit passive).
-- Enemies within fearAoE slabs → fail Wisdom(50) → Panicked, else Berserk; refresh their AP.
function Unit:VengefulTemperament(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local aoe = (action and action:ResolveValue("fearAoE")) or 5
	for _, unit in ipairs(g_Units) do
		if unit ~= self and IsValidTarget(unit) and self:IsOnEnemySide(unit)
			and DivRound(self:GetDist(unit), const.SlabSizeX) <= aoe then
			if not RollSkillCheck(unit, "Wisdom", 50) then
				unit:AddStatusEffect("Panicked")
			else
				unit:AddStatusEffect("Berserk")
			end
			unit.ActionPoints = unit:GetMaxActionPoints()
		end
	end
	self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, false)
end

-- Igor Nazdarovya: drink — clear Pain, heal 15–20 HP, stack Drunk (≤5); CD recharge_on_kill.
function Unit:Nazdarovya(action_id, cost_ap, args)
	local action = CombatActions[action_id]
	local max_stacks = (action and action:ResolveValue("maxStacks")) or 5
	local drunk = self:GetStatusEffect("Drunk")
	local stacks = drunk and (drunk.stacks or 1) or 0
	if stacks >= max_stacks then
		return
	end

	local heal_min = (action and action:ResolveValue("healMin")) or 15
	local heal_max = (action and action:ResolveValue("healMax")) or 20
	local span = Max(0, heal_max - heal_min)
	local heal = heal_min + InteractionRand(span + 1, "NazdarovyaHeal")
	if type(self.HitPoints) == "number" and type(self.MaxHitPoints) == "number" then
		self.HitPoints = Min(self.MaxHitPoints, self.HitPoints + heal)
		ObjModified(self)
	end

	local refund_ap = rawget(_G, "JazzRefundPainStartTurnAP")
	if type(refund_ap) == "function" then
		refund_ap(self)
	end
	self:RemoveStatusEffect("Pain", "all")
	Msg("UnitAPChanged", self)

	self:AddStatusEffect("Drunk", 1)

	local recharge_on_kill = action and action:ResolveValue("recharge_on_kill")
	if recharge_on_kill then
		self:AddSignatureRechargeTime(action_id, const.Combat.SignatureAbilityRechargeTime, recharge_on_kill > 0)
	end
end

--- Ensure Nazdarovya has recharge_on_kill=1 (ResolveValue reads g_PresetParamCache).
function Jazz_EnsureNazdarovyaRechargeOnKill()
	local ca = CombatActions and CombatActions.Nazdarovya
	if not ca then
		return false
	end
	local params = ca.Parameters or {}
	local has = false
	for _, p in ipairs(params) do
		if p and p.Name == "recharge_on_kill" then
			p.Value = 1
			has = true
			break
		end
	end
	if not has then
		params[#params + 1] = PlaceObj("PresetParamNumber", {
			"Name", "recharge_on_kill",
			"Value", 1,
			"Tag", "<recharge_on_kill>",
		})
		ca.Parameters = params
	end
	if type(rawget(_G, "g_PresetParamCache")) ~= "table" then
		return false
	end
	local cache = g_PresetParamCache[ca]
	if not cache then
		cache = {}
		g_PresetParamCache[ca] = cache
	end
	cache.recharge_on_kill = 1
	return true
end

Jazz_EnsureNazdarovyaRechargeOnKill()

-- Pierre GloryHog List2: once/combat recruit visible non-boss enemy → ally (AI-controlled).
-- Charge (non-straight +15 grit) stays vanilla CombatActions.GloryHog / Unit:GloryHogCharge.
g_JAZZ_PierreRecruitCAPatched = rawget(_G, "g_JAZZ_PierreRecruitCAPatched") or false

function Jazz_IsPierreRecruitBossBlocked(unit)
	if not unit then
		return true
	end
	if unit.villain or unit.ImportantNPC then
		return true
	end
	local sid = unit.session_id
	local ud = sid and gv_UnitData and gv_UnitData[sid]
	if ud and (ud.villain or ud.ImportantNPC) then
		return true
	end
	return false
end

function Jazz_PierreRecruitGetTargets(attacker)
	local out = {}
	if not attacker or not attacker.GetVisibleEnemies then
		return out
	end
	for _, u in ipairs(attacker:GetVisibleEnemies() or empty_table) do
		if IsValidTarget(u) and attacker:IsOnEnemySide(u) and not Jazz_IsPierreRecruitBossBlocked(u) then
			out[#out + 1] = u
		end
	end
	return out
end

function Unit:Jazz_PierreRecruit(action_id, cost_ap, args)
	args = args or empty_table
	local target = args.target
	-- ExecuteCombatChoice may pass the unit as args itself in odd call shapes.
	if not IsKindOf(target, "Unit") and IsKindOf(args, "Unit") then
		target = args
	end
	if self.GetEffectValue and self:GetEffectValue("Jazz_PierreRecruitUsed") then
		return
	end
	if not IsKindOf(target, "Unit") or not IsValidTarget(target) then
		return
	end
	if not self:IsOnEnemySide(target) or Jazz_IsPierreRecruitBossBlocked(target) then
		return
	end
	if target.Interrupt then
		pcall(function()
			target:Interrupt()
		end)
	end
	if target.SetSide then
		target:SetSide("ally")
	end
	if target.SetCommand then
		pcall(function()
			target:SetCommand("Idle")
		end)
	end
	if target.GetMaxActionPoints and target.ActionPoints ~= nil then
		target.ActionPoints = target:GetMaxActionPoints()
	end
	if target.SetEffectValue then
		target:SetEffectValue("Jazz_PierreRecruited", true)
	end
	if self.SetEffectValue then
		self:SetEffectValue("Jazz_PierreRecruitUsed", true)
	end
	local nick = (target.GetLogName and target:GetLogName()) or target.Nick or target.Name
	CombatLog("important", T{890000000009942, "<merc> recruited <target> as an ally.", merc = self.Nick, target = nick})
	ObjModified(self)
	ObjModified(target)
	if g_Combat then
		ObjModified(g_Combat)
	end
end

-- Recruit is a targeted signature like PinDown/MarkTarget: one hotbar button, then
-- click the enemy in the world. ShowCombatActionTargetChoice spawned one GloryHog
-- icon per visible enemy (the "extra buttons" on Pierre's bar / enemy badge).
g_JAZZ_PierreRecruitAttackStartWrapped = rawget(_G, "g_JAZZ_PierreRecruitAttackStartWrapped") or false
g_JAZZ_CombatActionAttackStartBase = rawget(_G, "g_JAZZ_CombatActionAttackStartBase") or false
g_JAZZ_PierreRecruitImpossibleAttackWrapped = rawget(_G, "g_JAZZ_PierreRecruitImpossibleAttackWrapped") or false
g_JAZZ_CheckAndReportImpossibleAttackBase = rawget(_G, "g_JAZZ_CheckAndReportImpossibleAttackBase") or false
g_JAZZ_PierreRecruitCAPatched = rawget(_G, "g_JAZZ_PierreRecruitCAPatched") or false

local function lInstallPierreRecruitTargetingWraps()
	local start = rawget(_G, "CombatActionAttackStart")
	if type(start) == "function" then
		local prev_base = rawget(_G, "g_JAZZ_CombatActionAttackStartBase")
		-- ReloadLua may restore vanilla while the wrap flag stays set.
		if not (rawget(_G, "g_JAZZ_PierreRecruitAttackStartWrapped")
			and type(prev_base) == "function"
			and start ~= prev_base)
		then
			rawset(_G, "g_JAZZ_CombatActionAttackStartBase", start)
			rawset(_G, "g_JAZZ_PierreRecruitAttackStartWrapped", true)
			function CombatActionAttackStart(self, units, args, mode, noChangeAction)
				if self and self.id == "Jazz_PierreRecruit" then
					args = args or {}
					local unit = units and units[1]
					if not args.target then
						local t = Jazz_PierreRecruitGetTargets(unit)
						args.target = t and t[1]
					end
					if not unit or not args.target then
						return
					end
					-- Skip Aim/crosshair (no weapon). IModeCombatAttack still lets you click a unit.
					SetInGameInterfaceMode("IModeCombatAttack", {
						action = self,
						attacker = unit,
						target = args.target,
					})
					return
				end
				return g_JAZZ_CombatActionAttackStartBase(self, units, args, mode, noChangeAction)
			end
		end
	end
	local check = rawget(_G, "CheckAndReportImpossibleAttack")
	if type(check) == "function" then
		local prev_base = rawget(_G, "g_JAZZ_CheckAndReportImpossibleAttackBase")
		if not (rawget(_G, "g_JAZZ_PierreRecruitImpossibleAttackWrapped")
			and type(prev_base) == "function"
			and check ~= prev_base)
		then
			rawset(_G, "g_JAZZ_CheckAndReportImpossibleAttackBase", check)
			rawset(_G, "g_JAZZ_PierreRecruitImpossibleAttackWrapped", true)
			function CheckAndReportImpossibleAttack(unit, action, args)
				if action and action.id == "Jazz_PierreRecruit" then
					local state, err = action:GetUIState({ unit }, args)
					if state == "enabled" then
						return "enabled"
					end
					if err then
						ReportAttackError(IsValid(args and args.target) and args.target or unit, err)
					end
					return state
				end
				return g_JAZZ_CheckAndReportImpossibleAttackBase(unit, action, args)
			end
		end
	end
end

function Jazz_InstallPierreRecruitCombatAction()
	lInstallPierreRecruitTargetingWraps()
	local ca = CombatActions and CombatActions.Jazz_PierreRecruit
	if not ca then
		return false
	end
	ca.IsTargetableAttack = true
	ca.Icon = "UI/Icons/Hud/talk"
	ca.UIBegin = function(self, units, args)
		CombatActionAttackStart(self, units, args, "IModeCombatAttack")
	end
	ca.GetAnyTarget = function(self, units)
		local t = Jazz_PierreRecruitGetTargets(units and units[1])
		return t and t[1]
	end
	ca.GetTargets = function(self, units)
		return Jazz_PierreRecruitGetTargets(units and units[1]) or empty_table
	end
	ca.GetDefaultTarget = function(self, unit)
		local t = Jazz_PierreRecruitGetTargets(unit)
		return t and t[1]
	end
	if not rawget(ca, "jazz_recruit_uistate_wrapped") then
		rawset(ca, "jazz_recruit_uistate_base", ca.GetUIState)
		rawset(ca, "jazz_recruit_uistate_wrapped", true)
	end
	local baseUI = rawget(ca, "jazz_recruit_uistate_base")
	if type(baseUI) == "function" then
		ca.GetUIState = function(self, units, args)
			local state, reason = baseUI(self, units, args)
			if state ~= "enabled" then
				return state, reason
			end
			local target = args and args.target
			if IsKindOf(target, "Unit") then
				local ok = false
				for _, u in ipairs(self:GetTargets(units) or empty_table) do
					if u == target then
						ok = true
						break
					end
				end
				if not ok then
					return "disabled", AttackDisableReasons.NoTarget
				end
			end
			return "enabled"
		end
	end
	-- Charge signature tooltip should stay Charge-only; recruit has its own CA.
	local gh = CombatActions.GloryHog
	if gh and not rawget(gh, "jazz_charge_desc_patched") then
		rawset(gh, "jazz_charge_desc_patched", true)
		gh.GetActionDescription = function(self, units)
			local unit = units and units[1]
			local perk = unit and CharacterEffectDefs and CharacterEffectDefs.GloryHog
			local grit = (perk and perk:ResolveValue("temp_hp")) or 15
			return T{890000000009943, "Machete <em>Charge</em> without a straight-line path; grants <em><grit></em> <GameTerm('Grit')>.", grit = grit}
		end
	end
	rawset(_G, "g_JAZZ_PierreRecruitCAPatched", true)
	return true
end

function OnMsg.CombatStart()
	Jazz_InstallPierreRecruitCombatAction()
end

Jazz_InstallPierreRecruitCombatAction()
