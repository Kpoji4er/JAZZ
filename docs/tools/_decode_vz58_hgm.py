"""Read static VZ58 HGM v14 for offline QA, including the post-sphere float.
The older HgmViewer schema omits this v14 field and misaligns its second mesh.
No runtime assets are modified. --input mesh.hgm --output decoded.json
"""
import argparse,json,struct
from pathlib import Path

def decode(path):
 data=path.read_bytes();offset=0;keys=[]
 def take(fmt):
  nonlocal offset
  values=struct.unpack_from('<'+fmt,data,offset);offset+=struct.calcsize('<'+fmt)
  return values[0] if len(values)==1 else list(values)
 def string():
  nonlocal offset
  size=take('I');assert size<4096
  value=data[offset:offset+size].decode('ascii').rstrip('\0');offset+=size;return value
 assert data[:4]==b'hsmh';offset=4;version=take('H');assert version==14,version
 take('H');bbox=take('6f');n=take('I');assert 0<n<32;meshes=[]
 for _ in range(n):
  mat=take('I');take('2I');nv=take('I');ni=take('I');assert nv<65536 and ni%3==0
  vt=take('B');assert vt in (0,2)
  if vt==2:string()
  fields=[];count=take('I');assert count<32
  for j in range(count):
   marker=take('B');assert marker in (1,2),marker
   if marker==2:key=string();keys.append(key)
   else:key=keys[take('I')]
   take('I');fmt=string();take('I');pos=take('I');kind=take('B');fields.append((key,fmt,pos,kind))
  take('I');stride=take('I');assert 6<=stride<=128;assert take('B')==1
  field=next(v for v in fields if v[0]=='pos');assert field[1]=='fmt_sint16_c3'
  points=[list(struct.unpack_from('<3h',data,offset+i*stride+field[2])) for i in range(nv)];offset+=nv*stride
  assert take('B')==1;faces=[take('3H') for i in range(ni//3)];assert all(0<=i<nv for f in faces for i in f)
  b=take('6f');sphere=take('4f');scale_field=take('f');assert scale_field==1.0,scale_field
  # v14 static positions share the entity quantization frame across materials.
  scale=max(1,max(abs(bbox[i+3]-bbox[i]) for i in range(3))/2)
  points=[[v/32767*scale for v in p] for p in points]
  meshes.append({'vertices':points,'faces':faces,'bbox':bbox,'submesh_bounds':b,'material_index':mat})
 # The remaining static trailer is deliberately not interpreted as an armature.
 return {'source':path.name,'version':version,'bbox':bbox,'meshes':meshes,'trailer_bytes':len(data)-offset}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=decode(a.input);a.output.write_text(json.dumps(d),encoding='utf-8');print(a.input.name,len(d['meshes']),'meshes',sum(len(m['faces']) for m in d['meshes']),'triangles')
