import bpy,bmesh,importlib.util,math,json,numpy as np
from pathlib import Path
from mathutils import Matrix,Vector
import argparse,sys
parser=argparse.ArgumentParser()
parser.add_argument('--build',type=Path,required=True)
parser.add_argument('--game-root',type=Path,required=True)
parser.add_argument('--assets',type=Path,default=Path(__file__).resolve().parents[2].parent/'jazz_assets')
parser.add_argument('--weapon',choices=['AK74','AKM','AK74M','AK105'],action='append')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=args.build
game=args.game_root
assets=args.assets

spec=importlib.util.spec_from_file_location('ak_hge',game/'ModTools/BlenderExport.py');hge=importlib.util.module_from_spec(spec);spec.loader.exec_module(hge)
hge.SETTINGS.update(version='71',game='Zulu',appid='Jagged Alliance 3',mtl_prop_0_visible=True,mtl_prop_0_name='Unit',enable_colliders=True);hge.register()
report={}
def separate(obj,name,predicate):
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
    for poly in obj.data.polygons:
        center=sum((obj.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices);poly.select=predicate(center)
    assert any(p.select for p in obj.data.polygons),name
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.separate(type='SELECTED');bpy.ops.object.mode_set(mode='OBJECT')
    new=next(o for o in bpy.context.selected_objects if o!=obj);new.name=name;return new
def join(objects,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    if len(objects)>1:bpy.ops.object.join()
    o=bpy.context.object;o.name=name;return o
def separate_islands(obj,name,predicate):
    """Select complete mesh islands; never cut through a magazine or grip face."""
    parent=list(range(len(obj.data.vertices)))
    def find(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]];i=parent[i]
        return i
    for edge in obj.data.edges:
        a,b=map(find,edge.vertices)
        if a!=b:parent[b]=a
    groups={}
    for vertex in obj.data.vertices:groups.setdefault(find(vertex.index),[]).append(vertex)
    selected=set()
    for vertices in groups.values():
        lo=Vector(tuple(min(v.co[i] for v in vertices) for i in range(3)))
        hi=Vector(tuple(max(v.co[i] for v in vertices) for i in range(3)))
        if predicate(lo,hi):selected.update(v.index for v in vertices)
    bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
    for vertex in obj.data.vertices:vertex.select=False
    for edge in obj.data.edges:edge.select=False
    for poly in obj.data.polygons:
        membership=[i in selected for i in poly.vertices]
        assert all(membership) or not any(membership),name
        poly.select=all(membership)
    assert any(p.select for p in obj.data.polygons),name
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.separate(type='SELECTED');bpy.ops.object.mode_set(mode='OBJECT')
    new=next(o for o in bpy.context.selected_objects if o!=obj);new.name=name;return new

for weapon in args.weapon or ['AK74','AKM','AK74M','AK105']:
    bpy.ops.wm.open_mainfile(filepath=str(out/(weapon+'_review.blend')))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    if weapon=='AK74':
        stock=bpy.data.objects['AK74_17'];hand=bpy.data.objects['AK74_20'];mag=bpy.data.objects['AK74_12'];core=[bpy.data.objects['AK74_10'],bpy.data.objects['AK74_14']]
        transform=Matrix.Translation(Vector((0,-.01845,.01678)))@Matrix.Scale(.9,4)
    elif weapon=='AKM':
        furniture=bpy.data.objects['AKM_0'];stock=separate(furniture,'Stock',lambda c:c.y>.04);hand=separate(furniture,'Handguard',lambda c:c.y<-.18);mag=bpy.data.objects['AKM_2'];core=[bpy.data.objects['AKM_1'],furniture]
        transform=Matrix.Translation(Vector((0,-.026,.00577)))@Matrix.Scale(.95,4)
    elif weapon=='AK74M':
        furniture=bpy.data.objects['AK74M_0']
        # Source islands form four spatially disjoint assemblies. The magazine
        # includes its feed lips and latch up to y=.0891, z=.0506; the former
        # face-centre cut removed both and also sliced through the pistol grip.
        mag=separate_islands(furniture,'Magazine',lambda lo,hi:lo.y>-.05 and hi.y<.10 and (hi.y>0 or hi.z<.02))
        stock=separate_islands(furniture,'Stock',lambda lo,hi:lo.y>.21)
        hand=separate_islands(furniture,'Handguard',lambda lo,hi:hi.y<0)
        core=[bpy.data.objects['AK74M_1'],furniture]
        transform=Matrix.Translation(Vector((0,-.14,.04)))
    else:
        stock=bpy.data.objects['AK105_0'];mag=bpy.data.objects['AK105_3'];body=bpy.data.objects['AK105_1']
        hand=separate_islands(body,'Handguard',lambda lo,hi:lo.y>=-.296 and hi.y<=-.1385)
        core=[body,bpy.data.objects['AK105_2']]
        transform=Matrix.Translation(Vector((0,-.025,0)))
    meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
    for o in meshes:o.data.transform(transform@o.matrix_world);o.matrix_world=Matrix.Identity(4)
    root=join(core,'AKR_'+weapon)
    for o in list(bpy.data.objects):
        if o.type!='MESH':bpy.data.objects.remove(o,do_unlink=True)
    def bounds(o):return [Vector(tuple(fn(v.co[i] for v in o.data.vertices) for i in range(3))) for fn in (min,max)]
    slo,shi=bounds(stock);mlo,mhi=bounds(mag);hlo,hhi=bounds(hand);rlo,rhi=bounds(root)
    magazine=Vector((0,(mlo.y+mhi.y)/2,mhi.z-.010))
    # Shared magazines use a feed-lip origin, not their geometric center.
    top=[v.co for v in mag.data.vertices if v.co.z>mhi.z-.025]
    magazine.y=sum(v.y for v in top)/len(top)
    if weapon=='AK74M':
        # Shared legacy AK magazines use the receiver interface, not the top
        # of the separately modelled cartridges in the source magazine.
        magazine=Vector((0,-.09,.06299))
    stockpivot=Vector((-.02,slo.y+.005,(slo.z+shi.z)/2))
    spots={'Stock':stockpivot,'Magazine':magazine,'Handguard':(hlo+hhi)/2,'Muzzle':Vector((0,rlo.y,rhi.z-.04)),
           'Hand_l_grip':Vector((0,(hlo.y+hhi.y)/2,hlo.z+.015)),'Trigger':Vector((0,-.045,.01)),
           'Scope':Vector((0,-.065,rhi.z+.01)),'Mount':Vector((0,-.065,rhi.z-.03)),
           'Under':Vector((0,hlo.y,hlo.z)),'Bipod':Vector((0,hlo.y,hlo.z)),
           'Side':Vector((-.025,(hlo.y+hhi.y)/2,(hlo.z+hhi.z)/2))}
    if weapon in ('AK74M','AK105'):
        # Native AK74M side rail: source x=.0159..0219, y=.0687..1883,
        # z=.0259..0478. Align AKSeriaMount's mounting plate to its centre;
        # retain the established Scope/General/Mount relationship of AK74.
        import xml.etree.ElementTree as ET
        ref={n.get('name'):Vector(tuple(map(float,n.get('spot_pos').split(',')))) for n in ET.parse(assets/'Entities/AK74.ent').findall('.//attach')}
        general=Vector((1.666,-.10,8.162)) if weapon=='AK74M' else Vector((1.35,-.109,4.897))
        for name in ('General','Scope','Mount'):
            q=general+ref[name]-ref['General']
            spots[name]=Vector((-q.y/100,-q.x/100,q.z/100))
        # GP fore-end ends at the rear of the front sight (49.19 cm).
        # Preserve donor clamp height relative to the bore (9.655 cm).
        spots['Under']=Vector((0,-.4179,.08961)) if weapon=='AK74M' else Vector((0,-.37,.04888))
        spots['Bipod']=Vector((0,-.38,.09132)) if weapon=='AK74M' else Vector((0,-.35,.05059))
    if weapon in ('AK74','AKM'):
        import xml.etree.ElementTree as ET
        reference=(assets/'Entities')/(weapon+'.ent')
        for node in ET.parse(reference).findall('.//attach'):
            x,y,z=map(float,node.attrib['spot_pos'].split(','));spots[node.attrib['name']]=Vector((-y/100,-x/100,z/100))
    else:
        front=[v.co for v in root.data.vertices if v.co.y<rlo.y+.008]
        spots['Muzzle']=Vector((0,rlo.y,sum(v.z for v in front)/len(front)))
    # Detach the native muzzle device so replacement attachments do not overlap it.
    muzzle_cut=rlo.y+(.025 if weapon=='AKM' else .05)
    muzzle=separate(root,'Muzzle',lambda c:c.y<muzzle_cut)
    front=[v.co for v in muzzle.data.vertices if v.co.y<rlo.y+.008]
    spots['Muzzle']=Vector((0,muzzle_cut,sum(v.z for v in front)/len(front)))
    entities={root.name:root,'AKR_'+weapon+'_Stock':stock,'AKR_'+weapon+'_Handguard':hand,'AKR_'+weapon+'_Magazine':mag,'AKR_'+weapon+'_Muzzle':muzzle}
    tex=out/weapon/'Textures';tex.mkdir(parents=True,exist_ok=True)
    materials={m for o in entities.values() for m in o.data.materials}
    for idx,mat in enumerate(sorted(materials,key=lambda m:m.name)):
        # Read the restored shader links, ensuring every map follows the correct UV atlas.
        bsdf=mat.node_tree.nodes.get('Principled BSDF');images={}
        for key,socket in [('Base','Base Color'),('Rough','Roughness'),('Metal','Metallic'),('Normal','Normal')]:
            links=bsdf.inputs[socket].links
            if not links:continue
            node=links[0].from_node
            if key=='Normal':node=node.inputs['Color'].links[0].from_node
            if node.type!='TEX_IMAGE':continue
            im=bpy.data.images.load(bpy.path.abspath(node.image.filepath),check_existing=False);im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color';im.scale(2048,2048)
            arr=np.empty(2048*2048*4,np.float32);im.pixels.foreach_get(arr);images[key]=arr.reshape(-1,4);bpy.data.images.remove(im)
        rm=np.ones((2048*2048,4),np.float32);rm[:,0]=images.get('Rough',rm)[:,0];rm[:,1]=0;rm[:,2]=images['Metal'][:,0] if 'Metal' in images else 0;images['RM']=rm
        paths={};mat.name=f'AKR_{weapon}_{idx}'
        for key in ['Base','Normal','RM']:
            if key not in images:continue
            im=bpy.data.images.new(mat.name+'_'+key,width=2048,height=2048,alpha=True);im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color';im.pixels.foreach_set(images[key].ravel());im.filepath_raw=str(tex/(im.name+'.tga'));im.file_format='TARGA_RAW';im.save();paths[key]=im.filepath_raw
        hge.add_material_props(mat)
        for prop in hge.MATERIAL_PROPERTIES:
            if prop.settings_name:
                key={'base_color':'Base','normal_map':'Normal','roughness_metallic_map':'RM'}.get(prop.settings_name)
                mat[prop.id]=paths[key] if key in paths else '' if prop.map else getattr(mat.hgm_settings,prop.settings_name)
    for name,o in entities.items():
        o.name=name;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
        tri=o.modifiers.new('Triangulate','TRIANGULATE');tri.keep_custom_normals=True;bpy.ops.object.modifier_apply(modifier=tri.name)
        pivot=spots[name.rsplit('_',1)[1]] if o!=root else Vector()
        origin=bpy.data.objects.new(name+'_Origin',None);bpy.context.collection.objects.link(origin);origin.location=pivot;o.data.transform(Matrix.Translation(-pivot));o.parent=origin;o.location=Vector()
        st=o.hge_obj_settings;st.entity=name;st.mesh='Mesh';st.state='idle';st.lod=1;st.ignore=False;o.hge_export=True
    folded=stock.copy();folded.data=stock.data.copy();folded.name='AKR_'+weapon+'_StockFolded';bpy.context.collection.objects.link(folded);folded.data.transform(Matrix.Rotation(math.pi,4,'Z'));folded.hge_obj_settings.entity=folded.name;folded.hide_render=True;entities[folded.name]=folded
    for name,point in spots.items():
        e=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(e);e.parent=root;e.location=point;e.hge_obj_settings.spot_name=name
    s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
    bpy.ops.wm.save_as_mainfile(filepath=str(out/(weapon+'_JAZZ.blend')))
    with hge.ObjectNamesExportContext(bpy.context):
        bpy.ops.export_scene.fbx(filepath=str(out/(weapon+'_JAZZ.fbx')),axis_forward='Y',axis_up='Z',apply_scale_options='FBX_SCALE_ALL',object_types={'MESH','EMPTY'},use_custom_props=True,add_leaf_bones=False,bake_anim=False)
    report[weapon]={'entities':list(entities),'spots':{n:list(p) for n,p in spots.items()}}
(out/'export-report.json').write_text(json.dumps(report,indent=2))
