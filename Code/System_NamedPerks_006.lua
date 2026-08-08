-- JAZZ-UNITS-006 §A (+ shared helpers for Nervous stack / Lucky / Dynamo / Vince / Mike / Blade Brutalize)
-- Loc exclusive note: 6300-6499 occupied by VR; new CE text uses free 6218+ and existing perk IDs.

g_JAZZ_NamedPerks006Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Wrapped") or false

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

OnMsg.ModsReloaded = lInstallNamedPerks006
OnMsg.DataLoaded = lInstallNamedPerks006
OnMsg.NewGame = lInstallNamedPerks006
OnMsg.LoadGame = lInstallNamedPerks006
