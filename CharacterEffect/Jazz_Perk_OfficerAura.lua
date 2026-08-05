UndefineClass('Jazz_Perk_OfficerAura')
DefineClass.Jazz_Perk_OfficerAura = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	comment = "AI officer command aura (source)",
	object_class = "Perk",
	unit_reactions = {},
	DisplayName = T(890000000006100, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura DisplayName]] "Командная аура"),
	Description = T(890000000006101, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura Description]] "Этот командир отдаёт приказы союзникам поблизости."),
	AddEffectText = T(890000000006102, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAura AddEffectText]] "Отдаёт приказы"),
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Jazz_OfficerAura.png",
	Tier = "System",
	RemoveOnEndCombat = true,
	Shown = true,
}

-- File-local: avoid PropertyObject dynamic-member assert on instances.
local l_desc_reentry = false

-- Raw preset Description (T), never via ResolveValue/GetProperty — those re-enter
-- GetDescription after Jazz ResolveValue("Description") and double-append the order line.
local function JazzOfficerAuraRawDescription(effect)
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

-- Combat-badge INFO (MercStatusEffectsMoreInfo) renders T("<Description>") via
-- ResolveValue("Description") → GetProperty("Description"). It never calls GetDescription
-- unless a GetDescription method exists — then PropObjGetProperty re-enters it.
function Jazz_Perk_OfficerAura:ResolveValue(key)
	if key == "Description" then
		return self:GetDescription()
	end
	return CharacterEffect.ResolveValue(self, key)
end

function Jazz_Perk_OfficerAura:GetDescription()
	if l_desc_reentry then
		return JazzOfficerAuraRawDescription(self)
	end
	l_desc_reentry = true
	local base = JazzOfficerAuraRawDescription(self)
	local format = rawget(_G, "JazzAI_FormatOfficerAuraDescription")
	local result = base
	if type(format) == "function" then
		result = format(self, base, "source")
	end
	l_desc_reentry = false
	return result
end
