-- M.E.R.C. credit account: daily accrual, Pay, reminder → quit (JAZZ-UI-MERC-001).
-- Hire path: vanilla chat / HireMerc still runs prepaid; OnMsg.MercHired refunds into
-- the credit account and charges the first day only (no HireMerc wrap — avoids double refund).

GameVar("gv_JAZZ_MERC_Account", function()
	return {
		initialized = false,
		balance = 0,
		paid_total = 0,
		last_reminder_day = false,
		warning_stage = 0,
		welcome_sent = false,
		welcome_read = false,
		unlocked = false,
		met = {},
		-- Implementation: last campaign day salary was accrued (not part of public schema).
		last_accrual_day = false,
	}
end)

local MERC_REMINDER_DAYS = 7
local MERC_GRACE_DAYS = 3

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
	return rawget(_G, "gv_JAZZ_MERC_Account")
end

function JAZZ_MERC_EnsureAccount()
	local account = lAccount()
	if not account then
		return false
	end
	account.balance = account.balance or 0
	account.paid_total = account.paid_total or 0
	account.warning_stage = account.warning_stage or 0
	account.met = account.met or {}
	if account.welcome_sent == nil then
		account.welcome_sent = false
	end
	if account.welcome_read == nil then
		account.welcome_read = false
	end
	if account.unlocked == nil then
		account.unlocked = false
	end
	if account.initialized == nil then
		account.initialized = false
	end
	return account
end

function JAZZ_MERC_IsUnlocked()
	local account = JAZZ_MERC_EnsureAccount()
	return account and account.unlocked and true or false
end

function JAZZ_MERC_ApplyTabLock()
	local tabState = rawget(_G, "PDABrowserTabState")
	if type(tabState) ~= "table" then
		return
	end
	local unlocked = JAZZ_MERC_IsUnlocked()
	if tabState.merc then
		tabState.merc.locked = not unlocked
	else
		tabState.merc = { locked = not unlocked }
	end
	ObjModified("pda browser tabs")
end

local function lDailyWage(ud)
	if not ud then
		return 0
	end
	local getFlag = rawget(_G, "GetMercStateFlag")
	if type(getFlag) == "function" and ud.session_id then
		local flagged = getFlag(ud.session_id, "CurrentDailySalary")
		local n = tonumber(flagged)
		if n and n > 0 then
			return n
		end
	end
	return tonumber(ud.StartingSalary) or 0
end

local function lNoteDebtClock(account, day)
	if not account then
		return
	end
	if (account.balance or 0) <= 0 then
		account.warning_stage = 0
		account.last_reminder_day = false
		return
	end
	-- Start unpaid clock when balance first goes positive.
	if (account.warning_stage or 0) == 0 and not account.last_reminder_day then
		account.last_reminder_day = day
	end
end

--- Accrue StartingSalary (or CurrentDailySalary) for each Hired Affiliation=MERC.
function JAZZ_MERC_AccrueDaily(force)
	local account = JAZZ_MERC_EnsureAccount()
	if not account then
		return false
	end
	local day = lCampaignDay()
	if not force and account.last_accrual_day == day then
		return false
	end
	account.last_accrual_day = day
	local unitData = rawget(_G, "gv_UnitData")
	if type(unitData) ~= "table" then
		return false
	end
	local added = 0
	for _, ud in pairs(unitData) do
		if ud and ud.Affiliation == "MERC" and ud.HireStatus == "Hired" then
			local wage = lDailyWage(ud)
			if wage > 0 then
				account.balance = (account.balance or 0) + wage
				added = added + wage
			end
		end
	end
	if added > 0 then
		lNoteDebtClock(account, day)
	elseif (account.balance or 0) <= 0 then
		account.warning_stage = 0
		account.last_reminder_day = false
	end
	return added > 0
end

--- Spend player money against the MERC credit balance.
function JAZZ_MERC_PayAccount(amount)
	local account = JAZZ_MERC_EnsureAccount()
	if not account then
		return false
	end
	amount = tonumber(amount) or 0
	if amount <= 0 then
		return false
	end
	local due = account.balance or 0
	if due <= 0 then
		return false
	end
	local pay = amount
	if pay > due then
		pay = due
	end
	local game = rawget(_G, "Game")
	local money = game and tonumber(game.Money) or 0
	if money < pay then
		pay = money
	end
	if pay <= 0 then
		return false
	end
	local addMoney = rawget(_G, "AddMoney")
	if type(addMoney) ~= "function" then
		return false
	end
	addMoney(-pay, "salary", "noCombatLog")
	account.balance = due - pay
	account.paid_total = (account.paid_total or 0) + pay
	if account.balance <= 0 then
		account.balance = 0
		account.warning_stage = 0
		account.last_reminder_day = false
	end
	ObjModified(account)
	return true
