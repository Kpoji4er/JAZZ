-- JAZZ-ECON-004: Bobby Ray restock soft-tail / ammo boost / staples flat + tier price.
-- Wraps PrepareShopItemsForRestock, PickRandomWeightItems, RestockStandardItem,
-- RestockUsedWeapon, RestockUsedArmor. BobbyPays stays after tier/jitter (instance Cost).

g_JAZZ_BobbyEcon004Wrapped = rawget(_G, "g_JAZZ_BobbyEcon004Wrapped") or false
g_JAZZ_PrepareShopItemsForRestockBase = rawget(_G, "g_JAZZ_PrepareShopItemsForRestockBase") or false
g_JAZZ_PickRandomWeightItemsBase = rawget(_G, "g_JAZZ_PickRandomWeightItemsBase") or false
g_JAZZ_RestockStandardItemBase = rawget(_G, "g_JAZZ_RestockStandardItemBase") or false
g_JAZZ_RestockUsedWeaponBase = rawget(_G, "g_JAZZ_RestockUsedWeaponBase") or false
g_JAZZ_RestockUsedArmorBase = rawget(_G, "g_JAZZ_RestockUsedArmorBase") or false
g_JAZZ_BobbyEffWeights = rawget(_G, "g_JAZZ_BobbyEffWeights") or {}

local JAZZ_BOBBY_FLAT = {
	Meds = true,
	Parts = true,
	JAZZ_Bandage = true,
	JAZZ_Morphine = true,
	FirstAidKit = true,
	Medkit = true,
	Lockpick = true,
	Wirecutter = true,
	Crowbar = true,
	BlackPowder = true,
	JAZZ_BarrelParts = true,
	JAZZ_ScopeParts = true,
	SkillMag_Medical = true,
}

local function lPow10(delta)
	local m = 1
	for _ = 1, delta do
		m = m / 10
	end
	return m
end

local function lPow3(delta)
	local m = 1
	for _ = 1, delta do
		m = m * 3
	end
	return m
end

local function lPow03(delta)
	local m = 1
	for _ = 1, delta do
		m = m * 0.3
	end
	return m
end

local function lIsAmmoItem(item)
	return IsKindOf(item, "Ammo") or IsKindOf(item, "Ordnance")
end

local function lIsPoorAmmo(item)
	local cls = item.class or ""
	return string.find(cls, "_Poor", 1, true) and true or false
end

function JazzBobbyEffectiveRestockWeight(item, unlocked_tier)
	local rw = item.RestockWeight or 0
	if rw <= 0 then
		return 0
	end
	local U = unlocked_tier or 0
	if U < 1 then
		return 0
	end
	local T = tonumber(item.Tier) or 1
	local cls = item.class

	if JAZZ_BOBBY_FLAT[cls] then
		return rw
	end

	if lIsAmmoItem(item) then
		local tier_mult = 1.0
		if T > U then
			tier_mult = lPow10(T - U)
		elseif T < U then
			local d = U - T
			tier_mult = 2 ^ d
			if tier_mult > 8 then
				tier_mult = 8
			end
		end
		local poor_mult = 1.0
		if lIsPoorAmmo(item) then
			if U >= 4 then
				poor_mult = 0
			elseif U == 3 then
				poor_mult = 0.08
			elseif U == 2 then
				poor_mult = 0.35
			end
		end
		return rw * tier_mult * poor_mult
	end

	local delta = abs(T - U)
	return rw * lPow10(delta)
end

local function lPriceMult(item, unlocked_tier)
	if JAZZ_BOBBY_FLAT[item.class] then
		return 1
	end
	local U = unlocked_tier or BobbyRayShopGetUnlockedTier() or 1
	local T = tonumber(item.Tier) or 1
	local d = T - U
	if d > 0 then
		return lPow3(d)
	elseif d < 0 then
		return lPow03(-d)
	end
	return 1
end

local function lStockJitter()
	local r = InteractionRand(41, "BobbyRayShop")
	return 0.80 + (r / 100)
end

function JazzBobbyApplyTierPriceToItem(item)
	if not item then
		return
	end
	local U = BobbyRayShopGetUnlockedTier() or 1
	local base = item.Cost or 0
	item.Cost = Max(1, round(base * lPriceMult(item, U) * lStockJitter()))
end

