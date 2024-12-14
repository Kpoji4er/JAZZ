UndefineClass('Crowbar')
DefineClass.Crowbar = {
	__parents = { "CrowbarBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "CrowbarBase",
	ScrapParts = 2,
	Repairable = false,
	Icon = "UI/Icons/Items/crowbar",
	DisplayName = T(736175574176, --[[ModItemInventoryItemCompositeDef Crowbar DisplayName]] "Фомка"),
	DisplayNamePlural = T(488481985235, --[[ModItemInventoryItemCompositeDef Crowbar DisplayNamePlural]] "Фомки"),
	AdditionalHint = T(895419226911, --[[ModItemInventoryItemCompositeDef Crowbar AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вскрывает замки на дверях и контейнерах (в зависимости от силы)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Может повредить содержимое контейнера\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Изнашивается при каждом употреблении\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не поддается ремонту\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Strength",
	Cost = 100,
	CanAppearInShop = true,
	CategoryPair = "Tool",
}

