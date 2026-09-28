"""Offline material UV-orientation diagnostic for AK103; no installation/export.
Blender --python ... -- --source <rig blend> --out <directory>.
Compares original UVs against a vertical flip within each native atlas tile.
"""
import argparse,sys,math,json
from pathlib import Path
import bpy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _optimize_ak103_mesh import render_pairs
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source),use_scripts=False)
objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('AKR_AK103')]
before={o.name:o.data.copy() for o in objects}
for o in objects:
 grid=4 if o.name=='AKR_AK103' else 2 if o.name=='AKR_AK103_Handguard' else 1
 uv=o.data.uv_layers.active.data
 for poly in o.data.polygons:
  tile=min(grid-1,int(sum(uv[i].uv.y for i in poly.loop_indices)/len(poly.loop_indices)*grid))
  for i in poly.loop_indices:uv[i].uv.y=(2*tile+1)/grid-uv[i].uv.y
render_pairs(a.out,objects,before)
