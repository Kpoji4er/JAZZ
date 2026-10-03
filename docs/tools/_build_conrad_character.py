"""Fit the approved Conrad low-poly GLB to the unmodified official Male rig.
Blender -b --factory-startup --python this.py -- --input GLB --game-root JA3 --output DIR
Writes sources, pose previews and official-exporter FBX; never installs runtime files.
"""
import argparse, importlib.util, json, math, sys
from pathlib import Path
import bpy, bmesh
import numpy as np
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform

p=argparse.ArgumentParser()
for key in ('input','game-root','output'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--native-arms',action='store_true',help='Use official forearm/hand topology and native skin below the cuffs')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh, audit_triangles, triangulate_without_custom_normals
from _weapon_material_finish import separate_hard_edges
from _conrad_surface_orientation import uv_winding, prepare_author_facing
spec=importlib.util.spec_from_file_location('conrad_hge',a.game_root/'ModTools/BlenderExport.py')
hge=importlib.util.module_from_spec(spec);spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71',game='Zulu',appid='Jagged Alliance 3',mtl_prop_0_visible=True,mtl_prop_0_name='Unit',enable_colliders=True)
hge.register()
bpy.ops.wm.open_mainfile(filepath=str(a.game_root/'ModTools/Samples/Assets/SampleMaleModel/BlenderScene_Appearance.blend'))
rig=bpy.data.objects['Bip001'];donor=bpy.data.objects['M_BaseMesh Skin_BIP']
rig.animation_data_clear()
for pb in rig.pose.bones:
    pb.location=(0,0,0);pb.scale=(1,1,1);pb.rotation_mode='QUATERNION';pb.rotation_quaternion=Quaternion()
for collection in bpy.data.collections:collection.hide_viewport=False;collection.hide_render=False
rig.hide_set(False);donor.hide_set(False)
for ob in list(bpy.data.objects):
    if ob not in (rig,donor):bpy.data.objects.remove(ob,do_unlink=True)
bpy.context.view_layer.update()
donor.data.calc_loop_triangles()
def world_bone_rotation(name, axis, degrees):
    pb=rig.pose.bones[name]
    basis=(rig.matrix_world@pb.bone.matrix_local).to_quaternion()
    pb.rotation_quaternion=basis.inverted()@Quaternion(Vector(axis),math.radians(degrees))@basis
def pose_limb(side, segment, degrees):
    root='Bip001 '+side+' '+segment
    pivot=rig.matrix_world@rig.data.bones[root].head_local
    rotation=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(degrees),4,'Y' if segment=='UpperArm' else 'X')@Matrix.Translation(-pivot)
    if segment=='UpperArm':
        names=[b.name for b in rig.data.bones if b.name.startswith('Bip001 '+side+' ') and any(k in b.name for k in ('UpperArm','Fore','Hand','Finger')) or b.name.startswith('Bip001 '+side+'UpArm')]
    else:
        names=[b.name for b in rig.data.bones if b.name.startswith('Bip001 '+side+' ') and any(k in b.name for k in ('Fore','Hand','Finger'))]
    # Twist helpers in this rig are animated explicitly. Transform them too;
    # rotating only the main bone leaves donor sleeves in the old position.
    target={n:rig.matrix_world.inverted()@rotation@rig.matrix_world@rig.data.bones[n].matrix_local for n in names}
    for pb in rig.pose.bones:
        if pb.name in target:
            pb.matrix=target[pb.name]
            bpy.context.view_layer.update()
