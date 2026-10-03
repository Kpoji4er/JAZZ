"""Blender read-only source audit: --source OBJ --output JSON.
Measures angular change when authored corner normals are removed. No asset writes.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import clear_custom_normals
p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=a.source)
rows=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH':continue
 m=o.data;before=np.array([n.vector[:] for n in m.corner_normals]);had=m.has_custom_normals
 clear_custom_normals(o)
 after=np.array([n.vector[:] for n in m.corner_normals]);assert before.shape==after.shape
 angles=np.degrees(np.arccos(np.clip((before*after).sum(axis=1),-1,1)))
 rows.append({'object':o.name,'authored_custom_normals':had,'corners':len(angles),'angle_mean':float(angles.mean()),'angle_p95':float(np.percentile(angles,95)),'over_10_degrees_fraction':float((angles>10).mean())})
a.output.write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
