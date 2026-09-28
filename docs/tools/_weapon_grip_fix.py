"""Blender one-item grip repair; --blend FILE --entity ID --output DIR --game-root ROOT.
--y moves the grip along the fore-end; height is measured on its bottom surface.
Stages strict-prepared geometry; installation and runtime acceptance are separate.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
from _export_m14_family_assets import load_hge,export_fbx
p=argparse.ArgumentParser()
for k in ('blend','output','game-root'):p.add_argument('--'+k,type=Path,required=True)
p.add_argument('--entity',required=True);p.add_argument('--y',type=float)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
hge=load_hge(a.game_root);bpy.ops.wm.open_mainfile(filepath=str(a.blend));obj=bpy.data.objects[a.entity]
spot=next(c for c in obj.children if c.type=='EMPTY' and c.hge_obj_settings.spot_name=='Hand_l_grip')
old=list(spot.location)
if a.y is not None:spot.location.y=a.y
hit,loc,normal,index=obj.ray_cast(Vector((spot.location.x,spot.location.y,-1)),Vector((0,0,1)))
assert hit,'No fore-end at proposed grip'
spot.location.z=loc.z-.002
issues=prepare_export_mesh(obj)
keep={obj,*obj.children}
if obj.parent:keep.add(obj.parent)
for other in list(bpy.data.objects):
 if other not in keep:bpy.data.objects.remove(other,do_unlink=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(a.entity+'.blend')))
export_fbx(hge,a.output/(a.entity+'.fbx'))
report={'entity':a.entity,'old_grip_m':old,'new_grip_m':list(spot.location),'issues':issues,'runtime':'NOT_RUN'}
(a.output/'grip-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
