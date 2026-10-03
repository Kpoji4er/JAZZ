"""Non-destructive local Chainmail cleanup experiment. Blender: -- --input GLB --output DIR."""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector

p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
jobs=[]
for variant,iterations in [('normals',0),('relaxed',6)]:
    bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(a.input))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH'];details=[]
    for obj in meshes:
        bpy.context.view_layer.objects.active=obj;obj.select_set(True)
        if obj.data.has_custom_normals:bpy.ops.mesh.customdata_custom_splitnormals_clear()
        bm=bmesh.new();bm.from_mesh(obj.data)
        lo=Vector(tuple(min(v.co[i] for v in bm.verts) for i in range(3)));hi=Vector(tuple(max(v.co[i] for v in bm.verts) for i in range(3)));diag=(hi-lo).length
        bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=diag*1e-7)
        bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=diag*1e-9)
        bm.normal_update()
        original={v:v.co.copy() for v in bm.verts}
        # Gentle bilateral relaxation: smooth small noisy patches without moving
        # boundary vertices or merging disconnected surfaces. Limit displacement.
        eligible=[v for v in bm.verts if v.is_manifold]
        for step in range(iterations):
            updates={}
            for v in eligible:
                ns=[e.other_vert(v) for e in v.link_edges]
                if not ns:continue
                avg=sum((n.co for n in ns),Vector())/len(ns)
                delta=(avg-v.co)*.23
                target=v.co+delta
                displacement=target-original[v]
                if displacement.length>diag*.008:target=original[v]+displacement.normalized()*diag*.008
                updates[v]=target
            for v,pos in updates.items():v.co=pos
        bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
        for f in bm.faces:f.smooth=True
        details.append(dict(vertices=len(bm.verts),faces=len(bm.faces),boundary=sum(e.is_boundary for e in bm.edges),nonmanifold=sum(not e.is_manifold for e in bm.edges),max_displacement=max((v.co-original[v]).length for v in bm.verts)))
        bm.to_mesh(obj.data);bm.free();obj.data.update()
    out=a.output/variant;out.mkdir(exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'Chainmail.blend'))
    bpy.ops.export_scene.gltf(filepath=str(out/'Chainmail.glb'),export_format='GLB',export_animations=False)
    (out/'cleanup.json').write_text(json.dumps(details,indent=2),encoding='utf-8')
    jobs.append(dict(name=variant,project=str(out.resolve()),model=str((out/'Chainmail.glb').resolve())))
(a.output/'render-manifest.json').write_text(json.dumps(dict(jobs=jobs),indent=2),encoding='utf-8')
