"""Split restored HAV into connected islands and preserve UV/materials for variants."""
import argparse
import json
import sys
from pathlib import Path
import bpy
from mathutils import Vector

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--audit-only', action='store_true')
p.add_argument('--body', type=Path, help='Calibrated HGM JSON for rest fit only')
a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
a.output.mkdir(parents=True, exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(a.source))
originals = [o for o in bpy.context.scene.objects if o.type == 'MESH']
for obj in originals:
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.mode_set(mode='OBJECT')
report = []
for obj in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    pts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    lo = [min(v[k] for v in pts) for k in range(3)]
    hi = [max(v[k] for v in pts) for k in range(3)]
    center = [(x+y)/2 for x,y in zip(lo,hi)]
    x,y,z = center
    role = obj.get('source_role')
    if role == 'limb_neck_groin_protection':
        if z < .5:
            role = 'shins'
        elif z < .75:
            role = 'thighs'
        elif z < 1.1:
            role = 'groin' if abs(x) < .1 else 'thighs'
        elif abs(x) < .15:
            role = 'collar'
        else:
            role = 'arms'
    obj['armor_part'] = role
    report.append(dict(name=obj.name, source=obj.get('source_role'), vertices=len(pts),
                       bounds=[lo,hi], center=center, part=role))
(a.output/'islands.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'modular-source.blend'))
if a.audit_only:
    print('Audited',len(report),'islands')
    sys.exit(0)
parts = {}
for role in sorted({r['part'] for r in report}):
    objects = [o for o in bpy.context.scene.objects if o.type=='MESH' and o.get('armor_part')==role]
    bpy.ops.object.select_all(action='DESELECT')
    for o in objects:o.select_set(True)
    bpy.context.view_layer.objects.active=objects[0]
    bpy.ops.object.join()
    obj=bpy.context.object;obj.name='HAV_'+role;parts[role]=obj
    obj.data.calc_loop_triangles()
variants = {'Light':['vest'], 'Medium':['vest','belt','collar','groin'],
            'Full':['vest','belt','collar','groin','arms'],
            'Legs':['thighs'], 'HeavyLegs':['thighs','shins']}
manifest={'status':'SOURCE_ONLY', 'geometry_shared_by':['Twaron','Guardian','Zylon'],
          'material_status':'original olive only; Guardian and Zylon pending',
          'runtime':'NOT_INSTALLED', 'variants':{}}
scene=bpy.context.scene
scene.cycles.device='CPU';scene.cycles.samples=24
scene.render.resolution_x=600;scene.render.resolution_y=800
for variant,roles in variants.items():
    for role,obj in parts.items():obj.hide_render=role not in roles
    target=Vector((0,0,1.3 if variant in ('Light','Medium','Full') else .65))
    scene.camera.location=(1,-3,1.9 if variant in ('Light','Medium','Full') else 1.0)
    scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
    scene.camera.data.ortho_scale=1.8 if variant=='Full' else 1.15
    if variant=='Legs':
        target=Vector((0,0,.81));scene.camera.rotation_euler=(target-scene.camera.location).to_track_quat('-Z','Y').to_euler()
        scene.camera.data.ortho_scale=.75
    scene.render.filepath=str(a.output/(variant+'.png'));bpy.ops.render.render(write_still=True)
    manifest['variants'][variant]={'parts':roles, 'triangles':sum(len(parts[r].data.loop_triangles) for r in roles)}
for obj in parts.values():obj.hide_render=False
if a.body:
    data=json.loads(a.body.read_text(encoding='utf-8'))
    mat=bpy.data.materials.new('Actual Legion shirt - geometry reference');mat.use_nodes=True
    mat.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.25,.04,.025,1)
    for k,m in enumerate(data['meshes']):
        box=m['bbox'] or data['bbox'];c=[(box[i]+box[i+3])/2 for i in range(3)]
        verts=[(-(v[1]+c[1]),-(v[0]+c[0]),v[2]+c[2]) for v in m['vertices']]
        mesh=bpy.data.meshes.new('Legion shirt '+str(k));mesh.from_pydata(verts,[],[tuple(reversed(f)) for f in m['faces']]);mesh.update()
        obj=bpy.data.objects.new(mesh.name,mesh);bpy.context.collection.objects.link(obj);mesh.materials.append(mat)
        for face in mesh.polygons:face.use_smooth=True
    for role,obj in parts.items():obj.hide_render=role not in variants['Light']
    for side,loc in [('front',(1,-3,1.9)),('back',(-1,3,1.9))]:
        scene.camera.location=loc
        scene.camera.rotation_euler=(Vector((0,0,1.27))-scene.camera.location).to_track_quat('-Z','Y').to_euler()
        scene.camera.data.ortho_scale=1.5
        scene.render.filepath=str(a.output/('initial-fit-'+side+'.png'));bpy.ops.render.render(write_still=True)
    manifest['fit']={'body':a.body.stem,'status':'UNADJUSTED_REST_REFERENCE; no rig or animation validation'}
bpy.ops.wm.save_as_mainfile(filepath=str(a.output/'modular-source.blend'))
(a.output/'variants.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest))
