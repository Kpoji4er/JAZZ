"""Blender: apply Meshy maps to canonical cleaned blend without importing output geometry."""
import argparse, hashlib, json, sys
from pathlib import Path
import bpy

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--source',type=Path,required=True)
p.add_argument('--maps',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
a.output.mkdir(parents=True,exist_ok=True)
if (a.output/'PASGT.blend').exists(): raise RuntimeError('Use a new output directory')
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
objects=[o for o in bpy.context.scene.objects if o.type=='MESH']
def geometry():
    return {o.name:{'positions':[list(v.co) for v in o.data.vertices],
                    'polygons':[list(f.vertices) for f in o.data.polygons],
                    'uv':[[list(x.uv) for x in layer.data] for layer in o.data.uv_layers],
                    'matrix':[list(r) for r in o.matrix_world]} for o in objects}
before=geometry()
mat=bpy.data.materials.new('PASGT_Woodland_UserReference');mat.use_nodes=True
n=mat.node_tree.nodes;l=mat.node_tree.links;bs=n.get('Principled BSDF')
files={}
for key,socket,space in [('base_color','Base Color','sRGB'),('roughness','Roughness','Non-Color'),('metallic','Metallic','Non-Color'),('normal',None,'Non-Color')]:
    path=a.maps/f'texture_0_{key}.png'
    image=bpy.data.images.load(str(path.resolve()));image.colorspace_settings.name=space;image.pack()
    tex=n.new('ShaderNodeTexImage');tex.image=image
    if key=='normal':
        normal=n.new('ShaderNodeNormalMap');l.new(tex.outputs['Color'],normal.inputs['Color']);l.new(normal.outputs['Normal'],bs.inputs['Normal'])
    else:l.new(tex.outputs['Color'],bs.inputs[socket])
    files[key]={'file':str(path.resolve()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':list(image.size)}
for o in objects:
    o.data.materials.clear();o.data.materials.append(mat)
    for f in o.data.polygons:f.material_index=0
assert geometry()==before, 'Material assignment changed geometry or UVs'
bpy.ops.wm.save_as_mainfile(filepath=str((a.output/'PASGT.blend').resolve()))
bpy.ops.export_scene.gltf(filepath=str((a.output/'PASGT.glb').resolve()),export_format='GLB',export_animations=False)
report={'source':str(a.source.resolve()),'source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),
        'positions_topology_uv_transforms_unchanged':True,'textures':files,'mesh_source':'clean-v3; Meshy retexture geometry not imported'}
(a.output/'material-transfer.json').write_text(json.dumps(report,indent=2))
(a.output/'render-manifest.json').write_text(json.dumps({'jobs':[{'name':'woodland','project':str(a.output.resolve()),'model':str((a.output/'PASGT.glb').resolve())}]},indent=2))
print(json.dumps(report))
