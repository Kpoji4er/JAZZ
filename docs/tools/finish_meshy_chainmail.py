"""Finish the recorded Chainmail repair before image-guided texturing.
Blender: -- --input candidate.blend --output DIR. Does not install game assets.
"""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh,numpy as np
from mathutils import Vector

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.input))
obj=bpy.data.objects['Chainmail_repaired_candidate']
for other in list(bpy.data.objects):
    if other!=obj:bpy.data.objects.remove(other,do_unlink=True)
bpy.context.view_layer.objects.active=obj;obj.hide_set(False);obj.hide_render=False;obj.select_set(True)
if obj.data.has_custom_normals:bpy.ops.mesh.customdata_custom_splitnormals_clear()
bm=bmesh.new();bm.from_mesh(obj.data)
# The 15 remaining boundary edges are five isolated tiny triangles, not
# openings in the main shell. Delete only these measured debris components.
seen=set();debris=[];removed=[]
for seed in bm.verts:
    if seed in seen:continue
    stack=[seed];seen.add(seed);component=[]
    while stack:
        v=stack.pop();component.append(v)
        for e in v.link_edges:
            n=e.other_vert(v)
            if n not in seen:seen.add(n);stack.append(n)
    faces=set(f for v in component for f in v.link_faces)
    extent=Vector(tuple(max(v.co[i] for v in component)-min(v.co[i] for v in component) for i in range(3))).length
    if len(faces)<=3 and extent<.02:
        debris.extend(component);removed.append(dict(vertices=len(component),faces=len(faces),extent=extent))
if debris:bmesh.ops.delete(bm,geom=debris,context='VERTS')
bm.normal_update()
# Restore a gently curved continuous front on each breast plate. Change only
# depth inside the plate, with a tapered border; silhouette stays untouched.
changes=[]
for sign in [-1,1]:
    selected=[v for v in bm.verts if .08<sign*v.co.x<.49 and .08<v.co.z<.62 and v.co.y<-.29]
    if not selected:continue
    coords=np.array([list(v.co) for v in selected]);x=coords[:,0];z=coords[:,2]
    design=np.column_stack([np.ones(len(x)),x,z,x*x,x*z,z*z])
    coeff=np.linalg.lstsq(design,coords[:,1],rcond=None)[0];target=design@coeff
    for v,y in zip(selected,target):
        sx=sign*v.co.x
        weight=min(1,(sx-.08)/.055,(.49-sx)/.055,(v.co.z-.08)/.065,(.62-v.co.z)/.065)
        weight=max(0,weight);weight=weight*weight*(3-2*weight)
        delta=max(-.035,min(.035,float(y)-v.co.y))*.9*weight
        v.co.y+=delta;changes.append(abs(delta))
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
for f in bm.faces:f.smooth=True
stats=dict(removed_debris=removed,boundary_edges=sum(e.is_boundary for e in bm.edges),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),max_plate_depth_adjustment=max(changes,default=0),custom_normals=False)
assert stats['boundary_edges']==0 and stats['nonmanifold_edges']==0,stats
bm.to_mesh(obj.data);bm.free();obj.data.update();obj.data.calc_loop_triangles();stats['triangles']=len(obj.data.loop_triangles)
stats['passages']=[]
for side in [-1,1]:
    for start,end in [(Vector((side*.15,.08,.35)),Vector((side*.5795,.08,.35))), (Vector((side*.5795,.08,.35)),Vector((side*.95,.08,-.30)))]:
        delta=end-start;hit,*_=obj.ray_cast(start,delta.normalized(),distance=delta.length)
        stats['passages'].append(dict(start=list(start),end=list(end),blocked=bool(hit)))
assert not any(t['blocked'] for t in stats['passages'])
# Voxel reconstruction invalidated source UVs: let the retexture service
# generate a fresh layout instead of pretending the old one is usable.
for uv in list(obj.data.uv_layers):obj.data.uv_layers.remove(uv)
obj.name='Chainmail_clean'
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'Chainmail_clean.blend'))
bpy.ops.export_scene.gltf(filepath=str(a.output/'Chainmail_clean.glb'),export_format='GLB',use_selection=True,export_animations=False)
(a.output/'repair.json').write_text(json.dumps(stats,indent=2),encoding='utf-8')
(a.output/'render-manifest.json').write_text(json.dumps({'jobs':[{'name':'clean','project':str(a.output.resolve()),'model':str((a.output/'Chainmail_clean.glb').resolve())}]},indent=2),encoding='utf-8')
print(json.dumps(stats))