# Pose the existing donor toward Meshy's narrow A pose. Transferring in that
# pose and inverse-skinning back to bind preserves sleeve and holster shapes.
pose_limb('L','UpperArm',27)
pose_limb('R','UpperArm',-27)
bpy.context.view_layer.update()
evaluated=donor.evaluated_get(bpy.context.evaluated_depsgraph_get())
dv=[evaluated.matrix_world@v.co for v in evaluated.data.vertices]
posed_bone_matrices={pb.name:rig.matrix_world@pb.matrix@pb.bone.matrix_local.inverted()@rig.matrix_world.inverted() for pb in rig.pose.bones}
df=[tuple(t.vertices) for t in donor.data.loop_triangles]
tree=BVHTree.FromPolygons(dv,df,all_triangles=True)
bpy.ops.import_scene.gltf(filepath=str(a.input.resolve()))
mesh=next(o for o in bpy.context.selected_objects if o.type=='MESH')
author_winding=uv_winding(mesh)
bpy.context.view_layer.objects.active=mesh
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
lo=Vector(tuple(min(v.co[i] for v in mesh.data.vertices) for i in range(3)))
hi=Vector(tuple(max(v.co[i] for v in mesh.data.vertices) for i in range(3)))
scale=1.7985/(hi.z-lo.z)
# Whole-body uniform scale preserves the approved adult proportions.
for v in mesh.data.vertices:
    v.co=Vector((v.co.x-(hi.x+lo.x)/2,v.co.y,(v.co.z-lo.z)))*scale
