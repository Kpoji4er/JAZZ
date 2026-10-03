"""Stage the approved small VZ58 roughness / M14 metallic adjustments.

--assets PATH --game-root PATH --build NEW_DIR. Numerical RM processing only:
preserves author Base/Normal and unrelated channels. Apply with _reimport_weapon_rm.
"""
import argparse,io,json,shutil,struct
from pathlib import Path
import numpy as np
from PIL import Image
from _reimport_weapon_rm import sha,header,pixels,run_converter

p=argparse.ArgumentParser(description=__doc__)
for k in ('assets','game-root','build'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();a.build.mkdir(parents=True,exist_ok=False)
tex=a.assets/'Entities/Textures';exe=a.game_root/'ModTools/hgimgcvt.exe'
def color(name):
 raw=bytearray((tex/name).read_bytes())
 if raw[84:88]==b'DX10':
  dx=struct.unpack_from('<I',raw,128)[0]
  if dx in (72,99):struct.pack_into('<I',raw,128,{72:71,99:98}[dx])
 return np.array(Image.open(io.BytesIO(raw)).convert('RGB')).astype(np.float32)

report={'guards':{},'maps':[],'files':[],'applied':False,'converter_sha256':sha(exe)}
names=[('JAZZ_VZ58_12_RM.dds','JAZZ_VZ58_11_Base.dds',0,6),
       ('JAZZ_VZ58_27_RM.dds','JAZZ_VZ58_26_Base.dds',0,6),
       ('JAZZ_M14_RM.dds','JAZZ_M14_Base.dds',2,20)]
for name,base,channel,amount in names:
 old=pixels(tex/name);bc=color(base);new=old.copy();meta=header(tex/name)
 if channel==0:
  mask=(bc[:,:,0]>1.25*bc[:,:,1])&(bc[:,:,0]>1.25*bc[:,:,2])&(old[:,:,2]<8)
 else:
  # The source atlas separates brown wood/brass from neutral gunmetal.
  # Restrict the modest boost to neutral occupied pixels, not the wood UVs.
  hi=bc.max(axis=2);lo=bc.min(axis=2)
  mask=(hi>6)&((hi-lo)<=hi*.12)
 new[:,:,channel]=np.where(mask,np.minimum(255,old[:,:,channel].astype(int)+amount),old[:,:,channel])
 new[:,:,1]=new[:,:,0]
 Image.fromarray((mask*255).astype('uint8')).save(a.build/(name+'.mask.png'))
 tga=a.build/(name+'.tga');Image.fromarray(new).save(tga,compression=None)
 dest=a.build/'staged/Entities/Textures'/name;dest.parent.mkdir(parents=True,exist_ok=True)
 run_converter(exe,tga,dest,'--compression','BC7' if meta['dxgi']==98 else 'BC1','--alpha','0','--mips',str(meta['mips']))
 raw=bytearray(dest.read_bytes())
 if raw[84:88]==b'DX10' and struct.unpack_from('<I',raw,128)[0]==99:
  struct.pack_into('<I',raw,128,98);dest.write_bytes(raw)
 header(dest);out=pixels(dest);error=np.abs(out.astype(int)-new.astype(int))
 assert error.mean()<3 and np.percentile(error,99)<13,(name,error.mean())
 fb=dest.parent/'Fallbacks'/name;fb.parent.mkdir(exist_ok=True)
 run_converter(exe,dest,fb,'--truncate','64');header(fb)
 report['maps'].append({'name':name,'channel':channel,'increment':amount,'mask_fraction':float(mask.mean()),
  'compression_mean_error':error.mean(axis=(0,1)).tolist(),
  'masked_before_median':float(np.median(old[:,:,channel][mask])),
  'masked_after_median':float(np.median(out[:,:,channel][mask]))})
 for f in (dest,fb):
  rel=f.relative_to(a.build/'staged');original=a.assets/rel
  backup=a.build/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,backup)
  report['files'].append({'path':str(rel),'before':sha(original),'after':sha(f)})
changed={f['path'] for f in report['files']}
for folder in ('Entities/Textures','Entities/Textures/Fallbacks','Entities/Materials','Entities/Meshes'):
 for f in (a.assets/folder).iterdir():
  if f.is_file() and f.name.startswith(('JAZZ_VZ58','JAZZ_M14')) and str(f.relative_to(a.assets)) not in changed:
   report['guards'][str(f.relative_to(a.assets))]=sha(f)
(a.build/'manifest.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report['maps'],indent=2))
