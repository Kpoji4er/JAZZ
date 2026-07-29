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


function AIActionBasicAttack:PrecalcAction(context, action_state)
	local unit = context.unit
	local attack = context.default_attack

	if not attack then
		context.default_attack = context.default_attack_old or context.default_attack
		context.default_attack_cost = context.default_attack_cost_old or context.default_attack_cost
		attack = context.default_attack
	end

	if not attack then
		return
	end

	local target =
		context.attack_target or
		((context.dest_target or empty_table)[context.ai_destination])

	if not IsValidTarget(target) then
		return
	end

	local cost = context.default_attack_cost or attack.ap or 0
	if cost >= 0 and unit:HasAP(cost) then
		action_state.args = {
			target = target,
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




-- POL-001: ScoreMode for ally/enemy clustering (default preserves raw-distance math).
AppendClass.AIPolicyProximity = {
	properties = {
		{
			id = "ScoreMode",
			name = "Score Mode",
			help = "farther_better: higher distance score (legacy). closer_better: utility 1000/(1+dist).",
			editor = "choice",
			default = "farther_better",
			items = function()
				return { "closer_better", "farther_better" }
			end,
		},
	},
}

local function JazzAICoverThreatWeight(context, unit, enemy, dest)
	local weight = 40
	local epos = context.enemy_pack_pos_stance[enemy]
	if epos then
		local dist = Max(1, DivRound(stance_pos_dist(dest, epos), const.SlabSizeX))
		weight = 40 + DivRound(160, dist)
	end
	local best = context.best_attack
	if (best and best.target == enemy) or context.attack_target == enemy then
		weight = MulDivRound(weight, 150, 100)
	end
	if unit.IsThreatened and unit:IsThreatened({ enemy }) then
		weight = MulDivRound(weight, 130, 100)
	end
	return Max(1, weight)
end

local function JazzAICoverCanShot(context, dest, any_in_range)
	local dts = (context.dest_target_score or empty_table)[dest]
	if dts and dts > 0 then
		return true
	end
	if (context.dest_target or empty_table)[dest] then
		return true
	end
	return not not any_in_range
end

--- Evaluates cover with threat-weighted enemies and cover×shot composite (POL-001).
function AIPolicyTakeCover:EvalDest(context, dest, grid_voxel)
	local unit = context.unit
	local tbl = context.enemies or empty_table
	local x, y, z, stance = stance_pos_unpack(dest)
	local dest_pt = point(x, y, z)
	local score_acc = 0
	local threat_acc = 0
	local any_in_range = false
	local eff_range = context.EffectiveRange or context.ExtremeRange or 20

	for _, enemy in ipairs(tbl) do
		local visible = true
		if self.visibility_mode == "self" then
			visible = context.enemy_visible[enemy]
		elseif self.visibility_mode == "team" then
			visible = context.enemy_visible_by_team[enemy]
		end

		if visible then
			local epos = context.enemy_pack_pos_stance[enemy]
			if not epos then
				goto continue
			end

			local coverstd = GetCoverFrom(dest, epos)
			local base = self.CoverScores[coverstd] or 0

			local ex, ey, ez = point_unpack(epos)
			local enemy_pt = point(ex, ey, ez)
			if not enemy_pt:IsValidZ() then
				goto continue
			end

			local dist = Max(1, DivRound(stance_pos_dist(dest, epos), const.SlabSizeX))
			if dist <= eff_range then
				any_in_range = true
			end

			local _, any, coverage = GetCoverPercentage(dest_pt, enemy_pt, stance or "Crouch")
			coverage = coverage or 0

			local local_cover
			if not any or coverage < 30 then
				local_cover = MulDivRound(base, 10, 100)
			else
				local_cover = base + MulDivRound(base, coverage, 200)
			end

			local threat = JazzAICoverThreatWeight(context, unit, enemy, dest)
			score_acc = score_acc + local_cover * threat
			threat_acc = threat_acc + threat
		end
		::continue::
	end

	if threat_acc <= 0 then
		return 0
	end

	local cover_term = DivRound(score_acc, threat_acc)
	local shot_mult = JazzAICoverCanShot(context, dest, any_in_range) and 100 or 50
	return MulDivRound(cover_term, shot_mult, 100)
end

function AIPolicyTakeCover:GetEditorView()
	return "Seek Cover"
end

AIPolicyTakeCover.CoverScores = {
	[const.CoverPass] = 0,
	[const.CoverNone] = 0,
	[const.CoverLow] = 40,
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
			if enemy:IsSurrounded(context.position_override, context) then
				context.enemy_surrounded[enemy] = true
			end
		end
	end
	
	local delta = 0
	for _, enemy in ipairs(context.enemies) do
		if IsValid(enemy) and not enemy:IsDead() then
			local before = enemy:GetFlankThreat(context.enemy_surrounded, context)
			local after  = enemy:GetFlankThreat(context.position_override, context)
			delta = delta + (after - before)
		end
	end
    
    return delta * 100
end



--
--- Checks if the given unit is surrounded by enemy units.
---
--- @param unitReplace table|nil A table that maps units to their replacement positions. If provided, the function will use the replacement positions instead of the units' actual positions.
--- @return boolean true if the unit is surrounded, false otherwise
---
function Unit:IsSurrounded(unitReplace, context)
	if not g_Visibility or not g_Combat or self:IsDead() then
		return
	end

	if context and context.surrounded_cache and context.surrounded_cache[self] ~= nil then
		return context.surrounded_cache[self]
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
			if context and context.surrounded_cache then
		context.surrounded_cache[self] = false
	end
		return false
	end

	local pts = ConvexHull2D(enemy_pos)
	if not pts or #pts < 2 then
			if context and context.surrounded_cache then
		context.surrounded_cache[self] = false
	end
		return false
	end

	for i = 1, #pts - 1 do
		local v1 = pts[i]:Equal2D(pos) and point30 or SetLen(pts[i] - pos, guim)
		for j = i + 1, #pts do
			local v2 = pts[j]:Equal2D(pos) and point30 or SetLen(pts[j] - pos, guim)
			local dp = Dot2D(v1, v2)
			if dp < cosa then
				if context and context.surrounded_cache then context.surrounded_cache[self] = true end
				return true
			end
		end
	end	

		if context and context.surrounded_cache then
		context.surrounded_cache[self] = false
	end
	return false
end

function Unit:GetFlankThreat(unitReplace, context)
	if not g_Visibility or not g_Combat or self:IsDead() then
		return 0
	end

	if context and context.flank_threat_cache and context.flank_threat_cache[self] ~= nil then
		return context.flank_threat_cache[self]
	end

	local pos = unitReplace and unitReplace[self] or self:GetPos()
	if not IsPoint(pos) then
		if context and context.flank_threat_cache then context.flank_threat_cache[self] = 0 end
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

	if #enemy_pos < 2 then
		if context and context.flank_threat_cache then
			context.flank_threat_cache[self] = 0
		end
		return 0
	end

	local pts = ConvexHull2D(enemy_pos)
	if not pts or #pts < 2 then
		if context and context.flank_threat_cache then
			context.flank_threat_cache[self] = 0
		end
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

	if context and context.flank_threat_cache then context.flank_threat_cache[self] = max_flank end


	return max_flank
end--]]


