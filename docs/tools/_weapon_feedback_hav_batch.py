"""Stage rear skin corrections on current HAV HGMs; preserve all other bytes.
--build DIR --assets DIR --reader EXE --blender EXE --shirt JSON.
No active-mod writes. Both mesh descriptions in each existing entity are covered.
"""
import argparse,json,subprocess,sys,hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
p=argparse.ArgumentParser()
for k in ('build','assets','reader','blender','shirt'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();tools=Path(__file__).resolve().parent;out=a.build/'hav';out.mkdir(parents=True,exist_ok=True);report=[]
for family in ('Twaron','Guardian','Zylon'):
 for variant in ('Light','Medium','Full'):
  entity='JAZZ_'+family+variant+'_Male'
  for resource in sorted({n.get('file') for n in ET.parse(a.assets/'Entities'/(entity+'.ent')).findall('.//mesh')}):
   src=a.assets/'Entities'/resource;label=src.stem;folder=out/label;folder.mkdir(exist_ok=True);decoded=folder/'before.json';candidate=folder/src.name
   subprocess.run([str(a.reader),str(src),str(decoded)],check=True,capture_output=True)
   if not json.loads(decoded.read_text())['bones']:
    print('PRESERVED static mesh description',resource,flush=True);continue
   with (folder/'weights.log').open('w') as log:
    subprocess.run([str(a.blender),'-b','--factory-startup','--python-exit-code','1','--python',str(tools/'_weapon_feedback_native_skin.py'),'--','--armor',str(decoded),'--shirt',str(a.shirt),'--output',str(folder/'weights.json')],check=True,stdout=log,stderr=subprocess.STDOUT)
   subprocess.run([sys.executable,str(tools/'_weapon_feedback_hgm_skin.py'),'--input',str(src),'--decoded',str(decoded),'--weights',str(folder/'weights.json'),'--output',str(candidate)],check=True)
   subprocess.run([str(a.reader),str(candidate),str(folder/'after.json')],check=True,capture_output=True)
   before=json.loads(decoded.read_text());after=json.loads((folder/'after.json').read_text());assert before['bones']==after['bones'] and before['bbox']==after['bbox']
   for x,y in zip(before['meshes'],after['meshes']):
    for key in ('vertices','faces','bbox','material_index'):assert x[key]==y[key],(entity,key)
    for old,new in zip(x['bone_weights'],y['bone_weights']):
     if old!=new:assert abs(sum(new)-1)<1e-6
   report.append({'entity':entity,'resource':resource,'candidate':str(candidate),'before':hashlib.sha256(src.read_bytes()).hexdigest(),'after':hashlib.sha256(candidate.read_bytes()).hexdigest(),'only_skin_changed':True})
  print('STAGED',entity,flush=True)
(out/'manifest.json').write_text(json.dumps(report,indent=2))
