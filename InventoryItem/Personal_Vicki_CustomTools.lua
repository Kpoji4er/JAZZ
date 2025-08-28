UndefineClass('Personal_Vicki_CustomTools')
DefineClass.Personal_Vicki_CustomTools = {
	__parents = { "LockpickBase" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "LockpickBase",
	RepairCost = 120,
	Icon = "UI/Icons/Items/vicki_lockpick",
	DisplayName = T(139588576447, "Набор отмычек Вики"),
	DisplayNamePlural = T(766692495920, "Набор отмычек Вики"),
	AdditionalHint = T(903095626259, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вскрывает замки на дверях и контейнерах (зависит от навыка механики)\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Дает бонус к проверке навыка при вскрытии замков\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Изнашивается при каждом употреблении\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Поддается ремонту\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется автоматически, просто находясь в инвентаре"),
	UnitStat = "Mechanical",
	locked = true,
	RestockWeight = 0,
	skillCheckPenalty = -10,
}

