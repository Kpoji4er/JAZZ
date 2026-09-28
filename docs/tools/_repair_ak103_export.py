"""Repair AK103 export budget/materials and receiver optic anchors.
Blender --python this.py -- --source <rigged blend> --output <new build>
--game-root <JA3_ROOT> --assets <jazz_assets>. No active-mod writes.
Require a decoded-HGM comparison after AssetsProcessor; blend QA alone is insufficient.
"""
import argparse,json,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_ak103_assets import load_hge,ent_spots
from _ja3_mesh_prepare import prepare_export_mesh
from _export_m14_family_assets import assign_hge_maps,export_fbx
from _render_m14_family_icons import render_one
p=argparse.ArgumentParser()
for n in ('source','output','game-root','assets'):p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
hge=load_hge(a.game_root);bpy.ops.wm.open_mainfile(filepath=str(a.source))
body=bpy.data.objects['AKR_AK103']
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);bpy.context.view_layer.objects.active=body
before=len(body.data.polygons)
mod=body.modifiers.new('Export vertex budget','DECIMATE');mod.ratio=.32
bpy.ops.object.modifier_apply(modifier=mod.name)
issues=prepare_export_mesh(body,strict=False)
bad={i['triangle'] for i in issues if i['kind'] in ('degenerate','zero_normal')}
if bad:
    bm=bmesh.new();bm.from_mesh(body.data);bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in bad],context='FACES_ONLY')
    bm.to_mesh(body.data);bm.free()
prepare_export_mesh(body)
# Every corner may split at an UV/tangent seam. Bound the worst-case vertex
# count below uint16 instead of trusting only Blender's shared-vertex count.
assert len(body.data.loops)<60000,len(body.data.loops)
akm=ent_spots(a.assets/'Entities/AKM.ent')
for obj in bpy.data.objects:
    if obj.type!='EMPTY':continue
    name=obj.hge_obj_settings.spot_name
    if name in ('General','Scope','Mount'):
        obj.location=akm[name]+Vector((0,0,-.01064))
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=1
sc.render.bake.use_clear=True;sc.render.bake.margin=8
sc.render.bake.use_selected_to_active=False
report={'body_before':before,'body_after':len(body.data.polygons),'corner_budget':len(body.data.loops),'materials':{}}
meshes=[o for o in bpy.data.objects if o.type=='MESH']
folded=bpy.data.objects['AKR_AK103_StockFolded']
for obj in meshes:
    prepare_export_mesh(obj)
    if obj==folded:continue
    mat=bpy.data.materials.new(obj.name+'_Repair');mat.use_nodes=True
    nodes=mat.node_tree.nodes;nodes.clear();links=mat.node_tree.links
    out=nodes.new('ShaderNodeOutputMaterial');emit=nodes.new('ShaderNodeEmission');links.new(emit.outputs[0],out.inputs['Surface'])
    geo=nodes.new('ShaderNodeNewGeometry');sep=nodes.new('ShaderNodeSeparateXYZ');links.new(geo.outputs['Position'],sep.inputs[0])
    plastic=nodes.new('ShaderNodeValue');plastic.outputs[0].default_value=0 if obj in (body,bpy.data.objects['AKR_AK103_Muzzle']) else 1
    if obj==body:
        low=nodes.new('ShaderNodeMath');low.operation='LESS_THAN';low.inputs[1].default_value=.02;links.new(sep.outputs['Z'],low.inputs[0])
        rear=nodes.new('ShaderNodeMath');rear.operation='GREATER_THAN';rear.inputs[1].default_value=-.055;links.new(sep.outputs['Y'],rear.inputs[0])
        both=nodes.new('ShaderNodeMath');both.operation='MULTIPLY';links.new(low.outputs[0],both.inputs[0]);links.new(rear.outputs[0],both.inputs[1]);plastic=both
    base=nodes.new('ShaderNodeMixRGB');base.inputs[1].default_value=(.055,.061,.067,1);base.inputs[2].default_value=(.019,.022,.024,1);links.new(plastic.outputs[0],base.inputs[0])
    noise=nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=350;noise.inputs['Detail'].default_value=2;links.new(geo.outputs['Position'],noise.inputs['Vector'])
    grain=nodes.new('ShaderNodeMath');grain.operation='MULTIPLY_ADD';grain.inputs[1].default_value=.12;grain.inputs[2].default_value=.94;links.new(noise.outputs['Fac'],grain.inputs[0])
    color=nodes.new('ShaderNodeMixRGB');color.blend_type='MULTIPLY';color.inputs[0].default_value=1;links.new(base.outputs[0],color.inputs[1]);links.new(grain.outputs[0],color.inputs[2])
    rough=nodes.new('ShaderNodeMath');rough.operation='MULTIPLY_ADD';rough.inputs[1].default_value=.22;rough.inputs[2].default_value=.43;links.new(plastic.outputs[0],rough.inputs[0])
    metal=nodes.new('ShaderNodeMath');metal.operation='SUBTRACT';metal.inputs[0].default_value=1;links.new(plastic.outputs[0],metal.inputs[1])
    packed=nodes.new('ShaderNodeCombineColor');links.new(rough.outputs[0],packed.inputs[0]);links.new(metal.outputs[0],packed.inputs[2])
    obj.data.materials.clear();obj.data.materials.append(mat)
    bpy.ops.object.select_all(action='DESELECT');obj.hide_render=False;obj.select_set(True);bpy.context.view_layer.objects.active=obj
    for other in meshes:
        if other!=obj:other.hide_render=True
    images={}
    for key,source in [('Base',color.outputs[0]),('RM',packed.outputs[0])]:
        im=bpy.data.images.new(obj.name+'_'+key,width=1024,height=1024,alpha=False)
        im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color'
        target=nodes.new('ShaderNodeTexImage');target.image=im;nodes.active=target
        links.new(source,emit.inputs['Color']);bpy.ops.object.bake(type='EMIT')
        im.filepath_raw=str(a.output/(obj.name+'_'+key+'.tga'));im.file_format='TARGA_RAW';im.save();images[key]=im
    normal=bpy.data.images.new(obj.name+'_Normal',width=128,height=128,alpha=False)
    normal.colorspace_settings.name='Non-Color'
    normal.pixels.foreach_set([.5,.5,1,1]*(128*128))
    normal.filepath_raw=str(a.output/(obj.name+'_Normal.tga'));normal.file_format='TARGA_RAW';normal.save();images['Normal']=normal
    assign_hge_maps(hge,mat,images)
    # Preview shader reads the exact baked maps, not a separate artistic shader.
    nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');bsdf=nodes.new('ShaderNodeBsdfPrincipled')
    tex=nodes.new('ShaderNodeTexImage');tex.image=images['Base'];nodes.active=tex
    links.new(tex.outputs[0],bsdf.inputs['Base Color']);links.new(bsdf.outputs[0],out.inputs['Surface'])
    report['materials'][obj.name]={k:v.filepath_raw for k,v in images.items()}
folded.data.materials.clear();folded.data.materials.append(bpy.data.objects['AKR_AK103_Stock'].data.materials[0])
for obj in meshes:obj.hide_render=False
folded.hide_render=True
blend=a.output/'AK103_JA3.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
export_fbx(hge,a.output/'AK103_JA3.fbx')
(a.output/'repair-report.json').write_text(json.dumps(report,indent=2))
render_one(blend,a.output/'preview.png')
bpy.context.scene.display.shading.color_type='TEXTURE';bpy.context.scene.render.filepath=str(a.output/'textured.png');bpy.ops.render.render(write_still=True)