bm=bmesh.new();bm.from_mesh(mesh.data)
bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
bm.to_mesh(mesh.data);bm.free()
prepare_export_mesh(mesh)
# Transfer native skin from the closest donor triangle in matching bind pose.
mesh.vertex_groups.clear()
groups={b.name:mesh.vertex_groups.new(name=b.name) for b in rig.data.bones}
distances=[]
for v in mesh.data.vertices:
    co,normal,idx,dist=tree.find_nearest(v.co);distances.append(dist)
    ids=df[idx]
    bary=barycentric_transform(co,*[dv[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
    weights={}
    for i,factor in zip(ids,bary):
        for g in donor.data.vertices[i].groups:
            name=donor.vertex_groups[g.group].name
            if name in groups and factor>0:weights[name]=weights.get(name,0)+factor*g.weight
    # Preserve face/hair as a rigid skull; the base sample has no facial rig.
    if v.co.z>1.565:weights={'Bip001 Head':1.0}
    # Raised pouches must not inherit the nearby upper arm.
    elif abs(v.co.x)<.235 and 1.10<v.co.z<1.39:
        weights={n:w for n,w in weights.items() if any(s in n for s in ('Spine','Pelvis'))}
        if not weights:weights={'Bip001 Spine2':1.0}
    weights=dict(sorted(weights.items(),key=lambda q:q[1],reverse=True)[:4])
    total=sum(weights.values());assert total>0,(v.index,list(v.co))
    for n,w in weights.items():
        if w>1e-8:groups[n].add([v.index],w/total,'REPLACE')
    skin=Matrix([[0.0]*4 for _ in range(4)])
    for n,w in weights.items():
        skin+=posed_bone_matrices[n]*(w/total)
    v.co=skin.inverted()@v.co
for pb in rig.pose.bones:
    pb.location=(0,0,0);pb.scale=(1,1,1);pb.rotation_quaternion=Quaternion()
bpy.context.view_layer.update()
arm=mesh.modifiers.new('Official Male skin','ARMATURE');arm.object=rig
# Keep the original UV atlas; split along existing triangle edges under collar/belt.
def region(face):
    c=sum((mesh.data.vertices[i].co for i in face.vertices),Vector())/len(face.vertices)
    return 'Head' if c.z>1.535 else ('Pants' if c.z<1.005 else 'Body')
parts=[]
native_material=None
native_maps={}
for part in ('Body','Pants','Head'):
    ob=mesh.copy();ob.data=mesh.data.copy();bpy.context.collection.objects.link(ob)
    ob.name='JAZZ_Conrad'+part
    kill=[f.index for f in mesh.data.polygons if region(f)!=part]
    bm=bmesh.new();bm.from_mesh(ob.data);bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in kill],context='FACES')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(ob.data);bm.free()
    parts.append(ob)
if a.native_arms:
    # Keep native hand placement, finger topology and weights. The overlap starts
    # inside the rolled cuff; no nearest-surface finger weights are used.
    def beyond_cuff(pos, fraction):
        side='L' if pos.x>0 else 'R'
        elbow=rig.matrix_world@rig.data.bones['Bip001 '+side+' Forearm'].head_local
        wrist=rig.matrix_world@rig.data.bones['Bip001 '+side+' Hand'].head_local
        axis=wrist-elbow
        return abs(pos.x)>.39 and pos.z>.9 and (pos-elbow).dot(axis)/axis.length_squared>fraction
    bodypart=parts[0]
    # Sleeve edges must follow the same native elbow/twist weights as the arm
    # underneath. Re-sample in bind space after fitting, preserving positions.
    rest_vertices=[donor.matrix_world@v.co for v in donor.data.vertices]
    rest_tree=BVHTree.FromPolygons(rest_vertices,df,all_triangles=True)
    for v in bodypart.data.vertices:
        if abs(v.co.x)<.34 or v.co.z<1.0:continue
        hit,_,idx,_=rest_tree.find_nearest(v.co);ids=df[idx]
        factors=barycentric_transform(hit,*[rest_vertices[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
        weights={}
        for index,factor in zip(ids,factors):
            for g in donor.data.vertices[index].groups:
                name=donor.vertex_groups[g.group].name
                if factor>0:weights[name]=weights.get(name,0)+factor*g.weight
        for index in [g.group for g in v.groups]:bodypart.vertex_groups[index].remove([v.index])
        for name,weight in weights.items():bodypart.vertex_groups[name].add([v.index],weight,'REPLACE')
    bodypart.data.calc_loop_triangles()
    old_surface=BVHTree.FromPolygons([v.co.copy() for v in bodypart.data.vertices],[tuple(f.vertices) for f in bodypart.data.loop_triangles],all_triangles=True)
    source_base=next(n.image for n in bodypart.data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and n.image and n.image.name=='texture_0')
    def mean_surface_color(obj,image,filter_fn,skin_only=False):
        pixels=np.empty(len(image.pixels),np.float32);image.pixels.foreach_get(pixels);pixels=pixels.reshape(image.size[1],image.size[0],4)
        uv=obj.data.uv_layers.active.data;colors=[]
        for f in obj.data.polygons:
            center=sum((obj.data.vertices[i].co for i in f.vertices),Vector())/len(f.vertices)
            if not filter_fn(center):continue
            tex=sum((uv[i].uv for i in f.loop_indices),Vector((0,0)))/len(f.loop_indices)
            colors.append(pixels[int(tex.y*image.size[1])%image.size[1],int(tex.x*image.size[0])%image.size[0],:3])
        colors=np.asarray(colors)
        if skin_only:colors=colors[colors[:,0]-colors[:,1]>.08]
        assert len(colors)>10,'Insufficient skin samples'
        return np.median(colors,axis=0)
    target_skin=mean_surface_color(bodypart,source_base,lambda c:beyond_cuff(c,.15) and not beyond_cuff(c,.8),skin_only=True)
    print('TARGET_SKIN',target_skin.tolist(),flush=True)
    bm=bmesh.new();bm.from_mesh(bodypart.data)
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if beyond_cuff(f.calc_center_median(),.86)],context='FACES')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(bodypart.data);bm.free()
    arms=donor.copy();arms.data=donor.data.copy();bpy.context.collection.objects.link(arms)
    arms.name='Conrad_native_forearms'
    world=arms.matrix_world.copy();arms.parent=None;arms.matrix_world=world
    bpy.ops.object.select_all(action='DESELECT');arms.select_set(True);bpy.context.view_layer.objects.active=arms
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    bm=bmesh.new();bm.from_mesh(arms.data)
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if not beyond_cuff(f.calc_center_median(),.68)],context='FACES')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(arms.data);bm.free()
    triangulate_without_custom_normals(arms)
    active_uv=arms.data.uv_layers.active
    for layer in list(arms.data.uv_layers):
        if layer!=active_uv:arms.data.uv_layers.remove(layer)
    active_uv.name=bodypart.data.uv_layers.active.name
    author_winding.update(uv_winding(arms))
    for v in arms.data.vertices:
        side='L' if v.co.x>0 else 'R'
        elbow=rig.matrix_world@rig.data.bones['Bip001 '+side+' Forearm'].head_local
        wrist=rig.matrix_world@rig.data.bones['Bip001 '+side+' Hand'].head_local
        axis=wrist-elbow;t=(v.co-elbow).dot(axis)/axis.length_squared
        blend=max(0,min(1,(1.0-t)/.32));blend=blend*blend*(3-2*blend)
        if blend>0 and t>.12:
            center=elbow+axis*t;radial=v.co-center
            hit=old_surface.find_nearest(v.co)[0]
            hit_radial=hit-elbow-axis*((hit-elbow).dot(axis)/axis.length_squared)
            ratio=max(.65,min(1.35,hit_radial.length/max(radial.length,1e-6)))
            v.co=center+radial*(1+blend*(ratio-1))
    native_material=bpy.data.materials.new('Conrad_native_skin');native_material.use_nodes=True
    nodes=native_material.node_tree.nodes;links=native_material.node_tree.links;bsdf=nodes.get('Principled BSDF')
    sample=a.game_root/'ModTools/Samples/Assets/SampleMaleModel'
    for key,filename in [('Base','body_BC.tga'),('Norm','body_NM.tga'),('RM','body_RM.tga')]:
        im=bpy.data.images.load(str(sample/filename),check_existing=False)
        im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color';native_maps[key]=im
        if key=='Base':
            native_skin=mean_surface_color(arms,im,lambda c:True)
            pixels=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(pixels);pixels=pixels.reshape(-1,4)
            pixels[:,:3]*=np.clip(target_skin/np.maximum(native_skin,.001),.1,2)
            tinted=bpy.data.images.new('Conrad_skin_matched',width=im.size[0],height=im.size[1],alpha=True)
            tinted.colorspace_settings.name='sRGB';tinted.pixels.foreach_set(np.clip(pixels,0,1).ravel());tinted.update()
            tinted.pack()
            print('NATIVE_SKIN',native_skin.tolist(),'MATCHED',mean_surface_color(arms,tinted,lambda c:True).tolist(),flush=True)
            im=tinted;native_maps[key]=im
        node=nodes.new('ShaderNodeTexImage');node.image=im
        if key=='Base':links.new(node.outputs['Color'],bsdf.inputs['Base Color'])
        elif key=='Norm':
            nm=nodes.new('ShaderNodeNormalMap');links.new(node.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
        else:
            rgb=nodes.new('ShaderNodeSeparateColor');links.new(node.outputs['Color'],rgb.inputs[0])
            links.new(rgb.outputs['Red'],bsdf.inputs['Roughness']);links.new(rgb.outputs['Blue'],bsdf.inputs['Metallic'])
    arms.data.materials.clear();arms.data.materials.append(native_material)
    for f in arms.data.polygons:f.material_index=0
    bpy.ops.object.select_all(action='DESELECT');arms.select_set(True);bodypart.select_set(True);bpy.context.view_layer.objects.active=bodypart
    bpy.ops.object.join()
    for v in bodypart.data.vertices:
        ws=sorted([(g.group,g.weight) for g in v.groups if g.weight>1e-8],key=lambda x:x[1],reverse=True)[:4]
        total=sum(w for _,w in ws);assert total>0
        for group_index in [g.group for g in v.groups]:bodypart.vertex_groups[group_index].remove([v.index])
        for index,weight in ws:bodypart.vertex_groups[index].add([v.index],weight/total,'REPLACE')
bpy.data.objects.remove(mesh,do_unlink=True);bpy.data.objects.remove(donor,do_unlink=True)
# Strip unused sample data objects; shared original material stays for render QA.
for ob in list(bpy.data.objects):
    if ob not in parts and ob!=rig:bpy.data.objects.remove(ob,do_unlink=True)
for ob in parts:
    ob.hide_set(False);ob.hide_render=False
    for f in ob.data.polygons:f.use_smooth=True
    prepare_export_mesh(ob)
    separate_hard_edges(ob)
    prepare_author_facing(ob,author_winding)
report={'source_triangles':20809,'bone_count':len(rig.data.bones),'parts':{},'donor_distance_p99':float(np.percentile(distances,99)),'runtime':'NOT_RUN'}
for ob in parts:
    ob.data.calc_loop_triangles()
    issues=audit_triangles([tuple(v.co) for v in ob.data.vertices],[tuple(t.vertices) for t in ob.data.loop_triangles],name=ob.name)
    entry={'triangles':len(ob.data.loop_triangles),'vertices':len(ob.data.vertices),
        'unweighted':sum(not any(g.weight>0 for g in v.groups) for v in ob.data.vertices),
        'max_influences':max(sum(g.weight>1e-7 for g in v.groups) for v in ob.data.vertices),
        'custom_normals':ob.data.has_custom_normals,'geometry_issues':issues}
    assert entry['unweighted']==0 and entry['max_influences']<=4 and not issues,entry
    report['parts'][ob.name]=entry
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
scene.render.resolution_x=900;scene.render.resolution_y=1000;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.15,.17,.2,1)
scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
scene.view_settings.view_transform='AgX'
center=Vector((0,0,.9))
def aim(ob,target):ob.rotation_euler=(target-ob.location).to_track_quat('-Z','Y').to_euler()
for name,xyz,power in [('Key',(2,-3,4),650),('Fill',(-3,-1,2),400),('Rim',(1,3,3),650)]:
    bpy.ops.object.light_add(type='AREA',location=xyz);light=bpy.context.object
    light.name=name;light.data.energy=power;light.data.size=3;aim(light,center)
