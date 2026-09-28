"""Patch only four bone indices/weights in existing v12 HGM from reviewed fields.
--input HGM --decoded JSON --weights JSON --output HGM. No geometry/UV changes.
"""
import argparse,json,struct,hashlib
from pathlib import Path
p=argparse.ArgumentParser()
for k in ('input','decoded','weights','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();original=a.input.read_bytes();data=bytearray(original);offset=0;keys=[]
def take(fmt):
 global offset
 v=struct.unpack_from('<'+fmt,data,offset);offset+=struct.calcsize('<'+fmt);return v[0] if len(v)==1 else v
def string():
 global offset
 n=take('I');assert n<4096;s=bytes(data[offset:offset+n]).decode('ascii').rstrip('\0');offset+=n;return s
assert data[:4]==b'hsmh';offset=4;assert take('H')==12;offset=32;count=take('I')
decoded=json.loads(a.decoded.read_text());fields=json.loads(a.weights.read_text());assert len(fields)==count
names={b['name']:i for i,b in enumerate(decoded['bones'])};allowed=set();changed=0
for mi in range(count):
 take('I');take('2I');nv=take('I');ni=take('I');vt=take('B');assert vt in (0,2)
 if vt==2:string()
 descriptors={}
 for _ in range(take('I')):
  marker=take('B');assert marker in (1,2)
  if marker==2:key=string();keys.append(key)
  else:key=keys[take('I')]
  take('I');fmt=string();take('I');pos=take('I');take('B');descriptors[key]=(fmt,pos)
 take('I');stride=take('I');assert take('B')==1
 assert descriptors['bi'][0]=='fmt_uint8_c4' and descriptors['bw'][0]=='fmt_unorm8_c4',descriptors
 assert nv==len(fields[mi])==len(decoded['meshes'][mi]['vertices'])
 for i,w in enumerate(fields[mi]):
  if w is None:continue
  pairs=sorted(w.items(),key=lambda x:-x[1])[:4];assert all(n in names for n,v in pairs)
  total=sum(v for n,v in pairs);raw=[v/total*255 for n,v in pairs];quant=[int(v) for v in raw]
  for j in sorted(range(len(raw)),key=lambda j:raw[j]-quant[j],reverse=True)[:255-sum(quant)]:quant[j]+=1
  ids=[names[n] for n,v in pairs];ids+=[0]*(4-len(ids));quant+=[0]*(4-len(quant));assert sum(quant)==255
  for key,values in (('bi',ids),('bw',quant)):
   start=offset+i*stride+descriptors[key][1];allowed.update(range(start,start+4));data[start:start+4]=bytes(values)
  changed+=1
 offset+=nv*stride;assert take('B')==1;offset+=ni*2+40
assert changed>100
assert len(data)==len(original) and all(i in allowed for i,(x,y) in enumerate(zip(original,data)) if x!=y)
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(data)
a.output.with_suffix('.skin-audit.json').write_text(json.dumps({'vertices_rebound':changed,'only_bi_bw_changed':True,'source_sha256':hashlib.sha256(original).hexdigest(),'output_sha256':hashlib.sha256(data).hexdigest(),'runtime':'NOT_RUN'}))
