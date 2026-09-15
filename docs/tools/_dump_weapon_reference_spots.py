"""Read vanilla AK attachment positions using disposable engine objects.

Uses the existing live DAP session without initialize/pause; writes a TSV in
AppData. Does not edit inventories, savegames or mod data.
"""
from _probe_weapon_imports_runtime import evaluate
expression='''(function()
 CreateGameTimeThread(function()
  local ign=SafeEvalStart("vanilla-weapon-spots")
  local objects,rows={},{}
  local ok,err=pcall(function()
   for _,entity in ipairs({"Weapon_AK74","Weapon_AK47","Weapon_AKS74U"}) do
    local obj=PlaceObject("Object")
    objects[#objects+1]=obj
    obj:ChangeEntity(entity)
    obj:SetPos(point(0,0,0))
    local first,last=obj:GetAllSpots(obj:GetState())
    for i=first,last do
     local p=obj:GetSpotPos(i)
     if p then rows[#rows+1]=string.format("%s\\t%s\\t%d\\t%d\\t%d",entity,obj:GetSpotName(i),p:x(),p:y(),p:z()) end
    end
   end
  end)
  for _,obj in ipairs(objects) do DoneObject(obj) end
  SafeEvalEnd(ign,"vanilla-weapon-spots")
  AsyncStringToFile("AppData/jazz_vanilla_weapon_spots.tsv",ok and table.concat(rows,"\\n") or tostring(err))
 end)
 return "Scheduled vanilla attachment position export"
end)()'''
print(evaluate(expression))
