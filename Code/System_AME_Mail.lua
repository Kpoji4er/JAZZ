-- AME mail + PDA tab lock until welcome read (JAZZ-UI-AME-001).
-- Extends gv_JAZZ_AME_Market (defined in System_AME_Market.lua).

g_JAZZ_AME_MarkEmailWrapped = rawget(_G, "g_JAZZ_AME_MarkEmailWrapped") or false
g_JAZZ_AME_MarkEmailBase = rawget(_G, "g_JAZZ_AME_MarkEmailBase") or false

local AME_WELCOME_ID = "AME_Welcome"
local AME_LISTING_ID = "AME_ListingUpdate"

local AME_CAT_LABEL = {
	Irregulars = T(890000000006900, "Irregulars"),
	Fighters = T(890000000006901, "Fighters"),
	Hardened = T(890000000006902, "Hardened"),
	Specialists = T(890000000006903, "Specialists"),
}

-- Ad pitches: role first, then stats. Sales desk tone, not a stat dump.
local AME_ROLE_PITCH = {
	Medic = T(890000000006960, "keeps your people on their feet"),
	Instructor = T(890000000006961, "turns green recruits into fighters"),
	Sniper = T(890000000006962, "puts rounds where it hurts from far out"),
	Sapper = T(890000000006963, "handles bombs, traps, and loud solutions"),
	Mechanic = T(890000000006964, "fixes guns and gear when the bush eats them"),
	Rifle = T(890000000006965, "solid rifle work, no drama"),
	Autorifleman = T(890000000006966, "lays down automatic fire when you need volume"),
	Machinegunner = T(890000000006967, "anchors the line with a heavy gun"),
	Grenadier = T(890000000006968, "throws trouble over walls and into rooms"),
}

local AME_STAT_PITCH = {
	{ key = "Marksmanship", min = 58, text = T(890000000006970, "a sharp shooter") },
	{ key = "Medical", min = 40, text = T(890000000006971, "knows how to patch wounds") },
	{ key = "Mechanical", min = 40, text = T(890000000006972, "handy with tools and weapons") },
	{ key = "Explosives", min = 35, text = T(890000000006973, "comfortable around explosives") },
	{ key = "Strength", min = 70, text = T(890000000006974, "built like a truck") },
	{ key = "Health", min = 80, text = T(890000000006975, "tough as nails") },
	{ key = "Leadership", min = 45, text = T(890000000006976, "people listen when they speak") },
	{ key = "Wisdom", min = 65, text = T(890000000006977, "high growth potential") },
	{ key = "Agility", min = 68, text = T(890000000006978, "moves fast under fire") },
	{ key = "Dexterity", min = 68, text = T(890000000006979, "steady hands") },
}

local AME_CAT_PITCH = {
	Irregulars = T(890000000006980, "cheap entry — room to grow on your payroll"),
	Fighters = T(890000000006981, "ready for real jobs, not just guard duty"),
	Hardened = T(890000000006982, "already blooded — less babysitting"),
	Specialists = T(890000000006983, "scarce skill — worth the weekly"),
}

local function lMarket()
	return gv_JAZZ_AME_Market
end

