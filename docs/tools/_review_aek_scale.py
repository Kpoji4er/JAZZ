"""Blender: --build DIR. Save each unfolded AEK separately for AK74M scale overlay."""
import argparse,sys
from pathlib import Path
import bpy
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for variant in ('971','973S'):
 bpy.ops.wm.open_mainfile(filepath=str(a.build/'rigged/AEK_JA3.blend'),use_scripts=False)
 keep={'JAZZ_AEK'+variant,'JAZZ_AEK'+variant+'_Magazine','JAZZ_AEK'+variant+'_Stock'}
 for o in list(bpy.data.objects):
  if o.type=='MESH' and o.name not in keep:bpy.data.objects.remove(o,do_unlink=True)
 folder=a.build/'scale-review';folder.mkdir(exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(folder/('AEK'+variant+'.blend')))
