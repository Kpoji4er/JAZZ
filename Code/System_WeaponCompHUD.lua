-- JAZZ-UI-002: FoldStock / Flashlight HUD helpers for UIWeaponDisplay col2 chips.
-- Top-level globals are registered at Code load (safe); do not create new _G keys later.

function JazzWeaponCompIdLooksUnfolded(comp_id)
	if type(comp_id) ~= "string" then
		return false
	end
	return string.find(comp_id, "UnFolded", 1, true)
		or string.find(comp_id, "UnFold", 1, true)
		or string.find(comp_id, "Unfold", 1, true)
end

function JazzWeaponCompIdLooksFolded(comp_id)
	if type(comp_id) ~= "string" then
		return false
	end
	if JazzWeaponCompIdLooksUnfolded(comp_id) then
		return false
	end
	return string.find(comp_id, "Folded", 1, true)
		or string.find(comp_id, "Fold", 1, true)
end

function JazzWeaponCompHasFoldingPair(comp_id)
	local wc = comp_id and WeaponComponents and WeaponComponents[comp_id]
	local pair = wc and wc.zzFoldingPair
	local partner = pair and pair[1]
	return type(partner) == "string" and partner ~= ""
end

function JazzWeaponCompIdLooksFlashOff(comp_id)
	if type(comp_id) ~= "string" then
		return false
	end
	return string.find(comp_id, "Off", 1, true) ~= nil
end

--- Resolve enabled fold/unfold CombatAction for the unit's active firearm Stock.
--- @return CombatAction|nil, "enabled"|"disabled"|"hidden", reason?
function JazzResolveFoldStockAction(unit)
	if not unit then
		return nil, "hidden"
	end
	local weapon = unit:GetActiveWeapons()
	if not IsKindOf(weapon, "Firearm") then
		return nil, "hidden"
	end
	local stock_id = weapon.components and weapon.components.Stock
	if not JazzWeaponCompHasFoldingPair(stock_id) then
		return nil, "hidden"
	end
	local action
	if JazzWeaponCompIdLooksUnfolded(stock_id) then
		action = CombatActions.FoldStock
	elseif JazzWeaponCompIdLooksFolded(stock_id) then
		action = CombatActions.UnFoldStock
	else
		return nil, "hidden"
	end
	if not action then
		return nil, "hidden"
	end
	local state, reason = action:GetUIState({ unit })
	return action, state, reason
end

--- Resolve enabled flashlight CombatAction for the unit's active firearm Side.
function JazzResolveFlashlightAction(unit)
	if not unit then
		return nil, "hidden"
	end
	local weapon = unit:GetActiveWeapons()
	if not IsKindOf(weapon, "Firearm") then
		return nil, "hidden"
	end
	local side_id = weapon.components and weapon.components.Side
	if not JazzWeaponCompHasFoldingPair(side_id) then
		-- Fallback: known flashlight ids without authored pair still toggle via action gates.
		if not side_id then
			return nil, "hidden"
		end
	end
	local action
	if JazzWeaponCompIdLooksFlashOff(side_id) then
		action = CombatActions.FlashlightOn
	elseif side_id and (string.find(side_id, "Flashlight", 1, true) or string.find(side_id, "Flash", 1, true)) then
		action = CombatActions.FlashlightOff
	else
		return nil, "hidden"
	end
	if not action then
		return nil, "hidden"
	end
	local state, reason = action:GetUIState({ unit })
	return action, state, reason
end

function JazzWeaponCompToggleUIBegin(kind)
	local unit = Selection and Selection[1]
	if not unit or not unit:CanBeControlled() then
		return
	end
	local action, state
	if kind == "stock" then
		action, state = JazzResolveFoldStockAction(unit)
	elseif kind == "flashlight" then
		action, state = JazzResolveFlashlightAction(unit)
	end
	if action and state == "enabled" then
		action:UIBegin({ unit })
	end
end
