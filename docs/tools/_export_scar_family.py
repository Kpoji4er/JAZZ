"""HGE export and icon renders from recovered, datum-aligned SCAR source.

--source SCAR-family-source.blend --build DIR --game-root DIR
Candidates only; compiled mesh audit is required before installation.
"""
import argparse,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Matrix,Vector
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _export_m14_family_assets import load_hge,assign_hge_maps
from _prepare_weapon_open_surfaces import prepare_export_mesh
from _ja3_mesh_prepare import triangulate_without_custom_normals
from _render_ak103_icon import build_compositor
p=argparse.ArgumentParser()
for k in ('source','build','game-root'):p.add_argument('--'+k,type=Path,required=True)
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
for folder in ('rigged','previews'):(a.build/folder).mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
hge=load_hge(a.game_root);created={};report={}
transform=Matrix(((0,.01,0,0),(-.01,0,0,.08),(0,0,.01,.13),(0,0,0,1)))
def load(family):
    with bpy.data.libraries.load(str(a.source),link=False) as (src,dst):dst.objects=[n for n in src.objects if n.startswith(family+'_')]
    result={}
    for o in dst.objects:
        if o.type!='MESH':continue
        bpy.context.scene.collection.objects.link(o);o.hide_render=False
        result[o.get('source_part')]=o
    return result
def clean(o):
    bm=bmesh.new();bm.from_mesh(o.data)
    bad=[f for f in bm.faces if f.calc_area()<1e-7]
    bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
    bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-5)
    bad=[f for f in bm.faces if f.calc_area()<1e-7]
    bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(o.data);bm.free()
    o.data.transform(transform)
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_area()<2e-8],context='FACES_ONLY')
    bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS')
    bm.to_mesh(o.data);bm.free()
    bpy.context.view_layer.objects.active=o;o.select_set(True)
    triangulate_without_custom_normals(o)
    issues=prepare_export_mesh(o,strict=False)
    if issues and all(i['kind']=='degenerate' for i in issues):
        assert len(issues)<10,(o.name,issues)
        bm=bmesh.new();bm.from_mesh(o.data);bm.faces.ensure_lookup_table()
        bmesh.ops.delete(bm,geom=[bm.faces[i] for i in sorted({r['triangle'] for r in issues})],context='FACES_ONLY')
        bm.to_mesh(o.data);bm.free()
        issues=prepare_export_mesh(o,strict=False)
    assert not issues,(o.name,issues[:4])
    bm=bmesh.new();bm.from_mesh(o.data)
    bmesh.ops.split_edges(bm,edges=[e for e in bm.edges if len(e.link_faces)==2 and e.calc_face_angle(0)>math.radians(60)])
    bm.to_mesh(o.data);bm.free()
    for poly in o.data.polygons:poly.use_smooth=True
