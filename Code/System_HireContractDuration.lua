-- Raise AIM/AME merc-chat contract MaxDuration 14 → 30 (owner playtest).
-- Vanilla AIMHiringScreen lNextNodeMap hardcodes MaxDuration = 14; duration-refusal
-- paths that set MaxDuration = 7 are left alone. AME market tick (AME_TICK_DAYS = 14)
-- is unrelated — AME hire uses the same StartMercChat / GetNextMercConversation path as AIM.
--
-- Also stretch GetMercDurationDiscountPercent maxDay 14 → 30 so long contracts keep the
-- duration discount (vanilla returns 0% for days > 14, which made 15–30 worse than 14).

g_JAZZ_GetNextMercConversationBase = rawget(_G, "g_JAZZ_GetNextMercConversationBase") or false
g_JAZZ_HireContractDurationFn = rawget(_G, "g_JAZZ_HireContractDurationFn") or false
g_JAZZ_PDAMessengerSetupUIBase = rawget(_G, "g_JAZZ_PDAMessengerSetupUIBase") or false
g_JAZZ_HireSetupUIFn = rawget(_G, "g_JAZZ_HireSetupUIFn") or false
g_JAZZ_GetMercDurationDiscountPercentBase = rawget(_G, "g_JAZZ_GetMercDurationDiscountPercentBase") or false
g_JAZZ_HireDurationDiscountFn = rawget(_G, "g_JAZZ_HireDurationDiscountFn") or false

local JAZZ_HIRE_MAX_DURATION = 30
local VANILLA_HIRE_MAX_DURATION = 14

local function lRaiseMaxHireDuration(ctx)
	if type(ctx) ~= "table" then
		return
	end
	if ctx.MaxDuration == VANILLA_HIRE_MAX_DURATION then
		ctx.MaxDuration = JAZZ_HIRE_MAX_DURATION
	end
end

local function lInstallGetNextMercConversationWrap()
	local ourFn = rawget(_G, "g_JAZZ_HireContractDurationFn")
	local current = rawget(_G, "GetNextMercConversation")
	if type(current) ~= "function" then
		return false
	end
	if ourFn and current == ourFn then
		return true
	end
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_GetNextMercConversationBase", current)
	elseif not rawget(_G, "g_JAZZ_GetNextMercConversationBase") then
		return false
	end
	local function wrap(merc, ctx, currentConv)
		local preset, input, nextNode = g_JAZZ_GetNextMercConversationBase(merc, ctx, currentConv)
		lRaiseMaxHireDuration(ctx)
		return preset, input, nextNode
	end
	rawset(_G, "g_JAZZ_HireContractDurationFn", wrap)
	rawset(_G, "GetNextMercConversation", wrap)
	return true
end

-- Resume path restores conversation_context without calling GetNextMercConversation;
-- raise MaxDuration before the duration slider reads context (covers AIM + AME).
local function lInstallSetupUIForChatWrap()
	if not rawget(_G, "PDAMessengerClass") or type(PDAMessengerClass.SetupUIForChat) ~= "function" then
		return false
	end
	local ourFn = rawget(_G, "g_JAZZ_HireSetupUIFn")
	if ourFn and PDAMessengerClass.SetupUIForChat == ourFn then
		return true
	end
	local current = PDAMessengerClass.SetupUIForChat
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_PDAMessengerSetupUIBase", current)
	elseif not rawget(_G, "g_JAZZ_PDAMessengerSetupUIBase") then
		return false
	end
	local base = g_JAZZ_PDAMessengerSetupUIBase
	local function wrap(self, hide)
		lRaiseMaxHireDuration(self.conversation_context)
		return base(self, hide)
	end
	rawset(_G, "g_JAZZ_HireSetupUIFn", wrap)
	PDAMessengerClass.SetupUIForChat = wrap
	return true
end

-- Vanilla Mercenary.lua: linear discount 3–14 (normal →25%) / 7–14 (long only →35%);
-- days outside the window → 0%. Stretch maxDay to JAZZ_HIRE_MAX_DURATION.
local function lInstallDurationDiscountWrap()
	local ourFn = rawget(_G, "g_JAZZ_HireDurationDiscountFn")
	local current = rawget(_G, "GetMercDurationDiscountPercent")
	if type(current) ~= "function" then
		return false
	end
	if ourFn and current == ourFn then
		return true
	end
	if current ~= ourFn then
		rawset(_G, "g_JAZZ_GetMercDurationDiscountPercentBase", current)
	elseif not rawget(_G, "g_JAZZ_GetMercDurationDiscountPercentBase") then
		return false
	end
	local function wrap(merc, duration)
		local discount = merc and merc:GetProperty("DurationDiscount")
		if discount == "none" then
			return 0
		end
		local minDay, minDiscount, maxDay, maxDiscount = 0, 0, 0, 0
		if discount == "normal" then
			minDay = 3
			minDiscount = 0
			maxDay = JAZZ_HIRE_MAX_DURATION
			maxDiscount = 25
		elseif discount == "long only" then
			minDay = 7
			minDiscount = 0
			maxDay = JAZZ_HIRE_MAX_DURATION
			maxDiscount = 35
		end
		if duration >= minDay and duration <= maxDay then
			return minDiscount + MulDivRound(duration - minDay, (maxDiscount - minDiscount), maxDay - minDay)
		end
		return 0
	end
	rawset(_G, "g_JAZZ_HireDurationDiscountFn", wrap)
	rawset(_G, "GetMercDurationDiscountPercent", wrap)
	return true
end

local function lInstallHireContractDuration()
	lInstallGetNextMercConversationWrap()
	lInstallSetupUIForChatWrap()
	lInstallDurationDiscountWrap()
end

function OnMsg.ModsReloaded()
	lInstallHireContractDuration()
end

function OnMsg.DataLoaded()
	lInstallHireContractDuration()
end

lInstallHireContractDuration()
