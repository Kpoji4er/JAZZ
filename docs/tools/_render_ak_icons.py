import bpy
from pathlib import Path
from mathutils import Vector
import argparse,sys
parser=argparse.ArgumentParser()
parser.add_argument('--build',type=Path,required=True)
parser.add_argument('--weapon',choices=['AK74','AKM','AK74M','AK105'],action='append')
args=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
out=args.build

for weapon in args.weapon or ['AK74','AKM','AK74M','AK105']:
    names=[weapon,weapon+'_Magazine']
    scene_name=weapon+'_JAZZ'
    bpy.ops.wm.open_mainfile(filepath=str(out/(scene_name+'.blend')))
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=48;s.render.resolution_x=512;s.render.resolution_y=256;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
    c=bpy.data.cameras.new('InventoryCamera');camera=bpy.data.objects.new(c.name,c);s.collection.objects.link(camera);c.type='ORTHO';s.camera=camera
    lights=[]
    for i,loc in enumerate([(-1,-.5,1.5),(-.5,.5,1),(1,1,0)]):
        d=bpy.data.lights.new('InventoryLight'+str(i),'AREA');d.energy=25;d.size=1.5
        o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o);lights.append((o,Vector(loc)))
    s.use_nodes=True;n=s.node_tree.nodes;n.clear();link=s.node_tree.links.new
    r=n.new('CompositorNodeRLayers');d=n.new('CompositorNodeDilateErode');d.mode='DISTANCE';d.distance=2;link(r.outputs['Alpha'],d.inputs[0])
    black=n.new('CompositorNodeSetAlpha');black.inputs['Image'].default_value=(.006,.005,.004,1);link(d.outputs[0],black.inputs['Alpha'])
    over=n.new('CompositorNodeAlphaOver');over.inputs[0].default_value=1;link(black.outputs[0],over.inputs[1]);link(r.outputs['Image'],over.inputs[2]);comp=n.new('CompositorNodeComposite');link(over.outputs[0],comp.inputs[0])
    for name in names:
        meshes=[o for o in s.objects if o.type=='MESH']
        for o in meshes:o.hide_render=(o.name.endswith('_StockFolded') or (name.endswith('_Magazine') and o.name!='AKR_'+name))
        component=name.endswith('_Magazine')
        s.render.resolution_x=100 if component else 512;s.render.resolution_y=100 if component else 256
        d.distance=1 if component else 2
        bpy.context.view_layer.update()
        points=[o.matrix_world@Vector(v) for o in meshes if not o.hide_render for v in o.bound_box]
        lo=Vector(tuple(min(p[i] for p in points) for i in range(3)));hi=Vector(tuple(max(p[i] for p in points) for i in range(3)));target=(lo+hi)/2
        c.ortho_scale=max(hi.y-lo.y,(hi.z-lo.z)*(1 if component else 2))*(1.25 if component else 1.1)
        camera.location=target+Vector((-2,.04,.25));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler()
        for light,offset in lights:light.location=target+offset;light.rotation_euler=(target-light.location).to_track_quat('-Z','Y').to_euler()
        s.render.filepath=str(out/(name+'_icon.png'));bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/(scene_name+'_icons.blend')))
