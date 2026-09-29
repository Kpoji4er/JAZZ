"""Cover missing native layer signatures with a finite greedy supplement batch.

Waits for the initial batch if requested, compares the pairwise/dense native
oracle to photographs, and only photographs new native positions/entities.
"""
import argparse,json,subprocess,sys
from pathlib import Path
from run_dependencies import wait,read

def plan(catalog,captures,graphs):
    known=set()
    for directory in captures:
        for row in read(directory/'capture-report.json')['rows']:
            if row['status']=='captured' and row.get('layer_signature') and row.get('layer_entity'):
                known.add(row['layer_signature'])
    slots={w['id']:[s['slot'] for s in w['slots']] for w in catalog['weapons']}
    candidates=[];missing=set();defaults=[]
    for path in graphs.glob('*.json'):
        if path.stem not in slots:continue
        graph_rows=read(path)['rows']
        for row in graph_rows:
            absent={d['signature'] for d in row['layer_graph'] if d['entity']}-known
            if absent:candidates.append((row,absent));missing.update(absent)
        default=graph_rows[0]
        host=next(d['signature'] for d in default['layer_graph'] if d['spot']=='__host')
        if host not in known:defaults.append(default)
    total=len(missing);builds=[]
    for row in defaults:
        builds.append({'weapon':row['weapon'],'label':'default','components':{},'expected':row['components'],'order':slots[row['weapon']]})
        missing-={d['signature'] for d in row['layer_graph'] if d['entity']}
    while missing:
        row,covered=max(candidates,key=lambda r:len(r[1]&missing))
        assert covered&missing,'Uncoverable native layers'
        builds.append({'weapon':row['weapon'],'label':'combination-'+str(len(builds)+1).zfill(4),'components':row['requested'],'expected':row['components'],'order':slots[row['weapon']]})
        missing-=covered
    return {'missing_layers':total,'builds':builds,'known_layers':{s:True for s in sorted(known)}}

def main():
    p=argparse.ArgumentParser(__doc__);p.add_argument('--catalog',type=Path,required=True);p.add_argument('--captures',type=Path,nargs='+',required=True);p.add_argument('--graphs',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--wait',action='store_true');p.add_argument('--dispatch',action='store_true');a=p.parse_args()
    if a.wait:
        for directory in a.captures:wait(directory)
    result=plan(read(a.catalog),a.captures,a.graphs)
    a.output.mkdir(parents=True,exist_ok=True);plan_path=a.output/'supplement-plan.json'
    plan_path.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({'builds':len(result['builds']),'missing_layers':result['missing_layers']}),flush=True)
    if a.dispatch and result['builds']:
        subprocess.run([sys.executable,str(Path(__file__).with_name('dispatch_capture.py')),'--configurations',str(plan_path),'--output',str(a.output),'--layers','--matte','--resume-inventory-pause'],check=True)
        wait(a.output,True)

if __name__=='__main__':main()