--- Evaluates the destination position for an AI unit based on its proximity to target units.
---
--- @param context AIContext The current AI context.
--- @param dest point The destination position to evaluate.
--- @param grid_voxel point The grid voxel at the destination position.
--- @return number The score of the destination based on its proximity to target units.
function AIPolicyProximity:EvalDest(context, dest, grid_voxel)
	local unit = context.unit
	local target_enemies = self.TargetUnits == "enemies"
	local units = target_enemies and context.enemies or context.allies
	local tdist = self.TargetDist



	local height_decay_per_lvl = 0.7   -- 30% штраф за этаж
	local indoors_mult_single  =  1.15   -- буст, если только мы indoors
	local indoors_mult_both    =  1.25   -- если оба indoors
	local max_height_levels    =  5      -- кап на учёт этажей

	if #units < 3 then return end

	local score = nil          -- для min удобно начать с nil
	local count = 0
	local scale = const.SlabSizeX
  
	-- высота точки назначения по вокселю
	local vx_d, vy_d, vz_d = point_unpack(grid_voxel)
  
	-- indoors на точке назначения
	local dest_is_indoors = AICheckIndoors and AICheckIndoors(dest) or false
  
	for _, other in ipairs(units) do
	  if other ~= unit and not other:IsDead() then
		local upos
		if target_enemies then
		  upos = context.enemy_pack_pos_stance[other]
		else
		  upos = context.ally_pack_pos_stance[other]
		  if self.AllyPlannedPosition and other.ai_context then
			upos = other.ai_context.ai_destination or upos
		  end
		end
  
		if upos then
		  -- базовая горизонтальная дистанция (как раньше)
		  local dist = stance_pos_dist(dest, upos) / scale
  
		  -- разница по высоте (воксели → уровни)
		  local wx, wy, wz = stance_pos_unpack(upos)
		  local vx_o, vy_o, vz_o = WorldToVoxel(wx, wy, wz)
		  local dz_levels = abs((vz_o or vz_d) - vz_d)
		  dz_levels = Min(dz_levels or 0, max_height_levels)
  
		  -- прогрессивный штраф по высоте
		  local h_mult = height_decay_per_lvl ^ dz_levels
  
		  -- indoors-мультипликатор (снижает эффективную дистанцию)
		  local other_is_indoors = AICheckIndoors and AICheckIndoors(upos) or false
		  local ind_mult = 1
		  if dest_is_indoors and other_is_indoors then
			ind_mult = indoors_mult_both
		  elseif dest_is_indoors then
			ind_mult = indoors_mult_single
		  end
  
		  -- ВКЛАД ЭТОГО ЮНИТА: уже с применёнными множителями
		  local contrib = dist * h_mult / ind_mult
  
		  if tdist == "min" then
			-- берём минимум ПО УЖЕ ПРЕОБРАЗОВАННЫМ значениям
			score = (score == nil) and contrib or Min(score, contrib)
		  else
			score = (score or 0) + contrib
			count = count + 1
		  end
		end
	  end
	end
  
	if not score then return 0 end
	if tdist == "average" and count > 0 then
	  score = DivRound(score, count)
	end

	-- POL-001: closer_better converts distance into a utility; farther_better keeps legacy score.
	local mode = self.ScoreMode or "farther_better"
	if mode == "closer_better" then
		score = DivRound(1000, 1 + Max(0, score))
	end

	return score >= (self.MinScore or 0) and score or 0
  end


