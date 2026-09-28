UndefineClass('Jazz_Perk_OfficerAura')
DefineClass.Jazz_Perk_OfficerAura = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {},
	DisplayName = T(890000000006100, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura DisplayName]] "Командная аура"),
	Description = T(890000000006101, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura Description]] "Этот командир отдаёт приказы союзникам поблизости."),
	AddEffectText = T(890000000006102, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura AddEffectText]] "Отдаёт приказы"),
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Jazz_OfficerAura.png",
	RemoveOnEndCombat = true,
	Shown = true,
}

