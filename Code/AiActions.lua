function AIActionThrowGrenade:PrecalcAction(context, action_state)
    local action_id, grenade
    local actions = {"ThrowGrenadeA", "ThrowGrenadeB", "ThrowGrenadeC", "ThrowGrenadeD", "ThrowGrenadeAG",
                     "ThrowGrenadeBG", "ThrowGrenadeCG", "ThrowGrenadeDG", "ThrowGrenadeAO", "ThrowGrenadeBO"}

    for _, id in ipairs(actions) do
        local caction = CombatActions[id]
        local cost = caction and caction:GetAPCost(context.unit) or -1
        if cost > 0 and context.unit:HasAP(cost) then
            action_id = id
            local weapon = caction:GetAttackWeapons(context.unit)
            local aoetype = weapon.aoeType or "none"
            -- print(weapon)
            -- print(aoetype)
            -- local triggerType = weapon.TriggerType or "Contact"
            if IsKindOfClasses(weapon, "Grenade", "Ordnance", "Flare", "GrenadeItem", "Molotov") and
                self.AllowedAoeTypes[aoetype] then
                -- self.AllowedTriggerTypes[triggerType] then
                grenade = weapon
                break
            end
        end
    end

    -- print(action_id)
    if not action_id or not grenade then
        return
    end

    local max_range = Min(self.MaxDist, grenade:GetMaxAimRange(context.unit) * const.SlabSizeX)
    local blast_radius = grenade.AreaOfEffect * const.SlabSizeX

    -- print("maxrange "..max_range /  const.SlabSizeX)
    -- print(blast_radius)
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
    local zones = AIPrecalcGrenadeZones(context, action_id, self.MinDist, max_range, blast_radius, grenade.aoeType,
        target_pts)

    -- print(zones)
    local zone, score = self:EvalZones(context, zones)
    -- print(zone)
    -- print("score"..score)
    if zone then
        action_state.action_id = action_id
        action_state.target_pos = zone.target_pos
        action_state.score = score
    end

    -- print(action_state.score)
end

function AIFilterTargetPoints(unit, target_pts, min_range, max_range)

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
    if not IsKindOf(hit.obj, "Unit") then
        return false
    end
    -- print("damage "..hit.damage)
    if hit.damage > 0 then
        return true
    end
    for _, effect in ipairs(hit.effects) do
        if effect and effect ~= "" then
            return true
        end
    end
end

function AIPrecalcGrenadeZones(context, action_id, min_range, max_range, blast_radius, aoeType, target_pts)
    if context.target_locked then
        return {}
    end

    if not target_pts then
        target_pts = AICalcAOETargetPoints(context, min_range, max_range, blast_radius)
    else
        -- make sure the target points are within the allowed range
        AIFilterTargetPoints(context.unit, target_pts, min_range, max_range)
    end

    -- print(target_pts)
    -- calculate parabolas and affected units to each target point
    local zones = {}
    local action = CombatActions[action_id]
    local args = {
        target = false
    }
    for i, target_pt in ipairs(target_pts) do
        args.target = target_pt
        local results = action:GetActionResults(context.unit, args)

        local units
        local trajectory = results.trajectory or empty_table
        -- print("trajectory")
        -- print(aoeType)
        local pos = #trajectory > 0 and trajectory[#trajectory].pos or results.target_pos
        if pos and (aoeType == "smoke" or aoeType == "toxicgas" or aoeType == "teargas" or aoeType == "fire") then
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
            zones[#zones + 1] = {
                target_pos = target_pt,
                units = units
            }
        end
    end

    -- print("--print(zones) ")
    -- print(zones)
    ----print("grenade targeting precalc in", GetPreciseTicks() - tstart, "ms")
    return zones
end