local function lInstallBobbyEcon004()
	if rawget(_G, "g_JAZZ_BobbyEcon004Wrapped") then
		return
	end
	if type(PrepareShopItemsForRestock) ~= "function" then
		return
	end

	rawset(_G, "g_JAZZ_PrepareShopItemsForRestockBase", PrepareShopItemsForRestock)
	rawset(_G, "g_JAZZ_PickRandomWeightItemsBase", PickRandomWeightItems)
	rawset(_G, "g_JAZZ_RestockStandardItemBase", RestockStandardItem)
	rawset(_G, "g_JAZZ_RestockUsedWeaponBase", RestockUsedWeapon)
	rawset(_G, "g_JAZZ_RestockUsedArmorBase", RestockUsedArmor)

	function PrepareShopItemsForRestock(unlocked_tier, used)
		local category_weights = {}
		local category_count = {}
		local category_items = {}
		local category_items_set = {}
		local eff_map = {}
		rawset(_G, "g_JAZZ_BobbyEffWeights", eff_map)
		NetUpdateHash("PrepareShopItemsForRestock1", unlocked_tier, used)
		ForEachPreset("InventoryItemCompositeDef", function(preset)
			local item = g_Classes[preset.id]
			if not item then
				return
			end
			local usedOrStandard
			if used then
				usedOrStandard = item.CanAppearUsed
			else
				usedOrStandard = item.CanAppearStandard
			end
			if not (item.CanAppearInShop and usedOrStandard) then
				return
			end
			local eff = JazzBobbyEffectiveRestockWeight(item, unlocked_tier)
			if not (eff and eff > 0) then
				return
			end
			eff_map[item] = eff
			local catObj = item:GetCategory()
			if not catObj then
				return
			end
			local cat = catObj.id
			if not category_weights[cat] then
				category_weights[cat] = 0
				category_count[cat] = 0
				category_items[cat] = {}
				category_items_set[cat] = {}
			end
			table.insert(category_items[cat], item)
			category_items_set[cat][item] = true
			category_weights[cat] = category_weights[cat] + eff
			category_count[cat] = category_count[cat] + 1
			NetUpdateHash("PrepareShopItemsForRestock2", cat, item.class, eff, category_count[cat], category_weights[cat])
		end)
		return category_items, category_count, category_weights, category_items_set
	end

	function PickRandomWeightItems(num, items_array, max_weight)
		local picked_items = {}
		local picked_items_set = {}
		local eff_map = rawget(_G, "g_JAZZ_BobbyEffWeights") or {}
		for i = 1, num do
			local rand_weight = InteractionRand(max_weight, "BobbyRayShop")
			local cur_weight = 0
			local cur_index = 1
			while true do
				local item = items_array[cur_index]
				while picked_items_set[item] do
					cur_index = cur_index + 1
					item = items_array[cur_index]
				end
				local w = eff_map[item] or item.RestockWeight or 0
				cur_weight = cur_weight + w
				cur_index = cur_index + 1
				if cur_weight > rand_weight then
					table.insert(picked_items, item.class)
					picked_items_set[item] = true
					max_weight = max_weight - w
					break
				end
			end
		end
		return picked_items
	end

	function RestockStandardItem(item_class)
		g_JAZZ_RestockStandardItemBase(item_class)
		local item = g_BobbyRayStore.standard[item_class]
		if not item then
			return
		end
		local U = BobbyRayShopGetUnlockedTier() or 1
		local T = tonumber(item.Tier) or 1
		if lIsAmmoItem(item) and T < U and not lIsPoorAmmo(item) then
			local base_max = item.MaxStock or 1
			local factor = Min(3, 1 + (U - T))
			item.Stock = Max(item.Stock or 1, Min(base_max * factor, base_max * 3))
		end
		local catalog = g_Classes[item_class]
		if catalog and catalog.Cost then
			item.Cost = catalog.Cost
		end
		JazzBobbyApplyTierPriceToItem(item)
	end

	function RestockUsedWeapon(weapon_id)
		g_JAZZ_RestockUsedWeaponBase(weapon_id)
		for _, it in pairs(g_BobbyRayStore.used) do
			if it.class == weapon_id and it.New then
				local U = BobbyRayShopGetUnlockedTier() or 1
				it.Cost = Max(1, round((it.Cost or 0) * lPriceMult(it, U) * lStockJitter()))
				break
			end
		end
	end

	function RestockUsedArmor(armor_id)
		g_JAZZ_RestockUsedArmorBase(armor_id)
		for _, it in pairs(g_BobbyRayStore.used) do
			if it.class == armor_id and it.New then
				local U = BobbyRayShopGetUnlockedTier() or 1
				it.Cost = Max(1, round((it.Cost or 0) * lPriceMult(it, U) * lStockJitter()))
				break
			end
		end
	end

	rawset(_G, "g_JAZZ_BobbyEcon004Wrapped", true)
end

OnMsg.ClassesBuilt = lInstallBobbyEcon004
OnMsg.ModsReloaded = lInstallBobbyEcon004
OnMsg.DataLoaded = lInstallBobbyEcon004
