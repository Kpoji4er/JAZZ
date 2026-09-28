"""Repair one installed HAV skin against preserved cuirass v7; geometry/UV unchanged.
Blender --python this.py -- --source <compiled-source.blend> --reference <v7.blend>
 --output <new folder> --game-root <JA3_ROOT>. No installation or game launch.
"""
import argparse,importlib.util,json,sys,hashlib,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
from mathutils.kdtree import KDTree
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _ja3_mesh_prepare import prepare_export_mesh
p=argparse.ArgumentParser()
for n in ('source','reference','output','game-root'):p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source));armor=next(o for o in bpy.data.objects if o.type=='MESH');rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');entity=armor.name
def geom():return hashlib.sha256(json.dumps([[list(v.co)for v in armor.data.vertices],[list(f.vertices)for f in armor.data.polygons]],sort_keys=True).encode()).hexdigest()
before=geom();old=[{armor.vertex_groups[g.group].name:g.weight for g in v.groups}for v in armor.data.vertices]
with bpy.data.libraries.load(str(a.reference),link=False)as(src,dst):
    dst.objects=['M_BaseMesh Skin_BIP','TEST_ImprovisedCuirass_Male_v7','Bip001']
body,cuirass,reference_rig=dst.objects
for o in dst.objects:bpy.context.scene.collection.objects.link(o)
assert set(rig.data.bones.keys())==set(reference_rig.data.bones.keys())
assert max(abs(x-y)for b in rig.data.bones for row,other in zip(b.matrix_local,reference_rig.data.bones[b.name].matrix_local)for x,y in zip(row,other))<1e-5
for o in (body,cuirass):
    for m in o.modifiers:
        if m.type=='ARMATURE':m.object=rig
    o.parent=None
bpy.data.objects.remove(reference_rig,do_unlink=True)
bpy.context.view_layer.update()
def surface(obj,torso=False):
    obj.data.calc_loop_triangles();vs=[obj.matrix_world@v.co for v in obj.data.vertices]
    fs=[tuple(f.vertices)for f in obj.data.loop_triangles if not torso or all(abs(vs[i].x)<.20 for i in f.vertices)]
    return obj,vs,fs,BVHTree.FromPolygons(vs,fs,all_triangles=True)
sample,plate=surface(body),surface(cuirass,True)
def norm(w):
    w=dict(sorted(((k,v)for k,v in w.items()if v>1e-7),key=lambda x:x[1],reverse=True)[:4]);s=sum(w.values());assert s>0
    return {k:v/s for k,v in w.items()}
def bind(p,s):
    obj,vs,fs,bvh=s;q,_,idx,_=bvh.find_nearest(p);ids=fs[idx]
    b=barycentric_transform(q,*[vs[i]for i in ids],Vector((1,0,0)),Vector((0,1,0)),Vector((0,0,1)));w={}
    for i,factor in zip(ids,b):
        for g in obj.data.vertices[i].groups:
            n=obj.vertex_groups[g.group].name
            if factor>0 and n in rig.data.bones:w[n]=w.get(n,0)+factor*g.weight
    return norm(w)
def clamp(x):return max(0,min(1,x))
def mix(x,y,t):return norm({n:x.get(n,0)*(1-t)+y.get(n,0)*t for n in x.keys()|y.keys()})
new=[]
for v,previous in zip(armor.data.vertices,old):
    pt=armor.matrix_world@v.co
    # Surface sampling retains the native clavicle/twist chains. The old field
    # discarded these on the upper back and froze disconnected shoulder panels.
    torso=bind(pt,plate);native=bind(pt,sample)
    upper=clamp((pt.z-1.31)/.12)
    shoulder=clamp((abs(pt.x)-.16)/.07)*clamp((pt.z-1.25)/.12)
    field=mix(torso,native,max(upper,shoulder))
    # Keep rigid forearm/elbow geometry on its existing limb chain; blend only
    # the transition into the shoulder, not the whole armored sleeve.
    retain=max(clamp((abs(pt.x)-.27)/.18),clamp((1.02-pt.z)/.08))
    # Only the reported upper back/shoulder region changes. Keep the fitted
    # lower skirt and front plate on their established rigid torso field.
    repair_region=max(clamp((pt.y+.03)/.06)*clamp((pt.z-1.24)/.10),
                      clamp((abs(pt.x)-.13)/.07)*clamp((pt.z-1.29)/.12),
                      clamp((pt.z-1.43)/.07))
    new.append(mix(previous,field,repair_region*(1-retain)))
