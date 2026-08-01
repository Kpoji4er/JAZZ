UndefineClass('Merc_SamuelNkosi_Perk')
DefineClass.Merc_SamuelNkosi_Perk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Custom Perk for Samuel Nkosi",
	object_class = "Perk",
	msg_reactions = {
		PlaceObj('MsgReaction', {
			Event = "GatherDamageModifications",
			Handler = function (self, attacker, target, attack_args, hit_descr, mod_data)
				local reaction_idx = table.find(self.msg_reactions or empty_table, "Event", "GatherDamageModifications")
				if not reaction_idx then return end
				
				local function exec(self, attacker, target, attack_args, hit_descr, mod_data)
				if not hit_descr.aoe and attack_args.opportunity_attack_type == "Overwatch" and IsKindOf(target, "Unit") then
					local bonus = self:ResolveValue("Merc_SamuelNkosi_DamageBonus")
					mod_data.base_damage = MulDivRound(mod_data.base_damage, 100 + bonus, 100)
					mod_data.breakdown[#mod_data.breakdown + 1] = { name = self.DisplayName, value = bonus }
				end
				end
				local id = GetCharacterEffectId(self)
				
				if id then
					if IsKindOf(attacker, "StatusEffectObject") and attacker:HasStatusEffect(id) then
						exec(self, attacker, target, attack_args, hit_descr, mod_data)
					end
				else
					exec(self, attacker, target, attack_args, hit_descr, mod_data)
				end
				
			end,
			HandlerCode = function (self, attacker, target, attack_args, hit_descr, mod_data)
				if not hit_descr.aoe and attack_args.opportunity_attack_type == "Overwatch" and IsKindOf(target, "Unit") then
					local bonus = self:ResolveValue("Merc_SamuelNkosi_DamageBonus")
					mod_data.base_damage = MulDivRound(mod_data.base_damage, 100 + bonus, 100)
					mod_data.breakdown[#mod_data.breakdown + 1] = { name = self.DisplayName, value = bonus }
				end
			end,
			param_bindings = false,
		}),
	},
	DisplayName = T(142999241799, --[[ModItemCharacterEffectCompositeDef Merc_SamuelNkosi_Perk DisplayName]] "Overwatch Expert"),
	Description = T(390711016208, --[[ModItemCharacterEffectCompositeDef Merc_SamuelNkosi_Perk Description]] "<color EmStyle>Samuel</color> inflicts <color EmStyle>+30%</color> bonus damage with attacks during <color EmStyle>Overwatch</color>."),
	Icon = "Mod/e6L4ECj/Images/WorkshopMercs/Samuel_Perk.png",
	Tier = "Personal",
}

