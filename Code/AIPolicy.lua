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
    function AIPolicyAttackAP:EvalDest(context, dest, grid_voxel)
        local unit = context.unit
        local ap = context.dest_ap[dest] or 0
    
        if context.best_attack then
            if ap > context.best_attack.ap then
                return 120
            elseif ap >= context.best_attack.ap then
                return 110
            end
        elseif ap > context.default_attack_cost then
            return 100
        elseif ap >= context.default_attack_cost then
            return 90
        else
            return 0
        end
    end

end


function AIActionBasicAttack:PrecalcAction(context, action_state)
	local unit = context.unit
	local attack = context.default_attack

	if not attack.target then
		print("❌ BasicAttack: No target in default_attack")
		context.default_attack = context.default_attack_old or context.default_attack 
		context.default_attack_cost = context.default_attack_cost_old or context.default_attack_cost
		attack = context.default_attack
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

	-- распаковка позиции назначения
	local x, y, z, stance = stance_pos_unpack(dest)
	local dest_pt = point(x, y, z)

	for _, enemy in ipairs(tbl) do
		local visible = true
		if self.visibility_mode == "self" then
			visible = context.enemy_visible[enemy]
		elseif self.visibility_mode == "team" then
			visible = context.enemy_visible_by_team[enemy]
		end

		if visible then
			local packed_enemy = context.enemy_pack_pos_stance[enemy]
			if not packed_enemy then goto continue end

            local x, y, z = point_unpack(packed_enemy)
            local enemy_pt = point(x, y, z)
            if not enemy_pt:IsValidZ() then goto continue end

			local cover, any, coverage = GetCoverPercentage(dest_pt, enemy_pt, stance or "Crouch")
			cover = cover or const.CoverNone

			local weight = Max(1, 100 - coverage)
			local cover_score = self.CoverScores[cover] or 0
			local localscore = DivRound(cover_score, weight)
			score = score + localscore
		end
		::continue::
	end

	return score / Max(1, #tbl)
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



--- Evaluates the desirability of a destination location for the AIPolicyFlanking policy.
---
--- @param context AIContext The AI context for the current unit.
--- @param dest point The destination location to evaluate.
--- @param grid_voxel point The grid voxel for the destination location.
--- @return number The score for the destination based on the ability to flank enemies.
function AIPolicyFlanking:EvalDest(context, dest, grid_voxel)
	local unit = context.unit
	
	local ap = context.dest_ap[dest] or 0
	if self.ReserveAttackAP and ap < context.default_attack_cost then
		return 0
	end
	
	if not context.position_override then
		context.position_override = {}
		if self.AllyPlannedPosition then
			for _, ally in ipairs(unit.team.units) do
				local dest = ally.ai_context and ally.ai_context.ai_destination
				if dest then
					local x, y, z = stance_pos_unpack(dest)
					context.position_override[ally] = point(x, y, z)
				end
			end
		end
	end
	
	local x, y, z = stance_pos_unpack(dest)
	context.position_override[unit] = point(x, y, z)
	
	if not context.enemy_surrounded then
		context.enemy_surrounded = {}
		for _, enemy in ipairs(context.enemies) do
			if enemy:IsSurrounded() then
				context.enemy_surrounded[enemy] = true
			end
		end
	end
	
    local delta = 0
    for _, enemy in ipairs(context.enemies) do
        if IsValid(enemy) and not enemy:IsDead() then
            local before = enemy:GetFlankThreat(context.enemy_surrounded)
            local after  = enemy:GetFlankThreat(context.position_override)
            delta = delta + (after - before)
        end
    end
    
    return delta * self.Weight
end


--
--- Checks if the given unit is surrounded by enemy units.
---
--- @param unitReplace table|nil A table that maps units to their replacement positions. If provided, the function will use the replacement positions instead of the units' actual positions.
--- @return boolean true if the unit is surrounded, false otherwise
---
function Unit:IsSurrounded(unitReplace)
	if not g_Visibility or not g_Combat or self:IsDead() then
		return
	end
	
	local pos = unitReplace and unitReplace[self] or self:GetPos()
	local enemy_pos = {}
	local angle = 120*60
	local cosa = MulDivRound(cos(angle), guim*guim, 4096)

	for _, team in ipairs(g_Teams) do
		if team.side ~= "neutral" then
			for _, u in ipairs(team.units) do
				if u:CanSurround(self, unitReplace and unitReplace[u]) then
					enemy_pos[#enemy_pos + 1] = unitReplace and unitReplace[u] or u:GetPos()
				end
			end
		end
	end
	if #enemy_pos < 2 then
		return
	end

	local pts = ConvexHull2D(enemy_pos)
	if not pts or #pts < 2 then
		return false
	end

	for i = 1, #pts - 1 do
		local v1 = pts[i]:Equal2D(pos) and point30 or SetLen(pts[i] - pos, guim)
		for j = i + 1, #pts do
			local v2 = pts[j]:Equal2D(pos) and point30 or SetLen(pts[j] - pos, guim)
			local dp = Dot2D(v1, v2)
			if dp < cosa then
				return true
			end
		end
	end	
end

function Unit:GetFlankThreat(unitReplace)
	if not g_Visibility or not g_Combat or self:IsDead() then
		return 0
	end

	local pos = unitReplace and unitReplace[self] or self:GetPos()
	if not IsPoint(pos) then
		print("Invalid pos in GetFlankThreat", pos)
		return 0
	end
	
	local enemy_pos = {}

	for _, team in ipairs(g_Teams) do
		if team.side ~= "neutral" then
			for _, u in ipairs(team.units) do
				local repl = unitReplace and IsPoint(unitReplace[u]) and unitReplace[u] or nil
				if u:CanSurround(self, repl) then
					enemy_pos[#enemy_pos + 1] = repl or u:GetPos()
				end
			end
		end
	end

	if #enemy_pos < 2 then return 0 end

	local pts = ConvexHull2D(enemy_pos)
	if not pts or #pts < 2 then
		return 0
	end
	
	local max_flank = 0
	local cos30 = MulDivRound(cos(30 * 60), guim * guim, 4096)

	for i = 1, #pts - 1 do
		local pi = pts[i]
		if not pi then goto continue_i end
		
		local v1 = pi:Equal2D(pos) and point30 or SetLen(pi - pos, guim)
	
		for j = i + 1, #pts do
			local pj = pts[j]
			if not pj then goto continue_j end
			local v2 = pj:Equal2D(pos) and point30 or SetLen(pj - pos, guim)
			local dp = Dot2D(v1, v2)
	
			if dp < cos30 then
				local flank = Clamp((cos30 - dp) / (cos30 + guim * guim), 0, 1)
				if flank > max_flank then
					max_flank = flank
				end
			end
			::continue_j::
		end
		::continue_i::
	end

	return max_flank
end