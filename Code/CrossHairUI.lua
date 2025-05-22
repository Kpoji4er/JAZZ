function CrosshairUI:UpdateAim()
	local pContext = self.context
	if not pContext then
		return
	end
	
	local attacker = pContext.attacker
	local action = self.show_data_for_action or pContext.action
	local target = pContext.target

	if not IsValid(target) or not action then
		return
	end

	local args = {
		target = target,
		goto_pos = pContext.meleeTargetPos,
		target_spot_group = self.targetPart.id,
		step_pos = pContext.override_pos,
		cth_breakdown = true,
		damage_breakdown = true,
		free_aim = pContext.free_aim
	}
	if not self.context.noAim then
		self.aim = self.aim or 0
		args.aim = self.aim
		
		-- make sure the attacker has the AP for the aiming
		while self.aim > 0 and action:GetUIState({ attacker }, args) ~= "enabled" do
			self.aim = self.aim - 1
			args.aim = self.aim
		end
	end
	
	-- Action can no longer be used.
	if action:GetUIState({ attacker }, args) ~= "enabled" then
		if not attacker.move_attack_in_progress then
			SetInGameInterfaceMode(g_Combat and "IModeCombatMovement" or "IModeExploration")
		end
		return
	end

	local attackResultTable = {}
	local cthTable = {}
	local critChance = 0
	
	-- Gather information from attack results, to display.
	if not self.cached_results then self.cached_results = {} end
	
	local cached_results = self.cached_results[action.id]
	local invalidCache = not cached_results or
									cached_results.aim ~= self.aim or
									cached_results.ap ~= attacker.ActionPoints or
									cached_results.free_move_ap ~= attacker.free_move_ap
									
		
	if invalidCache then
		local cthCalc, attackResultCalc = {}, {}
		local crit = 0
		
		-- Check for spotter unit, shows a specific icon and rollover
		local spotter = false
		for _, u in ipairs(attacker.team.units) do  
			if u ~= attacker and VisibilityCheckAll(u, target, nil, const.uvVisible) then
				spotter = u
			end
		end
		
		local spotterCth, noLoSCth, grazingProtected = false, false, false -- needed for ui
		local inDarkness = false -- needed for tutorials
		
		-- Non-unit targets (such as traps) need to provide an empty string as the target_spot_group (due to lof internal logic)
		local queryBodyParts = IsKindOf(target, "Unit") 
		for i, p in ipairs(pContext.body_parts) do
			local partId = p.id
			args.target_spot_group = queryBodyParts and partId or ""
			local results, attack_args = action:GetActionResults(attacker, args)
			cthCalc[partId] = results.chance_to_hit
			results.crosshair_attack_args = attack_args
			attackResultCalc[partId] = results
			
			-- skip calling ResolveAttackParams for every body part
			if results.lof then
				args.lof = results.lof
			end
			
			spotterCth = spotterCth or table.find(results.chance_to_hit_modifiers, "id", "SeenBySpotter")
			noLoSCth = noLoSCth or table.find(results.chance_to_hit_modifiers, "id", "NoLineOfSight")
			inDarkness = inDarkness or table.find(results.chance_to_hit_modifiers, "id", "Darkness")

			results.cantSeeBodyPart = false
			results.spotter = false -- no longer per body part but leaving this here for clarity
			
			local hitOnTarget = table.find_value(results, "obj", target)
			if hitOnTarget and hitOnTarget.grazing then
				results.grazing = true
				results.crit_chance = 0
				if hitOnTarget.grazing_reason == "cover" then
					grazingProtected = true
				end
			end
			
			if results and results.crit_chance then
				crit = results.crit_chance
			end
			
			local damage = 0
			for i, hit in ipairs(results) do
				if hit.obj == target then
					damage = damage + hit.damage + (hit.armor_prevented or 0)
				end
			end
			
			local aoeDamage = 0
			for i, hit in ipairs(results.area_hits) do
				if hit.obj == target then
					aoeDamage = aoeDamage + hit.damage + (hit.armor_prevented or 0)
				end
			end
			results.calculated_target_damage = damage
			results.calculated_target_aoeDamage = aoeDamage
		end

		if (noLoSCth or spotterCth) then
			local defaultPartId = self.defaultTargetPart.id
			cthCalc["BlindFire"] = cthCalc[defaultPartId]
			local attackResultCopy = table.copy(attackResultCalc[defaultPartId])
			attackResultCopy.cantSeeBodyPart = true
			attackResultCopy.spotter = spotterCth and spotter
			attackResultCalc["BlindFire"] = attackResultCopy
			
			-- Overwrite some of the torso data so it's more ambigious which
			-- part you're hitting
		--	attackResultCopy.chance_to_hit_modifiers = {
		--		{
		--			id = "Unknown",
		--			value = 0 ,
		--			name = T(553504408105, "Unknown Modifiers"),
		--		}
		--	}
			
			-- For debug functionality display the highest cth bodypart
			if CthVisible() then
				local highestCth = 0
				local highestCthPart = false
				for partName, partData in pairs(attackResultCalc) do
					local cth = partData.chance_to_hit
					if not highestCthPart or cth > highestCth then
						highestCthPart = partData
						highestCth = highestCth
					end
				end
				attackResultCopy.chance_to_hit_modifiers = highestCthPart.chance_to_hit_modifiers
				attackResultCopy.chance_to_hit = highestCthPart.chance_to_hit
				cthCalc["BlindFire"] = highestCthPart.chance_to_hit
			end
			
			local noneOfPartsHit = true
			for partName, partData in pairs(attackResultCalc) do
				if partData.target_hit then
					noneOfPartsHit = false
					break
				end
			end
			if not noneOfPartsHit then
				attackResultCopy.target_hit = true
			end
			
			self.targetPart = Presets.TargetBodyPart.Default.BlindFire
		elseif target:HasStatusEffect("Protected") and grazingProtected then
			local highestCth = 0
			local highestCthPart, highestCthId = false, false
			for partName, partData in pairs(attackResultCalc) do
				local cth = partData.chance_to_hit
				if not highestCthPart or cth > highestCth then
					highestCthPart = partData
					highestCth = highestCth
					highestCthId = partName
				end
			end
		
			-- InCover body part selects the body part with highest cth (191329)
			local attackResultCopy = table.copy(highestCthPart)
			attackResultCopy.actual_body_part = highestCthId			
			attackResultCopy.bodyPartDisplayName = Presets.TargetBodyPart.Default[highestCthId].display_name
			cthCalc["InCover"] = cthCalc[highestCthId]
			attackResultCalc["InCover"] = attackResultCopy
			
			self.targetPart = Presets.TargetBodyPart.Default.InCover
		elseif self.targetPart == Presets.TargetBodyPart.Default.BlindFire or
				 self.targetPart == Presets.TargetBodyPart.Default.InCover then -- No longer valid fake bodypart
			self.targetPart = g_DefaultShotBodyPart
		end
		
		self.cached_results[action.id] = {
			cthCalc = cthCalc,
			attackResultCalc = attackResultCalc,
			crit = crit,
			aim = self.aim,
			ap = attacker.ActionPoints,
			free_move_ap = attacker.free_move_ap,
		}
		
		if inDarkness and not TutorialHintsState.InDarkness then
			self.darkness_tutorial = true
		end

		local target_dummy
		local lof_data = args.lof and args.lof[1]
		local atk_results = attackResultCalc[args.target_spot_group or false]
		if lof_data then
			target_dummy = {
				obj = lof_data.obj,
				anim = lof_data.anim,
				phase = 0,
				pos = lof_data.step_pos,
				angle = lof_data.angle,
				stance = lof_data.stance,
			}
		elseif args.goto_pos and attacker:GetDist(args.goto_pos) > const.SlabSizeX / 2 then
			target_dummy = {
				obj = attacker,
				pos = args.goto_pos,
			}
		elseif atk_results and atk_results.step_pos then
			target_dummy = { 
				obj = attacker, 
				pos = atk_results.step_pos, 
			}
		end
		self.context.danger = AnyAttackInterrupt(attacker, target, action, target_dummy)
		if not self.context.danger and args.goto_pos then
			local combatPath = GetMeleeAttackCombatPath(action, attacker)
			local targetPath = combatPath and combatPath:GetCombatPathFromPos(args.goto_pos)
			if targetPath then
				self.context.danger = AnyInterruptsAlongPath(attacker, targetPath, "all", action)
			end
		end
	end

	assert(self.cached_results[action.id])
	local cachedRe = self.cached_results[action.id]
	cthTable = cachedRe.cthCalc
	attackResultTable = cachedRe.attackResultCalc
	critChance  = cachedRe.crit
	
	-- Write data to context
	if not action.AlwaysHits then
		pContext.cth = cthTable
	else
		pContext.cth = {}
	end
	pContext.attackResultTable = attackResultTable
	
	local actualAction = pContext.action -- Dont use "show_for_action" for these calculations
	local distToTarget = attacker:GetDist(target)
	pContext.attack_distance = DivCeil(distToTarget, const.SlabSizeX)
	
	local weapon1, _ = actualAction:GetAttackWeapons(attacker)
	pContext.weapon_range = actualAction:GetMaxAimRange(attacker, weapon1) or weapon1.WeaponRange
    pContext.weapon_eff_range = actualAction:GetMaxAimRange(attacker, weapon1) or weapon1.BulletDropRange
    pContext.aim = self.aim;
    assert(pContext.aim)
	assert(pContext.weapon_range)
    assert(pContext.weapon_eff_range)
	pContext.weapon_range = pContext.weapon_range or 0
    pContext.weapon_eff_range = pContext.weapon_eff_range or 0
    pContext.aim = pContext.aim or 0;
	
	local hasflashlight = false
	if weapon1:HasComponent("IgnoreInTheDarkWhenFullyAimed") and pContext.aim >= (GetComponentEffectValue(weapon1, "ScopeMagnification", "ScopeAimLevel") or -1) then
		hasflashlight = true
	else 
		hasflashlight = false
	end


    local ScopeMagn = GetComponentEffectValue(weapon1, "ScopeMagnification", "ScopeMagnification") or 1
    local ScopeSubMagn = GetComponentEffectValue(weapon1, "ScopeMagnification", "ScopeSubMagnification") or 0
    pContext.ScopeAimLevel = GetComponentEffectValue(weapon1, "ScopeMagnification", "ScopeAimLevel") or -1

    local SmallMagn = GetComponentEffectValue(weapon1, "SmallMagnification", "SmallMagnification") or 1
    local SmallSubMagn = GetComponentEffectValue(weapon1, "SmallMagnification", "SmallSubMagnification") or 0
    pContext.SmallAimLevel = GetComponentEffectValue(weapon1, "SmallMagnification", "SmallAimLevel") or -1
    pContext.ScopeLevelText = ScopeMagn.."."..ScopeSubMagn.."x" or ""
    pContext.SmallScopeLevelText = SmallMagn.."."..SmallSubMagn.."x" or ""


	local scope = weapon1.components.Scope
	if WeaponComponents[scope] then  
	local ScopeImage = WeaponComponents[scope].ReticleInner or ""
    local SmallScopeImage = WeaponComponents[scope].ReticleInnerSub or ""
	local ScopeOuterImage = WeaponComponents[scope].ReticleOuter or ""

	pContext.ScopeImage = ScopeImage
	pContext.SmallScopeImage = SmallScopeImage
	pContext.ScopeOuterImage = ScopeOuterImage


	--if (GameState.Night or GameState.Underground) and not attacker:HasNightVision() and not target:HasStatusEffect("Protected") and not hasflashlight then 
	if not (hasflashlight or not (GameState.Night or GameState.Underground) or IsIlluminated(target))  then
		print('cth crosshair - night')
		pContext.ScopeImage = ""
		pContext.SmallScopeImage = ""
		pContext.ScopeOuterImage = ""
		pContext.ScopeAimLevel = 10
		pContext.SmallAimLevel = 10
		pContext.ScopeLevelText = ""
		pContext.SmallScopeLevelText = ""
	end

	assert(pContext.ScopeImage)
    assert(pContext.SmallScopeImage)
    assert(pContext.ScopeOuterImage)

	end



    assert(pContext.ScopeAimLevel)
    assert(pContext.SmallAimLevel)
    assert(pContext.ScopeLevelText)
    assert(pContext.SmallScopeLevelText)

    pContext.ScopeAimLevel = pContext.ScopeAimLevel or -1
    pContext.SmallAimLevel = pContext.SmallAimLevel or -1
    pContext.ScopeLevelText = pContext.ScopeLevelText or ""
    pContext.SmallScopeLevelText = pContext.SmallScopeLevelText or ""

        

	local dialog = GetInGameInterfaceModeDlg()
	self.attack_cursor = GetRangeBasedMouseCursor(dialog.penalty, actualAction, "attack")

	local bodyPartsUI = self:ResolveId("idButtonsContainer")
	for i, p in ipairs(bodyPartsUI) do
		local cth = CthVisible() and cthTable[p.context.id]
		if cth then
			p.idHitChance:SetText(T{483116174778, "<percent(cth)>", cth = cth})
		else
			p.idHitChance:SetVisible(false)
		end
	end
	ObjModified("crosshair")
	ObjModified("firing_mode")
	ObjModified(pContext)
	
	args.target_spot_group = self.targetPart.id -- restore potentially changed argument by the loop above
	if RolloverWin then
		RolloverWin:UpdateRolloverContent()
	end
	--self:SetScaleModifier(GetUIStyleGamepad() and point(1150, 1150) or point(1000, 1000))
	
	if self.idAPCostText then
		args.ap_cost_breakdown = {}
		local apCost = action:GetAPCost(attacker, args)	
		local free_move_ap_used = Min(args.ap_cost_breakdown.move_cost or 0, attacker.free_move_ap)
		apCost = apCost - Max(0, free_move_ap_used)
		-- round the cost to match before/after AP readings
		local unitAp = attacker:GetUIActionPoints()
		local before = unitAp / const.Scale.AP
		local after = (unitAp - apCost) / const.Scale.AP -- free move is already accounted for in apCost
		apCost = (before - after) * const.Scale.AP
		
		--local has_movement = action.AimType == "melee"
		--local apCost, unitAp = attacker:GetUIAdjustedActionCost(cost, has_movement)
		--apCost, unitAp = apCost * const.Scale.AP, unitAp * const.Scale.AP
		if g_Combat then
			self.idAPCostText:SetText(
				T{444327862984, "<apn(apCost)><style CrosshairAPTotal><valign bottom -2>/<apn(unitAp)> AP</style>", apCost = apCost, unitAp = unitAp}
			)
		else
			self.idAPCostText:SetText(T{235238255759, "<apn(apCost)><style CrosshairAPTotal><valign bottom -2> AP</style>", apCost = apCost})
		end
		if self.aim ~= 0 then
			self.idAPCostText:SetTextStyle("CrosshairAPCostYellow")
		else
			self.idAPCostText:SetTextStyle("CrosshairAPCost")
		end
	end

