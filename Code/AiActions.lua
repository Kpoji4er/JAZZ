function AIActionThrowGrenade:PrecalcAction(context, action_state)
    local action_id, grenade
    local actions = {
        "ThrowGrenadeA", "ThrowGrenadeB", "ThrowGrenadeC", "ThrowGrenadeD",
        "ThrowGrenadeAG", "ThrowGrenadeBG", "ThrowGrenadeCG", "ThrowGrenadeDG",
        "ThrowGrenadeAO", "ThrowGrenadeBO"
    }

    for _, id in ipairs(actions) do
        local caction = CombatActions[id]
        local cost = caction and caction:GetAPCost(context.unit) or -1
        if cost > 0 and context.unit:HasAP(cost) then
            action_id = id
            local weapon = caction:GetAttackWeapons(context.unit)
            local aoetype = weapon.aoeType or "none"
            if IsKindOfClasses(weapon, "Grenade", "Ordnance", "Flare",
                               "GrenadeItem", "Molotov") and
                self.AllowedAoeTypes[aoetype] then
                grenade = weapon
                break
            end
        end
    end

    if not action_id or not grenade then return end

    local max_range = Min(self.MaxDist, grenade:GetMaxAimRange(context.unit) *
                              const.SlabSizeX)
    local blast_radius = grenade.AreaOfEffect * const.SlabSizeX
    local is_smoke = (grenade.aoeType or "none") == "smoke"
        and (self.BiasId == "SmokeGrenade"
            or (self.AllowedAoeTypes and self.AllowedAoeTypes.smoke and not self.AllowedAoeTypes.none))

    local target_pts
    if is_smoke and JazzAI_CollectSmokeCurtainTargets then
        context.jazz_smoke_blast = blast_radius
        target_pts = JazzAI_CollectSmokeCurtainTargets(context, self.MinDist, max_range,
            blast_radius)
    elseif self.TargetLastAttackPos then
        for _, enemy in ipairs(context.enemies) do
            if enemy.last_attack_pos then
                target_pts = target_pts or {}
                target_pts[#target_pts + 1] = enemy.last_attack_pos
            end
        end
    end
    local zones = AIPrecalcGrenadeZones(context, action_id, self.MinDist,
                                        max_range, blast_radius,
                                        grenade.aoeType, target_pts)
    -- Curtain landings may not put any head in the cloud; keep those target points.
    if is_smoke and JazzAI_EnsureSmokeZones then
        zones = JazzAI_EnsureSmokeZones(context, action_id, target_pts, zones, grenade.aoeType)
    end

    local zone, score = self:EvalZones(context, zones)
    if zone then
        action_state.action_id = action_id
        action_state.target_pos = zone.target_pos
        action_state.score = score
    end
end

function AIFilterTargetPoints(unit, target_pts, min_range, max_range)

    --print(#target_pts)
    for i = #target_pts, 1, -1 do
        local dist = unit:GetDist(target_pts[i])
        if dist == 0 or (max_range and dist > max_range) then
            table.remove(target_pts, i)
        elseif min_range and min_range < max_range and dist < min_range then
            table.remove(target_pts, i)
        end
    end

    -- print(target_pts)
end

local function IsUnitHit(hit)
    if not IsKindOf(hit.obj, "Unit") then return false end
    -- print("damage "..hit.damage)
    if hit.damage > 0 then return true end
    for _, effect in ipairs(hit.effects) do
        if effect and effect ~= "" then return true end
    end
    --return true
end

function AIPrecalcGrenadeZones(context, action_id, min_range, max_range,
                               blast_radius, aoeType, target_pts)
    if context.target_locked then return {} end

    if not target_pts then
        target_pts = AICalcAOETargetPoints(context, min_range, max_range,
                                           blast_radius)
    else
        -- make sure the target points are within the allowed range
        AIFilterTargetPoints(context.unit, target_pts, min_range, max_range)
    end

    -- print(target_pts)
    -- calculate parabolas and affected units to each target point
    local zones = {}
    local action = CombatActions[action_id]
    local args = {target = false}
    for i, target_pt in ipairs(target_pts) do
        args.target = target_pt
        local results = action:GetActionResults(context.unit, args)

        local units
        local trajectory = results.trajectory or empty_table
        -- print("trajectory")
        -- print(aoeType)
        local pos = #trajectory > 0 and trajectory[#trajectory].pos or
                        results.target_pos
        if pos and
            (aoeType == "smoke" or aoeType == "toxicgas" or aoeType == "teargas" or
                aoeType == "fire") then
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
            ----print(results)
            for _, hit in ipairs(results) do
                ----print(hit)
                if IsUnitHit(hit) then
                    -- print("hit!")
                    units = units or {}
                    table.insert(units, hit.obj)
                end
            end
        end
        if units then
            zones[#zones + 1] = {target_pos = target_pt, units = units}
        end
    end

    -- print("--print(zones) ")
    -- print(zones)
    ----print("grenade targeting precalc in", GetPreciseTicks() - tstart, "ms")
    return zones
end

function AIReloadWeapons(unit)
    if IsMerc(unit) then return end

    local action = unit:GetDefaultAttackAction()
    local weapon1, weapon2 = action:GetAttackWeapons(unit)
    -- Clear jam only: never pass Condition (0..100) into RepairJammed — that API
    -- takes absolute WeaponResource units and would collapse e.g. 9695 → ≤100.
    -- NPC/AI free-clear; player Unjam still uses Mechanical roll + fail wear (1–3% max).
    if weapon1 and weapon1.jammed then
        weapon1:RepairJammed(nil, unit)
        unit.Mechanical = unit.Mechanical + 1;
    end
    if weapon2 and weapon2.jammed then
        weapon2:RepairJammed(nil, unit)
        unit.Mechanical = unit.Mechanical + 1;
    end
    --	target:SetActionCommand("ChangeStance", nil, nil, "Prone")
    -- if weapon1 and weapon1.jammed then unit:SetActionCommand("UnjamWeapon", self.id, nil)  end
    -- unit:SetActionCommand("UnjamWeapon", self.id, ap, args) 
    -- if weapon2 and weapon2.jammed then unit:SetActionCommand("UnjamWeapon", self.id, nil)  end

    local firearms = select(3, unit:GetActiveWeapons("Firearm"))
    table.iappend(firearms, select(3, unit:GetActiveWeapons("HeavyWeapon")))
    for _, firearm in ipairs(firearms) do
        if not firearm.ammo then
            local ammos = unit:GetAvailableAmmos(firearm) or empty_table
            ----print(ammos)
            local ammo
            if #ammos > 0 then
                if unit:CanAddItem("AmmoInventory", ammos[1]) then
                    unit:TryEquip("AmmoInventory", ammos[1])
                    ammo = ammos[1]
                else
                    ammo = PlaceInventoryItem(ammos[1].id)
                end
                ammo.Amount = firearm.MagazineSize
                unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
                CreateFloatingText(unit, T(160472488023, "Reload"))
                ObjModified(unit)
            else
                ammos = GetAmmosWithCaliber(firearm.Caliber, "sorted")
                if #ammos > 0 then
                    if unit:CanAddItem("AmmoInventory", ammos[1]) then
                        unit:TryEquip("AmmoInventory", ammos[1])
                        ammo = PlaceInventoryItem(ammos[1].id)
                    else
                        ammo = PlaceInventoryItem(ammos[1].id)
                    end
                    ammo.Amount = firearm.MagazineSize
                    unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
                    CreateFloatingText(unit, T(160472488023, "Reload"))
                    DoneObject(ammo)
                    ObjModified(unit)
                end
            end
        elseif firearm.ammo.Amount < Max(1, firearm.MagazineSize / 2) then    
  --      elseif firearm.ammo.Amount < Max(1, 
        
  --      table.find(firearm.AvailableAttacks, "AutoFire") and firearm.Autoshots or
  --      table.find(firearm.AvailableAttacks, "MGBurstFire") and firearm.BurstShots * 2 
  --      or table.find(firearm.AvailableAttacks, "BurstFire") and firearm.BurstShots or 1 ) then
            local ammo = firearm.ammo
            ammo.Amount = firearm.MagazineSize
            unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
            CreateFloatingText(unit, T(160472488023, "Reload"))
            ObjModified(unit)
            -- DoneObject(ammo)
        end
    end
end

function AICalcAttacksAndAim(context, ap, target)

    -- local skill = (self[weapon.base_skill]+self["Dexterity"]*2+self:GetLevel()*10)/3
    -- if IsKindOf(weapon, "MachineGun") then local skill = (self[weapon.base_skill]*2+self["Dexterity"]+self["Strength"]+self:GetLevel()*10)/4 end

    -- local unit = context.Unit
    -- local target = context.target
    local weapon = context.weapon

    ----print(unit)
    ----print(target)
    ----print(weapon)

    -- local base = unit:CalcChanceToHit

    -- if GameState.RainHeavy then
    --	aim_cost = MulDivRound(aim_cost, 100 + const.EnvEffects.RainAimingMultiplier, 100)
    -- end
    local min_aim, max_aim = context.unit:GetBaseAimLevelRange(
                                 context.default_attack, false)

    local cost = context.default_attack_cost
    local num_attacks = Min(ap / cost, context.max_attacks)

    local remaining = ap - num_attacks * cost
    local aims = {}

    local attack_idx = 1
    local unit = context.unit

    local aim = 0

     if IsKindOfClasses(context.weapon,"SniperRifle") then local aim = max_aim end
    -- if IsKindOfClasses(context.weapon,"AssaultRifle","MachineGun","SubmachineGun","Shotgun","Pistol") then local aim = Clamp(Unit:Random(3),min_aim, max_aim) end

    local aim_cost = const.Scale.AP

    ----print('EffectiveRange'..context.EffectiveRange)

    -- if target then
    --	if context.force_max_aim 
    --	or (IsKindOfClasses(context.weapon,"SniperRifle","MachineGun") and (ap - cost * max_aim) > 0 and unit:GetDist(target) >= 2*const.SlabSizeX)
    --	or ((IsKindOf(context.weapon,"AssaultRifle")) and (ap - cost * max_aim) > 0 and unit:GetDist(target) >= (4) * const.SlabSizeX) 
    --	or ((IsKindOf(context.weapon,"SubmachineGun")) and (ap - cost * max_aim) > 0 and unit:GetDist(target) >= (Min(context.weapon.BulletDropRange,8)) * const.SlabSizeX) 
    --	or ((IsKindOf(context.weapon,"Pistol")) and (ap - cost * max_aim) > 0 and unit:GetDist(target) >= (Min(context.weapon.BulletDropRange,8)) * const.SlabSizeX) 
    --	or ((IsKindOf(context.weapon,"Shotgun")) and (ap - cost * max_aim) > 0 and unit:GetDist(target) >= (Min(context.weapon.BulletDropRange,8)) * const.SlabSizeX) 
    --	   then
    --		num_attacks = Min(Max(1,(ap / (cost + aim_cost * max_aim))), context.max_attacks)
    --		local aim = max_aim
    --		aims[attack_idx] = aim
    --		return num_attacks, aims
    --	end
    --
    --	if unit:GetDist(target) <= 3*const.SlabSizeX then
    --		local num_attacks = Min(ap / cost)	
    --		local aim = min_aim or 0
    --		aims[attack_idx] = aim
    --		return num_attacks, aims
    --	end
    -- end
    local args = {aim = 0}

    if context.force_max_aim then
        num_attacks = Min(ap / (cost + aim_cost * max_aim), context.max_attacks)
    end

    local cthtreshold = 100
    -- if IsKindOfClasses(context.weapon,"SniperRifle") then cthtreshold = 100 end
    -- if IsKindOfClasses(context.weapon,"SubmachineGun","Shotgun","Pistol") then cthtreshold = 50 end

    while remaining > (2 * aim_cost) do
        local aim = (aims[attack_idx] or 0)

        if context.unit then
            local cth = context.unit:CalcChanceToHit(target,
                                                     context.default_attack)
            while cth < 100 and aim <= (max_aim) and remaining > aim_cost do
                aim = aim + 1
                remaining = remaining - aim_cost
                args.aim = aim
                cth = context.unit:CalcChanceToHit(target,
                                                   context.default_attack, args)
            end
            -- print('aim '..aim.." cth "..cth)
        end

        if aim > context.weapon.MaxAimActions then break end
        aims[attack_idx] = aim
        attack_idx = attack_idx + 1
        if attack_idx > num_attacks then attack_idx = 1 end
        ----print(aims)
    end

    NetUpdateHash("AICalcAttacksAndAimSmart", num_attacks, aims, aim_cost,
                  context.force_max_aim)
    return num_attacks, aims
end

-- JAZZ-AI-002: Commit → Dump → Disengage / BunkerDown
local JAZZ_AI_SOFT_DUMP_CAP = 4

local function JAZZ_AIFilterEnemies(context)
    local enemies = context.enemies
    for i = #enemies, 1, -1 do
        if not IsValidTarget(enemies[i]) then
            table.remove(enemies, i)
        end
    end
    return enemies
end

-- ACT-004: close MG doctrine — prefer direct fire over distant sector.
JazzAI_MGCloseFireTiles = 8
JazzAI_MGCloseEnemyZoneBonus = 160
JazzAI_MGMissedCloseZonePenalty = 220

function JazzAI_MGCloseFireRange()
    return (JazzAI_MGCloseFireTiles or 8) * const.SlabSizeX
end

-- Visible enemy within close tiles (no InteractionRand). Used by Dump/setup/Positioning.
function JazzAI_UnitWantsCloseMGDirectFire(unit)
    if not IsValid(unit) or unit:IsDead() then
        return false
    end
    if unit:HasStatusEffect("StationedMachineGun")
        or unit:HasStatusEffect("ManningEmplacement") then
        return false
    end
    local weapon = unit:GetActiveWeapons()
    if not weapon or not IsKindOfClasses(weapon, "MachineGun", "LightMachineGun") then
        return false
    end
    local maxd = JazzAI_MGCloseFireRange()
    for _, enemy in ipairs(GetEnemies(unit) or empty_table) do
        if IsValidTarget(enemy) and not enemy:IsDowned() and not enemy:IsIncapacitated()
            and unit:GetDist(enemy) <= maxd then
            if HasVisibilityTo(unit, enemy) or HasVisibilityTo(unit.team, enemy) then
                return true
            end
        end
    end
    return false
end

function JazzAI_ContextCloseEnemies(context)
    local unit = context and context.unit
    if not unit then
        return empty_table
    end
    local maxd = JazzAI_MGCloseFireRange()
    local close = {}
    for _, enemy in ipairs(context.enemies or empty_table) do
        if IsValidTarget(enemy) and not enemy:IsDowned() and not enemy:IsIncapacitated()
            and unit:GetDist(enemy) <= maxd then
            local visible = context.enemy_visible and context.enemy_visible[enemy]
            if not visible and context.enemy_visible_by_team then
                visible = context.enemy_visible_by_team[enemy]
            end
            if visible then
                close[#close + 1] = enemy
            end
        end
    end
    return close
end

function JazzAI_MGPreferDirectFire(context)
    local unit = context and context.unit
    if not unit or unit:HasStatusEffect("StationedMachineGun")
        or unit:HasStatusEffect("ManningEmplacement") then
        return false
    end
    local weapon = context.weapon
    if not weapon or not IsKindOfClasses(weapon, "MachineGun", "LightMachineGun") then
        return false
    end
    return #(JazzAI_ContextCloseEnemies(context) or empty_table) > 0
end

-- Permanent MG/emplacement sector keeps AP and should Dump-fire (vanilla AIPlayAttacks).
-- Temporary Overwatch / other prepared attacks still block Dump.
local function JAZZ_AICanDump(unit, context)
    if not IsValid(unit) or unit:IsDead() or unit:IsIncapacitated()
        or unit:HasStatusEffect("Unconscious")
        or unit:HasStatusEffect("suppressionPinned")
        or IsSetpiecePlaying() then
        return false
    end
    if (context.max_attacks or 0) <= 0 or unit.ActionPoints <= 0 then
        return false
    end
    local ow = g_Overwatch and g_Overwatch[unit]
    if ow and ow.permanent then
        return true
    end
    if unit:HasPreparedAttack() or ow then
        return false
    end
    return true
end

-- PositioningAI Label/Bias MGSetup: do not walk to a distant setup lane while a close
-- threat is already visible (ACT-004). Patch instance Score once presets exist.
JazzAI_MGPositioningScoresPatched = rawget(_G, "JazzAI_MGPositioningScoresPatched") or false

local function JazzAI_PatchMGPositioningScores()
    if rawget(_G, "JazzAI_MGPositioningScoresPatched") then
        return
    end
    if type(ForEachPreset) ~= "function" then
        return
    end
    ForEachPreset("AIArchetype", function(arch)
        for _, behavior in ipairs(arch.Behaviors or empty_table) do
            if IsKindOf(behavior, "PositioningAI")
                and (behavior.Label == "MGSetup" or behavior.BiasId == "MGSetup")
                and not behavior.jazz_mg_close_score_wrapped then
                local prev = behavior.Score
                behavior.Score = function(self, unit, proto_context, debug_data)
                    if JazzAI_UnitWantsCloseMGDirectFire(unit) then
                        return 0
                    end
                    if type(prev) == "function" then
                        return prev(self, unit, proto_context, debug_data)
                    end
                    return self.Weight or 0
                end
                behavior.jazz_mg_close_score_wrapped = true
            end
        end
    end)
    rawset(_G, "JazzAI_MGPositioningScoresPatched", true)
end

function OnMsg.DataLoaded()
    JazzAI_PatchMGPositioningScores()
    if JazzAI_InstallMobileShotResolve then
        JazzAI_InstallMobileShotResolve()
    end
end

function OnMsg.ModsReloaded()
    rawset(_G, "JazzAI_MGPositioningScoresPatched", false)
    JazzAI_PatchMGPositioningScores()
    if JazzAI_InstallMobileShotResolve then
        JazzAI_InstallMobileShotResolve()
    end
end

if type(ForEachPreset) == "function" then
    JazzAI_PatchMGPositioningScores()
end

local function JAZZ_AIHasGoodCover(unit)
    local cover_high, cover_low = GetCoverTypes(unit)
    return cover_high or cover_low
end

function JAZZ_AIBunkerDown(unit, context, did_attack)
    context = context or (unit and unit.ai_context)
    if not g_Combat or not IsValid(unit) or unit:IsDead() then
        return
    end
    if context and context.bunker_used then
        return
    end
    if unit:HasPreparedAttack() or g_Overwatch[unit] then
        return
    end
    if unit.species ~= "Human" then
        return
    end
    if unit:HasStatusEffect("StationedMachineGun") or unit:HasStatusEffect("ManningEmplacement") then
        return
    end

    local cover_high, cover_low = GetCoverTypes(unit)

    -- 1) TakeCover when possible
    if unit:CanTakeCover() and (cover_high or cover_low) then
        local take = did_attack
        if not take then
            local chance = context and context.behavior and context.behavior.TakeCoverChance or 0
            take = chance >= 100 or (chance > 0 and unit:Random(100) < chance)
        end
        if take then
            local dest = GetPackedPosAndStance(unit)
            local enemy_visible = context and context.enemy_visible or empty_table
            local enemy_pos = context and context.enemy_pack_pos_stance or empty_table
            local ok = false
            for _, enemy in ipairs((context and context.enemies) or empty_table) do
                if (enemy_visible[enemy] and GetCoverFrom(dest, enemy_pos[enemy]) or 0) > 0 then
                    ok = true
                    break
                end
            end
            if ok or did_attack then
                if AIPlayCombatAction("TakeCover", unit, 0) then
                    if context then context.bunker_used = true end
                    return true
                end
            end
        end
    end

    -- 2) Crouch behind low cover
    if cover_low and not cover_high and unit.stance ~= "Crouch" and unit.stance ~= "Prone" then
        local cost = GetStanceToStanceAP(unit.stance, "Crouch") or 0
        if cost >= 0 and unit.ActionPoints >= cost then
            if AIPlayChangeStance(unit, "Crouch") then
                if context then context.bunker_used = true end
                return true
            end
        end
    end

    -- 3) Prone in the open
    if not cover_high and not cover_low and unit.stance ~= "Prone" then
        local cost = GetStanceToStanceAP(unit.stance, "Prone") or 0
        if HasPerk(unit, "HitTheDeck") then
            cost = 0
        end
        if cost >= 0 and unit.ActionPoints >= cost then
            if AIPlayChangeStance(unit, "Prone") then
                if context then context.bunker_used = true end
                return true
            end
        end
    end

    -- 4) PrefStance
    local pref = context and context.archetype and context.archetype.PrefStance
    if pref and (pref == "Crouch" or pref == "Prone") and unit.stance == "Standing" then
        local cost = GetStanceToStanceAP(unit.stance, pref) or 0
        if pref == "Prone" and HasPerk(unit, "HitTheDeck") then
            cost = 0
        end
        if cost >= 0 and unit.ActionPoints >= cost then
            if AIPlayChangeStance(unit, pref) then
                if context then context.bunker_used = true end
                return true
            end
        end
    end
