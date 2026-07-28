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
  for _, region in sorted_pairs(Regions or empty_table) do
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
      { category = "Legion AI", id = "LegionAIEnabled", name = "Enable Legion AI", editor = "bool", default = false },
      { category = "Legion AI", id = "ManagedOutposts", name = "Managed outposts", editor = "string_list", default = {}, item_default = "", items = function(self) return GetCampaignSectorsCombo("") end },
      { category = "Legion AI", id = "MajorHQSector", name = "Major HQ sector", editor = "combo", default = "", items = function(self) return GetCampaignSectorsCombo("") end },
      { category = "Legion AI", id = "CommandInterval", name = "Command interval (hours)", editor = "number", default = 6 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 168 * const.Scale.h },
      { category = "Legion AI", id = "OutpostRebootDelay", name = "Outpost reboot (hours)", editor = "number", default = 12 * const.Scale.h, scale = const.Scale.h, min = 0, max = 168 * const.Scale.h },
      { category = "Legion AI/Economy", id = "StartingSupply", name = "Starting money ($)", editor = "number", default = 12000, min = 0 },
      { category = "Legion AI/Economy", id = "SupplyCapacity", name = "Outpost money capacity ($)", editor = "number", default = 120000, min = 1 },
      { category = "Legion AI/Economy", id = "PassiveSupplyPerHour", name = "Base money per hour ($)", editor = "number", default = 0, min = 0 },
      { category = "Legion AI/Economy", id = "CitySupplyBonus", name = "City money per POI pulse ($)", editor = "number", default = 2500, min = 0, help = "Added to poi_money every POIGenerationInterval (default 3 days)." },
      { category = "Legion AI/Economy", id = "FarmSupplyBonus", name = "Farm money per POI pulse ($)", editor = "number", default = 800, min = 0, help = "Added to poi_money every POIGenerationInterval (default 3 days)." },
      { category = "Legion AI/Economy", id = "PoiMoneyCap", name = "POI money stock cap ($)", editor = "number", default = 12000, min = 1, help = "Max tax stock waiting on one economic POI. Prevents catch-up/debug blowups." },
      { category = "Legion AI/Economy", id = "POIGenerationInterval", name = "POI resource pulse (hours)", editor = "number", default = 72 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 336 * const.Scale.h, help = "How often city/farm $ and recruits accrue on economic POIs." },
      { category = "Legion AI/Economy", id = "POIGenerationMaxCatchup", name = "POI pulse max catch-up cycles", editor = "number", default = 1, min = 1, max = 8, help = "Missed pulses never replay more than this many cycles (avoids $21M after timer=0 / time skip)." },
      { category = "Legion AI/Economy", id = "MineDiamondPerHour", name = "Mine money per hour to shipment stock ($)", editor = "number", default = 250, min = 0 },
      { category = "Legion AI/Economy", id = "SupplyConvoyTriggerPercent", name = "Supply convoy trigger (%)", editor = "number", default = 40, min = 0, max = 100 },
      { category = "Legion AI/Economy", id = "SupplyConvoyCargo", name = "Supply convoy cargo ($)", editor = "number", default = 12000, min = 1 },
      { category = "Legion AI/Economy", id = "DiamondShipmentThreshold", name = "Shipment threshold ($)", editor = "number", default = 12000, min = 1 },
      { category = "Legion AI/Economy", id = "TaxThreshold", name = "Tax collector threshold ($)", editor = "number", default = 1000, min = 1 },
      { category = "Legion AI/Economy", id = "TaxCap", name = "Tax collector cap", editor = "number", default = 1, min = 0 },
      { category = "Legion AI/Economy", id = "TaxCargoMax", name = "Tax collector cargo max ($)", editor = "number", default = 12000, min = 1 },
      { category = "Legion AI/Economy", id = "TaxCooldown", name = "Tax collector cooldown (hours)", editor = "number", default = 24 * const.Scale.h, scale = const.Scale.h, min = 0, max = 168 * const.Scale.h },
      { category = "Legion AI/Manpower", id = "StartingManpower", name = "Outpost starting manpower", editor = "number", default = 20, min = 0 },
      { category = "Legion AI/Manpower", id = "ManpowerCapacity", name = "Outpost manpower capacity", editor = "number", default = 32, min = 1 },
      { category = "Legion AI/Manpower", id = "MajorStartingManpower", name = "Major starting manpower", editor = "number", default = 80, min = 0 },
      { category = "Legion AI/Manpower", id = "MajorManpowerCapacity", name = "Major manpower capacity", editor = "number", default = 600, min = 1 },
      { category = "Legion AI/Manpower", id = "FarmRecruitsPerDay", name = "Farm recruits per POI pulse", editor = "number", default = 2, min = 0, help = "Added every POIGenerationInterval (default 3 days)." },
      { category = "Legion AI/Manpower", id = "CityRecruitsPerDay", name = "City recruits per POI pulse", editor = "number", default = 3, min = 0, help = "Added every POIGenerationInterval (default 3 days)." },
      { category = "Legion AI/Manpower", id = "GuardpostRecruitsPerDay", name = "Guardpost recruits per POI pulse", editor = "number", default = 2, min = 0 },
      { category = "Legion AI/Manpower", id = "PortRecruitsPerDay", name = "Port recruits per POI pulse", editor = "number", default = 1, min = 0 },
      { category = "Legion AI/Manpower", id = "FarmRecruitCap", name = "Farm recruit stock cap", editor = "number", default = 8, min = 0 },
      { category = "Legion AI/Manpower", id = "CityRecruitCap", name = "City recruit stock cap", editor = "number", default = 16, min = 0 },
      { category = "Legion AI/Manpower", id = "GuardpostRecruitCap", name = "Guardpost recruit stock cap", editor = "number", default = 12, min = 0 },
      { category = "Legion AI/Manpower", id = "PortRecruitCap", name = "Port recruit stock cap", editor = "number", default = 8, min = 0 },
      { category = "Legion AI/Manpower", id = "RecruiterThreshold", name = "Recruiter threshold (people)", editor = "number", default = 8, min = 1 },
      { category = "Legion AI/Manpower", id = "RecruiterCap", name = "Recruiter cap", editor = "number", default = 1, min = 0 },
      { category = "Legion AI/Manpower", id = "RecruiterCargoMax", name = "Recruiter cargo max (people)", editor = "number", default = 16, min = 1 },
      { category = "Legion AI/Manpower", id = "RecruiterUnitTemplate", name = "Recruiter unit template", editor = "text", default = "JAZZ_Legion_Recruit", help = "Unit class added into the recruiter squad per collected recruit." },
      { category = "Legion AI/Manpower", id = "RecruiterCooldown", name = "Recruiter cooldown (hours)", editor = "number", default = 24 * const.Scale.h, scale = const.Scale.h, min = 0, max = 168 * const.Scale.h },
      { category = "Legion AI/Manpower", id = "ManpowerConvoyCargo", name = "Manpower convoy cargo", editor = "number", default = 16, min = 1 },
      { category = "Legion AI/Manpower", id = "ManpowerConvoyTriggerPercent", name = "Manpower inbound trigger (%) — unused", editor = "number", default = 0, min = 0, max = 100, help = "Legacy. Inbound Major→outpost fires only when outpost manpower is 0." },
      { category = "Legion AI/Economy", id = "MajorStartingReserve", name = "Major starting money ($)", editor = "number", default = 120000, min = 0 },
      { category = "Legion AI/Economy", id = "MajorReserveCapacity", name = "Major money capacity ($)", editor = "number", default = 1200000, min = 1 },
      { category = "Legion AI/Caps", id = "RegularSquadCap", name = "Regular squad cap", editor = "number", default = 7, min = 0 },
      { category = "Legion AI/Caps", id = "GarrisonCap", name = "Garrison cap (fallback)", editor = "number", default = 2, min = 0, help = "Used only if dynamic key-sector count is unavailable; runtime uses important Legion sectors + 1." },
      { category = "Legion AI/Caps", id = "PatrolCap", name = "Patrol cap", editor = "number", default = 2, min = 0 },
      { category = "Legion AI/Caps", id = "ReconCap", name = "Recon cap", editor = "number", default = 1, min = 0 },
      { category = "Legion AI/Caps", id = "QRFCap", name = "QRF cap", editor = "number", default = 1, min = 0 },
      { category = "Legion AI/Caps", id = "ReinforceCap", name = "Reinforce cap", editor = "number", default = 1, min = 0 },
      { category = "Legion AI/Costs", id = "GarrisonCost", name = "Garrison cost ($)", editor = "number", default = 120000, min = 0 },
      { category = "Legion AI/Costs", id = "PatrolCost", name = "Patrol cost ($)", editor = "number", default = 18000, min = 0 },
      { category = "Legion AI/Costs", id = "ReconCost", name = "Recon cost ($)", editor = "number", default = 8000, min = 0 },
      { category = "Legion AI/Costs", id = "QRFCost", name = "QRF cost ($)", editor = "number", default = 40000, min = 0 },
      { category = "Legion AI/Costs", id = "ReinforceCost", name = "Reinforce cost ($)", editor = "number", default = 25000, min = 0 },
      { category = "Legion AI/Missions", id = "GarrisonMissions", name = "Garrison missions", editor = "number", default = 3, min = 1 },
      { category = "Legion AI/Missions", id = "PatrolMissions", name = "Patrol missions", editor = "number", default = 3, min = 1 },
      { category = "Legion AI/Missions", id = "ReconMissions", name = "Recon missions", editor = "number", default = 2, min = 1 },
      { category = "Legion AI/Missions", id = "QRFMissions", name = "QRF missions", editor = "number", default = 2, min = 1 },
      { category = "Legion AI/Missions", id = "ReinforceMissions", name = "Reinforce missions", editor = "number", default = 2, min = 1 },
      { category = "Legion AI/Routine", id = "BaseRestMin", name = "Base rest min (hours)", editor = "number", default = 12 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 168 * const.Scale.h, help = "After mission budget exhausted, non-garrison squads rest this long at home (min)." },
      { category = "Legion AI/Routine", id = "BaseRestMax", name = "Base rest max (hours)", editor = "number", default = 36 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 168 * const.Scale.h, help = "After mission budget exhausted, non-garrison squads rest this long at home (max)." },
      { category = "Legion AI/Routine", id = "PatrolSectorDwellMin", name = "Patrol sector dwell min (hours)", editor = "number", default = 6 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 168 * const.Scale.h },
      { category = "Legion AI/Routine", id = "PatrolSectorDwellMax", name = "Patrol sector dwell max (hours)", editor = "number", default = 24 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 168 * const.Scale.h },
      { category = "Legion AI/Recon", id = "ReconHeatThreshold", name = "Recon Heat threshold", editor = "number", default = 250, min = 0, max = 1000 },
      { category = "Legion AI/Recon", id = "ReconObservationTime", name = "Recon observation (hours)", editor = "number", default = 3 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 168 * const.Scale.h },
      { category = "Legion AI/Recon", id = "ReconNoContactHeatReduction", name = "No-contact sector Heat reduction", editor = "number", default = 50, min = 0, max = 1000 },
      { category = "Legion AI/Recon", id = "ReportExpiryTime", name = "Report expiry (hours)", editor = "number", default = 24 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 720 * const.Scale.h },
      { category = "Legion AI/Major", id = "MajorResponseHeat", name = "Major response Heat", editor = "number", default = 800, min = 0, max = 1000 },
      { category = "Legion AI/Major", id = "MajorResponseCost", name = "Major response cost ($)", editor = "number", default = 50000, min = 0 },
      { category = "Legion AI/Major", id = "MajorResponseCooldown", name = "Major response cooldown (hours)", editor = "number", default = 72 * const.Scale.h, scale = const.Scale.h, min = 0, max = 720 * const.Scale.h },
      { category = "Legion AI/Heat", id = "SectorHeatDecay", name = "Sector Heat decay", editor = "number", default = 10, min = 0, max = 1000 },
      { category = "Legion AI/Heat", id = "RegionHeatDecay", name = "Region Heat decay", editor = "number", default = 5, min = 0, max = 1000 },
      { category = "Legion AI/Heat", id = "HeatDecayInterval", name = "Heat decay interval (hours)", editor = "number", default = 7 * const.Scale.h, scale = const.Scale.h, min = const.Scale.h, max = 168 * const.Scale.h },
      { category = "Legion AI/Squads", id = "SupplySquads", name = "Supply squads", editor = "preset_id_list", default = {}, preset_class = "EnemySquads", item_default = "" },
      { category = "Legion AI/Squads", id = "TaxSquads", name = "Tax collector squads", editor = "preset_id_list", default = {}, preset_class = "EnemySquads", item_default = "" },
      { category = "Legion AI/Squads", id = "RecruiterSquads", name = "Recruiter squads", editor = "preset_id_list", default = {}, preset_class = "EnemySquads", item_default = "" },
      { category = "Legion AI/Squads", id = "ManpowerSquads", name = "Manpower convoy squads", editor = "preset_id_list", default = {}, preset_class = "EnemySquads", item_default = "" },
      { category = "Legion AI/Squads", id = "ShipmentSquads", name = "Shipment squads", editor = "preset_id_list", default = {}, preset_class = "EnemySquads", item_default = "" },
      { category = "Legion AI/Squads", id = "MajorResponseSquads", name = "Major response squads", editor = "preset_id_list", default = {}, preset_class = "EnemySquads", item_default = "" },
      { id = "Id", editor = "text", default = "", help = "Уникальный ID региона" },
      { id = "DisplayName", editor = "text", default = "", help = "Отображаемое имя региона" },
      { id = "Description", editor = "text", default = "", help = "Описание региона" },
      { id = "Sectors", editor = "string_list", default = {}, item_default = "", items = function (self) return GetCampaignSectorsCombo("") end, help = "Сектора региона" },
      { id = "Heat", editor = "number", default = 0, help = "Legacy/default Heat; managed runtime state lives in gv_JAZZ_LegionAI", min = 0, max = 1000 },
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
        hint[#hint+1] = T{227814808041, "<Description>", Description = self.Description} 
    end
    hint[#hint+1] = T{2378508273055, "  Лояльность: <loyalty>%", loyalty = self.Loyalty or 0}
    hint[#hint+1] = T{2378508273056, "  Уровень тревоги: <heat>", heat = self:GetHeat()}

    return table.concat(hint, "\n")
end
  

  function Region:GetRuntimeState(create)
    local region_id = self.id or self.Id
    if self.LegionAIEnabled and JAZZ_GetLegionAIRegionState then
      return JAZZ_GetLegionAIRegionState(region_id, create)
    end
    return false
  end

  function Region:GetHeat()
    local state = self:GetRuntimeState(false)
    return state and state.heat or Clamp(self.Heat or 0, 0, 1000)
  end

  function Region:IncreaseHeat(amount)
    local region_id = self.id or self.Id
    if self.LegionAIEnabled and JAZZ_LegionAIChangeRegionHeat then
      return JAZZ_LegionAIChangeRegionHeat(region_id, amount or 0)
    end
    self.Heat = Clamp((self.Heat or 0) + (amount or 0), 0, 1000)
    return self.Heat
  end
  
  function Region:DecreaseHeat(amount)
    return self:IncreaseHeat(-(amount or 0))
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
    local region_id = self.id or self.Id
    if self.LegionAIEnabled and JAZZ_LegionAISetRegionHeat then
      JAZZ_LegionAISetRegionHeat(region_id, 0)
    else
      self.Heat = 0
    end
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
  

  

function JAZZ_DecaySectorHeat(region, amount)
  if not region or not gv_Sectors then
    return
  end
  for _, sector_id in ipairs(region.Sectors or empty_table) do
    local sector = gv_Sectors[sector_id]
    if sector then
      sector.Heat = Clamp((sector.Heat or 0) - (amount or 0), 0, 1000)
    end
  end
end

function JAZZ_ClampAllSectorHeat()
  for _, sector in sorted_pairs(gv_Sectors or empty_table) do
    sector.Heat = Clamp(sector.Heat or 0, 0, 1000)
  end
end

  function OnMsg.NewHour()
    local time = Game.CampaignTime
    local hours = Game.CampaignTime / const.Scale.h
    local heatdecay = 10;
    if hours % 7 ~= 0 then return end
    for _, region in pairs(Regions) do
      if region and not region.LegionAIEnabled and region.Heat and region.Heat > 0 then
        region:DecreaseHeat(MulDivRound(heatdecay, 10, 100))
      end
    end
     
  -- Уменьшаем Heat по всем открытым секторам
  for sector_id, sector in pairs(gv_Sectors) do
    local region = GetRegionForSector(sector_id)
    if not (region and region.LegionAIEnabled) and sector.Heat and sector.Heat > 0 then
      sector.Heat = Clamp(sector.Heat - heatdecay, 0, 1000)
    end
  end
end

