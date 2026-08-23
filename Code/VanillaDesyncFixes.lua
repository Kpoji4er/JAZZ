-- Vanilla / CommonLib desync mitigations that JAZZ does not already cover via full overrides.
-- Keep fixes narrow: replace wall-clock / AsyncRand in synced game-state paths only.

local function JazzPlayOutroCredits()
	local dlg = OpenDialog("Fade")
	dlg.idFade:SetVisible(true, true)
	StartRadioStation("_Playlist_Outro", 0, "force")
	WaitDialog("Outro")
	StartRadioStation("_Playlist_Credits", 0, "force")
	WaitDialog("Credits")
	Sleep(500)
	Msg("CampaignEnd", "HotDiamonds")
	CloseDialog(dlg)
	OpenPreGameMainMenu()
end

-- Ending setup runs on ALL clients via NetSyncEvents.HotDiamonds_SetupEnding в†’ LocalHotDiamonds_SetupEnding.
-- Vanilla used AsyncRand for outro quest flags в†’ clients diverge on Major/Pierre/etc.
function LocalHotDiamonds_SetupEnding(ending)
	local quest_05 = gv_Quests["05_TakeDownMajor"] and QuestGetState("05_TakeDownMajor")
	if not quest_05 then
		return
	end
	local quest_06 = gv_Quests["06_Endgame"] and QuestGetState("06_Endgame")
	if not quest_06 then
		return
	end

	SetQuestVar(quest_06, "Outro_PeaceRestored", ending == "peace")
	SetQuestVar(quest_06, "Outro_CivilWar", ending == "civil war")
	SetQuestVar(quest_06, "Outro_Coup", ending == "coup")

	local pierre = InteractionRand(2, "HotDiamondsEnding")
	SetQuestVar(quest_06, "Outro_PierreLiberated", pierre == 1)

	local rabies = InteractionRand(2, "HotDiamondsEnding")
	SetQuestVar(quest_06, "Outro_RedRabiesDone", rabies == 1)

	local diamonds = InteractionRand(3, "HotDiamondsEnding")
	SetQuestVar(quest_06, "Outro_GreenDiamondAIM", diamonds == 1)
	SetQuestVar(quest_06, "Outro_GreenDiamondMERC", diamonds == 2)

	local corazon = InteractionRand(3, "HotDiamondsEnding")
	SetQuestVar(quest_06, "Outro_CorazoneGoodEnd", corazon == 1)
	SetQuestVar(quest_06, "Outro_CorazoneMidEnd", corazon == 2)

	local major = InteractionRand(3, "HotDiamondsEnding")
	SetQuestVar(quest_05, "MajorDead", major == 0)
	SetQuestVar(quest_05, "MajorJail", major == 1)
	SetQuestVar(quest_05, "MajorRecruited", major == 2)

	CreateRealTimeThread(JazzPlayOutroCredits)
end

-- Book / effect stat boosts: vanilla modId used GetPreciseTicks() (wall clock).
function UnitStatBoost:__exec(obj, context)
	if obj.is_clone then
		return
	end
	local modId
	local stamp = string.format("%d-%d", GameTime(), InteractionRand(nil, "StatBoost"))
	if self.source == "Book" then
		modId = string.format("StatBoostBook-%s-%s-%s", self.Stat, obj.session_id, stamp)
		GainStat(obj, self.Stat, self.Amount, modId, "Studying")
	else
		modId = string.format("StatBoost-%s-%s-%s", self.Stat, obj.session_id, stamp)
		GainStat(obj, self.Stat, self.Amount, modId)
	end
end

-- Harden nil-seed callers: prefer synced InteractionRand when campaign/combat exists.
-- Main-menu UI (no InteractionRand / no Game) still falls back to AsyncRand.
function GetWeightedRandom(weights, seed)
	local totalPool = 0
	for i, weight in ipairs(weights) do
		totalPool = totalPool + weight[1]
	end

	if not seed then
		if InteractionRand and Game then
			seed = InteractionRand(nil, "WeightedRandom")
		else
			seed = AsyncRand()
		end
	end
	local rand = BraidRandom(seed, totalPool) + 1

	for i, weight in ipairs(weights) do
		rand = rand - weight[1]
		if rand <= 0 then
			return weight[2]
		end
	end
