-- M.E.R.C. mail: Day-2 welcome unlock, reminder / quit emails (JAZZ-UI-MERC-001).
-- Chains MarkEmailAsRead after AME/RIS wraps (install captures current as base).

g_JAZZ_MERC_MarkEmailWrapped = rawget(_G, "g_JAZZ_MERC_MarkEmailWrapped") or false
g_JAZZ_MERC_MarkEmailBase = rawget(_G, "g_JAZZ_MERC_MarkEmailBase") or false
g_JAZZ_MERC_MarkEmailFn = rawget(_G, "g_JAZZ_MERC_MarkEmailFn") or false

local MERC_WELCOME_ID = "MERC_Welcome"
local MERC_REMINDER_ID = "MERC_AccountReminder"
local MERC_QUIT_ID = "MERC_QuitWarning"
local MERC_WELCOME_DAY = 2

local function lCampaignDay()
	local game = rawget(_G, "Game")
	local scale = rawget(_G, "const")
	scale = scale and scale.Scale and scale.Scale.day
	if not game or not game.CampaignTime or not game.CampaignTimeStart or not scale then
		return 0
	end
	return (game.CampaignTime - game.CampaignTimeStart) / scale
end

local function lAccount()
	local ensure = rawget(_G, "JAZZ_MERC_EnsureAccount")
	if type(ensure) == "function" then
		return ensure()
	end
	return rawget(_G, "gv_JAZZ_MERC_Account")
end

local function lReceive(email_id, context)
	local receiveEmail = rawget(_G, "ReceiveEmail")
	local emails = rawget(_G, "Emails")
	if type(receiveEmail) ~= "function" then
		return false
	end
	if type(emails) == "table" and not emails[email_id] then
		return false
	end
	if context then
		receiveEmail(email_id, context)
	else
		receiveEmail(email_id)
	end
	return true
end

function JAZZ_MERC_SendWelcomeMail()
	local account = lAccount()
	if not account or account.welcome_sent then
		return false
	end
	if lCampaignDay() < MERC_WELCOME_DAY then
		return false
	end
	if not lReceive(MERC_WELCOME_ID) then
		return false
	end
	account.welcome_sent = true
	account.unlocked = true
	local apply = rawget(_G, "JAZZ_MERC_ApplyTabLock")
	if type(apply) == "function" then
		apply()
	end
	-- Optional: open shelf Availability when unlock mail lands (idempotent with Browser init).
	local initRoster = rawget(_G, "JAZZ_MERC_InitRoster")
	if type(initRoster) == "function" then
		initRoster(false)
	end
	return true
end

function JAZZ_MERC_SendAccountReminder()
	-- Speck voice reminder that the credit balance is overdue.
	return lReceive(MERC_REMINDER_ID, {
		balance = Untranslated(tostring((lAccount() and lAccount().balance) or 0)),
	})
end

function JAZZ_MERC_SendQuitWarning()
	return lReceive(MERC_QUIT_ID, {
		balance = Untranslated(tostring((lAccount() and lAccount().balance) or 0)),
	})
end

function JAZZ_MERC_TrySendWelcome()
	return JAZZ_MERC_SendWelcomeMail()
end

--- Save-compat: old campaigns without MERC flags / Speck mail.
-- Recover from inbox if Welcome already received; otherwise send once when day >= 2.
function JAZZ_MERC_MigrateWelcomeFromSave()
	local account = lAccount()
	if not account then
		return false
	end
	local getReceivedEmails = rawget(_G, "GetReceivedEmails")
	if type(getReceivedEmails) == "function" then
		for _, email in ipairs(getReceivedEmails()) do
			if email and email.id == MERC_WELCOME_ID then
				account.welcome_sent = true
				account.unlocked = true
				if email.read then
					account.welcome_read = true
				end
				local apply = rawget(_G, "JAZZ_MERC_ApplyTabLock")
				if type(apply) == "function" then
					apply()
				end
				local initRoster = rawget(_G, "JAZZ_MERC_InitRoster")
				if type(initRoster) == "function" then
					initRoster(false)
				end
				return "recovered"
			end
		end
	end
	if account.welcome_sent then
		-- Unlock may still be false on partial GameVar migration.
		if not account.unlocked then
			account.unlocked = true
			local apply = rawget(_G, "JAZZ_MERC_ApplyTabLock")
			if type(apply) == "function" then
				apply()
			end
		end
		return false
	end
	-- Mid-campaign / pre-MERC saves: do not wait for the next NewDay tick.
	if lCampaignDay() >= MERC_WELCOME_DAY then
		if JAZZ_MERC_SendWelcomeMail() then
			return "sent"
		end
	end
	return false
