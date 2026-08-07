UndefineClass('WoundInfected')
DefineClass.WoundInfected = {
	__parents = { "StatusEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",
	object_class = "StatusEffect",
	DisplayName = T(890000000010300, "Infected Wound"),
	Description = T(890000000010301, "Festering wound. Progress checks on the campaign map: failure can be fatal. Heavy trauma that fails to improve may become infected."),
	AddEffectText = T(890000000010302, "<color EmStyle><DisplayName></color>"),
	OnAdded = function(self, obj)
		local init = rawget(_G, "JazzInitWoundInfectedProgressTimer")
		if type(init) == "function" then
			init(self)
		end
	end,
	type = "Debuff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/WoundInfected.png",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}
