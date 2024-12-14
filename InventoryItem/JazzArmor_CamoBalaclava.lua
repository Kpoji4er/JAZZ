UndefineClass('JazzArmor_CamoBalaclava')
DefineClass.JazzArmor_CamoBalaclava = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	ScrapParts = 2,
	Degradation = 12,
	Icon = "Mod/e6L4ECj/ArmorIcons/CamoMask.png",
	DisplayName = T(127699575645, --[[ModItemInventoryItemCompositeDef JazzArmor_CamoBalaclava DisplayName]] "Камуфляжная балаклава"),
	DisplayNamePlural = T(599960117734, --[[ModItemInventoryItemCompositeDef JazzArmor_CamoBalaclava DisplayNamePlural]] "Камуфляжные балаклавы"),
	Description = T(346368526537, --[[ModItemInventoryItemCompositeDef JazzArmor_CamoBalaclava Description]] "ШПС-ка, она же шапка-пи... пряталка спецназовская. Тканевая маска, скрывающая лицо, с прорезями для глаз и рта. Камуфляжная раскраска помогает хозяину прятать свое лицо еще лучше."),
	AdditionalHint = T(557858399256, --[[ModItemInventoryItemCompositeDef JazzArmor_CamoBalaclava AdditionalHint]] "Помогает лучше прятаться"),
	Cost = 500,
	AttachEntries = {
		PlaceObj('BodyPartData', {
			'EditableColor1', RGBA(27, 75, 10, 255),
			'EditableColor2', RGBA(36, 117, 11, 255),
			'Slot', "HeadGear",
			'Gender', "Male",
			'Entity', "Faction_Thugs_Mask_01",
			'Spot', "Origin",
			'X', 5,
			'Hide', {
				"Hair",
			},
		}),
	},
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 1,
	RestockWeight = 1,
	Slot = "HeadGear",
	PenetrationClass = 2,
	AdditionalReduction = 20,
	ProtectedBodyParts = set( "Head" ),
	CamouflagePercent = 5,
	Vision = -5,
}

