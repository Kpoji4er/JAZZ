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

  function Region:GetPatrolTargetWeights()
    local weights = {}
  
    for _, sector_id in ipairs(self.Sectors or empty_table) do
      local sector = gv_Sectors[sector_id]
      if sector and (sector.Side == "neutral" or sector.Side == "enemy1") then
        local weight = 0
  
        -- город
        if sector.City and sector.City ~= "none" then
          weight = weight + 50
        end

        -- бонус за ферму, остальное и так точки интереса
        if sector.Mine then
          weight = weight + 50
        end
        

        -- Точки интереса в секторе (включая шахту)
local poi_list = {}
for _, poi in ipairs(POIDescriptions) do
    if sector[poi.id] then
      weight = weight + 50
    end
end                
  
        -- +1 за каждый очко Heat
        weight = weight + (sector.Heat or 0)
  
        -- +30 если в секторе давно не было врагов (примерно)
        if sector.LastPatrolledTime then
          local days_since = (Game.CampaignTime - sector.LastPatrolledTime) / const.Scale.day
          weight = weight + Clamp(MulDivRound(days_since, 20, 1), 0, 1000)  -- 20 веса за день, макс 100
        else
          weight = weight + 100
        end
  
        if weight > 0 then
          weights[#weights + 1] = {weight, sector_id}
        end
      end
    end
  
    return weights
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

