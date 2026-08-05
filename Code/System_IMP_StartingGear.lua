-- JAZZ-IMP-001: JA2-style IMP starting gear from final stats/perks.
-- Called from CreateImpMercData after stats + status effects are applied.

local function JazzImpStat(unit, stat)
	return (unit and unit[stat]) or 0
end

local function JazzImpHas(unit, perk)
	return unit and HasPerk(unit, perk)
end

local function JazzImpAdd(items, class, amount)
	if not class or not g_Classes[class] then
		return
	end
	amount = amount or 1
	local item = PlaceInventoryItem(class)
	if not item then
		return
	end
	if IsKindOf(item, "InventoryStack") and amount > 1 then
		item.Amount = amount
	end
	items[#items + 1] = item
	-- Extra stacks for non-stackable multiples
	if not IsKindOf(item, "InventoryStack") and amount > 1 then
		for _ = 2, amount do
			local extra = PlaceInventoryItem(class)
			if extra then
				items[#items + 1] = extra
			end
		end
	end
end

local function JazzImpPickStartingAmmoId(caliber)
	local ammos = GetAmmosWithCaliber(caliber, "sort")
	if not ammos or not ammos[1] then
		return false
	end
	-- Prefer FMJ / standard over surplus "LOT" junk when present.
	for _, def in ipairs(ammos) do
		local id = def.id or ""
		if id:find("FMJ", 1, true) or id:find("_AP", 1, true) then
			return id
		end
	end
	for _, def in ipairs(ammos) do
		local id = def.id or ""
		if not id:find("LOT", 1, true) and not id:find("Match", 1, true) then
			return id
		end
	end
	return ammos[1].id
end

local function JazzImpAddSpareAmmo(items, weapon)
	if not IsKindOf(weapon, "Firearm") then
		return
	end
	local ammoId = JazzImpPickStartingAmmoId(weapon.Caliber)
	if not ammoId then
		return
	end
	local ammo = PlaceInventoryItem(ammoId)
	if not ammo then
		return
	end
	local mag = weapon.MagazineSize or 30
	-- Magazines in gun are filled separately via clone reload; spare stays intact.
	ammo.Amount = Max(mag * 4, 60)
	if ammo.MaxStacks and ammo.Amount > ammo.MaxStacks then
		ammo.Amount = ammo.MaxStacks
	end
	items[#items + 1] = ammo
end

local function JazzImpPickMarkLadder(mark, low, mid, high)
	if mark >= 85 then
		return high
	elseif mark >= 70 then
		return mid
	elseif mark >= 50 then
		return low
	end
	return false
end

--- Build starting item list for an IMP UnitData after quiz stats/perks are applied.
function JazzBuildImpStartingGear(unit)
	local items = {}
	if not unit then
		return items
	end

	local mark = JazzImpStat(unit, "Marksmanship")
	local health = JazzImpStat(unit, "Health")
	local agi = JazzImpStat(unit, "Agility")
	local dex = JazzImpStat(unit, "Dexterity")
	local str = JazzImpStat(unit, "Strength")
	local ldr = JazzImpStat(unit, "Leadership")
	local mech = JazzImpStat(unit, "Mechanical")
	local expl = JazzImpStat(unit, "Explosives")
	local med = JazzImpStat(unit, "Medical")

	local hasAuto = JazzImpHas(unit, "AutoWeapons")
	local hasHeavy = JazzImpHas(unit, "HeavyWeaponsTraining")
	local hasStealthy = JazzImpHas(unit, "Stealthy")
	local hasMelee = JazzImpHas(unit, "MeleeTraining")
	local lmgPath = hasHeavy and hasAuto and str >= 80

	-- Primary (Stealthy > LMG Mark≥60 > AutoWeapons ladder > Mark ladder)
	local primaryId = false
	if hasStealthy then
		primaryId = "MP5SD"
	elseif lmgPath and mark >= 80 then
		primaryId = "RPD"
	elseif lmgPath and mark >= 60 then
		primaryId = "BAR"
	elseif hasAuto then
		primaryId = JazzImpPickMarkLadder(mark, "MPL", "TMP", "CAR15")
	else
		primaryId = JazzImpPickMarkLadder(mark, "TT33", "R870", "SKS")
	end
	if primaryId then
		JazzImpAdd(items, primaryId)
	end

	-- Secondary: M79 on heavy paths
	local giveM79 = hasHeavy
	if giveM79 then
		JazzImpAdd(items, "M79")
		JazzImpAdd(items, "JAZZ_AMMO_40mmFlashbangGrenade", 2)
		JazzImpAdd(items, "JAZZ_AMMO_40mmFragGrenade", 3)
	end

	-- Melee/CQC sidearm ladder
	if hasMelee then
		local side = JazzImpPickMarkLadder(mark, "APS", "MicroUZI", "Glock17")
		if side then
			JazzImpAdd(items, side)
		end
	end

	-- Armor (Health). Stealthy → Zylon; otherwise Flak vest by Health.
	-- Helm/legs at 70+: M1 + leather pants (not vanilla Kevlar/FlakLeggings).
	if hasStealthy then
		JazzImpAdd(items, "JazzArmor_ZylonLight")
	elseif health >= 60 then
		JazzImpAdd(items, "JazzArmor_FlakM1955")
	end
	if health >= 70 then
		JazzImpAdd(items, "JazzArmor_M1Helm")
		JazzImpAdd(items, "JazzArmor_LeatherPants")
	end

	-- Agility flares
	if agi >= 80 then
		JazzImpAdd(items, "FlareStick", 4)
	elseif agi >= 70 then
		JazzImpAdd(items, "FlareStick", 2)
	end

	-- Dexterity knives
	if dex >= 80 then
		JazzImpAdd(items, "Knife_Balanced", 3)
	elseif dex >= 70 then
		JazzImpAdd(items, "Knife")
	end

	-- Strength grenades + crowbar
	if str >= 70 then
		JazzImpAdd(items, "FragGrenade", 2)
	end
	if str >= 80 then
		JazzImpAdd(items, "Crowbar")
	end

	-- Leadership journals
	if ldr >= 80 then
		JazzImpAdd(items, "SkillMag_Leadership", 3)
	end

	-- Mechanical
	if mech >= 40 then
		JazzImpAdd(items, "Wirecutter")
	end
	if mech >= 60 then
		JazzImpAdd(items, "Lockpick")
	end
	if mech >= 80 then
		JazzImpAdd(items, "Parts", 100)
	end

	-- Explosives
	if expl >= 80 then
		JazzImpAdd(items, "TNT", 2)
	elseif expl >= 50 then
		JazzImpAdd(items, "PipeBomb", 2)
	end

	-- Medical
	if med >= 60 then
		JazzImpAdd(items, "Medkit")
		if med >= 80 then
			JazzImpAdd(items, "Meds", 100)
		end
	elseif med >= 30 then
		JazzImpAdd(items, "FirstAidKit")
	end

	-- Personality quirks
	if JazzImpHas(unit, "Psycho") then
		JazzImpAdd(items, "Molotov", 2)
	end
	if JazzImpHas(unit, "Negotiator") then
		JazzImpAdd(items, "SmokeGrenade", 2)
	end
	if JazzImpHas(unit, "Scoundrel") then
		JazzImpAdd(items, "ConcussiveGrenade", 2)
	end

	-- Specialization skills
	if JazzImpHas(unit, "MartialArts") then
		JazzImpAdd(items, "Knife_Balanced", 2)
	end
	if JazzImpHas(unit, "CQCTraining") then
		JazzImpAdd(items, "Machete")
	end
	if JazzImpHas(unit, "MrFixit") then
		JazzImpAdd(items, "Parts", 100)
	end
	if JazzImpHas(unit, "NightOps") then
		JazzImpAdd(items, "FlareStick", 3)
	end
	if JazzImpHas(unit, "Teacher") then
		JazzImpAdd(items, "SkillMag_Wisdom")
		JazzImpAdd(items, "SkillMag_Mechanical")
		JazzImpAdd(items, "SkillMag_Medical")
	end
	if JazzImpHas(unit, "Throwing") then
		JazzImpAdd(items, "FragGrenade", 2)
	end

	-- Spare ammo for firearms already placed
	local placed = {}
	for _, item in ipairs(items) do
		if IsKindOf(item, "Firearm") and not placed[item.class] then
			placed[item.class] = true
			JazzImpAddSpareAmmo(items, item)
		end
	end

	return items
end

function JazzClearUnitInventory(unit)
	if not unit then
		return
	end
	-- Collect first — RemoveItem during ForEachItem can skip slots.
	local doomed = {}
	unit:ForEachItem(function(item, slot_name)
		doomed[#doomed + 1] = { item = item, slot = slot_name }
	end)
	for _, entry in ipairs(doomed) do
		unit:RemoveItem(entry.slot, entry.item)
		DoneObject(entry.item)
	end
end

function JazzApplyImpStartingGear(unit)
	if not unit then
		return
	end
	JazzClearUnitInventory(unit)
	local items = JazzBuildImpStartingGear(unit)
	unit:EquipStartingGear(items)
end
