local function lAoEGetAimPoint(obj, pt, start_pos)
    if not pt:IsValidZ() then pt = pt:SetTerrainZ() end
    if not start_pos:IsValidZ() then start_pos = start_pos:SetTerrainZ() end
    local min_range = const.SlabSizeX / 2
    if IsCloser2D(start_pos, pt, min_range) then
        pt = RotateRadius(min_range, obj:GetAngle(), start_pos)
    end
    return pt
end

local AreaTargetMoveAvatarVisibilityDelay = 300

local function VisUpdateThread(blackboard)
    while IsValid(blackboard.movement_avatar) do
        local dt = blackboard.move_avatar_time - RealTime()
        if blackboard.move_avatar_visible ~= blackboard.movement_avatar.visible then
            if dt <= 0 then
                blackboard.movement_avatar:SetVisible(
                    blackboard.move_avatar_visible)
                blackboard.move_avatar_time = RealTime() +
                                                  AreaTargetMoveAvatarVisibilityDelay
                WaitWakeup()
            else
                WaitWakeup(dt)
            end
        else
            WaitWakeup()
        end
    end
end

local function SetAreaMovementAvatarVisibile(dialog, blackboard, visible, time)
    if not IsValidThread(dialog.real_time_threads.MovementAvatarVisibilityUpdate) then
        dialog:CreateThread("MovementAvatarVisibilityUpdate", VisUpdateThread,
                            blackboard)
    end
    if visible == blackboard.move_avatar_visible then return end
    blackboard.move_avatar_visible = visible
    Wakeup(dialog.real_time_threads.MovementAvatarVisibilityUpdate)
end

function GetRingAOETiles(center, stance, min_r, max_r)
    local outer = GetAOETiles(center, stance, max_r)
    local inner = GetAOETiles(center, stance, min_r)
    local ring = {}

    local hash = {}
    for _, p in ipairs(inner) do hash[p:x() * 10000 + p:y()] = true end

    for _, p in ipairs(outer) do
        local key = p:x() * 10000 + p:y()
        if not hash[key] then table.insert(ring, p) end
    end

    return ring
end

local function JAZZ_ApplyMishapTintToSphereTiles(mat, tint)
    if not tint then
        return
    end
    -- CRM_SphereAOETilesMaterial has no `color`; shader reads Fill/Border/Pulse.
    mat.FillColor = tint
    mat.BorderColor = tint
    mat.PulseColor = tint
end

local function JAZZ_ApplyMishapTintToGrenadeSphere(visuals, data)
    local tint = data and data.tint
    local sphere = visuals and visuals.sphere_mesh
    if not tint or not IsValid(sphere) then
        return
    end
    local sm = CRM_GrenadeSphereMaterial:GetById("DefaultGrenadeSphere"):Clone()
    sm.FillColor = tint
    sm.OuterColor = tint
    sm.dirty = true
    sphere:SetCRMaterial(sm)
end

