"""Blender CPU preview of supplied Heavy Armor Vest OBJ parts, without materials."""
import bpy,argparse,sys,json
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--textured',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
colors=[(.22,.12,.05),(.11,.20,.15),(.09,.12,.18)]
for i,file in enumerate(sorted(a.source.glob('*.obj'))):
 bpy.ops.wm.obj_import(filepath=str(file),forward_axis='NEGATIVE_Z',up_axis='Y')
 for obj in bpy.context.selected_objects:
  if obj.type!='MESH':continue
  obj.scale=(.01,.01,.01);obj.location.x=-.062
  bpy.context.view_layer.objects.active=obj;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  obj.data.materials.clear();m=bpy.data.materials.new(file.stem);m.use_nodes=True;m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(*colors[i],1);m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.7;obj.data.materials.append(m)
  if a.textured:
   nodes=m.node_tree.nodes;links=m.node_tree.links;bsdf=nodes['Principled BSDF']
   base,normal,packed=[(3,1,0),(7,5,4),(10,9,8)][i]
   def tex(name,noncolor=False):
    node=nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(a.source/name),check_existing=True)
    if noncolor:node.image.colorspace_settings.name='Non-Color'
    return node.outputs['Color']
   links.new(tex(f'gltf_embedded_{base}.png'),bsdf.inputs['Base Color'])
   nm=nodes.new('ShaderNodeNormalMap');links.new(tex(f'gltf_embedded_{normal}.png',True),nm.inputs['Color']);links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
   links.new(tex(f'gltf_embedded_{packed}@channels=G.png',True),bsdf.inputs['Roughness'])
   links.new(tex(f'gltf_embedded_{packed}@channels=B.png',True),bsdf.inputs['Metallic'])
   obj['source_role']=['belt','vest','limb_neck_groin_protection'][i]
   obj['material_mapping_status']='Reconstructed from texture atlas layout; glTF G roughness / B metallic convention'
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.resolution_x=800;scene.render.resolution_y=1000
scene.world=bpy.data.worlds.new('World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[1].default_value=.3
for loc,power in [((-2,-3,3),230),((2,-1,3),140),((1,2,3),200)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.size=2;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(2,-4,2.1));scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=1.95;scene.camera.rotation_euler=(Vector((0,0,.94))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
stem='donor-textured' if a.textured else 'donor-parts'
if a.textured:
 bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(stem+'.blend')));scene.render.filepath=str(a.output/(stem+'.png'));bpy.ops.render.render(write_still=True)
