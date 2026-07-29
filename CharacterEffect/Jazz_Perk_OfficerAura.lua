UndefineClass('Jazz_Perk_OfficerAura')
DefineClass.Jazz_Perk_OfficerAura = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	comment = "AI officer command aura (source)",
	object_class = "Perk",
	unit_reactions = {},
	DisplayName = T(890000000006100, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura DisplayName]] "Командная аура"),
	Description = T(890000000006101, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura Description]] "Этот командир держит ауру приказа над союзниками в радиусе (сержант 15, лейтенант 25, капитан — вся карта).\n\nВозможные приказы: <em>Держать линию</em>, <em>Давить</em>, <em>Охват</em>, <em>Отход</em>, <em>Сосредоточить огонь</em>, <em>Низкая видимость — держать</em>. Приказ обновляется по обстановке."),
	AddEffectText = T(890000000006102, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura AddEffectText]] "Отдаёт приказы"),
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Jazz_OfficerAura.png",
	Tier = "System",
	RemoveOnEndCombat = true,
	Shown = true,
}