function GrenadeAOEVisuals:RecreateAoeTiles(data)
    self.data = data
    local mesh_pstr = CreateAOETiles(data.step_positions, data.step_objs,
                                     data.los_values)

    -- основной меш
    local aoe_tiles_mesh = self.aoe_tiles_mesh
    if not aoe_tiles_mesh then
        aoe_tiles_mesh = Mesh:new({})
        self.aoe_tiles_mesh = aoe_tiles_mesh
        aoe_tiles_mesh:SetAttachOffset(point(0, 0, -10))
        aoe_tiles_mesh:SetMeshFlags(aoe_tiles_mesh:GetMeshFlags() |
                                        const.mfSortByPosZ | const.mfWorldSpace)
        self:Attach(aoe_tiles_mesh)
    end

    aoe_tiles_mesh:SetMesh(mesh_pstr)

    local m = CRM_SphereAOETilesMaterial:GetById("GrenadeTilesCast"):Clone()
    m.center = data.explosion_pos
    m.radius = data.range
    JAZZ_ApplyMishapTintToSphereTiles(m, data.tint)
    m.dirty = true
    aoe_tiles_mesh:SetCRMaterial(m)
    JAZZ_ApplyMishapTintToGrenadeSphere(self, data)

    -- вторая зона — min_range
    if data.min_range then
        local aoe_tiles_mesh2 = self.aoe_tiles_mesh2
        if not aoe_tiles_mesh2 then
            aoe_tiles_mesh2 = Mesh:new({})
            self.aoe_tiles_mesh2 = aoe_tiles_mesh2
            aoe_tiles_mesh2:SetAttachOffset(point(0, 0, -10))
            aoe_tiles_mesh2:SetMeshFlags(
                aoe_tiles_mesh2:GetMeshFlags() | const.mfSortByPosZ |
                    const.mfWorldSpace)
            self:Attach(aoe_tiles_mesh2)
        end

        local mesh_inner = CreateAOETiles(
                               GetAOETiles(data.explosion_pos, data.stance,
                                           data.min_range), {}, {})
        aoe_tiles_mesh2:SetMesh(mesh_inner)

        local m2 = CRM_SphereAOETilesMaterial:GetById("GrenadeTilesCast")
                       :Clone()
        m2.center = data.explosion_pos
        m2.radius = data.min_range
        JAZZ_ApplyMishapTintToSphereTiles(m2, data.tint)
        m2.dirty = true
        aoe_tiles_mesh2:SetCRMaterial(m2)
    end
end

function SafeDoneMesh(obj)
	if not obj then return end
    if IsValid(obj) then
        DoneObject(obj)
		return
    end

	for _, v in ipairs(obj) do
		if IsValid(v) then DoneObject(v) end
	end

end