bpy.ops.object.camera_add(location=(0,-5,1.0));cam=bpy.context.object;scene.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=2.12;aim(cam,center)
for name,xyz in [('front',(0,-5,1)),('back',(0,5,1)),('three-quarter',(2,-5,1))]:
    cam.location=xyz;aim(cam,center);scene.render.filepath=str(out/(name+'.png'));bpy.ops.render.render(write_still=True)
# Synthetic articulation is an offline skin check, never a substitute for game QA.
pose_limb('L','Forearm',-60)
pose_limb('R','Forearm',-60)
bpy.context.view_layer.update()
cam.location=(2,-5,1);aim(cam,center);scene.render.filepath=str(out/'pose.png');bpy.ops.render.render(write_still=True)
for pb in rig.pose.bones:
    pb.location=(0,0,0);pb.scale=(1,1,1);pb.rotation_quaternion=Quaternion()
bpy.context.view_layer.update()
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(out/'Conrad_Rigged.blend'),compress=True)
# Shared atlas: preserve base and tangent normal; glTF G roughness/B metal -> JA3 R/B.
mat=parts[0].data.materials[0];nodes=mat.node_tree.nodes
imgs={n.image.name:n.image for n in nodes if n.type=='TEX_IMAGE' and n.image}
base=next(im for name,im in imgs.items() if name=='texture_0')
norm=next(im for name,im in imgs.items() if name=='normal')
orm=next(im for name,im in imgs.items() if 'metallic_roughness' in name)
tex=out/'Textures';tex.mkdir(exist_ok=True)
for key,im in [('Base',base),('Norm',norm)]:
    data=np.empty(len(im.pixels),np.float32);im.pixels.foreach_get(data)
    copy=bpy.data.images.new('JAZZ_Conrad_'+key,width=im.size[0],height=im.size[1],alpha=True)
    copy.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color'
    copy.pixels.foreach_set(data)
    copy.filepath_raw=str(tex/('JAZZ_Conrad_'+key+'.tga'));copy.file_format='TARGA_RAW';copy.save()
