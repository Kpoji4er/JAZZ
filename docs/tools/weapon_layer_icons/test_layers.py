"""Exercise native-layer selection, exact captured graphs, and Cartesian coverage."""
import argparse,hashlib,itertools,json
from pathlib import Path
from lupa import LuaRuntime

def main():
 p=argparse.ArgumentParser(__doc__);p.add_argument('--registry',type=Path,required=True);p.add_argument('--captures',type=Path,nargs='*',default=[]);p.add_argument('--graphs',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 data=json.loads(a.registry.read_text(encoding='utf-8'));lua=LuaRuntime(unpack_returned_tuples=True)
 def table(value):
  if isinstance(value,dict):return lua.table_from({k:table(v) for k,v in value.items()})
  if isinstance(value,list):return lua.table_from([table(v) for v in value])
  return value
 registry=table(data);selector=lua.execute((Path(__file__).parent/'layer_selector.lua').read_text(encoding='utf-8-sig'))
 def resolve(item):
  result=selector.resolve(registry,table(item))
  return result if isinstance(result,tuple) else (result,None)
 cases=0;failures=[];coverage=[];excluded_fixed_variants=0;superseded_camera_references=0;excluded_blocked_combinations=0
 for weapon,profile in data['weapons'].items():
  slots=profile['slots'];miss=0;total=0;blocked=0
  for combination in itertools.product(*[list(s['options']) for s in slots]):
   item={'class':weapon,'Entity':profile['base']['__host'],'components':dict(zip([s['slot'] for s in slots],combination))}
   if any(item['components'].get(other) for s,value in zip(slots,combination) for other in s.get('blocked_slots',{}).get(value,[])):
    blocked+=1;excluded_blocked_combinations+=1;continue
   for s,value in zip(slots,combination):
    effect=profile['rules'].get(s['slot'],{}).get(value,{})
    if effect.get('__host'):item['Entity']=effect['__host']
   plan,error=resolve(item);cases+=1;total+=1
   if not plan:
    miss+=1
    if miss<=3:failures.append({'weapon':weapon,'components':item['components'],'reason':error})
  coverage.append({'weapon':weapon,'cartesian_cases':total,'excluded_blocked_combinations':blocked,'unresolved':miss})
 receipts=[directory/'capture-report.json' for directory in a.captures]
 if a.graphs:receipts.extend(p for p in a.graphs.glob('*.json') if p.stem in data['weapons'])
 for path in receipts:
  receipt=json.loads(path.read_text(encoding='utf-8'))
  for row in receipt['rows']:
   if row['weapon'] not in data['weapons'] or row.get('layer') or row['status'] not in ('captured','graph-only'):continue
   if row['status']=='captured' and row.get('camera_distance',1500)!=data['weapons'][row['weapon']].get('camera_distance',1500):
    superseded_camera_references+=1;continue
   slot=row.get('requested_slot')
   declared=next((s for s in data['weapons'][row['weapon']]['slots'] if s['slot']==slot),None)
   if declared and row.get('requested_component','') not in declared['options']:
    excluded_fixed_variants+=1;continue
   plan,error=resolve({'class':row['weapon'],'Entity':row['entity'],'components':row['components']})
   expected={hashlib.sha256(d['signature'].encode()).hexdigest()[:20] for d in row['layer_graph'] if d['entity']}
   actual={ident for _,ident in plan.nodes.items()} if plan else set()
   if actual!=expected:failures.append({'weapon':row['weapon'],'label':row['label'],'reason':'native graph mismatch','resolution_error':error,'missing':sorted(expected-actual),'extra':sorted(actual-expected)})
   cases+=1
 # Unknown inputs must never leave a partial assembly.
 assert resolve({'class':'unknown','components':{}})[0] is None
 for weapon,profile in data['weapons'].items():
  components={s['slot']:s['default'] for s in profile['slots']};components['unknown']='unknown'
  assert resolve({'class':weapon,'Entity':profile['base']['__host'],'components':components})[0] is None
  original={'class':weapon,'Entity':profile['base']['__host'],'components':{s['slot']:s['default'] for s in profile['slots']}}
  first,_=resolve(original);second,_=resolve(original)
  if not first or not second or first.key!=second.key:failures.append({'weapon':weapon,'reason':'default unresolved or unstable'})
 report={'status':'FAIL' if failures else 'PASS','registry_sha256':hashlib.sha256(a.registry.read_bytes()).hexdigest(),'selector_sha256':hashlib.sha256(Path(__file__).with_name('layer_selector.lua').read_bytes()).hexdigest(),'cases':cases,'excluded_blocked_combinations':excluded_blocked_combinations,'excluded_fixed_variants':excluded_fixed_variants,'superseded_camera_references':superseded_camera_references,'coverage':coverage,'failures':failures,'level':'offline Lua and captured native graph; UI not exercised'}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=True));raise SystemExit(bool(failures))
if __name__=='__main__':main()
