UndefineClass('Merc_JerrySinclair_Perk')
DefineClass.Merc_JerrySinclair_Perk = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	comment = "Character Effect for Jerry Sinclair",
	object_class = "Perk",
	msg_reactions = {
		PlaceObj('MsgReaction', {
			Event = "NewDay",
			Handler = function (self)
				local reaction_idx = table.find(self.msg_reactions or empty_table, "Event", "NewDay")
				if not reaction_idx then return end
				
				local function exec(self)
				local unit = gv_UnitData["Merc_JerrySinclair"]
				if unit.HireStatus == "Hired" then
					local tracker = unit:GetStatusEffect("Merc_JerrySinclair_Perk")
					if not tracker or Game.CampaignTime >= tracker.CampaignTimeAdded + self:ResolveValue("Merc_JerrySinclair_hoursToProduce") * const.Scale.h then	
						local amountToReceive = self:ResolveValue("Merc_JerrySinclair_amountToReceive")
						unit:RemoveStatusEffect("Merc_JerrySinclair_Perk")
						unit:AddStatusEffect("Merc_JerrySinclair_Perk")
						local item_name = amountToReceive > 1 and g_Classes["Merc_JerrySinclair_40mmTB"].DisplayNamePlural or  g_Classes["Merc_JerrySinclair_40mmTB"].DisplayName
						local canPlaceError = CanPlaceItemInInventory("Merc_JerrySinclair_40mmTB", amountToReceive, unit)
						if canPlaceError then
							CombatLog("important", T{251718627996, "<merc> received <amount> <item_name> but inventory is full.", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
							return
						end
						PlaceItemInInventory("Merc_JerrySinclair_40mmTB", amountToReceive, unit)
						CombatLog("important", T{272759676645, "<merc> received <amount> <item_name>", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
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
				local unit = gv_UnitData["Merc_JerrySinclair"]
				if unit.HireStatus == "Hired" then
					local tracker = unit:GetStatusEffect("Merc_JerrySinclair_Perk")
					if not tracker or Game.CampaignTime >= tracker.CampaignTimeAdded + self:ResolveValue("Merc_JerrySinclair_hoursToProduce") * const.Scale.h then	
						local amountToReceive = self:ResolveValue("Merc_JerrySinclair_amountToReceive")
						unit:RemoveStatusEffect("Merc_JerrySinclair_Perk")
						unit:AddStatusEffect("Merc_JerrySinclair_Perk")
						local item_name = amountToReceive > 1 and g_Classes["Merc_JerrySinclair_40mmTB"].DisplayNamePlural or  g_Classes["Merc_JerrySinclair_40mmTB"].DisplayName
						local canPlaceError = CanPlaceItemInInventory("Merc_JerrySinclair_40mmTB", amountToReceive, unit)
						if canPlaceError then
							CombatLog("important", T{251718627996, "<merc> received <amount> <item_name> but inventory is full.", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
							return
						end
						PlaceItemInInventory("Merc_JerrySinclair_40mmTB", amountToReceive, unit)
						CombatLog("important", T{272759676645, "<merc> received <amount> <item_name>", merc = unit.Nick, amount = amountToReceive,item_name = item_name})
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
				obj:AddStatusEffect("Merc_JerrySinclair_Perk")
				end
				local _id = GetCharacterEffectId(self)
				if _id == id then exec(self, obj, id, stacks) end
				
			end,
			HandlerCode = function (self, obj, id, stacks)
				obj:AddStatusEffect("Merc_JerrySinclair_Perk")
			end,
			param_bindings = false,
		}),
	},
	DisplayName = T(268650586874, --[[ModItemCharacterEffectCompositeDef Merc_JerrySinclair_Perk DisplayName]] "Grenade Tinkerer"),
	Description = T(861875679464, --[[ModItemCharacterEffectCompositeDef Merc_JerrySinclair_Perk Description]] "<color EmStyle>Jerry</color> produces two <color EmStyle>40-mm-TB Grenades</color> every <color EmStyle>7 days</color>."),
	Icon = "Mod/e6L4ECj/Images/WorkshopMercs/Jerry_Perk.png",
	Tier = "Personal",
}

