"""HGE export of recovered SCAR L/H assemblies. Writes candidates, never installs.

Blender --background --factory-startup --python ... -- --assemblies DIR
--build DIR --game-root DIR. Requires six <L|H>_<Short|Standard|Long> scenes.
"""
import argparse
import json
import math
import sys
from pathlib import Path
import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge, assign_hge_maps
from _ja3_mesh_prepare import prepare_export_mesh, triangulate_without_custom_normals
from _render_ak103_icon import build_compositor

p=argparse.ArgumentParser()
for key in ('assemblies','build','game-root'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for folder in ('rigged','previews'):(a.build/folder).mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
hge=load_hge(a.game_root)
created={}
report={'entities':{},'runtime':'NOT_RUN'}
# Assembly X points forward; JA3 FBX convention points down -Y. Put the
# trigger at the shared firearm origin, without modifying source proportions.
transform=Matrix(((0,1,0,0),(-1,0,0,-.125),(0,0,1,.055),(0,0,0,1)))

def adopt(objects,name):
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects:
        ob.data.transform(ob.matrix_world)
        ob.matrix_world=Matrix.Identity(4)
        ob.data.transform(transform)
        ob.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    if len(objects)>1:bpy.ops.object.join()
    ob=objects[0];ob.name=name;created[name]=ob
    return ob

for caliber in ('L','H'):
    for length in ('Short','Standard','Long'):
        path=a.assemblies/f'{caliber}_{length}'/'SCAR-recovery.blend'
        with bpy.data.libraries.load(str(path),link=False) as (src,dst):
            dst.objects=[n for n in src.objects if n in ('Common','Upper','Lower','Stock','Magazine','RearSight','Muzzle')]
        loaded={o.name.split('.')[0]:o for o in dst.objects}
        for ob in loaded.values():bpy.context.collection.objects.link(ob)
        adopt([loaded[n] for n in ('Common','Upper','Lower','RearSight','Muzzle')],f'JAZZ_SCAR_{caliber}_{length}')
        if length=='Standard':adopt([loaded['Magazine']],f'JAZZ_SCAR_{caliber}_Magazine')
        else:bpy.data.objects.remove(loaded['Magazine'],do_unlink=True)
        if caliber=='L' and length=='Standard':adopt([loaded['Stock']],'JAZZ_SCAR_Stock')
        else:bpy.data.objects.remove(loaded['Stock'],do_unlink=True)

stock=created['JAZZ_SCAR_Stock']
folded=stock.copy();folded.data=stock.data.copy();bpy.context.collection.objects.link(folded)
folded.name='JAZZ_SCAR_StockFolded';created[folded.name]=folded
hinge=transform@Vector((-.22,-.027,.01))
folded.data.transform(Matrix.Translation(hinge)@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation(-hinge))

converted={}
for ob in created.values():
    for index,mat in enumerate(ob.data.materials):
        prefix=mat.name.split('.')[0]
        if prefix in converted:ob.data.materials[index]=converted[prefix];continue
        images={}
        for node in mat.node_tree.nodes:
            if node.type!='TEX_IMAGE' or not node.image:continue
            stem=Path(node.image.filepath).stem
            key='Base' if stem.endswith('_BaseColor') else 'Normal' if stem.endswith('_Normal') else 'RM' if stem.endswith('_RM') else None
            if key:images[key]=node.image
        assert set(images)=={'Base','Normal','RM'},(prefix,images)
        assign_hge_maps(hge,mat,images)
        converted[prefix]=mat
    triangulate_without_custom_normals(ob)
    issues=prepare_export_mesh(ob,strict=False)
    assert not issues,(ob.name,issues[:5])
    assert not ob.data.has_custom_normals
    origin=bpy.data.objects.new(ob.name+'_Origin',None);bpy.context.collection.objects.link(origin);ob.parent=origin
    settings=ob.hge_obj_settings
    settings.entity=ob.name;settings.mesh='Mesh';settings.state='idle';settings.lod=1;settings.ignore=False;ob.hge_export=True
    if ob.name.endswith(('Short','Standard','Long')):
        x=2.176 if '_H_' in ob.name else 0
        muzzle=min(v.co.y for v in ob.data.vertices)
        spots={'Magazine':(0,0,0),'Stock':(0,0,0),'Barrel':(0,0,0),
               'Scope':(0,-.025,.110),'Under':(0,-.225-x*.01,.027),
               'Side':(-.028,-.245-x*.01,.05),'Muzzle':(0,muzzle,.0527),
               'MuzzleTip':(0,muzzle,.0527),'Trigger':(0,0,.005),
               'Hand_l_grip':(0,-.225-x*.01,.030)}
        for name,pos in spots.items():
            spot=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(spot)
            spot.parent=ob;spot.location=pos;spot.hge_obj_settings.spot_name=name
    report['entities'][ob.name]={'triangles':len(ob.data.polygons),'custom_normals':False}
    bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);origin.select_set(True)
    for child in ob.children:child.select_set(True)
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(a.build/'rigged'/(ob.name+'.fbx')),use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged/SCAR_JA3.blend'))
(a.build/'build-report.json').write_text(json.dumps(report,indent=2))

scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE_NEXT'
scene.render.film_transparent=True;scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard'
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[1].default_value=.65
for name,loc,power in [('Key',(-2,-1,3),500),('Fill',(2,0,1),300)]:
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.size=3
    ob=bpy.data.objects.new(name,ld);scene.collection.objects.link(ob);ob.location=loc
    ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
data=bpy.data.cameras.new('Camera');data.type='ORTHO';data.ortho_scale=1.15
camera=bpy.data.objects.new('Camera',data);scene.collection.objects.link(camera);scene.camera=camera
target=Vector((0,-.10,-.015));camera.location=target+Vector((-2,0,0));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
build_compositor(scene)
scene.render.resolution_x=324;scene.render.resolution_y=165;scene.render.resolution_percentage=100
for caliber in ('L','H'):
    for length in ('Short','Standard','Long'):
        for fold in (False,True):
            names={f'JAZZ_SCAR_{caliber}_{length}',f'JAZZ_SCAR_{caliber}_Magazine','JAZZ_SCAR_StockFolded' if fold else 'JAZZ_SCAR_Stock'}
            for name,ob in created.items():ob.hide_render=name not in names
            scene.render.filepath=str(a.build/'previews'/f'SCAR_{caliber}_{length}{"_Folded" if fold else ""}.png')
            bpy.ops.render.render(write_still=True)
print('SCAR_BUILD',len(created),'entities')
