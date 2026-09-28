import bpy,sys,json
from pathlib import Path
from mathutils import Vector
root=Path(sys.argv[sys.argv.index('--')+1]);report={}
for family in ['classic','modern']:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 meshes=[]
 for p in sorted((root/'source'/family).glob('*.obj')):
  bpy.ops.wm.obj_import(filepath=str(p),forward_axis='Y',up_axis='Z');o=bpy.context.object;o.name=p.stem
  o.color=[(.8,.3,.2,1),(.3,.7,.3,1),(.3,.4,.8,1),(.8,.7,.2,1),(.7,.3,.7,1),(.2,.7,.7,1),(.8,.5,.2,1),(.6,.6,.6,1)][len(meshes)];meshes.append(o)
 scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.light='STUDIO';scene.display.shading.color_type='OBJECT';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
 cam=bpy.data.cameras.new('Camera');cam.type='ORTHO';cam.ortho_scale=110;o=bpy.data.objects.new('Camera',cam);scene.collection.objects.link(o);scene.camera=o
 target=Vector((0,0,2));o.location=Vector((180,0,2));o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
 # Look along X, Y is image up; source muzzle +Z becomes horizontal.
 o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler();o.rotation_euler.rotate_axis('Z',1.57079632679)
 scene.render.resolution_x=1500;scene.render.resolution_y=850;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.filepath=str(root/(family+'-parts.png'));bpy.ops.render.render(write_still=True)
 bpy.ops.wm.save_as_mainfile(filepath=str(root/(family+'-inspect.blend')))
