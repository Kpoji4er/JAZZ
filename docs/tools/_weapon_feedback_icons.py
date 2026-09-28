"""Blender: assemble exact entity-local parts at installed spots and render icons.

--config JSON --assets DIR --maps DIR --output DIR [--only LABEL]
Config names source blend/entity and parent/spot per part. No active-mod writes.
Writes 324x165 icons, 1200px reviews and a source/placement manifest.
"""
import argparse,json,math,sys
from pathlib import Path
import xml.etree.ElementTree as ET
import bpy
from mathutils import Vector,Matrix
sys.path.insert(0,str(Path(__file__).resolve().parent))
from _render_ak103_icon import build_compositor
p=argparse.ArgumentParser()
for key in ('config','assets','maps','output'):p.add_argument('--'+key,type=Path,required=True)
p.add_argument('--only');p.add_argument('--series-light',action='store_true',help='Common lighting; zero display exposure preserves dark outline')
p.add_argument('--component',action='store_true',help='100x100 component icon rendered from exact model')
p.add_argument('--oblique',action='store_true',help='Opposite oblique fit review; do not install as inventory icons')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);a.output.mkdir(parents=True,exist_ok=True)
configs=json.loads(a.config.read_text());report={}
for label,parts in configs.items():
    if a.only and a.only!=label:continue
    bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;objects={};placement=[]
    for part in parts:
        name=part['entity']
        if part.get('geometry'):
            data=json.loads(Path(part['geometry']).read_text());verts=[];faces=[]
            for mesh in data['meshes']:
                assert mesh['vertices'],name
                box=mesh['bbox'] or data['bbox'];center=Vector(tuple((box[i]+box[i+3])/2 for i in range(3)));offset=len(verts)
                for v in mesh['vertices']:
                    x,y,z=Vector(v)+center;verts.append((-y,-x,z))
                faces.extend(tuple(offset+i for i in reversed(f)) for f in mesh['faces'])
            mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);obj=bpy.data.objects.new(name,mesh)
        else:
            with bpy.data.libraries.load(part['blend'],link=False) as (src,dst):
                assert name in src.objects,(label,name,part['blend']);dst.objects=[name]
            obj=dst.objects[0]
        sc.collection.objects.link(obj);obj.parent=None;obj.matrix_world=Matrix.Identity(4)
        if part.get('parent'):
            parent=part['parent'];ent=ET.parse(a.assets/'Entities'/(parent+'.ent'))
            spot=next(n for n in ent.findall('.//attach') if n.get('name')==part['spot'])
            x,y,z=[float(v)/100 for v in spot.get('spot_pos').split(',')]
            obj.location=objects[parent].location+Vector((-y,-x,z))
            rot=list(map(float,spot.get('spot_rot','0,0,1,0').split(',')))
            if abs(rot[3])>=.001:
                obj.rotation_euler=Matrix.Rotation(math.radians(rot[3]),4,Vector((rot[1],rot[0],-rot[2]))).to_euler()
        obj.hide_render=False;objects[name]=obj
        mat=bpy.data.materials.new(name+'_Installed');mat.use_nodes=True
        nodes=mat.node_tree.nodes;links=mat.node_tree.links;bs=nodes.get('Principled BSDF')
        if part.get('geometry'):
            bs.inputs['Base Color'].default_value=(*part.get('color',(.025,.028,.03)),1)
            bs.inputs['Metallic'].default_value=.6;bs.inputs['Roughness'].default_value=.55
        for key in ('Base','Normal','RM'):
            path=a.maps/(name+'_'+key+'.png')
            if not path.exists():continue
            im=bpy.data.images.load(str(path));im.colorspace_settings.name='sRGB' if key=='Base' else 'Non-Color'
            tex=nodes.new('ShaderNodeTexImage');tex.image=im
            if key=='Base':links.new(tex.outputs['Color'],bs.inputs['Base Color'])
            elif key=='Normal':
                nm=nodes.new('ShaderNodeNormalMap');links.new(tex.outputs['Color'],nm.inputs['Color']);links.new(nm.outputs['Normal'],bs.inputs['Normal'])
            else:
                sep=nodes.new('ShaderNodeSeparateColor');links.new(tex.outputs['Color'],sep.inputs[0]);links.new(sep.outputs[0],bs.inputs['Roughness']);links.new(sep.outputs[2],bs.inputs['Metallic'])
        obj.data.materials.clear();obj.data.materials.append(mat)
        for poly in obj.data.polygons:poly.material_index=0
        for slot in obj.material_slots:slot.link='DATA';slot.material=mat
        placement.append({'entity':name,'source':part.get('blend',part.get('geometry')),'position_m':list(obj.location)})
    bpy.context.view_layer.update()
    points=[o.matrix_world@Vector(v) for o in objects.values() for v in o.bound_box]
    lo=Vector(tuple(min(v[i] for v in points) for i in range(3)));hi=Vector(tuple(max(v[i] for v in points) for i in range(3)));center=(lo+hi)/2
    sc.render.engine='CYCLES';sc.cycles.samples=32;sc.render.film_transparent=True
    sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA'
    sc.view_settings.view_transform='AgX'
    sc.world=bpy.data.worlds.new('World');sc.world.use_nodes=True;sc.world.node_tree.nodes['Background'].inputs[1].default_value=.3
    camera=bpy.data.objects.new('Camera',bpy.data.cameras.new('Camera'));sc.collection.objects.link(camera);sc.camera=camera
    width,height=(100,100) if a.component else (324,165)
    camera.data.type='ORTHO';camera.data.ortho_scale=max((hi-lo).y*1.1,(hi-lo).z*width/height*1.1)
    if label.startswith('M4A1'):
        # A common camera is essential: independent auto-fit hides barrel length.
        center=Vector((0,-.15,.04));camera.data.ortho_scale=1.15
    camera.location=center+Vector((2,.6,.3) if a.oblique else (-2,0,0));camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
    for pos,power in [((-1,-.5,1.5),35),((-.5,.5,1),25),((1,1,0),25)]:
        light=bpy.data.lights.new('Light','AREA');light.energy=power;light.size=1.5
        ob=bpy.data.objects.new('Light',light);sc.collection.objects.link(ob);ob.location=center+Vector(pos);ob.rotation_euler=(center-ob.location).to_track_quat('-Z','Y').to_euler()
    sc.render.resolution_x=1200;sc.render.resolution_y=611;sc.render.resolution_percentage=100
    sc.render.filepath=str(a.output/(label+'-review.png'));bpy.ops.render.render(write_still=True)
    # Inventory lighting needs readable metal on the dark slot background.
    sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
    if a.series_light:
        # Exposure after compositing also lightened the outline differently per weapon.
        # Raise physical light intensity instead, identically for the whole series.
        sc.view_settings.exposure=0
        for light in bpy.data.lights:light.energy*=2
        sc.world.node_tree.nodes['Background'].inputs[1].default_value*=2
    else:
        sc.view_settings.exposure=2.0 if label.startswith('M4A1') else (1.4 if label=='AK103' else 1.0)
    if not label.startswith('M4A1'):camera.data.ortho_scale*=1.20/1.10
    build_compositor(sc);sc.render.resolution_x=width;sc.render.resolution_y=height
    sc.render.filepath=str(a.output/(label+'.png'));bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(a.output/(label+'.blend')))
    report[label]={'parts':placement,'length_m':float((hi-lo).y),'height_m':float((hi-lo).z)}
    print('ICON_READY',label,flush=True)
(a.output/('icons-report'+('-'+a.only if a.only else '')+'.json')).write_text(json.dumps(report,indent=2))
