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
				if load_game then
					return
				end
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
				-- Personal morale = team BD + likes/wounds/etc, clamped −5…5; chance uses max(0,morale).
				local morale = 0
				if target.GetPersonalMorale then
					morale = target:GetPersonalMorale() or 0
				end
				local chance = 10 * Max(0, morale)
				if chance <= 0 then
					return
				end
				local roll = InteractionRand(100, "GruntyPerk_JAZZ")
				if roll < chance then
					target:AddStatusEffect("Grunty_AdditionalAP")
					CombatLog("short", T{890000000009960, "<em><LogName></em>: Überraschung! (+50% AP; morale <morale>, chance <chance>%, roll <roll>)",
						LogName = target:GetLogName(),
						morale = morale,
						chance = chance,
						roll = roll,
					})
				else
					CombatLog("short", T{890000000009961, "<em><LogName></em>: Überraschung did not proc (morale <morale>, chance <chance>%, roll <roll>)",
						LogName = target:GetLogName(),
						morale = morale,
						chance = chance,
						roll = roll,
					})
				end
			end,
		}),
	},
	DisplayName = T(890000000000723, --[[ModItemCharacterEffectCompositeDef GruntyPerk_JAZZ DisplayName]] "Юберрашунг"),
	Description = T(845332100943, --[[ModItemCharacterEffectCompositeDef GruntyPerk_JAZZ Description]] "В начале боя получает +50% ОД на первый ход. На каждом следующем ходу с шансом <em>10% × личный боевой дух</em> снова получает тот же бонус (+50% ОД). Личный БД = командный уровень ± симпатии/раны (как в бою), для шанса 0…5; при 0 эффект не срабатывает."),
	Icon = "UI/Icons/Perks/GruntyPerk",
	Tier = "Personal",
}
