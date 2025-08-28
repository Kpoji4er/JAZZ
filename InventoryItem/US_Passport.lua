UndefineClass('US_Passport')
DefineClass.US_Passport = {
	__parents = { "QuestItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "QuestItem",
	Repairable = false,
	Icon = "UI/Icons/Items/american_passport",
	DisplayName = T(764440710259, "Паспорт США"),
	DisplayNamePlural = T(725867878955, "Паспорт США"),
	Description = T(827657816504, "Загранпаспорт на имя некой Карен Гослинг"),
	AdditionalHint = T(227052415098, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пропуск в страну, где угроза пожаловаться менеджеру решает любые проблемы"),
	Cost = 200,
	RestockWeight = 0,
}