end

-- Vanilla used float i/10 and num_vectors/10 inside MulDivRound → potential client float drift on shot vectors.
function Firearm:CalcShotVectors(attacker, action_id, target, shot_attack_args, lof_data, dispersion, max_offset, extend, num_hits, num_misses, num_grazing)
	local spot_group, stance, step_pos = shot_attack_args.target_spot_group, shot_attack_args.stance, shot_attack_args.step_pos
	local target_pos = lof_data.target_pos or (IsValid(target) and target:GetPos())
	local lof_pos1 = lof_data.lof_pos1
	local ally_hits_count = lof_data.ally_hits_count or 0
	NetUpdateHash("CalcShotVectors", attacker, action_id, target, spot_group, step_pos, lof_pos1, target_pos, dispersion, max_offset, extend, num_hits, num_misses)
	local num_vectors = 50
	local hit_dist_threshold = 20 -- percent of max offset; used when target is point
	
	extend = extend or guim
	if not target_pos:IsValidZ() then
		target_pos = target_pos:SetTerrainZ()
	end
	lof_pos1 = lof_pos1 or step_pos
	if not lof_pos1:IsValidZ() then
		lof_pos1 = lof_pos1:SetTerrainZ()
	end

	local dir = target_pos - lof_pos1
	local dist = lof_pos1:Dist(target_pos)
	if dir:Len() == 0 and target then
		if IsValid(target) then
			target_pos = target:GetPos()
		elseif IsPoint(target) then
			target_pos = target
		end
		if not target_pos:IsValidZ() then
			target_pos = target_pos:SetTerrainZ()
		end
		dir = target_pos - lof_pos1
	end
	if dir:Len() == 0 then
		dir = Rotate(point(guim, 0, 0), IsValid(attacker) and attacker:GetAngle() or 0)
	end
	dir = SetLen(dir, guim)

	local min_angle, max_angle = 0, 360*60
	--[[if spot_group == "Head" then
		min_angle, max_angle = -90*60, 90*60		
	end--]]
	
	local offset_dir = RotateAxis(point(0, 0, guim), dir, attacker:RandRange(min_angle, max_angle))
	max_offset = Max(max_offset, MulDivRound(max_offset, dist, 8*guim))
	--alternative max dispersion calculation below
	--max_offset = Min(Max(max_offset, MulDivRound(max_offset, dist, 8*guim)), max_offset*4)


	local lof_params = {
		action_id = action_id,
		obj = attacker,
		stance = stance,
		step_pos = step_pos,
		can_use_covers = false,
		ignore_colliders = attacker,
		prediction = true,
		range = dist + extend,
		weapon = self,
		ignore_los = true,
		inside_attack_area_check = false,
		forced_hit_on_eye_contact = false,
	}

	
	local targets = {}
	targets[1] = target_pos
	for i = 2, num_vectors do
		targets[i] = target_pos + SetLen(offset_dir, MulDivRound(max_offset, i, num_vectors)) + RotateAxis(point(0, 0, attacker:Random(dispersion)), dir, attacker:Random(360*60)) + dir/2
	end

	local shot_hits, part_hits, shot_misses = {}, {}, {}
	local attack_data = GetLoFData(attacker, targets, lof_params)
	local hdt = MulDivRound(max_offset, hit_dist_threshold, 100)

	local anyVectorHitsTarget = false
	for i, data in ipairs(attack_data) do
		local lof = data.lof and data.lof[1]
		if lof then
			local hits = lof and lof.hits
			local target_hit = false
			if IsPoint(target) then
				local a, b = lof.attack_pos, target
				local p = lof.target_pos
				local ab, ap = b-a, p-a
				if ab:Len() >  0 then
					local p1 = a + MulDivRound(ab, Dot(ap, ab), Dot(ab, ab))
					local dist = p1:Dist(p)
					local trajectory = { lof_pos1 = lof.lof_pos1, attack_pos = lof.attack_pos, target_pos = lof.target_pos, idx = i}
					if dist <= hdt then
						table.insert(shot_hits, trajectory)
						target_hit = true
					else
						table.insert(shot_misses, trajectory)
					end
				end
			else
				local target_hit_data 
				for _, hit in ipairs(hits) do
					if hit.obj == target then
						target_hit_data = hit
						break
					end
				end
				target_hit = target_hit_data and true or false
				-- also match friendly fire lof data
				local part_hit =
					target_hit_data and target_hit_data.spot_group == spot_group
					and (lof.ally_hits_count or 0) == ally_hits_count
					and (ally_hits_count == 0 or lof.allyHit == lof_data.allyHit)
				local trajectory = { lof_pos1 = lof.lof_pos1, attack_pos = lof.attack_pos, target_pos = lof.target_pos, idx = i, accurate = part_hit, target_hit = target_hit}
				table.insert(target_hit and shot_hits or shot_misses, trajectory)
				if part_hit then
					table.insert(part_hits, trajectory)
				end
				--ShowVector(lof.target_pos - lof.attack_pos, lof.attack_pos, target_hit and const.clrGreen or const.clrYellow, 5000)
			end
			anyVectorHitsTarget = anyVectorHitsTarget or target_hit
		end
	end
	
	while #part_hits < num_hits and #shot_hits > 0 do
		local trajectory, hit_idx = table.rand(shot_hits, attacker:Random())
		table.remove(shot_hits , hit_idx)
		if not table.find(part_hits, "idx", trajectory.idx) then
			table.insert(part_hits, trajectory)
		end
	end
	
	while #part_hits > num_hits do
		local _, hit_idx = table.rand(part_hits, attacker:Random())
		table.remove(part_hits, hit_idx)
	end

	if #part_hits == num_hits then
		local inaccurate = table.ifilter(shot_hits, function(idx, trajectory) return trajectory.inaccurate end)
		while #part_hits < (num_hits + num_grazing) and #inaccurate > 0 and num_misses > 0 do
			local trajectory, hit_idx = table.rand(inaccurate, attacker:Random())
			table.remove(inaccurate , hit_idx)
			if not table.find(part_hits, "idx", trajectory.idx) then
				table.insert(part_hits, trajectory)
				num_misses = num_misses - 1
			end
		end
		
		while #part_hits < (num_hits + num_grazing) and #shot_hits > 0 and num_misses > 0 do			
			local trajectory = table.remove(shot_hits) -- walk in reverse order, from furthest to closest to pick the most "inaccurate" lines for grazing
			if not table.find(part_hits, "idx", trajectory.idx) then
				trajectory.accurate = false -- mark it for GetActionResults
				table.insert(part_hits, trajectory)
				num_misses = num_misses - 1
			end
		end
	end

	while #shot_misses > num_misses  do
		local _, miss_idx = table.rand(shot_misses, attacker:Random())
		table.remove(shot_misses, miss_idx)		
	end
	--NetUpdateHash("CalcShotVectors_end", hashParamTable(part_hits), hashParamTable(shot_misses))
	return part_hits, shot_misses, anyVectorHitsTarget, target_pos, dir
