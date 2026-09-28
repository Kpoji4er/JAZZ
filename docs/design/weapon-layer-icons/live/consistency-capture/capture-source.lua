-- Invoked as a temporary function by live.py, never installed or registered.
return function(settings)
  local function assert(value,message)
    if not value then error(message or "capture precondition failed") end
    return value
  end
  assert(GetMapName()=="ModEditor", "Capture requires isolated ModEditor test map")
  local camera={GetCamera()}
  local light=CurrentLightmodel and CurrentLightmodel[1]
  -- Explicit defaults match the photographed recipe. table.copy(Preset) is invalid
  -- in this engine and returns {}, so never pretend it clones a named preset.
  local studio=setmetatable({},LightmodelPreset)
  studio.grading_lut="Default";studio.exposure=100;studio.sun_diffuse_color=RGB(255,255,255)
  studio.sun_intensity=1000;studio.sun_azi=90;studio.sun_alt=400
  studio.use_time_of_day=false;studio.fog_density=0;studio.pp_bloom_strength=0
  local vis,weapon,backdrop
  local report={phase="running",rows={},errors={},recipe={angle=0,fov=1200,distance=(settings.distance or 0)>0 and settings.distance or 1500,
    light="fixed neutral studio v1: LightmodelPreset defaults, Default LUT, EV+1, sun1000 az90 alt40",mounts="provisional",width=1296,height=660}}
  local render_flags={RenderTerrain=0,RenderSky=0,RenderClutter=0,RenderRain=0,RenderParticles=0,
    EnablePostProcVignette=0,EnableContourOuter=0,EnableContourInner=0,EnableObjectMarking=0,
    AutoExposureMode=0,NearZ=1,ObjectLODCapMin=0}
  report.original_render={}
  for key in pairs(render_flags) do report.original_render[key]=hr[key] end
  report.original_light=light and light.id
  local function write(name,value)
    local encode_err,text=LuaToJSON(value)
    assert(not encode_err,tostring(encode_err))
    local err=AsyncStringToFile(settings.output.."/"..name,text)
    assert(not err,tostring(err))
  end
  local function dispose()
    if IsValid(backdrop) then DoneObject(backdrop) end
    backdrop=nil
    if IsValid(vis) then DoneObject(vis) end
    vis=nil
    if weapon then weapon.visual_obj=false; weapon:delete() end
    weapon=nil
  end
  local function translate(t)
    if not t then return "" end
    if type(t)=="string" then return t end
    local ok,s=pcall(_InternalTranslate,t)
    return ok and s or tostring(t)
  end
  local function snapshot(id,label,slot,cid)
    label=(settings.prefix or "")..label
    local row={weapon=id,label=label,requested_slot=slot,requested_component=cid}
    local ok,err=pcall(function()
      InventoryItem.DetachIdInitialization("JAZZ_CaptureStage")
      local created,object=pcall(function() return g_Classes[id]:new({is_clone=true}) end)
      InventoryItem.AttachIdInitialization("JAZZ_CaptureStage")
      assert(created,object);weapon=object
      assert(weapon and weapon.CreateVisualObj,"No visual constructor")
      row.prerequisites=table.copy(settings.prerequisites or {})
      InventoryItem.DetachIdInitialization("JAZZ_CaptureStage")
      local applied,apply_error=pcall(function()
        for dependency,component in sorted_pairs(settings.prerequisites or {}) do
          weapon:SetWeaponComponent(dependency,component)
          assert(weapon.components[dependency]==component,"Prerequisite rejected: "..dependency)
        end
        if slot then weapon:SetWeaponComponent(slot,cid) end
      end)
      InventoryItem.AttachIdInitialization("JAZZ_CaptureStage")
      assert(applied,apply_error)
      row.components=table.copy(weapon.components or {})
      row.entity=weapon.Entity
      row.name=translate(weapon.DisplayName)
      row.plural=translate(weapon.DisplayNamePlural)
      row.valid_entity=IsValidEntity(weapon.Entity)
      assert(row.valid_entity,"Invalid entity "..tostring(weapon.Entity))
      if slot and (weapon.components[slot] or "")~=(cid or "") then
        row.status="rejected-component";return
      end
      vis=weapon:CreateVisualObj("JAZZ_CaptureStage")
      assert(IsValid(vis),"Invalid visual")
      weapon:UpdateVisualObj(vis)
      local position=point(150000,150000,150000)
      vis:SetPos(position);vis:SetAngle(0);vis:SetScale(100);vis:SetForcedLOD(0)
      vis:SetEnumFlags(const.efVisible);vis:SetGameFlags(const.gofAlwaysRenderable)
      row.parts={}
      for spot,part in sorted_pairs(vis.parts or {}) do
        if IsValid(part) then
          row.parts[#row.parts+1]={spot=spot,entity=part:GetEntity(),parent=part:GetParent():GetEntity()}
          part:SetForcedLOD(0)
        end
      end
      local bbox=vis:GetObjectBBox()
      local target=position+point(100,0,40)
      local distance=(id=="BrowningM2HMG" or id=="MortarInventoryItem") and 2500 or 1500
      if (settings.distance or 0)>0 then distance=settings.distance end
      row.camera_distance=distance
      SetCamera(target+point(0,distance,0),target,"Max",nil,nil,1200,0)
      SetLightmodel(1,studio,0)
      hr.AutoExposureMode=0
      WaitNextFrame(20)
      row.exposure=hr.AutoExposureMode
      row.light=CurrentLightmodel[1].id
      row.bounds=tostring(bbox)
      local screen=UIL.GetScreenSize()
      local width=screen:x();local height=MulDivRound(width,660,1296)
      if height>screen:y() then height=screen:y();width=MulDivRound(height,1296,660) end
      local x=(screen:x()-width)/2;local y=(screen:y()-height)/2
      local filename=id.."__"..label..".png"
      local err=WaitCaptureScreenshot(settings.output.."/raw/"..filename,
        {interface=false,alpha=true,width=1296,height=660,src=box(x,y,x+width,y+height),timeout=10000})
      assert(not err,tostring(err))
      if settings.matte then
        SetLightmodel(1,"WeaponModification",0)
        hr.AutoExposureMode=0
        backdrop=PlaceObject("WeaponModCMTPlane")
        backdrop:SetColorModifier(RGB(255,255,255))
        backdrop:SetSIModulation(0)
        backdrop:SetAxis(point(0,4096,4096));backdrop:SetAngle(10800)
        backdrop:SetPos(position+point(0,-2800,0));backdrop:SetScale(500)
        backdrop:SetGameFlags(const.gofAlwaysRenderable);backdrop:SetEnumFlags(const.efVisible)
        WaitNextFrame(20)
        local opts={interface=false,alpha=false,width=1296,height=660,src=box(x,y,x+width,y+height),timeout=10000}
        assert(not WaitCaptureScreenshot(settings.output.."/raw/"..id.."__"..label.."-white.png",opts))
        vis:SetVisible(false)
        WaitNextFrame(3)
        assert(not WaitCaptureScreenshot(settings.output.."/raw/"..id.."__"..label.."-background.png",opts))
        vis:SetVisible(true)
      end
      row.image="raw/"..filename;row.status="captured"
    end)
    if not ok then row.status="error";row.error=tostring(err) end
    dispose()
    report.rows[#report.rows+1]=row
    write("capture-report.json",report)
  end
  local ok,err=pcall(function()
    table.change(hr,"JAZZ_CaptureStage",render_flags)
    SetLightmodel(1,studio,0)
    for _,id in ipairs(settings.ids) do
      snapshot(id,"default")
      if settings.variants then
        local definition=g_Classes[id]
        for _,slot in ipairs(definition and definition.ComponentSlots or {}) do
          if settings.variants[slot.SlotType] or settings.variants.all then
            for _,cid in ipairs(slot.AvailableComponents or {}) do
              if cid~=slot.DefaultComponent then snapshot(id,slot.SlotType.."-"..cid,slot.SlotType,cid) end
            end
            if slot.CanBeEmpty and (slot.DefaultComponent or "")~="" then
              snapshot(id,slot.SlotType.."-empty",slot.SlotType,"")
            end
          end
        end
      end
      Sleep(1)
    end
  end)
  dispose()
  if light then SetLightmodel(1,light,0) end
  table.restore(hr,"JAZZ_CaptureStage")
  SetCamera(unpack_params(camera))
  report.phase=ok and "done" or "error"
  report.error=not ok and tostring(err) or nil
  report.restored_camera=ValueToLuaCode({GetCamera()})
  report.original_camera=ValueToLuaCode(camera)
  report.restored_light=CurrentLightmodel[1]==light
  report.restored_render={}
  for key in pairs(render_flags) do report.restored_render[key]=hr[key] end
  report.disposed=not vis and not backdrop and not weapon
  write("capture-report.json",report)
  return ok and "capture complete" or tostring(err)
end