function AIReloadWeapons(unit)
    if IsMerc(unit) then
        return
    end

    local action = unit:GetDefaultAttackAction()
    local weapon1, weapon2 = action:GetAttackWeapons(unit)
    if weapon1 and weapon1.jammed then
        weapon1:RepairJammed(weapon1.Condition, unit)
        unit.Mechanical = unit.Mechanical + 1;
        weapon1.Condition = weapon1:GetMaxCondition()
    end
    if weapon2 and weapon2.jammed then
        weapon2:RepairJammed(weapon2.Condition, unit)
        unit.Mechanical = unit.Mechanical + 1;
        weapon2.Condition = weapon2:GetMaxCondition()
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
                -- ammo = ammos[1]
                if unit:CanAddItem("AmmoInventory", ammos[1]) then
                    unit:TryEquip("AmmoInventory", ammos[1])
                else
                    ammo = PlaceInventoryItem(ammos[1].id)
                end
                ammo.Amount = firearm.MagazineSize
                -- InventoryAddItem(unit, ammo)   
                -- ammo.Amount = Max(ammo.Amount, firearm.MagazineSize)
                unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
                CreateFloatingText(unit, T(160472488023, "Reload"))
                -- DoneObject(ammo)
                ObjModified(unit)
            else
                ammos = GetAmmosWithCaliber(firearm.Caliber, "sorted")
                if #ammos > 0 then
                    if unit:CanAddItem("AmmoInventory", ammos[1]) then
                        unit:TryEquip("AmmoInventory", ammos[1])
                    else
                        ammo = PlaceInventoryItem(ammos[1].id)
                    end
                    ammo.Amount = firearm.MagazineSize
                    -- InventoryAddItem(unit, ammo)   
                    unit:ReloadWeapon(firearm, ammo, "delay fx", "ai")
                    CreateFloatingText(unit, T(160472488023, "Reload"))
                    DoneObject(ammo)
                    ObjModified(unit)
                end
            end
        elseif firearm.ammo.Amount < Max(1, firearm.MagazineSize / 2) then
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
    local min_aim, max_aim = context.unit:GetBaseAimLevelRange(context.default_attack, false)

    local cost = context.default_attack_cost
    local num_attacks = Min(ap / cost, context.max_attacks)

    local remaining = ap - num_attacks * cost
    local aims = {}

    local attack_idx = 1
    local unit = context.unit

    local aim = 0

    -- if IsKindOfClasses(context.weapon,"SniperRifle") then local aim = max_aim end
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
    local args = {
        aim = 0
    }

    if context.force_max_aim then
        num_attacks = Min(ap / (cost + aim_cost * max_aim), context.max_attacks)
    end

    local cthtreshold = 100
    -- if IsKindOfClasses(context.weapon,"SniperRifle") then cthtreshold = 100 end
    -- if IsKindOfClasses(context.weapon,"SubmachineGun","Shotgun","Pistol") then cthtreshold = 50 end

    while remaining > (2 * aim_cost) do
        local aim = (aims[attack_idx] or 0)

        if context.unit then
            local cth = context.unit:CalcChanceToHit(target, context.default_attack)
            while cth < 100 and aim <= (max_aim) and remaining > aim_cost do
                aim = aim + 1
                remaining = remaining - 1
                args.aim = aim
                cth = context.unit:CalcChanceToHit(target, context.default_attack, args)
            end
            -- print('aim '..aim.." cth "..cth)
        end

        if aim > context.weapon.MaxAimActions then
            break
        end
        aims[attack_idx] = aim
        attack_idx = attack_idx + 1
        if attack_idx > num_attacks then
            attack_idx = 1
        end
        ----print(aims)
        remaining = remaining - aim_cost
    end

    NetUpdateHash("AICalcAttacksAndAimSmart", num_attacks, aims, aim_cost, context.force_max_aim)
    return num_attacks, aims
end

function IsUnitHiddenFromPlayer(unit)
    if not unit or unit:IsDead() then
        return true
    end

    for _, player in ipairs(g_Units) do
        if player.team and player.team.side == "player1" and not player:IsDead() then
            if player:CanSee(unit) then
                return false -- хотя бы один игрок видит юнита
            end
        end
    end

    return true -- никто не видит
end

function AIExecuteUnitBehavior(unit, force_or_skip_action)
    if not g_Combat or not IsValid(unit) or unit:IsDead() then
        return
    end

    local options = CurrentModOptions or empty_table

    if CurrentModOptions.AutoFastForward ~= "Off" then

        if IsUnitHiddenFromPlayer(unit) then
            g_FastForwardGameSpeed = "Fast"
            UpdateFastForwardGameSpeed()
        else
            g_FastForwardGameSpeed = "Normal"
            UpdateFastForwardGameSpeed()
        end
    end

    if unit.ai_context.behavior then
        local status = unit.ai_context.behavior:Play(unit)
        if g_AIExecutionController then
            g_AIExecutionController:Log("  Behavior %s for unit %s (%d) returned '%s'",
                unit.ai_context.behavior:GetEditorView(), unit.unitdatadef_id, unit.handle, tostring(status))
        end

        if status then -- support behaviors that want to restart or stop the unit's ai
            return status
        end
    end

    -- recheck unit, they could be killed or despawned during Play
    if IsValid(unit) and not unit:IsDead() then

        if CurrentModOptions.AutoFastForward == "Always" then

            if IsUnitHiddenFromPlayer(unit) then
                g_FastForwardGameSpeed = "Fast"
                UpdateFastForwardGameSpeed()
            else
                g_FastForwardGameSpeed = "Normal"
                UpdateFastForwardGameSpeed()
            end
        end

    end

    -- use the rest of the ap (if any) in signature actions and basic attacks
    return AIPlayAttacks(unit, unit.ai_context, unit.ai_context.forced_signature_action, force_or_skip_action) or
               AITakeCover(unit)
end

