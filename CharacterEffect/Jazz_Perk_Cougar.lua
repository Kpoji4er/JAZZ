UndefineClass('Jazz_Perk_Cougar')
DefineClass.Jazz_Perk_Cougar = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "noise_mul",
			'Value', 67,
			'Tag', "<noise_mul>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results then
					return
				end
				if results.stealth_kill and type(Jazz_CougarOnStealthKill) == "function" then
					Jazz_CougarOnStealthKill(attacker)
				end
			end,
		}),
	},
	DisplayName = T(890000000003100, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Cougar DisplayName]] "Мягкая лапа"),
	Description = T(890000000003101, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Cougar Description]] "Выстрелы Пумы на 33% тише. Скрытое убийство даёт Inspired 1×/ход (не возврат ОД)."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Cougar.png",
	Tier = "Personal",
}
