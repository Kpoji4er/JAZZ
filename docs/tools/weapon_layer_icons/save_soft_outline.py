"""Official final soft-outline code/editor save with an immutable Lua baseline.

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
 local ign=SafeEvalStart("weapon soft outline final save")
 local ok,result=pcall(function()
  local m=Mods.e6L4ECj
  if not (Platform.debug and GetMapName()=="ModEditor" and m.version==VERSION and m:ItemsLoaded() and not m:IsItemsFileModified()) then error("editor precondition") end
  m:UnloadItems();m:LoadItems()
  if m:IsItemsFileModified() then error("editor reload failed") end
  local note="\\n- Мягкий внешний контур иконок без дополнительной резкости; исправлена посадка магазинов АК-103 и Type 56."
  if not (m.last_changes or ""):find(note,1,true) then m.last_changes=(m.last_changes or "")..note end
  m:SaveWholeMod()
  if m.version~=VERSION+1 then error("revision did not advance") end
  return {status="PASS",version_before=VERSION,version_after=m.version}
 end)
 SafeEvalEnd(ign,"weapon soft outline final save")
 local _,text=LuaToJSON({ok=ok,result=result});AsyncStringToFile(RECEIPT,text)
end);return "editor save scheduled"
""".replace('VERSION',str(a.version)).replace('RECEIPT',quote((a.backup/'editor-result.json').resolve().as_posix()))
evaluate(body,a.backup/'dispatch.json')
