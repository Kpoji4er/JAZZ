UndefineClass('Jazz_Perk_Henning')
DefineClass.Jazz_Perk_Henning = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "radius",
			'Value', 10,
			'Tag', "<radius>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if not g_Combat then
					return
				end
				for _, ally in ipairs(target.team and target.team.units or empty_table) do
					if ally ~= target and IsValid(ally) and not ally:IsDead() then
						if DivRound(target:GetDist(ally), const.SlabSizeX) <= (self:ResolveValue("radius") or 10) then
							ally:AddStatusEffect("Jazz_OrderAP")
						end
					end
				end
			end,
		}),
	},
	DisplayName = T(890000000004000, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Henning DisplayName]] "Полевой командир"),
	Description = T(890000000004001, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Henning Description]] "В начале хода союзники в радиусе 10 клеток получают +3 ОД."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Henning.png",
	Tier = "Personal",
}