def assign(fields):
    armor.vertex_groups.clear();groups={}
    for v,w in zip(armor.data.vertices,fields):
        for n,x in norm(w).items():
            if n not in groups:groups[n]=armor.vertex_groups.new(name=n)
            groups[n].add([v.index],x,'REPLACE')
def bounds(obj):return [[min((obj.matrix_world@v.co)[i]for v in obj.data.vertices)for i in range(3)],[max((obj.matrix_world@v.co)[i]for v in obj.data.vertices)for i in range(3)]]
report={'entity':entity,'geometry_before':before,'native_rig_matches_v7':True,'bounds_m':bounds(armor),'cuirass_bounds_m':bounds(cuirass),'changed_vertices':sum(any(abs(w.get(n,0)-v.get(n,0))>.001 for n in w.keys()|v.keys())for w,v in zip(old,new)),'runtime':'NOT_RUN','poses':[]}
cuirass.hide_render=True;body.hide_render=False
scene=bpy.context.scene;scene.render.engine='BLENDER_WORKBENCH';scene.display.shading.color_type='OBJECT';scene.display.shading.light='STUDIO';scene.display.shading.show_cavity=True
armor.color=(.28,.38,.22,1);body.color=(.2,.2,.2,1);scene.render.resolution_x=700;scene.render.resolution_y=700;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.ops.object.camera_add();camera=bpy.context.object;scene.camera=camera;camera.data.type='ORTHO';camera.data.ortho_scale=1.05
poses={'rest':[], 'lean':[('Bip001 Spine1',(12,0,0)),('Bip001 Spine2',(23,0,12)),('Bip001 R UpperArm',(0,35,-25))],'twist':[('Bip001 Spine1',(0,0,25)),('Bip001 Spine2',(0,0,25)),('Bip001 L Clavicle',(0,0,20))]}
for stage,weights in [('before',old),('after',new)]:
    assign(weights)
    for name,rotations in poses.items():
        for b in rig.pose.bones:b.matrix_basis.identity();b.rotation_mode='XYZ'
        for n,angles in rotations:rig.pose.bones[n].rotation_euler=[math.radians(x)for x in angles]
        bpy.context.view_layer.update();evaluated=armor.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
        strains=[]
        for e in armor.data.edges:
            i,j=e.vertices;d=(armor.data.vertices[i].co-armor.data.vertices[j].co).length
            if d>.003:strains.append((mesh.vertices[i].co-mesh.vertices[j].co).length/d)
        strains.sort();p99=strains[int(.99*(len(strains)-1))]
        assert all(math.isfinite(x)for v in mesh.vertices for x in v.co)
        report['poses'].append({'stage':stage,'pose':name,'strain_p99':p99});evaluated.to_mesh_clear()
        if stage=='after':assert p99<2.0,(entity,name,p99)
        camera.location=(1,2.8,1.9);camera.rotation_euler=(Vector((0,0,1.30))-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(a.output/(stage+'-'+name+'-back.png'));bpy.ops.render.render(write_still=True)
for b in rig.pose.bones:b.matrix_basis.identity()
assign(new);assert geom()==before
report['geometry_after']=geom();report['issues']=prepare_export_mesh(armor)
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'review.blend'))
for obj in list(bpy.data.objects):
    if obj not in (armor,rig,armor.parent):bpy.data.objects.remove(obj,do_unlink=True)
spec=importlib.util.spec_from_file_location('hav_repair_hge',a.game_root/'ModTools/BlenderExport.py');hge=importlib.util.module_from_spec(spec);spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71',game='Zulu',appid='Jagged Alliance 3',mtl_prop_0_visible=True,mtl_prop_0_name='Unit',enable_colliders=True);hge.register()
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(entity+'.blend')))
with hge.ObjectNamesExportContext(bpy.context):
    bpy.ops.export_scene.fbx(filepath=str(a.output/(entity+'.fbx')),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY','ARMATURE'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
(a.output/'repair-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
