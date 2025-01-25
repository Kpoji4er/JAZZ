function RATOAI_UnpackPos(pos)
    if not pos then
        return
    end
    local ux, uy, uz, ustance_idx = stance_pos_unpack(pos)
    local new_pos = point(ux, uy, uz)
    return new_pos
end

DefineClass.AIPolicyCustomSeekCover = {
    __parents = {"AIPositioningPolicy"},
    __generated_by_class = "ClassDef",

    properties = {
        {id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true},
        {id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true},
        {
            id = "visibility_mode",
            name = "Visibility Mode",
            editor = "choice",
            default = "team",
            items = function(self)
                return {"self", "team", "all"}
            end
        },
        {
            id = "ScalePerDistance",
            editor = "bool",
            default = false,
            read_only = false,
            no_edit = false
        }, {
            id = "ForceCheckLastEnemyPos",
            editor = "bool",
            default = false,
            read_only = false,
            no_edit = false
        }, {
            id = "ExposedAtCloseRange_Score",
            editor = "number",
            default = -30,
            read_only = false,
            no_edit = false
        }
    }
}

----- Args
local distance_impact = 1.00
local max_range = 30
local min_dist = 5 * const.SlabSizeX
local pb_range = const.Weapons.PointBlankRange * const.SlabSizeX
local close_range = ((const.Weapons.PointBlankRange * 2) + (1)) * const.SlabSizeX
local close_range_mul = 75

local extra_score_arg_mul = 220
-----

function AIPolicyCustomSeekCover:GetEditorView()
    return "Custom Seek Cover"
end

function AIPolicyCustomSeekCover:EvalDest(context, dest, grid_voxel)
    local score = 0

    -- local ux, uy, uz, ustance_idx = stance_pos_unpack(dest)
    if not dest then
        return score
    end

    local tbl = context.enemies or empty_table

    ----
    local table_num = 0 -- #tbl
    local extra_mul = self.ScalePerDistance and extra_score_arg_mul or 100
    ----

    for _, enemy in ipairs(tbl) do
        local visible = true
        if self.visibility_mode == "self" then
            visible = context.enemy_visible[enemy]
        elseif self.visibility_mode == "team" then
            visible = context.enemy_visible_by_team[enemy]
        end

        if visible then
            table_num = table_num + 1
            local cover = GetCoverFrom(dest, context.enemy_pack_pos_stance[enemy])
            local cover_score = self:GetCoverScore(context, self.CoverScores[cover] or 0, dest,
                                                   grid_voxel, enemy)

            score = score + cover_score
        end
    end

    ------------- If possible, need to check direction
    if self.ForceCheckLastEnemyPos or table_num < 1 then
        local last_pos = context.unit.last_known_enemy_pos
        -- DbgAddCircle(last_pos)
        if last_pos then
            local cover = GetCoverFrom(dest, stance_pos_pack(last_pos))
            local cover_score = self:GetCoverScore(context, self.CoverScores[cover] or 0, dest,
                                                   last_pos)

            table_num = table_num + 1
            score = score + cover_score
        end
    end

    return MulDivRound(score / Max(1, table_num), extra_mul, 100)
end

function AIPolicyCustomSeekCover:GetCoverScore(context, cover_score, dest, grid_voxel, enemy)

    if not dest then
        return cover_score
    end

    local new_pos, dist
    if self.ScalePerDistance and cover_score > 0 then
        new_pos = RATOAI_UnpackPos(dest)
        new_pos = IsValidZ(new_pos) and new_pos or new_pos:SetTerrainZ()
        if enemy then
            local enemy_pos = IsValid(enemy) and enemy:GetPos() or enemy
            new_pos = IsValidZ(enemy_pos) and enemy_pos or enemy_pos:SetTerrainZ()
        end

        if enemy_pos and enemy then
            dist = Max(min_dist, new_pos:Dist(enemy_pos))
            local range = max_range * const.Scale.AP
            local ratio = 100 - ((Min(range, dist) * 1.00) / (range * 1.00)) *
                              (100 * distance_impact)

            cover_score = MulDivRound(cover_score, ratio, 100)
        end
        -- print(enemy.session_id, dist / const.SlabSizeX, cover_score1, cover_score, ratio)
    end

    if self.ExposedAtCloseRange_Score ~= 0 and cover_score <= 0 and context.enemy_grid_voxel[enemy] and
        grid_voxel and enemy then

        local x1, y1, z1 = point_unpack(context.enemy_grid_voxel[enemy])
        local x2, y2, z2 = point_unpack(grid_voxel)
        if IsCloser(x1, y1, z1, x2, y2, z2, pb_range + 1) then
            cover_score = self.ExposedAtCloseRange_Score
        elseif IsCloser(x1, y1, z1, x2, y2, z2, close_range + 1) then
            cover_score = MulDivRound(self.ExposedAtCloseRange_Score, close_range_mul, 100)
        end

        -- print(enemy.session_id, cover_score)
    end

    -- if new_pos then
    --     DbgAddText(enemy.session_id .. " " .. cover_score, new_pos)
    -- end

    return cover_score
end

AIPolicyCustomSeekCover.CoverScores = {
    [const.CoverPass] = 0,
    [const.CoverNone] = 0,
    [const.CoverLow] = 50,
    [const.CoverHigh] = 100
}

--[[function AIPolicyCustomSeekCover:EvalDest(context, dest, grid_voxel)
    local score = 0

    local ux, uy, uz, ustance_idx = stance_pos_unpack(dest)

    local tbl = context.enemies or empty_table

    ---
    local denominador = 0
    local total_score = 0
    ---
    for _, enemy in ipairs(tbl) do
        local visible = true
        if self.visibility_mode == "self" then
            visible = context.enemy_visible[enemy]
        elseif self.visibility_mode == "team" then
            visible = context.enemy_visible_by_team[enemy]
        end

        if visible then

            local cover = GetCoverFrom(dest, context.enemy_pack_pos_stance[enemy])
            local cover_score = self.CoverScores[cover] or 0

            -------------
            total_score = total_score + cover_score
            denominador = denominador + 1

            local cover_score1 = cover_score
            if self.ScalePerDistance and cover_score > 0 then
                local ux, uy, uz, ustance_idx = stance_pos_unpack(dest)
                local new_pos = point(ux, uy, uz)

                local dist = new_pos:Dist(enemy:GetPos())
                local range = max_range * const.Scale.AP
                local ratio = 100 - ((Min(range, dist) * 1.00) / (range * 1.00)) *
                                  (100 * distance_impact)

                cover_score = MulDivRound(cover_score, ratio, 100)
                print(enemy.session_id, dist / const.SlabSizeX, cover_score1, cover_score, ratio)

            end

            -------------
            score = score + cover_score

        end
    end

    local score_ratio = 0
    if total_score > 0 then
        total_score = total_score / Max(1, denominador)
        -- score = score / Max(1, denominador)

        local ux, uy, uz, ustance_idx = stance_pos_unpack(dest)
        local new_pos = point(ux, uy, uz)

        score_ratio = ((score * 1.00) / (total_score * 1.00)) * 100
        DbgAddText(total_score .. " / " .. score .. " = " .. score_ratio, new_pos)
    end

    local final_score = MulDivRound(self.Score, score_ratio, 100)
    ic(total_score, score, final_score)
    return score / Max(1, #tbl)
end]]
