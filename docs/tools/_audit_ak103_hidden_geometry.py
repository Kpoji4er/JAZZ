"""Audit every native AK103 entity independently for hidden geometry and duplicates.
Blender --python ... -- --build <native build> --out <audit directory>.
No model writes. Independent entities prevent detachable parts acting as occluders.
Finite ray sampling identifies candidates, never authorizes deletion by itself.
"""
import argparse,json,math,sys
from collections import defaultdict
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _inspect_weapon_source import setup_render,render_views
from _build_ak103_archive import world_bbox

def directions(n):
 return [Vector((math.sqrt(1-(1-2*(i+.5)/n)**2)*math.cos(i*math.pi*(3-math.sqrt(5))),math.sqrt(1-(1-2*(i+.5)/n)**2)*math.sin(i*math.pi*(3-math.sqrt(5))),1-2*(i+.5)/n)) for i in range(n)]

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.out.mkdir(parents=True,exist_ok=True)
 bpy.ops.wm.open_mainfile(filepath=str(a.build/'clean/AK103.blend'),use_scripts=False)
 sources={o.name:[m.name for m in o.data.materials] for o in bpy.context.scene.objects if o.type=='MESH'}
 bpy.ops.wm.open_mainfile(filepath=str(a.build/'rigged/AK103_JA3.blend'),use_scripts=False)
 objs=sorted([o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('AKR_AK103')],key=lambda o:o.name)
 dirs=directions(192);report={'method':'Each entity isolated, two-sided opaque ray occlusion, 192 sphere directions, centroid plus 3 near-corners and 3 near-edge samples per still-hidden triangle; 2 micrometre offset. Sample-hidden is a candidate only.','entities':{}}
 masks={}
 for o in objs:
  m=o.data;m.calc_loop_triangles();vs=[v.co.copy() for v in m.vertices];fs=[tuple(t.vertices) for t in m.loop_triangles];tree=BVHTree.FromPolygons(vs,fs,all_triangles=True)
  parent=list(range(len(vs)))
  def find(x):
   while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
   return x
  for f in fs:
   for v in f[1:]:parent[find(v)]=find(f[0])
  islands=defaultdict(list)
  for i,f in enumerate(fs):islands[find(f[0])].append(i)
  mats=sources[o.name.replace('AKR_','').replace('StockFolded','Stock')];grid=2**math.ceil(math.log2(math.ceil(math.sqrt(len(mats))))) if len(mats)>1 else 1
  uv=m.uv_layers.active.data;labels=[];dupes=defaultdict(list)
  for i,t in enumerate(m.loop_triangles):
   c=sum((uv[j].uv for j in t.loops),Vector((0,0)))/3;tile=min(grid-1,int(c.x*grid))+min(grid-1,int(c.y*grid))*grid
   labels.append(mats[tile] if tile<len(mats) else 'UNKNOWN')
   key=tuple(sorted(tuple(round(k,8) for k in vs[j]) for j in fs[i]));dupes[key].append(i)
  hidden=[];rescued=0
  for idx,f in enumerate(fs):
   points=[vs[j] for j in f];c=sum(points,Vector())/3
   def visible(pt):
    return any(tree.ray_cast(pt+d*.000002,d,2)[0] is None for d in dirs)
   if visible(c):continue
   extra=[v*.98+c*.02 for v in points]+[(points[k]+points[(k+1)%3])*.49+c*.02 for k in range(3)]
   if any(visible(pt) for pt in extra):rescued+=1
   else:hidden.append(idx)
  hs=set(hidden);masks[o.name]=hs;stats={}
  for i,mat in enumerate(labels):
   row=stats.setdefault(mat,{'triangles':0,'sample_hidden':0});row['triangles']+=1;row['sample_hidden']+=int(i in hs)
  parts=[]
  for k,indices in enumerate(sorted(islands.values(),key=len,reverse=True)):
   vertices={v for i in indices for v in fs[i]};lo=[min(vs[v][j] for v in vertices) for j in range(3)];hi=[max(vs[v][j] for v in vertices) for j in range(3)]
   parts.append({'id':k,'triangles':len(indices),'hidden':sum(i in hs for i in indices),'materials':sorted(set(labels[i] for i in indices)),'bbox_mm':[[round(v*1000,3) for v in lo],[round(v*1000,3) for v in hi]],'face_indices':indices})
  result={'triangles':len(fs),'vertices':len(vs),'islands':len(parts),'sample_hidden_triangles':len(hs),'rescued_by_corner_edge_samples':rescued,'fully_hidden_islands':[p for p in parts if p['hidden']==p['triangles']],'material_groups':stats,'coincident_triangle_groups':[v for v in dupes.values() if len(v)>1],'components':parts,'sample_hidden_faces':hidden}
  report['entities'][o.name]=result
  (a.out/'all-parts-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
  print(o.name, 'triangles',len(fs),'hidden',len(hs),'islands',len(parts),'whole hidden',[(p['id'],p['triangles']) for p in result['fully_hidden_islands']], 'duplicates',len(result['coincident_triangle_groups']),flush=True)
 # Render candidates in red in each independent module, and candidate faces alone.
 setup_render(1100,'MATERIAL')
 for name,col in [('VisibleShell',(.45,.45,.45,1)),('HiddenCandidate',(1,.08,.02,1))]:
  mat=bpy.data.materials.new(name);mat.diffuse_color=col
 import bmesh
 for o in objs:
  for other in objs:other.hide_render=other!=o
  o.data.materials.clear()
  for name in ['VisibleShell','HiddenCandidate']:o.data.materials.append(bpy.data.materials[name])
  for t in o.data.loop_triangles:o.data.polygons[t.polygon_index].material_index=int(t.index in masks[o.name])
  lo,hi=world_bbox([o]);render_views(a.out,o.name+'_highlight',lo,hi)
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.material_index==0],context='FACES');bm.to_mesh(o.data);bm.free()
  render_views(a.out,o.name+'_hidden_only',lo,hi)
if __name__=='__main__':main()