local function lAmeIds()
	local ids = {}
	for i = 1, 60 do
		ids[#ids + 1] = string.format("JAZZ_AME_%02d", i)
	end
	return ids
end

local function lNickOrName(ud)
	if not ud then
		return false
	end
	if ud.Nick and ud.Nick ~= "" then
		return ud.Nick
	end
	return ud.Name
end

local function lCategoryLabel(ud)
	local cat = ud and ud.AMECategory
	return (cat and AME_CAT_LABEL[cat]) or Untranslated(tostring(cat or "?"))
end

local function lAsStr(val)
	if val == nil or val == false then
		return "?"
	end
	if type(val) == "string" then
		return val
	end
	if type(_InternalTranslate) == "function" then
		local ok, s = pcall(_InternalTranslate, val)
		if ok and type(s) == "string" and s ~= "" then
			return s
		end
	end
	return tostring(val)
end

local function lStat(ud, key)
	return tonumber(ud and ud[key]) or 0
end

--- Pick 1–2 sales pitches for a merc (role / stats / category fallback).
function JAZZ_AME_PickMercPitches(ud)
	local pitches = {}
	local role = ud and ud.AMERole
	if role and AME_ROLE_PITCH[role] then
		pitches[#pitches + 1] = AME_ROLE_PITCH[role]
	end
	local scored = {}
	for _, row in ipairs(AME_STAT_PITCH) do
		local v = lStat(ud, row.key)
		if v >= row.min then
			scored[#scored + 1] = { text = row.text, key = row.key, score = v - row.min }
		end
	end
	table.sort(scored, function(a, b)
		return a.score > b.score
	end)
	local roleCovers = {
		Medic = "Medical",
		Mechanic = "Mechanical",
		Sapper = "Explosives",
		Sniper = "Marksmanship",
		Rifle = "Marksmanship",
	}
	local coveredStat = role and roleCovers[role]
	for _, row in ipairs(scored) do
		if #pitches >= 2 then
			break
		end
		if not (coveredStat and row.key == coveredStat) then
			pitches[#pitches + 1] = row.text
		end
	end
	if #pitches == 0 then
		local cat = ud and ud.AMECategory
		pitches[1] = (cat and AME_CAT_PITCH[cat]) or T(890000000006984, "looking for steady work")
	elseif #pitches == 1 then
		local cat = ud and ud.AMECategory
		if cat and AME_CAT_PITCH[cat] and cat ~= "Fighters" then
			pitches[2] = AME_CAT_PITCH[cat]
		end
	end
	return pitches
end

--- Sales blurb listing for Email context (Untranslated multiline).
function JAZZ_AME_BuildAvailableListingText()
	local lines = {}
	for _, id in ipairs(lAmeIds()) do
		local ud = gv_UnitData and gv_UnitData[id]
		if ud and ud.HireStatus == "Available" then
			local nickStr = lAsStr(lNickOrName(ud))
			local catStr = lAsStr(lCategoryLabel(ud))
			local pitches = JAZZ_AME_PickMercPitches(ud)
			local pitchParts = {}
			for _, p in ipairs(pitches) do
				pitchParts[#pitchParts + 1] = lAsStr(p)
			end
			local pitchStr = table.concat(pitchParts, "; ")
			lines[#lines + 1] = string.format("• %s (%s) — %s.", nickStr, catStr, pitchStr)
		end
	end
	if #lines == 0 then
		return lAsStr(T(890000000006904, "(no fighters listed right now)"))
	end
	return table.concat(lines, "\n")
end

function JAZZ_AME_BuildListingSnapshot()
	local parts = {}
	for _, id in ipairs(lAmeIds()) do
		local ud = gv_UnitData and gv_UnitData[id]
		if ud then
			local hs = ud.HireStatus or ""
			if hs == "Available" or hs == "Dead" or hs == "MIA" then
				parts[#parts + 1] = id .. "=" .. hs
			end
		end
	end
	table.sort(parts)
	return table.concat(parts, ";")
end

function JAZZ_AME_IsWelcomeRead()
	local market = lMarket()
	if market and market.welcome_read then
		return true
	end
	-- Recover from received emails if GameVar lagged.
	if type(GetReceivedEmails) == "function" then
		for _, email in ipairs(GetReceivedEmails()) do
			if email.id == AME_WELCOME_ID and email.read then
				if market then
					market.welcome_read = true
					market.welcome_sent = true
				end
				return true
			end
		end
	end
	return false
end

function JAZZ_AME_ApplyTabLock()
	-- JAZZ-UI-AME-001: tab always open (welcome mail is informational only).
	-- Starting hire PDA has no Mail access — lock blocked early AME hires.
	if not PDABrowserTabState then
		return
	end
	if PDABrowserTabState.ame then
		PDABrowserTabState.ame.locked = false
	else
		PDABrowserTabState.ame = { locked = false }
	end
	ObjModified("pda browser tabs")
end

function JAZZ_AME_SendWelcomeMail()
	local market = lMarket()
	if not market or market.welcome_sent then
		return false
	end
	if type(ReceiveEmail) ~= "function" then
		return false
	end
	if not Emails or not Emails[AME_WELCOME_ID] then
		return false
	end
	local listing = JAZZ_AME_BuildAvailableListingText()
	ReceiveEmail(AME_WELCOME_ID, { listing = Untranslated(listing) })
	market.welcome_sent = true
	market.listing_snapshot = JAZZ_AME_BuildListingSnapshot()
	JAZZ_AME_ApplyTabLock()
	return true
end

function JAZZ_AME_SendListingUpdateMail()
	local market = lMarket()
	if not market or not market.welcome_sent then
		return false
	end
	if type(ReceiveEmail) ~= "function" then
		return false
	end
	if not Emails or not Emails[AME_LISTING_ID] then
		return false
	end
	local snap = JAZZ_AME_BuildListingSnapshot()
	if snap == (market.listing_snapshot or false) then
		return false
	end
	local listing = JAZZ_AME_BuildAvailableListingText()
	ReceiveEmail(AME_LISTING_ID, { listing = Untranslated(listing) })
	market.listing_snapshot = snap
	return true
end

function JAZZ_AME_OnWelcomeRead()
	local market = lMarket()
	if market then
		market.welcome_read = true
		market.welcome_sent = true
	end
	JAZZ_AME_ApplyTabLock()
	if type(DockBrowserTab) == "function" then
		-- Prefer base unlock without triggering aim→ame recurse issues.
		local base = rawget(_G, "g_JAZZ_AME_DockBase")
		if type(base) == "function" then
			base("ame")
		else
			DockBrowserTab("ame")
		end
	end
end

local function lMaybeUnlockFromEmail(uniqueId)
	local mail = type(GetReceivedEmail) == "function" and GetReceivedEmail(uniqueId)
	if not mail or mail == empty_table then
		return
	end
	if mail.id == AME_WELCOME_ID and mail.read then
		JAZZ_AME_OnWelcomeRead()
	end
end

local function lInstallMarkEmailWrap()
	if rawget(_G, "g_JAZZ_AME_MarkEmailWrapped") then
		local base = rawget(_G, "g_JAZZ_AME_MarkEmailBase")
		if type(base) == "function" and NetSyncEvents and NetSyncEvents.MarkEmailAsRead then
			-- re-bind if wiped
		else
			return
		end
	end
	if not NetSyncEvents or type(NetSyncEvents.MarkEmailAsRead) ~= "function" then
		return
	end
	if not rawget(_G, "g_JAZZ_AME_MarkEmailBase") then
		rawset(_G, "g_JAZZ_AME_MarkEmailBase", NetSyncEvents.MarkEmailAsRead)
	end
	local base = g_JAZZ_AME_MarkEmailBase
	function NetSyncEvents.MarkEmailAsRead(uniqueId, val)
		base(uniqueId, val)
		if val then
			lMaybeUnlockFromEmail(uniqueId)
		end
	end
	rawset(_G, "g_JAZZ_AME_MarkEmailWrapped", true)
end

function OnMsg.DataLoaded()
	lInstallMarkEmailWrap()
end

function OnMsg.ModsReloaded()
	lInstallMarkEmailWrap()
	JAZZ_AME_ApplyTabLock()
end
