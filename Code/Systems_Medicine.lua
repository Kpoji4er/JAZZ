-- JAZZ-MED-001.  The helpers here are intentionally global: generated
-- CharacterEffect and CombatAction definitions call them after reload.
JazzBleedTierOrder = { "BleedingHeavy", "BleedingMedium", "Bleeding" }

local JazzBleedDamage = {
	Bleeding = 3,
	BleedingMedium = 6,
	BleedingHeavy = 12,
}

local function lBleedStacks(unit, id)
	local effect = unit and unit:GetStatusEffect(id)
	return effect and effect.stacks or 0
end

local function lHasSquadMedic(unit)
	local squad_id = unit and unit.Squad
	local squad = squad_id and gv_Squads and gv_Squads[squad_id]
	for _, member_id in ipairs(squad and squad.units or empty_table) do
		local member = g_Units and g_Units[member_id]
		if member and (member.Medical or 0) >= 70 then
			return true
		end
	end
	return false
end

function JazzIsExpandingAmmo(ammo)
	if not ammo then
		return false
	end
	local class_id = tostring(ammo.class or ammo.id or "")
	if string.find(string.upper(class_id), "JHP", 1, true) then
		return true
	end
	if ammo.colorStyle == "AmmoJHPColor" then
		return true
	end
	for _, effect in ipairs(ammo.AppliedEffects or empty_table) do
		if effect == "BleedingHeavy" then
			return true
		end
	end
	return false
end

function JazzUnitBleedDamagePerTurn(unit)
	local total = 0
	for id, damage in pairs(JazzBleedDamage) do
		total = total + lBleedStacks(unit, id) * damage
	end
	return Min(30, total)
end

function JazzBleedDealTurnDamage(unit)
	if not unit or unit:HasStatusEffect("BeingBandaged") then
		return 0
	end
	local damage = JazzUnitBleedDamagePerTurn(unit)
	if damage <= 0 then
		return 0
	end
	local floating_text = T{193053798048, "<num> (bleeding)", num = damage}
	local visible = HasVisibilityTo(GetPoVTeam(), unit)
	local log_msg = T{890000000000971, "<name> takes <em><num></em> bleeding damage", name = unit:GetLogName(), num = damage}
	unit:TakeDirectDamage(damage, visible and floating_text or false, "short", log_msg)
	return damage
end

function JazzBleedTransitionRoll(unit)
	if not unit or unit:HasStatusEffect("BeingBandaged") then
		return false
	end
	local medic_bias = lHasSquadMedic(unit) and 10 or 0
	for _, id in ipairs(JazzBleedTierOrder) do
		local stacks = lBleedStacks(unit, id)
		for _ = 1, stacks do
			local roll = unit:Random(100)
			if id == "Bleeding" then
				if roll < 70 + medic_bias then
					unit:RemoveStatusEffect("Bleeding", 1)
				elseif roll >= 85 + medic_bias then
					unit:RemoveStatusEffect("Bleeding", 1)
					unit:AddStatusEffect("BleedingMedium")
				end
			elseif id == "BleedingMedium" then
				if roll < 35 + medic_bias then
					unit:RemoveStatusEffect("BleedingMedium", 1)
					unit:AddStatusEffect("Bleeding")
				elseif roll >= 80 + medic_bias then
					unit:RemoveStatusEffect("BleedingMedium", 1)
					unit:AddStatusEffect("BleedingHeavy")
				end
			elseif roll < 15 + medic_bias then
				unit:RemoveStatusEffect("BleedingHeavy", 1)
				unit:AddStatusEffect("BleedingMedium")
			end
		end
	end
	return true
end

function JazzReduceBleedOneTier(patient)
	if not patient then
		return false
	end
	for _, id in ipairs(JazzBleedTierOrder) do
		if lBleedStacks(patient, id) > 0 then
			patient:RemoveStatusEffect(id, 1)
			if id == "BleedingHeavy" then
				patient:AddStatusEffect("BleedingMedium")
			elseif id == "BleedingMedium" then
				patient:AddStatusEffect("Bleeding")
			end
			return true
		end
	end
	return false
end

function JazzClearBleedStrong(patient, max_tiers_or_stacks)
	if not patient then
		return false
	end
	local remaining = max_tiers_or_stacks or 1
	local changed = false
	while remaining > 0 do
		local removed = false
		for _, id in ipairs(JazzBleedTierOrder) do
			if lBleedStacks(patient, id) > 0 then
				patient:RemoveStatusEffect(id, 1)
				removed = true
				changed = true
				break
			end
		end
		if not removed then
			break
		end
		remaining = remaining - 1
	end
	return changed
end

