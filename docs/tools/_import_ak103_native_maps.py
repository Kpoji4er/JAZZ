"""Rebuild existing AK103 rig with native archive UV/PBR, without launching JA3.

Blender --python ... -- --archive <zip> --reference <installed rig blend>
--build <new build> --game-root <JA3_ROOT>. Does not install into active mods.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import math

import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _build_ak103_archive import import_assembled, orient_and_scale, zero_at_butt, group_modules, world_bbox
from _export_ak103_assets import load_hge
from _export_m14_family_assets import assign_hge_maps, export_fbx, save_tga
from _ja3_mesh_prepare import prepare_export_mesh
from _inspect_weapon_source import setup_render, render_views

MAPS = {
    0:'Weapon_AK-103', 1:'ksk', 2:'Handguard_AK103', 3:'Bolt_group',
    4:'Dovetail_AK-103', 5:'mag_ak_762x39_izhmash_103', 6:'Muzzlebrake',
    7:'Gascover', 8:'Gastube', 9:None, 10:'Pistolgrip',
    11:'Rearsight', 12:'Stock',
}


def atlas_material(obj,hge,dest):
    materials=list(obj.data.materials)
    if len(materials)<=1:return
    grid=2**math.ceil(math.log2(math.ceil(math.sqrt(len(materials)))))
    size=1024; side=size*grid
    arrays={key:np.zeros((side,side,4),np.float32) for key in ('Base','Normal','RM')}
    arrays['Normal'][:,:,:]=(.5,.5,1,1)
    arrays['RM'][:,:,:]=(.5,0,0,1)
    for i,mat in enumerate(materials):
        x,y=(i%grid)*size,(i//grid)*size
        for key in arrays:
            node=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.label==key)
            im=bpy.data.images.load(bpy.path.abspath(node.image.filepath),check_existing=False)
            im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color';im.scale(size,size)
            values=np.empty(size*size*4,np.float32);im.pixels.foreach_get(values);bpy.data.images.remove(im)
            arrays[key][y:y+size,x:x+size]=values.reshape(size,size,4)
    uv=obj.data.uv_layers.active
    for poly in obj.data.polygons:
        x,y=poly.material_index%grid,poly.material_index//grid
        for loop in poly.loop_indices:
            u,v=uv.data[loop].uv
            assert -.001<=u<=1.001 and -.001<=v<=1.001,(obj.name,u,v)
            uv.data[loop].uv=((u+x)/grid,(v+y)/grid)
        poly.material_index=0
    images={k:save_tga(obj.name+'_NativeAtlas_'+k,v,dest,k=='Base') for k,v in arrays.items()}
    mat=bpy.data.materials.new(obj.name+'_NativeAtlas');mat.use_nodes=True
    shader=mat.node_tree.nodes.get('Principled BSDF');nodes=mat.node_tree.nodes;links=mat.node_tree.links
    for key,im in images.items():
        node=nodes.new('ShaderNodeTexImage');node.image=im;node.label=key
        if key=='Base':links.new(node.outputs['Color'],shader.inputs['Base Color']);base=node
        elif key=='Normal':
            normal=nodes.new('ShaderNodeNormalMap');links.new(node.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs['Normal'],shader.inputs['Normal'])
        else:
            sep=nodes.new('ShaderNodeSeparateColor');links.new(node.outputs['Color'],sep.inputs['Color'])
            links.new(sep.outputs['Red'],shader.inputs['Roughness']);links.new(sep.outputs['Blue'],shader.inputs['Metallic'])
    nodes.active=base;assign_hge_maps(hge,mat,images)
    obj.data.materials.clear();obj.data.materials.append(mat)


def clean_mesh(obj):
    issues = prepare_export_mesh(obj, strict=False)
    bad = {i['triangle'] for i in issues if i['kind'] in ('degenerate','zero_normal')}
    if bad:
        obj.data.calc_loop_triangles()
        ids = {obj.data.loop_triangles[i].polygon_index for i in bad}
        bm = bmesh.new(); bm.from_mesh(obj.data); bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm, geom=[bm.faces[i] for i in ids], context='FACES')
        bm.to_mesh(obj.data); bm.free(); obj.data.update()
    prepare_export_mesh(obj)
    return len(bad)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('archive','reference','build','game-root'): p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--cover-prefix', help='Verified texture prefix for model_9 dust cover; never assume the receiver map')
    a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
    if not a.cover_prefix:
        p.error('model_9 dust-cover material is unverified: provide its verified --cover-prefix; receiver texture fallback is rejected')
    MAPS[9]=a.cover_prefix
    a.build.mkdir(parents=True,exist_ok=True)
    source=a.build/'source';source.mkdir(exist_ok=True)
    digest=hashlib.sha256(a.archive.read_bytes()).hexdigest()
    with zipfile.ZipFile(a.archive) as z:
        for member in z.infolist():
            if member.is_dir():continue
            dest=(source/member.filename).resolve()
            assert dest.is_relative_to(source.resolve())
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(member))
    hge=load_hge(a.game_root)
    meshes=import_assembled(source)
    orient_and_scale(meshes);zero_at_butt(meshes)
    tex=a.build/'Textures';tex.mkdir(exist_ok=True)
    cache={}
    for obj in meshes:
        prefix=MAPS[int(obj.name.split('_')[1])]
        if prefix not in cache:
            maps={}
            for key,suffix in [('Base','BaseColor'),('Normal','Normal'),('Rough','Roughness'),('Metal','Metallic'),('AO','AO')]:
                path=source/(prefix+'_'+suffix+'.png')
                if not path.exists():continue
                im=bpy.data.images.load(str(path),check_existing=False)
                im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color'
                im.scale(2048,2048)
                arr=np.empty(2048*2048*4,np.float32);im.pixels.foreach_get(arr)
                maps[key]=arr.reshape(2048,2048,4);bpy.data.images.remove(im)
            assert all(k in maps for k in ('Base','Normal','Rough','Metal')),prefix
            rm=np.ones_like(maps['Rough']);rm[:,:,0]=maps['Rough'][:,:,0];rm[:,:,1]=0;rm[:,:,2]=maps['Metal'][:,:,0]
            maps['RM']=rm
            images={k:save_tga('AKR_AK103_'+prefix+'_'+k,v,tex,k=='Base') for k,v in maps.items() if k in ('Base','Normal','RM','AO')}
            mat=bpy.data.materials.new('AKR_AK103_'+prefix);mat.use_nodes=True
            shader=mat.node_tree.nodes.get('Principled BSDF');nodes=mat.node_tree.nodes;links=mat.node_tree.links
            for key,im in images.items():
                node=nodes.new('ShaderNodeTexImage');node.image=im;node.label=key
                if key=='Base':links.new(node.outputs['Color'],shader.inputs['Base Color']);base=node
                elif key=='Normal':
                    normal=nodes.new('ShaderNodeNormalMap');links.new(node.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs['Normal'],shader.inputs['Normal'])
                elif key=='RM':
                    sep=nodes.new('ShaderNodeSeparateColor');links.new(node.outputs['Color'],sep.inputs['Color'])
                    links.new(sep.outputs['Red'],shader.inputs['Roughness']);links.new(sep.outputs['Blue'],shader.inputs['Metallic'])
            nodes.active=base;assign_hge_maps(hge,mat,images);cache[prefix]=mat
        obj.data.materials.clear();obj.data.materials.append(cache[prefix])
    grouped=group_modules(meshes)
    clean=a.build/'clean';clean.mkdir(exist_ok=True)
    clean_path=clean/'AK103.blend';bpy.ops.wm.save_as_mainfile(filepath=str(clean_path))
    bpy.ops.wm.open_mainfile(filepath=str(a.reference),use_scripts=False)
    with bpy.data.libraries.load(str(clean_path),link=False) as (src,dst):
        dst.objects=[n for n in src.objects if n=='AK103' or n.startswith('AK103_')]
    incoming={o.name:o for o in dst.objects if o and o.type=='MESH'}
    for obj in incoming.values():bpy.context.scene.collection.objects.link(obj)
    old_mag=bpy.data.objects['AKR_AK103_Magazine'];new_mag=incoming['AK103_Magazine']
    old_bounds=world_bbox([old_mag]);new_bounds=world_bbox([new_mag])
    shift=(old_bounds[0]+old_bounds[1]-new_bounds[0]-new_bounds[1])/2
    report={'source_sha256':digest,'mapping':MAPS,'shift_m':list(shift),'entities':{}}
    for name,obj in incoming.items():
        target=bpy.data.objects['AKR_'+name]
        data=obj.data.copy();data.transform(target.matrix_world.inverted()@Matrix.Translation(shift)@obj.matrix_world)
        target.data=data
        bpy.data.objects.remove(obj,do_unlink=True)
        bpy.ops.object.select_all(action='DESELECT');target.hide_set(False);target.select_set(True);bpy.context.view_layer.objects.active=target
        # Local weld only; per-loop UVs retain original material seams.
        bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=0.000001);bpy.ops.object.mode_set(mode='OBJECT')
        removed=clean_mesh(target)
        if len(target.data.loops)>59000:
            mod=target.modifiers.new('Safe uint16 corner budget','DECIMATE');mod.ratio=57000/len(target.data.loops)
            bpy.ops.object.modifier_apply(modifier=mod.name);removed+=clean_mesh(target)
        assert len(target.data.loops)<60000,(target.name,len(target.data.loops))
        atlas_material(target,hge,tex)
        report['entities'][target.name]={'triangles':len(target.data.polygons),'corners':len(target.data.loops),'removed_degenerate':removed,'materials':[m.name for m in target.data.materials]}
    stock=bpy.data.objects['AKR_AK103_Stock'];folded=bpy.data.objects['AKR_AK103_StockFolded']
    folded.data=stock.data.copy();folded.data.transform(Matrix.Rotation(np.pi,4,'Z'));clean_mesh(folded)
    folded.hide_render=True
    rigged=a.build/'rigged';rigged.mkdir(exist_ok=True)
    visible=[o for o in bpy.context.scene.objects if o.type=='MESH' and o!=folded]
    lo,hi=world_bbox(visible);report['length_m']=hi.y-lo.y
    assert abs(report['length_m']-.943)<.001,report['length_m']
    bpy.ops.wm.save_as_mainfile(filepath=str(rigged/'AK103_JA3.blend'))
    export_fbx(hge,rigged/'AK103_JA3.fbx')
    review=a.build/'review';review.mkdir(exist_ok=True);setup_render(1400,'TEXTURE')
    render_views(review,'AK103',lo,hi)
    assert hashlib.sha256(a.archive.read_bytes()).hexdigest()==digest
    (a.build/'native-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
