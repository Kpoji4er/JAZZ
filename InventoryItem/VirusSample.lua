UndefineClass('VirusSample')
DefineClass.VirusSample = {
	__parents = { "QuestStackItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "QuestStackItem",
	Repairable = false,
	Icon = "UI/Icons/Items/red_rabies_virus_sample",
	DisplayName = T(219970007960, "Образец вируса"),
	DisplayNamePlural = T(277474900460, "Образцы вируса"),
	Description = T(931089747795, "Биологический материал, необходимый для расшифровки генома вируса красного бешенства. Не кантовать."),
	AdditionalHint = T(626501302662, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Во время сбора образца не пострадало ни одной летучей мыши"),
	Cost = 100,
	RestockWeight = 0,
}

