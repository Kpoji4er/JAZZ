UndefineClass('Jazz_MakeThemBleedBuff')
DefineClass.Jazz_MakeThemBleedBuff = {
	__parents = { "CharacterEffect" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "CharacterEffect",
	DisplayName = T(890000000009863, --[[ModItemCharacterEffectCompositeDef Jazz_MakeThemBleedBuff DisplayName]] "Кровавый след"),
	Description = T(890000000009864, --[[ModItemCharacterEffectCompositeDef Jazz_MakeThemBleedBuff Description]] "Видимые враги с кровотечением: <em><stacks></em> (+10% урона за каждого, макс. +50%)."),
	type = "Buff",
	Icon = "Mod/e6L4ECj/Icons/StatusEffects/Jazz_MakeThemBleedBuff.png",
	max_stacks = 5,
	RemoveOnEndCombat = true,
	Shown = true,
}
