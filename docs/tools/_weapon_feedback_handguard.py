"""Fit M16 RIS forward to standard handguard front; receiver end stays fixed.
Blender --blend FILE --output DIR --game-root DIR. No installed writes.
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
bpy.ops.wm.open_mainfile(filepath=str(a.blend),use_scripts=False)
name='M16R_M16A4_HandguardRIS';o=bpy.data.objects[name]
rear=max(v.co.y for v in o.data.vertices);front=min(v.co.y for v in o.data.vertices)
target=min(v.co.y for v in bpy.data.objects['M16R_M16A4_Handguard'].data.vertices)
# Whole assembly preserves the original relative attachment layout and UV.
factor=(rear-target)/(rear-front)
assert 1<factor<1.2,(front,target,factor)
for v in o.data.vertices:v.co.y=rear+(v.co.y-rear)*factor
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
(out/'repair.json').write_text(json.dumps({'front_before':front,'front_after':target,'rear_preserved':rear,'length_factor':factor,'barrel_unchanged':True}))
