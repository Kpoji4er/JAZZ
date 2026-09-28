"""Refresh existing R4/VZ58 mesh and texture bytes without changing registrations.

--build DIR --export-root DIR --family vz58|r4 [--apply]
Requires compiled-audit pass. Maps exported PBR slots onto existing texture names;
backs up every changed file. Emits official ReloadEntityResource Lua for live
editor refresh; never runs it automatically or alters save state / ModItems.
"""
import argparse,json,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
from _integrate_vz58 import ROOT,ASSETS
p=argparse.ArgumentParser()
p.add_argument('--build',type=Path,required=True);p.add_argument('--export-root',type=Path,required=True)
p.add_argument('--family',choices=['vz58','r4'],required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
assert json.loads((a.build/'compiled-audit.json').read_text())['pass']
prefix='JAZZ_VZ58' if a.family=='vz58' else 'JAZZ_VektorR4'
entities=sorted((ASSETS/'Entities').glob(prefix+'*.ent'));assert len(entities)==(14 if a.family=='vz58' else 1)
updates={};tex_sources={};resource_paths=[]
for path in entities:
 old=ET.parse(path);new=ET.parse(a.export_root/path.name)
 for tag in ['mesh','material']:
  before=old.findall('.//'+tag);after=new.findall('.//'+tag)
  assert [x.get('file') for x in before]==[x.get('file') for x in after]
 for mesh in new.findall('.//mesh'):
  rel=Path(mesh.get('file'));updates[ASSETS/'Entities'/rel]=(a.export_root/rel).read_bytes()
 for material in old.findall('.//material'):
  rel=Path(material.get('file'));old_m=ET.parse(ASSETS/'Entities'/rel);new_m=ET.parse(a.export_root/rel)
  old_maps={t.tag:t.get('Name') for t in old_m.getroot().iter() if t.get('Name')}
  new_maps={t.tag:t.get('Name') for t in new_m.getroot().iter() if t.get('Name')}
  assert old_maps.keys()==new_maps.keys()
  for slot,name in old_maps.items():
   source=a.export_root/'Textures'/new_maps[slot]
   assert name.startswith(prefix+'_')
   if name in tex_sources:assert source.read_bytes()==tex_sources[name].read_bytes(),name
   tex_sources[name]=source
stage=a.build/'surface-stage';stage.mkdir(exist_ok=True)
# Locate installed converter via explicit export pipeline config, not a tracked path.
import os
game=Path(os.environ['JA3_ASSET_GAME_ROOT']);cvt=game/'ModTools/hgimgcvt.exe'
for name,source in tex_sources.items():
 for sub,size in [('Textures',2048),('Textures/Fallbacks',64)]:
  target=stage/sub/name;target.parent.mkdir(parents=True,exist_ok=True)
  subprocess.run([str(cvt),str(source),str(target),'--truncate',str(size)],check=True,capture_output=True)
  updates[ASSETS/'Entities'/sub/name]=target.read_bytes()
icon='VZ58' if a.family=='vz58' else 'VektorR4'
updates[ROOT/'WeaponIcons'/(icon+'.png')]=(a.build/(icon+'_icon.png')).read_bytes()
changed={path:data for path,data in updates.items() if path.read_bytes()!=data}
for path,data in changed.items():
 if path.is_relative_to(ASSETS/'Entities'):resource_paths.append(path.relative_to(ASSETS/'Entities').as_posix())
 if a.apply:
  backup=a.build/'surface-backup'/path.relative_to(ROOT.parent);backup.parent.mkdir(parents=True,exist_ok=True)
  assert not backup.exists(),'Refuse to overwrite first backup'
  backup.write_bytes(path.read_bytes());path.write_bytes(data)
lua='''local mod=assert(Mods.pDGDhr)
CreateRealTimeThread(function()
 local paths=PATHS
 for _,rel in ipairs(paths) do ReloadEntityResource(mod.content_path.."Entities/"..rel,"modified") end
 ReloadTextureHeaders()
 AsyncStringToFile("AppData/jazz_surface_refresh_FAMILY.txt","refreshed "..#paths.." resources")
end)
return "scheduled FAMILY resource refresh"
'''.replace('PATHS','{'+','.join(json.dumps(x) for x in resource_paths)+'}').replace('FAMILY',a.family)
(a.build/'reload-surfaces.lua').write_text(lua,encoding='utf-8')
(a.build/'surface-refresh.json').write_text(json.dumps({'applied':a.apply,'files':[str(x.relative_to(ROOT.parent)) for x in changed],'resource_count':len(resource_paths)},indent=2))
print('APPLIED' if a.apply else 'STAGED',len(changed),'files; existing registrations/material paths preserved')
