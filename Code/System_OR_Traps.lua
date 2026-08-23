function ThrowableTrapItem:OnLand(thrower, attackResults, visual_obj)

	if self.TriggerType == "Contact" then
		Grenade.OnLand(self, thrower, attackResults, visual_obj)
		return
	end
	
	PushUnitAlert("thrown", visual_obj, thrower)

	-- <Unit> Heard a thud
	PushUnitAlert("noise", visual_obj, self.ThrowNoise, Presets.NoiseTypes.Default.ThrowableLandmine.display_name)

	local finalPointOfTrajectory = attackResults.explosion_pos	
	assert(finalPointOfTrajectory, "Where'd that grenade fall?")
	if not finalPointOfTrajectory then return end
	 
	local teamSide = thrower and thrower.team and thrower.team.side
	assert(teamSide)
	teamSide = teamSide or "player1"
	
	local newLandmine = PlaceObject("DynamicSpawnLandmine", {
		-- The landmine properties need to be set at init time
		TriggerType = self.TriggerType, 
		triggerRadius = (self.TriggerType == "Proximity" or self.TriggerType == "Proximity-Timed") and 1 or 0,
		TimedExplosiveTurns = self.TimedExplosiveTurns,
		DisplayName = self.DisplayName,
		triggerChance = self.triggerChance,
		fx_actor_class = self.class .. "_OnGround",
		item_thrown = self.class,
		team_side = teamSide,
		attacker = thrower,
	})
	
	if IsValid(visual_obj) then
		DoneObject(visual_obj)
	end

    if thrower:GetEffectValue("Jazz_Perk_00") then
        newLandmine.TimedExplosiveTurns = 0 end
	
	-- Copy explosive type config to the mine
	local explosiveTypePreset = self:GetExplosiveTypePreset()
	newLandmine:CopyProperties(explosiveTypePreset, TrapExplosionProperties:GetProperties())
	
	-- Add explosive skill to landmine damage.
	newLandmine.BaseDamage = thrower:GetBaseDamage(self)
	
	-- Throwable mines are seen by all
	newLandmine.discovered_by[teamSide] = true
	newLandmine:SetPos(finalPointOfTrajectory)
	newLandmine:EnterSectorInit()
	VisibilityUpdate(true)

   -- newLandmine.toExplode = true

	table.iclear(attackResults)
	attackResults.trap_placed = true
end

-- JAZZ-INV-004: successful Landmine disarm may salvage a placeable charge.
local Jazz_MineThrownToCharge = {
	ProximityC4 = "C4",
	TimedC4 = "C4",
	RemoteC4 = "C4",
	ProximityTNT = "TNT",
	TimedTNT = "TNT",
	RemoteTNT = "TNT",
	ProximityPETN = "PETN",
	TimedPETN = "PETN",
	RemotePETN = "PETN",
}

local Jazz_MineChargeWeights = {
	{ 60, "TNT" },
	{ 30, "C4" },
	{ 10, "PETN" },
}

function Jazz_TrySalvageMineCharge(trap, unit)
	if not trap or not unit or not unit.Squad then
		return
	end
	if not IsKindOf(trap, "Landmine") then
		return
	end
	local roll = unit:Random(100)
	if roll >= 40 then
		return
	end
	local item_id = Jazz_MineThrownToCharge[rawget(trap, "item_thrown") or false]
	if not item_id then
		item_id = GetWeightedRandom(Jazz_MineChargeWeights, unit:Random()) or "TNT"
	end
	AddItemToSquadBag(unit.Squad, item_id, 1)
	local defs = rawget(_G, "InventoryItemDefs")
	local def = type(defs) == "table" and defs[item_id]
	local name = def and def.DisplayName
	if name then
		CreateFloatingText(unit:GetVisualPos(), name)
	end
end

function OnMsg.TrapDisarm(trap, unit, success, stat)
	if not success then
		return
	end
	Jazz_TrySalvageMineCharge(trap, unit)
end