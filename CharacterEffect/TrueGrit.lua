UndefineClass('TrueGrit')
DefineClass.TrueGrit = {
	__parents = { "Perk" },
	__generated_by_class = "ModItemCharacterEffectCompositeDef",


	object_class = "Perk",
	unit_reactions = {
		PlaceObj('UnitReaction', {
			Event = "OnEndTurn",
			Handler = function (self, target)
				-- out of cover buff
				if not target:IsUsingCover() and g_Combat:AreEnemiesAware(g_CurrentTeam) then
					target:ApplyTempHitPoints(self:ResolveValue("outOfCoverGrit"))
				end
				
				-- next to enemy buff
				local nearestEnemy = GetNearestEnemy(target)
				if nearestEnemy and target:IsAdjacentTo(nearestEnemy) then
					target:ApplyTempHitPoints(self:ResolveValue("nextToEnemyGrit"))
				end
			end,
		}),
	},
	DisplayName = T(551122384582, --[[ModItemCharacterEffectCompositeDef TrueGrit DisplayName]] "Vanguard"),
	Description = T(835802440630, --[[ModItemCharacterEffectCompositeDef TrueGrit Description]] "Вам дается <color EmStyle>Сила воли</color> (<color EmStyle><outOfCoverGrit></color>), если вы заканчиваете ход вне <color EmStyle>укрытия</color>.\n\nВам дается <color EmStyle>Сила воли</color> (<color EmStyle><nextToEnemyGrit></color>), если вы заканчиваете ход <color EmStyle>вплотную</color> к врагу."),
	Icon = "UI/Icons/Perks/ContestGround",
	Tier = "Silver",
	Stat = "Health",
	StatValue = 80,
}

