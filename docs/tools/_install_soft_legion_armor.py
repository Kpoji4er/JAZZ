"""Install three staged armor graphs and isolated test units, with backups."""
import argparse,re,subprocess,hashlib,json
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image
from lupa import LuaRuntime
from _integrate_sr3m import add_metadata,append_root_item
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT.parent/'jazz_assets';UNITS=ROOT.parent/'jazz-units'
ROWS=[('chainmail','Chainmail'),('brigantine','TireBrigantine'),('tire','TireArmor')]
def validate(build,entity,item):
 stage=build/'mod-assets-stage/Entities';tree=ET.parse(stage/(entity+'.ent'))
 assert any('Male' in str(e.attrib) for e in tree.getroot().iter()),'Missing Male inheritance'
 for tag in tree.findall('.//mesh')+tree.findall('.//material'):
  path=stage/tag.attrib['file'];assert path.is_file(),path
  if tag.tag=='material':
   for node in ET.parse(path).getroot().iter():
    name=node.get('Name')
    if name:
     for folder in ['Textures','Textures/Fallbacks']:
      f=stage/folder/name;assert f.read_bytes()[:4]==b'DDS ',f
 im=Image.open(build/(item+'.png'));assert im.size==(110,110) and im.mode=='RGBA';assert im.getchannel('A').getextrema()==(0,255)
 return stage
def main():
 p=argparse.ArgumentParser();p.add_argument('--build-root',type=Path,required=True);p.add_argument('--apply',action='store_true');p.add_argument('--heavy-torso',action='store_true');a=p.parse_args()
 global ROWS
 if a.heavy_torso:ROWS=[(f+v,f+v) for f in ['Twaron','Guardian','Zylon'] for v in ['Light','Medium','Full']]
 check=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
 if a.apply:assert not check.stdout.strip(),'Game/editor is open; cannot install over its loaded data'
 paths=[ASSETS/'items.lua',ASSETS/'metadata.lua',UNITS/'items.lua',UNITS/'metadata.lua']
 if a.heavy_torso:paths.append(ROOT/'Code/System_LegionArmorVisuals.lua')
 before={p:p.read_bytes() for p in paths};texts={p:v.decode('utf-8-sig') for p,v in before.items()};writes={}
 if a.heavy_torso:
  runtime=ROOT/'Code/System_LegionArmorVisuals.lua'
  marker='local armor_entities = {'
  assert marker in texts[runtime]
  additions=''.join('\n\tJazzArmor_'+item+' = { Male = "JAZZ_'+item+'_Male" },' for _,item in ROWS)
  texts[runtime]=texts[runtime].replace(marker,marker+additions,1)
 template=(UNITS/'UnitData/JAZZ_Legion_ArmorTest.lua').read_text(encoding='utf-8-sig');lua=LuaRuntime()
 for kind,item in ROWS:
  entity='JAZZ_'+item+'_Male';uid='JAZZ_Legion_ArmorTest_'+item;armor='JazzArmor_'+item
  build=a.build_root/kind/'build';stage=validate(build,entity,item)
  if a.heavy_torso:
   fit=json.loads((a.build_root/kind/'source/fit.json').read_text())
   assert fit['rear_inner_gap_after_m']['min']>-.003 and fit['rear_inner_gap_after_m']['p95']<.035,'Rear fit gate failed'
  assert entity not in texts[ASSETS/'items.lua'] and uid not in texts[UNITS/'items.lua'],'Already registered'
  companion=template.replace('JAZZ_Legion_ArmorTest',uid).replace('JazzArmor_ImprovisedCuirass',armor).replace('cuirass + MP40',item+' + MP40')
  props=companion[companion.index('    comment ='):companion.rfind('}')]
  props=re.sub(r'^    (\w+) = ',r"    '\1', ",props,flags=re.M)
  record="PlaceObj('ModItemUnitDataCompositeDef', {\n    'Group', \"JAZZ Tests\",\n    'Id', \""+uid+'",\n'+props+'}),'
  text=texts[UNITS/'items.lua'];pos=text.rfind('}');texts[UNITS/'items.lua']=text[:pos]+record+'\n'+text[pos:]
  texts[UNITS/'metadata.lua']=add_metadata(texts[UNITS/'metadata.lua'],'code',['"UnitData/'+uid+'.lua"'])
  texts[UNITS/'metadata.lua']=add_metadata(texts[UNITS/'metadata.lua'],'affected_resources',["PlaceObj('ModResourcePreset', { 'Class', \"UnitDataCompositeDef\", 'Id', \""+uid+"\", 'ClassDisplayName', \"Unit\" })"])
  entityitem="PlaceObj('ModItemEntity', {\n    'name', \""+entity+"\",\n    'ClassParents', { \"CharacterArmorMale\" },\n    'entity_name', \""+entity+'",\n}),'
  texts[ASSETS/'items.lua']=append_root_item(texts[ASSETS/'items.lua'],entityitem)
  texts[ASSETS/'metadata.lua']=add_metadata(texts[ASSETS/'metadata.lua'],'code',['"Entities/'+entity+'.lua"'])
  texts[ASSETS/'metadata.lua']=add_metadata(texts[ASSETS/'metadata.lua'],'entities',['"'+entity+'"'])
  writes[UNITS/'UnitData'/(uid+'.lua')]=companion.encode()
  for f in stage.rglob('*'):
   if f.is_file():writes[ASSETS/'Entities'/f.relative_to(stage)]=f.read_bytes()
  writes[ASSETS/'Entities'/(entity+'.lua')]=('EntityData["'+entity+'"] = { editor_artset = "Mods", entity = { class_parent = "CharacterArmorMale" } }\n').encode()
  if not a.heavy_torso:writes[ROOT/'ArmorIcons'/(item+'.png')]=(build/(item+'.png')).read_bytes()
 for path,text in texts.items():writes[path]=text.encode('utf-8')
 for path,data in writes.items():
  if path.suffix=='.lua':lua.compile(data.decode('utf-8-sig'))
 for path,data in before.items():assert path.read_bytes()==data,'Concurrent edit '+str(path)
 if not a.apply:
  prepared=a.build_root/'prepared-install'
  for path,data in writes.items():
   target=prepared/path.relative_to(ROOT.parent);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
  (a.build_root/'planned-install.json').write_text(json.dumps({'installed':False,'files':[str(p.relative_to(ROOT.parent)) for p in writes]},indent=2))
  print('PASS staging resources and Lua compilation; complete transaction prepared in',prepared);return
 backup=a.build_root/'installation-backup';assert not backup.exists(),'Backup already exists'
 snapshot={path:path.read_bytes() if path.exists() else None for path in writes}
 for path,data in snapshot.items():
  if data is not None:
   dest=backup/path.relative_to(ROOT.parent);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 try:
  for path,data in writes.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
  for path,data in writes.items():assert path.read_bytes()==data
 except Exception:
  for path,data in snapshot.items():
   if data is None:path.unlink(missing_ok=True)
   else:path.write_bytes(data)
  raise
 manifest={'installed':True,'runtime':'NOT_RUN','units':['JAZZ_Legion_ArmorTest_'+item for _,item in ROWS],
           'sha256':{str(path.relative_to(ROOT.parent)):hashlib.sha256(data).hexdigest() for path,data in writes.items()}}
 (a.build_root/'installation.json').write_text(json.dumps(manifest,indent=2));print('INSTALLED',len(writes),'files; entity resources and test units')
if __name__=='__main__':main()