end

-- Assigned-area AI dest: pairs(id_to_individual_area) then interaction_rand → order-dependent dest.
function TacticalMap:FindOptimalLocationInAssignedArea(unit, context)	
	local positions
	local assigned_area = self.assigned_individual_areas[unit] or 0
	local cur_pos = point_pack(unit:GetPos())	
	
	if assigned_area ~= 0 then
		local area = self.ppos_to_individual_area[cur_pos]
		if band(area, assigned_area) ~= 0 then
			-- already in one of the areas
			context.best_dest = GetPackedPosAndStance(unit)
			return true			
		end
		positions = {}		
		if self.assigned_area_priority[unit] then
			for p = self.PriorityHigh, self.PriorityLow do
				for id in tac_area_ids(self.assigned_area_priority[unit][p]) do
					local flag = self.id_to_individual_area[id]
					if band(assigned_area, flag) ~= 0 then
						positions = table.union(positions, self.area_to_positions[id])
					end
				end
				if #positions > 0 then break end
			end
		end
		if #positions == 0 then
			for id, flag in sorted_pairs(self.id_to_individual_area) do
				if band(assigned_area, flag) ~= 0 then
					positions = table.union(positions, self.area_to_positions[id])
				end
			end
		end
	end
	
	positions = positions or empty_table
	if #positions > 0 then
		local goto_pos = table.interaction_rand(positions, "Behavior")
		local x, y, z = point_unpack(goto_pos)
		context.best_dest = stance_pos_pack(x, y, z, StancesList.Standing)
		context.optimal_dest_in_assigned_area = true
		return true
	end
