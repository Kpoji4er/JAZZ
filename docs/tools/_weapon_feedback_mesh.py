"""Blender: explicit hard joins without custom normals; preserve surface and UV.

--blend FILE --entity NAME --output DIR --game-root DIR [--angle 40]
Writes isolated candidate blend/FBX and audit. No installed writes.
"""
import argparse, json, math, sys
from collections import Counter
from pathlib import Path
import bpy, bmesh
from mathutils import Matrix
from mathutils import Vector
from mathutils.kdtree import KDTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge, export_fbx
from _prepare_weapon_open_surfaces import prepare_export_mesh

p=argparse.ArgumentParser()
for key in ('blend','entity','output','game-root'):p.add_argument('--'+key,required=True)
p.add_argument('--angle',type=float,default=40)
p.add_argument('--compiled-prior',type=Path,help='Remove only source slivers collapsing in this compiled candidate')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
hge=load_hge(Path(a.game_root));bpy.ops.wm.open_mainfile(filepath=a.blend,use_scripts=False)
obj=bpy.data.objects[a.entity]
keep={obj,*obj.children}
if obj.parent:keep.add(obj.parent)
for other in list(bpy.data.objects):
    if other not in keep:bpy.data.objects.remove(other,do_unlink=True)
for im in bpy.data.images:
    if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
for mat in obj.data.materials:
    for prop in hge.MATERIAL_PROPERTIES:
        if prop.map and isinstance(mat.get(prop.id),str) and mat[prop.id].startswith('//'):
            mat[prop.id]=bpy.path.abspath(mat[prop.id])
def surface():
    m=obj.data;m.calc_loop_triangles();uv=m.uv_layers.active.data
    return Counter(tuple(sorted(tuple(round(x,7) for x in m.vertices[vi].co)+tuple(round(x,7) for x in uv[li].uv) for vi,li in zip(t.vertices,t.loops))) for t in m.loop_triangles)
before=surface();bm=bmesh.new();bm.from_mesh(obj.data)
# Remove only measured near-collinear submicron faces that fail native normals.
slivers=[f for f in bm.faces if f.calc_area()<1e-8 and f.calc_area()/max(max(e.calc_length() for e in f.edges)**2,1e-20)<1e-4]
if a.compiled_prior:
    decoded=json.loads(a.compiled_prior.read_text());points=[]
    for part in decoded['meshes']:
        box=part.get('bbox') or decoded['bbox'];c=[(box[i]+box[i+3])/2 for i in range(3)]
        points.extend(Vector((-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2])) for v in part['vertices'])
    tree=KDTree(len(points))
    for i,point in enumerate(points):tree.insert(point,i)
    tree.balance()
    for face in bm.faces:
        if len(face.verts)!=3 or face in slivers:continue
        nearest=[tree.find(v.co) for v in face.verts]
        assert max(item[2] for item in nearest)<.0001
        x,y,z=[item[0] for item in nearest]
        if (y-x).cross(z-x).length<1e-14:
            assert face.calc_area()<1e-7,('Unexpected collapsed large face',face.calc_area())
            slivers.append(face)
assert len(slivers)<10,(a.entity,len(slivers))
removed_area=sum(face.calc_area() for face in slivers)
bmesh.ops.delete(bm,geom=slivers,context='FACES_ONLY')
bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
bm.to_mesh(obj.data);bm.free()
# Keep each mechanical plane separate from bevels; smooth curved strips within it.
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
mod=obj.modifiers.new('Explicit mechanical joins','EDGE_SPLIT');mod.split_angle=math.radians(a.angle);mod.use_edge_angle=True;mod.use_edge_sharp=False
bpy.ops.object.modifier_apply(modifier=mod.name)
issues=prepare_export_mesh(obj)
after=surface();missing=sum((before-after).values());added=sum((after-before).values())
assert added==0 and missing==len(slivers),(missing,added,len(slivers))
assert not issues and not obj.data.has_custom_normals,issues
report={'entity':a.entity,'angle_degrees':a.angle,'triangles_before':sum(before.values()),'triangles_after':sum(after.values()),'removed_submicron_faces':len(slivers),'removed_area_m2':removed_area,'added_faces':added,'remaining_surface_uv_exact':True,'custom_normals':False,'issues':issues}
# Some assembly blends position modules through object translation rather than
# an Origin parent. The game attaches their local mesh at its own entity spot.
if obj.parent:obj.parent.matrix_world=Matrix.Identity(4)
obj.matrix_world=Matrix.Identity(4)
bpy.ops.wm.save_as_mainfile(filepath=str(out/(a.entity+'.blend')))
export_fbx(hge,out/(a.entity+'.fbx'))
(out/'mesh-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
