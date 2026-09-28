"""Review or export one existing rebuilt armor candidate; never install resources."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser(description=__doc__)
for key in ('blender', 'game-root', 'root', 'shirt'):
    p.add_argument('--'+key, required=True, type=Path)
p.add_argument('--kind', required=True, choices=('chainmail','brigantine','tire'))
p.add_argument('--phase', required=True, choices=('review','export','compiled'))
p.add_argument('--reader', type=Path, help='Built armor-hgm-reader executable')
a = p.parse_args()
tools = Path(__file__).resolve().parent
folder = a.root/a.kind
source = folder/(a.kind+'.blend')
item = {'chainmail':'Chainmail','brigantine':'TireBrigantine','tire':'TireArmor'}[a.kind]
entity = 'JAZZ_'+item+'_Male'
base = [a.blender,'-b','--factory-startup','--threads','4','--python-exit-code','1','--python']

def run(label, args):
    print('START',a.kind,label,flush=True)
    with (folder/(label+'.log')).open('w',encoding='utf8') as stream:
        subprocess.run([str(x) for x in args], stdout=stream, stderr=subprocess.STDOUT, check=True)
    print('PASS',a.kind,label,flush=True)

if a.phase == 'review':
    run('pose',base+[tools/'_check_soft_armor_poses.py','--','--source',source,'--output',folder/'poses','--no-renders'])
    run('views',base+[tools/'_audit_armor_views.py','--','--source',source,'--output',folder/'clothed-audit','--diagnostic','--poses','--shirt',a.shirt]+(['--wide'] if a.kind=='tire' else []))
elif a.phase == 'export':
    pose = json.loads((folder/'poses/pose-check.json').read_text())
    assert pose['status']=='PASS_SKIN_STRUCTURE'
    build = folder/'build'
    run('bake',base+[tools/'_build_legion_armor.py','--','--source',source,'--output',build,'--game-root',a.game_root,'--entity',entity,'--mesh-prefix','TEST_'+a.kind,'--icon',item,'--texture-size','2048'])
    started=time.time()
    run('processor',[a.game_root/'ModTools/AssetsProcessor/AssetsProcessor.exe',build/(entity+'.fbx'),'-globalappdirs','-gamepath',a.game_root])
    candidates=[a.root/'ExportedEntities',folder/'ExportedEntities',build/'ExportedEntities']
    export=next((path for path in candidates if (path/(entity+'.ent')).is_file() and (path/(entity+'.ent')).stat().st_mtime>=started-2),None)
    assert export is not None,'No fresh compiled entity'
    run('stage',[sys.executable,tools/'_prepare_rifle_assets.py','--build',build,'--prefix','JAZZ_'+item,'--entities',entity,'--export-root',export,'--game-root',a.game_root])
else:
    assert a.reader and a.reader.is_file(),'--reader is required for compiled audit'
    build=folder/'build'
    run('decode',[a.reader,build/'mod-assets-stage/Entities/Meshes'/(entity+'_mesh.m.hgm'),folder/'compiled.json'])
    run('roundtrip',base+[tools/'_audit_compiled_weapon_mesh.py','--','--blend',build/(entity+'.blend'),'--entity',entity,'--decoded',folder/'compiled.json','--report',folder/'compiled-audit.json'])
