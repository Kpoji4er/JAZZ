UndefineClass('Merc_AnnieDubois_Perk')
DefineClass.Merc_AnnieDubois_Perk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Character Effect for Annie Dubois",
	object_class = "Perk",
	msg_reactions = {
		PlaceObj('MsgReaction', {
			Event = "OnKill",
			Handler = function (self, attacker, killedUnits)
				local reaction_idx = table.find(self.msg_reactions or empty_table, "Event", "OnKill")
				if not reaction_idx then return end
				
				local function exec(self, attacker, killedUnits)
				if HasPerk(attacker, self.id) then
					attacker:AddStatusEffect("Inspired")
				end
				end
				local id = GetCharacterEffectId(self)
				
				if id then
					if IsKindOf(attacker, "StatusEffectObject") and attacker:HasStatusEffect(id) then
						exec(self, attacker, killedUnits)
					end
				else
					exec(self, attacker, killedUnits)
				end
				
			end,
			HandlerCode = function (self, attacker, killedUnits)
				if HasPerk(attacker, self.id) then
					attacker:AddStatusEffect("Inspired")
				end
			end,
			param_bindings = false,
		}),
	},
	Conditions = {},
	DisplayName = T(285234191511, --[[ModItemCharacterEffectCompositeDef Merc_AnnieDubois_Perk DisplayName]] "Femme Fatale"),
	Description = T(961103911917, --[[ModItemCharacterEffectCompositeDef Merc_AnnieDubois_Perk Description]] "Whenever <color EmStyle>Annie</color> eliminates an enemy, she becomes <color EmStyle>Inspired</color>."),
	Icon = "Mod/e6L4ECj/Images/WorkshopMercs/Annie_Perk.png",
	Tier = "Personal",
}

