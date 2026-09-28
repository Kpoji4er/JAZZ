"""Stage original AK103 magazine tangent normal at reduced strength, BC5+fallback.
--source native.tga --output DIR --game-root DIR. No albedo or body edits.
"""
import argparse,subprocess,json
from pathlib import Path
import numpy as np
from PIL import Image
p=argparse.ArgumentParser()
for k in ('source','output','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
arr=np.array(Image.open(a.source).convert('RGB'));xyz=arr.astype(float)/127.5-1
xyz[:,:,:2]*=.5;xyz[:,:,2]=np.maximum(xyz[:,:,2],.01);xyz/=np.maximum(np.linalg.norm(xyz,axis=2,keepdims=True),1e-8)
png=a.output/'AKR_AK103_Magazine_Normal.png';Image.fromarray(np.rint((xyz+1)*127.5).astype(np.uint8)).save(png)
dest=a.output/'AKR_AK103_6_Norm.dds';fb=a.output/'Fallbacks';fb.mkdir(exist_ok=True)
subprocess.run([str(a.game_root/'ModTools/AssetsProcessor/hgnvcompress.exe'),'-normal','-nocuda','-bc5',str(png),str(dest)],check=True,capture_output=True)
subprocess.run([str(a.game_root/'ModTools/hgimgcvt.exe'),str(dest),str(fb/dest.name),'--truncate','64'],check=True,capture_output=True)
(a.output/'normal-report.json').write_text(json.dumps({'source':str(a.source),'strength':.5,'resource':dest.name,'dimensions':list(arr.shape[:2]),'body_untouched':True}))
