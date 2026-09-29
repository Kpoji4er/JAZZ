-- Disposable native graph oracle: no screenshot, camera, light, UI or saved item.
return function(settings)
  local function require_ok(value,message) if not value then error(message) end end
  require_ok(Platform.debug and GetMapName()=="ModEditor","ModEditor debug required")
  local function write(path,value)
    local err,text=LuaToJSON(value);require_ok(not err,tostring(err))
    require_ok(not AsyncStringToFile(path,text),"write failed: "..path)
  end
  local report={phase="running",weapons={},attempts=0,graphs=0}
  local weapon,vis
  local function dispose()
    if IsValid(vis) then DoneObject(vis) end;vis=nil
    if weapon then weapon.visual_obj=false;weapon:delete() end;weapon=nil
  end
  local pause_reason="InventoryPauseSP_mp_coop_host"
  local was_paused=PauseReasons[pause_reason]
  if was_paused then Resume(pause_reason) end
  local ok,err=pcall(function()
    for _,task in ipairs(settings.tasks) do
      local rows,seen={},{}
      for _,requested in ipairs(task.builds) do
        report.attempts=report.attempts+1
        InventoryItem.DetachIdInitialization("JAZZ_LayerOracle")
        local created,result=pcall(function()
          weapon=g_Classes[task.id]:new({is_clone=true})
          for _,slot in ipairs(task.slots) do
            if requested[slot]~=nil then weapon:SetWeaponComponent(slot,requested[slot]) end
          end
        end)
        InventoryItem.AttachIdInitialization("JAZZ_LayerOracle")
        require_ok(created,tostring(result))
        local parts={task.id,weapon.Entity}
        for slot,value in sorted_pairs(weapon.components or {}) do parts[#parts+1]=slot.."="..tostring(value) end
        local key=table.concat(parts,"|")
        if not seen[key] then
          seen[key]=true
          vis=weapon:CreateVisualObj("JAZZ_LayerOracle")
          require_ok(IsValid(vis),"invalid visual: "..task.id)
          weapon:UpdateVisualObj(vis)
          local position=point(150000,150000,150000)
          vis:SetVisible(false);vis:SetPos(position);vis:SetAngle(0);vis:SetScale(100)
          local distance=(settings.camera_distances or {})[task.id] or 1500
          local function descriptor(object,spot)
            local fields={task.id,object:GetEntity(),object:GetStateText(),tostring(object:GetVisualPos()-position),tostring(object:GetVisualAxis()),object:GetVisualAngle(),object:GetWorldScale(),object:GetColorModifier(),distance}
            for n=1,#fields do fields[n]=tostring(fields[n]) end
            return {spot=spot,entity=object:GetEntity(),signature=table.concat(fields,"|")}
          end
          local graph={descriptor(vis,"__host")}
          for spot,part in sorted_pairs(vis.parts or empty_table) do
            if IsValid(part) then graph[#graph+1]=descriptor(part,spot) end
          end
          rows[#rows+1]={weapon=task.id,entity=weapon.Entity,components=table.copy(weapon.components),layer_graph=graph,label="native-pair-"..#rows,status="graph-only",requested=requested}
          report.graphs=report.graphs+1
        end
        dispose()
      end
      write(settings.output.."/"..task.id..".json",{phase="done",rows=rows})
      report.weapons[#report.weapons+1]={weapon=task.id,graphs=#rows,attempts=#task.builds}
      write(settings.output.."/progress.json",report)
      Sleep(1)
    end
  end)
  dispose()
  if was_paused then Pause(pause_reason) end
  report.inventory_pause_restored=not was_paused or not not PauseReasons[pause_reason]
  report.phase=ok and "done" or "error";report.error=not ok and tostring(err) or nil
  report.disposed=not vis and not weapon
  write(settings.output.."/progress.json",report)
  return ok and "native graph audit complete" or tostring(err)
end
