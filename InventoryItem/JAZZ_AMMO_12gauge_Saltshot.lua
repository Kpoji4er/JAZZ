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
	Description = T(790667718698, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_12gauge_Saltshot Description]] "20ый калибр это не серьёзно говорили они, но тем не менее всё лучше чем ничего, люди всё также дырявятся."),
	AdditionalHint = "",
	Cost = 180,
	CanAppearInShop = true,
	MaxStock = 5,
	RestockWeight = 5,
	ShopStackSize = 25,
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
			target_prop = "BuckshotProjectiles",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 1300,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -2,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 0,
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 1,
			target_prop = "PenetrationBonus",
		}),
	},
	AppliedEffects = {
		"HeadshotTorsoshotArmsshotLegsshot",
	},
	ammo_type_icon = "UI/Icons/Items/ta_hp.png",
}

