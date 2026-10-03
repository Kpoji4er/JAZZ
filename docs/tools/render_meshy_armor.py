"""Blender background: -- --manifest batch.json [--name NAME]. Read-only GLB review."""
import argparse
import json
import sys
from pathlib import Path
import bpy
from mathutils import Vector

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--manifest',type=Path,required=True)
p.add_argument('--name')
p.add_argument('--interior',action='store_true',help='Add top and bottom views to inspect openings')
a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
batch=json.loads(a.manifest.read_text(encoding='utf-8'))
for job in batch['jobs']:
    if not job.get('model') or (a.name and job['name']!=a.name): continue
    root=Path(job['project'])
    if (root/'views-complete.json').exists() and (not a.interior or (root/'bottom.png').exists()): continue
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=job['model'])
    scene=bpy.context.scene
    meshes=[o for o in scene.objects if o.type=='MESH']
    pts=[o.matrix_world@Vector(v) for o in meshes for v in o.bound_box]
    low=Vector(tuple(min(v[i] for v in pts) for i in range(3)))
    high=Vector(tuple(max(v[i] for v in pts) for i in range(3)))
    center=(low+high)*.5;size=max(high-low)
    counts=[]
    for o in meshes:
        o.data.calc_loop_triangles()
        counts.append({'name':o.name,'vertices':len(o.data.vertices),'triangles':len(o.data.loop_triangles)})
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=16;scene.cycles.use_denoising=True
    scene.render.resolution_x=800;scene.render.resolution_y=800;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    scene.world=bpy.data.worlds.new('Studio');scene.world.use_nodes=True
    bg=scene.world.node_tree.nodes['Background'];bg.inputs['Color'].default_value=(.15,.17,.20,1);bg.inputs['Strength'].default_value=.7
    scene.view_settings.view_transform='AgX'
    for name,direction,power in [('Key',(2,-3,4),350),('Fill',(-3,-1,2),220),('Back',(1,3,3),350)]:
        ld=bpy.data.lights.new(name,'AREA');light=bpy.data.objects.new(name,ld);scene.collection.objects.link(light)
        light.location=center+Vector(direction)*size;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
        ld.energy=power*size*size;ld.shape='DISK';ld.size=size*3
    cd=bpy.data.cameras.new('Review');camera=bpy.data.objects.new('Review',cd);scene.collection.objects.link(camera);scene.camera=camera
    cd.type='ORTHO';cd.ortho_scale=size*1.3;cd.clip_end=size*100
    views=[('front',(0,-4,.15)),('back',(0,4,.15)),('side',(4,0,.15)),('oblique',(2.6,-4,1.2))]
    if a.interior: views += [('top',(0,-.3,4)),('bottom',(0,-.3,-4))]
    for view,direction in views:
        camera.location=center+Vector(direction)*size;camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler()
        scene.render.filepath=str(root/(view+'.png'));bpy.ops.render.render(write_still=True)
    report={'name':job['name'],'meshes':counts,'triangles':sum(o['triangles'] for o in counts),'rigged':any(o.type=='ARMATURE' for o in scene.objects),'views':[v[0] for v in views],'game_ready':False}
    (root/'views-complete.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('RENDERED '+job['name']+' '+str(report['triangles']),flush=True)
