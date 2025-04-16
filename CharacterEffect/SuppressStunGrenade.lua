UndefineClass('SuppressStunGrenade')
DefineClass.SuppressStunGrenade = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	unit_reactions = {},
	DisplayName = T(609065847626, --[[ModItemCharacterEffectCompositeDef SuppressStunGrenade DisplayName]] "Подавление сш гранатой"),
	Description = "",
	OnAdded = function (self, obj)
		local willPointsDamage = 40
		
		obj.WillPoints = obj.WillPoints - MulDivRound(100-Unit:StunGrenadeProtection(),willPointsDamage,100)
		obj:ApplySuppressionStatus()
	end,
	OnRemoved = function (self, obj)  end,
	lifetime = "Until End of Turn",
	Icon = "UI/Hud/Status effects/unconscious",
	max_stacks = 2,
}

