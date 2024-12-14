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
		merc.wounds_being_treated = merc.wounds_being_treated - 1
		if merc.wounds_being_treated>0 then
			local effect = merc:GetStatusEffect("Wounded") 
			merc.wounds_being_treated = Min(merc.wounds_being_treated, effect and effect.stacks or 0)
		end
		merc.heal_wound_progress = merc.heal_wound_progress - max_progress
		wounds_healed = true
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
	elseif wounds_healed and not dont_log then
		CombatLog("short", T{394097034872, "<merc_name> was <em>cured of a wound</em>.", merc_name = merc.Nick})
	end
end