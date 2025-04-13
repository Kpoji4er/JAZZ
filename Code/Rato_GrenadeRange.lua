DefineClass.AIPolicyGrenadeRange = {
    __parents = {"AIPositioningPolicy"},
    __generated_by_class = "ClassDef",

    properties = {
        {id = "CheckLOS", editor = "bool", default = true}, {
            id = "EnvState",
            name = "Environmental State",
            editor = "set",
            default = false,
            three_state = true,
            items = function(self)
                return AIEnvStateCombo
            end
        }, {
            id = "RangeMin",
            name = "Preferred Range (Min)",
            help = "Percent of base preferred range",
            editor = "number",
            default = 80,
            min = 0,
            max = 1000
        }, {
            id = "RangeMax",
            name = "Preferred Range (Max)",
            help = "Percent of base preferred range",
            editor = "number",
            default = 120,
            min = 0,
            max = 1000
        }, {
            id = "DownedWeightModifier",
            name = "Downed Enemy Weight Modifier",
            editor = "number",
            default = 5,
            scale = "%",
            min = 0
        }, {
            id = "AllowedAoeTypes",
            editor = "set",
            items = {"none", "fire", "smoke", "teargas", "toxicgas"},
            default = set("none")
        }, {id = "SaveAP", editor = "bool", default = false},
        {id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true},
        {id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true}
    }
}

----TODO: probably need to check visibility and save ap?
----TODO: add a check to all positioning behaviors, if same position as start then dont use
---- Sometimes positioning behavior uses a position with a bit less score?

function AIPolicyGrenadeRange:GetEditorView()
    return string.format("Be in %d%% to %d%% of grenade range", self.RangeMin, self.RangeMax)
end

function AIPolicyGrenadeRange:EvalDest(context, dest, grid_voxel)
    if self.CheckLOS and not g_AIDestEnemyLOSCache[dest] then
        return 0
    end

    for state, value in pairs(self.EnvState) do
        if value ~= not not GameState[state] then
            return 0
        end
    end
    local enemy_grid_voxel = context.enemy_grid_voxel
    local range_type = "Weapon" -- "Absolute" --self.RangeBase
    local range_min = self.RangeMin
    local range_max = self.RangeMax
    local weight = 0
    for _, enemy in ipairs(context.enemies) do
        if self:RangeCheckGrenade(context, grid_voxel, enemy, enemy_grid_voxel[enemy], range_type,
                                  range_min, range_max, dest) then
            if enemy:IsIncapacitated() then
                weight = self.DownedWeightModifier
            else
                return 100
            end
        end
    end
    return weight
end

function AIPolicyGrenadeRange:RangeCheckGrenade(context, ppt1, target, ppt2, range_type, range_min,
                                                range_max, dest)

    local base_range, cost_check = self:GetGrenadeMaxRangeAndAPcost(context)

    if not base_range then
        return false
    end

    if self.SaveAP and cost_check and cost_check >= 0 then
        local ap = context.dest_ap[dest]
        if ap < cost_check then
            return false
        end
    end

    range_min = range_min and MulDivRound(range_min, base_range, 100)
    range_max = range_max and MulDivRound(range_max, base_range, 100)

    local x1, y1, z1 = point_unpack(ppt1)
    local x2, y2, z2 = point_unpack(ppt2)
    if (range_min or 0) > 0 and IsCloser(x1, y1, z1, x2, y2, z2, range_min) then
        return false
    end
    if (range_max or 0) > 0 and not IsCloser(x1, y1, z1, x2, y2, z2, range_max + 1) then
        return false
    end
    return true
end

function AIPolicyGrenadeRange:GetGrenadeMaxRangeAndAPcost(context)

    local function set_to_table(sett)
        local ttable = {}
        for k, b in pairs(sett) do
            if b then
                table.insert_unique(ttable, k)
            end
        end
        if not next(ttable) then
            return false
        end
        return ttable
    end

    local function any_value_in_table(table1, table2)
        for i, v in ipairs(table1) do
            if table.find(table2, v) then
                return true
            end
        end
        return false
    end

    local archetype = context and context.archetype
    for i, sig in ipairs(archetype.SignatureActions) do
        if sig.class == "AIActionThrowGrenade" then
            local aoetype = set_to_table(sig.AllowedAoeTypes) or {"none"}
            local triggerType =  {"Contact"}
            local self_aoe_type = set_to_table(self.AllowedAoeTypes) or {"none"}
            local self_trigger_type =  {"Contact"}

            if any_value_in_table(self_aoe_type, aoetype) and
                any_value_in_table(self_trigger_type, triggerType) then
                return RATOAI_GetGrenadeActionMaxRangeAndApCost(context, sig, self.SaveAP)
            end
        end
    end
    return false
end

function RATOAI_GetGrenadeActionMaxRangeAndApCost(context, signature, check_ap)
    local max_range, cost
    local actions = { "ThrowGrenadeA", "ThrowGrenadeB", "ThrowGrenadeC", "ThrowGrenadeD","ThrowGrenadeAG", "ThrowGrenadeBG", "ThrowGrenadeCG", "ThrowGrenadeDG","ThrowGrenadeAO", "ThrowGrenadeBO" }
    for _, id in ipairs(actions) do
        local caction = CombatActions[id]
        local actcost = check_ap and (caction and caction:GetAPCost(context.unit) or -1)
        local weapon = caction and caction:GetAttackWeapons(context.unit)
        if weapon then
            local aoetype = weapon.aoeType or "none"
            ----
            local triggerType = "Contact"
            ----
            if weapon and IsKindOf(weapon, "Grenade") then
                max_range = caction:GetMaxAimRange(context.unit, weapon)
                cost = actcost
                break
            end
        end
    end

    return max_range
end

