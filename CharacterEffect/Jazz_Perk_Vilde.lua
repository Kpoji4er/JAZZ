UndefineClass('Jazz_Perk_Vilde')
DefineClass.Jazz_Perk_Vilde = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				if target ~= attacker or not action then
					return
				end
				if not (GameState.Night or GameState.Underground) then
					return
				end
				local id = action.id
				if id == "AutoFire" or id == "BurstFire" or id == "MGBurstFire" or id == "JAZZ_LargeAutoFire" or id == "JAZZ_SmgStorm" or id == "JAZZ_Zipper" then
					ApplyCthModifier_Add(self, data, 15)
				end
			end,
		}),
	},
	DisplayName = T(890000000005037, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vilde DisplayName]] "Ночной автоматчик"),
	Description = T(890000000005038, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vilde Description]] "Ночью и под землёй автоогонь/очередь получают +15 к шансу попадания."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Vilde.png",
	Tier = "Personal",
}
