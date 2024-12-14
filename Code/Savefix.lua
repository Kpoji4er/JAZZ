function SavegameSessionDataFixups.InventoryRemoveObsoleteItems(data)
    local l_gv_unit_data = GetGameVarFromSession(data, "gv_UnitData")
    local l_gv_sectors = GetGameVarFromSession(data, "gv_Sectors")
    local l_gv_squads = GetGameVarFromSession(data, "gv_Squads")
    -- units
    for k, merc in pairs(l_gv_unit_data) do
        -- all inventory slots 
        local deleted =  false
        merc:ForEachItem(function(item, slot_name,left, top )
            if item.ammo and (item.ammo.Amount > 0 and not table.get(Presets, "Caliber", "Default", item.ammo.Caliber, "ImpactForce")) then
                item.ammo.Amount = 0
                local tempAmmo = PlaceInventoryItem(GetAmmosWithCaliber(weapon.Caliber, "sort")[1].id)
                tempAmmo.Amount = tempAmmo.MaxStacks
                item:Reload(tempAmmo, "suspend_fx" and true)
            end
            if item.class=="InventoryItem" then
                merc:RemoveItem(slot_name, item)
                deleted =  true
            end
        end)
        if deleted then
            print("Inventory items of unknown type were found in the inventory "..merc.session_id.." - deleting them.") 
        end
    end
    -- containers
    for sector, sector_data in pairs(l_gv_sectors) do
        local deleted =  false
        local sector_inventory = sector_data.sector_inventory
        if sector_inventory then
            for _, inv_data in ipairs(sector_inventory) do
                local items = inv_data[3] or {}
                for i = #items,1, -1  do
                    local item = items[i]
                    if item and item.class=="InventoryItem" then
                        table.remove(items,i)
                        deleted = true
                    end
                end
            end
        end
        if deleted then
            print("Inventory items of unknown type were found in some containers in sector "..sector.." - deleting them.") 
        end
    end
    -- squad bags
    for squad_id, squad_data in pairs(l_gv_squads) do
        local deleted =  false
        local bag = squad_data.squad_bag
        if bag then
            for i = #bag, 1, -1  do
                local item = bag[i]
                if item and item.class=="InventoryItem" then
                    table.remove(bag,i)
                    deleted = true
                end
            end
        end
        if deleted then
            print("Inventory items of unknown type were found in the squad bags of squad "..squad_id.." - deleting them.") 
        end
    end
end