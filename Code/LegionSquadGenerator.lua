-- Runtime composition generator for Legion Global AI (roadmap 6c / JAZZ-STRATEGY-008).
-- Builds JAZZ_Legion_* unit lists from role recipes, unit prices, officer density, soft caps.
-- HOTFIX-006: same-id cap + logistics Front-family cap; Marksman deny lives on recipes.

local function lTierRank(unit_id)
	if string.find(unit_id, "T4", 1, true) then
		return 4
	elseif string.find(unit_id, "T3", 1, true) then
		return 3
	elseif string.find(unit_id, "T2", 1, true) then
		return 2
	end
	return 1
end

function JAZZ_GetLegionUnitClassBucket(unit_id)
	if type(unit_id) ~= "string" then
		return "line"
	end
	if JAZZ_IsLegionMedicUnit and JAZZ_IsLegionMedicUnit(unit_id) then
		return "medic"
	end
	if string.find(unit_id, "Leader", 1, true) then
		return "officer"
	end
	if string.find(unit_id, "Gunner", 1, true) then
		return "mg"
	end
	if string.find(unit_id, "Sniper", 1, true) or string.find(unit_id, "Marksman", 1, true) then
		return "sniper"
	end
	if string.find(unit_id, "Heavy", 1, true) then
		return "heavy"
	end
	if string.find(unit_id, "Grenadier", 1, true)
		or string.find(unit_id, "Pyro", 1, true)
		or string.find(unit_id, "Rocketeer", 1, true)
		or string.find(unit_id, "Mortar", 1, true)
	then
		return "specialist"
	end
	return "line"
end

local function lSoftCaps(n)
	n = math.max(n or 0, 1)
	return {
		mg = math.min(4, math.floor(n * 0.35)),
		sniper = math.min(3, math.floor(n * 0.25)),
		heavy = math.min(2, math.floor(n * 0.15)),
		specialist = math.min(3, math.floor(n * 0.20)),
	}
end

local function lCountBucket(units, bucket)
	local count = 0
	for _, id in ipairs(units) do
		if JAZZ_GetLegionUnitClassBucket(id) == bucket then
			count = count + 1
		end
	end
	return count
end

local function lCountId(units, unit_id)
	local count = 0
	for _, id in ipairs(units) do
		if id == unit_id then
			count = count + 1
		end
	end
	return count
end

-- HOTFIX-006: copies of one UnitData ID. n=6 → 2; n≥9 → 3.
-- Uncapped line IDs (Roughneck/Pillager/ShockTrooper/Rifleman/Marauder/Raider/Veteran) skip this.
local function lSameIdCap(n)
	n = math.max(n or 0, 1)
	return math.max(1, math.min(3, math.floor(n * 0.34)))
end

-- Front specialists on logistics escorts (not medic, not owner-uncapped line).
local function lIsEscortFrontLine(unit_id)
	if type(unit_id) ~= "string" then
		return false
	end
	if not string.find(unit_id, "Front", 1, true) then
		return false
	end
	if JAZZ_IsLegionMedicUnit and JAZZ_IsLegionMedicUnit(unit_id) then
		return false
	end
	if JAZZ_IsLegionUncappedLineUnit and JAZZ_IsLegionUncappedLineUnit(unit_id) then
		return false
	end
	return true
end

-- HOTFIX-006: tax/supply/etc. n=4–7 → 1 Front; n≥8 → 2.
local function lEscortFrontCap(n)
	n = math.max(n or 0, 1)
	return math.min(2, math.max(1, math.floor(n * 0.25)))
end

local function lCountEscortFront(units)
	local count = 0
	for _, id in ipairs(units) do
		if lIsEscortFrontLine(id) then
			count = count + 1
		end
	end
	return count
end

