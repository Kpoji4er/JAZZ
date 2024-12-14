function ChangeSpecialization()
    local Autoriflemen = {
        "Ivan", "Ice", "Raven", "Omryn"
    }
    local Marksmen = {
        "Kalyna", "Buns"
    }
    local AllRounder = {
        "Tex","Blood"
    }
    local HeavyWeapons = {
        "Meltdown", "Grunty", "Grizzly", "Fauda"
    }
    local Stealth = {
        "Shadow", "Igor", "Reaper", "Mouse"
    }
 
    local Leader = {
        "Wolf"
    }
    
    for _, characterName in ipairs(Leader) do

        if _G[characterName] then
            _G[characterName].Specialization = "Leader"
        end
        
        if UnitDataDefs and UnitDataDefs[characterName] then
            UnitDataDefs[characterName].Specialization = "Leader"
        end
        
        if gv_UnitData and gv_UnitData[characterName] then
            gv_UnitData[characterName].Specialization = "Leader"
        end
        
        if g_Units and g_Units[characterName] then
            g_Units[characterName].Specialization = "Leader"
        end
    end

    for _, characterName in ipairs(Autoriflemen) do

        if _G[characterName] then
            _G[characterName].Specialization = "Autoriflemen"
        end
        
        if UnitDataDefs and UnitDataDefs[characterName] then
            UnitDataDefs[characterName].Specialization = "Autoriflemen"
        end
        
        if gv_UnitData and gv_UnitData[characterName] then
            gv_UnitData[characterName].Specialization = "Autoriflemen"
        end
        
        if g_Units and g_Units[characterName] then
            g_Units[characterName].Specialization = "Autoriflemen"
        end
    end

    for _, characterName in ipairs(Marksmen) do

        if _G[characterName] then
            _G[characterName].Specialization = "Marksmen"
        end
        
        if UnitDataDefs and UnitDataDefs[characterName] then
            UnitDataDefs[characterName].Specialization = "Marksmen"
        end
        
        if gv_UnitData and gv_UnitData[characterName] then
            gv_UnitData[characterName].Specialization = "Marksmen"
        end
        
        if g_Units and g_Units[characterName] then
            g_Units[characterName].Specialization = "Marksmen"
        end
    end

    for _, characterName in ipairs(AllRounder) do
        
        if _G[characterName] then
            _G[characterName].Specialization = "AllRounder"
        end
        
        if UnitDataDefs and UnitDataDefs[characterName] then
            UnitDataDefs[characterName].Specialization = "AllRounder"
        end
        
        if gv_UnitData and gv_UnitData[characterName] then
            gv_UnitData[characterName].Specialization = "AllRounder"
        end
        
        if g_Units and g_Units[characterName] then
            g_Units[characterName].Specialization = "AllRounder"
        end
    end
    
    for _, characterName in ipairs(HeavyWeapons) do
        
        if _G[characterName] then
            _G[characterName].Specialization = "HeavyWeapons"
        end
        
        if UnitDataDefs and UnitDataDefs[characterName] then
            UnitDataDefs[characterName].Specialization = "HeavyWeapons"
        end
        
        if gv_UnitData and gv_UnitData[characterName] then
            gv_UnitData[characterName].Specialization = "HeavyWeapons"
        end
        
        if g_Units and g_Units[characterName] then
            g_Units[characterName].Specialization = "HeavyWeapons"
        end
    end

    for _, characterName in ipairs(Stealth) do
        local Specialization = "Stealth"
        
        if _G[characterName] then
            _G[characterName].Specialization = "Stealth"
        end
        
        if UnitDataDefs and UnitDataDefs[characterName] then
            UnitDataDefs[characterName].Specialization = "Stealth"
        end
        
        if gv_UnitData and gv_UnitData[characterName] then
            gv_UnitData[characterName].Specialization = "Stealth"
        end
        
        if g_Units and g_Units[characterName] then
            g_Units[characterName].Specialization = "Stealth"
        end
    end

end

OnMsg.DataLoaded = function()
    ChangeSpecialization()
end

ChangeSpecialization()