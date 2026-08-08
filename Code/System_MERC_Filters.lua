-- MERC hire browser filters / roster tables (JAZZ-UI-MERC-001).
-- Top-level globals OK at file load.

MERCScreenFilters = false
CurrentMERCFilter = 1

JAZZ_MERC_SHELF_IDS = {
	"Jazz_Flo",
	"Jazz_Cougar",
	"Jazz_Madman",
	"Jazz_Blade",
	"Jazz_Conrad",
	"Jazz_Dynamo",
	"Jazz_Gaston",
	"Jazz_Nervous",
	"Jazz_Ricochet",
	"Jazz_Cord",
	"Jazz_Hobbit",
	"Jazz_Horg",
	"Jazz_Meat",
	"Jazz_Shank",
}

JAZZ_MERC_WORLD_IDS = {
	"Jazz_Biff",
	"Larry",
	"Larry_Clean",
	"Smiley",
}

JAZZ_MERC_ALL_IDS = {}
do
	local all = JAZZ_MERC_ALL_IDS
	for _, id in ipairs(JAZZ_MERC_SHELF_IDS) do
		all[#all + 1] = id
	end
	for _, id in ipairs(JAZZ_MERC_WORLD_IDS) do
		all[#all + 1] = id
	end
end

local SHELF_SET = {}
for _, id in ipairs(JAZZ_MERC_SHELF_IDS) do
	SHELF_SET[id] = true
end

local WORLD_SET = {}
for _, id in ipairs(JAZZ_MERC_WORLD_IDS) do
	WORLD_SET[id] = true
end

local ALL_SET = {}
for _, id in ipairs(JAZZ_MERC_ALL_IDS) do
	ALL_SET[id] = true
end

function JAZZ_MERC_IsShelfId(id)
	return id and SHELF_SET[id] or false
end

function JAZZ_MERC_IsWorldId(id)
	return id and WORLD_SET[id] or false
end

function JAZZ_MERC_IsRosterId(id)
	return id and ALL_SET[id] or false
end

local function lIsWorldMet(id)
	if not id or not WORLD_SET[id] then
		return true
	end
	local account = rawget(_G, "gv_JAZZ_MERC_Account")
	local met = account and account.met
	return met and met[id] and true or false
end

local function lIsListedMERC(merc)
	if not merc or merc.Affiliation ~= "MERC" then
		return false
	end
	local id = merc.session_id
	-- World-gated: NotMet / unmet custom flag → hidden until MarkMet.
	if id and WORLD_SET[id] then
		if merc.HireStatus == "NotMet" or not lIsWorldMet(id) then
			return false
		end
	end
	local hs = merc.HireStatus
	return hs == "Available" or hs == "Hired" or hs == "Retired" or hs == "Dead" or hs == "MIA"
end

function IsListedMERCMerc(merc)
	return lIsListedMERC(merc)
end

local tformat = rawget(_G, "TFormat")
if type(tformat) == "table" then
	function tformat.MERCPlayerMercCount()
		local count = 0
		for _, merc in pairs(gv_UnitData or empty_table) do
			if merc.Affiliation == "MERC" and merc.HireStatus == "Hired" then
				count = count + 1
			end
		end
		return count
	end
end

function GetMERCScreenFilters()
	if MERCScreenFilters then
		return MERCScreenFilters
	end
	MERCScreenFilters = {
		{
			name = T(890000000009903, "All"),
			nameString = "all",
			urlSlug = "All",
			func = function(item)
				return lIsListedMERC(item)
			end,
			id = 1,
		},
		{
			name = T(890000000009904, "Available"),
			nameString = "available",
			urlSlug = "Available",
			func = function(item)
				return lIsListedMERC(item) and item.HireStatus == "Available"
			end,
			id = 2,
		},
		{
			name = T(890000000009905, "My Team [<MERCPlayerMercCount()>]"),
			urlSlug = "My%20Team",
			nameString = "hired",
			func = function(item)
				return item.Affiliation == "MERC" and item.HireStatus == "Hired"
			end,
			id = 3,
			hire = true,
		},
	}
	return MERCScreenFilters
end

function GetFilteredMERCMercs(filter_index)
	local filters = GetMERCScreenFilters()
	local filter = filters[filter_index] and filters[filter_index].func
	local filteredItems = {}
	if not filter then
		return filteredItems
	end
	local forEach = rawget(_G, "ForEachMerc")
	if type(forEach) == "function" then
		forEach(function(mId)
			local data = gv_UnitData[mId]
			if data and filter(data) then
				filteredItems[#filteredItems + 1] = data
			end
		end)
	else
		for _, id in ipairs(JAZZ_MERC_ALL_IDS) do
			local data = gv_UnitData and gv_UnitData[id]
			if data and filter(data) then
				filteredItems[#filteredItems + 1] = data
			end
		end
	end
	local getPrice = rawget(_G, "GetMercPrice")
	table.sort(filteredItems, function(a, b)
		local priceA = (type(getPrice) == "function" and getPrice(a, 7, true)) or 0
		local priceB = (type(getPrice) == "function" and getPrice(b, 7, true)) or 0
		if priceA == priceB then
			return (a.session_id or "") < (b.session_id or "")
		end
		return priceA < priceB
	end)
	return filteredItems
end
