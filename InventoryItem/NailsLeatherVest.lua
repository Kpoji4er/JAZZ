UndefineClass('NailsLeatherVest')
DefineClass.NailsLeatherVest = {
	__parents = { "Armor" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	object_class = "Armor",
	RepairCost = 10,
	Degradation = 0,
	Icon = "UI/Icons/Items/leather_jacket",
	DisplayName = T(401256529188, "Кожаный жилет"),
	DisplayNamePlural = T(245710665922, "Кожаные жилеты"),
	Description = T(509587299532, "Кожаная байкерская жилетка. Гвоздь никогда с ней не расстается, так что рассмотреть вблизи, что она из себя представляет, увы, не получается."),
	AdditionalHint = T(640774197340, "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> На спине вышит символ «Всадников смерти»\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Притягивает женщин и драки"),
	locked = true,
	RestockWeight = 0,
	Slot = "HeadGear",
	DamageReduction = 20,
	AdditionalReduction = 0,
	ProtectedBodyParts = set( "Torso" ),
	ArmorRating = 8,
}

