UndefineClass('ExplodingPalm')
DefineClass.ExplodingPalm = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamPercent', {
			'Name', "sat_debt_speed_percent",
			'Value', 30,
			'Tag', "<sat_debt_speed_percent>",
		}),
	},
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnUnitAttack",
			Handler = function (self, target, attacker, action, attack_target, results, attack_args)
				if target ~= attacker or not results or results.miss then
					return
				end
				if type(Jazz_ExplodingPalmOnUnarmedHit) == "function" then
					Jazz_ExplodingPalmOnUnarmedHit(attacker, action, attack_target, results, attack_args)
				end
			end,
		}),
	},
	DisplayName = T(890000000009924, --[[ModItemCharacterEffectCompositeDef ExplodingPalm DisplayName]] "Взрывная ладонь"),
	Description = T(890000000009892, --[[ModItemCharacterEffectCompositeDef ExplodingPalm Description]] "Пассивно. Удары <em>голыми руками</em> по живому противнику в зависимости от его текущего HP: ≤20% — нокдаун и без сознания; ≤35% — контузия; ≤50% — травма рёбер; ≤65% — травма рук; ≤80% — травма ног; иначе — травма паха (рёбра/«яйца»). В отряде на сателлите: восстановление травм, ожогов и HP-долга на <sat_debt_speed_percent>% быстрее; защищает от инфекции ран."),
	Icon = "UI/Icons/Perks/ExplodingPalm",
	Tier = "Personal",
}
