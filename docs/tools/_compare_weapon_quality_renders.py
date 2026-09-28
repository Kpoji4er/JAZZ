"""Compare paired Blender diagnostic PNGs; image differences require visual review.
python ... <review-or-sweep directory> [another directory]. Writes pixel-diff.json.
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
for arg in sys.argv[1:]:
 root=Path(arg);rows=[]
 for before in sorted(root.glob('*_before.png')):
  after=before.with_name(before.name.replace('_before.png','_after.png'))
  if not after.exists():continue
  x=np.asarray(Image.open(before).convert('RGBA'),dtype=np.int16);y=np.asarray(Image.open(after).convert('RGBA'),dtype=np.int16)
  alpha=np.maximum(x[:,:,3],y[:,:,3])>8
  # Premultiply to discard undefined colour under fully transparent pixels.
  cx=x[:,:,:3]* (x[:,:,3:4]/255);cy=y[:,:,:3]*(y[:,:,3:4]/255)
  diff=np.max(np.abs(cx-cy),axis=2);coords=np.argwhere((diff>8)&alpha)
  rows.append({'view':before.name.replace('_before.png',''),'pixels':int(alpha.sum()),'rgb_gt8_pixels':int(len(coords)),'max_rgb_delta':float(diff.max()),'mean_rgb_delta_object':float(diff[alpha].mean()) if alpha.any() else 0,'alpha_gt16_pixels':int((np.abs(x[:,:,3]-y[:,:,3])>16).sum()),'changed_bbox_xy':[[int(coords[:,1].min()),int(coords[:,0].min())],[int(coords[:,1].max()),int(coords[:,0].max())]] if len(coords) else None})
 rows.sort(key=lambda r:r['rgb_gt8_pixels'],reverse=True)
 (root/'pixel-diff.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 print(root,'pairs',len(rows),'worst',json.dumps(rows[:5]))
