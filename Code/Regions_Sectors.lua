function RegisterRegions()
    local regions = {}
    for id, region in pairs(Presets.Region.Default or {}) do
      regions[id] = region
    end
    return regions
 
end



if FirstLoad then
	--RegisterRegions()
end

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

  function SatelliteSector:IncreaseHeat(amount)
    self.Heat = (self.Heat or 0) + amount
end

function SatelliteSector:DecreaseHeat(amount)
    self.Heat = Max((self.Heat or 0) - amount, 0)
end

  function Region:Reset()
    self.Heat = 0
    self.PanicLevel = 0
  end

  