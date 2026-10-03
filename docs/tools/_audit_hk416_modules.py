"""Audit HK416 archive, duplicate transforms and source texture families.
--source DIR --archive ZIP --output DIR. No source/runtime mutation.
"""
import argparse,hashlib,json,re
from pathlib import Path
from zipfile import ZipFile
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ('source','archive','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
def read(i):
 vertices=[];uv=[];faces=[]
 for line in (a.source/f'model_{i}.obj').read_text().splitlines():
  q=line.split()
  if q and q[0]=='v':vertices.append(list(map(float,q[1:4])))
  elif q and q[0]=='vt':uv.append(list(map(float,q[1:3])))
  elif q and q[0]=='f':faces.append(q[1:])
 return np.array(vertices),np.array(uv),faces
duplicates=[]
for i,j in [(21,25),(11,22)]:
 v,uv,f=read(i);w,uw,g=read(j);assert v.shape==w.shape and np.array_equal(uv,uw)
 vc=v-v.mean(0);wc=w-w.mean(0);u,s,t=np.linalg.svd(vc.T@wc);rot=u@t;scale=s.sum()/(vc*vc).sum()
 translation=w.mean(0)-v.mean(0)@rot*scale
 err=np.linalg.norm(v@rot*scale+translation-w,axis=1)
 assert max(err)<1e-5
 duplicates.append({'source':i,'duplicate':j,'scale':float(scale),'row_vector_rotation':rot.tolist(),'translation':translation.tolist(),'max_position_error':float(max(err)),'uv_exact':True,'topology_exact':f==g})
textures={}
pattern=re.compile(r'(?i)^(.*)_(co|spec|gloss|nohq|normals|as)(?:\.tga)?\.png$')
for f in sorted(a.source.glob('*.png')):
 m=pattern.match(f.name);assert m,f.name
 family,kind=m.groups();family=family.lower();kind=kind.lower()
 im=Image.open(f);textures.setdefault(family,{})[kind]={'source':f.name,'size':list(im.size),'mode':im.mode,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
 if kind in ('co','nohq','normals'):
  target=a.output/'source-tga'/(f.stem+'.tga');target.parent.mkdir(exist_ok=True)
  im.convert('RGB').save(target,compression=None)
  assert np.array_equal(np.array(im.convert('RGB')),np.array(Image.open(target)))
  textures[family][kind]['tga_roundtrip_exact']=True
with ZipFile(a.archive) as z:
 entries=z.namelist();missing=[]
 for obj in a.source.glob('*.obj'):
  refs=[l.split(maxsplit=1)[1] for l in obj.read_text().splitlines() if l.startswith('mtllib ')]
  missing.extend([{'obj':obj.name,'missing_mtl':r} for r in refs if not any(Path(n).name==r for n in entries)])
report={'status':'PREPARED_REVIEW_NOT_EXPORTABLE','archive_sha256':hashlib.sha256(a.archive.read_bytes()).hexdigest(),'duplicate_evidence':duplicates,'missing_material_libraries':missing,'texture_families':textures,'no_uv':['model_17'],'rm_generated':False,'installed':False}
(a.output/'source-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('PASS source TGA roundtrips;',len(textures),'texture families;',len(duplicates),'proved duplicate pairs;',len(missing),'missing MTL files')
