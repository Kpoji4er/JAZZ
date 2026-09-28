"""Verify installed material transaction hashes, DDS layout and normal amplitude.

--install DIR: directory produced by _install_vz58_r4_materials.py.
Read-only; writes audit.json next to the install report.
"""
import argparse,hashlib,io,json,struct
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--install',type=Path,required=True);a=p.parse_args()
report=json.loads((a.install/'install-report.json').read_text());assert report['applied']
def read(path):
 raw=bytearray(path.read_bytes())
 if raw[84:88]==b'DX10':
  fmt=struct.unpack_from('<I',raw,128)[0];struct.pack_into('<I',raw,128,{72:71,78:77,99:98}.get(fmt,fmt))
 return np.asarray(Image.open(io.BytesIO(raw)).convert('RGB')).astype(np.float32)
checks=[]
for entry in report['files']:
 rel=Path(entry['path']);current=ROOT.parent/rel;old=a.install/'backup'/rel
 assert hashlib.sha256(current.read_bytes()).hexdigest()==entry['after'],str(rel)
 assert hashlib.sha256(old.read_bytes()).hexdigest()==entry['before'],str(rel)
 check={'path':str(rel),'hashes':'PASS'}
 if current.suffix=='.dds':
  header=current.read_bytes();prior=old.read_bytes()
  assert header[12:20]==prior[12:20],('size',rel)
  assert header[84:88]==prior[84:88] and header[128:132]==prior[128:132],('encoding',rel)
  if 'Fallbacks' not in str(rel) and '_Norm' in current.name:
   before=read(old)[:,:,:2]/127.5-1;after=read(current)[:,:,:2]/127.5-1
   ratio=float(np.sqrt(np.mean(after**2))/max(np.sqrt(np.mean(before**2)),1e-6))
   assert ratio<.65,('normal amplitude not reduced',rel,ratio)
   check['normal_rms_ratio']=ratio
 if current.suffix=='.png':
  im=Image.open(current);assert im.mode=='RGBA' and im.size==(324,165)
 checks.append(check)
out={'pass':True,'files':checks,'runtime_verified':False}
(a.install/'audit.json').write_text(json.dumps(out,indent=2));print('PASS',len(checks),'installed files; runtime pending')
