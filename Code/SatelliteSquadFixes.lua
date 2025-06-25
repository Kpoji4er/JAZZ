function NetSyncEvents.SquadCancelTravel(squad_id, keepJoiningSquad, force)
	local self = gv_Squads[squad_id]
	if not self then return end
	if not force and (SquadTravelCancelled(self) or not IsSquadTravelling(self, "skip_satellite_tick")) then
		return
	end

	local route = false
	-- If cancelling on a shortcut just stop after it
	-- todo: should we maybe backtrack?
	if IsTraversingShortcut(self) then
		route = {}
		route[1] = { self.route[1][1], shortcuts = { true } }
	-- Don't consider as water route if cancelling at last tile (which is supposed to be a land tile)
	elseif self.water_route and self.water_route[1] and self.water_route[1] ~= self.CurrentSector then
		route = {}
		route[1] = table.reverse(self.water_route)
		self.returning_water_travel = true
	-- If currently not centered then return to center
	elseif not IsSquadInSectorVisually(self, self.CurrentSector) then
		route = {}
		route[1] = {self.CurrentSector, ["returning_land_travel"] = true}
	end

	local visualPos = g_SatelliteUI and g_SatelliteUI.squad_to_wnd[self.UniqueId] and g_SatelliteUI.squad_to_wnd[self.UniqueId]:GetVisualPos()
	NetSyncEvents.AssignSatelliteSquadRoute(self.UniqueId, route, keepJoiningSquad, visualPos, true)
end
