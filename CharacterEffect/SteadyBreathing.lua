UndefineClass('SteadyBreathing')
DefineClass.SteadyBreathing = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcFreeMove",
			Handler = function (self, target, data)
				local armourItems = target:GetEquipedArmour()
				for _, item in ipairs(armourItems) do
					if item.Weight > 2 then
						return
					end
				end
				data.add = data.add + self:ResolveValue("freeMoveBonusAp")
			end,
		}),
	},
	DisplayName = T(855415767233, "Fast Runner"),
	Description = T(785177734706, "Increased <GameTerm('FreeMove')> <em>Range</em> when wearing <em>Light Armor</em> or not wearing any Armor."),
	Icon = "UI/Icons/Perks/SteadyBreathing",
	Tier = "Bronze",
	Stat = "Agility",
	StatValue = 70,
}

