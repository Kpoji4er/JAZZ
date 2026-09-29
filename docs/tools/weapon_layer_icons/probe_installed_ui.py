"""Capture real installed UI and temporary combined-weapon widgets, then clean up."""
import argparse,json
from pathlib import Path
from install_layers import lua
from live import evaluate,quote

p=argparse.ArgumentParser(__doc__);p.add_argument('--graphs',type=Path,required=True);p.add_argument('--catalog',type=Path,required=True);p.add_argument('--captures',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
for directory in a.captures:
 r=json.loads((directory/'capture-report.json').read_text(encoding='utf-8'));assert r['phase']=='done' and r['disposed']
catalog={w['id']:w for w in json.loads(a.catalog.read_text(encoding='utf-8'))['weapons']}
builds=[]
for weapon in ('AK74','M4A1','DesertEagle'):
 rows=json.loads((a.graphs/(weapon+'.json')).read_text(encoding='utf-8'))['rows'];defaults=rows[0]['components']
 selected=max(rows,key=lambda r:sum(bool(v) and v!=defaults.get(k) for k,v in r['components'].items()))
 builds.append({'weapon':weapon,'order':[s['slot'] for s in catalog[weapon]['slots'] if isinstance(s['slot'],str)],'requested':selected['requested'],'expected':selected['components']})
a.output.mkdir(parents=True,exist_ok=True)
source=Path(__file__).with_suffix('.lua').read_text(encoding='utf-8')
body='local fn=assert(load('+quote(source)+',"installed layer UI probe","t",_G))();return fn('+lua({'output':a.output.resolve().as_posix(),'builds':builds})+')'
evaluate(body,a.output/'dispatch.json',True)
