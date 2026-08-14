function AIBehavior:OnStart(unit)

    if (self.VoiceResponse or "") ~= "" then
		PlayVoiceResponse(unit, self.VoiceResponse)
	end
    
	self:OnActivate(unit)
end

-- JAZZ-AI-DES-001: Deserter LOS-despawn only when player units are far enough.
-- Entrance-marker despawn stays unrestricted. Panicked keeps DespawnAllowed=false.
JazzAI_DeserterSafeDespawnTiles = 16

local function JazzAI_EnsureEntranceMarkers(context)
	if not context then
		return empty_table
	end
	if not context.entrance_markers then
		context.entrance_markers = MapGetMarkers("Entrance") or empty_table
	end
	return context.entrance_markers
end

local function JazzAI_PlayerWithinTiles(unit, tiles)
	if not unit or not tiles or tiles <= 0 then
		return false
	end
	local max_dist = tiles * const.SlabSizeX
	for _, team in ipairs(g_Teams or empty_table) do
		if team.player_team then
			for _, other in ipairs(team.units or empty_table) do
				if other ~= unit and IsValid(other) and not other:IsDead() then
					if unit:GetDist(other) <= max_dist then
						return true
					end
				end
			end
		end
	end
	return false
end

-- JAZZ-AI-CMD-002: assigned Early/Normal/Late, then vanilla Threatened → Late.
function AIBehavior:GetTurnPhase(unit)
	local phase
	local slot = type(rawget(_G, "JazzAI_GetUnitActSlot")) == "function" and JazzAI_GetUnitActSlot(unit)
	if slot and slot.phase then
		phase = slot.phase
	else
		phase = self.turn_phase
	end
	if unit and unit.IsThreatened and unit:IsThreatened() then
		return "Late"
	end
	return phase
end

function RetreatAI:CanDespawn(unit)
	if not self.DespawnAllowed then
		return false
	end
	local context = unit.ai_context
	if not context then
		return false
	end

	-- Exit/entrance escape: always allowed (even next to the player).
	local vx, vy = unit:GetGridCoords()
	for _, marker in ipairs(JazzAI_EnsureEntranceMarkers(context)) do
		if marker:IsVoxelInsideArea(vx, vy) then
			return true
		end
	end

	local pos = GetPassSlab(unit)
	if not pos then
		return false
	end
	local wx, wy, wz = pos:xyz()
	local unit_stance_pos = stance_pos_pack(wx, wy, wz, StancesList[unit.stance])

	-- Unseen / no LOS to enemies: only despawn if player mercs are outside R.
	if not AIHasLOSToEnemyFromDest(unit_stance_pos) and unit_stance_pos == context.unit_stance_pos then
		if JazzAI_PlayerWithinTiles(unit, JazzAI_DeserterSafeDespawnTiles) then
			return false
		end
		return true
	end
end
