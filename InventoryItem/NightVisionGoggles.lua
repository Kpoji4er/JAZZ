UndefineClass('NightVisionGoggles')
DefineClass.NightVisionGoggles = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "UI/Icons/Items/night_vision",
	DisplayName = T(263962000489, --[[ModItemInventoryItemCompositeDef NightVisionGoggles DisplayName]] "Night Vision Goggles"),
	DisplayNamePlural = T(940518526415, --[[ModItemInventoryItemCompositeDef NightVisionGoggles DisplayNamePlural]] "Night Vision Goggles"),
	AdditionalHint = T(213348209507, --[[ModItemInventoryItemCompositeDef NightVisionGoggles AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снижает штрафы к точности ночью и в подземных секторах\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не суммируется с чертой «Ночные операции»\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нельзя совмещать с обивкой или керамическими пластинами"),
	Cost = 4000,
	CanAppearInShop = true,
	Tier = 3,
	RestockWeight = 35,
	Slot = "HeadGear",
	DamageReduction = 0,
	AdditionalReduction = 0,
	ProtectedBodyParts = set( "Head" ),
}

