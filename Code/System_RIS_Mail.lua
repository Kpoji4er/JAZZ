-- R.I.S. mail: delayed queue (welcome + Legion briefs), tab lock (JAZZ-UI-RIS-001).
-- Desk sends at most one notification every RIS_DISPATCH_SPACING_H campaign hours.
-- Items become eligible at their own ready_at (welcome ~2h; baseline brief ~7h; raises ~5h after event).

GameVar("gv_JAZZ_RIS", function()
	return {
		welcome_sent = false,
		welcome_read = false,
		last_mailed_tier = 0,
		mod_awake_at = false,
		mail_queue = {},
		next_dispatch_at = 0,
		kills = {},
		met_types = {},
		obits_sent = {},
		battles = {},
		dossiers = {},
		quest_met = {},
		-- legacy fields kept for old saves (ignored once queue is live)
		welcome_due_at = false,
	}
end)

g_JAZZ_RIS_MarkEmailWrapped = rawget(_G, "g_JAZZ_RIS_MarkEmailWrapped") or false
g_JAZZ_RIS_MarkEmailBase = rawget(_G, "g_JAZZ_RIS_MarkEmailBase") or false
g_JAZZ_RIS_BrowserInstalled = rawget(_G, "g_JAZZ_RIS_BrowserInstalled") or false

local RIS_WELCOME_ID = "RIS_Welcome"
local RIS_WELCOME_DELAY_H = 2
local RIS_BASELINE_BRIEF_DELAY_H = 7
local RIS_RAISE_BRIEF_DELAY_H = 5
local RIS_FIELD_NOTE_DELAY_H = 5
local RIS_DISPATCH_SPACING_H = 5

local RIS_SIGHTING_ID = "RIS_UnitSighting"
local RIS_ELITE_OBIT_ID = "RIS_EliteObit"
local RIS_NPC_OBIT_ID = "RIS_NpcObit"

local RIS_BRIEF_TIERS = { 11, 12, 13, 21, 22, 23, 24, 25, 31, 32, 33 }

local function lState()
	local st = gv_JAZZ_RIS
	if not st then
		return false
	end
	if type(st.mail_queue) ~= "table" then
		st.mail_queue = {}
	end
	if type(st.next_dispatch_at) ~= "number" then
		st.next_dispatch_at = 0
	end
	if type(st.kills) ~= "table" then
		st.kills = {}
	end
	if type(st.battles) ~= "table" then
		st.battles = {}
	end
	if type(st.dossiers) ~= "table" then
		st.dossiers = {}
	end
	if type(st.met_types) ~= "table" then
		st.met_types = {}
	end
	if type(st.obits_sent) ~= "table" then
		st.obits_sent = {}
	end
	return st
end

local function lHour()
	return (const and const.Scale and const.Scale.h) or (60 * 60 * 1000)
end

local function lNow()
	return Game and Game.CampaignTime or 0
end

local function lBriefEmailId(tier)
	return string.format("RIS_LegionBrief_%d", tier)
end

local function lResolveBriefEmail(tier)
	tier = tonumber(tier)
	if not tier then
		return false, false
	end
	local emailId = lBriefEmailId(tier)
	if Emails and Emails[emailId] then
		return emailId, tier
	end
	for i = #RIS_BRIEF_TIERS, 1, -1 do
		local t = RIS_BRIEF_TIERS[i]
		if t <= tier and Emails and Emails[lBriefEmailId(t)] then
			return lBriefEmailId(t), t
		end
	end
	return false, false
end

local function lHasAnyLegionBriefMail()
	if type(GetReceivedEmails) ~= "function" then
		return false
	end
	for _, email in ipairs(GetReceivedEmails()) do
		if type(email.id) == "string" and string.match(email.id, "^RIS_LegionBrief_") then
			return true
		end
	end
	return false
end

local function lQueueHasKey(st, key)
	for _, item in ipairs(st.mail_queue) do
		if item.key == key then
			return true
		end
	end
	return false
end

