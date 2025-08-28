UndefineClass('Loner')
DefineClass.Loner = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				for _, other in ipairs(target.team.units) do
					if target ~= other and DivRound(target:GetDist(other), const.SlabSizeX) <= self:ResolveValue("loner_radius") then
						return
					end
				end
				
				target:AddStatusEffect("Inspired")
				PlayVoiceResponse(target, "Loner")
			end,
		}),
	},
	DisplayName = T(487342591563, "Одиночка"),
	Description = T(124325843871, "Дает <GameTerm('Inspired')>, если в начале хода рядом с вами нет бойцов вашего отряда."),
	Icon = "UI/Icons/Perks/Loner",
	Tier = "Quirk",
}

