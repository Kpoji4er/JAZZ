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
	return (ap > context.best_attack.ap and 120) or (ap >= context.best_attack.ap and 110) or (ap > context.default_attack_cost and 100) or (ap >= context.default_attack_cost and 9) or 0
end


function AIActionBasicAttack:PrecalcAction(context, action_state)
	local unit = context.unit
	local attack = context.default_attack

	if not attack.target then
		print("❌ BasicAttack: No target in default_attack")
	end

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

function AIActionBasicAttack:IsAvailable(context, action_state)
	return action_state.has_ap
end

function AIActionBasicAttack:Execute(context, action_state)
	assert(action_state.has_ap)
	
	AIPlayCombatAction(context.default_attack.id, context.unit, nil, action_state.args)
end





---
--- Evaluates the destination position for the AI policy to take cover.
---
--- @param context table The AI context, containing information about the unit, allies, enemies, and other relevant data.
--- @param dest table The destination position, represented as a 3D point.
--- @param grid_voxel table The grid voxel associated with the destination.
--- @return number The calculated score for the destination.
function AIPolicyTakeCover:EvalDest(context, dest, grid_voxel)
	local score = 0
	local unit = context.unit
	local tbl = context.enemies or empty_table

	for _, enemy in ipairs(tbl) do

		local visible = true
		if self.visibility_mode == "self" then
			 visible = context.enemy_visible[enemy]
		elseif  self.visibility_mode == "team" then
			visible = context.enemy_visible_by_team[enemy]
		end
		if visible then
			--local cover = GetCoverFrom(dest, context.enemy_pack_pos_stance[enemy])
			local enemy_pos = context.enemy_pack_pos_stance[enemy]
			local cover, any, coverage = unit:GetCoverPercentage(dest, enemy_pos)
			local dist = dest:Dist(enemy_pos) / const.SlabSizeX
			local proximity = Clamp(10 - dist, 1, 10)



			local weight = Max(1, 100 - coverage)
			local localscore = DivRound(cover_score * proximity, weight)

			print("cover =", cover, "coverage =", coverage, "distance =", dist)
			print("localscore =", localscore)
			score = score + localscore
		end
	end

	return  score / Max(1, #tbl)
end

---
--- Returns a string describing the editor view for the AIPolicyTakeCover class.
---
--- @return string The editor view description.
function AIPolicyTakeCover:GetEditorView()
	return "Seek Cover"
end

----- AIPolicyTakeCover CoverScores

AIPolicyTakeCover.CoverScores = { 
	[const.CoverPass] = 0, 
	[const.CoverNone] = 0, 
	[const.CoverLow] = 50,
	[const.CoverHigh] = 100,
}