local function lEnqueue(st, item)
	if not st or not item or not item.key or not item.email_id then
		return false
	end
	if lQueueHasKey(st, item.key) then
		-- Refresh ready_at if an older pending entry exists (e.g. raise again).
		for _, row in ipairs(st.mail_queue) do
			if row.key == item.key then
				if item.ready_at and (not row.ready_at or item.ready_at < row.ready_at) then
					row.ready_at = item.ready_at
				end
				if item.tier then
					row.tier = item.tier
					row.email_id = item.email_id
				end
				return false
			end
		end
	end
	st.mail_queue[#st.mail_queue + 1] = item
	return true
end

function JAZZ_RIS_IsWelcomeRead()
	local st = lState()
	if st and st.welcome_read then
		return true
	end
	if type(GetReceivedEmails) == "function" then
		for _, email in ipairs(GetReceivedEmails()) do
			if email.id == RIS_WELCOME_ID and email.read then
				if st then
					st.welcome_read = true
					st.welcome_sent = true
				end
				return true
			end
		end
	end
	return false
end

function JAZZ_RIS_ApplyTabLock()
	if not PDABrowserTabState then
		return
	end
	local unlocked = JAZZ_RIS_IsWelcomeRead()
	if PDABrowserTabState.ris then
		PDABrowserTabState.ris.locked = not unlocked
	else
		PDABrowserTabState.ris = { locked = not unlocked }
	end
	ObjModified("pda browser tabs")
end

local function lEnsureAwake(st)
	if not st.mod_awake_at then
		st.mod_awake_at = lNow()
	end
	return st.mod_awake_at
end

--- Schedule welcome + baseline supply brief (usually T1-1) after mod awake / NewGame.
function JAZZ_RIS_EnsureStartupQueue()
	local st = lState()
	if not st then
		return
	end
	local awake = lEnsureAwake(st)
	if not st.welcome_sent and not lQueueHasKey(st, "welcome") then
		if type(GetReceivedEmails) == "function" then
			for _, email in ipairs(GetReceivedEmails()) do
				if email.id == RIS_WELCOME_ID then
					st.welcome_sent = true
					break
				end
			end
		end
	end
	if not st.welcome_sent and not lQueueHasKey(st, "welcome") and Emails and Emails[RIS_WELCOME_ID] then
		lEnqueue(st, {
			key = "welcome",
			kind = "welcome",
			email_id = RIS_WELCOME_ID,
			ready_at = awake + RIS_WELCOME_DELAY_H * lHour(),
		})
	end
	-- Baseline brief: current tier once, ~2h after awake (fixes missing T1-1).
	local current = (rawget(_G, "JAZZ_GetLegionTier") and tonumber(JAZZ_GetLegionTier())) or 11
	local emailId, tier = lResolveBriefEmail(current)
	local briefKey = emailId and ("brief_" .. tostring(tier)) or false
	local already = (tonumber(st.last_mailed_tier) or 0) >= (tier or 0) and lHasAnyLegionBriefMail()
	if emailId and briefKey and not already and not lQueueHasKey(st, briefKey) then
		-- Poisoned saves marked last_mailed without inbox: still queue.
		if (tonumber(st.last_mailed_tier) or 0) >= tier and not lHasAnyLegionBriefMail() then
			st.last_mailed_tier = 0
		end
		if (tonumber(st.last_mailed_tier) or 0) < tier then
			lEnqueue(st, {
				key = briefKey,
				kind = "brief",
				email_id = emailId,
				tier = tier,
				ready_at = awake + RIS_BASELINE_BRIEF_DELAY_H * lHour(),
			})
		end
	end
end

local function lTrPlain(t)
	if t == nil then
		return ""
	end
	if type(t) == "string" then
		return t
	end
	if type(_InternalTranslate) == "function" then
		local ok, s = pcall(_InternalTranslate, t)
		if ok and s then
			return s
		end
	end
	return tostring(t)
end

local function lContextForEmail(ctx)
	if type(ctx) ~= "table" then
		return false
	end
	local out = {}
	for k, v in pairs(ctx) do
		if type(v) == "string" then
			out[k] = Untranslated(v)
		else
			out[k] = v
		end
	end
	return out
end

local function lDeliver(st, item)
	if type(ReceiveEmail) ~= "function" or not Emails or not Emails[item.email_id] then
		return false
	end
	local ctx = lContextForEmail(item.context)
	if ctx then
		ReceiveEmail(item.email_id, ctx)
	else
		ReceiveEmail(item.email_id)
	end
	if item.kind == "welcome" then
		st.welcome_sent = true
		JAZZ_RIS_ApplyTabLock()
	elseif item.kind == "brief" and item.tier then
		st.last_mailed_tier = Max(tonumber(st.last_mailed_tier) or 0, item.tier)
	elseif item.kind == "meet" and item.type_id then
		st.met_types[item.type_id] = true
		-- Catalog unlock when the sighting mail actually arrives.
		st.dossiers[item.type_id] = true
		ObjModified("jazz_ris")
	elseif item.kind == "obit" and item.obit_key then
		st.obits_sent[item.obit_key] = true
	end
	return true
end

--- Drain at most one eligible item when the 5h desk slot is free.
function JAZZ_RIS_ProcessMailQueue()
	local st = lState()
	if not st then
		return false
	end
	JAZZ_RIS_EnsureStartupQueue()
	local now = lNow()
	if now < (tonumber(st.next_dispatch_at) or 0) then
		return false
	end
	local idx = false
	for i, item in ipairs(st.mail_queue) do
		if (tonumber(item.ready_at) or 0) <= now then
			idx = i
			break
		end
	end
	-- Note: scan finds the earliest *ready* item in FIFO order (skip not-yet-ready heads).
	if not idx then
		return false
	end
	local item = table.remove(st.mail_queue, idx)
	if not lDeliver(st, item) then
		-- Put back at front if preset missing (retry later).
		table.insert(st.mail_queue, 1, item)
		st.next_dispatch_at = now + RIS_DISPATCH_SPACING_H * lHour()
		return false
	end
	st.next_dispatch_at = now + RIS_DISPATCH_SPACING_H * lHour()
	return true
end

function JAZZ_RIS_EnqueueLegionBrief(tier, delay_h)
	tier = tonumber(tier)
	if not tier then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	local emailId, resolved = lResolveBriefEmail(tier)
	if not emailId then
		return false
	end
	if (tonumber(st.last_mailed_tier) or 0) >= resolved and lHasAnyLegionBriefMail() then
		return false
	end
	delay_h = tonumber(delay_h) or RIS_RAISE_BRIEF_DELAY_H
	lEnqueue(st, {
		key = "brief_" .. tostring(resolved),
		kind = "brief",
		email_id = emailId,
		tier = resolved,
		ready_at = lNow() + delay_h * lHour(),
	})
	return true
end

function JAZZ_RIS_OnTierRaised(new_tier)
	new_tier = tonumber(new_tier)
	if not new_tier then
		return
	end
	JAZZ_RIS_EnqueueLegionBrief(new_tier, RIS_RAISE_BRIEF_DELAY_H)
end

--- First contact with a Legion archetype → desk note using dossier prose.
function JAZZ_RIS_EnqueueUnitSighting(type_id, delay_h)
	if type(type_id) ~= "string" or not string.match(type_id, "^JAZZ_Legion_") then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	if st.met_types[type_id] or lQueueHasKey(st, "meet_" .. type_id) then
		return false
	end
	local card = rawget(_G, "JAZZ_RIS_DOSSIERS") and JAZZ_RIS_DOSSIERS[type_id]
	if not card then
		return false
	end
	if not Emails or not Emails[RIS_SIGHTING_ID] then
		return false
	end
	delay_h = tonumber(delay_h) or RIS_FIELD_NOTE_DELAY_H
	local title = lTrPlain(card.title)
	local body = lTrPlain(card.body)
	lEnqueue(st, {
		key = "meet_" .. type_id,
		kind = "meet",
		email_id = RIS_SIGHTING_ID,
		type_id = type_id,
		ready_at = lNow() + delay_h * lHour(),
		context = {
			unit_title = title,
			dossier = body,
		},
	})
	-- Mark met immediately so CombatStart spam cannot double-queue before deliver.
	st.met_types[type_id] = true
	return true
end

function JAZZ_RIS_EnqueueEliteObit(name, delay_h)
	local name_str = lTrPlain(name)
	if name_str == "" then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	local obit_key = "elite:" .. name_str
	if st.obits_sent[obit_key] or lQueueHasKey(st, "obit_" .. obit_key) then
		return false
	end
	if not Emails or not Emails[RIS_ELITE_OBIT_ID] then
		return false
	end
	delay_h = tonumber(delay_h) or RIS_FIELD_NOTE_DELAY_H
	lEnqueue(st, {
		key = "obit_" .. obit_key,
		kind = "obit",
		email_id = RIS_ELITE_OBIT_ID,
		obit_key = obit_key,
		ready_at = lNow() + delay_h * lHour(),
		context = {
			name = name_str,
		},
	})
	st.obits_sent[obit_key] = true
	return true
end

function JAZZ_RIS_EnqueueNpcObit(session_id, name, delay_h)
	if type(session_id) ~= "string" or session_id == "" then
		return false
	end
	local st = lState()
	if not st then
		return false
	end
	local keys = rawget(_G, "JAZZ_RIS_KEY_NPCS")
	local is_key = (keys and keys[session_id]) or (rawget(_G, "JAZZ_RIS_QUEST_DOSSIERS") and JAZZ_RIS_QUEST_DOSSIERS[session_id])
	if not is_key then
		return false
	end
	local obit_key = "npc:" .. session_id
	if st.obits_sent[obit_key] or lQueueHasKey(st, "obit_" .. obit_key) then
		return false
	end
	if not Emails or not Emails[RIS_NPC_OBIT_ID] then
		return false
	end
	local name_str = lTrPlain(name)
	if name_str == "" then
		name_str = session_id
	end
	delay_h = tonumber(delay_h) or RIS_FIELD_NOTE_DELAY_H
	lEnqueue(st, {
		key = "obit_" .. obit_key,
		kind = "obit",
		email_id = RIS_NPC_OBIT_ID,
		obit_key = obit_key,
		ready_at = lNow() + delay_h * lHour(),
		context = {
			name = name_str,
		},
	})
	st.obits_sent[obit_key] = true
	return true
end

--- LoadGame / awake: queue missing current brief (delayed), do not dump a pack.
function JAZZ_RIS_CatchUpBriefs()
	local st = lState()
	if not st then
		return
	end
	JAZZ_RIS_EnsureStartupQueue()
	local current = (rawget(_G, "JAZZ_GetLegionTier") and tonumber(JAZZ_GetLegionTier())) or false
	if not current then
		return
	end
	local last = tonumber(st.last_mailed_tier) or 0
	if current > last or (current == last and not lHasAnyLegionBriefMail()) then
		if current == last and not lHasAnyLegionBriefMail() then
			st.last_mailed_tier = 0
		end
		-- Old save jumped ahead: one brief for current, eligible after baseline delay from awake.
		local emailId, tier = lResolveBriefEmail(current)
		if emailId and (tonumber(st.last_mailed_tier) or 0) < tier then
			local awake = lEnsureAwake(st)
			local ready = Max(awake + RIS_BASELINE_BRIEF_DELAY_H * lHour(), lNow())
			-- If already past baseline window, still respect desk spacing via queue (ready now).
			if last > 0 and current > last then
				ready = lNow() + RIS_RAISE_BRIEF_DELAY_H * lHour()
			end
			lEnqueue(st, {
				key = "brief_" .. tostring(tier),
				kind = "brief",
				email_id = emailId,
				tier = tier,
				ready_at = ready,
			})
		end
	end
end

function JAZZ_RIS_OnWelcomeRead()
	local st = lState()
	if st then
		st.welcome_read = true
		st.welcome_sent = true
	end
	JAZZ_RIS_ApplyTabLock()
	if type(DockBrowserTab) == "function" then
		DockBrowserTab("ris")
	end
end

local function lMaybeUnlock(uniqueId)
	local mail = type(GetReceivedEmail) == "function" and GetReceivedEmail(uniqueId)
	if not mail or mail == empty_table then
		return
	end
	if mail.id == RIS_WELCOME_ID and mail.read then
		JAZZ_RIS_OnWelcomeRead()
	end
end

local function lInstallMarkEmailWrap()
	if not NetSyncEvents or type(NetSyncEvents.MarkEmailAsRead) ~= "function" then
		return
	end
	if rawget(_G, "g_JAZZ_RIS_MarkEmailWrapped") and NetSyncEvents.MarkEmailAsRead == rawget(_G, "g_JAZZ_RIS_MarkEmailFn") then
		return
	end
	rawset(_G, "g_JAZZ_RIS_MarkEmailBase", NetSyncEvents.MarkEmailAsRead)
	local base = g_JAZZ_RIS_MarkEmailBase
	local function wrap(uniqueId, val)
		base(uniqueId, val)
		if val then
			lMaybeUnlock(uniqueId)
		end
	end
	rawset(_G, "g_JAZZ_RIS_MarkEmailFn", wrap)
	NetSyncEvents.MarkEmailAsRead = wrap
	rawset(_G, "g_JAZZ_RIS_MarkEmailWrapped", true)
end

local function lEnsureRisTabData()
	if not PDABrowserTabData then
		return
	end
	if not table.find(PDABrowserTabData, "id", "ris") then
		local aimIdx = table.find(PDABrowserTabData, "id", "aim") or 1
		local ameIdx = table.find(PDABrowserTabData, "id", "ame")
		local insertAt = (ameIdx or aimIdx) + 1
		table.insert(PDABrowserTabData, insertAt, {
			id = "ris",
			DisplayName = T(890000000006920, "R.I.S."),
		})
	end
	if IsKindOf(PDABrowser, "PDABrowser") or rawget(_G, "PDABrowser") then
		PDABrowser.InternalModes = table.concat(table.map(PDABrowserTabData, "id"), ", ")
	end
end

function OnMsg.DataLoaded()
	lInstallMarkEmailWrap()
	lEnsureRisTabData()
	if rawget(_G, "JAZZ_RIS_InstallBrowser") then
		JAZZ_RIS_InstallBrowser()
	end
	JAZZ_RIS_ApplyTabLock()
end

function OnMsg.ModsReloaded()
	lInstallMarkEmailWrap()
	lEnsureRisTabData()
	if rawget(_G, "JAZZ_RIS_InstallBrowser") then
		JAZZ_RIS_InstallBrowser()
	end
	JAZZ_RIS_ApplyTabLock()
end

function OnMsg.NewGame()
	DelayedCall(0, function()
		local st = lState()
		if st then
			st.mod_awake_at = lNow()
			st.welcome_sent = false
			st.welcome_read = false
			st.last_mailed_tier = 0
			st.mail_queue = {}
			st.next_dispatch_at = 0
			st.welcome_due_at = false
		end
		JAZZ_RIS_EnsureStartupQueue()
		JAZZ_RIS_ApplyTabLock()
	end)
end

function OnMsg.LoadGame()
	DelayedCall(0, function()
		JAZZ_RIS_EnsureStartupQueue()
		JAZZ_RIS_CatchUpBriefs()
		JAZZ_RIS_ProcessMailQueue()
		JAZZ_RIS_ApplyTabLock()
	end)
end

function OnMsg.SatelliteTick()
	JAZZ_RIS_ProcessMailQueue()
end

function OnMsg.OpenSatelliteView()
	JAZZ_RIS_ProcessMailQueue()
end
