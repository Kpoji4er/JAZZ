-- DefineClass.AIPolicyAvoidThreatenedAreas = {
--     __parents = {"AIPositioningPolicy"},
--     __generated_by_class = "ClassDef",
--     properties = {
--         {id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true},
--         {id = "CheckLOS", editor = "bool", default = true}
--     }
-- }
-- function AIPolicyAvoidThreatenedAreas:EvalDest(context, dest, grid_voxel)
--     local enemy
--     local enemy_ow = g_Overwatch[enemy]
-- @ dist
-- @ cone_angle
-- @ target_pos 
-- @ orient or or CalcOrientation(enemy:GetPos(), enemy_ow.target_pos)
-- end
--------------------------

function _AIFindDestinations(unit, context)
    local pos = GetPassSlab(unit) or unit:GetPos()
    local destinations, paths, dest_ap, dest_path, voxel_to_dest, closest_free_pos =
        AIBuildArchetypePaths(unit, pos, context)
    if not closest_free_pos then
        if unit.ActionPoints == 0 then
            assert(not "AI try to act with 0 action points!!!")
        else
            print("AI can't find unit free destination prints!!!")
            printf("      AP = %d", unit.ActionPoints)
            printf("      Command = %s", unit.command)
            printf("      Status effects: %s", table.concat(table.keys(unit.StatusEffects), ", "))
            printf("      Pos: %s", tostring(unit:GetPos()))
            printf("      Pass slab pos: %s", tostring(GetPassSlab(unit) or ""))
            printf("      Target dummy pos %s",
                   unit.target_dummy and tostring(unit.target_dummy:GetPos()) or "")
            local o = GetOccupiedBy(unit:GetPos(), unit)
            if o then
                printf("Other pos %s", tostring(o:GetPos()))
                printf("Other target dummy pos %s",
                       o.target_dummy and tostring(o.target_dummy:GetPos()) or "")
                printf("Other efResting=%d", o:GetEnumFlags(const.efResting))
                if o.reposition_dest then
                    printf("Other reposition dest=%s",
                           tostring(point(stance_pos_unpack(o.reposition_dest))))
                end
            end
            assert(not "AI can't find unit free destination")
        end
    end
    local crouch_idx = StancesList.Crouch
    local important_dests = context.important_dests or {}
    context.important_dests = important_dests
    local change_stance_costs = {}
    for stance_idx in ipairs(StancesList) do
        change_stance_costs[stance_idx] = GetStanceToStanceAP(StancesList[stance_idx], "Crouch")
    end

    -- preprocess destinations to find those where we need to change stance at the dest to take cover
    local low = const.CoverLow
    -- local high = const.CoverHigh
    for i, dest in ipairs(destinations) do
        local x, y, z, stance_idx = stance_pos_unpack(dest)
        if stance_idx ~= crouch_idx then
            local cost = change_stance_costs[stance_idx]
            local ap = dest_ap[dest]
            if cost and ap and ap >= cost then
                local up, right, down, left = GetCover(x, y, z)
                if up then
                    local cover_low = up == low or right == low or down == low or left == low
                    -- local cover_high = up == high or right == high or down == high or left == high
                    if cover_low then -- and not cover_high then
                        table.remove_value(important_dests, dest)
                        local new_dest = stance_pos_pack(x, y, z, crouch_idx)
                        destinations[i] = new_dest
                        voxel_to_dest[point_pack(x, y, z)] = new_dest
                        dest_ap[new_dest] = ap - cost
                        dest_path[new_dest] = dest_path[dest]
                        table.insert_unique(important_dests, new_dest)
                    end
                end
            end
        end
    end

    context.destinations = destinations -- available destinations
    context.dest_ap = dest_ap -- dest -> available ap
    context.combat_paths = paths
    context.dest_combat_path = dest_path -- dest -> index in context.combat_paths (to reach this dest)
    context.voxel_to_dest = voxel_to_dest
    context.closest_free_pos = closest_free_pos

    context.all_destinations = AIEnumValidDests(context)
end

function _AIFindOptimalLocation(context, dest_score_details)
    if context.best_dest then
        -- optimal location doesn't change across behaviors, no need to recalc it
        return context.best_dest
    end

    
    local unit = context.unit
    context.best_dests = {}

    local r = context.archetype.OptLocSearchRadius * const.SlabSizeX
    local ux, uy, uz = point_unpack(context.unit_grid_voxel)
    local px, py, pz = VoxelToWorld(ux, uy, uz)
    local bbox = box(px - r, py - r, 0, px + r + 1, py + r + 1, MapSlabsBBox_MaxZ)
    context.best_score = 0
    local unit_voxels = {}
    local dest_scores = {}

    local sees_enemy = false
for _, enemy in ipairs(context.enemies or empty_table) do
    if context.enemy_visible and context.enemy_visible[enemy] then
        sees_enemy = true
        break
    end
end

    local policies = table.ifilter(context.archetype.OptLocPolicies, function(idx, policy)
        return policy:MatchUnit(unit)
    end)

    local effective_range = context.EffectiveRange * 2
    if not effective_range then
        effective_range = sees_enemy and 40 or 60
    elseif effective_range <= 40 then
        effective_range = effective_range + (sees_enemy and 20 or 60)
    end

    effective_range = effective_range * (sees_enemy and 2 or 4.0)

    local multiplier = sees_enemy and 1.1 or 1.0

