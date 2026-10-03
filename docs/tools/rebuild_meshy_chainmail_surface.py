"""Local repair candidate: voxel surface reconstruction and sleeve tunnels, no game writes.
Blender: -- --input GLB --output DIR. Coordinates are specific to the recorded Meshy Chainmail.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.input))
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH');bpy.context.view_layer.objects.active=obj
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True)
if obj.data.has_custom_normals:bpy.ops.mesh.customdata_custom_splitnormals_clear()
# Work in imported local coordinates, retaining the same world transform.
transform=obj.matrix_world.copy();obj.matrix_world.identity()
obj.data.remesh_voxel_size=.012
obj.data.use_remesh_preserve_volume=True
bpy.ops.object.voxel_remesh()
smooth=obj.modifiers.new('Surface relaxation','SMOOTH');smooth.factor=.65;smooth.iterations=4
bpy.ops.object.modifier_apply(modifier=smooth.name)
cuts=[]
for side in [-1,1]:
    cuts.extend([(Vector((side*.38,.08,.70)),Vector((side*.95,.08,-.30))),
                 (Vector((side*.15,.08,.35)),Vector((side*.66,.08,.35)))])
for inner,outer in cuts:
    direction=outer-inner
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.16,depth=direction.length,location=(inner+outer)*.5)
    cutter=bpy.context.object;cutter.name='Sleeve opening cutter'
    cutter.rotation_euler=direction.to_track_quat('Z','Y').to_euler()
    bpy.context.view_layer.objects.active=obj
    mod=obj.modifiers.new('Open sleeve','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
bpy.context.view_layer.objects.active=obj
obj.data.calc_loop_triangles();high_count=len(obj.data.loop_triangles)
high=obj.copy();high.data=obj.data.copy();bpy.context.collection.objects.link(high);high.name='High detail repaired source';high.hide_render=True;high.hide_set(True)
dec=obj.modifiers.new('Game candidate reduction','DECIMATE');dec.ratio=min(1,15000/high_count)
bpy.ops.object.modifier_apply(modifier=dec.name)
obj.data.validate(verbose=True,clean_customdata=True)
bm=bmesh.new();bm.from_mesh(obj.data)
bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
# Decimation can leave tiny boundary loops. Fill only loops with perimeter
# below 0.2 source units, well below the anatomical opening perimeters.
edges={e for e in bm.edges if e.is_boundary}
while edges:
    seed=edges.pop();component={seed};stack=[seed]
    while stack:
        edge=stack.pop()
        for v in edge.verts:
            for other in v.link_edges:
                if other in edges:edges.remove(other);component.add(other);stack.append(other)
    if sum(e.calc_length() for e in component)<.2:
        bmesh.ops.holes_fill(bm,edges=list(component),sides=0)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
for f in bm.faces:f.smooth=True
stats=dict(high_triangles=high_count,boundary_edges=sum(e.is_boundary for e in bm.edges),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges))
bm.to_mesh(obj.data);bm.free();obj.data.update();obj.data.calc_loop_triangles();stats['triangles']=len(obj.data.loop_triangles)
obj.matrix_world=transform;high.matrix_world=transform
stats['passages']=[]
for side in [-1,1]:
    for start,end in [(Vector((side*.15,.08,.35)),Vector((side*.5795,.08,.35))),
                      (Vector((side*.5795,.08,.35)),Vector((side*.95,.08,-.30)))]:
        delta=end-start
        hit,location,normal,index=obj.ray_cast(start,delta.normalized(),distance=delta.length)
        stats['passages'].append(dict(start=list(start),end=list(end),blocked=bool(hit)))
obj.name='Chainmail_repaired_candidate'
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'Chainmail.blend'))
bpy.ops.export_scene.gltf(filepath=str(a.output/'Chainmail.glb'),export_format='GLB',use_selection=True,export_animations=False)
(a.output/'repair.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
(a.output/'render-manifest.json').write_text(json.dumps({'jobs':[{'name':'reconstructed','project':str(a.output.resolve()),'model':str((a.output/'Chainmail.glb').resolve())}]},indent=2),encoding='utf-8')
print(json.dumps(stats))
