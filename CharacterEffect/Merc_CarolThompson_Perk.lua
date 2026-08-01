UndefineClass('Merc_CarolThompson_Perk')
DefineClass.Merc_CarolThompson_Perk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	msg_reactions = {
		PlaceObj('MsgReaction', {
			Event = "NewHour",
			Handler = function (self)
				local reaction_idx = table.find(self.msg_reactions or empty_table, "Event", "NewHour")
				if not reaction_idx then return end
				
				local function exec(self)
				local unit = gv_UnitData["Merc_CarolThompson"]
				unit = unit.HireStatus == "Hired" and unit
				if unit then
					local conditionPerHour = self:ResolveValue("Merc_CarolThompson_ConditionPerHour")
					local armor = unit:GetEquipedArmour()
					for _, item in ipairs(armor) do
						if item.Repairable and item.Condition < 100 then
							item.Condition = item.Condition + conditionPerHour
						end
					end
					
					local weapons = unit:GetHandheldItems()
					for _, item in ipairs(weapons) do
						if item.Repairable and item.Condition < 100 then
							item.Condition = item.Condition + conditionPerHour
						end
					end
				end
				end
				local id = GetCharacterEffectId(self)
				
				if id then
					local objs = {}
					for session_id, data in pairs(gv_UnitData) do
						local obj = g_Units[session_id] or data
						if obj:HasStatusEffect(id) then
							objs[session_id] = obj
						end
					end
					for _, obj in sorted_pairs(objs) do
						exec(self)
					end
				else
					exec(self)
				end
				
			end,
		}),
	},
	DisplayName = T(196588040075, --[[ModItemCharacterEffectCompositeDef Merc_CarolThompson_Perk DisplayName]] "Savvy Gearhead"),
	Description = T(607768359102, --[[ModItemCharacterEffectCompositeDef Merc_CarolThompson_Perk Description]] "<color EmStyle>Carol</color> repairs equipped <color EmStyle>Weapons</color>, <color EmStyle>Armor</color> and <color EmStyle>Items</color> automatically over time."),
	Icon = "Mod/e6L4ECj/Images/WorkshopMercs/Carol_Perk.png",
	Tier = "Personal",
}