end
-- Cosmetic buckshot FX: vanilla burned attacker:Random on the sync path.
-- AsyncRand keeps combat braid / NetUpdateHash isolated (FX may differ per client).
function Firearm:CalcBuckshotScatter(attacker, action, attack_pos, target_pos, num_vectors, aoe_params)
	aoe_params = aoe_params or self:GetAreaAttackParams(action.id, attacker, target_pos)
	local range = self.WeaponRange * const.SlabSizeX
	local dir = SetLen(target_pos - attack_pos, guim)

	local min_offset = 35 * guic
	local scatter = Max(min_offset, MulDivRound(range, sin(aoe_params.cone_angle / 2), Max(1, cos(aoe_params.cone_angle / 2))))

	local var_offset = Max(0, scatter - min_offset)
	local targets = {}
	target_pos = attack_pos + SetLen(dir, range)
	for i = 1, num_vectors do
		local offset = RotateAxis(point(0, 0, min_offset + AsyncRand(var_offset)), dir, AsyncRand(360 * 60))
		local pt = target_pos + offset
		local test_dir = pt - attack_pos
		targets[i] = attack_pos + SetLen(test_dir, range + scatter)
	end

	local lof_params = {
		attack_pos = attack_pos,
		obj = attacker,
		output_collisions = true,
		range = range + scatter + guim,
		seed = AsyncRand(),
	}
	local attack_data = GetLoFData(attacker, targets, lof_params)
	local hits = {}
	for i, data in ipairs(attack_data) do
		local lof_hits = data.lof and data.lof[1] and data.lof[1].hits
		for _, hit in ipairs(lof_hits) do
			if (hit.obj or hit.terrain) and not IsKindOf(hit.obj, "Unit") then
				hits[#hits + 1] = hit
				break
			end
		end
	end
	return hits
end

local function JazzBiasObjKey(obj)
	if not obj then
		return ""
	end
	if IsKindOf(obj, "Unit") then
		return "U:" .. tostring(obj.session_id or obj.handle or "")
	end
	if IsKindOf(obj, "CombatTeam") or IsKindOf(obj, "Team") then
		return "T:" .. tostring(obj.side or obj.handle or "")
	end
	return "O:" .. tostring(obj.handle or obj)
end

-- Nested pairs(g_AIBiases) while mutating; sort for stable cleanup order.
function AIUpdateBiases()
	for id, item_mods in sorted_pairs(g_AIBiases) do
		local objs = {}
		for obj in pairs(item_mods) do
			objs[#objs + 1] = obj
		end
		table.sort(objs, function(a, b)
			return JazzBiasObjKey(a) < JazzBiasObjKey(b)
		end)
		for _, obj in ipairs(objs) do
			local mods = item_mods[obj]
			local total = 0
			mods.disable = false
			mods.priority = false
			for i = #mods, 1, -1 do
				if mods[i].end_turn < g_Combat.current_turn then
					table.remove(mods, i)
				else
					total = total + mods[i].value
					mods.disable = mods.disable or mods[i].disable
					mods.priority = mods.priority or mods[i].priority
				end
			end
			mods.total = total
		end
	end
end

-- CraftAmmo: only JAZZ homemade (_Crafted) and JAZZ saltshot. Factory vanilla
-- recipes stay in data (RemoveCraft / loot IDs) but never enter the picker.
function Jazz_IsAllowedCraftAmmoRecipe(recipe)
	local item = recipe and recipe.ResultItem and recipe.ResultItem.item
	if type(item) ~= "string" then
		return false
	end
	if string.match(item, "^JAZZ_AMMO_.+_Crafted$") then
		return true
	end
	return item == "JAZZ_AMMO_12gauge_Saltshot"
end

-- Craft list: vanilla pairs + weak sort; CommonLib FixRecipes does full sort.
-- Keep a local copy so craft order stays deterministic if CLib is absent.
function SectorOperationFillItemsToCraft(sector_id, operation_id)
	if not IsCraftOperationId(operation_id) then
		return
	end

	local id = "g_Recipes" .. operation_id
	local all_to_craft = _G[id] or {}
	_G[id] = all_to_craft
	table.iclear(all_to_craft)
	local count = 0
	local res_items = SectorOperation_CalcCraftResources(sector_id, operation_id)
	local professionals = GetOperationProfessionals(sector_id, operation_id) or {}
	local professional = professionals[1]
	local squad = professional and gv_Squads[professional.Squad]
	local squad_units = squad and squad.units
	local checked_amount_cache = {}
	for recipe_id, recipe in pairs(CraftOperationsRecipes) do
		if operation_id == "CraftAmmo" and not Jazz_IsAllowedCraftAmmoRecipe(recipe) then
			goto continue
		end
		if (operation_id == "CraftAmmo" and recipe.group == "Ammo" or
			operation_id == "CraftExplosives" and recipe.group == "Explosives" or
			operation_id == recipe.CraftOperationId) and recipe.ResultItem then

			local hidden
			local crafter = recipe.RequiredCrafter or ""
			if crafter ~= "" then
				hidden = not table.find(professionals, "session_id", crafter)
			end
			if not hidden and recipe.QuestConditions then
				hidden = not EvalConditionList(recipe.QuestConditions)
			end

			local enabled = squad_units and SectorOperation_ValidateRecipeIngredientsAmount(squad_units, recipe, res_items, checked_amount_cache)
			count = count + 1
			all_to_craft[count] = {
				recipe = recipe_id,
				item_id = recipe.ResultItem.item,
				amount = recipe.ResultItem.amount,
				enabled = enabled,
				hidden = hidden
			}
		end
		::continue::
	end

	table.sort(all_to_craft, function(a, b)
		if a.enabled ~= b.enabled then
			return a.enabled and not b.enabled
		end
		if a.hidden ~= b.hidden then
			return not a.hidden and b.hidden
		end
		if a.item_id ~= b.item_id then
			return a.item_id < b.item_id
		end
		return a.recipe < b.recipe
	end)

	return all_to_craft
end

SectorOperationValidateItemsToCraft = SectorOperationFillItemsToCraft

g_JAZZ_CraftAddResWrapped = rawget(_G, "g_JAZZ_CraftAddResWrapped") or false
g_JAZZ_CraftAddResBase = rawget(_G, "g_JAZZ_CraftAddResBase") or false

local function Jazz_InstallCraftAddResFilter()
	if rawget(_G, "g_JAZZ_CraftAddResWrapped") then
		return
	end
	local base = rawget(_G, "SectorOperations_CraftAdditionalResources")
	if type(base) ~= "function" then
		return
	end
	rawset(_G, "g_JAZZ_CraftAddResBase", base)
	rawset(_G, "g_JAZZ_CraftAddResWrapped", true)
	function SectorOperations_CraftAdditionalResources(sector_id, operation_id)
		if operation_id ~= "CraftAmmo" then
			return g_JAZZ_CraftAddResBase(sector_id, operation_id)
		end
		local res_table = {}
		for _, recipe in pairs(CraftOperationsRecipes) do
			if Jazz_IsAllowedCraftAmmoRecipe(recipe) then
				for _, ingr in ipairs(recipe.Ingredients) do
					res_table[ingr.item] = (res_table[ingr.item] or 0) + ingr.amount
				end
			end
		end
		local needed_res_table = SectorOperation_CalcCraftResources(sector_id, operation_id)
		local mercs = GetOperationProfessionals(sector_id, operation_id)
		local merc
		if next(mercs) then
			merc = mercs[1].session_id
		else
			mercs = GetPlayerMercsInSector(sector_id)
			merc = mercs[1]
		end
		local array = {}
		for res, val in pairs(res_table) do
			if res ~= "Money" and res ~= "Parts" then
				local result, amount_found = HasItemInSquad(merc, res, "all")
				if amount_found and amount_found > 0 then
					array[#array + 1] = { res = res, value = val, queued_val = needed_res_table[res], amount_found = amount_found or 0 }
				end
			end
		end
		table.sortby(array, "res")
		return array
	end
end

function OnMsg.DataLoaded()
	Jazz_InstallCraftAddResFilter()
end

function OnMsg.ModsReloaded()
	Jazz_InstallCraftAddResFilter()
end
