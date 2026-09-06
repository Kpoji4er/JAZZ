-- M.E.R.C. credit account: daily accrual, Pay, reminder → quit (JAZZ-UI-MERC-001).
-- Alarm (JAZZ-UI-MERC-002): satellite debt chip + day-7 / day-9 popups; CombatLog on quit.
-- Hire path: vanilla chat / HireMerc still runs prepaid; OnMsg.MercHired refunds into
-- the credit account and charges the first day only (no HireMerc wrap — avoids double refund).
-- Gate: PDAMessengerClass:CanAffordMerc must allow Affiliation=MERC with $0 cash
-- (otherwise Offer stays disabled / "Insufficient funds" like AIM prepaid).

g_JAZZ_MERC_CanAffordBase = rawget(_G, "g_JAZZ_MERC_CanAffordBase") or false
g_JAZZ_MERC_CanAffordFn = rawget(_G, "g_JAZZ_MERC_CanAffordFn") or false
g_JAZZ_MERC_MoneyOpenBase = rawget(_G, "g_JAZZ_MERC_MoneyOpenBase") or false
g_JAZZ_MERC_MoneyOpenFn = rawget(_G, "g_JAZZ_MERC_MoneyOpenFn") or false
g_JAZZ_MERC_DebtPopupOpen = rawget(_G, "g_JAZZ_MERC_DebtPopupOpen") or false

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
		reminder_popup_sent = false,
		eve_popup_sent = false,
		-- Implementation: last campaign day salary was accrued (not part of public schema).
		last_accrual_day = false,
	}
end)

local MERC_REMINDER_DAYS = 7
local MERC_GRACE_DAYS = 3
local MERC_EVE_DAYS = 2
local MERC_TL_TYP = "jazz_merc_debt"
local MERC_TL_REMINDER = "jazz-merc-reminder"
local MERC_TL_QUIT = "jazz-merc-quit"

local function lIsMERCUnit(ud)
	return ud and ud.Affiliation == "MERC"
end

--- JA2-style credit: messenger Offer must not require prepaid cash.
local function lInstallCanAffordMercWrap()
	local cls = rawget(_G, "PDAMessengerClass")
	if not cls or type(cls.CanAffordMerc) ~= "function" then
		return false
	end
	local ourFn = rawget(_G, "g_JAZZ_MERC_CanAffordFn")
	if ourFn and cls.CanAffordMerc == ourFn then
		return true
	end
	local current = cls.CanAffordMerc
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_MERC_CanAffordBase", current)
	elseif not rawget(_G, "g_JAZZ_MERC_CanAffordBase") then
		return false
	end
	local base = g_JAZZ_MERC_CanAffordBase
	local function wrap(self, moneyOverride)
		local merc = self and self.context
		if lIsMERCUnit(merc) then
			return true
		end
		return base(self, moneyOverride)
	end
	rawset(_G, "g_JAZZ_MERC_CanAffordFn", wrap)
	cls.CanAffordMerc = wrap
	return true
end

local function lInstallMoneyOpenWrap()
	local cls = rawget(_G, "PDAMoneyText")
	if type(cls) ~= "table" or type(cls.Open) ~= "function" then
		return false
	end
	local ourFn = rawget(_G, "g_JAZZ_MERC_MoneyOpenFn")
	if ourFn and cls.Open == ourFn then
		return true
	end
	local current = cls.Open
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_MERC_MoneyOpenBase", current)
	elseif not rawget(_G, "g_JAZZ_MERC_MoneyOpenBase") then
		return false
	end
	local base = g_JAZZ_MERC_MoneyOpenBase
	local function wrap(self, ...)
		local res = base(self, ...)
		local getDlg = rawget(_G, "GetDialog")
		local sat = type(getDlg) == "function" and getDlg("PDADialogSatellite")
		if sat and self and (self == sat.idMoney or self.Id == "idMoney") then
			local refresh = rawget(_G, "JAZZ_MERC_RefreshDebtChip")
			if type(refresh) == "function" then
				refresh()
			end
		end
		return res
	end
	rawset(_G, "g_JAZZ_MERC_MoneyOpenFn", wrap)
	cls.Open = wrap
	return true
