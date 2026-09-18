"""Blender read-only audit of the developer clothing sample; no export/mutation."""
import bpy,argparse,sys,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--sample',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.sample))
rows=[]
for obj in bpy.data.objects:
 if obj.type not in ('MESH','ARMATURE'):continue
 row={'name':obj.name,'type':obj.type,'parent':obj.parent.name if obj.parent else None,'scale':list(obj.scale),'location':list(obj.location),'hgskeleton':obj.get('hgskeleton'),'armatures':[m.object.name if m.object else None for m in obj.modifiers if m.type=='ARMATURE']}
 if obj.type=='MESH':
  positions=[obj.matrix_world@v.co for v in obj.data.vertices]
  row.update(vertices=len(positions),uv_maps=len(obj.data.uv_layers),materials=[m.name if m else None for m in obj.data.materials],bounds=[[min(v[i] for v in positions),max(v[i] for v in positions)] for i in range(3)],unweighted=sum(not any(g.weight>1e-6 for g in v.groups) for v in obj.data.vertices),max_weights=max((sum(g.weight>1e-6 for g in v.groups) for v in obj.data.vertices),default=0))
 rows.append(row)
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows,indent=2))
