"""Bake and export the preserved v2 cuirass using Blender and JA3's exporter.

Blender --background --factory-startup --python this.py -- --source <blend>
  --output <build> --game-root <JA3_ROOT>
Writes staging only; no active mod mutations. Native Blender render supplies the icon.
"""
import argparse, importlib.util, json, sys
from pathlib import Path
import bpy
import numpy as np
from mathutils import Vector

p=argparse.ArgumentParser(); p.add_argument('--source',required=True,type=Path); p.add_argument('--output',required=True,type=Path); p.add_argument('--game-root',required=True,type=Path)
p.add_argument('--entity',default='JAZZ_ImprovisedCuirass_Male');p.add_argument('--mesh-prefix',default='TEST_ImprovisedCuirass');p.add_argument('--icon',default='ImprovisedCuirass')
p.add_argument('--frame-all',action='store_true',help='Frame the full mesh for non-torso characters')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
entity=a.entity
spec=importlib.util.spec_from_file_location('armor_hge',a.game_root/'ModTools/BlenderExport.py'); hge=importlib.util.module_from_spec(spec); spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71',game='Zulu',appid='Jagged Alliance 3',mtl_prop_0_visible=True,mtl_prop_0_name='Unit',enable_colliders=True); hge.register()
bpy.ops.wm.open_mainfile(filepath=str(a.source.resolve()))
armor=next(o for o in bpy.data.objects if o.name.startswith(a.mesh_prefix))
rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
scene=bpy.context.scene; scene.cycles.device="CPU"
# The icon is a direct render of the same model, with native antialiasing.
for o in bpy.data.objects:
    if o.type=='MESH' and o!=armor:o.hide_render=True
cam=scene.camera; cam.location=(-.95,-2.6,1.85); cam.rotation_euler=(Vector((-.035,0,1.28))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.ortho_scale=.78
scene.render.film_transparent=True; scene.render.resolution_x=110; scene.render.resolution_y=110; scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'; scene.cycles.samples=96
if a.mesh_prefix!='TEST_ImprovisedCuirass':cam.data.ortho_scale=1.02
if a.frame_all:
    points=[armor.matrix_world@v.co for v in armor.data.vertices]
    lo=Vector(tuple(min(v[i] for v in points) for i in range(3)));hi=Vector(tuple(max(v[i] for v in points) for i in range(3)));target=(lo+hi)/2
    cam.location=target+Vector((-.95,-2.6,.55));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=max(hi-lo)*1.2
scene.render.filepath=str(out/(a.icon+'.png')); bpy.ops.render.render(write_still=True)
# Bake the real shader to a shared UV atlas before replacing it with HGE material.
for o in list(bpy.data.objects):
    if o not in (armor,rig):bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.object.select_all(action='DESELECT'); armor.hide_set(False); armor.select_set(True); bpy.context.view_layer.objects.active=armor
scene.cycles.samples=16; scene.render.bake.margin=8; scene.render.bake.use_selected_to_active=False
original=list(armor.data.materials); imgs={}
for label,kind in [('Base','DIFFUSE'),('Norm','NORMAL'),('Rough','ROUGHNESS'),('Metal','EMIT')]:
    im=bpy.data.images.new(entity+'_'+label,width=1024,height=1024,alpha=True); im.colorspace_settings.name='sRGB' if label=='Base' else 'Non-Color'; imgs[label]=im
    restore=[]
    for m in original:
        node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=im;m.node_tree.nodes.active=node
        if label=='Metal':
            output=next(n for n in m.node_tree.nodes if n.type=='OUTPUT_MATERIAL'); old=output.inputs['Surface'].links[0].from_socket
            value=m.node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value
            emission=m.node_tree.nodes.new('ShaderNodeEmission');emission.inputs[0].default_value=(value,value,value,1);m.node_tree.links.new(emission.outputs[0],output.inputs['Surface']);restore.append((m,output,old,emission))
            metallic=m.node_tree.nodes.get('Principled BSDF').inputs['Metallic']
            if metallic.is_linked:m.node_tree.links.new(metallic.links[0].from_socket,emission.inputs[0])
    scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.use_pass_color=True
    bpy.ops.object.bake(type=kind)
    for m,output,old,emission in restore:m.node_tree.links.new(old,output.inputs['Surface']);m.node_tree.nodes.remove(emission)
    im.filepath_raw=str(out/(entity+'_'+label+'.tga'));im.file_format='TARGA_RAW';im.save()
    print('BAKED',label,flush=True)
r=np.empty(1024*1024*4,np.float32);me=np.empty_like(r);imgs['Rough'].pixels.foreach_get(r);imgs['Metal'].pixels.foreach_get(me)
rm=np.ones((1024*1024,4),np.float32);rm[:,0]=r.reshape(-1,4)[:,0];rm[:,1]=0;rm[:,2]=me.reshape(-1,4)[:,0]
im=bpy.data.images.new(entity+'_RM',width=1024,height=1024,alpha=True);im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(rm.ravel());im.filepath_raw=str(out/(entity+'_RM.tga'));im.file_format='TARGA_RAW';im.save();imgs['RM']=im
mat=bpy.data.materials.new(entity);mat.use_nodes=True;hge.add_material_props(mat)
for prop in hge.MATERIAL_PROPERTIES:
    if prop.settings_name:
        key={'base_color':'Base','normal_map':'Norm','roughness_metallic_map':'RM'}.get(prop.settings_name)
        if key:mat[prop.id]=imgs[key].filepath_raw
        elif prop.map:mat[prop.id]=''
        else:mat[prop.id]=getattr(mat.hgm_settings,prop.settings_name)
# Standard opaque unit material; actual values match exporter's property names.
for prop in hge.MATERIAL_PROPERTIES:
    if prop.settings_name in ('project_specific_0','cast_shadows','receive_shadows','depth_write'):mat[prop.id]=True
armor.data.materials.clear();armor.data.materials.append(mat)
for face in armor.data.polygons:face.material_index=0
armor.name=entity
origin=bpy.data.objects.new(entity+'_Origin',None);bpy.context.collection.objects.link(origin)
world=armor.matrix_world.copy();armor.parent=origin;armor.matrix_world=world
settings=armor.hge_obj_settings;settings.entity=entity;settings.mesh='mesh';settings.lod=1;settings.inherit_animation='Male';settings.ignore=False;armor.hge_export=True
rig['hgskeleton']=entity+'_mesh';rig.hge_obj_settings.ignore=False
tri=armor.modifiers.new('Export triangulation','TRIANGULATE');bpy.context.view_layer.objects.active=armor;bpy.ops.object.modifier_apply(modifier=tri.name)
bpy.ops.wm.save_as_mainfile(filepath=str(out/(entity+'.blend')))
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(out/(entity+'.fbx')),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY','ARMATURE'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
armor.data.calc_loop_triangles();report={'entity':entity,'triangles':len(armor.data.loop_triangles),'inherit':'Male','hgskeleton':rig['hgskeleton'],'icon':[110,110],'baked_maps':['Base','Norm','RM']}
(out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('EXPORT_READY',report,flush=True)
