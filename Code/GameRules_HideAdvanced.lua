-- Hide all vanilla Advanced Game Rules from New Game / Options.
-- Rules stay in GameRuleDefs so IsGameRuleActive still works for old saves;
-- players cannot enable them on a new run under JAZZ.

function OnMsg.DataLoaded()
	ForEachPreset("GameRuleDef", function(rule)
		if rule.advanced then
			rule.show_in_new_game = false
			rule.option = false
		end
	end)
end
