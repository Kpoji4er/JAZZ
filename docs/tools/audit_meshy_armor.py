"""Blender read-only mesh audit: -- --input model.glb --output report.json."""
import argparse
import json
import sys
from pathlib import Path
import bpy
import bmesh
from mathutils import Vector

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--input',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(a.input))
report=[]
for obj in [o for o in bpy.context.scene.objects if o.type=='MESH']:
    mesh=obj.data;mesh.calc_loop_triangles()
    bm=bmesh.new();bm.from_mesh(mesh)
    lo=Vector(tuple(min(v.co[i] for v in bm.verts) for i in range(3)))
    hi=Vector(tuple(max(v.co[i] for v in bm.verts) for i in range(3)))
    row=dict(name=obj.name,vertices=len(mesh.vertices),triangles=len(mesh.loop_triangles),smooth_faces=sum(f.use_smooth for f in mesh.polygons),custom_normals=mesh.has_custom_normals,bounds=[list(lo),list(hi)],boundary_before=sum(e.is_boundary for e in bm.edges))
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=(hi-lo).length*1e-7)
    bm.verts.ensure_lookup_table();bm.faces.ensure_lookup_table()
    seen=set();components=[]
    for seed in bm.verts:
        if seed in seen:continue
        stack=[seed];seen.add(seed);vs=[]
        while stack:
            v=stack.pop();vs.append(v)
            for e in v.link_edges:
                n=e.other_vert(v)
                if n not in seen:seen.add(n);stack.append(n)
        components.append(dict(vertices=len(vs),bounds=[[min(v.co[i] for v in vs) for i in range(3)],[max(v.co[i] for v in vs) for i in range(3)]]))
    row.update(welded_vertices=len(bm.verts),welded_faces=len(bm.faces),boundary_after=sum(e.is_boundary for e in bm.edges),nonmanifold_after=sum(not e.is_manifold for e in bm.edges),components=sorted(components,key=lambda c:-c['vertices'])[:20])
    report.append(row);bm.free()
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
