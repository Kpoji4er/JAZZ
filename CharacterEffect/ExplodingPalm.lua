UndefineClass('ExplodingPalm')
DefineClass.ExplodingPalm = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function (self, target, patient, medic, medkit, data)
				if target ~= medic or not data then
					return
				end
				-- Soft: +30% heal when treating (trauma-specific ops deferred).
				data.heal_modifier = MulDivRound(data.heal_modifier or 100, 130, 100)
			end,
		}),
	},
	DisplayName = T(890000000009891, --[[ModItemCharacterEffectCompositeDef ExplodingPalm DisplayName]] "Взрывная ладонь"),
	Description = T(890000000009892, --[[ModItemCharacterEffectCompositeDef ExplodingPalm Description]] "Удары кулаком: статусы по HP. Satellite trauma heal +30%; сопротивление инфекции (partial)."),
	Icon = "UI/Icons/Perks/ExplodingPalm",
	Tier = "Personal",
}
