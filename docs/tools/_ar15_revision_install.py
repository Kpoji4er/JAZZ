"""Install audited M4 sight/barrel correction: --build DIR --export-root DIR [--apply].
Registers one FrontSight entity, reuses installed barrel textures, preserves other data.
"""
import argparse,json,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
from lupa import LuaRuntime
from _integrate_sr3m import add_metadata,matching
from _integrate_ar15_family import wire_visuals
from _wire_ar15_visible_modules import register_entities
from _apply_weapon_geometry_update import clean_ent
p=argparse.ArgumentParser()
p.add_argument('--weapon',choices=('M4A1','M16A4'),default='M4A1')
for k in ('build','export-root'):p.add_argument('--'+k,type=Path,required=True)
p.add_argument('--apply',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[2];assets=root.parent/'jazz_assets'
prefix='M4R_M4A1' if a.weapon=='M4A1' else 'M16R_M16A4'
suffixes=('','_Barrel','_BarrelShort','_BarrelLong','_RearSight','_FrontSight') if a.weapon=='M4A1' else ('','_Barrel','_BarrelShort','_FrontSight')
names=[prefix+suffix for suffix in suffixes]
new=names[-1];outputs={}
for name in names:
 assert json.loads((a.build/(name+'-audit.json')).read_text())['pass'],name
 tree=clean_ent(a.export_root/(name+'.ent'),name)
 outputs[assets/'Entities'/(name+'.ent')]=ET.tostring(tree.getroot(),encoding='utf-8',xml_declaration=True)
 mesh=tree.getroot().find('.//mesh').get('file')
 outputs[assets/'Entities'/mesh]=(a.export_root/mesh).read_bytes()
 if name==new:
  material=tree.getroot().find('.//material').get('file')
  outputs[assets/'Entities'/material]=(assets/'Entities/Materials'/(prefix+'_Barrel_Mesh.mtl')).read_bytes()
 outputs.setdefault(assets/'Entities'/(new+'.lua'),f'EntityData["{new}"] = {{ editor_artset = "Mods" }}\n'.encode())
items=(root/'items.lua').read_text(encoding='utf-8')
# The long barrel must not own the Handguard visual.
removed=0
for m in reversed(list(re.finditer(r"PlaceObj\('WeaponComponentVisual'",items))):
 end=matching(items,items.index('(',m.start()));block=items[m.start():end]
 if a.weapon=='M4A1' and 'Entity = "M4R_M4A1_HandguardRifle"' in block and 'ApplyTo = "M4A1"' in block:
  assert items[end]==',';items=items[:m.start()]+items[end+1:];removed+=1
assert removed==(1 if a.weapon=='M4A1' else 0),removed
iron='JAZZ_IronSight' if a.weapon=='M4A1' else 'JAZZ_DefaultIronsight_AR15'
items,log=wire_visuals(items,a.weapon,{
 'JAZZ_CarryHandle_AR15':('Gassblock','FrontSight'),
 iron:('Gassblock','FrontSight'),
})
if a.weapon=='M16A4':
 assert items.count('Entity = "M16R_M16A4_RearSight"')==1
 items=items.replace('Entity = "M16R_M16A4_RearSight"','Entity = "M4R_M4A1_RearSight"')
outputs[root/'items.lua']=items.encode()
asset_items=register_entities((assets/'items.lua').read_text(encoding='utf-8'),[new])
one_line=f"PlaceObj('ModItemEntity', {{ 'name', \"{new}\", 'ClassParents', {{}}, 'entity_name', \"{new}\" }}),"
multi_line=f"PlaceObj('ModItemEntity', {{\n    'name', \"{new}\",\n    'ClassParents', {{}},\n    'entity_name', \"{new}\",\n}}),"
assert asset_items.count(one_line)==1
outputs[assets/'items.lua']=asset_items.replace(one_line,multi_line).encode()
meta=(assets/'metadata.lua').read_text(encoding='utf-8')
meta=add_metadata(meta,'entities',[f'"{new}"'])
meta=add_metadata(meta,'code',[f'"Entities/{new}.lua"'])
outputs[assets/'metadata.lua']=meta.encode()
for path,data in outputs.items():
 if path.suffix=='.lua':LuaRuntime().compile(data.decode('utf-8'))
before={path:path.read_bytes() if path.exists() else None for path in outputs}
stage=a.build/'install-stage'
for path,data in outputs.items():
 relative=path.relative_to(root.parent);out=stage/relative;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
if a.apply:
 check=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,Ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True)
 assert not check.stdout.strip(),'Game/editor must be closed'
 backup=a.build/'install-backup';assert not backup.exists(),backup
 for path,old in before.items():assert (path.read_bytes() if path.exists() else None)==old,str(path)
 for path,old in before.items():
  if old is not None:
   keep=backup/path.relative_to(root.parent);keep.parent.mkdir(parents=True,exist_ok=True);keep.write_bytes(old)
 for path,data in outputs.items():path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
print('APPLIED' if a.apply else 'STAGED',len(outputs),'files;',log)
