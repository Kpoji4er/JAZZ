UndefineClass('Nazdarovya')
DefineClass.Nazdarovya = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	Parameters = {
		PlaceObj('PresetParamNumber', {
			'Name', "healMin",
			'Value', 15,
			'Tag', "<healMin>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "healMax",
			'Value', 20,
			'Tag', "<healMax>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "maxStacks",
			'Value', 5,
			'Tag', "<maxStacks>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "melee_damage_flat",
			'Value', 20,
			'Tag', "<melee_damage_flat>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "range_cth_mod",
			'Value', -15,
			'Tag', "<range_cth_mod>",
		}),
		PlaceObj('PresetParamNumber', {
			'Name', "hoursPerStack",
			'Value', 3,
			'Tag', "<hoursPerStack>",
		}),
	},
	unit_reactions = {},
	DisplayName = T(890000000009887, --[[ModItemCharacterEffectCompositeDef Nazdarovya DisplayName]] "Наздаровье"),
	Description = T(890000000009888, --[[ModItemCharacterEffectCompositeDef Nazdarovya Description]] "Активка (2 ОД): снимает боль, лечит <healMin>–<healMax> HP, даёт стак опьянения (до <maxStacks>). За стак: <range_cth_mod> CTH, +<melee_damage_flat> урона в ближке. <color EmStyle>Заряжается после убийства.</color> Опьянение в долг — −1 стак каждые <hoursPerStack> ч."),
	Icon = "UI/Icons/Perks/Nazdarovya",
	Tier = "Personal",
}
