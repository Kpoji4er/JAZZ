UndefineClass('Jazz_Perk_OfficerAuraInfluence')
DefineClass.Jazz_Perk_OfficerAuraInfluence = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	comment = "AI officer aura receiver",
	object_class = "Perk",
	unit_reactions = {},
	DisplayName = T(890000000006103, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence DisplayName]] "Под влиянием ауры"),
	Description = T(890000000006104, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence Description]] "Боец следует приказам командира. Эффект снимается, если командир погиб или боец вышел из зоны влияния."),
	AddEffectText = T(890000000006105, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence AddEffectText]] "Под приказом"),
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Jazz_OfficerAuraInfluence.png",
	Tier = "System",
	RemoveOnEndCombat = true,
	Shown = true,
}

local l_desc_reentry = false

local function JazzOfficerAuraInfluenceRawDescription(effect)
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

-- Same UI path as Jazz_Perk_OfficerAura: rollover binds <Description>, not GetDescription.
function Jazz_Perk_OfficerAuraInfluence:ResolveValue(key)
	if key == "Description" then
		return self:GetDescription()
	end
	return CharacterEffect.ResolveValue(self, key)
end

function Jazz_Perk_OfficerAuraInfluence:GetDescription()
	if l_desc_reentry then
		return JazzOfficerAuraInfluenceRawDescription(self)
	end
	l_desc_reentry = true
	local base = JazzOfficerAuraInfluenceRawDescription(self)
	local format = rawget(_G, "JazzAI_FormatOfficerAuraDescription")
	local result = base
	if type(format) == "function" then
		result = format(self, base, "influence")
	end
	l_desc_reentry = false
	return result
end
