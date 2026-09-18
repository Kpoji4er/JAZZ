"""Create nine editable, unrigged HAV blends without modifying donor geometry."""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy
from mathutils import Vector

p=argparse.ArgumentParser()
for key in ('source','woodland','output'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
variants={'Light':['vest'],'Medium':['vest','belt','collar','groin'],'Full':['vest','belt','collar','groin','arms']}
reference={};rows=[]
for family in ('Twaron','Guardian','Zylon'):
 for variant,roles in variants.items():
  bpy.ops.wm.open_mainfile(filepath=str(a.source))
  parts=[bpy.data.objects['HAV_'+r] for r in roles]
  for obj in list(bpy.data.objects):
   if obj.type in ('MESH','ARMATURE') and obj not in parts:bpy.data.objects.remove(obj,do_unlink=True)
  signature=[];materials=set()
  for obj in parts:
   assert not obj.modifiers and not obj.data.shape_keys and obj.parent is None,obj.name
   obj.hide_render=False;obj.hide_set(False);obj.vertex_groups.clear()
   signature.append((obj.name,[list(v.co) for v in obj.data.vertices],[list(f.vertices) for f in obj.data.polygons],list(map(list,obj.matrix_world))))
   materials.update(obj.data.materials)
  digest=hashlib.sha256(json.dumps(signature).encode()).hexdigest()
  assert reference.setdefault(variant,digest)==digest
  for mat in materials:
   nodes=mat.node_tree.nodes;links=mat.node_tree.links;bsdf=nodes.get('Principled BSDF')
   old=bsdf.inputs['Base Color'].links[0].from_socket
   if family=='Guardian':
    hue=nodes.new('ShaderNodeHueSaturation');hue.inputs['Saturation'].default_value=0;hue.inputs['Value'].default_value=.28
    links.new(old,hue.inputs['Color']);links.new(hue.outputs['Color'],bsdf.inputs['Base Color'])
   elif family=='Zylon':
    tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(a.woodland),check_existing=True);tex.extension='REPEAT'
    coords=nodes.new('ShaderNodeTexCoord');split=nodes.new('ShaderNodeSeparateXYZ');links.new(coords.outputs['Object'],split.inputs[0])
    combine=nodes.new('ShaderNodeCombineXYZ')
    for axis,output,scale in [('X','X',1/1.8),('Y','Z',tex.image.size[0]/tex.image.size[1]/1.8)]:
     mul=nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=scale
     links.new(split.outputs[output],mul.inputs[0]);links.new(mul.outputs[0],combine.inputs[axis])
    links.new(combine.outputs[0],tex.inputs['Vector'])
    gray=nodes.new('ShaderNodeRGBToBW');links.new(old,gray.inputs[0])
    detail=nodes.new('ShaderNodeMapRange');detail.inputs['From Max'].default_value=.5;detail.inputs['To Min'].default_value=.45;detail.inputs['To Max'].default_value=1
    links.new(gray.outputs[0],detail.inputs['Value'])
    mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1
    links.new(detail.outputs[0],mix.inputs[1]);links.new(tex.outputs['Color'],mix.inputs[2]);links.new(mix.outputs[0],bsdf.inputs['Base Color'])
  for im in bpy.data.images:
   if im.source=='FILE' and im.has_data:im.pack()
  bpy.ops.object.select_all(action='DESELECT')
  for obj in parts:obj.select_set(True)
  bpy.context.view_layer.objects.active=parts[0]
  scene=bpy.context.scene;scene.cycles.device='CPU';scene.cycles.samples=24
  pts=[obj.matrix_world@v.co for obj in parts for v in obj.data.vertices]
  lo=Vector(tuple(min(v[i] for v in pts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in pts) for i in range(3)));center=(lo+hi)/2
  scene.camera.location=center+Vector((-1,-3,.7));rotation=(center-scene.camera.location).to_track_quat('-Z','Y')
  scene.camera.rotation_euler=rotation.to_euler();scene.camera.data.ortho_scale=max(hi-lo)*1.3
  for screen in bpy.data.screens:
   for area in screen.areas:
    if area.type=='VIEW_3D':
     space=area.spaces.active;space.shading.type='MATERIAL';space.region_3d.view_location=center;space.region_3d.view_distance=max(hi-lo)*1.8;space.region_3d.view_rotation=rotation
  name=family+variant;scene['asset_status']='Clean donor geometry; no rig, morph, body fitting or game export'
  bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(name+'.blend')))
  rows.append({'name':name,'parts':roles,'geometry_sha256':digest,'rigged':False})
(a.output/'manifest.json').write_text(json.dumps({'source':str(a.source),'geometry_configurations':3,'material_variants':9,'models':rows},indent=2))
print('PASS: nine packed blends, three unchanged donor geometries, no armatures/modifiers/shape keys')
