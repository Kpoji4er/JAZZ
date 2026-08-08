-- JAZZ-UNITS-006 §A + §C Batch2 (Grizzly G1, JackOfAll ops, Steroid melee CTH, …)
-- Loc exclusive note: 6300-6499 occupied by VR; batch2 CE text uses 6500+.

g_JAZZ_NamedPerks006Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Wrapped") or false
g_JAZZ_NamedPerks006Batch2Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Batch2Wrapped") or false
g_JAZZ_JackOfAllOpsBase = rawget(_G, "g_JAZZ_JackOfAllOpsBase") or false

local function lHas(unit, perk)
	return unit and HasPerk(unit, perk)
end

function Jazz_NervousGetBonusShots(unit)
	if not unit then
		return 0
	end
	return Clamp(tonumber(unit:GetEffectValue("Jazz_NervousBonusShots")) or 0, 0, 10)
end

function Jazz_NervousAddHitStack(unit, hits)
	if not lHas(unit, "Jazz_Perk_Nervous") then
		return
	end
	hits = hits or 1
	local cur = Jazz_NervousGetBonusShots(unit)
	unit:SetEffectValue("Jazz_NervousBonusShots", Clamp(cur + hits, 0, 10))
end

function Jazz_NervousConsumeBonus(unit)
	if not unit then
		return
	end
	unit:SetEffectValue("Jazz_NervousBonusShots", nil)
end

function Jazz_SquadHasVince(unit)
	if not unit or not unit.team then
		return false
	end
	for _, u in ipairs(unit.team.units or empty_table) do
		if IsValid(u) and not u:IsDead() and HasPerk(u, "Jazz_Perk_Vince") then
			return true
		end
	end
	return false
end

-- Probabilistic −25% med consume: 25% chance to skip one charge when Vince in squad.
function Jazz_VinceShouldSkipMedConsume(healer)
	if not Jazz_SquadHasVince(healer) then
		return false
	end
	return InteractionRand(100, "Jazz_Perk_Vince") < 25
end

function Jazz_MadmanDrainWill(center_unit)
	if not center_unit or not g_Combat then
		return
	end
	local slab = const.SlabSizeX
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and IsKindOf(u, "Unit") and not u:IsDead() then
			if DivRound(center_unit:GetDist(u), slab) <= 5 then
				local wp = u.WillPoints or 0
				u.WillPoints = Max(0, wp - 10)
				if u.ApplySuppressionStatus then
					u:ApplySuppressionStatus()
				end
			end
		end
	end
end

local function lInstallNamedPerks006()
	if rawget(_G, "g_JAZZ_NamedPerks006Wrapped") then
		return
	end

	-- Dynamo: skip lock traps when lockpicking / opening.
	if IsKindOf(ItemContainer, "Lockpickable") or true then
		local base_trap = ItemContainer.TriggerTrap
		if type(base_trap) == "function" then
			function ItemContainer:TriggerTrap(unit, ...)
				if unit and HasPerk(unit, "Jazz_Perk_Dynamo") then
					return
				end
				return base_trap(self, unit, ...)
			end
		end
	end

	-- Mike: +2 Overwatch attacks.
	local base_ow = Unit.GetOverwatchAttacksAndAim
	if type(base_ow) == "function" then
		function Unit:GetOverwatchAttacksAndAim(...)
			local attacks, aim = base_ow(self, ...)
			if HasPerk(self, "Jazz_Perk_Mike") and type(attacks) == "number" then
				attacks = attacks + 2
			end
			return attacks, aim
		end
	end

	rawset(_G, "g_JAZZ_NamedPerks006Wrapped", true)
end

local function lInstallNamedPerks006Batch2()
	if rawget(_G, "g_JAZZ_NamedPerks006Batch2Wrapped") then
		return
	end

	-- GrizzlyPerk signature: 2× suppression on GetActionResults (shots doubled in GetAutofireShots).
	local ca = CombatActions and CombatActions.GrizzlyPerk
	if ca and type(ca.GetActionResults) == "function" and not rawget(ca, "JazzUnits006GrizzlyWrapped") then
		local base_grizzly = ca.GetActionResults
		ca.GetActionResults = function(self, unit, args)
			args = args and table.copy(args) or {}
			local base_sup = args.suppressionbonus or 100
			args.suppressionbonus = base_sup * 2
			return base_grizzly(self, unit, args)
		end
		rawset(ca, "JazzUnits006GrizzlyWrapped", true)
	end

	-- Wolf JackOfAllTrades: −33% satellite operation time (JAZZ wrap; CE param jazz_ops_bonus is display-only).
	local base_ops = rawget(_G, "GetOperationTimeLeft")
	if type(base_ops) == "function" and not rawget(_G, "g_JAZZ_JackOfAllOpsBase") then
		rawset(_G, "g_JAZZ_JackOfAllOpsBase", base_ops)
		rawset(_G, "GetOperationTimeLeft", function(merc, operation_id, ...)
			local t = g_JAZZ_JackOfAllOpsBase(merc, operation_id, ...)
			if type(t) == "number" and merc and HasPerk(merc, "JackOfAllTrades") then
				local perk = merc.GetStatusEffect and merc:GetStatusEffect("JackOfAllTrades")
				local bonus = (perk and perk.ResolveValue and perk:ResolveValue("jazz_ops_bonus")) or 33
				t = MulDivRound(t, 100 - bonus, 100)
			end
			return t
		end)
	end

	rawset(_G, "g_JAZZ_NamedPerks006Batch2Wrapped", true)
end

OnMsg.ModsReloaded = function()
	lInstallNamedPerks006()
	lInstallNamedPerks006Batch2()
	if type(Jazz_InstallNamedPerks006Batch3) == "function" then
		Jazz_InstallNamedPerks006Batch3()
	end
end
OnMsg.DataLoaded = function()
	lInstallNamedPerks006()
	lInstallNamedPerks006Batch2()
	if type(Jazz_InstallNamedPerks006Batch3) == "function" then
		Jazz_InstallNamedPerks006Batch3()
	end
end
OnMsg.NewGame = function()
	lInstallNamedPerks006()
	lInstallNamedPerks006Batch2()
	if type(Jazz_InstallNamedPerks006Batch3) == "function" then
		Jazz_InstallNamedPerks006Batch3()
	end
end
OnMsg.LoadGame = function()
	lInstallNamedPerks006()
	lInstallNamedPerks006Batch2()
	if type(Jazz_InstallNamedPerks006Batch3) == "function" then
		Jazz_InstallNamedPerks006Batch3()
	end
end

OnMsg.CombatStart = function()
	if type(Jazz_NamedPerks006Batch3OnCombatStart) == "function" then
		Jazz_NamedPerks006Batch3OnCombatStart()
	end
end
OnMsg.TurnStart = function()
	if type(Jazz_NamedPerks006Batch3OnTurnStart) == "function" then
		Jazz_NamedPerks006Batch3OnTurnStart()
	end
end
