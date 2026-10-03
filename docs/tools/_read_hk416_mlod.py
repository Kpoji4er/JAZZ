"""Read the editable first P3DM LOD and its named selections, without normals import.
--input model.p3d --output model.json. Format: Bohemia P3D File Format - MLOD.
"""
import argparse,json,struct
from pathlib import Path
def read(path, *, audit_normals=False):
 data=path.read_bytes();offset=0
 def take(fmt):
  nonlocal offset
  values=struct.unpack_from('<'+fmt,data,offset);offset+=struct.calcsize('<'+fmt);return values
 def string():
  nonlocal offset
  end=data.index(b'\0',offset);s=data[offset:end].decode('utf-8',errors='replace');offset=end+1;return s
 assert data[:4]==b'MLOD';offset=4;version,nlod=take('II')
 assert data[offset:offset+4]==b'P3DM';offset+=4
 major,minor,nv,nn,nf,flags=take('6I');assert max(nv,nn,nf)<1000000
 vertices=[take('3fI')[:3] for _ in range(nv)]
 if audit_normals:normals=[take('3f') for _ in range(nn)]
 else:offset+=nn*12
 faces=[]
 for _ in range(nf):
  count,=take('I');assert count in (3,4),count
  corners=[take('IIff') for _ in range(4)];flag,=take('I');texture=string();material=string()
  faces.append({'vertices':[c[0] for c in corners[:count]],'uv':[[c[2],1-c[3]] for c in corners[:count]],'texture':texture,'material':material,'flags':flag})
  if audit_normals:faces[-1]['audit_normals']=[normals[c[1]] for c in corners[:count]]
 assert data[offset:offset+4]==b'TAGG',data[offset:offset+4];offset+=4;selections={};tags=[];sharp_edges=[]
 while True:
  active,=take('B');name=string();size,=take('I');payload=data[offset:offset+size];offset+=size
  if name=='#EndOfFile#':break
  if name=='#SharpEdges#':
   assert size%8==0
   sharp_edges=list(struct.iter_unpack('<II',payload))
  if not name.startswith('#') and size==nv+nf:
   selections[name]={'vertices':[i for i,v in enumerate(payload[:nv]) if v],'faces':[i for i,v in enumerate(payload[nv:]) if v]}
  tags.append({'name':name,'size':size,'active':active})
 resolution,=take('f')
 return {'source':path.name,'version':version,'lod_count':nlod,'resolution':resolution,'vertices':vertices,'faces':faces,'selections':selections,'tags':tags,'sharp_edges':sharp_edges}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=read(a.input);a.output.write_text(json.dumps(r),encoding='utf-8');print(len(r['vertices']),'vertices;',len(r['faces']),'faces;',len(r['selections']),'selections');print(sorted({f['texture'] for f in r['faces']}));print(list(r['selections']))
