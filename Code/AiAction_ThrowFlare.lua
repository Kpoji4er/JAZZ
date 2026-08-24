DefineClass.AIActionThrowFlare = {
    __parents = {"AIActionBaseZoneAttack"},
    properties = {
        {id = "MinDist", editor = "number", scale = "m", default = 2 * guim, min = 0},
        {id = "MaxDist", editor = "number", scale = "m", default = 100 * guim, min = 0},
        {id = "TargetLastAttackPos", editor = "bool", default = false}
    },
    hidden = false,
    voice_response = "AIThrowGrenade"
}

--- Find equipped or backpack FlareGun (signal pistol).
local function JazzAI_FindFlareGun(unit)
	if not IsValid(unit) then
		return
	end
	for _, slot in ipairs({"Handheld A", "Handheld B"}) do
		local gun = unit:GetItemInSlot(slot, "FlareGun")
		if gun then
			return gun, slot
		end
	end
	local found
	unit:ForEachItemInSlot("Inventory", function(item)
		if not found and IsKindOf(item, "FlareGun") and (item.Condition or 0) > 0 then
			found = item
		end
	end)
	return found, nil
end

--- Equip FlareGun into an empty hand and reload FlareAmmo; never displace a combat firearm.
local function JazzAI_EnsureFlareGunReady(unit, gun, slot)
	if slot then
		if rawget(_G, "AIReloadWeapons") then
			AIReloadWeapons(unit)
		end
		return true
	end
	for _, empty_slot in ipairs({"Handheld B", "Handheld A"}) do
		if #(unit:GetItemsInWeaponSlot(empty_slot) or empty_table) == 0 then
			local item = unit:RemoveItem("Inventory", gun)
			if item then
				local pos = unit:AddItem(empty_slot, item, 1, 1)
				if pos then
					unit:FlushCombatCache()
					if rawget(_G, "AIReloadWeapons") then
						AIReloadWeapons(unit)
					end
					return true
				end
				unit:AddItem("Inventory", item)
			end
			break
		end
	end
	return false
end

