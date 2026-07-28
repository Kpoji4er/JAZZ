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

-- Role composition allow-lists (roadmap 6b). Consumed by LegionSquadGenerator (STRATEGY-008).
-- `allow_prefixes` match UnitData IDs; officers always use Leader* within density caps.
JAZZ_LegionRoleRecipes = {
	recon = {
		size_min = 8,
		size_max = 12,
		tier_bias = "light",
		allow_prefixes = {
			"JAZZ_Legion_Flanker",
			"JAZZ_Legion_FrontT1",
			"JAZZ_Legion_FrontT2",
			"JAZZ_Legion_Leader",
		},
	},
	patrol = {
		size_min = 12,
		size_max = 18,
		tier_bias = "mixed",
		allow_prefixes = {
			"JAZZ_Legion_Assault",
			"JAZZ_Legion_Front",
			"JAZZ_Legion_Flanker",
			"JAZZ_Legion_GunnerT1",
			"JAZZ_Legion_GunnerT2",
			"JAZZ_Legion_Leader",
		},
	},
	garrison = {
		size_min = 25,
		size_max = 40,
		tier_bias = "heavy",
		allow_prefixes = {
			"JAZZ_Legion_Assault",
			"JAZZ_Legion_Front",
			"JAZZ_Legion_Gunner",
			"JAZZ_Legion_Heavy",
			"JAZZ_Legion_Leader",
		},
	},
	qrf = {
		size_min = 12,
		size_max = 20,
		tier_bias = "t2_plus",
		allow_prefixes = {
			"JAZZ_Legion_AssaultT2",
			"JAZZ_Legion_AssaultT3",
			"JAZZ_Legion_AssaultT4",
			"JAZZ_Legion_FrontT2",
			"JAZZ_Legion_FrontT3",
			"JAZZ_Legion_FrontT4",
			"JAZZ_Legion_GunnerT2",
			"JAZZ_Legion_GunnerT3",
			"JAZZ_Legion_GunnerT4",
			"JAZZ_Legion_HeavyT2",
			"JAZZ_Legion_HeavyT3",
			"JAZZ_Legion_Leader",
		},
	},
	reinforce = {
		size_min = 15,
		size_max = 25,
		tier_bias = "garrison_lite",
		allow_prefixes = {
			"JAZZ_Legion_Assault",
			"JAZZ_Legion_Front",
			"JAZZ_Legion_GunnerT1",
			"JAZZ_Legion_GunnerT2",
			"JAZZ_Legion_HeavyT1",
			"JAZZ_Legion_HeavyT2",
			"JAZZ_Legion_Leader",
		},
	},
	retribution = {
		size_min = 18,
		size_max = 30,
		tier_bias = "strike",
		allow_prefixes = {
			"JAZZ_Legion_AssaultT2",
			"JAZZ_Legion_AssaultT3",
			"JAZZ_Legion_AssaultT4",
			"JAZZ_Legion_FrontT2",
			"JAZZ_Legion_FrontT3",
			"JAZZ_Legion_FrontT4",
			"JAZZ_Legion_GunnerT2",
			"JAZZ_Legion_GunnerT3",
			"JAZZ_Legion_GunnerT4",
			"JAZZ_Legion_Heavy",
			"JAZZ_Legion_Leader",
		},
	},
	supply = {
		size_min = 8,
		size_max = 15,
		tier_bias = "escort",
		allow_prefixes = {
			"JAZZ_Legion_AssaultT1",
			"JAZZ_Legion_AssaultT2",
			"JAZZ_Legion_FrontT1",
			"JAZZ_Legion_FrontT2",
			"JAZZ_Legion_LeaderT1",
			"JAZZ_Legion_LeaderT2",
		},
	},
	shipment = {
		size_min = 8,
		size_max = 15,
		tier_bias = "escort",
		allow_prefixes = {
			"JAZZ_Legion_AssaultT1",
			"JAZZ_Legion_AssaultT2",
			"JAZZ_Legion_FrontT1",
			"JAZZ_Legion_FrontT2",
			"JAZZ_Legion_LeaderT1",
			"JAZZ_Legion_LeaderT2",
		},
	},
	tax = {
		size_min = 6,
		size_max = 12,
		tier_bias = "escort",
		allow_prefixes = {
			"JAZZ_Legion_AssaultT1",
			"JAZZ_Legion_AssaultT2",
			"JAZZ_Legion_FrontT1",
			"JAZZ_Legion_FrontT2",
			"JAZZ_Legion_LeaderT1",
			"JAZZ_Legion_LeaderT2",
		},
	},
	recruiter = {
		size_min = 6,
		size_max = 12,
		tier_bias = "escort",
		allow_prefixes = {
			"JAZZ_Legion_AssaultT1",
			"JAZZ_Legion_FrontT1",
			"JAZZ_Legion_FlankerT1",
			"JAZZ_Legion_LeaderT1",
		},
	},
	manpower = {
		size_min = 6,
		size_max = 12,
		tier_bias = "escort",
		allow_prefixes = {
			"JAZZ_Legion_AssaultT1",
			"JAZZ_Legion_AssaultT2",
			"JAZZ_Legion_FrontT1",
			"JAZZ_Legion_LeaderT1",
		},
	},
}

function JAZZ_GetLegionRoleRecipe(role)
	return role and JAZZ_LegionRoleRecipes[role] or false
end

function JAZZ_LegionUnitAllowedForRole(unit_id, role)
	local recipe = JAZZ_GetLegionRoleRecipe(role)
	if not recipe or type(unit_id) ~= "string" then
		return false
	end
	for _, prefix in ipairs(recipe.allow_prefixes or {}) do
		if string.sub(unit_id, 1, #prefix) == prefix then
			return true
		end
	end
	return false
end