end

local function JAZZ_AITryCoverMove(unit, context)
    if not context or context.disengage_used then
        return
    end
    if JAZZ_AIHasGoodCover(unit) then
        return
    end
    local ap = unit.ActionPoints
    if ap <= 0 then
        return
    end

    local best_dest, best_score, best_path, best_goto_ap, best_move_stance
    local dests = context.all_destinations or context.destinations or empty_table
    for _, dest in ipairs(dests) do
        local x, y, z, stance_idx = stance_pos_unpack(dest)
        local up, right, down, left = GetCover(x, y, z)
        if not (up or right or down or left) then
            goto continue
        end
        local move_stance_idx = context.dest_combat_path and context.dest_combat_path[dest]
        local cpath = move_stance_idx and context.combat_paths and context.combat_paths[move_stance_idx]
        local pt = SnapToPassSlab(x, y, z)
        local path = pt and cpath and cpath:GetCombatPathFromPos(pt)
        local goto_ap = (pt and cpath and cpath.paths_ap[point_pack(pt)]) or 0
        if path and goto_ap > 0 and goto_ap <= ap then
            local score = 40
            local high = const.CoverHigh
            if up == high or right == high or down == high or left == high then
                score = 100
            end
            score = score - DivRound(goto_ap, const.Scale.AP)
            if not best_score or score > best_score then
                best_dest, best_score = dest, score
                best_path, best_goto_ap = path, goto_ap
                best_move_stance = move_stance_idx
            end
        end
        ::continue::
    end

    if not best_dest or not best_path then
        return
    end

    local x, y, z, stance_idx = stance_pos_unpack(best_dest)
    local goto_stance = StancesList[best_move_stance or stance_idx]
    if goto_stance and goto_stance ~= unit.stance and best_path[2] then
        AIPlayChangeStance(unit, goto_stance, point(point_unpack(best_path[2])))
    end
    context.ai_destination = best_path[1]
    AIPlayCombatAction("Move", unit, best_goto_ap, {
        goto_pos = point(point_unpack(best_path[1])),
        fallbackMove = true,
        goto_stance = stance_idx
    })
    context.disengage_used = true
    while not unit:IsIdleCommand() do
        WaitMsg("Idle", 50)
    end
