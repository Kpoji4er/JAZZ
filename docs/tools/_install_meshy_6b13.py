"""Install the approved 6B13 resources/registration and Legion mapping; dry-run by default."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--build-root',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[2];assets=root.parent/'jazz_assets';src=a.build_root.resolve();stage=src/'build/mod-assets-stage/Entities';entity='JAZZ_6B13_Male'
assert json.loads((src/'compiled-audit.json').read_text())['pass']
assert json.loads((src/'texture-audit.json').read_text())['pass']
assert (src/'clothed-poses/pose-check.json').exists()
receipt=src/'installation.json';assert not receipt.exists(),'Already installed; inspect receipt'
changes={}
files=[Path(entity+'.ent'),Path('Meshes')/(entity+'_mesh.m.hgm'),Path('Materials')/(entity+'_mesh.mtl')]+[Path(d)/(entity+'_'+s+'.dds') for d in ['Textures','Textures/Fallbacks'] for s in ['Base','Norm','RM']]
for f in files:changes[assets/'Entities'/f]=(stage/f).read_bytes()
changes[assets/'Entities'/(entity+'.lua')]=f'EntityData["{entity}"] = {{ editor_artset = "Mods", entity = {{ class_parent = "CharacterArmorMale" }} }}\n'.encode()
items=assets/'items.lua';data=items.read_bytes();assert entity.encode() not in data
pat=rb"PlaceObj\('ModItemEntity', \{\r?\n    'name', \"JAZZ_6B3_Male\",.*?\r?\n\}\),"
m=re.search(pat,data,re.S);assert m
new=m[0].replace(b'JAZZ_6B3_Male',entity.encode());new=new.replace(b"    'ClassParents'",b"    'class_parent', \"CharacterArmorMale\",\n    'ClassParents'")
changes[items]=data[:m.end()]+b'\n'+new+data[m.end():]
meta=assets/'metadata.lua';data=meta.read_bytes()
for old,new in [(b'"JAZZ_6B3_Male",',b'"JAZZ_6B13_Male",'),(b'"Entities/JAZZ_6B3_Male.lua",',b'"Entities/JAZZ_6B13_Male.lua",')]:
 assert data.count(old)==1 and new not in data;data=data.replace(old,old+b'\n\t\t'+new)
changes[meta]=data
code=root/'Code/System_LegionArmorVisuals.lua';data=code.read_bytes();anchor=b'\tJazzArmor_6B3 = { Male = "JAZZ_6B3_Male" },';assert data.count(anchor)==1 and b'JazzArmor_6B13' not in data
changes[code]=data.replace(anchor,anchor+b'\n\tJazzArmor_6B13 = { Male = "JAZZ_6B13_Male" },')
print('Prepared',len(changes),'files')
if not a.apply:raise SystemExit(0)
r=subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug,ged -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True);assert not r.stdout.strip(),'Game/editor is open'
rows=[]
for dest,content in changes.items():
 rel=dest.relative_to(root.parent);old=None
 if dest.exists():
  old=hashlib.sha256(dest.read_bytes()).hexdigest();backup=src/'installation-backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,backup)
 rows.append({'path':str(rel),'old_sha256':old,'sha256':hashlib.sha256(content).hexdigest()})
for dest,content in changes.items():dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
for row in rows:assert hashlib.sha256((root.parent/row['path']).read_bytes()).hexdigest()==row['sha256']
receipt.write_text(json.dumps({'files':rows,'runtime':'NOT_RUN','editor':'NOT_RUN'},indent=2));print('Installed and SHA256 verified')
