local lAboveBadgeTexts = {
	-- Enemies
	NoSight = T(853501212617, "NO SIGHT"),
	NoLOF = T(625870963186, "NO LINE OF FIRE"),
	Suspicious = T(891958507003, "SUSPICIOUS"),
	Surprised = T(144402315512, "SURPRISED"),
	Unaware = T(395978046294, "UNAWARE"),
	-- Allies
	OutOfAmmo = T(846615723770, "OUT OF AMMO"),
	Reload = T(402669531723, "RELOAD"),
	Hidden = T(928205349561, "HIDDEN"),
	Bandaging = T(633661081662, "Bandaging"),
	InDanger = T(608680053799, "IN DANGER!"),
	-- queued actions (active pause
	QueuedAction = T(262910234067, "QUEUED ACTION"),
	
	InterruptAttacksRemaining = T(760116982146, "MAX. ATTACKS: <number>"),
}

function CombatBadgeAboveNameTextUpdate(win)
	local badge = win:ResolveId("node")
	local unit = badge.unit
	local attacker = Selection and Selection[1]
	if badge.window_state == "destroying" then
		win:SetVisible(false)
		return
	end
	
	local text = false
	local style = false
	
	if not text and g_Overwatch[unit] then
		local overwatchData = g_Overwatch[unit]
		local numberOfAttacks = overwatchData and overwatchData.num_attacks
		if numberOfAttacks and numberOfAttacks > 0 then
			text = T{lAboveBadgeTexts.InterruptAttacksRemaining, number = numberOfAttacks}
			style = "BadgeName_Red"
		end
	end
	
	if badge.mode == "enemy" and attacker then
		local enemySeesPlayer = VisibilityCheckAll(attacker, unit, nil, const.uvVisible)
		local outOfRange = false
		if attacker and IsKindOf(attacker, "Unit") then	
			local canAttack = true
			local action = attacker:GetDefaultAttackAction()
			local wep = action and action:GetAttackWeapons(attacker)
			if IsKindOf(wep, "Firearm") then
				local distance = attacker:GetDist(unit) / const.SlabSizeX
				outOfRange = distance >= wep.WeaponRange
				if canAttack then canAttack = not outOfRange end
			else
				outOfRange = false
			end
		end

--[[		if outOfRange then
			text = lAboveBadgeTexts.NoRange
			style = "BadgeName_Red"]]
		if unit.StealthKillChance > -1 then -- Shown during damage prediction, such as mobile shot
			text = T(142002637794, "Stealth Kill")
			style = "BadgeName_Red" 
		elseif table.find(s_PredictionNoLofTargets, unit) then
			text = lAboveBadgeTexts.NoLOF
			style = "BadgeName_Red"
		elseif not enemySeesPlayer then
			text = lAboveBadgeTexts.NoSight
			style = "BadgeName_Red"
		elseif unit:HasStatusEffect("Suspicious") then
			text = lAboveBadgeTexts.Suspicious
			style = "BadgeName_Red"
		elseif unit:HasStatusEffect("Surprised") then
			text = lAboveBadgeTexts.Surprised
			style = "BadgeName_Red"
		elseif unit:HasStatusEffect("Unaware") then
			text = lAboveBadgeTexts.Unaware
			style = "BadgeName_Red"
		end
	elseif badge.mode == "friend" and (g_Combat or badge.selected) then
		if not text then
			local w1, w2 = unit:GetActiveWeapons("Firearm")
			if w1 and (not w1.ammo or w1.ammo.Amount == 0) then
				local ammoForWeapon = unit:GetAvailableAmmos(w1, nil, "unique")
				text = #ammoForWeapon == 0 and lAboveBadgeTexts.OutOfAmmo or lAboveBadgeTexts.Reload
				style = "BadgeName_Red"
			elseif w2 and (not w2.ammo or w2.ammo.Amount == 0) then
				local ammoForWeapon = unit:GetAvailableAmmos(w2, nil, "unique")
				text = #ammoForWeapon == 0 and lAboveBadgeTexts.OutOfAmmo or lAboveBadgeTexts.Reload
				style = "BadgeName_Red"
			end
		end

		if not text and unit:HasStatusEffect("Hidden") then
			text = lAboveBadgeTexts.Hidden
			style = "BadgeName_Red"
		end

		if not text and IsMerc(unit) and IsActivePaused() and unit.queued_action_id then
			local action = CombatActions[unit.queued_action_id]
			style = "BadgeName_Red"
			text = action and action.QueuedBadgeText or lAboveBadgeTexts.QueuedAction
		end

		if not text then
			if IsMerc(unit) then
				local operation = unit.Operation
				local operation_preset = SectorOperations[operation]
				if operation_preset.ShowInCombatBadge and gv_Sectors[gv_CurrentSectorId] and not gv_Sectors[gv_CurrentSectorId].conflict then
					text = operation_preset and operation_preset.display_name
					style = "BadgeName"
				end
			end
		end
		
		if not text then				
			local damagePredicted = unit.PotentialDamage > 0 or unit.SmallPotentialDamageIcon or unit.LargePotentialDamageIcon
			if damagePredicted then
				text = lAboveBadgeTexts.InDanger
				style = "BadgeName_Red"
			elseif unit:IsDowned() and not unit:HasStatusEffect("Unconscious") then
                local effect = unit:GetStatusEffect("Bleeding")
                local count = 0
                    if effect then
                         count = effect.stacks 
                    end
                local Turns
                    Turns = (unit.Health / (count * 5 + 8)) or 100
				local dieChance = 100 - (unit.Health + unit.downed_check_penalty)
				if FindBandagingUnit(unit) then
					dieChance = 0
				end
				
				local chanceAsText = false
				if dieChance > 75 then
					chanceAsText = DieChanceToText.VeryHigh
				elseif dieChance > 50 then
					chanceAsText = DieChanceToText.High
				elseif dieChance > 20 then
					chanceAsText = DieChanceToText.Moderate
				elseif dieChance > 0 then
					chanceAsText = DieChanceToText.Low
				elseif dieChance <= 0 then
					chanceAsText = DieChanceToText.None
				end
				
				if Turns == 1 then
				text = T{890000000001392, "Умрёт через <chanceAsText> ход", chanceAsText = Turns}
				elseif Turns < 5 then
				text = T{890000000001394, "Умрёт через <chanceAsText> хода", chanceAsText = Turns}
				else text = T{890000000001393, "Умрёт через <chanceAsText> ходов", chanceAsText = Turns}
				end
				text = T{890000000001391, "Умрёт без перевязки", chanceAsText = Turns}

				style = "BadgeName_Red"
			elseif unit:HasStatusEffect("BandageInCombat") then
				text = lAboveBadgeTexts.Bandaging
				style = "BadgeName"
			end
		end
	end
	
	win:SetVisible(not not text)
	win:SetText(text)
	win:SetTextStyle(style)
end

-- Party portrait: combat used to show only Wounded/Tired; match satellite ShownSatelliteView list.
-- Always keep Tired/Exhausted (vanilla combat party showed them even without satellite flag).
-- Resolve ShownSatelliteView from CharacterEffectDefs when instance/template props do not stick
-- (MissingEffect placeholders keyed under the real preset id).
local function lJazzStatusEffectPresetId(effect, status_effects)
	if status_effects then
		for key, idx in pairs(status_effects) do
			if type(key) == "string" and type(idx) == "number" and status_effects[idx] == effect then
				return key
			end
		end
	end
	return effect and effect.class
end

local function lJazzStatusEffectDefProp(effect, status_effects, prop)
	local id = lJazzStatusEffectPresetId(effect, status_effects)
	local def = id and CharacterEffectDefs and CharacterEffectDefs[id]
	if not def then
		return nil
	end
	if def.GetProperty then
		return def:GetProperty(prop)
	end
	return def[prop]
end

function JazzStatusEffectShownSatelliteView(effect, status_effects)
	if not effect then
		return false
	end
	if effect.ShownSatelliteView then
		return true
	end
	return not not lJazzStatusEffectDefProp(effect, status_effects, "ShownSatelliteView")
end

-- Critical statuses first so satellite MaxHeight clip does not hide infection.
local JazzPartyStatusPriority = {
	WoundInfected = 10,
	BleedingHeavy = 20,
	BleedingMedium = 21,
	Bleeding = 22,
	BloodLoss1 = 30,
	BloodLoss5 = 31,
	BloodLoss10 = 32,
	BloodLoss20 = 33,
	BloodLoss30 = 34,
	BloodLoss40 = 35,
	BloodLoss50 = 36,
	Unconscious = 40,
	Exhausted = 50,
	Tired = 51,
}

function JazzGetPartyPortraitStatusEffects(status_effects)
	status_effects = status_effects or empty_table
	local list = {}
	for _, effect in ipairs(status_effects) do
		if JazzStatusEffectShownSatelliteView(effect, status_effects) then
			list[#list + 1] = effect
			local stamp = rawget(_G, "JazzStampStatusEffectUIProps")
			if type(stamp) == "function" then
				stamp(effect, lJazzStatusEffectPresetId(effect, status_effects))
			end
		end
	end
	for _, id in ipairs({ "Tired", "Exhausted" }) do
		local effect = table.find_value(status_effects, "class", id)
		if effect and not table.find(list, effect) then
			list[#list + 1] = effect
		end
	end
	table.sort(list, function(a, b)
		local ida = lJazzStatusEffectPresetId(a, status_effects)
		local idb = lJazzStatusEffectPresetId(b, status_effects)
		local pa = (ida and JazzPartyStatusPriority[ida]) or 1000
		local pb = (idb and JazzPartyStatusPriority[idb]) or 1000
		if pa ~= pb then
			return pa < pb
		end
		local defa = ida and CharacterEffectDefs and CharacterEffectDefs[ida]
		local defb = idb and CharacterEffectDefs and CharacterEffectDefs[idb]
		local sa = (defa and defa.SortKey) or 0
		local sb = (defb and defb.SortKey) or 0
		return sa < sb
	end)
	return list
end

-- Combat badge / rollover: same Def-aware Shown+Icon resolution.
g_JAZZ_GetUIVisibleStatusEffectsBase = rawget(_G, "g_JAZZ_GetUIVisibleStatusEffectsBase") or false
g_JAZZ_GetUIVisibleStatusEffectsFn = rawget(_G, "g_JAZZ_GetUIVisibleStatusEffectsFn") or false

local function lInstallJazzGetUIVisibleStatusEffects()
	if not StatusEffectObject or type(StatusEffectObject.GetUIVisibleStatusEffects) ~= "function" then
		return
	end
	local our = rawget(_G, "g_JAZZ_GetUIVisibleStatusEffectsFn")
	if our and StatusEffectObject.GetUIVisibleStatusEffects == our then
		return
	end
	rawset(_G, "g_JAZZ_GetUIVisibleStatusEffectsBase", StatusEffectObject.GetUIVisibleStatusEffects)
	local function jazz_get_ui_visible_status_effects(self, addBadgeHidden)
		local vis = {}
		local effects = self.StatusEffects or empty_table
		for _, effect in ipairs(effects) do
			if effect then
				local shown = effect.Shown or lJazzStatusEffectDefProp(effect, effects, "Shown")
				local icon = effect.Icon or lJazzStatusEffectDefProp(effect, effects, "Icon")
				local hide = effect.HideOnBadge
				if hide == nil then
					hide = lJazzStatusEffectDefProp(effect, effects, "HideOnBadge")
				end
				if shown and icon and (addBadgeHidden or not hide) then
					local stamp = rawget(_G, "JazzStampStatusEffectUIProps")
					if type(stamp) == "function" then
						stamp(effect, lJazzStatusEffectPresetId(effect, effects))
						icon = effect.Icon or icon
					end
					if icon then
						vis[#vis + 1] = effect
					end
				end
			end
		end
		return vis
	end
	StatusEffectObject.GetUIVisibleStatusEffects = jazz_get_ui_visible_status_effects
	rawset(_G, "g_JAZZ_GetUIVisibleStatusEffectsFn", jazz_get_ui_visible_status_effects)
end

lInstallJazzGetUIVisibleStatusEffects()

function OnMsg.DataLoaded()
	lInstallJazzGetUIVisibleStatusEffects()
end

function OnMsg.ModsReloaded()
	lInstallJazzGetUIVisibleStatusEffects()
end