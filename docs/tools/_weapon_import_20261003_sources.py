"""Inventory 32 active plan entries (Mk12 deferred), reuse hash-matched imports.

--weapons DIR --output DIR --blender EXE [--import-new]
Does not install game data. Stores original archive hashes and per-source errors.
"""
import argparse,hashlib,json,re,subprocess,sys,zipfile
from pathlib import Path
from _audit_jaweapons_materials import inventory,rar_inventory,classify
from _import_jaweapons_batch import extract_source
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser(description=__doc__)
for k in ('weapons','output','blender'):p.add_argument('--'+k,type=Path,required=True)
p.add_argument('--import-new',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
text=(ROOT/'docs/design/weapons-import-plan-jaweapons.md').read_text(encoding='utf-8-sig').split('### Предложения по характеристикам')[0]
entries={}
for line in text.splitlines():
 m=re.match(r'\|\s*(\d+)(а?)\s*\|\s*([^|]+)\|',line)
 if not m:continue
 n=int(m[1]);entry=entries.setdefault(n,{'number':n,'name':m[3].strip(),'sources':[]})
 entry['sources']+=re.findall(r'`E:/JaWeapons/Weapons/([^`]+\.(?:zip|rar|glb))`',line)
entries[20]={'number':20,'name':'СКС: продвинутое цевьё','sources':['Assault/SKS Modern Assault Rifle.zip']}
assert set(entries)==set(range(1,34))-{10},entries.keys()
existing={1:[],2:[],3:[],4:['M14SAW','M21'],5:['G36','G36c'],6:[],7:['Sig550','Sig550Custom','Sig552','Sig552SWAT'],8:[],9:[],10:[],11:['Gewehr98'],12:['MP5','MP5A2','MP5A4','MP5K','MP5SD'],13:['G3A3','G3A4','G3SniperV1'],14:[],15:[],16:[],17:[],18:[],19:[],20:['SKS'],21:['R870'],22:[],23:[],24:[],25:[],26:[],27:[],28:[],29:[],30:['M72LAW'],31:[],32:[],33:[]}
cache={}
for state in (a.weapons/'_batch_jazz_import').glob('*/source-state.json'):
 d=json.loads(state.read_text());cache[(Path(d['source']).name.lower(),d['sha256'])]=state.parent
report={'entries':list(entries.values()),'sources':{}}
def save():
 (a.output/'sources.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
for n,entry in sorted(entries.items()):
 entry['existing_ids']=existing[n];entry['integration']='PENDING'
 if n==1 and (a.weapons/'_aek_jazz_build/integration-receipt.json').exists() and (ROOT/'InventoryItem/AEK971.lua').exists():entry['integration']='INSTALLED_CANDIDATE_RUNTIME_PENDING'
 for ident in existing[n]:assert (ROOT/'InventoryItem'/(ident+'.lua')).is_file(),ident
 for rel in entry['sources']:
  if rel in report['sources']:continue
  source=a.weapons/rel;row={'relative_path':rel,'exists':source.is_file()};report['sources'][rel]=row;save()
  if not source.is_file():row['status']='MISSING';save();continue
  digest=hashlib.file_digest(source.open('rb'),'sha256').hexdigest();row['sha256']=digest
  old=cache.get((source.name.lower(),digest))
  if old and (old/'import-report.json').exists():
   result=json.loads((old/'import-report.json').read_text());row.update(build=str(old),status=result['status'],audit=result,reused=True)
   if source.name=='Mk 12 Special Purpose Rifle.zip':row.update(status='REJECT_INCOMPLETE',reason='Main meshes have no UV; historical diagnosis retained')
   print(f'{n}: REUSED {source.name}: {row["status"]}',flush=True);save();continue
  try:
   data={'path':str(source),'name':source.name}
   if source.suffix.lower()=='.zip':
    with zipfile.ZipFile(source) as z:data.update(inventory(z.namelist(),z.read))
   elif source.suffix.lower()=='.rar':data.update(rar_inventory(source,'C:/Program Files/7-Zip/7z.exe'))
   else:data.update(inventory([source.name],lambda _:source.read_bytes()))
   data['status'],data['reason']=classify(data);row['material_audit']=data;row['status']=data['status']
   slug=re.sub('[^A-Za-z0-9_-]+','_',source.stem).strip('_')
   # The legacy worker reserves numeric folder prefixes for its original queue.
   # Keep this queue in a distinct namespace; numbers are not material profiles.
   build=a.output/'sources'/('q'+str(n).zfill(2)+'_'+slug);row['build']=str(build)
   if a.import_new and data['status']!='REJECT':
    if build.exists():
     assert json.loads((build/'source-state.json').read_text())['sha256']==digest
    else:
     build.mkdir(parents=True);extract_source(source,build/'source','C:/Program Files/7-Zip/7z.exe')
     (build/'source-state.json').write_text(json.dumps({'source':str(source),'sha256':digest}))
    if not (build/'import-report.json').exists():
     with (build/'blender.log').open('w') as log:
      proc=subprocess.run([str(a.blender),'--background','--factory-startup','--disable-autoexec','--python-exit-code','1','--python',str(Path(__file__).with_name('_import_jaweapons_scene.py')),'--','--build',str(build)],stdout=log,stderr=subprocess.STDOUT,timeout=600)
     assert proc.returncode==0,'Blender import failed; see '+str(build/'blender.log')
    row['audit']=json.loads((build/'import-report.json').read_text());row['status']=row['audit']['status']
   assert hashlib.file_digest(source.open('rb'),'sha256').hexdigest()==digest
  except Exception as e:row.update(status='ERROR',reason=str(e))
  print(f'{n}: {source.name}: {row["status"]}',flush=True);save()
print('ALL_ENTRIES',len(entries),'SOURCES',len(report['sources']),flush=True)
