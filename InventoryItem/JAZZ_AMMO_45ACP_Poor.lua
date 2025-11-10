UndefineClass('JAZZ_AMMO_45ACP_Poor')
DefineClass.JAZZ_AMMO_45ACP_Poor = {
	__parents = { "Ammo" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ammo",
	Icon = "Mod/e6L4ECj/Ammopics/45ACPsub.png",
	DisplayName = T(270886313378, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_Poor DisplayName]] ".45ACP, M1911 Substandard"),
	DisplayNamePlural = T(136983924045, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_Poor DisplayNamePlural]] ".45ACP, M1911 Substandard"),
	colorStyle = "AmmoSubstandardColor",
	Description = T(654722607287, --[[ModItemInventoryItemCompositeDef JAZZ_AMMO_45ACP_Poor Description]] "Какая-то китайская хренотень, работает плохо, как и всё китайское, если вам больше нечем стрелять или не хватает острых ощущений, используйте данные патроны, это лучше чем ничего."),
	AdditionalHint = "",
	Cost = 180,
	CanAppearInShop = true,
	MaxStock = 50,
	RestockWeight = 30,
	CategoryPair = "45ACP",
	ShopStackSize = 50,
	MaxStacks = 80,
	Caliber = "JAZZ_Caliber_45ACP",
	Modifications = {
		PlaceObj('CaliberModification', {
			target_prop = "PenetrationClass",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -4,
			target_prop = "PenetrationBonus",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 950,
			target_prop = "Damage",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -15,
			target_prop = "Reliability",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 150,
			target_prop = "BaseJamChance",
		}),
		PlaceObj('CaliberModification', {
			mod_mul = 900,
			target_prop = "Grouping",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "BulletDropRange",
		}),
		PlaceObj('CaliberModification', {
			mod_add = 5,
			target_prop = "CritChance",
		}),
		PlaceObj('CaliberModification', {
			mod_add = -1,
			target_prop = "Recoil",
		}),
	},
}

