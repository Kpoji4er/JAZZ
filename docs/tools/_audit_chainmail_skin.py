"""Blender compare compiled HGM skin weights against the actual exported source."""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree
p=argparse.ArgumentParser()
for n in ('blend','decoded','report'):p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);bpy.ops.wm.open_mainfile(filepath=str(a.blend.resolve()))
obj=bpy.data.objects['JAZZ_Chainmail_Male'];tree=KDTree(len(obj.data.vertices))
for v in obj.data.vertices:tree.insert(v.co,v.index)
tree.balance();data=json.loads(a.decoded.read_text());bones={i:b['name'] for i,b in enumerate(data['bones'])};errors=[]
for sub in data['meshes']:
    box=sub.get('bbox') or data['bbox'];center=Vector(tuple((box[i]+box[i+3])/2 for i in range(3)))
    for pos,ids,weights in zip(sub['vertices'],sub['bone_indices'],sub['bone_weights']):
        q=Vector(pos)+center;q=Vector((-q.y,-q.x,q.z));_,index,distance=tree.find(q)
        expected={obj.vertex_groups[g.group].name:g.weight for g in obj.data.vertices[index].groups if g.weight>1e-7}
        actual={}
        for i,w in zip(ids,weights):
            if w>0:actual[bones[i]]=actual.get(bones[i],0)+w
        error=sum(abs(expected.get(n,0)-actual.get(n,0)) for n in expected.keys()|actual.keys())
        errors.append(error)
report={'vertices':len(errors),'max_weight_l1_error':max(errors),'mean_weight_l1_error':sum(errors)/len(errors),'limit':.04,'pass':max(errors)<.04}
a.report.write_text(json.dumps(report,indent=2));print(json.dumps(report));assert report['pass'],report