function Targeting_AOE_ParabolaAoE(dialog, blackboard, command, pt)
    local attacker = dialog.attacker
    local action = dialog.action
    if dialog:PlayerActionPending(attacker) or dialog.attack_confirmed then
        command = "delete-except-grenade"
    end

    if command == "setup" then
        local weapon = action:GetAttackWeapons(attacker)
        if IsKindOf(weapon, "Grenade") then
            blackboard.grenade_actor = attacker
        end
    elseif command == "delete" or command == "delete-except-grenade" then
        for _, mesh_pair in ipairs(blackboard.meshes) do
            if type(mesh_pair) == "table" then
                for _, mesh in ipairs(mesh_pair) do
                    SafeDoneMesh(mesh)
                end
            else
                SafeDoneMesh(mesh_pair)
            end
        end

        blackboard.meshes = false
        blackboard.meshes = false
        for _, mesh in ipairs(blackboard.arc_meshes) do SafeDoneMesh(mesh) end
        blackboard.arc_meshes = false

        if command ~= "delete-except-grenade" then
            if blackboard.grenade_actor then
                local grenade = action:GetAttackWeapons(attacker)
                if grenade then
                    blackboard.grenade_actor:DetachGrenade(grenade)
                end
            end
        end

        SetAPIndicator(false, "free-aim")
        SetAPIndicator(false, "mishap-chance")
        SetAPIndicator(false, "instakill-chance")
        SetAPIndicator(false, "danger-close")
        ClearDamagePrediction()
        return
    end

    -- Snapping cone to target
    local target = dialog.target or
                       (dialog.potential_target_is_enemy and
                           dialog.potential_target)

    -- Get attack data
    local weapon = action:GetAttackWeapons(attacker)
    local min_aim_range = action:GetMinAimRange(attacker, weapon)
    min_aim_range = min_aim_range and min_aim_range * const.SlabSizeX
    local max_aim_range = action:GetMaxAimRange(attacker, weapon)
    max_aim_range = max_aim_range and max_aim_range * const.SlabSizeX
    local gas = weapon and
                    (weapon.aoeType == "smoke" or weapon.aoeType == "teargas" or
                        weapon.aoeType == "toxicgas")
    local lof_params = {
        weapon = weapon,
        step_pos = dialog.move_step_position or attacker:GetOccupiedPos(),
        stance = "Standing",
        prediction = true
    }
    local attack_data = attacker:ResolveAttackParams(action.id, pt, lof_params)
    local attacker_pos3D = attack_data.step_pos
    if not attacker_pos3D:IsValidZ() then
        attacker_pos3D = attacker_pos3D:SetTerrainZ()
    end
    local attacker_pos = attack_data.step_pos
    local aim_pt = lAoEGetAimPoint(attacker, pt, attacker_pos3D)
    if not IsCloser(attacker_pos3D, aim_pt, max_aim_range + 1) then
        aim_pt = attacker_pos3D + SetLen(aim_pt - attacker_pos3D, max_aim_range)
    end

    aim_pt = weapon:ValidatePos(aim_pt)

    -- Update prediction only when hasn't moved for a while or passed some time
    if not gas and blackboard.prediction_args and
        (RealTime() - blackboard.prediction_time > 0 or
            not blackboard.last_prediction or RealTime() -
            blackboard.last_prediction > 1000) then
        ApplyDamagePrediction(attacker, action, blackboard.prediction_args)
        blackboard.prediction_args = false
        blackboard.last_prediction = RealTime()

        local dialog_target =
            IsKindOf(dialog.target, "Unit") and dialog.target or pt
        dialog:AttackerAimAnimation(dialog_target)
    end

    -- Update targeting if unit not moving and the prediction pos is different or if too far from the last prediction pos
    local moved = dialog.target_as_pos ~= aim_pt or blackboard.attacker_pos ~=
                      attack_data.step_pos
    if not moved then return end

    -- Show damage in hp bars
    dialog.target_as_pos = aim_pt
    dialog.args_gotopos = attacker_pos
    blackboard.attacker_pos = attack_data.step_pos

    -- If no aim pt clear meshes.
    if not aim_pt then
        blackboard.prediction_args = false
        blackboard.last_prediction = false
        ClearDamagePrediction()

        for i, m in ipairs(blackboard.meshes) do DoneObject(m) end
        blackboard.meshes = false

        for i, m in ipairs(blackboard.arc_meshes) do DoneObject(m) end
        blackboard.arc_meshes = false

        SetAPIndicator(1000, "mishap-chance",
                       AttackDisableReasons.InvalidTarget, "append")
        return
    end

    if IsKindOf(weapon, "MishapProperties") then
        local chance = weapon:GetMishapChance(attacker, aim_pt, "async")
        if CthVisible() then
            SetAPIndicator(1, "mishap-chance", T {
                426191353094,
                "<percent(num)> Mishap Chance",
                num = chance
            }, "append", "force update") -- force update because chance may change
        else
            SetAPIndicator(1, "mishap-chance", TFormat.MishapToText(chance),
                           "append", "force update") -- force update because chance may change
        end
        blackboard.mishap_tint = GetCTHColor(100 - chance)
    else
        blackboard.mishap_tint = false
    end

    if IsKindOfClasses(weapon, "HeavyWeapon", "Grenade") and
        HasPerk(attacker, "DangerClose") then
        local targetRange = attacker:GetDist(pt)
        local dangerClose = CharacterEffectDefs.DangerClose
        local rangeThreshold = dangerClose:ResolveValue("rangeThreshold") *
                                   const.SlabSizeX
        if targetRange <= rangeThreshold then
            SetAPIndicator(1, "danger-close", T {
                190936138167,
                "<perkName> - in range",
                perkName = dangerClose.DisplayName
            }, "append")
        else
            SetAPIndicator(false, "danger-close")
        end
    end

    local results, attack_args = action:GetActionResults(attacker, {
        target = aim_pt,
        step_pos = attacker_pos,
        prediction = true
    })

    -- Queue damage prediction
    blackboard.prediction_args = {
        target = aim_pt,
        distance = attacker_pos3D:Dist(aim_pt)
    }
    blackboard.prediction_time = RealTime() + 50

    local attacks = results.attacks or {results}
    blackboard.meshes = blackboard.meshes or {}

    blackboard.arc_meshes = blackboard.arc_meshes or {}
    -- local blackboard2 = blackboard

    local attack_params =
        weapon:GetAreaAttackParams(action.id, attacker, aim_pt)
    local range = attack_params.max_range * const.SlabSizeX
    local min_range = attack_params.min_range * const.SlabSizeX or range
    local stance =
        attack_params.stance or IsValid(attacker) and attacker.stance or 1

    for i, attack in ipairs(attacks) do
        -- Build mesh
        blackboard.meshes[i] = blackboard.meshes[i] or {}
        local attack_args = attack.attack_args or attack_args
        local trajectory = attack.trajectory or empty_table
        local atk_pos = attack_args.target
        local explosion_pos = attack.explosion_pos or
                                  ((#trajectory > 0) and
                                      trajectory[#trajectory].pos)

        if explosion_pos then
            if weapon.coneShaped then
                local cone_length = attack_params.cone_length
                local cone_angle = attack_params.cone_angle
                if terrain.GetHeight(explosion_pos) > explosion_pos:z() - guim then
                    explosion_pos = explosion_pos:SetTerrainZ(guim)
                end
                local target = RotateRadius(cone_length, CalcOrientation(
                                                attack_args.step_pos,
                                                explosion_pos), explosion_pos)
                local step_positions, step_objs, los_values = GetAOETiles(
                                                                  explosion_pos,
                                                                  stance,
                                                                  cone_length,
                                                                  cone_angle,
                                                                  target,
                                                                  "force2d")
                blackboard.meshes[i][1] = CreateAOETilesSector(step_positions,
                                                            step_objs,
                                                            los_values,
                                                            blackboard.meshes[i][1],
                                                            explosion_pos,
                                                            target, 0,
                                                            cone_length,
                                                            cone_angle,
                                                            "GrenadeConeShapedTilesCast")
                if blackboard.mishap_tint and blackboard.meshes[i][1] then
                    blackboard.meshes[i][1]:SetColorModifier(blackboard.mishap_tint)
                end
            else
                local step_positions, step_objs, los_values = GetAOETiles(
                                                                  explosion_pos,
                                                                  stance, range)
                if gas then
                    step_objs, los_values = empty_table, empty_table
                end

                blackboard.meshes[i] = blackboard.meshes[i] or {}

                local tint = blackboard.mishap_tint
                local data_inner = {
                    explosion_pos = explosion_pos,
                    stance = stance,
                    range = min_range,
                    min_range = min_range,
                    step_positions = {},
                    step_objs = {},
                    los_values = {},
                    tint = tint
                }
                local data_outer = {
                    explosion_pos = explosion_pos,
                    stance = stance,
                    range = range,
                    step_positions = step_positions,
                    step_objs = step_objs,
                    los_values = los_values,
                    tint = tint
                }

                if not blackboard.meshes[i][1] then
                    blackboard.meshes[i][1] =
                        GrenadeAOEVisuals:new({}, nil, data_inner)
                else
                    blackboard.meshes[i][1]:RecreateAoeTiles(data_inner)
                    blackboard.meshes[i][1]:SetPos(explosion_pos)
                end

                if not blackboard.meshes[i][2] then
                    blackboard.meshes[i][2] =
                        GrenadeAOEVisuals:new({}, nil, data_outer)
                else
                    blackboard.meshes[i][2]:RecreateAoeTiles(data_outer)
                    blackboard.meshes[i][2]:SetPos(explosion_pos)
                end
            end

            -- Build trajectory mesh
            local arc_mesh = blackboard.arc_meshes[i]
            if not arc_mesh then
                arc_mesh = Mesh:new()
                arc_mesh:SetMeshFlags(const.mfWorldSpace)
                arc_mesh:SetShader(ProceduralMeshShaders.path_contour)
                blackboard.arc_meshes[i] = arc_mesh
            end

            local mesh = pstr("", 1024)

            local attackVector = attacker_pos - atk_pos
            if attackVector:Len() == 0 then attackVector = false end

            local prev
            local prevDir
            local distance = 0
            for _, step in ipairs(trajectory) do
                local pos = step.pos
                if prev then
                    distance, prevDir = CRTrail_AppendLineSegment(mesh, prev,
                                                                  pos, distance,
                                                                  prevDir,
                                                                  attackVector)
                end
                prev = pos
            end

            arc_mesh:SetPos(attacker_pos)
            arc_mesh:SetMesh(mesh)
            local mat = CRM_VisionLinePreset:GetById("CastTrajectoryArc")
                            :Clone()
            mat.length = distance
            -- Same mishap scale as AoE rings / crosshair CTH (JAZZ-GRENADES-001).
            if blackboard.mishap_tint then
                mat.fill_color = blackboard.mishap_tint
                mat.glow_color = blackboard.mishap_tint
            end
            arc_mesh:SetCRMaterial(mat) -- "CastTrajectoryArc")
        else
            if blackboard.meshes[i] then
                SafeDoneMesh(blackboard.meshes[i])
                blackboard.meshes[i] = false
            end

            if blackboard.arc_meshes[i] then
                SafeDoneMesh(blackboard.arc_meshes[i])
                blackboard.arc_meshes[i] = false
            end
            local reason = (#trajectory > 0) and
                               AttackDisableReasons.InvalidTarget or
                               AttackDisableReasons.NoFireArc
            SetAPIndicator(1000, "mishap-chance", reason, "append")
        end
    end

    if g_ShowGrenadeVolume then
        DbgClearVectors()
        for _, voxel in ipairs(volume or empty_table) do
            local pos = point(point_unpack(voxel))
            DbgAddVoxel(pos, const.clrWhite)
        end
    end
end

function Targeting_AOE_Cone(dialog, blackboard, command, pt)
    pt = GetCursorPos("walkableFlag")
    local attacker = dialog.attacker
    local action = dialog.action
    if not blackboard.firing_mode_action then
        if action.group == "FiringModeMetaAction" then
            action = GetUnitDefaultFiringModeActionFromMetaAction(attacker,
                                                                  action)
        end
        blackboard.firing_mode_action = action
    end
    action = action.group == "FiringModeMetaAction" and
                 blackboard.firing_mode_action or action

    if action.IsTargetableAttack and not dialog.context.free_aim then
        blackboard.gamepad_aim = false
        return
            Targeting_AOE_Cone_TargetRequired(dialog, blackboard, command, pt)
    end

    if dialog:PlayerActionPending(attacker) then command = "delete" end

    if command == "delete" then

        if blackboard.mesh then
            if IsActivePaused() and dialog.action and
                dialog.action.ActivePauseBehavior == "queue" and
                attacker.queued_action_id == dialog.action.id then
                attacker.queued_action_visual = blackboard.mesh
            else
                
                DoneObject(blackboard.mesh)
            end
            blackboard.mesh = false
            
        end
        if blackboard.movement_avatar then
            UpdateMovementAvatar(dialog, point20, nil, "delete")
        end
        UnlockCamera("AOE-Gamepad")
        SetAPIndicator(false, "free-aim")
        ClearDamagePrediction()
        return
    end

    local shouldGamepadAim = GetUIStyleGamepad()
    local wasGamepadAim = blackboard.gamepad_aim

    if shouldGamepadAim ~= wasGamepadAim then
        if shouldGamepadAim then
            LockCamera("AOE-Gamepad")
            if not CurrentActionCamera then
                SnapCameraToObj(attacker, "force")
            end
        else
            UnlockCamera("AOE-Gamepad")
        end
        blackboard.gamepad_aim = shouldGamepadAim
    end

    -- Get attack data
    local weapon = action:GetAttackWeapons(attacker)
    local aoe_params = action:GetAimParams(attacker, weapon) or
                           (weapon and
                               weapon:GetAreaAttackParams(action.id, attacker))
    if not aoe_params then return end
    local min_aim_range = aoe_params.min_range * const.SlabSizeX
    local max_aim_range = aoe_params.max_range * const.SlabSizeX
    local lof_params =
        { -- todo: building lof_params should be a function of the combat action
            weapon = weapon,
            step_pos = dialog.move_step_position or attacker:GetOccupiedPos(),
            prediction = true
        }
    local attack_data = attacker:ResolveAttackParams(action.id, pt, lof_params)
    local attacker_pos3D = attack_data.step_pos
    if not attacker_pos3D:IsValidZ() then
        attacker_pos3D = attacker_pos3D:SetTerrainZ()
    end

    if not blackboard.movement_avatar then
        UpdateMovementAvatar(dialog, point20, nil, "setup")
        UpdateMovementAvatar(dialog, point20, nil, "update_weapon")
        blackboard.movement_avatar:SetVisible(false)
        blackboard.move_avatar_visible = false
        blackboard.move_avatar_time = RealTime()
        -- blackboard.movement_avatar:SetOpacity(0)
        -- blackboard.movement_avatar_opacity = 0
    end

    if not IsCloser(attacker, attack_data.step_pos, const.SlabSizeX / 2 + 1) then
        UpdateMovementAvatar(dialog, attack_data.step_pos, false, "update_pos")
        local aim_anim = attacker:GetAimAnim(attack_data.action_id,
                                             attack_data.stance)
        blackboard.movement_avatar:SetState(aim_anim, 0, 0)
        blackboard.movement_avatar:Face(pt)
        -- blackboard.movement_avatar:SetVisible(true)
        SetAreaMovementAvatarVisibile(dialog, blackboard, true,
                                      AreaTargetMoveAvatarVisibilityDelay)
        --[[if blackboard.movement_avatar_opacity == 0 then
			local o = blackboard.movement_avatar:GetOpacity()
			local t = MulDivRound(AreaTargetMoveAvatarVisibilityDelay, 100 - o, 100)
			blackboard.movement_avatar:SetOpacity(100, t)
			blackboard.movement_avatar_opacity = 100
		end--]]
    elseif blackboard.movement_avatar then
        -- blackboard.movement_avatar:SetVisible(false)
        SetAreaMovementAvatarVisibile(dialog, blackboard, false,
                                      AreaTargetMoveAvatarVisibilityDelay)
        --[[if blackboard.movement_avatar_opacity ~= 0 then
			local o = blackboard.movement_avatar:GetOpacity()
			local t = MulDivRound(AreaTargetMoveAvatarVisibilityDelay, o, 100)
			blackboard.movement_avatar:SetOpacity(0, t)
			blackboard.movement_avatar_opacity = 0
		end--]]
    end

    if blackboard.gamepad_aim then
        local currentLength = blackboard.gamepad_aim_length
        if not currentLength then currentLength = max_aim_range end

        local gamepadState = GetActiveGamepadState()

        local ptRight = gamepadState and gamepadState.RightThumb or point20
        if ptRight ~= point20 then
            local up = ptRight:y() < -1
            currentLength = currentLength + 500 * (up and -1 or 1)
            currentLength = Clamp(currentLength, min_aim_range, max_aim_range)
            blackboard.gamepad_aim_length = currentLength
        end

        local ptLeft = gamepadState and gamepadState.LeftThumb or point20
        if ptLeft == point20 then
            if blackboard.gamepad_aim_last_pos then
                ptLeft = blackboard.gamepad_aim_last_pos
            else
                local p1 = attacker:GetPos()
                local p2 = p1 + Rotate(point(5 * guim, 0), attacker:GetAngle())
                local s1 = select(2, GameToScreen(p1))
                local s2 = select(2, GameToScreen(p2))
                local angle = CalcOrientation(s1, s2)
                ptLeft = Rotate(point(guim, 0), -angle) -- screen Y is reversed
            end
        end
        blackboard.gamepad_aim_last_pos = ptLeft

        ptLeft = ptLeft:SetY(-ptLeft:y())
        ptLeft = Normalize(ptLeft)

        local cameraDirection = point(camera.GetDirection():xy())
        local directionAngle = atan(cameraDirection:y(), cameraDirection:x())
        directionAngle = directionAngle + 90 * 60
        ptLeft = RotateAxis(ptLeft, axis_z, directionAngle)

        pt = attacker:GetPos() + SetLen(ptLeft, currentLength)

        local zoom = Lerp(800, hr.CameraTacMaxZoom * 10, currentLength,
                          max_aim_range)
        cameraTac.SetZoom(zoom, 50)
    end

    -- Update targeting if unit not moving and the prediction pos is different or if too far from the last prediction pos
    local moved = dialog.target_as_pos ~= pt or blackboard.attacker_pos ~=
                      attack_data.step_pos
    moved = moved or
                (dialog.target_as_pos and dialog.target_as_pos:Dist(pt) > 8 *
                    guim)
    if not moved then return end
    local attacker_pos = attack_data.step_pos
    blackboard.attacker_pos = attacker_pos  

    -- Show damage in hp bars, and highlit hit areas
    local aim_pt = lAoEGetAimPoint(attacker, pt, attacker_pos3D)
    dialog.target_as_pos = aim_pt
    local attack_distance = Clamp(attacker_pos3D:Dist(aim_pt), min_aim_range,
                                  max_aim_range)
    local args = {
        target = aim_pt,
        distance = attack_distance,
        step_pos = dialog.move_step_position
    }
    ApplyDamagePrediction(attacker, action, args)
    dialog:AttackerAimAnimation(pt)

    local cover, any, coverage = attacker:GetCoverPercentage(pt)
    local halfcover = cover and cover == const.CoverLow and coverage > 80
    -- halfcover = attacker:HasStatusEffect("BipodUnfolded")
    -- Show targeting cone
    local cone2d = action.id == "Overwatch" or action.id == "DanceForMe" or
                       action.id == "MGSetup" or action.id == "JAZZ_TargetSweep"
    local cone_target = cone2d and CalcOrientation(attacker_pos, aim_pt) or
                            aim_pt
    local stance = action.id == "MGSetup" and "Prone" or attacker.stance
    if halfcover then stance = attacker.stance end
    -- local stance = (action.id == "MGSetup" and halfcover) and attacker.stance or (action.id == "MGSetup" and not halfcover) and "Prone" or attacker.stance
    --	local stance = action.id == "MGSetup" and "Prone" or attacker.stance
    --	local stance = action.id == ("MGSetup" and halfcover and attacker.stance) or("MGSetup" and "Prone") or attacker.stance
    local step_positions, step_objs, los_values
    if action.id == "EyesOnTheBack" then
        step_positions, step_objs, los_values =
            GetAOETiles(attacker_pos, stance, attack_distance)
        blackboard.mesh = CreateAOETilesCircle(step_positions, step_objs,
                                               blackboard.mesh, attacker_pos3D,
                                               attack_distance, los_values)
    else
        step_positions, step_objs, los_values =
            GetAOETiles(attacker_pos, stance, attack_distance,
                        aoe_params.cone_angle, cone_target, "force2d")
        blackboard.mesh = CreateAOETilesSector(step_positions, step_objs,
                                               los_values, blackboard.mesh,
                                               attacker_pos3D, aim_pt, guim,
                                               attack_distance,
                                               aoe_params.cone_angle, false,
                                               aoe_params.falloff_start)
    end
    blackboard.mesh:SetColorFromTextStyle("WeaponAOE")
end

