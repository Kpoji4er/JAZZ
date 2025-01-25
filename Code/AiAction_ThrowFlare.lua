DefineClass.AIActionThrowFlare = {
    __parents = {"AIActionBaseZoneAttack"},
    properties = {
        {id = "MinDist", editor = "number", scale = "m", default = 2 * guim, min = 0},
        {id = "MaxDist", editor = "number", scale = "m", default = 100 * guim, min = 0}, --  {
        --     id = "AllowedAoeTypes",
        --     editor = "set",
        --     items = {"none", "fire", "smoke", "teargas", "toxicgas"},
        --     default = set("none")
        -- },
        {id = "TargetLastAttackPos", editor = "bool", default = false}
    },
    hidden = false,
    voice_response = "AIThrowGrenade"

}

function AIActionThrowFlare:PrecalcAction(context, action_state)
    local action_id, grenade
    local actions = {"ThrowGrenadeA", "ThrowGrenadeB", "ThrowGrenadeC", "ThrowGrenadeD"}
    for _, id in ipairs(actions) do
        local caction = CombatActions[id]
        local cost = caction and caction:GetAPCost(context.unit) or -1
        if cost > 0 and context.unit:HasAP(cost) then
            action_id = id
            local weapon = caction:GetAttackWeapons(context.unit)
            local aoetype = weapon.aoeType or "none"
            ---
            if IsKindOf(weapon, "FlareStick") or IsKindOf(weapon, "GlowStick") then
                grenade = weapon
                break
            end
            ---
        end
    end

    -- if not grenade then
    --     action_id = 'ThrowGrenadeA'
    --     grenade = context.unit:GetItemInSlot("Inventory", "FlareStick")
    -- end

    if not action_id or not grenade then
        return
    end

    local max_range = Min(self.MaxDist, grenade:GetMaxAimRange(context.unit) * const.SlabSizeX)
    local blast_radius = grenade.AreaOfEffect * const.SlabSizeX
    local target_pts
    if self.TargetLastAttackPos then
        -- collect enemy last attack positions and pass them as target_pos array to AIPrecalcGrenadeZones
        for _, enemy in ipairs(context.enemies) do
            if enemy.last_attack_pos then
                target_pts = target_pts or {}
                target_pts[#target_pts + 1] = enemy.last_attack_pos
            end
        end
    end
    local zones = AIPrecalcFlareZones(context, action_id, self.MinDist, max_range, blast_radius,
                                      grenade.aoeType, target_pts)
    local zone, score = self:EvalZones(context, zones)
    if zone then
        action_state.action_id = action_id
        action_state.target_pos = zone.target_pos
        action_state.score = score
    end
end

function AIActionThrowFlare:IsAvailable(context, action_state)
    return not not action_state.action_id
end

function AIActionThrowFlare:Execute(context, action_state)
    assert(action_state.action_id and action_state.target_pos)
    AIPlayCombatAction(action_state.action_id, context.unit, nil, {target = action_state.target_pos})
end

local function IsUnitInTheDark(hit)
    if not IsKindOf(hit.obj, "Unit") then
        return false
    end

    if hit.obj:HasStatusEffect("Darkness") then
        return true
    end

    return false
end

function AIPrecalcFlareZones(context, action_id, min_range, max_range, blast_radius, aoeType,
                             target_pts)
    if context.target_locked then
        return {}
    end

    if not target_pts then
        target_pts = AICalcAOETargetPoints(context, min_range, max_range, blast_radius)
    else
        -- make sure the target points are within the allowed range
        AIFilterTargetPoints(context.unit, target_pts, min_range, max_range)
    end

    -- calculate parabolas and affected units to each target point
    local zones = {}
    local action = CombatActions[action_id]
    local args = {target = false}
    for i, target_pt in ipairs(target_pts) do
        args.target = target_pt
        local results = action:GetActionResults(context.unit, args)
        local units
        local trajectory = results.trajectory or empty_table
        local pos = #trajectory > 0 and trajectory[#trajectory].pos or results.target_pos
        if pos and (aoeType == "smoke" or aoeType == "toxicgas" or aoeType == "teargas") then
            local water = terrain.IsWater(pos) and terrain.GetWaterHeight(pos)
            if not (water and (not pos:IsValidZ() or water >= pos:z())) then
                pos = SnapToPassSlab(pos) or pos
                local dx, dy = 1, 1
                for i = #trajectory - 1, 1, -1 do
                    local step = trajectory[i]
                    if step.pos:Dist2D(pos) > 0 then
                        local px, py = step.pos:xy()
                        local x, y = pos:xy()
                        dx = (px == x) and 1 or ((x - px) / abs(x - px))
                        dy = (py == y) and 1 or ((y - py) / abs(y - py))
                        break
                    end
                end

                local gx, gy, gz = WorldToVoxel(pos)
                local smoke, blocked = PropagateSmokeInGrid(gx, gy, gz, dx, dy)
                local smoke_voxels = {}
                for _, wpt in pairs(smoke) do
                    local ppos = point_pack(WorldToVoxel(wpt))
                    smoke_voxels[ppos] = true
                end

                for _, unit in ipairs(g_Units) do
                    local _, head = unit:GetVisualVoxels()
                    if smoke_voxels[head] then
                        units = units or {}
                        table.insert(units, unit)
                    end
                end
            end
        else
            for _, hit in ipairs(results) do
                if IsUnitInTheDark(hit) then
                    units = units or {}
                    table.insert(units, hit.obj)
                end
            end
        end
        if units then
            zones[#zones + 1] = {target_pos = target_pt, units = units}
        end
    end

    -- print("grenade targeting precalc in", GetPreciseTicks() - tstart, "ms")
    return zones
end
