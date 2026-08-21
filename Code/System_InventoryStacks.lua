-- JAZZ-INV-001: dual stack limits — storage (SquadBag/SectorStash) vs personal loadout.

const.JazzStorageStackMax = 10000
JazzEjectedAmmoPreferUnit = rawget(_G, "JazzEjectedAmmoPreferUnit") or false

function JazzIsStorageInventory(inv)
	return IsKindOfClasses(inv, "SquadBag", "SectorStash", "UnopennedSquadBag")
end

function JazzInventoryItemsCanStack(a, b)
	if not a or not b or a.class ~= b.class then
		return false
	end
	if IsKindOf(a, "JAZZ_RemovableAttachment") or IsKindOf(b, "JAZZ_RemovableAttachment") then
		return (rawget(a, "RemovableComponentId") or a.class) == (rawget(b, "RemovableComponentId") or b.class)
	end
	return true
end

function JazzGetPersonalMaxStacks(item)
	if not item then
		return 10
	end
	local class = item.class
	local def = InventoryItemDefs and InventoryItemDefs[class]
	if def then
		local v = def.MaxStacks or (def.GetProperty and def:GetProperty("MaxStacks"))
		if type(v) == "number" and v > 0 then
			return v
		end
	end
	local g = g_Classes and g_Classes[class]
	if g then
		local v = rawget(g, "MaxStacks")
		if type(v) == "number" and v > 0 then
			return v
		end
	end
	local cur = rawget(item, "MaxStacks")
	if type(cur) == "number" and cur > 0 and cur < const.JazzStorageStackMax then
		return cur
	end
	return 10
end

function JazzGetStackMax(item, inv)
	-- Identical remountables (same RemovableComponentId) stack in storage.
	-- Mixed IDs never share a stack — see JazzInventoryItemsCanStack.
	if JazzIsStorageInventory(inv) then
		return const.JazzStorageStackMax
	end
	return JazzGetPersonalMaxStacks(item)
end

function JazzApplyStackContext(item, inv)
	if not IsKindOf(item, "InventoryStack") then
		return
	end
	rawset(item, "MaxStacks", JazzGetStackMax(item, inv))
end

function JazzEnsureContainerStackContext(inv)
	if not inv or not inv.ForEachItem then
		return
	end
	inv:ForEachItem(function(item)
		JazzApplyStackContext(item, inv)
	end)
end

function JazzIsStorageStackUI(item)
	if not IsKindOf(item, "InventoryStack") then
		return false
	end
	-- Membership only. Do not trust MaxStacks==10000: a stack that left the bag
	-- can keep that instance cap and then show / merge as storage in loadout.
	if gv_SquadBag and gv_SquadBag.Inventory then
		local found
		gv_SquadBag:ForEachItem(function(it)
			if it == item then
				found = true
				return "break"
			end
		end)
		if found then
			return true
		end
	end
	if gv_SectorInventory and IsKindOf(gv_SectorInventory, "SectorStash") then
		local found
		gv_SectorInventory:ForEachItem(function(it)
			if it == item then
				found = true
				return "break"
			end
		end)
		if found then
			return true
		end
	end
	return false
end

function JazzMarkSquadBagData(squad_id)
	local bag = GetSquadBag and GetSquadBag(squad_id)
	if not bag then
		return
	end
	for _, item in ipairs(bag) do
		if IsKindOf(item, "InventoryStack") then
			rawset(item, "MaxStacks", const.JazzStorageStackMax)
		end
	end
end

function OnMsg.LoadGame()
	for squad_id in pairs(gv_Squads or empty_table) do
		JazzMarkSquadBagData(squad_id)
	end
	local ud = rawget(_G, "gv_UnitData")
	if type(ud) == "table" then
		for _, unit in pairs(ud) do
			JazzSpillUnitInventoryExcess(unit)
		end
	end
end

function JazzGetAmmoLoadoutSlot(unit, item)
	if not unit or not item then
		return false
	end
	if IsKindOf(item, "Ordnance") then
		-- OrdnanceInventory is ThrowableTrapItem (C4); RPG warheads live in backpack.
		if unit.CheckClass and unit:CheckClass(item, "OrdnanceInventory") then
			return "OrdnanceInventory"
		end
		return GetContainerInventorySlotName and GetContainerInventorySlotName(unit) or "Inventory"
	end
	if IsKindOf(item, "Ammo") then
		return "AmmoInventory"
	end
	return GetContainerInventorySlotName and GetContainerInventorySlotName(unit) or "Inventory"
