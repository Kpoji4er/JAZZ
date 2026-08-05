-- AME living market: listing, 14-day (2-week) tick, specialist soft-guarantee (JAZZ-UNITS-005).

GameVar("gv_JAZZ_AME_Market", function()
	return {
		initialized = false,
		next_tick_day = 0,
		-- slots[id] = { reason = false|"JoinedLegion"|"Killed"|"HiredElsewhere" }
		slots = {},
	}
end)

local AME_TARGET_AVAILABLE = 15
local AME_TICK_DAYS = 14
local AME_SPECIALIST_ROLES = { Medic = true, Instructor = true, Sniper = true, Sapper = true, Mechanic = true }

local function lAmeIds()
	local ids = {}
	for i = 1, 60 do
		ids[#ids + 1] = string.format("JAZZ_AME_%02d", i)
	end
	return ids
end

local function lCampaignDay()
	if not Game or not Game.CampaignTime or not Game.CampaignTimeStart then
		return 0
	end
	return (Game.CampaignTime - Game.CampaignTimeStart) / const.Scale.day
end

local function lRoll(seed_parts, lo, hi)
	local h = xxhash(table.unpack(seed_parts))
	return BraidRandom(h, lo, hi)
end

local function lGetUd(id)
	return gv_UnitData and gv_UnitData[id]
end

local function lCountAvailable()
	local n = 0
	for _, id in ipairs(lAmeIds()) do
		local ud = lGetUd(id)
		if ud and ud.HireStatus == "Available" then
			n = n + 1
		end
	end
	return n
end

local function lSpecialistAvailableOrPending()
	for _, id in ipairs(lAmeIds()) do
		local ud = lGetUd(id)
		if ud and AME_SPECIALIST_ROLES[ud.AMERole or ""] then
			if ud.HireStatus == "Available" then
				return true
			end
		end
	end
	return false
end

local function lSetHireStatus(ud, status)
	if not ud then
		return
	end
	ud.HireStatus = status
	ObjModified(ud)
end

function JAZZ_AME_InitMarket(force)
	local market = gv_JAZZ_AME_Market
	if not market then
		return
	end
	if market.initialized and not force then
		return
	end
	market.slots = market.slots or {}
	local gameId = Game and Game.id or 0
	-- Reset all AME to NotMet, then open a starting window.
	local pool = {}
	for _, id in ipairs(lAmeIds()) do
		local ud = lGetUd(id)
		if ud then
			market.slots[id] = market.slots[id] or { reason = false }
			if ud.HireStatus ~= "Hired" then
				lSetHireStatus(ud, "NotMet")
			end
			pool[#pool + 1] = id
		end
	end
	-- Deterministic shuffle by game id
	table.sort(pool, function(a, b)
		return lRoll({ gameId, a, "init_order" }, 0, 1000000) < lRoll({ gameId, b, "init_order" }, 0, 1000000)
	end)
	-- Prefer mix: take first TARGET from sorted pool but ensure ≥1 specialist.
	local opened = 0
	local hasSpec = false
	for _, id in ipairs(pool) do
		if opened >= AME_TARGET_AVAILABLE then
			break
		end
		local ud = lGetUd(id)
		if ud and ud.HireStatus ~= "Hired" then
			local isSpec = AME_SPECIALIST_ROLES[ud.AMERole or ""]
			if opened < AME_TARGET_AVAILABLE - 1 or hasSpec or isSpec then
				lSetHireStatus(ud, "Available")
				market.slots[id].reason = false
				opened = opened + 1
				hasSpec = hasSpec or isSpec
			end
		end
	end
	if not hasSpec then
		for _, id in ipairs(pool) do
			local ud = lGetUd(id)
			if ud and AME_SPECIALIST_ROLES[ud.AMERole or ""] and ud.HireStatus ~= "Hired" then
				lSetHireStatus(ud, "Available")
				market.slots[id].reason = false
				break
			end
		end
	end
	market.initialized = true
	market.next_tick_day = lCampaignDay() + AME_TICK_DAYS
	ObjModified("pda browser tabs")
end

local function lTerminalize(id, reason)
	local market = gv_JAZZ_AME_Market
	local ud = lGetUd(id)
	if not ud or ud.HireStatus == "Hired" then
		return
	end
	market.slots[id] = market.slots[id] or {}
	market.slots[id].reason = reason
	if reason == "Killed" then
		lSetHireStatus(ud, "Dead")
	else
		-- JoinedLegion / HiredElsewhere → MIA (visible disabled)
		lSetHireStatus(ud, "MIA")
	end
end

local function lOpenSlot(id)
	local ud = lGetUd(id)
	local market = gv_JAZZ_AME_Market
	if not ud or ud.HireStatus == "Hired" or ud.HireStatus == "Dead" then
		return false
	end
	if ud.HireStatus == "MIA" and market.slots[id] and market.slots[id].reason then
		return false -- permanent terminal
	end
	lSetHireStatus(ud, "Available")
	market.slots[id] = market.slots[id] or {}
	market.slots[id].reason = false
	return true
end

function JAZZ_AME_MarketTick()
	local market = gv_JAZZ_AME_Market
	if not market or not market.initialized then
		JAZZ_AME_InitMarket()
		return
	end
	local day = lCampaignDay()
	if day < (market.next_tick_day or 0) then
		return
	end
	local gameId = Game and Game.id or 0
	local tick = market.next_tick_day or day
	-- Departures from Available
	for _, id in ipairs(lAmeIds()) do
		local ud = lGetUd(id)
		if ud and ud.HireStatus == "Available" then
			local roll = lRoll({ gameId, id, tick, "leave" }, 1, 100)
			if roll <= 18 then
				if roll <= 6 then
					lTerminalize(id, "JoinedLegion")
				elseif roll <= 10 then
					lTerminalize(id, "Killed")
				else
					lTerminalize(id, "HiredElsewhere")
				end
			end
		end
	end
	-- Refill to target
	local need = AME_TARGET_AVAILABLE - lCountAvailable()
	if need > 0 then
		local candidates = {}
		for _, id in ipairs(lAmeIds()) do
			local ud = lGetUd(id)
			if ud and ud.HireStatus == "NotMet" then
				candidates[#candidates + 1] = id
			end
		end
		table.sort(candidates, function(a, b)
			return lRoll({ gameId, a, tick, "enter" }, 0, 1000000) < lRoll({ gameId, b, tick, "enter" }, 0, 1000000)
		end)
		for i = 1, need do
			if candidates[i] then
				lOpenSlot(candidates[i])
			end
		end
	end
	-- Specialist soft-guarantee
	if not lSpecialistAvailableOrPending() then
		for _, id in ipairs(lAmeIds()) do
			local ud = lGetUd(id)
			if ud and AME_SPECIALIST_ROLES[ud.AMERole or ""] then
				if ud.HireStatus == "NotMet" or (ud.HireStatus == "MIA" and not (market.slots[id] and market.slots[id].reason == "Killed")) then
					if ud.HireStatus ~= "Hired" and ud.HireStatus ~= "Dead" then
						lOpenSlot(id)
						break
					end
				end
			end
		end
	end
	market.next_tick_day = day + AME_TICK_DAYS
	ObjModified("pda browser tabs")
end

function OnMsg.NewGame()
	DelayedCall(0, function()
		JAZZ_AME_InitMarket(true)
	end)
end

function OnMsg.LoadGame()
	DelayedCall(0, function()
		if not gv_JAZZ_AME_Market or not gv_JAZZ_AME_Market.initialized then
			JAZZ_AME_InitMarket(true)
		end
	end)
end

function OnMsg.SatelliteTick()
	if gv_JAZZ_AME_Market and gv_JAZZ_AME_Market.initialized then
		JAZZ_AME_MarketTick()
	end
end

function OnMsg.MercHireStatusChanged(unitData, oldStatus, newStatus)
	if not unitData or unitData.Affiliation ~= "AME" then
		return
	end
	local market = gv_JAZZ_AME_Market
	if not market or not market.slots then
		return
	end
	local id = unitData.session_id
	market.slots[id] = market.slots[id] or {}
	if newStatus == "Hired" then
		market.slots[id].reason = false
	end
end
