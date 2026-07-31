UndefineClass('Jazz_Perk_Vicious')
DefineClass.Jazz_Perk_Vicious = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatStarted",
			Handler = function (self, target, load_game)
				if load_game then
					return
				end
				local women = 0
				for _, u in ipairs(target.team and target.team.units or empty_table) do
					if u.gender == "Female" then
						women = women + 1
					end
				end
				women = Min(women, 3)
				target:SetEffectValue("Jazz_Perk_Vicious", women > 0 and women or nil)
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local women = target:GetEffectValue("Jazz_Perk_Vicious")
				if women and not target:GetEffectValue("Jazz_Perk_Vicious_Applied") then
					target:GainAP(women * const.Scale.AP)
					target:SetEffectValue("Jazz_Perk_Vicious_Applied", true)
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnCombatEnd",
			Handler = function (self, target)
				target:SetEffectValue("Jazz_Perk_Vicious", nil)
				target:SetEffectValue("Jazz_Perk_Vicious_Applied", nil)
			end,
		}),
	},
	DisplayName = T(890000000002700, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vicious DisplayName]] "Дамский угодник"),
	Description = T(890000000002701, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Vicious Description]] "В начале боя: +1 ОД за каждую женщину в отряде (макс. 3)."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Vicious.png",
	Tier = "Personal",
}
