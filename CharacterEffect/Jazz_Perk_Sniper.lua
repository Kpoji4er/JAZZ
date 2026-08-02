UndefineClass('Jazz_Perk_Sniper')
DefineClass.Jazz_Perk_Sniper = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcMaxAimActions",
			Handler = function(self, value, attacker, target, action, weapon)
				return value + 1
			end,
		}),
	},
	DisplayName = T(890000000001935, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Sniper DisplayName]] "Снайпер"),
	Description = T(890000000001936, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Sniper Description]] "Максимальный уровень прицеливания <em>+1</em> при стрельбе из любого оружия."),
	Icon = "UI/Icons/Perks/Deadeye",
	Tier = "Personality",
}
