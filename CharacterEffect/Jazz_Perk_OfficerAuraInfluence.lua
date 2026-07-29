UndefineClass('Jazz_Perk_OfficerAuraInfluence')
DefineClass.Jazz_Perk_OfficerAuraInfluence = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	comment = "AI officer aura receiver",
	object_class = "Perk",
	unit_reactions = {},
	DisplayName = T(890000000006103, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence DisplayName]] "Под влиянием ауры"),
	Description = T(890000000006104, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence Description]] "Боец в радиусе командирской ауры и следует текущему приказу отряда (удержание, натиск, охват и т.д.). Эффект снимается, если командир погиб или боец вышел из радиуса."),
	AddEffectText = T(890000000006105, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence AddEffectText]] "Под приказом"),
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Jazz_OfficerAuraInfluence.png",
	Tier = "System",
	RemoveOnEndCombat = true,
	Shown = true,
}
