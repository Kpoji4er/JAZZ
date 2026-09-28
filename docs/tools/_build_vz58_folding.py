"""Build VZ58V folded stock from the installed native wire stock, keeping its hinge fixed.
Blender --python this.py -- --source BLEND --build DIR --game-root DIR
"""
import argparse,sys,json,math
from pathlib import Path
import bpy
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge
from _prepare_weapon_open_surfaces import prepare_export_mesh

def folded_copy(src):
 o=src.copy();o.data=src.data.copy();o.name='JAZZ_VZ58_StockWireFolded';bpy.context.collection.objects.link(o)
 # Connectivity across UV seams is used for classification only: no mesh vertices are welded.
 vertices=o.data.vertices;parent=list(range(len(vertices)));same={}
 def find(i):
  while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
  return i
 for v in vertices:
  key=tuple(round(x,6) for x in v.co);first=same.setdefault(key,v.index);parent[find(v.index)]=find(first)
 for face in o.data.polygons:
  for i in face.vertices[1:]:parent[find(i)]=find(face.vertices[0])
 groups={}
 for v in vertices:groups.setdefault(find(v.index),[]).append(v)
 scale=.845/(42.41209411621094+42.3818244934082)
 pivot=Vector((-1.95*scale,1.82*scale,0)) # local frame: source z=-20.82, stock spot z=-19.
 transform=Matrix.Translation(pivot)@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation(-pivot)
 moved=0;stationary=0
 for group in groups.values():
  if max(v.co.y for v in group)>.1:
   for v in group:v.co=transform@v.co
   moved+=len(group)
  else:stationary+=len(group)
 assert moved and stationary
 prepare_export_mesh(o);o.hge_obj_settings.entity=o.name
 return o,{'moving_vertices':moved,'stationary_vertices':stationary,'pivot_local':list(pivot),'rotation_degrees':180}

def main():
 p=argparse.ArgumentParser()
 for k in ('source','build','game-root'):p.add_argument('--'+k,type=Path,required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.build.mkdir(parents=True,exist_ok=True);(a.build/'rigged').mkdir(exist_ok=True)
 bpy.ops.wm.open_mainfile(filepath=str(a.source));hge=load_hge(a.game_root);src=bpy.data.objects['JAZZ_VZ58_StockWire'];o,report=folded_copy(src)
 loc=o.location.copy();o.parent=None;o.location=(0,0,0);origin=bpy.data.objects.new(o.name+'_Origin',None);bpy.context.collection.objects.link(origin);o.parent=origin
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);origin.select_set(True)
 filename=a.build/'rigged/JAZZ_VZ58_StockWireFolded.fbx'
 with hge.ObjectNamesExportContext(bpy.context):bpy.ops.export_scene.fbx(filepath=str(filename),use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
 o.location=loc;bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged/VZ58_Folding.blend'))
 o.data.calc_loop_triangles();report.update(triangles=len(o.data.loop_triangles),custom_normals=o.data.has_custom_normals);(a.build/'fold-build-report.json').write_text(json.dumps(report,indent=2))
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=20;scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
 scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.4
 active={'JAZZ_VZ58','JAZZ_VZ58_StockWireFolded','JAZZ_VZ58_GripWood','JAZZ_VZ58_HandguardWood','JAZZ_VZ58_Magazine'}
 for ob in scene.objects:
  if ob.type=='MESH':ob.hide_render=ob.name not in active
 target=Vector((0,-.26,.015));cam=bpy.data.cameras.new('Camera');cam.type='ORTHO';cam.ortho_scale=.84;camera=bpy.data.objects.new('Camera',cam);scene.collection.objects.link(camera);scene.camera=camera
 for i,offset in enumerate([(-1,-.5,1.5),(-.5,.5,1),(1,1,0)]):
  light=bpy.data.lights.new('Light'+str(i),'AREA');light.energy=25;light.size=1.5;ob=bpy.data.objects.new(light.name,light);scene.collection.objects.link(ob);ob.location=target+Vector(offset);ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
 for name,direction in [('folded',(-2,-.5,.6)),('folded-side',(-2,0,.04)),('folded-opposite',(2,0,.1))]:
  scene.render.resolution_x=1300;scene.render.resolution_y=600;scene.render.resolution_percentage=100;camera.location=target+Vector(direction);camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(a.build/(name+'.png'));bpy.ops.render.render(write_still=True)
if __name__=='__main__':main()
