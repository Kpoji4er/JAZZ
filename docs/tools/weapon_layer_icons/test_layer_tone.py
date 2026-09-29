"""Verify an arsenal tone-only rebuild against the installed previous images."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image

p=argparse.ArgumentParser(__doc__);p.add_argument('--library',type=Path,required=True);p.add_argument('--before',type=Path,required=True);p.add_argument('--profiles',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
r=json.loads((a.library/'registry.json').read_text(encoding='utf-8'));profiles=json.loads(a.profiles.read_text(encoding='utf-8'))
failures=[];count=0;changed=0;digest=hashlib.sha256()
for ident,layer in sorted(r['layers'].items()):
 if not layer['image']:continue
 before=np.array(Image.open(a.before/(ident+'.png')).convert('RGBA'))
 path=a.library/'layers'/(ident+'.png');after=np.array(Image.open(path).convert('RGBA'))
 if before.shape!=after.shape or not np.array_equal(before[...,3],after[...,3]):failures.append(ident)
 if not np.array_equal(before,after):changed+=1
 count+=1;digest.update(ident.encode()+hashlib.sha256(path.read_bytes()).digest())
for name,profile in profiles['profiles'].items():
 x=np.array(profile['source_luma']);y=np.array(profile['target_luma'])
 if not (np.all(np.isfinite(y)) and np.all(np.diff(x)>0) and np.all(np.diff(y)>=0) and y.min()>=0 and y.max()<=1):failures.append(name)
report={'status':'FAIL' if failures else 'PASS','images':count,'changed_rgb':changed,'unchanged_alpha':count-len([v for v in failures if v in r['layers']]),'profiles':len(profiles['profiles']),'fallback_weapons':profiles['fallback_weapons'],'combined_png_sha256':digest.hexdigest(),'profiles_sha256':hashlib.sha256(a.profiles.read_bytes()).hexdigest(),'failures':failures,'level':'offline pixels and smooth monotonic profiles; visual comparison is separate'}
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report));raise SystemExit(bool(failures))
