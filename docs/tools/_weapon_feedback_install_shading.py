"""Install two audited shading meshes and icons, preserving material/texture bytes.
--build DIR [--apply]. Separate staging, backup, hash guards; game must be closed.
"""
import argparse,json,hashlib,subprocess
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
root=Path(__file__).resolve().parents[2];suite=root.parent;b=a.build
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=b/'shading-install.json'
if not a.apply:
 audits=json.loads((b/'compiled-report.json').read_text());assert len(audits)==2 and all(r['pass'] for r in audits)
 files={}
 for entity,icon in [('JAZZ_VektorR4','VektorR4'),('JAZZ_VZ58','VZ58')]:
  for rel,src in [('jazz_assets/Entities/Meshes/'+entity+'_Mesh.m.hgm',b/'ExportedEntities/Meshes'/(entity+'_Mesh.m.hgm')),('jazz/WeaponIcons/'+icon+'.png',b/'icons'/(icon+'.png'))]:
   if src.suffix=='.png':
    im=Image.open(src);assert im.size==(324,165) and im.mode=='RGBA'
   dest=b/'install-stage'/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(src.read_bytes())
   files[rel]={'before':sha(suite/rel),'after':sha(dest)}
 guards={}
 for folder in ('Entities/Materials','Entities/Textures'):
  for prefix in ('JAZZ_VZ58','JAZZ_VektorR4'):
   for f in (suite/'jazz_assets'/folder).rglob(prefix+'*'):
    if f.is_file():guards[str(f.relative_to(suite))]=sha(f)
 manifest.write_text(json.dumps({'files':files,'guards':guards,'applied':False},indent=2));print('STAGED',len(files),'files;',len(guards),'material/texture guards')
else:
 report=json.loads(manifest.read_text());assert not report['applied']
 assert not subprocess.run(['powershell','-NoProfile','-Command','Get-Process JA3,JA3Debug -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id'],capture_output=True,text=True).stdout.strip(),'Game/editor running'
 for rel,digest in report['guards'].items():assert sha(suite/rel)==digest,rel
 for rel,h in report['files'].items():assert sha(suite/rel)==h['before'] and sha(b/'install-stage'/rel)==h['after'],rel
 for rel in report['files']:
  backup=b/'install-backup'/rel;assert not backup.exists();backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes((suite/rel).read_bytes())
 try:
  for rel,h in report['files'].items():
   (suite/rel).write_bytes((b/'install-stage'/rel).read_bytes());assert sha(suite/rel)==h['after']
 except Exception:
  for rel in report['files']:(suite/rel).write_bytes((b/'install-backup'/rel).read_bytes())
  raise
 for rel,digest in report['guards'].items():assert sha(suite/rel)==digest
 report['applied']=True;manifest.write_text(json.dumps(report,indent=2));print('INSTALLED',len(report['files']),'files; materials/textures unchanged')
