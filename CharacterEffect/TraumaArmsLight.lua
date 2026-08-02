UndefineClass('TraumaArmsLight')
DefineClass.TraumaArmsLight = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Arms")
				end
			end,
		}),
	},
	DisplayName = T(890000000010100, "Arm Trauma (Light)"),
	Description = T(890000000010101, "Pain when shooting or using arms. No direct accuracy penalty."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaArmsLight.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
