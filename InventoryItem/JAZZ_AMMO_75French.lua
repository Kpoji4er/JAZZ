UndefineClass('JAZZ_AMMO_75French')
DefineClass.JAZZ_AMMO_75French = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/75.png",
	DisplayName = T(195831313662, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French DisplayName]] "7,5х54 мм, обычный"),
	DisplayNamePlural = T(790852334727, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French DisplayNamePlural]] "7,5х54 мм, обычные"),
	colorStyle = "AmmoBasicColor",
	Description = T(634152164577, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French Description]] "Немецкий боеприпас калибра 7.5х55мм MAS"),
	AdditionalHint = T(727230096414, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_75French AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 100,
	CanAppearInShop = true,
	MaxStock = 5,
	CategoryPair = "792",
	ShopStackSize = 30,
	MaxStacks = 40,
	Caliber = "JAZZ_Caliber_75French",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
}

