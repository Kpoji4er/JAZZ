"""Rig and validate a staged leather carrier. No mod or game writes.

python docs/tools/_qa_leather_armor.py --blender EXE --sample BLEND --shirt JSON
  --reference V7_BLEND --output existing-model-folder [--views]
"""
import argparse
import json
import subprocess
from pathlib import Path

p=argparse.ArgumentParser(description=__doc__)
for key in ('blender','sample','shirt','reference','output'):
    p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--views',action='store_true')
a=p.parse_args()
root=Path(__file__).resolve().parent
out=a.output.resolve()
source=out/'source/LeatherArmor.blend'
base=[a.blender,'-b','--factory-startup','--threads','4','--python-exit-code','1']
def run(label,args):
    print('START',label,flush=True)
    with (out/(label+'.log')).open('w',encoding='utf8') as stream:
        subprocess.run([str(v) for v in args],stdout=stream,stderr=subprocess.STDOUT,check=True)
    print('PASS',label,flush=True)

run('rig',base+['--python',root/'_rig_6b3_vest.py','--','--sample',a.sample,
    '--clean',out/'clean/JazzArmor_LeatherArmor.blend','--output',source,
    '--shirt',a.shirt,'--reference',a.reference,'--native-only','--surface-skin','--torso-carrier','--item','LeatherArmor'])
run('normals',base+[source,'--python',root/'_audit_blender_normals.py','--','--mesh-prefix','TEST_LeatherArmor'])
run('poses',base+['--python',root/'_check_soft_armor_poses.py','--','--source',source,
    '--output',out/'poses','--no-renders'])
run('contacts',base+['--python',root/'_check_leather_armor_contacts.py','--','--source',source,
    '--output',out/'contacts.json'])
if a.views:
    run('clothed-poses',base+['--python',root/'_audit_armor_views.py','--','--source',source,
        '--output',out/'clothed-audit','--shirt',a.shirt,'--poses','--diagnostic'])
rig=json.loads((source.parent/'rig-report.json').read_text())
poses=json.loads((out/'poses/pose-check.json').read_text())
assert poses['status']=='PASS_SKIN_STRUCTURE'
(out/'qa-report.json').write_text(json.dumps({'status':'PASS_SOURCE_OFFLINE','rig':rig,
    'poses':poses,'contacts':json.loads((out/'contacts.json').read_text()),
    'export':'NOT_RUN','installed':False,'runtime':'NOT_RUN',
    'human_acceptance':'PENDING'},indent=2))
