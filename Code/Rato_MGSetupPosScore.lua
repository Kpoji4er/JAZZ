DefineClass.AIPolicyMGSetupPosScore = {
    __parents = {"AIPositioningPolicy"},
    __generated_by_class = "ClassDef",

    properties = {
        {id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true}, {
            id = "ReserveAPforCrouchProne",
            name = "Reserve AP for Stance change",
            help = "do not consider locations where the unit will be out of ap and will not be able to change stance to crouching or going prone",
            editor = "bool",
            default = false
        },
        {id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true}

    }
}

-----TODO: completely refactor this
function AIPolicyMGSetupPosScore:EvalDest(context, dest, grid_voxel)

    local ap = context.dest_ap[dest] or 0

    local check_ap = self.ReserveAPforCrouchProne and 2000 or 0

    if ap < check_ap then
        return 0
    end

    local unit = context.unit
    local current_pos = context.unit_stance_pos
    context = Update_AIPrecalcDamageScore(unit) or context

    local score = 0

    local weapon = context.weapon or unit:GetActiveWeapons()
    local x, y, z = stance_pos_unpack(dest)
    local new_pos = point(x, y, z)

    local enemies = 0
    for enemy, pos in pairs(context.enemy_pos) do
        if not enemy:IsDowned() and context.enemy_visible[enemy] and IsValidPos(pos) and
            IsValidPos(new_pos) then

            local angle = GetShootingAngleDiff(unit, weapon, enemy, true)
            enemies = enemies + 1
            score = RATOAI_GetEnemyCoverScore(unit, enemy, context, score, new_pos, pos, nil, angle)
        end
    end
    return score / Max(1, enemies)
end
