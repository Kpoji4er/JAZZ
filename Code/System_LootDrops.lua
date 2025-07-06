--local OR_UnitLootDrop = Unit:DropLoot

--function Unit:DropLoot()



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
		
	
--		if not item.locked and (not is_npc or roll < item.drop_chance) then
		if not item.locked and (item.drop_chance>0) then
			if IsGameRuleActive("AmmoScarcity") and is_npc and IsKindOf(item, "InventoryStack") and IsKindOfClasses(item,{"Ammo", "Ordnance", "Grenade", "ThrowableTrapItem", "Flare"}) then
				local percent = GameRuleDefs.AmmoScarcity:ResolveValue("LootDecrease")
				item.Amount =  Max(1,item.Amount - MulDivRound(item.Amount, percent, 100))
			end	
			--qsr print(item)
			if IsKindOf(item, "Firearm") and (item.drop_chance<100) then
				local quality_roll = random(100)
				local max = item:GetMaxResource()
				local cur = item:GetCurrentResource()
				local maxres = item.WeaponResourceMax
				local maxroll = 0
				local curroll maxroll = 0

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
				local curroll maxroll = 0

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
				item.Condition = MulDivRound(cur, 100, max )
			else
				-- Обычное условие для не-оружия
				if item.Condition and item.drop_chance < 100 then
					item.Condition = Max(0, item.Condition - Min(random(100 - item.drop_chance), item.Condition))
				end
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

