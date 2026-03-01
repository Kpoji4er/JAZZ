UndefineClass('Jazz_Perk_00')
DefineClass.Jazz_Perk_00 = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target:SetEffectValue("Jazz_Perk_00", nil)
			end,
		}),
	},
	DisplayName = T(163764621255, --[[ModItemCharacterEffectCompositeDef AutoWeapons DisplayName]] "00:00"),
	Description = T(841645965970, --[[ModItemCharacterEffectCompositeDef AutoWeapons Description]] "При активации взрывчатка с таймером, кинутая Споуком, взорвётся в начале вражеского хода."),
	Icon = "UI/Icons/Perks/DesignerExplosives",
	Tier = "Personal",
}

