-- AME mail + welcome-read analytics for the always-open PDA tab (JAZZ-UI-AME-001).
-- Extends gv_JAZZ_AME_Market (defined in System_AME_Market.lua).

g_JAZZ_AME_MarkEmailWrapped = rawget(_G, "g_JAZZ_AME_MarkEmailWrapped") or false
g_JAZZ_AME_MarkEmailBase = rawget(_G, "g_JAZZ_AME_MarkEmailBase") or false
g_JAZZ_AME_MarkEmailFn = rawget(_G, "g_JAZZ_AME_MarkEmailFn") or false

local AME_WELCOME_ID = "AME_Welcome"
local AME_LISTING_ID = "AME_ListingUpdate"

local AME_IDS = {}
for i = 1, 60 do
	AME_IDS[i] = string.format("JAZZ_AME_%02d", i)
end

local AME_CAT_LABEL = {
	Irregulars = T(890000000006900, "Irregulars"),
	Fighters = T(890000000006901, "Fighters"),
	Hardened = T(890000000006902, "Hardened"),
	Specialists = T(890000000006903, "Specialists"),
}

-- Ad pitches: role first, then stats. Sales desk tone, not a stat dump.
local AME_ROLE_PITCH = {
	Medic = T(890000000006960, "keeps a squad moving after the shooting starts"),
	Instructor = T(890000000006961, "knows how to turn raw hands into a team"),
	Sniper = T(890000000006962, "makes distance work in your favor"),
	Sapper = T(890000000006963, "understands mines, charges, and stubborn doors"),
	Mechanic = T(890000000006964, "keeps worn guns and gear alive"),
	Rifle = T(890000000006965, "steady with a rifle and easy to work with"),
	Autorifleman = T(890000000006966, "brings automatic fire when the line needs weight"),
	Machinegunner = T(890000000006967, "holds ground behind a heavy gun"),
	Grenadier = T(890000000006968, "reaches enemies who think a wall is enough"),
}

local AME_STAT_PITCH = {
	{ key = "Marksmanship", min = 58, text = T(890000000006970, "a reliable shot") },
	{ key = "Medical", min = 40, text = T(890000000006971, "can keep a wound from becoming a funeral") },
	{ key = "Mechanical", min = 40, text = T(890000000006972, "knows one end of a toolkit from the other") },
	{ key = "Explosives", min = 35, text = T(890000000006973, "does not lose their nerve around explosives") },
	{ key = "Strength", min = 70, text = T(890000000006974, "can carry more than their share") },
	{ key = "Health", min = 80, text = T(890000000006975, "hard to put down") },
	{ key = "Leadership", min = 45, text = T(890000000006976, "people tend to listen") },
	{ key = "Wisdom", min = 65, text = T(890000000006977, "learns quickly") },
	{ key = "Agility", min = 68, text = T(890000000006978, "moves well under fire") },
	{ key = "Dexterity", min = 68, text = T(890000000006979, "good hands under pressure") },
}

local AME_CAT_PITCH = {
	Irregulars = T(890000000006980, "an affordable start with room to grow"),
	Fighters = T(890000000006981, "ready for field work"),
	Hardened = T(890000000006982, "already tested under fire"),
	Specialists = T(890000000006983, "a scarce skill worth securing"),
}

local function lMarket()
	return gv_JAZZ_AME_Market
end

local function lAmeIds()
	return AME_IDS
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
	local translate = rawget(_G, "_InternalTranslate")
	if type(translate) == "function" then
		local ok, s = pcall(translate, val)
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
	local getReceivedEmails = rawget(_G, "GetReceivedEmails")
	if type(getReceivedEmails) == "function" then
		for _, email in ipairs(getReceivedEmails()) do
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
	local tabState = rawget(_G, "PDABrowserTabState")
	if type(tabState) ~= "table" then
		return
	end
	if tabState.ame then
		tabState.ame.locked = false
	else
		tabState.ame = { locked = false }
	end
	ObjModified("pda browser tabs")
end

local function lSendListingMail(email_id, market)
	local receiveEmail = rawget(_G, "ReceiveEmail")
	local emails = rawget(_G, "Emails")
	if type(receiveEmail) ~= "function" then
		return false
	end
	if type(emails) ~= "table" or not emails[email_id] then
		return false
	end
	local listing = JAZZ_AME_BuildAvailableListingText()
	receiveEmail(email_id, { listing = Untranslated(listing) })
	market.listing_snapshot = JAZZ_AME_BuildListingSnapshot()
	return true
end

function JAZZ_AME_SendWelcomeMail()
	local market = lMarket()
	if not market or market.welcome_sent then
		return false
	end
	if not lSendListingMail(AME_WELCOME_ID, market) then
		return false
	end
	market.welcome_sent = true
	JAZZ_AME_ApplyTabLock()
	return true
end

function JAZZ_AME_SendListingUpdateMail()
	local market = lMarket()
	if not market or not market.welcome_sent then
		return false
	end
	local snap = JAZZ_AME_BuildListingSnapshot()
	if snap == (market.listing_snapshot or false) then
		return false
	end
	return lSendListingMail(AME_LISTING_ID, market)
end

function JAZZ_AME_OnWelcomeRead()
	local market = lMarket()
	if market then
		market.welcome_read = true
		market.welcome_sent = true
	end
	JAZZ_AME_ApplyTabLock()
	local dock = rawget(_G, "DockBrowserTab")
	if type(dock) == "function" then
		-- Prefer base unlock without triggering aim→ame recurse issues.
		local base = rawget(_G, "g_JAZZ_AME_DockBase")
		if type(base) == "function" then
			base("ame")
		else
			dock("ame")
		end
	end
end

local function lMaybeUnlockFromEmail(uniqueId)
	local getReceivedEmail = rawget(_G, "GetReceivedEmail")
	local mail = type(getReceivedEmail) == "function" and getReceivedEmail(uniqueId)
	if not mail or mail == empty_table then
		return
	end
	if mail.id == AME_WELCOME_ID and mail.read then
		JAZZ_AME_OnWelcomeRead()
	end
end

local function lInstallMarkEmailWrap()
	local events = rawget(_G, "NetSyncEvents")
	if type(events) ~= "table" or type(events.MarkEmailAsRead) ~= "function" then
		return
	end
	local current = events.MarkEmailAsRead
	local installed = rawget(_G, "g_JAZZ_AME_MarkEmailFn")
	if installed and current == installed then
		return
	end
	rawset(_G, "g_JAZZ_AME_MarkEmailBase", current)
	local base = current
	local wrap = function(uniqueId, val)
		base(uniqueId, val)
		if val then
			lMaybeUnlockFromEmail(uniqueId)
		end
	end
	rawset(_G, "g_JAZZ_AME_MarkEmailFn", wrap)
	events.MarkEmailAsRead = wrap
	rawset(_G, "g_JAZZ_AME_MarkEmailWrapped", true)
end

function OnMsg.DataLoaded()
	lInstallMarkEmailWrap()
end

function OnMsg.ModsReloaded()
	lInstallMarkEmailWrap()
	JAZZ_AME_ApplyTabLock()
end
