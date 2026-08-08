UndefineClass('Jazz_Perk_Laura')
DefineClass.Jazz_Perk_Laura = {
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
				healer:AddStatusEffect("Jazz_CombatMedicBuff")
			end,
		}),
	},
	DisplayName = T(890000000005045, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Laura DisplayName]] "Боевой медик"),
	Description = T(890000000005046, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Laura Description]] "После лечения союзника Лора получает +15 к шансу попадания и критическому удару до конца следующего хода."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Laura.png",
	Tier = "Personal",
}
