"""Live roundtrip: donor entities and absolute magazine offsets survive repeated updates."""
import argparse
from pathlib import Path
from live import evaluate, quote

p = argparse.ArgumentParser(__doc__)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
body = '''local function check(v,m) if not v then error(m) end end
check(Platform.debug and GetMapName()=="ModEditor","isolated editor required")
local report={rows={}};local item,vis
local ok,err=pcall(function()
 for _,weapon in ipairs({"AKM","AK103","AK47","Type56","Zastava_M70","ZastavaM92"}) do
  InventoryItem.DetachIdInitialization("JAZZ_MagazineCycle")
  local created,result=pcall(function() return g_Classes[weapon]:new({is_clone=true}) end)
  InventoryItem.AttachIdInitialization("JAZZ_MagazineCycle")
  check(created,tostring(result));item=result
  vis=item:CreateVisualObj("JAZZ_MagazineCycle")
  item:UpdateVisualObj(vis)
  local normal=vis.parts.Magazine:GetEntity()
  for cycle=1,3 do
   for _,component in ipairs({"JAZZ_MagNormal","JAZZ_MagQuick_AK","JAZZ_MagLarge_30_40","JAZZ_MagDrum_30_75","JAZZ_MagNormal"}) do
    item:SetWeaponComponent("Magazine",component);item:UpdateVisualObj(vis)
    check(item.components.Magazine==component,"component rejected")
    local part=vis.parts.Magazine
    local expected=component=="JAZZ_MagNormal" and normal or component=="JAZZ_MagQuick_AK" and "WeaponAttA_MagazineAK47_03" or component=="JAZZ_MagLarge_30_40" and "WeaponAttA_MagazineAK47_02" or "WeaponAttA_MagazineRPK74_03"
    check(part:GetEntity()==expected,weapon..": donor mismatch")
    local z=0
    if component~="JAZZ_MagNormal" then
     if weapon=="Type56" then z=23 end
    end
    local offset=point(0,0,z)
    if weapon=="AK103" then
     if component=="JAZZ_MagNormal" then offset=point(6,-9,-9)
     elseif component=="JAZZ_MagDrum_30_75" then offset=point(-9,-10,-8)
     else offset=point(3,-10,-2) end
    end
    check(part:GetAttachOffset()==offset,weapon..": wrong initial offset "..tostring(part:GetAttachOffset()))
    local position=part:GetVisualPos()
    for update=1,3 do
     item:UpdateVisualObj(vis);part=vis.parts.Magazine
     check(part:GetAttachOffset()==offset and part:GetVisualPos()==position,weapon..": offset drift")
    end
    report.rows[#report.rows+1]={weapon=weapon,component=component,cycle=cycle,entity=expected,offset=tostring(offset)}
   end
  end
  DoneObject(vis);vis=nil;item.visual_obj=false;item:delete();item=nil
 end
end)
if IsValid(vis) then DoneObject(vis) end
if item then item.visual_obj=false;item:delete() end
report.status=ok and "PASS" or "FAIL";report.error=not ok and tostring(err) or nil;report.disposed=true
local _,text=LuaToJSON(report);AsyncStringToFile(OUTPUT,text)
return report.status
'''.replace('OUTPUT', quote(a.output.resolve().as_posix()))
evaluate(body, a.output.with_suffix('.dispatch.json'), True)
