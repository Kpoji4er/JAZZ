"""Check a Chainmail skin-only Base calibration against its previous bake.
--before BUILD --after BUILD --report JSON; reads Base/Color TGA, no mutations.
"""
import argparse,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
p=argparse.ArgumentParser()
for n in ('before','after','report'):p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args()
def maps(root):
 return [np.asarray(Image.open(root/('JAZZ_Chainmail_Male_'+k+'.tga')).convert('RGB')).astype(float) for k in ('Base','Color')]
old,old_mask=maps(a.before);new,mask=maps(a.after)
assert old.shape==new.shape
skin=(mask[:,:,0]>250)&(mask[:,:,1]<5)&(mask[:,:,2]<5)
# Exclude the bake margin around skin islands from armor invariance comparison.
expanded=np.asarray(Image.fromarray((skin*255).astype('uint8')).filter(ImageFilter.MaxFilter(21)))>0
armor=(~expanded)&(np.max(old,axis=2)>3)
report={'skin_before_mean':float(old[skin].mean()),'skin_after_mean':float(new[skin].mean()),
 'armor_mean_absolute_delta':float(np.abs(new[armor]-old[armor]).mean()),
 'color_mask_identical':bool(np.array_equal(mask,old_mask)),'runtime':'NOT_RUN'}
report['pass']=bool(report['color_mask_identical'] and report['skin_after_mean']>220 and report['armor_mean_absolute_delta']<1)
a.report.write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report));assert report['pass'],report
