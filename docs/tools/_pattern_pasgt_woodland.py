"""Blender: project supplied woodland at fixed physical scale; bake onto existing UV."""
import argparse,json,sys,hashlib
from pathlib import Path
import bpy

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,required=True);p.add_argument('--pattern',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
if (a.output/'PASGT.blend').exists():raise RuntimeError('Fresh output required')
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
obj=next(o for o in bpy.context.scene.objects if o.type=='MESH')
def state():return ([tuple(v.co) for v in obj.data.vertices],[tuple(f.vertices) for f in obj.data.polygons],[[tuple(x.uv) for x in u.data] for u in obj.data.uv_layers])
before=state();mat=obj.data.materials[0];n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF');out=n.get('Material Output')
lo=[min(v.co[i] for v in obj.data.vertices) for i in range(3)];hi=[max(v.co[i] for v in obj.data.vertices) for i in range(3)]
attr=obj.data.color_attributes.new(name='WoodlandClothMask',type='FLOAT_COLOR',domain='CORNER')
for f in obj.data.polygons:
    c=f.center; x,y,z=[(c[i]-lo[i])/(hi[i]-lo[i]) for i in range(3)];edge=min(x,1-x)
    inward=f.normal.x*(x-.5)+f.normal.y*(y-.5)<-.12
    vertical=.085<edge<.19 and .53<z<.765
    front_strap=y<.5 and .12<edge<.34 and .475<z<.54
    back_strap=y>.5 and edge<.28 and (.175<z<.24 or .325<z<.39)
    cloth=0.0 if inward or vertical or front_strap or back_strap else 1.0
    for idx in f.loop_indices:attr.data[idx].color=(cloth,cloth,cloth,1)
old=bs.inputs['Base Color'].links[0].from_socket
coord=n.new('ShaderNodeTexCoord');scale=n.new('ShaderNodeVectorMath');scale.operation='MULTIPLY';scale.inputs[1].default_value=(.46,.31,1.65);l.new(coord.outputs['Generated'],scale.inputs[0])
tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(a.pattern.resolve()));tex.image.pack();tex.projection='BOX';tex.projection_blend=.06;l.new(scale.outputs['Vector'],tex.inputs['Vector'])
# Use the explicit cloth-zone mask to leave webbing and lining olive.
# This is material-only and cannot alter positions or the original UV layout.
mask=n.new('ShaderNodeVertexColor');mask.layer_name='WoodlandClothMask'
mix=n.new('ShaderNodeMixRGB');l.new(mask.outputs['Color'],mix.inputs[0]);mix.inputs[1].default_value=(.105,.125,.06,1);l.new(tex.outputs['Color'],mix.inputs[2])
em=n.new('ShaderNodeEmission');l.new(mix.outputs[0],em.inputs[0]);l.new(em.outputs[0],out.inputs['Surface'])
image=bpy.data.images.new('PASGT_Woodland_Large_Base',width=4096,height=4096);image.colorspace_settings.name='sRGB'
target=n.new('ShaderNodeTexImage');target.image=image
for node in n:node.select=False
target.select=True;n.active=target
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=1;s.render.bake.margin=16
bpy.ops.object.bake(type='EMIT')
image.filepath_raw=str((a.output/'Base.png').resolve());image.file_format='PNG';image.save();image.pack()
# Deliver a separate editable mask and monochrome base, not just a flattened map.
for name,color_socket,color in [('ClothMask',mask.outputs['Color'],None),('OliveBase',None,(.105,.125,.06,1))]:
    extra=bpy.data.images.new(name,width=4096,height=4096)
    target.image=extra
    for link in list(em.inputs[0].links):l.remove(link)
    if color_socket:l.new(color_socket,em.inputs[0])
    else:em.inputs[0].default_value=color
    bpy.ops.object.bake(type='EMIT');extra.filepath_raw=str((a.output/(name+'.png')).resolve());extra.file_format='PNG';extra.save();extra.pack()
target.image=image
l.new(target.outputs['Color'],bs.inputs['Base Color']);l.new(bs.outputs['BSDF'],out.inputs['Surface'])
# Strip unused projection nodes so the exported GLB uses only the baked UV map.
for node in [coord,scale,tex,mask,mix,em]:n.remove(node)
assert state()==before
bpy.ops.wm.save_as_mainfile(filepath=str((a.output/'PASGT.blend').resolve()))
bpy.ops.export_scene.gltf(filepath=str((a.output/'PASGT.glb').resolve()),export_format='GLB',export_animations=False)
(a.output/'report.json').write_text(json.dumps({'source':str(a.source),'pattern':str(a.pattern),'geometry_and_uv_unchanged':True,'projection_scale':[.46,.31,1.65],'normal_roughness_metallic':'unchanged'},indent=2))
(a.output/'render-manifest.json').write_text(json.dumps({'jobs':[{'name':'large-woodland','project':str(a.output.resolve()),'model':str((a.output/'PASGT.glb').resolve())}]}))
