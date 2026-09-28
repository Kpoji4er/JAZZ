"""Numerical PBR tuning for the approved weapon feedback pass; staging only.

--maps DIR --output DIR --ak-native DIR --game-root DIR
Uses RGB albedo multipliers, tangent-vector strength, untouched UVs/alpha/metalness.
Creates inspection PNGs and compressed DDS/fallbacks under original resource names.
"""
import argparse,json,shutil,struct,subprocess
from pathlib import Path
import numpy as np
from PIL import Image

p=argparse.ArgumentParser()
for key in ('maps','output','ak-native','game-root'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
for src in a.maps.glob('*.png'):shutil.copy2(src,a.output/src.name)
bindings=json.loads((a.maps/'bindings.json').read_text());changes=[]
def read(entity,key):return np.array(Image.open(a.maps/(entity+'_'+key+'.png')).convert('RGBA'))
def save(entity,key,arr,details):
    dest=a.output/(entity+'_'+key+'.png');Image.fromarray(arr).save(dest)
    changes.append({'entity':entity,'map':key,'resource':Path(bindings[entity][key]).name,**details})
def strength(arr,value):
    arr=arr.copy();xyz=arr[:,:,:3].astype(float)/127.5-1
    xyz[:,:,:2]*=value;xyz[:,:,2]=np.maximum(xyz[:,:,2],.01)
    xyz/=np.maximum(np.linalg.norm(xyz,axis=2,keepdims=True),1e-8)
    arr[:,:,:3]=np.rint((xyz+1)*127.5).astype(np.uint8);return arr
# The rebased map contains compensation for the previously smooth mesh. Use
# the original authored atlas under the explicit hard joins instead.
raw=Image.open(a.ak_native/'Textures/AKR_AK103_NativeAtlas_Normal.tga').convert('RGBA')
raw=raw.resize(Image.open(a.maps/'AKR_AK103_Normal.png').size,Image.Resampling.LANCZOS)
save('AKR_AK103','Normal',strength(np.array(raw),.5),{'native_atlas':True,'tangent_strength':.5})
save('MK14EBR','Normal',strength(read('MK14EBR','Normal'),.55),{'tangent_strength':.55})
for entity,key,factor in [('JAZZ_M14','wood',.85),('JAZZ_VektorR4','metal',.88)]:
    base=read(entity,'Base');rm=read(entity,'RM');rgb=base[:,:,:3].astype(float)
    if key=='wood':
        mask=(rgb[:,:,0]>rgb[:,:,1]*1.25)&(rgb[:,:,1]>rgb[:,:,2]*1.15)&(rgb[:,:,0]>20)
        mask[base.shape[0]//2:]=False
        assert .15<mask.mean()<.25,mask.mean()
    else:mask=rm[:,:,2]>127
    changed=base.copy();changed[:,:,:3][mask]=np.rint(rgb[mask]*factor).astype(np.uint8)
    assert np.array_equal(changed[~mask],base[~mask]) and np.array_equal(changed[:,:,3],base[:,:,3])
    save(entity,'Base',changed,{'mask':key,'fraction':float(mask.mean()),'rgb_multiplier':factor,'outside_mask_unchanged':True})
tex=a.output/'dds';tex.mkdir(exist_ok=True);fallback=tex/'Fallbacks';fallback.mkdir(exist_ok=True)
for change in changes:
    key=change['map'];source=a.output/(change['entity']+'_'+key+'.png');dest=tex/change['resource']
    command=([str(a.game_root/'ModTools/AssetsProcessor/hgnvcompress.exe'),'-normal','-nocuda','-bc5',str(source),str(dest)] if key=='Normal' else
             [str(a.game_root/'ModTools/hgimgcvt.exe'),str(source),str(dest),'--compression','BC7','--profile','slow','--mips','0'])
    subprocess.run(command,check=True,capture_output=True)
    raw=bytearray(dest.read_bytes())
    if key!='Base' and raw[84:88]==b'DX10':
        fmt=struct.unpack_from('<I',raw,128)[0];struct.pack_into('<I',raw,128,{84:83,99:98}.get(fmt,fmt));dest.write_bytes(raw)
    subprocess.run([str(a.game_root/'ModTools/hgimgcvt.exe'),str(dest),str(fallback/dest.name),'--truncate','64'],check=True,capture_output=True)
    print('STAGED',change['resource'],flush=True)
(a.output/'material-report.json').write_text(json.dumps(changes,indent=2))
