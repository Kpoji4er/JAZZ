"""Stage/install existing VZ58/R4 DDS names from native material exports.

--vz58-build DIR --r4-build DIR --export-root DIR --game-root DIR --output DIR
[--icon FILE] [--apply]. R4 mesh requires compiled+UV audit; no registration writes.
"""
import argparse,hashlib,json,struct,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];ASSETS=ROOT.parent/'jazz_assets'
p=argparse.ArgumentParser()
for key in ('vz58-build','r4-build','export-root','game-root','output'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--icon',type=Path);p.add_argument('--apply',action='store_true');a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True);sources={};updates={}
for build in (a.vz58_build,a.r4_build):
 report=json.loads((build/'material-report.json').read_text())
 for entity in report['entities']:
  log=build/(entity+'-processor.log')
  assert log.exists() and '*** Done! ***' in log.read_text(errors='replace') and '[Error]' not in log.read_text(errors='replace'),('Compile incomplete',entity)
  assert log.stat().st_mtime>=(build/'rigged'/(entity+'.fbx')).stat().st_mtime,('Stale compile',entity)
  ent=ET.parse(ASSETS/'Entities'/(entity+'.ent'))
  for ref in ent.findall('.//material'):
   rel=Path(ref.get('file'));before=ET.parse(ASSETS/'Entities'/rel);after=ET.parse(a.export_root/rel)
   old={n.tag:n.get('Name') for n in before.getroot().iter() if n.get('Name')}
   new={n.tag:n.get('Name') for n in after.getroot().iter() if n.get('Name')}
   assert old.keys()==new.keys()
   for slot in ('NormalMap','RMMap','BaseColorMap'):
    if slot not in old:continue
    name=old[slot]
    # Keep base albedo byte-exact except for the two explicitly repainted atlases.
    if slot=='BaseColorMap' and name not in ('JAZZ_VZ58_11_Base.dds','JAZZ_VZ58_26_Base.dds'):continue
    src=a.export_root/'Textures'/new[slot]
    if name in sources:assert sources[name].read_bytes()==src.read_bytes(),name
    sources[name]=src
for name,src in sources.items():
 assert name.startswith(('JAZZ_VZ58_','JAZZ_VektorR4_'))
 for folder,size in (('Textures',2048),('Textures/Fallbacks',64)):
  dest=a.output/'staged'/folder/name;dest.parent.mkdir(parents=True,exist_ok=True)
  subprocess.run([str(a.game_root/'ModTools/hgimgcvt.exe'),str(src),str(dest),'--truncate',str(size)],check=True,capture_output=True)
  raw=dest.read_bytes();assert raw[:4]==b'DDS ';h,w=struct.unpack_from('<II',raw,12);assert max(h,w)<=size
  target=ASSETS/'Entities'/folder/name;assert target.exists()
  if target.read_bytes()!=raw:updates[target]=raw
if a.icon:
 from PIL import Image
 im=Image.open(a.icon);assert im.size==(324,165) and im.mode=='RGBA'
 updates[ROOT/'WeaponIcons/VZ58.png']=a.icon.read_bytes()
r4audit=json.loads((a.r4_build/'compiled-audit.json').read_text());assert r4audit['pass']
r4uv=json.loads((a.r4_build/'uv-audit.json').read_text())['JAZZ_VektorR4']
assert r4uv['added']==0 and r4uv['missing']==r4uv.get('allowed_submicron_slivers',0)
mesh=ASSETS/'Entities/Meshes/JAZZ_VektorR4_Mesh.m.hgm'
raw=(a.export_root/'Meshes'/mesh.name).read_bytes()
if mesh.read_bytes()!=raw:updates[mesh]=raw
report=[]
for target,raw in updates.items():
 rel=target.relative_to(ROOT.parent);old=target.read_bytes()
 report.append({'path':rel.as_posix(),'before':hashlib.sha256(old).hexdigest(),'after':hashlib.sha256(raw).hexdigest()})
 if a.apply:
  backup=a.output/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True)
  assert not backup.exists(),'Refuse to overwrite backup'
  backup.write_bytes(old);target.write_bytes(raw)
(a.output/'install-report.json').write_text(json.dumps({'applied':a.apply,'files':report},indent=2))
print('APPLIED' if a.apply else 'STAGED',len(report),'files')