end

function OnMsg.ModsReloaded()
	lInstallCanAffordMercWrap()
	lInstallMoneyOpenWrap()
	local ensureTl = rawget(_G, "JAZZ_MERC_EnsureTimelineEventDef")
	if type(ensureTl) == "function" then
		ensureTl()
	end
end

function OnMsg.DataLoaded()
	lInstallCanAffordMercWrap()
	lInstallMoneyOpenWrap()
	local ensureTl = rawget(_G, "JAZZ_MERC_EnsureTimelineEventDef")
	if type(ensureTl) == "function" then
		ensureTl()
	end
end

lInstallCanAffordMercWrap()
-- PDAMoneyText wrap waits for DataLoaded / ModsReloaded (class may be missing at file load).

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
	if account.reminder_popup_sent == nil then
		account.reminder_popup_sent = false
	end
	if account.eve_popup_sent == nil then
		account.eve_popup_sent = false
	end
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

local function lClearDebtAlarm(account)
	if not account then
		return
	end
	account.warning_stage = 0
	account.last_reminder_day = false
	account.reminder_popup_sent = false
	account.eve_popup_sent = false
	local rem = rawget(_G, "RemoveTimelineEvent")
	if type(rem) == "function" then
		rem(MERC_TL_REMINDER)
		rem(MERC_TL_QUIT)
	end
end

local function lNoteDebtClock(account, day)
	if not account then
		return
	end
	if (account.balance or 0) <= 0 then
		lClearDebtAlarm(account)
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
		lClearDebtAlarm(account)
	end
	ObjModified(account)
	local refreshChip = rawget(_G, "JAZZ_MERC_RefreshDebtChip")
	if type(refreshChip) == "function" then
		refreshChip()
	end
	local syncTl = rawget(_G, "JAZZ_MERC_SyncTimeline")
	if type(syncTl) == "function" then
		syncTl()
	end
	return added > 0
end

--- Spend player money against the MERC credit balance.
-- Returns paid amount (number > 0) on success, or false.
function JAZZ_MERC_PayAccount(amount)
	local account = JAZZ_MERC_EnsureAccount()
	if not account then
		return false
	end
	amount = tonumber(amount)
	if not amount or amount <= 0 then
		amount = tonumber(account.balance) or 0
	end
	if amount <= 0 then
		return false
	end
	local due = tonumber(account.balance) or 0
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
	-- Visible CombatLog "Spent …" so Pay Account is not silent when the strip button is clipped.
	addMoney(-pay, "salary")
	account.balance = due - pay
	account.paid_total = (account.paid_total or 0) + pay
	if account.balance <= 0 then
		account.balance = 0
		lClearDebtAlarm(account)
	end
	ObjModified(account)
	ObjModified(game)
	local refreshChip = rawget(_G, "JAZZ_MERC_RefreshDebtChip")
	if type(refreshChip) == "function" then
		refreshChip()
	end
	local syncTl = rawget(_G, "JAZZ_MERC_SyncTimeline")
	if type(syncTl) == "function" then
		syncTl()
	end
	return pay
end

function JAZZ_MERC_CanPayAccount()
	local account = JAZZ_MERC_EnsureAccount()
	if not account then
		return false
	end
	local due = tonumber(account.balance) or 0
	if due <= 0 then
		return false
	end
	local game = rawget(_G, "Game")
	local money = game and tonumber(game.Money) or 0
	return money > 0
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