-- модификаторы погоды/ночи
if GameState.Night then
    multiplier = multiplier * (sees_enemy and 1.1 or 1.5)
end
if GameState.Fog then
    multiplier = multiplier * (sees_enemy and 1.05 or 1.3)
end
if GameState.DustStorm then
    multiplier = multiplier * (sees_enemy and 1.0 or 1.2)
end
if GameState.FireStorm then
    multiplier = multiplier * 1.1
end
if GameState.RainHeavy then
    multiplier = multiplier * (sees_enemy and 1.05 or 1.25)
end

effective_range = effective_range * multiplier

    local max_dist = effective_range * const.SlabSizeX

--    local max_dist = (context.EffectiveRange or (50 + InteractionRand(20, "max_dist"))) * const.SlabSizeX  -- максимум дистанции до позиции
    local max_positions =  InteractionRand(500, "max_positions") + 500               -- максимум позиций на оценку
    local filtered_dests = {}
    
    -- Фильтрация по расстоянию и AP
    for _, dest in ipairs(context.all_destinations) do
        local x, y, z = stance_pos_unpack(dest)
        local dist = context.unit:GetPos():Dist2D(point(x, y))
        local ap = context.dest_ap and context.dest_ap[dest] or 0
        if dist <= max_dist and (not ap or ap >= 0) then
            table.insert(filtered_dests, dest)
        end
    end

    
    if #filtered_dests == 0 then
        -- fallback: просто берём 1–2 ближайшие точки вообще
        filtered_dests = table.copy(context.all_destinations or {})
        table.shuffle(filtered_dests)
    end
    
    -- Обрежем до ближайших 40 точек
    --table.sort(filtered_dests, function(a, b)
    --    local ax, ay = stance_pos_unpack(a)
    --    local bx, by = stance_pos_unpack(b)
     --   return context.unit:GetPos():Dist2D(point(ax, ay)) < context.unit:GetPos():Dist2D(point(bx, by))
    --end)
    local trimmed = table.slice(filtered_dests, 1, max_positions)


    for _, dest in ipairs(trimmed) do
        local x, y, z = stance_pos_unpack(dest)
        local gx, gy, gz = WorldToVoxel(x, y, z)
        local world_voxel = point_pack(x, y, z)
        local grid_voxel = point_pack(gx, gy, gz)
        -- eval_voxel(x, y, z, context, ux, uy, uz)

        if not context.voxel_to_dest[world_voxel] then
            context.voxel_to_dest[world_voxel] = dest
        end
        local scores
        if dest_score_details then
            scores = {}
            dest_score_details[dest] = scores
        end
        table.iclear(unit_voxels)
        local score = AIScoreDest(context, policies, dest, grid_voxel, 0, unit_voxels, scores)
        score = score + InteractionRand(5, "AIChoiceNoise")
        if score > 0 then
            context.best_score = Max(context.best_score, score)
            local threshold = MulDivRound(context.best_score, const.AIDecisionThreshold, 100)
            if score >= threshold then
                dest_scores[dest] = score
                context.best_dests[#context.best_dests + 1] = dest
                for i = #context.best_dests, 1, -1 do
                    local dest = context.best_dests[i]
                    if dest_scores[dest] < threshold then
                        table.remove(context.best_dests, i)
                    end
                end
            end
        end
        if scores then
            scores.final_score = score
        end
    end

    table.shuffle(context.best_dests)


    -- check if a best dest candidate is on our starting voxel, default to it
    for _, dest in ipairs(context.best_dests) do
        if stance_pos_dist(context.unit_stance_pos, dest) == 0 then
            context.best_dest = dest
        end
    end

    if not context.best_dest and #(context.best_dests or empty_table) > 0 then
        if #(context.best_dests or empty_table) > 15 then
            context.collapsed = CollapsePoints(context.best_dests, 1)
        else
            context.collapsed = context.best_dests
        end
        local pf_dests = {}
        for i, dest in ipairs(context.collapsed) do
            local x, y, z = stance_pos_unpack(dest)
            pf_dests[i] = point(x, y, z)
        end

        context.best_dest_path = pf.GetPosPath(unit, pf_dests)
        if #(context.best_dest_path or empty_table) > 0 then
            local voxel = point_pack(SnapToPassSlabXYZ(context.best_dest_path[1]))
            local dest = context.voxel_to_dest[voxel]
            if not dest then
                -- try non-snapped
                voxel = point_pack(context.best_dest_path[1])
                dest = context.voxel_to_dest[voxel]
            end
            -- assert(dest and (not dest_score_details or dest_score_details[dest]))
            context.best_dest = dest
        end
    end

    context.dest_scores = dest_scores
    context.best_dest = context.best_dest or context.voxel_to_dest[context.unit_world_voxel] or
                            context.unit_stance_pos
    if context.dest_combat_path[context.best_dest] then
        table.insert_unique(context.important_dests, context.best_dest)
        table.insert_unique(context.destinations, context.best_dest)
    end
    if not context.best_dest then
        print("DEBUG: Fallback to standing position")
        context.best_dest = context.unit_stance_pos
    end
    return context.best_dest
end
