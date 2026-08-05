-- MED-001: load before CharacterEffect/Trauma* companions (see metadata.code).
-- Shared parent so trauma tooltips append progress-check text without
-- runtime GetDescription hook installers / global re-entry flags.

UndefineClass("JazzTraumaEffect")
DefineClass.JazzTraumaEffect = {
	__parents = { "StatusEffect" },
}

-- File-local: avoid PropertyObject dynamic-member assert on instances.
local l_desc_reentry = false

-- Raw preset Description (T), never via ResolveValue/GetProperty — those re-enter
-- GetDescription after Jazz ResolveValue("Description") and double-append progress text.
function JazzTraumaRawDescription(effect)
	if not effect then
		return ""
	end
	local class_name = effect.class
	local def = CharacterEffectDefs and class_name and CharacterEffectDefs[class_name]
	if def then
		local d = rawget(def, "Description") or def.Description
		if d and d ~= "" then
			return d
		end
	end
	local cls = class_name and g_Classes and g_Classes[class_name]
	if cls then
		local d = rawget(cls, "Description") or cls.Description
		if d and d ~= "" then
			return d
		end
	end
	return ""
end

-- MercStatusEffectsMoreInfo / StatusEffectIcon use T("<Description>") → ResolveValue.
-- Vanilla CharacterEffect.ResolveValue → GetProperty(Description field) and never calls
-- GetDescription, so progress text must be injected here.
function JazzTraumaEffect:ResolveValue(key)
	if key == "Description" then
		return self:GetDescription()
	end
	return CharacterEffect.ResolveValue(self, key)
end

function JazzTraumaEffect:GetDescription()
	-- Re-entry guard: formatting ResolveValue/tag eval must not nest another format.
	if l_desc_reentry then
		return JazzTraumaRawDescription(self)
	end
	l_desc_reentry = true
	local base = JazzTraumaRawDescription(self)
	local format = rawget(_G, "JazzFormatTraumaStatusDescription")
	local result = base
	if type(format) == "function" then
		result = format(self, base)
	end
	l_desc_reentry = false
	return result
end
