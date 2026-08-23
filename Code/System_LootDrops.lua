--local OR_UnitLootDrop = Unit:DropLoot

--function Unit:DropLoot()

-- JAZZ-INV-002: NPC corpse magazine fill by Game.game_difficulty.
-- MachineGun and LightMachineGun are sibling Firearm children, not parent/child.
JAZZ_LOOT_AMMO_KEEP = {
	Normal = { other = 80, mg = 50 },
	Hard = { other = 60, mg = 30 },
	VeryHard = { other = 45, mg = 18 },
}

function JAZZ_IsLootAmmoMGClass(item)
	return IsKindOf(item, "MachineGun") or IsKindOf(item, "LightMachineGun")
end

function JAZZ_GetLootAmmoKeepPercent(item, difficulty)
	local row = JAZZ_LOOT_AMMO_KEEP[difficulty or ""] or JAZZ_LOOT_AMMO_KEEP.Normal
	if JAZZ_IsLootAmmoMGClass(item) then
		return row.mg
	end
	return row.other
end

function JAZZ_CapLootFirearmAmmo(item, difficulty)
	if not item or not item.ammo then
		return item
	end
	local amount = item.ammo.Amount or 0
	if amount <= 0 then
		return item
	end
	local mag = item.MagazineSize or amount
	local pct = JAZZ_GetLootAmmoKeepPercent(item, difficulty)
	local cap = Max(1, MulDivRound(mag, pct, 100))
	if amount > cap then
		item.ammo.Amount = cap
	end
	return item
end

function Unit:DropLoot(container)
--	local start = GetPreciseTicks(1000)
	local is_npc = self:IsNPC() -- not a merc

	local seed = Unit:Random()
	local random = BraidRandomCreate(seed)
	
	local debugText =  _InternalTranslate(self.Name) .. " dropping loot: (roll must be lower)"
	
	-- Locked items never drop.
	-- Go over the equipped items, drop them to "Inventory" based on their drop chance,
	-- Equipped items from Mercs always drop(except locked items). Otherwise check the drop chance.
	local droped_items = 0
	self:ForEachItem(function(item, slot_name, left, top, self, container, is_npc)
		if slot_name == "InventoryDead" then return end
		self:RemoveItem(slot_name, item)	
				
		local dropped
		local slot = container and "Inventory" or "InventoryDead"
		local roll = self:Random(100)

		if IsKindOf(item,"Ammo") then item.drop_chance = 5 end
		if IsKindOf(item,"Ordnance") then item.drop_chance = 15 end
		if IsKindOf(item,"Grenade") then item.drop_chance = 10 end
		if IsKindOf(item,"Flare") then item.drop_chance = 10 end
		
	
--		if not item.locked and (not is_npc or roll < item.drop_chance) then
		if (not item.locked and (item.drop_chance>0) and not IsKindOfClasses(item,{"Ammo", "Ordnance", "Grenade", "ThrowableTrapItem", "Flare"}))
		or (IsKindOfClasses(item,{"Ammo", "Ordnance", "Grenade", "ThrowableTrapItem", "Flare"}) and (not is_npc or roll < item.drop_chance)) then
			--qsr print(item)
			if IsKindOf(item, "Firearm") and (item.drop_chance<100) then
				local quality_roll = random(100)
				local max = item:GetMaxResource()
				local cur = item:GetCurrentResource()
				local maxres = item.WeaponResourceMax
				local maxroll = 0
				local curroll = 0

				if quality_roll <= 30 then
					-- Юзабельный
					curroll = random(40, 100)
					maxroll = random(90, 100)
					

				elseif quality_roll <= 50 then
					-- Мусор
					curroll = random(0, 70)
					maxroll = random(0, 80)
				
				else
					-- Средняк
					curroll = random(0, 90)
					maxroll = random(60, 90)

				end	

				local factory = item:GetFactoryResource() or 1000
				max = MulDivRound(max, maxroll, 100)
				cur = MulDivRound(cur, curroll, 100 ) - (max > item.WeaponResource and (max - item.WeaponResource) or 0)

				cur = Clamp(cur,0,max)
				item.WeaponResourceMax = max
				item.WeaponResource = cur
				--item.Condition = MulDivRound(100, cur, max)
				item.Condition = MulDivRound(cur, 100, max )
			
			elseif IsKindOf(item, "Armor") and (item.drop_chance<100) then
				local quality_roll = random(100)
				local max = item:GetMaxResource()
				local cur = item:GetCurrentResource()
				local maxres = item.ArmorResourceMax
				local maxroll = 0
				local curroll = 0

				if quality_roll <= 30 then
					-- Юзабельный
					curroll = random(40, 100)
					maxroll = random(90, 100)
					

				elseif quality_roll <= 50 then
					-- Мусор
					curroll = random(0, 70)
					maxroll = random(0, 80)
				
				else
					-- Средняк
					curroll = random(0, 90)
					maxroll = random(60, 90)

				end	

				local factory = item:GetFactoryResource() or 1000
				max = MulDivRound(max, maxroll, 100)
				cur = MulDivRound(cur, curroll, 100 ) - (max > item.ArmorResource and (max - item.ArmorResource) or 0)
				cur = Clamp(cur,0,max)
				item.ArmorResourceMax = max
				item.ArmorResource = cur
				item.Condition = MulDivRound(cur, 100, max ) or item.Condition
			else
				-- Обычное условие для не-оружия
				if item.Condition and item.drop_chance < 100 then
					item.Condition = Max(0, item.Condition - Min(random(100 - item.drop_chance), item.Condition))
				end
			end

			if is_npc and IsKindOf(item, "Firearm") then
				JAZZ_CapLootFirearmAmmo(item, Game and Game.game_difficulty)
			end
			 
			local addTo = container or self
			
			local pos, err = addTo:CanAddItem(slot, item)
		--	local pos, err = addTo:CanAddItem(slot, LBE)
			assert(pos, "Couldn't FIND pos in Inventory to place dropped item. Err: '" .. err .. "'")
			if pos then
				dropped, err = addTo:AddItem(slot, item, point_unpack(pos))
				assert(dropped, "Couldn't PLACE dropped item in Inventory. Err: '" .. err .. "'")
			end			
		end
		
		
		if not dropped then
			DoneObject(item)
		elseif slot == "InventoryDead" then
			droped_items = droped_items + (item:IsLargeItem() and 2 or 1)
		end
	end, self, container, is_npc)

	if droped_items > 0 then
		self.max_dead_slot_tiles = droped_items
	end
--	print(start - GetPreciseTicks(1000))

	CombatLog("debug", debugText)
end

