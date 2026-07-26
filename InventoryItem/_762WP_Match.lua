UndefineClass('_762WP_Match')
DefineClass._762WP_Match = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Disabled",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/TEST.png",
	DisplayName = T(983548612559, --[[ModItemInventoryItemCompositeDef _762WP_Match DisplayName]] "7.62 mm WP Match"),
	DisplayNamePlural = T(565381152146, --[[ModItemInventoryItemCompositeDef _762WP_Match DisplayNamePlural]] "7.62 mm WP Match"),
	colorStyle = "AmmoMatchColor",
	Description = T(587024333620, --[[ModItemInventoryItemCompositeDef _762WP_Match Description]] "7.62 Warsaw Pact ammo for Assault Rifles, SMGs, Machine Guns, and Rifles."),
	AdditionalHint = T(664395917370, --[[ModItemInventoryItemCompositeDef _762WP_Match AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания"),
	Cost = 100,
	Tier = 3,
	MaxStock = 5,
	RestockWeight = 25,
	CategoryPair = "762WP",
	ShopStackSize = 30,
	MaxStacks = 5000,
	Caliber = "",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 0,
			target_prop = "Damage",
		}),
	},
	ammo_type_icon = "UI/Icons/Items/ta_match.png",
}

