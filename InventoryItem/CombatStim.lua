UndefineClass('CombatStim')
DefineClass.CombatStim = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/combat_stim",
	DisplayName = T(233252386562, "Боевой стимулятор"),
	DisplayNamePlural = T(838459151033, "Боевые стимуляторы"),
	AdditionalHint = T(952937600404, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дает доп. ОД до конца след. хода\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снижает запас энергии после окончания действия эффекта"),
	Cost = 400,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 6,
	RestockWeight = 25,
	CategoryPair = "Medicine",
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitAddStatusEffect', {
			Status = "Stimmed",
		}),
	},
	action_name = T(593242783730, "ИСП."),
	destroy_item = true,
	onlyOnMap = true,
}

