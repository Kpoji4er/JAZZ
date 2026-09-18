"""CPU rest-fit candidate, preserving the original modular donor."""
import argparse,sys,json
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source))
obj=bpy.data.objects['HAV_vest'];inv=obj.matrix_world.inverted()
for v in obj.data.vertices:
    co=obj.matrix_world@v.co
    upper=max(0,min(1,(co.z-1.2)/.15))
    shoulder=max(0,min(1,(co.z-1.45)/.1))
    co.x*=1.03;co.y*=1.16
    if co.y<0:co.y-=.055*upper
    co.z-=.075-.025*shoulder
    v.co=inv@co
obj.data.update();obj['fit_status']='LegionGoon rest candidate, unrigged'
scene=bpy.context.scene
for side,loc in [('front',(1,-3,1.9)),('back',(-1,3,1.9))]:
    scene.camera.location=loc;scene.camera.rotation_euler=(Vector((0,0,1.25))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(a.output/(side+'.png'));bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'vest-fit.blend'))
(a.output/'fit.json').write_text(json.dumps({'status':'UNRIGGED_REST_CANDIDATE','body':'NPCCostumeMale_Shirt_08','scale_xy':[1.03,1.16],'offset_z_m':-.075,'upper_front_clearance_m':.055,'shoulder_lift_m':.025,'installed':False},indent=2))
