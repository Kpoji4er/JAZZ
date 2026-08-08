-- JAZZ-UNITS-006 §D Batch6: Benny decoy lure + Simon perfect shot (stubs / soft CombatAction).
-- Install from System_NamedPerks_006.lua.

g_JAZZ_NamedPerks006Batch6Wrapped = rawget(_G, "g_JAZZ_NamedPerks006Batch6Wrapped") or false

function Jazz_BennyDecoyReady(unit)
	return unit and HasPerk(unit, "Jazz_Perk_Benny") and not unit:GetEffectValue("Jazz_BennyDecoyCd")
end

function Jazz_BennyMarkDecoyUsed(unit)
	if unit and unit.SetEffectValue then
		unit:SetEffectValue("Jazz_BennyDecoyCd", true)
	end
end

-- Soft-cut full CombatAction decoy: helper for future CA. Lure prefers lowest-Will enemy ≤8.
function Jazz_BennyPickLureTarget(unit)
	if not Jazz_BennyDecoyReady(unit) then
		return false
	end
	local best, best_will
	local slab = const.SlabSizeX
	for _, enemy in ipairs(g_Units or empty_table) do
		if IsValid(enemy) and not enemy:IsDead() and unit:IsOnEnemySide(enemy) then
			if DivRound(unit:GetDist(enemy), slab) <= 8 then
				local will = enemy.WillPoints or enemy.Will or 999
				if not best or will < best_will then
					best, best_will = enemy, will
				end
			end
		end
	end
	return best
end

function Jazz_SimonHas4xOptic(unit)
	if not unit then
		return false
	end
	local w = unit.GetActiveWeapons and unit:GetActiveWeapons("Firearm")
	if not w then
		return false
	end
	local components = w.components or w.Components
	if type(components) ~= "table" then
		-- Fallback: Magnification / Scope zoom property if present.
		local zoom = w.ScopeAccuracyBonus or w.Magnification or 0
		return type(zoom) == "number" and zoom >= 4
	end
	for _, comp in pairs(components) do
		if comp then
			local id = type(comp) == "string" and comp or (comp.Id or comp.id or comp.class)
			local def = id and WeaponComponents and WeaponComponents[id]
			local mag = def and (def.Magnification or def.Zoom or def.OpticalZoom)
			if type(mag) == "number" and mag >= 4 then
				return true
			end
			if id and (string.find(tostring(id), "4x", 1, true) or string.find(tostring(id), "Scope", 1, true)) then
				-- Soft: Scope* ids count as eligible until precise mag table wired.
				if string.find(tostring(id), "4x", 1, true) or string.find(tostring(id), "8x", 1, true) or string.find(tostring(id), "10x", 1, true) then
					return true
				end
			end
		end
	end
	return false
end

function Jazz_SimonPerfectShotReady(unit)
	return unit
		and HasPerk(unit, "Jazz_Perk_Simon")
		and not unit:GetEffectValue("Jazz_SimonPerfectCd")
		and Jazz_SimonHas4xOptic(unit)
end

function Jazz_SimonMarkPerfectUsed(unit)
	if unit and unit.SetEffectValue then
		unit:SetEffectValue("Jazz_SimonPerfectCd", true)
	end
end

function Jazz_SimonOnKillCharge(attacker, results, target)
	if not attacker or not HasPerk(attacker, "Jazz_Perk_Simon") then
		return
	end
	local killed = false
	if results and results.killed_units then
		for _, u in ipairs(results.killed_units) do
			if IsValid(u) then
				killed = true
				break
			end
		end
	end
	if not killed and IsKindOf(target, "Unit") and target:IsDead() then
		killed = true
	end
	if killed and attacker.SetEffectValue then
		attacker:SetEffectValue("Jazz_SimonPerfectCd", nil)
	end
end

function Jazz_InstallNamedPerks006Batch6()
	if rawget(_G, "g_JAZZ_NamedPerks006Batch6Wrapped") then
		return
	end
	-- Soft-cut: no CombatAction registration yet; CE + StartingPerks + helpers above.
	rawset(_G, "g_JAZZ_NamedPerks006Batch6Wrapped", true)
end

function Jazz_NamedPerks006Batch6OnCombatStart()
	for _, u in ipairs(g_Units or empty_table) do
		if IsValid(u) and u.SetEffectValue then
			u:SetEffectValue("Jazz_BennyDecoyCd", nil)
			-- Simon starts charged (no CD) each combat; CD set after use until kill.
			u:SetEffectValue("Jazz_SimonPerfectCd", nil)
		end
	end
end