end

local function lReleaseHiredMerc(merc_id)
	local nse = rawget(_G, "NetSyncEvent")
	if type(nse) == "function" then
		nse("ReleaseMerc", merc_id)
		return true
	end
	local events = rawget(_G, "NetSyncEvents")
	if type(events) == "table" and type(events.ReleaseMerc) == "function" then
		events.ReleaseMerc(merc_id)
		return true
	end
	-- Fallback: return to Available without full despawn path (best-effort).
	local ud = gv_UnitData and gv_UnitData[merc_id]
	if ud and ud.HireStatus == "Hired" then
		ud.HireStatus = "Available"
		ud.HiredUntil = false
		Msg("MercHireStatusChanged", ud, "Hired", "Available")
		ObjModified(ud)
		return true
	end
	return false
end

local function lQuitAllHiredMERC()
	local unitData = rawget(_G, "gv_UnitData")
	if type(unitData) ~= "table" then
		return
	end
	local ids = {}
	for id, ud in pairs(unitData) do
		if ud and ud.Affiliation == "MERC" and ud.HireStatus == "Hired" then
			ids[#ids + 1] = ud.session_id or id
		end
	end
	table.sort(ids)
	for _, merc_id in ipairs(ids) do
		lReleaseHiredMerc(merc_id)
	end
end

--- Reminder after ~7d unpaid balance; grace +3d → quit hired MERC. Deterministic.
function JAZZ_MERC_TrySendReminder()
	local account = JAZZ_MERC_EnsureAccount()
	if not account then
		return false
	end
	local day = lCampaignDay()
	local balance = account.balance or 0
	if balance <= 0 then
		account.warning_stage = 0
		account.last_reminder_day = false
		return false
	end
	local stage = account.warning_stage or 0
	local clock = account.last_reminder_day
	if not clock then
		account.last_reminder_day = day
		return false
	end
	if stage == 0 then
		if day - clock >= MERC_REMINDER_DAYS then
			local send = rawget(_G, "JAZZ_MERC_SendAccountReminder")
			if type(send) == "function" then
				send()
			end
			account.warning_stage = 1
			account.last_reminder_day = day
			return true
		end
		return false
	end
	if stage == 1 then
		if day - clock >= MERC_GRACE_DAYS then
			local sendQuit = rawget(_G, "JAZZ_MERC_SendQuitWarning")
			if type(sendQuit) == "function" then
				sendQuit()
			end
			lQuitAllHiredMERC()
			account.warning_stage = 2
			account.last_reminder_day = day
			return true
		end
	end
	return false
end

--- After vanilla HireMerc succeeds: refund prepaid into credit model; charge first day only.
-- AIM/AME prepaid unchanged (Affiliation ~= MERC). Extensions: refund prepaid; NewDay keeps accrual.
function JAZZ_MERC_OnHired(merc_id, price, days, alreadyHired)
	local ud = gv_UnitData and gv_UnitData[merc_id]
	if not ud or ud.Affiliation ~= "MERC" then
		return false
	end
	local account = JAZZ_MERC_EnsureAccount()
	if not account then
		return false
	end
	local refund = tonumber(price) or 0
	if refund > 0 then
		local addMoney = rawget(_G, "AddMoney")
		if type(addMoney) == "function" then
			addMoney(refund, "salary", "noCombatLog")
		end
	end
	-- New hire first day: only if NewDay already accrued today (otherwise NewDay will charge them).
	-- Avoids double-charging when hire happens before the day's accrual tick.
	if not alreadyHired then
		local day = lCampaignDay()
		if account.last_accrual_day == day then
			local wage = lDailyWage(ud)
			if wage <= 0 then
				wage = tonumber(ud.StartingSalary) or 0
			end
			if wage > 0 then
				account.balance = (account.balance or 0) + wage
				lNoteDebtClock(account, day)
			end
		end
	end
	ObjModified(account)
	return true
end

function OnMsg.MercHired(merc_id, price, days, alreadyHired)
	JAZZ_MERC_OnHired(merc_id, price, days, alreadyHired)
end

function OnMsg.NewDay()
	JAZZ_MERC_EnsureAccount()
	JAZZ_MERC_AccrueDaily()
	JAZZ_MERC_TrySendReminder()
end

function OnMsg.SatelliteTick()
	-- Backup if NewDay is skipped in some satellite flows.
	JAZZ_MERC_EnsureAccount()
	JAZZ_MERC_AccrueDaily()
	JAZZ_MERC_TrySendReminder()
end
