-- Disposable real-engine visual acceptance after installation; camera untouched.
return function(settings)
  local function check(v,m) if not v then error(m) end return v end
  check(Platform.debug and GetMapName()=="ModEditor","isolated editor runtime required")
  check(type(JazzWeaponIcon_BindItemImage)=="function","binder missing")
  local pause="InventoryPauseSP_mp_coop_host"
  local resumed=PauseReasons[pause]
  if resumed then Resume(pause) end
  local panel,items=nil,{}
  local report={level="runtime XImage rendering",weapons={}}
  local ok,err=pcall(function()
    check(not WaitCaptureScreenshot(settings.output.."/inventory.png",{interface=true,alpha=false,timeout=10000}),"inventory screenshot failed")
    panel=XWindow:new({HAlign="center",VAlign="center",MinWidth=1080,MaxWidth=1080,MinHeight=440,MaxHeight=440,Background=RGB(26,30,34),Padding=box(20,20,20,20),LayoutMethod="HList",LayoutHSpacing=12,HandleMouse=false,DrawOnTop=true},terminal.desktop)
    for _,build in ipairs(settings.builds) do
      InventoryItem.DetachIdInitialization("JAZZ_LayerUIProbe")
      local created,item=pcall(function()
        local item=g_Classes[build.weapon]:new({is_clone=true});items[#items+1]=item
        for _,slot in ipairs(build.order) do if build.requested[slot]~=nil then item:SetWeaponComponent(slot,build.requested[slot]) end end
        return item
      end)
      InventoryItem.AttachIdInitialization("JAZZ_LayerUIProbe")
      check(created,tostring(item))
      for slot,value in pairs(build.expected) do check(item.components[slot]==value,"effective component changed") end
      local column=XWindow:new({MinWidth=336,MaxWidth=336,LayoutMethod="VList",HandleMouse=false},panel)
      XText:new({Text=build.weapon,Translate=false,TextStyle="HUDHeader",HandleMouse=false},column)
      local img=XImage:new({Image=item.Icon,ImageFit="scale-down",MinWidth=324,MaxWidth=324,MinHeight=185,MaxHeight=185,HandleMouse=false},column)
      check(JazzWeaponIcon_BindItemImage(img,item),"installed binder failed: "..build.weapon)
      local group=img:ResolveId("idJazzNativeWeaponLayers")
      check(group and #group>0,"missing UI layers")
      local tile=XInventoryItem:new({HAlign="center",HandleMouse=false},column,item)
      tile:OnContextUpdate(item)
      check(tile.idItemImg:ResolveId("idJazzNativeWeaponLayers"),"inventory context hook failed")
      report.weapons[#report.weapons+1]={weapon=build.weapon,components=table.copy(item.components),draw_nodes=#group,inventory_tile=true}
    end
    panel:Open();WaitNextFrame(30)
    check(not WaitCaptureScreenshot(settings.output.."/combinations.png",{interface=true,alpha=false,timeout=10000}),"combination screenshot failed")
  end)
  if panel then panel:delete() end
  for _,item in ipairs(items) do item.visual_obj=false;item:delete() end
  if resumed then Pause(pause) end
  report.status=ok and "PASS" or "FAIL";report.error=not ok and tostring(err) or nil
  report.disposed=true;report.inventory_pause_restored=not resumed or not not PauseReasons[pause]
  local encode_err,text=LuaToJSON(report)
  check(not encode_err,tostring(encode_err));check(not AsyncStringToFile(settings.output.."/verification.json",text),"receipt write failed")
  return report.status
end
