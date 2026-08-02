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
function JazzGetPartyPortraitStatusEffects(status_effects)
	local list = table.ifilter(status_effects or empty_table, "ShownSatelliteView")
	for _, id in ipairs({ "Tired", "Exhausted" }) do
		local effect = table.find_value(status_effects or empty_table, "class", id)
		if effect and not table.find(list, effect) then
			list[#list + 1] = effect
		end
	end
	return list
end