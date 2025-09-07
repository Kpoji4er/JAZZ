UndefineClass('JAZZ_AMMO_40mmFragGrenade')
DefineClass.JAZZ_AMMO_40mmFragGrenade = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "UI/Icons/Items/40mm_frag_grenade",
	DisplayName = T(553319203791, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFragGrenade DisplayName]] "40-мм о/ф граната"),
	DisplayNamePlural = T(972658646505, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFragGrenade DisplayNamePlural]] "40-мм о/ф гранаты"),
	colorStyle = "AmmoBasicColor",
	Description = T(205133319221, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFragGrenade Description]] "Осколочно-фугасный боеприпас для гранатометов калибра 40 мм."),
	AdditionalHint = T(231013791244, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_40mmFragGrenade AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В центре взрыва вызывает у целей <color EmStyle>кровотечение</color>"),
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 25,
	RestockWeight = 50,
	CategoryPair = "Ordnance",
	MaxStacks = 6,
	CenterUnitDamageMod = 130,
	CenterObjDamageMod = 500,
	CenterAppliedEffects = {
		"Exposed",
	},
	AreaUnitDamageMod = 80,
	AreaObjDamageMod = 500,
	PenetrationClass = 4,
	DeathType = "BlowUp",
	Caliber = "JAZZ_Caliber_40mmGrenade",
	BaseDamage = 80,
	Entity = "Weapon_MilkorMGL_Shell",
}

