-- JAZZ-MED-001.  The helpers here are intentionally global: generated
-- CharacterEffect and CombatAction definitions call them after reload.
JazzBleedTierOrder = { "BleedingHeavy", "BleedingMedium", "Bleeding" }

-- JA3 resolves many engine globals through _G's metatable __index.
-- rawget(_G, "CanBandageUI" / "g_Classes" / …) returns nil even when the bare
-- name works — that used to skip all medicine melee / Unit.Bandage wraps.
local function lG(name)
	local v = rawget(_G, name)
	if v ~= nil then
		return v
	end
	local mt = getmetatable(_G)
	local idx = mt and mt.__index
	if type(idx) == "function" then
		return idx(_G, name)
	end
	if type(idx) == "table" then
		return idx[name]
	end
end

local JazzBleedDamage = {
	Bleeding = 3,
	BleedingMedium = 6,
	BleedingHeavy = 12,
}

local function lBleedStacks(unit, id)
	-- MoveStep/melee can put a Point in args.target; never call methods on it.
	if not unit or type(unit.GetStatusEffect) ~= "function" then
		return 0
	end
	local effect = unit:GetStatusEffect(id)
	return effect and effect.stacks or 0
end

-- CombatAction args.target is usually a Unit, but melee MoveStep may pass a voxel Point.
function JazzResolveMedicinePatient(healer, target)
	if IsKindOf(target, "Unit") then
		return (IsValid(target) and not target:IsDead()) and target or false
	end
	if type(target) == "string" then
		local unit = g_Units and g_Units[target]
		if IsKindOf(unit, "Unit") and IsValid(unit) and not unit:IsDead() then
			return unit
		end
		return false
	end
	if not IsPoint(target) or not healer then
		return false
	end
	local occupant = GetOccupiedBy and GetOccupiedBy(target, healer)
	if IsKindOf(occupant, "Unit") and IsValid(occupant) and not occupant:IsDead()
		and not healer:IsOnEnemySide(occupant) then
		return occupant
	end
	local best, best_dist
	local max_dist = (const.SlabSizeX or guim) * 2
	local function consider(unit)
		if not IsKindOf(unit, "Unit") or not IsValid(unit) or unit:IsDead() then
			return
		end
		if healer:IsOnEnemySide(unit) then
			return
		end
		local dist = unit:GetDist(target)
		if dist <= max_dist and (not best or dist < best_dist) then
			best, best_dist = unit, dist
		end
	end
	consider(healer)
	for _, ally in ipairs(GetAllAlliedUnits(healer) or empty_table) do
		consider(ally)
	end
	return best or false
end

local function lHasSquadMedic(unit)
	local squad_id = unit and unit.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	for _, member_id in ipairs(squad and squad.units or empty_table) do
		local member = g_Units and g_Units[member_id]
		if member and (member.Medical or 0) >= 70 then
			return true
		end
	end
	return false
end

function JazzIsExpandingAmmo(ammo)
	if not ammo then
		return false
	end
	local class_id = tostring(ammo.class or ammo.id or "")
	if string.find(string.upper(class_id), "JHP", 1, true) then
		return true
	end
	if ammo.colorStyle == "AmmoJHPColor" then
		return true
	end
	for _, effect in ipairs(ammo.AppliedEffects or empty_table) do
		if effect == "BleedingHeavy" then
			return true
		end
	end
	return false
end

function JazzUnitBleedDamagePerTurn(unit)
	local total = 0
	for id, damage in pairs(JazzBleedDamage) do
		total = total + lBleedStacks(unit, id) * damage
	end
	return Min(30, total)
end

function JazzBleedDealTurnDamage(unit)
	if not unit or unit:HasStatusEffect("BeingBandaged") then
		return 0
	end
	local damage = JazzUnitBleedDamagePerTurn(unit)
	if damage <= 0 then
		return 0
	end
	local floating_text = T{193053798048, "<num> (bleeding)", num = damage}
	local visible = HasVisibilityTo(GetPoVTeam(), unit)
	local log_msg = T{890000000000971, "<name> takes <em><num></em> bleeding damage", name = unit:GetLogName(), num = damage}
	unit:TakeDirectDamage(damage, visible and floating_text or false, "short", log_msg)
	return damage
end

function JazzBleedTransitionRoll(unit)
	if not unit or unit:HasStatusEffect("BeingBandaged") then
		return false
	end
	local medic_bias = lHasSquadMedic(unit) and 10 or 0
	for _, id in ipairs(JazzBleedTierOrder) do
		local stacks = lBleedStacks(unit, id)
		for _ = 1, stacks do
			local roll = unit:Random(100)
			if id == "Bleeding" then
				if roll < 70 + medic_bias then
					unit:RemoveStatusEffect("Bleeding", 1)
				elseif roll >= 85 + medic_bias then
					unit:RemoveStatusEffect("Bleeding", 1)
					unit:AddStatusEffect("BleedingMedium")
				end
			elseif id == "BleedingMedium" then
				if roll < 35 + medic_bias then
					unit:RemoveStatusEffect("BleedingMedium", 1)
					unit:AddStatusEffect("Bleeding")
				elseif roll >= 80 + medic_bias then
					unit:RemoveStatusEffect("BleedingMedium", 1)
					unit:AddStatusEffect("BleedingHeavy")
				end
			elseif roll < 15 + medic_bias then
				unit:RemoveStatusEffect("BleedingHeavy", 1)
				unit:AddStatusEffect("BleedingMedium")
			end
		end
	end
	return true
end

function JazzReduceBleedOneTier(patient)
	if not patient or type(patient.GetStatusEffect) ~= "function" then
		return false
	end
	for _, id in ipairs(JazzBleedTierOrder) do
		if lBleedStacks(patient, id) > 0 then
			patient:RemoveStatusEffect(id, 1)
			if id == "BleedingHeavy" then
				patient:AddStatusEffect("BleedingMedium")
			elseif id == "BleedingMedium" then
				patient:AddStatusEffect("Bleeding")
			end
			return true
		end
	end
	return false
end

function JazzClearBleedStrong(patient, max_tiers_or_stacks)
	if not patient then
		return false
	end
	local remaining = max_tiers_or_stacks or 1
	local changed = false
	while remaining > 0 do
		local removed = false
		for _, id in ipairs(JazzBleedTierOrder) do
			if lBleedStacks(patient, id) > 0 then
				patient:RemoveStatusEffect(id, 1)
				removed = true
				changed = true
				break
			end
		end
		if not removed then
			break
		end
		remaining = remaining - 1
	end
	return changed
end

function JazzClearAllBleeding(patient)
	if not patient then
		return false
	end
	local changed = false
	for _, id in ipairs(JazzBleedTierOrder) do
		local stacks = lBleedStacks(patient, id)
		for _ = 1, stacks do
			patient:RemoveStatusEffect(id, 1)
			changed = true
		end
	end
	return changed
end

function JazzHasAnyBleed(unit)
	for _, id in ipairs(JazzBleedTierOrder) do
		if lBleedStacks(unit, id) > 0 then
			return true
		end
	end
	return false
end

-- Ally/self targeting for field bandage / kit bandage (all Jazz bleed tiers + HP debt).
function JazzUnitNeedsFieldOrKitBandage(unit)
	if not unit or unit:IsDead() then
		return false
	end
	if JazzHasAnyBleed(unit) then
		return true
	end
	if (unit.HitPoints or 0) < (unit.MaxHitPoints or 0) then
		return true
	end
	if unit.IsDowned and unit:IsDowned() then
		return true
	end
	if unit:HasStatusEffect("Unconscious") then
		return true
	end
	return false
end

-- Stack bandage action: only bleeding (any Jazz tier), not HP debt alone.
function JazzUnitNeedsFieldBandage(unit)
	return unit and not unit:IsDead() and JazzHasAnyBleed(unit)
end

function JazzUnitNeedsMorphine(unit)
	if not unit or unit:IsDead() then
		return false
	end
	if unit:HasStatusEffect("Pain") then
		return true
	end
	return JazzUnitNeedsMorphineRally(unit)
end

function JazzUnitNeedsMorphineRally(unit)
	if not unit or unit:IsDead() then
		return false
	end
	if unit.IsDowned and unit:IsDowned() then
		return true
	end
	return unit.command == "Downed"
		or unit.combat_behavior == "Downed"
		or unit:HasStatusEffect("Unconscious")
		or unit:HasStatusEffect("BleedingOut")
		or unit:HasStatusEffect("Downed")
end

