"""Blender: measure sewn strap/pad separation in rest and synthetic poses.

--source rigged.blend --output report.json
Uses persistent authored point attributes, not nearest-body guesses.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy
from mathutils.bvhtree import BVHTree

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(a.source))
armor=bpy.data.objects['TEST_LeatherArmor']
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
surfaces=[v.value for v in armor.data.attributes['leather_surface'].data]
anchors=[v.value for v in armor.data.attributes['leather_anchor'].data]
assert sum(v==1 for v in anchors)>=10 and sum(v==2 for v in anchors)>=10,'Missing anchor footprint'
poses={'rest':[], 'lean':[('Bip001 Spine1',(12,0,0)),('Bip001 Spine2',(23,0,12)),('Bip001 R UpperArm',(0,35,-25))],
       'deep_lean':[('Bip001 Spine1',(28,0,0)),('Bip001 Spine2',(35,0,-18))],
       'twist':[('Bip001 Spine1',(0,0,25)),('Bip001 Spine2',(0,0,25)),('Bip001 L Clavicle',(0,0,20))]}
report={'source':str(a.source),'runtime':'NOT_RUN','poses':[]}
failures=[]
for name,rotations in poses.items():
    for bone in rig.pose.bones:
        bone.rotation_mode='XYZ';bone.rotation_euler=(0,0,0)
    for bone,angles in rotations:rig.pose.bones[bone].rotation_euler=[math.radians(x) for x in angles]
    bpy.context.view_layer.update()
    evaluated=armor.evaluated_get(bpy.context.evaluated_depsgraph_get())
    mesh=evaluated.to_mesh();mesh.calc_loop_triangles()
    vertices=[armor.matrix_world@v.co for v in mesh.vertices]
    for side in (1,2):
        faces=[tuple(t.vertices) for t in mesh.loop_triangles if all(surfaces[v]==side for v in t.vertices)]
        assert faces
        bvh=BVHTree.FromPolygons(vertices,faces,all_triangles=True)
        distances=sorted(bvh.find_nearest(vertices[i])[3] for i,v in enumerate(anchors) if v==side)
        limit=.0015 if name=='rest' else .006
        maximum=max(distances)
        report['poses'].append({'pose':name,'side':side,'samples':len(distances),'max_gap_m':maximum,
                                'p95_gap_m':distances[int((len(distances)-1)*.95)],'limit_m':limit})
        if maximum>limit:failures.append((name,side,maximum,limit))
    evaluated.to_mesh_clear()
report['status']='FAIL' if failures else 'PASS_SEWN_CONTACT'
report['failures']=failures
a.output.write_text(json.dumps(report,indent=2))
assert not failures,failures
print(report['status'],max(row['max_gap_m'] for row in report['poses']))
