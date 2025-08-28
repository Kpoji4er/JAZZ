UndefineClass('_40mmFragGrenade')
DefineClass._40mmFragGrenade = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "UI/Icons/Items/40mm_frag_grenade",
	DisplayName = T(615603318057, "40-мм о/ф граната"),
	DisplayNamePlural = T(208050145313, "40-мм о/ф гранаты"),
	colorStyle = "AmmoBasicColor",
	Description = T(800783522595, "Осколочно-фугасный боеприпас для гранатометов калибра 40 мм."),
	AdditionalHint = T(956592215973, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В центре взрыва вызывает у целей <color EmStyle>кровотечение</color>"),
	Tier = 2,
	MaxStock = 25,
	RestockWeight = 50,
	CategoryPair = "Ordnance",
	MaxStacks = 100,
	CenterUnitDamageMod = 130,
	CenterObjDamageMod = 500,
	CenterAppliedEffects = {
		"Exposed",
	},
	AreaUnitDamageMod = 10,
	AreaObjDamageMod = 500,
	PenetrationClass = 4,
	DeathType = "BlowUp",
	Caliber = "40mmGrenade",
	BaseDamage = 80,
	Entity = "Weapon_MilkorMGL_Shell",
}