--	print(pContext.ScopeLevelText)
--	print(pContext.aim)
	if self.ScopeZoom and pContext.ScopeLevelText and pContext.aim >= pContext.ScopeAimLevel and pContext.ScopeAimLevel > 0 then
		self.ZoomLevelWindow:SetVisible(true)
		local ScopeLevelText = pContext.ScopeLevelText
		self.ScopeZoom:SetText(
			T{444327862984111, "<ScopeLevelText>", ScopeLevelText = pContext.ScopeLevelText}
		)   
	elseif self.ScopeZoom and pContext.SmallScopeLevelText and pContext.aim >= pContext.SmallAimLevel and pContext.SmallAimLevel > 0 then
			local ScopeLevelText = pContext.SmallScopeLevelText
			self.ScopeZoom:SetText(
				T{444327862984111, "<ScopeLevelText>", ScopeLevelText = pContext.SmallScopeLevelText}
			)  
		self.ZoomLevelWindow:SetVisible(true) 
	elseif self.ScopeZoom then
			self.ScopeZoom:SetText(
				T{""}
			)   
			self.ZoomLevelWindow:SetVisible(false)

	end
	
	WeaponRangeTutorial(self)
	ShowCrosshairTutorial(self)
end

function CrosshairUI:OnLayoutComplete()
	if not self.dynamic then
		self:SetInteractionBox(self.box:minx(), self.box:miny(), point(1000, 1000), true)
	end
	local target = self.context.target
	local playVr = IsKindOf(self.parent, "IModeCombatAttack")
	if playVr and not target:IsPlayerAlly() and (not IsKindOf(target, "Unit") or not target:IsCivilian()) then
		-- Get attack results from crosshair to determine whether to play VR
		local attackResult = self and self.cached_results
		attackResult = attackResult and attackResult[self.context.action.id]
		
		local one_non_obstructed = false
		local bestChance = 0
		local worstChance = max_int
		local attackResultCalc = attackResult and attackResult.attackResultCalc
		local is_blind_fire = attackResultCalc and not not attackResultCalc.BlindFire
		for id, bodyPartData in pairs(attackResultCalc) do
			bestChance = Max(bestChance, bodyPartData.chance_to_hit)
			worstChance = Min(worstChance, bodyPartData.chance_to_hit)
			one_non_obstructed = one_non_obstructed or not bodyPartData.obstructed
		end
		
		local torsoAttackResult = attackResult and attackResult.attackResultCalc
		torsoAttackResult = torsoAttackResult and torsoAttackResult.Torso
		local torso_stealth_kill = torsoAttackResult and torsoAttackResult.stealth_attack
		local attacker = self.context.attacker
		local is_hidden = attacker:HasStatusEffect("Hidden") or torso_stealth_kill
		if not one_non_obstructed or is_blind_fire or bestChance <= 20 then
			PlayVoiceResponse(attacker, is_hidden and "AimAttack_LowStealth" or "AimAttack_Low")
		elseif bestChance > 50 then
			PlayVoiceResponse(attacker, is_hidden and "AimAttackStealth" or "AimAttack")
		end
	end	
