-- Strategic dollar prices for JAZZ Legion UnitData IDs (roadmap 6a / JAZZ-STRATEGY-004).
-- Anchor: full expensive garrison ≈ outpost capacity ≈ 10× DiamondBriefcase ($12000) = $120000.
-- Not wired into spawn costs yet; flat role costs remain until money ledger + generator.

JAZZ_LegionUnitPrices = {
	JAZZ_Legion_AssaultT1_Roughneck = 300,
	JAZZ_Legion_Recruit = 200,
	JAZZ_Legion_AssaultT1_Grenadier = 800,
	JAZZ_Legion_AssaultT1_Crusher = 400,
	JAZZ_Legion_AssaultT2_Pillager = 800,
	JAZZ_Legion_AssaultT2_ShockTrooper = 1000,
	JAZZ_Legion_AssaultT2_Pyro = 1500,
	JAZZ_Legion_AssaultT3_Punisher = 2000,
	JAZZ_Legion_AssaultT3_SkullCrusher = 2000,
	JAZZ_Legion_AssaultT4_Headsman = 3500,

	JAZZ_Legion_FrontT1_Rifleman = 500,
	JAZZ_Legion_FrontT1_Bonemaker = 800,
	JAZZ_Legion_FrontT1_Marauder = 500,
	JAZZ_Legion_FrontT2_Ambusher = 1000,
	JAZZ_Legion_FrontT2_Raider = 1000,
	JAZZ_Legion_FrontT2_Marksman = 1000,
	JAZZ_Legion_FrontT3_Sniper = 2800,
	JAZZ_Legion_FrontT3_Veteran = 2000,
	JAZZ_Legion_FrontT4_Mercenary = 3500,
	JAZZ_Legion_FrontT4_MercenarySniper = 4500,

	JAZZ_Legion_FlankerT1_Warden = 500,
	JAZZ_Legion_FlankerT2_Scout = 1000,
	JAZZ_Legion_FlankerT2_Skirmisher = 1000,
	JAZZ_Legion_FlankerT3_Recon = 2000,
	JAZZ_Legion_FlankerT3_Pathfinder = 2000,
	JAZZ_Legion_FlankerT4_Ranger = 3500,

	JAZZ_Legion_GunnerT1_Gunner = 800,
	JAZZ_Legion_GunnerT2_GMPG = 1500,
	JAZZ_Legion_GunnerT2_AssaultGunner = 1500,
	JAZZ_Legion_GunnerT3_VeteranGunner = 2800,
	JAZZ_Legion_GunnerT4_MercGunner = 4500,

	JAZZ_Legion_LeaderT1_Sergeant = 800,
	JAZZ_Legion_LeaderT2_Lieutenant = 1500,
	JAZZ_Legion_LeaderT3_Captain = 2500,
	JAZZ_Legion_LeaderT4_MercenaryCaptain = 4000,

	JAZZ_Legion_HeavyT1_Rocketeer = 800,
	JAZZ_Legion_HeavyT2_Grenadier = 1500,
	JAZZ_Legion_HeavyT3_Mortarman = 2800,
}

function JAZZ_GetLegionUnitPrice(unit_or_id)
	local id = unit_or_id
	if type(unit_or_id) == "table" then
		id = unit_or_id.unitdatadef_id or unit_or_id.class or unit_or_id.session_id
	end
	if type(id) ~= "string" or id == "" then
		return false
	end
	return JAZZ_LegionUnitPrices[id] or false
end

function JAZZ_GetLegionSquadUnitPriceSum(unit_ids)
	if type(unit_ids) ~= "table" then
		return false
	end
	local sum = 0
	for _, id in ipairs(unit_ids) do
		local price = JAZZ_GetLegionUnitPrice(id)
		if not price then
			return false
		end
		sum = sum + price
	end
	return sum
end
