"""Narrow Chainmail sleeves around native upper arms without shortening them.
Blender -- --source BLEND --output DIR. Staging only; preserves UVs and native skin weights.
"""
import argparse,json,sys
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.kdtree import KDTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
p.add_argument('--source',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
obj=bpy.data.objects['TEST_Chainmail'];rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
skin={i for f in obj.data.polygons if obj.data.materials[f.material_index].get('jazz_skin_colorization') for i in f.vertices}
skin_tree=KDTree(len(skin))
for i in skin:skin_tree.insert(obj.data.vertices[i].co,i)
skin_tree.balance()
def smooth(t):
 t=max(0,min(1,t));return t*t*(3-2*t)
changes=[]
for v in obj.data.vertices:
 if v.index in skin:continue
 q=v.co.copy();side='L' if q.x>0 else 'R'
 shoulder=rig.matrix_world@rig.data.bones['Bip001 '+side+' UpperArm'].head_local
 elbow=rig.matrix_world@rig.data.bones['Bip001 '+side+' Forearm'].head_local
 axis=(elbow-shoulder).normalized();along=(q-shoulder).dot(axis)
 center=shoulder+axis*along;radial=q-center
 sleeve=smooth((abs(q.x)-.175)/.080)*(1-smooth((q.z-1.39)/.045))
 # Reduce only the excess radius; the axial coordinate (sleeve length) is exact.
 radius=radial.length;target=max(.092,radius*.90)
 if radius>target and sleeve>0:
  v.co=center+radial*(1-sleeve*(1-target/radius))
  assert abs((v.co-q).dot(axis))<1e-6
  changes.append((v.co-q).length)
 # The mail sleeve must follow the native arm, while the upper metal cap
 # remains rigid. The old broad height fade anchored most of the sleeve to
 # Spine2 and let the arm pass through it when aiming.
 arm_mix=.40*smooth((abs(q.x)-.15)/.12)*(1-smooth((q.z-1.34)/.095))*smooth((q.z-1.10)/.12)
 if arm_mix>0:
  donor={};total=0
  for _,i,d in skin_tree.find_n(q,8):
   factor=1/max(d,.003)**2;total+=factor
   for g in obj.data.vertices[i].groups:
    n=obj.vertex_groups[g.group].name;donor[n]=donor.get(n,0)+g.weight*factor
  old={obj.vertex_groups[g.group].name:g.weight for g in v.groups}
  weights={n:old.get(n,0)*(1-arm_mix)+donor.get(n,0)/total*arm_mix for n in old.keys()|donor.keys()}
  pairs=sorted(weights.items(),key=lambda x:-x[1])[:4];norm=sum(w for _,w in pairs)
  for g in list(v.groups):obj.vertex_groups[g.group].remove([v.index])
  for n,w in pairs:obj.vertex_groups[n].add([v.index],w/norm,'REPLACE')
 # Seat the oversized rigid cap closer to the shoulder in the rest mesh.
 # Its existing Spine2 weights stay unchanged.
 cap=smooth((q.z-1.435)/.025)*smooth((abs(q.x)-.15)/.08)
 if cap>0:
  v.co.x-=(1 if q.x>0 else -1)*.012*cap
  v.co.y*=1-.08*cap
  v.co.z-=.006*cap
prepare_export_mesh(obj)
for material in obj.data.materials:
 if not material.get('jazz_skin_colorization'):continue
 # Developer body_BC has a mid-grey neutral base; shipped Shirt08 skin has a
 # near-white base before C1 tint. Calibrate only this sample skin material.
 bs=material.node_tree.nodes.get('Principled BSDF');old=bs.inputs['Base Color'].links[0].from_socket
 gain=material.node_tree.nodes.new('ShaderNodeMixRGB');gain.name='Native skin base calibration';gain.blend_type='MULTIPLY';gain.use_clamp=True
 gain.inputs[0].default_value=1;gain.inputs[2].default_value=(4.3,4.3,4.3,1)
 material.node_tree.links.new(old,gain.inputs[1]);material.node_tree.links.new(gain.outputs[0],bs.inputs['Base Color'])
report={'changed_vertices':len(changes),'max_displacement_m':max(changes),'sleeve_axial_length_preserved':True,'skin_geometry_and_weights_unchanged':True,'skin_base_linear_gain':4.3,'sleeve_weights':'native skin field below rigid caps','upper_caps_seated_inward_mm':12,'upper_caps_lowered_mm':6,'runtime':'NOT_RUN'}
(a.output/'fit-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str((a.output/'Chainmail.blend').resolve()))
scene=bpy.context.scene;scene.cycles.samples=12;scene.render.resolution_x=800;scene.render.resolution_y=800
scene.camera.data.ortho_scale=1.05
for name,pos in [('front',(0,-3,1.60)),('back',(0,3,1.60)),('side',(3,0,1.60))]:
 scene.camera.location=pos;scene.camera.rotation_euler=(Vector((0,0,1.30))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
 scene.render.filepath=str((a.output/(name+'.png')).resolve());bpy.ops.render.render(write_still=True)
print(json.dumps(report))
