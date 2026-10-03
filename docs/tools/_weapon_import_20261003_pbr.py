"""Stage unambiguous author metallic/roughness textures from the complete queue.
--sources sources.json --output DIR. No inferred metallic from specular maps.
Preserve source BC/NM pixels, pack linear scalar RM=(rough,rough,metal).
"""
import argparse,hashlib,json,re
from pathlib import Path
import numpy as np
from PIL import Image
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--sources',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
channel=re.compile(r'(?i)(?:[_. -])(?P<kind>base_?colou?r|albedo(?:transparency)?|diffuse|roughness|metallic|metalness|normal(?:s)?|rough|metal)(?P<tail>(?:[_. -]\d+)?)$')
manifest={'installed':False,'rule':'RM = (Roughness, Roughness, Metallic); data maps are Non-Color','sources':{}}
for source,row in json.loads(a.sources.read_text())['sources'].items():
 root=Path(row['build'])/'source';groups={};files=[]
 for path in root.rglob('*'):
  if not path.is_file() or path.suffix.lower() not in ('.png','.jpg','.jpeg','.tga','.dds'):continue
  m=channel.search(path.stem)
  if not m:continue
  kind=m['kind'].lower();kind='Base' if kind.startswith(('base','albedo','diffuse')) else 'Rough' if kind.startswith('rough') else 'Metal' if kind.startswith('metal') else 'Normal'
  key=(path.stem[:m.start()]+m['tail']).lower();groups.setdefault(key,{}).setdefault(kind,[]).append(path)
 entry={'groups':{},'stage_only':True};manifest['sources'][source]=entry
 for key,channels in groups.items():
  record={'channels':{k:[str(p.relative_to(root)) for p in paths] for k,paths in channels.items()},'status':'REVIEW'};entry['groups'][key]=record
  if any(len(v)!=1 for v in channels.values()):record['reason']='Multiple channel candidates';continue
  if not all(k in channels for k in ('Base','Rough','Metal','Normal')):record['reason']='Incomplete explicit metallic/roughness set; no guessing';continue
  selected={k:v[0] for k,v in channels.items()};images={k:Image.open(path).convert('RGBA') for k,path in selected.items()}
  if len({im.size for im in images.values()})!=1:record['reason']='Source dimensions differ; no automatic resampling';continue
  rough=np.asarray(images['Rough']);metal=np.asarray(images['Metal'])
  if not all(np.max(np.abs(arr[:,:,:3].astype(int)-arr[:,:,:1].astype(int)))<=1 for arr in (rough,metal)):
   record['reason']='Colored data map requires channel inspection';continue
  folder=a.output/hashlib.sha256(source.encode()).hexdigest()[:10]/re.sub('[^A-Za-z0-9_-]','_',key);folder.mkdir(parents=True,exist_ok=True)
  images['Base'].save(folder/'Base.tga');images['Normal'].save(folder/'Normal.tga')
  rm=np.stack((rough[:,:,0],rough[:,:,0],metal[:,:,0]),axis=-1);Image.fromarray(rm).save(folder/'RM.tga')
  assert np.array_equal(np.asarray(Image.open(folder/'RM.tga')),rm)
  for k in ('Base','Normal'):assert np.array_equal(np.asarray(Image.open(folder/(k+'.tga'))),np.asarray(images[k]))
  record.update(status='STAGED_EXPLICIT_PBR',size=list(images['Base'].size),output=str(folder),hashes={k:hashlib.sha256(path.read_bytes()).hexdigest() for k,path in selected.items()})
 print(source,sum(g['status']=='STAGED_EXPLICIT_PBR' for g in entry['groups'].values()),'sets',flush=True)
(a.output/'pbr-stage.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