local function lCollectHiredMERCIds()
	local unitData = rawget(_G, "gv_UnitData")
	if type(unitData) ~= "table" then
		return {}
	end
	local ids = {}
	for id, ud in pairs(unitData) do
		if ud and ud.Affiliation == "MERC" and ud.HireStatus == "Hired" then
			ids[#ids + 1] = ud.session_id or id
		end
	end
	table.sort(ids)
	return ids
end

local function lDayTimestamp(day)
	local game = rawget(_G, "Game")
	local scale = rawget(_G, "const")
	scale = scale and scale.Scale and scale.Scale.day
	if not game or not game.CampaignTimeStart or not scale or not day then
		return false
	end
	return game.CampaignTimeStart + day * scale
end

function JAZZ_MERC_EnsureTimelineEventDef()
	local map = rawget(_G, "SatelliteTimelineEvents")
	if type(map) ~= "table" then
		return false
	end
	if map[MERC_TL_TYP] then
		return true
	end
	local place = rawget(_G, "PlaceObj")
	if type(place) ~= "function" then
		return false
	end
	local def = place("SatelliteTimelineEventDef", {
		id = MERC_TL_TYP,
		group = "Default",
		Title = T(890000000009953, "M.E.R.C. contractors"),
		Text = T(890000000009954, "Hired MERC contractors leave if $<balance> is unpaid."),
		Hint = T(890000000009955, "Pay Account on the M.E.R.C. site. Right-click opens the site."),
		GetIcon = function(self, eventCtx)
			return "UI/Icons/SateliteView/icon_ally", "UI/Icons/SateliteView/contract_expiration"
		end,
		GetTextContext = function(self, eventCtx)
			return eventCtx
		end,
		GetDescriptionText = function(self, eventCtx)
			if eventCtx and eventCtx.kind == "reminder" then
				return T(890000000009956, "Speck will demand payment. Contractors leave 3 days later if $<balance> is still unpaid."), self.Title, self.Hint
			end
			return self.Text, self.Title, self.Hint
		end,
		GetAssociatedMercs = function(self, eventCtx)
			return eventCtx and eventCtx.mercs
		end,
		GetMapLocation = function(self, eventCtx)
			local mercs = eventCtx and eventCtx.mercs
			local unitData = rawget(_G, "gv_UnitData")
			local sat = rawget(_G, "g_SatelliteUI")
			if type(mercs) ~= "table" or type(unitData) ~= "table" then
				return
			end
			for _, merc_id in ipairs(mercs) do
				local ud = unitData[merc_id]
				local squadId = ud and ud.Squad
				local wnd = sat and sat.squad_to_wnd and sat.squad_to_wnd[squadId]
				if wnd and wnd.GetVisualPos then
					return wnd:GetVisualPos()
				end
			end
		end,
		OnClick = function(self, event)
			return T(890000000009957, "Open M.E.R.C."), function()
				local open = rawget(_G, "JAZZ_MERC_OpenSite")
				if type(open) == "function" then
					open()
				end
			end
		end,
	})
	if not map[MERC_TL_TYP] and def then
		map[MERC_TL_TYP] = def
	end
	return not not map[MERC_TL_TYP]
end

function JAZZ_MERC_SyncTimeline()
	local rem = rawget(_G, "RemoveTimelineEvent")
	local add = rawget(_G, "AddTimelineEvent")
	if type(rem) ~= "function" or type(add) ~= "function" then
		return false
	end
	local account = JAZZ_MERC_EnsureAccount()
	local due = account and tonumber(account.balance) or 0
	local stage = account and (account.warning_stage or 0) or 0
	if due <= 0 or stage >= 2 then
		rem(MERC_TL_REMINDER)
		rem(MERC_TL_QUIT)
		return false
	end
	if not JAZZ_MERC_EnsureTimelineEventDef() then
		return false
	end
	local clock = account.last_reminder_day
	if not clock then
		clock = lCampaignDay()
		account.last_reminder_day = clock
	end
	local mercs = lCollectHiredMERCIds()
	local quitDay = stage == 0 and (clock + MERC_REMINDER_DAYS + MERC_GRACE_DAYS) or (clock + MERC_GRACE_DAYS)
	local quitDue = lDayTimestamp(quitDay)
	if quitDue then
		add(MERC_TL_QUIT, quitDue, MERC_TL_TYP, {
			kind = "quit",
			balance = due,
			mercs = mercs,
		})
	end
	if stage == 0 then
		local reminderDue = lDayTimestamp(clock + MERC_REMINDER_DAYS)
		if reminderDue then
			add(MERC_TL_REMINDER, reminderDue, MERC_TL_TYP, {
				kind = "reminder",
				balance = due,
				mercs = mercs,
			})
		end
	else
		rem(MERC_TL_REMINDER)
	end
	return true
end

local function lMercNickPlain(merc_id)
	local unitData = rawget(_G, "gv_UnitData")
	local ud = type(unitData) == "table" and unitData[merc_id]
	if not ud then
		return tostring(merc_id)
	end
	local nick = ud.Nick or ud.Name or merc_id
	local tr = rawget(_G, "_InternalTranslate")
	if type(tr) == "function" and nick then
		local ok, text = pcall(tr, nick)
		if ok and type(text) == "string" and text ~= "" then
			return text
		end
	end
	return tostring(merc_id)
end

local function lLogQuitCombatLog(ids)
	local log = rawget(_G, "CombatLog")
	if type(log) ~= "function" or type(ids) ~= "table" or #ids == 0 then
		return
	end
	local names = {}
	for _, merc_id in ipairs(ids) do
		names[#names + 1] = lMercNickPlain(merc_id)
	end
	log("important", T{
		890000000009952,
		"M.E.R.C. contractors left: <names>",
		names = Untranslated(table.concat(names, ", ")),
	})
end

local function lQuitAllHiredMERC()
	local ids = lCollectHiredMERCIds()
	lLogQuitCombatLog(ids)
	for _, merc_id in ipairs(ids) do
		lReleaseHiredMerc(merc_id)
	end
	return ids
end

local function lPopupParent()
	local getDlg = rawget(_G, "GetDialog")
	if type(getDlg) ~= "function" then
		return terminal and terminal.desktop
	end
	local sat = getDlg("PDADialogSatellite")
	if sat then
		local host = sat.ResolveId and sat:ResolveId("idDisplayPopupHost")
		return host or sat
	end
	local pda = getDlg("PDADialog")
	if pda then
		local host = pda.ResolveId and pda:ResolveId("idDisplayPopupHost")
		return host or pda
	end
	return terminal and terminal.desktop
end

local function lInCombat()
	return not not rawget(_G, "g_Combat")
end

--- Satellite header chip left of the date (HList after idMoney).
function JAZZ_MERC_RefreshDebtChip()
	local getDlg = rawget(_G, "GetDialog")
	if type(getDlg) ~= "function" then
		return false
	end
	local sat = getDlg("PDADialogSatellite")
	local money = sat and sat.idMoney
	if not money or money.window_state == "destroying" then
		return false
	end
	local parent = money.parent
	if not parent then
		return false
	end
	local account = JAZZ_MERC_EnsureAccount()
	local due = account and tonumber(account.balance) or 0
	local stage = account and (account.warning_stage or 0) or 0
	local chip = (sat.ResolveId and sat:ResolveId("idJazzMERCDebt"))
		or (parent.ResolveId and parent:ResolveId("idJazzMERCDebt"))
	if due <= 0 then
		if chip then
			chip:SetVisible(false)
		end
		return true
	end
	if not chip then
		local XText = rawget(_G, "XText")
		if type(XText) ~= "table" or type(XText.new) ~= "function" then
			return false
		end
		chip = XText:new({
			Id = "idJazzMERCDebt",
			HAlign = "right",
			VAlign = "center",
			Clip = false,
			UseClipBox = false,
			FoldWhenHidden = true,
			HandleMouse = true,
			Translate = true,
			TextStyle = "TimeTextBold",
			RolloverTemplate = "RolloverGeneric",
			RolloverAnchor = "center-bottom",
			RolloverTitle = T(890000000009945, "M.E.R.C. account"),
			RolloverText = T(890000000009946, "Unpaid credit. Click to open M.E.R.C. and Pay Account."),
		}, parent)
		chip.OnMouseButtonDown = function(self, pt, button)
			if button == "L" then
				local open = rawget(_G, "JAZZ_MERC_OpenSite")
				if type(open) == "function" then
					open()
				end
				return "break"
			end
		end
		if chip.window_state == "new" and type(chip.Open) == "function" then
			chip:Open()
		end
		-- ChildJoining appends; keep the chip immediately after money, not after the date.
		local moneyIdx
		for i, child in ipairs(parent) do
			if child == money then
				moneyIdx = i
				break
			end
		end
		if moneyIdx and parent[#parent] == chip and #parent ~= moneyIdx + 1 then
			table.remove(parent, #parent)
			table.insert(parent, moneyIdx + 1, chip)
			if parent.InvalidateLayout then
				parent:InvalidateLayout()
			end
		end
	end
	chip:SetText(T{890000000009944, "MERC $<balance>", balance = due})
	if type(chip.SetTextColor) == "function" then
		-- Yellow while the unpaid clock runs; red after Speck's 7-day reminder.
		chip:SetTextColor(stage >= 1 and RGB(220, 48, 40) or RGB(230, 186, 40))
	end
	chip:SetVisible(true)
	return true
end

function JAZZ_MERC_ShowDebtPopup(kind)
	if rawget(_G, "g_JAZZ_MERC_DebtPopupOpen") then
		return false
	end
	if lInCombat() then
		return false
	end
	local waitChoice = rawget(_G, "WaitPopupChoice")
	local createThread = rawget(_G, "CreateRealTimeThread")
	if type(waitChoice) ~= "function" or type(createThread) ~= "function" then
		return false
	end
	local account = JAZZ_MERC_EnsureAccount()
	local due = account and tonumber(account.balance) or 0
	if due <= 0 then
		return false
	end
	local title, body
	if kind == "eve" then
		title = T(890000000009949, "M.E.R.C. — they leave tomorrow")
		body = T{
			890000000009950,
			"Speck: $<balance> still unpaid. Hired MERC contractors leave tomorrow.",
			balance = due,
		}
	else
		title = T(890000000009947, "M.E.R.C. — settle the account")
		body = T{
			890000000009948,
			"Speck: your M.E.R.C. account shows $<balance>. All hired MERC contractors leave in 3 days if you do not pay.",
			balance = due,
		}
	end
	rawset(_G, "g_JAZZ_MERC_DebtPopupOpen", true)
	createThread(function()
		local result = waitChoice(lPopupParent(), {
			translate = true,
			title = title,
			text = body,
			choice1 = T(890000000009919, "Pay Account"),
			choice1_gamepad_shortcut = "ButtonA",
			choice1_state_func = function()
				local can = rawget(_G, "JAZZ_MERC_CanPayAccount")
				if type(can) == "function" and can() then
					return "enabled"
				end
				return "disabled"
			end,
			choice2 = T(890000000009951, "Later"),
			choice2_gamepad_shortcut = "ButtonB",
		})
		rawset(_G, "g_JAZZ_MERC_DebtPopupOpen", false)
		if result == 1 then
			local pay = rawget(_G, "JAZZ_MERC_PayAccount")
			if type(pay) == "function" then
				pay()
			end
		end
		JAZZ_MERC_RefreshDebtChip()
	end)
	return true
end

--- Reminder after ~7d unpaid balance; eve popup at +2d; grace +3d → quit hired MERC.
function JAZZ_MERC_TrySendReminder()
	local account = JAZZ_MERC_EnsureAccount()
	if not account then
		return false
	end
	local day = lCampaignDay()
	local balance = account.balance or 0
	if balance <= 0 then
		lClearDebtAlarm(account)
		return false
	end
	local stage = account.warning_stage or 0
	local clock = account.last_reminder_day
	if not clock then
		account.last_reminder_day = day
		JAZZ_MERC_SyncTimeline()
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
			account.reminder_popup_sent = false
			account.eve_popup_sent = false
			if JAZZ_MERC_ShowDebtPopup("reminder") then
				account.reminder_popup_sent = true
			end
			ObjModified(account)
			JAZZ_MERC_RefreshDebtChip()
			JAZZ_MERC_SyncTimeline()
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
			account.eve_popup_sent = true
			account.reminder_popup_sent = true
			ObjModified(account)
			JAZZ_MERC_RefreshDebtChip()
			JAZZ_MERC_SyncTimeline()
			return true
		end
		if day - clock >= MERC_EVE_DAYS then
			if not account.eve_popup_sent and JAZZ_MERC_ShowDebtPopup("eve") then
				account.eve_popup_sent = true
				ObjModified(account)
				JAZZ_MERC_RefreshDebtChip()
				JAZZ_MERC_SyncTimeline()
				return true
			end
			return false
		end
		if not account.reminder_popup_sent and JAZZ_MERC_ShowDebtPopup("reminder") then
			account.reminder_popup_sent = true
			ObjModified(account)
			JAZZ_MERC_RefreshDebtChip()
			JAZZ_MERC_SyncTimeline()
			return true
		end
	end
	return false
end

--- After vanilla HireMerc succeeds: refund prepaid into credit model; charge first day only.
-- AIM/AME prepaid unchanged (Affiliation ~= MERC). Extensions: refund prepaid; NewDay keeps accrual.
-- Clear MedicalPaidWhenHired: full prepaid (incl. medical) was refunded, so vanilla end-of-contract
-- deposit return would otherwise double-pay medical for MERC credit hires.
function JAZZ_MERC_OnHired(merc_id, price, days, alreadyHired)
	local ud = gv_UnitData and gv_UnitData[merc_id]
	if not lIsMERCUnit(ud) then
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
	local setFlag = rawget(_G, "SetMercStateFlag")
	if type(setFlag) == "function" then
		setFlag(merc_id, "MedicalPaidWhenHired", 0)
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
	JAZZ_MERC_RefreshDebtChip()
	JAZZ_MERC_SyncTimeline()
	return true
end

-- Vanilla sets MedicalPaidWhenHired on Available→Hired; credit refund already returned the
-- prepaid medical, so clear the flag after vanilla handlers (mod OnMsg runs later).
function OnMsg.MercHireStatusChanged(unit_data, previousState, newState)
	if not lIsMERCUnit(unit_data) then
		return
	end
	if previousState == "Available" and newState == "Hired" then
		local setFlag = rawget(_G, "SetMercStateFlag")
		if type(setFlag) == "function" and unit_data.session_id then
			setFlag(unit_data.session_id, "MedicalPaidWhenHired", 0)
		end
	end
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

function OnMsg.OpenSatelliteView()
	local delayed = rawget(_G, "DelayedCall")
	local boot = function()
		JAZZ_MERC_EnsureAccount()
		JAZZ_MERC_RefreshDebtChip()
		JAZZ_MERC_TrySendReminder()
		JAZZ_MERC_SyncTimeline()
	end
	if type(delayed) == "function" then
		delayed(0, boot)
	else
		boot()
	end
end

function OnMsg.LoadGame()
	local delayed = rawget(_G, "DelayedCall")
	local boot = function()
		JAZZ_MERC_EnsureAccount()
		JAZZ_MERC_EnsureTimelineEventDef()
		JAZZ_MERC_SyncTimeline()
	end
	if type(delayed) == "function" then
		delayed(0, boot)
	else
		boot()
	end
end
