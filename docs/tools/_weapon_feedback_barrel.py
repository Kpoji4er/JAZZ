"""Extend M16 barrel's hidden rear cylinder to receiver; preserve muzzle/UV.
Blender --blend FILE --output DIR --game-root DIR. Candidate exports only.
"""
import argparse,sys,json
from pathlib import Path
import bpy
from mathutils import Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh
p=argparse.ArgumentParser()
for key in ('blend','output','game-root'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);hge=load_hge(a.game_root)
for name in ('M16R_M16A4_Barrel','M16R_M16A4_BarrelShort'):
 bpy.ops.wm.open_mainfile(filepath=str(a.blend),use_scripts=False);o=bpy.data.objects[name]
 # Cylinder side faces are the only faces spanning over 50 mm axially.
 faces=[f for f in o.data.polygons if max(o.data.vertices[i].co.y for i in f.vertices)-min(o.data.vertices[i].co.y for i in f.vertices)>.05]
 ids={i for f in faces for i in f.vertices};assert ids
 rear=max(o.data.vertices[i].co.y for i in ids);tip=min(o.data.vertices[i].co.y for i in ids)
 selected=[o.data.vertices[i] for i in ids if abs(o.data.vertices[i].co.y-rear)<1e-5]
 assert 6<=len(selected)<=48,(name,len(selected))
 for v in selected:v.co.y=0
 assert min(v.co.y for v in o.data.vertices)==tip
 for im in bpy.data.images:
  if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
 for mat in o.data.materials:
  for prop in hge.MATERIAL_PROPERTIES:
   if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):mat[prop.id]=bpy.path.abspath(mat[prop.id])
 keep={o,*o.children}
 if o.parent:keep.add(o.parent)
 for other in list(bpy.data.objects):
  if other not in keep:bpy.data.objects.remove(other,do_unlink=True)
 if o.parent:o.parent.matrix_world=Matrix.Identity(4)
 o.matrix_world=Matrix.Identity(4);assert not prepare_export_mesh(o)
 out=a.output/name;out.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(out/(name+'.blend')));export_fbx(hge,out/(name+'.fbx'))
 (out/'repair.json').write_text(json.dumps({'rear_before':rear,'rear_after':0,'tip_preserved':tip,'vertices_moved':len(selected)}))