-- Переработанный AIPlayAttacks: теперь AI может двигаться и стрелять в произвольном порядке
function AIPlayAttacks(unit, context, dbg_action, force_or_skip_action)
    if g_AIExecutionController then
        g_AIExecutionController:Log("Unit %s (%d) start attack sequence", unit.unitdatadef_id, unit.handle)
    end

    -- удалить мёртвых врагов
    local enemies = context.enemies
    for i = #enemies, 1, -1 do
        if not IsValidTarget(enemies[i]) then
            table.remove(enemies, i)
        end
    end

    local remaining_free_ap = unit.free_move_ap
    unit:RemoveStatusEffect("FreeMove")

    local default_attack = context.default_attack
    local default_attack_vr =
        default_attack and default_attack.FiringModeMember == "AttackShotgun" and "AIDoubleBarrel" or "AIAttack"

    -- выполнить signature action (однократно)
    local signature_action = nil
    if dbg_action then
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
    if not context.reposition and not unit:HasStatusEffect("Numbness") then
        signature_action = signature_action or AIChooseSignatureAction(context)
    end

    local voice_response = signature_action and (signature_action:GetVoiceResponse() or "") or default_attack_vr
    if voice_response == "" then
        voice_response = nil
    end

    if signature_action then
        if g_AIExecutionController then
            g_AIExecutionController:Log("  Signature Action: %s", signature_action:GetEditorView())
        end
        signature_action:OnActivate(unit)
        context.action_states = context.action_states or {}
        context.action_states[signature_action] = context.action_states[signature_action] or {}
        if voice_response then
            context.action_states[signature_action].args = context.action_states[signature_action].args or {}
            context.action_states[signature_action].args.voiceResponse = voice_response
        end
        local status = signature_action:Execute(context, context.action_states[signature_action])
        context.ap_after_signature = unit.ActionPoints
        if status then
            return status
        end
        AIReloadWeapons(unit)
        context.max_attacks = context.max_attacks - 1
    end

    unit:SequentialActionsStart()

    while unit.ActionPoints > 0 and context.max_attacks > 0 do
        AIUpdateContext(context, unit)

        -- проверить, хватает ли ОД на текущую атаку
        local attack = context.default_attack
        if not attack or not IsValidTarget(attack.target) or attack.ap > unit.ActionPoints then
            -- пересчёт подходящей атаки
            local new_attack = PickBestAttack(unit, context.attack_target or context.attack_target,
                context.basic_attacks, context.cth_by_aim_map)
            if new_attack and new_attack.ap <= unit.ActionPoints then
                context.default_attack = new_attack
                context.default_attack_cost = new_attack.ap
				context.best_attack = new_attack
            else
                break -- нет подходящей атаки
            end
        end

        -- Обновить видимость
        local any_visible = false
        for _, enemy in ipairs(context.enemies) do
            local visible = context.enemy_visible_by_team[enemy]
            context.enemy_visible[enemy] = visible
            if visible then
                any_visible = true
            end
        end

        -- Пересчитать цели если кто-то виден
        if any_visible then
            AIPrecalcDamageScore(context, {GetPackedPosAndStance(unit)})
        else
            break
        end

        local best_attack = context.best_attack
        local target = best_attack and best_attack.target
        if not IsValidTarget(target) then
            break
        end

        local action = best_attack.action or context.default_attack
        local cost = best_attack.ap or action:GetActionAPCost(unit, target)
        if unit.ActionPoints < cost then
            break
        end

        local args = {
            target = target,
            voiceResponse = voice_response
        }
        local aim_levels = AICalcAttacksAndAimSmart(context, unit.ActionPoints, target)
        args.aim = aim_levels[1]

        local body_parts = AIGetAttackTargetingOptions(unit, context, target)
        if body_parts and #body_parts > 0 then
            local pick = table.weighted_rand(body_parts, "chance", InteractionRand(1000000, "Combat"))
            if pick then
                args.target_spot_group = pick.id
            end
        end

        Sleep(0)
        local result = AIPlayCombatAction(action.id, unit, nil, args)
        AIReloadWeapons(unit)
        context.max_attacks = context.max_attacks - 1

        if not result or not IsValidTarget(unit) then
            break
        end
        while IsKindOf(target, "Unit") and target:IsGettingDowned() do
            WaitMsg("UnitDowned", 20)
        end
    end

    unit:SequentialActionsEnd()
    while not unit:IsIdleCommand() do
        WaitMsg("Idle", 50)
    end

    TryChangeStance(unit)
end

