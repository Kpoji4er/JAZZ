"""Blender scene with actual decoded attachments at installed entity spots.

Geometry-only references, colour coded for fit inspection. No active mod writes.
"""
import bpy,json,argparse,sys,xml.etree.ElementTree as ET
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser()
for key in ('build','reference','assets'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--reuse-renders',action='store_true')
p.add_argument('--config',action='append',choices=['GP30','GP45','Bipod30','PSO','Kobra','tyulpan','NSPU'])
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])

def material(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.7
    return m

def add_mesh(path,name,position,mat):
    data=json.loads(path.read_text());vertices=[];faces=[]
    for mesh in data['meshes']:
        if not mesh['vertices']:
            print('PARTIAL REFERENCE: skipping unsupported empty submesh in',path)
            continue
        assert all(0<=i<len(mesh['vertices']) for f in mesh['faces'] for i in f),(name,'invalid vertex indices')
        b=mesh['bbox'] or data['bbox'];center=[(b[i]+b[i+3])*.5 for i in range(3)];offset=len(vertices)
        for v in mesh['vertices']:
            x,y,z=[v[i]+center[i] for i in range(3)]
            vertices.append((-y,-x,z))
        faces.extend(tuple(i+offset for i in reversed(f)) for f in mesh['faces'])
    m=bpy.data.meshes.new(name);m.from_pydata(vertices,[],faces);m.update()
    o=bpy.data.objects.new(name,m);bpy.context.collection.objects.link(o);o.location=position;o.data.materials.append(mat)
    return o

for weapon in ('AK74M','AK105'):
    bpy.ops.wm.open_mainfile(filepath=str(a.build/(weapon+'_JAZZ.blend')))
    s=bpy.context.scene
    gray=material('Gun geometry',(.24,.28,.31));orange=material('Vanilla GP',(.75,.25,.045));blue=material('Vanilla bipod',(.07,.35,.7));green=material('Existing optic',(.2,.55,.16))
    for o in list(s.objects):
        if o.type=='MESH':
            o.hide_render=o.name.endswith('_StockFolded');o.data.materials.clear();o.data.materials.append(gray)
        elif o.type in ('LIGHT','CAMERA'):bpy.data.objects.remove(o,do_unlink=True)
    spots={}
    for n in ET.parse(a.assets/'Entities'/('AKR_'+weapon+'.ent')).findall('.//attach'):
        x,y,z=map(float,n.get('spot_pos').split(','));spots[n.get('name')]=Vector((-y/100,-x/100,z/100))
    gp=add_mesh(a.reference/'Geometry/WeaponAttA_GrenadeLauncherAK47_mesh.json','Vanilla GP at Under',spots['Under'],orange)
    bipod=add_mesh(a.reference/'Geometry/WeaponAttA_BipodAK47_mesh.json','Vanilla bipod at Bipod',spots['Bipod'],blue)
    mag45=add_mesh(a.reference/'CustomGeometry/AK74_Backelite_45.json','Shared magazine 45',spots['Magazine'],orange)
    mag30=bpy.data.objects['AKR_'+weapon+'_Magazine']
    optics={}
    for optic in ('PKAA','Kobra','tyulpan','NSPU','PSO'):
        path=a.reference/('Geometry/WeaponAttA_ScopeDragunov_01_mesh.json' if optic=='PSO' else 'CustomGeometry/'+optic+'.json')
        optics[optic]=add_mesh(path,optic+' at Scope',spots['Scope'],green)
    plate=add_mesh(a.reference/'CustomGeometry/AKSeriaMount.json','AK plate at General',spots['General'],green)
    for name,pos in spots.items():
        e=bpy.data.objects.new('Installed '+name,None);s.collection.objects.link(e);e.location=pos;e.empty_display_size=.008;e.show_name=True
    s.render.engine='CYCLES';s.cycles.samples=32;s.render.resolution_x=1400;s.render.resolution_y=650;s.render.resolution_percentage=100
    s.world=bpy.data.worlds.new('Fit neutral world');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.18,.18,.18,1)
    s.render.image_settings.file_format='PNG'
    camera_data=bpy.data.cameras.new('FitCamera');camera=bpy.data.objects.new('FitCamera',camera_data);s.collection.objects.link(camera);s.camera=camera;camera_data.type='ORTHO';camera_data.ortho_scale=1.05
    target=Vector((0,-.18,-.015))
    for i,pos in enumerate([(1,-.4,1),(-1,.1,.7)]):
        d=bpy.data.lights.new('Fit light '+str(i),'AREA');d.energy=70;d.size=1.2;o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(target-o.location).to_track_quat('-Z','Y').to_euler()
    for config in a.config or ('GP30','GP45','Bipod30','PSO','Kobra','tyulpan','NSPU'):
        gp.hide_render=config not in ('GP30','GP45');bipod.hide_render=config!='Bipod30'
        mag45.hide_render=config!='GP45';mag30.hide_render=config=='GP45'
        selected=config if config in optics else 'PKAA'
        for name,obj in optics.items():obj.hide_render=name!=selected
        plate.hide_render=selected in ('PSO','Kobra')
        bpy.context.view_layer.update()
        points=[o.matrix_world@Vector(v) for o in s.objects if o.type=='MESH' and not o.hide_render for v in o.bound_box]
        lo=Vector(tuple(min(v[i] for v in points) for i in range(3)));hi=Vector(tuple(max(v[i] for v in points) for i in range(3)))
        target=(lo+hi)/2
        camera_data.ortho_scale=max(hi.y-lo.y,(hi.z-lo.z)*1400/650)*1.10
        for side in (1,-1):
            camera.location=target+Vector((side*2,.04,.18));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
            s.render.filepath=str(a.reference/(weapon+'_'+config+('_left' if side==1 else '_right')+'_fit.png'))
            if not (a.reuse_renders and Path(s.render.filepath).exists()):bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(a.reference/(weapon+'_attachment_fit.blend')))
