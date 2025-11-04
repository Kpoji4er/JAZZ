local RegenerateLegionLootVar
function RegenerateLegionLoot() RegenerateLegionLootVar = true end

function OnMsg.OpenSatelliteView()
    if RegenerateLegionLootVar then
        _RegenerateLegionLoot()
    end
end


function _RegenerateLegionLoot()
    --print("regenerate loot")
    for _, sector in pairs(gv_Sectors) do
        local squads = sector.enemy_squads
        --print(#squads)
           for _, squad in pairs(squads) do
            local  units = squad.units
             for _, unit_id in pairs(units) do
                local unitdata = gv_UnitData[unit_id]
                --  print(unit_id)
                --  print(unit.id)
                --  print(unit.Affiliation)
                --  print(unit:IsDead())
                --  print(unit.IsMercenary)
                if unitdata and not unitdata.IsMercenary and not unitdata:IsDead() and not unitdata:IsNPC() and
                    unitdata.Affiliation then    
                
                 unitdata:ForEachItem(function(item, slot_name)
                    unitdata:RemoveItem(slot_name, item)	
                end)

                unitdata:CreateStartingEquipment(unitdata.randomization_seed)
                unitdata.innerInfoRevealed = false
                --unitdata:EquipStartingGear(items)
                --print("regenerated")
                end
                
    
            end
            --print(#units)
           end
    end
    RegenerateLegionLootVar = false
end

function __RegenerateLegionLoot()
    print("regenerate loot")
    for _, squad in ipairs(gv_Squads) do
        local units = squad.units

        for _, unit_id in ipairs(units) do
            local unitdata = gv_UnitData[unit_id]
            local unit = g_Units[unit_id]
            --  print(unit_id)
            --  print(unit.id)
            --  print(unit.Affiliation)
            --  print(unit:IsDead())
            --  print(unit.IsMercenary)
            if unitdata and not unitdata.IsMercenary and not unitdata:IsDead() and
                unitdata.Affiliation and unitdata.Affiliation == "Legion" then
                if unit then
                    unit:ForEachItem(function(item, slot)
                        unit:RemoveItem(slot, item)
                    end)
                    unit:CreateStartingEquipment(unitdata.randomization_seed)
                end

            end
            unitdata.Items = {}
            unitdata:CreateStartingEquipment(unitdata.randomization_seed)
            print("regenerated")

        end
        print(#units)
    end
    RegenerateLegionLootVar = false
end
