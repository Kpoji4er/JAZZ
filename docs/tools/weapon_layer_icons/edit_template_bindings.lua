-- Official editor transaction; dispatch only after every camera batch finishes.
return function(settings)
  local function check(value,message) if not value then error(message) end return value end
  local mod=check(Mods.e6L4ECj,"core mod missing")
  check(Platform.debug and GetMapName()=="ModEditor","isolated editor runtime required")
  check(mod.version==settings.version,"metadata revision changed")
  check(mod:ItemsLoaded() and not mod:IsItemsFileModified(),"reload current ModItems before editing")
  local template
  mod:ForEachModItem(function(item)
    if IsKindOf(item,"ModItemXTemplate") and item.id=="UIWeaponDisplay" then template=item end
  end)
  check(template,"weapon template missing")
  check(not template:GetCodeFileName(),"unexpected template companion")
  local edits={}
  local function visit(node)
    if node.comment=="weapon" and type(node.run_after)=="function" then
      local name,params,body=GetFuncSource(node.run_after)
      check(body,"missing callback source")
      if type(body)=="table" then body=table.concat(body,"\n") end
      check(not body:find("JazzWeaponIcon_BindItemImage",1,true),"binding already installed")
      local anchor="itemIcon:SetImage(item.Icon)"
      local first,last=body:find(anchor,1,true)
      check(first and not body:find(anchor,last+1,true),"ambiguous icon assignment")
      local indent=body:match("([ \t]*)itemIcon:SetImage") or ""
      local replacement=anchor.."\n"..indent.."if JazzWeaponIcon_BindItemImage then\n"..indent.."\tJazzWeaponIcon_BindItemImage(itemIcon, item)\n"..indent.."end"
      local fn,err=CompileFunc(name,params,body:sub(1,first-1)..replacement..body:sub(last+1),"JAZZ native weapon icon binding")
      check(not err,tostring(err));edits[#edits+1]={node=node,fn=fn}
    end
    for _,child in ipairs(node) do if type(child)=="table" then visit(child) end end
  end
  visit(template);check(#edits==2,"expected two weapon callbacks")
  for _,edit in ipairs(edits) do edit.node:SetProperty("run_after",edit.fn);ObjModified(edit.node) end
  mod.last_changes=(mod.last_changes or "").."\n"..settings.bullet
  local before=mod.version
  mod:SaveWholeMod()
  check(mod.version==before+1,"unexpected editor revision")
  check(not mod:IsItemsFileModified(),"saved source timestamp mismatch")
  mod:UnloadItems();mod:LoadItems()
  local callbacks=0
  local function verify(node)
    if node.comment=="weapon" and type(node.run_after)=="function" then
      local source=GetFuncSourceString(node.run_after)
      if source:find("JazzWeaponIcon_BindItemImage",1,true) then callbacks=callbacks+1 end
    end
    for _,child in ipairs(node) do if type(child)=="table" then verify(child) end end
  end
  mod:ForEachModItem(function(item) if IsKindOf(item,"ModItemXTemplate") and item.id=="UIWeaponDisplay" then verify(item) end end)
  check(callbacks==2,"saved template did not survive reload")
  return {status="PASS",version_before=before,version_after=mod.version,callbacks=callbacks,companion=false,roundtrip="official SaveWholeMod and UnloadItems/LoadItems"}
end
