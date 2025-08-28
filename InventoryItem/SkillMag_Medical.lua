UndefineClass('SkillMag_Medical')
DefineClass.SkillMag_Medical = {
	__parents = { "MiscItem" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "MiscItem",
	Repairable = false,
	Icon = "UI/Icons/Items/mag_national_paramedic",
	DisplayName = T(520828600732, "Для тех, кто вяжет"),
	DisplayNamePlural = T(981036857917, "Для тех, кто вяжет"),
	Description = T(505843277064, "Модные схемы для перевязки и узорная работа жгутом."),
	AdditionalHint = T(438853574488, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Используется через меню предмета\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Одноразовый предмет\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Повышает навык «Медицина»"),
	UnitStat = "Medical",
	Valuable = 1,
	Cost = 1500,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 10,
	effect_moment = "on_use",
	Effects = {
		PlaceObj('UnitStatBoost', {
			Amount = 1,
			Stat = "Medical",
		}),
	},
	action_name = T(887526961257, "ЧИТАТЬ"),
	destroy_item = true,
}