end

function JAZZ_MERC_IsWelcomeRead()
	local account = lAccount()
	if account and account.welcome_read then
		return true
	end
	local getReceivedEmails = rawget(_G, "GetReceivedEmails")
	if type(getReceivedEmails) == "function" then
		for _, email in ipairs(getReceivedEmails()) do
			if email.id == MERC_WELCOME_ID and email.read then
				if account then
					account.welcome_read = true
					account.welcome_sent = true
					account.unlocked = true
				end
				return true
			end
		end
	end
	return false
end

function JAZZ_MERC_OnWelcomeRead()
	local account = lAccount()
	if account then
		account.welcome_read = true
		account.welcome_sent = true
		account.unlocked = true
	end
	local apply = rawget(_G, "JAZZ_MERC_ApplyTabLock")
	if type(apply) == "function" then
		apply()
	end
	local dock = rawget(_G, "DockBrowserTab")
	if type(dock) == "function" then
		dock("merc")
	end
end

local function lMaybeWelcomeRead(uniqueId)
	local getReceivedEmail = rawget(_G, "GetReceivedEmail")
	local mail = type(getReceivedEmail) == "function" and getReceivedEmail(uniqueId)
	if not mail or mail == rawget(_G, "empty_table") then
		return
	end
	if mail.id == MERC_WELCOME_ID and mail.read then
		JAZZ_MERC_OnWelcomeRead()
	end
end

local function lInstallMarkEmailWrap()
	local events = rawget(_G, "NetSyncEvents")
	if type(events) ~= "table" or type(events.MarkEmailAsRead) ~= "function" then
		return
	end
	local current = events.MarkEmailAsRead
	local installed = rawget(_G, "g_JAZZ_MERC_MarkEmailFn")
	if installed and current == installed then
		return
	end
	-- Capture whatever is current (AME/RIS wrap) so we chain after them.
	rawset(_G, "g_JAZZ_MERC_MarkEmailBase", current)
	local base = current
	local wrap = function(uniqueId, val)
		base(uniqueId, val)
		if val then
			lMaybeWelcomeRead(uniqueId)
		end
	end
	rawset(_G, "g_JAZZ_MERC_MarkEmailFn", wrap)
	events.MarkEmailAsRead = wrap
	rawset(_G, "g_JAZZ_MERC_MarkEmailWrapped", true)
end

function OnMsg.DataLoaded()
	lInstallMarkEmailWrap()
end

function OnMsg.ModsReloaded()
	-- Re-chain on top after other mods reinstall their wraps.
	local delayed = rawget(_G, "DelayedCall")
	if type(delayed) == "function" then
		delayed(0, lInstallMarkEmailWrap)
	else
		lInstallMarkEmailWrap()
	end
	local apply = rawget(_G, "JAZZ_MERC_ApplyTabLock")
	if type(apply) == "function" then
		apply()
	end
end

function OnMsg.NewDay()
	JAZZ_MERC_TrySendWelcome()
end

function OnMsg.SatelliteTick()
	JAZZ_MERC_TrySendWelcome()
end

function OnMsg.LoadGame()
	-- Old saves: deliver Speck welcome once (or recover flags from inbox).
	local delayed = rawget(_G, "DelayedCall")
	local boot = function()
		local ensure = rawget(_G, "JAZZ_MERC_EnsureAccount")
		if type(ensure) == "function" then
			ensure()
		end
		JAZZ_MERC_MigrateWelcomeFromSave()
		local apply = rawget(_G, "JAZZ_MERC_ApplyTabLock")
		if type(apply) == "function" then
			apply()
		end
	end
	if type(delayed) == "function" then
		delayed(0, boot)
	else
		boot()
	end
end

-- Loc note: Email body presets live in items.lua (parent). Inline UI strings use 890000000009903+.
-- Reminder/quit ids: MERC_AccountReminder / MERC_QuitWarning (sender Speck / M.E.R.C.).
-- Save-compat: JAZZ_MERC_MigrateWelcomeFromSave on LoadGame (inbox recover or send if day>=2).
