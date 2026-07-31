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
				healer:AddStatusEffect("Hidden")
				if healer.UpdateMoveAnim then
					healer:UpdateMoveAnim()
				end
			end,
		}),
	},
	DisplayName = T(890000000005025, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Laura DisplayName]] "Скрытный врач"),
	Description = T(890000000005026, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Laura Description]] "Лечение союзника не снимает с Лоры скрытность."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Laura.png",
	Tier = "Personal",
}
