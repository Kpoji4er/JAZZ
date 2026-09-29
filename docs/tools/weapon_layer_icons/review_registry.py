"""Compare photographed full builds to composed layers, optionally fit draw order.

Optimizes one consistent order per weapon across all native references; never
changes geometry or fabricates hidden surfaces. Outputs quantitative diagnostics
and side-by-side default/worst reference sheets for visual review.
"""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from process_live import extract
from icon_layout import colorize,fit,ROOT

def main():
 p=argparse.ArgumentParser(__doc__);p.add_argument('--library',type=Path,required=True);p.add_argument('--captures',type=Path,nargs='+',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--optimize',action='store_true');a=p.parse_args()
 registry=json.loads((a.library/'registry.json').read_text(encoding='utf-8'));a.output.mkdir(parents=True,exist_ok=True)
 cache_path=a.output/'order-cache.json';cache=json.loads(cache_path.read_text()) if cache_path.exists() else {}
 tone_path=ROOT/'docs/design/weapon-layer-icons/live/layer-color-profiles.json'
 tones=json.loads(tone_path.read_text(encoding='utf-8'))
 recipe=hashlib.sha256(Path(__file__).read_bytes()+tone_path.read_bytes()).hexdigest()
 rows={}
 for directory in a.captures:
  receipt=json.loads((directory/'capture-report.json').read_text(encoding='utf-8-sig'))
  for row in receipt['rows']:
   if row['weapon'] in registry['weapons'] and row['status']=='captured' and not row.get('layer') and row.get('layer_graph'):
    if row.get('camera_distance',1500)!=registry['weapons'][row['weapon']].get('camera_distance',1500):continue
    rows.setdefault(row['weapon'],[]).append((directory,row))
 reports=[]
 for weapon,refs in rows.items():
  ids={hashlib.sha256(d['signature'].encode()).hexdigest()[:20] for _,r in refs for d in r['layer_graph'] if d['entity']}
  if not ids<=registry['layers'].keys():continue
  stamp=hashlib.sha256((recipe+str(a.optimize)+str([(str(d),r['image'],(d/r['image']).stat().st_mtime_ns) for d,r in refs])+str([(i,(a.library/'layers'/(i+'.png')).stat().st_mtime_ns if registry['layers'][i]['image'] else 0) for i in sorted(ids)])).encode()).hexdigest()
  cached=cache.get(weapon,{})
  if cached.get('stamp')==stamp and (a.output/(weapon+'.png')).exists():
   if a.optimize:
    for z,ident in enumerate(cached['order']):registry['layers'][ident]['z']=z
   reports.append(cached['report']);continue
  images={i:Image.open(a.library/'layers'/(i+'.png')).convert('RGBA').resize((324,165),Image.Resampling.LANCZOS) if registry['layers'][i]['image'] else Image.new('RGBA',(324,165)) for i in ids}
  references=[]
  for directory,row in refs:
   raw,_,_=extract(directory,row);reference=colorize(raw,weapon,profiles=tones).resize((324,165),Image.Resampling.LANCZOS)
   arr=np.asarray(reference,dtype=np.float32);mask=arr[...,3]>16
   premul=arr.copy();premul[...,:3]*=arr[...,3:4]/255
   references.append((row,reference,premul,mask,{hashlib.sha256(d['signature'].encode()).hexdigest()[:20] for d in row['layer_graph'] if d['entity']}))
  def compose(order,present):
   canvas=Image.new('RGBA',(324,165))
   for ident in order:
    if ident in present:canvas.alpha_composite(images[ident])
   return canvas
  def scores(order,indices=None):
   values=[]
   for index in range(len(references)) if indices is None else indices:
    row,ref,target,mask,present=references[index]
    arr=np.asarray(compose(order,present),dtype=np.float32).copy();arr[...,:3]*=arr[...,3:4]/255
    values.append(float(np.abs(arr-target)[mask].mean()) if mask.any() else 0)
   return values
  order=sorted(ids,key=lambda i:(registry['layers'][i]['z'],i));before=scores(order);best=sum(before)
  if a.optimize:
   current=before.copy()
   def overlaps(left,right):
    x=registry['layers'][left]['bounds'];y=registry['layers'][right]['bounds']
    return x and y and max(x[0],y[0])<min(x[2],y[2]) and max(x[1],y[1])<min(x[3],y[3])
   # Folded and unfolded stocks may need different depths. Move individual
   # native layers only across overlapping co-occurring parts, and never trade
   # a markedly worse reference for an improvement in the arsenal average.
   for _ in range(3):
    changed=False
    for ident in list(order):
     affected=[i for i,r in enumerate(references) if ident in r[4]]
     partners={other for i in affected for other in references[i][4] if other!=ident and overlaps(ident,other)}
     others=[i for i in order if i!=ident]
     positions=sorted({position for other in partners for position in (others.index(other),others.index(other)+1)})
     for target in positions:
      trial=others.copy();trial.insert(target,ident);values=scores(trial,affected)
      if sum(values)<sum(current[i] for i in affected)-.001 and all(v<=current[i]+.02 and v<=before[i]+.05 for i,v in zip(affected,values)):
       order=trial;changed=True
       for i,value in zip(affected,values):current[i]=value
    if not changed:break
   for z,ident in enumerate(order):registry['layers'][ident]['z']=z
  after=scores(order);worst=max(range(len(after)),key=after.__getitem__)
  selected=sorted({0,worst});sheet=Image.new('RGB',(680,len(selected)*210),(38,42,46));draw=ImageDraw.Draw(sheet)
  for y,index in enumerate(selected):
   row,ref,_,_,present=references[index]
   left=fit(ref,(324,165));right=fit(compose(order,present),(324,165))
   sheet.paste(left,(8,y*210+28),left);sheet.paste(right,(344,y*210+28),right)
   draw.text((8,y*210+4),weapon+' '+row['label']+' | native / layers',fill='white')
  sheet.save(a.output/(weapon+'.png'))
  reports.append({'weapon':weapon,'references':len(refs),'mean_before':round(float(np.mean(before)),3),'mean_after':round(float(np.mean(after)),3),'worst':round(after[worst],3),'worst_label':references[worst][0]['label']})
  cache[weapon]={'stamp':stamp,'order':order,'report':reports[-1]}
  cache_path.write_text(json.dumps(cache,indent=2),encoding='utf-8')
 if a.optimize:(a.library/'registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')
 (a.output/'report.json').write_text(json.dumps({'level':'offline raster comparison; human visual review required','weapons':reports},indent=2),encoding='utf-8')
 print(json.dumps({'weapons':len(reports),'worst':sorted(reports,key=lambda r:r['worst'],reverse=True)[:10]}))

if __name__=='__main__':main()
