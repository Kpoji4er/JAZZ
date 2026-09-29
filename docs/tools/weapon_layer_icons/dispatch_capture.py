"""Dispatch one bounded capture batch into existing JA3Debug, leave it running."""
import argparse
import hashlib
import json
from pathlib import Path
from live import evaluate,quote
from content_scope import disabled_ids
from install_layers import lua
from capture_settings import CAMERA_DISTANCES

p=argparse.ArgumentParser(__doc__)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--ids',nargs='+')
p.add_argument('--catalog',type=Path)
p.add_argument('--configurations',type=Path,help='Native oracle builds with ordered requests and expected effective components')
p.add_argument('--variants',nargs='*',default=[])
p.add_argument('--matte',action='store_true')
p.add_argument('--resume-inventory-pause',action='store_true',help='Temporarily resume only inventory pause on ModEditor and restore after capture')
p.add_argument('--layers',action='store_true',help='Capture native host and every attached part in the reference build')
p.add_argument('--distance',type=int,default=0,help='Whole-family camera override for oversized configurations')
p.add_argument('--prerequisite',action='append',default=[],help='Explicit slot=component applied before each requested change')
p.add_argument('--label-prefix',default='')
a=p.parse_args()
configuration=json.loads(a.configurations.read_text(encoding='utf-8')) if a.configurations else None
prerequisites=dict(value.split('=',1) for value in a.prerequisite)
if any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in a.label_prefix):
    p.error('label prefix must be alphanumeric, underscore or hyphen')
if a.catalog:
    a.ids=[r['id'] for r in json.loads(a.catalog.read_text(encoding='utf-8'))['weapons']]
if configuration:a.ids=sorted({b['weapon'] for b in configuration['builds']})
if not a.ids: p.error('--ids or --catalog is required')
excluded=disabled_ids() | ({'DebugAuto','UnderslungGrenadeLauncher'} if a.layers else set())
a.ids=[weapon for weapon in a.ids if weapon not in excluded]
if not a.ids: p.error('No active weapons: disabled content is excluded from capture')
a.output=a.output.resolve()
(a.output/'raw').mkdir(parents=True,exist_ok=True)
source=(Path(__file__).parent/'capture.lua').read_text(encoding='utf-8')
result=a.output/'dispatch.result.txt'
if result.exists(): result.unlink()
(a.output/'capture-plan.json').write_text(json.dumps({'ids':a.ids,'variants':a.variants,
    'layers':a.layers,'matte':a.matte,'resume_inventory_pause':a.resume_inventory_pause,'distance':a.distance,'prerequisites':prerequisites,'label_prefix':a.label_prefix,
    'configurations':configuration,'camera_distances':CAMERA_DISTANCES,
    'capture_source_sha256':hashlib.sha256(source.encode()).hexdigest()},indent=2),encoding='utf-8')
(a.output/'capture-source.lua').write_text(source,encoding='utf-8')
settings='{resume_inventory_pause='+str(a.resume_inventory_pause).lower()+',layers='+str(a.layers).lower()+',output='+quote(a.output.as_posix())+',distance='+str(a.distance)+',matte='+str(a.matte).lower()+',prefix='+quote(a.label_prefix)+',prerequisites={'+','.join('[ '+quote(k)+' ]='+quote(v) for k,v in prerequisites.items())+'},ids={'+','.join(quote(i) for i in a.ids)+'},variants={'+','.join('[ '+quote(s)+' ]=true' for s in a.variants)+'}}'
if configuration:
    configuration['builds']=[b for b in configuration['builds'] if b['weapon'] not in excluded]
    settings=settings[:-1]+',builds='+lua(configuration['builds'])+',known_layers='+lua(configuration.get('known_layers',{}))+'}'
body='local settings='+settings+';settings.camera_distances='+lua(CAMERA_DISTANCES)+';local factory=assert(load('+quote(source)+',"capture","t",_G))();return factory(settings)'
evaluate(body,a.output/'dispatch.json',True)
