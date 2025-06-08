UndefineClass('AIPolicyAttackAP')
DefineClass.AIPolicyAttackAP = {
	__parents = { "AIPositioningPolicy", },
	__generated_by_class = "ClassDef",

	properties = {
		{ id = "end_of_turn", 
			editor = "bool", default = true, read_only = true, no_edit = true, },
	},
}

--- Evaluates the destination for the AI policy to attack with available action points.
---
--- @param context AIContext The current AI context.
--- @param dest number The destination tile index.
--- @param grid_voxel GridVoxel The grid voxel at the destination.
--- @return number The score for the destination based on available action points.
function AIPolicyAttackAP:EvalDest(context, dest, grid_voxel)
	local unit = context.unit
	
	local ap = context.dest_ap[dest] or 0
	return ap > context.default_attack_cost and 100 or 0
end


function AIActionBasicAttack:PrecalcAction(context, action_state)
	local unit = context.unit
	local attack = context.default_attack
	if not attack or not IsValidTarget(attack.target) then
		print("AIActionBasicAttack: invalid target", attack.target)

		return
	end
	
	local cost = context.default_attack_cost or attack.ap or 0
	if cost >= 0 and unit:HasAP(cost) then
		action_state.args = {
			target = attack.target,
			aim = attack.aim or 0,
			target_spot_group = attack.target_spot_group,
		}
		action_state.has_ap = true
	end
end