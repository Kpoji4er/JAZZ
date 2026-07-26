UndefineClass('_40mmFragGrenade')
DefineClass._40mmFragGrenade = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "UI/Icons/Items/40mm_frag_grenade",
	DisplayName = T(551384656328, --[[ModItemInventoryItemCompositeDef _40mmFragGrenade DisplayName]] "40 mm HE"),
	DisplayNamePlural = T(922038247898, --[[ModItemInventoryItemCompositeDef _40mmFragGrenade DisplayNamePlural]] "40 mm HE"),
	colorStyle = "AmmoBasicColor",
	Description = T(997055293212, --[[ModItemInventoryItemCompositeDef _40mmFragGrenade Description]] "40 mm ordnance ammo for Grenade Launchers."),
	AdditionalHint = T(956592215973, --[[ModItemInventoryItemCompositeDef _40mmFragGrenade AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В центре взрыва вызывает у целей <color EmStyle>кровотечение</color>"),
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

