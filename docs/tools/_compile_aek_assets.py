"""Compile AEK FBX candidates and check actual HGM winding, never active mods.
--build DIR --game-root DIR --blender EXE
"""
import argparse,json,shutil,subprocess,sys
from pathlib import Path
from _prepare_rifle_assets import stage
from _decode_vz58_hgm import decode
p=argparse.ArgumentParser()
for k in ('build','game-root','blender'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();results=[];names=[]
for d in ('ModAssets','ExportedEntities','compiled'):(a.build/d).mkdir(exist_ok=True)
for f in sorted((a.build/'rigged').glob('JAZZ_AEK*.fbx')):
 name=f.stem;names.append(name);target=a.build/'mesh'/name/f.name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,target)
 logpath=a.build/'compiled'/(name+'-processor.log')
 with logpath.open('w') as log:subprocess.run([str(a.game_root/'ModTools/AssetsProcessor/AssetsProcessor.exe'),str(target),'-globalappdirs','-gamepath',str(a.game_root)],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=180)
 log=logpath.read_text(errors='replace');assert '*** Done! ***' in log and '[Error]' not in log and 'normals with 0 length' not in log,log[-1000:]
 decoded=a.build/'compiled'/(name+'.json');decoded.write_text(json.dumps(decode(a.build/'ExportedEntities/Meshes'/(name+'_Mesh.m.hgm'))))
 result=a.build/'compiled'/(name+'-audit.json')
 with (a.build/'compiled'/(name+'-audit.log')).open('w') as log:subprocess.run([str(a.blender),'--background','--factory-startup','--python-exit-code','1','--python',str(Path(__file__).with_name('_audit_compiled_weapon_mesh.py')),'--','--blend',str(a.build/'rigged/AEK_JA3.blend'),'--entity',name,'--decoded',str(decoded),'--report',str(result),'--check-winding'],stdout=log,stderr=subprocess.STDOUT,check=True)
 results.append(json.loads(result.read_text()));assert results[-1]['pass'];print('PASS',name,flush=True)
assert len(names)==8
stage(a.build,a.build/'ExportedEntities',a.game_root,'JAZZ_AEK',names)
(a.build/'compiled-audit.json').write_text(json.dumps(results,indent=2))
