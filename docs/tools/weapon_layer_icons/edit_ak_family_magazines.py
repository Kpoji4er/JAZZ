"""Official AK family magazine editor transaction with an immutable Lua baseline.

Run after capture cleanup; companion and unrelated serialization are reviewed
separately. No actor inventories are changed.
"""
import argparse, hashlib, json, shutil, subprocess
from pathlib import Path
from live import evaluate, quote

p=argparse.ArgumentParser(__doc__)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--backup',type=Path,required=True)
p.add_argument('--version',type=int,required=True)
a=p.parse_args()
assert not a.backup.exists()
a.backup.mkdir(parents=True)
hashes={}
for name in subprocess.check_output(['git','-C',str(a.repo),'ls-files','-z']).decode().split('\0'):
    if not name.endswith('.lua') or not (a.repo/name).is_file():continue
    target=a.backup/name;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(a.repo/name,target)
    hashes[name]=hashlib.sha256(target.read_bytes()).hexdigest()
(a.backup/'manifest.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
body="""CreateRealTimeThread(function()
 local ign=SafeEvalStart("AK family magazines")
 local ok,result=pcall(function()
  local function check(v,m) if not v then error(m or "magazine transaction precondition") end return v end
  check(Platform.debug and GetMapName()=="ModEditor")
  local mod=Mods.e6L4ECj
  check(mod.version==VERSION and mod:ItemsLoaded() and not mod:IsItemsFileModified())
  local weapon,components
  components={}
  mod:ForEachModItem(function(item)
   if IsKindOf(item,"ModItemInventoryItemCompositeDef") and item.id=="AK103" then weapon=item end
   if IsKindOf(item,"ModItemWeaponComponent") then components[item.id]=item end
  end)
  check(weapon)
  for _,slot in ipairs(weapon.ComponentSlots) do if slot.SlotType=="Magazine" then
   local options=table.icopy(slot.AvailableComponents)
   check(not table.find(options,"JAZZ_MagQuick_AK"),"quick already present")
   table.insert(options,2,"JAZZ_MagQuick_AK");slot:SetProperty("AvailableComponents",options)
  end end
  local edits={}
  for id,targets in pairs({JAZZ_MagQuick_AK={"AK103","Type56","ZastavaM92"},JAZZ_MagDrum_30_75={"Type56"}}) do
   local c=components[id];check(c)
   local donor
   for _,v in ipairs(c.Visuals) do if v.ApplyTo=="AKM" then donor=v end end
   check(donor)
   local visuals=table.icopy(c.Visuals)
   for _,target in ipairs(targets) do
    local found
    for _,v in ipairs(visuals) do if v.ApplyTo==target then v:SetProperty("Entity",donor.Entity);found=true end end
    if not found then visuals[#visuals+1]=PlaceObj("WeaponComponentVisual",{ApplyTo=target,Entity=donor.Entity,Slot=donor.Slot,Icon=donor.Icon,param_bindings=false}) end
    edits[#edits+1]={component=id,weapon=target,entity=donor.Entity}
   end
   c:SetProperty("Visuals",visuals);ObjModified(c)
  end
  ObjModified(weapon)
  mod.last_changes=(mod.last_changes or "").."\\n- Уточнены магазины семейства АК: быстрый магазин АКМ для АК-103, Type 56 и M92; барабан Type 56."
  mod:SaveWholeMod();check(mod.version==VERSION+1)
  return {status="PASS",version_before=VERSION,version_after=mod.version,edits=edits}
 end)
 SafeEvalEnd(ign,"AK family magazines")
 local _,text=LuaToJSON({ok=ok,result=result});AsyncStringToFile(RECEIPT,text)
end);return "editor save scheduled"
""".replace('VERSION',str(a.version)).replace('RECEIPT',quote((a.backup/'editor-result.json').resolve().as_posix()))
evaluate(body,a.backup/'dispatch.json')