-- Mirror vanilla GetBandageTargets, but with a custom need predicate + AP action id.
function JazzGetAllyMedicineTargets(unit, mode, range_mode, need_fn, action_id)
	if not unit or type(need_fn) ~= "function" then
		return (mode ~= "any") and {} or false
	end
	local targets = (mode ~= "any") and {}
	if need_fn(unit) then
		if mode == "any" then
			return unit
		end
		targets[1] = unit
	end
	local allies = GetAllAlliedUnits(unit)
	if unit.team and unit.team.player_team then
		allies = table.icopy(allies)
		for _, team in ipairs(g_Teams or empty_table) do
			if team.neutral then
				table.iappend(allies, team.units)
			end
		end
	end
	local action = action_id and CombatActions[action_id]
	local base_cost = action and action:GetAPCost(unit) or 0
	for _, ally in ipairs(allies) do
		if need_fn(ally) then
			local range_ok = range_mode == "ignore" or IsMeleeRangeTarget(unit, nil, nil, ally)
			if range_mode == "reachable" and base_cost and base_cost > 0 then
				if g_Combat then
					local pos = unit:GetClosestMeleeRangePos(ally)
					if pos then
						local path = GetCombatPath(unit)
						local ap = path and path:GetAP(pos)
						if ap then
							local cost = base_cost + Max(0, ap - (unit.free_move_ap or 0))
							range_ok = unit:HasAP(cost)
						else
							range_ok = false
						end
					else
						range_ok = false
					end
				else
					range_ok = true
				end
			end
			if range_ok then
				if mode == "any" then
					return ally
				end
				targets[#targets + 1] = ally
			end
		end
	end
	return targets
end

function JazzGetFieldBandageTargets(unit, mode, range_mode)
	return JazzGetAllyMedicineTargets(unit, mode, range_mode, JazzUnitNeedsFieldBandage, "JazzBandage")
end

function JazzGetMorphineTargets(unit, mode, range_mode)
	return JazzGetAllyMedicineTargets(unit, mode, range_mode, JazzUnitNeedsMorphine, "JazzMorphine")
end

-- Vanilla GetBandageTargets only checks status id "Bleeding" — miss Medium/Heavy.
-- Keep kit Bandage targeting consistent with Jazz bleed tiers.
JazzGetBandageTargets_Vanilla = rawget(_G, "JazzGetBandageTargets_Vanilla") or false
local jazz_get_bandage_targets_fn

local function lInstallBandageTargetsHook()
	local current = lG("GetBandageTargets")
	if type(current) ~= "function" or current == jazz_get_bandage_targets_fn then
		return
	end
	JazzGetBandageTargets_Vanilla = current
	jazz_get_bandage_targets_fn = function(unit, mode, range_mode)
		return JazzGetAllyMedicineTargets(unit, mode, range_mode, JazzUnitNeedsFieldOrKitBandage, "Bandage")
	end
	GetBandageTargets = jazz_get_bandage_targets_fn
end

-- Vanilla CombatActionAttackStart free-aim gate:
--   isFreeAimMode = isFreeAimMode and self.id ~= "Bandage"
-- JazzBandage / JazzMorphine use the same IModeCombatMelee UIBegin path but are
-- not excluded, so ally-only medicine pops «Free Aim / no enemies» confirmation.
-- RequireTargets skips that branch (same outcome as the Bandage id hardcode).
--
-- IMPORTANT: RequireTargets alone is not enough. IModeCombatMelee / Targeting_UnitInMelee
-- hardcode `action.id == "Bandage"` for ally bandage targeting; without that path
-- Jazz actions fall through to Unit:CanAttack (ActionType "Other" → always false) and
-- clicks on mercs do nothing. See lInstallMedicineMeleeUIHooks.
function JazzIsAllyMedicineCombatAction(action)
	local id = action and action.id
	return id == "Bandage" or id == "JazzBandage" or id == "JazzMorphine"
end

function JazzIsFieldMedicineActionId(id)
	return id == "JazzBandage" or id == "JazzMorphine"
end

-- While Targeting_UnitInMelee spoofs action.id to "Bandage", remember the real Jazz id
-- so CanBandageUI still validates against JazzBandage / JazzMorphine rules.
g_JAZZ_ActiveMedicineActionId = rawget(_G, "g_JAZZ_ActiveMedicineActionId") or false

JazzCombatActionAttackStart_Vanilla = rawget(_G, "JazzCombatActionAttackStart_Vanilla") or false
JazzCombatActionAttackStart_Wrapped = rawget(_G, "JazzCombatActionAttackStart_Wrapped") or false
JazzCanBandageUI_Vanilla = rawget(_G, "JazzCanBandageUI_Vanilla") or false
g_JAZZ_MedicineMeleeUIHooks = rawget(_G, "g_JAZZ_MedicineMeleeUIHooks") or false

local function lInstallCombatActionAttackStartMedHook()
	local current = lG("CombatActionAttackStart")
	if type(current) ~= "function" then
		return
	end
	if current == JazzCombatActionAttackStart_Wrapped then
		return
	end
	JazzCombatActionAttackStart_Vanilla = current
	local function jazz_CombatActionAttackStart(self, units, args, mode, noChangeAction)
		-- Bandage is already excluded by vanilla id hardcode; Jazz med actions need RequireTargets.
		if JazzIsAllyMedicineCombatAction(self) and self.id ~= "Bandage" and not self.RequireTargets then
			self.RequireTargets = true
		end
		return JazzCombatActionAttackStart_Vanilla(self, units, args, mode, noChangeAction)
	end
	JazzCombatActionAttackStart_Wrapped = jazz_CombatActionAttackStart
	CombatActionAttackStart = jazz_CombatActionAttackStart
end

function JazzGetActiveMedicineActionId()
	local marked = g_JAZZ_ActiveMedicineActionId
	if marked then
		return marked
	end
	local dlg = GetInGameInterfaceModeDlg and GetInGameInterfaceModeDlg()
	local action = dlg and dlg.action
	return action and action.id
end

local function lJazzMedicineUIRangeAndAP(attacker, target, action, args)
	local cost = action:GetAPCost(attacker, args) or 0
	local err = false
	if target ~= attacker and g_Combat then
		if not IsMeleeRangeTarget(attacker, nil, nil, target) then
			local pos = attacker:GetClosestMeleeRangePos(target)
			local cpath = GetCombatPath(attacker)
			local ap = cpath and cpath:GetAP(pos)
			if not ap then
				err = AttackDisableReasons.NoAP
			else
				cost = cost + Max(0, ap - (attacker.free_move_ap or 0))
			end
		end
	end
	if not err and g_Combat and cost >= 0 and attacker.UIHasAP and not attacker:UIHasAP(cost) then
		err = AttackDisableReasons.NoAP
	elseif not err and not g_Combat and cost >= 0 and attacker.UIHasAP and not attacker:UIHasAP(cost) then
		err = AttackDisableReasons.TooFar
	end
	return not err, err
end

function JazzCanFieldBandageUI(attacker, args)
	local target = args and args.target
	if not target then
		return false, AttackDisableReasons.NoTarget
	end
	if not target:IsPlayerAlly() and not (target.team and target.team.neutral) then
		return false, AttackDisableReasons.InvalidTarget
	end
	local action = CombatActions.JazzBandage
	if not action then
		return false, AttackDisableReasons.InvalidTarget
	end
	local state, reason = action:GetUIState({ attacker }, args)
	if state ~= "enabled" then
		return false, reason
	end
	local ok, err = lJazzMedicineUIRangeAndAP(attacker, target, action, args)
	if not ok then
		return false, err
	end
	if not JazzUnitNeedsFieldBandage(target) then
		return false, AttackDisableReasons.NoBandageTarget or AttackDisableReasons.FullHP
	end
	return true
end

function JazzCanMorphineUI(attacker, args)
	local target = args and args.target
	if not target then
		return false, AttackDisableReasons.NoTarget
	end
	if not target:IsPlayerAlly() and not (target.team and target.team.neutral) then
		return false, AttackDisableReasons.InvalidTarget
	end
	local action = CombatActions.JazzMorphine
	if not action then
		return false, AttackDisableReasons.InvalidTarget
	end
	local state, reason = action:GetUIState({ attacker }, args)
	if state ~= "enabled" then
		return false, reason
	end
	local ok, err = lJazzMedicineUIRangeAndAP(attacker, target, action, args)
	if not ok then
		return false, err
	end
	if not JazzUnitNeedsMorphine(target) then
		return false, AttackDisableReasons.NoBandageTarget or AttackDisableReasons.FullHP
	end
	return true
end

local jazz_targeting_melee_fn
local jazz_targeting_unit_in_melee_fn
local jazz_can_bandage_ui_fn
local jazz_melee_confirm_fn
local jazz_melee_confirm_base
local jazz_melee_set_target_fn
local jazz_melee_set_target_base
local jazz_start_move_attack_fn
local jazz_start_move_attack_base
local jazz_update_cursor_fn
local jazz_update_cursor_base

local function lSpoofMedicineTargeting(base_targeting, dialog, blackboard, command, pt)
	local action = dialog and dialog.action
	local real_id = action and action.id
	if JazzIsFieldMedicineActionId(real_id) then
		g_JAZZ_ActiveMedicineActionId = real_id
		action.id = "Bandage"
		local ok, a, b, c = pcall(base_targeting, dialog, blackboard, command, pt)
		action.id = real_id
		g_JAZZ_ActiveMedicineActionId = false
		if not ok then
			error(a)
		end
		return a, b, c
	end
	return base_targeting(dialog, blackboard, command, pt)
end

function JazzMedicineNeedsApproach(attacker, target)
	if not attacker or not IsValid(target) then
		return false
	end
	if target == attacker then
		return false
	end
	return not IsMeleeRangeTarget(attacker, nil, nil, target)
end

-- false = stay put (no goto_pos). Never return current slab: GetDist(visual, slab)
-- can exceed SlabSizeX/2 and StartMoveAndAttack still issues a one-tile Move.
function JazzResolveMedicineGotoPos(attacker, target)
	if not JazzMedicineNeedsApproach(attacker, target) then
		return false
	end
	return attacker:GetClosestMeleeRangePos(target)
end

local function lInstallMedicineMeleeUIHooks()
	-- CanBandageUI: dispatch Jazz field actions; kit Bandage also accepts all Jazz bleed tiers.
	local current_can = lG("CanBandageUI")
	if type(current_can) == "function" and current_can ~= jazz_can_bandage_ui_fn then
		JazzCanBandageUI_Vanilla = current_can
		jazz_can_bandage_ui_fn = function(attacker, args)
			local id = JazzGetActiveMedicineActionId()
			if id == "JazzBandage" then
				return JazzCanFieldBandageUI(attacker, args)
			end
			if id == "JazzMorphine" then
				return JazzCanMorphineUI(attacker, args)
			end
			local ok, err = JazzCanBandageUI_Vanilla(attacker, args)
			if not ok and (err == AttackDisableReasons.NoTarget or err == AttackDisableReasons.InvalidTarget) then
				return ok, err
			end
			local eligible_kit = JazzGetEquippedKitMedicine(attacker)
			if not eligible_kit then
				local blocked_kit = JazzGetBlockedKitMedicine(attacker)
				if blocked_kit then
					return false, JazzMedicineRequirementWarning(attacker, blocked_kit)
				end
			end
			if not ok and err == AttackDisableReasons.FullHP then
				local target = args and args.target
				-- Vanilla only checked status id "Bleeding"; Medium/Heavy looked like FullHP.
				if target and JazzUnitNeedsFieldOrKitBandage(target) then
					return true
				end
			end
			return ok, err
		end
		CanBandageUI = jazz_can_bandage_ui_fn
	end

	-- Spoof action.id → "Bandage" so bandaging=true visuals / click acceptance run.
	-- Prefer Targeting_Melee (AimType "melee" entry); also wrap UnitInMelee for direct calls.
	-- Real id kept in g_JAZZ_ActiveMedicineActionId for CanBandageUI dispatch.
	local current_melee = lG("Targeting_Melee")
	if type(current_melee) == "function" and current_melee ~= jazz_targeting_melee_fn then
		local base_melee = current_melee
		jazz_targeting_melee_fn = function(dialog, blackboard, command, pt)
			return lSpoofMedicineTargeting(base_melee, dialog, blackboard, command, pt)
		end
		Targeting_Melee = jazz_targeting_melee_fn
	end
	local current_targeting = lG("Targeting_UnitInMelee")
	if type(current_targeting) == "function" and current_targeting ~= jazz_targeting_unit_in_melee_fn then
		local base_targeting = current_targeting
		jazz_targeting_unit_in_melee_fn = function(dialog, blackboard, command, pt)
			return lSpoofMedicineTargeting(base_targeting, dialog, blackboard, command, pt)
		end
		Targeting_UnitInMelee = jazz_targeting_unit_in_melee_fn
	end

	local classes = lG("g_Classes")

	-- Healing cursor: vanilla compares action object identity to CombatActions.Bandage only.
	local common_cls = classes and classes.IModeCommonUnitControl
	if type(common_cls) == "table" and type(common_cls.UpdateCursorImage) == "function"
		and common_cls.UpdateCursorImage ~= jazz_update_cursor_fn
	then
		jazz_update_cursor_base = common_cls.UpdateCursorImage
		jazz_update_cursor_fn = function(self, ...)
			if JazzIsAllyMedicineCombatAction(self.action) then
				if GetUIStyleGamepad and GetUIStyleGamepad() then
					return
				end
				if self.potential_target and CanBandageUI(SelectedObj, { target = self.potential_target }) then
					self.desktop:SetMouseCursor("UI/Cursors/Healing_on.tga")
				else
					self.desktop:SetMouseCursor("UI/Cursors/Healing_off.tga")
				end
				return
			end
			return jazz_update_cursor_base(self, ...)
		end
		common_cls.UpdateCursorImage = jazz_update_cursor_fn
	end

	-- Portrait always StartMoveAndAttack(GetClosestMeleeRangePos). Even "stay on current slab"
	-- still Moves when visual pos is > half-slab from GetPassSlab. Skip the move thread entirely.
	local base_mode_cls = classes and classes.IModeCombatBase
	if type(base_mode_cls) == "table" and type(base_mode_cls.StartMoveAndAttack) == "function"
		and base_mode_cls.StartMoveAndAttack ~= jazz_start_move_attack_fn
	then
		jazz_start_move_attack_base = base_mode_cls.StartMoveAndAttack
		jazz_start_move_attack_fn = function(self, attacker, action, target, step_pos, args)
			if JazzIsAllyMedicineCombatAction(action) and attacker and IsValid(target) then
				if not JazzMedicineNeedsApproach(attacker, target) then
					if attacker.move_attack_in_progress then
						return
					end
					args = args or {}
					args.target = target
					args.goto_pos = nil
					self.attack_confirmed = true
					if ClearAPIndicator then
						ClearAPIndicator()
					end
					action:Execute({ attacker }, args)
					return
				end
				step_pos = step_pos or attacker:GetClosestMeleeRangePos(target)
			end
			return jazz_start_move_attack_base(self, attacker, action, target, step_pos, args)
		end
		base_mode_cls.StartMoveAndAttack = jazz_start_move_attack_fn
	end

	local melee_cls = classes and classes.IModeCombatMelee

	-- SetTarget CanAttack eject: ActionType "Other" always fails → kicks out of mode on world hover.
	if type(melee_cls) == "table" and type(melee_cls.SetTarget) == "function"
		and melee_cls.SetTarget ~= jazz_melee_set_target_fn
	then
		jazz_melee_set_target_base = melee_cls.SetTarget
		jazz_melee_set_target_fn = function(self, ...)
			if JazzIsAllyMedicineCombatAction(self.action) then
				return IModeCombatBase.SetTarget(self, ...)
			end
			return jazz_melee_set_target_base(self, ...)
		end
		melee_cls.SetTarget = jazz_melee_set_target_fn
	end

	-- Confirm: do not spoof id (would fire kit Bandage). Skip CheckAndReportImpossibleAttack
	-- (CanAttack always false for ActionType Other) — validate via CanBandageUI then Execute/move.
	if type(melee_cls) == "table" and type(melee_cls.Confirm) == "function"
		and melee_cls.Confirm ~= jazz_melee_confirm_fn
	then
		jazz_melee_confirm_base = melee_cls.Confirm
		jazz_melee_confirm_fn = function(self, ...)
			local action = self.action
			local real_id = action and action.id
			if not JazzIsFieldMedicineActionId(real_id) then
				return jazz_melee_confirm_base(self, ...)
			end
			if self.crosshair then
				return jazz_melee_confirm_base(self, ...)
			end
			local attacker = SelectedObj or self.attacker
			local target = self.target
			if not IsValid(attacker) or not IsValid(target) then
				return
			end
			g_JAZZ_ActiveMedicineActionId = real_id
			local ok_check = CheckCanBeBandagedAndReport(attacker, { target = target })
			g_JAZZ_ActiveMedicineActionId = false
			if not ok_check then
				return
			end
			local goto_pos = JazzResolveMedicineGotoPos(attacker, target)
			local args = { target = target }
			if goto_pos then
				args.goto_pos = goto_pos
			end
			self.attack_confirmed = true
			if ClearAPIndicator then
				ClearAPIndicator()
			end
			if goto_pos then
				self:StartMoveAndAttack(attacker, action, target, goto_pos, args)
			else
				action:Execute({ attacker }, args)
			end
			return "break"
		end
		melee_cls.Confirm = jazz_melee_confirm_fn
	end

	g_JAZZ_MedicineMeleeUIHooks = true
end

function JazzTryRollBleedFromHit(target, hit, attacker)
	if not target or not hit or hit.setpiece then
		return false
	end
	local armor_hit = hit.armor_decay and next(hit.armor_decay) ~= nil
	local pierced = not armor_hit or hit.armor_pen and next(hit.armor_pen) ~= nil
	if not pierced then
		return false
	end
	local trauma_bias = JazzHasAnyTrauma(target) and 15 or 0
	local roll = target:Random(100)
	if roll < 10 + trauma_bias then
		target:AddStatusEffect("BleedingMedium")
		return true
	elseif roll < 55 + trauma_bias then
		target:AddStatusEffect("Bleeding")
		return true
	end
	return false
end

-- Grazing / scratch: low chance of light bleed only (no Medium/Heavy, no trauma / BAT / *shot).
JazzGrazeLightBleedChance = 15

function JazzTryRollBleedFromGraze(target, hit, attacker)
	if not target or not hit or hit.setpiece then
		return false
	end
	if target:Random(100) >= (JazzGrazeLightBleedChance or 15) then
		return false
	end
	target:AddStatusEffect("Bleeding")
	return true
end

-- TargetBodyPart → trauma zone for behind-armor blunt.
function JazzHitBodyPartToTraumaZone(part)
	if part == "Arms" then
		return "Arms"
	elseif part == "Legs" then
		return "Legs"
	elseif part == "Head" or part == "Neck" then
		return "Head"
	elseif part == "Torso" or part == "Groin" then
		return "Ribs"
	end
	return false
end

-- Behind-armor trauma (BAT): armor stopped the round (armor_decay, no armor_pen).
-- No bleeding / no *shot effects; chance of Light (rarely Medium) trauma + Pain.
-- Chance scales with impact energy (armor_prevented + residual damage).
function JazzTryBehindArmorTrauma(unit, hit, attacker)
	if not unit or not hit or hit.setpiece then
		return false
	end
	local armor_hit = hit.armor_decay and next(hit.armor_decay) ~= nil
	if not armor_hit then
		return false
	end
	if hit.armor_pen and next(hit.armor_pen) ~= nil then
		return false
	end
	local zone = JazzHitBodyPartToTraumaZone(hit.spot_group or hit.target_spot_group or g_DefaultShotBodyPart)
	if not zone then
		return false
	end
	local prevented = hit.armor_prevented or 0
	local residual = hit.damage or 0
	local energy = prevented + residual
	if energy < 8 then
		return false
	end
	-- ~15% + energy/2, cap 65%. Soft hits often glance; heavy impacts often bruise.
	local chance = Min(65, 15 + DivRound(energy, 2))
	if unit:Random(100) >= chance then
		return false
	end
	local tier = "Light"
	if zone == "Head" and energy >= 35 and unit:Random(100) < 30 then
		tier = "Medium"
	elseif energy >= 50 and unit:Random(100) < 18 then
		tier = "Medium"
	end
	JazzApplyTrauma(unit, zone, tier)
	-- Pain: damaging hits already get +1 via JazzPainOnDamagingHit. Full absorb (0 HP)
	-- still needs a stack here so BAT without residual damage is not painless.
	if residual <= 0 then
		JazzAddPainStacks(unit, 1)
	end
	Msg("JAZZ_BehindArmorTrauma", unit, zone, tier, hit, attacker)
	return true
end

-- Damaging blast (aoeType none): guaranteed concussion + trauma chance.
-- Smoke/tear/toxic/fire skip. Flashbang (0 dmg, aoe none) still gets concussion.
-- Blast statuses ignore ballistic pierce. TempHitPoints still blocks this package.
function JazzIsBlastExplosiveHit(hit)
	if not hit or not hit.explosion or hit.grazing then
		return false
	end
	local aoe = hit.aoe_type
	if aoe == nil or aoe == false or aoe == "" then
		local w = hit.weapon
		if w and w.aoeType then
			aoe = w.aoeType
		end
	end
	aoe = aoe or "none"
	-- Only pure blast (frag/HE/flashbang/demo). Smoke/tear/toxic/fire use other packages.
	return aoe == "none"
end

function JazzTryApplyExplosionConcussionAndTrauma(unit, hit, attacker)
	if not unit or not JazzIsBlastExplosiveHit(hit) then
		return false
	end
	if (unit.TempHitPoints or 0) > 0 then
		return false
	end
	local center = hit.explosion_center
	local trauma_gate = center and 100 or 40 -- center always attempts *shot-style trauma roll

	local applied_conc = false
	if CharacterEffectDefs and CharacterEffectDefs.Concussion then
		unit:AddStatusEffect("Concussion")
		applied_conc = true
	end

	local applied_trauma = false
	-- When CenterAppliedEffects already listed *shot and pierce bypass applied them,
	-- skip a second trauma roll to avoid stacking three body-part rollers + this gate.
	local effects = hit.effects
	local has_shot_roller = false
	if type(effects) == "table" then
		for _, effect in ipairs(effects) do
			if effect == "Headshot" or effect == "Armsshot" or effect == "Legsshot"
				or effect == "Torsoshot" or effect == "Groinshot" then
				has_shot_roller = true
				break
			end
		end
	elseif effects == "Headshot" or effects == "Armsshot" or effects == "Legsshot"
		or effects == "Torsoshot" or effects == "Groinshot" then
		has_shot_roller = true
	end
	if not has_shot_roller and unit:Random(100) < trauma_gate then
		local zones = { "Arms", "Legs", "Ribs", "Head" }
		local zone
		if center and unit:Random(100) < 40 then
			zone = "Head"
		elseif center and unit:Random(100) < 50 then
			zone = "Ribs"
		else
			zone = zones[1 + unit:Random(#zones)]
		end
		applied_trauma = JazzTryRollTraumaFromBodyPart(unit, zone) and true or false
	end

	if applied_conc or applied_trauma then
		Msg("JAZZ_ExplosionConcussionTrauma", unit, hit, attacker, applied_conc, applied_trauma)
	end
	return applied_conc or applied_trauma
end

function JazzRemapHitBleedEffect(effect, hit, attacker)
	if effect ~= "Bleeding" then
		return effect
	end
	local weapon = hit and hit.weapon
	local ammo = weapon and weapon.ammo
	return JazzIsExpandingAmmo(ammo) and "BleedingHeavy" or effect
end

function JazzFindInventoryItem(unit, class_id)
	local result
	if unit then
		unit:ForEachItem(function(item)
			if not result and (item.class == class_id or item.id == class_id) then
				result = item
			end
		end)
	end
	return result
end

function JazzConsumeInventoryItem(unit, class_id, amount)
	local item = JazzFindInventoryItem(unit, class_id)
	if not item then
		return false
	end
	amount = amount or 1
	if IsKindOf(item, "InventoryStack") and (item.Amount or 0) > amount then
		item.Amount = item.Amount - amount
	else
		local slot = unit:GetItemSlot(item)
		if slot then
			unit:RemoveItem(slot, item)
		end
		DoneObject(item)
	end
	Msg("InventoryChange", unit)
	return true
end

function GetUnitEquippedMedicine(unit)
	return JazzGetEquippedKitMedicine(unit)
end

function JazzGetBandageItem(unit)
	return JazzFindInventoryItem(unit, "JAZZ_Bandage")
end

function JazzGetMorphineItem(unit)
	return JazzFindInventoryItem(unit, "JAZZ_Morphine")
end

-- IFAK / Medkit / Reanimationsset for the Bandage combat action (not field bandage stacks).
function JazzGetEquippedKitMedicine(unit)
	if not unit then
		return false
	end
	local result
	unit:ForEachItem(function(item)
		if JazzMedicineIsKitClass(item.class)
			and JazzMedicineIsUsable(item)
			and JazzMedicineMeetsRequirement(unit, item)
			and (not result or (result.UsePriority or 0) < (item.UsePriority or 0))
		then
			result = item
		end
	end)
	return result
end

function JazzGetBlockedKitMedicine(unit)
	if not unit then
		return false
	end
	local result
	local result_requirement
	unit:ForEachItem(function(item)
		local required = JazzMedicineRequiredMedical(item)
		if JazzMedicineIsKitClass(item.class)
			and JazzMedicineIsUsable(item)
			and required > 0
			and not JazzMedicineMeetsRequirement(unit, item)
			and (not result_requirement or required < result_requirement)
		then
			result = item
			result_requirement = required
		end
	end)
	return result
end

function JazzApplyBandageAction(healer, patient)
	patient = JazzResolveMedicinePatient(healer, patient)
	if not healer or not patient or not JazzGetBandageItem(healer) then
		return false
	end
	if not JazzReduceBleedOneTier(patient) then
		return false
	end
	JazzConsumeInventoryItem(healer, "JAZZ_Bandage", 1)
	Msg("OnBandaged", healer, patient, 0)
	return true
end

function JazzRefundPainStartTurnAP(unit)
	local combat = rawget(_G, "g_Combat")
	if not combat or not unit or type(unit.GetStatusEffect) ~= "function" then
		return 0
	end
	local pain = unit:GetStatusEffect("Pain")
	if not pain or type(pain.ResolveValue) ~= "function" or type(pain.SetParameter) ~= "function" then
		return 0
	end
	local refund = Max(0, tonumber(pain:ResolveValue("jazz_ap_penalty_applied")) or 0)
	local penalty_turn = tonumber(pain:ResolveValue("jazz_ap_penalty_turn")) or -1
	pain:SetParameter("jazz_ap_penalty_applied", 0)
	pain:SetParameter("jazz_ap_penalty_turn", -1)
	if refund <= 0 or penalty_turn ~= combat.current_turn or type(unit.ActionPoints) ~= "number" then
		return 0
	end
	unit.ActionPoints = Max(0, unit.ActionPoints + refund)
	Msg("UnitAPChanged", unit)
	ObjModified(unit)
	return refund
end

function JazzApplyMorphineAction(healer, patient)
	patient = JazzResolveMedicinePatient(healer, patient)
	if not healer or not patient or not JazzGetMorphineItem(healer) then
		return false
	end
	if type(patient.AddStatusEffect) ~= "function" then
		return false
	end
	patient:AddStatusEffect("Analgesia")
	JazzConsumeInventoryItem(healer, "JAZZ_Morphine", 1)
	-- Vanilla DownedRally with no medic/medicine — get-up only, no Condition math on stacks.
	if JazzUnitNeedsMorphineRally(patient) and patient.SetCommand then
		patient:SetCommand("DownedRally")
	end
	Msg("JAZZ_MorphineApplied", healer, patient)
	return true
end

-- Called from Bleeding* CharacterEffect OnEndTurn (deduped per unit/turn).
function JazzBleedOnUnitEndTurn(unit)
	if not unit or not JazzHasAnyBleed(unit) then
		return
	end
	local key = (g_Combat and g_Combat.current_turn) or (GameTime and GameTime()) or 0
	if unit.jazz_bleed_tick_key == key then
		return
	end
	unit.jazz_bleed_tick_key = key
	JazzBleedDealTurnDamage(unit)
	JazzBleedTransitionRoll(unit)
end

-- ---------------------------------------------------------------------------
-- Zonal traumas (MED-001 expanded). Eye folded into Head for v1.
-- ---------------------------------------------------------------------------
JazzTraumaZones = { "Arms", "Legs", "Ribs", "Head", "Burn" }
JazzTraumaTiers = { "Light", "Medium", "Heavy" }
JazzTraumaTierRank = { Light = 1, Medium = 2, Heavy = 3 }

local function lTraumaId(zone, tier)
	return "Trauma" .. zone .. tier
end

function JazzTraumaEffectId(zone, tier)
	return lTraumaId(zone, tier)
end

function JazzGetTraumaTier(unit, zone)
	if not unit or not zone then
		return false
	end
	for _, tier in ipairs(JazzTraumaTiers) do
		if unit:HasStatusEffect(lTraumaId(zone, tier)) then
			return tier
		end
	end
	return false
end

function JazzHasAnyTrauma(unit)
	if not unit then
		return false
	end
	for _, zone in ipairs(JazzTraumaZones) do
		if JazzGetTraumaTier(unit, zone) then
			return true
		end
	end
	return false
end

function JazzClearZoneTrauma(unit, zone)
	if not unit or not zone then
		return false
	end
	local changed = false
	for _, tier in ipairs(JazzTraumaTiers) do
		local id = lTraumaId(zone, tier)
		if unit:HasStatusEffect(id) then
			unit:RemoveStatusEffect(id, "all")
			changed = true
		end
	end
	return changed
end

-- Apply or upgrade trauma for a zone. Never downgrades.
local lJazzPhysicalTraumaZones = { "Arms", "Legs", "Ribs", "Head" }

function JazzApplyTrauma(unit, zone, tier)
	if not unit or not zone or not tier or not JazzTraumaTierRank[tier] then
		return false
	end
	-- UnitDowned guarantees one Heavy physical trauma. A later *shot effect from
	-- the same hit must not leave an extra Light/Medium trauma beside it.
	if tier ~= "Heavy" and unit.HasStatusEffect and unit:HasStatusEffect("Downed") then
		for _, physical_zone in ipairs(lJazzPhysicalTraumaZones) do
			if JazzGetTraumaTier(unit, physical_zone) == "Heavy" then
				return false
			end
		end
		tier = "Heavy"
	end
	local current = JazzGetTraumaTier(unit, zone)
	if current and JazzTraumaTierRank[current] >= JazzTraumaTierRank[tier] then
		return false
	end
	JazzClearZoneTrauma(unit, zone)
	local id = lTraumaId(zone, tier)
	unit:AddStatusEffect(id)
	local effect = unit:GetStatusEffect(id)
	if effect then
		JazzInitTraumaProgressTimer(effect, zone, tier)
	end
	Msg("JAZZ_TraumaApplied", unit, zone, tier)
	return true
end

-- Trauma zone → TargetBodyPart keys that armor may cover.
function JazzTraumaZoneBodyParts(zone)
	if zone == "Arms" then
		return { "Arms" }
	elseif zone == "Legs" then
		return { "Legs" }
	elseif zone == "Ribs" then
		-- Torsoshot + Groinshot both roll Ribs trauma.
		return { "Torso", "Groin" }
	elseif zone == "Head" then
		return { "Head", "Neck" }
	end
	return empty_table
end

-- Chance factor for trauma thresholds: 100 = full chance, lower = armor softens.
-- Unpierced armor already blocks *shot effects; this softens pierced / residual hits
-- when worn armor still lists ProtectedBodyParts for that zone.
-- Best covering piece: mitigation ~= Coverage × Condition%, max ~60% chance cut (floor 40%).
function JazzGetTraumaArmorChanceFactor(unit, zone)
	if not unit or not zone or zone == "Burn" then
		return 100
	end
	local parts = JazzTraumaZoneBodyParts(zone)
	if not next(parts) then
		return 100
	end
	local best = 0
	unit:ForEachItem("Armor", function(item, slot)
		if slot == "Inventory" or (item.Condition or 0) <= 0 then
			return
		end
		local protected = item.ProtectedBodyParts
		if not protected then
			return
		end
		local covers = false
		for _, part in ipairs(parts) do
			if protected[part] then
				covers = true
				break
			end
		end
		if not covers then
			return
		end
		local cov = item.Coverage or 80
		local cond = item.GetConditionPercent and item:GetConditionPercent() or (item.Condition or 100)
		local score = MulDivRound(cov, cond, 100)
		if score > best then
			best = score
		end
	end)
	if best <= 0 then
		return 100
	end
	local reduction = MulDivRound(best, 60, 100)
	return Max(40, 100 - reduction)
end

-- Body-part *shot rollers → trauma. Grit (Temp HP) still blocks like legacy *shot.
-- Fixed d100 base (not Random(HP)): low HP no longer collapses almost all rolls into Medium+.
-- Limbs favor Light; Head still biased toward Medium/Heavy.
-- Armor covering the zone scales thresholds down (JazzGetTraumaArmorChanceFactor).
function JazzTryRollTraumaFromBodyPart(unit, zone)
	if not unit or not zone or (unit.TempHitPoints or 0) > 0 then
		return false
	end
	local factor = JazzGetTraumaArmorChanceFactor(unit, zone)
	local thr_heavy, thr_medium, thr_light
	if zone == "Head" then
		-- Head: Light harder; Medium/Heavy more common than limbs.
		thr_heavy, thr_medium, thr_light = 15, 45, 65
	else
		-- Limbs/Ribs/Burn: all three tiers remain visible in ordinary combat.
		thr_heavy, thr_medium, thr_light = 8, 28, 60
	end
	if factor < 100 then
		thr_heavy = Max(1, MulDivRound(thr_heavy, factor, 100))
		thr_medium = Max(thr_heavy + 1, MulDivRound(thr_medium, factor, 100))
		thr_light = Max(thr_medium + 1, MulDivRound(thr_light, factor, 100))
	end
	local roll = unit:Random(100)
	local tier
	if roll < thr_heavy then
		tier = "Heavy"
	elseif roll < thr_medium then
		tier = "Medium"
	elseif roll < thr_light then
		tier = "Light"
	end
	if not tier then
		return false
	end
	return JazzApplyTrauma(unit, zone, tier)
end

-- Knockout / Unconscious: one heavy trauma + Pain spike (not Wounded stacks).
function JazzStripCombatWounded(unit)
	if unit and unit.HasStatusEffect and unit:HasStatusEffect("Wounded") then
		unit:RemoveStatusEffect("Wounded", "all")
	end
end

function JazzApplyDownedHeavyTrauma(unit)
	if not unit then
		return false
	end
	-- MED-001: never leave HP-stack Wounded on downed/knockout; one Heavy
	-- physical trauma replaces it immediately and only once.
	JazzStripCombatWounded(unit)
	for _, zone in ipairs(lJazzPhysicalTraumaZones) do
		if JazzGetTraumaTier(unit, zone) == "Heavy" then
			return false
		end
	end

	local zone
	local hit = unit.on_die_hit_descr
	if hit then
		local hit_zone = JazzHitBodyPartToTraumaZone(
			hit.spot_group or hit.target_spot_group or g_DefaultShotBodyPart
		)
		if table.find(lJazzPhysicalTraumaZones, hit_zone) then
			zone = hit_zone
		end
	end
	if not zone then
		for _, physical_zone in ipairs(lJazzPhysicalTraumaZones) do
			if JazzGetTraumaTier(unit, physical_zone) then
				zone = physical_zone
				break
			end
		end
	end
	zone = zone or lJazzPhysicalTraumaZones[1 + unit:Random(#lJazzPhysicalTraumaZones)]
	if not JazzApplyTrauma(unit, zone, "Heavy") then
		return false
	end
	for _ = 1, 3 do
		unit:AddStatusEffect("Pain")
	end
	return true
end

function JazzApplyKnockoutTraumaPackage(unit)
	return JazzApplyDownedHeavyTrauma(unit)
end

-- Pain stacks added when an injured zone is used (deduped per unit/zone/turn).
-- Light 1 / Medium 2 / Heavy 3. Heavy zones that stay unused still get +1 via JazzTraumaHeavyPainRamp.
-- Separate source: solid damaging hits add +1 via JazzPainOnDamagingHit (not graze; not zone-use).
JazzTraumaPainStacksOnZoneUse = { Light = 1, Medium = 2, Heavy = 3 }

-- +1 Pain when a solid (non-graze) hit deals HP damage. Cap via JazzAddPainStacks / Pain.max_stacks.
-- Graze excluded (scratch package: HP + rare light bleed only). Zone-use / heavy ramp stay separate.
function JazzPainOnDamagingHit(unit, hit, damage)
	if not unit or not hit or hit.setpiece then
		return 0
	end
	if hit.grazing then
		return 0
	end
	damage = tonumber(damage) or 0
	if damage <= 0 then
		return 0
	end
	return JazzAddPainStacks(unit, 1)
end

function JazzAddPainStacks(unit, amount)
	if not unit or type(unit.AddStatusEffect) ~= "function" then
		return 0
	end
	amount = tonumber(amount) or 0
	if amount <= 0 then
		return 0
	end
	local pain = unit.GetStatusEffect and unit:GetStatusEffect("Pain")
	local stacks = pain and pain.stacks or 0
	local max_stacks = (CharacterEffectDefs.Pain and CharacterEffectDefs.Pain.max_stacks) or 8
	local added = 0
	for _ = 1, amount do
		if stacks + added >= max_stacks then
			break
		end
		unit:AddStatusEffect("Pain")
		added = added + 1
	end
	return added
end

function JazzTraumaPainZoneTurnKey(zone, turn)
	return tostring(zone) .. "|" .. tostring(turn or 0)
end

function JazzTraumaCurrentTurnKey()
	return (g_Combat and g_Combat.current_turn) or (GameTime and GameTime()) or 0
end

function JazzTraumaPainOnZoneUse(unit, zone)
	if not unit or not zone then
		return false
	end
	local tier = JazzGetTraumaTier(unit, zone)
	if not tier then
		return false
	end
	local turn = JazzTraumaCurrentTurnKey()
	local key = JazzTraumaPainZoneTurnKey(zone, turn)
	unit.jazz_trauma_pain_keys = unit.jazz_trauma_pain_keys or {}
	if unit.jazz_trauma_pain_keys[key] then
		return false
	end
	unit.jazz_trauma_pain_keys[key] = true
	local stacks = JazzTraumaPainStacksOnZoneUse[tier] or 1
	return JazzAddPainStacks(unit, stacks) > 0
end

-- Heavy traumas: +1 Pain each EndTurn for every heavy zone that was not used this turn.
function JazzTraumaHeavyPainRamp(unit)
	if not unit then
		return
	end
	local turn = JazzTraumaCurrentTurnKey()
	if unit.jazz_trauma_heavy_pain_key == turn then
		return
	end
	unit.jazz_trauma_pain_keys = unit.jazz_trauma_pain_keys or {}
	local unused = 0
	for _, zone in ipairs(JazzTraumaZones) do
		if JazzGetTraumaTier(unit, zone) == "Heavy" then
			local zkey = JazzTraumaPainZoneTurnKey(zone, turn)
			if not unit.jazz_trauma_pain_keys[zkey] then
				unused = unused + 1
			end
		end
	end
	if unused <= 0 then
		return
	end
	unit.jazz_trauma_heavy_pain_key = turn
	JazzAddPainStacks(unit, unused)
end

function JazzTraumaBlockFreeMove(unit)
	return unit and (
		JazzGetTraumaTier(unit, "Legs") == "Medium"
		or JazzGetTraumaTier(unit, "Legs") == "Heavy"
		or JazzGetTraumaTier(unit, "Ribs") == "Medium"
		or JazzGetTraumaTier(unit, "Ribs") == "Heavy"
	)
end

-- After Burning expires: leave a lasting light burn trauma (debt).
function JazzApplyBurnTraumaFromBurning(unit)
	if not unit then
		return false
	end
	return JazzApplyTrauma(unit, "Burn", "Light")
end

-- ---------------------------------------------------------------------------
-- Trauma progress timers (satellite hours): improve / worsen checks + UI text.
-- Tooltip append lives on JazzTraumaEffect:ResolveValue("Description") (System_JazzTraumaEffect.lua).
-- GetDescription stays raw — save path uses it and cannot serialize T{hours=...}.
-- ---------------------------------------------------------------------------

function JazzParseTraumaEffectId(effect_id)
	if type(effect_id) ~= "string" or not string.find(effect_id, "^Trauma", 1, true) then
		return false, false
	end
	local rest = string.sub(effect_id, 7)
	for _, tier in ipairs(JazzTraumaTiers) do
		local suffix = tier
		if string.sub(rest, -#suffix) == suffix then
			local zone = string.sub(rest, 1, #rest - #suffix)
			if zone ~= "" then
				return zone, tier
			end
		end
	end
	return false, false
end

function JazzTraumaCheckIntervalHours(zone, tier)
	if zone == "Burn" then
		if tier == "Light" then
			return 12
		elseif tier == "Medium" then
			return 36
		end
		return 72
	end
	if tier == "Light" then
		return 8
	elseif tier == "Medium" then
		return 24
	end
	return 48
end

-- Field TreatWounds / OperationHeal marks Trauma* as healing (parameter jazz_healing=1).
-- Healing: worsen 0, improve 100% each check (guaranteed tier step-down over time),
-- check interval halved (floor 2h). HealWounds effect does NOT set this.
function JazzTraumaIsHealing(effect)
	return effect and (effect:ResolveValue("jazz_healing") or 0) ~= 0
end

function JazzSetTraumaHealing(effect, healing)
	if not effect then
		return false
	end
	effect:SetParameter("jazz_healing", healing and 1 or 0)
	return true
end

function JazzMarkUnitTraumasHealing(unit)
	if not unit then
		return false
	end
	local any = false
	for _, zone in ipairs(JazzTraumaZones) do
		local tier = JazzGetTraumaTier(unit, zone)
		if tier then
			local effect = unit:GetStatusEffect(lTraumaId(zone, tier))
			if effect then
				JazzSetTraumaHealing(effect, true)
				JazzInitTraumaProgressTimer(effect, zone, tier)
				any = true
			end
		end
	end
	return any
end

-- Chance table: roll 1..100 → improve / worsen / stay.
-- healing=true (after OperationHeal): worsen blocked; improve guaranteed (100).
-- Successful improve still uses JazzDowngradeTrauma (Light clear / Medium→Light / Heavy→Medium).
function JazzTraumaProgressChances(zone, tier, healing)
	if healing then
		return 100, 0
	end
	local improve, worsen
	if tier == "Light" then
		improve, worsen = 55, 10
	elseif tier == "Medium" then
		improve, worsen = 20, 25
	else
		-- Heavy: rarely improves untreated; no worsen (infection deferred).
		improve, worsen = 8, 0
	end
	return improve, worsen
end

-- ---------------------------------------------------------------------------
-- Satellite HP regen: vanilla UnitData:Tick adds NaturalHealPerTick /
-- PatientHealPerTick every Satellite.Tick (15 min) → Natural 4 HP/h, Patient 20 HP/h.
-- JAZZ reinterprets those ConstDef values as HP per campaign hour via accumulator
-- (same numbers → Natural ~1 HP/h, Patient ~5 HP/h; R&R still × RandRActivityHealingMultiplier).
-- ---------------------------------------------------------------------------
local function lJazzSatelliteHealHpThisTick(unit, rate_per_hour)
	rate_per_hour = rate_per_hour or 0
	if rate_per_hour <= 0 then
		return 0
	end
	local scale_h = (const.Scale and const.Scale.h) or 3600
	local tick = (const.Satellite and const.Satellite.Tick) or scale_h
	-- Accumulate thousandths of an HP so Patient 5/h yields steady steps on 15-min ticks.
	local progress = (unit.jazz_sat_hp_heal_progress or 0) + MulDivRound(rate_per_hour * 1000, tick, scale_h)
	local whole = progress / 1000
	whole = whole - whole % 1
	if whole < 1 then
		unit.jazz_sat_hp_heal_progress = progress
		return 0
	end
	unit.jazz_sat_hp_heal_progress = progress - whole * 1000
	return whole
end

function UnitData:Tick()
	if self.HiredUntil and Game.CampaignTime + const.Scale.h * 60 > self.HiredUntil then
		TutorialHintsState.ContractExpireHint = true
	end

	if self.HiredUntil and Game.CampaignTime >= self.HiredUntil then
		MercContractExpired(self)
	end

	-- heal player mercs; heal militia/enemy when not traveling
	if IsMerc(self) or self.Operation ~= "Traveling" then
		local rate = IsPatient(self) and const.Satellite.PatientHealPerTick or const.Satellite.NaturalHealPerTick
		if self.Operation == "RAndR" then
			rate = const.Satellite.RandRActivityHealingMultiplier * rate
		end
		local add = lJazzSatelliteHealHpThisTick(self, rate)
		if add > 0 then
			local old_hp = self.HitPoints
			self.HitPoints = Min(self.HitPoints + add, self.MaxHitPoints)
			local healed = self.HitPoints - old_hp
			if healed > 0 then
				self:OnHeal(healed)
			end
		end
	end
	Msg("UnitDataTick", self)
end

function JazzInitTraumaProgressTimer(effect, zone, tier)
	if not effect or not Game or not Game.CampaignTime then
		return false
	end
	if not zone or not tier then
		zone, tier = JazzParseTraumaEffectId(effect.class)
	end
	if not zone or not tier then
		return false
	end
	local hours = JazzTraumaCheckIntervalHours(zone, tier)
	if JazzTraumaIsHealing(effect) then
		hours = Max(2, DivRound(hours, 2))
	end
	local scale_h = (const.Scale and const.Scale.h) or 1
	effect:SetParameter("next_check_time", Game.CampaignTime + hours * scale_h)
	effect:SetParameter("check_interval_h", hours)
	return true
end

function JazzTraumaHoursUntilNextCheck(effect)
	if not effect or not Game or not Game.CampaignTime then
		return false
	end
	local next_t = effect:ResolveValue("next_check_time")
	if not next_t or next_t == 0 then
		local zone, tier = JazzParseTraumaEffectId(effect.class)
		JazzInitTraumaProgressTimer(effect, zone, tier)
		next_t = effect:ResolveValue("next_check_time")
	end
	if not next_t then
		return false
	end
	local scale_h = (const.Scale and const.Scale.h) or 1
	return Max(0, DivRound(next_t - Game.CampaignTime, scale_h))
end

function JazzFormatTraumaStatusDescription(effect, base_desc)
	local zone, tier = JazzParseTraumaEffectId(effect and effect.class)
	local hours = JazzTraumaHoursUntilNextCheck(effect)
	local healing = JazzTraumaIsHealing(effect)
	local timing
	if hours == false then
		timing = T(890000000010203, "Next progress check: pending.")
	elseif healing then
		if hours <= 0 then
			timing = T(890000000010198, "Next progress check: <em>due now</em> (healing — will improve).")
		else
			timing = T{890000000010199, "Next progress check in <em><hours> h</em> (healing — will improve).", hours = hours}
		end
	elseif hours <= 0 then
		timing = T(890000000010204, "Next progress check: <em>due now</em> (may improve or worsen).")
	else
		timing = T{890000000010205, "Next progress check in <em><hours> h</em> (may improve or worsen).", hours = hours}
	end
	local flavor
	if healing then
		flavor = T(890000000010197, "Treated: healing. Progress checks are faster; each check improves the trauma (will not worsen).")
	elseif tier == "Light" then
		flavor = T(890000000010206, "Light trauma can clear on its own over time.")
	elseif tier == "Medium" then
		flavor = T(890000000010207, "Without treatment this may improve or worsen.")
	elseif tier == "Heavy" then
		flavor = T(890000000010208, "Heavy trauma rarely improves without hospital / field surgery.")
	else
		flavor = ""
	end
	-- Never fall back to effect.Description / ResolveValue — that re-enters GetDescription
	-- and double-appends the progress line (Missing text + two timing lines).
	if not base_desc or base_desc == "" then
		local raw = rawget(_G, "JazzTraumaRawDescription")
		base_desc = (type(raw) == "function" and raw(effect)) or ""
	end
	-- Dedup if a stacked/re-entered path already baked progress into a string.
	if type(base_desc) == "string" then
		local cut = string.find(base_desc, "Next progress check", 1, true)
		if cut and cut > 1 then
			base_desc = string.match(base_desc, "^(.-)%s*\n") or string.sub(base_desc, 1, cut - 1)
			base_desc = string.gsub(base_desc, "%s+$", "")
		end
	end
	-- table.concat of T values returns a TConcat; UI translates it with the effect as
	-- context so <cth_penalty>% / <APLoss> tags resolve (same as Concussion).
	if flavor and flavor ~= "" then
		return table.concat({ base_desc, timing, flavor }, "\n\n")
	end
	return table.concat({ base_desc, timing }, "\n\n")
end

function JazzDowngradeTrauma(unit, zone)
	if not unit or not zone then
		return false
	end
	local current = JazzGetTraumaTier(unit, zone)
	if not current then
		return false
	end
	local old_effect = unit:GetStatusEffect(lTraumaId(zone, current))
	local was_healing = JazzTraumaIsHealing(old_effect)
	local rank = JazzTraumaTierRank[current]
	JazzClearZoneTrauma(unit, zone)
	if rank <= 1 then
		Msg("JAZZ_TraumaCleared", unit, zone)
		return "cleared"
	end
	local new_tier = JazzTraumaTiers[rank - 1]
	unit:AddStatusEffect(lTraumaId(zone, new_tier))
	local effect = unit:GetStatusEffect(lTraumaId(zone, new_tier))
	if effect then
		if was_healing then
			JazzSetTraumaHealing(effect, true)
		end
		JazzInitTraumaProgressTimer(effect, zone, new_tier)
	end
	Msg("JAZZ_TraumaApplied", unit, zone, new_tier)
	return new_tier
end

function JazzTraumaResolveProgressCheck(unit, zone, tier, effect)
	if not unit or not zone or not tier then
		return false
	end
	local healing = JazzTraumaIsHealing(effect)
	local improve_chance, worsen_chance = JazzTraumaProgressChances(zone, tier, healing)
	local roll = (unit.Random and unit:Random(100)) or InteractionRand(100, "JazzTraumaProgress")
	roll = roll + 1 -- 1..100
	local nick = unit.Nick or unit.Name or ""
	if roll <= improve_chance then
		local result = JazzDowngradeTrauma(unit, zone)
		if result == "cleared" then
			CombatLog("short", T{890000000010210, "<merc> trauma improved (cleared)", merc = nick})
		elseif result then
			CombatLog("short", T{890000000010211, "<merc> trauma improved to a lighter tier", merc = nick})
		end
		return "improve"
	elseif roll <= improve_chance + worsen_chance then
		local next_tier
		if tier == "Light" then
			next_tier = "Medium"
		elseif tier == "Medium" then
			next_tier = "Heavy"
		end
		if next_tier and JazzApplyTrauma(unit, zone, next_tier) then
			CombatLog("short", T{890000000010212, "<merc> trauma worsened", merc = nick})
			return "worsen"
		end
	end
	-- Stay: refresh timer.
	if effect then
		JazzInitTraumaProgressTimer(effect, zone, tier)
	else
		local id = lTraumaId(zone, tier)
		local e = unit:GetStatusEffect(id)
		if e then
			JazzInitTraumaProgressTimer(e, zone, tier)
		end
	end
	return "stay"
end

function JazzTraumaProgressOnNewHour(unit)
	if not unit or (unit.IsDead and unit:IsDead()) then
		return
	end
	if not JazzHasAnyTrauma(unit) then
		return
	end
	for _, zone in ipairs(JazzTraumaZones) do
		local tier = JazzGetTraumaTier(unit, zone)
		if tier then
			local id = lTraumaId(zone, tier)
			local effect = unit:GetStatusEffect(id)
			if effect then
				local next_t = effect:ResolveValue("next_check_time")
				if not next_t or next_t == 0 then
					JazzInitTraumaProgressTimer(effect, zone, tier)
					next_t = effect:ResolveValue("next_check_time")
				end
				if next_t and Game and Game.CampaignTime and Game.CampaignTime >= next_t then
					JazzTraumaResolveProgressCheck(unit, zone, tier, effect)
				end
			end
		end
	end
end

function OnMsg.DataLoaded()
	lInstallBandageTargetsHook()
	lInstallCombatActionAttackStartMedHook()
	lInstallMedicineMeleeUIHooks()
end

-- MED-001: disable vanilla HP→Wounded stack conversion (trauma/bleed replace it).
-- HpLossToAddStack=999999 alone is not enough if CharacterEffectDefs lag companion sync.
function UnitProperties:AccumulateDamageTaken(amount)
end

function UnitProperties:AddWounds(wounds)
end

function OnMsg.UnitDowned(unit)
	JazzApplyDownedHeavyTrauma(unit)
end

function OnMsg.NewHour()
	local seen = {}
	if g_Units then
		for _, unit in ipairs(g_Units) do
			if IsValid(unit) and JazzHasAnyTrauma(unit) then
				local sid = unit.session_id
				if sid then
					seen[sid] = true
				end
				JazzTraumaProgressOnNewHour(unit)
			end
		end
	end
	if gv_UnitData then
		for sid, ud in pairs(gv_UnitData) do
			if ud and not seen[sid] and JazzHasAnyTrauma(ud) then
				JazzTraumaProgressOnNewHour(ud)
			end
		end
	end
end

-- Exploration/sat Bandage loops used medicine.Condition > 0; stack kits need Amount.
-- Bind against g_Classes.Unit (instances use that table). A sticky "base saved" flag
-- alone is not enough: ReloadLua / class rebuild restores vanilla methods while the
-- flag stays set, so JazzBandage/JazzMorphine silently fall through to vanilla
-- Unit:Bandage (no field item → early return, or kit path without our one-shot anim).
g_JAZZ_CombatBandageBase = rawget(_G, "g_JAZZ_CombatBandageBase") or false
g_JAZZ_DownedRallyBase = rawget(_G, "g_JAZZ_DownedRallyBase") or false
g_JAZZ_UnitBandageBase = rawget(_G, "g_JAZZ_UnitBandageBase") or false
g_JAZZ_MedicineStackHooks = rawget(_G, "g_JAZZ_MedicineStackHooks") or false

local jazz_combat_bandage_fn
local jazz_unit_bandage_fn
local jazz_downed_rally_fn
local jazz_combat_bandage_base
local jazz_downed_rally_base

local function lJazzUnitClass()
	local classes = lG("g_Classes")
	local cls = classes and classes.Unit
	if type(cls) == "table" and type(cls.Bandage) == "function" then
		return cls
	end
	return false
end

-- Prefer vanilla UnitActions.lua; never chain a previous Systems_Medicine wrap as base.
-- IMPORTANT: bare `debug` is often nil in JA3 (_G sandbox). A previous install crashed on
-- debug.getinfo and aborted before Unit.Bandage was rebound → field actions had no anim.
local function lCaptureNonMedicineBase(current, our_fn, existing_base)
	if type(current) ~= "function" or current == our_fn then
		return false
	end
	local dbg = rawget(_G, "debug")
	local getinfo = dbg and dbg.getinfo
	if getinfo then
		local di = getinfo(current, "S")
		local src = di and di.source or ""
		if string.find(src, "Systems_Medicine", 1, true) then
			return false
		end
		return current
	end
	-- No debug library: only accept on cold first bind for this method.
	if existing_base then
		return false
	end
	return current
end

local function lInstallMedicineStackBandageHooks()
	local unit_cls = lJazzUnitClass()
	if not unit_cls then
		return
	end

	-- Bandage first: full reimplementation (does not need vanilla base). Must not depend on
	-- CombatBandage capture succeeding — that used to abort this whole installer.
	if unit_cls.Bandage ~= jazz_unit_bandage_fn then
		local captured = lCaptureNonMedicineBase(unit_cls.Bandage, jazz_unit_bandage_fn, g_JAZZ_UnitBandageBase)
		if captured then
			g_JAZZ_UnitBandageBase = captured
		end
		if not jazz_unit_bandage_fn then
			jazz_unit_bandage_fn = function(self, action_id, cost_ap, args)
				-- Mirror UnitActions.lua Unit:Bandage; field actions diverge only after Idle.
				args = type(args) == "table" and args or {}
				local goto_ap = args.goto_ap or 0
				local action_cost = (cost_ap or 0) - goto_ap
				local pos = args.goto_pos
				local target = JazzResolveMedicinePatient(self, args.target)
				if target then
					args.target = target
				end
				local sat_view = args.sat_view or false
				local target_self = target == self
				local is_field = action_id == "JazzBandage" or action_id == "JazzMorphine"
				local function clear_bandage_behavior()
					if self.behavior == "Bandage" then
						self:SetBehavior()
					end
					if self.combat_behavior == "Bandage" then
						self:SetCombatBehavior()
					end
				end
				if not target then
					clear_bandage_behavior()
					self:GainAP(action_cost)
					return
				end
				if g_Combat then
					if goto_ap > 0 then
						self:PushDestructor(function(self)
							self:GainAP(action_cost)
						end)
						local result = self:CombatGoto(action_id, goto_ap, args.goto_pos)
						self:PopDestructor()
						if not result then
							self:GainAP(action_cost)
							return
						end
					end
				elseif not target_self then
					self:GotoSlab(pos)
				end
				local myVoxel = SnapToPassSlab(self:GetPos())
				if pos and myVoxel:Dist(pos) ~= 0 then
					clear_bandage_behavior()
					self:GainAP(action_cost)
					return
				end
				local action = CombatActions[action_id]
				local medicine
				if action_id == "JazzBandage" then
					medicine = JazzGetBandageItem(self)
				elseif action_id == "JazzMorphine" then
					medicine = JazzGetMorphineItem(self)
				else
					medicine = GetUnitEquippedMedicine(self)
				end
				if not medicine then
					clear_bandage_behavior()
					self:GainAP(action_cost)
					return
				end
				self:SetBehavior("Bandage", { action_id, cost_ap, args })
				self:SetCombatBehavior("Bandage", { action_id, cost_ap, args })
				if not target_self then
					self:Face(target, 200)
					Sleep(200)
				end
				if not sat_view then
					-- Exact vanilla Unit:Bandage stance/anim calls (UnitActions.lua).
					if self.stance ~= "Crouch" then
						self:ChangeStance(false, 0, "Crouch")
					end
					self:SetState(target_self and "nw_Bandaging_Self_Start" or "nw_Bandaging_Start")
					Sleep(self:TimeToAnimEnd() or 100)
					if not args.provoked then
						self:ProvokeOpportunityAttacks(action, "attack interrupt")
						args.provoked = true
						self:SetBehavior("Bandage", { action_id, cost_ap, args })
						self:SetCombatBehavior("Bandage", { action_id, cost_ap, args })
					end
					self:SetState(target_self and "nw_Bandaging_Self_Idle" or "nw_Bandaging_Idle")
					if not g_Combat and not GetMercInventoryDlg() then
						SetInGameInterfaceMode("IModeExploration")
					end
				elseif not g_Combat and not is_field then
					while IsValid(target) and not target:IsDead()
						and (target.HitPoints < target.MaxHitPoints or JazzHasAnyBleed(target)) do
						medicine = GetUnitEquippedMedicine(self)
						if not JazzMedicineIsUsable(medicine) then
							break
						end
						target:GetBandaged(medicine, self)
					end
				end
				if is_field then
					-- One-shot field apply (not kit Halt channel). Skip BandageInCombat on
					-- morphine→downed: OnRemoved re-adds BleedingOut while still IsDowned.
					local morphine_rally = action_id == "JazzMorphine" and JazzUnitNeedsMorphineRally(target)
					if not sat_view then
						if IsValid(target) then
							target:AddStatusEffect("BeingBandaged")
							ObjModified(target)
							self:Face(target, 0)
						end
						local heal_anim = target_self and "nw_Bandaging_Self_Idle" or "nw_Bandaging_Idle"
						self:SetState(heal_anim, const.eKeepComponentTargets)
						if not target_self then
							PlayVoiceResponse(self, "BandageDownedUnit")
						end
						if not morphine_rally then
							self:AddStatusEffect("BandageInCombat")
						end
						Sleep(1200)
					end
					local ok = false
					if action_id == "JazzBandage" then
						ok = JazzApplyBandageAction(self, target)
					else
						ok = JazzApplyMorphineAction(self, target)
					end
					if not morphine_rally then
						self:RemoveStatusEffect("BandageInCombat")
					end
					ObjModified(self)
					if IsValid(target) then
						target:RemoveStatusEffect("BeingBandaged")
						ObjModified(target)
					end
					if not sat_view then
						local normal_anim = self:TryGetActionAnim("Idle", self.stance)
						if normal_anim then
							self:PlayTransitionAnims(normal_anim)
						end
					end
					clear_bandage_behavior()
					if not ok then
						self:GainAP(action_cost)
					end
					return
				end
				self:SetCommand("CombatBandage", target, medicine)
			end
		end
		unit_cls.Bandage = jazz_unit_bandage_fn
	end

	if unit_cls.CombatBandage ~= jazz_combat_bandage_fn then
		local captured = lCaptureNonMedicineBase(
			unit_cls.CombatBandage,
			jazz_combat_bandage_fn,
			jazz_combat_bandage_base or g_JAZZ_CombatBandageBase
		)
		if captured then
			jazz_combat_bandage_base = captured
			g_JAZZ_CombatBandageBase = captured
		elseif not jazz_combat_bandage_base then
			jazz_combat_bandage_base = g_JAZZ_CombatBandageBase or false
		end
		-- g_Combat branch needs vanilla base; skip rebind until one is known.
		if jazz_combat_bandage_base then
			if not jazz_combat_bandage_fn then
				jazz_combat_bandage_fn = function(self, target, medicine)
					local base = jazz_combat_bandage_base or g_JAZZ_CombatBandageBase
					if g_Combat then
						return base(self, target, medicine)
					end
					target:AddStatusEffect("BeingBandaged")
					ObjModified(target)
					if IsValid(target) then
						self:Face(target, 0)
					end
					self:PushDestructor(function()
						self:SetCombatBehavior()
						self:SetBehavior()
						self:RemoveStatusEffect("BandageInCombat")
						target:RemoveStatusEffect("BeingBandaged")
						ObjModified(target)
						ObjModified(self)
					end)
					self:AddStatusEffect("BandageInCombat")
					while IsValid(target) and not target:IsDead()
						and (target.HitPoints < target.MaxHitPoints or JazzHasAnyBleed(target)) do
						medicine = GetUnitEquippedMedicine(self)
						if not JazzMedicineIsUsable(medicine) then
							break
						end
						Sleep(5000)
						target:GetBandaged(medicine, self)
					end
					self:SetState(self == target and "nw_Bandaging_Self_End" or "nw_Bandaging_End")
					Sleep(self:TimeToAnimEnd() or 100)
					self:PopAndCallDestructor()
				end
			end
			unit_cls.CombatBandage = jazz_combat_bandage_fn
		end
	end

	-- InventoryStack kits: vanilla DownedRally does medicine.Condition -= … and breaks stacks.
	-- Always install (do not require base capture). Morphine calls DownedRally() with no args.
	if unit_cls.DownedRally ~= jazz_downed_rally_fn then
		local captured = lCaptureNonMedicineBase(
			unit_cls.DownedRally,
			jazz_downed_rally_fn,
			jazz_downed_rally_base or g_JAZZ_DownedRallyBase
		)
		if captured then
			jazz_downed_rally_base = captured
			g_JAZZ_DownedRallyBase = captured
		elseif not jazz_downed_rally_base then
			jazz_downed_rally_base = g_JAZZ_DownedRallyBase or false
		end
		jazz_downed_rally_fn = function(self, medic, medicine)
			local base = jazz_downed_rally_base or g_JAZZ_DownedRallyBase
			if medic and medicine and IsKindOf(medicine, "InventoryStack") then
				self:SetCombatBehavior()
				self:RemoveStatusEffect("Stabilized")
				self:RemoveStatusEffect("BleedingOut")
				self:RemoveStatusEffect("Unconscious")
				self:RemoveStatusEffect("Downed")
				self:SetTired(Min(self.Tiredness, 2))
				self.downed_check_penalty = 0
				self:GetBandaged(medicine, medic)
				medic:SetCommand("EndCombatBandage")
				local stance = self.immortal and "Standing" or self.stance
				self.stance = stance
				local normal_anim = self:TryGetActionAnim("Idle", self.stance)
				self:PlayTransitionAnims(normal_anim)
				if g_Combat then
					self:GainAP(self:GetMaxActionPoints() - self.ActionPoints)
				end
				self.TempHitPoints = 0
				ObjModified(self)
				ObjModified(self.team)
				ForceUpdateCommonUnitControlUI("recreate")
				CreateFloatingText(self, T(979333850225, "Recovered"))
				PlayFX("UnitDownedRally", "start", self)
				Msg("OnDownedRally", medic, self)
				self:CallReactions("OnUnitRallied", medic, self)
				if medic ~= self and IsKindOf(medic, "Unit") then
					medic:CallReactions("OnUnitRallied", medic, self)
				end
				self:SetCommand("Idle")
				return
			end
			if base then
				return base(self, medic, medicine)
			end
			-- No captured base: still get up (Morphine uses this path — no medicine arg).
			self:SetCombatBehavior()
			self:RemoveStatusEffect("Stabilized")
			self:RemoveStatusEffect("BleedingOut")
			self:RemoveStatusEffect("Unconscious")
			self:RemoveStatusEffect("Downed")
			self:SetTired(Min(self.Tiredness, 2))
			self.downed_check_penalty = 0
			local stance = self.immortal and "Standing" or self.stance
			self.stance = stance
			local normal_anim = self:TryGetActionAnim("Idle", self.stance)
			self:PlayTransitionAnims(normal_anim)
			if g_Combat then
				self:GainAP(self:GetMaxActionPoints() - self.ActionPoints)
			end
			self.TempHitPoints = 0
			ObjModified(self)
			ObjModified(self.team)
			ForceUpdateCommonUnitControlUI("recreate")
			CreateFloatingText(self, T(979333850225, "Recovered"))
			PlayFX("UnitDownedRally", "start", self)
			Msg("OnDownedRally", medic, self)
			self:CallReactions("OnUnitRallied", medic, self)
			self:SetCommand("Idle")
		end
		unit_cls.DownedRally = jazz_downed_rally_fn
	end

	g_JAZZ_MedicineStackHooks = true
end

function OnMsg.ClassesBuilt()
	lInstallMedicineStackBandageHooks()
	lInstallCombatActionAttackStartMedHook()
	lInstallMedicineMeleeUIHooks()
end

function OnMsg.ModsReloaded()
	-- Classes may be redefined; reinstall targeting + Bandage wraps.
	lInstallBandageTargetsHook()
	lInstallCombatActionAttackStartMedHook()
	lInstallMedicineMeleeUIHooks()
	-- Identity rebind in lInstall* handles wiped Unit methods; no sticky-flag skip.
	lInstallMedicineStackBandageHooks()
end

lInstallCombatActionAttackStartMedHook()
lInstallMedicineMeleeUIHooks()
lInstallMedicineStackBandageHooks()
