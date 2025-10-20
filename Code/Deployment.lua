-- Соседние стороны
local function AdjacentDirs(dir)
    if dir == "North" then
        return {"East", "West"}
    elseif dir == "South" then
        return {"East", "West"}
    elseif dir == "East" then
        return {"North", "South"}
    elseif dir == "West" then
        return {"North", "South"}
    end
    return {}
end

local function CollectEntranceMarkersByDirs(dirs)
    local out = {}
    for _, d in ipairs(dirs) do
        local avail = GetAvailableEntranceMarkers(d)
        for _, m in ipairs(avail or empty_table) do
            table.insert_unique(out, m)
        end
    end
    return out
end

local SIDE_SPLIT_MIN_UNITS = 30

function _GetEnemyDeploymentMarkers()
    local markers = {}
    local _, enemy_squads = GetSquadsInSector(gv_CurrentSectorId)
    local count = 0
    for _, squad in ipairs(enemy_squads or empty_table) do
        local first = squad.units and squad.units[1]
        local udata = first and gv_UnitData[first]
        local dir = udata and udata.arrival_dir -- "North"/"South"/"East"/"West"

        if dir then
            count = count + (squad.units and #squad.units or 0)

            if count >= SIDE_SPLIT_MIN_UNITS then
                local dirs = {dir}
                for _, d in ipairs(AdjacentDirs(dir)) do
                    dirs[#dirs + 1] = d
                end
                local all_side = CollectEntranceMarkersByDirs(dirs)
                for _, m in ipairs(all_side) do
                    table.insert_unique(markers, m)
                end
            else
                local avail = GetAvailableEntranceMarkers(dir)
                for _, m in ipairs(avail or empty_table) do
                    table.insert_unique(markers, m)
                end
            end
        end
    end

    return markers
end

local DEPLOY_DELAY_DEFAULT = 10000
local DEPLOY_DELAY_BY_ARCHETYPE = {
    Skirmisher = 3500,
    Brute = 4000,
    Soldier = 6000,
    Grenadier = 7000,
    HeavyGunner = 8000,
    Soldier_Sniper = 12000,
    Artillery = 20000,
    Medic = 16000
}
-- Небольшой разброс, чтобы не выходили одновременно (± N мс)
local DEPLOY_DELAY_JITTER = 3500

local MOVE_BY_ARCHETYPE = {
    Skirmisher = "Run",
    Brute = "Run",
    Soldier = "CombatWalk",
    Grenadier = "CombatWalk",
    HeavyGunner = "Walk",
    Soldier_Sniper = "Walk"
}

    local offset_x = const.SlabSizeX / 2  - 70 * guic
    local pt_right = point(offset_x, 0, 0)

function Unit:RandomRun()
	local run_angle = self:Random(360 * 60)
	local delta = const.AmbientLife.CowerRunAngleSpanAvoid / 2
    local cower_angle = 30
	if cower_angle - delta < run_angle and run_angle < cower_angle + delta then
		run_angle = cower_angle + (run_angle < cower_angle and -delta or delta)
	end


	
	local dir = Rotate(pt_right, run_angle)
	local pos = self:GetPos()
	local dest = pos + SetLen(dir, const.AmbientLife.CowerRunDist)
	local slab_x, slab_y, slab_z = SnapToPassSlabXYZ(dest)
	while not slab_x and not IsCloser2D(dest, pos, guim) do
		dest = dest - dir
		slab_x, slab_y, slab_z = SnapToPassSlabXYZ(dest)
	end
	if slab_x then
		PlayFX("CowerRun", "start", self, self.gender)
		self:GotoSlab(point(slab_x, slab_y, slab_z))
		PlayFX("CowerRun", "end", self, self.gender)
	end
	self.cower_cooldown = GameTime() + const.AmbientLife.CowerRunCooldownTime

    self:SetState("ar_Standing_To_Crouch", const.eKeepComponentTargets)
    self:UpdateMoveAnim()
end

function Unit:CombatCover(delay,move_anim)

    if delay then
        Sleep(delay)
        if g_Combat then
            if self.combat_behavior == "AdvanceTo" then
                self:SetCombatBehavior()
            end
            return
        end
    end

        local visitable = self:GetVisitable()
        print(visitable)

    		if self:CanChangeCowerSpot() then
			local visitable = self:GetRandomVisitable("low covers")
			if visitable then
				self:FreeVisitable()
				self:ReserveVisitable(visitable)
				
				pos = pos or marker:GetPos()
				self:PlayAnimStyleEndAnim(self.cur_idle_style)
				if self:GotoSlab(pos, nil, nil, "Run") then
					self:UpdateMoveAnim(nil, "Run", pos)
					if self:Goto(pos, "sl") and lookat then
						local angle = visitable.cover and table.rand(lookat, self:Random()) or CalcOrientation(self, lookat)
						self:SetOrientationAngle(angle, 200)
					end
				end
			end
			self.cower_cooldown = false
		end
	


    local marker, pos, lookat = visitable and unpack_params(visitable)
    if marker and IsValidAnim(self, marker.VisitIdle) then
        local anim, phase = self:GetNearbyUniqueRandomAnim(marker.VisitIdle)
        self:SetState(anim, const.eKeepComponentTargets)
        if phase > 0 then self:SetAnimPhase(1, phase) end

        if not IsKindOf(marker, "GridMarker") then
            StoreErrorSource(marker or self,
                             "Invalid marker handle in Unit:AdvanceTo")
            self:SetBehavior()
            return
        end

        local positions = marker:GetAreaPositions()
        if #(positions or empty_table) == 0 then
            self:SetBehavior()
            return
        end

        self:SetBehavior("AdvanceTo", {handle})
        if self.team and self.team.player_enemy then
            self:AddStatusEffect("HighAlert")
        end

        local goto_pos = table.interaction_rand(positions, "Behavior")
        goto_pos = point(point_unpack(goto_pos))
        self:GotoSlab(goto_pos, nil, nil,
                      move_anim or "Walk")

        local x, y = self:GetGridCoords()
        if marker:IsVoxelInsideArea(x, y) then
            self:SetBehavior("Roam", {marker})
            local params = self:GetCommandParamsTbl("AdvanceTo")
            if params.PropagateAnimParams then
                self:SetCommandParams("Roam", params)
            end
        else
            Sleep(100)
        end
    else
        self:RandomRun()
        self:UpdateMoveAnim()
    end
end

function Unit:MoveToCover()
    print("MoveToCover")
    local visitable = self:GetRandomVisitable("low covers")
    if visitable then
        self:ReserveVisitable(visitable)
        local obj, dest, lookat = table.unpack(visitable)
        if dest then
            self:SetPos(dest)
        else
            self:SetPos(obj:GetPosXYZ())
        end
        if visitable.cover then
            local angle = table.rand(lookat, self:Random())
            self:SetOrientationAngle(angle)
        elseif lookat then
            self:Face(lookat)
        else
            self:SetOrientationAngle(obj:GetAngle())
        end
    end
    
    self:SetState("ar_Standing_To_Crouch", const.eKeepComponentTargets)
    
    self:CombatCover(1000,"Run")
    self:UpdateMoveAnim()
end

local function GetDeployDelayForUnit(unit, basedelay)
    local base = DEPLOY_DELAY_BY_ARCHETYPE[unit.archetype] or
                     DEPLOY_DELAY_DEFAULT + basedelay
    -- InteractionRand доступна в JA3; если нет — замени на math.random(-DEPLOY_DELAY_JITTER, DEPLOY_DELAY_JITTER)
    local jitter =
        (InteractionRand(DEPLOY_DELAY_JITTER * 2 + 1, "DeployDelay") -
            DEPLOY_DELAY_JITTER)
    local delay = base + jitter
    if delay < 300 then delay = 300 end
    return delay
end


function Unit:MovementCoverToCover(handle, manim, delay)
  local marker = HandleToObject[handle]
  if not marker or not marker:IsKindOf("GridMarker") then return end
  local h = marker:GetHandle()

  -- первая попытка занять укрытие
  self:MoveToCover()
  Sleep(delay or 500)

  self:SetCommandParams("AdvanceTo", {move_anim = manim or "Walk"})
  self:AdvanceTo(h, delay)
  Sleep(delay or 500)
  
  self:MoveToCover()
  Sleep(delay or 500)
  
  -- затем движение к маркеру (правильная сигнатура)
  self:SetCommandParams("AdvanceTo", {move_anim = manim or "Walk"})
  self:SetCommand("AdvanceTo", h, delay)

  -- по пути иногда обновляем укрытие, но без спама
  for i = 1, 2 do
    Sleep(1500 + self:Random(750))
    self:MoveToCover()
  end

  -- финальный дожим
  Sleep(800)
  self:SetCommand("AdvanceTo", h, 0)
end

function NetSyncEvents.DeploymentToExploration(quick_deploy, person_who_clicked)
    if quick_deploy then
        if netUniqueId == person_who_clicked then HideDeployButton() end
        ShowUnitsOnDeployment(true, netUniqueId == person_who_clicked)
    end

    if not IsDeploymentReady() or not gv_DeploymentStarted then return end

    if gv_Deployment == "defend" then
        -- local delay = 10000 -- Wait a bit before sending the enemies on their way
        local markers_per_group = {}
        local basedelay = 3000
        local defender_markers = MapGetMarkers("Defender", false, function(m)
            return m:IsMarkerEnabled()
        end)
        if next(defender_markers) then
            local _, enemy_squads = GetSectorSquadsToSpawnInTactical(
                                        gv_CurrentSectorId)
            for _, squad in ipairs(enemy_squads) do
                if squad.Side == "neutral" then goto continue end

                local squad_marker = table.interaction_rand(defender_markers) -- move unit to this marker if it was not grouped with other units in SpawnSquads
                for _, session_id in ipairs(squad.units or empty_table) do
                    local marker = false
                    local unit = g_Units[session_id]

                    if not unit then goto continue end

                    for idx, group in ipairs(g_GroupedSquadUnits) do

                        if table.find(group, unit.session_id) then
                            basedelay = basedelay + 3000
                            if not markers_per_group[idx] then
                                markers_per_group[idx] =
                                    table.interaction_rand(defender_markers)
                            end
                            marker = markers_per_group[idx]
                            break
                        end
                    end
                    -- marker = table.interaction_rand(defender_markers) or squad_marker
                    marker = marker or squad_marker

                    local delay = GetDeployDelayForUnit(unit, basedelay)
                    local manim = MOVE_BY_ARCHETYPE[unit.archetype] or "Walk"
                    local h = marker and marker:GetHandle()

                    unit:SetBehavior("MovementCoverToCover", {marker:GetHandle(),manim, delay})
                    unit:SetCommandParams("MovementCoverToCover", {move_anim = manim})
                    --unit:SetCommandParams("AdvanceTo", {move_anim = manim})
                    unit:SetCommand("MovementCoverToCover", marker:GetHandle(),manim, delay)
                    --unit:MoveToCover(basedelay,manim)


                    --unit:SetBehavior("AdvanceTo", {marker:GetHandle(), basedelay+delay})
                    --unit:SetCommandParams("AdvanceTo", {move_anim = manim})
                    --unit:SetCommand("AdvanceTo", marker:GetHandle(), basedelay+delay)
                    --Sleep(delay)
                  --  local function func(unit)
                  --      unit:SetBehavior("AdvanceTo", {marker:GetHandle(), 0})
                  --      unit:SetCommandParams("AdvanceTo", {move_anim = manim})
                  --      unit:SetCommand("AdvanceTo", marker:GetHandle(), 0)
                  --  end

                    --DelayedCall(delay, func)

                    ::continue::
                end

                ::continue::
            end
        end
    end

    gv_DeploymentStarted = false
    SetDeploymentMode(false)
    local firstSelected = Selection and Selection[1]
    if firstSelected and not IsOnScreen(firstSelected) then
        DelayedCall(0, SnapCameraToObj, firstSelected, "player-input")
    end
    SyncStartExploration()
end
