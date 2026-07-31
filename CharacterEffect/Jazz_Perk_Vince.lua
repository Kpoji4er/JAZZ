UndefineClass('Jazz_Perk_Vince')
DefineClass.Jazz_Perk_Vince = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitBandaged",
			Handler = function (self, target, healer, patient, hp_restored)
				if target ~= healer or not patient or patient == healer then
					return
				end
				if healer:GetEffectValue("Jazz_Perk_Vince") then
					return
				end
				healer:SetEffectValue("Jazz_Perk_Vince", true)
				patient:GainAP(4 * const.Scale.AP)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target:SetEffectValue("Jazz_Perk_Vince", nil)
			end,
		}),
	},
	DisplayName = T(890000000005009, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vince DisplayName]] "Полевой наставник"),
	Description = T(890000000005010, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vince Description]] "Раз за бой первое лечение или перевязка союзника даёт цели +4 ОД."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Vince.png",
	Tier = "Personal",
}
