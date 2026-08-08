UndefineClass('SecondStoryMan')
DefineClass.SecondStoryMan = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcCritChance",
			Handler = function (self, target, attacker, attack_target, action, weapon, data)
				if target ~= attacker or not data or not IsKindOf(attack_target, "Unit") then
					return
				end
				local apos = attacker:GetPos()
				local tpos = attack_target:GetPos()
				if not apos or not tpos then
					return
				end
				local az = apos:IsValidZ() and apos:z() or terrain.GetHeight(apos)
				local tz = tpos:IsValidZ() and tpos:z() or terrain.GetHeight(tpos)
				local threshold = const.SlabSizeZ / 2
				local presets = Presets.ChanceToHitModifier and Presets.ChanceToHitModifier.Default
				local gd = presets and presets.GroundDifference
				if gd and gd.ResolveValue then
					local pct = gd:ResolveValue("RangeThreshold")
					if pct then
						threshold = MulDivRound(const.SlabSizeZ, pct, 100)
					end
				end
				if az > tz + threshold then
					data.crit_chance = (data.crit_chance or 0) + 50
				end
			end,
		}),
	},
	DisplayName = T(890000000006508, --[[ModItemCharacterEffectCompositeDef SecondStoryMan DisplayName]] "Человек со второго этажа"),
	Description = T(890000000006509, --[[ModItemCharacterEffectCompositeDef SecondStoryMan Description]] "Атаки <em>сверху</em> получают <em>+50%</em> к шансу критического удара."),
	Icon = "UI/Icons/Perks/SecondStoryMan",
	Tier = "Personal",
}
