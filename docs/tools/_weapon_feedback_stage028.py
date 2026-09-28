"""Stage second visual acceptance transaction. --build DIR [--apply].

Bounded data edits, compiled meshes, inspected icons. Original hashes/backups
protect unrelated working changes. Apply requires closed game/editor.
"""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
from lupa import LuaRuntime
from _integrate_m14_family import matching,find_item_block
from _integrate_sr3m import add_metadata,append_root_item
ROOT=Path(__file__).resolve().parents[2];SUITE=ROOT.parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
def main():
 p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args();b=a.build;stage=b/'stage'
 if a.apply:
  proc=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
  assert not proc.stdout.strip(),'Game/editor must be closed'
  manifest=json.loads((b/'manifest.json').read_text());backup=b/'backup';assert not backup.exists()
  for rel,h in manifest.items():assert sha(SUITE/rel)==h['before'] and sha(stage/rel)==h['after'],rel
  for rel,h in manifest.items():
   if h['before'] is not None:
    dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SUITE/rel,dest)
  try:
   for rel in manifest:
    (SUITE/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(stage/rel,SUITE/rel)
   for rel,h in manifest.items():assert sha(SUITE/rel)==h['after'] and sha(backup/rel)==h['before'],rel
  except Exception:
   for rel,h in manifest.items():
    if h['before'] is not None:shutil.copy2(backup/rel,SUITE/rel)
    elif sha(SUITE/rel)==h['after']:(SUITE/rel).unlink()
   raise
  (b/'installed.json').write_text(json.dumps({'files':len(manifest),'hashes_verified':True,'runtime_verified':False},indent=2));print('INSTALLED',len(manifest));return
 outputs={}
 def read(rel):return (SUITE/rel).read_bytes().decode('utf-8-sig').replace('\r\n','\n')
 def put(rel,s):
  old=(SUITE/rel).read_bytes() if (SUITE/rel).exists() else b''
  if isinstance(s,str):s=(b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in old else '\n').encode('utf-8')
  outputs[rel]=s
 s=read('jazz/items.lua')
 # Put both root-level weapons next to AK47 in the existing rifle folder.
 moved=[]
 for name in ('VZ58','VektorR4'):
  start,end=find_item_block(s,name);moved.append(s[start:end]);assert s[end]==',';s=s[:start]+s[end+1:]
 start,_=find_item_block(s,'AK47');indent=s[s.rfind('\n',0,start)+1:start]
 normalized=[]
 for block in moved:
  lines=block.splitlines();base=re.match(r'\s*',lines[-1])[0]
  normalized.append(lines[0]+'\n'+'\n'.join(indent+'\t'+(line[len(base):] if line.startswith(base) else line) for line in lines[1:-1])+'\n'+indent+lines[-1].lstrip())
 s=s[:start]+(',\n'+indent).join(normalized)+',\n'+indent+s[start:]
 # Remove the EBR M203 choice in both editor and generated runtime definition.
 start,end=find_item_block(s,'MK14EBR');block=s[start:end];assert block.count('"JAZZ_GrenadeLauncher_M14",')==1
 s=s[:start]+block.replace('"JAZZ_GrenadeLauncher_M14",','')+s[end:]
 companion=read('jazz/InventoryItem/MK14EBR.lua');assert companion.count('"JAZZ_GrenadeLauncher_M14",')==1
 put('jazz/InventoryItem/MK14EBR.lua',companion.replace('"JAZZ_GrenadeLauncher_M14",',''))
 scopes={}
 from _audit_ar15_slots import parse_slots
 for weapon in ('M14SAW','M21'):
  scopes[weapon]=parse_slots(read('jazz/InventoryItem/'+weapon+'.lua'))['Scope']['components']
 for m in reversed(list(re.finditer(r"PlaceObj\('ModItemWeaponComponent'",s))):
  end=matching(s,s.index('(',m.start()));block=s[m.start():end];ids=re.findall(r'\bid = "([^"]+)"',block);assert len(ids)==1
  for v in reversed(list(re.finditer(r"PlaceObj\('WeaponComponentVisual'",block))):
   ve=matching(block,block.index('(',v.start()));visual=block[v.start():ve]
   if 'ApplyTo = "MK14EBR"' in visual:
    visual=visual.replace('Entity = "WeaponAttA_SideMountM14"','Entity = ""').replace('Slot = "Side1"','Slot = "Side"')
   block=block[:v.start()]+visual+block[ve:]
  for weapon,options in scopes.items():
   if ids[0] in options:
    extra=f'\nPlaceObj(\'WeaponComponentVisual\', {{ ApplyTo = "{weapon}", Entity = "JAZZ_M14_OpticsMount", Slot = "OpticsMount", param_bindings = false }}),'
    block,n=re.subn(r'Visuals\s*=\s*\{',lambda m:m[0]+extra,block,count=1);assert n==1
  s=s[:m.start()]+block+s[end:]
 put('jazz/items.lua',s)
 # Fix vanilla's nil-versus-empty test without bypassing occupied slot checks.
 rel='jazz/Code/System_WeaponRemovableModify.lua';code=read(rel)
 anchor='local VanillaCanModifySlot = ModifyWeaponDlg.CanModifySlot'
 helper='''-- Missing slots are empty: Side2 must not block short-barrel previews on AR15s.
function GetComponentBlocksAnyOfAttachedSlots(weapon, partDef)
\tfor _, slot in ipairs(partDef and partDef.BlockSlots or empty_table) do
\t\tlocal attached = weapon.components[slot] or ""
\t\tlocal slotDef = table.find_value(weapon.ComponentSlots, "SlotType", slot)
\t\tlocal default = slotDef and slotDef.DefaultComponent or ""
\t\tif attached ~= "" and attached ~= default then
\t\t\treturn true, attached
\t\tend
\tend
end

'''
 assert code.count(anchor)==1;put(rel,code.replace(anchor,helper+anchor,1))
 # Existing setter/migration own removal of the obsolete EBR launcher.
 rel='jazz/Code/System_WeaponComponent_Set.lua';code=read(rel)
 anchor='\tif not slot then'
 guard='''\tif self.class == "MK14EBR" and slot == "Under" and id == "JAZZ_GrenadeLauncher_M14" then
\t\tid = ""
\t\tdef = nil
\tend

'''
 assert code.count(anchor)==1;code=code.replace(anchor,guard+anchor,1)
 anchor='\t\t\tJazzReseatObsoleteMagazineOnFirearm(item)'
 migrate='''\t\t\tif item.class == "MK14EBR" and item.components and item.components.Under == "JAZZ_GrenadeLauncher_M14" then
\t\t\t\titem:SetWeaponComponent("Under", "", "init")
\t\t\tend
'''
 assert code.count(anchor)==1;put(rel,code.replace(anchor,migrate+anchor,1))
 # Bind attachment spots to actual surfaces measured in the prepared meshes.
 for name,positions in {'JAZZ_M14':{'Under':'56.000,-0.425,7.295'},'MK14EBR':{'Side':'44.000,-2.780,8.750','Under':'40.000,0.000,5.774','Bipod':'49.000,0.000,5.774'}}.items():
  rel='jazz_assets/Entities/'+name+'.ent';s=read(rel)
  for spot,pos in positions.items():
   s,n=re.subn(r'(<attach name="'+spot+r'" spot_pos=")[^"]+',lambda m:m[1]+pos,s);assert n==1
  if name=='MK14EBR':s,n=re.subn(r'(<attach name="Side"[^>]*spot_rot=")[^"]+',lambda m:m[1]+'1.000000,0.000000,0.000000,90.0000',s);assert n==1
  else:s=s.replace('</mesh_description>','<attach name="OpticsMount" spot_pos="0.000,0.000,0.000" spot_rot="0.000000,0.000000,1.000000,0.0000" />\n\t</mesh_description>')
  put(rel,s)
 name='JAZZ_M14_OpticsMount';rel='jazz_assets/Entities/'+name
 import xml.etree.ElementTree as ET
 tree=ET.parse(b/'ExportedEntities'/(name+'.ent'));entity=tree.getroot();entity.set('path','');entity.set('name',name)
 for node in list(entity):
  if node.tag=='src':entity.remove(node)
 for parent in entity.iter():
  for child in list(parent):
   if child.tag in ('src','attach'):parent.remove(child)
 for node in entity.findall('.//material'):node.set('file','Materials/JAZZ_M14_Mesh.mtl')
 put(rel+'.ent',ET.tostring(entity,encoding='utf-8',xml_declaration=True));put(rel+'.lua','EntityData["'+name+'"] = { editor_artset = "Mods" }\n')
 s=read('jazz_assets/items.lua');assert name not in s;s=append_root_item(s,f'PlaceObj(\'ModItemEntity\', {{\n\t\'name\', "{name}",\n\t\'ClassParents\', {{}},\n\t\'entity_name\', "{name}",\n}}),');put('jazz_assets/items.lua',s)
 s=read('jazz_assets/metadata.lua');s=add_metadata(s,'entities',['"'+name+'"']);s=add_metadata(s,'code',['"Entities/'+name+'.lua"']);put('jazz_assets/metadata.lua',s)
 reports=json.loads((b/'compiled-report.json').read_text());assert len(reports)==4 and all(r['pass'] for r in reports)
 for r in reports:
  name=r['entity'];put('jazz_assets/Entities/Meshes/'+name+'_Mesh.m.hgm',(b/'ExportedEntities/Meshes'/(name+'_Mesh.m.hgm')).read_bytes())
 for name in ('AK103','M14','M21','VZ58','JAZZ_M14_MkIII'):
  icon=b/'icons'/(name+'.png')
  if icon.exists():put('jazz/WeaponIcons/'+icon.name,icon.read_bytes())
 manifest={}
 for rel,data in outputs.items():
  if rel.endswith('.lua'):LuaRuntime().compile(data.decode('utf-8-sig'))
  target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  manifest[rel]={'before':sha(SUITE/rel),'after':sha(target)}
 (b/'manifest.json').write_text(json.dumps(manifest,indent=2));print('STAGED',len(manifest))
if __name__=='__main__':main()
