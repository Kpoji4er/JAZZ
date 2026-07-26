UndefineClass('_762NATO_Tracer')
DefineClass._762NATO_Tracer = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Как M80, но трассера",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(634358146978, --[[ModItemInventoryItemCompositeDef _762NATO_Tracer DisplayName]] "7.62х51мм НАТО, M62"),
	DisplayNamePlural = T(915862614034, --[[ModItemInventoryItemCompositeDef _762NATO_Tracer DisplayNamePlural]] "7.62х51мм НАТО, M62"),
	colorStyle = "AmmoTracerColor",
	Description = T(223701622960, --[[ModItemInventoryItemCompositeDef _762NATO_Tracer Description]] "7.62 NATO ammo for Assault Rifles, Rifles, and Machine Guns."),
	AdditionalHint = T(941135261525, --[[ModItemInventoryItemCompositeDef _762NATO_Tracer AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Пораженные цели получают статус «<color EmStyle>Вне укрытия</color>» и лишаются его преимуществ\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Обеспечивает уверенное поражение целей обладающих 3-м классом брони"),
	Cost = 200,
	Tier = 2,
	MaxStock = 10,
	RestockWeight = 25,
	CategoryPair = "762NATO",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "762NATO",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_add = 2,
			target_prop = "PenetrationClass",
		}),
	},
	AppliedEffects = {
		"Exposed",
	},
	ammo_type_icon = "UI/Icons/Items/ta_tracer.png",
}