end

-- JAZZ-AI-OW-001: Fallback OW only toward a known aim point; no random 360°/door/ally-front.
-- No usable point → return false (caller reverts / Unaware), never spam OW into a wall.
local function JazzAI_FallbackOverwatchTargetPos(unit, context)
	if not IsValid(unit) then
		return false
	end
	local known = unit.last_known_enemy_pos
	if known then
		local slab = GetPassSlab(known) or known
		if slab then
			return slab
		end
	end
	local best, best_dist
	for _, enemy in ipairs(context and context.enemies or empty_table) do
		if IsValidTarget(enemy) then
			local dist = unit:GetDist(enemy)
			if not best_dist or dist < best_dist then
				best = enemy
				best_dist = dist
			end
		end
	end
	if best then
		local pos = best:GetPos()
		return GetPassSlab(pos) or pos
	end
	return false
end

function AIPlaceFallbackOverwatch(unit, context)
	if not context or not IsKindOf(context.weapon, "Firearm") then
		return false
	end
	if context.weapon.PreparedAttackType ~= "Overwatch"
		and context.weapon.PreparedAttackType ~= "Both" then
		return false
	end

	local target_pt = JazzAI_FallbackOverwatchTargetPos(unit, context)
	if not target_pt then
		return false
	end

	local args, has_ap = AIGetAttackArgs(context, CombatActions.Overwatch, nil, "None")
	if args and has_ap then
		args.target_pos = target_pt
		args.target = target_pt
		if AIPlayCombatAction("Overwatch", context.unit, nil, args) then
			PlayVoiceResponse(context.unit, "AIOverwatch")
			return true
		end
	end
	return false
end

function JAZZ_AIDisengage(unit, context, did_attack)
    if not IsValid(unit) or unit:IsDead() then
        return
    end
    if unit:HasStatusEffect("Berserk") or unit:HasStatusEffect("Panicked") then
        return
    end
    JAZZ_AITryCoverMove(unit, context)
    JAZZ_AIBunkerDown(unit, context, did_attack)

    if context and not context.bunker_used and context.archetype
        and context.archetype.FallbackAction == "overwatch" then
        local sight = false
        for _, enemy in ipairs(context.enemies or empty_table) do
            sight = sight or HasVisibilityTo(unit, enemy)
        end
        if not sight then
            AIPlaceFallbackOverwatch(unit, context)
        end
    end
end

function AITakeCover(unit, context)
    context = context or (unit and unit.ai_context)
    if context and context.bunker_used then
        return
    end
    return JAZZ_AIBunkerDown(unit, context, false)
end

function AIExecuteUnitBehavior(unit, force_or_skip_action)
    if not g_Combat or not IsValid(unit) or unit:IsDead()
        or unit:HasStatusEffect("Unconscious")
        or unit:HasStatusEffect("suppressionPinned") then
        return
    end

    -- JAZZ-QOL-001: auto speed for unseen AI (see Code/AiFastForward.lua)
    JAZZ_UpdateAutoFastForward(unit, "behavior")

    if unit.ai_context and unit.ai_context.behavior then
        local status = unit.ai_context.behavior:Play(unit)
        if g_AIExecutionController then
            g_AIExecutionController:Log(
                "  Behavior %s for unit %s (%d) returned '%s'",
                unit.ai_context.behavior:GetEditorView(), unit.unitdatadef_id,
                unit.handle, tostring(status))
        end
        if status then
            return status
        end
    end

    if IsValid(unit) and not unit:IsDead() then
        JAZZ_UpdateAutoFastForward(unit, "attacks")
    end

    local status = AIPlayAttacks(unit, unit.ai_context,
        unit.ai_context.forced_signature_action, force_or_skip_action)
    if status then
        return status
    end
    return AITakeCover(unit, unit.ai_context)
end

