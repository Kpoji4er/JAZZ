UndefineClass('CombatStim')
DefineClass.CombatStim = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/combat_stim",
	DisplayName = T(634691805568, --[[ModItemInventoryItemCompositeDef CombatStim DisplayName]] "Combat Stim"),
	DisplayNamePlural = T(713501369682, --[[ModItemInventoryItemCompositeDef CombatStim DisplayNamePlural]] "Combat Stims"),
	AdditionalHint = T(952937600404, --[[ModItemInventoryItemCompositeDef CombatStim AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дает доп. ОД до конца след. хода\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снижает запас энергии после окончания действия эффекта"),
	Cost = 400,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 6,
	RestockWeight = 25,
	CategoryPair = "Medicine",
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitAddStatusEffect', {
			Status = "Stimmed",
		}),
	},
	action_name = T(767441148476, --[[ModItemInventoryItemCompositeDef CombatStim action_name]] "USE"),
	destroy_item = true,
	onlyOnMap = true,
}

