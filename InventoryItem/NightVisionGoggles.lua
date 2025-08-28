UndefineClass('NightVisionGoggles')
DefineClass.NightVisionGoggles = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "UI/Icons/Items/night_vision",
	DisplayName = T(753212837827, "ПНВ"),
	DisplayNamePlural = T(216190457512, "ПНВ"),
	AdditionalHint = T(213348209507, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Снижает штрафы к точности ночью и в подземных секторах\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не суммируется с чертой «Ночные операции»\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Нельзя совмещать с обивкой или керамическими пластинами"),
	Cost = 3500,
	Tier = 2,
	RestockWeight = 15,
	Slot = "HeadGear",
	DamageReduction = 0,
	AdditionalReduction = 0,
	ProtectedBodyParts = set( "Head" ),
}

