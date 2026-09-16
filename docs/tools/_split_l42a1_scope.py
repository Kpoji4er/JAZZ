import bpy
from pathlib import Path
from mathutils import Vector
import argparse,sys
parser=argparse.ArgumentParser()
parser.add_argument('--build',type=Path,required=True)
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=args.build

bpy.ops.wm.open_mainfile(filepath=str(out/'L42A1_material_review.blend'))
meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
body=max(meshes,key=lambda o:len(o.data.vertices));lenses=min(meshes,key=lambda o:len(o.data.vertices))
# OBJ import retains a 90-degree transform. Select in source-local coordinates.
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
for p in body.data.polygons:
    points=[body.data.vertices[v].co/.0007 for v in p.vertices]
    p.select=all(-430<v.x<80 and v.y>68 for v in points)
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.separate(type='SELECTED');bpy.ops.object.mode_set(mode='OBJECT')
scope=[o for o in bpy.context.selected_objects if o!=body][0]
body.name='L42A1';scope.name='L42A1_ScopeBody';lenses.name='L42A1_Lenses'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'L42A1_split_review.blend'))
body.hide_render=True
s=bpy.context.scene;s.render.filepath=str(out/'L42A1_scope_review.png')
bpy.ops.render.render(write_still=True)
print('Scope polygons:',len(scope.data.polygons),'Body polygons:',len(body.data.polygons))
