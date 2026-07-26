UndefineClass('GruntyPerk_JAZZ')
DefineClass.GruntyPerk_JAZZ = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Хряпти",
	object_class = "Perk",
	msg_reactions = {},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatStarted",
			Handler = function (self, target, load_game)
				local ap = target:AddStatusEffect("Grunty_AdditionalAP")
			end,
		}),
	},
	DisplayName = T(890000000000723, --[[ModItemCharacterEffectCompositeDef GruntyPerk_JAZZ DisplayName]] "Юберрашунг"),
	Description = T(845332100943, --[[ModItemCharacterEffectCompositeDef GruntyPerk_JAZZ Description]] "Дает +50% од на первом ходу"),
	Icon = "UI/Icons/Perks/GruntyPerk",
	Tier = "Personal",
}

