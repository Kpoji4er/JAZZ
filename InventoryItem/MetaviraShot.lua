UndefineClass('MetaviraShot')
DefineClass.MetaviraShot = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/metvira_shot",
	DisplayName = T(704109326715, --[[ModItemInventoryItemCompositeDef MetaviraShot DisplayName]] "Metaviron"),
	DisplayNamePlural = T(736601384762, --[[ModItemInventoryItemCompositeDef MetaviraShot DisplayNamePlural]] "Metaviron"),
	Description = T(288596816028, --[[ModItemInventoryItemCompositeDef MetaviraShot Description]] "Miracle cure derived from the sap of the Fallow trees indigenous to the island of Metavira"),
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
	action_name = T(509524872124, --[[ModItemInventoryItemCompositeDef MetaviraShot action_name]] "USE"),
	destroy_item = true,
}

