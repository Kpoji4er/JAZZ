"""Blender read-only AEK material/geometry study; --batch-root DIR --output DIR.
Renders each 971 OBJ against both author atlases and lists welded mesh islands.
"""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector,Matrix
p=argparse.ArgumentParser()
p.add_argument('--batch-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
report=[]
for family,filename in [('23_AEK_971_Assault_Rifle','model_0.obj'),('23_AEK_971_Assault_Rifle','model_1.obj'),('22_AEK_-_973S','model_0.obj')]:
 bpy.ops.wm.read_factory_settings(use_empty=True)
 src=a.batch_root/family/'source';bpy.ops.wm.obj_import(filepath=str(src/filename))
 o=next(o for o in bpy.context.scene.objects if o.type=='MESH')
 o.data.transform(o.matrix_world);o.matrix_world=Matrix.Identity(4)
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table()
 remaining=set(bm.verts);islands=[]
 while remaining:
  v=remaining.pop();group={v};todo=[v]
  while todo:
   v=todo.pop()
   for e in v.link_edges:
    other=e.other_vert(v)
    if other in remaining:remaining.remove(other);group.add(other);todo.append(other)
  faces={f for v in group for f in v.link_faces}
  mn=[min(v.co[i] for v in group) for i in range(3)];mx=[max(v.co[i] for v in group) for i in range(3)]
  islands.append({'vertices':len(group),'faces':len(faces),'min':mn,'max':mx})
 bm.free();vs=[v.co for v in o.data.vertices];mn=Vector([min(v[i] for v in vs) for i in range(3)]);mx=Vector([max(v[i] for v in vs) for i in range(3)])
 tag=family.split('_')[0]+'_'+Path(filename).stem
 report.append({'tag':tag,'bounds':[list(mn),list(mx)],'islands':sorted(islands,key=lambda i:-i['faces'])})
 scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.color_type='TEXTURE';scene.display.shading.light='STUDIO';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
 scene.view_settings.view_transform='Standard';scene.render.resolution_x=1100;scene.render.resolution_y=700;scene.render.resolution_percentage=100
 cam=bpy.data.cameras.new('Camera');cam.type='ORTHO';span=max(mx-mn);cam.ortho_scale=span*1.2;cam.clip_end=span*10;cam.clip_start=span*.001
 ob=bpy.data.objects.new('Camera',cam);scene.collection.objects.link(ob);scene.camera=ob;center=(mn+mx)/2
 direction=Vector((1,0,0)) if family.startswith('23') else Vector((0,1,0))
 ob.location=center+direction*span*3;ob.rotation_euler=(-direction).to_track_quat('-Z','Y').to_euler()
 if family.startswith('23'):ob.rotation_euler.rotate_axis('Z',1.57079632679)
 for path in src.glob('*BaseColor.png'):
  mat=bpy.data.materials.new(path.stem);mat.use_nodes=True;node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(path));mat.node_tree.nodes.active=node
  mat.node_tree.links.new(node.outputs['Color'],mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
  o.data.materials.clear();o.data.materials.append(mat)
  for f in o.data.polygons:f.material_index=0
  scene.render.filepath=str(a.output/(tag+'_'+path.stem+'.png'));bpy.ops.render.render(write_still=True)
(a.output/'audit.json').write_text(json.dumps(report,indent=2))
print('SOURCE_AUDIT',[(r['tag'],len(r['islands'])) for r in report])
