"""Stage source-byte AEK BaseColor repair; --build NEW_DIR --weapons DIR --game-root DIR.
Apply with _reimport_weapon_rm.py after closing JA3. All non-Base assets are guarded.
"""
import argparse,io,json,shutil,struct,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
from _integrate_sr3m import ASSETS
from _reimport_weapon_rm import sha
from _audit_recent_weapon_textures import dds

p=argparse.ArgumentParser()
for k in ('build','weapons','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();a.build.mkdir(parents=True,exist_ok=False)
r={'kind':'author-textures','files':[],'maps':[],'guards':{},'applied':False}
sets=[(2,'23_AEK_971_Assault_Rifle','aektexture_blue.001','JAZZ_AEK971_Blue'),(5,'23_AEK_971_Assault_Rifle','aektexture_red.002','JAZZ_AEK971_Red'),(8,'22_AEK_-_973S','31_AEK','JAZZ_AEK973S_Main')]
for folder in ('Entities','Entities/Meshes','Entities/Materials','Entities/Textures','Entities/Textures/Fallbacks'):
 for f in (ASSETS/folder).glob('JAZZ_AEK*'):
  if f.is_file() and not f.name.endswith('_Base.dds'):r['guards'][str(f.relative_to(ASSETS))]=sha(f)
for idx,folder,prefix,material in sets:
 name=f'JAZZ_AEK_{idx}_Base.dds';old=ASSETS/'Entities/Textures'/name;meta=dds(old)
 source=a.weapons/'_batch_jazz_import'/folder/'source'/(prefix+'_BaseColor.png')
 im=Image.open(source).convert('RGB').resize((meta['width'],meta['height']),Image.Resampling.LANCZOS)
 tga=a.build/(material+'_Base.tga');im.save(tga,compression=None)
 assert np.array_equal(np.array(im),np.array(Image.open(tga)))
 full=a.build/'staged/Entities/Textures'/name;full.parent.mkdir(parents=True,exist_ok=True)
 cvt=str(a.game_root/'ModTools/hgimgcvt.exe')
 subprocess.run([cvt,str(tga),str(full),'--compression','BC1','--alpha','0','--mips',str(meta['mips'])],check=True,capture_output=True)
 data=bytearray(full.read_bytes());assert data[84:88]==b'DX10';struct.pack_into('<I',data,128,72);full.write_bytes(data)
 struct.pack_into('<I',data,128,71)
 error=float(np.abs(np.array(Image.open(io.BytesIO(data)).convert('RGB')).astype(float)-np.array(im)).mean());assert error<8
 fallback=full.parent/'Fallbacks'/name;fallback.parent.mkdir(exist_ok=True)
 subprocess.run([cvt,str(full),str(fallback),'--truncate','64'],check=True,capture_output=True)
 for f in (full,fallback):
  assert dds(f)['complete_mips'];rel=f.relative_to(a.build/'staged');backup=a.build/'backup'/rel;backup.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ASSETS/rel,backup)
  r['files'].append({'path':str(rel),'before':sha(ASSETS/rel),'after':sha(f)})
 r['maps'].append({'name':name,'source':str(source),'source_sha':sha(source),'mean_compression_error':error,'source_tga_exact':True})
(a.build/'manifest.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('PASS source bytes preserved;',len(r['files']),'DDS staged;',len(r['guards']),'guards')
