# Party combat status parity with satellite (ShownSatelliteView).
# Does NOT add icons next to CombatBadge nick — those stay under the HP bar only.
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "items.lua"
text = path.read_text(encoding="utf-8")

old_arr = "'array', function (parent, context) return context.Wounded and { context[context.Wounded] } or empty_table end,"
new_arr = "'array', function (parent, context) return JazzGetPartyPortraitStatusEffects(context) end,"
c1 = text.count(old_arr)
text = text.replace(old_arr, new_arr)

old_pair = """PlaceObj('XTemplateTemplate', {
														'__context', function (parent, context) return table.find_value(context, "class", "Wounded") end,
														'__condition', function (parent, context) return not not context end,
														'__template', "StatusEffectIcon",
													}),
													PlaceObj('XTemplateTemplate', {
														'__context', function (parent, context) return table.find_value(context, "class", "Tired") or table.find_value(context, "class", "Exhausted") end,
														'__condition', function (parent, context) return not not context end,
														'__template', "StatusEffectIcon",
													}),"""
new_pair = """PlaceObj('XTemplateForEach', {
														'comment', "ShownSatelliteView statuses (combat party parity with satellite)",
														'array', function (parent, context) return JazzGetPartyPortraitStatusEffects(context) end,
														'__context', function (parent, context, item, i, n) return item end,
													}, {
														PlaceObj('XTemplateTemplate', {
															'__condition', function (parent, context) return not not context end,
															'__template', "StatusEffectIcon",
														}),
														}),"""
old_pair3 = """PlaceObj('XTemplateTemplate', {
															'__context', function (parent, context) return table.find_value(context, "class", "Wounded") end,
															'__condition', function (parent, context) return not not context end,
															'__template', "StatusEffectIcon",
														}),
														PlaceObj('XTemplateTemplate', {
															'__context', function (parent, context) return table.find_value(context, "class", "Tired") or table.find_value(context, "class", "Exhausted") end,
															'__condition', function (parent, context) return not not context end,
															'__template', "StatusEffectIcon",
														}),"""
new_pair3 = """PlaceObj('XTemplateForEach', {
															'comment', "ShownSatelliteView statuses (combat party parity with satellite)",
															'array', function (parent, context) return JazzGetPartyPortraitStatusEffects(context) end,
															'__context', function (parent, context, item, i, n) return item end,
														}, {
															PlaceObj('XTemplateTemplate', {
																'__condition', function (parent, context) return not not context end,
																'__template', "StatusEffectIcon",
															}),
															}),"""
c2 = text.count(old_pair)
c3 = text.count(old_pair3)
text = text.replace(old_pair, new_pair).replace(old_pair3, new_pair3)

# Strip nick-adjacent critical icons if a previous run added them.
old_critical = """PlaceObj('XTemplateWindow', {
								'__context', function (parent, context) return context.StatusEffects end,
								'__condition', function (parent, context) return IsKindOf(parent:ResolveId("node").context, "StatusEffectObject") end,
								'__class', "XContentTemplate",
								'Id', "idCriticalStatusEffects",
								'HAlign', "left",
								'VAlign', "center",
								'LayoutMethod', "HList",
								'UseClipBox', false,
								'FoldWhenHidden', true,
								'ChildrenHandleMouse', false,
							}, {
								PlaceObj('XTemplateForEach', {
									'comment', "top critical statuses next to nick",
									'array', function (parent, context) return JazzGetCriticalBadgeStatusEffects(parent:ResolveId("node").context, 3) end,
									'__context', function (parent, context, item, i, n) return item end,
								}, {
									PlaceObj('XTemplateTemplate', {
										'__template', "StatusEffectIcon",
										'RolloverTemplate', "",
										'RolloverText', "",
										'RolloverTitle', "",
										'MinWidth', 16,
										'MinHeight', 16,
										'MaxWidth', 16,
										'MaxHeight', 16,
										'ImageScale', point(700, 700),
									}),
									}),
								}),
"""
c_crit = text.count("'Id', \"idCriticalStatusEffects\"")
text = text.replace(old_critical, "")
# Also drop HList from name stripe if left from nick-icon experiment.
text = text.replace(
	"""'Id', "idNameStripe",
							'Padding', box(2, 2, 2, 2),
							'Dock', "top",
							'VAlign', "top",
							'LayoutMethod', "HList",
							'LayoutHSpacing', 2,
							'UseClipBox', false,""",
	"""'Id', "idNameStripe",
							'Padding', box(2, 2, 2, 2),
							'Dock', "top",
							'VAlign', "top",
							'UseClipBox', false,""",
)
text = text.replace(
	"'comment', \"only shows wounded effect\",",
	"'comment', \"ShownSatelliteView statuses (was wounded-only)\",",
)

print(f"arr={c1} pair={c2} pair3={c3} critical_ids={c_crit}")
path.write_text(text, encoding="utf-8")
print("OK")
