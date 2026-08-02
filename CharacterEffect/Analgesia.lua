UndefineClass('Analgesia')
DefineClass.Analgesia = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	DisplayName = T(890000000009204, "Analgesia"),
	Description = T(890000000009205, "Suppresses AP and chance-to-hit penalties from Pain. Does not stop bleeding or heal injuries."),
	type = "Buff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Analgesia.png",
	RemoveOnEndCombat = true,
	Shown = true,
	ShownSatelliteView = true,
}
