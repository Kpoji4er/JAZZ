UndefineClass('Jazz_Perk_Steiger')
DefineClass.Jazz_Perk_Steiger = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if not g_Combat or not (GameState.Night or GameState.Underground) then
					return
				end
				for _, ally in ipairs(target.team and target.team.units or empty_table) do
					if ally ~= target and IsValid(ally) and not ally:IsDead() then
						if DivRound(target:GetDist(ally), const.SlabSizeX) <= 5 then
							ally:AddStatusEffect("Jazz_OrderCTH")
						end
					end
				end
			end,
		}),
	},
	DisplayName = T(890000000005041, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Steiger DisplayName]] "Ночной инструктор"),
	Description = T(890000000005042, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Steiger Description]] "Ночью и под землёй в начале хода союзники в радиусе 5 клеток получают +5 к шансу попадания."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Steiger.png",
	Tier = "Personal",
}
