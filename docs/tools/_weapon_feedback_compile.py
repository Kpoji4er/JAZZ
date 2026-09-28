"""Compile isolated feedback candidates and audit the produced HGM before staging.

--build DIR --game-root DIR --blender EXE. Never installs resources.
"""
import argparse,json,subprocess,sys
from pathlib import Path
from _decode_vz58_hgm import decode
p=argparse.ArgumentParser()
for key in ('build','game-root','blender'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--only',help='Recompile one changed entity and retain other completed audits')
a=p.parse_args();reports=[]
if a.only:
    reports=[r for r in json.loads((a.build/'compiled-report.json').read_text()) if r['entity']!=a.only]
(a.build/'compiled-report.json').write_text('[]')  # Invalidate any previous completed run.
for fbx in sorted((a.build/'mesh').glob('*/*.fbx')):
    if a.only and fbx.stem!=a.only:continue
    name=fbx.stem;out=fbx.parent
    with (out/'processor.log').open('w') as log:
        subprocess.run([str(a.game_root/'ModTools/AssetsProcessor/AssetsProcessor.exe'),str(fbx),'-globalappdirs','-gamepath',str(a.game_root)],check=True,stdout=log,stderr=subprocess.STDOUT)
    log=(out/'processor.log').read_text(errors='replace')
    assert '*** Done! ***' in log and '[Error]' not in log and 'normals with 0 length' not in log,(name,log[-1200:])
    exported=a.build/'ExportedEntities';hgm=exported/'Meshes'/(name+'_Mesh.m.hgm')
    assert hgm.is_file(),hgm
    (out/'compiled.json').write_text(json.dumps(decode(hgm)))
    with (out/'audit.log').open('w') as log:
        subprocess.run([str(a.blender),'--background','--factory-startup','--python-exit-code','1','--python',str(Path(__file__).parent/'_audit_compiled_weapon_mesh.py'),'--','--blend',str(out/(name+'.blend')),'--entity',name,'--decoded',str(out/'compiled.json'),'--report',str(out/'compiled-audit.json'),'--check-winding'],check=True,stdout=log,stderr=subprocess.STDOUT)
    reports.append(json.loads((out/'compiled-audit.json').read_text()));assert reports[-1]['pass']
    print('COMPILED_AND_AUDITED',name,flush=True)
(a.build/'compiled-report.json').write_text(json.dumps(reports,indent=2))