end

function JazzCloneStackRemainder(item, amount)
	if not item or not amount or amount <= 0 then
		return false
	end
	local clone = PlaceInventoryItem(item.class)
	if not IsKindOf(clone, "InventoryStack") then
		if clone then
			DoneObject(clone)
		end
		return false
	end
	clone.Amount = amount
	if IsKindOf(item, "JAZZ_RemovableAttachment") then
		clone.RemovableComponentId = rawget(item, "RemovableComponentId")
	end
	return clone
end

function JazzItemIsInInventory(inv, item)
	if not inv or not item or not inv.ForEachItem then
		return false
	end
	local found
	inv:ForEachItem(function(it)
		if it == item then
			found = true
			return "break"
		end
	end)
	return not not found
end

-- Extra rounds over personal MaxStacks → squad bag. Never silent-delete.
function JazzDepositItemToSquadBag(unit, item)
	if not item then
		return true
	end
	if (item.Amount or 0) <= 0 then
		DoneObject(item)
		return true
	end
	local squad_id = unit and unit.Squad
	local bag = squad_id and GetSquadBagInventory and GetSquadBagInventory(squad_id)
	if bag and bag.AddAndStackItem then
		local prev = rawget(_G, "JazzEjectedAmmoPreferUnit")
		rawset(_G, "JazzEjectedAmmoPreferUnit", false)
		JazzApplyStackContext(item, bag)
		bag:AddAndStackItem(item)
		rawset(_G, "JazzEjectedAmmoPreferUnit", prev or false)
		if JazzItemIsInInventory(bag, item) then
			return true
		end
		local ok_amt, amount = pcall(function()
			return item.Amount
		end)
		if ok_amt and amount and amount > 0 then
			return JazzDropAmmoAtFeet(unit, item)
		end
		return true
	end
	return JazzDropAmmoAtFeet(unit, item)
end

function JazzSpillPersonalStackExcess(unit, item)
	if not unit or not IsKindOf(item, "InventoryStack") then
		return
	end
	if JazzIsStorageInventory(unit) then
		return
	end
	local personal = JazzGetPersonalMaxStacks(item)
	JazzApplyStackContext(item, unit)
	local amount = item.Amount or 0
	if amount <= personal then
		return
	end
	local excess = amount - personal
	local refund = JazzCloneStackRemainder(item, excess)
	if not refund then
		-- Keep oversized rather than lose rounds.
		return
	end
	item.Amount = personal
	if not JazzDepositItemToSquadBag(unit, refund) then
		local ok_amt, leftover = pcall(function()
			return refund.Amount
		end)
		if ok_amt and leftover and leftover > 0 then
			item.Amount = personal + leftover
			DoneObject(refund)
		end
	end
	ObjModified(unit)
end

