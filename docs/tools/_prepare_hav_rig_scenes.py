"""Add a JA3 Male skeleton and clothed reference to clean HAV source variants."""
import argparse,json,sys,hashlib
from pathlib import Path
import bpy
from mathutils import Vector
p=argparse.ArgumentParser()
for k in ('source','reference','output'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
rows=[]
for family in ('Twaron','Guardian','Zylon'):
 for variant in ('Light','Medium','Full'):
  name=family+variant;bpy.ops.wm.open_mainfile(filepath=str(a.source/(name+'.blend')))
  armor=[o for o in bpy.data.objects if o.type=='MESH']
  def signature():return hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices],list(map(list,o.matrix_world))) for o in armor]).encode()).hexdigest()
  before=signature()
  with bpy.data.libraries.load(str(a.reference),link=False) as (src,dst):
   dst.objects=['Bip001','M_BaseMesh Skin_BIP','QA actual LegionGoon shirt']
  collection=bpy.data.collections.new('REFERENCE - JA3 Male and Legion shirt');bpy.context.scene.collection.children.link(collection)
  for obj in dst.objects:
   assert obj is not None
   collection.objects.link(obj);obj.hide_render=False;obj.hide_set(False)
  rig,body,shirt=dst.objects
  rig.data.pose_position='REST';rig.show_in_front=True;rig.hide_render=True
  for bone in rig.pose.bones:bone.matrix_basis.identity()
  # This shirt was reconstructed from vanilla geometry; its earlier approximate
  # weights are deliberately discarded, rather than presented as vanilla skin.
  world=shirt.matrix_world.copy();shirt.parent=None;shirt.matrix_world=world
  shirt.modifiers.clear();shirt.vertex_groups.clear();shirt.name='REFERENCE_LegionGoon_Shirt08_STATIC'
  shirt['rig_status']='Static vanilla garment geometry; unweighted. Do not transfer old approximate weights.'
  body['rig_status']='Official JA3 Male sample with native sample weights; use this skeleton for armor rigging.'
  mannequin=bpy.data.materials.new('Matte mannequin reference');mannequin.use_nodes=True
  shader=mannequin.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=(.20,.16,.12,1);shader.inputs['Roughness'].default_value=.85
  body.data.materials.clear();body.data.materials.append(mannequin)
  for mat in shirt.data.materials:
   if mat and mat.use_nodes:mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.9
  body.hide_select=True;shirt.hide_select=True
  for obj in armor:
   assert not obj.modifiers and not obj.vertex_groups and obj.parent is None
   obj['rig_target']='Bip001';obj['rig_status']='Unbound clean donor; fit and assign weights manually'
  text=bpy.data.texts.new('START_HERE.txt')
  text.write('JA3 armor rig preparation\n\nArmor: clean donor components, original coordinates, no weights or modifiers.\nTarget skeleton: Bip001, official JA3 Male, REST display. Preserve bone names, rest matrices and scale.\nBody: official sample with its native weights.\nRed shirt: static NPCCostumeMale_Shirt_08 geometry. Old approximate weights removed.\nFit armor components to the clothing before binding; this scene is not a finished fit or game export.\nRigid steel plates should keep their shape; use flexible weight transitions at joints and straps.\nOriginal nine clean files remain in the parent folder.\n')
  bpy.context.view_layer.update();assert signature()==before
  scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=True
  scene.render.resolution_x=850;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
  target=Vector((0,0,1.20));scene.camera.location=(-1,-3,1.9);rotation=(target-scene.camera.location).to_track_quat('-Z','Y');scene.camera.rotation_euler=rotation.to_euler();scene.camera.data.ortho_scale=1.65
  for screen in bpy.data.screens:
   for area in screen.areas:
    if area.type=='VIEW_3D':
     sp=area.spaces.active;sp.region_3d.view_location=target;sp.region_3d.view_distance=2.2;sp.region_3d.view_rotation=rotation;sp.shading.type='MATERIAL'
  bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(name+'.blend')))
  # One visual check per geometry, not nine repeated geometry checks.
  if family=='Twaron':
   for side,loc in [('front',(-1,-3,1.9)),('back',(1,3,1.9))]:
    scene.camera.location=loc;scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(a.output/(name+'_'+side+'.png'));bpy.ops.render.render(write_still=True)
  rows.append({'file':name+'.blend','armor_geometry_unchanged':True,'skeleton':'Bip001','armor_bound':False,'shirt':'static vanilla geometry'})
(a.output/'manifest.json').write_text(json.dumps(rows,indent=2))
print('PASS nine rig-preparation scenes; clean geometry preserved, reference skeleton included')
