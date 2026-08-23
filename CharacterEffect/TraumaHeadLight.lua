UndefineClass('TraumaHeadLight')
DefineClass.TraumaHeadLight = {
	__parents = { "JazzTraumaEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "JazzTraumaEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnFirearmAttackStart",
			Handler = function(self, target, attacker, attack_target, action, attack_args)
				if target == attacker then
					JazzTraumaPainOnZoneUse(attacker, "Head")
				end
			end,
		}),
	},
	DisplayName = T(890000000010118, "Head Trauma (Light)"),
	Description = T(890000000010119, "Pain when aiming or firing."),
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/TraumaHeadLight.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