function JazzSpillUnitInventoryExcess(unit)
	if not unit or not unit.ForEachItem then
		return
	end
	local spills = {}
	unit:ForEachItem(function(item)
		if IsKindOf(item, "InventoryStack") then
			local personal = JazzGetPersonalMaxStacks(item)
			if (item.Amount or 0) > personal then
				spills[#spills + 1] = item
			end
		end
	end)
	for _, item in ipairs(spills) do
		JazzSpillPersonalStackExcess(unit, item)
	end
end

-- Put ejected magazine ammo back into merc loadout; remainder drops at feet (not squad bag).
function JazzDropAmmoAtFeet(unit, item)
	if not item then
		return true
	end
	if item.Amount <= 0 then
		DoneObject(item)
		return true
	end
	local map_unit = unit
	if IsKindOf(unit, "UnitData") then
		map_unit = g_Units and unit.session_id and g_Units[unit.session_id]
	end
	if map_unit and IsValid(map_unit) and GetDropContainer then
		local container = GetDropContainer(map_unit, false, item)
		if container then
			MergeStackIntoContainer(container, "Inventory", item)
			if item.Amount <= 0 then
				DoneObject(item)
				return true
			end
			local pos = container:AddItem("Inventory", item)
			if pos then
				return true
			end
			container = GetDropContainer(map_unit, false, item)
			if container then
				pos = container:AddItem("Inventory", item)
				if pos then
					return true
				end
			end
		end
	end
	-- Satellite / no tactical unit: sector inventory, never silent delete.
	if unit and unit.Squad and gv_Squads and gv_Squads[unit.Squad] then
		local sector = gv_Squads[unit.Squad].CurrentSector
		if sector and AddToSectorInventory then
			AddToSectorInventory(sector, { item })
			return true
		end
	end
	return false
end

function JazzReturnEjectedAmmo(unit, item)
	if not item then
		return true
	end
	if item.Amount <= 0 then
		DoneObject(item)
		return true
	end
	if unit then
		local slot = JazzGetAmmoLoadoutSlot(unit, item)
		if slot and unit.CheckClass and unit:CheckClass(item, slot) then
			JazzApplyStackContext(item, unit)
			MergeStackIntoContainer(unit, slot, item)
			if item.Amount <= 0 then
				DoneObject(item)
				ObjModified(unit)
				return true
			end
			local pos = unit:AddItem(slot, item)
			if pos then
				ObjModified(unit)
				return true
			end
		end
	end
	return JazzDropAmmoAtFeet(unit, item)
end

-- Prefer largest stacks, then stable id — avoids "random" AmmoInventory pick order.
function JazzSortAmmoStacksForReload(ammo_items)
	if not ammo_items or #ammo_items < 2 then
		return ammo_items
	end
	table.sort(ammo_items, function(a, b)
		local aa, ba = a.Amount or 0, b.Amount or 0
		if aa ~= ba then
			return aa > ba
		end
		return (a.id or 0) < (b.id or 0)
	end)
	return ammo_items
end

function MergeStackIntoContainer(dest_container, dest_slot, item, check, up_to_amount, local_changes)
	local function get_local_changes(i)
		return local_changes and local_changes[i] or 0
	end

	-- Same class, different RemovableComponentId — never merge (was: collimator+compensator → Amount=2).
	-- Identical catalog remountables (five JAZZ_Bipod) must stack; clipping Amount to 1 deleted extras.
	local a = Min(item.Amount, up_to_amount or item.Amount)
	local other_stack_items = {}
	dest_container:ForEachItemInSlot(dest_slot, false, function(item_at_dest)
		if JazzInventoryItemsCanStack(item, item_at_dest) then
			table.insert(other_stack_items, item_at_dest)
		end
	end)

	table.sort(other_stack_items, function(a, b)
		local a_a = a.Amount + get_local_changes(a)
		local b_a = b.Amount + get_local_changes(b)
		return a_a > b_a
	end)

	for _, item_at_dest in ipairs(other_stack_items) do
		local max = JazzGetStackMax(item_at_dest, dest_container)
		JazzApplyStackContext(item_at_dest, dest_container)
		local to_add = max - (item_at_dest.Amount + get_local_changes(item_at_dest))
		to_add = Min(to_add, a)
		if to_add > 0 then
			a = a - to_add
			if not check then
				item.Amount = item.Amount - to_add
				item_at_dest.Amount = item_at_dest.Amount + to_add
			elseif local_changes then
				local_changes[item] = (local_changes[item] or 0) - to_add
				local_changes[item_at_dest] = (local_changes[item_at_dest] or 0) + to_add
			end
			if a <= 0 then
				break
			end
		end
	end

	assert(a >= 0)
	return a ~= item.Amount, a
end

local JazzMoveItem_Original = rawget(_G, "MoveItem")
if JazzMoveItem_Original then
	local function JazzClampMoveStorageToPersonal(args)
		local item = args.item
		local dest = args.dest_container
		local src = args.src_container
		if not item or not dest or type(dest) ~= "table" then
			return
		end
		if not IsKindOf(item, "InventoryStack") then
			return
		end
		-- drop / unopened bag ids resolved later inside MoveItem
		if dest == "drop" or type(dest) == "number" then
			return
		end
		if JazzIsStorageInventory(dest) then
			return
		end
		-- only clamp when leaving storage (or oversized storage-marked stack)
		local from_storage = src and JazzIsStorageInventory(src)
		local personal = JazzGetPersonalMaxStacks(item)
		if not from_storage and item.Amount <= personal then
			return
		end
		if item.Amount <= personal then
			return
		end

		local dest_slot = args.dest_container_slot_name or args.dest_slot
		local dest_x = args.dest_x or args.x

		if args.check_only then
			if not args.amount or args.amount > personal then
				args.amount = personal
			end
			return
		end

		-- Auto-place: fill existing personal stacks first, then place at most one personal stack.
		if not dest_x and not args.amount and dest_slot then
			JazzEnsureContainerStackContext(dest)
			MergeStackIntoContainer(dest, dest_slot, item, false, nil)
			if item.Amount <= 0 then
				if src then
					local src_slot = args.src_container_slot_name or args.src_slot
					if src_slot then
						src:RemoveItem(src_slot, item, "no_update")
					end
				end
				DoneObject(item)
				args.item = false
				args._jazz_fully_merged = true
				ObjModified(src)
				ObjModified(dest)
				if not args.no_ui_respawn and InventoryUIRespawn then
					InventoryUIRespawn()
				end
				return
			end
		end

		if item.Amount > personal and (not args.amount or args.amount > personal) then
			args.amount = personal
		end
	end

	function MoveItem(args)
		local prefer_set = false
		if type(args) == "table" then
			if args.dest_container and type(args.dest_container) == "table" then
				JazzEnsureContainerStackContext(args.dest_container)
			end
			if args.src_container and type(args.src_container) == "table" then
				JazzEnsureContainerStackContext(args.src_container)
			end
			if args.s_item_at_dest and args.dest_container and type(args.dest_container) == "table" then
				JazzApplyStackContext(args.s_item_at_dest, args.dest_container)
			end
			JazzClampMoveStorageToPersonal(args)
			if args._jazz_fully_merged then
				return false
			end
			if not args.item then
				return false
			end
			-- Drag-reload onto weapon: vanilla dumps prev mag into squad bag — prefer loadout stacks.
			if not args.check_only and IsReload and args.dest_container and type(args.dest_container) == "table" then
				local dest = args.dest_container
				local dest_slot = args.dest_container_slot_name or args.dest_slot
				local dx, dy = args.dest_x or args.x, args.dest_y or args.y
				local item_at_dest = dx and dest_slot and dest.GetItemInSlot and dest:GetItemInSlot(dest_slot, nil, dx, dy)
				if item_at_dest and IsReload(args.item, item_at_dest) then
					local unit = IsKindOfClasses(dest, "Unit", "UnitData") and dest
						or IsKindOfClasses(args.src_container, "Unit", "UnitData") and args.src_container
					if unit then
						rawset(_G, "JazzEjectedAmmoPreferUnit", unit)
						prefer_set = true
					end
				end
			end
		end
		local a, b, c = JazzMoveItem_Original(args)
		if prefer_set then
			rawset(_G, "JazzEjectedAmmoPreferUnit", false)
		end
		if type(args) == "table" and args.item and args.dest_container and type(args.dest_container) == "table" and IsValid(args.item) then
			JazzApplyStackContext(args.item, args.dest_container)
			-- Safety: never leave Amount > personal max on a unit stack after move.
			-- Excess goes to squad bag (never silent-delete).
			if not JazzIsStorageInventory(args.dest_container) and IsKindOf(args.item, "InventoryStack") then
				local unit = IsKindOfClasses(args.dest_container, "Unit", "UnitData") and args.dest_container
					or IsKindOfClasses(args.src_container, "Unit", "UnitData") and args.src_container
				if JazzSpillPersonalStackExcess then
					JazzSpillPersonalStackExcess(unit, args.item)
				end
			end
		end
		return a, b, c
	end
end

function InventoryStack:MergeStack(otherItem, amount)
	if not JazzInventoryItemsCanStack(self, otherItem) then
		return false
	end
	amount = amount or otherItem.Amount
	local max
	if JazzIsStorageStackUI(self) then
		max = const.JazzStorageStackMax
	else
		max = JazzGetPersonalMaxStacks(self)
		rawset(self, "MaxStacks", max)
	end
	local to_add = Min(amount, otherItem.Amount, max - self.Amount)
	if to_add < 0 then
		to_add = 0
	end
	self.Amount = self.Amount + to_add
	otherItem.Amount = otherItem.Amount - to_add
	return otherItem.Amount <= 0
end

function InventoryStack:GetItemSlotUI()
	if JazzIsStorageStackUI(self) then
		if self.colorStyle then
			return Untranslated("<style " .. self.colorStyle .. ">" .. self.Amount .. "<valign bottom 0></style>")
		end
		return Untranslated("<style InventoryItemsCount>" .. self.Amount .. "<valign bottom 0></style>")
	end
	local max = JazzGetPersonalMaxStacks(self)
	if self.colorStyle then
		return Untranslated("<style " .. self.colorStyle .. ">" .. self.Amount .. "<valign bottom 0><style " .. self.colorStyle .. ">/" .. max .. "</style>")
	end
	return T{709831548750, "<style InventoryItemsCount><cur><valign bottom 0><style InventoryItemsCountMax>/<max></style>",
		cur = self.Amount, max = max}
end