local function lWouldBreakSoftCap(units, candidate, target_size, role)
	local n = math.max(target_size or 0, #(units or empty_table) + 1)
	local bucket = JAZZ_GetLegionUnitClassBucket(candidate)
	-- Officers/medics use density plans; owner-uncapped line may repeat freely.
	-- Same-id copy cap is off on VeryHard (Mission Impossible).
	if bucket ~= "officer" and bucket ~= "medic"
		and not (JAZZ_IsLegionUncappedLineUnit and JAZZ_IsLegionUncappedLineUnit(candidate))
		and (not JAZZ_LegionSameIdCapApplies or JAZZ_LegionSameIdCapApplies())
	then
		if lCountId(units, candidate) >= lSameIdCap(n) then
			return true
		end
	end
	if role and JAZZ_LegionRoleIsLogisticsEscort and JAZZ_LegionRoleIsLogisticsEscort(role) and lIsEscortFrontLine(candidate) then
		if lCountEscortFront(units) >= lEscortFrontCap(n) then
			return true
		end
	end
	-- Line has no specialist-bucket cap (STRATEGY-008); same-id / escort Front already applied.
	if bucket == "line" or bucket == "officer" or bucket == "medic" then
		return false
	end
	local caps = lSoftCaps(n)
	local cap = caps[bucket]
	if not cap then
		return false
	end
	return lCountBucket(units, bucket) >= cap
end

local function lMedicPlan(target_size)
	local plan = {}
	local count = JAZZ_GetLegionMaxMedics and JAZZ_GetLegionMaxMedics(target_size) or 0
	local medic_id = JAZZ_GetLegionMedicUnitId and JAZZ_GetLegionMedicUnitId() or "JAZZ_Legion_FrontT1_Bonemaker"
	for _ = 1, count do
		plan[#plan + 1] = medic_id
	end
	return plan
end

local function lCountMedics(units)
	local count = 0
	for _, id in ipairs(units or empty_table) do
		if JAZZ_IsLegionMedicUnit and JAZZ_IsLegionMedicUnit(id) then
			count = count + 1
		end
	end
	return count
end

local function lEligibleUnits(role)
	local list = {}
	for unit_id, price in sorted_pairs(JAZZ_LegionUnitPrices or empty_table) do
		if type(unit_id) == "string"
			and type(price) == "number"
			and JAZZ_LegionUnitAllowedForRole(unit_id, role)
		then
			list[#list + 1] = {
				id = unit_id,
				price = price,
				tier = lTierRank(unit_id),
				bucket = JAZZ_GetLegionUnitClassBucket(unit_id),
			}
		end
	end
	table.sort(list, function(a, b)
		if a.price ~= b.price then
			return a.price < b.price
		end
		return a.id < b.id
	end)
	return list
end

local function lTierWeight(entry, bias, mode)
	local tier = entry.tier
	if mode == "poor" or bias == "light" or bias == "escort" then
		return ({ [1] = 8, [2] = 3, [3] = 1, [4] = 0 })[tier] or 1
	end
	if bias == "t2_plus" or bias == "strike" then
		return ({ [1] = 0, [2] = 4, [3] = 5, [4] = 3 })[tier] or 1
	end
	if bias == "specialty" then
		-- Support detachments: T3 base, T4 welcome; never T1/T2 line.
		return ({ [1] = 0, [2] = 0, [3] = 5, [4] = 4 })[tier] or 0
	end
	if bias == "heavy" or bias == "garrison_lite" then
		return ({ [1] = 2, [2] = 4, [3] = 4, [4] = 2 })[tier] or 1
	end
	return ({ [1] = 3, [2] = 4, [3] = 3, [4] = 2 })[tier] or 1
end

local function lPickWeighted(entries, context)
	local total = 0
	for _, entry in ipairs(entries) do
		total = total + Max(entry.weight or 0, 0)
	end
	if total <= 0 or #entries == 0 then
		return false
	end
	local roll = InteractionRand(total, "JAZZ_LegionGen_" .. context)
	for _, entry in ipairs(entries) do
		roll = roll - Max(entry.weight or 0, 0)
		if roll < 0 then
			return entry
		end
	end
	return entries[#entries]
end

local function lSupportEscortBucket(unit_id)
	local bucket = JAZZ_GetLegionUnitClassBucket(unit_id)
	return bucket == "line" or bucket == "specialist" or bucket == "sniper" or bucket == "mg" or bucket == "heavy"
end

local function lCollectSupportSpecialists()
	local specialist_ids = {}
	local seen = {}
	for _, def in sorted_pairs(JAZZ_LegionSupportArchetypes or empty_table) do
		for _, id in ipairs(def.specialists or empty_table) do
			if not seen[id] and JAZZ_LegionUnitAllowedForRole(id, "support") and JAZZ_GetLegionUnitPrice(id) then
				seen[id] = true
				specialist_ids[#specialist_ids + 1] = id
			end
		end
	end
	return specialist_ids
end

local function lSupportSpecialistWeight(unit_id, mode)
	local tier = lTierRank(unit_id)
	local weight = ({ [3] = 5, [4] = 4 })[tier] or 1
	if mode == "poor" and tier >= 4 then
		weight = 1
	end
	-- Mortar was specialist_max 1 when mono-archetype; keep it rarer in the mixed pool.
	if string.find(unit_id, "Mortar", 1, true) then
		weight = Max(1, DivRound(weight, 2))
	end
	return weight
end

--- Specialty builder: 1 leader + 2–3 mixed specialists (sniper/MG/mortar pool) + T3 escort.
--- Each slot is an independent roll; STRATEGY-008 / HOTFIX-006 caps apply (no mono clone pack).
--- preferred_archetype is ignored (kept for call-site compat).
local function lTryBuildSupport(recipe, budget_money, budget_manpower, mode, context, preferred_archetype)
	local target = mode == "poor" and recipe.size_min or recipe.size_max
	target = Clamp(target, recipe.size_min, recipe.size_max)
	if budget_manpower and budget_manpower < recipe.size_min then
		return false
	end
	if budget_manpower then
		target = Min(target, budget_manpower)
	end
	if target < recipe.size_min then
		return false
	end

	local specialist_ids = lCollectSupportSpecialists()
	if #specialist_ids == 0 then
		return false
	end

	local want_specialists = 2
	if mode == "full" then
		want_specialists = 3
	end
	-- Leave room for leader + at least one escort when size allows.
	want_specialists = Min(want_specialists, Max(1, target - 2))

	local units = {}
	local spent = 0

	local function lAffordAdd(unit_id)
		local price = JAZZ_GetLegionUnitPrice(unit_id)
		if not price or spent + price > budget_money then
			return false
		end
		if budget_manpower and #units + 1 > budget_manpower then
			return false
		end
		if #units >= target then
			return false
		end
		if lWouldBreakSoftCap(units, unit_id, target, "support") then
			return false
		end
		units[#units + 1] = unit_id
		spent = spent + price
		return true
	end

	-- Force one leader (density caps yield 0 for n≤7).
	local leaders = { "JAZZ_Legion_LeaderT2_Lieutenant", "JAZZ_Legion_LeaderT3_Captain" }
	if mode == "full" then
		leaders = { "JAZZ_Legion_LeaderT3_Captain", "JAZZ_Legion_LeaderT2_Lieutenant", "JAZZ_Legion_LeaderT4_MercenaryCaptain" }
	end
	local leader_ok = false
	for _, lid in ipairs(leaders) do
		if JAZZ_LegionUnitAllowedForRole(lid, "support") and lAffordAdd(lid) then
			leader_ok = true
			break
		end
	end
	if not leader_ok then
		return false
	end

	local specialists_added = 0
	local slot = 0
	while specialists_added < want_specialists and #units < target do
		slot = slot + 1
		local candidates = {}
		for _, id in ipairs(specialist_ids) do
			local price = JAZZ_GetLegionUnitPrice(id)
			if price and spent + price <= budget_money and not lWouldBreakSoftCap(units, id, target, "support") then
				candidates[#candidates + 1] = {
					id = id,
					price = price,
					weight = lSupportSpecialistWeight(id, mode),
				}
			end
		end
		local picked = lPickWeighted(candidates, context .. "_spec_" .. slot)
		if not picked or not lAffordAdd(picked.id) then
			break
		end
		specialists_added = specialists_added + 1
	end
	if specialists_added < 1 then
		return false
	end

	-- Escort: T3+ line/flanker/assault from allow-list; prefer non-specialty buckets.
	local eligible = lEligibleUnits("support")
	local escort_slot = 0
	while #units < target do
		escort_slot = escort_slot + 1
		local candidates = {}
		for _, entry in ipairs(eligible) do
			if entry.bucket ~= "officer"
				and entry.bucket ~= "medic"
				and spent + entry.price <= budget_money
				and lSupportEscortBucket(entry.id)
				and not lWouldBreakSoftCap(units, entry.id, target, "support")
			then
				local weight = lTierWeight(entry, "specialty", mode)
				if entry.bucket == "line" then
					weight = weight + 3
				elseif string.find(entry.id, "Mortar", 1, true)
					or string.find(entry.id, "Sniper", 1, true)
					or string.find(entry.id, "Gunner", 1, true)
					or string.find(entry.id, "MercGunner", 1, true)
				then
					weight = Max(1, weight - 2)
				end
				if weight > 0 then
					candidates[#candidates + 1] = {
						id = entry.id,
						price = entry.price,
						weight = weight,
					}
				end
			end
		end
		local picked = lPickWeighted(candidates, context .. "_escort_" .. escort_slot)
		if not picked or not lAffordAdd(picked.id) then
			break
		end
	end

	if #units < recipe.size_min then
		return false
	end

	return {
		units = units,
		money_cost = spent,
		manpower_cost = #units,
		mode = mode,
		role = "support",
		support_archetype = "mixed",
	}
end

local function lOfficerPlan(target_size, want_t4)
	local caps = JAZZ_GetLegionOfficerCaps(target_size, want_t4 and 4 or 1)
	local plan = {}
	for _ = 1, caps.sergeants or 0 do
		plan[#plan + 1] = "JAZZ_Legion_LeaderT1_Sergeant"
	end
	for _ = 1, caps.lieutenants or 0 do
		plan[#plan + 1] = "JAZZ_Legion_LeaderT2_Lieutenant"
	end
	for _ = 1, caps.captains or 0 do
		plan[#plan + 1] = "JAZZ_Legion_LeaderT3_Captain"
	end
	if (caps.merc_captain_required or 0) > 0 then
		plan[#plan + 1] = "JAZZ_Legion_LeaderT4_MercenaryCaptain"
	end
	return plan
end

local function lMaxTierInList(units)
	local max_tier = 1
	for _, id in ipairs(units) do
		max_tier = Max(max_tier, lTierRank(id))
	end
	return max_tier
end

local function lTryBuild(role, recipe, budget_money, budget_manpower, mode, context)
	local target = mode == "poor" and recipe.size_min or recipe.size_max
	target = Clamp(target, recipe.size_min, recipe.size_max)
	if budget_manpower and budget_manpower < recipe.size_min then
		return false
	end
	if budget_manpower then
		target = Min(target, budget_manpower)
	end
	if target < recipe.size_min then
		return false
	end

	local eligible = lEligibleUnits(role)
	if #eligible == 0 then
		return false
	end

	local want_t4 = mode == "full" and (recipe.tier_bias == "heavy" or recipe.tier_bias == "strike" or recipe.tier_bias == "t2_plus")
	local officers = lOfficerPlan(target, want_t4)
	local medics = lMedicPlan(target)
	local units = {}
	local spent = 0

	for _, officer_id in ipairs(officers) do
		if not JAZZ_LegionUnitAllowedForRole(officer_id, role) then
			goto continue_officer
		end
		local price = JAZZ_GetLegionUnitPrice(officer_id)
		if not price or spent + price > budget_money then
			return false
		end
		if budget_manpower and #units + 1 > budget_manpower then
			return false
		end
		units[#units + 1] = officer_id
		spent = spent + price
		::continue_officer::
	end

	-- Medic density is soft on budget: skip unaffordable slots rather than fail the squad.
	for _, medic_id in ipairs(medics) do
		if not JAZZ_LegionUnitAllowedForRole(medic_id, role) then
			goto continue_medic
		end
		local price = JAZZ_GetLegionUnitPrice(medic_id)
		if not price or spent + price > budget_money then
			goto continue_medic
		end
		if budget_manpower and #units + 1 > budget_manpower then
			goto continue_medic
		end
		if #units >= target then
			break
		end
		units[#units + 1] = medic_id
		spent = spent + price
		::continue_medic::
	end

	local slot = 0
	while #units < target do
		slot = slot + 1
		local candidates = {}
		for _, entry in ipairs(eligible) do
			if entry.bucket ~= "officer"
				and entry.bucket ~= "medic"
				and spent + entry.price <= budget_money
				and not lWouldBreakSoftCap(units, entry.id, target, role)
			then
				local weight = lTierWeight(entry, recipe.tier_bias, mode)
				if entry.bucket == "line" then
					weight = weight + 2
				end
				if weight > 0 then
					candidates[#candidates + 1] = {
						id = entry.id,
						price = entry.price,
						weight = weight,
					}
				end
			end
		end
		local picked = lPickWeighted(candidates, context .. "_" .. mode .. "_" .. slot)
		if not picked then
			break
		end
		units[#units + 1] = picked.id
		spent = spent + picked.price
	end

	if #units < recipe.size_min then
		return false
	end

	-- If composition reached T4 without MercCaptain and role allows it, try swap/add.
	if lMaxTierInList(units) >= 4 and JAZZ_LegionUnitAllowedForRole("JAZZ_Legion_LeaderT4_MercenaryCaptain", role) then
		local has_merc = false
		for _, id in ipairs(units) do
			if id == "JAZZ_Legion_LeaderT4_MercenaryCaptain" then
				has_merc = true
				break
			end
		end
		if not has_merc then
			local price = JAZZ_GetLegionUnitPrice("JAZZ_Legion_LeaderT4_MercenaryCaptain") or 0
			if spent + price <= budget_money and (not budget_manpower or #units < budget_manpower) then
				units[#units + 1] = "JAZZ_Legion_LeaderT4_MercenaryCaptain"
				spent = spent + price
			end
		end
	end

	return {
		units = units,
		money_cost = spent,
		manpower_cost = #units,
		mode = mode,
		role = role,
	}
end

--- Generate a combat/logistics composition for a strategic role.
-- @param role string recipe key (major uses "retribution")
-- @param budget_money number
-- @param budget_manpower number|nil nil = unlimited people
-- @param mode "auto"|"full"|"poor"
-- @param rand_context string InteractionRand suffix
-- @param growth_progress number|nil 0..1000 STRATEGY-016 size curve
-- @param preferred_archetype string|nil unused (STRATEGY-024 mixed per-unit; kept for call-site compat)
function JAZZ_GenerateLegionSquadComposition(role, budget_money, budget_manpower, mode, rand_context, growth_progress, preferred_archetype)
	local recipe_role = role == "major" and "retribution" or role
	local recipe = JAZZ_ResolveLegionRoleRecipe and JAZZ_ResolveLegionRoleRecipe(recipe_role, growth_progress)
		or JAZZ_GetLegionRoleRecipe(recipe_role)
	if not recipe then
		return false
	end
	budget_money = math.floor(tonumber(budget_money) or 0)
	if budget_money <= 0 then
		return false
	end
	if budget_manpower ~= nil then
		budget_manpower = math.floor(tonumber(budget_manpower) or 0)
	end
	mode = mode or "auto"
	rand_context = tostring(rand_context or recipe_role)

	local function lBuild(build_mode)
		if recipe_role == "support" then
			return lTryBuildSupport(recipe, budget_money, budget_manpower, build_mode, rand_context, preferred_archetype)
		end
		return lTryBuild(recipe_role, recipe, budget_money, budget_manpower, build_mode, rand_context)
	end

	if mode == "full" or mode == "poor" then
		return lBuild(mode)
	end

	local full = lBuild("full")
	if full then
		return full
	end
	return lBuild("poor")
end

function JAZZ_LegionRoleUsesCompositionGenerator(role)
	return role == "garrison"
		or role == "patrol"
		or role == "recon"
		or role == "qrf"
		or role == "reinforce"
		or role == "support"
		or role == "major"
		or role == "tax"
		or role == "shipment"
		or role == "supply"
		or role == "recruiter"
		or role == "manpower"
end

function JAZZ_LegionRoleIsLogisticsEscort(role)
	return role == "tax"
		or role == "shipment"
		or role == "supply"
		or role == "recruiter"
		or role == "manpower"
end

--- Build a list of UnitData template IDs to add onto an existing squad.
-- existing_template_ids: current living unit class/template ids (for soft-cap accounting).
-- preferred_archetype: unused (mixed support; kept for call-site compat).
-- Returns { units = {...}, money_cost, manpower_cost } or false if nothing affordable.
function JAZZ_GenerateLegionSquadTopUp(existing_template_ids, role, budget_money, budget_manpower, rand_context, growth_progress, preferred_archetype)
	local recipe_role = role == "major" and "retribution" or role
	local recipe = JAZZ_ResolveLegionRoleRecipe and JAZZ_ResolveLegionRoleRecipe(recipe_role, growth_progress)
		or JAZZ_GetLegionRoleRecipe(recipe_role)
	if not recipe then
		return false
	end
	existing_template_ids = existing_template_ids or {}
	local current = {}
	for _, id in ipairs(existing_template_ids) do
		current[#current + 1] = id
	end
	budget_money = math.floor(tonumber(budget_money) or 0)
	if budget_manpower ~= nil then
		budget_manpower = math.floor(tonumber(budget_manpower) or 0)
	end
	local target = recipe.size_max
	if budget_manpower then
		target = Min(target, #current + budget_manpower)
	end
	if #current >= target or budget_money <= 0 then
		return false
	end

	-- Support top-up: mixed specialists + escort; no mono-archetype lock.
	if recipe_role == "support" then
		local need = target - #current
		if need <= 0 then
			return false
		end
		local eligible = lEligibleUnits("support")
		local added = {}
		local spent = 0
		local slot = 0
		local specialist_set = {}
		for _, id in ipairs(lCollectSupportSpecialists()) do
			specialist_set[id] = true
		end
		while #added < need do
			slot = slot + 1
			local candidates = {}
			for _, entry in ipairs(eligible) do
				if entry.bucket ~= "officer"
					and entry.bucket ~= "medic"
					and spent + entry.price <= budget_money
					and (not budget_manpower or (#added + 1) <= budget_manpower)
					and not lWouldBreakSoftCap(current, entry.id, target, "support")
				then
					local weight = lTierWeight(entry, "specialty", "full")
					if specialist_set[entry.id] then
						weight = weight + 4
					elseif entry.bucket == "line" then
						weight = weight + 2
					end
					if weight > 0 then
						candidates[#candidates + 1] = {
							id = entry.id,
							price = entry.price,
							weight = weight,
						}
					end
				end
			end
			local picked = lPickWeighted(candidates, tostring(rand_context or "support") .. "_topup_" .. slot)
			if not picked then
				break
			end
			current[#current + 1] = picked.id
			added[#added + 1] = picked.id
			spent = spent + picked.price
		end
		if #added == 0 then
			return false
		end
		return {
			units = added,
			money_cost = spent,
			manpower_cost = #added,
			role = recipe_role,
			target_size = target,
			support_archetype = "mixed",
		}
	end

	local eligible = lEligibleUnits(recipe_role)
	local added = {}
	local spent = 0
	local slot = 0
	local medic_id = JAZZ_GetLegionMedicUnitId and JAZZ_GetLegionMedicUnitId() or "JAZZ_Legion_FrontT1_Bonemaker"
	local medic_need = (JAZZ_GetLegionMaxMedics and JAZZ_GetLegionMaxMedics(target) or 0) - lCountMedics(current)
	while medic_need > 0 and #current < target do
		local price = JAZZ_GetLegionUnitPrice(medic_id)
		if not price
			or spent + price > budget_money
			or (budget_manpower and (#added + 1) > budget_manpower)
			or not JAZZ_LegionUnitAllowedForRole(medic_id, recipe_role)
		then
			break
		end
		current[#current + 1] = medic_id
		added[#added + 1] = medic_id
		spent = spent + price
		medic_need = medic_need - 1
	end
	while #current < target do
		slot = slot + 1
		local candidates = {}
		for _, entry in ipairs(eligible) do
			if entry.bucket ~= "officer"
				and entry.bucket ~= "medic"
				and spent + entry.price <= budget_money
				and (not budget_manpower or (#added + 1) <= budget_manpower)
				and not lWouldBreakSoftCap(current, entry.id, target, recipe_role)
			then
				local weight = lTierWeight(entry, recipe.tier_bias, "full")
				if entry.bucket == "line" then
					weight = weight + 2
				end
				if weight > 0 then
					candidates[#candidates + 1] = {
						id = entry.id,
						price = entry.price,
						weight = weight,
					}
				end
			end
		end
		local picked = lPickWeighted(candidates, tostring(rand_context or recipe_role) .. "_topup_" .. slot)
		if not picked then
			break
		end
		current[#current + 1] = picked.id
		added[#added + 1] = picked.id
		spent = spent + picked.price
	end
	if #added == 0 then
		return false
	end
	return {
		units = added,
		money_cost = spent,
		manpower_cost = #added,
		role = recipe_role,
		target_size = target,
	}
end

function JAZZ_GetLegionRoleOptimalSize(role, growth_progress)
	local recipe = JAZZ_ResolveLegionRoleRecipe and JAZZ_ResolveLegionRoleRecipe(role == "major" and "retribution" or role, growth_progress)
		or JAZZ_GetLegionRoleRecipe(role == "major" and "retribution" or role)
	return recipe and recipe.size_max or false
end

function JAZZ_GetLegionRoleMinSize(role, growth_progress)
	local recipe = JAZZ_ResolveLegionRoleRecipe and JAZZ_ResolveLegionRoleRecipe(role == "major" and "retribution" or role, growth_progress)
		or JAZZ_GetLegionRoleRecipe(role == "major" and "retribution" or role)
	return recipe and recipe.size_min or false
end
