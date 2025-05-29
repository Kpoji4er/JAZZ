DefineClass.AIPolicyCustomFlanking = {
    __parents = {"AIPositioningPolicy"},
    __generated_by_class = "ClassDef",

    properties = {
        {id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true}, {
            id = "ReserveAttackAP",
            name = "Reserve Attack AP",
            help = "do not consider locations where the unit will be out of ap and couldn't attack",
            editor = "choice",
            default = false,
            items = function(self)
                return {"AP", "Stance", false}
            end
        }, {
            id = "visibility_mode",
            name = "Visibility Mode",
            editor = "choice",
            default = "self",
            items = function(self)
                return {"self", "team", "all"}
            end
        },
        {id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true},
        {id = "OnlyTarget", editor = "bool", default = false, read_only = false, no_edit = false},
        {
            id = "ScalePerDistance",
            editor = "bool",
            default = false,
            read_only = false,
            no_edit = false
        }
    }
}

local debug = false
local draw_debug = false

local function IsInCover(unit, enemy, cover_data, los_data)

    local cover_penalty =
        Presets["ChanceToHitModifier"]["Default"]["RangeAttackTargetStanceCover"]:ResolveValue(
            "Cover")

    if not los_data or (not los_data[enemy] or los_data[enemy] == 0) then
        return true, cover_penalty, "No LOS"
    end

    if cover_data and cover_data[enemy] then
        return true, cover_data[enemy]
    end

    return false
end

local function CompareCovers(enemy, current_pos_cover_data, new_pos_cover_data)
    local cover_penalty =
        Presets["ChanceToHitModifier"]["Default"]["RangeAttackTargetStanceCover"]:ResolveValue(
            "Cover")

    local current_cover_cth = current_pos_cover_data[enemy].cover_cth or 0
    local new_cover_cth = new_pos_cover_data[enemy].cover_cth or 0
    local new_ratio = new_cover_cth * 1.00 / cover_penalty
    local current_ratio = current_cover_cth * 1.00 / cover_penalty

    local cover_difference = current_ratio - new_ratio
    return cover_difference
end

---- Args
local effective_range_mul = 1.00
local distance_impact = 0.25
local extra_target_weight = 100
local unit_weight = 100
----

function AIPolicyCustomFlanking:GetEnemyWeight(unit, enemy, dist, effective_range, target)
    local weight = unit_weight
    if target and enemy == target then
        weight = weight + extra_target_weight
    end

    if self.ScalePerDistance then
        weight = MulDivRound(weight, Max(0,
                                         unit_weight - ((dist * 1.00) / (effective_range * 1.00)) *
                                             (100 * distance_impact)), 100)
    end
    return weight
end

function AIPolicyCustomFlanking:EvalDest(context, dest, grid_voxel)
    local unit = context.unit
    local ap = context.dest_ap[dest] or 0
    local attack_ap = context.default_attack_cost or 0
    if ap < attack_ap then return 0 end

    local x, y, z = stance_pos_unpack(dest)
    local new_pos = point(x, y, z)

    local effective_range = (context.EffectiveRange or 30) * const.SlabSizeX
    local target = context.dest_target[dest]
    local target_only = self.OnlyTarget
    local scale = self.ScalePerDistance

    local enemies = {}
    local weights = {}

    -- [1] Собираем релевантных врагов + вес
    for _, enemy in ipairs(context.enemies or empty_table) do
        if not target_only or enemy == target then
            local dist = new_pos:Dist(enemy:GetPos())
            if dist <= effective_range then
                local visible = true
                if self.visibility_mode == "self" then
                    visible = context.enemy_visible[enemy]
                elseif self.visibility_mode == "team" then
                    visible = context.enemy_visible_by_team[enemy]
                end

                if visible then
                    local weight = 100
                    if enemy == target then weight = weight + extra_target_weight end
                    if scale and effective_range > 0 then
                        local dist_factor = Clamp(1 - (dist / effective_range), 0, 1)
                        weight = MulDivRound(weight, dist_factor * 100, 100)
                    end
                    weights[enemy] = weight
                    enemies[#enemies+1] = enemy
                end
            end
        end
    end

    -- [2] Оценка укрытия — просто: если нет укрытия от врага, +вес
    local cover_data = context.dest_target_cover_score[dest] or empty_table
    local los_data = context.dest_target_los[dest] or empty_table

    local score = 0
    for _, enemy in ipairs(enemies) do
        local los = los_data[enemy]
        local cover = cover_data[enemy] or 0
        if los and los > 0 and cover < 50 then
            score = score + (weights[enemy] or 100)
        end
    end

    return score
end

--[[function AIPolicyCustomFlanking_IndividualTarget:EvalDest(context, dest, grid_voxel)

    local unit = context.unit

    local ap = context.dest_ap[dest] or 0
    if self.ReserveAttackAP and ap < context.default_attack_cost then
        return 0
    end

    local target = context.dest_target[dest]

    if not target then

        return 0
    end
    ic(target.session_id)

    local target_in_cover = IsInCover(unit, target)
    local new_target_in_cover = IsInCover(unit, target, dest)

    return (target_in_cover and not new_target_in_cover) and self.Weight or 0
end]]

--[[function Update_AICoverLOS_currentpos(unit, current_pos_arg)
    local context = unit.ai_context
    local context_copy = table.copy(unit.ai_context)
    local current_pos = current_pos_arg or context.unit_stance_pos -- stance_pos_pack(unit:GetPos())
    if current_pos then
        if not context.dest_target_cover_score[current_pos] or
            not context.dest_target_los[current_pos] then
            print("-- not current_pos", GameTime())
            AIPrecalcDamageScore(context_copy, {current_pos})

            context.dest_target_cover_score[current_pos] =
                context_copy.dest_target_cover_score[current_pos]
            context.dest_target_los[current_pos] = context_copy.dest_target_los[current_pos]
            -- unit.ai_context = context
            return context
        end

    end
    return nil
end]]
