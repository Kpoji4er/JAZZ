"""Fit approved Meshy Chainmail as a Male Body, retain native exposed skin; staging only.
Blender -- --input GLB --game-root DIR --output DIR
"""
import argparse,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
for key in ('input','game-root','output'):p.add_argument('--'+key,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.input=a.input.resolve();a.output=a.output.resolve();a.output.mkdir(parents=True,exist_ok=True)
sample=a.game_root/'ModTools/Samples/Assets/SampleMaleModel'
bpy.ops.wm.open_mainfile(filepath=str(sample/'BlenderScene_Appearance.blend'))
rig=bpy.data.objects['Bip001'];donor=bpy.data.objects['M_BaseMesh Skin_BIP']
for ob in list(bpy.data.objects):
    if ob not in (rig,donor):bpy.data.objects.remove(ob,do_unlink=True)
for c in bpy.data.collections:c.hide_render=False;c.hide_viewport=False
rig.hide_set(False);donor.hide_set(False);bpy.context.view_layer.update()
verts=[donor.matrix_world@v.co for v in donor.data.vertices];donor.data.calc_loop_triangles()
tris=[tuple(t.vertices) for t in donor.data.loop_triangles]
bvh=BVHTree.FromPolygons(verts,tris,all_triangles=True)
def bind(pos):
    hit,_,idx,_=bvh.find_nearest(pos);ids=tris[idx]
    bary=barycentric_transform(hit,*[verts[i] for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)))
    weights={}
    for i,f in zip(ids,bary):
        for g in donor.data.vertices[i].groups:
            name=donor.vertex_groups[g.group].name
            if name in rig.data.bones and f>0:weights[name]=weights.get(name,0)+g.weight*f
    return weights
def smooth(t):
    t=max(0,min(1,t));return t*t*(3-2*t)
def bone(name):return rig.matrix_world@rig.data.bones[name].head_local
print('ARM_JOINTS',[(n,list(bone('Bip001 L '+n))) for n in ('UpperArm','Forearm','Hand')],flush=True)
bpy.ops.import_scene.gltf(filepath=str(a.input))
armor=next(o for o in bpy.context.selected_objects if o.type=='MESH');armor.name='TEST_Chainmail'
bpy.context.view_layer.objects.active=armor;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
for v in armor.data.vertices:
    x,y,z=v.co;v.co=Vector((x*.45,y*.38-.015,z*.40+1.215))
    # Align short sleeves with the sample upper arms; taper into the torso.
    s=1 if x>=0 else -1;t=smooth((abs(x)-.42)/.25)*smooth((z+.18)/.32)
    pivot=Vector((s*.19,0,1.475));rel=v.co-pivot;angle=math.radians(17)*t
    v.co.x=pivot.x+rel.x*math.cos(angle)-s*rel.z*math.sin(angle)
    v.co.z=pivot.z+s*rel.x*math.sin(angle)+rel.z*math.cos(angle)
bm=bmesh.new();bm.from_mesh(armor.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bm.to_mesh(armor.data);bm.free();prepare_export_mesh(armor)
shoulder_mask=armor.data.attributes.new('qa_rigid_shoulders','BOOLEAN','POINT')
for v in armor.data.vertices:
    pos=v.co;ws={}
    # Smooth surface weights across voxel detail; low torso excludes arms/legs.
    for delta in ((0,0,0),(.012,0,0),(-.012,0,0),(0,0,.012),(0,0,-.012)):
        for n,w in bind(pos+Vector(delta)).items():ws[n]=ws.get(n,0)+w/5
    # Mail/plates form a continuous torso shell: use broad spine transitions,
    # then blend into native clavicle/arm skin only across the short sleeves.
    if pos.z<1.20:
        t=smooth((pos.z-1.00)/.20);core={'Bip001 Spine':1-t,'Bip001 Spine1':t}
    else:
        t=smooth((pos.z-1.20)/.24);core={'Bip001 Spine1':1-t,'Bip001 Spine2':t}
    arm_blend=smooth((abs(pos.x)-.17)/.14)*smooth((pos.z-1.09)/.14)
    # Upper layered pauldrons belong to the chest, not the upper-arm envelope.
    # Fade only below the rigid cap, into the flexible mail sleeve.
    plate=smooth((pos.z-1.240)/.195)
    arm_blend*=1-plate
    if pos.z>=1.435:
        core={'Bip001 Spine2':1.0}
        shoulder_mask.data[v.index].value=abs(pos.x)>.13
    total=sum(ws.values());ws={n:w/total for n,w in ws.items()}
    ws={n:core.get(n,0)*(1-arm_blend)+ws.get(n,0)*arm_blend for n in core.keys()|ws.keys()}
    pairs=sorted(ws.items(),key=lambda x:-x[1])[:4];total=sum(w for _,w in pairs)
    for n,w in pairs:(armor.vertex_groups.get(n) or armor.vertex_groups.new(name=n)).add([v.index],w/total,'REPLACE')
# Native skin includes short-sleeve forearms/hands and the neck, never the head.
skin=donor.copy();skin.data=donor.data.copy();bpy.context.collection.objects.link(skin);skin.name='Chainmail_native_skin'
world=skin.matrix_world.copy();skin.parent=None;skin.matrix_world=world
bpy.ops.object.select_all(action='DESELECT');skin.select_set(True);bpy.context.view_layer.objects.active=skin;bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
def retain(pos):
    # A native Body contains the chest beneath the neck opening, not just a
    # disconnected neck strip. Keep the entire developer torso under the mail.
    if abs(pos.x)<.285 and 1.015<pos.z<1.60:return True
    side='L' if pos.x>0 else 'R';shoulder=bone('Bip001 '+side+' UpperArm');elbow=bone('Bip001 '+side+' Forearm')
    axis=elbow-shoulder;t=(pos-shoulder).dot(axis)/axis.length_squared
    return abs(pos.x)>.235 and pos.z>.95 and t>.47
bm=bmesh.new();bm.from_mesh(skin.data);bmesh.ops.delete(bm,geom=[f for f in bm.faces if not retain(f.calc_center_median())],context='FACES');bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bm.to_mesh(skin.data);bm.free();prepare_export_mesh(skin)
mat=bpy.data.materials.new('Chainmail_native_skin');mat.use_nodes=True;nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get('Principled BSDF')
mat['jazz_skin_colorization']=True
for kind,filename in [('Base','body_BC.tga'),('Norm','body_NM.tga'),('RM','body_RM.tga')]:
    im=bpy.data.images.load(str(sample/filename));im.colorspace_settings.name='sRGB' if kind=='Base' else 'Non-Color';im.pack();node=nodes.new('ShaderNodeTexImage');node.image=im
    if kind=='Base':links.new(node.outputs['Color'],bs.inputs['Base Color'])
    elif kind=='Norm':
        nm=nodes.new('ShaderNodeNormalMap');links.new(node.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],bs.inputs['Normal'])
    else:
        split=nodes.new('ShaderNodeSeparateColor');links.new(node.outputs['Color'],split.inputs[0]);links.new(split.outputs['Red'],bs.inputs['Roughness']);links.new(split.outputs['Blue'],bs.inputs['Metallic'])