DefineClass.AIPolicyAvoidDeathZones = {
	__parents = { "AIPositioningPolicy", },
	__generated_by_class = "ClassDef",

	properties = {
		{ id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true },
		{ id = "TargetDist", name = "Death Distance", 
		  help = "Как далеко от трупа позиция считается опасной", 
		  editor = "number", default = 5, min = 1 },
		{ id = "Penalty", name = "Danger Penalty", 
		  help = "Штраф за нахождение в пределах опасной зоны", 
		  editor = "number", default = 100, min = 0 },
		  {id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true},
			{id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true}
	},
}

function AIPolicyAvoidDeathZones:EvalDest(context, dest, grid_voxel)
	local scale = const.SlabSizeX
	local penalty = 0
	local radius = self.TargetDist or 5
	local max_dist = radius

	local unit = context.unit
	local all_units = g_Units or empty_table

	local x, y, z = stance_pos_unpack(dest)
	local dest_pt = point(x, y, z)

	for _, other in ipairs(all_units) do
		if other ~= unit and other:IsDead() and not other:IsOnEnemySide(unit) then
			local death_pos = other:GetPos()
			if death_pos then
				local dist = dest_pt:Dist2D(death_pos) / const.SlabSizeX
				if dist <= max_dist then
					local mult = Clamp(1 - dist * 1.0 / max_dist, 0, 1)
					penalty = penalty + self.Penalty * mult
				end
			end
		end
	end

	return -penalty
end



function AIPolicyHighGround:EvalDest(context, dest, grid_voxel)
	local ux, uy, uz = point_unpack(context.unit_grid_voxel)
	local x, y, z = point_unpack(grid_voxel)
	local score = 100 * (z - uz)
	local penalty = 0
	local max_dist = 6
	local dest_pt = point(x, y, z)
	local unit = context.unit

	local all_units = g_Units or empty_table
	for _, other in ipairs(all_units) do
		if other ~= unit and not other:IsDead() and not other:IsOnEnemySide(unit) then

			local ox, oy, oz = other:GetPosXYZ()
			if oz == z then
				local dist = dest_pt:Dist2D(other:GetPos()) / const.SlabSizeX
				if dist <= max_dist then
					local mult = Clamp(1 - dist / max_dist, 0, 1)
					penalty = penalty + 30 * mult
				end
			end
		end
	end	


	return score - penalty
end




DefineClass.AITargetingEnemyWill = {
	__parents = { "AITargetingPolicy", },
	__generated_by_class = "ClassDef",

	properties = {
		{ id = "Score", 
			editor = "number", default = 100, },
		{ id = "Will", 
			editor = "number", default = 100, scale = "%", min = 1, max = 100, },
		{ id = "AboveWill", 
			editor = "bool", default = false, },
	},
}

function AITargetingEnemyWill:GetEditorView()
	if self.AboveWill then
		return string.format("Enemy Will >= %d%%", self.Will)
	end
	return string.format("Enemy Will <= %d%%", self.Will)
end

