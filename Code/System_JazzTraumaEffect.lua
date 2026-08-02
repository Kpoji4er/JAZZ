-- MED-001: load before CharacterEffect/Trauma* companions (see metadata.code).
-- Shared parent so trauma tooltips append progress-check text without
-- runtime GetDescription hook installers / global re-entry flags.

UndefineClass("JazzTraumaEffect")
DefineClass.JazzTraumaEffect = {
	__parents = { "StatusEffect" },
}

function JazzTraumaEffect:GetDescription()
	local base
	local ce = rawget(_G, "CharacterEffect")
	if type(ce) == "table" and type(ce.GetDescription) == "function" then
		base = ce.GetDescription(self)
	else
		base = self.Description
	end
	-- JazzFormatTraumaStatusDescription lives in Systems_Medicine (later in load order).
	local format = rawget(_G, "JazzFormatTraumaStatusDescription")
	if type(format) == "function" then
		return format(self, base)
	end
	return base
end
