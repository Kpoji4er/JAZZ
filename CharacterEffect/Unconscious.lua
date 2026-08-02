UndefineClass('Unconscious')
DefineClass.Unconscious = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnBeginTurn",
			Handler = function (self, target)
				local recovery_turn = self:ResolveValue("recovery_turn")
				local stabilized = target:GetStatusEffect("Stabilized")
				local rally = stabilized and stabilized:ResolveValue("stabilized")
				if not rally and g_Combat and g_Combat.current_turn >= recovery_turn then
					rally = RollSkillCheck(target, "Health", 50)
				end
				if rally and target:IsDowned() then
					target:SetCommand("DownedRally")
				end
			end,
		}),
		PlaceObj('UnitReaction', {
			Event = "OnExplorationTick",
			Handler = function (self, target)
				local recovery = self:ResolveValue("recovery_time") 
				if not target:IsDead() and GameTime() >= recovery then
					target:SetTired(const.utExhausted)
					target:SetCommand("DownedRally")
				end
			end,
		}),
	},
	DisplayName = T(132204403941, --[[ModItemCharacterEffectCompositeDef Unconscious DisplayName]] "Unconscious"),
	Description = T(801008446056, --[[ModItemCharacterEffectCompositeDef Unconscious Description]] "Unconscious and unable to take any action. "),
	AddEffectText = T(319734703137, --[[ModItemCharacterEffectCompositeDef Unconscious AddEffectText]] "<color EmStyle><DisplayName></color> без сознания"),
	RemoveEffectText = T(483912406649, --[[ModItemCharacterEffectCompositeDef Unconscious RemoveEffectText]] "<color EmStyle><DisplayName></color> приходит в себя"),
	OnAdded = function (self, obj)
		self:SetParameter("recovery_turn", (g_Combat and g_Combat.current_turn or 1) + self:ResolveValue("recovery_delay_turns"))
		self:SetParameter("recovery_time", GameTime() + self:ResolveValue("recovery_delay_seconds") * 1000)
		obj:AddStatusEffectImmunity("Surprised", self.class)
		if IsMerc(obj) then
			JazzApplyKnockoutTraumaPackage(obj)
		end
		CreateGameTimeThread(obj.SetCommandIfNotDead, obj, obj.command == "GetDowned" and "Downed" or "KnockDown")
	end,
	OnRemoved = function (self, obj)
		obj:RemoveStatusEffectImmunity("Surprised", self.class)
		if obj.command == "Downed" then
			obj:SetCommand("DownedRally")
		else
			obj:SetTired(Min(obj.Tiredness, const.utExhausted))
		end
	end,
	Icon = "UI/Hud/Status effects/unconscious",
	Shown = true,
	ShownSatelliteView = true,
	HasFloatingText = true,
}

