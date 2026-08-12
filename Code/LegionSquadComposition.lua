-- Officer density + tier complementarity (roadmap 6b/6c / JAZZ-STRATEGY-005).
-- Medic density (JAZZ-STRATEGY-015). Consumed by LegionSquadGenerator.

JAZZ_LegionOfficerDensity = {
	SergeantPerMen = 8,
	LieutenantPerMen = 15, -- densest allowed; preferred band 15–20
	CaptainPerMen = 30,
}

-- Owner band ~1 medic / 10–20 men (2026-08-02). Mid = 15; min 1 once n >= 10.
-- Difficulty (owner 2026-08-10): Easy +1 / Hard −1 vs Normal — Bonemaker is primary Meds loot.
JAZZ_LegionMedicDensity = {
	MedicPerMen = 15,
	MedicMinSquadSize = 10,
	EasyMedicBonus = 1,
	HardMedicPenalty = 1,
	UnitId = "JAZZ_Legion_FrontT1_Bonemaker",
}

function JAZZ_GetLegionMedicUnitId()
	return JAZZ_LegionMedicDensity.UnitId
end

function JAZZ_IsLegionMedicUnit(unit_id)
	return type(unit_id) == "string" and unit_id == JAZZ_LegionMedicDensity.UnitId
end

-- HOTFIX-006: owner 2026-08-13 — these line classes may repeat without same-id / escort-Front caps.
-- Sniper/MG/heavy/specialist buckets and recipe deny_ids still apply to everyone else.
JAZZ_LegionUncappedLineIds = {
	JAZZ_Legion_AssaultT1_Roughneck = true,
	JAZZ_Legion_AssaultT2_Pillager = true,
	JAZZ_Legion_AssaultT2_ShockTrooper = true,
	JAZZ_Legion_FrontT1_Rifleman = true,
	JAZZ_Legion_FrontT1_Marauder = true,
	JAZZ_Legion_FrontT2_Raider = true,
	JAZZ_Legion_FrontT3_Veteran = true,
}

function JAZZ_IsLegionUncappedLineUnit(unit_id)
	return type(unit_id) == "string" and JAZZ_LegionUncappedLineIds[unit_id] and true or false
end

--- Same-id copy cap is off on Mission Impossible (`VeryHard`).
function JAZZ_LegionSameIdCapApplies(difficulty)
	local diff = difficulty
	if diff == nil and Game then
		diff = Game.game_difficulty
	end
	return diff ~= "VeryHard"
end

--- Easy/VeryEasy → +EasyMedicBonus; Hard/VeryHard → −HardMedicPenalty; else 0.
--- Optional override: pass difficulty id string, or omit to read Game.game_difficulty.
function JAZZ_GetLegionMedicDifficultyDelta(difficulty)
	local diff = difficulty
	if diff == nil and Game then
		diff = Game.game_difficulty
	end
	if diff == "Easy" or diff == "VeryEasy" then
		return JAZZ_LegionMedicDensity.EasyMedicBonus or 1
	end
	if diff == "Hard" or diff == "VeryHard" then
		return -(JAZZ_LegionMedicDensity.HardMedicPenalty or 1)
	end
	return 0
end

--- Max Bonemaker slots for squad size n (STRATEGY-015).
--- Optional difficulty: string id, or nil to use Game.game_difficulty.
function JAZZ_GetLegionMaxMedics(squad_size, difficulty)
	local n = tonumber(squad_size) or 0
	if n < 1 then
		return 0
	end
	local dens = JAZZ_LegionMedicDensity
	local by_ratio = math.floor(n / dens.MedicPerMen)
	local base
	if n >= dens.MedicMinSquadSize then
		base = math.max(1, by_ratio)
	else
		base = by_ratio
	end
	local result = base + JAZZ_GetLegionMedicDifficultyDelta(difficulty)
	if n >= dens.MedicMinSquadSize then
		return math.max(1, result)
	end
	return math.max(0, result)
end

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
-- Returns table { sergeants, lieutenants, captains, merc_captain_required, medics }.
-- Optional difficulty forwarded to medic density (STRATEGY-015).
function JAZZ_GetLegionOfficerCaps(squad_size, squad_tier, difficulty)
	return {
		sergeants = JAZZ_GetLegionMaxSergeants(squad_size),
		lieutenants = JAZZ_GetLegionMaxLieutenants(squad_size),
		captains = JAZZ_GetLegionMaxCaptains(squad_size),
		merc_captain_required = JAZZ_LegionSquadRequiresMercenaryCaptain(squad_tier) and 1 or 0,
		medics = JAZZ_GetLegionMaxMedics(squad_size, difficulty),
	}