function AIActionThrowFlare:PrecalcAction(context, action_state)
	if not (GameState.Night or GameState.Underground) then
		return
	end

	local unit = context.unit
	local action_id, grenade, aoe_type, max_range, blast_radius

	-- 1) Throwable GlowStick / FlareStick in grenade slots.
	local throw_actions = {
		"ThrowGrenadeA", "ThrowGrenadeB", "ThrowGrenadeC", "ThrowGrenadeD",
		"ThrowGrenadeAG", "ThrowGrenadeBG", "ThrowGrenadeCG", "ThrowGrenadeDG",
		"ThrowGrenadeAO", "ThrowGrenadeBO"
	}
	for _, id in ipairs(throw_actions) do
		local caction = CombatActions[id]
		local cost = caction and caction:GetAPCost(unit) or -1
		if cost > 0 and unit:HasAP(cost) then
			local weapon = caction:GetAttackWeapons(unit)
			if IsKindOf(weapon, "Flare") then
				action_id = id
				grenade = weapon
				aoe_type = weapon.aoeType or "none"
				max_range = Min(self.MaxDist, weapon:GetMaxAimRange(unit) * const.SlabSizeX)
				blast_radius = weapon.AreaOfEffect * const.SlabSizeX
				break
			end
		end
	end

	-- 2) Signal pistol (FlareHandgun) via FireFlare.
	if not action_id then
		local gun, slot = JazzAI_FindFlareGun(unit)
		if not gun or not JazzAI_EnsureFlareGunReady(unit, gun, slot) then
			return
		end
		local caction = CombatActions.FireFlare
		local cost = caction and caction:GetAPCost(unit) or -1
		if cost <= 0 or not unit:HasAP(cost) then
			return
		end
		local weapon = caction:GetAttackWeapons(unit)
		if not IsKindOf(weapon, "FlareGun") then
			return
		end
		action_id = "FireFlare"
		aoe_type = "none"
		local aoe = (weapon.ammo and weapon.ammo.AreaOfEffect) or 5
		max_range = Min(self.MaxDist, (weapon.WeaponRange or 20) * const.SlabSizeX)
		blast_radius = aoe * const.SlabSizeX
	end

	local target_pts
	if self.TargetLastAttackPos then
		for _, enemy in ipairs(context.enemies) do
			if enemy.last_attack_pos then
				target_pts = target_pts or {}
				target_pts[#target_pts + 1] = enemy.last_attack_pos
			end
		end
	end
	for _, src in ipairs(g_NoiseSources or empty_table) do
		if src.Actor and src.Actor:IsOnEnemySide(unit) then
			target_pts = target_pts or {}
			target_pts[#target_pts + 1] = src.pos
		end
	end
	local zones = AIPrecalcFlareZones(context, action_id, self.MinDist, max_range, blast_radius,
		aoe_type, target_pts)
	local zone, score = self:EvalZones(context, zones)
	if zone then
		action_state.action_id = action_id
		action_state.target_pos = zone.target_pos
		action_state.score = score
	end
end

function AIActionThrowFlare:IsAvailable(context, action_state)
	return not not action_state.action_id
end

function AIActionThrowFlare:Execute(context, action_state)
	assert(action_state.action_id and action_state.target_pos)
	-- ACT-001: after flare, bias Push for one combat turn
	if g_Combat then
		JazzAI_FlarePushUntil = (g_Combat.current_turn or 0) + 1
	end
	AIPlayCombatAction(action_state.action_id, context.unit, nil, {target = action_state.target_pos})
	if JazzAI_TryCombatBark then
		JazzAI_TryCombatBark(context.unit, "nade_flare", { pos = action_state.target_pos })
	end
end

local function IsUnitInTheDark(hit)
	if not IsKindOf(hit.obj, "Unit") then
		return false
	end

	if hit.obj:HasStatusEffect("Darkness") then
		return true
	end

	return false
end

function AIPrecalcFlareZones(context, action_id, min_range, max_range, blast_radius, aoeType,
							 target_pts)
	if context.target_locked then
		return {}
	end

	if not target_pts then
		target_pts = AICalcAOETargetPoints(context, min_range, max_range, blast_radius)
	else
		-- make sure the target points are within the allowed range
		AIFilterTargetPoints(context.unit, target_pts, min_range, max_range)
	end

	-- calculate parabolas and affected units to each target point
	local zones = {}
	local action = CombatActions[action_id]
	local args = {target = false}
	for i, target_pt in ipairs(target_pts) do
		args.target = target_pt
		local results = action:GetActionResults(context.unit, args)
		local units
		local trajectory = results.trajectory or empty_table
		local pos = #trajectory > 0 and trajectory[#trajectory].pos or results.target_pos
		if pos and (aoeType == "smoke" or aoeType == "toxicgas" or aoeType == "teargas") then
			local water = terrain.IsWater(pos) and terrain.GetWaterHeight(pos)
			if not (water and (not pos:IsValidZ() or water >= pos:z())) then
				pos = SnapToPassSlab(pos) or pos
				local dx, dy = 1, 1
				for i = #trajectory - 1, 1, -1 do
					local step = trajectory[i]
					if step.pos:Dist2D(pos) > 0 then
						local px, py = step.pos:xy()
						local x, y = pos:xy()
						dx = (px == x) and 1 or ((x - px) / abs(x - px))
						dy = (py == y) and 1 or ((y - py) / abs(y - py))
						break
					end
				end

				local gx, gy, gz = WorldToVoxel(pos)
				local smoke, blocked = PropagateSmokeInGrid(gx, gy, gz, dx, dy)
				local smoke_voxels = {}
				for _, wpt in pairs(smoke) do
					local ppos = point_pack(WorldToVoxel(wpt))
					smoke_voxels[ppos] = true
				end

				for _, unit in ipairs(g_Units) do
					local _, head = unit:GetVisualVoxels()
					if smoke_voxels[head] then
						units = units or {}
						table.insert(units, unit)
					end
				end
			end
		else
			for _, hit in ipairs(results) do
				if IsUnitInTheDark(hit) then
					units = units or {}
					table.insert(units, hit.obj)
				end
			end
			-- FireFlare: GetActionResults may not list unit hits the same way as thrown flares.
			-- If illumination lands and enemies are in darkness nearby, still score the zone.
			if not units and action_id == "FireFlare" and pos then
				for _, enemy in ipairs(context.enemies or empty_table) do
					if IsValid(enemy) and enemy:HasStatusEffect("Darkness")
						and enemy:GetDist(pos) <= (blast_radius or 0) then
						units = units or {}
						table.insert(units, enemy)
					end
				end
			end
		end
		if units then
			zones[#zones + 1] = {target_pos = target_pt, units = units}
		end
	end

	return zones
end
