DefineClass.AIPolicyTryNotToBeFlanked = {
    __parents = {"AIPositioningPolicy"},
    __generated_by_class = "ClassDef",

    properties = {
        {id = "end_of_turn", editor = "bool", default = true, read_only = true, no_edit = true},
        {id = "optimal_location", editor = "bool", default = true, read_only = true, no_edit = true}
    }
}

local function atan2(y, x)
    if x > 0 then return math.atan(y / x)
    elseif x < 0 and y >= 0 then return math.atan(y / x) + math.pi
    elseif x < 0 and y < 0 then return math.atan(y / x) - math.pi
    elseif x == 0 and y > 0 then return math.pi / 2
    elseif x == 0 and y < 0 then return -math.pi / 2
    else return 0 end
end

local function GetThreatDirections(unit, dest, enemies)
    local x, y, z = stance_pos_unpack(dest)
    local pos = point(x, y)
    if not x or not y then return 4 end  -- максимально опасно если позиция сломана


    local threat_dirs = {}  -- например: { "N", "S", "E" }

    for _, enemy in ipairs(enemies) do
        local ex, ey = enemy:GetPos():xy()
        local dx, dy = ex - x, ey - y

        local angle = atan2(dy, dx) * 180 / math.pi

        local dir
        if angle > -45 and angle <= 45 then
            dir = "E"
        elseif angle > 45 and angle <= 135 then
            dir = "N"
        elseif angle <= -45 and angle > -135 then
            dir = "S"
        else
            dir = "W"
        end

        if not threat_dirs[dir] then
            if CheckLOS(enemy, pos, enemy:GetSightRadius()) then
                threat_dirs[dir] = true
            end
        end
    end

    local open_flanks = 0
    for _, val in pairs(threat_dirs) do
        if val then open_flanks = open_flanks + 1 end
    end

    return open_flanks
end

function AIPolicyTryNotToBeFlanked:EvalDest(context, dest, grid_voxel)
    local unit = context.unit

    -- local is_surrounded = unit:IsSurrounded()
    local x, y, z = stance_pos_unpack(dest)
    local pos_table = {}
    local new_pos = point(x, y, z)
    pos_table[unit] = new_pos
    local open_flanks = GetThreatDirections(unit, dest, context.enemies)

    -- Чем меньше флангов — тем лучше. 0 = идеально. 3–4 = плохо.
    return Clamp(4 - open_flanks, 0, 4) * 100
end

function Unit:RATOAI_IsSurrounded(unitReplace)
    if not g_Visibility or not g_Combat or self:IsDead() then
        return
    end

    local pos = unitReplace and unitReplace[self] or self:GetPos()
    local enemy_pos = {}
    local angle = 120 * 60
    local cosa = MulDivRound(cos(angle), guim * guim, 4096)

    for _, team in ipairs(g_Teams) do
        if team.side ~= "neutral" then
            for _, u in ipairs(team.units) do
                ------------------------------------------------------------
                if u:RATOAI_CanSurround(self, unitReplace and unitReplace[u], pos) then
                    ------------------------------------------------------------
                    enemy_pos[#enemy_pos + 1] = unitReplace and unitReplace[u] or u:GetPos()
                end
            end
        end
    end
    if #enemy_pos < 2 then
        return
    end
    local pts = ConvexHull2D(enemy_pos)

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

function Unit:RATOAI_CanSurround(other, check_pos, custom_other_pos)
    -- side
    if not self:IsOnEnemySide(other) or self:IsDead() or self:IsDowned() then
        return false
    end

    -- status effects
    if self:HasStatusEffect("Suppressed") then
        return false
    end

    -- Not valid gameplay wise, but happens in some rare cases and fires asserts down the line.
    local pos = check_pos or self:GetPos()
    if other:GetPos() == pos then
        return false
    end

    -- visibility
    if check_pos then
        -- checking from another position, use CheckLOS
        if not CheckLOS(other, self, self:GetSightRadius()) then
            return false
        end
        ------------------------------------------------------------
    elseif custom_other_pos then
        if not CheckLOS(custom_other_pos, self, self:GetSightRadius()) then
            return false
        end
        ------------------------------------------------------------
    else
        -- checking from current position, can use precomputed visibility
        if not HasVisibilityTo(self, other) then
            return false
        end
    end

    -- weapon range
    local adjacent = self:IsAdjacentTo(other, check_pos)
    local in_range = false
    local w1, w2, weapons = self:GetActiveWeapons()
    for _, weapon in ipairs(weapons) do
        if IsKindOf(weapon, "Firearm") or (IsKindOf(weapon, "MeleeWeapon") and weapon.CanThrow) then
            -- heavy weapons are Firearms and go here too
            in_range = in_range or other:GetDist(pos) <= weapon.WeaponRange * const.SlabSizeX
        elseif IsKindOf(weapon, "MeleeWeapon") then
            in_range = in_range or adjacent
        end
    end

    return in_range
end
