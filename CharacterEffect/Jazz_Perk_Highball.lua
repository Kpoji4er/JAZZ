UndefineClass('Jazz_Perk_Highball')
DefineClass.Jazz_Perk_Highball = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcHealAmount",
			Handler = function (self, target, patient, medic, medkit, data)
				if target ~= medic or not data then
					return
				end
				local ok = false
				local slab = const.SlabSizeX
				for _, u in ipairs(medic.team and medic.team.units or empty_table) do
					if u ~= medic and IsValid(u) and not u:IsDead() and (u.Medical or 0) >= 80 then
						if DivRound(medic:GetDist(u), slab) <= 5 then
							ok = true
							break
						end
					end
				end
				if ok then
					local roll = 50 + InteractionRand(101, "Jazz_Perk_Highball")
					data.heal_modifier = MulDivRound(data.heal_modifier or 100, roll, 100)
				end
			end,
		}),
	},
	DisplayName = T(890000000004200, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Highball DisplayName]] "Полевой химик"),
	Description = T(890000000004201, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Highball Description]] "Лечение ±50%, если рядом (≤5) союзник-врач с Medical≥80 / в отряде на спутнике."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Highball.png",
	Tier = "Personal",
}
