"""Read-only OBJ UV / author-atlas contact sheets for the current weapon queue.
--report sources.json --output DIR. Candidate scores are review hints, not bindings.
"""
import argparse,hashlib,json,re
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
report=json.loads(a.report.read_text());results={}
for source,row in report['sources'].items():
 audit=row.get('audit',{});unresolved=set(audit.get('unresolved_materials',[]))
 if not unresolved:continue
 build=Path(row['build']);root=build/'source';tag=hashlib.sha256(source.encode()).hexdigest()[:10];out=a.output/tag;out.mkdir(exist_ok=True)
 library=set(audit.get('material_library',[]));paths=[f for f in root.rglob('*') if f.is_file() and f.stem in library and f.suffix.lower() in ('.png','.tga','.dds','.jpg','.jpeg')]
 unique={}
 for f in paths:
  if f.stem not in unique or f.suffix.lower()=='.png':unique[f.stem]=f
 atlases=[]
 for name,path in unique.items():
  try:
   im=Image.open(path).convert('RGB').resize((256,256));rgb=np.asarray(im);corners=np.concatenate((rgb[:4].reshape(-1,3),rgb[-4:].reshape(-1,3),rgb[:,:4].reshape(-1,3),rgb[:,-4:].reshape(-1,3)))
   colors,counts=np.unique(corners,axis=0,return_counts=True);background=colors[counts.argmax()].astype(float)
   active=np.max(np.abs(rgb.astype(float)-background),axis=2)>12
   atlases.append((name,path,im,active))
  except Exception as e:print('IMAGE_ERROR',path,e,flush=True)
 entries=[]
 for obj in audit.get('objects',[]):
  if obj['object'] not in unresolved:continue
  source_file=obj.get('source_file')
  if not source_file or Path(source_file).suffix.lower()!='.obj':continue
  path=root/source_file
  if not path.exists():continue
  uvs=[];faces=[]
  for line in path.read_text(errors='replace').splitlines():
   fields=line.split()
   if not fields:continue
   if fields[0]=='vt':uvs.append(tuple(map(float,fields[1:3])))
   elif fields[0]=='f':
    ids=[]
    for token in fields[1:]:
     parts=token.split('/')
     if len(parts)<2 or not parts[1]:break
     i=int(parts[1]);ids.append(i-1 if i>0 else len(uvs)+i)
    if len(ids)==len(fields)-1:faces.append(ids)
  mask=Image.new('1',(256,256));draw=ImageDraw.Draw(mask);lines=[];outside=0
  for face in faces:
   coords=[uvs[i] for i in face]
   if any(u<-.001 or u>1.001 or v<-.001 or v>1.001 for u,v in coords):outside+=1;continue
   xy=[(round(u*255),round((1-v)*255)) for u,v in coords];draw.polygon(xy,fill=1);lines.append(xy)
  occupied=np.asarray(mask,dtype=bool);count=int(occupied.sum());rank=[]
  for name,imagepath,im,active in atlases:
   rank.append({'atlas':name,'image':str(imagepath),'occupied_nonbackground_fraction':float(active[occupied].mean()) if count else None})
  rank.sort(key=lambda r:r['occupied_nonbackground_fraction'] or 0,reverse=True)
  sheet=Image.new('RGB',(min(4,max(1,len(atlases)))*280,((max(1,len(atlases))+3)//4)*305),(40,40,40));sd=ImageDraw.Draw(sheet)
  for i,r in enumerate(rank):
   im=next(t[2] for t in atlases if t[0]==r['atlas']).copy();overlay=ImageDraw.Draw(im)
   for xy in lines:overlay.line(xy+[xy[0]],fill=(0,255,120),width=1)
   x=(i%4)*280;y=(i//4)*305;sheet.paste(im,(x,y));sd.text((x,y+258),r['atlas'][:38],fill='white');sd.text((x,y+273),str(round(r['occupied_nonbackground_fraction'] or 0,3)),fill='white')
  filename=re.sub('[^A-Za-z0-9_-]','_',obj['object'])+'.png';sheet.save(out/filename)
  entries.append({'object':obj['object'],'source_file':source_file,'uv_pixels':count,'outside_01_faces':outside,'rank':rank,'sheet':str(out/filename),'status':'REVIEW_ONLY'})
 results[source]={'objects':entries,'atlas_count':len(atlases)}
 print(source,len(entries),'meshes',len(atlases),'atlases',flush=True)
(a.output/'atlas-review.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
