UndefineClass('GutHookKnife')
DefineClass.GutHookKnife = {
	__parents = { "MeleeWeapon" },
	__generated_by_class = "ModItemInventoryItemCompositeDef",


	comment = "Омрыновский",
	object_class = "MeleeWeapon",
	ScrapParts = 2,
	Reliability = 50,
	Icon = "UI/Icons/Weapons/GutHookKnife",
	DisplayName = T(271517940366, --[[ModItemInventoryItemCompositeDef GutHookKnife DisplayName]] "Gut Hook Knife"),
	DisplayNamePlural = T(947457047925, --[[ModItemInventoryItemCompositeDef GutHookKnife DisplayNamePlural]] "Gut Hook Knives"),
	Description = T(322627335890, --[[ModItemInventoryItemCompositeDef GutHookKnife Description]] "Специальным шкуродером такой опытный охотник, как Омрын может освежевать оленя за пятнадцать минут."),
	AdditionalHint = T(403761935169, --[[ModItemInventoryItemCompositeDef GutHookKnife AdditionalHint]] "<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Вызывает <color EmStyle>кровотечение</color>\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Низкая цена атаки\n<image UI/Conversation/T_Dialogue_IconBackgroundCircle.tga 400 130 128 120> Увеличенная эффективность прицеливания"),
	UnitStat = "Dexterity",
	Cost = 150,
	RestockWeight = 0,
	BaseChanceToHit = 100,
	CritChanceScaled = 40,
	BaseDamage = 26,
	AimAccuracy = 20,
	PenetrationClass = 4,
	DamageMultiplier = 110,
	AttackAP = 3000,
	MaxAimActions = 1,
	Noise = 1,
	Entity = "Weapon_FC_AMZ_Knife_01",
	HolsterSlot = "Leg",
}

