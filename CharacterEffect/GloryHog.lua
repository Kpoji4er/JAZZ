UndefineClass('GloryHog')
DefineClass.GloryHog = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "temp_hp",
			'Value', 15,
			'Tag', "<temp_hp>",
		}),
	},
	DisplayName = T(890000000009927, --[[ModItemCharacterEffectCompositeDef GloryHog DisplayName]] "Жажда славы"),
	Description = T(890000000009928, --[[ModItemCharacterEffectCompositeDef GloryHog Description]] "Спецатака мачете <em>Charge</em> без прямой линии пути и даёт <em><temp_hp></em> <GameTerm('Grit')>. Активка: один раз за бой перевербовать видимого врага в союзника под ИИ (не боссы)."),
	Icon = "UI/Icons/Perks/GloryHog",
	Tier = "Personal",
}
