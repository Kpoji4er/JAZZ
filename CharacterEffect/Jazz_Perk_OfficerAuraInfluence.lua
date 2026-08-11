UndefineClass('Jazz_Perk_OfficerAuraInfluence')
DefineClass.Jazz_Perk_OfficerAuraInfluence = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",

	comment = "AI officer aura receiver",
	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnCalcChanceToHit",
			Handler = function (self, target, attacker, action, attack_target, weapon1, weapon2, data)
				local directive
				if self.InstParameters then
					local found = table.find_value(self.InstParameters, "Name", "directive")
					if found then
						directive = found.Value
					end
				end
				if not directive and JazzAI_GetEffectDirective then
					directive = JazzAI_GetEffectDirective(self)
				end
				if not directive then
					return
				end
				if target == attacker then
					local bonus = JazzAI_GetDirectiveCthAttackBonus and JazzAI_GetDirectiveCthAttackBonus(directive) or 0
					if bonus > 0 then
						ApplyCthModifier_Add(self, data, bonus)
					end
				elseif attack_target == target and attacker and attacker ~= target then
					local def = JazzAI_GetDirectiveCthDefenseBonus and JazzAI_GetDirectiveCthDefenseBonus(directive) or 0
					if def > 0 then
						ApplyCthModifier_Add(self, data, -def)
					end
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local directive
				if self.InstParameters then
					local found = table.find_value(self.InstParameters, "Name", "directive")
					if found then
						directive = found.Value
					end
				end
				if not directive and JazzAI_GetEffectDirective then
					directive = JazzAI_GetEffectDirective(self)
				end
				local ap = JazzAI_GetDirectiveApBonus and JazzAI_GetDirectiveApBonus(directive) or 0
				if ap > 0 and IsValid(target) then
					target:GainAP(ap * const.Scale.AP)
				end
			end,
		}),
	},
	DisplayName = T(890000000006103, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence DisplayName]] "Под влиянием ауры"),
	Description = T(890000000006104, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_OfficerAuraInfluence Description]] "Боец следует приказам командира и получает небольшой бонус текущего приказа. Эффект снимается, если командир погиб или боец вышел из зоны влияния."),
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

-- Same as Jazz_Perk_OfficerAura: format in ResolveValue only; GetDescription = raw for save.
local function JazzOfficerAuraInfluenceFormattedDescription(effect)
	if l_desc_reentry then
		return JazzOfficerAuraInfluenceRawDescription(effect)
	end
	l_desc_reentry = true
	local base = JazzOfficerAuraInfluenceRawDescription(effect)
	local format = rawget(_G, "JazzAI_FormatOfficerAuraDescription")
	local result = base
	if type(format) == "function" then
		result = format(effect, base, "influence")
	end
	l_desc_reentry = false
	return result
end

function Jazz_Perk_OfficerAuraInfluence:ResolveValue(key)
	if key == "Description" then
		return JazzOfficerAuraInfluenceFormattedDescription(self)
	end
	return CharacterEffect.ResolveValue(self, key)
end

function Jazz_Perk_OfficerAuraInfluence:GetDescription()
	return JazzOfficerAuraInfluenceRawDescription(self)
end
