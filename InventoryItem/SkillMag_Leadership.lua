UndefineClass('SkillMag_Leadership')
DefineClass.SkillMag_Leadership = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_puntastic_dad_jokes",
	DisplayName = T(624085403180, --[[ModItemInventoryItemCompositeDef SkillMag_Leadership DisplayName]] "Puntastic Dad Jokes"),
	DisplayNamePlural = T(542345156012, --[[ModItemInventoryItemCompositeDef SkillMag_Leadership DisplayNamePlural]] "Puntastic Dad Jokes"),
	Description = T(437039053771, --[[ModItemInventoryItemCompositeDef SkillMag_Leadership Description]] "Why is issue six afraid of issue seven?"),
	AdditionalHint = T(575413455352, --[[ModItemInventoryItemCompositeDef SkillMag_Leadership AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает лидерство"),
	UnitStat = "Leadership",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Leadership",
		}),
	},
	action_name = T(134463686670, --[[ModItemInventoryItemCompositeDef SkillMag_Leadership action_name]] "READ"),
	destroy_item = true,
}

