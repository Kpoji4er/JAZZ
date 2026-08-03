-- AME hire browser category filters (JAZZ-UNITS-005).
-- Top-level globals OK at file load.

AMEScreenFilters = false
CurrentAMEFilter = 1

local function lIsListedAME(merc)
	if not merc or merc.Affiliation ~= "AME" then
		return false
	end
	-- NotMet = NotListed (hidden). Dead/MIA = terminal visible. Available/Hired/Retired = listed.
	local hs = merc.HireStatus
	return hs == "Available" or hs == "Hired" or hs == "Retired" or hs == "Dead" or hs == "MIA"
end

function IsListedAMEMerc(merc)
	return lIsListedAME(merc)
end

function GetAMEScreenFilters()
	if AMEScreenFilters then
		return AMEScreenFilters
	end
	AMEScreenFilters = {
		{
			name = T(890000000005001, "Irregulars"),
			nameString = "irregulars",
			urlSlug = "Irregulars",
			func = function(item)
				return lIsListedAME(item) and item.AMECategory == "Irregulars"
			end,
			id = 1,
		},
		{
			name = T(890000000005003, "Fighters"),
			nameString = "fighters",
			urlSlug = "Fighters",
			func = function(item)
				return lIsListedAME(item) and item.AMECategory == "Fighters"
			end,
			id = 2,
		},
		{
			name = T(890000000005005, "Hardened"),
			nameString = "hardened",
			urlSlug = "Hardened",
			func = function(item)
				return lIsListedAME(item) and item.AMECategory == "Hardened"
			end,
			id = 3,
		},
		{
			name = T(890000000005007, "Specialists"),
			nameString = "specialists",
			urlSlug = "Specialists",
			func = function(item)
				return lIsListedAME(item) and item.AMECategory == "Specialists"
			end,
			id = 4,
		},
		{
			name = T(890000000005009, "All"),
			nameString = "all",
			urlSlug = "All",
			func = function(item)
				return lIsListedAME(item)
			end,
			id = 5,
		},
		{
			name = T(890000000005011, "My Team [<PlayerMercCount()>]"),
			urlSlug = "My%20Team",
			nameString = "hired",
			func = function(item)
				return item.HireStatus == "Hired"
			end,
			id = 6,
			hire = true,
		},
	}
	return AMEScreenFilters
end

function GetFilteredAMEMercs(filter_index)
	local filters = GetAMEScreenFilters()
	local filter = filters[filter_index] and filters[filter_index].func
	local filteredItems = {}
	if not filter then
		return filteredItems
	end
	ForEachMerc(function(mId)
		local data = gv_UnitData[mId]
		if data and filter(data) then
			filteredItems[#filteredItems + 1] = data
		end
	end)
	table.sort(filteredItems, function(a, b)
		local priceA = GetMercPrice(a, 7, true) or 0
		local priceB = GetMercPrice(b, 7, true) or 0
		if priceA == priceB then
			return (a.session_id or "") < (b.session_id or "")
		end
		return priceA < priceB
	end)
	return filteredItems
end
