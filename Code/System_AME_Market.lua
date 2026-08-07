-- AME living market: listing, 14-day (2-week) tick, specialist soft-guarantee (JAZZ-UNITS-005).

GameVar("gv_JAZZ_AME_Market", function()
	return {
		initialized = false,
		next_tick_day = 0,
		-- slots[id] = { reason = false|"JoinedLegion"|"Killed"|"HiredElsewhere" }
		slots = {},
		-- JAZZ-UI-AME-001 mail / tab lock
		welcome_sent = false,
		welcome_read = false,
		listing_snapshot = false,
		specialist_missing_ticks = {},
	}
end)

local AME_TARGET_AVAILABLE = 15
local AME_TICK_DAYS = 14
local AME_SPECIALIST_ROLES = { Medic = true, Instructor = true, Sniper = true, Sapper = true, Mechanic = true }
local AME_SOFT_GUARANTEE_ROLES = { "Medic", "Instructor", "Sniper" }
local AME_DEPARTURE_REASON_TEXT = {
	JoinedLegion = T(890000000006990, "Joined the Legion"),
	Killed = T(890000000006991, "<style PDAMercPrice_Dead>Killed in action</style>"),
	HiredElsewhere = T(890000000006992, "Signed with another employer"),
}

local AME_IDS = {}
for i = 1, 60 do
	AME_IDS[i] = string.format("JAZZ_AME_%02d", i)
end

local function lAmeIds()
	return AME_IDS
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

function JAZZ_AME_GetDepartureReasonText(ud)
	local market = gv_JAZZ_AME_Market
	local id = ud and ud.session_id
	local slot = id and market and market.slots and market.slots[id]
	return slot and AME_DEPARTURE_REASON_TEXT[slot.reason] or false
end

local function lCountAvailable()
	local n = 0
	for _, id in ipairs(AME_IDS) do
		local ud = lGetUd(id)
		if ud and ud.HireStatus == "Available" then
			n = n + 1
		end
	end
	return n
end

local function lRoleAvailable(role)
	for _, id in ipairs(AME_IDS) do
		local ud = lGetUd(id)
		if ud and ud.AMERole == role and ud.HireStatus == "Available" then
			return true
		end
	end
	return false
end

local function lInitializeSpecialistTracking(market)
	market.specialist_missing_ticks = market.specialist_missing_ticks or {}
	for _, role in ipairs(AME_SOFT_GUARANTEE_ROLES) do
		if market.specialist_missing_ticks[role] == nil then
			market.specialist_missing_ticks[role] = lRoleAvailable(role) and 0 or 1
		end
	end
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
	for _, id in ipairs(AME_IDS) do
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
	market.specialist_missing_ticks = {}
	lInitializeSpecialistTracking(market)
	market.initialized = true
	market.next_tick_day = lCampaignDay() + AME_TICK_DAYS
	ObjModified("pda browser tabs")
	if rawget(_G, "JAZZ_AME_SendWelcomeMail") then
		JAZZ_AME_SendWelcomeMail()
	end
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

local function lApplyDepartures(gameId, tick)
	for _, id in ipairs(AME_IDS) do
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
end

local function lRefillAvailable(gameId, tick)
	local need = AME_TARGET_AVAILABLE - lCountAvailable()
	if need <= 0 then
		return
	end
	local candidates = {}
	for _, id in ipairs(AME_IDS) do
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

local function lAdvanceSpecialistTracking(market)
	lInitializeSpecialistTracking(market)
	local due = {}
	for _, role in ipairs(AME_SOFT_GUARANTEE_ROLES) do
		if lRoleAvailable(role) then
			market.specialist_missing_ticks[role] = 0
		else
			local missing = (market.specialist_missing_ticks[role] or 0) + 1
			market.specialist_missing_ticks[role] = missing
			if missing >= 2 then
				due[#due + 1] = role
			end
		end
	end
	return due
end

local function lGuaranteedCandidates(market, role)
	local candidates = {}
	for _, id in ipairs(AME_IDS) do
		local ud = lGetUd(id)
		local slot = market.slots[id]
		local temporaryAway = ud and ud.HireStatus == "MIA" and not (slot and slot.reason)
		if ud and ud.AMERole == role and (ud.HireStatus == "NotMet" or temporaryAway) then
			candidates[#candidates + 1] = id
		end
	end
	return candidates
end

local function lMakeRoomForGuaranteedRoles(gameId, tick, due)
	local excess = lCountAvailable() + #due - AME_TARGET_AVAILABLE
	if excess <= 0 then
		return
	end
	local candidates = {}
	for _, id in ipairs(AME_IDS) do
		local ud = lGetUd(id)
		if ud and ud.HireStatus == "Available" then
			local protected = table.find(due, ud.AMERole)
			if not protected then
				candidates[#candidates + 1] = id
			end
		end
	end
	table.sort(candidates, function(a, b)
		return lRoll({ gameId, a, tick, "guarantee_room" }, 0, 1000000) < lRoll({ gameId, b, tick, "guarantee_room" }, 0, 1000000)
	end)
	for i = 1, excess do
		local id = candidates[i]
		if id then
			lTerminalize(id, "HiredElsewhere")
		end
	end
end

local function lOpenGuaranteedRoles(market, gameId, tick, due)
	for _, role in ipairs(due) do
		if not lRoleAvailable(role) then
			local candidates = lGuaranteedCandidates(market, role)
			table.sort(candidates, function(a, b)
				return lRoll({ gameId, a, tick, role, "guarantee_enter" }, 0, 1000000) < lRoll({ gameId, b, tick, role, "guarantee_enter" }, 0, 1000000)
			end)
			if candidates[1] and lOpenSlot(candidates[1]) then
				market.specialist_missing_ticks[role] = 0
			end
		end
	end
end

local function lResetPresentSpecialistTracking(market)
	for _, role in ipairs(AME_SOFT_GUARANTEE_ROLES) do
		if lRoleAvailable(role) then
			market.specialist_missing_ticks[role] = 0
		end
	end
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
	lApplyDepartures(gameId, tick)
	local due = lAdvanceSpecialistTracking(market)
	due = table.ifilter(due, function(_, role)
		return #lGuaranteedCandidates(market, role) > 0
	end)
	lMakeRoomForGuaranteedRoles(gameId, tick, due)
	lOpenGuaranteedRoles(market, gameId, tick, due)
	lRefillAvailable(gameId, tick)
	lResetPresentSpecialistTracking(market)
	market.next_tick_day = day + AME_TICK_DAYS
	ObjModified("pda browser tabs")
	if rawget(_G, "JAZZ_AME_SendListingUpdateMail") then
		JAZZ_AME_SendListingUpdateMail()
	end
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
		elseif rawget(_G, "JAZZ_AME_SendWelcomeMail") then
			-- Existing AME save: still send welcome once if never mailed.
			JAZZ_AME_SendWelcomeMail()
		end
		if rawget(_G, "JAZZ_AME_ApplyTabLock") then
			JAZZ_AME_ApplyTabLock()
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
