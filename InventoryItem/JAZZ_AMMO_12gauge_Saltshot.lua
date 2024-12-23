UndefineClass('JAZZ_AMMO_12gauge_Saltshot')
DefineClass.JAZZ_AMMO_12gauge_Saltshot = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Соль - 20 частиц",
	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/12gSALT.png",
	DisplayName = T(242458393978, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Saltshot DisplayName]] "12-й калибр, соль"),
	DisplayNamePlural = T(907508796040, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Saltshot DisplayNamePlural]] "12-й калибр, соль"),
	colorStyle = "AmmoHPColor",
	Description = T(790667718698, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Saltshot Description]] "Боеприпас с солью 12-го калибра."),
	AdditionalHint = T(901574745246, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Saltshot AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> очень низкий урон\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Сниженная дальнобойность\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенный сектор атаки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает у цели <color EmStyle>случайные травмы</color>"),
	Cost = 100,
	CanAppearInShop = true,
	MaxStock = 5,
	RestockWeight = 80,
	ShopStackSize = 12,
	MaxStacks = 20,
	Caliber = "JAZZ_Caliber_12gauge",
	Modifications = {
		PlaceObj('CaliberModification', {
			mod_mul = 200,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 700,
			target_prop = "WeaponRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1700,
			target_prop = "OverwatchAngle",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 20000,
			target_prop = "AutoShots",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 800,
			target_prop = "Grouping",
		}),
	},
	AppliedEffects = {
		"Headshot",
		"Torsoshot",
		"Armsshot",
		"Legsshot",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

