local equip_slots = {
	["Handheld A"] = true,	
	["Handheld B"] = true,
	["Head"] = true,
	["HeadGear"] = true,    
	["ArmorPlate"] = true,  
	["Torso"] = true,
	["Legs"] = true,
	["Vest"] = true,    
	["Belt1"] = true,
	["Belt2"] = true,
	["Backpack"] = true,
}

function IsEquipSlot(slot_name)
	return equip_slots[slot_name]
end

function IsWeaponSlot(slot_name)
	return slot_name=="Handheld A" or slot_name=="Handheld B"
end

function GetSlotsToEquipItem(item)
	if not item then return end
	local canequipslots = {}
	local slots = UnitInventory.inventory_slots
	for _, slot_data in ipairs(slots) do
		local slot_name = slot_data.slot_name
		if IsEquipSlot(slot_name) then
			local base_class = slot_data.base_class
			if item:IsKindOfClasses(base_class) and (not slot_data.check_slot_name or item.Slot==slot_name) then
				canequipslots[#canequipslots +1] = slot_name
			end	
		end
	end
	return canequipslots
end

UndefineClass('UnitInventory')
DefineClass.UnitInventory = {
	__parents = { "Inventory" },
	inventory_slots = {
		{ slot_name = "Inventory",     width = 4, height = 5, base_class = "InventoryItem", enabled = true },
		{ slot_name = "InventoryDead", width = 7, height = 3, base_class = "InventoryItem", enabled = true },
		{ slot_name = "Pick",          width = 2, height = 1, base_class = "InventoryItem", enabled = true },
		{ slot_name = "Handheld A",    width = 2, height = 1, base_class = {"Firearm","MeleeWeapon","HeavyWeapon","QuickSlotItem"}, enabled = true },
		{ slot_name = "Handheld B",    width = 2, height = 1, base_class = {"Firearm","MeleeWeapon","HeavyWeapon","QuickSlotItem"}, enabled = true },
		{ slot_name = "Head",          width = 1, height = 1, base_class = "Armor", check_slot_name = true, enabled = true },
        { slot_name = "HeadGear",      width = 1, height = 1, base_class = "Armor", check_slot_name = true, enabled = true },       
		{ slot_name = "ArmorPlate",      width = 1, height = 1, base_class = "Armor", check_slot_name = true, enabled = true },      
		{ slot_name = "Torso",         width = 1, height = 1, base_class = "Armor", check_slot_name = true, enabled = true },
		{ slot_name = "Legs",          width = 1, height = 1, base_class = "Armor", check_slot_name = true, enabled = true },
		{ slot_name = "SetpieceWeapon",width = 2, height = 1, base_class = {"Firearm","MeleeWeapon","HeavyWeapon"}, enabled = true },
		{ slot_name = "Vest",      width = 1, height = 1, base_class = "Vest", check_slot_name = true, enabled = true },   
--		{ slot_name = "InventoryVest",     width = 0, height = 0, base_class = "InventoryItem", enabled = true },    
		{ slot_name = "Belt1",         width = 1, height = 1, base_class = {"Armor","MeleeWeapon","QuickSlotItem"}, check_slot_name = true, enabled = true },
		{ slot_name = "Belt2",          width = 1, height = 1, base_class = {"Armor","MeleeWeapon","QuickSlotItem"}, check_slot_name = true, enabled = true },
		{ slot_name = "Backpack",	width = 1, height = 1, base_class = {"Vest"}, check_slot_name = true, enabled = true },

	},
	properties = {
		{ id = "current_weapon", editor = "text", default =  "Handheld A"},
	},
	pick_slot_item_src = false,
}

function UnitInventory:GetMaxTilesInSlot(slot_name)
	if slot_name=="Inventory" then
		return self:GetInventoryMaxSlots()
	elseif slot_name=="InventoryDead" then
		local max_slots = 21--self.max_dead_slot_tiles or 28
		local rem = max_slots % 7
		if rem > 0 then
			max_slots = max_slots + 7 - rem
		end
		
		return max_slots
	else
		return Inventory.GetMaxTilesInSlot(self,slot_name)
	end
end

function UnitProperties:GetInventoryMaxSlots()
	return IsMerc(self) and Max(4, (self.Strength - 30)/5) or self.max_dead_slot_tiles or 20
end

function UnitInventory:GetEquipedArmour()
	local slots = {"Head", "Torso", "Legs", "HeadGear", "ArmorPlate"}
	local items = {}
	
	for _, slot in ipairs(slots) do
		local item = self:GetItemAtPos(slot, 1, 1)
		if item then
			items[#items+1] = item
		end
	end

	
	return items
end


function UnitInventory:AddItem(slot_name, item, left, top, local_execution)
	local pos, reason = Inventory.AddItem(self, slot_name, item, left, top)
	if not pos then return pos, reason end
	
	item.owner = IsMerc(self) and self.session_id or false -- Dont bloat save with non-merc owners.
	if not local_execution then
		Msg("ItemAdded", self, item, slot_name, pos)
	end
	item:OnAdd(self, slot_name, pos, item)

	return pos, reason
end

-- add already generated items (from loot table) into inventory, stack them if can
function AddItemsToInventory(inventoryObj, items, bLog)
	local pos, reason
	for i = #items, 1, -1 do
		local item =  items[i]
		if IsKindOf(item, "InventoryStack") then
			inventoryObj:ForEachItemDef(item.class, 
				function(curitm, slot_name, item_left, item_top)
					if slot_name~="Inventory" then return end
					
				   if curitm.Amount < curitm.MaxStacks then
						local to_add = Min(curitm.MaxStacks - curitm.Amount, item.Amount)
						curitm.Amount =curitm.Amount + to_add
						curitm.drop_chance = Max(curitm.drop_chance, item.drop_chance)
						if bLog then
							Msg("InventoryAddItem", inventoryObj, curitm, to_add)
						end
						item.Amount =  item.Amount - to_add			
						if item.Amount <= 0 then
							DoneObject(item)
							item = false
							table.remove(items, i)
							return "break"
						end
					end
				end)
		end
		if item then 
			pos, reason = inventoryObj:AddItem("Inventory", item)
			if pos then
				if bLog then
					Msg("InventoryAddItem", inventoryObj, item, IsKindOf(item, "InventoryStack") and item.Amount or 1)
				end
				table.remove(items, i)
			end
		else
			pos = true
		end				
	end
	ObjModified(inventoryObj)
	return pos, reason
end

function UnitInventory:AddItemsToInventory(items)
	return AddItemsToInventory(self, items, true)
end


function OnMsg.InventoryAddItem(unit, item, amount)
	LogGotItem(unit, item, amount)
end

GameVar("g_GossipItemsTakenByPlayer",{})
GameVar("g_GossipItemsSeenByPlayer",{})
GameVar("g_GossipItemsEquippedByPlayer",{})
GameVar("g_GossipItemsMoveFromPlayerToContainer",{})

function OnMsg.InventoryTakeAllAddItem(unit, item, amount, bAutoResolve)
	local item_id = item.id
	if not g_GossipItemsTakenByPlayer[item_id] and (bAutoResolve or g_GossipItemsSeenByPlayer[item_id]) then
		NetGossip("Loot","TakeByPlayer", item.class, amount, GetCurrentPlaytime(), Game and Game.CampaignTime)
		g_GossipItemsTakenByPlayer[item_id] = true
	end
	LogGotItem(unit, item, amount)
end

function OnMsg.SquadBagAddItem(item, amount)
	LogGotItem(false, item, amount)
end

function OnMsg.SquadBagTakeAllAddItem(item, amount, bAutoResolve)
	local item_id = item.id
	if not g_GossipItemsTakenByPlayer[item_id] and (bAutoResolve or g_GossipItemsSeenByPlayer[item_id])then
		NetGossip("Loot","TakeByPlayer", item.class, amount, GetCurrentPlaytime(), Game and Game.CampaignTime)
		g_GossipItemsTakenByPlayer[item_id] = true
	end	
	LogGotItem(false, item, amount)
end

if FirstLoad then
	DeferredItemLog = false
	CombatLogActorOverride = false
end

function OnMsg.NewGame()
	DeferredItemLog = false
	CombatLogActorOverride = false
end

TFormat.ItemLog = function(itemLog, unit, isSingleEntry)
	local amount = itemLog.amount or 1
	local itemNameT
	if amount > 1 then
		itemNameT = itemLog.item.DisplayNamePlural
	else
		itemNameT = itemLog.item.DisplayName
	end
	
	local res 
	if isSingleEntry then
		if unit then
			if IsKindOf(unit, "SectorStash") then
				res = T(585970067597, "Some of the items were placed in the sector stash")
			else	
				res = T{849649099073, " <amount> x <em><itemNameT></em> taken by <mercName>", amount = amount, itemNameT = itemNameT, mercName = unit:GetDisplayName()}
			end
		else
			res = T{359344947585, " <amount> x <em><itemNameT></em> added in the squad bag", amount = amount, itemNameT = itemNameT}
		end
	else
		if unit then
			if IsKindOf(unit, "SectorStash") then
				res = T(585970067597, "Some of the items were placed in the sector stash")
			else	
				res = T{581384045758, " <amount> x <em><itemNameT></em> (<mercName>)", amount = amount, itemNameT = itemNameT, mercName = unit:GetDisplayName()}
			end
		else
			res = T{437609056132, " <amount> x <em><itemNameT></em> (squad bag)", amount = amount, itemNameT = itemNameT}
		end
	end
	return res
end

function LogGotItem(unit, item, amount)
	if not item then return end
	--allow logs of ammo, parts and meds
	--if not IsKindOf(unit, "Unit") then return false end
	
	amount = amount or 1
	local actor = CombatLogActorOverride or "short"
	local logItem = { 
		unit = unit,
		item = item,
		amount = amount,
		actor = actor,
	}
	
	if DeferredItemLog then
		DeferredItemLog[#DeferredItemLog + 1] = logItem
		return
	end
	
	DeferredItemLog = { logItem }
	CreateRealTimeThread(function()
		Sleep(1)
		local text = false
		if #DeferredItemLog > 1 then
			local mercPickedUpItems = {}
			for i, log in ipairs(DeferredItemLog) do
				local amount = log.amount
				if amount == 0 then goto continue end

				if not mercPickedUpItems[log.unit] then
					mercPickedUpItems[log.unit] = {log}
				else
					for j, logItem in ipairs(mercPickedUpItems[log.unit]) do
						if log.item.class == logItem.item.class then
							logItem.amount = logItem.amount + log.amount
							goto continue
						end
					end
					table.insert(mercPickedUpItems[log.unit], log)
				end
				::continue::
			end
			
			local lineActor = DeferredItemLog[1].actor == "short" and "helper" or "importanthelper"
			
			CombatLog(DeferredItemLog[1].actor, T(435437836774, "Items acquired:"))
			local lines = {}
			
			for unit, itemsLog in pairs(mercPickedUpItems) do
				
				for _, itemLog in ipairs(itemsLog) do
					CombatLog(lineActor, TFormat.ItemLog(itemLog, unit))
				end
			end
			
			
			
			
		else
			text = TFormat.ItemLog({amount = amount, item = item}, unit, "singleEntry")
			CombatLog(DeferredItemLog[1].actor, text)
		end
		DeferredItemLog = false
	end)
end

function UnitInventory:RemoveItem(slot_name, item,...)
	local item, pos = Inventory.RemoveItem(self, slot_name, item,...)
	if not item then return end
	item:OnRemove(self, slot_name, pos, item)
	if IsKindOf(item, "BaseWeapon") and IsKindOf(self, "Unit") then
		-- Remove perk modifiers associated with this item.
		for _, id in ipairs(self.StatusEffects) do
			item:RemoveModifiers(id)
		end
	end	
	Msg("ItemRemoved", self, item, slot_name, pos)
	
	return item, pos
end

function UnitInventory:GetAvailableAmmos(weapon, ammo_type, unique)
	if not IsKindOfClasses(weapon, "Firearm", "HeavyWeapon") then
		return empty_table
	end
	local ammo_class = IsKindOfClasses(weapon, "HeavyWeapon", "FlareGun") and "Ordnance" or "Ammo"
	local types = {}
	local containers = {}
	local slots = {}

	local slot_name = GetContainerInventorySlotName(self)
	local caliber = weapon.Caliber
	self:ForEachItemInSlot(slot_name, ammo_class, function(ammo, slot_name, left, top, types, ammo_type, caliber, unique)
		if (not ammo_type or ammo.class == ammo_type) and ammo.Caliber == caliber then
			if not unique or not table.find(types, "class", ammo.class) then
				table.insert(types, ammo)
			end
		end
	end, types, ammo_type, caliber, unique)
	for i = 1, #types do
		containers[i] = self
		slots[i] = slot_name
	end

	local bag = GetSquadBag(self.Squad)	
	for _, ammo in ipairs(bag) do
		if IsKindOf(ammo, ammo_class)and (not ammo_type or ammo.class == ammo_type) and ammo.Caliber == caliber then
			if not unique or not table.find(types, "class", ammo.class) then
				table.insert(types, ammo)
				table.insert(containers, bag)
			end
		end
	end
	return types, containers, slots
end

local l_count_available_ammo

-- count available ammo im mercs backpack and squads backpack
function UnitInventory:CountAvailableAmmo(ammo_type)
	l_count_available_ammo = 0
	local slot_name = GetContainerInventorySlotName(self)
	self:ForEachItemInSlot(slot_name, ammo_type, function(ammo, slot, left, top, ammo_type)
		if (not ammo_type or ammo.class == ammo_type) then
			l_count_available_ammo = l_count_available_ammo + ammo.Amount
		end
	end, ammo_type)
	local bag = GetSquadBag(self.Squad)
	for _, ammo in ipairs(bag) do
		if (not ammo_type or ammo.class == ammo_type) then
			l_count_available_ammo = l_count_available_ammo + ammo.Amount
		end
	end
	return l_count_available_ammo
end

function UnitInventory:ReloadWeapon(gun, ammo_type, delayed_fx, ai)
	local reloaded
	local ammo
	local ammo_items = {}
	local bag = self.Squad and GetSquadBagInventory(self.Squad)
	if not ammo_type or type(ammo_type) == "string" then
		if not ammo_type and gun.ammo then 
			ammo_type = gun.ammo.class
			ammo = self:GetAvailableAmmos(gun, ammo_type)
			if not ammo then 
				ammo = self:GetAvailableAmmos(gun)
			end
		else
			ammo = self:GetAvailableAmmos(gun, ammo_type)
		end
		ammo_items = ammo and table.ifilter(ammo, function(idx, stack) return stack.class == ammo[1].class and stack.Amount > 0 end)
		ammo = table.remove(ammo_items, 1)
	else
		ammo = ammo_type
		ammo_items = self:GetAvailableAmmos(gun, ammo_type.class)
		table.remove_value(ammo_items, ammo)
	end
	
	local prev, playedFX, change
	while ammo and (ai or ((gun.ammo and gun.ammo.Amount or 0) < gun.MagazineSize) or not gun.ammo or gun.ammo.class ~= ammo.class) do
		prev, playedFX, change = gun:Reload(ammo, nil, delayed_fx)
		local vo = gun:GetVisualObj()
		if (change or ai) and vo and not playedFX then
			CreateGameTimeThread(function(weapon, obj, delayed_fx)
				--Added randomness for weapon reload to cover the case with all mercs reloading on combat end or ReloadMultiSelection shortcut(both are during unpaused game)
				if delayed_fx then
					Sleep(InteractionRand(500, "ReloadDelay"))
				end
				if GetMercInventoryDlg() then
					PlayFX("WeaponLoad", "start", obj.object_class or (obj.weapon and obj.weapon.object_class), obj)
				else
					local actor_class = obj.fx_actor_class
					obj.fx_actor_class = weapon.class
					PlayFX("WeaponReload", "start", obj)
					obj.fx_actor_class = actor_class
				end
			end, gun, vo, delayed_fx)
			playedFX = true
		end
		ai = false	
		reloaded = true	
		local slot_name = GetContainerInventorySlotName(self)
		if ammo.Amount <= 0 then
			self:RemoveItem(slot_name, ammo)	
			if bag then
				bag:RemoveItem("Inventory", ammo)
			end
			ammo = table.remove(ammo_items, 1) -- keep loading from the next item stack if there's one and still not fully loaded
		else
			ObjModified(ammo)
		end
		if prev then
			if prev.Amount == 0 then
				DoneObject(prev)
			else
				bag:AddAndStackItem(prev)
			end
		end
	end
	
	if reloaded then
		local reloadOptions = GetReloadOptionsForWeapon(gun, self)
		if gun.ammo and gun.ammo.Amount and gun.ammo.Amount < gun.MagazineSize and not next(reloadOptions) then
			PlayVoiceResponse(self, "AmmoLow")
		end
	end
	
	Msg("WeaponReloaded", self)
	ObjModified("WeaponReloaded")
	return reloaded
end

function UnitInventory:GetEquippedWeaponSlot(weapon)
	if self:FindItemInSlot("Handheld A", function(item, weapon) return item == weapon end, weapon) then
		return "Handheld A"
	elseif self:FindItemInSlot("Handheld B", function(item, weapon) return item == weapon end, weapon) then
		return "Handheld B"
	end
end

-- check for equipped weapons in specified Handheld slot
function UnitInventory:GetEquippedWeapons(slot_name, class)
	local weapons = {}
	self:ForEachItemInSlot(slot_name,function(item, s, l,t, weapons, class)
		if item:IsWeapon() and (not class or IsKindOf(item, class)) then
			weapons[#weapons + 1] = item
		end	
	end, weapons, class)
	return weapons
end

function UnitInventory:GetItemsInWeaponSlot(slot_name) 
	local items = {}
	self:ForEachItemInSlot(slot_name, function(item, slot, x, y, items)
		items[x] = item
	end, items)
	table.compact(items) -- Items will be sorted by x
	return items
end

function UnitInventory:FindWeaponInSlotById(slot, id)
	return self:FindItemInSlot(slot, function(item, id)
		if item.id == id then
			return item
		end
		if IsKindOf(item, "Firearm") then
			local min
			for slot, sub in pairs(item.subweapons) do
				if sub.id == id and (not min or lessthan(sub, min)) then
					min = sub
				end
			end
			if min then
				return min
			end
		end
	end, id)
end

function UnitInventory:InventoryBandage()
	local target = self
	local medicine = GetUnitEquippedMedicine(self)

	target:GetBandaged(medicine, self)
	Msg("InventoryChange", self)
end

function UnitInventory:GetBandaged(medkit, healer)
	if not self:HasStatusEffect("Bleeding") and self.HitPoints >= self.MaxHitPoints then
		return
	end
	
	-- Hemophobic quirk
	local chance = CharacterEffectDefs.Hemophobic:ResolveValue("procChance")
	if HasPerk(self, "Hemophobic") then
		local roll = InteractionRand(100, "Hemophobic")
		if roll < chance then
			PlayVoiceResponse(self, "Hemophobic")
			CombatLog("debug", T{Untranslated("<em>Hemophobic</em> proc on <unit>"), unit = self.Name})
			if g_Combat and IsValid(healer) and healer:GetBandageTarget() == self then
				healer:SetCommand("EndCombatBandage")
			end
			PanicOutOfSequence({self})
			return
		end
	end
	
	local heal_amount, condition_rate = healer:CalcHealAmount(medkit, self)	
	if (heal_amount or 0) <= 0 then
		return
	end
		
	-- restore hp up to (current) max hp
	local old_hp = self.HitPoints
	self.HitPoints = Min(self.MaxHitPoints, self.HitPoints + heal_amount)
	local restored = self.HitPoints - old_hp
	self:OnHeal(restored, medkit, healer)
	
	if healer == self then
		CombatLog("short", T{934288978076, "<target> <em>bandaged</em> their wounds (<em><amount> HP</em> restored)",
			target = self.Nick or self.Name,
			amount = restored,
		})
	else
		CombatLog("short", T{559041931277, "<target> was <em>bandaged</em> by <healer> (<em><amount> HP</em> restored)",
			healer = healer.Nick or healer.Name,
			target = self.Nick or self.Name,
			amount = restored,
		})
		PlayVoiceResponse(self, "HealReceived")
	end
	
	local condition_loss = Max(1, MulDivRound(restored, 100, CombatActions.Bandage:ResolveValue("MaxConditionHPRestore")))
	condition_loss = Max(1, MulDivRound(condition_loss, condition_rate, 100))
	medkit.Condition = Clamp(medkit.Condition - condition_loss, 0, 100)
	local slot = healer:GetItemSlot(medkit)
	if slot and medkit.Condition <= 0 then
		CombatLog("short", T{831717454393, "<merc>'s <item> has been depleted", merc = healer.Nick, item = medkit.DisplayName})
		--healer:RemoveItem(slot, medkit)
		--DoneObject(medkit)
	end
		
	ObjModified(self)
	Msg("OnBandage", healer, self, restored)
	Msg("OnBandaged", healer, self, restored)
	healer:CallReactions("OnUnitBandaged", healer, self, restored)
	if healer ~= self then
		self:CallReactions("OnUnitBandaged", healer, self, restored)
	end
	if IsValid(healer) then
		Msg("InventoryChange", healer)
	end
end

function UnitInventory:OnHeal(hp, medkit, healer)
	Msg("OnHeal", self, hp, medkit, healer)
end

function UnitInventory:GetHandheldItems()
	local items = {}
	local slots = {}
	local item = false
	
	local y = 1
	for i = 1, 2 do
		local slot = (i == 1) and "Handheld A" or "Handheld B"
		for x = 1, 2 do
			item = self:GetItemAtPos(slot, x, y)
			if item then
				items[#items+1] = item
				slots[#slots+1] = slot
			end
		end
	end
	
	return items, slots
end



function NpcUnitGiveItem:__exec(obj, context)
	local units = empty_table
	local group = Groups[self.TargetUnit] 
	if group then
		local unitClass = {}
		for i, obj in ipairs(group) do
			if IsKindOf(obj, "Unit") then
				unitClass[#unitClass + 1] = obj
			end
		end
		units = unitClass
	else
		units = context.target_units or units
	end
	if not units or not units[1] then return end
	
	local items = {}
	if self.ItemId and self.ItemId~="" then
		table.insert(items, PlaceInventoryItem(self.ItemId))	
	end
	
	if self.LootTableId then
		local loot_tbl = LootDefs[self.LootTableId]
		if loot_tbl then
			loot_tbl:GenerateLoot(self, {}, InteractionRand(nil, "NpcGive"), items)
		end
	end
	
	local unit = units[1]
	for i, item in ipairs(items) do
		item.drop_chance = self.DontDrop and 0 or 100
		if unit:CanAddItem("Handheld A", item) then
			unit:AddItem("Handheld A", item)
		elseif unit:CanAddItem("Head", item) then
			unit:AddItem("Head", item)
        elseif unit:CanAddItem("HeadGear", item) then
			unit:AddItem("HeadGear", item)
		elseif unit:CanAddItem("Torso", item) then
			unit:AddItem("Torso", item)
		elseif unit:CanAddItem("ArmorPlate", item) then
			unit:AddItem("ArmorPlate", item)	
		elseif unit:CanAddItem("Legs", item) then
			unit:AddItem("Legs", item)
		elseif unit:CanAddItem("Vest", item) then
			unit:AddItem("Vest", item)
		elseif unit:CanAddItem("Backpack", item) then
			unit:AddItem("Backpack", item)
		elseif unit:CanAddItem("Belt1", item) then
			unit:AddItem("Belt1", item)
		elseif unit:CanAddItem("Belt2", item) then
			unit:AddItem("Belt2", item)
		else
			unit:AddItem("Inventory", item)
		end
	end
	unit:UpdateOutfit()
end

function Unit:HasNightVision()
	if HasPerk(self, "NightOps") then
		return true
	end
	local helm = self:GetItemInSlot("Head") or self:GetItemInSlot("HeadGear")
	return IsKindOf(helm, "NightVisionGoggles") and helm.Condition > 0
end

UndefineClass('ArmorProperties')
DefineClass.ArmorProperties = {
	__parents = { "ItemWithCondition", },
	__generated_by_class = "ClassDef",

	properties = {
		{ id = "Slot", 
			editor = "combo", default = "Torso", template = true, items = function (self) return {"Head","HeadGear", "Torso", "Legs"} end, },
		{ category = "Combat", id = "PenetrationClass", 
			editor = "number", default = 1, template = true, 
			name = function(self) return "Penetration Class: " .. (PenetrationClassIds[self.PenetrationClass] or "") end, slider = true, min = 1, max = 5, modifiable = true, },
		{ category = "Combat", id = "DamageReduction", name = "Damage Reduction (Base)", help = "How much damage the armor absorbs when the attack lands in an area covered by the armor.", 
			editor = "number", default = 10, template = true, scale = "%", slider = true, min = 0, max = 100, },
		{ category = "Combat", id = "AdditionalReduction", name = "Damage Reduction (Additional)", help = "Additional damage reduction applied when the effective Penetration Class of the attack is lower than the Penetration Class of the armor protecting the hit body part.", 
			editor = "number", default = 10, template = true, scale = "%", slider = true, min = 0, max = 100, },
		{ category = "Combat", id = "ProtectedBodyParts", name = "Protected Body Parts", 
			editor = "set", default = false, template = true, items = function (self) return PresetGroupCombo("TargetBodyPart", "Default") end, },
		{ category = "Combat", id = "Camouflage", 
			editor = "bool", default = false, template = true, },
	},
}