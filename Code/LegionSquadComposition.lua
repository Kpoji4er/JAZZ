-- Officer density + tier complementarity policy (roadmap 6b/6c / JAZZ-STRATEGY-005).
-- Not wired into spawn/generator yet.

JAZZ_LegionOfficerDensity = {
	SergeantPerMen = 8,
	LieutenantPerMen = 15, -- densest allowed; preferred band 15–20
	CaptainPerMen = 30,
}

--- Max LeaderT1_Sergeant slots for squad size n.
function JAZZ_GetLegionMaxSergeants(squad_size)
	local n = tonumber(squad_size) or 0
	if n < 1 then
		return 0
	end
	return math.floor(n / JAZZ_LegionOfficerDensity.SergeantPerMen)
end

--- Max LeaderT2_Lieutenant slots for squad size n.
function JAZZ_GetLegionMaxLieutenants(squad_size)
	local n = tonumber(squad_size) or 0
	if n < 1 then
		return 0
	end
	return math.floor(n / JAZZ_LegionOfficerDensity.LieutenantPerMen)
end

--- Max LeaderT3_Captain slots for squad size n.
function JAZZ_GetLegionMaxCaptains(squad_size)
	local n = tonumber(squad_size) or 0
	if n < 1 then
		return 0
	end
	return math.floor(n / JAZZ_LegionOfficerDensity.CaptainPerMen)
end

--- MercenaryCaptain is required for T4 squad bands (not density-based).
function JAZZ_LegionSquadRequiresMercenaryCaptain(squad_tier)
	local tier = tonumber(squad_tier) or 0
	return tier >= 4
end

--- Officer caps summary for generator / debug.
-- Returns table { sergeants, lieutenants, captains, merc_captain_required }.
function JAZZ_GetLegionOfficerCaps(squad_size, squad_tier)
	return {
		sergeants = JAZZ_GetLegionMaxSergeants(squad_size),
		lieutenants = JAZZ_GetLegionMaxLieutenants(squad_size),
		captains = JAZZ_GetLegionMaxCaptains(squad_size),
		merc_captain_required = JAZZ_LegionSquadRequiresMercenaryCaptain(squad_tier) and 1 or 0,
	}
end
