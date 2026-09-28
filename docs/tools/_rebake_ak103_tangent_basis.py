"""Rebake archive shading onto prepared AK103 normals; staging only.

Blender --background --python this.py -- --native BUILD --out BUILD --game-root ROOT
Reads the original source corner normals for projection; never writes custom
normals to the target or exports the source. Preserves target geometry and UVs.
Requires a native build made with the owner's verified cover prefix ksk.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _export_ak103_assets import load_hge
from _export_m14_family_assets import assign_hge_maps, export_fbx, save_tga
from _restore_ak103_materials import geometry_digest, pixels

p=argparse.ArgumentParser(description=__doc__)
for arg in ('native','out','game-root'):p.add_argument('--'+arg,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
assert a.native.resolve()!=a.out.resolve()
report=json.loads((a.native/'native-report.json').read_text())
assert report['mapping']['9']=='ksk'
tex=a.out/'Textures';tex.mkdir(parents=True,exist_ok=True)
rig=a.out/'rigged';rig.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.native/'rigged/AK103_JA3.blend'),use_scripts=False)
targets={o.name:o for o in bpy.context.scene.objects if o.type=='MESH' and o.name.startswith('AKR_AK103')}
assert len(targets)==6
for im in bpy.data.images:
    if im.filepath:im.filepath=bpy.path.abspath(im.filepath)
before={n:geometry_digest(o.data) for n,o in targets.items()}
uv_before={n:hashlib.sha256(np.array([l.uv[:] for l in o.data.uv_layers.active.data]).tobytes()).hexdigest() for n,o in targets.items()}
with bpy.data.libraries.load(str(a.native/'clean/AK103.blend'),link=False) as (src,dst):
    dst.objects=[n for n in src.objects if n=='AK103' or n.startswith('AK103_')]
sources={o.name:o for o in dst.objects if o and o.type=='MESH'}
shift=Vector(report['shift_m'])
for o in sources.values():
    bpy.context.scene.collection.objects.link(o)
    o.matrix_world=Matrix.Translation(shift)@o.matrix_world
    o.hide_render=True
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=1
scene.render.bake.use_selected_to_active=True
scene.render.bake.use_clear=True
scene.render.bake.margin=16
scene.render.bake.cage_extrusion=.002
scene.render.bake.max_ray_distance=.008
scene.render.bake.normal_space='TANGENT'
hge=load_hge(a.game_root)
result={'native':str(a.native),'source_custom_normals_read_only':True,'targets':{}}
for name,target in targets.items():
    if name.endswith('StockFolded'):continue
    assert not target.data.has_custom_normals,name
    source=sources[name.removeprefix('AKR_')]
    size=4096 if name=='AKR_AK103' else 2048
    baked=bpy.data.images.new(name+'_RebasedNormal',width=size,height=size,alpha=True,float_buffer=False)
    baked.colorspace_settings.name='Non-Color';baked.generated_color=(.5,.5,1,1)
    for mat in target.data.materials:
        node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=baked
        mat.node_tree.nodes.active=node
    for ob in scene.objects:
        if ob.type=='MESH':ob.hide_render=True
    bpy.ops.object.select_all(action='DESELECT')
    for ob in (source,target):ob.hide_set(False);ob.hide_render=False;ob.select_set(True)
    bpy.context.view_layer.objects.active=target
    bpy.ops.object.bake(type='NORMAL')
    normal=pixels(baked)
    assert np.isfinite(normal).all()
    # Save actual bake before material rebinding; neutral padding remains neutral.
    normal_image=save_tga(name+'_RebasedNormal',normal,tex,False)
    mat=target.data.materials[0];images={}
    for node in list(mat.node_tree.nodes):
        if node.type!='TEX_IMAGE':continue
        key=node.label
        if key not in ('Base','Normal','RM','AO'):
            mat.node_tree.nodes.remove(node);continue
        if key=='Normal':node.image=normal_image
        else:
            arr=pixels(node.image)
            if key=='RM':arr[:,:,0]=np.maximum(arr[:,:,0],.52 if name.endswith(('Stock','Magazine')) else .44)
            node.image=save_tga(name+'_'+key,arr,tex,key=='Base')
        images[key]=node.image
    assign_hge_maps(hge,mat,images)
    result['targets'][name]={'size':size,'triangles':len(target.data.polygons),'source_triangles':len(source.data.polygons),'source_has_custom_normals':source.data.has_custom_normals}
    source.hide_render=True
    print('BAKED',name,flush=True)
stock=targets['AKR_AK103_Stock'];fold=targets['AKR_AK103_StockFolded']
fold.data.materials.clear()
for mat in stock.data.materials:fold.data.materials.append(mat)
for ob in list(sources.values()):bpy.data.objects.remove(ob,do_unlink=True)
for name,o in targets.items():
    assert geometry_digest(o.data)==before[name],name
    assert hashlib.sha256(np.array([l.uv[:] for l in o.data.uv_layers.active.data]).tobytes()).hexdigest()==uv_before[name],name
    assert not o.data.has_custom_normals,name
    o.hide_render=name.endswith('StockFolded')
    result['targets'].setdefault(name,{})['geometry_normals_uv_unchanged']=True
bpy.ops.wm.save_as_mainfile(filepath=str(rig/'AK103_JA3.blend'))
export_fbx(hge,rig/'AK103_JA3.fbx')
(a.out/'rebake-report.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('DONE; candidate only, not installed')
