UndefineClass('PlasmaGun_Crowbar')
DefineClass.PlasmaGun_Crowbar = {
	__parents = { "CrowbarBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "CrowbarBase",
	ScrapParts = 4,
	RepairCost = 120,
	CanAppearInShop = false,
	Icon = "UI/Icons/Items/plasma_gun_crowbar",
	DisplayName = T(507871191066, --[[ModItemInventoryItemCompositeDef PlasmaGun_Crowbar DisplayName]] "Plasma Gun Crowbar"),
	DisplayNamePlural = T(593438446878, --[[ModItemInventoryItemCompositeDef PlasmaGun_Crowbar DisplayNamePlural]] "Plasma Gun Crowbars"),
	AdditionalHint = T(972121373391, --[[ModItemInventoryItemCompositeDef PlasmaGun_Crowbar AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В идеальном вакууме стреляет смертоносными сгустками плазмы. Во всех остальных случаях работает как фомка\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вскрывает замки на дверях и контейнерах (в зависимости от силы)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дает бонус к проверке навыка при взломе замков\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Может повредить содержимое контейнера\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Изнашивается при каждом употреблении\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Поддается ремонту\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	Valuable = 1,
	RestockWeight = 0,
	skillCheckPenalty = -15,
}