def adopt(objects,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:clean(o);o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    if len(objects)>1:bpy.ops.object.join()
    o=objects[0];o.name=name;created[name]=o;return o

for family in ('H','L','SSR'):
    for length in (('SSR',) if family=='SSR' else ('Short','Standard','Long')):
        parts=load(family)
        delta={'Short':-10.16,'Standard':0,'Long':10.16,'SSR':10.16}[length]
        # Change only the straight exposed barrel span; receiver, gas block,
        # chamber and every mount remain fixed. Translate the muzzle as a unit.
        common=parts['Common'];end=max(v.co.x for v in common.data.vertices);start=47
        for v in common.data.vertices:
            if v.co.x>start:v.co.x+=delta*(v.co.x-start)/(end-start)
        for v in parts['Muzzle'].data.vertices:v.co.x+=delta
        if family=='SSR':
            bm=bmesh.new();bm.from_mesh(common.data)
            bmesh.ops.delete(bm,geom=[f for f in bm.faces if all(v.co.x>40 and v.co.z>-2 for v in f.verts)],context='FACES_ONLY')
            bm.to_mesh(common.data);bm.free()
        body_parts=[parts[k] for k in ('Upper','Common','Lower','RearSight')]
        if family=='SSR':body_parts.append(parts['StockPlate'])
        name='JAZZ_SCAR_SSR' if family=='SSR' else f'JAZZ_SCAR_{family}_{length}'
        adopt(body_parts,name)
        if length=='Standard':adopt([parts['Muzzle']],f'JAZZ_SCAR_{family}_Muzzle')
        else:bpy.data.objects.remove(parts['Muzzle'],do_unlink=True)
        if length=='Standard':adopt([parts['Magazine']],f'JAZZ_SCAR_{family}_Magazine')
        else:bpy.data.objects.remove(parts['Magazine'],do_unlink=True)
        if family=='H' and length=='Standard':adopt([parts['Stock']],'JAZZ_SCAR_Stock')
        elif family=='SSR':adopt([parts['Stock']],'JAZZ_SCAR_StockSSR')
        else:bpy.data.objects.remove(parts['Stock'],do_unlink=True)

stock=created['JAZZ_SCAR_Stock'];fold=stock.copy();fold.data=stock.data.copy();bpy.context.scene.collection.objects.link(fold)
fold.name='JAZZ_SCAR_StockFolded';created[fold.name]=fold
hinge=transform@Vector((0,3.1,-4.5))
fold.data.transform(Matrix.Translation(hinge)@Matrix.Rotation(math.pi,4,'Z')@Matrix.Translation(-hinge))
converted={}
for name,o in created.items():
    for index,m in enumerate(o.data.materials):
        prefix=m.name.split('.')[0]
        if prefix in converted:o.data.materials[index]=converted[prefix];continue
        imgs={}
        for n in m.node_tree.nodes:
            if n.type=='TEX_IMAGE' and n.image:
                stem=Path(n.image.filepath).stem
                for key,suffix in [('Base','BaseColor'),('Normal','Normal'),('RM','RM')]:
                    if stem.endswith('_'+suffix):imgs[key]=n.image
        assert len(imgs)==3,(prefix,imgs)
        assign_hge_maps(hge,m,imgs);converted[prefix]=m
    assert not o.data.has_custom_normals
    origin=bpy.data.objects.new(name+'_Origin',None);bpy.context.scene.collection.objects.link(origin);o.parent=origin
    st=o.hge_obj_settings;st.entity=name;st.mesh='Mesh';st.state='idle';st.lod=1;st.ignore=False;o.hge_export=True
    if name.endswith(('Short','Standard','Long')) or name=='JAZZ_SCAR_SSR':
        muzzle=min(v.co.y for v in o.data.vertices)
        spots={'Magazine':(0,0,0),'Stock':(0,0,0),'Barrel':(0,0,0),'Scope':(0,-.08,.131),
               'Under':(0,-.26,.039),'Side':(-.030,-.26,.085),'Muzzle':(0,0,0),
               'MuzzleTip':(.0036,muzzle,.0835),'Trigger':(0,0,.008),'Hand_l_grip':(0,-.22,.045)}
        for label,pos in spots.items():
            spot=bpy.data.objects.new(label,None);bpy.context.scene.collection.objects.link(spot);spot.parent=o;spot.location=pos;spot.hge_obj_settings.spot_name=label
    bpy.ops.object.select_all(action='DESELECT');o.select_set(True);origin.select_set(True)
    for c in o.children:c.select_set(True)
    export_path=a.build/'rigged'/(name+'.fbx')
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(export_path),use_selection=True,axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
    report[name]={'triangles':len(o.data.polygons),'custom_normals':False}
bpy.ops.wm.save_as_mainfile(filepath=str(a.build/'rigged/SCAR_JA3.blend'))
(a.build/'build-report.json').write_text(json.dumps(report,indent=2))
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE_NEXT';s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard'
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[1].default_value=.65
for name,loc,power in [('Key',(-2,-1,3),700),('Fill',(2,0,1),400)]:
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.size=3;ob=bpy.data.objects.new(name,ld);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(-ob.location).to_track_quat('-Z','Y').to_euler()
c=bpy.data.cameras.new('Camera');c.type='ORTHO';c.ortho_scale=1.2
cam=bpy.data.objects.new('Camera',c);s.collection.objects.link(cam);s.camera=cam
target=Vector((0,-.12,.05));cam.location=target+Vector((-2,0,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
build_compositor(s);s.render.resolution_x=324;s.render.resolution_y=165;s.render.resolution_percentage=100
for family in ('L','H','SSR'):
    for length in (('',) if family=='SSR' else ('Short','Standard','Long')):
        for folded in ((False,) if family=='SSR' else (False,True)):
            base='SCAR_SSR' if family=='SSR' else f'SCAR_{family}_{length}'
            stock='StockSSR' if family=='SSR' else 'StockFolded' if folded else 'Stock'
            names={'JAZZ_'+base,'JAZZ_SCAR_'+('L' if family=='L' else 'H')+'_Magazine','JAZZ_SCAR_'+stock,'JAZZ_SCAR_'+('L' if family=='L' else 'H')+'_Muzzle'}
            for fam in ('L','H'):
                created['JAZZ_SCAR_'+fam+'_Muzzle'].location.y=-({'Short':-.1016,'Long':.1016}.get(length,0) if family!='SSR' else .1016)
            for name,o in created.items():o.hide_render=name not in names
            points=[o.matrix_world@v.co for name,o in created.items() if name in names for v in o.data.vertices]
            target=Vector((0,(min(v.y for v in points)+max(v.y for v in points))/2,(min(v.z for v in points)+max(v.z for v in points))/2))
            c.ortho_scale=(max(v.y for v in points)-min(v.y for v in points))*1.18
            cam.location=target+Vector((-2,0,0));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
            s.render.filepath=str(a.build/'previews'/(base+('_Folded' if folded else '')+'.png'));bpy.ops.render.render(write_still=True)
print('SCAR_EXPORT',len(created))
