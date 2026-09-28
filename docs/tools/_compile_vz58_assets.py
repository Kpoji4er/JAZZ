"""Compile/stage/audit VZ58 entities; --build DIR --game-root DIR --blender EXE --decoder EXE [--skip-compile]."""
import argparse,json,subprocess,sys,xml.etree.ElementTree as ET
from pathlib import Path
from _prepare_rifle_assets import stage
p=argparse.ArgumentParser()
for k in ('build','game-root','blender','decoder'):p.add_argument('--'+k,type=Path,required=True)
p.add_argument('--skip-compile',action='store_true');a=p.parse_args();r=a.build;game=a.game_root
files=sorted((r/'rigged').glob('JAZZ_VZ58*.fbx'));assert len(files)==14
if not a.skip_compile:
 for f in files:
  with (r/(f.stem+'-processor.log')).open('w') as log:
   subprocess.run([str(game/'ModTools/AssetsProcessor/AssetsProcessor.exe'),str(f),'-globalappdirs','-gamepath',str(game)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=180)
export=r.parent/'ExportedEntities';names=[f.stem for f in files];stage(r,export,game,'JAZZ_VZ58',names)
# A repeated build may rename shared DDS indices after adding a map.
# Remove only our stale stage textures; the active mod is refreshed separately.
staged=r/'mod-assets-stage/Entities';used=set()
for material in (staged/'Materials').glob('JAZZ_VZ58*.mtl'):
 used.update(t.get('Name') for t in ET.parse(material).getroot().iter() if t.get('Name'))
for folder in ['Textures','Textures/Fallbacks']:
 for texture in (staged/folder).glob('JAZZ_VZ58_*.dds'):
  if texture.name not in used:
   assert texture.resolve().is_relative_to(staged.resolve());texture.unlink()
qa=r/'compiled';qa.mkdir(exist_ok=True);results=[]
for name in names:
 hgm=export/'Meshes'/(name+'_Mesh.m.hgm');decoded=qa/(name+'.json');report=qa/(name+'-audit.json')
 from _decode_vz58_hgm import decode
 decoded.write_text(json.dumps(decode(hgm)),encoding='utf-8')
 with (qa/(name+'.log')).open('w') as log:
  subprocess.run([str(a.blender),'--background','--factory-startup','--python-exit-code','1','--python',str(Path(__file__).parent/'_audit_compiled_weapon_mesh.py'),'--','--blend',str(r/'rigged/VZ58_JA3.blend'),'--entity',name,'--check-winding','--decoded',str(decoded),'--report',str(report)],check=True,stdout=log,stderr=subprocess.STDOUT)
 results.append(json.loads(report.read_text()));print('PASS',name,flush=True)
(r/'compiled-audit.json').write_text(json.dumps({'pass':all(v['pass'] for v in results),'entities':results},indent=2),encoding='utf-8')
