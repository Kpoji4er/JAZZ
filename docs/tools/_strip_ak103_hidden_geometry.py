"""Build a non-installed AK103 hidden-face candidate from the independent audit.
No decimation; protects two adjacency rings around every potentially visible face.
Verifies retained positions/UV and normals on all initially visible faces.
"""
import argparse,json,sys,math
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
from _optimize_ak103_mesh import render_pairs

def sweep(out,objs,before):
 scene=bpy.context.scene;cam=scene.camera;after={o.name:o.data for o in objs}
 scene.render.resolution_x=1000;scene.render.resolution_y=750
 configs={o.name:[o.name] for o in objs}
 unfolded=[o.name for o in objs if 'Folded' not in o.name]
 configs['assembled']=unfolded
 configs['folded']=[n for n in unfolded if n!='AKR_AK103_Stock']+['AKR_AK103_StockFolded']
 configs['no_magazine']=[n for n in unfolded if n!='AKR_AK103_Magazine']
 dirs=[(math.cos(i*math.pi/3),math.sin(i*math.pi/3),z) for z in [-.6,.6] for i in range(6)]+[(0,0,1),(0,0,-1)]
 out.mkdir(parents=True,exist_ok=True)
 for label,names in configs.items():
  for o in objs:o.hide_render=o.name not in names
  points=[o.matrix_world@v.co for o in objs if o.name in names for v in before[o.name].vertices]
  lo=Vector(tuple(min(v[i] for v in points) for i in range(3)));hi=Vector(tuple(max(v[i] for v in points) for i in range(3)))
  centre=(lo+hi)/2;span=max(hi-lo)*1.35
  for i,d in enumerate(dirs):
   cam.location=centre+Vector(d).normalized()*2;cam.rotation_euler=(centre-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=span
   for phase,meshes in [('before',before),('after',after)]:
    for o in objs:o.data=meshes[o.name]
    scene.render.engine='BLENDER_EEVEE_NEXT'
    scene.render.filepath=str(out/f'{label}_{i:02}_{phase}.png');bpy.ops.render.render(write_still=True)
 for o in objs:o.data=after[o.name];o.hide_render='Folded' in o.name

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ['source','audit','out']:p.add_argument('--'+n,type=Path,required=True)
 p.add_argument('--rings',type=int,default=2);p.add_argument('--whole-islands',action='store_true');p.add_argument('--render',action='store_true');p.add_argument('--game-root',type=Path)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
 audit=json.loads(a.audit.read_text());bpy.ops.wm.open_mainfile(filepath=str(a.source),use_scripts=False)
 for im in bpy.data.images:
  if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
 objs=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('AKR_AK103')]
 before={o.name:o.data.copy() for o in objs};report={}
 for o in objs:
  old=o.data;old.calc_loop_triangles();r=audit['entities'][o.name];hidden=set(r['sample_hidden_faces']);assert len(old.polygons)==r['triangles']
  bm=bmesh.new();bm.from_mesh(old);bm.faces.ensure_lookup_table();bm.verts.ensure_lookup_table()
  layer=bm.faces.layers.int.new('audit_original_face')
  for f in bm.faces:f[layer]=f.index
  if a.whole_islands:
   kill={i for c in r['fully_hidden_islands'] for i in c['face_indices']}
  else:
   protected=set(range(len(old.polygons)))-hidden
   for _ in range(a.rings):
    protected|={f.index for i in protected for v in bm.faces[i].verts for f in v.link_faces}
   kill=hidden-protected
  # All retained corners must keep exact coordinates and original UVs.
  uv=old.uv_layers.active.data
  expected={f.index:{tuple(old.vertices[old.loops[l].vertex_index].co):(tuple(uv[l].uv),old.corner_normals[l].vector.copy()) for l in f.loop_indices} for f in old.polygons if f.index not in kill}
  bmesh.ops.delete(bm,geom=[bm.faces[i] for i in sorted(kill)],context='FACES')
  bm.to_mesh(o.data);bm.free();prepare_export_mesh(o)
  ids=o.data.attributes['audit_original_face'].data;uvnew=o.data.uv_layers.active.data;maximum=0
  for f in o.data.polygons:
   original=ids[f.index].value;corners=expected[original]
   for l in f.loop_indices:
    v=tuple(o.data.vertices[o.data.loops[l].vertex_index].co);assert v in corners,(o.name,'vertex moved')
    uvold,normold=corners[v];assert tuple(uvnew[l].uv)==uvold,(o.name,'UV changed')
    if original not in hidden:
     n=o.data.corner_normals[l].vector
     # atan2 is stable for almost-identical unit normals.
     angle=math.degrees(math.atan2(normold.cross(n).length,normold.dot(n)));maximum=max(maximum,angle)
  o.data.attributes.remove(o.data.attributes['audit_original_face'])
  report[o.name]={'before':r['triangles'],'after':len(o.data.polygons),'removed':len(kill),'visible_corner_normal_max_degrees':maximum,'retained_positions_uv_exact':True,'normal_gate':maximum<.01,'deleted_original_faces':sorted(kill)}
  print(o.name,{k:v for k,v in report[o.name].items() if k!='deleted_original_faces'},flush=True)
 (a.out/'strip-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 assert all(v['normal_gate'] for v in report.values()),'Visible normals changed; candidate rejected'
 bpy.ops.wm.save_as_mainfile(filepath=str(a.out/'AK103_JA3.blend'))
 if a.game_root:
  from _export_ak103_assets import load_hge
  from _export_m14_family_assets import export_fbx
  export_fbx(load_hge(a.game_root),a.out/'AK103_JA3.fbx')
 if a.render:
  render_pairs(a.out/'review',objs,before)
  sweep(a.out/'sweep',objs,before)
if __name__=='__main__':main()