function AIPlayAttacks(unit, context, dbg_action, force_or_skip_action)
    if g_AIExecutionController then
        g_AIExecutionController:Log("Unit %s (%d) start attack sequence",
            unit.unitdatadef_id, unit.handle)
    end

    -- Context creation tries Handheld A/B and then an inventory firearm. If no
    -- normal firearm exists, it supplies JA3's virtual Unarmed weapon instead;
    -- do not enter Dump or its Idle wait with a nil active weapon.
    local firearm = JAZZ_AIEnsureActiveFirearm(unit)
    if not firearm then
        if g_AIExecutionController then
            g_AIExecutionController:Log("  No active firearm; skip Dump (Unarmed fallback)")
        end
        unit:SequentialActionsEnd()
        return "done"
    end

    local remaining_free_ap = unit.free_move_ap
    unit:RemoveStatusEffect("FreeMove")
    AIUpdateContext(context, unit)
    JAZZ_AIFilterEnemies(context)

    if g_AIExecutionController then
        g_AIExecutionController:Log("  Num enemies: %d", #context.enemies)
        g_AIExecutionController:Log("  Action Points: %d", unit.ActionPoints)
    end

    local start_ap = context.start_ap
    local did_attack = false
    local dump_steps = 0
    local voice_response

    while JAZZ_AICanDump(unit, context) and dump_steps < JAZZ_AI_SOFT_DUMP_CAP do
        dump_steps = dump_steps + 1
        JAZZ_AIFilterEnemies(context)
        AIUpdateContext(context, unit)

        local dest = GetPackedPosAndStance(unit)
        if dump_steps == 1 and not force_or_skip_action and context.ai_destination then
            -- prefer planned dest target on first step if still standing on it
            local planned = context.ai_destination
            if stance_pos_dist(planned, dest) == 0 then
                dest = planned
            end
        end

        context.dest_ap[dest] = unit.ActionPoints
        local preferred = context.target_locked
            or (context.dest_target or empty_table)[dest]
        AIPrecalcDamageScore(context, {dest}, preferred)

        local signature_action
        if dump_steps == 1 and dbg_action then
            context.action_states = context.action_states or {}
            context.action_states[dbg_action] = {}
            dbg_action:PrecalcAction(context, context.action_states[dbg_action])
            if dbg_action:IsAvailable(context, context.action_states[dbg_action]) then
                signature_action = dbg_action
            elseif force_or_skip_action then
                table.insert(failed_actions, dbg_action.BiasId or dbg_action.class)
                return
            end
        end
        if dump_steps == 1 and not context.reposition and not unit:HasStatusEffect("Numbness") then
            signature_action = signature_action or AIChooseSignatureAction(context)
        end

        local default_attack = context.default_attack
        local default_attack_vr = "AIAttack"
        if default_attack and default_attack.FiringModeMember
            and default_attack.FiringModeMember == "AttackShotgun" then
            default_attack_vr = "AIDoubleBarrel"
        end
        voice_response = signature_action and (signature_action:GetVoiceResponse() or "")
            or default_attack_vr
        if voice_response == "" then
            voice_response = nil
        end

        if signature_action then
            if g_AIExecutionController then
                g_AIExecutionController:Log("  Signature Action: %s",
                    signature_action:GetEditorView())
            end
            context.action_states = context.action_states or {}
            context.action_states[signature_action] = context.action_states[signature_action] or {}
            signature_action:OnActivate(unit)
            if voice_response then
                context.action_states[signature_action].args =
                    context.action_states[signature_action].args or {}
                context.action_states[signature_action].args.voiceResponse = voice_response
            end
            local status = signature_action:Execute(context,
                context.action_states[signature_action])
            context.ap_after_signature = unit.ActionPoints
            context.max_attacks = context.max_attacks - 1
            did_attack = true
            if status then
                return status
            end
            AIReloadWeapons(unit)

            local sig_target = (context.dest_target or empty_table)[dest]
            if not IsValidTarget(sig_target)
                or (IsKindOf(sig_target, "Unit") and sig_target:IsIncapacitated()) then
                if context.archetype.TargetChangePolicy == "restart" then
                    return "restart"
                end
                context.dest_ap[dest] = unit.ActionPoints
                context.target_locked = nil
                context.dump_attack_mode = nil
                context.dump_attack_target = nil
            end
        else
            local target = (context.dest_target or empty_table)[dest]
            if not IsValidTarget(target) then
                if g_AIExecutionController then
                    g_AIExecutionController:Log("  No target")
                end
                break
            end

            if g_AIExecutionController then
                g_AIExecutionController:Log("  Target: %s",
                    IsKindOf(target, "Unit") and target.unitdatadef_id or target.class)
            end

            if context.dump_attack_target ~= target then
                context.dump_attack_mode = nil
                context.dump_attack_target = target
            end
            local best_attack = PickBestAttack(unit, target, context.basic_attacks,
                unit.ActionPoints, context.dump_attack_mode)
            if best_attack and best_attack.action then
                context.default_attack = best_attack.action
                context.default_attack_cost = best_attack.ap or context.default_attack_cost
                context.attack_target = target
                context.dump_attack_mode = best_attack.mode or best_attack.action.id
                context.dump_attack_target = target
            end

            if context.default_attack and context.default_attack.id == "Bombard" and AICheckIndoors(dest) then
                break
            end

            if not best_attack and not context.default_attack then
                break
            end

            local attack_action = (best_attack and best_attack.action) or context.default_attack
            local aim = best_attack and best_attack.aim or 0
            if not best_attack then
                local attacks, aims = AICalcAttacksAndAim(context, unit.ActionPoints, target)
                if not attacks or attacks < 1 then
                    break
                end
                aim = aims and aims[1] or 0
            end

            local cost = best_attack and best_attack.ap
                or (context.default_attack_cost or attack_action:GetAPCost(unit))
            if not cost or cost <= 0 or unit.ActionPoints < cost then
                if not unit:HasAP(cost or 0) then
                    break
                end
            end

            local args = {target = target, voiceResponse = voice_response, aim = aim}
            -- JAZZ-AI-002 Dump: no LOF → Disengage. CalcChanceToHit / PickBestAttack
            -- ignore stuck; GetActionResults zeros CTH when obstructed. Firing with an
            -- empty body-part list animates a wall/miss shot — abort instead.
            local body_parts = AIGetAttackTargetingOptions(unit, context, target, attack_action)
            if IsKindOf(target, "Unit") and (not body_parts or #body_parts == 0) then
                if g_AIExecutionController then
                    g_AIExecutionController:Log("  No LOF (all body parts CTH=0)")
                end
                context.dump_attack_mode = nil
                context.dump_attack_target = nil
                break
            end
            if body_parts and #body_parts > 0 then
                local pick = table.weighted_rand(body_parts, "chance",
                    InteractionRand(1000000, "Combat"))
                if pick then
                    args.target_spot_group = pick.id
                end
            end

            Sleep(0)
            local result = AIPlayCombatAction(attack_action.id, unit, nil, args)
            context.max_attacks = context.max_attacks - 1
            did_attack = true
            if g_AIExecutionController then
                g_AIExecutionController:Log("  Attack result: %s", tostring(result))
            end
            if IsSetpiecePlaying() then
                unit:SequentialActionsEnd()
                return
            end
            AIReloadWeapons(unit)
            if not result or not IsValidTarget(unit) or context.max_attacks <= 0 then
                break
            end

            while IsKindOf(target, "Unit") and target:IsGettingDowned() do
                WaitMsg("UnitDowned", 20)
            end
            if not IsValidTarget(target)
                or (IsKindOf(target, "Unit") and target:IsIncapacitated()) then
                if context.archetype.TargetChangePolicy == "restart" then
                    unit:SequentialActionsEnd()
                    return "restart"
                end
                context.dest_ap[dest] = unit.ActionPoints
                context.target_locked = nil
                context.dump_attack_mode = nil
                context.dump_attack_target = nil
            end
        end

        Sleep(0)
    end

    unit:SequentialActionsEnd()

    -- Vanilla: stationed + no Dump target → MGPack + restart (reposition).
    -- Jazz previously packed only when OW missing (recovery after ACT Dump/OW gate).
    -- ACT-004: Dump runs with permanent OW again; restore pack-when-idle so gunners
    -- do not sit forever in a rear sector after the fight moves on.
    -- Skip when did_attack (includes fresh MGSetup this sequence) to avoid setup→pack thrash.
    if unit:HasStatusEffect("StationedMachineGun")
        and CombatActions.MGPack:GetUIState({unit}) == "enabled"
        and (not g_Overwatch[unit] or not did_attack) then
        unit:SequentialActionsEnd()
        AIPlayCombatAction("MGPack", unit)
        return "restart"
    end

    while not unit:IsIdleCommand() do
        WaitMsg("Idle", 50)
    end

    -- Vanilla-style fallback when nothing was spent
    if unit.ActionPoints + remaining_free_ap == start_ap
        and not unit:HasStatusEffect("ManningEmplacement") then
        if context.closest_dest then
            unit:GainAP(remaining_free_ap)
            local dest = context.closest_dest
            local x, y, z, stance_idx = stance_pos_unpack(dest)
            local move_stance_idx = context.dest_combat_path[dest]
            local cpath = context.combat_paths[move_stance_idx]
            local pt = SnapToPassSlab(x, y, z)
            local path = pt and cpath and cpath:GetCombatPathFromPos(pt)
            if path then
                local goto_stance = StancesList[move_stance_idx]
                if goto_stance ~= unit.stance then
                    AIPlayChangeStance(unit, goto_stance, point(point_unpack(path[2])))
                end
                local goto_ap = unit.ActionPoints
                context.ai_destination = path[1]
                AIPlayCombatAction("Move", unit, goto_ap, {
                    goto_pos = point(point_unpack(path[1])),
                    fallbackMove = true,
                    goto_stance = stance_idx
                })
            end
        end
        if unit:GetDist(context.unit_pos) < const.SlabSizeX / 2 then
            local revert = true
            local sight = false
            for _, enemy in ipairs(context.enemies) do
                sight = sight or HasVisibilityTo(unit.team, enemy)
            end
            if context.archetype.FallbackAction == "overwatch" and not sight then
                revert = not AIPlaceFallbackOverwatch(unit, context)
            end
            if revert and not sight then
                unit.last_known_enemy_pos = unit.last_known_enemy_pos or AIPickScoutLocation(unit)
                if not unit.last_known_enemy_pos then
                    table.insert(g_UnawareQueue, unit)
                end
            end
        end
    end

    JAZZ_AIDisengage(unit, context, did_attack)
end

-- ACT-002: mark unit as acted after attack sequence (smoke self-cover gate).
do
	local JazzAI_AIPlayAttacks_Orig = AIPlayAttacks
	function AIPlayAttacks(unit, context, dbg_action, force_or_skip_action)
		local result = JazzAI_AIPlayAttacks_Orig(unit, context, dbg_action, force_or_skip_action)
		if JazzAI_MarkUnitActed then
			JazzAI_MarkUnitActed(unit)
		end
		return result
	end
end

-- Legacy name kept so accidental callers resolve to BunkerDown.
function TryChangeStance(unit)
    return JAZZ_AIBunkerDown(unit, unit and unit.ai_context, false)
end

-- SameTarget + TakeAim (Пристрелка) + same-target weapon components for approximate AI score.
function AICalcSameTargetScoreBonus(unit, target, action, weapon, attacker_pos)
    if not IsValid(unit) or not IsValidTarget(target) then
        return 0
    end
    if unit:GetLastAttack() ~= target then
        return 0
    end
    local mod = Presets.ChanceToHitModifier and Presets.ChanceToHitModifier.Default
                    and Presets.ChanceToHitModifier.Default.SameTarget
    if not mod then
        return 0
    end
    local target_pos = IsValid(target) and target:GetPos() or attacker_pos
    local mod_data = {
        attacker = unit,
        target = target,
        target_spot_group = "Torso",
        action = action,
        weapon1 = weapon,
        weapon2 = false,
        aim = 0,
        opportunity_attack = false,
        attacker_pos = attacker_pos,
        target_pos = target_pos,
        min = 0,
        max = 100,
        display_name = mod.DisplayName or mod.display_name,
        meta_text = {},
        enabled = false,
        mod_add = 0,
        mod_mul = 100,
    }
    local apply, value = mod:CalcValue(unit, target, "Torso", action, weapon, false,
        false, 0, false, attacker_pos, target_pos)
    if not apply then
        return 0
    end
    value = unit:GatherCTHModifications("SameTarget", value or 0, mod_data) or 0
    if IsKindOf(weapon, "Firearm") and weapon.components then
        for _, component_id in sorted_pairs(weapon.components) do
            local def = WeaponComponents[component_id]
            local effects = def and def.ModificationEffects or empty_table
            if table.find(effects, "AccuracyBonusSameTarget") then
                mod_data.weapon1 = weapon
                mod_data.display_name = def.DisplayName
                mod_data.meta_text = nil
                local comp_val = unit:GatherCTHModifications(component_id, 0, mod_data)
                if comp_val and comp_val ~= 0 then
                    value = value + comp_val
                end
            end
        end
    end
    return value
end

function AIPrecalcDamageScore(context, destinations, preferred_target,
                              debug_data)

    --print('AIPrecalcDamageScore')
    local unit = context.unit
    local weapon = context.weapon
    local action = CombatActions[context.override_attack_id or false] or
                       context.default_attack
    local archetype = context.archetype
    local behavior = context.behavior
    local tStart = config.JAZZ_AIPerfLog and GetPreciseTicks() or nil
    -- Think may pass a dest subset; never expand to all_destinations (JAZZ-AI-PERF-001).
    local destinations_were_passed = destinations ~= nil

    if not weapon or context.reposition or unit:HasStatusEffect("Burning") then
        return
    end
    if not destinations and context.damage_score_precalced then return end

    local action_targets = action:GetTargets({unit})

    local targets = table.ifilter(action_targets, function(idx, target)
        return unit:IsOnEnemySide(target) and IsValid(target) and GetPackedPosAndStance(target)
    end)


    if #targets == 0 then return end
    context.damage_score_precalced = true
    local target_score_mod = {}
    local tsr = archetype.TargetScoreRandomization
    for i, target in ipairs(targets) do
        target_score_mod[i] = 100 +
                                  ((tsr > 0) and unit:RandRange(-tsr, tsr) or 0)
    end
    context.target_score_mod = target_score_mod

    local base_mod = unit[weapon.base_skill]
    local cost_ap = context.default_attack_cost or 1

    local max_check_range, is_melee =
        AIGetWeaponCheckRange(unit, weapon, action)
    local is_heavy = IsKindOf(weapon, "HeavyWeapon")

    local hit_modifiers = Presets["ChanceToHitModifier"]["Default"]
    -- stance mod
    local modCrouchBonus = 0
    local modProneBonus = 0
    -- if IsKindOf(weapon, "Firearm") then
    -- modCrouchBonus = hit_modifiers.AttackerStance:ResolveValue("CrouchBonus")
    -- modProneBonus = hit_modifiers.AttackerStance:ResolveValue("ProneBonus")
    local value = GetComponentEffectValue(weapon, "AccuracyBonusProne",
                                          "bonus_cth")
    if value then modProneBonus = modProneBonus + value end
    -- end
    -- ground difference mod
    local MinGroundDifference = hit_modifiers.GroundDifference:ResolveValue(
                                    "RangeThreshold") * const.SlabSizeZ / 100
    local modHighGround = hit_modifiers.GroundDifference:ResolveValue(
                              "HighGround")
    local modLowGround =
        hit_modifiers.GroundDifference:ResolveValue("LowGround")
    -- cover
    local modCover = hit_modifiers.RangeAttackTargetStanceCover:ResolveValue(
                         "Cover")

    local target_policies = archetype.TargetingPolicies
    if behavior and #(behavior.TargetingPolicies or empty_table) > 0 then
        target_policies = behavior.TargetingPolicies
    end

    local dest_target = context.dest_target
    local dest_target_score = context.dest_target_score
    local dest_ap = context.dest_ap
    local aim_mod = Presets.ChanceToHitModifier.Default.Aim
    local dest_cth = {}
    context.dest_cth = dest_cth
    local lof_params
    local attacker_pos = unit:GetPos()


    -- script-driven modifiers (based on groups)
    local target_modifiers
    for _, groupname in ipairs(unit.Groups) do
        local group_modifiers = gv_AITargetModifiers[groupname]
        for target_group, mod in sorted_pairs(group_modifiers or empty_table) do
            target_modifiers = target_modifiers or {}
            target_modifiers[target_group] =
                (target_modifiers[target_group] or 0) + mod
            for _, obj in ipairs(Groups[target_group]) do
                if IsKindOf(obj, "Unit") and IsValid(obj) and GetPackedPosAndStance(obj)
                    and not table.find(targets, obj) then
                    table.insert(targets, obj) -- make sure the target is considired regardless if it's an enemy or not
                    table.insert(target_score_mod, 100 +
                                     ((tsr > 0) and unit:RandRange(-tsr, tsr) or
                                         0))
                end
            end
        end
    end

    if unit:HasStatusEffect("StationedMachineGun") or
        unit:HasStatusEffect("ManningEmplacement") then
        local ow_units = {unit}
        targets = table.ifilter(targets, function(idx, target)
            return target:IsThreatened(ow_units, "overwatch")
        end)
    end

    if not IsValidTarget(preferred_target) or
        (IsKindOf(preferred_target, "Unit") and
            preferred_target:IsIncapacitated() or
            not table.find(targets, preferred_target)) then
        preferred_target = nil
    end

    if weapon and not is_melee then
        lof_params = {
            obj = unit,
            action_id = action.id,
            weapon = weapon,
            step_pos = false,
            stance = false,
            range = max_check_range,
            prediction = true,
            output_collisions = true
        }
        if not destinations or #destinations > 1 then
            lof_params.target_spot_group = "Torso"
        end
    end
    --[[	local logdata = {}
	if destinations then
		table.insert(g_AIDamageScoreLog, logdata)
	end
	logdata.preferred_target = preferred_target and (IsKindOf(preferred_target, "Unit") and _InternalTranslate(preferred_target.Name or "") or preferred_target.class) or tostring(preferred_target)--]]
    -- Prefer explicit Think subset; do not fall back to all_destinations.
    destinations = destinations or context.destinations
    if not destinations_were_passed and context.all_destinations
        and destinations == context.all_destinations then
        -- Defensive: scoring full OptLoc slab set is pathological; use behavior dests only.
        destinations = context.destinations
    end
    -- гарантируем сравнение со "стоя на месте"
local stay = GetPackedPosAndStance(unit)
if destinations and not table.find(destinations, stay) then
  -- не мутируй оригинальный массив из контекста
  local copy = {}
  for i = 1, #destinations do copy[i] = destinations[i] end
  copy[#copy + 1] = stay
  destinations = copy
  -- стоя на месте все AP доступны для атаки
  context.dest_ap[stay] = context.dest_ap[stay] or unit.ActionPoints
end

    -- Cap GetLoFData dest matrix (M1 path dests can be 200–400 → multi-second Precalc).
    -- Do not rawget(_G,…): JAZZ_* live in the mod env, not always on _G.
    local precalc_cap = (rawget(_G, "JAZZ_AI_PERF_PRECALC_DEST_CAP") or JAZZ_AI_PERF_PRECALC_DEST_CAP) or 48
    local precalc_capped = 0
    local cap_fn = rawget(_G, "JAZZ_AICapDestLosCandidates") or JAZZ_AICapDestLosCandidates
    if destinations and #destinations > precalc_cap and type(cap_fn) == "function" then
        local capped
        capped, precalc_capped = cap_fn(unit, context, destinations, precalc_cap)
        destinations = capped
        if stay and not table.find(destinations, stay) then
            -- Cap must never drop stay (attack-from-here baseline).
            if #destinations >= precalc_cap then
                destinations[precalc_cap] = stay
            else
                destinations[#destinations + 1] = stay
            end
        end
    end

    -- Soft target prune: only when many targets; wide margin (smarter near edge cases).
    local base_margin = JAZZ_AI_PERF_RANGE_MARGIN or (2 * const.SlabSizeX)
    local soft_mult = JAZZ_AI_PERF_PRECALC_MARGIN_MULT or 4
    local soft_gate = JAZZ_AI_PERF_PRECALC_TARGET_SOFT or 12
    local shortlist_range = max_check_range
        and (max_check_range + base_margin * soft_mult)
        or nil
    if shortlist_range and #targets > soft_gate and rawget(_G, "JAZZ_AIShortlistTargetsByRange") then
        local shortlisted = JAZZ_AIShortlistTargetsByRange(targets, destinations, stay, shortlist_range)
        if preferred_target and IsValid(preferred_target) and not table.find(shortlisted, preferred_target) then
            if table.find(targets, preferred_target) then
                shortlisted[#shortlisted + 1] = preferred_target
                JAZZ_AISortUnitsByHandle(shortlisted)
            end
        end
        if #shortlisted < #targets then
            local new_mods = {}
            for i, target in ipairs(shortlisted) do
                local old_idx = table.find(targets, target)
                new_mods[i] = old_idx and target_score_mod[old_idx] or (100 + ((tsr > 0) and unit:RandRange(-tsr, tsr) or 0))
            end
            targets = shortlisted
            target_score_mod = new_mods
            context.target_score_mod = target_score_mod
        end
    end
    if #targets == 0 then
        if tStart and rawget(_G, "JAZZ_AIPerfLog") then
            JAZZ_AIPerfLog("Precalc unit=%s ms=%d dests=%d targets=0 (shortlist empty) capped=%d",
                tostring(unit.unitdatadef_id or unit.class), GetPreciseTicks() - tStart,
                destinations and #destinations or 0, precalc_capped)
        end
        return
    end

    NetUpdateHash("AIPrecalcDamageScore", unit, hashParamTable(destinations),
                  hashParamTable(targets), preferred_target, shortlist_range or 0, precalc_capped, precalc_cap)
    local los_cache = g_AIDestEnemyLOSCache
    local scored_dests, skipped_los = 0, 0
    for j, upos in ipairs(destinations) do
        
        local ux, uy, uz, ustance_idx = stance_pos_unpack(upos)
        local ustance = StancesList[ustance_idx]
        uz = uz or terrain.GetHeight(ux, uy)

        local ap = dest_ap[upos] or 0
        local best_target, best_cth
        local best_score = 0
        local potential_targets, target_score, target_cth = {}, {}, {}
        --print('print(mod)'..ap..' '..cost_ap)
        --print(ap.." ap cost_ap"..cost_ap)
        if los_cache[upos] == false then
            skipped_los = skipped_los + 1
            dest_target_score[upos] = 0
            dest_target[upos] = nil
            dest_cth[upos] = nil
        elseif weapon and ap >= cost_ap then
            scored_dests = scored_dests + 1
            local pos_mod = base_mod
            pos_mod = pos_mod +
                          (ustance_idx == 2 and modCrouchBonus or ustance_idx ==
                              3 and modProneBonus or 0)

            local targets_attack_data
            if not is_melee then
                attacker_pos = point(ux, uy, uz)
                lof_params.step_pos = point_pack(ux, uy, uz)
                lof_params.stance = ustance
                targets_attack_data = GetLoFData(unit, targets, lof_params)
            end
            for k, target in ipairs(targets) do
                local tpos = GetPackedPosAndStance(target)
                if not tpos then
                    -- Invalid / despawning target: skip (melee Knife Think hit this on M1).
                else
                local dist = stance_pos_dist(upos, tpos)
                
                if dist <= (max_check_range or dist) and
                    (is_melee or targets_attack_data[k] and
                        not targets_attack_data[k].stuck) then
                    local tx, ty, tz, tstance_idx = stance_pos_unpack(tpos)
                    tz = tz or terrain.GetHeight(tx, ty)
                    local hit_mod = pos_mod
                    if not is_heavy then
                        hit_mod = hit_mod +
                                      (uz > tz + MinGroundDifference and
                                          modHighGround or uz < tz -
                                          MinGroundDifference and modLowGround or
                                          0)
                        hit_mod = hit_mod + AICalcSameTargetScoreBonus(unit,
                                                                       target,
                                                                       action,
                                                                       weapon,
                                                                       attacker_pos)
                    end
                    local target_cover = GetCoverFrom(tpos, upos)
                    if target_cover == const.CoverLow or target_cover ==
                        const.CoverHigh then
                        hit_mod = hit_mod + modCover
                    end

                    local penalty = is_heavy and 0 or
                                        (100 - weapon:GetAccuracy(dist))

                    local mod = hit_mod - penalty -- dist_penalty
                    -- environmental modifiers when applicable
                    local apply, value, target_spot_group, action, weapon1,
                          weapon2, lof, aim, opportunity_attack
                    apply, value = hit_modifiers.Darkness:CalcValue(unit,
                                                                    target,
                                                                    target_spot_group,
                                                                    action,
                                                                    weapon1,
                                                                    weapon2,
                                                                    lof, aim,
                                                                    opportunity_attack,
                                                                    attacker_pos)
                    if apply then mod = mod + value end

                    if not is_heavy and unit:IsPointBlankRange(target) then
                        mod = MulDivRound(mod,
                                          100 + const.AIPointBlankTargetMod, 100)
                    end
                    mod = Max(0, mod)

                    
                    if mod > const.AIShootAboveCTH then
                        -- calc base score based on cth/attacks/aiming
                        local base_mod = mod
                        local attacks, aims =
                            AICalcAttacksAndAimSmart(context, ap, target)
                        mod = 0
                        for i = 1, attacks do
                            local use, bonus
                            if (aims[i] or 0) > 0 then
                                use, bonus =
                                    aim_mod:CalcValue(unit, nil, nil, nil, nil,
                                                      nil, nil, aims[i])
                            end
                            mod = mod + base_mod + (use and bonus or 0)
                        end
                        -- modify score by archetype-specific weight and (optional) targeting policies
                        mod = MulDivRound(mod, archetype.TargetBaseScore, 100)
                        for _, policy in ipairs(target_policies) do
                            local peval = policy:EvalTarget(unit, target)
                            mod = mod +
                                      MulDivRound(peval or 0, policy.Weight, 100)
                        end

                        if IsKindOf(target, "Unit") and
                            (target:IsDowned() or target:IsGettingDowned()) then
                            mod = MulDivRound(mod, 5, 100)
                        end

                        local attack_data =
                            targets_attack_data and targets_attack_data[k]
                        local ally_in_danger = attack_data and
                                                   (attack_data.best_ally_hits_count or
                                                       0) > 0

                        if action and action.AimType == "cone" then
                            ally_in_danger = ally_in_danger or
                                                 AIAllyInDanger(context.allies,
                                                                context.ally_pos,
                                                                attacker_pos,
                                                                target,
                                                                const.AIFriendlyFire_LOFConeNear,
                                                                const.AIFriendlyFire_LOFConeFar)
                        else
                            ally_in_danger = ally_in_danger or
                                                 AIAllyInDanger(context.allies,
                                                                context.ally_pos,
                                                                attacker_pos,
                                                                target,
                                                                const.AIFriendlyFire_LOFWidth,
                                                                const.AIFriendlyFire_LOFWidth)
                        end
                        if ally_in_danger then
                            mod = MulDivRound(mod,
                                              const.AIFriendlyFire_ScoreMod, 100)
                        end

                        mod = MulDivRound(mod, target_score_mod[k], 100)

                        -- apply group-based modifiers
                        if target_modifiers and IsKindOf(target, "Unit") then
                            local group_mod = 0
                            for _, groupname in ipairs(target.Groups) do
                                group_mod = group_mod +
                                                (target_modifiers[groupname] or
                                                    0)
                            end
                            if group_mod > 0 then
                                mod = MulDivRound(mod, group_mod, 100)
                            end
                        end

                        --[[table.insert(logdata, {
							name = IsKindOf(target, "Unit") and _InternalTranslate(target.Name or "") or target.class,
							score = mod
						})--]]

                        if mod > 0 and target == preferred_target then
                            best_target = target
                            best_score = mod
                            best_cth = base_mod
                            potential_targets = {}
                            break
                        end

                        best_score = Max(best_score, mod)
                        target_cth[target] = base_mod
                        target_score[target] = mod
                        
                        local threshold =
                            MulDivRound(best_score or 0,
                                        const.AIDecisionThreshold, 100)

                       -- print(mod.." -< mod threshold -> "..threshold)
                                        
                        if mod >= threshold then
                            potential_targets[#potential_targets + 1] = target
                            for i = #potential_targets, 1, -1 do
                                local target = potential_targets[i]
                                local score = target_score[target]
                                if score < threshold then
                                    table.remove(potential_targets, i)
                                end
                            end
                            -- best_target, best_score, best_cth = target, mod, base_mod
                        end
                        NetUpdateHash("AIPrecalcDamageScore_mod",
                                      target_score[target], mod, threshold)

                    end
                end
                end -- tpos valid
            end
        end

        --print(#potential_targets)
        if #potential_targets > 0 then
            local total = 0
            for _, target in ipairs(potential_targets) do
                local score = target_score[target]
                total = total + score
                if debug_data then debug_data[target] = score end
                NetUpdateHash("AIPrecalcDamageScore_total",
                              target_score[target], total)
            end
            local roll = InteractionRand(total, "AIDecision")
            for _, target in ipairs(potential_targets) do
                local score = target_score[target]
                if roll < score then
                    best_target = target
                    break
                end
                roll = roll - score
            end
            best_target =
                best_target or potential_targets[#potential_targets] or false
            best_score = target_score[best_target] or 0
            best_cth = target_cth[best_target] or 0
        end

        --[[
		if destinations and IsKindOf(best_target, "Unit") then
			if best_target == preferred_target then
				--printf("%s (%d) selected target (preferred): %s (score %d)", _InternalTranslate(unit.Name or ""), unit.handle, _InternalTranslate(best_target.Name or ""), best_score)
			else
				--printf("%s (%d) selected target: %s (score %d)", _InternalTranslate(unit.Name or ""), unit.handle, _InternalTranslate(best_target.Name or ""), best_score)
				--printf("  potential targets:")
				for _, target in ipairs(potential_targets) do
					--printf("    %s (score %d)", _InternalTranslate(target.Name or ""), target_score[target])
				end
			end
		end--]]

        -- logdata.chosen_target = best_target and (IsKindOf(best_target, "Unit") and _InternalTranslate(best_target.Name or "") or best_target.class) or tostring(best_target)
        if los_cache[upos] ~= false then
            dest_target_score[upos] = best_score
            dest_target[upos] = best_target
            dest_cth[upos] = best_cth
        end
    end

    if tStart and rawget(_G, "JAZZ_AIPerfLog") then
        JAZZ_AIPerfLog("Precalc unit=%s ms=%d dests=%d targets=%d scored_dests=%d skipped_los=%d capped=%d",
            tostring(unit.unitdatadef_id or unit.class), GetPreciseTicks() - tStart,
            destinations and #destinations or 0, #targets, scored_dests, skipped_los, precalc_capped or 0)
    end

    -- выбираем лучший и сравниваем со "стоя на месте"
local best_dest, best_score = nil, -1
for _, d in ipairs(destinations or empty_table) do
  local s = context.dest_target_score[d] or 0
  if s > best_score then best_score, best_dest = s, d end
end

local stay_score = context.dest_target_score[stay] or 0
-- Integer percent gain (default +10%). Avoid float multiply for MP determinism.
local min_gain_pct = context.min_move_gain_pct
if not min_gain_pct and context.min_move_gain then
  min_gain_pct = floatfloor((context.min_move_gain * 100) + 0.5)
end
min_gain_pct = min_gain_pct or 10

-- гистерезис: двигаться только если улучшение заметное
local picked = stay
if best_dest and best_dest ~= stay and best_score >= MulDivRound(stay_score, 100 + min_gain_pct, 100) then
  picked = best_dest
end

-- "липкость": если прошлый выбор почти так же хорош — остаёмся при нём
local prev = context.last_ai_destination
if prev then
  local prev_score = context.dest_target_score[prev] or -1
  local thr = MulDivRound((context.dest_target_score[picked] or 0), const.AIDecisionThreshold, 100)  -- обычно 80%
  if prev_score >= thr then
    picked = prev
  end
end

context.ai_destination = picked
context.last_ai_destination = picked

end

-- JAZZ-AI-ACT-005: weapon availability + mobile resolve (not ui_actions).
JazzAI_MobileAttackIds = {
	MobileShot = true,
	RunAndGun = true,
	RunAndGun_Carbine = true,
	JAZZ_MobileShotgun = true,
	JAZZ_RunAndSMGStorm = true,
}

JazzAI_PickBestExcludeIds = {
	MGSetup = true,
	MGPack = true,
	MGRotate = true,
	Overwatch = true,
	PinDown = true,
	Reload = true,
	Unjam = true,
	ChangeWeapon = true,
	Bandage = true,
	JazzBandage = true,
	JazzMorphine = true,
	TakeCover = true,
	Hide = true,
	LeaveCover = true,
}

function JazzAI_IsMobileAttackId(action_id)
	return not not (action_id and JazzAI_MobileAttackIds[action_id])
end

function JazzAI_IsAttackActionAvailable(unit, action_id)
	if not IsValid(unit) or not action_id then
		return false
	end
	local action = CombatActions[action_id]
	if not action then
		return false
	end
	local weapon = unit:GetActiveWeapons()
	if not weapon then
		return false
	end
	local in_list = table.find(weapon.AvailableAttacks or empty_table, action_id)
	if not in_list then
		if action_id == "RunAndGun" and weapon:HasComponent("EnableRunNGun") then
			in_list = true
		else
			return false
		end
	end
	return action:GetUIState({unit}) == "enabled"
end

function JazzAI_ResolveMobileAttackId(unit)
	if not IsValid(unit) then
		return false
	end
	local order = {
		"JAZZ_MobileShotgun",
		"RunAndGun",
		"RunAndGun_Carbine",
		"MobileShot",
	}
	for _, id in ipairs(order) do
		if JazzAI_IsAttackActionAvailable(unit, id) then
			return id
		end
	end
	return false
end

g_JAZZ_AIActionMobileShotWrapped = rawget(_G, "g_JAZZ_AIActionMobileShotWrapped") or false
g_JAZZ_AIActionMobileShotPrecalcBase = rawget(_G, "g_JAZZ_AIActionMobileShotPrecalcBase") or false
g_JAZZ_AIActionMobileShotExecuteBase = rawget(_G, "g_JAZZ_AIActionMobileShotExecuteBase") or false

function JazzAI_InstallMobileShotResolve()
	if rawget(_G, "g_JAZZ_AIActionMobileShotWrapped") then
		return
	end
	if not rawget(_G, "AIActionMobileShot") then
		return
	end
	local precalc = AIActionMobileShot.PrecalcAction
	local execute = AIActionMobileShot.Execute
	if type(precalc) ~= "function" or type(execute) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_AIActionMobileShotPrecalcBase", precalc)
	rawset(_G, "g_JAZZ_AIActionMobileShotExecuteBase", execute)
	rawset(_G, "g_JAZZ_AIActionMobileShotWrapped", true)

	function AIActionMobileShot:PrecalcAction(context, action_state)
		local resolved = JazzAI_ResolveMobileAttackId(context and context.unit)
		if not resolved then
			return
		end
		action_state.jazz_mobile_action_id = resolved
		local prev = self.action_id
		self.action_id = resolved
		local base = g_JAZZ_AIActionMobileShotPrecalcBase
		local ok, err = pcall(base, self, context, action_state)
		self.action_id = prev
		if not ok then
			assert(false, tostring(err))
		end
	end

	function AIActionMobileShot:Execute(context, action_state)
		local resolved = (action_state and action_state.jazz_mobile_action_id)
			or JazzAI_ResolveMobileAttackId(context and context.unit)
		if not resolved then
			return
		end
		local prev = self.action_id
		self.action_id = resolved
		local base = g_JAZZ_AIActionMobileShotExecuteBase
		local ok, err = pcall(base, self, context, action_state)
		self.action_id = prev
		if not ok then
			assert(false, tostring(err))
		end
	end
end

JazzAI_InstallMobileShotResolve()

function JazzAI_EstimateAttackShots(weapon, action)
	if not weapon or not action then
		return 1
	end
	local id = action.id or action
	if id == "BurstFire" or id == "AbakanBurst" or id == "JAZZ_ControllableBurst" or id == "JAZZ_Zipper" then
		return weapon.BurstShots or 3
	end
	if id == "AutoFire" or id == "AbakanAutoFire" or id == "JAZZ_LargeAutoFire"
		or id == "JAZZ_SmgStorm" or id == "JAZZ_MGSuppressionFire" then
		return weapon.AutoShots or 5
	end
	if id == "MGBurstFire" then
		if weapon.GetAutofireShots then
			return weapon:GetAutofireShots(action) or (weapon.BurstShots or 3)
		end
		return weapon.BurstShots or 3
	end
	if id == "JAZZ_DoubleTap" or id == "JAZZ_Salvo" or id == "DualShot" or id == "Dualshot"
		or id == "DoubleBarrel" then
		return 2
	end
	if id == "JAZZ_Mozambique" or id == "JAZZ_Fanning" then
		return 3
	end
	if id == "Buckshot" or id == "BuckshotBurst" or id == "AttackShotgun" then
		return weapon.BuckshotProjectiles or 1
	end
	if weapon.GetAutofireShots and IsKindOf(action, "CombatAction") then
		local n = weapon:GetAutofireShots(action)
		if type(n) == "number" and n > 1 then
			return n
		end
	end
	return 1
end

function AISignatureAction:MatchUnit(unit)
	for state, _ in pairs(self.AvailableInState) do
		if not GameState[state] then return end
	end
	for state, _ in pairs(self.ForbiddenInState) do
		if GameState[state] then return end
	end
	for _, keyword in ipairs(self.RequiredKeywords) do
		if not table.find(unit.AIKeywords or empty_table, keyword) then
			return
		end
	end

	if IsKindOf(self, "AIActionMobileShot") then
		return JazzAI_ResolveMobileAttackId(unit) and true
	end

	local attack_type = self.action_id
	if attack_type and CombatActions[attack_type] then
		if not JazzAI_IsAttackActionAvailable(unit, attack_type) then
			return
		end
	end

	return true
end

-- ACT-003: same halfcover predicate as player Unit:MGSetup / Bipod CTH,
-- evaluated as Crouch so Standing does not zero CoverLow.
function JazzAI_IsMGHalfCoverDeploy(unit, aim_pos, stance)
    if not IsValid(unit) or not aim_pos then
        return false
    end
    stance = stance or "Crouch"
    local cover, _, coverage = unit:GetCoverPercentage(aim_pos, nil, stance)
    return cover and cover == const.CoverLow and (coverage or 0) > 80
end

function JazzAI_IsMGHalfCoverAtPos(stand_pos, aim_pos, stance)
    if not stand_pos or not aim_pos then
        return false
    end
    local cover, _, coverage = GetCoverPercentage(stand_pos, aim_pos, stance or "Crouch")
    return cover and cover == const.CoverLow and (coverage or 0) > 80
end

-- Modest EndTurn/OptLoc bias toward usable low cover for MG gunners (ACT-003).
JazzAI_MGHalfCoverDestBonusValue = 45

function JazzAI_ContextNeedsMGHalfCoverBias(context)
    local unit = context and context.unit
    if not unit or unit:HasStatusEffect("StationedMachineGun")
        or unit:HasStatusEffect("ManningEmplacement") then
        return false
    end
    local weapon = context.weapon
    return weapon and IsKindOfClasses(weapon, "MachineGun", "LightMachineGun")
end

function JazzAI_MGHalfCoverDestBonus(context, dest)
    if not JazzAI_ContextNeedsMGHalfCoverBias(context) then
        return 0
    end
    local x, y, z = stance_pos_unpack(dest)
    local dest_pt = point(x, y, z)
    for _, enemy in ipairs(context.enemies or empty_table) do
        local visible = context.enemy_visible and context.enemy_visible[enemy]
        if not visible and context.enemy_visible_by_team then
            visible = context.enemy_visible_by_team[enemy]
        end
        if visible then
            local epos = context.enemy_pack_pos_stance and context.enemy_pack_pos_stance[enemy]
            if epos then
                local ex, ey, ez = stance_pos_unpack(epos)
                if JazzAI_IsMGHalfCoverAtPos(dest_pt, point(ex, ey, ez), "Crouch") then
                    return JazzAI_MGHalfCoverDestBonusValue
                end
            end
        end
    end
    return 0
end

function AIActionMGSetup:PrecalcAction(context, action_state)
    local curr_target_pt = g_Overwatch[context.unit] and
                               g_Overwatch[context.unit].target_pos

    if not context.unit:HasStatusEffect("StationedMachineGun") then
        -- ACT-004: close visible threat → Dump-fire instead of distant OW setup.
        if JazzAI_MGPreferDirectFire(context) then
            return
        end
        -- Zone pick first (LoS from current stance). Halfcover only after aim known.
        action_state.stance = context.unit.stance or "Crouch"
        action_state.jazz_mg_halfcover = false
        context.jazz_mg_cone_eval = true
        AIActionBaseConeAttack.PrecalcAction(self, context, action_state)
        context.jazz_mg_cone_eval = nil
        local aim = action_state.args
            and (action_state.args.target_pos or action_state.args.target)
        if aim and JazzAI_IsMGHalfCoverDeploy(context.unit, aim, "Crouch") then
            action_state.stance = "Crouch"
            action_state.jazz_mg_halfcover = true
        else
            action_state.stance = "Prone"
            action_state.jazz_mg_halfcover = false
        end
    else
        local zones = AIPrecalcConeTargetZones(context, self.action_id,
                                               curr_target_pt)
        local cur_zone = zones[#zones]
        if not cur_zone then return end
        cur_zone.score_mod = self.cur_zone_mod
        context.jazz_mg_cone_eval = true
        local zone, best_score = self:EvalZones(context, zones)
        context.jazz_mg_cone_eval = nil

        -- check best zone:
        if not zone then -- no suitable zone, pack up
            action_state.action_id = "MGPack"
        elseif zone ~= cur_zone then -- another best zone, rotate
            action_state.action_id = "MGRotate"
            action_state.target_pos = zone.target_pos
        end

        if action_state.action_id then
            action_state.score = best_score
            action_state.target_pos = zone and zone.target_pos

            local caction = CombatActions[action_state.action_id]
            if not caction then return end

            local args, has_ap = AIGetAttackArgs(context, caction, nil, "None")
            action_state.has_ap = has_ap
            if has_ap then g_LastSelectedZone = zone end
        end
    end
end

function AIActionMGSetup:Execute(context, action_state)
    assert(action_state.has_ap)
    local args = {}
    local action_id = action_state.action_id or self.action_id
    if action_id ~= "MGPack" then
        assert(action_state.args)
        args.target = action_state.args.target_pos
    end
    -- Always re-check at execute pos (Precalc may have run before Move).
    -- Crouch first so Unit:MGSetup sees CoverLow (Standing zeroes it).
    if action_id == "MGSetup" and args.target
        and JazzAI_IsMGHalfCoverDeploy(context.unit, args.target, "Crouch") then
        if context.unit.stance ~= "Crouch" then
            AIPlayChangeStance(context.unit, "Crouch", args.target)
        end
    end
    AIPlayCombatAction(action_id, context.unit, nil, args)
    if action_state.action_id == "MGPack" then
        return "restart"
    end
end

function AIActionBaseZoneAttack:EvalZones(context, zones)
	-- Smoke-only signatures (BiasId SmokeGrenade): curtain doctrine. Do not treat
	-- Stun/frag entries that merely list smoke among AllowedAoeTypes as smoke eval.
	local smoke_only = self.AllowedAoeTypes and self.AllowedAoeTypes.smoke
		and not self.AllowedAoeTypes.none and not self.AllowedAoeTypes.fire
	if smoke_only or self.BiasId == "SmokeGrenade" then
		context.jazz_smoke_eval = true
		context.jazz_smoke_blast = context.jazz_smoke_blast or (const.SlabSizeX * 4)
	end
	local best_target, best_score = AIEvalZones(context, zones, self.min_score, self.enemy_score,
		self.team_score, self.self_score_mod, self.enemy_cover_mod)
	context.jazz_smoke_eval = nil
	return best_target, best_score
end

-- ACT-002 helpers: smoke curtain targets + scoring (OW → ally exit; self-cover after acted).
local function JazzAI_UnpackAllyExitPos(ally)
	if not IsValid(ally) then
		return
	end
	local dest = ally.ai_context and ally.ai_context.ai_destination
	if dest then
		local x, y, z = stance_pos_unpack(dest)
		return point(x, y, z), true
	end
	return ally:GetPos(), false
end

local function JazzAI_EnemyOverwatchOrigin(enemy)
	if not IsValid(enemy) then
		return
	end
	local ow = g_Overwatch and g_Overwatch[enemy]
	if ow then
		return ow.target_pos or enemy:GetPos(), true
	end
	-- Soft threat: last attack / visible enemy position as stand-in for a fire lane.
	if enemy.last_attack_pos then
		return enemy.last_attack_pos, false
	end
	return enemy:GetPos(), false
end

local function JazzAI_DistPointToSegment2D(pt, a, b)
	if not pt or not a or not b then
		return const.SlabSizeX * 1000
	end
	local ax, ay = a:xy()
	local bx, by = b:xy()
	local px, py = pt:xy()
	local abx, aby = bx - ax, by - ay
	local apx, apy = px - ax, py - ay
	local ab2 = abx * abx + aby * aby
	if ab2 <= 0 then
		return pt:Dist2D(a)
	end
	local t = MulDivRound(apx * abx + apy * aby, 4096, ab2)
	t = Clamp(t, 0, 4096)
	local cx = ax + MulDivRound(abx, t, 4096)
	local cy = ay + MulDivRound(aby, t, 4096)
	return point(px, py):Dist2D(point(cx, cy))
end

function JazzAI_CollectSmokeCurtainTargets(context, min_range, max_range, blast_radius)
	local unit = context.unit
	local pts = {}
	local seen = {}
	local function add_pt(pt)
		if not pt then
			return
		end
		local key = point_pack(WorldToVoxel(pt))
		if seen[key] then
			return
		end
		seen[key] = true
		pts[#pts + 1] = pt
	end

	for _, ally in ipairs(unit.team and unit.team.units or empty_table) do
		if IsValid(ally) and not ally:IsDead() and ally ~= unit then
			local exit_pos, has_dest = JazzAI_UnpackAllyExitPos(ally)
			local acted = JazzAI_AllyHasActed and JazzAI_AllyHasActed(ally)
			-- Self-cover candidate: already acted — allow landing on/near them.
			if acted and exit_pos then
				add_pt(exit_pos)
			end
			for _, enemy in ipairs(context.enemies or empty_table) do
				local ow_pos, is_ow = JazzAI_EnemyOverwatchOrigin(enemy)
				if ow_pos and exit_pos then
					-- Curtain: prefer allies who still plan a dash (dest) under OW / fire lane.
					if is_ow or has_dest then
						add_pt((ow_pos + exit_pos) / 2)
						-- Bias toward the exit corner (angle they want to clear).
						add_pt(exit_pos)
						if has_dest then
							local cur = ally:GetPos()
							if cur and cur:Dist2D(exit_pos) > const.SlabSizeX then
								add_pt((cur + exit_pos) / 2)
							end
						end
					end
				end
			end
		end
	end

	-- Fallback: vanilla AOE candidate pool so smoke still has somewhere to land.
	local base = AICalcAOETargetPoints(context, min_range, max_range, blast_radius)
	for _, pt in ipairs(base or empty_table) do
		add_pt(pt)
	end

	AIFilterTargetPoints(unit, pts, min_range, max_range)
	return pts
end

-- Keep smoke target points even when PropagateSmoke hits no unit heads (pure curtain).
function JazzAI_EnsureSmokeZones(context, action_id, target_pts, zones, aoeType)
	zones = zones or {}
	if not target_pts or #target_pts == 0 then
		return zones
	end
	local have = {}
	for _, z in ipairs(zones) do
		if z.target_pos then
			have[point_pack(WorldToVoxel(z.target_pos))] = true
		end
	end
	for _, pt in ipairs(target_pts) do
		local key = point_pack(WorldToVoxel(pt))
		if not have[key] then
			zones[#zones + 1] = { target_pos = pt, units = {} }
			have[key] = true
		end
	end
	return zones
end

function JazzAI_ScoreSmokeZone(context, zone)
	local score = 0
	local target_pos = zone and zone.target_pos
	local blast = context.jazz_smoke_blast or (const.SlabSizeX * 4)
	local unit = context.unit
	local curtain_hits = 0

	for _, ally in ipairs(unit.team and unit.team.units or empty_table) do
		if IsValid(ally) and not ally:IsDead() and ally ~= unit then
			local exit_pos, has_dest = JazzAI_UnpackAllyExitPos(ally)
			local acted = JazzAI_AllyHasActed and JazzAI_AllyHasActed(ally)
			for _, enemy in ipairs(context.enemies or empty_table) do
				local ow_pos, is_ow = JazzAI_EnemyOverwatchOrigin(enemy)
				if ow_pos and exit_pos and target_pos then
					local dist = JazzAI_DistPointToSegment2D(target_pos, ow_pos, exit_pos)
					if dist <= blast then
						local bonus = is_ow and 140 or 60
						if has_dest then
							bonus = bonus + 40
						end
						-- Stronger when ally still has a move planned (curtain for dash).
						if has_dest and not acted then
							bonus = bonus + 40
						end
						score = score + bonus
						curtain_hits = curtain_hits + 1
					end
				end
			end
		end
	end

	for _, u in ipairs(zone.units or empty_table) do
		if IsValid(u) and not u:IsDead() and not u:IsDowned() then
			if u:IsOnEnemySide(unit) then
				-- Do not smother enemies you still want to shoot.
				score = score - 50
			elseif u.team == unit.team then
				if u == unit then
					-- Thrower may end in own smoke; mild only.
					score = score + 15
				elseif JazzAI_AllyHasActed and JazzAI_AllyHasActed(u) then
					-- Direct self-cover only after ally already acted.
					score = score + 70
				else
					-- Blinding allies who still need to shoot/move this turn.
					score = score - 90
				end
			end
		end
	end

	-- Empty curtain / no acted cover → fail min_score unless curtain landed.
	if curtain_hits == 0 and score < 100 then
		score = Min(score, 40)
	end
	return score
end

function AIEvalZones(context, zones, min_score, enemy_score, team_score,
                     self_score_mod, enemy_cover_score) -- , heigth_score)
    local best_target, best_score = nil, (min_score or 0) - 1
    local close_enemies = context.jazz_mg_cone_eval and JazzAI_ContextCloseEnemies(context)
        or empty_table
    local close_bonus = JazzAI_MGCloseEnemyZoneBonus or 160
    local miss_penalty = JazzAI_MGMissedCloseZonePenalty or 220

    for _, zone in ipairs(zones) do
        local score
		if context.jazz_smoke_eval and JazzAI_ScoreSmokeZone then
			score = JazzAI_ScoreSmokeZone(context, zone)
		else
			local selfmod = 0
			for _, unit in ipairs(zone.units) do
				local uscore = 0
				if not unit:IsDead() and not unit:IsDowned() then
					if unit:IsOnEnemySide(context.unit) then
						uscore = enemy_score or 0
						if enemy_cover_score and enemy_cover_score ~= 0 then
							local cover_high, cover_low = GetCoverTypes(unit)
							if cover_low or cover_high then
								uscore = uscore + enemy_cover_score
							end
						end
						-- ACT-004: prefer cones that cover close threats.
						if context.jazz_mg_cone_eval then
							local dist = context.unit:GetDist(unit)
							if dist <= JazzAI_MGCloseFireRange() then
								uscore = uscore + close_bonus
							end
						end
					elseif unit.team == context.unit.team then
						uscore = team_score or 0
						if unit == context.unit then
							selfmod = self_score_mod or 0
						end
					end
				end
				score = (score or 0) + uscore
			end
			if context.jazz_mg_cone_eval and #close_enemies > 0 then
				for _, ce in ipairs(close_enemies) do
					if not table.find(zone.units, ce) then
						score = (score or 0) - miss_penalty
					end
				end
			end
			score = score and MulDivRound(score, zone.score_mod or 100, 100)
			score = score and MulDivRound(score, 100 + selfmod, 100)
		end

		if score and score > best_score then
			best_target, best_score = zone, score
		end
		zone.score = score
	end
	return best_target, best_score
end

-- JAZZ-AI-MED-001: only plan Bandage when heal score > 0; use kit Bandage or
-- field JazzBandage when the medic only has stack bandages.
function AIActionBandage:PrecalcAction(context, action_state)
	local unit = context.unit
	local x, y, z = unit:GetGridCoords()
	local grid_voxel = point_pack(x, y, z)
	local dest = GetPackedPosAndStance(unit)
	local target, score = AISelectHealTarget(context, dest, grid_voxel, self)
	if not target or not score or score <= 0 then
		return
	end

	local bleeding = type(rawget(_G, "JazzHasAnyBleed")) == "function" and JazzHasAnyBleed(target)
		or target:HasStatusEffect("Bleeding")
		or target:HasStatusEffect("BleedingMedium")
		or target:HasStatusEffect("BleedingHeavy")
	local kit = JazzGetEquippedKitMedicine and JazzGetEquippedKitMedicine(unit)
	local field = JazzGetBandageItem and JazzGetBandageItem(unit)
	local action_id = "Bandage"
	if kit then
		action_id = "Bandage"
	elseif bleeding and field then
		action_id = "JazzBandage"
	else
		return
	end

	local caction = CombatActions[action_id]
	if not caction then
		return
	end
	action_state.args = {
		target = target,
		goto_pos = SnapToVoxel(unit:GetPos()),
	}
	action_state.jazz_bandage_action = action_id
	action_state.score = score
	local cost = caction:GetAPCost(unit, action_state.args)
	action_state.has_ap = (cost >= 0) and unit:HasAP(cost)
end

-- MED-001: Bandage fail-safe — do not freeze turn when target unreachable
function AIActionBandage:Execute(context, action_state)
	assert(action_state.has_ap)
	local unit = context.unit
	local target = action_state.args and action_state.args.target
	if not IsValidTarget(target) then
		context.jazz_medic_bandage_fail = true
		return
	end
	if not IsMeleeRangeTarget(unit, nil, nil, target) then
		context.jazz_medic_bandage_fail = true
		-- revert to faction Frontliner for remainder of Think/Play
		if JazzAI_FactionArchetypePrefix then
			local id = JazzAI_FactionArchetypePrefix(unit) .. "Frontliner"
			unit.archetype = id
			if context.archetype and Presets and Presets.AIArchetype then
				local preset = Presets.AIArchetype.Default and Presets.AIArchetype.Default[id]
				if preset then
					context.archetype = preset
				end
			end
		end
		return
	end
	unit:Face(target)
	local action_id = action_state.jazz_bandage_action or "Bandage"
	AIPlayCombatAction(action_id, unit, nil, action_state.args)
	return "stop"
end

-- ACT-001: lower OW min_score in LowVis when few enemies visible
local JazzAI_AIConeAttack_Precalc = AIConeAttack and AIConeAttack.PrecalcAction
if AIConeAttack and JazzAI_AIConeAttack_Precalc then
	function AIConeAttack:PrecalcAction(context, action_state)
		local profile = context and context.jazz_profile
		local saved
		if profile and profile.OverwatchMinScore and self.action_id == "Overwatch" then
			local visible = 0
			for _, e in ipairs(context.enemies or empty_table) do
				if context.enemy_visible and context.enemy_visible[e] then
					visible = visible + 1
				end
			end
			local peek_boost = false
			for _, e in ipairs(context.enemies or empty_table) do
				if JazzAI_EnemyPeekStreak and JazzAI_EnemyPeekStreak(e) >= 2 then
					peek_boost = true
					break
				end
			end
			if visible <= 2 or peek_boost then
				saved = self.min_score
				self.min_score = Min(self.min_score or 300, profile.OverwatchMinScore)
				if peek_boost then
					self.min_score = Min(self.min_score, 100)
				end
			end
		end
		local result = JazzAI_AIConeAttack_Precalc(self, context, action_state)
		if saved ~= nil then
			self.min_score = saved
		end
		return result
	end
end

function AIPolicyIndoorsOutdoors:EvalDest(context, dest, grid_voxel)
    local check = AICheckIndoors(dest) == self.Indoors
    return check and 100 or 0
end


function AIGetAttackTargetingOptions(unit, context, target, action, targeting)
    local visible_parts, targeted_parts
    targeting = targeting or context.archetype.BaseAttackTargeting or empty_table
    action = action or context.default_attack
    if action and IsKindOf(target, "Unit") then
        local args = { target = target, aim = 0 }
        for _, part in ipairs(target:GetBodyParts(context.weapon)) do
            args.target_spot_group = part.id
            local results = action:GetActionResults(unit, args) or empty_table
            if (results.chance_to_hit or 0) > 0 then
                if targeting[part.id] then
                    targeted_parts = table.create_add(targeted_parts, {id = part.id, chance = results.chance_to_hit})
                else
                    visible_parts = table.create_add(visible_parts, {id = part.id, chance = results.chance_to_hit})
                end
            end            
        end
    end
    return targeted_parts or visible_parts
end