-- бекап чтоб быстро забрать
function _AIPlayAttacks(unit, context, dbg_action, force_or_skip_action)
    -- filter enemies because they might have been killed by a teammate
    if g_AIExecutionController then
        g_AIExecutionController:Log("Unit %s (%d) start attack sequence", unit.unitdatadef_id, unit.handle)
    end
    local enemies = context.enemies
    for i = #enemies, 1, -1 do
        if not IsValidTarget(enemies[i]) then
            table.remove(enemies, i)
        end
    end

    local remaining_free_ap = unit.free_move_ap
    unit:RemoveStatusEffect("FreeMove") -- lose any remaining free movement points, we're going to use actions now
    AIUpdateContext(context, unit)

    if g_AIExecutionController then
        g_AIExecutionController:Log("  Num enemies: %d", #enemies)
        g_AIExecutionController:Log("  Action Points: %d", unit.ActionPoints)
    end

    local dest = not force_or_skip_action and context.ai_destination or GetPackedPosAndStance(unit)

    -- recalc target to make sure we're firing at a valid target, but prefer the already picked target if there's one
    -- table.insert(g_AIDamageScoreLog, string.format("[%s] AIPlayAttacks (%s)", _InternalTranslate(unit.Name or ""), context.archetype.id))
    context.dest_ap[dest] = context.dest_ap[dest] or unit.ActionPoints
    AIPrecalcDamageScore(context, {dest}, context.target_locked or (context.dest_target or empty_table)[dest])

    -- archetype signature actions
    local signature_action
    if dbg_action then
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
    if not context.reposition and not unit:HasStatusEffect("Numbness") then
        signature_action = signature_action or AIChooseSignatureAction(context)
    end

    local default_attack = context.default_attack
    local default_attack_vr = "AIAttack"
    if default_attack and default_attack.FiringModeMember and default_attack.FiringModeMember == "AttackShotgun" then
        default_attack_vr = "AIDoubleBarrel"
    end
    local voice_response = signature_action and (signature_action:GetVoiceResponse() or "") or default_attack_vr
    if voice_response == "" then
        voice_response = nil
    end

    if signature_action then
        if g_AIExecutionController then
            g_AIExecutionController:Log("  Signature Action: %s", signature_action:GetEditorView())
        end
        signature_action:OnActivate(unit)
        ----printf("[signature] %s (%d)", _InternalTranslate(unit.Name or ""), unit.handle)
        if voice_response then
            context.action_states[signature_action].args = context.action_states[signature_action].args or {}
            context.action_states[signature_action].args.voiceResponse = voice_response
        end
        local status = signature_action:Execute(context, context.action_states[signature_action])
        context.ap_after_signature = unit.ActionPoints
        if status then -- support signature actions that want to restart or stop ai turn execution
            return status
        end
        AIReloadWeapons(unit)
        context.max_attacks = context.max_attacks - 1
    else
        if g_AIExecutionController then
            g_AIExecutionController:Log("  No Signature Action chosen")
        end
    end

    local target = (context.dest_target or empty_table)[dest]
    if signature_action and (not IsValidTarget(target) or (IsKindOf(target, "Unit") and target:IsIncapacitated())) then
        -- table.insert(g_AIDamageScoreLog, string.format("[%s] TargetChange (%s)", _InternalTranslate(unit.Name or ""), context.archetype.TargetChangePolicy))
        if context.archetype.TargetChangePolicy == "restart" then
            return "restart"
        end
        context.dest_ap[dest] = unit.ActionPoints
        context.target_locked = nil
        AIPrecalcDamageScore(context, {dest})
        target = context.dest_target[dest]
    end

    if IsValidTarget(target) then
        if g_AIExecutionController then
            g_AIExecutionController:Log("  Target: %s",
                IsKindOf(target, "Unit") and target.unitdatadef_id or target.class)
        end
        -- revert to basic attacks
        local attacks, aim = AICalcAttacksAndAimSmart(context, unit.ActionPoints, target)
        if context.default_attack.id == "Bombard" and AICheckIndoors(dest) then
            attacks = 0
        end

        local args = {
            target = target,
            voiceResponse = voice_response
        }
        if attacks > 1 then
            unit:SequentialActionsStart()
        end
        if g_AIExecutionController then
            g_AIExecutionController:Log("  Executing %d attacks...", attacks)
        end
        local body_parts = AIGetAttackTargetingOptions(unit, context, target)

        for i = 1, attacks do
            args.aim = aim[i]
            args.target_spot_group = nil
            if body_parts and #body_parts > 0 then
                local pick = table.weighted_rand(body_parts, "chance", InteractionRand(1000000, "Combat"))
                if pick then
                    args.target_spot_group = pick.id
                end
            end
            Sleep(0)
            local result = AIPlayCombatAction(context.default_attack.id, unit, nil, args)
            context.max_attack = context.max_attacks - 1
            if g_AIExecutionController then
                g_AIExecutionController:Log("  Attack %d result: %s", i, tostring(result))
            end
            if IsSetpiecePlaying() then
                unit:SequentialActionsEnd()
                return
            end
            AIReloadWeapons(unit)
            if not result or i == attacks or not IsValidTarget(unit) or context.max_attacks <= 0 then
                break
            end
            while IsKindOf(target, "Unit") and target:IsGettingDowned() do
                WaitMsg("UnitDowned", 20)
            end
            if not IsValidTarget(target) or (IsKindOf(target, "Unit") and target:IsIncapacitated()) then
                -- table.insert(g_AIDamageScoreLog, string.format("[%s] TargetChange (%s)", _InternalTranslate(unit.Name or ""), context.archetype.TargetChangePolicy))
                if context.archetype.TargetChangePolicy == "restart" then
                    unit:SequentialActionsEnd()
                    return "restart"
                end
                -- look for another target
                context.dest_ap[dest] = unit.ActionPoints
                context.target_locked = nil
                AIPrecalcDamageScore(context, {dest})
                target = context.dest_target[dest]
                if not IsValidTarget(target) then
                    break
                end
            end
            Sleep(0)
        end
        unit:SequentialActionsEnd()
    elseif unit:HasStatusEffect("StationedMachineGun") and CombatActions.MGPack:GetUIState({unit}) == "enabled" then
        unit:SequentialActionsEnd()
        AIPlayCombatAction("MGPack", unit)
        return "restart"
    else
        if g_AIExecutionController then
            g_AIExecutionController:Log("  No target")
        end
    end
    unit:SequentialActionsEnd()

    while not unit:IsIdleCommand() do
        WaitMsg("Idle", 50)
    end

    if unit.ActionPoints + remaining_free_ap == context.start_ap and not unit:HasStatusEffect("ManningEmplacement") then
        -- no action was taken, use a fallback one
        -- if all fails, move toward optimal loc
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
                local goto_ap = unit.ActionPoints -- context.dest_ap[dest] --cpath.paths_ap[point_pack(x, y, z)] or 0
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
            if context.archetype.FallbackAction == "overwatch" then
                -- try to place overwatch
                revert = not AIPlaceFallbackOverwatch(unit, context)
            end
            if revert then
                -- we're stuck somewhere and unable to move or act, revert back to being Unaware (only if no sight of any enemies)
                local sight = false
                for _, enemy in ipairs(context.enemies) do
                    sight = sight or HasVisibilityTo(unit, enemy)
                end
                if not sight then
                    unit.last_known_enemy_pos = unit.last_known_enemy_pos or AIPickScoutLocation(unit)
                    -- local archetype = "Scout_LastLocation"
                    -- unit.current_archetype = archetype or unit.archetype or "Assault"
                    if not unit.last_known_enemy_pos then
                        table.insert(g_UnawareQueue, unit)
                    end
                end
                -- if not sight and unit.current_archetype == "Scout_LastLocation" then
                --	table.insert(g_UnawareQueue, unit)
                -- end
            end
        end
    end

    TryChangeStance(unit)

    -- local ProneStanceAP = unit:GetStanceToStanceAP(unit.stance, "Prone")
    -- local CrouchStanceAP = unit:GetStanceToStanceAP(unit.stance, "Crouch")
    -- if unit.ActionPoints >= ProneStanceAP and unit.stance ~= "Prone" and not g_Overwatch[unit] then 
    --	--unit:ChangeStance("StanceProne", ProneStanceAP, unit.stance)
    --	AIPlayChangeStance(unit, "Prone")
    -- end
    -- if unit.ActionPoints >= CrouchStanceAP and unit.stance ~= "Prone" and unit.stance ~= "Crouch" and not g_Overwatch[unit] then 
    --	--unit:ChangeStance("CrouchStance", CrouchStanceAP, unit.stance)
    --	AIPlayChangeStance(unit, "Crouch")
    -- end
end

function AIPrecalcDamageScore(context, destinations, preferred_target, debug_data)
    local unit = context.unit
    local weapon = context.weapon
    local action = CombatActions[context.override_attack_id or false] or context.default_attack
    local archetype = context.archetype
    local behavior = context.behavior

    if not weapon or context.reposition or unit:HasStatusEffect("Burning") then
        return
    end
    if not destinations and context.damage_score_precalced then
        return
    end

    local action_targets = action:GetTargets({unit})
    local targets = table.ifilter(action_targets, function(idx, target)
        return unit:IsOnEnemySide(target)
    end)
    if #targets == 0 then
        return
    end
    context.damage_score_precalced = true
    local target_score_mod = {}
    local tsr = archetype.TargetScoreRandomization
    for i, target in ipairs(targets) do
        target_score_mod[i] = 100 + ((tsr > 0) and unit:RandRange(-tsr, tsr) or 0)
    end
    context.target_score_mod = target_score_mod

    local base_mod = unit[weapon.base_skill]
    local cost_ap = context.override_attack_cost or context.default_attack_cost

    local max_check_range, is_melee = AIGetWeaponCheckRange(unit, weapon, action)
    local is_heavy = IsKindOf(weapon, "HeavyWeapon")

    local hit_modifiers = Presets["ChanceToHitModifier"]["Default"]
    -- stance mod
    local modCrouchBonus = 0
    local modProneBonus = 0
    -- if IsKindOf(weapon, "Firearm") then
    -- modCrouchBonus = hit_modifiers.AttackerStance:ResolveValue("CrouchBonus")
    -- modProneBonus = hit_modifiers.AttackerStance:ResolveValue("ProneBonus")
    local value = GetComponentEffectValue(weapon, "AccuracyBonusProne", "bonus_cth")
    if value then
        modProneBonus = modProneBonus + value
    end
    -- end
    -- ground difference mod
    local MinGroundDifference = hit_modifiers.GroundDifference:ResolveValue("RangeThreshold") * const.SlabSizeZ / 100
    local modHighGround = hit_modifiers.GroundDifference:ResolveValue("HighGround")
    local modLowGround = hit_modifiers.GroundDifference:ResolveValue("LowGround")
    -- cover
    local modCover = hit_modifiers.RangeAttackTargetStanceCover:ResolveValue("Cover")
    local modSameTarget = hit_modifiers.SameTarget:ResolveValue("Bonus")

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
        for target_group, mod in pairs(group_modifiers) do
            target_modifiers = target_modifiers or {}
            target_modifiers[target_group] = (target_modifiers[target_group] or 0) + mod
            for _, obj in ipairs(Groups[target_group]) do
                if IsKindOf(obj, "Unit") and not table.find(targets, obj) then
                    table.insert(targets, obj) -- make sure the target is considired regardless if it's an enemy or not
                    table.insert(target_score_mod, 100 + ((tsr > 0) and unit:RandRange(-tsr, tsr) or 0))
                end
            end
        end
    end

    if unit:HasStatusEffect("StationedMachineGun") or unit:HasStatusEffect("ManningEmplacement") then
        local ow_units = {unit}
        targets = table.ifilter(targets, function(idx, target)
            return target:IsThreatened(ow_units, "overwatch")
        end)
    end

    if not IsValidTarget(preferred_target) or
        (IsKindOf(preferred_target, "Unit") and preferred_target:IsIncapacitated() or
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
    destinations = destinations or context.destinations
    NetUpdateHash("AIPrecalcDamageScore", unit, hashParamTable(destinations), hashParamTable(targets), preferred_target)
    for j, upos in ipairs(destinations) do
        local ux, uy, uz, ustance_idx = stance_pos_unpack(upos)
        local ustance = StancesList[ustance_idx]
        uz = uz or terrain.GetHeight(ux, uy)

        local ap = dest_ap[upos] or 0
        local best_target, best_cth
        local best_score = 0
        local potential_targets, target_score, target_cth = {}, {}, {}
        if weapon and ap >= cost_ap then
            local pos_mod = base_mod
            pos_mod = pos_mod + (ustance_idx == 2 and modCrouchBonus or ustance_idx == 3 and modProneBonus or 0)

            local targets_attack_data
            if not is_melee then
                attacker_pos = point(ux, uy, uz)
                lof_params.step_pos = point_pack(ux, uy, uz)
                lof_params.stance = ustance
                targets_attack_data = GetLoFData(unit, targets, lof_params)
            end
            for k, target in ipairs(targets) do
                local tpos = GetPackedPosAndStance(target)
                local dist = stance_pos_dist(upos, tpos)
                if dist <= (max_check_range or dist) and
                    (is_melee or targets_attack_data[k] and not targets_attack_data[k].stuck) then
                    local tx, ty, tz, tstance_idx = stance_pos_unpack(tpos)
                    tz = tz or terrain.GetHeight(tx, ty)
                    local hit_mod = pos_mod
                    if not is_heavy then
                        hit_mod = hit_mod +
                                      (uz > tz + MinGroundDifference and modHighGround or uz < tz - MinGroundDifference and
                                          modLowGround or 0)
                        hit_mod = hit_mod + (unit:GetLastAttack() == target and modSameTarget or 0)
                    end
                    local target_cover = GetCoverFrom(tpos, upos)
                    if target_cover == const.CoverLow or target_cover == const.CoverHigh then
                        hit_mod = hit_mod + modCover
                    end

                    local penalty = is_heavy and 0 or (100 - weapon:GetAccuracy(dist))

                    local mod = hit_mod - penalty -- dist_penalty
                    -- environmental modifiers when applicable
                    local apply, value, target_spot_group, action, weapon1, weapon2, lof, aim, opportunity_attack
                    apply, value = hit_modifiers.Darkness:CalcValue(unit, target, target_spot_group, action, weapon1,
                        weapon2, lof, aim, opportunity_attack, attacker_pos)
                    if apply then
                        mod = mod + value
                    end

                    if not is_heavy and unit:IsPointBlankRange(target) then
                        mod = MulDivRound(mod, 100 + const.AIPointBlankTargetMod, 100)
                    end
                    mod = Max(0, mod)

                    if mod > const.AIShootAboveCTH then
                        -- calc base score based on cth/attacks/aiming
                        local base_mod = mod
                        local attacks, aims = AICalcAttacksAndAimSmart(context, ap, target)
                        mod = 0
                        for i = 1, attacks do
                            local use, bonus
                            if (aims[i] or 0) > 0 then
                                use, bonus = aim_mod:CalcValue(unit, nil, nil, nil, nil, nil, nil, aims[i])
                            end
                            mod = mod + base_mod + (use and bonus or 0)
                        end
                        -- modify score by archetype-specific weight and (optional) targeting policies
                        mod = MulDivRound(mod, archetype.TargetBaseScore, 100)
                        for _, policy in ipairs(target_policies) do
                            local peval = policy:EvalTarget(unit, target)
                            mod = mod + MulDivRound(peval or 0, policy.Weight, 100)
                        end

                        if IsKindOf(target, "Unit") and (target:IsDowned() or target:IsGettingDowned()) then
                            mod = MulDivRound(mod, 5, 100)
                        end

                        local attack_data = targets_attack_data and targets_attack_data[k]
                        local ally_in_danger = attack_data and (attack_data.best_ally_hits_count or 0) > 0

                        if action and action.AimType == "cone" then
                            ally_in_danger = ally_in_danger or
                                                 AIAllyInDanger(context.allies, context.ally_pos, attacker_pos, target,
                                    const.AIFriendlyFire_LOFConeNear, const.AIFriendlyFire_LOFConeFar)
                        else
                            ally_in_danger = ally_in_danger or
                                                 AIAllyInDanger(context.allies, context.ally_pos, attacker_pos, target,
                                    const.AIFriendlyFire_LOFWidth, const.AIFriendlyFire_LOFWidth)
                        end
                        if ally_in_danger then
                            mod = MulDivRound(mod, const.AIFriendlyFire_ScoreMod, 100)
                        end

                        mod = MulDivRound(mod, target_score_mod[k], 100)

                        -- apply group-based modifiers
                        if target_modifiers and IsKindOf(target, "Unit") then
                            local group_mod = 0
                            for _, groupname in ipairs(target.Groups) do
                                group_mod = group_mod + (target_modifiers[groupname] or 0)
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
                        local threshold = MulDivRound(best_score or 0, const.AIDecisionThreshold, 100)
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
                        NetUpdateHash("AIPrecalcDamageScore_mod", target_score[target], mod, threshold)

                    end
                end
            end
        end

        if #potential_targets > 0 then
            local total = 0
            for _, target in ipairs(potential_targets) do
                local score = target_score[target]
                total = total + score
                if debug_data then
                    debug_data[target] = score
                end
                NetUpdateHash("AIPrecalcDamageScore_total", target_score[target], total)
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
            best_target = best_target or potential_targets[#potential_targets] or false
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
        dest_target_score[upos] = best_score
        dest_target[upos] = best_target
        dest_cth[upos] = best_cth
    end
end

function AISignatureAction:MatchUnit(unit)
    for state, _ in pairs(self.AvailableInState) do
        if not GameState.state then
            return
        end
    end
    for state, _ in pairs(self.ForbiddenInState) do
        if GameState and GameState.state then
            return
        end
    end
    for _, keyword in ipairs(self.RequiredKeywords) do
        if not table.find(unit.AIKeywords or empty_table, keyword) then
            return
        end
    end
    --------------------------
    if unit then
        local actions = unit.ui_actions
        local attack_type = self.action_id
        local weapon = unit:GetActiveWeapons()

        if attack_type == "BurstFire" or attack_type == "AutoFire" or attack_type == "RunAndGun" then
            if actions[attack_type] ~= nil then
                local ui_status = actions[attack_type]
                if ui_status and ui_status == "Hidden" then
                    ----print("noburst")
                    return
                end
            else
                return
            end
        end

    end
    --------------------------

    return true
end

function AIActionMGSetup:PrecalcAction(context, action_state)

    local curr_target_pt = g_Overwatch[context.unit] and g_Overwatch[context.unit].target_pos

    local target = curr_target_pt or context.unit
    local cover, any, coverage = context.unit:GetCoverPercentage(target)
    local halfcover = cover and cover == const.CoverLow and coverage > 80

    if not context.unit:HasStatusEffect("StationedMachineGun") then
        -- setup
        if halfcover then
            action_state.stance = "Crouch"
        else
            action_state.stance = "Prone"
        end
        AIActionBaseConeAttack.PrecalcAction(self, context, action_state)
    else
        local zones = AIPrecalcConeTargetZones(context, self.action_id, curr_target_pt)
        local cur_zone = zones[#zones]
        if not cur_zone then
            return
        end
        cur_zone.score_mod = self.cur_zone_mod
        local zone, best_score = self:EvalZones(context, zones)

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
            if not caction then
                return
            end

            local args, has_ap = AIGetAttackArgs(context, caction, nil, "None")
            action_state.has_ap = has_ap
            if has_ap then
                g_LastSelectedZone = zone
            end
        end
    end
end

----RATO

function AIActionBaseZoneAttack:EvalZones(context, zones)
    return AIEvalZones(context, zones, self.min_score, self.enemy_score, self.team_score, self.self_score_mod,
        self.enemy_cover_mod)
end

function AIEvalZones(context, zones, min_score, enemy_score, team_score, self_score_mod, enemy_cover_score) -- , heigth_score)
    local best_target, best_score = nil, (min_score or 0) - 1

    for _, zone in ipairs(zones) do
        local score
        local selfmod = 0
        for _, unit in ipairs(zone.units) do
            local uscore = 0
            if not unit:IsDead() and not unit:IsDowned() then
                if unit:IsOnEnemySide(context.unit) then

                    uscore = enemy_score or 0
                    -----------------------------------

                    if enemy_cover_score and enemy_cover_score ~= 0 then
                        local cover_high, cover_low = GetCoverTypes(unit)
                        if cover_low or cover_high then
                            uscore = uscore + enemy_cover_score
                        end
                    end

                    -- if heigth_score and heigth_score ~= 0 then

                    -----------------------------------

                elseif unit.team == context.unit.team then
                    uscore = team_score or 0
                    if unit == context.unit then
                        selfmod = self_score_mod or 0
                    end
                end
            end
            score = (score or 0) + uscore
        end

        score = score and MulDivRound(score, zone.score_mod or 100, 100)
        score = score and MulDivRound(score, 100 + selfmod, 100)

        -- print("score "..score.."/")
        if score and score > best_score then
            best_target, best_score = zone, score
        end
        zone.score = score
    end
    ----print("AIEvalZones"..best_target.." "..best_score)
    return best_target, best_score
end

function AIPolicyIndoorsOutdoors:EvalDest(context, dest, grid_voxel)
    local check = AICheckIndoors(dest) == self.Indoors
    return check and self.Weight or 0
end

function TryChangeStance(unit)
    if not g_Combat then
        return 0
    end

    if unit:HasPreparedAttack() then
        return 0
    end

    local weapon = unit:GetActiveWeapons()
    if not weapon or not IsKindOf(weapon, "Firearm") then
        return 0
    end

    if unit:CanTakeCover() then
        AITakeCover(unit)
        return 0
    end

    if unit.species == "Human" and unit.stance ~= "Prone" then
        local cover_high, cover_low = GetCoverTypes(unit)
        local ap = unit.ActionPoints
        if not cover_high and not cover_low then
            local prone_AP = unit.stance == "Crouch" and 1000 or 2000
            if HasPerk(unit, "HitTheDeck") then
                prone_AP = 0
            end
            if ap >= prone_AP then
                -- unit:SetActionCommand("ChangeStance", "RATOAI_ChangeStance", prone_AP, "Prone")
                AIPlayChangeStance(unit, "Prone")
                unit.ActionPoints = unit.ActionPoints - prone_AP
                return prone_AP
            end
        end

        if unit.stance ~= "Crouch" then
            local crouch_ap = 1000
            if ap >= crouch_ap then
                -- unit:SetActionCommand("ChangeStance", "RATOAI_ChangeStance", crouch_ap, "Crouch")
                AIPlayChangeStance(unit, "Crouch")
                unit.ActionPoints = unit.ActionPoints - crouch_ap
                return crouch_ap
            end
        end
    end
    return 0
end

function AIGetAttackTargetingOptions(unit, context, target, action, targeting)
    local body_parts
    targeting = targeting or context.archetype.BaseAttackTargeting
    ----
    local valid, fallback = false, {}
    ---
    if IsKindOf(target, "Unit") and targeting then
        action = action or context.default_attack
        ---
        local args = {
            target = target,
            aim = 3
        }
        ---
        local parts = target:GetBodyParts(context.weapon)
        for _, part in ipairs(parts) do
            args.target_spot_group = part.id
            local results = action:GetActionResults(unit, args)
            body_parts = body_parts or {}
            results.chance_to_hit = results.chance_to_hit or 0
            -- table.insert(body_parts, {id = part.id, chance = results.chance_to_hit})
            if results.chance_to_hit > 0 then
                table.insert(fallback, {
                    id = part.id,
                    chance = results.chance_to_hit
                })
                if targeting[part.id] then
                    valid = true
                    -----
                    table.insert(body_parts, {
                        id = part.id,
                        chance = results.chance_to_hit
                    })
                    -----
                end
            end
        end
    end
    ----
    return valid and body_parts or fallback
    ----
end

