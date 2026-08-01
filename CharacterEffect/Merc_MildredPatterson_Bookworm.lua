UndefineClass('Merc_MildredPatterson_Bookworm')
DefineClass.Merc_MildredPatterson_Bookworm = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Character Effect Bookworm for Milder Patterson Bookworm",
	object_class = "Perk",
	msg_reactions = {
		PlaceObj('MsgReaction', {
			Event = "NewDay",
			Handler = function (self)
				local reaction_idx = table.find(self.msg_reactions or empty_table, "Event", "NewDay")
				if not reaction_idx then return end
				
				local function exec(self)
				local unit = gv_UnitData["Merc_MildredPatterson"]
				if unit.HireStatus == "Hired" then
					local tracker = unit:GetStatusEffect("Merc_MildredPatterson_Bookworm")
					if not tracker or Game.CampaignTime >= tracker.CampaignTimeAdded + self:ResolveValue("Merc_MildredPatterson_hoursToProduce") * const.Scale.h then	
						local amountToReceive = self:ResolveValue("Merc_MildredPatterson_amountToReceive")
						unit:RemoveStatusEffect("Merc_MildredPatterson_Bookworm")
						unit:AddStatusEffect("Merc_MildredPatterson_Bookworm")
						local item_name = amountToReceive > 1 and g_Classes["SkillMag_Health"].DisplayNamePlural or  g_Classes["SkillMag_Health"].DisplayName
						local canPlaceError = CanPlaceItemInInventory("SkillMag_Health", amountToReceive, unit)
						if canPlaceError then
							CombatLog("important", T{899101854825, "<merc> received <amount> <item_name> but inventory is full.", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
							return
						end
						PlaceItemInInventory("SkillMag_Health", amountToReceive, unit)
						CombatLog("important", T{318623454402, "<merc> received <amount> <item_name>", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
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
			HandlerCode = function (self)
				local unit = gv_UnitData["Merc_MildredPatterson"]
				if unit.HireStatus == "Hired" then
					local tracker = unit:GetStatusEffect("Merc_MildredPatterson_Bookworm")
					if not tracker or Game.CampaignTime >= tracker.CampaignTimeAdded + self:ResolveValue("Merc_MildredPatterson_hoursToProduce") * const.Scale.h then	
						local amountToReceive = self:ResolveValue("Merc_MildredPatterson_amountToReceive")
						unit:RemoveStatusEffect("Merc_MildredPatterson_Bookworm")
						unit:AddStatusEffect("Merc_MildredPatterson_Bookworm")
						local item_name = amountToReceive > 1 and g_Classes["SkillMag_Health"].DisplayNamePlural or  g_Classes["SkillMag_Health"].DisplayName
						local canPlaceError = CanPlaceItemInInventory("SkillMag_Health", amountToReceive, unit)
						if canPlaceError then
							CombatLog("important", T{899101854825, "<merc> received <amount> <item_name> but inventory is full.", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
							return
						end
						PlaceItemInInventory("SkillMag_Health", amountToReceive, unit)
						CombatLog("important", T{318623454402, "<merc> received <amount> <item_name>", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
					end
				end
			end,
			param_bindings = false,
		}),
		PlaceObj('MsgReaction', {
			Event = "StatusEffectAdded",
			Handler = function (self, obj, id, stacks)
				local reaction_idx = table.find(self.msg_reactions or empty_table, "Event", "StatusEffectAdded")
				if not reaction_idx then return end
				
				local function exec(self, obj, id, stacks)
				obj:AddStatusEffect("Merc_MildredPatterson_Bookworm")
				end
				local _id = GetCharacterEffectId(self)
				if _id == id then exec(self, obj, id, stacks) end
				
			end,
			HandlerCode = function (self, obj, id, stacks)
				obj:AddStatusEffect("Merc_MildredPatterson_Bookworm")
			end,
			param_bindings = false,
		}),
	},
	Modifiers = {},
	DisplayName = T(526647186745, --[[ModItemCharacterEffectCompositeDef Merc_MildredPatterson_Bookworm DisplayName]] "Bookworm"),
	Description = T(373439154061, --[[ModItemCharacterEffectCompositeDef Merc_MildredPatterson_Bookworm Description]] 'As lifetime member of the reading circle "Doctors Without Borders" <color EmStyle>Mildred</color> receives one skill magazine <color EmStyle>An Apple a Day</color> every <color EmStyle>7 days</color>.'),
	Icon = "Mod/e6L4ECj/Images/WorkshopMercs/Mildred_Perk.png",
	Tier = "Personal",
}