function JazzHasAnyBleed(unit)
	for _, id in ipairs(JazzBleedTierOrder) do
		if lBleedStacks(unit, id) > 0 then
			return true
		end
	end
	return false
end

function JazzTryRollBleedFromHit(target, hit, attacker)
	if not target or not hit or hit.setpiece then
		return false
	end
	local armor_hit = hit.armor_decay and next(hit.armor_decay) ~= nil
	local pierced = not armor_hit or hit.armor_pen and next(hit.armor_pen) ~= nil
	if not pierced then
		return false
	end
	local trauma_bias = JazzHasAnyTrauma(target) and 15 or 0
	local roll = target:Random(100)
	if roll < 10 + trauma_bias then
		target:AddStatusEffect("BleedingMedium")
		return true
	elseif roll < 55 + trauma_bias then
		target:AddStatusEffect("Bleeding")
		return true
	end
	return false
end

function JazzRemapHitBleedEffect(effect, hit, attacker)
	if effect ~= "Bleeding" then
		return effect
	end
	local weapon = hit and hit.weapon
	local ammo = weapon and weapon.ammo
	return JazzIsExpandingAmmo(ammo) and "BleedingHeavy" or effect
end

function JazzFindInventoryItem(unit, class_id)
	local result
	if unit then
		unit:ForEachItem(function(item)
			if not result and (item.class == class_id or item.id == class_id) then
				result = item
			end
		end)
	end
	return result
end

function JazzConsumeInventoryItem(unit, class_id, amount)
	local item = JazzFindInventoryItem(unit, class_id)
	if not item then
		return false
	end
	amount = amount or 1
	if item.Amount and item.Amount > amount then
		item.Amount = item.Amount - amount
	else
		local slot = unit:GetItemSlot(item)
		if slot then
			unit:RemoveItem(slot, item)
		end
	end
	Msg("InventoryChange", unit)
	return true
end

function JazzGetBandageItem(unit)
	return JazzFindInventoryItem(unit, "JAZZ_Bandage")
end

function JazzGetMorphineItem(unit)
	return JazzFindInventoryItem(unit, "JAZZ_Morphine")
end

function JazzApplyBandageAction(healer, patient)
	if not healer or not patient or not JazzGetBandageItem(healer) then
		return false
	end
	if not JazzReduceBleedOneTier(patient) then
		return false
	end
	JazzConsumeInventoryItem(healer, "JAZZ_Bandage", 1)
	Msg("OnBandaged", healer, patient, 0)
	return true
end

function JazzApplyMorphineAction(healer, patient)
	if not healer or not patient or not JazzGetMorphineItem(healer) then
		return false
	end
	patient:AddStatusEffect("Analgesia")
	JazzConsumeInventoryItem(healer, "JAZZ_Morphine", 1)
	Msg("JAZZ_MorphineApplied", healer, patient)
	return true
end

-- Called from Bleeding* CharacterEffect OnEndTurn (deduped per unit/turn).
function JazzBleedOnUnitEndTurn(unit)
	if not unit or not JazzHasAnyBleed(unit) then
		return
	end
	local key = (g_Combat and g_Combat.current_turn) or (GameTime and GameTime()) or 0
	if unit.jazz_bleed_tick_key == key then
		return
	end
	unit.jazz_bleed_tick_key = key
	JazzBleedDealTurnDamage(unit)
	JazzBleedTransitionRoll(unit)
end

-- ---------------------------------------------------------------------------
-- Zonal traumas (MED-001 expanded). Eye folded into Head for v1.
-- ---------------------------------------------------------------------------
JazzTraumaZones = { "Arms", "Legs", "Ribs", "Head", "Burn" }
JazzTraumaTiers = { "Light", "Medium", "Heavy" }
JazzTraumaTierRank = { Light = 1, Medium = 2, Heavy = 3 }

local function lTraumaId(zone, tier)
	return "Trauma" .. zone .. tier
end

function JazzTraumaEffectId(zone, tier)
	return lTraumaId(zone, tier)
end

function JazzGetTraumaTier(unit, zone)
	if not unit or not zone then
		return false
	end
	for _, tier in ipairs(JazzTraumaTiers) do
		if unit:HasStatusEffect(lTraumaId(zone, tier)) then
			return tier
		end
	end
	return false
end

function JazzHasAnyTrauma(unit)
	if not unit then
		return false
	end
	for _, zone in ipairs(JazzTraumaZones) do
		if JazzGetTraumaTier(unit, zone) then
			return true
		end
	end
	return false
end

