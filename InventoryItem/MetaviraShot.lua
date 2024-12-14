UndefineClass('MetaviraShot')
DefineClass.MetaviraShot = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/metvira_shot",
	DisplayName = T(130291829266, --[[ModItemInventoryItemCompositeDef MetaviraShot DisplayName]] "Метавирон"),
	DisplayNamePlural = T(284293135018, --[[ModItemInventoryItemCompositeDef MetaviraShot DisplayNamePlural]] "Метавирон"),
	Description = T(771071455278, --[[ModItemInventoryItemCompositeDef MetaviraShot Description]] "Чудесное лекарство, добываемое из сока парового дерева, растущего исключительно на острове Метавира."),
	AdditionalHint = T(415192510445, --[[ModItemInventoryItemCompositeDef MetaviraShot AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Полностью восстанавливает запас ОЗ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Исцеляет все ранения"),
	Valuable = 1,
	Cost = 50000,
	CanAppearInShop = true,
	Tier = 3,
	MaxStock = 1,
	RestockWeight = 2,
	CategoryPair = "Medicine",
	effect_moment = "on_use",
	Effects = {
		PlaceObj('HealWounds', {}),
		PlaceObj('RestoreHealth', {}),
	},
	action_name = T(922193570040, --[[ModItemInventoryItemCompositeDef MetaviraShot action_name]] "ИСП."),
	destroy_item = true,
}

