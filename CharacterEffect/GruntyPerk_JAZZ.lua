UndefineClass('GruntyPerk_JAZZ')
DefineClass.GruntyPerk_JAZZ = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Хряпти",
	object_class = "Perk",
	msg_reactions = {},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCombatStarted",
			Handler = function (self, target, load_game)
				target:AddStatusEffect("Grunty_AdditionalAP")
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				if not g_Combat then
					return
				end
				-- First turn already covered by OnCombatStarted buff.
				if target:HasStatusEffect("Grunty_AdditionalAP") then
					return
				end
				local morale = 0
				if target.GetPersonalMorale then
					morale = target:GetPersonalMorale() or 0
				end
				local chance = 10 * Max(0, morale)
				if chance <= 0 then
					return
				end
				if InteractionRand(100, "GruntyPerk_JAZZ") < chance then
					target:AddStatusEffect("Grunty_AdditionalAP")
				end
			end,
		}),
	},
	DisplayName = T(890000000000723, --[[ModItemCharacterEffectCompositeDef GruntyPerk_JAZZ DisplayName]] "Юберрашунг"),
	Description = T(845332100943, --[[ModItemCharacterEffectCompositeDef GruntyPerk_JAZZ Description]] "В начале боя получает +50% ОД на первый ход. На каждом следующем ходу с шансом <em>10% × уровень боевого духа</em> снова получает тот же бонус (+50% ОД)."),
	Icon = "UI/Icons/Perks/GruntyPerk",
	Tier = "Personal",
}