function JazzClearZoneTrauma(unit, zone)
	if not unit or not zone then
		return false
	end
	local changed = false
	for _, tier in ipairs(JazzTraumaTiers) do
		local id = lTraumaId(zone, tier)
		if unit:HasStatusEffect(id) then
			unit:RemoveStatusEffect(id, "all")
			changed = true
		end
	end
	return changed
end

-- Apply or upgrade trauma for a zone. Never downgrades.
function JazzApplyTrauma(unit, zone, tier)
	if not unit or not zone or not tier or not JazzTraumaTierRank[tier] then
		return false
	end
	local current = JazzGetTraumaTier(unit, zone)
	if current and JazzTraumaTierRank[current] >= JazzTraumaTierRank[tier] then
		return false
	end
	JazzClearZoneTrauma(unit, zone)
	unit:AddStatusEffect(lTraumaId(zone, tier))
	Msg("JAZZ_TraumaApplied", unit, zone, tier)
	return true
end

-- Body-part *shot rollers → trauma. Grit (Temp HP) still softens like legacy *shot.
-- Head biases toward Medium/Heavy; other zones mostly Light.
function JazzTryRollTraumaFromBodyPart(unit, zone)
	if not unit or not zone or (unit.TempHitPoints or 0) > 0 then
		return false
	end
	local hp = (unit.TempHitPoints or 0) + (unit.HitPoints or 0)
	if hp <= 0 then
		hp = 1
	end
	local roll = unit:Random(hp)
	local tier
	if zone == "Head" then
		if roll < 8 then
			tier = "Heavy"
		elseif roll < 28 then
			tier = "Medium"
		elseif roll < 50 then
			tier = "Light"
		end
	else
		if roll < 4 then
			tier = "Heavy"
		elseif roll < 18 then
			tier = "Medium"
		elseif roll < 45 then
			tier = "Light"
		end
	end
	if not tier then
		return false
	end
	return JazzApplyTrauma(unit, zone, tier)
end

-- Knockout / Unconscious: one heavy trauma + Pain spike (not Wounded stacks).
function JazzApplyKnockoutTraumaPackage(unit)
	if not unit then
		return false
	end
	local zones = { "Arms", "Legs", "Ribs", "Head" }
	local zone = zones[1 + unit:Random(#zones)]
	JazzApplyTrauma(unit, zone, "Heavy")
	for _ = 1, 3 do
		unit:AddStatusEffect("Pain")
	end
	return true
end

-- Light/Medium: Pain when the injured zone is used. Deduped per unit/zone/turn.
function JazzTraumaPainOnZoneUse(unit, zone)
	if not unit or not zone then
		return false
	end
	local tier = JazzGetTraumaTier(unit, zone)
	if not tier or tier == "Heavy" then
		-- Heavy ramps Pain on EndTurn instead.
		return false
	end
	local key = tostring(zone) .. "|" .. tostring((g_Combat and g_Combat.current_turn) or (GameTime and GameTime()) or 0)
	unit.jazz_trauma_pain_keys = unit.jazz_trauma_pain_keys or {}
	if unit.jazz_trauma_pain_keys[key] then
		return false
	end
	unit.jazz_trauma_pain_keys[key] = true
	unit:AddStatusEffect("Pain")
	return true
end

-- Heavy traumas: Pain climbs toward Pain.max_stacks each EndTurn.
function JazzTraumaHeavyPainRamp(unit)
	if not unit then
		return
	end
	local key = (g_Combat and g_Combat.current_turn) or (GameTime and GameTime()) or 0
	if unit.jazz_trauma_heavy_pain_key == key then
		return
	end
	local has_heavy = false
	for _, zone in ipairs(JazzTraumaZones) do
		if JazzGetTraumaTier(unit, zone) == "Heavy" then
			has_heavy = true
			break
		end
	end
	if not has_heavy then
		return
	end
	unit.jazz_trauma_heavy_pain_key = key
	local pain = unit:GetStatusEffect("Pain")
	local stacks = pain and pain.stacks or 0
	local max_stacks = (CharacterEffectDefs.Pain and CharacterEffectDefs.Pain.max_stacks) or 8
	if stacks < max_stacks then
		unit:AddStatusEffect("Pain")
	end
end

function JazzTraumaBlockFreeMove(unit)
	return unit and (
		JazzGetTraumaTier(unit, "Legs") == "Medium"
		or JazzGetTraumaTier(unit, "Legs") == "Heavy"
		or JazzGetTraumaTier(unit, "Ribs") == "Medium"
		or JazzGetTraumaTier(unit, "Ribs") == "Heavy"
	)
end

-- After Burning expires: leave a lasting light burn trauma (debt).
function JazzApplyBurnTraumaFromBurning(unit)
	if not unit then
		return false
	end
	return JazzApplyTrauma(unit, "Burn", "Light")
end