end

-- Role composition allow-lists (roadmap 6b). Consumed by LegionSquadGenerator (STRATEGY-008).
-- `size_*` = mature. `size_early_*` = day-1 band; growth lerps early→mature (STRATEGY-016).
-- `allow_prefixes` match UnitData IDs; officers always use Leader* within density caps.
JAZZ_LegionRoleRecipes = {
	recon = {
		size_early_min = 4,
		size_early_max = 6,
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
		size_early_min = 5,
		size_early_max = 8,
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
		-- Static defense: no early shrink (STRATEGY-016).
		size_early_min = 25,
		size_early_max = 40,
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
		size_early_min = 6,
		size_early_max = 10,
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
		size_early_min = 6,
		size_early_max = 10,
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
	-- STRATEGY-024: small specialist detachments (sniper / MG / mortar), T3–T4.
	-- Fixed size band (no early→mature growth).
	support = {
		size_early_min = 4,
		size_early_max = 7,
		size_min = 4,
		size_max = 7,
		tier_bias = "specialty",
		allow_prefixes = {
			"JAZZ_Legion_FrontT3",
			"JAZZ_Legion_FrontT4",
			"JAZZ_Legion_GunnerT3",
			"JAZZ_Legion_GunnerT4",
			"JAZZ_Legion_HeavyT3",
			"JAZZ_Legion_FlankerT3",
			"JAZZ_Legion_FlankerT4",
			"JAZZ_Legion_AssaultT3",
			"JAZZ_Legion_AssaultT4",
			"JAZZ_Legion_LeaderT2",
			"JAZZ_Legion_LeaderT3",
			"JAZZ_Legion_LeaderT4",
		},
	},
	retribution = {
		size_early_min = 10,
		size_early_max = 14,
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
		size_early_min = 4,
		size_early_max = 6,
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
		deny_ids = {
			"JAZZ_Legion_FrontT2_Marksman",
		},
	},
	shipment = {
		size_early_min = 4,
		size_early_max = 6,
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
		deny_ids = {
			"JAZZ_Legion_FrontT2_Marksman",
		},
	},
	tax = {
		size_early_min = 4,
		size_early_max = 6,
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
		deny_ids = {
			"JAZZ_Legion_FrontT2_Marksman",
		},
	},
	recruiter = {
		size_early_min = 4,
		size_early_max = 6,
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
		size_early_min = 4,
		size_early_max = 6,
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

-- STRATEGY-024: specialty detachments for role `support`.
-- One archetype per squad; generator picks by weight then fills specialists + escort.
JAZZ_LegionSupportArchetypes = {
	sniper = {
		weight = 34,
		specialist_min = 2,
		specialist_max = 3,
		specialists = {
			"JAZZ_Legion_FrontT3_Sniper",
			"JAZZ_Legion_FrontT4_MercenarySniper",
		},
	},
	mg = {
		weight = 33,
		specialist_min = 2,
		specialist_max = 3,
		specialists = {
			"JAZZ_Legion_GunnerT3_VeteranGunner",
			"JAZZ_Legion_GunnerT4_MercGunner",
		},
	},
	mortar = {
		weight = 33,
		specialist_min = 1,
		specialist_max = 1,
		specialists = {
			"JAZZ_Legion_HeavyT3_Mortarman",
		},
	},
}

-- NoMaps (mainland) size bands — owner lock 2026-08-02 (smaller than Ernie STRATEGY-016).
-- Applied only when JAZZ_NoMapsIsActive(); Ernie/maps keep JAZZ_LegionRoleRecipes sizes.
JAZZ_LegionRoleSizeOverrideNoMaps = {
	recon = { size_early_min = 3, size_early_max = 5, size_min = 6, size_max = 9 },
	patrol = { size_early_min = 4, size_early_max = 6, size_min = 8, size_max = 12 },
	qrf = { size_early_min = 4, size_early_max = 7, size_min = 8, size_max = 14 },
	reinforce = { size_early_min = 4, size_early_max = 7, size_min = 10, size_max = 16 },
	-- support stays 4–7 (no NoMaps shrink; already a micro detachment).
	support = { size_early_min = 4, size_early_max = 7, size_min = 4, size_max = 7 },
	retribution = { size_early_min = 8, size_early_max = 12, size_min = 14, size_max = 22 },
	garrison = { size_early_min = 12, size_early_max = 20, size_min = 12, size_max = 20 },
	tax = { size_early_min = 3, size_early_max = 5, size_min = 5, size_max = 8 },
	recruiter = { size_early_min = 3, size_early_max = 5, size_min = 5, size_max = 8 },
	manpower = { size_early_min = 3, size_early_max = 5, size_min = 5, size_max = 8 },
	supply = { size_early_min = 3, size_early_max = 5, size_min = 5, size_max = 10 },
	shipment = { size_early_min = 3, size_early_max = 5, size_min = 5, size_max = 10 },
}

-- STRATEGY-016 growth curve.
JAZZ_LegionSquadGrowth = {
	DaysToMature = 21,
	HeatToMature = 500,
}

local function lLerpInt(a, b, p)
	a = tonumber(a) or 0
	b = tonumber(b) or a
	p = Clamp(tonumber(p) or 0, 0, 1000)
	return a + DivRound((b - a) * p, 1000)
end

local function lNoMapsSizeProfile()
	return rawget(_G, "JAZZ_NoMapsIsActive") and JAZZ_NoMapsIsActive() or false
end

--- Growth progress 0..1000 from time / heat / gear major (max of signals).
function JAZZ_GetLegionSquadGrowthProgress(region_heat)
	local day_scale = (const and const.Scale and const.Scale.day)
		or (24 * ((const and const.Scale and const.Scale.h) or 1))
	local days = 0
	if Game and Game.CampaignTime and day_scale > 0 then
		days = Game.CampaignTime / day_scale
	end
	local cfg = JAZZ_LegionSquadGrowth
	local p_time = Clamp(DivRound(days * 1000, cfg.DaysToMature), 0, 1000)
	local p_heat = Clamp(DivRound((tonumber(region_heat) or 0) * 1000, cfg.HeatToMature), 0, 1000)
	local tier = (JAZZ_GetLegionTier and JAZZ_GetLegionTier()) or 11
	tier = tonumber(tier) or 11
	local major = Max(1, DivRound(tier, 10)) -- 11→1, 21→2, 31→3
	local p_tier = 0
	if major >= 3 then
		p_tier = 1000
	elseif major >= 2 then
		p_tier = 500
	end
	return Max(p_time, p_heat, p_tier)
end

function JAZZ_GetLegionRoleRecipe(role)
	return role and JAZZ_LegionRoleRecipes[role] or false
end

--- Shallow recipe with size_min/max lerped early→mature for progress 0..1000.
function JAZZ_ResolveLegionRoleRecipe(role, growth_progress)
	local recipe_key = role == "major" and "retribution" or role
	local base = JAZZ_GetLegionRoleRecipe(recipe_key)
	if not base then
		return false
	end
	local early_min = base.size_early_min or base.size_min
	local early_max = base.size_early_max or base.size_max
	local mature_min = base.size_min
	local mature_max = base.size_max
	if lNoMapsSizeProfile() then
		local ov = JAZZ_LegionRoleSizeOverrideNoMaps[recipe_key]
		if ov then
			early_min = ov.size_early_min or early_min
			early_max = ov.size_early_max or early_max
			mature_min = ov.size_min or mature_min
			mature_max = ov.size_max or mature_max
		end
	end
	local p = Clamp(tonumber(growth_progress) or 0, 0, 1000)
	local size_min = lLerpInt(early_min, mature_min, p)
	local size_max = lLerpInt(early_max, mature_max, p)
	if size_max < size_min then
		size_max = size_min
	end
	return {
		size_min = size_min,
		size_max = size_max,
		size_early_min = early_min,
		size_early_max = early_max,
		size_mature_min = mature_min,
		size_mature_max = mature_max,
		tier_bias = base.tier_bias,
		allow_prefixes = base.allow_prefixes,
		deny_ids = base.deny_ids,
		growth_progress = p,
		nomaps_sizes = lNoMapsSizeProfile() and true or false,
	}
end

function JAZZ_LegionUnitAllowedForRole(unit_id, role)
	local recipe = JAZZ_GetLegionRoleRecipe(role)
	if not recipe or type(unit_id) ~= "string" then
		return false
	end
	-- Reserved medic slots for combat generator roles (STRATEGY-015), even if allow-list is T2+.
	-- `major` spawn uses recipe key `retribution` inside the generator.
	if JAZZ_IsLegionMedicUnit(unit_id) then
		if role == "garrison"
			or role == "patrol"
			or role == "recon"
			or role == "qrf"
			or role == "reinforce"
			or role == "support"
			or role == "retribution"
			or role == "major"
		then
			return true
		end
	end
	for _, denied in ipairs(recipe.deny_ids or empty_table) do
		if unit_id == denied then
			return false
		end
	end
	for _, prefix in ipairs(recipe.allow_prefixes or {}) do
		if string.sub(unit_id, 1, #prefix) == prefix then
			return true
		end
	end
	return false
end
