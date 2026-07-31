UndefineClass('Jazz_Perk_Lynx')
DefineClass.Jazz_Perk_Lynx = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	-- Sight bonus lives in Code/System_OR_Unit.lua (+Jazz_LynxSightBonus).
	-- The same value softens Range/Bullet Drop CTH: vision is the accuracy buff.
	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnModifyCTHModifier",
			Handler = function (self, target, id, attacker, attack_target, action, weapon1, weapon2, data)
				if target ~= attacker or id ~= "Range" then
					return
				end
				local vision = rawget(_G, "Jazz_LynxSightBonus") or 8
				data.mod_add = (data.mod_add or 0) + vision
				if data.meta_text then
					data.meta_text[#data.meta_text + 1] = T{776394275735, "Perk: <name>", name = self.DisplayName}
				end
			end,
		}),
	},
	DisplayName = T(623665702916, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Lynx DisplayName]] "Рысий взгляд"),
	Description = T(890000000000868, --[[ModItemCharacterEffectCompositeDef Jazz_Perk_Lynx Description]] "Днём увеличен обзор. Это зрение также снижает штрафы меткости за дальность."),
	Icon = "Mod/e6L4ECj/Perks/Personal/Lynx.png",
	Tier = "Personal",
}
