UndefineClass('Warhead_Frag')
DefineClass.Warhead_Frag = {
	__parents = { "Ordnance" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Ordnance",
	Icon = "UI/Icons/Items/warhead_frag",
	DisplayName = T(938082134003, --[[ModItemInventoryItemCompositeDef Warhead_Frag DisplayName]] "ПГ-7В"),
	DisplayNamePlural = T(520121604271, --[[ModItemInventoryItemCompositeDef Warhead_Frag DisplayNamePlural]] "ПГ-7В"),
	Description = T(340753503694, --[[ModItemInventoryItemCompositeDef Warhead_Frag Description]] "Кумулятивный боеприпас для реактивных гранатометов."),
	AdditionalHint = T(944051778480, --[[ModItemInventoryItemCompositeDef Warhead_Frag AdditionalHint]] '<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В центре взрыва вызывает эффект «Горение»\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> В радиусе взрыва вызывает эффект "Подавление"'),
	Cost = 750,
	CanAppearInShop = true,
	Tier = 2,
	MaxStock = 16,
	RestockWeight = 50,
	CategoryPair = "Ordnance",
	MaxStacks = 1,
	CenterObjDamageMod = 500,
	CenterAppliedEffects = {
		"Burning",
		"Exposed",
	},
	AreaOfEffect = 2,
	AreaUnitDamageMod = 70,
	AreaAppliedEffects = {
		"Exposed",
	},
	PenetrationClass = 4,
	coneShaped = true,
	DeathType = "BlowUp",
	Caliber = "JAZZ_Caliber_Warhead",
	BaseDamage = 150,
	Noise = 100,
}

