"""Official AK-103 magazine editor transaction with an immutable Lua baseline.

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
body='''CreateRealTimeThread(function()
 local ign=SafeEvalStart("AK103 magazine editor transaction")
 local ok,result=pcall(function()
  local function assert(v,m) if not v then error(m or "AK103 transaction precondition") end return v end
  assert(Platform.debug and GetMapName()=="ModEditor")
  local mod=Mods.e6L4ECj
  assert(mod.version==VERSION and mod:ItemsLoaded() and not mod:IsItemsFileModified())
  local weapon,drum
  mod:ForEachModItem(function(item)
   if IsKindOf(item,"ModItemInventoryItemCompositeDef") and item.id=="AK103" then weapon=item end
   if IsKindOf(item,"ModItemWeaponComponent") and item.id=="JAZZ_MagDrum_30_75" then drum=item end
  end)
  assert(weapon and drum)
  local removed=0
  for _,slot in ipairs(weapon.ComponentSlots) do
   if slot.SlotType=="Magazine" then
    local options={}
    for _,id in ipairs(slot.AvailableComponents) do
     if id=="JAZZ_MagQuick_AK" then removed=removed+1 else options[#options+1]=id end
    end
    slot:SetProperty("AvailableComponents",options)
   end
  end
  assert(removed==1)
  local donor
  for _,visual in ipairs(drum.Visuals) do
   assert(visual.ApplyTo~="AK103","AK103 drum visual already exists")
   if visual.ApplyTo=="AKM" then donor=visual end
  end
  assert(donor and donor.Entity=="WeaponAttA_MagazineRPK74_03")
  local visuals=table.icopy(drum.Visuals)
  visuals[#visuals+1]=PlaceObj("WeaponComponentVisual",{ApplyTo="AK103",Entity=donor.Entity,Slot=donor.Slot,Icon=donor.Icon,param_bindings=false})
  drum:SetProperty("Visuals",visuals)
  ObjModified(weapon);ObjModified(drum)
  mod.last_changes=(mod.last_changes or "").."\\n- Исправлены магазины АК-103 и внешний контур составных иконок; быстросъёмный магазин АК-103 убран."
  mod:SaveWholeMod()
  assert(mod.version==VERSION+1)
  return {status="PASS",version_before=VERSION,version_after=mod.version,quick_removed=removed,drum_entity=donor.Entity}
 end)
 SafeEvalEnd(ign,"AK103 magazine editor transaction")
 local _,text=LuaToJSON({ok=ok,result=result})
 AsyncStringToFile(RECEIPT,text)
end);return "editor save scheduled"
'''.replace('VERSION',str(a.version)).replace('RECEIPT',quote((a.backup/'editor-result.json').resolve().as_posix()))
evaluate(body,a.backup/'dispatch.json')
