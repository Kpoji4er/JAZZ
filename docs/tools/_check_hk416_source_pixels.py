"""Blender -- --build DIR --source DIR. Compare TGA to identically resized sources.
Tests channel/gamma preservation; resizing is explicit and not byte-identical input.
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import pixels
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--source',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);r=json.loads((a.build/'build-report.json').read_text());out=[]
for name,row in r['materials'].items():
 prefix=name.lower().rsplit('_co',1)[0]
 for kind,key in [('Base','base'),('Normal','normal')]:
  source=pixels(a.source/row[key]);current=pixels(a.build/'Textures'/('HK416_'+prefix+'_'+kind+'.tga'))
  delta=float(np.max(np.abs(source[:,:,:3]-current[:,:,:3]))*255)
  assert delta<=1.01,(name,kind,delta)
  out.append({'material':name,'map':kind,'max_byte_error_after_same_resize':delta})
(a.build/'source-pixel-audit.json').write_text(json.dumps(out,indent=2));print('PASS',len(out),'CO/NM maps, same resize, no channel or gamma transform')