pixels=np.empty(len(orm.pixels),np.float32);orm.pixels.foreach_get(pixels);pixels=pixels.reshape(-1,4)
rm=np.ones_like(pixels);rm[:,0]=pixels[:,1];rm[:,1]=0;rm[:,2]=pixels[:,2]
im=bpy.data.images.new('JAZZ_Conrad_RM',width=orm.size[0],height=orm.size[1],alpha=True)
im.colorspace_settings.name='Non-Color';im.pixels.foreach_set(rm.ravel());im.file_format='TARGA_RAW';im.filepath_raw=str(tex/'JAZZ_Conrad_RM.tga');im.save()
native_exportmat=None
if native_material:
    native_exportmat=bpy.data.materials.new('JAZZ_ConradNativeSkin');native_exportmat.use_nodes=True;hge.add_material_props(native_exportmat)
    for key,source in native_maps.items():
        pixels=np.empty(len(source.pixels),np.float32);source.pixels.foreach_get(pixels)
        target=bpy.data.images.new('ConradNative_'+key,width=source.size[0],height=source.size[1],alpha=True)
        target.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color';target.pixels.foreach_set(pixels)
        target.file_format='TARGA_RAW';target.filepath_raw=str(tex/('JAZZ_ConradNative_'+key+'.tga'));target.save()
    for prop in hge.MATERIAL_PROPERTIES:
        if not prop.settings_name:continue
        label={'base_color':'Base','normal_map':'Norm','roughness_metallic_map':'RM'}.get(prop.settings_name)
        if label:native_exportmat[prop.id]=str(tex/('JAZZ_ConradNative_'+label+'.tga'))
        elif prop.map:native_exportmat[prop.id]=''
        else:native_exportmat[prop.id]=getattr(native_exportmat.hgm_settings,prop.settings_name)
        if prop.settings_name in ('project_specific_0','cast_shadows','receive_shadows','depth_write'):native_exportmat[prop.id]=True
