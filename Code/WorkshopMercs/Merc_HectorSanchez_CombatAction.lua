PlaceObj('CombatAction', {
	ActionType = "Passive",
	Comment = "passive",
	ConfigurableKeybind = false,
	DisplayName = T(427751362832, --[[CombatAction Merc_HectorSanchez_Perk DisplayName]] "<placeholder>"),
	GetActionDescription = function (self, units)
		return GetSignatureActionDescription(self)
	end,
	GetActionDisplayName = function (self, units)
		return GetSignatureActionDisplayName(self)
	end,
	GetUIState = function (self, units, args)
		local unit = units[1]
		local cost = self:GetAPCost(unit, args)
		if cost < 0 then return "hidden" end
		if not unit:UIHasAP(cost) then return "disabled" end
		return "enabled"
	end,
	Icon = "Mod/e6L4ECj/Images/WorkshopMercs/Hector_Perk_Passive.png",
	KeybindingFromAction = "actionRedirectSignatureAbility",
	RequireState = "any",
	Run = function (self, unit, ap, ...)
		return false
	end,
	ShowIn = "SignatureAbilities",
	SortKey = 100,
	group = "SignatureAbilities",
	id = "Merc_HectorSanchez_Perk",
})