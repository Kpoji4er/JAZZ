function GetMeleeAttackAPCost(action, unit, args)
	local cost
	if action.CostBasedOnWeapon then
		local weapon = action:GetAttackWeapons(unit, args)	
		local knife = unit:GetItemInSlot("KnifeInventory", "StackableMeleeWeapon", 1, 1)
		--if knife then weapon = knife 
		print(knife)
		cost = (knife.weapon or weapon) and unit:GetAttackAPCost(action, weapon, nil, args and args.aim or 0, action.ActionPointDelta) or -1
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