exportmat=bpy.data.materials.new('JAZZ_Conrad');exportmat.use_nodes=True;hge.add_material_props(exportmat)
for prop in hge.MATERIAL_PROPERTIES:
    if not prop.settings_name:continue
    label={'base_color':'Base','normal_map':'Norm','roughness_metallic_map':'RM'}.get(prop.settings_name)
    if label:exportmat[prop.id]=str(tex/('JAZZ_Conrad_'+label+'.tga'))
    elif prop.map:exportmat[prop.id]=''
    else:exportmat[prop.id]=getattr(exportmat.hgm_settings,prop.settings_name)
    if prop.settings_name in ('project_specific_0','cast_shadows','receive_shadows','depth_write'):exportmat[prop.id]=True
for ob in list(bpy.data.objects):
    if ob not in parts and ob!=rig:bpy.data.objects.remove(ob,do_unlink=True)
origin=bpy.data.objects.new('Origin_Conrad',None);bpy.context.collection.objects.link(origin)
for ob in parts:
    ob.data.materials[0]=exportmat
    if len(ob.data.materials)>1:
        assert native_exportmat
        ob.data.materials[1]=native_exportmat
    ob.parent=origin
    s=ob.hge_obj_settings;s.entity=ob.name;s.mesh='mesh';s.state='_mesh';s.lod=1;s.lod_distance=0;s.inherit_animation='Male';s.ignore=False;ob.hge_export=True
    prepare_author_facing(ob,author_winding)
rig['hgskeleton']='|'.join(o.name+'_mesh' for o in parts);rig.hge_obj_settings.ignore=False
bpy.ops.wm.save_as_mainfile(filepath=str(out/'Conrad_Export.blend'),compress=True)
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(out/'Conrad.fbx'),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY','ARMATURE'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
(out/'rig-report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('CONRAD_EXPORT_READY',json.dumps(report))
