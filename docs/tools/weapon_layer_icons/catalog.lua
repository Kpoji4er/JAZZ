return function(output)
  local catalog={source="running JA3Debug, effective temporary instances",map=GetMapName(),weapons={},mods={}}
  local function tr(value)
    if not value then return "" end
    if type(value)=="string" then return value end
    local ok,text=pcall(_InternalTranslate,value)
    return ok and text or tostring(value)
  end
  for id,definition in sorted_pairs(InventoryItemDefs) do
    local declared=g_Classes[id]
    if declared and IsKindOfClasses(declared,"Firearm","HeavyWeapon") then
      InventoryItem.DetachIdInitialization("JAZZ_CaptureCatalog")
      local ok,cls=pcall(function() return declared:new({is_clone=true}) end)
      InventoryItem.AttachIdInitialization("JAZZ_CaptureCatalog")
      if not ok then return "catalog constructor failed: "..id..": "..tostring(cls) end
      local row={id=id,entity=cls.Entity,name=tr(cls.DisplayName),plural=tr(cls.DisplayNamePlural),
        icon=cls.Icon,caliber=cls.Caliber,parents=table.copy(cls.__parents or {}),slots={}}
      for _,slot in ipairs(cls.ComponentSlots or {}) do
        local s={slot=slot.SlotType,default=slot.DefaultComponent or "",empty=slot.CanBeEmpty,
          modifiable=slot.Modifiable,options={}}
        for _,cid in ipairs(slot.AvailableComponents or {}) do
          local comp=WeaponComponents[cid]
          local option={id=cid,name=comp and tr(comp.DisplayName) or "",visuals={}}
          local chosen={}
          for _,v in ipairs(comp and comp.Visuals or {}) do
            if v:Match(id) then
              if not chosen[v.Slot] or (chosen[v.Slot]:IsGeneric() and not v:IsGeneric()) then chosen[v.Slot]=v end
            end
          end
          for spot,v in sorted_pairs(chosen) do option.visuals[#option.visuals+1]={spot=spot,entity=v.Entity or ""} end
          s.options[#s.options+1]=option
        end
        row.slots[#row.slots+1]=s
      end
      catalog.weapons[#catalog.weapons+1]=row
      cls.visual_obj=false;cls:delete()
    end
  end
  for _,mod in ipairs(ModsLoaded or {}) do
    catalog.mods[#catalog.mods+1]={id=mod.id,title=tr(mod.title),version=tostring(mod.version or mod.version_major or "")}
  end
  local err,text=LuaToJSON(catalog)
  assert(not err,tostring(err))
  assert(not AsyncStringToFile(output,text))
  return "catalog="..#catalog.weapons
end