skin.data.materials.clear();skin.data.materials.append(mat)
for f in skin.data.polygons:f.material_index=0
for obj in (armor,skin):
    obj.data.uv_layers.active.name='SourceUV'
    for m in obj.data.materials:
        uv=m.node_tree.nodes.new('ShaderNodeUVMap');uv.uv_map='SourceUV'
        for n in list(m.node_tree.nodes):
            if n.type=='TEX_IMAGE':m.node_tree.links.new(uv.outputs['UV'],n.inputs['Vector'])
            elif n.type=='NORMAL_MAP':n.uv_map='SourceUV'
    atlas=obj.data.uv_layers.new(name='ExportUV');obj.data.uv_layers.active=atlas;atlas.active_render=True
    if obj==armor:
        for src,dst in zip(obj.data.uv_layers['SourceUV'].data,atlas.data):dst.uv=(src.uv.x*.80,src.uv.y)
    else:
        bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj;bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.smart_project(island_margin=.02);bpy.ops.object.mode_set(mode='OBJECT')
        # Edit mode replaces Mesh UV storage; reacquire the layer afterwards.
        atlas=obj.data.uv_layers['ExportUV']
        for uvloop in atlas.data:uvloop.uv=(.81+uvloop.uv.x*.18,.01+uvloop.uv.y*.98)
        assert min(v.uv.x for v in atlas.data)>=.81
bpy.ops.object.select_all(action='DESELECT');armor.select_set(True);skin.select_set(True);bpy.context.view_layer.objects.active=armor;bpy.ops.object.join()
for v in armor.data.vertices:
    ws=sorted([(g.group,g.weight) for g in v.groups if g.weight>1e-7 and armor.vertex_groups[g.group].name in rig.data.bones],key=lambda x:-x[1])[:4];total=sum(w for _,w in ws);assert total>0
    for group_index in [g.group for g in v.groups]:armor.vertex_groups[group_index].remove([v.index])
    for i,w in ws:armor.vertex_groups[i].add([v.index],w/total,'REPLACE')
armor.modifiers.clear();arm=armor.modifiers.new('JA3 Male','ARMATURE');arm.object=rig
prepare_export_mesh(armor);armor.data.calc_loop_triangles()
donor.hide_render=True;donor.hide_set(True)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.render.resolution_x=800;scene.render.resolution_y=800;scene.render.resolution_percentage=100
scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.17,.19,.23,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.5
for pos,energy in [((2,-3,4),450),((-3,-1,2),300),((1,3,3),400)]:
    bpy.ops.object.light_add(type='AREA',location=pos);light=bpy.context.object;light.data.energy=energy;light.data.shape='DISK';light.data.size=3;light.rotation_euler=(Vector((0,0,1.3))-light.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add();scene.camera=bpy.context.object;scene.camera.data.type='ORTHO';scene.camera.data.ortho_scale=1.65
report=dict(triangles=len(armor.data.loop_triangles),vertices=len(armor.data.vertices),custom_normals=armor.data.has_custom_normals,max_influences=max(sum(g.weight>1e-7 for g in v.groups) for v in armor.data.vertices),runtime='NOT_RUN')
(a.output/'source-report.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'Chainmail.blend'))
for name,pos in [('front',(0,-3,1.35)),('back',(0,3,1.35)),('side',(3,0,1.35)),('oblique',(2,-3,1.85))]:
    scene.camera.location=pos;scene.camera.rotation_euler=(Vector((0,0,1.23))-scene.camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(a.output/(name+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(report))
