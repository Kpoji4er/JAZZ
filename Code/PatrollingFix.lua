-- Patroling enemy squads
--function PatrollingSquadSetDestination(squadId)
--	local squad = gv_Squads[squadId]
--	local enemySquadDef = EnemySquadDefs[squad.enemy_squad_def]
--	if enemySquadDef and enemySquadDef.patrolling then
--		local waypoints = table.icopy(enemySquadDef.waypoints)
--		if waypoints and #waypoints > 0 then
--			table.remove_value(waypoints, squad.CurrentSector)
--			if #waypoints > 0 then
--				local nextDest = InteractionRand(#waypoints, "PatrollingSquads") + 1
--				nextDest = waypoints[nextDest]
--			
--				local route = GenerateRouteDijkstra(squad.CurrentSector, nextDest, false, squad.units, "land_water", nil, squad.Side)
--				NetSyncEvent("AssignSatelliteSquadRoute", squadId, {route})
--			else 
--				table.shuffle(enemySquadDef.waypoints, self:Random(#waypoints))
--				waypoints = table.icopy(enemySquadDef.waypoints)
--				PatrollingSquadSetDestination(squadId)
--			end
--		end
--	end
--end

function PatrollingSquadSetDestination(squadId)
	local squad = gv_Squads[squadId]
	local enemySquadDef = EnemySquadDefs[squad.enemy_squad_def]
	if enemySquadDef and enemySquadDef.patrolling then
		local waypoints = table.icopy(enemySquadDef.waypoints)
		if waypoints and #waypoints > 0 then
			--table.remove_value(waypoints, squad.CurrentSector)
			if #waypoints > 0 then
				local nextDest = InteractionRand(#waypoints, "PatrollingSquads") + 1
				nextDest = waypoints[nextDest]
			
				local route = GenerateRouteDijkstra(squad.CurrentSector, nextDest, false, squad.units, "land_water", nil, squad.Side)
				NetSyncEvent("AssignSatelliteSquadRoute", squadId, {route})
			end
		end
	end
end

--for , squad in ipairs(gv_Squads) do   
--	print(squad.UniqueID) end