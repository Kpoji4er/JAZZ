UndefineClass('ShoulderToShoulder')
DefineClass.ShoulderToShoulder = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				if not g_Combat then
					return
				end
				local nearby = {}
				for _, ally in ipairs(target.team and target.team.units or empty_table) do
					if ally ~= target and IsValid(ally) and not ally:IsDead() then
						if DivRound(target:GetDist(ally), const.SlabSizeX) <= 1 then
							nearby[#nearby + 1] = ally
						end
					end
				end
				if #nearby == 0 then
					return
				end
				target:ApplyTempHitPoints(15)
				for _, ally in ipairs(nearby) do
					ally:ApplyTempHitPoints(15)
				end
			end,
		}),
	},
	DisplayName = T(890000000006510, --[[ModItemCharacterEffectCompositeDef ShoulderToShoulder DisplayName]] "Плечом к плечу"),
	Description = T(890000000006511, --[[ModItemCharacterEffectCompositeDef ShoulderToShoulder Description]] "В конце хода, если рядом есть союзник (≤1 клетка), Скалли и ближайшие союзники получают <em>+15 Силы воли (Grit)</em>."),
	Icon = "UI/Icons/Perks/ShoulderToShoulder",
	Tier = "Personal",
}
