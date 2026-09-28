"""Read-only AK103 native interior/visibility audit; never deletes geometry.
Blender --python ... -- --build <native build> --out <audit directory>.
Finite ray samples identify candidates only, not proof that faces can be removed.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _inspect_weapon_source import setup_render,render_views
from _build_ak103_archive import world_bbox
p=argparse.ArgumentParser();p.add_argument('--build',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.build/'clean/AK103.blend'),use_scripts=False)
source={o.name:[m.name for m in o.data.materials] for o in bpy.context.scene.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(a.build/'rigged/AK103_JA3.blend'),use_scripts=False)
objects=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('AKR_AK103') and 'Folded' not in o.name]
verts=[];faces=[];records=[]
for o in objects:
 o.data.calc_loop_triangles();offset=len(verts);verts.extend(o.matrix_world@v.co for v in o.data.vertices)
 mats=source[o.name.replace('AKR_','')];grid=2**math.ceil(math.log2(math.ceil(math.sqrt(len(mats))))) if len(mats)>1 else 1
 uv=o.data.uv_layers.active.data
 for t in o.data.loop_triangles:
  faces.append(tuple(offset+i for i in t.vertices));center=sum((uv[i].uv for i in t.loops),Vector((0,0)))/3
  tile=min(grid-1,int(center.x*grid))+min(grid-1,int(center.y*grid))*grid
  records.append((o.name,t.polygon_index,mats[tile] if tile<len(mats) else 'unknown'))
tree=BVHTree.FromPolygons(verts,faces,all_triangles=True)
directions=[]
for i in range(96):
 z=1-2*(i+.5)/96;r=math.sqrt(1-z*z);ang=i*math.pi*(3-math.sqrt(5));directions.append(Vector((r*math.cos(ang),r*math.sin(ang),z)))
counts={};unseen=[]
for idx,(f,record) in enumerate(zip(faces,records)):
 key=record[0]+'/'+record[2];row=counts.setdefault(key,{'triangles':0,'sample_visible':0,'unseen_samples':0})
 row['triangles']+=1;v=[verts[i] for i in f];c=sum(v,Vector())/3
 visible=False
 # Surface offset is 2 micrometres. Sample both sides; no backface culling.
 for d in directions:
  if tree.ray_cast(c+d*.000002,d,2)[0] is None:visible=True;break
 if visible:row['sample_visible']+=1
 else:row['unseen_samples']+=1;unseen.append(idx)
report={'method':'96 global directions, triangle centroid, opaque assembled mesh. Unseen is only a candidate, not safe-to-delete proof. Folded stock excluded.','groups':counts}
(a.out/'interior-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
# Red internal source parts among grey opaque receiver; second preview exposes only these parts.
for o in objects:
 o.data.materials.clear()
for name,color in [('shell',(.32,.32,.32,1)),('bolt',(1,.06,.015,1)),('ksk',(.1,.5,1,1))]:
 m=bpy.data.materials.new(name);m.diffuse_color=color
for o in objects:
 for n in ['shell','bolt','ksk']:o.data.materials.append(bpy.data.materials[n])
for name,poly,mat in records:
 bpy.data.objects[name].data.polygons[poly].material_index=1 if 'Bolt_group' in mat else 2 if '_ksk' in mat else 0
setup_render(1400,'MATERIAL');lo,hi=world_bbox(objects)
render_views(a.out,'assembled_highlight',lo,hi)
# Hide shell faces in a diagnostic copy only, retain the original on disk.
import bmesh
for o in objects:
 bm=bmesh.new();bm.from_mesh(o.data)
 bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index==0],context='FACES');bm.to_mesh(o.data);bm.free()
render_views(a.out,'internal_only',lo,hi)
