UndefineClass('Crowbar')
DefineClass.Crowbar = {
	__parents = { "CrowbarBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "CrowbarBase",
	ScrapParts = 2,
	Repairable = false,
	Icon = "UI/Icons/Items/crowbar",
	DisplayName = T(851337385387, --[[ModItemInventoryItemCompositeDef Crowbar DisplayName]] "Crowbar"),
	DisplayNamePlural = T(855121960280, --[[ModItemInventoryItemCompositeDef Crowbar DisplayNamePlural]] "Crowbars"),
	AdditionalHint = T(895419226911, --[[ModItemInventoryItemCompositeDef Crowbar AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вскрывает замки на дверях и контейнерах (в зависимости от силы)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Может повредить содержимое контейнера\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Изнашивается при каждом употреблении\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Не поддается ремонту\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Strength",
	Cost = 100,
	CanAppearInShop = true,
	CategoryPair = "Tool",
}

