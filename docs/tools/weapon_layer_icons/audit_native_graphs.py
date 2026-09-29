"""Dispatch native graph checks for every pair of attachment slot choices.

Produces effective combinations after native compatibility/setter rules, including
automatic removals. It does not photograph, move the camera, or install anything.
"""
import argparse,hashlib,itertools,json
from pathlib import Path
from content_scope import disabled_ids
from install_layers import lua
from capture_settings import CAMERA_DISTANCES
from live import evaluate,quote

p=argparse.ArgumentParser(__doc__);p.add_argument('--catalog',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--only',nargs='+');a=p.parse_args()
catalog=json.loads(a.catalog.read_text(encoding='utf-8-sig'));tasks=[]
for w in catalog['weapons']:
 if w['id'] in disabled_ids()|{'DebugAuto','UnderslungGrenadeLauncher'}:continue
 if a.only and w['id'] not in a.only:continue
 slots=w['slots'];domains={s['slot']:sorted({o['id'] for o in s['options']}|({''} if s['empty'] else set())) for s in slots if s['modifiable']}
 builds=[{}]
 for slot,options in domains.items():builds.extend({slot:option} for option in options)
 for (left,aopts),(right,bopts) in itertools.combinations(domains.items(),2):
  builds.extend({left:x,right:y} for x,y in itertools.product(aopts,bopts))
 # Include dense configurations as well as pairwise interactions.
 for index in range(max(map(len,domains.values()),default=0)):
  builds.append({slot:options[index%len(options)] for slot,options in domains.items() if options})
 tasks.append({'id':w['id'],'slots':[s['slot'] for s in slots],'builds':builds})
a.output.mkdir(parents=True,exist_ok=True)
source=Path(__file__).with_suffix('.lua').read_text(encoding='utf-8')
(a.output/'plan.json').write_text(json.dumps({'camera_distances':CAMERA_DISTANCES,'weapons':len(tasks),'attempts':sum(len(t['builds']) for t in tasks),'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'catalog_sha256':hashlib.sha256(a.catalog.read_bytes()).hexdigest()}),encoding='utf-8')
(a.output/'oracle-source.lua').write_text(source,encoding='utf-8')
body='local fn=assert(load('+quote(source)+',"native-layer-oracle","t",_G))();return fn('+lua({'output':a.output.resolve().as_posix(),'tasks':tasks,'camera_distances':CAMERA_DISTANCES})+')'
evaluate(body,a.output/'dispatch.json',True)