function AITargetingEnemyWill:EvalTarget(unit, target)
	local health_perc = MulDivRound(target.WillPoints, 100, target.MaxWillPoints)
	if self.AboveWill then
		return health_perc >= self.Will and self.Score or 0
	end
	return health_perc <= self.Will and self.Score or 0
end

----- POL-002: AllyRoleAnchor + AvoidPeekVoxel

DefineClass.AIPolicyAllyRoleAnchor = {
	__parents = { "AIPositioningPolicy" },
	properties = {
		{ id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true },
		{ id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true },
		{ id = "Mode", editor = "choice", default = "screen", items = function() return { "screen", "retinue" } end },
		{ id = "AnchorKeyword", editor = "choice", default = "Sniper", items = function() return { "Sniper", "Marksman", "Leader" } end },
		{ id = "MaxDist", editor = "number", default = 12, min = 1 },
	},
}

function AIPolicyAllyRoleAnchor:GetEditorView()
	return string.format("Ally anchor %s/%s", self.Mode, self.AnchorKeyword)
end

function AIPolicyAllyRoleAnchor:EvalDest(context, dest, grid_voxel)
	local unit = context.unit
	local team = unit.team
	if not team then
		return 0
	end
	local anchor
	for _, ally in ipairs(team.units) do
		if ally ~= unit and not ally:IsDead() then
			local keys = ally.AIKeywords or empty_table
			for _, k in ipairs(keys) do
				if k == self.AnchorKeyword then
					anchor = ally
					break
				end
			end
			if anchor then
				break
			end
		end
	end
	if not anchor then
		return 0
	end

	local ax, ay, az = stance_pos_unpack(context.ally_pack_pos_stance[anchor] or GetPackedPosAndStance(anchor))
	local dx, dy, dz = stance_pos_unpack(dest)
	local dist = DivRound(point(dx, dy, dz):Dist2D(point(ax, ay, az)), const.SlabSizeX)
	if dist > (self.MaxDist or 12) then
		return 0
	end

	if self.Mode == "retinue" then
		return Max(0, 100 - dist * 8)
	end

	-- screen: prefer dest between anchor and nearest enemy
	local enemy = GetNearestEnemy(anchor)
	if not enemy then
		return Max(0, 60 - dist * 5)
	end
	local ex, ey, ez = enemy:GetPosXYZ()
	local to_enemy = point(ex, ey, ez):Dist2D(point(ax, ay, az))
	local to_dest = point(dx, dy, dz):Dist2D(point(ax, ay, az))
	local dest_to_enemy = point(dx, dy, dz):Dist2D(point(ex, ey, ez))
	if to_dest < to_enemy and dest_to_enemy < to_enemy then
		return 100 - dist * 5
	end
	return Max(0, 40 - dist * 4)
end

DefineClass.AIPolicyAvoidPeekVoxel = {
	__parents = { "AIPositioningPolicy" },
	properties = {
		{ id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true },
		{ id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true },
		{ id = "Penalty", editor = "number", default = 80, min = 0 },
		{ id = "Radius", editor = "number", default = 1, min = 0 },
	},
}

function AIPolicyAvoidPeekVoxel:GetEditorView()
	return "Avoid peek voxels"
end

function AIPolicyAvoidPeekVoxel:EvalDest(context, dest, grid_voxel)
	local penalty = 0
	local radius = self.Radius or 1
	local dx, dy, dz = stance_pos_unpack(dest)
	local dest_pt = point(dx, dy, dz)
	local function consider(pos)
		if not pos then
			return
		end
		local dist = DivRound(dest_pt:Dist2D(pos), const.SlabSizeX)
		if dist <= radius then
			penalty = penalty + self.Penalty
		end
	end
	consider(context.unit and context.unit.last_attack_pos)
	for _, enemy in ipairs(context.enemies or empty_table) do
		consider(enemy.last_attack_pos)
	end
	return -penalty
end

----- POL-003: optional Weightable ally spacing (mirrors JazzAI_AllySpacingScore)

DefineClass.AIPolicyAllySpacing = {
	__parents = { "AIPositioningPolicy" },
	properties = {
		{ id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true },
		{ id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true },
		{ id = "MinDist", editor = "number", default = 2, min = 1 },
		{ id = "Penalty", editor = "number", default = 50, min = 0 },
		{ id = "AllyPlannedPosition", editor = "bool", default = true },
	},
}

function AIPolicyAllySpacing:GetEditorView()
	return string.format("Ally spacing min %d", self.MinDist or 2)
end

function AIPolicyAllySpacing:EvalDest(context, dest, grid_voxel)
	if JazzAI_AllySpacingScore then
		return JazzAI_AllySpacingScore(context, dest, self.MinDist or 2, self.Penalty or 50)
	end
	return 0
end
