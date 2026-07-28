-- Runtime composition generator for Legion Global AI (roadmap 6c / JAZZ-STRATEGY-008).
-- Builds JAZZ_Legion_* unit lists from role recipes, unit prices, officer density, soft caps.

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

local function lWouldBreakSoftCap(units, candidate, target_size)
	local bucket = JAZZ_GetLegionUnitClassBucket(candidate)
	if bucket == "line" or bucket == "officer" then
		return false
	end
	local caps = lSoftCaps(math.max(target_size, #units + 1))
	local cap = caps[bucket]
	if not cap then
		return false
	end
	return lCountBucket(units, bucket) >= cap
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

	local slot = 0
	while #units < target do
		slot = slot + 1
		local candidates = {}
		for _, entry in ipairs(eligible) do
			if entry.bucket ~= "officer"
				and spent + entry.price <= budget_money
				and not lWouldBreakSoftCap(units, entry.id, target)
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

--- Generate a combat composition for a strategic role.
-- @param role string recipe key (major uses "retribution")
-- @param budget_money number
-- @param budget_manpower number|nil nil = unlimited people
-- @param mode "auto"|"full"|"poor"
-- @param rand_context string InteractionRand suffix
function JAZZ_GenerateLegionSquadComposition(role, budget_money, budget_manpower, mode, rand_context)
	local recipe_role = role == "major" and "retribution" or role
	local recipe = JAZZ_GetLegionRoleRecipe(recipe_role)
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

	if mode == "full" or mode == "poor" then
		return lTryBuild(recipe_role, recipe, budget_money, budget_manpower, mode, rand_context)
	end

	local full = lTryBuild(recipe_role, recipe, budget_money, budget_manpower, "full", rand_context)
	if full then
		return full
	end
	return lTryBuild(recipe_role, recipe, budget_money, budget_manpower, "poor", rand_context)
end

function JAZZ_LegionRoleUsesCompositionGenerator(role)
	return role == "garrison"
		or role == "patrol"
		or role == "recon"
		or role == "qrf"
		or role == "reinforce"
		or role == "major"
end

--- Build a list of UnitData template IDs to add onto an existing squad.
-- existing_template_ids: current living unit class/template ids (for soft-cap accounting).
-- Returns { units = {...}, money_cost, manpower_cost } or false if nothing affordable.
function JAZZ_GenerateLegionSquadTopUp(existing_template_ids, role, budget_money, budget_manpower, rand_context)
	local recipe_role = role == "major" and "retribution" or role
	local recipe = JAZZ_GetLegionRoleRecipe(recipe_role)
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

	local eligible = lEligibleUnits(recipe_role)
	local added = {}
	local spent = 0
	local slot = 0
	while #current < target do
		slot = slot + 1
		local candidates = {}
		for _, entry in ipairs(eligible) do
			if entry.bucket ~= "officer"
				and spent + entry.price <= budget_money
				and (not budget_manpower or (#added + 1) <= budget_manpower)
				and not lWouldBreakSoftCap(current, entry.id, target)
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

function JAZZ_GetLegionRoleOptimalSize(role)
	local recipe = JAZZ_GetLegionRoleRecipe(role == "major" and "retribution" or role)
	return recipe and recipe.size_max or false
end

function JAZZ_GetLegionRoleMinSize(role)
	local recipe = JAZZ_GetLegionRoleRecipe(role == "major" and "retribution" or role)
	return recipe and recipe.size_min or false
end
