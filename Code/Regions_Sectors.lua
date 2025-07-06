SatelliteSector.properties[#SatelliteSector.properties + 1] = {
    category = "Region",
    id = "Heat",
    name = "Heat",
    help = "Накопленная жара в этом секторе, влияет на реакцию AI.",
    editor = "number",
    default = 0,
    min = 0,
    max = 1000,
}


function GetRegionForSector(sector_id)
  for _, region in pairs(Regions) do
      if region.Sectors then
          for _, s_id in ipairs(region.Sectors) do
              if s_id == sector_id then
                  return region
              end
          end
      end
  end
  return nil
end


DefineClass.Region = {
    __parents = {"Preset","PropertyObject" },
	__generated_by_class = "PresetDef",
    GlobalMap = "Regions",
    EditorMenubarName = "Regions",
    EditorIcon = "CommonAssets/UI/Icons/cpu.png",
    EditorMenubar = "Editors",
  
    properties = {
      { id = "Id", editor = "text", default = "", help = "Уникальный ID региона" },
      { id = "DisplayName", editor = "text", default = "", help = "Отображаемое имя региона" },
      { id = "Description", editor = "text", default = "", help = "Описание региона" },
      { id = "Sectors", editor = "string_list", default = {}, item_default = "", items = function (self) return GetCampaignSectorsCombo("") end, help = "Сектора региона" },
      { id = "Heat", editor = "number", default = 0, help = "Накопленная жара в регионе" },
      { id = "LegionScore", editor = "number", default = 0, help = "Важность региона для майора" },
      { id = "ArmyScore", editor = "number", default = 0, help = "Важность региона для армии" },
      { id = "AdonisScore", editor = "number", default = 0, help = "Важность региона для адонис" },
      { id = "PanicLevel", editor = "number", default = 0, help = "Уровень паники в регионе" },
      { id = "Loyalty", editor = "number", default = 0, help = "Лояльность" },
    },
  }

  DefineModItemPreset("Region", { EditorName = "Region", EditorSubmenu = "Satellite" })

  function Region:GetRolloverHint(sector_id)
    local hint = {}

    local sector = gv_Sectors and gv_Sectors[sector_id]
    if not sector or not g_RevealedSectors[sector_id] then
        hint[#hint+1] = T{2378508273050, "<em>Нет данных о секторе</em>"}
    else

        -- Городская часть, если есть POI с городом
        if sector.City and sector.City ~= "none" then
            local city = gv_Cities[sector.City]
            hint[#hint+1] = T{2378508273052, "<em>Город: <city></em>", city = city and city.DisplayName or "Неизвестно"}
            hint[#hint+1] = T{2378508273053, "  Лояльность: <loyalty>%", loyalty = city and city.Loyalty or 0}
        end

        if sector.Heat then
          hint[#hint+1] = T{2378508273057, "  Уровень тревоги: <heat>", heat = sector.Heat or 0}
        end

        -- Точки интереса в секторе
        local poi_list = {}
        for _, poi in ipairs(POIDescriptions) do
            if sector[poi.id] then
                poi_list[#poi_list+1] = "  • " .. (poi.display_name or "Неизвестная точка")
            end
        end

       --[[ if #poi_list > 0 then
            hint[#hint+1] = Untranslated("<em>Точки интереса:</em>")
            for _, text in ipairs(poi_list) do
                hint[#hint+1] = text
            end
        end]]
    end

    -- Инфо по региону
    hint[#hint+1] = T{2378508273054, "<em>Регион: <region></em>", region = self.DisplayName or "Неизвестно"}
    if self.Description and self.Description ~= "" then
        hint[#hint+1] = T{23785082730502, "<Description>", Description = self.Description} 
    end
    hint[#hint+1] = T{2378508273055, "  Лояльность: <loyalty>%", loyalty = self.Loyalty or 0}
    hint[#hint+1] = T{2378508273056, "  Уровень тревоги: <heat>", heat = self.Heat or 0}

    return table.concat(hint, "\n")
end
  

  function Region:IncreaseHeat(amount)
    self.Heat = self.Heat + amount
  end
  
  function Region:DecreaseHeat(amount)
    self.Heat = Max(self.Heat - amount, 0)
  end
  
  function Region:IncreasePanic(amount)
    self.PanicLevel = Min(self.PanicLevel + amount, 100)
  end
  
  function Region:DecreasePanic(amount)
    self.PanicLevel = Max(self.PanicLevel - amount, 0)
  end

  function Region:IncreaseLoyalty(amount)
    self.Loyalty = Min(self.Loyalty + amount, 100)
  end
  
  function Region:DecreaseLoyalty(amount)
    self.Loyalty = Max(self.Loyalty - amount, 0)
  end

  function Region:Reset()
    self.Heat = 0
    self.PanicLevel = 0
  end


  local raisedAlarm = false

  function OnMsg.ConflictEnd(sector, _, playerAttacked, playerWon, autoResolve, isRetreat, startedFromMap)
    -- Проверяем, есть ли сектор
    raisedAlarm = false
    if not sector then return end
  
    -- 1) Если игрок выиграл
    local base_heat = 20 + (MulDivRound(sector.CombatHeat, 10, 100) or 0)  -- базовое значение, можешь сделать динамическим
    sector.CombatHeat = 0
    if playerWon then
      -- Поднять heat в секторе
     
      sector.Heat = sector.Heat + base_heat
  
      -- Поднять heat в регионе
      local region = GetRegionForSector(sector.Id)
      if region then
        local regional_heat = MulDivRound(base_heat, 10, 100) -- 10% от heat сектора
        region:IncreaseHeat(regional_heat)
      end
  
      -- Поднять heat в соседних секторах
      ForEachSectorAround(sector.Id, 1, function(neighbor_id)
        if neighbor_id ~= sector.Id then
          local neighbor = gv_Sectors[neighbor_id]
          if neighbor then
            local neighbor_heat = MulDivRound(base_heat, 40, 100) -- например, 25% от heat сектора
            neighbor.Heat = neighbor.Heat + neighbor_heat
          end
        end
      end)
      ForEachSectorAround(sector.Id, 2, function(neighbor_id)
        if neighbor_id ~= sector.Id then
          local neighbor = gv_Sectors[neighbor_id]
          if neighbor then
            local neighbor_heat = MulDivRound(base_heat, 10, 100) -- например, 25% от heat сектора
            neighbor.Heat = neighbor.Heat + neighbor_heat
          end
        end
      end)
    end
  
    -- 2) При поражении или отступлении тоже можно сделать свою логику heat
    if not playerWon or isRetreat then
      -- Например, сильно поднимать heat за проигрыш
      local penalty_heat = base_heat
      sector.Heat = sector.Heat + penalty_heat
  
      local region = GetRegionForSector(sector.Id)
      if region then
        local regional_heat = MulDivRound(penalty_heat, 20, 100)
        region:IncreaseHeat(regional_heat)
      end
    end
  end




  function OnMsg.TurnStart()

    local sector = gv_Sectors and gv_Sectors[gv_CurrentSectorId]
    if not sector then return end
  
    local totalheat = (sector.Heat or 0) + (sector.CombatHeat or 0)
    if totalheat > 500 then

      local units = GetCurrentMapUnits("enemy")
      if g_NoiseSources and #g_NoiseSources > 0 then
        for _, unit in pairs(units) do
          local rand = InteractionRand(#g_NoiseSources, "AlarmNoise")
          local pos = g_NoiseSources[rand + 1].pos
          unit.last_known_enemy_pos = unit.last_known_enemy_pos or (pos)
        end
      end
     -- raisedAlarm = true
    end

  end


  function OnMsg.ExplorationTick()
    if raisedAlarm then return end
    local sector = gv_Sectors and gv_Sectors[gv_CurrentSectorId]
    if not sector then return end
  
    local totalheat = (sector.Heat or 0) + (sector.CombatHeat or 0)
    if totalheat > 500 then

      local units = GetCurrentMapUnits("enemy")
      for _, unit in pairs(units) do
        unit:RemoveStatusEffect("Unaware")
        if g_NoiseSources and #g_NoiseSources > 0 then
          local rand = InteractionRand(#g_NoiseSources, "AlarmNoise")
          local pos = g_NoiseSources[rand + 1].pos
          unit.last_known_enemy_pos = unit.last_known_enemy_pos or (pos)
        end
      end
      raisedAlarm = true
    end

  end

  


  function OnMsg.NewHour()
    local time = Game.CampaignTime
    local hours = Game.CampaignTime / const.Scale.h
    local heatdecay = 10;
    if hours % 7 ~= 0 then return end
    for _, region in pairs(Regions) do
      if region and region.Heat and region.Heat > 0 then
        region:DecreaseHeat(MulDivRound(heatdecay, 10, 100))
      end
    end
     
  -- Уменьшаем Heat по всем открытым секторам
  for sector_id, sector in pairs(gv_Sectors) do
    if sector.Heat and sector.Heat > 0 then
      sector.Heat = Clamp(sector.Heat - heatdecay, 0, 1000)
    end
  end
end

