-- MED-001: Wounded stacks are disabled, so vanilla TreatWounds would see no
-- patients. A patient still needs treatment while HP is missing or at least one
-- trauma has not yet entered the healing state.
function JazzTraumaNeedsTreatment(unit)
	if not unit then
		return false
	end
	local trauma_zones = rawget(_G, "JazzTraumaZones") or empty_table
	local get_trauma_tier = rawget(_G, "JazzGetTraumaTier")
	local trauma_is_healing = rawget(_G, "JazzTraumaIsHealing")
	for _, zone in ipairs(trauma_zones) do
		local tier = type(get_trauma_tier) == "function" and get_trauma_tier(unit, zone)
		if tier then
			local effect = unit:GetStatusEffect("Trauma" .. zone .. tier)
			if effect and (type(trauma_is_healing) ~= "function" or not trauma_is_healing(effect)) then
				return true
			end
		end
	end
	return false
end

function JazzUnitNeedsTreatWounds(unit)
	if not unit or (unit.IsDead and unit:IsDead()) then
		return false
	end
	return (unit.HitPoints or 0) < (unit.MaxHitPoints or 0)
		or JazzTraumaNeedsTreatment(unit)
end

function IsPatientReady(merc)
	return not JazzUnitNeedsTreatWounds(merc)
end

-- One synthetic treatment unit replaces the removed Wounded stack contract.
-- HP regenerates through UnitData:Tick while Patient; completing this unit marks
-- all untreated traumas as healing.
function PatientGetWoundedStacks(merc)
	return JazzUnitNeedsTreatWounds(merc) and 1 or 0
end

function PatientGetWoundsBeingTreated(merc)
	if not IsPatient(merc) then
		return PatientGetWoundedStacks(merc)
	end
	return (merc.wounds_being_treated and merc.wounds_being_treated > 0)
		and merc.wounds_being_treated or PatientGetWoundedStacks(merc)
end

local function JazzInstallTreatWoundsEligibility()
	local operations = rawget(_G, "SectorOperations")
	local operation = operations and operations.TreatWounds
	if not operation then
		return
	end
	operation.FilterAvailable = function(self, merc, profession)
		if profession == "Patient" then
			return JazzUnitNeedsTreatWounds(merc)
		end
		return not self.min_requirement_stat
			or merc[self.min_requirement_stat] >= self.min_requirement_stat_value
	end
	operation.IsEnabled = function(self, sector)
		local mercs_available = GetAvailableMercs(sector, self, "Doctor")
		local mercs_current = GetOperationProfessionals(sector.Id, "Doctor")
		if #mercs_available == 0 and #mercs_current == 0 then
			return false, T(449205258912, "No doctors available")
		end

		local wounded, wounded_unavailable
		local unit_data = rawget(_G, "gv_UnitData") or empty_table
		for _, id in ipairs(GetPlayerMercsInSector(sector.Id)) do
			local unit = unit_data[id]
			if JazzUnitNeedsTreatWounds(unit) then
				if unit.Operation == "Idle" then
					wounded = true
				else
					wounded_unavailable = true
				end
			end
		end
		if not wounded and wounded_unavailable then
			return false, T(457589824008, "Wounded mercs are busy with another operation")
		elseif not wounded then
			return false, T(709401245024, "No wounded mercs")
		end
		return true
	end
end

function OnMsg.DataLoaded()
	JazzInstallTreatWoundsEligibility()
end

function OnMsg.ModsReloaded()
	JazzInstallTreatWoundsEligibility()
end

function PatientAddHealWoundProgress(merc, progress, max_progress, dont_log)
	if IsGameRuleActive("ForgivingMode") then 
		-- Boost resting/traveling and R&R heal speed by 25%. 
		local boost = GameRuleDefs.ForgivingMode:ResolveValue("HealingProgressBoost") or 0
		progress = MulDivRound(progress, 100 + boost, 100)
	end
	merc.heal_wound_progress = merc.heal_wound_progress + progress
	local wounds_healed = false
	while merc.heal_wound_progress > max_progress do
		merc:RemoveStatusEffect("Wounded", 1, merc.Operation)
		merc:RemoveStatusEffect("Inaccurate", 1, merc.Operation)
		merc:RemoveStatusEffect("Slowed", 1, merc.Operation)
		merc:RemoveStatusEffect("Bleeding", 1, merc.Operation)
		merc:RemoveStatusEffect("BleedingMedium", 1, merc.Operation)
		merc:RemoveStatusEffect("BleedingHeavy", 1, merc.Operation)
		merc.wounds_being_treated = merc.wounds_being_treated - 1
		if merc.wounds_being_treated>0 then
			local effect = merc:GetStatusEffect("Wounded") 
			merc.wounds_being_treated = Min(merc.wounds_being_treated, effect and effect.stacks or 0)
		end
		merc.heal_wound_progress = merc.heal_wound_progress - max_progress
		wounds_healed = true
	end
	-- MED-001: field operation starts trauma healing (does not clear Trauma*).
	-- HealWounds script effect does not mark healing — only OperationHeal / TreatWounds.
	local mark_healing = rawget(_G, "JazzMarkUnitTraumasHealing")
	if wounds_healed and type(mark_healing) == "function" then
		mark_healing(merc)
	end
	if wounds_healed and not dont_log then
		if merc.OperationProfession ~= "Doctor" then
			local context = {merc = merc}
			if merc.Operation ~= "TreatWounds" or
				(merc.Operation == "TreatWounds" and TreatWoundsTimeLeft(context,merc.operation) > 0) then
				PlayVoiceResponse(merc, "HealReceivedSatView")
			end
		end
	end
	if IsPatientReady(merc) then
		if merc.heal_wound_progress > 0 then
			merc:SetTired(Min(merc.Tiredness, const.utNormal))
		end
		merc.heal_wound_progress = 0
		merc.wounds_being_treated = 0
		if type(mark_healing) == "function" then
			mark_healing(merc)
		end
	elseif wounds_healed and not dont_log then
		CombatLog("short", T{394097034872, "<merc_name> was <em>cured of a wound</em>.", merc_name = merc.Nick})
	end
end