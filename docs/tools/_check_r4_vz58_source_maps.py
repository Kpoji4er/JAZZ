"""Compare installed receiver NM/RM to author PNGs. Read-only, no visual PASS.
--weapons DIR --assets DIR --output JSON
"""
import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image
from _weapon_feedback_maps import read_dds
p=argparse.ArgumentParser()
for name in ('weapons','assets','output'):p.add_argument('--'+name,type=Path,required=True)
a=p.parse_args();tex=a.assets/'Entities/Textures';out={}
for key,folder,prefix,normal,rm in [('VZ58','_vz58_jazz_20260926/source/classic','SA_vz.58_(TextureReady)_Steel_Body','JAZZ_VZ58_1_Norm.dds','JAZZ_VZ58_3_RM.dds'),('R4','_r4_jazz_20260926/source','R4_low_R4_','JAZZ_VektorR4_1_Norm.dds','JAZZ_VektorR4_4_RM.dds')]:
 d=read_dds(tex/normal,True)[:,:,:3].astype(float);h,w=d.shape[:2]
 def src(part):
  paths=list((a.weapons/folder).glob(prefix+'*'+part+'*.png'));assert len(paths)==1,paths
  return np.array(Image.open(paths[0]).convert('RGB').resize((w,h),Image.Resampling.LANCZOS)).astype(float)
 s=src('Normal');r=read_dds(tex/rm)[:,:,:3].astype(float);rough=src('Rough')[:,:,0];metal=src('Metall')[:,:,0]
 out[key]={'normal_xy_mae':np.abs(d[:,:,:2]-s[:,:,:2]).mean().item(),'normal_xy_rms_ratio':(np.sqrt(((d[:,:,:2]-127.5)**2).mean())/np.sqrt(((s[:,:,:2]-127.5)**2).mean())).item(),'roughness_mae':np.abs(r[:,:,0]-rough).mean().item(),'metallic_mae':np.abs(r[:,:,2]-metal).mean().item(),'roughness_mean':[rough.mean().item(),r[:,:,0].mean().item()],'metallic_mean':[metal.mean().item(),r[:,:,2].mean().item()]}
a.output.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