end

function PopulateCrosshairUICth(win, attacker, action, attackResults)
	local weapon = action:GetAttackWeapons(attacker)
	local dontShow = action.AlwaysHits
	win:SetVisible(not dontShow)
	if dontShow or not attackResults then return end

	local chanceToHit = attackResults.chance_to_hit
	local modifiers = attackResults.chance_to_hit_modifiers
	
	if CthVisible() or chanceToHit <= 0  then
		win.idChanceToHit:SetText(T{757275361770, "ACCURACY: <right><percent(chanceToHit)>", chanceToHit = chanceToHit})
		win.idChanceToHit.parent:SetZOrder(1)
	else
		win.idChanceToHit:SetText(T{906758075439, "ACCURACY", chanceToHit = chanceToHit})
		win.idChanceToHit.parent:SetZOrder(0)
	end
	if not modifiers then -- Invalid weapon, or invalid target, or something else
		win:SetVisible(false)
		return
	end
	
	-- Map and concat mods
	local concatList = {}
	for i, mod in ipairs(modifiers) do
		if mod.uiHidden then goto continue end
	
		if mod.value then -- Handle missing value just in case
			local sign = ""
			if (mod.id and mod.value > 0) then
				local repeats = Min((DivRound(mod.value,10) - 1),10)
				sign = "<color PDASectorInfo_Green>+</color>"
				while repeats > 0 do
					sign = "<color PDASectorInfo_Green>+</color>"..sign
					repeats = repeats - 1
				end
			elseif mod.value > 50 then
					local repeats = Min((DivRound(mod.value-50,10) - 1),10)
					sign = "<color PDASectorInfo_Green>+</color>"
					while repeats > 0 do
						sign = "<color PDASectorInfo_Green>+</color>"..sign
						repeats = repeats - 1
					end
			elseif (mod.id and mod.value < 0) then
				local repeats = Min((DivRound(mod.value,-10) - 1),10)
				sign = "<color DescriptionTextRed>-</color>"
				while repeats > 0 do
					sign = "<color DescriptionTextRed>-</color>"..sign
					repeats = repeats - 1
				end
			elseif mod.value < 50 then
				local repeats = Min((DivRound(mod.value-50,-10) - 1),10)
				sign = "<color DescriptionTextRed>-</color>"
				while repeats > 0 do
					sign = "<color DescriptionTextRed>-</color>"..sign
					repeats = repeats - 1
				end
			end
			--if CthVisible() or true then sign = sign..T{257328164584, "<percent(value)>", value = mod.value} end
			concatList[#concatList + 1] = T{221170966425, "<name><right><style PDABrowserTextLightBold><sign></style>", name = mod.name, sign = sign}
		else
			concatList[#concatList + 1] = mod.name
		end
		
		if mod.metaText then
			if IsT(mod.metaText) then
				concatList[#concatList + 1] = T{399490205680, "<left> <metaText>", metaText = mod.metaText}
			else
				for i, t in ipairs(mod.metaText) do
					concatList[#concatList + 1] = T{399490205680, "<left> <metaText>", metaText = t}
				end
			end
		end
		
		::continue::
	end
	local concatStr = table.concat(concatList, "\n<left>")
	win.idModifiers:SetVisible(true)
	win.idModifiers:SetText(Untranslated(concatStr))
end


function CthVisible()
	--return table.find(ModsLoaded, "id", "KAJY0RB")
	return false
end
