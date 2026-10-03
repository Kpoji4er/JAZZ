"""Build the supplied R4 OBJ with native UV/PBR, grip frame, FBX and previews.
Blender --background --factory-startup --python this.py -- --source DIR --build DIR --game-root DIR
Source is read-only. No active mod writes. Fixed original configuration.
"""
import argparse, json, math, sys
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Vector
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge, pixels, save_tga, assign_hge_maps
from _prepare_weapon_open_surfaces import prepare_export_mesh
from _render_ak103_icon import build_compositor
from _weapon_material_finish import separate_hard_edges

p=argparse.ArgumentParser()
for key in ('source','build','game-root'): p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for sub in ('clean','rigged','Textures'): (a.build/sub).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
hge=load_hge(a.game_root)
bpy.ops.wm.obj_import(filepath=str(a.source/'model_0.obj'))
o=next(o for o in bpy.context.scene.objects if o.type=='MESH');o.name='JAZZ_VektorR4'
assert o.data.uv_layers.active, 'Missing native UV'
# Source imports with muzzle -X, up Z. Exact overall length 1.005 m.
world=[o.matrix_world@v.co for v in o.data.vertices]
scale=1.005/(max(v.x for v in world)-min(v.x for v in world))
# Palm below the receiver at the original pistol grip; Trigger is forward of it.
grip=Vector((120,4.5,-12))
transform=Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Scale(scale,4)@Matrix.Translation(-grip)
o.data.transform(transform@o.matrix_world);o.matrix_world=Matrix.Identity(4)
tex=a.build/'Textures'
maps={k: pixels(a.source/('R4_low_R4_'+v+'.png')) for k,v in
      {'Base':'BaseColor','Normal':'Normal','Roughness':'Roughness','Metallic':'Metallic','AO':'AmbientOcclusion'}.items()}
rm=np.ones_like(maps['Base']);rm[:,:,0]=maps['Roughness'][:,:,0];rm[:,:,1]=rm[:,:,0];rm[:,:,2]=maps['Metallic'][:,:,0]
# Preserve author normal/roughness. Decode BC once for the sRGB TGA writer.
rgb=maps['Base'][:,:,:3];maps['Base'][:,:,:3]=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
images={k:save_tga('JAZZ_VektorR4_'+k,v,tex,k=='Base') for k,v in
        {'Base':maps['Base'],'Normal':maps['Normal'],'RM':rm,'AO':maps['AO']}.items()}
mat=bpy.data.materials.new('JAZZ_VektorR4');mat.use_nodes=True
nodes=mat.node_tree.nodes;links=mat.node_tree.links;shader=nodes.get('Principled BSDF')
for key,im in images.items():
    node=nodes.new('ShaderNodeTexImage');node.image=im;node.label=key
    if key=='Base': links.new(node.outputs['Color'],shader.inputs['Base Color'])
    elif key=='Normal':
        normal=nodes.new('ShaderNodeNormalMap');links.new(node.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs['Normal'],shader.inputs['Normal'])
    elif key=='RM':
        sep=nodes.new('ShaderNodeSeparateColor');links.new(node.outputs['Color'],sep.inputs['Color']);links.new(sep.outputs['Red'],shader.inputs['Roughness']);links.new(sep.outputs['Blue'],shader.inputs['Metallic'])
assign_hge_maps(hge,mat,images);o.data.materials.clear();o.data.materials.append(mat)
for f in o.data.polygons:f.material_index=0
# The supplied triangulation contains collinear, zero-area faces. Drop only
# these faces; never weld distant vertices or decimate the visible silhouette.
bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.normal_update()
bad=[f for f in bm.faces if f.calc_area()<2e-12 or f.normal.length<1e-10]
removed=len(bad);bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
# Reconnect coincident seam vertices before outward recalculation. UVs are loop data.
face_count=len(bm.faces);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
assert len(bm.faces)==face_count,'Seam weld changed surface triangle count'
bm.to_mesh(o.data);bm.free()
print('Removed degenerate source faces:',removed)
issues=prepare_export_mesh(o,strict=False)
if issues:
    assert all(i['kind'] in ('degenerate','zero_normal') for i in issues),issues
    indices={o.data.loop_triangles[i['triangle']].polygon_index for i in issues}
    bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in indices],context='FACES_ONLY');bm.to_mesh(o.data);bm.free()
    removed+=len(indices)
report=prepare_export_mesh(o)
separate_hard_edges(o)
report=prepare_export_mesh(o)
bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'clean/VektorR4.blend'))
origin=bpy.data.objects.new('JAZZ_VektorR4_Origin',None);bpy.context.collection.objects.link(origin);o.parent=origin
settings=o.hge_obj_settings;settings.entity=o.name;settings.mesh='Mesh';settings.state='idle';settings.lod=1;settings.ignore=False;o.hge_export=True
spots={'Muzzle':(0,-.691,.080),'MuzzleTip':(0,-.691,.080),'Barrel':(0,-.50,.080),
       'Trigger':(0,-.044,.013),'Hand_l_grip':(0,-.30,.032),'Magazine':(0,-.125,.022)}
for name,point in spots.items():
    spot=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(spot);spot.parent=o;spot.location=point;spot.hge_obj_settings.spot_name=name
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged/VektorR4_JA3.blend'))
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(a.build/'rigged/VektorR4_JA3.fbx'),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
o.data.calc_loop_triangles()
(a.build/'build-report.json').write_text(json.dumps({'length_m':1.005,'scale':scale,'triangles':len(o.data.loop_triangles),'uv_layers':len(o.data.uv_layers),'custom_normals':o.data.has_custom_normals,'spots':spots,'mesh_audit':report},indent=2),encoding='utf-8')
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.device='CPU'
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
pts=[o.matrix_world@Vector(v) for v in o.bound_box]
lo=Vector(tuple(min(v[i] for v in pts) for i in range(3)));hi=Vector(tuple(max(v[i] for v in pts) for i in range(3)));target=(lo+hi)/2
cam=bpy.data.cameras.new('R4Camera');cam.type='ORTHO';camera=bpy.data.objects.new('R4Camera',cam);scene.collection.objects.link(camera);scene.camera=camera
for i,offset in enumerate([(-1,-.5,1.5),(-.5,.5,1),(1,1,0)]):
    light=bpy.data.lights.new('R4Light'+str(i),'AREA');light.energy=25;light.size=1.5
    ob=bpy.data.objects.new(light.name,light);scene.collection.objects.link(ob);ob.location=target+Vector(offset);ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
scene.world=bpy.data.worlds.new('R4World');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.3
for name,direction in [('right',(-2,0,.05)),('left',(2,0,.05)),('threequarter',(-2,-1,.6))]:
    scene.render.resolution_x=1400;scene.render.resolution_y=600;scene.render.resolution_percentage=100
    cam.ortho_scale=1.13;camera.location=target+Vector(direction);camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(a.build/('VektorR4_'+name+'.png'));bpy.ops.render.render(write_still=True)
build_compositor(scene);scene.render.resolution_x=324;scene.render.resolution_y=165;cam.ortho_scale=1.23
camera.location=target+Vector((-2,.04,.25));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
scene.render.filepath=str(a.build/'VektorR4_icon.png');bpy.ops.render.render(write_still=True)
print('R4 build/export/previews complete')
