"""Bake, compile, stage and round-trip audit the approved leather source.

--blender EXE --game-root DIR --root candidate --reader HGM_READER
Requires successful source/contact checks. Does not install.
"""
import argparse,json,subprocess,sys,time
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
for key in ('blender','game-root','root','reader'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--skip-bake',action='store_true')
a=p.parse_args();root=a.root.resolve();tools=Path(__file__).resolve().parent
entity='JAZZ_LeatherArmor_Male';build=root/'build'
assert json.loads((root/'qa-report.json').read_text())['status']=='PASS_SOURCE_OFFLINE'
assert json.loads((root/'contacts.json').read_text())['status']=='PASS_SEWN_CONTACT'
base=[a.blender,'-b','--factory-startup','--threads','4','--python-exit-code','1','--python']
def run(label,args):
    print('START',label,flush=True)
    with (root/(label+'.log')).open('w',encoding='utf8') as stream:
        subprocess.run([str(x) for x in args],stdout=stream,stderr=subprocess.STDOUT,check=True)
    print('PASS',label,flush=True)
if not a.skip_bake:
    run('bake-export',base+[tools/'_build_legion_armor.py','--','--source',root/'source/LeatherArmor.blend',
        '--output',build,'--game-root',a.game_root,'--entity',entity,'--mesh-prefix','TEST_LeatherArmor',
        '--icon','LeatherArmor','--texture-size','2048'])
started=time.time()
run('processor',[a.game_root/'ModTools/AssetsProcessor/AssetsProcessor.exe',build/(entity+'.fbx'),
    '-globalappdirs','-gamepath',a.game_root])
export=next((folder for folder in (root/'ExportedEntities',root.parent/'ExportedEntities',build/'ExportedEntities')
    if (folder/(entity+'.ent')).is_file() and (folder/(entity+'.ent')).stat().st_mtime>=started-2),None)
assert export,'Missing freshly compiled entity'
run('stage',[sys.executable,tools/'_prepare_rifle_assets.py','--build',build,'--prefix','JAZZ_LeatherArmor',
    '--entities',entity,'--export-root',export,'--game-root',a.game_root])
run('decode',[a.reader,build/'mod-assets-stage/Entities/Meshes'/(entity+'_mesh.m.hgm'),root/'compiled.json'])
run('compiled-audit',base+[tools/'_audit_compiled_weapon_mesh.py','--','--blend',build/(entity+'.blend'),
    '--entity',entity,'--decoded',root/'compiled.json','--report',root/'compiled-audit.json','--check-winding'])
(root/'export-report.json').write_text(json.dumps({'status':'PASS_STAGED','entity':entity,
    'runtime':'NOT_RUN','installed':False,'compiled':json.loads((root/'compiled-audit.json').read_text())},indent=2))
