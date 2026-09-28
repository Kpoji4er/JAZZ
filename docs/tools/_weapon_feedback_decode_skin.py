"""Decode v14 skin using the legacy v12 reader through a temporary layout adapter.
--input HGM --reader EXE --output JSON. Original binary is never changed.
v14 adds one float after each mesh sphere; remove only that for reader input.
"""
import argparse,json,struct,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser()
for k in ('input','reader','output'):p.add_argument('--'+k,type=Path,required=True)
p.add_argument('--skeleton-reference',type=Path,help='Decoded native Male garment with canonical bone order')
a=p.parse_args();raw=a.input.read_bytes();data=bytearray(raw);version=struct.unpack_from('<H',data,4)[0];offset=32;keys=[];removals=[]
def take(fmt):
 global offset
 v=struct.unpack_from('<'+fmt,data,offset);offset+=struct.calcsize('<'+fmt);return v[0] if len(v)==1 else v
def string():
 global offset
 n=take('I');assert n<4096;s=bytes(data[offset:offset+n]).decode('ascii').rstrip('\0');offset+=n;return s
if version==14:
 for _ in range(take('I')):
  take('I');take('2I');nv=take('I');ni=take('I');vt=take('B');assert vt in (0,2)
  if vt==2:string()
  for _ in range(take('I')):
   marker=take('B');assert marker in (1,2)
   if marker==2:keys.append(string())
   else:assert take('I')<len(keys)
   take('I');string();take('I');take('I');take('B')
  take('I');stride=take('I');assert take('B')==1;offset+=nv*stride;assert take('B')==1;offset+=ni*2+40
  removals.append(offset);assert take('f')==1.0
 # v14 stores a reference to Male.hgskel, not the old inline bone names.
 assert a.skeleton_reference and raw[offset]==1
 bone_count=struct.unpack_from('<I',raw,offset+9)[0]
 assert raw[offset+13]==2
 length=struct.unpack_from('<I',raw,offset+14)[0]
 skeleton_path=raw[offset+18:offset+18+length].decode('ascii').rstrip('\0')
 assert skeleton_path=='Skeletons/Male_mesh.hgskel',skeleton_path
 canonical=json.loads(a.skeleton_reference.read_text())['bones'];assert len(canonical)==bone_count
 for pos in reversed(removals):del data[pos:pos+4]
 data[offset-4*len(removals)]=0
 struct.pack_into('<H',data,4,12)
assert version in (12,14)
a.output.parent.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory(prefix='jazz-skin-decode-') as tmp:
 path=Path(tmp)/a.input.name;path.write_bytes(data)
 subprocess.run([str(a.reader),str(path),str(a.output)],check=True)
d=json.loads(a.output.read_text());d['version']=version;d['source']=a.input.name
if version==14:d['bones']=canonical;d['skeleton_reference']=skeleton_path
assert d['bones'],'Skin trailer missing'
a.output.write_text(json.dumps(d));print('DECODED',a.input.name,'bones',len(d['bones']))
