"""Dispatch one bounded capture batch into existing JA3Debug, leave it running."""
import argparse
import hashlib
import json
from pathlib import Path
from live import evaluate,quote
from content_scope import disabled_ids

p=argparse.ArgumentParser(__doc__)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--ids',nargs='+')
p.add_argument('--catalog',type=Path)
p.add_argument('--variants',nargs='*',default=[])
p.add_argument('--matte',action='store_true')
p.add_argument('--distance',type=int,default=0,help='Whole-family camera override for oversized configurations')
p.add_argument('--prerequisite',action='append',default=[],help='Explicit slot=component applied before each requested change')
p.add_argument('--label-prefix',default='')
a=p.parse_args()
prerequisites=dict(value.split('=',1) for value in a.prerequisite)
if any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in a.label_prefix):
    p.error('label prefix must be alphanumeric, underscore or hyphen')
if a.catalog:
    a.ids=[r['id'] for r in json.loads(a.catalog.read_text(encoding='utf-8'))['weapons']]
if not a.ids: p.error('--ids or --catalog is required')
a.ids=[weapon for weapon in a.ids if weapon not in disabled_ids()]
if not a.ids: p.error('No active weapons: disabled content is excluded from capture')
a.output=a.output.resolve()
(a.output/'raw').mkdir(parents=True,exist_ok=True)
source=(Path(__file__).parent/'capture.lua').read_text(encoding='utf-8')
result=a.output/'dispatch.result.txt'
if result.exists(): result.unlink()
(a.output/'capture-plan.json').write_text(json.dumps({'ids':a.ids,'variants':a.variants,
    'matte':a.matte,'distance':a.distance,'prerequisites':prerequisites,'label_prefix':a.label_prefix,
    'capture_source_sha256':hashlib.sha256(source.encode()).hexdigest()},indent=2),encoding='utf-8')
(a.output/'capture-source.lua').write_text(source,encoding='utf-8')
settings='{output='+quote(a.output.as_posix())+',distance='+str(a.distance)+',matte='+str(a.matte).lower()+',prefix='+quote(a.label_prefix)+',prerequisites={'+','.join('[ '+quote(k)+' ]='+quote(v) for k,v in prerequisites.items())+'},ids={'+','.join(quote(i) for i in a.ids)+'},variants={'+','.join('[ '+quote(s)+' ]=true' for s in a.variants)+'}}'
body='local factory=assert(load('+quote(source)+',"capture","t",_G))(); return factory('+settings+')'
evaluate(body,a.output/'dispatch.json',True)
